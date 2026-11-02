"""EXP-003 Gate 3C synthesis (mechanical, cross-stage, read-only).

Reads the two committed Gate 3C stage primary-outcome audits, places them side by side, assesses
the one cross-stage expectation E7 (Set 002 keeps the direction of all ten within-detached far-
position cells of Set 001) by the spec's rule, prints the Set 002 paired verdicts in a separate
table labelled as historical-control evidence beside the Set 001 drift gauge, and computes the
closure rule from the records. Every number is copied from the audits it names, by sha256.
Stages are never pooled; nothing is corrected for drift.

Usage:
    python -m experiments.EXP_003.tools.gate3c_synthesis
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..gate_orchestrator import PROJECT_ROOT
from .corpus_audit import git_output, portable_path, sha256_file
from .gate3c_primary_outcome_audit import FLAT_BAND, SPEC_VERSION
from .primary_outcome_audit import output_paths

EXP003 = Path(__file__).resolve().parents[1]
AUDITS = EXP003 / "audits" / "gate_3c"
STAGE_FILES = {
    "set_001": AUDITS / "EXP_003_GATE_3C_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1.json",
    "set_002": AUDITS / "EXP_003_GATE_3C_SET_002_PRIMARY_OUTCOME_AUDIT_v0.1.json",
}
SHAPES = ("ring", "solo", "dyad", "bounce", "diamond")
CONDITIONS = ("free", "lineage")
SINGLE_STAGE = ("E1", "E2", "E3a", "E3b", "E4", "E5", "E6")
PAIRED = ("E1", "E3a", "E3b")   # twin-dependent; qualified in Set 002


def _sign(x: float | None) -> str:
    if x is None:
        return "n/a"
    if abs(x) <= FLAT_BAND:
        return "flat"
    return "positive" if x > 0 else "negative"


def detached_arm(report: dict[str, Any], shape: str) -> tuple[str, dict[str, Any]] | None:
    for sid, e in report["arms"].items():
        if e.get("detached") and e.get("base") == shape:
            return sid, e
    return None


def e7(stages: dict[str, dict[str, Any]]) -> dict[str, Any]:
    names = list(stages)
    cells, reversed_cells = [], []
    for shape in SHAPES:
        for condition in CONDITIONS:
            means = {}
            for n in names:
                arm = detached_arm(stages[n], shape)
                means[n] = arm[1]["far"][condition]["far_stage_mean_excess"] if arm else None
            signs = {n: _sign(means[n]) for n in names}
            rev = {"positive", "negative"} <= set(signs.values())
            key = f"{shape}_{condition}"
            if rev:
                reversed_cells.append(key)
            cells.append({"cell": key, "shape": shape, "condition": condition, "means": means, "signs": signs, "reversed": rev})
    assessable = all(c["signs"][n] != "n/a" for c in cells for n in names)
    return {"verdict": "contradicted" if reversed_cells else ("consistent" if assessable else "not assessable"),
            "flat_band": FLAT_BAND, "cells": cells, "reversed_cells": reversed_cells,
            "rule": "ten within-detached cells: sign of the stage mean certainty excess at the far position per shape and condition, "
                    "means within ±.005 counted as flat; contradicted if any cell is positive in one stage and negative in the other"}


def descriptive_replication(stages: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    names = list(stages)
    rows = []
    for shape in SHAPES:
        for condition in CONDITIONS:
            comp = {}
            for n in names:
                arm = detached_arm(stages[n], shape)
                comp[n] = arm[1]["far"][condition]["far_stage_mean_last_minus_first"] if arm else None
            rows.append({"quantity": "far-agent compounding (mean last − first)", "shape": shape, "condition": condition,
                         "values": comp, "signs": {n: _sign(v) for n, v in comp.items()}})
        e6 = {}
        for n in names:
            arm = detached_arm(stages[n], shape)
            e6[n] = arm[1]["E6"]["verdict"] if arm and "E6" in arm[1] else None
        if any(v is not None for v in e6.values()):
            rows.append({"quantity": "E6 strict verdict", "shape": shape, "condition": "lineage", "values": e6, "signs": {}})
    return rows


def closure_rule(stages: dict[str, dict[str, Any]], corpus: dict[str, dict[str, Any]]) -> dict[str, str]:
    names = list(stages)
    frozen = all(stages[n]["plan_status"] == "FROZEN" and all(stages[n]["anchors"].values()) for n in names)
    planned = complete = failures = 0
    statuses = []
    for n in names:
        c = corpus.get(n)
        if c is None:
            statuses.append(f"{n}: no corpus audit supplied")
            continue
        statuses.append(f"{n}: {c.get('status')}")
        planned += c["totals"]["planned_worlds"]; complete += c["totals"]["complete_worlds"]; failures += c["totals"]["failure_records"]
    corpus_ok = bool(corpus) and all(corpus.get(n, {}).get("status") == "PASS" for n in names) and planned == complete
    manip_ok = all(m["status"] == "PASS" for n in names for m in stages[n]["manipulation_check"].values())
    contradicted = sum(1 for n in names for k in SINGLE_STAGE if stages[n]["expectations"][k]["verdict"] == "contradicted")
    gauge = stages["set_001"].get("drift_gauge") if "set_001" in stages else None
    return {
        "both stages' manifests prospectively frozen": ("yes" if frozen else "NO") + ": plan status " + ", ".join(sorted({stages[n]["plan_status"] for n in names})),
        "every world in all fourteen arms has a valid archived execution or a documented technical failure":
            ("yes" if corpus_ok else "NO") + f": corpus audits {'; '.join(statuses)}, {complete}/{planned} complete, {failures} technical failure record(s) preserved",
        "raw outputs immutable": ("yes" if corpus_ok else "NO") + ": SHA-256 per raw file recorded in each corpus audit and re-checked by each primary-outcome audit, twins included",
        "manipulation check passed in every detached arm": "yes" if manip_ok else "NO",
        "predefined primary outcomes audited": f"yes: {len(names)} stage audit(s) under " + ", ".join(sorted({stages[n]['spec_version'] for n in names})),
        "arms, stages, conditions and agents reported separately; twins dated": "yes: per-arm tables in each stage audit; this synthesis keeps one column per stage",
        "drift gauge recorded": (f"yes: {gauge['status']} ({gauge['wording']})" if gauge else "NO: no drift gauge in Set 001"),
        "Set 002 paired verdicts qualified as historical-control evidence, never pooled or corrected": "yes",
        "negative results retained": f"yes: {contradicted} contradicted single-stage expectation verdict(s) stand as written",
    }


def synthesize(stages: dict[str, dict[str, Any]], sources: dict[str, dict[str, str]] | None = None,
               corpus: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    names = list(stages)
    expectations: dict[str, Any] = {}
    for key in SINGLE_STAGE:
        per = {n: stages[n]["expectations"][key] for n in names}
        expectations[key] = {"verdicts": {n: per[n]["verdict"] for n in names},
                             "agree": len({per[n]["verdict"] for n in names}) == 1,
                             "standing": ({n: ("primary (same-window twins)" if n == "set_001" else "qualified (historical twins)") for n in names}
                                          if key in PAIRED else {n: "primary (within-detached)" for n in names}),
                             "quantities": {n: {k: v for k, v in per[n].items() if k != "verdict"} for n in names}}
    expectations["E7"] = e7(stages)
    qualified = {n: {k: stages[n]["expectations"][k]["verdict"] for k in PAIRED} for n in names if n != "set_001"}
    report = {
        "experiment": "EXP-003", "gate": "3C", "kind": "SYNTHESIS", "version": "v0.1",
        "sources": sources or {}, "head_commit": git_output(["rev-parse", "HEAD"], PROJECT_ROOT),
        "spec_versions": sorted({stages[n]["spec_version"] for n in names}),
        "expectations": expectations,
        "descriptive_replication": descriptive_replication(stages),
        "set_002_paired_qualified": {"verdicts": qualified, "set_001_drift_gauge": stages.get("set_001", {}).get("drift_gauge"),
                                     "note": "Set 002 pairs are against historical controls and are not same-window evidence; never pooled with Set 001, never corrected by the gauge."},
        "twins": {n: {sid: e.get("twin") for sid, e in stages[n]["arms"].items() if e.get("twin")} for n in names},
        "closure_rule": closure_rule(stages, corpus or {}),
        "boundary": ("Mechanical cross-stage placement of two pre-registered audits. No pooling of stages or arms, no test, no threshold beyond "
                     "the spec's flat band, no drift correction, no causal or mechanism claim, nothing on H2. The relation to the hypothesis is "
                     "written separately under research/observations/."),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    return report


def _f(x: Any) -> str:
    if x is None:
        return "n/a"
    return f"{x:+.3f}" if isinstance(x, float) else str(x)


def render_markdown(r: dict[str, Any]) -> str:
    names = list(r["expectations"]["E1"]["verdicts"])
    L = ["# EXP-003 Gate 3C Synthesis v0.1", "", "## Status", "", "**SYNTHESIS** (mechanical, cross-stage)", "", r["boundary"], "", "## Sources", ""]
    for name, src in r["sources"].items():
        L.append(f"- {name}: `{src['path']}` (sha256 `{src['sha256']}`)")
    L += [f"- HEAD at synthesis time: `{r['head_commit']}`", "", "## Pre-registered expectations, both stages", "",
          "| Id | " + " | ".join(names) + " | Agree | Standing |", "|---|" + "---|" * (len(names) + 2)]
    for key in SINGLE_STAGE:
        e = r["expectations"][key]
        L.append(f"| {key} | " + " | ".join(f"**{e['verdicts'][n]}**" for n in names) + f" | {'yes' if e['agree'] else 'no'} | " + "; ".join(f"{n}: {s}" for n, s in e["standing"].items()) + " |")
    e7_ = r["expectations"]["E7"]
    L.append(f"| E7 | " + " | ".join("cross-stage" for _ in names) + f" | **{e7_['verdict']}** | within-detached |")
    L += ["", f"E7 cells (stage mean certainty excess at the far position; flat band ±{e7_['flat_band']}):", "",
          "| Cell | " + " | ".join(names) + " | Signs | Reversed |", "|---|" + "---:|" * len(names) + "---|---|"]
    for c in e7_["cells"]:
        L.append(f"| {c['cell']} | " + " | ".join(_f(c['means'][n]) for n in names) + f" | {' / '.join(c['signs'][n] for n in names)} | {'YES' if c['reversed'] else 'no'} |")
    L += ["", "## Descriptive replication (no verdict)", "", "| Quantity | Shape | Condition | " + " | ".join(names) + " |", "|---|---|---|" + "---|" * len(names)]
    for row in r["descriptive_replication"]:
        L.append(f"| {row['quantity']} | {row['shape']} | {row['condition']} | " + " | ".join(_f(row['values'][n]) if not isinstance(row['values'][n], str) else row['values'][n] for n in names) + " |")
    q = r["set_002_paired_qualified"]
    L += ["", "## Set 002 paired verdicts (historical controls, qualified)", "", q["note"], ""]
    if q["verdicts"]:
        L += ["| Stage | E1 | E3a | E3b | Set 001 drift gauge |", "|---|---|---|---|---|"]
        for n, v in q["verdicts"].items():
            g = q["set_001_drift_gauge"]
            L.append(f"| {n} | {v['E1']} | {v['E3a']} | {v['E3b']} | {g['status'] if g else 'none'} |")
    L += ["", "## Twins and temporal gaps", "", "| Stage | Set | Twin | Kind | Twin dates | Max gap (days) |", "|---|---|---|---|---|---:|"]
    for n, twins in r["twins"].items():
        for sid, t in twins.items():
            L.append(f"| {n} | `{sid}` | {t.get('set_id')} | {t.get('kind', t.get('role', ''))} | {', '.join(t.get('twin_dates', []))} | {t.get('gap_days_max', '')} |")
    L += ["", "## Closure rule", "", "| Requirement | Status |", "|---|---|"]
    for k, v in r["closure_rule"].items():
        L.append(f"| {k} | {v} |")
    L += ["", "## Boundary", "", r["boundary"], ""]
    return "\n".join(L)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=AUDITS)
    args = parser.parse_args()
    stages: dict[str, dict[str, Any]] = {}
    corpus: dict[str, dict[str, Any]] = {}
    sources: dict[str, dict[str, str]] = {}
    for name, path in STAGE_FILES.items():
        if not path.exists():
            raise SystemExit(f"missing stage audit: {path}")
        stages[name] = json.loads(path.read_text(encoding="utf-8"))
        if stages[name].get("status") != "COMPLETE":
            raise SystemExit(f"{path}: status {stages[name].get('status')!r} is not COMPLETE; refusing")
        if stages[name].get("spec_version") != SPEC_VERSION:
            raise SystemExit(f"{path}: spec_version {stages[name].get('spec_version')!r} is not {SPEC_VERSION}; refusing")
        sources[name] = {"path": portable_path(path), "sha256": sha256_file(path)}
        corpus_path = AUDITS / f"EXP_003_GATE_3C_{name.upper()}_CORPUS_AUDIT_v0.1.json"
        if not corpus_path.exists():
            raise SystemExit(f"missing corpus audit: {corpus_path}")
        if sha256_file(corpus_path) != stages[name]["corpus_audit"]["sha256"]:
            raise SystemExit(f"{corpus_path}: sha256 differs from the one recorded in the {name} primary-outcome audit; refusing")
        corpus[name] = json.loads(corpus_path.read_text(encoding="utf-8"))
        sources[f"{name}_corpus"] = {"path": portable_path(corpus_path), "sha256": sha256_file(corpus_path)}
    report = synthesize(stages, sources, corpus)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    json_path, md_path = output_paths(args.out_dir / "EXP_003_GATE_3C_SYNTHESIS_v0.1")
    json_path.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    e = report["expectations"]
    print("SYNTHESIS written: " + ", ".join(f"{k}=" + "/".join(e[k]["verdicts"].values()) for k in SINGLE_STAGE) + f", E7={e['E7']['verdict']}")
    print(f"wrote {json_path} and {md_path}")


if __name__ == "__main__":
    main()
