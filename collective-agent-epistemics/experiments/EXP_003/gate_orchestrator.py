"""EXP-003 gate execution/archive orchestrator.

Executes the worlds of a frozen gate plan, in manifest order, with the EXP-003 runtime,
and archives each world immutably. It performs no scientific analysis.

Sources of truth, never overridden from the command line:
- world membership and execution order: the arm's manifest JSON (from manifest.py);
- model, effort, execution policy, reliability, rounds, probe, topology, root mode:
  the gate plan JSON (GATE_3x_PLAN_v0.1.json).

Guarantees:
- no provider call before the manifest reproduces every world locally, the plan and
  manifest agree, and (live) the runtime matches the frozen commit;
- every archived attempt carries SHA-256 hashes, archive_metadata.json and its
  factor-ledger row;
- a technical failure is preserved as failure_metadata.json and stops the campaign;
  the next attempt needs --authorize-retry;
- a complete attempt is never re-executed; re-running resumes;
- --max-worlds caps how many new executions one invocation may start;
- refusal fallbacks are never enabled here; a fallback-served event is rejected.

Usage:
    python -m experiments.EXP_003.gate_orchestrator --plan GATE_3A_PLAN_v0.1.json --preflight
    python -m experiments.EXP_003.gate_orchestrator --plan GATE_3A_PLAN_v0.1.json --arm bounce_set_001 \
        --adapter openai --live --max-worlds 4
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
from typing import Any

from .adapters.registry import ProviderBinding, build_provider
from .factors import factors_from_metadata
from .run import RESULTS, build_metadata, run_experiment, write_results
from .topology import get_topology
from .world_generator import WorldGenerator, alignment, world_cell

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent.parent
DEFAULT_ARCHIVE_ROOT = HERE / "results" / "archive"
PREFLIGHT_ROOT = HERE / "results" / "preflight"
TRANSIENT_FILES = ("events.jsonl", "summary.csv", "run_metadata.json")
REQUIRED_CONDITIONS = {"free", "lineage", "macro"}
CAMPAIGN_STATUS_FILE = "campaign_status.json"


def run_class_for(gate: str, live: bool) -> str:
    """Gate-specific run classes, as Gate 2B used `gate_2b_real_model`."""
    return f"gate_{gate.lower()}_{'real_model' if live else 'preflight'}"

FROZEN_RUNTIME_PATHS = (
    "experiments/EXP_003/run.py",
    "experiments/EXP_003/world_generator.py",
    "experiments/EXP_003/lineage.py",
    "experiments/EXP_003/metrics.py",
    "experiments/EXP_003/models.py",
    "experiments/EXP_003/prompting.py",
    "experiments/EXP_003/provenance.py",
    "experiments/EXP_003/topology.py",
    "experiments/EXP_003/adapters/base.py",
    "experiments/EXP_003/adapters/deterministic_stub.py",
    "experiments/EXP_003/adapters/openai_responses.py",
    "experiments/EXP_003/adapters/anthropic_messages.py",
    "experiments/EXP_003/adapters/registry.py",
    "experiments/EXP_003/prompts/free.txt",
    "experiments/EXP_003/prompts/lineage.txt",
    "experiments/EXP_003/prompts/macro.txt",
)


class GateIntegrityError(RuntimeError):
    """A configuration, file or provenance inconsistency. Never a scientific outcome."""


@dataclass(frozen=True)
class Arm:
    set_id: str
    topology: str
    root_mode: str
    rounds: int
    probe: bool
    manifest: Path
    optional: bool
    worlds: int
    stage: str = "set_001"


@dataclass(frozen=True)
class WorldTask:
    set_id: str
    canonical_id: str
    seed: int
    truth: str
    observed: tuple[str, ...]
    cell: str
    alignment: str
    execution_order: int


# ----------------------------------------------------------------------------- loading


def load_plan(path: Path) -> dict[str, Any]:
    plan = json.loads(path.read_text(encoding="utf-8"))
    for key in ("gate", "anchors", "controlled_configuration", "arms"):
        if key not in plan:
            raise GateIntegrityError(f"plan is missing '{key}'")
    return plan


def plan_arms(plan: dict[str, Any], plan_path: Path) -> list[Arm]:
    arms = []
    for raw in plan["arms"]:
        manifest = Path(raw["manifest"])
        if not manifest.is_absolute():
            manifest = plan_path.parent / manifest
        arms.append(Arm(
            set_id=raw["set_id"], topology=raw["topology"], root_mode=raw["root_mode"],
            rounds=int(raw["rounds"]), probe=bool(raw["probe"]), manifest=manifest,
            optional=bool(raw.get("optional", False)), worlds=int(raw["worlds"]),
            stage=str(raw.get("stage", "set_001")),
        ))
    return arms


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise GateIntegrityError(f"manifest not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_tasks(manifest: dict[str, Any], arm: Arm) -> list[WorldTask]:
    tasks = [
        WorldTask(
            set_id=arm.set_id, canonical_id=w["canonical_id"], seed=int(w["seed"]), truth=w["truth"],
            observed=tuple(w["observed"]), cell=w["cell"], alignment=w["alignment"],
            execution_order=int(w["execution_order"]),
        )
        for w in manifest["worlds"]
    ]
    tasks.sort(key=lambda t: t.execution_order)
    return tasks


# ----------------------------------------------------------------------------- verification


def verify_plan_and_manifest(plan: dict[str, Any], arm: Arm, manifest: dict[str, Any]) -> None:
    config = plan["controlled_configuration"]
    mismatches = []
    for label, actual, expected in (
        ("topology", manifest.get("topology"), arm.topology),
        ("root_mode", manifest.get("root_mode"), arm.root_mode),
        ("sensor_reliability", manifest.get("sensor_reliability"), config["sensor_reliability"]),
        ("world count", len(manifest.get("worlds", [])), arm.worlds),
        ("experiment", manifest.get("experiment"), "EXP-003"),
    ):
        if actual != expected:
            mismatches.append(f"{label}: manifest={actual!r} plan={expected!r}")
    if manifest.get("model_calls_made", 0) != 0:
        mismatches.append("manifest records model calls; a manifest must be derived without any")
    if mismatches:
        raise GateIntegrityError(f"{arm.set_id}: plan/manifest disagreement: {mismatches}")


def verify_anchors_for_live(plan: dict[str, Any]) -> None:
    anchors = plan["anchors"]
    missing = [k for k in ("frozen_runtime", "protocol_tag", "plan_freeze_commit", "derivation_anchor") if not anchors.get(k)]
    if missing:
        raise GateIntegrityError(f"live execution requires frozen anchors; missing {missing}")
    if plan.get("status", "").upper() != "FROZEN":
        raise GateIntegrityError("live execution requires plan status FROZEN")


def verify_committed_unchanged(path: Path, label: str) -> None:
    """Live execution requires the plan and every manifest to be committed and byte-identical to HEAD.

    This is the EXP-003 form of Gate 2B's canonical-artifact check: world membership and
    configuration must come from a committed, frozen file, never from a working-tree edit.
    """
    # Resolve first: git interprets a relative pathspec against cwd, and cwd is set to the
    # file's own directory below, so a relative path such as experiments/EXP_003/plan.json
    # would be looked up as experiments/EXP_003/experiments/EXP_003/plan.json and fail.
    path = Path(path).resolve()
    try:
        tracked = subprocess.run(["git", "ls-files", "--error-unmatch", str(path)], cwd=path.parent,
                                 capture_output=True)
        if tracked.returncode != 0:
            raise GateIntegrityError(f"{label} is not committed: {path}")
        diff = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", str(path)], cwd=path.parent)
    except OSError as exc:
        raise GateIntegrityError(f"unable to invoke git to verify {label}: {exc}") from exc
    if diff.returncode == 1:
        raise GateIntegrityError(f"{label} differs from its committed version: {path}")
    if diff.returncode != 0:
        raise GateIntegrityError(f"unable to verify {label} against HEAD (git exit {diff.returncode})")


def verify_manifest_anchor(plan: dict[str, Any], arm: Arm, manifest: dict[str, Any]) -> None:
    expected = plan["anchors"].get("derivation_anchor")
    if expected and manifest.get("anchor") != expected:
        raise GateIntegrityError(
            f"{arm.set_id}: manifest anchor {manifest.get('anchor')!r} != plan derivation_anchor {expected!r}"
        )


def verify_runtime_matches_frozen(frozen_runtime_sha: str) -> None:
    try:
        result = subprocess.run(
            ["git", "diff", "--quiet", frozen_runtime_sha, "--", *FROZEN_RUNTIME_PATHS],
            cwd=PROJECT_ROOT,
        )
    except OSError as exc:
        raise GateIntegrityError(f"unable to invoke git to verify frozen runtime: {exc}") from exc
    if result.returncode == 1:
        raise GateIntegrityError(f"frozen runtime drift detected relative to {frozen_runtime_sha}")
    if result.returncode != 0:
        raise GateIntegrityError(f"unable to verify frozen runtime against {frozen_runtime_sha} (git exit {result.returncode})")


def verify_world_reproducibility(task: WorldTask, arm: Arm, reliability: float) -> None:
    world = WorldGenerator(task.seed, arm.topology, arm.root_mode, reliability).generate(seed=task.seed)
    observed = tuple(e.observed_state for e in world.evidence)
    mismatches = [
        label for label, actual, expected in (
            ("truth", world.truth, task.truth),
            ("observed", observed, task.observed),
            ("cell", world_cell(world), task.cell),
            ("alignment", alignment(world), task.alignment),
        ) if actual != expected
    ]
    if mismatches:
        raise GateIntegrityError(f"{task.canonical_id}: world reproducibility mismatch in {mismatches}")


def expected_actual_calls(arm: Arm) -> int:
    topo = get_topology(arm.topology)
    seed = topo.seed_firings()
    per_condition = seed + arm.rounds * topo.firings_per_round()
    return seed + 2 * (per_condition - seed)


# ----------------------------------------------------------------------------- archive helpers


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_last_commit_for(path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", path.name],
            cwd=path.resolve().parent, capture_output=True, text=True, check=True,
        )
        return result.stdout.strip() or None
    except (OSError, subprocess.CalledProcessError):
        return None


def set_directory_name(arm: Arm, plan: dict[str, Any], binding: ProviderBinding) -> str:
    """A model-layer set executed under another provider is archived as <set>_<provider>."""
    planned_provider = plan["controlled_configuration"].get("provider", "openai")
    provider = binding.metadata.get("provider")
    if provider in (None, "local") or provider == planned_provider:
        return arm.set_id
    return f"{arm.set_id}_{provider}"


def archive_destination(archive_root: Path, gate_dir: str, set_dir: str, task: WorldTask, attempt: int) -> Path:
    return archive_root / gate_dir / set_dir / task.canonical_id / f"attempt_{attempt:03d}"


def existing_attempts(world_dir: Path) -> list[int]:
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


def world_status(world_dir: Path, task: WorldTask) -> tuple[str, int | None]:
    """('complete' | 'failed' | 'pending', latest attempt or None). Raises on an inconsistent archive."""
    attempts = existing_attempts(world_dir)
    if not attempts:
        return "pending", None
    latest = attempts[-1]
    return classify_existing_attempt(world_dir / f"attempt_{latest:03d}", task, latest), latest


def classify_existing_attempt(dest: Path, task: WorldTask, attempt: int) -> str:
    raw_present = {name: (dest / name).exists() for name in TRANSIENT_FILES}
    archive_meta = dest / "archive_metadata.json"
    failure_meta = dest / "failure_metadata.json"
    if failure_meta.exists() and not archive_meta.exists():
        record = json.loads(failure_meta.read_text(encoding="utf-8"))
        if record.get("status") != "technical_failure":
            raise GateIntegrityError(f"{task.canonical_id} attempt_{attempt:03d}: failure metadata is not technical_failure")
        return "failed"
    if not all(raw_present.values()) or not archive_meta.exists() or failure_meta.exists():
        raise GateIntegrityError(
            f"{task.canonical_id} attempt_{attempt:03d}: inconsistent archive state at {dest}; manual review required"
        )
    metadata = json.loads(archive_meta.read_text(encoding="utf-8"))
    for key, expected in (("canonical_id", task.canonical_id), ("seed", task.seed), ("attempt", attempt)):
        if metadata.get(key) != expected:
            raise GateIntegrityError(f"{task.canonical_id} attempt_{attempt:03d}: archive identity mismatch on {key}")
    recorded = metadata.get("raw_file_sha256", {})
    for name in TRANSIENT_FILES:
        if recorded.get(name) != sha256_file(dest / name):
            raise GateIntegrityError(f"{task.canonical_id} attempt_{attempt:03d}: raw file hash mismatch on {name}")
    return "complete"


def clear_transient_outputs() -> None:
    for name in TRANSIENT_FILES:
        path = RESULTS / name
        if path.exists():
            path.unlink()


def read_summary_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


# ----------------------------------------------------------------------------- validation of one execution


def validate_execution(experiment, summary_rows: list[dict[str, str]], task: WorldTask, arm: Arm,
                       plan: dict[str, Any], binding: ProviderBinding, live: bool) -> None:
    config = plan["controlled_configuration"]
    meta = experiment.execution_metadata
    checks = [
        (meta.get("actual_model_call_count") == expected_actual_calls(arm),
         f"actual_model_call_count={meta.get('actual_model_call_count')} expected={expected_actual_calls(arm)}"),
        (meta.get("fallback_events", 0) == 0, f"fallback_events={meta.get('fallback_events')}"),
        ({row["condition"] for row in summary_rows} == REQUIRED_CONDITIONS, "conditions"),
        (all(row["truth"] == task.truth for row in summary_rows), "summary truth mismatch"),
        (experiment.execution_policy == config["execution_policy"], f"execution_policy={experiment.execution_policy}"),
        (experiment.rounds == arm.rounds, f"rounds={experiment.rounds}"),
        (experiment.seed == task.seed, f"seed={experiment.seed}"),
        (experiment.topology.name == arm.topology, f"topology={experiment.topology.name}"),
        (experiment.root_mode == arm.root_mode, f"root_mode={experiment.root_mode}"),
        (experiment.probe == arm.probe, f"probe={experiment.probe}"),
        (abs(experiment.sensor_reliability - config["sensor_reliability"]) < 1e-9, "sensor_reliability"),
    ]
    checks.append((experiment.run_class == run_class_for(plan["gate"], live), f"run_class={experiment.run_class}"))
    if live:
        checks.append((experiment.adapter_metadata.get("requested_model") == config["model"], "requested_model mismatch"))
        checks.append((experiment.adapter_metadata.get("reasoning_effort") == config["reasoning_effort"], "reasoning_effort mismatch"))
        checks.append((not experiment.adapter_metadata.get("fallbacks", False), "fallbacks must be off"))
        served = set(meta.get("served_models", []))
        checks.append((not served or all(s.startswith(config["model"]) for s in served), f"served_models={sorted(served)}"))
    failures = [detail for ok, detail in checks if not ok]
    if failures:
        raise GateIntegrityError(f"{task.canonical_id}: integrity check failed: {failures}")


# ----------------------------------------------------------------------------- execution


def _write_failure_record(dest: Path, task: WorldTask, arm: Arm, plan: dict[str, Any], attempt: int,
                          manifest_path: Path, exc: Exception) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    record = {
        "gate": plan["gate"], "set": arm.set_id, "canonical_id": task.canonical_id, "seed": task.seed,
        "attempt": attempt,
        "frozen_config": {**plan["controlled_configuration"], "rounds": arm.rounds, "probe": arm.probe,
                          "topology": arm.topology, "root_mode": arm.root_mode},
        "manifest_sha256": sha256_file(manifest_path),
        "exception_type": type(exc).__name__, "exception_message": str(exc),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "technical_failure",
    }
    (dest / "failure_metadata.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def run_and_archive_world(task: WorldTask, arm: Arm, plan: dict[str, Any], binding: ProviderBinding, *,
                          archive_root: Path, gate_dir: str, set_dir: str, manifest_path: Path,
                          live: bool, authorize_retry: bool) -> tuple[Path, bool]:
    """Returns (destination, executed). executed is False when a complete attempt already existed."""
    config = plan["controlled_configuration"]
    verify_world_reproducibility(task, arm, config["sensor_reliability"])

    world_dir = archive_root / gate_dir / set_dir / task.canonical_id
    status, latest = world_status(world_dir, task)
    next_attempt = 1
    if status == "complete":
        return world_dir / f"attempt_{latest:03d}", False
    if status == "failed":
        if not authorize_retry:
            raise GateIntegrityError(
                f"{task.canonical_id}: attempt_{latest:03d} recorded a technical failure; "
                f"--authorize-retry is required for attempt_{latest + 1:03d}"
            )
        next_attempt = latest + 1

    dest = archive_destination(archive_root, gate_dir, set_dir, task, next_attempt)
    if dest.exists():
        raise GateIntegrityError(f"{task.canonical_id}: {dest} already exists unexpectedly")

    clear_transient_outputs()
    try:
        experiment = run_experiment(
            trials=1, rounds=arm.rounds, seed=task.seed,
            topology=arm.topology, root_mode=arm.root_mode,
            adapter_factory=binding.factory, adapter_name=binding.adapter_name,
            adapter_metadata=binding.metadata,
            run_class=run_class_for(plan["gate"], live),
            execution_policy=config["execution_policy"], probe=arm.probe,
            sensor_reliability=config["sensor_reliability"],
        )
        write_results(experiment)
        summary_rows = read_summary_rows(RESULTS / "summary.csv")
        validate_execution(experiment, summary_rows, task, arm, plan, binding, live)
    except Exception as exc:
        _write_failure_record(dest, task, arm, plan, next_attempt, manifest_path, exc)
        raise GateIntegrityError(
            f"{task.canonical_id}: technical failure during attempt_{next_attempt:03d} "
            f"({type(exc).__name__}: {exc}); failure preserved, campaign stopped, no auto-retry"
        ) from exc

    pre_hashes = {name: sha256_file(RESULTS / name) for name in TRANSIENT_FILES}
    dest.mkdir(parents=True, exist_ok=False)
    for name in TRANSIENT_FILES:
        shutil.copy2(RESULTS / name, dest / name)
    post_hashes = {name: sha256_file(dest / name) for name in TRANSIENT_FILES}
    if pre_hashes != post_hashes:
        raise GateIntegrityError(f"{task.canonical_id}: archive copy hash mismatch")

    run_meta = build_metadata(experiment)
    archive_metadata = {
        "gate": plan["gate"], "set": set_dir, "planned_set": arm.set_id,
        "canonical_id": task.canonical_id, "seed": task.seed, "attempt": next_attempt,
        "execution_order": task.execution_order, "cell": task.cell, "alignment": task.alignment,
        "manifest_path": str(manifest_path), "manifest_sha256": sha256_file(manifest_path),
        "manifest_last_commit": git_last_commit_for(manifest_path),
        "plan_version": plan.get("plan_version"), "plan_status": plan.get("status"),
        "frozen_runtime": plan["anchors"].get("frozen_runtime"),
        "protocol_tag": plan["anchors"].get("protocol_tag"),
        "plan_freeze_commit": plan["anchors"].get("plan_freeze_commit"),
        "topology": arm.topology, "root_mode": arm.root_mode, "rounds": arm.rounds, "probe": arm.probe,
        "provider": binding.metadata.get("provider"), "requested_model": binding.metadata.get("requested_model"),
        "reasoning_effort": binding.metadata.get("reasoning_effort"),
        "run_class": experiment.run_class, "live": live,
        "actual_model_call_count": experiment.execution_metadata["actual_model_call_count"],
        "reused_response_count": experiment.execution_metadata["reused_response_count"],
        "served_models": experiment.execution_metadata.get("served_models", []),
        "fallback_events": experiment.execution_metadata.get("fallback_events", 0),
        "factors": {k: v for k, v in factors_from_metadata(run_meta).items() if k not in ("source",)},
        "raw_file_sha256": post_hashes,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "technical_integrity_status": "pass",
    }
    (dest / "archive_metadata.json").write_text(json.dumps(archive_metadata, indent=2) + "\n", encoding="utf-8")
    return dest, True


def campaign_status(plan: dict[str, Any], arms: list[Arm], binding: ProviderBinding | None,
                    archive_root: Path) -> dict[str, Any]:
    """Mechanical completeness of each set. A set is closable only when every world is complete."""
    gate_dir = f"gate_{plan['gate'].lower()}"
    report: dict[str, Any] = {"gate": plan["gate"], "plan_version": plan.get("plan_version"),
                              "archive_root": str(archive_root), "sets": {}, "all_required_sets_complete": True}
    for arm in arms:
        if not arm.manifest.exists():
            report["sets"][arm.set_id] = {"status": "no_manifest", "stage": arm.stage, "optional": arm.optional}
            if not arm.optional:
                report["all_required_sets_complete"] = False
            continue
        manifest = load_manifest(arm.manifest)
        tasks = manifest_tasks(manifest, arm)
        set_dir = set_directory_name(arm, plan, binding) if binding else arm.set_id
        counts = {"complete": 0, "failed": 0, "pending": 0}
        worlds = []
        for task in tasks:
            status, latest = world_status(archive_root / gate_dir / set_dir / task.canonical_id, task)
            counts[status] += 1
            worlds.append({"order": task.execution_order, "canonical_id": task.canonical_id,
                           "status": status, "latest_attempt": latest})
        complete = counts["complete"] == len(tasks)
        report["sets"][arm.set_id] = {"archive_set": set_dir, "stage": arm.stage, "optional": arm.optional,
                                      "planned": len(tasks), **counts, "closable": complete, "worlds": worlds}
        if not arm.optional and not complete:
            report["all_required_sets_complete"] = False
    return report


def write_campaign_status(report: dict[str, Any], archive_root: Path) -> Path:
    gate_dir = archive_root / f"gate_{report['gate'].lower()}"
    gate_dir.mkdir(parents=True, exist_ok=True)
    report = {**report, "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "note": ("Pacing record only. A set with pending or failed worlds is incomplete: it may not be "
                       "audited, pooled or reported, and execution must resume in frozen order until complete.")}
    path = gate_dir / CAMPAIGN_STATUS_FILE
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return path


def run_campaign(plan: dict[str, Any], plan_path: Path, arms: list[Arm], binding: ProviderBinding, *,
                 archive_root: Path, live: bool, authorize_retry: bool, max_worlds: int | None,
                 include_optional: bool) -> list[Path]:
    gate_dir = f"gate_{plan['gate'].lower()}"
    if live:
        verify_anchors_for_live(plan)
        verify_runtime_matches_frozen(plan["anchors"]["frozen_runtime"])
        verify_committed_unchanged(plan_path, "gate plan")
    destinations: list[Path] = []
    started = 0
    try:
        for arm in arms:
            if arm.optional and not include_optional:
                print(f"[{arm.set_id}] optional arm skipped (pass --include-optional to run it)")
                continue
            manifest = load_manifest(arm.manifest)
            verify_plan_and_manifest(plan, arm, manifest)
            verify_manifest_anchor(plan, arm, manifest)
            if live:
                verify_committed_unchanged(arm.manifest, f"{arm.set_id} manifest")
            tasks = manifest_tasks(manifest, arm)
            for task in tasks:
                verify_world_reproducibility(task, arm, plan["controlled_configuration"]["sensor_reliability"])
            set_dir = set_directory_name(arm, plan, binding)
            print(f"[{arm.set_id}] {len(tasks)} worlds, topology={arm.topology}, root_mode={arm.root_mode}, "
                  f"rounds={arm.rounds}, probe={arm.probe}, calls/world={expected_actual_calls(arm)}, archive={gate_dir}/{set_dir}")
            for task in tasks:
                world_dir = archive_root / gate_dir / set_dir / task.canonical_id
                status, latest = world_status(world_dir, task)
                if status == "pending" or status == "failed":
                    # The cap is a pacing device, blind to results: it only decides whether this
                    # invocation may start another execution. Frozen order is preserved on resume.
                    if max_worlds is not None and started >= max_worlds:
                        print(f"--max-worlds {max_worlds} reached; pausing before {task.canonical_id}. "
                              "The set is incomplete until every world is archived; re-run to resume.")
                        return destinations
                dest, executed = run_and_archive_world(
                    task, arm, plan, binding, archive_root=archive_root, gate_dir=gate_dir, set_dir=set_dir,
                    manifest_path=arm.manifest, live=live, authorize_retry=authorize_retry,
                )
                started += int(executed)
                destinations.append(dest)
                print(f"  order={task.execution_order:02d} {task.canonical_id} -> {dest} ({'executed' if executed else 'already complete'})")
        return destinations
    finally:
        write_campaign_status(campaign_status(plan, arms, binding, archive_root), archive_root)


def main() -> None:
    parser = argparse.ArgumentParser(description="EXP-003 gate orchestrator (execute and archive a frozen plan)")
    parser.add_argument("--plan", type=Path, required=True, help="GATE_3x_PLAN_v0.1.json")
    parser.add_argument("--arm", action="append", default=None, help="set_id to run; repeatable; default all non-optional")
    parser.add_argument("--stage", default=None,
                        help="run only arms of this stage (set_001 discovery, set_002 replication); default all")
    parser.add_argument("--include-optional", action="store_true")
    parser.add_argument("--adapter", choices=("deterministic_stub", "openai", "anthropic"), default="deterministic_stub")
    parser.add_argument("--stub-mode", choices=("naive", "dedup"), default="dedup")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--preflight", action="store_true",
                        help="stub execution of the whole plan into results/preflight (no calls, not an archive)")
    parser.add_argument("--archive-root", type=Path, default=None)
    parser.add_argument("--authorize-retry", action="store_true")
    parser.add_argument("--max-worlds", type=int, default=None,
                        help="pacing cap on new executions this invocation; the set stays incomplete until resumed to the end")
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--status", action="store_true", help="report completeness per set and exit; no calls")
    args = parser.parse_args()

    plan = load_plan(args.plan)
    config = plan["controlled_configuration"]
    arms = plan_arms(plan, args.plan)
    if args.stage:
        arms = [a for a in arms if a.stage == args.stage]
        if not arms:
            raise SystemExit(f"no arms with stage {args.stage!r}")

    if args.status:
        root = args.archive_root or (PREFLIGHT_ROOT if args.preflight else DEFAULT_ARCHIVE_ROOT)
        report = campaign_status(plan, arms, None, root)
        print(json.dumps(report, indent=2))
        return
    if args.arm:
        wanted = set(args.arm)
        unknown = wanted - {a.set_id for a in arms}
        if unknown:
            raise SystemExit(f"unknown arm(s): {sorted(unknown)}; plan has {[a.set_id for a in arms]}")
        arms = [a for a in arms if a.set_id in wanted]
        include_optional = True
    else:
        include_optional = args.include_optional

    if args.preflight:
        if args.live or args.adapter != "deterministic_stub":
            raise SystemExit("--preflight runs the stub only")
        archive_root = args.archive_root or PREFLIGHT_ROOT
        live = False
    else:
        if args.adapter == "deterministic_stub":
            raise SystemExit("stub execution outside --preflight is not allowed: it would write a non-scientific archive")
        if not args.live:
            raise SystemExit(f"{args.adapter} adapter requires --live; no network call made")
        archive_root = args.archive_root or DEFAULT_ARCHIVE_ROOT
        live = True

    # The plan is the only source of model/effort. Fallbacks are never passed from here.
    binding = build_provider(
        args.adapter, model=config.get("model"), reasoning_effort=config.get("reasoning_effort"),
        probe=True, timeout_seconds=args.timeout, stub_mode=args.stub_mode,
    )
    print(f"Gate {plan['gate']} orchestrator: plan={args.plan.name} status={plan.get('status')} "
          f"adapter={binding.adapter_name} live={live} archive_root={archive_root}")
    run_campaign(plan, args.plan, arms, binding, archive_root=archive_root, live=live,
                 authorize_retry=args.authorize_retry, max_worlds=args.max_worlds,
                 include_optional=include_optional)


if __name__ == "__main__":
    main()
