"""EXP-003 corpus integrity audit (read-only, no scientific analysis).

Verifies that a gate's archived stage is complete and technically sound, exactly as the
Gate 2B corpus audit did for EXP-002, and writes a JSON and a Markdown record under
experiments/EXP_003/audits/gate_<x>/. It reads lineage, provenance-of-execution and
provider metadata only. It never reads or reports an answer, a confidence, a P(A), a
message, or any metric value. A stage that passes this audit has finished data
collection; it has not been interpreted.

Usage:
    python -m experiments.EXP_003.tools.corpus_audit --plan experiments/EXP_003/GATE_3A_PLAN_v0.1.json --stage set_001
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..gate_orchestrator import (
    DEFAULT_ARCHIVE_ROOT,
    FROZEN_RUNTIME_PATHS,
    PROJECT_ROOT,
    load_plan,
    plan_arms,
    run_class_for,
)
from ..topology import get_topology

EXP003 = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_counts(topology_name: str, rounds: int, root_mode: str) -> tuple[int, int]:
    """(actual model calls, archived events) per world under paired execution.

    MACRO stops after the first recursive cycle that adds no new independent root. A root
    enters the lineage graph when its holder first fires. Under single and shared root
    modes there is one physical root (E1) and it enters at the seed cycle, so MACRO stops
    after cycle 1. Under dual root mode E2 is held by the topology's secondary sources: if
    one of them is a seed-cycle sender (hives: A2) E2 also enters at the seed and MACRO
    stops after cycle 1; if none is (diamond: C) E2 enters during cycle 1 and MACRO stops
    after cycle 2. Derived from the topology; never from the archived outcomes.
    """
    topo = get_topology(topology_name)
    seed = topo.seed_firings()
    per_condition = seed + rounds * topo.firings_per_round()
    calls = seed + 2 * (per_condition - seed)
    seed_senders = {firing.sender for firing in topo.seed_cycle}
    second_root_enters_in_cycle_1 = (root_mode == "dual"
                                     and not any(holder in seed_senders for holder in topo.secondary_sources))
    macro_cycles = min(rounds, 2 if second_root_enters_in_cycle_1 else 1)
    macro_events = seed + macro_cycles * topo.firings_per_round()
    return calls, 2 * per_condition + macro_events


def portable_path(path: Path) -> str:
    """A checkout-independent rendering of a path: relative to the project root when inside
    it, so that audit records produced in different checkouts compare equal."""
    resolved = Path(path).resolve()
    try:
        return resolved.relative_to(PROJECT_ROOT.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def git_output(args: list[str], cwd: Path) -> str | None:
    try:
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def audit_stage(plan_path: Path, stage: str, archive_root: Path, preflight: bool = False) -> dict[str, Any]:
    plan = load_plan(plan_path)
    cfg = plan["controlled_configuration"]
    gate = plan["gate"]
    gate_dir = archive_root / f"gate_{gate.lower()}"
    arms = [a for a in plan_arms(plan, plan_path) if a.stage == stage]
    if not arms:
        raise SystemExit(f"no arms with stage {stage!r} in {plan_path}")
    expected_run_class = run_class_for(gate, live=not preflight)
    problems: list[str] = []
    sets: dict[str, Any] = {}
    failures: list[dict[str, Any]] = []
    total_calls = 0
    total_tokens = 0

    for arm in arms:
        manifest_path = arm.manifest
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_sha = sha256_file(manifest_path)
        expected_ids = {w["canonical_id"]: w for w in manifest["worlds"]}
        set_dir = gate_dir / arm.set_id
        calls_expected, events_expected = expected_counts(arm.topology, arm.rounds, arm.root_mode)
        worlds: list[dict[str, Any]] = []
        found_ids = {p.name for p in set_dir.iterdir() if p.is_dir()} if set_dir.exists() else set()
        if found_ids != set(expected_ids):
            problems.append(f"{arm.set_id}: archived worlds {sorted(found_ids ^ set(expected_ids))} do not match the manifest")
        set_tokens = 0
        set_calls = 0
        for canonical_id, w in sorted(expected_ids.items(), key=lambda kv: kv[1]["execution_order"]):
            world_dir = set_dir / canonical_id
            attempts = sorted(p for p in world_dir.iterdir() if p.name.startswith("attempt_")) if world_dir.exists() else []
            complete: list[dict[str, Any]] = []
            for a in attempts:
                failure_meta = a / "failure_metadata.json"
                archive_meta = a / "archive_metadata.json"
                if failure_meta.exists() and not archive_meta.exists():
                    rec = json.loads(failure_meta.read_text(encoding="utf-8"))
                    failures.append({"set": arm.set_id, "canonical_id": canonical_id, "attempt": a.name,
                                     "exception_type": rec.get("exception_type"), "exception_message": rec.get("exception_message"),
                                     "timestamp_utc": rec.get("timestamp_utc"), "status": rec.get("status")})
                    if rec.get("status") != "technical_failure":
                        problems.append(f"{a}: failure record status is not technical_failure")
                    for raw in ("events.jsonl", "summary.csv", "run_metadata.json"):
                        if (a / raw).exists():
                            problems.append(f"{a}: failure record with raw output {raw} present")
                    continue
                if not archive_meta.exists():
                    problems.append(f"{a}: neither archive_metadata.json nor failure_metadata.json")
                    continue
                meta = json.loads(archive_meta.read_text(encoding="utf-8"))
                run = json.loads((a / "run_metadata.json").read_text(encoding="utf-8"))
                hashes_ok = all(sha256_file(a / name) == h for name, h in meta["raw_file_sha256"].items())
                if not hashes_ok:
                    problems.append(f"{a}: raw file hash mismatch")
                checks = {
                    "run_class": (meta.get("run_class"), expected_run_class),
                    "provider": (meta.get("provider"), None if preflight else cfg["provider"]),
                    "requested_model": (meta.get("requested_model"), None if preflight else cfg["model"]),
                    "reasoning_effort": (meta.get("reasoning_effort"), None if preflight else cfg["reasoning_effort"]),
                    "probe": (meta.get("probe"), arm.probe),
                    "topology": (meta.get("topology"), arm.topology),
                    "root_mode": (meta.get("root_mode"), arm.root_mode),
                    "rounds": (meta.get("rounds"), arm.rounds),
                    "actual_model_call_count": (meta.get("actual_model_call_count"), calls_expected),
                    "fallback_events": (meta.get("fallback_events"), 0),
                    "fallbacks_flag": (run.get("fallbacks"), False),
                    "frozen_runtime": (meta.get("frozen_runtime"), plan["anchors"].get("frozen_runtime")),
                    "plan_freeze_commit": (meta.get("plan_freeze_commit"), plan["anchors"].get("plan_freeze_commit")),
                    "manifest_sha256": (meta.get("manifest_sha256"), manifest_sha),
                    "seed": (meta.get("seed"), w["seed"]),
                    "cell": (meta.get("cell"), w["cell"]),
                    "technical_integrity_status": (meta.get("technical_integrity_status"), "pass"),
                }
                if preflight:
                    for k in ("provider", "requested_model", "reasoning_effort"):
                        checks.pop(k)
                bad = {k: v for k, v in checks.items() if v[0] != v[1]}
                if bad:
                    problems.append(f"{a}: {bad}")
                n_events = 0
                bad_events = 0
                max_depth = 0
                roots: set[str] = set()
                conditions: set[str] = set()
                for line in (a / "events.jsonl").read_text(encoding="utf-8").splitlines():
                    if not line.strip():
                        continue
                    e = json.loads(line)
                    n_events += 1
                    conditions.add(e["condition"])
                    max_depth = max(max_depth, e["actual_lineage"]["inference_depth"])
                    roots |= set(e["actual_lineage"]["actual_roots"])
                    pm = e.get("provider_metadata") or {}
                    if pm.get("fallback_ran"):
                        bad_events += 1
                    served = pm.get("served_model") or pm.get("returned_model")
                    if not preflight and served and not str(served).startswith(cfg["model"]):
                        bad_events += 1
                expected_roots = {"E1"} if arm.root_mode in ("single", "shared") else {"E1", "E2"}
                if n_events != events_expected or bad_events or max_depth != cfg.get("max_depth", 12) \
                        or roots != expected_roots or conditions != {"free", "lineage", "macro"}:
                    problems.append(f"{a}: events={n_events}/{events_expected} bad={bad_events} depth={max_depth} roots={sorted(roots)} conditions={sorted(conditions)}")
                tokens = int(run["execution_metadata"].get("total_tokens_actual") or 0)
                set_tokens += tokens
                set_calls += int(meta.get("actual_model_call_count") or 0)
                complete.append({"attempt": a.name, "raw_file_sha256": meta["raw_file_sha256"], "tokens": tokens,
                                 "timestamp_utc": meta.get("timestamp_utc")})
            if len(complete) != 1:
                problems.append(f"{world_dir}: {len(complete)} complete attempts; exactly one is required")
            worlds.append({"execution_order": w["execution_order"], "canonical_id": canonical_id, "seed": w["seed"],
                           "cell": w["cell"], "alignment": w["alignment"], "attempts_present": [p.name for p in attempts],
                           "complete": [c["attempt"] for c in complete], "raw_file_sha256": complete[0]["raw_file_sha256"] if complete else None})
        total_calls += set_calls
        total_tokens += set_tokens
        sets[arm.set_id] = {"topology": arm.topology, "root_mode": arm.root_mode, "rounds": arm.rounds, "probe": arm.probe,
                            "manifest": manifest_path.name, "manifest_sha256": manifest_sha,
                            "manifest_last_commit": git_output(["log", "-1", "--format=%H", "--", manifest_path.name], manifest_path.parent),
                            "planned_worlds": len(expected_ids), "complete_worlds": sum(1 for x in worlds if x["complete"]),
                            "calls_per_world_expected": calls_expected, "events_per_world_expected": events_expected,
                            "actual_calls": set_calls, "tokens": set_tokens, "worlds": worlds}

    # Runtime drift of the frozen paths relative to the recorded frozen runtime.
    runtime_sha = plan["anchors"].get("frozen_runtime")
    drift = None
    if runtime_sha and not preflight:
        r = subprocess.run(["git", "diff", "--quiet", runtime_sha, "--", *FROZEN_RUNTIME_PATHS], cwd=PROJECT_ROOT)
        drift = {0: "none", 1: "DRIFT"}.get(r.returncode, f"unverifiable (git exit {r.returncode})")
        if drift != "none":
            problems.append(f"frozen runtime drift check: {drift}")

    status = "PASS" if not problems else "FAIL"
    return {
        "experiment": "EXP-003", "gate": gate, "stage": stage, "plan_version": plan.get("plan_version"),
        "plan_status": plan.get("status"), "plan_sha256": sha256_file(plan_path),
        "anchors": plan["anchors"], "controlled_configuration": cfg,
        "archive_root": portable_path(archive_root), "head_commit": git_output(["rev-parse", "HEAD"], PROJECT_ROOT),
        "frozen_runtime_drift": drift, "expected_run_class": expected_run_class,
        "sets": sets, "technical_failures": failures,
        "totals": {"planned_worlds": sum(s["planned_worlds"] for s in sets.values()),
                   "complete_worlds": sum(s["complete_worlds"] for s in sets.values()),
                   "actual_calls": total_calls, "tokens": total_tokens, "failure_records": len(failures)},
        "problems": problems, "status": status,
        "scientific_boundary": ("No answer, confidence, P(A), Brier, message, provenance mark, excess, FIS, DSCD, FREE/LINEAGE "
                                "comparison or any other outcome was read, computed or reported. This audit establishes that "
                                "data collection for the stage is complete and technically sound. It is not an interpretation."),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


def render_markdown(r: dict[str, Any]) -> str:
    t = r["totals"]
    lines = [
        f"# EXP-003 Gate {r['gate']} {r['stage'].replace('_', ' ').title()} Corpus Integrity Audit v0.1",
        "",
        f"## Status",
        "",
        f"**{r['status']}**" + ("" if r["status"] == "PASS" else " (see Problems)"),
        "",
        "Read-only corpus/provenance audit. Scientific interpretation was **not performed**.",
        "",
        "## Provenance",
        "",
        f"- Plan: `{r['plan_version']}` (status `{r['plan_status']}`, sha256 `{r['plan_sha256']}`)",
        f"- Frozen runtime: `{r['anchors'].get('frozen_runtime')}`; protocol tag `{r['anchors'].get('protocol_tag')}`",
        f"- Plan freeze commit: `{r['anchors'].get('plan_freeze_commit')}`",
        f"- Derivation anchor: `{r['anchors'].get('derivation_anchor')}`",
        f"- HEAD at audit time: `{r['head_commit']}`",
        f"- Frozen runtime drift: {r['frozen_runtime_drift']}",
        f"- Expected run class: `{r['expected_run_class']}`; model `{r['controlled_configuration'].get('model')}`; effort `{r['controlled_configuration'].get('reasoning_effort')}`; paired; reliability `{r['controlled_configuration'].get('sensor_reliability')}`",
        "",
        "## Corpus shape",
        "",
        "| Set | Topology | Rounds | Probe | Manifest sha256 | Planned | Complete | Calls/world | Events/world | Actual calls | Tokens |",
        "|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for set_id, s in r["sets"].items():
        lines.append(f"| `{set_id}` | {s['topology']} | {s['rounds']} | {'on' if s['probe'] else 'off'} | `{s['manifest_sha256'][:12]}…` | {s['planned_worlds']} | {s['complete_worlds']} | {s['calls_per_world_expected']} | {s['events_per_world_expected']} | {s['actual_calls']} | {s['tokens']} |")
    lines += ["", f"Totals: planned {t['planned_worlds']}, complete {t['complete_worlds']}, actual provider calls {t['actual_calls']}, tokens {t['tokens']}, technical failure records {t['failure_records']}.", ""]
    lines += ["## Technical failures (preserved, excluded from scientific N)", ""]
    if r["technical_failures"]:
        lines += ["| Set | World | Attempt | Exception | Message | Timestamp |", "|---|---|---|---|---|---|"]
        for f in r["technical_failures"]:
            lines.append(f"| `{f['set']}` | `{f['canonical_id']}` | {f['attempt']} | `{f['exception_type']}` | {f['exception_message']} | {f['timestamp_utc']} |")
    else:
        lines.append("None.")
    lines += ["", "## Mechanical verification", "",
              "- Archived worlds equal the manifest's worlds for every set: " + ("PASS" if not any("do not match the manifest" in p for p in r["problems"]) else "FAIL"),
              "- Exactly one complete attempt per world: " + ("PASS" if not any("complete attempts" in p for p in r["problems"]) else "FAIL"),
              "- Raw file SHA-256 hashes match archive records: " + ("PASS" if not any("hash mismatch" in p for p in r["problems"]) else "FAIL"),
              "- Run class, provider, model, effort, probe, topology, root mode, rounds, call count, fallbacks, frozen runtime, plan freeze commit, manifest hash, seed and cell per attempt: " + ("PASS" if not any(": {" in p for p in r["problems"]) else "FAIL"),
              "- Event structure (count, three conditions, max depth, root set, served model on every event, no fallback-served event): " + ("PASS" if not any("events=" in p for p in r["problems"]) else "FAIL"),
              f"- Frozen runtime drift: {r['frozen_runtime_drift']}",
              "", "## Per-world raw hashes", ""]
    for set_id, s in r["sets"].items():
        lines += [f"### `{set_id}`", "", "| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |", "|---:|---|---|---|---|---|---|---|"]
        for w in s["worlds"]:
            h = w["raw_file_sha256"] or {}
            lines.append(f"| {w['execution_order']} | `{w['canonical_id']}` | {w['cell']} | {', '.join(w['attempts_present'])} | {', '.join(w['complete'])} | `{h.get('events.jsonl', '')[:12]}` | `{h.get('summary.csv', '')[:12]}` | `{h.get('run_metadata.json', '')[:12]}` |")
        lines.append("")
    if r["problems"]:
        lines += ["## Problems", ""] + [f"- {p}" for p in r["problems"]] + [""]
    lines += ["## Scientific boundary", "", r["scientific_boundary"], "",
              "## Replication start condition", "",
              ("A PASS here means this stage's data collection is complete. Under the frozen plan, the replication stage "
               "(Set 002) starts after Set 001 passes this audit and before any primary-outcome audit of Set 001, so that "
               "Set 002 runs regardless of what Set 001 shows. Gate closure requires both stages."), ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--archive-root", type=Path, default=None)
    parser.add_argument("--preflight", action="store_true", help="audit a stub preflight tree instead of a live archive")
    parser.add_argument("--out-dir", type=Path, default=None, help="default experiments/EXP_003/audits/gate_<x>/")
    args = parser.parse_args()
    archive_root = args.archive_root or (EXP003 / "results" / "preflight" if args.preflight else DEFAULT_ARCHIVE_ROOT)
    report = audit_stage(args.plan, args.stage, archive_root, preflight=args.preflight)
    out_dir = args.out_dir or (EXP003 / "audits" / f"gate_{report['gate'].lower()}")
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"EXP_003_GATE_{report['gate']}_{report['stage'].upper()}_CORPUS_AUDIT_v0.1"
    (out_dir / f"{stem}.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (out_dir / f"{stem}.md").write_text(render_markdown(report), encoding="utf-8")
    print(f"{report['status']}: {report['totals']['complete_worlds']}/{report['totals']['planned_worlds']} worlds complete, "
          f"{report['totals']['actual_calls']} calls, {report['totals']['failure_records']} failure record(s)")
    for p in report["problems"]:
        print(" -", p)
    print(f"wrote {out_dir / stem}.json and .md")
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
