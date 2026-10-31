"""EXP-003 Gate 3B synthesis (mechanical, cross-stage, read-only).

Reads the two committed Gate 3B stage primary-outcome audits (spec EXP-003-GATE-3B-PRIMARY-
OUTCOME-AUDIT-SPEC-v0.1), places them side by side, assesses the one cross-stage expectation
(E7: Set 002 reproduces the Set 001 direction in every matrix cell) by the spec's rule, and
writes experiments/EXP_003/audits/gate_3b/EXP_003_GATE_3B_SYNTHESIS_v0.1.{json,md}.

It introduces no new quantity: every number is copied from the audit records it names, by
their sha256. Stages stay separate (two columns, never a pooled one); the dual-root arm's
agreeing and conflicting strata stay separate. The secondary placement beside the Gate 3A
bounce and ring positions copies the committed Gate 3A audits and carries no verdict. No
test, no threshold beyond the spec's flat band. The relation of these findings to the
hypothesis is written separately, by a person, under research/observations/.

Usage:
    python -m experiments.EXP_003.tools.gate3b_synthesis
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..gate_orchestrator import PROJECT_ROOT
from .corpus_audit import git_output, portable_path, sha256_file
from .primary_outcome_audit import output_paths

EXP003 = Path(__file__).resolve().parents[1]
AUDITS = EXP003 / "audits" / "gate_3b"
AUDITS_3A = EXP003 / "audits" / "gate_3a"
STAGE_FILES = {
    "set_001": AUDITS / "EXP_003_GATE_3B_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1.json",
    "set_002": AUDITS / "EXP_003_GATE_3B_SET_002_PRIMARY_OUTCOME_AUDIT_v0.1.json",
}
GATE3A_FILES = {
    "set_001": AUDITS_3A / "EXP_003_GATE_3A_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1.json",
    "set_002": AUDITS_3A / "EXP_003_GATE_3A_SET_002_PRIMARY_OUTCOME_AUDIT_v0.1.json",
}
SPEC_VERSION = "EXP-003-GATE-3B-PRIMARY-OUTCOME-AUDIT-SPEC-v0.1"
E7_FLAT_BAND = 0.005   # spec 6, E7: stage means within ±.005 of zero count as flat
EXPECTATIONS = ("E1", "E2", "E3", "E4", "E5", "E6")
# The six matrix cells of E7: (key, label, arm selector, condition, stratum, quantity).
E7_CELLS = (
    ("arm1_free", "Arm 1 FREE", "arm1", "free", "None", "mean_certainty_excess"),
    ("arm1_lineage", "Arm 1 LINEAGE", "arm1", "lineage", "None", "mean_certainty_excess"),
    ("arm2_agreeing_free", "Arm 2 agreeing FREE", "arm2", "free", "agreeing", "mean_certainty_excess"),
    ("arm2_agreeing_lineage", "Arm 2 agreeing LINEAGE", "arm2", "lineage", "agreeing", "mean_certainty_excess"),
    ("arm2_conflicting_free", "Arm 2 conflicting FREE", "arm2", "free", "conflicting", "mean_departure_toward_e1"),
    ("arm2_conflicting_lineage", "Arm 2 conflicting LINEAGE", "arm2", "lineage", "conflicting", "mean_departure_toward_e1"),
)


def _find_set(report: dict[str, Any], **match: Any) -> str | None:
    for set_id, s in report["sets"].items():
        if all(s.get(k) == v for k, v in match.items()):
            return set_id
    return None


def _arm(report: dict[str, Any], which: str) -> str | None:
    if which == "arm1":
        return _find_set(report, topology="diamond", root_mode="single", probe=True)
    if which == "arm2":
        return _find_set(report, topology="diamond", root_mode="dual", probe=True)
    if which == "arm3":
        return _find_set(report, topology="solo")
    return _find_set(report, topology="diamond", root_mode="single", probe=False)


def cell_mean(report: dict[str, Any], arm: str, condition: str, stratum: str, quantity: str) -> float | None:
    """The stage mean of the cell's quantity over all D firings of the arm and stratum, as the
    stage audit recorded it (events-weighted, never pooled across strata)."""
    set_id = _arm(report, arm)
    if not set_id:
        return None
    return report["arm_aggregates"][set_id]["conditions"][condition].get(stratum, {}).get("D", {}).get(quantity)


def sign(value: float | None) -> str:
    if value is None:
        return "n/a"
    if abs(value) <= E7_FLAT_BAND:
        return "flat"
    return "positive" if value > 0 else "negative"


def e7(stages: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Spec 6, E7: contradicted if any cell is positive in one stage and negative in the other."""
    names = list(stages)
    cells = []
    reversed_cells = []
    for key, label, arm, condition, stratum, quantity in E7_CELLS:
        means = {n: cell_mean(stages[n], arm, condition, stratum, quantity) for n in names}
        signs = {n: sign(means[n]) for n in names}
        reversed_ = {"positive", "negative"} <= set(signs.values())
        if reversed_:
            reversed_cells.append(key)
        cells.append({"cell": key, "label": label, "quantity": quantity, "means": means, "signs": signs, "reversed": reversed_})
    assessable = all(c["signs"][n] != "n/a" for c in cells for n in names)
    verdict = "contradicted" if reversed_cells else ("consistent" if assessable else "not assessable")
    return {"verdict": verdict, "flat_band": E7_FLAT_BAND, "cells": cells, "reversed_cells": reversed_cells,
            "rule": ("per cell, the sign of the stage mean (certainty excess, or departure toward E1's state for the "
                     "conflicting cells), means within ±.005 of zero counted as flat; contradicted if any cell is positive "
                     "in one stage and negative in the other")}


def closure_rule(stages: dict[str, dict[str, Any]], corpus: dict[str, dict[str, Any]] | None,
                 bridge_present: bool) -> dict[str, str]:
    """The plan's closure rule ('Closure as Gate 3A'), each line computed from the records."""
    names = list(stages)
    frozen = all(stages[n]["plan_status"] == "FROZEN" and all(stages[n]["anchors"].values()) for n in names)
    planned = complete = failures = 0
    statuses = []
    if corpus:
        for n in names:
            c = corpus.get(n)
            if c is None:
                statuses.append(f"{n}: no corpus audit supplied")
                continue
            statuses.append(f"{n}: {c.get('status')}")
            planned += c["totals"]["planned_worlds"]
            complete += c["totals"]["complete_worlds"]
            failures += c["totals"]["failure_records"]
    corpus_ok = bool(corpus) and all(corpus.get(n, {}).get("status") == "PASS" for n in names) and planned == complete
    contradicted = sum(1 for n in names for k in EXPECTATIONS if stages[n]["expectations"][k]["verdict"] == "contradicted")
    return {
        "both stages' manifests prospectively frozen":
            ("yes" if frozen else "NO") + ": plan status " + ", ".join(sorted({stages[n]["plan_status"] for n in names}))
            + ", anchors " + ("all filled" if frozen else "incomplete"),
        "every world in all six arms has a valid archived execution or a documented technical failure":
            ("yes" if corpus_ok else "NO") + f": corpus audits {'; '.join(statuses) or 'absent'}, {complete}/{planned} complete, "
            f"{failures} technical failure record(s) preserved",
        "raw outputs immutable":
            ("yes" if corpus_ok else "NO") + ": SHA-256 per raw file recorded in each corpus audit and re-checked by each primary-outcome audit",
        "predefined primary outcomes audited":
            f"yes: {len(names)} stage audit(s) under " + ", ".join(sorted({stages[n]["spec_version"] for n in names})),
        "arms, stages and strata reported separately":
            "yes: per-arm, per-stratum tables in each stage audit; this synthesis keeps one column per stage",
        "Gate 3A comparison recorded as a secondary placement":
            ("yes: Gate 3A bounce and ring positions copied from the committed Gate 3A audits, no verdict" if bridge_present
             else "NO: Gate 3A primary-outcome audits not supplied"),
        "negative results retained":
            f"yes: {contradicted} contradicted expectation verdict(s) across the stages stand as written",
    }


def _kc(c: dict[str, Any] | None) -> dict[str, Any] | None:
    if not c:
        return None
    return {k: c.get(k) for k in ("events", "discount", "inflation", "at_reference", "departure_from_even_events",
                                  "mean_certainty_excess", "mean_departure_toward_e1", "fis_positive_events",
                                  "mean_reported_distinct_sources")}


def gate3a_bridge(gate3a: dict[str, dict[str, Any]] | None, stages: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Spec 7: Gate 3B D and A positions beside the Gate 3A bounce and ring A positions. Copied
    counts only. Gate 3A ran probe off, so the probe-off arm is the only like-for-like bridge."""
    rows: list[dict[str, Any]] = []
    if gate3a:
        for n, rep in gate3a.items():
            for set_id, s in rep["sets"].items():
                if s["topology"] not in ("bounce", "ring"):
                    continue
                for condition, c in rep["arm_aggregates"][set_id]["conditions"].items():
                    a = c["agents"].get("A") or {}
                    rows.append({"gate": "3A", "stage": n, "set": set_id, "topology": s["topology"], "probe": False,
                                 "condition": condition, "position": "A post-seed",
                                 "counts": {"events": a.get("events"), "discount": a.get("discount_events"),
                                            "inflation": a.get("inflation_events"), "at_reference": a.get("at_reference_events")}})
    for n, rep in stages.items():
        for arm, probe in (("arm4", False), ("arm1", True)):
            set_id = _arm(rep, arm)
            if not set_id:
                continue
            for condition, strata in rep["arm_aggregates"][set_id]["conditions"].items():
                c = strata.get("None", {})
                for position, key in (("D", "D"), ("A post-seed", "A_post_seed")):
                    k = c.get(key) or {}
                    rows.append({"gate": "3B", "stage": n, "set": set_id, "topology": "diamond", "probe": probe,
                                 "condition": condition, "position": position,
                                 "counts": {"events": k.get("events"), "discount": k.get("discount"),
                                            "inflation": k.get("inflation"), "at_reference": k.get("at_reference")}})
    return rows


def synthesize(stages: dict[str, dict[str, Any]], sources: dict[str, dict[str, str]] | None = None,
               corpus: dict[str, dict[str, Any]] | None = None,
               gate3a: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    names = list(stages)
    expectations: dict[str, Any] = {}
    for key in EXPECTATIONS:
        per = {n: stages[n]["expectations"][key] for n in names}
        verdicts = {n: per[n]["verdict"] for n in names}
        expectations[key] = {"verdicts": verdicts, "agree": len(set(verdicts.values())) == 1,
                             "quantities": {n: {k: v for k, v in per[n].items() if k != "verdict"} for n in names}}
    expectations["E7"] = e7(stages)

    # Arm aggregates per stage, condition and stratum (D and A post-seed), copied.
    aggregates = []
    for n in names:
        for set_id, agg in stages[n]["arm_aggregates"].items():
            for condition, strata in agg["conditions"].items():
                for stratum, v in strata.items():
                    aggregates.append({"stage": n, "set": set_id, "topology": agg["topology"], "root_mode": agg["root_mode"],
                                       "probe": agg["probe"], "condition": condition, "stratum": stratum, "worlds": v["worlds"],
                                       "D": _kc(v.get("D")), "A_post_seed": _kc(v.get("A_post_seed"))})

    # Probe reactivity and solo control per stage, copied.
    probe = {n: {"comparisons": len(stages[n]["probe_reactivity"]),
                 "gaps_over_tolerance": sum(1 for r in stages[n]["probe_reactivity"] if not r["within_tolerance"]),
                 "gaps": [{"seed": r["seed"], "condition": r["condition"], "gap": r["gap"]} for r in stages[n]["probe_reactivity"]]}
             for n in names}
    solo = {n: {"world_conditions": len(stages[n]["solo_control"]),
                "with_any_deviation": sum(1 for r in stages[n]["solo_control"] if r["any_deviation"]),
                "fis_positive_events": sum(r["fis_positive_events"] for r in stages[n]["solo_control"]),
                "firings": sum(len(r["certainty_excess_sequence"]) for r in stages[n]["solo_control"])}
            for n in names}

    # Secondary inbound-naming table per stage, copied (descriptive, no verdict).
    inbound = {n: stages[n]["secondary_inbound_naming"] for n in names}

    # Final state per stage.
    final = []
    for n in names:
        fam = stages[n]["family"]
        aligned = [r for r in fam if r["cell"].split("/")[0] == r["cell"].split("/")[1]]
        misleading = [r for r in fam if r["cell"].split("/")[0] != r["cell"].split("/")[1]]
        conf: dict[str, int] = {}
        for r in fam:
            k = f"{r['final_confidence']:.2f}"
            conf[k] = conf.get(k, 0) + 1
        final.append({"stage": n, "world_conditions": len(fam),
                      "final_answer_differs_from_E1": sum(1 for r in fam if r["final_answer"] != r["cell"].split("/")[1]),
                      "final_confidence_distribution": dict(sorted(conf.items())),
                      "accuracy_by_E1_alignment": {"aligned": f"{sum(r['accuracy'] for r in aligned)}/{len(aligned)}",
                                                   "misleading": f"{sum(r['accuracy'] for r in misleading)}/{len(misleading)}"},
                      "macro_stop_triggered": sum(1 for m in stages[n]["macro_boundary"] if m["macro_stop_triggered"]),
                      "macro_worlds": len(stages[n]["macro_boundary"]),
                      "macro_all_responses_reused": sum(1 for m in stages[n]["macro_boundary"] if m["all_responses_reused"]),
                      "strata": {s: stages[n]["sets"][s]["strata"] for s in stages[n]["sets"]}})

    bridge = gate3a_bridge(gate3a, stages)
    report = {
        "experiment": "EXP-003", "gate": "3B", "kind": "SYNTHESIS", "version": "v0.1",
        "sources": sources or {}, "head_commit": git_output(["rev-parse", "HEAD"], PROJECT_ROOT),
        "spec_versions": sorted({stages[n]["spec_version"] for n in names}),
        "expectations": expectations, "arm_aggregates": aggregates, "probe_reactivity": probe, "solo_control": solo,
        "secondary_inbound_naming": inbound, "final_state": final,
        "gate3a_bridge": bridge,
        "closure_rule": closure_rule(stages, corpus, bool(gate3a)),
        "boundary": ("Mechanical cross-stage placement of two pre-registered audits. No pooling of stages or strata, no test, "
                     "no threshold beyond the spec's E7 flat band, no causal claim. The Gate 3A placement is secondary and "
                     "carries no verdict. The relation to the hypothesis is written separately under research/observations/."),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    return report


def _f(x: Any) -> str:
    if x is None:
        return "n/a"
    return f"{x:+.3f}" if isinstance(x, float) else str(x)


def _cnt(c: dict[str, Any] | None) -> str:
    if not c or not c.get("events"):
        return "n/a"
    base = f"{c['discount']}d/{c['inflation']}i/{c['at_reference']}r of {c['events']}"
    if c.get("departure_from_even_events"):
        base += f" (+{c['departure_from_even_events']} even; dep {_f(c['mean_departure_toward_e1'])})"
    return base + f"; FIS>0 {c['fis_positive_events']}; x̄ {_f(c['mean_certainty_excess'])}"


def render_markdown(r: dict[str, Any]) -> str:
    names = list(r["expectations"]["E1"]["verdicts"])
    L = ["# EXP-003 Gate 3B Synthesis v0.1", "", "## Status", "", "**SYNTHESIS** (mechanical, cross-stage)", "", r["boundary"], "",
         "## Sources", ""]
    for name, src in r["sources"].items():
        L.append(f"- {name}: `{src['path']}` (sha256 `{src['sha256']}`)")
    L += [f"- HEAD at synthesis time: `{r['head_commit']}`", "",
          "## Pre-registered expectations, both stages", "",
          "| Id | " + " | ".join(names) + " | Agree |", "|---|" + "---|" * (len(names) + 1)]
    for key in EXPECTATIONS:
        e = r["expectations"][key]
        L.append(f"| {key} | " + " | ".join(f"**{e['verdicts'][n]}**" for n in names) + f" | {'yes' if e['agree'] else 'no'} |")
    e7_ = r["expectations"]["E7"]
    L.append(f"| E7 | " + " | ".join("cross-stage" for _ in names) + f" | **{e7_['verdict']}** |")
    L += ["", f"E7 by matrix cell (stage mean of the cell quantity; flat band ±{e7_['flat_band']}):", "",
          "| Cell | Quantity | " + " | ".join(names) + " | Signs | Reversed |", "|---|---|" + "---:|" * len(names) + "---|---|"]
    for c in e7_["cells"]:
        L.append(f"| {c['label']} | {c['quantity']} | " + " | ".join(_f(c['means'][n]) for n in names)
                 + f" | {' / '.join(c['signs'][n] for n in names)} | {'YES' if c['reversed'] else 'no'} |")
    L += ["", "Quantities behind each stage verdict:", ""]
    for key in EXPECTATIONS:
        for n in names:
            L.append(f"- {key} {n}: `{json.dumps(r['expectations'][key]['quantities'][n], default=str)}`")
    L += ["", "## Arm aggregates by stage (d = discount, i = inflation, r = at reference; strata separate)", "",
          "| Stage | Set | Condition | Stratum | Worlds | D | A post-seed |", "|---|---|---|---|---:|---|---|"]
    for a in r["arm_aggregates"]:
        L.append(f"| {a['stage']} | `{a['set']}` | {a['condition']} | {a['stratum']} | {a['worlds']} | {_cnt(a['D'])} | {_cnt(a['A_post_seed'])} |")
    L += ["", "## Probe reactivity (Arm 4 vs Arm 1) and solo control, by stage", "",
          "| Stage | Probe comparisons | Gaps over .02 | Solo world×conditions | Solo with any deviation | Solo FIS>0 events / firings |",
          "|---|---:|---:|---:|---:|---|"]
    for n in names:
        p, s = r["probe_reactivity"][n], r["solo_control"][n]
        L.append(f"| {n} | {p['comparisons']} | {p['gaps_over_tolerance']} | {s['world_conditions']} | {s['with_any_deviation']} | {s['fis_positive_events']} / {s['firings']} |")
    L += ["", "## Secondary: inbound messages naming the sensor, by stage (descriptive, no verdict)", "",
          "| Stage | Set | Condition | Stratum | Position | Inbound naming the sensor | Counts |", "|---|---|---|---|---|---:|---|"]
    for n in names:
        for sid, per in r["secondary_inbound_naming"][n].items():
            for condition, strata in per.items():
                for stratum, tabs in strata.items():
                    for pos, key in (("D", "D_by_inbound_naming_sensor"), ("A", "A_by_inbound_naming_sensor")):
                        for k, c in tabs[key].items():
                            L.append(f"| {n} | `{sid}` | {condition} | {stratum} | {pos} | {k} | {_cnt(c)} |")
    L += ["", "## Final state", "",
          "| Stage | World×conditions | Final answer ≠ E1 | Final confidence | Accuracy aligned / misleading (truth vs E1) | MACRO stop triggered | MACRO responses all reused |",
          "|---|---:|---:|---|---|---|---|"]
    for f in r["final_state"]:
        L.append(f"| {f['stage']} | {f['world_conditions']} | {f['final_answer_differs_from_E1']} | {f['final_confidence_distribution']} | "
                 f"{f['accuracy_by_E1_alignment']['aligned']} / {f['accuracy_by_E1_alignment']['misleading']} | "
                 f"{f['macro_stop_triggered']}/{f['macro_worlds']} | {f['macro_all_responses_reused']}/{f['macro_worlds']} |")
    L += ["", "## Secondary: Gate 3B positions beside the Gate 3A bounce and ring (copied counts, no verdict)", ""]
    if r["gate3a_bridge"]:
        L += ["Gate 3A ran probe off; the Gate 3B probe-off arm is the only like-for-like bridge.", "",
              "| Gate | Stage | Set | Topology | Probe | Condition | Position | Events | d | i | r |", "|---|---|---|---|---|---|---|---:|---:|---:|---:|"]
        for b in r["gate3a_bridge"]:
            c = b["counts"]
            L.append(f"| {b['gate']} | {b['stage']} | `{b['set']}` | {b['topology']} | {'on' if b['probe'] else 'off'} | {b['condition']} | {b['position']} | "
                     f"{c['events']} | {c['discount']} | {c['inflation']} | {c['at_reference']} |")
    else:
        L.append("Gate 3A primary-outcome audits not supplied; no placement.")
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
        corpus_path = AUDITS / f"EXP_003_GATE_3B_{name.upper()}_CORPUS_AUDIT_v0.1.json"
        if not corpus_path.exists():
            raise SystemExit(f"missing corpus audit: {corpus_path}")
        if sha256_file(corpus_path) != stages[name]["corpus_audit"]["sha256"]:
            raise SystemExit(f"{corpus_path}: sha256 differs from the one recorded in the {name} primary-outcome audit; refusing")
        corpus[name] = json.loads(corpus_path.read_text(encoding="utf-8"))
        sources[f"{name}_corpus"] = {"path": portable_path(corpus_path), "sha256": sha256_file(corpus_path)}
    gate3a: dict[str, dict[str, Any]] = {}
    for name, path in GATE3A_FILES.items():
        if path.exists():
            gate3a[name] = json.loads(path.read_text(encoding="utf-8"))
            sources[f"gate3a_{name}"] = {"path": portable_path(path), "sha256": sha256_file(path)}
    report = synthesize(stages, sources, corpus, gate3a or None)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    json_path, md_path = output_paths(args.out_dir / "EXP_003_GATE_3B_SYNTHESIS_v0.1")
    json_path.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    e = report["expectations"]
    print("SYNTHESIS written: " + ", ".join(f"{k}=" + "/".join(e[k]["verdicts"].values()) for k in EXPECTATIONS)
          + f", E7={e['E7']['verdict']}")
    print(f"wrote {json_path} and {md_path}")


if __name__ == "__main__":
    main()
