"""EXP-003 Gate 3B primary-outcome audit (descriptive, pre-registered, read-only).

Implements GATE_3B_PRIMARY_OUTCOME_AUDIT_SPEC_v0.1 and nothing beyond it. For one stage of the
Gate 3B plan it tabulates D at every firing, A at every post-seed firing, the matrix by world,
per-agent finals, the probe-reactivity comparison, the solo control, the secondary inbound-naming
table, the EXP-002 family, the MACRO boundary, and restates expectations E1..E6 by the plan's
"would be contradicted by" column (E7 belongs to the synthesis). Writes one JSON and one
Markdown record under experiments/EXP_003/audits/gate_3b/.

Boundaries built into the code (as in the Gate 3A tool):
- Refuses to run unless the stage's corpus audit exists, reads PASS, and the raw files hash to it.
- Re-measures nothing. Stored p_a, reference and excess are cross-checked against the raw answer,
  confidence and the world's roots with the frozen runtime's own functions.
- Never pools stages or strata. Rates are counts over events; no test, no threshold beyond the
  spec's stated tolerances.

Usage:
    python -m experiments.EXP_003.tools.gate3b_primary_outcome_audit --plan experiments/EXP_003/GATE_3B_PLAN_v0.1.json --stage set_001
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..gate_orchestrator import DEFAULT_ARCHIVE_ROOT, PROJECT_ROOT, load_plan, plan_arms
from ..metrics import probability_of_a, reference_probability_of_a
from ..models import Evidence
from .corpus_audit import git_output, portable_path, sha256_file
from .primary_outcome_audit import TOLERANCE, classify, load_summary, output_paths

EXP003 = Path(__file__).resolve().parents[1]
SPEC_VERSION = "EXP-003-GATE-3B-PRIMARY-OUTCOME-AUDIT-SPEC-v0.1"
CONDITIONS = ("free", "lineage", "macro")
E1_TOL, E5_TOL, E6_TOL = 0.01, 0.01, 0.02   # spec 6: tolerances written in the plan's own words
E2_MAJORITY = 7                              # of 12 worlds


# --------------------------------------------------------------------------------------
# Spec 3: direction rules
# --------------------------------------------------------------------------------------

def direction(p_a: float, reference: float, e1_observed: str) -> dict[str, Any]:
    """Spec 3.1/3.2. Favored-state certainty excess when the reference is not .5; signed
    departure from even (toward E1's observed state) with no discount/inflation label when it is."""
    if abs(reference - 0.5) <= TOLERANCE:
        departure = round((p_a - 0.5) if e1_observed == "A" else (0.5 - p_a), 6)
        return {"favored": None, "certainty_excess": None, "departure_toward_e1": departure,
                "kind": "departure_from_even", "magnitude": abs(departure)}
    favored = "A" if reference > 0.5 else "B"
    p_fav = p_a if favored == "A" else 1.0 - p_a
    ce = round(p_fav - max(reference, 1.0 - reference), 6)
    return {"favored": favored, "certainty_excess": ce, "departure_toward_e1": None, "kind": classify(ce), "magnitude": abs(ce)}


# --------------------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------------------

def world_evidence(attempt_dir: Path) -> tuple[Evidence, ...]:
    meta = json.loads((attempt_dir / "run_metadata.json").read_text(encoding="utf-8"))
    return tuple(Evidence(e["evidence_id"], e["observed_state"], e["source"], float(e["reliability"]), tuple(e["assigned_to"]))
                 for e in meta["worlds"][0]["evidence"])


def event_row(record: dict[str, Any], evidence: tuple[Evidence, ...]) -> dict[str, Any]:
    metrics, lineage, prov = record["metrics"], record["actual_lineage"], record.get("provenance") or {}
    e1 = next(e for e in evidence if e.evidence_id == "E1")
    p_a, reference = float(metrics["p_a"]), float(metrics["reference_p_a"])
    roots = list(lineage["actual_roots"])
    inconsistencies: list[str] = []
    answer, confidence = record["model_output"]["answer"], float(record["model_output"]["confidence"])
    if abs(probability_of_a(answer, confidence) - p_a) > TOLERANCE:
        inconsistencies.append(f"stored p_a {p_a} != recomputed from answer {answer!r} and confidence {confidence}")
    recomputed_reference = reference_probability_of_a(tuple(e for e in evidence if e.evidence_id in roots))
    if abs(recomputed_reference - reference) > TOLERANCE:
        inconsistencies.append(f"stored reference_p_a {reference} != {recomputed_reference} from roots {roots}")
    if abs(float(metrics["p_a_excess_over_reference"]) - (p_a - reference)) > TOLERANCE:
        inconsistencies.append("stored excess != p_a - reference")
    dsc = metrics.get("reported_distinct_source_count")
    fis = metrics.get("false_independent_support")
    if dsc is not None and fis != max(0, int(dsc) - len(roots)):
        inconsistencies.append(f"stored FIS {fis} != max(0, {dsc} - {len(roots)})")
    row = {
        "id": record["visible_message_id"], "sender": record["sender"], "receivers": list(record.get("receivers") or []),
        "cycle": record.get("cycle"), "answer": answer, "confidence": confidence, "p_a": p_a, "reference_p_a": reference,
        "excess_raw": round(p_a - reference, 6), **direction(p_a, reference, e1.observed_state),
        "reported_distinct_source_count": dsc, "roots": roots, "root_count": len(roots), "fis": fis,
        "redundant_root_exposures": lineage.get("redundant_root_exposures"), "depth": lineage["inference_depth"],
        "accuracy": metrics.get("accuracy"), "brier": metrics.get("brier_score"),
        "delta_without_new_evidence": metrics.get("p_a_delta_without_new_evidence"),
        "source_named": bool(prov.get("source_named")), "agent_as_source": bool(prov.get("agent_as_source")),
        "inbound_agent_as_source": bool(prov.get("inbound_agent_as_source")), "erosion": prov.get("erosion_count"),
        "response_reused": bool(record.get("response_reused")), "inconsistencies": inconsistencies,
    }
    return row


def load_events(events_path: Path, evidence: tuple[Evidence, ...]) -> dict[str, list[dict[str, Any]]]:
    by_condition: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for line in events_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            record = json.loads(line)
            by_condition[record["condition"]].append(record)
    out: dict[str, list[dict[str, Any]]] = {}
    for condition, records in by_condition.items():
        records.sort(key=lambda r: int(str(r["visible_message_id"]).lstrip("M")))
        out[condition] = [event_row(r, evidence) for r in records]
    return out


def positions(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """D firings with their two inbound messages; A post-seed firings with their inbound (spec 4)."""
    by_cycle: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    for index, row in enumerate(rows):
        row = dict(row, index=index)
        by_cycle[row["cycle"]].append(row)
    d_firings, a_firings = [], []
    last_a = 0
    for index, row in enumerate(rows):
        if row["sender"] == "D":
            inbound = [r for r in by_cycle[row["cycle"]] if "D" in r["receivers"] and r["index"] < index]
            d_firings.append({**row, "inbound": [{k: r[k] for k in ("id", "sender", "source_named", "agent_as_source", "root_count")} for r in inbound]})
        if row["sender"] == "A":
            if index > 0:
                inbound = [r for r in by_cycle[row["cycle"]] if "A" in r["receivers"] and r["index"] < index]
                a_firings.append({**row, "hops": index - last_a,
                                  "inbound": [{k: r[k] for k in ("id", "sender", "source_named", "agent_as_source", "root_count")} for r in inbound]})
            last_a = index
    return {"D": d_firings, "A_post_seed": a_firings}


def corpus_audit_path(gate: str, stage: str, out_dir: Path | None = None) -> Path:
    base = out_dir or (EXP003 / "audits" / f"gate_{gate.lower()}")
    return base / f"EXP_003_GATE_{gate.upper()}_{stage.upper()}_CORPUS_AUDIT_v0.1.json"


def load_stage(plan_path: Path, stage: str, archive_root: Path, corpus_audit_file: Path) -> dict[str, Any]:
    plan = load_plan(plan_path)
    gate = plan["gate"]
    if not corpus_audit_file.exists():
        raise SystemExit(f"corpus audit record missing: {corpus_audit_file}; run corpus_audit first")
    corpus = json.loads(corpus_audit_file.read_text(encoding="utf-8"))
    if corpus.get("status") != "PASS" or corpus.get("stage") != stage:
        raise SystemExit(f"corpus audit for {stage} is not PASS (status={corpus.get('status')!r}); refusing")
    arms = [a for a in plan_arms(plan, plan_path) if a.stage == stage]
    gate_dir = archive_root / f"gate_{gate.lower()}"
    problems: list[str] = []
    sets: dict[str, Any] = {}
    for arm in arms:
        record = corpus["sets"].get(arm.set_id)
        if record is None:
            raise SystemExit(f"corpus audit has no record for {arm.set_id}; refusing")
        worlds: dict[int, dict[str, Any]] = {}
        for w in record["worlds"]:
            if len(w["complete"]) != 1:
                problems.append(f"{arm.set_id}/{w['canonical_id']}: {len(w['complete'])} complete attempts in corpus record")
                continue
            attempt_dir = gate_dir / arm.set_id / w["canonical_id"] / w["complete"][0]
            for name in ("events.jsonl", "summary.csv", "run_metadata.json"):
                if sha256_file(attempt_dir / name) != w["raw_file_sha256"][name]:
                    raise SystemExit(f"{attempt_dir / name}: sha256 differs from the corpus audit record; refusing")
            evidence = world_evidence(attempt_dir)
            events = load_events(attempt_dir / "events.jsonl", evidence)
            summary = load_summary(attempt_dir / "summary.csv")
            for condition, rows in events.items():
                if condition in summary and abs(float(summary[condition]["final_p_a"]) - rows[-1]["p_a"]) > TOLERANCE:
                    problems.append(f"{arm.set_id}/{w['canonical_id']}/{condition}: summary final_p_a disagrees with last event")
                for row in rows:
                    for text in row["inconsistencies"]:
                        problems.append(f"{arm.set_id}/{w['canonical_id']}/{condition}/{row['id']}: {text}")
            observed = [e.observed_state for e in evidence]
            stratum = None
            if arm.root_mode == "dual":
                stratum = "agreeing" if len(set(observed)) == 1 else "conflicting"
            worlds[int(w["seed"])] = {
                "canonical_id": w["canonical_id"], "seed": int(w["seed"]), "cell": w["cell"], "alignment": w.get("alignment"),
                "execution_order": w["execution_order"], "attempt": w["complete"][0], "stratum": stratum,
                "events": events, "summary": summary, "positions": {c: positions(rows) for c, rows in events.items()},
            }
        sets[arm.set_id] = {"topology": arm.topology, "root_mode": arm.root_mode, "rounds": arm.rounds, "probe": arm.probe, "worlds": worlds}
    return {"plan": plan, "plan_path": plan_path, "gate": gate, "stage": stage, "sets": sets, "problems": problems,
            "corpus_audit": {"path": portable_path(corpus_audit_file), "sha256": sha256_file(corpus_audit_file),
                             "status": corpus["status"], "head_commit": corpus.get("head_commit")}}


# --------------------------------------------------------------------------------------
# Aggregation helpers
# --------------------------------------------------------------------------------------

def _rate(n: int, d: int) -> float | None:
    return round(n / d, 6) if d else None


def _mean(values: list[float]) -> float | None:
    return round(sum(values) / len(values), 6) if values else None


def kind_counts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    kinds = Counter(r["kind"] for r in rows)
    out = {"events": len(rows), "discount": kinds["discount"], "inflation": kinds["inflation"], "at_reference": kinds["at_reference"],
           "departure_from_even_events": kinds["departure_from_even"],
           "mean_certainty_excess": _mean([r["certainty_excess"] for r in rows if r["certainty_excess"] is not None]),
           "mean_departure_toward_e1": _mean([r["departure_toward_e1"] for r in rows if r["departure_toward_e1"] is not None]),
           "fis_positive_events": sum(1 for r in rows if (r["fis"] or 0) > 0),
           "mean_reported_distinct_sources": _mean([float(r["reported_distinct_source_count"]) for r in rows if r["reported_distinct_source_count"] is not None])}
    return out


def find_set(stage: dict[str, Any], **match: Any) -> tuple[str, dict[str, Any]] | None:
    for set_id, s in stage["sets"].items():
        if all(s.get(k) == v for k, v in match.items()):
            return set_id, s
    return None


def d_rows(world: dict[str, Any], condition: str) -> list[dict[str, Any]]:
    return world["positions"].get(condition, {}).get("D", [])


# --------------------------------------------------------------------------------------
# Spec 5: tables
# --------------------------------------------------------------------------------------

def table_matrix_by_world(stage: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for set_id, s in stage["sets"].items():
        if s["topology"] != "diamond" or not s["probe"]:
            continue
        for seed, w in sorted(s["worlds"].items(), key=lambda kv: kv[1]["execution_order"]):
            row = {"set": set_id, "seed": seed, "cell": w["cell"], "stratum": w["stratum"]}
            for condition in ("free", "lineage"):
                d = d_rows(w, condition)
                c = kind_counts(d)
                row[condition] = {"mean_certainty_excess": c["mean_certainty_excess"], "mean_departure_toward_e1": c["mean_departure_toward_e1"],
                                  "fis_positive_events": c["fis_positive_events"], "d_firings": len(d)}
            rows.append(row)
    return rows


def table_probe_reactivity(stage: dict[str, Any]) -> list[dict[str, Any]]:
    on = find_set(stage, topology="diamond", root_mode="single", probe=True)
    off = find_set(stage, topology="diamond", root_mode="single", probe=False)
    if not on or not off:
        return []
    rows = []
    for seed, w_off in sorted(off[1]["worlds"].items(), key=lambda kv: kv[1]["execution_order"]):
        w_on = on[1]["worlds"].get(seed)
        if not w_on:
            continue
        for condition in ("free", "lineage"):
            m_on = kind_counts(d_rows(w_on, condition))["mean_certainty_excess"]
            m_off = kind_counts(d_rows(w_off, condition))["mean_certainty_excess"]
            gap = round(abs((m_off or 0.0) - (m_on or 0.0)), 6)
            rows.append({"seed": seed, "condition": condition, "probe_on_mean_D_excess": m_on, "probe_off_mean_D_excess": m_off,
                         "gap": gap, "within_tolerance": gap <= E6_TOL})
    return rows


def table_solo(stage: dict[str, Any]) -> list[dict[str, Any]]:
    solo = find_set(stage, topology="solo")
    if not solo:
        return []
    rows = []
    for seed, w in sorted(solo[1]["worlds"].items(), key=lambda kv: kv[1]["execution_order"]):
        for condition in ("free", "lineage"):
            a = w["positions"][condition]["A_post_seed"]
            rows.append({"seed": seed, "condition": condition, "certainty_excess_sequence": [r["certainty_excess"] for r in a],
                         "any_deviation": any(r["kind"] != "at_reference" for r in a),
                         "fis_positive_events": sum(1 for r in a if (r["fis"] or 0) > 0)})
    return rows


def _inbound_naming_count(row: dict[str, Any]) -> int:
    return sum(1 for i in row["inbound"] if i["source_named"])


def table_inbound_naming(stage: dict[str, Any]) -> dict[str, Any]:
    """Spec 5.7, secondary: excess/FIS at D and at A against how many inbound messages named the sensor.
    Tabulated per condition and per stratum; the agreeing and conflicting strata are never pooled (spec 3.2)."""
    out: dict[str, Any] = {}
    for set_id, s in stage["sets"].items():
        if s["topology"] == "solo":
            continue
        per: dict[str, Any] = {}
        for condition in ("free", "lineage"):
            per[condition] = {}
            for stratum in sorted({w["stratum"] for w in s["worlds"].values()}, key=str):
                d_tab: dict[int, list] = defaultdict(list)
                a_tab: dict[int, list] = defaultdict(list)
                for w in s["worlds"].values():
                    if w["stratum"] != stratum:
                        continue
                    for r in d_rows(w, condition):
                        d_tab[_inbound_naming_count(r)].append(r)
                    for r in w["positions"][condition]["A_post_seed"]:
                        a_tab[_inbound_naming_count(r)].append(r)
                per[condition][str(stratum)] = {"D_by_inbound_naming_sensor": {str(k): kind_counts(v) for k, v in sorted(d_tab.items())},
                                                "A_by_inbound_naming_sensor": {str(k): kind_counts(v) for k, v in sorted(a_tab.items())}}
        out[set_id] = per
    return out


def table_family(stage: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for set_id, s in stage["sets"].items():
        for seed, w in sorted(s["worlds"].items(), key=lambda kv: kv[1]["execution_order"]):
            for condition in CONDITIONS:
                ev = w["events"].get(condition)
                if not ev:
                    continue
                last = ev[-1]
                rows.append({"set": set_id, "order": w["execution_order"], "seed": seed, "cell": w["cell"], "stratum": w["stratum"],
                             "condition": condition, "final_answer": last["answer"], "accuracy": last["accuracy"],
                             "final_confidence": last["confidence"], "final_p_a": last["p_a"], "final_reference_p_a": last["reference_p_a"],
                             "final_kind": last["kind"], "final_certainty_excess": last["certainty_excess"],
                             "final_departure_toward_e1": last["departure_toward_e1"], "final_brier": last["brier"],
                             "roots": last["root_count"], "max_depth": max(e["depth"] for e in ev),
                             "max_redundant_root_exposures": max((e["redundant_root_exposures"] or 0) for e in ev),
                             "erosion_trajectory": [e["erosion"] for e in ev], "agent_as_source_events": sum(e["agent_as_source"] for e in ev),
                             "fis_positive_events": sum(1 for e in ev if (e["fis"] or 0) > 0), "events": len(ev),
                             "per_agent_final_p_a": w["summary"].get(condition, {}).get("per_agent_final_p_a"),
                             "per_agent_max_excess": w["summary"].get(condition, {}).get("per_agent_max_excess"),
                             "per_agent_min_excess": w["summary"].get(condition, {}).get("per_agent_min_excess")})
    return rows


def table_macro(stage: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for set_id, s in stage["sets"].items():
        for seed, w in sorted(s["worlds"].items(), key=lambda kv: kv[1]["execution_order"]):
            macro = w["events"].get("macro") or []
            if not macro:
                continue
            rows.append({"set": set_id, "seed": seed, "stop_event": macro[-1]["id"], "macro_events": len(macro),
                         "macro_stop_triggered": w["summary"].get("macro", {}).get("macro_stop_triggered"),
                         "all_responses_reused": all(e["response_reused"] for e in macro[1:]) if len(macro) > 1 else None})
    return rows


def arm_aggregates(stage: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for set_id, s in stage["sets"].items():
        per: dict[str, Any] = {}
        for condition in ("free", "lineage"):
            strata = sorted({w["stratum"] for w in s["worlds"].values()}, key=str)
            per[condition] = {}
            for stratum in strata:
                worlds = [w for w in s["worlds"].values() if w["stratum"] == stratum]
                d = [r for w in worlds for r in d_rows(w, condition)]
                a = [r for w in worlds for r in w["positions"][condition]["A_post_seed"]]
                per[condition][str(stratum)] = {"worlds": len(worlds), "D": kind_counts(d), "A_post_seed": kind_counts(a)}
        out[set_id] = {"topology": s["topology"], "root_mode": s["root_mode"], "probe": s["probe"], "conditions": per}
    return out


# --------------------------------------------------------------------------------------
# Spec 6: expectations E1..E6 (E7 in the synthesis)
# --------------------------------------------------------------------------------------

def expectations(stage: dict[str, Any], probe_table: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    arm1 = find_set(stage, topology="diamond", root_mode="single", probe=True)
    arm2 = find_set(stage, topology="diamond", root_mode="dual", probe=True)
    worlds1 = list(arm1[1]["worlds"].values()) if arm1 else []

    # E1: FREE D shows positive excess in at least some Arm 1 worlds.
    if worlds1:
        any_positive = [any(r["certainty_excess"] is not None and r["certainty_excess"] > E1_TOL for r in d_rows(w, "free")) for w in worlds1]
        out["E1"] = {"verdict": "consistent" if any(any_positive) else "contradicted",
                     "arm1_worlds_with_FREE_D_excess_above_tolerance": sum(any_positive), "worlds": len(worlds1), "tolerance": E1_TOL}
    else:
        out["E1"] = {"verdict": "not assessable"}

    # E2: LINEAGE D excess not greater than FREE D excess in the same world.
    if worlds1:
        exceed = 0
        for w in worlds1:
            m_free = kind_counts(d_rows(w, "free"))["mean_certainty_excess"] or 0.0
            m_lin = kind_counts(d_rows(w, "lineage"))["mean_certainty_excess"] or 0.0
            exceed += int(m_lin > m_free + TOLERANCE)
        out["E2"] = {"verdict": "contradicted" if exceed >= E2_MAJORITY else "consistent",
                     "worlds_where_LINEAGE_mean_D_excess_exceeds_FREE": exceed, "worlds": len(worlds1), "majority": E2_MAJORITY}
    else:
        out["E2"] = {"verdict": "not assessable"}

    # E3: positive excess at D co-occurs with FIS > 0.
    if worlds1:
        cells = {}
        verdicts = []
        for condition in ("free", "lineage"):
            d = [r for w in worlds1 for r in d_rows(w, condition)]
            conc = sum(1 for r in d if (r["certainty_excess"] or 0) > TOLERANCE and (r["fis"] or 0) > 0)
            disc_a = sum(1 for r in d if (r["certainty_excess"] or 0) > TOLERANCE and (r["fis"] or 0) == 0)
            disc_b = sum(1 for r in d if (r["certainty_excess"] or 0) <= TOLERANCE and (r["fis"] or 0) > 0)
            cells[condition] = {"concordant": conc, "excess_without_FIS": disc_a, "FIS_without_excess": disc_b, "D_firings": len(d)}
            verdicts.append("contradicted" if disc_a + disc_b > conc else "consistent")
        out["E3"] = {"verdict": "contradicted" if "contradicted" in verdicts else "consistent", "by_condition": cells}
    else:
        out["E3"] = {"verdict": "not assessable"}

    # E4: inbound agent-as-source wording precedes positive excess more often than clean wording.
    if worlds1:
        res = {}
        verdicts = []
        for condition in ("free", "lineage"):
            d = [r for w in worlds1 for r in d_rows(w, condition)]
            marked = [r for r in d if any(i["agent_as_source"] for i in r["inbound"])]
            clean = [r for r in d if not any(i["agent_as_source"] for i in r["inbound"])]
            rm = _rate(sum(1 for r in marked if (r["certainty_excess"] or 0) > TOLERANCE), len(marked))
            rc = _rate(sum(1 for r in clean if (r["certainty_excess"] or 0) > TOLERANCE), len(clean))
            res[condition] = {"marked_firings": len(marked), "excess_rate_marked": rm, "clean_firings": len(clean), "excess_rate_clean": rc}
            verdicts.append("not assessable" if rm is None or rc is None else ("contradicted" if rm <= rc else "consistent"))
        out["E4"] = {"verdict": ("contradicted" if "contradicted" in verdicts else "not assessable" if "not assessable" in verdicts else "consistent"),
                     "by_condition": res}
    else:
        out["E4"] = {"verdict": "not assessable"}

    # E5: Arm 2 D approaches the two-root reference (agreeing stratum).
    if arm2:
        res = {}
        verdicts = []
        agreeing = [w for w in arm2[1]["worlds"].values() if w["stratum"] == "agreeing"]
        for condition in ("free", "lineage"):
            classes: Counter = Counter()
            for w in agreeing:
                for r in d_rows(w, condition):
                    if r["root_count"] != 2 or r["favored"] is None:
                        continue
                    two_root = max(r["reference_p_a"], 1 - r["reference_p_a"])
                    p_fav = r["p_a"] if r["favored"] == "A" else 1 - r["p_a"]
                    if abs(p_fav - two_root) <= E5_TOL:
                        classes["two_root"] += 1
                    elif abs(p_fav - 0.70) <= E5_TOL:
                        classes["single_root"] += 1
                    elif p_fav > two_root + E5_TOL:
                        classes["over"] += 1
                    else:
                        classes["other"] += 1
            modal = classes.most_common(1)[0][0] if classes else None
            res[condition] = {"classes": dict(classes), "modal": modal}
            verdicts.append("not assessable" if modal is None else ("contradicted" if modal in ("single_root", "over") else "consistent"))
        conflicting = [w for w in arm2[1]["worlds"].values() if w["stratum"] == "conflicting"]
        res["conflicting_stratum_departure"] = {c: kind_counts([r for w in conflicting for r in d_rows(w, c) if r["root_count"] == 2])["mean_departure_toward_e1"]
                                                for c in ("free", "lineage")}
        out["E5"] = {"verdict": ("contradicted" if "contradicted" in verdicts else "not assessable" if "not assessable" in verdicts else "consistent"),
                     "agreeing_worlds": len(agreeing), "conflicting_worlds": len(conflicting), "tolerance": E5_TOL, **res}
    else:
        out["E5"] = {"verdict": "not assessable"}

    # E6: probe reactivity.
    if probe_table:
        gaps_over = [r for r in probe_table if not r["within_tolerance"]]
        out["E6"] = {"verdict": "contradicted" if gaps_over else "consistent", "comparisons": len(probe_table),
                     "gaps_over_tolerance": len(gaps_over), "tolerance": E6_TOL}
    else:
        out["E6"] = {"verdict": "not assessable"}

    out["E7"] = {"verdict": "assessed in the synthesis across Set 001 and Set 002, not in a single-stage audit"}
    return out


# --------------------------------------------------------------------------------------
# Stage audit
# --------------------------------------------------------------------------------------

def audit_stage(plan_path: Path, stage: str, archive_root: Path, corpus_audit_file: Path) -> dict[str, Any]:
    data = load_stage(plan_path, stage, archive_root, corpus_audit_file)
    probe = table_probe_reactivity(data)
    report = {
        "experiment": "EXP-003", "gate": data["gate"], "stage": stage, "spec_version": SPEC_VERSION,
        "plan_version": data["plan"].get("plan_version"), "plan_status": data["plan"].get("status"),
        "plan_sha256": sha256_file(plan_path), "anchors": data["plan"]["anchors"], "corpus_audit": data["corpus_audit"],
        "head_commit": git_output(["rev-parse", "HEAD"], PROJECT_ROOT), "archive_root": portable_path(archive_root),
        "tolerances": {"direction": TOLERANCE, "E1": E1_TOL, "E2_majority_of_12": E2_MAJORITY, "E5": E5_TOL, "E6": E6_TOL},
        "sets": {sid: {"topology": s["topology"], "root_mode": s["root_mode"], "probe": s["probe"], "rounds": s["rounds"], "worlds": len(s["worlds"]),
                       "cells": dict(Counter(w["cell"] for w in s["worlds"].values())),
                       "strata": dict(Counter(str(w["stratum"]) for w in s["worlds"].values()))} for sid, s in data["sets"].items()},
        "arm_aggregates": arm_aggregates(data),
        "matrix_by_world": table_matrix_by_world(data),
        "probe_reactivity": probe,
        "solo_control": table_solo(data),
        "secondary_inbound_naming": table_inbound_naming(data),
        "expectations": expectations(data, probe),
        "family": table_family(data),
        "macro_boundary": table_macro(data),
        "D_firings": {sid: {str(seed): {c: w["positions"][c]["D"] for c in w["positions"]} for seed, w in s["worlds"].items()}
                      for sid, s in data["sets"].items() if s["topology"] == "diamond"},
        "A_post_seed_firings": {sid: {str(seed): {c: w["positions"][c]["A_post_seed"] for c in w["positions"]} for seed, w in s["worlds"].items()}
                                for sid, s in data["sets"].items()},
        "problems": data["problems"],
        "status": "COMPLETE" if not data["problems"] else "COMPLETE WITH PROBLEMS",
        "boundary": ("Descriptive and pre-registered. Rates are counts over events; the only tolerances are those the frozen plan "
                     "states in words. This stage is reported alone; strata are reported alone. Expectation verdicts restate the plan's "
                     "'would be contradicted by' column. The secondary inbound-naming table carries no verdict. Negative results stand."),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    return report


# --------------------------------------------------------------------------------------
# Markdown
# --------------------------------------------------------------------------------------

def _f(x: Any) -> str:
    if x is None:
        return "n/a"
    return f"{x:+.3f}" if isinstance(x, float) else str(x)


def _kc(c: dict[str, Any]) -> str:
    if not c or not c["events"]:
        return "n/a"
    base = f"{c['discount']}d/{c['inflation']}i/{c['at_reference']}r of {c['events']}"
    if c["departure_from_even_events"]:
        base += f" (+{c['departure_from_even_events']} even-reference; mean dep {_f(c['mean_departure_toward_e1'])})"
    return base + f"; FIS>0 at {c['fis_positive_events']}; x̄ {_f(c['mean_certainty_excess'])}"


def render_markdown(r: dict[str, Any]) -> str:
    L = [f"# EXP-003 Gate {r['gate']} {r['stage'].replace('_', ' ').title()} Primary-Outcome Audit v0.1", "", "## Status", "",
         f"**{r['status']}**", "", r["boundary"], "", "## Provenance", "",
         f"- Specification: `{r['spec_version']}`", f"- Plan: `{r['plan_version']}` (status `{r['plan_status']}`, sha256 `{r['plan_sha256']}`)",
         f"- Frozen runtime: `{r['anchors'].get('frozen_runtime')}`; Gate 3A checkpoint `{r['anchors'].get('gate3a_closure_checkpoint')}`",
         f"- Corpus audit: `{r['corpus_audit']['path']}` (status {r['corpus_audit']['status']}, sha256 `{r['corpus_audit']['sha256']}`)",
         f"- HEAD at audit time: `{r['head_commit']}`", f"- Tolerances: `{json.dumps(r['tolerances'])}`", "",
         "## Sets", "", "| Set | Topology | Root mode | Probe | Rounds | Worlds | Cells | Strata |", "|---|---|---|---|---:|---:|---|---|"]
    for sid, s in r["sets"].items():
        L.append(f"| `{sid}` | {s['topology']} | {s['root_mode']} | {'on' if s['probe'] else 'off'} | {s['rounds']} | {s['worlds']} | "
                 f"{', '.join(f'{k}: {v}' for k, v in sorted(s['cells'].items()))} | {', '.join(f'{k}: {v}' for k, v in sorted(s['strata'].items()))} |")
    L += ["", "## Arm aggregates (d = discount, i = inflation, r = at reference; strata separate)", "",
          "| Set | Condition | Stratum | D | A post-seed |", "|---|---|---|---|---|"]
    for sid, agg in r["arm_aggregates"].items():
        for condition, strata in agg["conditions"].items():
            for stratum, v in strata.items():
                L.append(f"| `{sid}` | {condition} | {stratum} | {_kc(v['D'])} | {_kc(v['A_post_seed'])} |")
    L += ["", "## Pre-registered expectations", "", "| Id | Verdict | Quantities |", "|---|---|---|"]
    for key in ("E1", "E2", "E3", "E4", "E5", "E6", "E7"):
        v = r["expectations"][key]
        L.append(f"| {key} | **{v['verdict']}** | `{json.dumps({k: x for k, x in v.items() if k != 'verdict'}, default=str)}` |")
    L += ["", "## Matrix by world (mean D certainty excess, or mean departure toward E1 for the conflicting stratum)", "",
          "| Set | Seed | Cell | Stratum | FREE | LINEAGE | FIS>0 FREE / LINEAGE |", "|---|---:|---|---|---:|---:|---|"]
    for row in r["matrix_by_world"]:
        f, l = row["free"], row["lineage"]
        val = lambda c: _f(c["mean_certainty_excess"]) if c["mean_certainty_excess"] is not None else f"dep {_f(c['mean_departure_toward_e1'])}"
        L.append(f"| `{row['set']}` | {row['seed']} | {row['cell']} | {row['stratum'] or 'single'} | {val(f)} | {val(l)} | {f['fis_positive_events']} / {l['fis_positive_events']} |")
    if r["probe_reactivity"]:
        L += ["", "## Probe reactivity (Arm 4 vs Arm 1, shared worlds)", "", "| Seed | Condition | Probe on | Probe off | Gap | Within .02 |", "|---:|---|---:|---:|---:|---|"]
        for row in r["probe_reactivity"]:
            L.append(f"| {row['seed']} | {row['condition']} | {_f(row['probe_on_mean_D_excess'])} | {_f(row['probe_off_mean_D_excess'])} | {_f(row['gap'])} | {'yes' if row['within_tolerance'] else 'no'} |")
    if r["solo_control"]:
        L += ["", "## Solo control (probe on)", "", "| Seed | Condition | certainty excess per firing | Any deviation | FIS>0 |", "|---:|---|---|---|---:|"]
        for row in r["solo_control"]:
            L.append(f"| {row['seed']} | {row['condition']} | {', '.join(_f(x) for x in row['certainty_excess_sequence'])} | {'yes' if row['any_deviation'] else 'no'} | {row['fis_positive_events']} |")
    L += ["", "## Secondary: inbound messages naming the sensor (descriptive, no verdict)", "",
          "| Set | Condition | Stratum | Position | Inbound naming the sensor | Counts |", "|---|---|---|---|---:|---|"]
    for sid, per in r["secondary_inbound_naming"].items():
        for condition, strata in per.items():
            for stratum, tabs in strata.items():
                for pos, key in (("D", "D_by_inbound_naming_sensor"), ("A", "A_by_inbound_naming_sensor")):
                    for n, c in tabs[key].items():
                        L.append(f"| `{sid}` | {condition} | {stratum} | {pos} | {n} | {_kc(c)} |")
    L += ["", "## MACRO stopping boundary", "", "| Set | Seed | Stop event | MACRO events | Stop triggered | Responses reused |", "|---|---:|---|---:|---|---|"]
    for row in r["macro_boundary"]:
        L.append(f"| `{row['set']}` | {row['seed']} | {row['stop_event']} | {row['macro_events']} | {row['macro_stop_triggered']} | {row['all_responses_reused']} |")
    L += ["", "## Primary outcome table by world (EXP-002 family)", "",
          "| Set | Order | Seed | Cell | Condition | Final | Acc | Conf | P(A) | Ref | Kind | Brier | Roots | Depth | FIS>0 | agent-as-source |",
          "|---|---:|---:|---|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|"]
    for row in r["family"]:
        L.append(f"| `{row['set']}` | {row['order']} | {row['seed']} | {row['cell']} | {row['condition']} | {row['final_answer']} | {row['accuracy']} | "
                 f"{row['final_confidence']:.2f} | {row['final_p_a']:.3f} | {row['final_reference_p_a']:.3f} | {row['final_kind']} | {row['final_brier']:.3f} | "
                 f"{row['roots']} | {row['max_depth']} | {row['fis_positive_events']} | {row['agent_as_source_events']} |")
    L += ["", "## Problems", ""] + ([f"- {p}" for p in r["problems"]] or ["None."])
    L += ["", "## Boundary", "", r["boundary"], ""]
    return "\n".join(L)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=EXP003 / "GATE_3B_PLAN_v0.1.json")
    parser.add_argument("--stage", required=True)
    parser.add_argument("--archive-root", type=Path, default=None)
    parser.add_argument("--corpus-audit", type=Path, default=None)
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()
    plan = load_plan(args.plan)
    gate = plan["gate"]
    archive_root = args.archive_root or DEFAULT_ARCHIVE_ROOT
    out_dir = args.out_dir or (EXP003 / "audits" / f"gate_{gate.lower()}")
    corpus_file = args.corpus_audit or corpus_audit_path(gate, args.stage, args.out_dir)
    report = audit_stage(args.plan, args.stage, archive_root, corpus_file)   # refuses before anything is written
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path, md_path = output_paths(out_dir / f"EXP_003_GATE_{gate.upper()}_{args.stage.upper()}_PRIMARY_OUTCOME_AUDIT_v0.1")
    json_path.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    verdicts = ", ".join(f"{k}={report['expectations'][k]['verdict']}" for k in ("E1", "E2", "E3", "E4", "E5", "E6"))
    print(f"{report['status']}: {sum(s['worlds'] for s in report['sets'].values())} worlds; {verdicts}")
    print(f"wrote {json_path} and {md_path}")
    if report["problems"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
