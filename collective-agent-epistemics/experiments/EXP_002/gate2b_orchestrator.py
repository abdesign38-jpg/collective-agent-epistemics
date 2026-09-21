"""Gate 2B execution/archive orchestration layer.

This module executes worlds frozen in GATE_2B_WORLD_MANIFEST_v0.1.json using the
unmodified EXP-002 v0.1 runtime, then archives the transient outputs immutably.
It performs no scientific analysis, changes no seeds/order, and does not modify
run.py, world_generator.py, lineage.py, metrics.py, models.py, prompting.py,
adapters/, prompts/, or tests/.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .adapters.base import AgentAdapter
from .adapters.deterministic_stub import DeterministicStubAdapter
from .adapters.openai_responses import OpenAIAdapterConfig, OpenAIResponsesAdapter
from .run import RESULTS, run_experiment, write_results
from .world_generator import generate_world

HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "GATE_2B_WORLD_MANIFEST_v0.1.json"
DEFAULT_ARCHIVE_ROOT = HERE / "results" / "archive" / "gate_2b"
TRANSIENT_FILES = ("events.jsonl", "summary.csv", "run_metadata.json")
REQUIRED_CALLS = 25
REQUIRED_REUSED = 4
REQUIRED_CONDITIONS = {"free", "lineage", "macro"}


class Gate2BIntegrityError(RuntimeError):
    """Raised on a configuration/file inconsistency; never on a scientific outcome."""


@dataclass(frozen=True)
class WorldTask:
    set_key: str
    canonical_world_id: str
    seed: int
    truth: str
    observed_state: str
    evidence_alignment: str
    sensor_reliability: float
    evidence_root: str
    execution_order: int


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_world_tasks(manifest: dict[str, Any], sets: tuple[str, ...]) -> list[WorldTask]:
    tasks: list[WorldTask] = []
    for set_key in sets:
        for world in manifest[set_key]["worlds"]:
            tasks.append(
                WorldTask(
                    set_key=set_key,
                    canonical_world_id=world["canonical_world_id"],
                    seed=world["seed"],
                    truth=world["truth"],
                    observed_state=world["observed_state"],
                    evidence_alignment=world["evidence_alignment"],
                    sensor_reliability=world["sensor_reliability"],
                    evidence_root=world["evidence_root"],
                    execution_order=world["execution_order"],
                )
            )
    tasks.sort(key=lambda t: (t.set_key, t.execution_order))
    return tasks


def verify_world_reproducibility(task: WorldTask) -> None:
    world = generate_world(task.seed)
    evidence = world.evidence[0]
    alignment = "aligned" if evidence.observed_state == world.truth else "misleading"
    mismatches = [
        label
        for label, actual, expected in (
            ("truth", world.truth, task.truth),
            ("observed_state", evidence.observed_state, task.observed_state),
            ("reliability", round(evidence.reliability, 6), round(task.sensor_reliability, 6)),
            ("evidence_root", evidence.evidence_id, task.evidence_root),
            ("alignment", alignment, task.evidence_alignment),
        )
        if actual != expected
    ]
    if mismatches:
        raise Gate2BIntegrityError(
            f"{task.canonical_world_id}: world reproducibility mismatch in {mismatches}"
        )


def clear_transient_outputs() -> None:
    for name in TRANSIENT_FILES:
        path = RESULTS / name
        if path.exists():
            path.unlink()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def archive_destination(archive_root: Path, task: WorldTask, attempt: int = 1) -> Path:
    return archive_root / task.set_key / task.canonical_world_id / f"attempt_{attempt:03d}"


def read_summary_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def git_last_commit_for(path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", path.name],
            cwd=path.resolve().parent,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip() or None
    except Exception:
        return None


def validate_execution(experiment, summary_rows: list[dict[str, str]], task: WorldTask, expected: dict[str, Any]) -> None:
    metadata = experiment.execution_metadata
    checks = [
        (metadata.get("actual_model_call_count") == REQUIRED_CALLS, f"actual_model_call_count={metadata.get('actual_model_call_count')}"),
        (metadata.get("reused_response_count") == REQUIRED_REUSED, f"reused_response_count={metadata.get('reused_response_count')}"),
        ({row["condition"] for row in summary_rows} == REQUIRED_CONDITIONS, f"conditions={sorted(row['condition'] for row in summary_rows)}"),
        (all(row["truth"] == task.truth for row in summary_rows), "summary truth mismatch"),
        (experiment.execution_policy == "paired", f"execution_policy={experiment.execution_policy}"),
        (experiment.rounds == expected["rounds"], f"rounds={experiment.rounds}"),
        (experiment.seed == task.seed, f"experiment.seed={experiment.seed}"),
    ]
    if expected.get("model") is not None:
        checks.append((experiment.adapter_metadata.get("requested_model") == expected["model"], "requested_model mismatch"))
    if expected.get("reasoning_effort") is not None:
        checks.append((experiment.adapter_metadata.get("reasoning_effort") == expected["reasoning_effort"], "reasoning_effort mismatch"))
    failures = [detail for ok, detail in checks if not ok]
    if failures:
        raise Gate2BIntegrityError(f"{task.canonical_world_id}: integrity check failed: {failures}")


def run_and_archive_world(
    task: WorldTask,
    *,
    adapter_factory: Callable[[], AgentAdapter],
    adapter_name: str,
    adapter_metadata: dict[str, Any],
    run_class: str,
    rounds: int,
    archive_root: Path,
    manifest_path: Path,
    expected: dict[str, Any],
) -> Path:
    verify_world_reproducibility(task)

    dest = archive_destination(archive_root, task)
    present = [name for name in TRANSIENT_FILES if (dest / name).exists()]
    if len(present) == len(TRANSIENT_FILES):
        return dest  # already archived; immutable, do not re-execute
    if present:
        raise Gate2BIntegrityError(
            f"{task.canonical_world_id}: partial archive at {dest} ({present}); manual review required, no auto-retry"
        )

    clear_transient_outputs()
    experiment = run_experiment(
        trials=1,
        rounds=rounds,
        seed=task.seed,
        adapter_factory=adapter_factory,
        adapter_name=adapter_name,
        adapter_metadata=adapter_metadata,
        run_class=run_class,
        execution_policy="paired",
    )
    write_results(experiment)

    summary_rows = read_summary_rows(RESULTS / "summary.csv")
    validate_execution(experiment, summary_rows, task, expected)

    pre_hashes = {name: sha256_file(RESULTS / name) for name in TRANSIENT_FILES}
    dest.mkdir(parents=True, exist_ok=False)
    for name in TRANSIENT_FILES:
        shutil.copy2(RESULTS / name, dest / name)
    post_hashes = {name: sha256_file(dest / name) for name in TRANSIENT_FILES}
    if pre_hashes != post_hashes:
        raise Gate2BIntegrityError(f"{task.canonical_world_id}: archive copy hash mismatch")

    archive_metadata = {
        "gate": "2B",
        "set": task.set_key,
        "canonical_world_id": task.canonical_world_id,
        "seed": task.seed,
        "attempt": 1,
        "manifest_path": str(manifest_path),
        "manifest_sha256": sha256_file(manifest_path),
        "manifest_last_commit": git_last_commit_for(manifest_path),
        "frozen_runtime": expected["frozen_runtime"],
        "protocol_tag": expected["protocol_tag"],
        "plan_freeze_commit": expected.get("plan_freeze_commit"),
        "runtime_emitted_world_id": summary_rows[0]["world_id"],
        "manifest_internal_world_id_note": (
            "manifest internal_world_id uses EXP_002_W_<seed>; the frozen runner "
            "emits EXP_002_W01 for trials=1. truth/observed_state are identical "
            "because both derive from the same seed."
        ),
        "raw_file_sha256": post_hashes,
        "adapter_name": adapter_name,
        "execution_policy": "paired",
        "rounds": rounds,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "technical_integrity_status": "pass",
    }
    (dest / "archive_metadata.json").write_text(json.dumps(archive_metadata, indent=2) + "\n", encoding="utf-8")
    return dest


def run_campaign(
    tasks: list[WorldTask],
    *,
    adapter_factory: Callable[[], AgentAdapter],
    adapter_name: str,
    adapter_metadata: dict[str, Any],
    run_class: str,
    rounds: int,
    archive_root: Path,
    manifest_path: Path,
    expected: dict[str, Any],
) -> list[Path]:
    destinations: list[Path] = []
    for task in tasks:
        dest = run_and_archive_world(
            task,
            adapter_factory=adapter_factory,
            adapter_name=adapter_name,
            adapter_metadata=adapter_metadata,
            run_class=run_class,
            rounds=rounds,
            archive_root=archive_root,
            manifest_path=manifest_path,
            expected=expected,
        )
        destinations.append(dest)
        print(f"[{task.set_key}] order={task.execution_order} {task.canonical_world_id} -> {dest}")
    return destinations


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gate 2B execution/archive orchestrator (does not modify the frozen EXP-002 runtime)"
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--sets", default="generalization_set_001,stress_set_001")
    parser.add_argument("--adapter", choices=("deterministic_stub", "openai"), default="deterministic_stub")
    parser.add_argument("--model", default=None)
    parser.add_argument("--reasoning-effort", default=None)
    parser.add_argument("--rounds", type=int, default=4)
    parser.add_argument("--archive-root", type=Path, default=DEFAULT_ARCHIVE_ROOT)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()

    if args.adapter == "openai" and not args.live:
        raise SystemExit("--adapter openai requires --live; no network call made")
    if args.adapter == "deterministic_stub" and args.live:
        raise SystemExit("--live is only valid with --adapter openai")

    manifest = load_manifest(args.manifest)
    sets = tuple(s.strip() for s in args.sets.split(",") if s.strip())
    tasks = manifest_world_tasks(manifest, sets)

    if args.adapter == "openai":
        config = OpenAIAdapterConfig.from_environment(model=args.model, reasoning_effort=args.reasoning_effort)
        adapter_factory: Callable[[], AgentAdapter] = lambda: OpenAIResponsesAdapter(config)
        adapter_name = "openai"
        adapter_metadata = config.metadata()
        run_class = "gate_2b_real_model"
    else:
        adapter_factory = DeterministicStubAdapter
        adapter_name = "deterministic_stub"
        adapter_metadata = {"provider": "local"}
        run_class = "gate_2b_preflight"

    expected = {
        "rounds": args.rounds,
        "model": args.model,
        "reasoning_effort": args.reasoning_effort,
        "frozen_runtime": manifest["anchors"]["frozen_runtime"],
        "protocol_tag": manifest["anchors"]["protocol_tag"],
        "plan_freeze_commit": manifest["anchors"].get("plan_freeze_commit"),
    }

    print(f"Gate 2B orchestrator: {len(tasks)} worlds queued across {sets} (adapter={adapter_name})")
    run_campaign(
        tasks,
        adapter_factory=adapter_factory,
        adapter_name=adapter_name,
        adapter_metadata=adapter_metadata,
        run_class=run_class,
        rounds=args.rounds,
        archive_root=args.archive_root,
        manifest_path=args.manifest,
        expected=expected,
    )


if __name__ == "__main__":
    main()
