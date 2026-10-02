"""EXP-003 Gate 3A primary-outcome audit (descriptive, pre-registered, read-only).

Implements EXP-003-GATE-3A-PRIMARY-OUTCOME-AUDIT-SPEC-v0.1 and nothing beyond it. For one
stage of the Gate 3A plan it tabulates the primary outcomes the frozen plan names, the five
focal comparisons paired by world, the pre-registered expectations E1..E5 restated by their
"would be contradicted by" column, and the MACRO stopping boundary. It writes one JSON and
one Markdown record under experiments/EXP_003/audits/gate_<x>/.

Boundaries built into the code:
- It depends on the stage's corpus integrity audit: it refuses to run unless that record
  exists, reads PASS, and the raw files it opens hash to what that record says.
- It re-measures nothing. Every quantity is an archived metric, or arithmetic over archived
  metrics (certainty_excess = p_observed - reference_observed), with the frozen runtime's
  own functions imported where a function is needed.
- It never pools stages. One invocation audits one stage. Set 001 and Set 002 are separate
  files; the cross-stage expectation E6 belongs to the synthesis, not here.
- No significance test, no threshold, no event selected after inspection. Rates are
  counts over events; ties count as "not below".

Usage:
    python -m experiments.EXP_003.tools.primary_outcome_audit --plan experiments/EXP_003/GATE_3A_PLAN_v0.1.json --stage set_001
    python -m experiments.EXP_003.tools.primary_outcome_audit --historical --set-id ring_control_set_001
"""
from __future__ import annotations

import argparse
import ast
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..factors import diff_factors, factors_for
from ..gate_orchestrator import DEFAULT_ARCHIVE_ROOT, PROJECT_ROOT, load_plan, plan_arms
from ..metrics import probability_of_a, reference_probability_of_a
from ..models import Evidence
from ..provenance import score_message
from ..topology import get_topology
from ..world_generator import WorldGenerator, world_cell
from .corpus_audit import git_output, portable_path, sha256_file

EXP003 = Path(__file__).resolve().parents[1]
EXP002_ARCHIVE = EXP003.parent / "EXP_002" / "results" / "archive"
SPEC_VERSION = "EXP-003-GATE-3A-PRIMARY-OUTCOME-AUDIT-SPEC-v0.1"
TOLERANCE = 1e-6
CONDITIONS = ("free", "lineage", "macro")
EXPECTATION_CONDITION = "lineage"  # spec 4.6 / D3: E2 and E3 assessed on LINEAGE, FREE printed beside


# --------------------------------------------------------------------------------------
# Spec 4.1: direction
# --------------------------------------------------------------------------------------

def certainty_excess(p_a: float, reference_p_a: float, observed: str) -> float:
    """p_observed - reference_observed (spec 4.1). Positive = inflation, negative = discount."""
    p_observed = p_a if observed == "A" else 1.0 - p_a
    reference_observed = max(reference_p_a, 1.0 - reference_p_a)
    return round(p_observed - reference_observed, 6)


def classify(ce: float) -> str:
    if abs(ce) <= TOLERANCE:
        return "at_reference"
    return "inflation" if ce > 0 else "discount"


# --------------------------------------------------------------------------------------
# Loading archived events (EXP-003 archives and, for the secondary observation, EXP-002)
# --------------------------------------------------------------------------------------

def _event_row(record: dict[str, Any], observed: str, prev_marks: dict[str, Any] | None,
               roots: tuple[Evidence, ...]) -> tuple[dict[str, Any], dict[str, Any]]:
    metrics = record["metrics"]
    p_a = float(metrics["p_a"])
    if "reference_p_a" in metrics:
        reference = float(metrics["reference_p_a"])
    else:  # EXP-002 archive: no reference stored; the frozen runtime's function from the roots
        reference = reference_probability_of_a(roots)
    receivers = record.get("receivers")
    if receivers is None:
        receivers = [record["receiver"]] if record.get("receiver") is not None else []
    provenance = record.get("provenance")
    if provenance is None:  # EXP-002 archive: same marks, computed from the visible text
        marks = score_message(record["model_output"]["message"], roots)
        provenance = {
            "agent_as_source": bool(marks["agent_as_source"]),
            "inbound_agent_as_source": bool(prev_marks and prev_marks["agent_as_source"]),
            "erosion_count": None,
        }
    else:
        marks = provenance
    ce = certainty_excess(p_a, reference, observed)
    # The stored metrics are not taken on trust: recompute them from the raw model output and
    # the world's root with the frozen runtime's own functions, and flag any disagreement.
    inconsistencies: list[str] = []
    answer = record["model_output"]["answer"]
    confidence = float(record["model_output"]["confidence"])
    recomputed_p_a = probability_of_a(answer, confidence)
    if abs(recomputed_p_a - p_a) > TOLERANCE:
        inconsistencies.append(f"stored p_a {p_a} != {recomputed_p_a} from answer {answer!r} and confidence {confidence}")
    recomputed_reference = reference_probability_of_a(roots)
    if abs(recomputed_reference - reference) > TOLERANCE:
        inconsistencies.append(f"stored reference_p_a {reference} != {recomputed_reference} from the world's root (E1 observed {observed})")
    if "p_a_excess_over_reference" in metrics and abs(float(metrics["p_a_excess_over_reference"]) - (p_a - reference)) > TOLERANCE:
        inconsistencies.append(f"stored excess {metrics['p_a_excess_over_reference']} != p_a - reference {round(p_a - reference, 6)}")
    if "E1" not in (record.get("actual_lineage") or {}).get("actual_roots", ["E1"]):
        inconsistencies.append("E1 not among the event's actual roots")
    row = {
        "id": record["visible_message_id"],
        "sender": record["sender"],
        "receivers": list(receivers),
        "cycle": record.get("cycle"),
        "answer": record["model_output"]["answer"],
        "confidence": float(record["model_output"]["confidence"]),
        "p_a": p_a,
        "reference_p_a": reference,
        "excess_raw": round(p_a - reference, 6),
        "certainty_excess": ce,
        "kind": classify(ce),
        "accuracy": metrics.get("accuracy"),
        "brier": metrics.get("brier_score"),
        "depth": metrics.get("inference_depth"),
        "roots": metrics.get("independent_evidence_root_count"),
        "redundant_root_exposures": metrics.get("redundant_root_exposures"),
        "delta_without_new_evidence": metrics.get("p_a_delta_without_new_evidence"),
        "false_independent_support": metrics.get("false_independent_support"),
        "erosion": provenance.get("erosion_count"),
        "agent_as_source": bool(provenance.get("agent_as_source")),
        "inbound_agent_as_source": bool(provenance.get("inbound_agent_as_source")),
        "response_reused": bool(record.get("response_reused")),
        "inconsistencies": inconsistencies,
    }
    return row, marks


def load_events(events_path: Path, observed: str, reliability: float = 0.70) -> dict[str, list[dict[str, Any]]]:
    """Events by condition, in firing order (M01, M02, ...)."""
    roots = (Evidence("E1", observed, "sensor_1", reliability, ("A",)),)
    by_condition: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for line in events_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            record = json.loads(line)
            by_condition[record["condition"]].append(record)
    out: dict[str, list[dict[str, Any]]] = {}
    for condition, records in by_condition.items():
        records.sort(key=lambda r: int(str(r["visible_message_id"]).lstrip("M")))
        rows: list[dict[str, Any]] = []
        prev_marks: dict[str, Any] | None = None
        for record in records:
            row, prev_marks = _event_row(record, observed, prev_marks, roots)
            rows.append(row)
        out[condition] = rows
    return out


def load_summary(summary_path: Path) -> dict[str, dict[str, Any]]:
    """summary.csv rows by condition; list/dict fields were written as Python literals."""
    out: dict[str, dict[str, Any]] = {}
    with summary_path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            parsed: dict[str, Any] = {}
            for key, value in row.items():
                if value is None:
                    parsed[key] = None
                    continue
                text = value.strip()
                if text.startswith(("[", "{")) or text in ("True", "False", "None"):
                    try:
                        parsed[key] = ast.literal_eval(text)
                        continue
                    except (ValueError, SyntaxError):
                        pass
                parsed[key] = value
            out[row["condition"]] = parsed
    return out


# --------------------------------------------------------------------------------------
# Spec 4.2 / 4.3: positions
# --------------------------------------------------------------------------------------

def positions(rows: list[dict[str, Any]], topology_name: str) -> dict[str, Any]:
    """Per-agent firing lists with hops (A), outward/return tags (bounce B), and the derived
    A quantities: restoration rate and sustained deviation (spec 4.3 table 4)."""
    topo = get_topology(topology_name)
    by_agent: dict[str, list[dict[str, Any]]] = defaultdict(list)
    last_index: dict[str, int] = {}
    for index, row in enumerate(rows):
        agent = row["sender"]
        entry = dict(row)
        entry["index"] = index
        entry["post_seed"] = index > 0
        entry["hops"] = index - last_index[agent] if agent in last_index else None
        if topology_name.startswith("bounce") and agent == "B":
            entry["leg"] = "outward" if row["receivers"] == ["C"] else "return"
        by_agent[agent].append(entry)
        last_index[agent] = index
    a_post = [e for e in by_agent.get("A", []) if e["post_seed"]]
    sustained = False
    sustained_at: list[str] = []
    for prev, cur in zip(a_post, a_post[1:]):
        if prev["kind"] != "at_reference" and prev["kind"] == cur["kind"]:
            sustained = True
            sustained_at.append(cur["id"])
    return {
        "focal_agent": topo.focal_agent,
        "by_agent": dict(by_agent),
        "A_post_seed": a_post,
        "A_restoration_rate": _rate(sum(e["kind"] == "at_reference" for e in a_post), len(a_post)),
        "A_sustained_deviation": sustained,
        "A_sustained_deviation_at": sustained_at,
        "A_deviations_after_inbound_agent_as_source": sum(
            1 for e in a_post if e["kind"] != "at_reference" and e["inbound_agent_as_source"]),
    }


def _rate(numerator: int, denominator: int) -> float | None:
    return round(numerator / denominator, 6) if denominator else None


def agent_rates(entries: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(entries)
    kinds = Counter(e["kind"] for e in entries)
    return {
        "events": n,
        "discount_events": kinds["discount"],
        "inflation_events": kinds["inflation"],
        "at_reference_events": kinds["at_reference"],
        "discount_rate": _rate(kinds["discount"], n),
        "inflation_rate": _rate(kinds["inflation"], n),
        "mean_magnitude": round(sum(abs(e["certainty_excess"]) for e in entries) / n, 6) if n else None,
        "certainty_excess_sequence": [e["certainty_excess"] for e in entries],
        "ids": [e["id"] for e in entries],
    }


# --------------------------------------------------------------------------------------
# Loading one stage
# --------------------------------------------------------------------------------------

def corpus_audit_path(gate: str, stage: str, out_dir: Path | None = None) -> Path:
    base = out_dir or (EXP003 / "audits" / f"gate_{gate.lower()}")
    return base / f"EXP_003_GATE_{gate.upper()}_{stage.upper()}_CORPUS_AUDIT_v0.1.json"


def load_stage(plan_path: Path, stage: str, archive_root: Path, corpus_audit_file: Path) -> dict[str, Any]:
    """Every complete world of every arm in the stage, keyed by set then seed, with events
    by condition and positions by condition. Refuses without a PASS corpus audit whose
    hashes match the files read."""
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
            for name in ("events.jsonl", "summary.csv"):
                actual = sha256_file(attempt_dir / name)
                if actual != w["raw_file_sha256"][name]:
                    raise SystemExit(f"{attempt_dir / name}: sha256 {actual} differs from the corpus audit record; refusing")
            observed = w["cell"].split("/")[1]
            events = load_events(attempt_dir / "events.jsonl", observed, float(plan["controlled_configuration"]["sensor_reliability"]))
            summary = load_summary(attempt_dir / "summary.csv")
            for condition, rows in events.items():
                if condition in summary and abs(float(summary[condition]["final_p_a"]) - rows[-1]["p_a"]) > TOLERANCE:
                    problems.append(f"{arm.set_id}/{w['canonical_id']}/{condition}: summary final_p_a disagrees with last event")
                for row in rows:
                    for text in row["inconsistencies"]:
                        problems.append(f"{arm.set_id}/{w['canonical_id']}/{condition}/{row['id']}: {text}")
            worlds[int(w["seed"])] = {
                "canonical_id": w["canonical_id"], "seed": int(w["seed"]), "cell": w["cell"],
                "alignment": w.get("alignment"), "execution_order": w["execution_order"],
                "attempt": w["complete"][0], "attempt_dir": portable_path(attempt_dir),
                "events": events, "summary": summary,
                "positions": {c: positions(rows, arm.topology) for c, rows in events.items()},
            }
        sets[arm.set_id] = {"topology": arm.topology, "rounds": arm.rounds, "root_mode": arm.root_mode,
                            "worlds": worlds}
    return {"plan": plan, "plan_path": plan_path, "gate": gate, "stage": stage, "sets": sets,
            "corpus_audit": {"path": portable_path(corpus_audit_file), "sha256": sha256_file(corpus_audit_file),
                             "status": corpus["status"], "head_commit": corpus.get("head_commit")},
            "problems": problems}


def _set_by_topology(stage: dict[str, Any], topology: str) -> tuple[str, dict[str, Any]] | None:
    for set_id, data in stage["sets"].items():
        if data["topology"] == topology:
            return set_id, data
    return None


# --------------------------------------------------------------------------------------
# Spec 4.3: the five focal tables, paired by seed
# --------------------------------------------------------------------------------------

def focal_tables(stage: dict[str, Any]) -> dict[str, Any]:
    arms = {t: _set_by_topology(stage, t) for t in ("solo", "dyad", "ring", "bounce")}
    seeds = sorted(set.intersection(*[set(v[1]["worlds"]) for v in arms.values() if v]) if any(arms.values()) else set())
    tables: dict[str, Any] = {"paired_seeds": seeds}

    def agent_entries(topology: str, seed: int, condition: str, agent: str) -> list[dict[str, Any]]:
        found = arms.get(topology)
        if not found or seed not in found[1]["worlds"]:
            return []
        return found[1]["worlds"][seed]["positions"][condition]["by_agent"].get(agent, [])

    # Table 1: B in dyad vs ring vs bounce.  Table 2: C in ring vs bounce.
    for name, agent, topologies in (("table_1_B_dyad_ring_bounce", "B", ("dyad", "ring", "bounce")),
                                    ("table_2_C_ring_bounce", "C", ("ring", "bounce"))):
        rows = []
        for condition in ("free", "lineage"):
            for seed in seeds:
                row: dict[str, Any] = {"condition": condition, "seed": seed}
                for topology in topologies:
                    row[topology] = agent_rates(agent_entries(topology, seed, condition, agent))
                rows.append(row)
        tables[name] = rows

    # Table 3: bounce B outward vs return, per cycle.
    rows = []
    for condition in ("free", "lineage"):
        for seed in seeds:
            entries = agent_entries("bounce", seed, condition, "B")
            by_cycle: dict[int, dict[str, Any]] = defaultdict(dict)
            for e in entries:
                by_cycle[e["cycle"]][e["leg"]] = e
            for cycle in sorted(by_cycle):
                legs = by_cycle[cycle]
                if "outward" in legs and "return" in legs:
                    o, r = legs["outward"], legs["return"]
                    rows.append({"condition": condition, "seed": seed, "cycle": cycle,
                                 "outward_id": o["id"], "outward_certainty_excess": o["certainty_excess"],
                                 "return_id": r["id"], "return_certainty_excess": r["certainty_excess"],
                                 "difference_return_minus_outward": round(r["certainty_excess"] - o["certainty_excess"], 6),
                                 "return_magnitude_vs_outward": _compare(abs(r["certainty_excess"]), abs(o["certainty_excess"]))})
    tables["table_3_bounce_B_outward_vs_return"] = rows

    # Table 4: A at every post-seed firing, all four arms.
    rows = []
    for condition in ("free", "lineage"):
        for topology in ("solo", "dyad", "ring", "bounce"):
            found = arms.get(topology)
            if not found:
                continue
            for seed in seeds:
                pos = found[1]["worlds"][seed]["positions"][condition]
                rows.append({"condition": condition, "topology": topology, "seed": seed,
                             "firings": [{"id": e["id"], "hops": e["hops"], "certainty_excess": e["certainty_excess"],
                                          "kind": e["kind"], "at_reference": e["kind"] == "at_reference",
                                          "inbound_agent_as_source": e["inbound_agent_as_source"]} for e in pos["A_post_seed"]],
                             "restoration_rate": pos["A_restoration_rate"],
                             "sustained_deviation": pos["A_sustained_deviation"],
                             "sustained_deviation_at": pos["A_sustained_deviation_at"]})
    tables["table_4_A_post_seed_all_arms"] = rows

    # Table 5: solo A at every step.
    rows = []
    for condition in ("free", "lineage"):
        for seed in seeds:
            entries = agent_entries("solo", seed, condition, "A")
            rows.append({"condition": condition, "seed": seed,
                         "certainty_excess_sequence": [e["certainty_excess"] for e in entries],
                         "kinds": [e["kind"] for e in entries],
                         "any_deviation": any(e["kind"] != "at_reference" for e in entries)})
    tables["table_5_solo_A_every_step"] = rows
    return tables


def _compare(a: float, b: float) -> str:
    if abs(a - b) <= TOLERANCE:
        return "equal"
    return "smaller" if a < b else "larger"


# --------------------------------------------------------------------------------------
# Arm-level aggregates (counts over events; no test)
# --------------------------------------------------------------------------------------

def arm_aggregates(stage: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for set_id, data in stage["sets"].items():
        per_condition: dict[str, Any] = {}
        for condition in ("free", "lineage"):
            agents: dict[str, list[dict[str, Any]]] = defaultdict(list)
            a_post_total = a_post_at_ref = 0
            sustained_worlds = 0
            for world in data["worlds"].values():
                pos = world["positions"].get(condition)
                if pos is None:
                    continue
                for agent, entries in pos["by_agent"].items():
                    agents[agent].extend(e for e in entries if e["post_seed"] or agent != "A")
                a_post_total += len(pos["A_post_seed"])
                a_post_at_ref += sum(e["kind"] == "at_reference" for e in pos["A_post_seed"])
                sustained_worlds += int(pos["A_sustained_deviation"])
            per_condition[condition] = {
                "agents": {agent: agent_rates(entries) for agent, entries in sorted(agents.items())},
                "A_post_seed_events": a_post_total,
                "A_restoration_rate": _rate(a_post_at_ref, a_post_total),
                "worlds_with_sustained_A_deviation": sustained_worlds,
                "worlds": len(data["worlds"]),
            }
            if data["topology"].startswith("bounce"):
                legs: dict[str, list[dict[str, Any]]] = defaultdict(list)
                for world in data["worlds"].values():
                    for e in world["positions"][condition]["by_agent"].get("B", []):
                        legs[e["leg"]].append(e)
                per_condition[condition]["bounce_B_legs"] = {leg: agent_rates(entries) for leg, entries in legs.items()}
        out[set_id] = {"topology": data["topology"], "conditions": per_condition}
    return out


# --------------------------------------------------------------------------------------
# Spec 4.6: expectations E1..E5 by the plan's "would be contradicted by" column
# --------------------------------------------------------------------------------------

def expectations(stage: dict[str, Any], aggregates: dict[str, Any]) -> dict[str, Any]:
    def agg(topology: str, condition: str) -> dict[str, Any] | None:
        found = _set_by_topology(stage, topology)
        return aggregates[found[0]]["conditions"][condition] if found else None

    def rate(topology: str, condition: str, agent: str, key: str) -> float | None:
        a = agg(topology, condition)
        if not a or agent not in a["agents"]:
            return None
        return a["agents"][agent][key]

    out: dict[str, Any] = {}
    L, F = EXPECTATION_CONDITION, "free"

    # E1: ring reproduces the historical pattern: discounts at B and C under LINEAGE, none at A, FREE at reference.
    ring_l, ring_f = agg("ring", L), agg("ring", F)
    if ring_l and ring_f:
        a_discounts = ring_l["agents"].get("A", {}).get("discount_events", 0) + ring_f["agents"].get("A", {}).get("discount_events", 0)
        free_deviations = sum(v["discount_events"] + v["inflation_events"] for v in ring_f["agents"].values())
        bc_discounts = sum(ring_l["agents"].get(x, {}).get("discount_events", 0) for x in ("B", "C"))
        contradicted = a_discounts > 0 or free_deviations > 0 or bc_discounts == 0
        out["E1"] = {"verdict": "contradicted" if contradicted else "consistent",
                     "ring_A_discount_events": a_discounts, "ring_FREE_deviation_events": free_deviations,
                     "ring_LINEAGE_B_plus_C_discount_events": bc_discounts}
    else:
        out["E1"] = {"verdict": "not assessable"}

    # E2: bounce C discounts at least as often as ring C (LINEAGE); bounce B return magnitude < outward magnitude.
    bc, rc = rate("bounce", L, "C", "discount_rate"), rate("ring", L, "C", "discount_rate")
    legs = (agg("bounce", L) or {}).get("bounce_B_legs", {})
    if bc is not None and rc is not None and "outward" in legs and "return" in legs:
        ret, outw = legs["return"]["mean_magnitude"], legs["outward"]["mean_magnitude"]
        contradicted = bc < rc or ret >= outw
        out["E2"] = {"verdict": "contradicted" if contradicted else "consistent",
                     "bounce_C_discount_rate_LINEAGE": bc, "ring_C_discount_rate_LINEAGE": rc,
                     "bounce_B_return_mean_magnitude_LINEAGE": ret, "bounce_B_outward_mean_magnitude_LINEAGE": outw,
                     "FREE": {"bounce_C_discount_rate": rate("bounce", F, "C", "discount_rate"),
                              "ring_C_discount_rate": rate("ring", F, "C", "discount_rate")}}
    else:
        out["E2"] = {"verdict": "not assessable"}

    # E3: dyad B discounts less per event than ring B (LINEAGE).
    db, rb = rate("dyad", L, "B", "discount_rate"), rate("ring", L, "B", "discount_rate")
    if db is not None and rb is not None:
        out["E3"] = {"verdict": "contradicted" if db >= rb else "consistent",
                     "dyad_B_discount_rate_LINEAGE": db, "ring_B_discount_rate_LINEAGE": rb,
                     "FREE": {"dyad_B_discount_rate": rate("dyad", F, "B", "discount_rate"),
                              "ring_B_discount_rate": rate("ring", F, "B", "discount_rate")}}
    else:
        out["E3"] = {"verdict": "not assessable"}

    # E4: A returns to the reference after each echo in every topology, at a rate not below the ring's;
    # contradicted by a sustained deviation in any arm.
    rows = {}
    contradicted = False
    for condition in (F, L):
        ring_rate = (agg("ring", condition) or {}).get("A_restoration_rate")
        for topology in ("solo", "dyad", "ring", "bounce"):
            a = agg(topology, condition)
            if not a:
                continue
            rows[f"{topology}/{condition}"] = {"A_restoration_rate": a["A_restoration_rate"],
                                               "worlds_with_sustained_A_deviation": a["worlds_with_sustained_A_deviation"]}
            if a["worlds_with_sustained_A_deviation"] > 0:
                contradicted = True
            if ring_rate is not None and a["A_restoration_rate"] is not None and a["A_restoration_rate"] < ring_rate:
                contradicted = True
    out["E4"] = {"verdict": ("contradicted" if contradicted else "consistent") if rows else "not assessable", "arms": rows}

    # E5: solo shows no excess in either direction.
    solo_dev = 0
    assessable = False
    for condition in (F, L):
        a = agg("solo", condition)
        if a:
            assessable = True
            solo_dev += sum(v["discount_events"] + v["inflation_events"] for v in a["agents"].values())
    out["E5"] = {"verdict": ("contradicted" if solo_dev > 0 else "consistent") if assessable else "not assessable",
                 "solo_deviation_events_FREE_plus_LINEAGE": solo_dev}

    out["E6"] = {"verdict": "assessed in the synthesis across Set 001 and Set 002, not in a single-stage audit",
                 "ordering_of_arms_by_LINEAGE_discount_rate_this_stage": _ordering(stage, aggregates)}
    return out


def _ordering(stage: dict[str, Any], aggregates: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for set_id, data in stage["sets"].items():
        agents = aggregates[set_id]["conditions"][EXPECTATION_CONDITION]["agents"]
        events = sum(v["events"] for v in agents.values())
        discounts = sum(v["discount_events"] for v in agents.values())
        rows.append({"set": set_id, "topology": data["topology"], "discount_rate_all_agents_post_seed": _rate(discounts, events)})
    return sorted(rows, key=lambda r: (-(r["discount_rate_all_agents_post_seed"] or 0), r["topology"]))


# --------------------------------------------------------------------------------------
# Spec 4.4 / 4.5: family table and MACRO boundary
# --------------------------------------------------------------------------------------

def family_table(stage: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for set_id, data in stage["sets"].items():
        for seed in sorted(data["worlds"], key=lambda s: data["worlds"][s]["execution_order"]):
            world = data["worlds"][seed]
            for condition in CONDITIONS:
                events = world["events"].get(condition)
                if not events:
                    continue
                last = events[-1]
                summary = world["summary"].get(condition, {})
                rows.append({
                    "set": set_id, "topology": data["topology"], "order": world["execution_order"], "seed": seed,
                    "canonical_id": world["canonical_id"], "cell": world["cell"], "condition": condition,
                    "final_answer": last["answer"], "accuracy": last["accuracy"], "final_confidence": last["confidence"],
                    "final_p_a": last["p_a"], "final_reference_p_a": last["reference_p_a"],
                    "final_excess_raw": last["excess_raw"], "final_certainty_excess": last["certainty_excess"],
                    "final_brier": last["brier"], "roots": last["roots"], "max_depth": max(e["depth"] for e in events),
                    "max_redundant_root_exposures": max((e["redundant_root_exposures"] or 0) for e in events),
                    "delta_without_new_evidence": [e["delta_without_new_evidence"] for e in events],
                    "certainty_excess_trajectory": [e["certainty_excess"] for e in events],
                    "erosion_trajectory": [e["erosion"] for e in events],
                    "agent_as_source_events": sum(e["agent_as_source"] for e in events),
                    "first_agent_as_source_event": next((e["id"] for e in events if e["agent_as_source"]), None),
                    "false_independent_support": [e["false_independent_support"] for e in events],
                    "per_agent_final_p_a": summary.get("per_agent_final_p_a"),
                    "per_agent_max_excess": summary.get("per_agent_max_excess"),
                    "per_agent_min_excess": summary.get("per_agent_min_excess"),
                    "events": len(events),
                })
    return rows


def cell_conditional(family: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in family:
        groups[(row["set"], row["cell"], row["condition"])].append(row)
    out = []
    for (set_id, cell, condition), rows in sorted(groups.items()):
        n = len(rows)
        out.append({"set": set_id, "cell": cell, "condition": condition, "n": n,
                    "accuracy": f"{sum(r['accuracy'] for r in rows)}/{n}",
                    "mean_final_confidence": round(sum(r["final_confidence"] for r in rows) / n, 6),
                    "mean_final_certainty_excess": round(sum(r["final_certainty_excess"] for r in rows) / n, 6),
                    "mean_final_brier": round(sum(r["final_brier"] for r in rows) / n, 6)})
    return out


def macro_boundary(stage: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for set_id, data in stage["sets"].items():
        for seed in sorted(data["worlds"], key=lambda s: data["worlds"][s]["execution_order"]):
            world = data["worlds"][seed]
            macro = world["events"].get("macro") or []
            lineage = world["events"].get("lineage") or []
            if not macro:
                continue
            stop = macro[-1]
            lineage_same = next((e for e in lineage if e["id"] == stop["id"]), None)
            summary = world["summary"].get("macro", {})
            rows.append({"set": set_id, "seed": seed, "cell": world["cell"],
                         "macro_stop_triggered": summary.get("macro_stop_triggered"), "stop_reason": summary.get("stop_reason"),
                         "stop_event": stop["id"], "macro_events": len(macro),
                         "macro_certainty_excess_at_stop": stop["certainty_excess"],
                         "lineage_certainty_excess_at_same_event": lineage_same["certainty_excess"] if lineage_same else None,
                         "lineage_final_certainty_excess": lineage[-1]["certainty_excess"] if lineage else None,
                         "all_macro_responses_reused": all(e["response_reused"] for e in macro[1:]) if len(macro) > 1 else None})
    return rows


# --------------------------------------------------------------------------------------
# Stage audit
# --------------------------------------------------------------------------------------

def audit_stage(plan_path: Path, stage: str, archive_root: Path, corpus_audit_file: Path) -> dict[str, Any]:
    data = load_stage(plan_path, stage, archive_root, corpus_audit_file)
    aggregates = arm_aggregates(data)
    family = family_table(data)
    report = {
        "experiment": "EXP-003", "gate": data["gate"], "stage": stage, "spec_version": SPEC_VERSION,
        "plan_version": data["plan"].get("plan_version"), "plan_status": data["plan"].get("status"),
        "plan_sha256": sha256_file(plan_path), "anchors": data["plan"]["anchors"],
        "corpus_audit": data["corpus_audit"], "head_commit": git_output(["rev-parse", "HEAD"], PROJECT_ROOT),
        "archive_root": portable_path(archive_root), "tolerance": TOLERANCE,
        "expectation_condition": EXPECTATION_CONDITION,
        "sets": {set_id: {"topology": d["topology"], "rounds": d["rounds"], "root_mode": d["root_mode"], "worlds": len(d["worlds"]),
                          "cells": dict(Counter(w["cell"] for w in d["worlds"].values()))} for set_id, d in data["sets"].items()},
        "arm_aggregates": aggregates,
        "focal": focal_tables(data),
        "expectations": expectations(data, aggregates),
        "family": family,
        "cell_conditional": cell_conditional(family),
        "macro_boundary": macro_boundary(data),
        "event_rows": {set_id: {str(seed): {c: rows for c, rows in w["events"].items()} for seed, w in d["worlds"].items()}
                       for set_id, d in data["sets"].items()},
        "problems": data["problems"],
        "status": "COMPLETE" if not data["problems"] else "COMPLETE WITH PROBLEMS",
        "boundary": ("Descriptive and pre-registered. Rates are counts over events; no significance test, threshold or "
                     "selected event. This stage is reported alone and is never pooled with the other stage. "
                     "Expectation verdicts restate the frozen plan's 'would be contradicted by' column; they are not "
                     "an interpretation, a causal claim or a ranking. Negative results are retained as written."),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    return report


# --------------------------------------------------------------------------------------
# Spec 4.7: secondary observation, contemporary ring vs the 36 archived EXP-002 ring runs
# --------------------------------------------------------------------------------------

def historical_runs(exp002_archive: Path, reliability: float = 0.70) -> list[dict[str, Any]]:
    """The archived EXP-002 ring runs with truth/E1 reproduced from the seed by the frozen
    EXP-003 generator (single root mode), checked against the archived truth."""
    runs = []
    for events_path in sorted(exp002_archive.rglob("events.jsonl")):
        attempt_dir = events_path.parent
        run_meta = json.loads((attempt_dir / "run_metadata.json").read_text(encoding="utf-8"))
        seed = int(run_meta["seed"])
        world = WorldGenerator(seed, "ring", "single", reliability).generate()
        cell = world_cell(world)
        summary = load_summary(attempt_dir / "summary.csv")
        archived_truth = {row["truth"] for row in summary.values()}
        if archived_truth != {world.truth}:
            raise SystemExit(f"{attempt_dir}: generator truth {world.truth} differs from archived truth {archived_truth}")
        observed = cell.split("/")[1]
        events = load_events(events_path, observed, reliability)
        runs.append({"label": str(attempt_dir.relative_to(exp002_archive)), "seed": seed, "cell": cell,
                     "run_class": run_meta.get("run_class"), "attempt_dir": attempt_dir,
                     "events": events, "positions": {c: positions(rows, "ring") for c, rows in events.items()}})
    return runs


def _ring_position_summary(worlds: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for condition in ("free", "lineage"):
        agents: dict[str, list[dict[str, Any]]] = defaultdict(list)
        a_total = a_ref = sustained = 0
        for w in worlds:
            pos = w["positions"].get(condition)
            if not pos:
                continue
            for agent, entries in pos["by_agent"].items():
                agents[agent].extend(e for e in entries if e["post_seed"] or agent != "A")
            a_total += len(pos["A_post_seed"])
            a_ref += sum(e["kind"] == "at_reference" for e in pos["A_post_seed"])
            sustained += int(pos["A_sustained_deviation"])
        out[condition] = {"runs": len(worlds), "agents": {a: agent_rates(e) for a, e in sorted(agents.items())},
                          "A_restoration_rate": _rate(a_ref, a_total), "runs_with_sustained_A_deviation": sustained}
    return out


def historical_observation(plan_path: Path, set_id: str, archive_root: Path, corpus_audit_file: Path,
                           exp002_archive: Path) -> dict[str, Any]:
    stage = next(a.stage for a in plan_arms(load_plan(plan_path), plan_path) if a.set_id == set_id)
    data = load_stage(plan_path, stage, archive_root, corpus_audit_file)
    contemporary = data["sets"][set_id]
    if contemporary["topology"] != "ring":
        raise SystemExit(f"{set_id} is not a ring arm")
    historical = historical_runs(exp002_archive, float(data["plan"]["controlled_configuration"]["sensor_reliability"]))
    first_contemporary = next(iter(contemporary["worlds"].values()))
    ledger_diff = diff_factors(factors_for(PROJECT_ROOT / first_contemporary["attempt_dir"]),
                               factors_for(historical[0]["attempt_dir"]))
    by_class = Counter(r["run_class"] for r in historical)
    return {
        "experiment": "EXP-003", "gate": data["gate"], "kind": "SECONDARY OBSERVATION", "spec_version": SPEC_VERSION,
        "contemporary_set": set_id, "contemporary_worlds": len(contemporary["worlds"]),
        "historical_archive": portable_path(exp002_archive), "historical_runs": len(historical),
        "historical_run_classes": dict(by_class),
        "historical_distinct_seeds": len({r["seed"] for r in historical}),
        "historical_cells": dict(Counter(r["cell"] for r in historical)),
        "factor_ledger_difference": {k: list(v) for k, v in ledger_diff.items()},
        "contemporary": _ring_position_summary(list(contemporary["worlds"].values())),
        "historical": _ring_position_summary(historical),
        "historical_gate_2b_only": _ring_position_summary([r for r in historical if r["run_class"] == "gate_2b_real_model"]),
        "corpus_audit": data["corpus_audit"], "head_commit": git_output(["rev-parse", "HEAD"], PROJECT_ROOT),
        "boundary": ("Secondary observation only. Same prompts, same model name, different dates; any difference is model "
                     "drift over time and is recorded, never used to adjust a Gate 3A outcome. Sixteen of the historical "
                     "runs are repeated executions of one world (seed 42); they are shown pooled and with the Gate 2B "
                     "worlds alone. No test, no threshold."),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


# --------------------------------------------------------------------------------------
# Markdown
# --------------------------------------------------------------------------------------

def _f(x: Any) -> str:
    if x is None:
        return "n/a"
    if isinstance(x, float):
        return f"{x:+.3f}" if x < 0 or 0 < x < 1 else f"{x:.3f}"
    return str(x)


def _rates_cell(r: dict[str, Any]) -> str:
    if not r or not r["events"]:
        return "n/a"
    return f"{r['discount_events']}d/{r['inflation_events']}i/{r['at_reference_events']}r of {r['events']} (|x̄| {r['mean_magnitude']:.3f})"


def render_markdown(r: dict[str, Any]) -> str:
    L = [f"# EXP-003 Gate {r['gate']} {r['stage'].replace('_', ' ').title()} Primary-Outcome Audit v0.1", "",
         "## Status", "", f"**{r['status']}**", "", r["boundary"], "",
         "## Provenance", "",
         f"- Specification: `{r['spec_version']}`",
         f"- Plan: `{r['plan_version']}` (status `{r['plan_status']}`, sha256 `{r['plan_sha256']}`)",
         f"- Frozen runtime: `{r['anchors'].get('frozen_runtime')}`; protocol tag `{r['anchors'].get('protocol_tag')}`",
         f"- Corpus audit: `{r['corpus_audit']['path']}` (status {r['corpus_audit']['status']}, sha256 `{r['corpus_audit']['sha256']}`)",
         f"- HEAD at audit time: `{r['head_commit']}`",
         f"- Direction: certainty_excess = p_observed − reference_observed; tolerance {r['tolerance']}; "
         f"d = discount, i = inflation, r = at reference; expectations assessed on `{r['expectation_condition']}`", "",
         "## Sets", "", "| Set | Topology | Rounds | Worlds | Cells |", "|---|---|---:|---:|---|"]
    for set_id, s in r["sets"].items():
        L.append(f"| `{set_id}` | {s['topology']} | {s['rounds']} | {s['worlds']} | {', '.join(f'{k}: {v}' for k, v in sorted(s['cells'].items()))} |")

    L += ["", "## Arm aggregates (post-seed events, counts over events)", "",
          "| Set | Condition | A | B | C | A restoration | Worlds with sustained A deviation |", "|---|---|---|---|---|---:|---:|"]
    for set_id, agg in r["arm_aggregates"].items():
        for condition, c in agg["conditions"].items():
            L.append(f"| `{set_id}` | {condition} | {_rates_cell(c['agents'].get('A'))} | {_rates_cell(c['agents'].get('B'))} | "
                     f"{_rates_cell(c['agents'].get('C'))} | {_f(c['A_restoration_rate'])} | {c['worlds_with_sustained_A_deviation']}/{c['worlds']} |")
            if "bounce_B_legs" in c:
                legs = c["bounce_B_legs"]
                L.append(f"| `{set_id}` | {condition} B legs | outward {_rates_cell(legs.get('outward'))} | return {_rates_cell(legs.get('return'))} | | | |")

    e = r["expectations"]
    L += ["", "## Pre-registered expectations (restated by the plan's 'would be contradicted by' column)", "",
          "| Id | Verdict | Quantities |", "|---|---|---|"]
    for key in ("E1", "E2", "E3", "E4", "E5", "E6"):
        v = e[key]
        quantities = {k: val for k, val in v.items() if k != "verdict"}
        L.append(f"| {key} | **{v['verdict']}** | `{json.dumps(quantities, default=str)}` |")

    foc = r["focal"]
    L += ["", f"## Focal comparisons, paired by world (seeds: {len(foc['paired_seeds'])})", "",
          "### Table 1: B in dyad vs ring vs bounce", "", "| Condition | Seed | dyad B | ring B | bounce B |", "|---|---:|---|---|---|"]
    for row in foc["table_1_B_dyad_ring_bounce"]:
        L.append(f"| {row['condition']} | {row['seed']} | {_rates_cell(row['dyad'])} | {_rates_cell(row['ring'])} | {_rates_cell(row['bounce'])} |")
    L += ["", "### Table 2: C in ring vs bounce", "", "| Condition | Seed | ring C | bounce C |", "|---|---:|---|---|"]
    for row in foc["table_2_C_ring_bounce"]:
        L.append(f"| {row['condition']} | {row['seed']} | {_rates_cell(row['ring'])} | {_rates_cell(row['bounce'])} |")
    L += ["", "### Table 3: bounce B outward (B→C) vs return (B→A), per cycle", "",
          "| Condition | Seed | Cycle | Outward | Return | Return − outward | Return magnitude |", "|---|---:|---:|---|---|---:|---|"]
    for row in foc["table_3_bounce_B_outward_vs_return"]:
        L.append(f"| {row['condition']} | {row['seed']} | {row['cycle']} | {row['outward_id']} {_f(row['outward_certainty_excess'])} | "
                 f"{row['return_id']} {_f(row['return_certainty_excess'])} | {_f(row['difference_return_minus_outward'])} | {row['return_magnitude_vs_outward']} |")
    L += ["", "### Table 4: A at every post-seed firing (hops = firings since A's previous firing)", "",
          "| Condition | Topology | Seed | Firings (id: certainty_excess) | Restoration | Sustained deviation |", "|---|---|---:|---|---:|---|"]
    for row in foc["table_4_A_post_seed_all_arms"]:
        firings = ", ".join(f"{f['id']}[{f['hops']}h]: {_f(f['certainty_excess'])}{'*' if f['inbound_agent_as_source'] else ''}" for f in row["firings"])
        L.append(f"| {row['condition']} | {row['topology']} | {row['seed']} | {firings} | {_f(row['restoration_rate'])} | "
                 f"{'yes at ' + ', '.join(row['sustained_deviation_at']) if row['sustained_deviation'] else 'no'} |")
    L.append("")
    L.append("`*` = the inbound message carried the agent-as-source mark.")
    L += ["", "### Table 5: solo A at every step", "", "| Condition | Seed | certainty_excess per firing | Any deviation |", "|---|---:|---|---|"]
    for row in foc["table_5_solo_A_every_step"]:
        L.append(f"| {row['condition']} | {row['seed']} | {', '.join(_f(x) for x in row['certainty_excess_sequence'])} | {'yes' if row['any_deviation'] else 'no'} |")

    L += ["", "## Primary outcome table by world (EXP-002 family)", "",
          "| Set | Order | Seed | Cell | Condition | Final | Acc | Conf | P(A) | Ref | certainty_excess | Brier | Roots | Depth | Erosion | agent-as-source |",
          "|---|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|"]
    for row in r["family"]:
        L.append(f"| `{row['set']}` | {row['order']} | {row['seed']} | {row['cell']} | {row['condition']} | {row['final_answer']} | {row['accuracy']} | "
                 f"{row['final_confidence']:.2f} | {row['final_p_a']:.3f} | {row['final_reference_p_a']:.2f} | {_f(row['final_certainty_excess'])} | "
                 f"{row['final_brier']:.3f} | {row['roots']} | {row['max_depth']} | {','.join(str(x) for x in row['erosion_trajectory'])} | "
                 f"{row['agent_as_source_events']}{' (' + row['first_agent_as_source_event'] + ')' if row['first_agent_as_source_event'] else ''} |")

    L += ["", "## Cell-conditional (truth/E1); unbalanced because worlds were unfiltered; mean P(A) is not averaged across cells", "",
          "| Set | Cell | Condition | n | Accuracy | Mean final confidence | Mean final certainty_excess | Mean final Brier |", "|---|---|---|---:|---:|---:|---:|---:|"]
    for row in r["cell_conditional"]:
        L.append(f"| `{row['set']}` | {row['cell']} | {row['condition']} | {row['n']} | {row['accuracy']} | {row['mean_final_confidence']:.3f} | "
                 f"{_f(row['mean_final_certainty_excess'])} | {row['mean_final_brier']:.3f} |")

    L += ["", "## MACRO stopping boundary (reuses paired LINEAGE responses; not an independent trajectory)", "",
          "| Set | Seed | Cell | Stop triggered | Reason | Stop event | MACRO events | certainty_excess at stop (MACRO / LINEAGE same event) | LINEAGE final | Responses reused |",
          "|---|---:|---|---|---|---|---:|---|---:|---|"]
    for row in r["macro_boundary"]:
        L.append(f"| `{row['set']}` | {row['seed']} | {row['cell']} | {row['macro_stop_triggered']} | {row['stop_reason']} | {row['stop_event']} | {row['macro_events']} | "
                 f"{_f(row['macro_certainty_excess_at_stop'])} / {_f(row['lineage_certainty_excess_at_same_event'])} | {_f(row['lineage_final_certainty_excess'])} | {row['all_macro_responses_reused']} |")

    L += ["", "## Problems", ""]
    L += [f"- {p}" for p in r["problems"]] or ["None."]
    L += ["", "## Boundary", "", r["boundary"], "",
          "Not performed here: pooling of stages, comparison against the historical EXP-002 ring (separate secondary file), "
          "E6 (synthesis), any significance test or threshold, any causal statement.", ""]
    return "\n".join(L)


def render_historical_markdown(r: dict[str, Any]) -> str:
    L = [f"# EXP-003 Gate {r['gate']} Historical Ring Observation v0.1 (secondary)", "", "## Status", "",
         f"**{r['kind']}**", "", r["boundary"], "", "## Provenance", "",
         f"- Contemporary set: `{r['contemporary_set']}` ({r['contemporary_worlds']} worlds); corpus audit `{r['corpus_audit']['path']}` ({r['corpus_audit']['status']})",
         f"- Historical archive: `{r['historical_archive']}`: {r['historical_runs']} runs, {r['historical_distinct_seeds']} distinct seeds, "
         f"run classes {r['historical_run_classes']}, cells {r['historical_cells']}",
         f"- Factor ledger difference (contemporary vs historical): `{json.dumps(r['factor_ledger_difference'], default=str)}`",
         f"- HEAD at audit time: `{r['head_commit']}`", "",
         "## Per-position summary (post-seed events; d = discount, i = inflation, r = at reference)", "",
         "| Corpus | Condition | Runs | A | B | C | A restoration | Sustained A deviation |", "|---|---|---:|---|---|---|---:|---:|"]
    for name in ("contemporary", "historical", "historical_gate_2b_only"):
        for condition, c in r[name].items():
            L.append(f"| {name} | {condition} | {c['runs']} | {_rates_cell(c['agents'].get('A'))} | {_rates_cell(c['agents'].get('B'))} | "
                     f"{_rates_cell(c['agents'].get('C'))} | {_f(c['A_restoration_rate'])} | {c['runs_with_sustained_A_deviation']} |")
    L += ["", "## Boundary", "", r["boundary"], ""]
    return "\n".join(L)


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=EXP003 / "GATE_3A_PLAN_v0.1.json")
    parser.add_argument("--stage", help="stage to audit (set_001 or set_002)")
    parser.add_argument("--archive-root", type=Path, default=None)
    parser.add_argument("--corpus-audit", type=Path, default=None, help="default audits/gate_<x>/..._CORPUS_AUDIT_v0.1.json")
    parser.add_argument("--out-dir", type=Path, default=None, help="default experiments/EXP_003/audits/gate_<x>/")
    parser.add_argument("--historical", action="store_true", help="write the secondary historical-ring observation instead")
    parser.add_argument("--set-id", default="ring_control_set_001", help="with --historical: the contemporary ring set")
    parser.add_argument("--exp002-archive", type=Path, default=EXP002_ARCHIVE)
    args = parser.parse_args()
    plan = load_plan(args.plan)
    gate = plan["gate"]
    archive_root = args.archive_root or DEFAULT_ARCHIVE_ROOT
    out_dir = args.out_dir or (EXP003 / "audits" / f"gate_{gate.lower()}")
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.historical:
        stage = next(a.stage for a in plan_arms(plan, args.plan) if a.set_id == args.set_id)
        corpus_file = args.corpus_audit or corpus_audit_path(gate, stage, args.out_dir)
        report = historical_observation(args.plan, args.set_id, archive_root, corpus_file, args.exp002_archive)
        stem = out_dir / f"EXP_003_GATE_{gate.upper()}_HISTORICAL_RING_OBSERVATION_v0.1"
        stem.with_suffix(".json").write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
        stem.with_suffix(".md").write_text(render_historical_markdown(report), encoding="utf-8")
        print(f"SECONDARY OBSERVATION written: contemporary {report['contemporary_worlds']} worlds vs historical {report['historical_runs']} runs")
        print(f"wrote {stem}.json and .md")
        return

    if not args.stage:
        raise SystemExit("--stage is required (or use --historical)")
    corpus_file = args.corpus_audit or corpus_audit_path(gate, args.stage, args.out_dir)
    report = audit_stage(args.plan, args.stage, archive_root, corpus_file)
    stem = out_dir / f"EXP_003_GATE_{gate.upper()}_{args.stage.upper()}_PRIMARY_OUTCOME_AUDIT_v0.1"
    stem.with_suffix(".json").write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    stem.with_suffix(".md").write_text(render_markdown(report), encoding="utf-8")
    verdicts = ", ".join(f"{k}={report['expectations'][k]['verdict']}" for k in ("E1", "E2", "E3", "E4", "E5"))
    print(f"{report['status']}: {sum(s['worlds'] for s in report['sets'].values())} worlds; {verdicts}")
    print(f"wrote {stem}.json and .md")
    if report["problems"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
