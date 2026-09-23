"""Gate 2B execution/archive orchestration layer.

This module executes worlds frozen in GATE_2B_WORLD_MANIFEST_v0.1.json using the
unmodified EXP-002 v0.1 runtime, then archives the transient outputs immutably.
It performs no scientific analysis, changes no seeds/order, and does not modify
run.py, world_generator.py, lineage.py, metrics.py, models.py, prompting.py,
adapters/, prompts/, or tests/.

World membership always comes exclusively from the world manifest; frozen
execution configuration (model/reasoning_effort/rounds/execution_policy) always
comes exclusively from GATE_2B_PLAN_v0.1.json, never from user-supplied values
compared against themselves.
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
PROJECT_ROOT = HERE.parent.parent
DEFAULT_PLAN = HERE / "GATE_2B_PLAN_v0.1.json"
DEFAULT_MANIFEST = HERE / "GATE_2B_WORLD_MANIFEST_v0.1.json"
DEFAULT_ARCHIVE_ROOT = HERE / "results" / "archive" / "gate_2b"
CANONICAL_PLAN_COMMIT = "ecbcbc77d0832b82ea9da2abc3d800db759c238c"
CANONICAL_MANIFEST_COMMIT = "1cd749c0cb8f04d64d7581d44364c8875e9799a2"
CANONICAL_PLAN_RELATIVE_PATH = "experiments/EXP_002/GATE_2B_PLAN_v0.1.json"
CANONICAL_MANIFEST_RELATIVE_PATH = "experiments/EXP_002/GATE_2B_WORLD_MANIFEST_v0.1.json"
TRANSIENT_FILES = ("events.jsonl", "summary.csv", "run_metadata.json")
REQUIRED_CALLS = 25
REQUIRED_REUSED = 4
REQUIRED_CONDITIONS = {"free", "lineage", "macro"}

# Files whose bytes must be identical to the frozen runtime commit before any
# provider call is made. Paths are relative to PROJECT_ROOT.
FROZEN_RUNTIME_PATHS = (
    "experiments/EXP_002/run.py",
    "experiments/EXP_002/world_generator.py",
    "experiments/EXP_002/lineage.py",
    "experiments/EXP_002/metrics.py",
    "experiments/EXP_002/models.py",
    "experiments/EXP_002/prompting.py",
    "experiments/EXP_002/adapters/base.py",
    "experiments/EXP_002/adapters/deterministic_stub.py",
    "experiments/EXP_002/adapters/openai_responses.py",
    "experiments/EXP_002/prompts/free.txt",
    "experiments/EXP_002/prompts/lineage.txt",
    "experiments/EXP_002/prompts/macro.txt",
)


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


def load_plan(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git_file_bytes(commit: str, relative_path: str) -> bytes:
    try:
        repo_root = Path(
            subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
        )
        repo_relative_path = str((PROJECT_ROOT / relative_path).resolve().relative_to(repo_root))
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        raise Gate2BIntegrityError("unable to resolve repository root for canonical artifact verification") from exc
    try:
        result = subprocess.run(
            ["git", "show", f"{commit}:{repo_relative_path}"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise Gate2BIntegrityError(
            f"unable to load canonical artifact {relative_path} at {commit}"
        ) from exc
    return result.stdout


def verify_canonical_artifacts(
    plan_path: Path,
    manifest_path: Path,
    plan: dict[str, Any],
    manifest: dict[str, Any],
) -> None:
    expected_plan_path = (PROJECT_ROOT / CANONICAL_PLAN_RELATIVE_PATH).resolve()
    expected_manifest_path = (PROJECT_ROOT / CANONICAL_MANIFEST_RELATIVE_PATH).resolve()
    if plan_path.resolve() != expected_plan_path:
        raise Gate2BIntegrityError("live execution requires the canonical Gate 2B plan path")
    if manifest_path.resolve() != expected_manifest_path:
        raise Gate2BIntegrityError("live execution requires the canonical Gate 2B manifest path")
    if plan_path.read_bytes() != git_file_bytes(CANONICAL_PLAN_COMMIT, CANONICAL_PLAN_RELATIVE_PATH):
        raise Gate2BIntegrityError("canonical Gate 2B plan bytes do not match the frozen plan commit")
    if manifest_path.read_bytes() != git_file_bytes(CANONICAL_MANIFEST_COMMIT, CANONICAL_MANIFEST_RELATIVE_PATH):
        raise Gate2BIntegrityError("canonical Gate 2B manifest bytes do not match the corrected manifest commit")
    plan_anchors = plan["anchors"]
    manifest_anchors = manifest["anchors"]
    if manifest_anchors.get("plan_freeze_commit") != CANONICAL_PLAN_COMMIT:
        raise Gate2BIntegrityError("manifest plan_freeze_commit does not match the canonical plan commit")
    if manifest_anchors.get("frozen_runtime") != plan_anchors.get("frozen_runtime"):
        raise Gate2BIntegrityError("manifest frozen_runtime does not match the plan frozen_runtime")
    if manifest_anchors.get("protocol_tag") != plan_anchors.get("protocol_tag"):
        raise Gate2BIntegrityError("manifest protocol_tag does not match the plan protocol_tag")


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


def resolve_and_verify_frozen_configuration(args: argparse.Namespace, plan: dict[str, Any]) -> dict[str, Any]:
    """Fail before any provider call unless the resolved config matches the frozen plan.

    The frozen plan is always the expected side of the comparison; user-supplied
    values are never compared against themselves.
    """
    frozen = plan["controlled_configuration"]
    resolved = {
        "rounds": frozen["rounds"] if args.rounds is None else args.rounds,
        "model": frozen["model"] if args.model is None else args.model,
        "reasoning_effort": frozen["reasoning_effort"] if args.reasoning_effort is None else args.reasoning_effort,
        "execution_policy": "paired",
    }
    mismatches = [
        f"{key}={resolved[key]!r} != frozen {frozen_value!r}"
        for key, frozen_value in (
            ("rounds", frozen["rounds"]),
            ("model", frozen["model"]),
            ("reasoning_effort", frozen["reasoning_effort"]),
            ("execution_policy", frozen["execution_policy"]),
        )
        if resolved[key] != frozen_value
    ]
    if mismatches:
        raise Gate2BIntegrityError(f"frozen configuration violation (no provider call made): {mismatches}")
    return resolved


def verify_runtime_matches_frozen(frozen_runtime_sha: str) -> None:
    """Fail before any provider call if any frozen runtime file has drifted."""
    try:
        result = subprocess.run(
            ["git", "diff", "--quiet", frozen_runtime_sha, "--", *FROZEN_RUNTIME_PATHS],
            cwd=PROJECT_ROOT,
        )
    except OSError as exc:
        raise Gate2BIntegrityError(f"unable to invoke git to verify frozen runtime: {exc}") from exc
    if result.returncode == 1:
        raise Gate2BIntegrityError(f"frozen runtime drift detected relative to {frozen_runtime_sha}")
    if result.returncode not in (0, 1):
        raise Gate2BIntegrityError(
            f"unable to verify frozen runtime against {frozen_runtime_sha} (git exit {result.returncode})"
        )


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


def archive_destination(archive_root: Path, task: WorldTask, attempt: int) -> Path:
    return archive_root / task.set_key / task.canonical_world_id / f"attempt_{attempt:03d}"


def existing_attempts(archive_root: Path, task: WorldTask) -> list[int]:
    world_dir = archive_root / task.set_key / task.canonical_world_id
    if not world_dir.exists():
        return []
    attempts = []
    for child in sorted(world_dir.iterdir()):
        if child.is_dir() and child.name.startswith("attempt_"):
            try:
                attempts.append(int(child.name.split("_", 1)[1]))
            except (IndexError, ValueError):
                continue
    return sorted(attempts)


def classify_existing_attempt(dest: Path, task: WorldTask, attempt: int) -> str:
    """Return "complete" or "failed"; raise Gate2BIntegrityError for any other state."""
    raw_present = {name: (dest / name).exists() for name in TRANSIENT_FILES}
    archive_meta_present = (dest / "archive_metadata.json").exists()
    failure_meta_present = (dest / "failure_metadata.json").exists()

    if failure_meta_present and not archive_meta_present:
        try:
            failure_metadata = json.loads((dest / "failure_metadata.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise Gate2BIntegrityError(
                f"{task.canonical_world_id} attempt_{attempt:03d}: unreadable failure_metadata.json: {exc}"
            ) from exc
        if failure_metadata.get("status") != "technical_failure":
            raise Gate2BIntegrityError(
                f"{task.canonical_world_id} attempt_{attempt:03d}: failure metadata is not technical_failure"
            )
        return "failed"

    if not all(raw_present.values()) or not archive_meta_present or failure_meta_present:
        raise Gate2BIntegrityError(
            f"{task.canonical_world_id} attempt_{attempt:03d}: inconsistent archive state at {dest} "
            f"(raw_present={raw_present}, archive_metadata={archive_meta_present}, "
            f"failure_metadata={failure_meta_present}); manual review required"
        )

    try:
        metadata = json.loads((dest / "archive_metadata.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Gate2BIntegrityError(
            f"{task.canonical_world_id} attempt_{attempt:03d}: unreadable archive_metadata.json: {exc}"
        ) from exc

    expected_identity = {
        "canonical_world_id": task.canonical_world_id,
        "set": task.set_key,
        "seed": task.seed,
        "attempt": attempt,
    }
    identity_mismatches = [
        f"{key}={metadata.get(key)!r} != {expected_value!r}"
        for key, expected_value in expected_identity.items()
        if metadata.get(key) != expected_value
    ]
    if identity_mismatches:
        raise Gate2BIntegrityError(
            f"{task.canonical_world_id} attempt_{attempt:03d}: archive_metadata identity mismatch {identity_mismatches}"
        )

    recorded_hashes = metadata.get("raw_file_sha256", {})
    hash_mismatches = [
        f"{name} recorded={recorded_hashes.get(name)!r} actual={sha256_file(dest / name)!r}"
        for name in TRANSIENT_FILES
        if recorded_hashes.get(name) != sha256_file(dest / name)
    ]
    if hash_mismatches:
        raise Gate2BIntegrityError(
            f"{task.canonical_world_id} attempt_{attempt:03d}: raw file hash mismatch {hash_mismatches}"
        )
    return "complete"


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
    except (OSError, subprocess.CalledProcessError):
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
    if experiment.adapter_name == "openai":
        checks.append((experiment.adapter_metadata.get("requested_model") == expected["model"], "requested_model mismatch"))
        checks.append((experiment.adapter_metadata.get("reasoning_effort") == expected["reasoning_effort"], "reasoning_effort mismatch"))
    failures = [detail for ok, detail in checks if not ok]
    if failures:
        raise Gate2BIntegrityError(f"{task.canonical_world_id}: integrity check failed: {failures}")


def _write_failure_record(dest: Path, task: WorldTask, attempt: int, manifest_path: Path, expected: dict[str, Any], exc: Exception) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    failure_metadata = {
        "gate": "2B",
        "set": task.set_key,
        "canonical_world_id": task.canonical_world_id,
        "seed": task.seed,
        "attempt": attempt,
        "frozen_config": {
            "rounds": expected["rounds"],
            "model": expected.get("model"),
            "reasoning_effort": expected.get("reasoning_effort"),
            "execution_policy": "paired",
        },
        "manifest_sha256": sha256_file(manifest_path),
        "exception_type": type(exc).__name__,
        "exception_message": str(exc),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "technical_failure",
    }
    (dest / "failure_metadata.json").write_text(json.dumps(failure_metadata, indent=2) + "\n", encoding="utf-8")


def _preserve_post_execution_failure(
    task: WorldTask,
    archive_root: Path,
    manifest_path: Path,
    expected: dict[str, Any],
    exc: Exception,
) -> None:
    attempts = existing_attempts(archive_root, task)
    attempt = attempts[-1] if attempts else 1
    dest = archive_destination(archive_root, task, attempt)
    dest.mkdir(parents=True, exist_ok=True)
    diagnostics = dest / "diagnostics"
    diagnostics.mkdir(exist_ok=True)
    diagnostic_hashes: dict[str, str] = {}
    for name in TRANSIENT_FILES:
        source = RESULTS / name
        if source.exists():
            target = diagnostics / name
            shutil.copy2(source, target)
            diagnostic_hashes[name] = sha256_file(target)
    failure_path = dest / "failure_metadata.json"
    if failure_path.exists():
        failure_metadata = json.loads(failure_path.read_text(encoding="utf-8"))
    else:
        _write_failure_record(dest, task, attempt, manifest_path, expected, exc)
        failure_metadata = json.loads(failure_path.read_text(encoding="utf-8"))
    failure_metadata["diagnostic_raw_file_sha256"] = diagnostic_hashes
    failure_metadata["diagnostics_are_invalid_incomplete_artifacts"] = True
    failure_path.write_text(json.dumps(failure_metadata, indent=2) + "\n", encoding="utf-8")


def _run_and_archive_world(
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
    authorize_retry: bool = False,
    execution_state: dict[str, bool] | None = None,
) -> Path:
    verify_world_reproducibility(task)

    attempts = existing_attempts(archive_root, task)
    next_attempt = 1
    if attempts:
        latest = attempts[-1]
        latest_dest = archive_destination(archive_root, task, latest)
        status = classify_existing_attempt(latest_dest, task, latest)
        if status == "complete":
            return latest_dest  # already archived and hash/identity verified; do not re-execute
        # status == "failed"
        if not authorize_retry:
            raise Gate2BIntegrityError(
                f"{task.canonical_world_id}: attempt_{latest:03d} recorded a technical failure; "
                f"a manually authorized retry (--authorize-retry) is required for attempt_{latest + 1:03d}"
            )
        next_attempt = latest + 1

    dest = archive_destination(archive_root, task, next_attempt)
    if dest.exists():
        raise Gate2BIntegrityError(f"{task.canonical_world_id}: attempt_{next_attempt:03d} directory already exists unexpectedly")

    clear_transient_outputs()
    if execution_state is not None:
        execution_state["started"] = True
    try:
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
    except Exception as exc:  # technical/provider failure, not a scientific outcome
        _write_failure_record(dest, task, next_attempt, manifest_path, expected, exc)
        raise Gate2BIntegrityError(
            f"{task.canonical_world_id}: technical failure during attempt_{next_attempt:03d} ({type(exc).__name__}); "
            "failure preserved, campaign stopped, no auto-retry"
        ) from exc

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
        "attempt": next_attempt,
        "manifest_path": str(manifest_path),
        "manifest_sha256": sha256_file(manifest_path),
        "manifest_last_commit": git_last_commit_for(manifest_path),
        "frozen_runtime": expected["frozen_runtime"],
        "protocol_tag": expected["protocol_tag"],
        "plan_freeze_commit": expected.get("plan_freeze_commit"),
        "runtime_emitted_world_id": summary_rows[0]["world_id"],
        "raw_run_metadata_note": (
            "Legacy field from frozen EXP-002 v0.1 run.py; run_class is the "
            "authoritative execution classification for Gate 2B."
        ),
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
    authorize_retry: bool = False,
) -> Path:
    execution_state = {"started": False}
    try:
        return _run_and_archive_world(
            task,
            adapter_factory=adapter_factory,
            adapter_name=adapter_name,
            adapter_metadata=adapter_metadata,
            run_class=run_class,
            rounds=rounds,
            archive_root=archive_root,
            manifest_path=manifest_path,
            expected=expected,
            authorize_retry=authorize_retry,
            execution_state=execution_state,
        )
    except Gate2BIntegrityError as exc:
        if execution_state["started"]:
            _preserve_post_execution_failure(task, archive_root, manifest_path, expected, exc)
        raise
    except Exception as exc:
        if execution_state["started"]:
            _preserve_post_execution_failure(task, archive_root, manifest_path, expected, exc)
        raise Gate2BIntegrityError(
            f"{task.canonical_world_id}: post-execution technical failure ({type(exc).__name__}); "
            "failure preserved, campaign stopped, no auto-retry"
        ) from exc


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
    authorize_retry: bool = False,
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
            authorize_retry=authorize_retry,
        )
        destinations.append(dest)
        print(f"[{task.set_key}] order={task.execution_order} {task.canonical_world_id} -> {dest}")
    return destinations


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gate 2B execution/archive orchestrator (does not modify the frozen EXP-002 runtime)"
    )
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--sets", default="generalization_set_001,stress_set_001")
    parser.add_argument("--adapter", choices=("deterministic_stub", "openai"), default="deterministic_stub")
    parser.add_argument("--model", default=None)
    parser.add_argument("--reasoning-effort", default=None)
    parser.add_argument("--rounds", type=int, default=None)
    parser.add_argument("--archive-root", type=Path, default=DEFAULT_ARCHIVE_ROOT)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--authorize-retry", action="store_true")
    args = parser.parse_args()

    if args.adapter == "openai" and not args.live:
        raise SystemExit("--adapter openai requires --live; no network call made")
    if args.adapter == "deterministic_stub" and args.live:
        raise SystemExit("--live is only valid with --adapter openai")

    plan = load_plan(args.plan)
    resolved = resolve_and_verify_frozen_configuration(args, plan)
    manifest = load_manifest(args.manifest)
    if args.adapter == "openai" and args.live:
        verify_canonical_artifacts(args.plan, args.manifest, plan, manifest)
    verify_runtime_matches_frozen(manifest["anchors"]["frozen_runtime"])

    sets = tuple(s.strip() for s in args.sets.split(",") if s.strip())
    tasks = manifest_world_tasks(manifest, sets)

    if args.adapter == "openai":
        config = OpenAIAdapterConfig.from_environment(model=resolved["model"], reasoning_effort=resolved["reasoning_effort"])
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
        "rounds": resolved["rounds"],
        "model": resolved["model"],
        "reasoning_effort": resolved["reasoning_effort"],
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
        rounds=resolved["rounds"],
        archive_root=args.archive_root,
        manifest_path=args.manifest,
        expected=expected,
        authorize_retry=args.authorize_retry,
    )


if __name__ == "__main__":
    main()

