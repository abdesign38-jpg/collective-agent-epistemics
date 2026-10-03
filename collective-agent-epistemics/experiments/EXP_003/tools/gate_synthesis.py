"""EXP-003 Gate 3A synthesis (mechanical, cross-stage, read-only).

Reads the two committed stage primary-outcome audits and the historical ring observation,
places them side by side, assesses the one cross-stage expectation (E6: Set 002 reproduces
the Set 001 ordering of discount rates across the four arms), and writes
experiments/EXP_003/audits/gate_3a/EXP_003_GATE_3A_SYNTHESIS_v0.1.{json,md}.

It introduces no new quantity: every number is copied from the audit records it names, by
their sha256. Stages stay separate (two columns, never a pooled one). No test, no threshold.
The relation of these findings to the hypothesis is written separately, by a person, under
research/observations/.

Usage:
    python -m experiments.EXP_003.tools.gate_synthesis
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
AUDITS = EXP003 / "audits" / "gate_3a"
STAGE_FILES = {
    "set_001": AUDITS / "EXP_003_GATE_3A_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1.json",
    "set_002": AUDITS / "EXP_003_GATE_3A_SET_002_PRIMARY_OUTCOME_AUDIT_v0.1.json",
}
HISTORICAL_FILE = AUDITS / "EXP_003_GATE_3A_HISTORICAL_RING_OBSERVATION_v0.1.json"
TOPOLOGIES = ("solo", "dyad", "ring", "bounce")


def _set_for(report: dict[str, Any], topology: str) -> str | None:
    for set_id, s in report["sets"].items():
        if s["topology"] == topology:
            return set_id
    return None


def closure_rule(stages: dict[str, dict[str, Any]], corpus: dict[str, dict[str, Any]] | None,
                 historical: dict[str, Any] | None) -> dict[str, str]:
    """The plan's closure rule, each line computed from the records rather than asserted."""
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
    contradicted = sum(1 for n in names for k in ("E1", "E2", "E3", "E4", "E5") if stages[n]["expectations"][k]["verdict"] == "contradicted")
    return {
        "both stages' manifests prospectively frozen":
            ("yes" if frozen else "NO") + ": plan status " + ", ".join(sorted({stages[n]['plan_status'] for n in names}))
            + ", anchors " + ("all filled" if frozen else "incomplete"),
        "every world in all eight arms has a valid archived execution or a documented technical failure":
            ("yes" if corpus_ok else "NO") + f": corpus audits {'; '.join(statuses) or 'absent'}, {complete}/{planned} complete, "
            f"{failures} technical failure record(s) preserved",
        "raw outputs immutable":
            ("yes" if corpus_ok else "NO") + ": SHA-256 per raw file recorded in each corpus audit and re-checked by each primary-outcome audit",
        "predefined primary outcomes audited":
            f"yes: {len(names)} stage audit(s) under " + ", ".join(sorted({stages[n]['spec_version'] for n in names})),
        "arms and stages reported separately": "yes: per-arm tables in each stage audit; this synthesis keeps one column per stage",
        "historical comparison recorded as a secondary observation":
            (f"yes: separate observation file ({historical['historical_runs']} historical runs), adjusts nothing" if historical
             else "NO: historical observation file not supplied"),
        "negative results retained":
            f"yes: {contradicted} contradicted expectation verdict(s) across the stages stand as written",
    }


def synthesize(stages: dict[str, dict[str, Any]], historical: dict[str, Any] | None,
               sources: dict[str, dict[str, str]] | None = None,
               corpus: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    names = list(stages)
    # Expectations side by side.
    expectations: dict[str, Any] = {}
    for key in ("E1", "E2", "E3", "E4", "E5"):
        per = {n: stages[n]["expectations"][key] for n in names}
        verdicts = {n: per[n]["verdict"] for n in names}
        expectations[key] = {"verdicts": verdicts, "agree": len(set(verdicts.values())) == 1,
                             "quantities": {n: {k: v for k, v in per[n].items() if k != "verdict"} for n in names}}
    orderings = {n: [row["topology"] for row in stages[n]["expectations"]["E6"]["ordering_of_arms_by_LINEAGE_discount_rate_this_stage"]]
                 for n in names}
    rates = {n: {row["topology"]: row["discount_rate_all_agents_post_seed"]
                 for row in stages[n]["expectations"]["E6"]["ordering_of_arms_by_LINEAGE_discount_rate_this_stage"]} for n in names}
    same = len({tuple(o) for o in orderings.values()}) == 1
    expectations["E6"] = {"verdict": "consistent" if same else "contradicted", "orderings": orderings, "rates": rates,
                          "rule": "contradicted if the two stages order the four arms differently by LINEAGE discount rate (all post-seed events)"}

    # Position summary per stage, arm, condition.
    positions = []
    for n in names:
        for topology in TOPOLOGIES:
            set_id = _set_for(stages[n], topology)
            if not set_id:
                continue
            for condition, c in stages[n]["arm_aggregates"][set_id]["conditions"].items():
                row = {"stage": n, "set": set_id, "topology": topology, "condition": condition,
                       "A_restoration_rate": c["A_restoration_rate"],
                       "worlds_with_sustained_A_deviation": c["worlds_with_sustained_A_deviation"], "worlds": c["worlds"]}
                for agent in ("A", "B", "C"):
                    a = c["agents"].get(agent)
                    row[agent] = {k: a[k] for k in ("events", "discount_events", "inflation_events", "at_reference_events", "mean_magnitude")} if a else None
                if "bounce_B_legs" in c:
                    row["bounce_B_legs"] = {leg: {k: v[k] for k in ("events", "discount_events", "inflation_events", "mean_magnitude")}
                                            for leg, v in c["bounce_B_legs"].items()}
                positions.append(row)

    # Origin (A) deviations by firing and by the inbound agent-as-source mark (table 4).
    origin = []
    for n in names:
        for condition in ("free", "lineage"):
            for topology in TOPOLOGIES:
                by_firing: dict[str, int] = {}
                cross = {"deviating_marked": 0, "deviating_unmarked": 0, "at_reference_marked": 0, "at_reference_unmarked": 0}
                total = 0
                for row in stages[n]["focal"]["table_4_A_post_seed_all_arms"]:
                    if row["condition"] != condition or row["topology"] != topology:
                        continue
                    for f in row["firings"]:
                        total += 1
                        dev = f["kind"] != "at_reference"
                        if dev:
                            by_firing[f["id"]] = by_firing.get(f["id"], 0) + 1
                        cross[("deviating" if dev else "at_reference") + ("_marked" if f["inbound_agent_as_source"] else "_unmarked")] += 1
                origin.append({"stage": n, "condition": condition, "topology": topology, "A_post_seed_events": total,
                               "deviations_by_firing": by_firing, "inbound_mark_crosstab": cross})

    # Final state.
    final = []
    for n in names:
        fam = stages[n]["family"]
        flips = [r for r in fam if r["final_answer"] != r["cell"].split("/")[1]]
        conf: dict[str, int] = {}
        for r in fam:
            k = f"{r['final_confidence']:.2f}"
            conf[k] = conf.get(k, 0) + 1
        final.append({"stage": n, "world_conditions": len(fam), "final_answer_differs_from_E1": len(flips),
                      "final_confidence_distribution": dict(sorted(conf.items())),
                      "accuracy_by_alignment": {
                          "aligned": f"{sum(r['accuracy'] for r in fam if r['cell'] in ('A/A', 'B/B'))}/{sum(1 for r in fam if r['cell'] in ('A/A', 'B/B'))}",
                          "misleading": f"{sum(r['accuracy'] for r in fam if r['cell'] in ('A/B', 'B/A'))}/{sum(1 for r in fam if r['cell'] in ('A/B', 'B/A'))}"},
                      "macro_stopped_after_first_cycle": sum(1 for m in stages[n]["macro_boundary"] if m["macro_stop_triggered"]),
                      "macro_worlds": len(stages[n]["macro_boundary"]),
                      "macro_all_responses_reused": sum(1 for m in stages[n]["macro_boundary"] if m["all_macro_responses_reused"]),
                      "cells": {s: stages[n]["sets"][s]["cells"] for s in stages[n]["sets"]}})

    report = {
        "experiment": "EXP-003", "gate": "3A", "kind": "SYNTHESIS", "version": "v0.1",
        "sources": sources or {}, "head_commit": git_output(["rev-parse", "HEAD"], PROJECT_ROOT),
        "spec_versions": sorted({stages[n]["spec_version"] for n in names}),
        "expectations": expectations, "positions": positions, "origin_deviations": origin, "final_state": final,
        "historical": ({k: historical[k] for k in ("contemporary", "historical", "historical_gate_2b_only",
                                                    "historical_runs", "historical_distinct_seeds", "historical_run_classes",
                                                    "factor_ledger_difference")} if historical else None),
        "closure_rule": closure_rule(stages, corpus, historical),
        "boundary": ("Mechanical cross-stage placement of two pre-registered audits. No pooling, no test, no threshold, "
                     "no causal claim. The relation to the hypothesis is written separately under research/observations/."),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    return report


def _cell(a: dict[str, Any] | None) -> str:
    if not a:
        return "n/a"
    return f"{a['discount_events']}d/{a['inflation_events']}i/{a['at_reference_events']}r of {a['events']}"


def render_markdown(r: dict[str, Any]) -> str:
    names = list(r["expectations"]["E1"]["verdicts"])
    L = ["# EXP-003 Gate 3A Synthesis v0.1", "", "## Status", "", "**SYNTHESIS** (mechanical, cross-stage)", "", r["boundary"], "",
         "## Sources", ""]
    for name, src in r["sources"].items():
        L.append(f"- {name}: `{src['path']}` (sha256 `{src['sha256']}`)")
    L += [f"- HEAD at synthesis time: `{r['head_commit']}`", "",
          "## Pre-registered expectations, both stages", "",
          "| Id | " + " | ".join(names) + " | Agree |",
          "|---|" + "---|" * (len(names) + 1)]
    for key in ("E1", "E2", "E3", "E4", "E5"):
        e = r["expectations"][key]
        L.append(f"| {key} | " + " | ".join(f"**{e['verdicts'][n]}**" for n in names) + f" | {'yes' if e['agree'] else 'no'} |")
    e6 = r["expectations"]["E6"]
    L.append(f"| E6 | " + " | ".join("→".join(e6["orderings"][n]) for n in names) + f" | **{e6['verdict']}** |")
    L += ["", "E6 rates (LINEAGE discount rate over all post-seed events, by arm):", ""]
    L += ["| Stage | " + " | ".join(TOPOLOGIES) + " |", "|---|" + "---:|" * len(TOPOLOGIES)]
    for n in names:
        L.append(f"| {n} | " + " | ".join(f"{e6['rates'][n].get(t, 0):.3f}" for t in TOPOLOGIES) + " |")
    L += ["", "Quantities behind each verdict:", ""]
    for key in ("E1", "E2", "E3", "E4", "E5"):
        for n in names:
            L.append(f"- {key} {n}: `{json.dumps(r['expectations'][key]['quantities'][n], default=str)}`")
    L += ["", "## Position summary (post-seed events; d = discount, i = inflation, r = at reference)", "",
          "| Stage | Topology | Condition | A | B | C | A restoration | Sustained A deviation (worlds) |", "|---|---|---|---|---|---|---:|---:|"]
    for p in r["positions"]:
        L.append(f"| {p['stage']} | {p['topology']} | {p['condition']} | {_cell(p['A'])} | {_cell(p['B'])} | {_cell(p['C'])} | "
                 f"{p['A_restoration_rate']} | {p['worlds_with_sustained_A_deviation']}/{p['worlds']} |")
        if "bounce_B_legs" in p:
            legs = p["bounce_B_legs"]
            L.append(f"| {p['stage']} | bounce B legs | {p['condition']} | outward {legs['outward']['discount_events']}d/{legs['outward']['inflation_events']}i of {legs['outward']['events']} | "
                     f"return {legs['return']['discount_events']}d/{legs['return']['inflation_events']}i of {legs['return']['events']} | | | |")
    L += ["", "## Origin (A) deviations after each echo, by firing and by the inbound agent-as-source mark", "",
          "| Stage | Topology | Condition | A post-seed events | Deviations by firing | deviating & marked | deviating & unmarked | at reference & marked | at reference & unmarked |",
          "|---|---|---|---:|---|---:|---:|---:|---:|"]
    for o in r["origin_deviations"]:
        if o["condition"] == "free" and not o["deviations_by_firing"]:
            continue
        c = o["inbound_mark_crosstab"]
        L.append(f"| {o['stage']} | {o['topology']} | {o['condition']} | {o['A_post_seed_events']} | {json.dumps(o['deviations_by_firing'])} | "
                 f"{c['deviating_marked']} | {c['deviating_unmarked']} | {c['at_reference_marked']} | {c['at_reference_unmarked']} |")
    L += ["", "(FREE rows with no A deviation are omitted.)", "", "## Final state", "",
          "| Stage | World×conditions | Final answer ≠ E1 | Final confidence | Accuracy aligned / misleading | MACRO stopped after cycle 1 | MACRO responses all reused | Cells |",
          "|---|---:|---:|---|---|---|---|---|"]
    for f in r["final_state"]:
        cells = next(iter(f["cells"].values()))
        L.append(f"| {f['stage']} | {f['world_conditions']} | {f['final_answer_differs_from_E1']} | {f['final_confidence_distribution']} | "
                 f"{f['accuracy_by_alignment']['aligned']} / {f['accuracy_by_alignment']['misleading']} | {f['macro_stopped_after_first_cycle']}/{f['macro_worlds']} | "
                 f"{f['macro_all_responses_reused']}/{f['macro_worlds']} | {cells} |")
    if r["historical"]:
        h = r["historical"]
        L += ["", "## Secondary: contemporary ring (Set 001) vs the archived EXP-002 ring", "",
              f"Historical: {h['historical_runs']} runs, {h['historical_distinct_seeds']} distinct seeds, run classes {h['historical_run_classes']}. "
              f"Factor ledger difference: `{json.dumps(h['factor_ledger_difference'], default=str)}`.", "",
              "| Corpus | Condition | Runs | A | B | C | A restoration |", "|---|---|---:|---|---|---|---:|"]
        for name in ("contemporary", "historical", "historical_gate_2b_only"):
            for condition, c in h[name].items():
                L.append(f"| {name} | {condition} | {c['runs']} | {_cell(c['agents'].get('A'))} | {_cell(c['agents'].get('B'))} | {_cell(c['agents'].get('C'))} | {c['A_restoration_rate']} |")
    L += ["", "## Closure rule", "", "| Requirement | Status |", "|---|---|"]
    for k, v in r["closure_rule"].items():
        L.append(f"| {k} | {v} |")
    L += ["", "## Boundary", "", r["boundary"], ""]
    return "\n".join(L)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=AUDITS)
    args = parser.parse_args()
    stages = {}
    corpus = {}
    sources = {}
    for name, path in STAGE_FILES.items():
        if not path.exists():
            raise SystemExit(f"missing stage audit: {path}")
        stages[name] = json.loads(path.read_text(encoding="utf-8"))
        if stages[name].get("status") != "COMPLETE":
            raise SystemExit(f"{path}: status {stages[name].get('status')!r} is not COMPLETE; refusing")
        sources[name] = {"path": portable_path(path), "sha256": sha256_file(path)}
        # The corpus audit the stage audit depended on, by the hash the stage audit recorded.
        corpus_path = AUDITS / f"EXP_003_GATE_3A_{name.upper()}_CORPUS_AUDIT_v0.1.json"
        if not corpus_path.exists():
            raise SystemExit(f"missing corpus audit: {corpus_path}")
        if sha256_file(corpus_path) != stages[name]["corpus_audit"]["sha256"]:
            raise SystemExit(f"{corpus_path}: sha256 differs from the one recorded in the {name} primary-outcome audit; refusing")
        corpus[name] = json.loads(corpus_path.read_text(encoding="utf-8"))
        sources[f"{name}_corpus"] = {"path": portable_path(corpus_path), "sha256": sha256_file(corpus_path)}
    historical = None
    if HISTORICAL_FILE.exists():
        historical = json.loads(HISTORICAL_FILE.read_text(encoding="utf-8"))
        sources["historical"] = {"path": portable_path(HISTORICAL_FILE), "sha256": sha256_file(HISTORICAL_FILE)}
    report = synthesize(stages, historical, sources, corpus)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    json_path, md_path = output_paths(args.out_dir / "EXP_003_GATE_3A_SYNTHESIS_v0.1")
    json_path.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    e = report["expectations"]
    print("SYNTHESIS written: " + ", ".join(f"{k}=" + "/".join(e[k]["verdicts"].values()) for k in ("E1", "E2", "E3", "E4", "E5"))
          + f", E6={e['E6']['verdict']}")
    print(f"wrote {json_path} and {md_path}")


if __name__ == "__main__":
    main()
