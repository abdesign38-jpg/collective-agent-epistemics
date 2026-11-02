"""EXP-003 Gate 3C primary-outcome audit (pre-registered, mechanical, read-only).

Implements GATE_3C_PRIMARY_OUTCOME_AUDIT_SPEC_v0.1 for one stage of the Gate 3C archive:
source detachment on worlds that have a re-grounded twin. Every detached world is paired with
its twin (contemporary Gate 3C arm, or an archived Gate 3A / Gate 3B execution read by the
hashes recorded in that gate's committed corpus audit), position by position at matched
visible message ids. The tool

  * refuses to run unless the stage's corpus audit is PASS and every twin file matches the
    hash its corpus audit recorded;
  * performs the manipulation check on archived prompts (detached A post-seed prompts carry
    "Direct observation: none"; twin A prompts carry the observation block; identical structure
    otherwise) and refuses to produce verdicts if it fails;
  * reports the seed-firing comparability table (identical prompt, sampled twice);
  * computes within-agent trajectories, paired differences, far-agent compounding, relay-
    position marker loss, origin behaviour after lineage return, the solo null and the drift
    gauge, and restates the plan's expectations E1 to E6 as verdicts by the spec's rules
    (E7 belongs to the synthesis).

It introduces no measurement: every quantity is an archived field or arithmetic over archived
fields, cross-checked against the raw answer, confidence and roots with the frozen runtime's
own functions. Stages are never pooled. Twins are reported with their execution dates and
the gap in days; nothing is corrected for drift.

Usage (defaults are the committed paths):
    python -m experiments.EXP_003.tools.gate3c_primary_outcome_audit --stage set_001
    python -m experiments.EXP_003.tools.gate3c_primary_outcome_audit --stage set_002
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..gate_orchestrator import DEFAULT_ARCHIVE_ROOT, PROJECT_ROOT, load_plan, plan_arms
from .corpus_audit import git_output, portable_path, sha256_file
from .gate3b_primary_outcome_audit import event_row as _gate3b_event_row
from .gate3b_primary_outcome_audit import world_evidence
from .primary_outcome_audit import output_paths

EXP003 = Path(__file__).resolve().parents[1]
AUDITS = EXP003 / "audits"
SPEC_VERSION = "EXP-003-GATE-3C-PRIMARY-OUTCOME-AUDIT-SPEC-v0.1"
TOLERANCE = 1e-6          # kind labels (at reference / discount / inflation), as Gate 3A
THRESHOLD = 0.01          # event, displacement and class threshold, spec sections 6-7
FLAT_BAND = 0.005         # sign flat band for stage means, spec E7 convention
MAJORITY = 7              # of 12 worlds: a strict majority; majority_of(n) generalises it to n paired worlds
GAUGE_COUNT_TOL = 4       # of 48 LINEAGE firings per position, spec 9
GAUGE_WORLD_TOL = 0.02    # per-world paired mean excess, spec 9
GAUGE_WORLDS = 10         # of 12: five sixths; gauge_worlds_required(n) generalises it to n paired worlds


def majority_of(n: int) -> int:
    """Strict majority of n paired worlds; 7 of 12 in the plan."""
    return n // 2 + 1


def gauge_worlds_required(n: int) -> int:
    """Five sixths of n paired worlds, rounded up; 10 of 12 in the plan."""
    return max(1, -(-n * GAUGE_WORLDS // 12))
CONDITIONS = ("free", "lineage", "macro")
PAIRED_CONDITIONS = ("free", "lineage")
LADDER = ("ring", "bounce", "dyad", "solo")   # Gate 3A ordering, E5
ORIGIN_RETURN_SHAPES = ("ring", "bounce", "diamond")   # A receives a descendant of its own lineage
FAR_AGENT = {"ring": "C", "bounce": "C", "dyad": "B", "solo": "A", "diamond": "D"}
RELAY_AGENTS = {"ring": ("B", "C"), "bounce": ("B", "C"), "dyad": ("B",), "solo": (), "diamond": ("B", "C", "D")}
PROMPT_SKELETON_PREFIXES = ("You are Agent", "Received message", "Sender:", "Message metadata:", "Evidence roots:",
                            "Derived from:", "Inference depth:", "New external evidence:")


def base_topology(name: str) -> str:
    return name[:-len("_detached")] if name.endswith("_detached") else name


# --------------------------------------------------------------------------------------
# Twins
# --------------------------------------------------------------------------------------

@dataclass(frozen=True)
class TwinRef:
    gate_dir: str          # "gate_3c", "gate_3a", "gate_3b"
    set_id: str
    corpus_audit: Path     # the committed corpus audit record that lists the twin's file hashes
    kind: str              # "contemporary" | "historical"


def default_twins(stage: str, archive_root: Path) -> dict[str, TwinRef]:
    """Spec 2 and 10: the pairing of every detached arm, plus the drift gauge pair."""
    a = AUDITS / "gate_3a"
    b = AUDITS / "gate_3b"
    c = AUDITS / "gate_3c"
    if stage == "set_001":
        return {
            "ring_detached_set_001": TwinRef("gate_3c", "ring_contemporary_set_001", c / "EXP_003_GATE_3C_SET_001_CORPUS_AUDIT_v0.1.json", "contemporary"),
            "solo_detached_set_001": TwinRef("gate_3c", "solo_contemporary_set_001", c / "EXP_003_GATE_3C_SET_001_CORPUS_AUDIT_v0.1.json", "contemporary"),
            "dyad_detached_set_001": TwinRef("gate_3c", "dyad_contemporary_set_001", c / "EXP_003_GATE_3C_SET_001_CORPUS_AUDIT_v0.1.json", "contemporary"),
            "bounce_detached_set_001": TwinRef("gate_3c", "bounce_contemporary_set_001", c / "EXP_003_GATE_3C_SET_001_CORPUS_AUDIT_v0.1.json", "contemporary"),
            "diamond_detached_set_001": TwinRef("gate_3b", "diamond_set_001", b / "EXP_003_GATE_3B_SET_001_CORPUS_AUDIT_v0.1.json", "historical"),
            # drift gauge: the contemporary ring against the archived Gate 3A ring on the same worlds
            "ring_contemporary_set_001": TwinRef("gate_3a", "ring_control_set_001", a / "EXP_003_GATE_3A_SET_001_CORPUS_AUDIT_v0.1.json", "historical"),
        }
    if stage == "set_002":
        return {
            "ring_detached_set_002": TwinRef("gate_3a", "ring_control_set_002", a / "EXP_003_GATE_3A_SET_002_CORPUS_AUDIT_v0.1.json", "historical"),
            "solo_detached_set_002": TwinRef("gate_3a", "solo_control_set_002", a / "EXP_003_GATE_3A_SET_002_CORPUS_AUDIT_v0.1.json", "historical"),
            "dyad_detached_set_002": TwinRef("gate_3a", "dyad_set_002", a / "EXP_003_GATE_3A_SET_002_CORPUS_AUDIT_v0.1.json", "historical"),
            "bounce_detached_set_002": TwinRef("gate_3a", "bounce_set_002", a / "EXP_003_GATE_3A_SET_002_CORPUS_AUDIT_v0.1.json", "historical"),
            "diamond_detached_set_002": TwinRef("gate_3b", "diamond_set_002", b / "EXP_003_GATE_3B_SET_002_CORPUS_AUDIT_v0.1.json", "historical"),
        }
    raise SystemExit(f"unknown stage {stage!r}")


# --------------------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------------------

def event_row(record: dict[str, Any], evidence: tuple) -> dict[str, Any]:
    """The Gate 3B row (with its raw-output cross-checks) plus the fields Gate 3C needs."""
    row = _gate3b_event_row(record, evidence)
    prov = record.get("provenance") or {}
    row["reliability_named"] = bool(prov.get("reliability_named"))
    row["message"] = record.get("agent_reported_information", "")
    row["prompt"] = record.get("model_visible_input", "")
    return row


def load_events(events_path: Path, evidence: tuple) -> dict[str, list[dict[str, Any]]]:
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


def load_set(archive_root: Path, gate_dir: str, set_id: str, corpus: dict[str, Any], problems: list[str],
             label: str) -> dict[str, Any]:
    """Worlds of one archived set, by seed, with every raw file re-checked against the corpus audit."""
    record = corpus["sets"].get(set_id)
    if record is None:
        raise SystemExit(f"{label}: corpus audit {portable_path(Path(corpus.get('archive_root', '')))} has no set {set_id!r}")
    set_dir = archive_root / gate_dir / set_id
    worlds: dict[int, dict[str, Any]] = {}
    for w in record["worlds"]:
        if not w["complete"]:
            problems.append(f"{label}: {w['canonical_id']} has no complete attempt")
            continue
        attempt_dir = set_dir / w["canonical_id"] / w["complete"][0]
        for name, expected in w["raw_file_sha256"].items():
            path = attempt_dir / name
            if not path.exists():
                problems.append(f"{label}: missing {portable_path(path)}")
                continue
            if sha256_file(path) != expected:
                problems.append(f"{label}: {portable_path(path)} differs from the hash in its corpus audit")
        evidence = world_evidence(attempt_dir)
        events = load_events(attempt_dir / "events.jsonl", evidence)
        for condition, rows in events.items():
            for r in rows:
                for inc in r["inconsistencies"]:
                    problems.append(f"{label}: {w['canonical_id']} {condition} {r['id']}: {inc}")
        meta = json.loads((attempt_dir / "archive_metadata.json").read_text(encoding="utf-8"))
        worlds[int(w["seed"])] = {
            "seed": int(w["seed"]), "canonical_id": w["canonical_id"], "execution_order": w["execution_order"],
            "cell": w["cell"], "attempt": w["complete"][0], "events": events,
            "timestamp_utc": meta.get("timestamp_utc"), "regrounding": meta.get("factors", {}).get("regrounding"),
        }
    return {"set_id": set_id, "gate_dir": gate_dir, "topology": record["topology"], "rounds": record["rounds"],
            "probe": record["probe"], "worlds": worlds}


def corpus_audit_path(gate: str, stage: str, out_dir: Path | None = None) -> Path:
    base = out_dir or (AUDITS / f"gate_{gate.lower()}")
    return base / f"EXP_003_GATE_{gate.upper()}_{stage.upper()}_CORPUS_AUDIT_v0.1.json"


def _days_between(a: str | None, b: str | None) -> int | None:
    if not a or not b:
        return None
    return abs((datetime.fromisoformat(a) - datetime.fromisoformat(b)).days)


def load_stage(plan_path: Path, stage: str, archive_root: Path, corpus_audit_file: Path,
               twins: dict[str, TwinRef] | None = None) -> dict[str, Any]:
    plan = load_plan(plan_path)
    gate = plan["gate"]
    if not corpus_audit_file.exists():
        raise SystemExit(f"corpus audit record missing: {corpus_audit_file}; run corpus_audit first")
    corpus = json.loads(corpus_audit_file.read_text(encoding="utf-8"))
    if corpus.get("status") != "PASS":
        raise SystemExit(f"corpus audit status is {corpus.get('status')!r}, not PASS; refusing")
    problems: list[str] = []
    twins = twins if twins is not None else default_twins(stage, archive_root)
    arms = [a for a in plan_arms(plan, plan_path) if a.stage == stage]
    sets: dict[str, dict[str, Any]] = {}
    for arm in arms:
        sets[arm.set_id] = load_set(archive_root, f"gate_{gate.lower()}", arm.set_id, corpus, problems, arm.set_id)
        sets[arm.set_id]["detached"] = arm.topology.endswith("_detached")
        sets[arm.set_id]["base"] = base_topology(arm.topology)
    twin_sets: dict[str, dict[str, Any]] = {}
    twin_corpora: dict[str, dict[str, Any]] = {}
    for set_id, ref in twins.items():
        if set_id not in sets:
            continue
        if not ref.corpus_audit.exists():
            raise SystemExit(f"twin corpus audit missing: {ref.corpus_audit}")
        tc = json.loads(ref.corpus_audit.read_text(encoding="utf-8"))
        if tc.get("status") != "PASS":
            raise SystemExit(f"twin corpus audit {portable_path(ref.corpus_audit)} is not PASS; refusing")
        twin_corpora[set_id] = {"path": portable_path(ref.corpus_audit), "sha256": sha256_file(ref.corpus_audit)}
        if ref.gate_dir == f"gate_{gate.lower()}" and ref.set_id in sets:
            twin_sets[set_id] = sets[ref.set_id]
        else:
            twin_sets[set_id] = load_set(archive_root, ref.gate_dir, ref.set_id, tc, problems, f"twin of {set_id}")
        twin_sets[set_id] = dict(twin_sets[set_id], kind=ref.kind, twin_gate=ref.gate_dir)
        if set(sets[set_id]["worlds"]) != set(twin_sets[set_id]["worlds"]):
            problems.append(f"{set_id}: seeds differ from its twin {ref.set_id}")
    return {"plan": plan, "gate": gate, "stage": stage, "sets": sets, "twins": twin_sets, "twin_corpora": twin_corpora,
            "corpus_audit": {"path": portable_path(corpus_audit_file), "sha256": sha256_file(corpus_audit_file),
                             "status": corpus.get("status")},
            "problems": problems}


# --------------------------------------------------------------------------------------
# Helpers over rows
# --------------------------------------------------------------------------------------

def post_seed(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [r for r in rows if (r["cycle"] or 0) > 0]


def by_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {r["id"]: r for r in rows}


def _mean(values: list[float]) -> float | None:
    return round(sum(values) / len(values), 6) if values else None


def _sign(x: float | None) -> str:
    if x is None:
        return "n/a"
    if abs(x) <= FLAT_BAND:
        return "flat"
    return "positive" if x > 0 else "negative"


def _class(delta: float | None) -> str:
    if delta is None:
        return "n/a"
    if delta > THRESHOLD:
        return "increasing"
    if delta < -THRESHOLD:
        return "decreasing"
    return "stable"


def _modal(classes: list[str]) -> tuple[str | None, bool]:
    """(modal class, tie) with ties counting as not greater."""
    if not classes:
        return None, False
    counts = Counter(classes).most_common()
    if len(counts) > 1 and counts[0][1] == counts[1][1]:
        return counts[0][0], True
    return counts[0][0], False


def prompt_skeleton(prompt: str) -> list[str]:
    """Structural lines of a prompt, excluding the direct-observation block (spec 5.2)."""
    return [line.strip() for line in prompt.splitlines() if line.strip().startswith(PROMPT_SKELETON_PREFIXES)]


def origin_inbound(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """For each post-seed A firing, the rows A received since its previous firing."""
    out: dict[str, list[dict[str, Any]]] = {}
    pending: list[dict[str, Any]] = []
    for r in rows:
        if r["sender"] == "A":
            if (r["cycle"] or 0) > 0:
                out[r["id"]] = list(pending)
            pending = []
        if "A" in r["receivers"] and r["sender"] != "A":
            pending.append(r)
    return out


# --------------------------------------------------------------------------------------
# Spec 5: integrity-level checks
# --------------------------------------------------------------------------------------

def manipulation_check(detached: dict[str, Any], twin: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for seed, w in detached["worlds"].items():
        t = twin["worlds"].get(seed)
        for condition in PAIRED_CONDITIONS:
            rows = w["events"].get(condition, [])
            trows = t["events"].get(condition, []) if t else []
            tid = by_id(trows)
            for r in rows:
                if r["sender"] == "A":
                    if (r["cycle"] or 0) == 0:
                        if "Direct observation:" not in r["prompt"] or "Source: sensor_1" not in r["prompt"]:
                            failures.append(f"{detached['set_id']} {w['canonical_id']} {condition} {r['id']}: seed prompt lacks the observation block")
                    elif "Direct observation: none" not in r["prompt"]:
                        failures.append(f"{detached['set_id']} {w['canonical_id']} {condition} {r['id']}: detached A prompt still shows an observation")
                tr = tid.get(r["id"])
                if tr is None:
                    failures.append(f"{detached['set_id']} {w['canonical_id']} {condition} {r['id']}: no twin firing at this id")
                    continue
                if tr["sender"] != r["sender"] or tr["cycle"] != r["cycle"]:
                    failures.append(f"{detached['set_id']} {w['canonical_id']} {condition} {r['id']}: twin sender/cycle differ")
                if tr["sender"] == "A" and ("Direct observation:" not in tr["prompt"] or "Direct observation: none" in tr["prompt"]):
                    failures.append(f"{detached['set_id']} {w['canonical_id']} {condition} {r['id']}: twin A prompt lacks the observation block")
                if prompt_skeleton(r["prompt"]) != prompt_skeleton(tr["prompt"]):
                    failures.append(f"{detached['set_id']} {w['canonical_id']} {condition} {r['id']}: prompt structure differs from twin")
    return failures


def seed_comparability(detached: dict[str, Any], twin: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for seed, w in sorted(detached["worlds"].items(), key=lambda kv: kv[1]["execution_order"]):
        t = twin["worlds"].get(seed)
        d0 = next((r for r in w["events"].get("free", []) if (r["cycle"] or 0) == 0), None)
        t0 = next((r for r in t["events"].get("free", []) if (r["cycle"] or 0) == 0), None) if t else None
        if d0 is None or t0 is None:
            continue
        diff = round(abs(d0["p_a"] - t0["p_a"]), 6)
        rows.append({"seed": seed, "p_a_detached": d0["p_a"], "p_a_twin": t0["p_a"], "abs_difference": diff,
                     "message_identical": d0["message"] == t0["message"]})
    dist = {"zero": sum(1 for r in rows if r["abs_difference"] == 0),
            "le_0.01": sum(1 for r in rows if 0 < r["abs_difference"] <= 0.01),
            "le_0.05": sum(1 for r in rows if 0.01 < r["abs_difference"] <= 0.05),
            "gt_0.05": sum(1 for r in rows if r["abs_difference"] > 0.05)}
    return {"rows": rows, "distribution": dist, "worlds": len(rows)}


# --------------------------------------------------------------------------------------
# Spec 6-7: quantities and expectations
# --------------------------------------------------------------------------------------

def paired_world(w: dict[str, Any], t: dict[str, Any], condition: str) -> dict[str, Any] | None:
    rows = post_seed(w["events"].get(condition, []))
    tid = by_id(t["events"].get(condition, []))
    d_by_cycle: dict[int, list[float]] = defaultdict(list)
    signed: list[float] = []
    absolute: list[float] = []
    matched = 0
    for r in rows:
        tr = tid.get(r["id"])
        if tr is None or r["certainty_excess"] is None or tr["certainty_excess"] is None:
            continue
        d = round(r["certainty_excess"] - tr["certainty_excess"], 6)
        matched += 1
        signed.append(d)
        absolute.append(abs(d))
        d_by_cycle[int(r["cycle"])].append(abs(d))
    if not matched:
        return None
    cycles = sorted(d_by_cycle)
    c = {k: _mean(d_by_cycle[k]) for k in cycles}
    c_first, c_last = c[cycles[0]], c[cycles[-1]]
    delta = round(c_last - c_first, 6)
    lo, hi = min(c_first, c_last), max(c_first, c_last)
    non_monotonic = any(c[k] < lo - THRESHOLD or c[k] > hi + THRESHOLD for k in cycles[1:-1])
    a_bar = _mean(absolute)
    return {"matched_positions": matched, "mean_abs_difference": a_bar, "mean_signed_difference": _mean(signed),
            "material_displacement": a_bar > THRESHOLD, "c_by_cycle": {str(k): c[k] for k in cycles},
            "c_last_minus_first": delta, "divergence_class": _class(delta), "non_monotonic": non_monotonic}


def far_agent_world(w: dict[str, Any], base: str, condition: str) -> dict[str, Any] | None:
    far = FAR_AGENT[base]
    rows = [r for r in post_seed(w["events"].get(condition, [])) if r["sender"] == far]
    if not rows:
        return None
    mags = {int(r["cycle"]): abs(r["certainty_excess"]) for r in rows}
    cycles = sorted(mags)
    delta = round(mags[cycles[-1]] - mags[cycles[0]], 6)
    return {"far_agent": far, "magnitude_by_cycle": {str(k): round(mags[k], 6) for k in cycles},
            "last_minus_first": delta, "class": _class(delta),
            "mean_certainty_excess": _mean([r["certainty_excess"] for r in rows]),
            "signed_by_cycle": {str(int(r["cycle"])): r["certainty_excess"] for r in rows}}


def retention_table(s: dict[str, Any], base: str) -> dict[str, Any]:
    """R_m by position and cycle, over the worlds of a set (spec 8.1)."""
    out: dict[str, Any] = {}
    for condition in PAIRED_CONDITIONS:
        per: dict[str, dict[str, Any]] = {}
        for w in s["worlds"].values():
            for r in w["events"].get(condition, []):
                key = f"{r['sender']}@cycle{int(r['cycle'] or 0)}"
                slot = per.setdefault(key, {"sender": r["sender"], "cycle": int(r["cycle"] or 0), "messages": 0, "source_named": 0,
                                            "reliability_named": 0, "erosion_sum": 0})
                slot["messages"] += 1
                slot["source_named"] += int(bool(r["source_named"]))
                slot["reliability_named"] += int(bool(r["reliability_named"]))
                slot["erosion_sum"] += int(r["erosion"] or 0)
        for slot in per.values():
            n = slot["messages"]
            slot["R_source_named"] = round(slot["source_named"] / n, 6)
            slot["R_reliability_named"] = round(slot["reliability_named"] / n, 6)
            slot["mean_erosion"] = round(slot["erosion_sum"] / n, 6)
        out[condition] = dict(sorted(per.items(), key=lambda kv: (kv[1]["cycle"], kv[1]["sender"])))
    return out


def e1_for_arm(detached: dict[str, Any], twin: dict[str, Any], base: str) -> dict[str, Any]:
    relays = RELAY_AGENTS[base]
    if not relays:
        return {"verdict": "not assessable", "reason": "no relay position in this shape"}
    res: dict[str, Any] = {"by_condition": {}}
    verdicts = []
    for condition in PAIRED_CONDITIONS:
        def loss(s: dict[str, Any]) -> dict[str, Any]:
            rows = [r for w in s["worlds"].values() for r in post_seed(w["events"].get(condition, [])) if r["sender"] in relays]
            if not rows:
                return {}
            cycles = sorted({int(r["cycle"]) for r in rows})
            first = [r for r in rows if int(r["cycle"]) == cycles[0]]
            last = [r for r in rows if int(r["cycle"]) == cycles[-1]]
            out = {}
            for m in ("source_named", "reliability_named"):
                r_first = sum(1 for r in first if r[m]) / len(first)
                r_last = sum(1 for r in last if r[m]) / len(last)
                out[m] = {"R_first": round(r_first, 6), "R_last": round(r_last, 6), "loss": round(r_first - r_last, 6)}
            return out
        d, t = loss(detached), loss(twin)
        cell: dict[str, Any] = {"detached": d, "twin": t}
        marker_verdicts = []
        for m in ("source_named", "reliability_named"):
            if not d or not t or (d[m]["R_first"] == 0 and t[m]["R_first"] == 0):
                marker_verdicts.append("not assessable")
            else:
                marker_verdicts.append("consistent" if d[m]["loss"] > t[m]["loss"] else "contradicted")
        cell["marker_verdicts"] = dict(zip(("source_named", "reliability_named"), marker_verdicts))
        if "contradicted" in marker_verdicts:
            v = "contradicted"
        elif "not assessable" in marker_verdicts:
            v = "not assessable"
        else:
            v = "consistent"
        cell["verdict"] = v
        verdicts.append(v)
        res["by_condition"][condition] = cell
    res["verdict"] = ("contradicted" if "contradicted" in verdicts else "not assessable" if "not assessable" in verdicts else "consistent")
    return res


def e6_for_arm(detached: dict[str, Any], twin: dict[str, Any], base: str, probe: bool) -> dict[str, Any]:
    def origin_stats(s: dict[str, Any], condition: str) -> dict[str, Any]:
        firings = events = 0
        mags: list[float] = []
        worlds_with = 0
        consecutive_worlds = 0
        fis_at_events = 0
        for w in s["worlds"].values():
            rows = [r for r in post_seed(w["events"].get(condition, [])) if r["sender"] == "A"]
            flags = [r["certainty_excess"] is not None and r["certainty_excess"] > THRESHOLD for r in rows]
            firings += len(rows)
            n = sum(flags)
            events += n
            mags += [r["certainty_excess"] for r, f in zip(rows, flags) if f]
            worlds_with += int(n > 0)
            consecutive_worlds += int(any(a and b for a, b in zip(flags, flags[1:])))
            fis_at_events += sum(1 for r, f in zip(rows, flags) if f and (r["fis"] or 0) > 0)
        return {"firings": firings, "events": events, "rate": round(events / firings, 6) if firings else None,
                "mean_magnitude": _mean(mags), "max_magnitude": round(max(mags), 6) if mags else None,
                "worlds_with_event": worlds_with, "worlds_with_consecutive_events": consecutive_worlds,
                "fis_positive_at_events": fis_at_events if probe else None}
    d_lin = origin_stats(detached, "lineage")
    t_lin = origin_stats(twin, "lineage")
    d_free = origin_stats(detached, "free")
    verdict = "consistent" if d_lin["events"] == 0 else "contradicted"
    if d_lin["events"] == 0:
        tier = 1
    elif t_lin["rate"] is not None and d_lin["rate"] < t_lin["rate"]:
        tier = 2
    else:
        tier = 3
    return {"verdict": verdict, "frequency_tier": tier,
            "tier_meaning": {1: "no qualifying detached event", 2: "detached rate below the twin's", 3: "detached rate equal to or above the twin's"}[tier],
            "detached_lineage": d_lin, "twin_lineage": t_lin, "detached_free_baseline": d_free,
            "free_baseline_events_present": d_free["events"] > 0}


def drift_gauge(contemporary: dict[str, Any], historical: dict[str, Any]) -> dict[str, Any]:
    """Spec 9: the contemporary ring against the archived Gate 3A ring, same worlds."""
    positions: dict[str, Any] = {}
    for agent in ("A", "B", "C"):
        def deviations(s: dict[str, Any]) -> int:
            return sum(1 for w in s["worlds"].values() for r in post_seed(w["events"].get("lineage", []))
                       if r["sender"] == agent and r["kind"] != "at_reference")
        c, h = deviations(contemporary), deviations(historical)
        positions[agent] = {"contemporary": c, "historical": h, "difference": c - h, "within_tolerance": abs(c - h) <= GAUGE_COUNT_TOL}
    per_world: dict[str, list[dict[str, Any]]] = {}
    within: dict[str, int] = {}
    for condition in PAIRED_CONDITIONS:
        rows_out = []
        for seed, w in sorted(contemporary["worlds"].items()):
            h = historical["worlds"].get(seed)
            if not h:
                continue
            hid = by_id(h["events"].get(condition, []))
            diffs = [r["certainty_excess"] - hid[r["id"]]["certainty_excess"]
                     for r in post_seed(w["events"].get(condition, [])) if r["id"] in hid]
            m = _mean(diffs)
            rows_out.append({"seed": seed, "mean_paired_excess_difference": m, "within": m is not None and abs(m) <= GAUGE_WORLD_TOL})
        per_world[condition] = rows_out
        within[condition] = sum(1 for r in rows_out if r["within"])
    counts_ok = all(p["within_tolerance"] for p in positions.values())
    required = gauge_worlds_required(len(contemporary["worlds"]))
    worlds_ok = all(v >= required for v in within.values())
    return {"status": "PASS" if counts_ok and worlds_ok else "FAIL", "positions_lineage_deviation_counts": positions,
            "per_world": per_world, "worlds_within_tolerance": within,
            "tolerances": {"count": GAUGE_COUNT_TOL, "per_world_mean_excess": GAUGE_WORLD_TOL, "worlds_required": required,
                           "rule": "five sixths of paired worlds (10 of 12)"},
            "wording": "observed behavior differed across execution windows under the same nominal model configuration"
                       if not (counts_ok and worlds_ok) else "no difference beyond the declared operational tolerances",
            "contemporary_dates": sorted({(w["timestamp_utc"] or "")[:10] for w in contemporary["worlds"].values()}),
            "historical_dates": sorted({(w["timestamp_utc"] or "")[:10] for w in historical["worlds"].values()})}


def within_agent_trajectories(w: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for condition in PAIRED_CONDITIONS:
        per_agent: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for r in w["events"].get(condition, []):
            seq = per_agent[r["sender"]]
            prev = seq[-1]["certainty_excess"] if seq else None
            seq.append({"id": r["id"], "cycle": r["cycle"], "p_a": r["p_a"], "certainty_excess": r["certainty_excess"], "kind": r["kind"],
                        "reported_distinct_source_count": r["reported_distinct_source_count"], "fis": r["fis"],
                        "delta_within_agent": None if prev is None else round(r["certainty_excess"] - prev, 6),
                        "delta_archived_sequential": r["delta_without_new_evidence"]})
        out[condition] = dict(per_agent)
    return out


def origin_inbound_table(s: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for condition in PAIRED_CONDITIONS:
        buckets: dict[str, list[dict[str, Any]]] = {"inbound_named_sensor": [], "inbound_unnamed": []}
        for w in s["worlds"].values():
            rows = w["events"].get(condition, [])
            inbound = origin_inbound(rows)
            for r in rows:
                if r["sender"] == "A" and (r["cycle"] or 0) > 0:
                    named = any(i["source_named"] for i in inbound.get(r["id"], []))
                    buckets["inbound_named_sensor" if named else "inbound_unnamed"].append(r)
        out[condition] = {k: {"firings": len(v), "inflation": sum(1 for r in v if r["kind"] == "inflation"),
                              "discount": sum(1 for r in v if r["kind"] == "discount"),
                              "events_over_threshold": sum(1 for r in v if r["certainty_excess"] is not None and r["certainty_excess"] > THRESHOLD),
                              "fis_positive": sum(1 for r in v if (r["fis"] or 0) > 0),
                              "mean_certainty_excess": _mean([r["certainty_excess"] for r in v])} for k, v in buckets.items()}
    return out


def family_rows(s: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for seed, w in sorted(s["worlds"].items(), key=lambda kv: kv[1]["execution_order"]):
        for condition in CONDITIONS:
            ev = w["events"].get(condition)
            if not ev:
                continue
            last = ev[-1]
            rows.append({"set": s["set_id"], "seed": seed, "cell": w["cell"], "condition": condition, "final_answer": last["answer"],
                         "accuracy": last["accuracy"], "final_confidence": last["confidence"], "final_p_a": last["p_a"],
                         "final_kind": last["kind"], "final_brier": last["brier"], "max_depth": max(e["depth"] for e in ev),
                         "fis_positive_events": sum(1 for e in ev if (e["fis"] or 0) > 0),
                         "agent_as_source_events": sum(e["agent_as_source"] for e in ev), "events": len(ev)})
    return rows


def macro_rows(s: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for seed, w in sorted(s["worlds"].items(), key=lambda kv: kv[1]["execution_order"]):
        macro = w["events"].get("macro") or []
        if macro:
            rows.append({"set": s["set_id"], "seed": seed, "stop_event": macro[-1]["id"], "macro_events": len(macro),
                         "all_responses_reused": all(e["response_reused"] for e in macro[1:]) if len(macro) > 1 else None})
    return rows


# --------------------------------------------------------------------------------------
# Stage audit
# --------------------------------------------------------------------------------------

def audit_stage(plan_path: Path, stage: str, archive_root: Path, corpus_audit_file: Path,
                twins: dict[str, TwinRef] | None = None) -> dict[str, Any]:
    data = load_stage(plan_path, stage, archive_root, corpus_audit_file, twins)
    problems = list(data["problems"])
    arms: dict[str, Any] = {}
    manipulation: dict[str, Any] = {}
    seed_tables: dict[str, Any] = {}
    gauge: dict[str, Any] | None = None
    for set_id, s in data["sets"].items():
        base = s["base"]
        twin = data["twins"].get(set_id)
        entry: dict[str, Any] = {"topology": s["topology"], "base": base, "detached": s["detached"], "probe": s["probe"],
                                 "worlds": len(s["worlds"]), "twin": None}
        if twin is not None and not s["detached"] and base == "ring":
            gauge = drift_gauge(s, twin)
            entry["twin"] = {"set_id": twin["set_id"], "gate": twin["twin_gate"], "kind": twin["kind"], "role": "drift gauge"}
        if s["detached"]:
            if twin is None:
                problems.append(f"{set_id}: no twin configured")
                arms[set_id] = entry
                continue
            failures = manipulation_check(s, twin)
            manipulation[set_id] = {"status": "PASS" if not failures else "FAIL", "failures": failures}
            problems += [f"manipulation check: {f}" for f in failures]
            seed_tables[set_id] = seed_comparability(s, twin)
            dates_d = sorted({(w["timestamp_utc"] or "")[:10] for w in s["worlds"].values()})
            dates_t = sorted({(w["timestamp_utc"] or "")[:10] for w in twin["worlds"].values()})
            gaps = [_days_between(w["timestamp_utc"], twin["worlds"][seed]["timestamp_utc"]) for seed, w in s["worlds"].items() if seed in twin["worlds"]]
            entry["twin"] = {"set_id": twin["set_id"], "gate": twin["twin_gate"], "kind": twin["kind"],
                             "detached_dates": dates_d, "twin_dates": dates_t,
                             "gap_days_max": max((g for g in gaps if g is not None), default=None)}
            paired: dict[str, Any] = {}
            far: dict[str, Any] = {}
            for condition in PAIRED_CONDITIONS:
                pw = {str(seed): paired_world(w, twin["worlds"][seed], condition) for seed, w in s["worlds"].items() if seed in twin["worlds"]}
                fw = {str(seed): far_agent_world(w, base, condition) for seed, w in s["worlds"].items()}
                valid = [v for v in pw.values() if v]
                fvalid = [v for v in fw.values() if v]
                displacement_worlds = sum(1 for v in valid if v["material_displacement"])
                div_modal, div_tie = _modal([v["divergence_class"] for v in valid])
                far_modal, far_tie = _modal([v["class"] for v in fvalid])
                paired[condition] = {
                    "worlds": pw, "worlds_with_material_displacement": displacement_worlds, "worlds_paired": len(valid),
                    "majority_required": majority_of(len(valid)),
                    "E3a_verdict": "consistent" if valid and displacement_worlds >= majority_of(len(valid)) else "contradicted",
                    "divergence_modal_class": div_modal, "divergence_tie": div_tie,
                    "E3b_verdict": "consistent" if div_modal == "increasing" and not div_tie else "contradicted",
                    "non_monotonic_worlds": sum(1 for v in valid if v["non_monotonic"]),
                }
                far[condition] = {
                    "worlds": fw, "modal_class": far_modal, "tie": far_tie,
                    "E2_verdict": "consistent" if far_modal == "increasing" and not far_tie else "contradicted",
                    "far_stage_mean_excess": _mean([v["mean_certainty_excess"] for v in fvalid if v["mean_certainty_excess"] is not None]),
                    "far_stage_mean_last_minus_first": _mean([v["last_minus_first"] for v in fvalid]),
                    "far_agent": FAR_AGENT[base],
                }
            entry["paired"] = paired
            entry["far"] = far
            entry["E1"] = e1_for_arm(s, twin, base)
            entry["E2_verdict"] = "consistent" if all(far[c]["E2_verdict"] == "consistent" for c in PAIRED_CONDITIONS) else "contradicted"
            entry["E3a_verdict"] = "consistent" if all(paired[c]["E3a_verdict"] == "consistent" for c in PAIRED_CONDITIONS) else "contradicted"
            entry["E3b_verdict"] = "consistent" if all(paired[c]["E3b_verdict"] == "consistent" for c in PAIRED_CONDITIONS) else "contradicted"
            if base == "solo":
                tau = {c: sum(1 for w in s["worlds"].values() for r in post_seed(w["events"].get(c, [])) if r["kind"] != "at_reference") for c in PAIRED_CONDITIONS}
                over = {c: sum(1 for w in s["worlds"].values() for r in post_seed(w["events"].get(c, [])) if abs(r["certainty_excess"]) > THRESHOLD) for c in PAIRED_CONDITIONS}
                entry["E4"] = {"deviations_tau": tau, "deviations_over_threshold": over,
                               "verdict": "consistent" if all(v == 0 for v in tau.values()) else "contradicted"}
            if base in ORIGIN_RETURN_SHAPES:
                entry["E6"] = e6_for_arm(s, twin, base, s["probe"])
            # within-detached LINEAGE rates (E5 quantity), all post-seed firings, all agents
            lin = [r for w in s["worlds"].values() for r in post_seed(w["events"].get("lineage", []))]
            entry["lineage_rates"] = {"firings": len(lin),
                                      "discount_rate": round(sum(1 for r in lin if r["kind"] == "discount") / len(lin), 6) if lin else None,
                                      "inflation_rate": round(sum(1 for r in lin if r["kind"] == "inflation") / len(lin), 6) if lin else None}
            tlin = [r for w in twin["worlds"].values() for r in post_seed(w["events"].get("lineage", []))]
            entry["lineage_rates"]["twin_discount_rate"] = round(sum(1 for r in tlin if r["kind"] == "discount") / len(tlin), 6) if tlin else None
        entry["retention"] = retention_table(s, base)
        entry["origin_inbound"] = origin_inbound_table(s) if base != "solo" else {}
        entry["within_agent"] = {str(seed): within_agent_trajectories(w) for seed, w in s["worlds"].items()}
        arms[set_id] = entry

    # Stage-level expectations (E1..E6), per spec 7.
    detached_arms = {sid: e for sid, e in arms.items() if e["detached"]}
    def collect(key: str) -> dict[str, str]:
        return {sid: e[key] for sid, e in detached_arms.items() if key in e}
    e1 = {sid: e["E1"]["verdict"] for sid, e in detached_arms.items() if "E1" in e}
    e2 = collect("E2_verdict")
    e3a = collect("E3a_verdict")
    e3b = collect("E3b_verdict")
    e4 = {sid: e["E4"]["verdict"] for sid, e in detached_arms.items() if "E4" in e}
    e6 = {sid: e["E6"]["verdict"] for sid, e in detached_arms.items() if "E6" in e}
    ladder = {e["base"]: e["lineage_rates"]["discount_rate"] for e in detached_arms.values() if e["base"] in LADDER}
    ladder_ok = all(b in ladder and ladder[b] is not None for b in LADDER) and all(ladder[LADDER[i]] > ladder[LADDER[i + 1]] for i in range(len(LADDER) - 1))
    expectations = {
        "E1": {"by_arm": e1, "verdict": _combine(e1.values())},
        "E2": {"by_arm": e2, "verdict": _combine(e2.values())},
        "E3a": {"by_arm": e3a, "verdict": _combine(e3a.values())},
        "E3b": {"by_arm": e3b, "verdict": _combine(e3b.values())},
        "E4": {"by_arm": e4, "verdict": _combine(e4.values())},
        "E5": {"lineage_discount_rate_by_shape": ladder, "required_order": list(LADDER),
               "verdict": ("consistent" if ladder_ok else "contradicted") if len(ladder) == len(LADDER) else "not assessable"},
        "E6": {"by_arm": e6, "tiers": {sid: e["E6"]["frequency_tier"] for sid, e in detached_arms.items() if "E6" in e}, "verdict": _combine(e6.values())},
        "E7": {"verdict": "assessed in the synthesis across Set 001 and Set 002, not in a single-stage audit"},
    }
    manipulation_failed = any(m["status"] == "FAIL" for m in manipulation.values())
    status = "REFUSED: manipulation check failed" if manipulation_failed else ("COMPLETE" if not problems else "COMPLETE WITH PROBLEMS")
    report = {
        "experiment": "EXP-003", "gate": data["gate"], "stage": stage, "spec_version": SPEC_VERSION,
        "plan_version": data["plan"].get("plan_version"), "plan_status": data["plan"].get("status"), "plan_sha256": sha256_file(plan_path),
        "anchors": data["plan"]["anchors"], "corpus_audit": data["corpus_audit"], "twin_corpus_audits": data["twin_corpora"],
        "head_commit": git_output(["rev-parse", "HEAD"], PROJECT_ROOT), "archive_root": portable_path(archive_root),
        "tolerances": {"kind": TOLERANCE, "threshold": THRESHOLD, "flat_band": FLAT_BAND, "majority_of_12": MAJORITY,
                       "gauge": {"count": GAUGE_COUNT_TOL, "per_world_mean_excess": GAUGE_WORLD_TOL, "worlds_required": GAUGE_WORLDS}},
        "manipulation_check": manipulation, "seed_comparability": seed_tables, "arms": arms,
        "expectations": expectations if not manipulation_failed else {k: {"verdict": "refused"} for k in ("E1", "E2", "E3a", "E3b", "E4", "E5", "E6", "E7")},
        "drift_gauge": gauge,
        "family": [row for s in data["sets"].values() for row in family_rows(s)],
        "macro_boundary": [row for s in data["sets"].values() for row in macro_rows(s)],
        "problems": problems, "status": status,
        "boundary": ("Descriptive and pre-registered. Worlds are the unit; arms, stages, conditions and agents are reported separately. "
                     "Paired quantities carry their twin's execution dates and are never corrected for drift. E6 tiers are frequency "
                     "descriptions, not mechanism labels; nothing here bears on H2. Negative results stand."),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    return report


def _combine(verdicts) -> str:
    vs = list(verdicts)
    if not vs:
        return "not assessable"
    if "contradicted" in vs:
        return "contradicted"
    if "not assessable" in vs:
        return "not assessable"
    return "consistent"


# --------------------------------------------------------------------------------------
# Markdown
# --------------------------------------------------------------------------------------

def _f(x: Any) -> str:
    if x is None:
        return "n/a"
    return f"{x:+.3f}" if isinstance(x, float) else str(x)


def render_markdown(r: dict[str, Any]) -> str:
    L = [f"# EXP-003 Gate {r['gate']} {r['stage'].replace('_', ' ').title()} Primary-Outcome Audit v0.1", "", "## Status", "",
         f"**{r['status']}**", "", r["boundary"], "", "## Provenance", "",
         f"- Specification: `{r['spec_version']}`", f"- Plan: `{r['plan_version']}` (status `{r['plan_status']}`, sha256 `{r['plan_sha256']}`)",
         f"- Corpus audit: `{r['corpus_audit']['path']}` (status {r['corpus_audit']['status']}, sha256 `{r['corpus_audit']['sha256']}`)"]
    for sid, tc in r["twin_corpus_audits"].items():
        L.append(f"- Twin corpus audit for `{sid}`: `{tc['path']}` (sha256 `{tc['sha256']}`)")
    L += [f"- HEAD at audit time: `{r['head_commit']}`", f"- Tolerances: `{json.dumps(r['tolerances'])}`", "",
          "## Arms and twins", "", "| Set | Topology | Probe | Worlds | Twin | Twin kind | Twin dates | Max gap (days) |", "|---|---|---|---:|---|---|---|---:|"]
    for sid, e in r["arms"].items():
        t = e.get("twin") or {}
        L.append(f"| `{sid}` | {e['topology']} | {'on' if e['probe'] else 'off'} | {e['worlds']} | {t.get('set_id', 'none')} | {t.get('kind', t.get('role', ''))} | "
                 f"{', '.join(t.get('twin_dates', []))} | {t.get('gap_days_max', '')} |")
    L += ["", "## Integrity-level checks", "", "| Set | Manipulation check | Seed firing: identical p(A) / ≤.01 / ≤.05 / >.05 | Identical seed message |", "|---|---|---|---:|"]
    for sid, m in r["manipulation_check"].items():
        sc = r["seed_comparability"].get(sid, {})
        d = sc.get("distribution", {})
        ident = sum(1 for row in sc.get("rows", []) if row["message_identical"])
        L.append(f"| `{sid}` | {m['status']} ({len(m['failures'])} failures) | {d.get('zero', 0)} / {d.get('le_0.01', 0)} / {d.get('le_0.05', 0)} / {d.get('gt_0.05', 0)} | {ident}/{sc.get('worlds', 0)} |")
    L += ["", "The seed firing has an identical prompt in both executions and is sampled separately; its difference measures sampling variance, not detachment.", "",
          "## Pre-registered expectations (this stage)", "", "| Id | Verdict | By arm / quantities |", "|---|---|---|"]
    for key in ("E1", "E2", "E3a", "E3b", "E4", "E5", "E6", "E7"):
        e = r["expectations"][key]
        detail = {k: v for k, v in e.items() if k != "verdict"}
        L.append(f"| {key} | **{e['verdict']}** | `{json.dumps(detail, default=str)}` |")
    L += ["", "## Paired displacement and divergence by arm (E3a, E3b)", "",
          "| Set | Condition | Worlds with Ā > .01 | E3a | Divergence modal class | Tie | Non-monotonic worlds | E3b |", "|---|---|---:|---|---|---|---:|---|"]
    for sid, e in r["arms"].items():
        for c, p in (e.get("paired") or {}).items():
            L.append(f"| `{sid}` | {c} | {p['worlds_with_material_displacement']}/{p['worlds_paired']} | {p['E3a_verdict']} | {p['divergence_modal_class']} | {'yes' if p['divergence_tie'] else 'no'} | {p['non_monotonic_worlds']} | {p['E3b_verdict']} |")
    L += ["", "## Far-agent compounding by arm (E2) and within-detached LINEAGE rates (E5 quantity)", "",
          "| Set | Far agent | Condition | Modal class | E2 | Stage mean excess (far) | Mean last − first | LINEAGE discount rate | LINEAGE inflation rate | Twin discount rate |",
          "|---|---|---|---|---|---:|---:|---:|---:|---:|"]
    for sid, e in r["arms"].items():
        for c, f in (e.get("far") or {}).items():
            lr = e.get("lineage_rates", {})
            L.append(f"| `{sid}` | {f['far_agent']} | {c} | {f['modal_class']} | {f['E2_verdict']} | {_f(f['far_stage_mean_excess'])} | {_f(f['far_stage_mean_last_minus_first'])} | "
                     f"{_f(lr.get('discount_rate'))} | {_f(lr.get('inflation_rate'))} | {_f(lr.get('twin_discount_rate'))} |")
    L += ["", "## Origin after lineage return (E6, strict H1) with descriptive frequency tiers", "",
          "| Set | Verdict | Tier | Detached LINEAGE events / firings | Mean, max magnitude | Worlds with event | Consecutive | Twin LINEAGE events / firings | Detached FREE events | FIS>0 at events |",
          "|---|---|---|---|---|---:|---:|---|---:|---|"]
    for sid, e in r["arms"].items():
        if "E6" in e:
            x = e["E6"]; d, t, fr = x["detached_lineage"], x["twin_lineage"], x["detached_free_baseline"]
            L.append(f"| `{sid}` | **{x['verdict']}** | {x['frequency_tier']} ({x['tier_meaning']}) | {d['events']} / {d['firings']} | {_f(d['mean_magnitude'])}, {_f(d['max_magnitude'])} | "
                     f"{d['worlds_with_event']} | {d['worlds_with_consecutive_events']} | {t['events']} / {t['firings']} | {fr['events']} | {d['fis_positive_at_events'] if d['fis_positive_at_events'] is not None else 'not probed'} |")
    L += ["", "## Relay-position marker loss (E1)", "", "| Set | Condition | Marker | Detached R first → last (loss) | Twin R first → last (loss) | Marker verdict |", "|---|---|---|---|---|---|"]
    for sid, e in r["arms"].items():
        e1 = e.get("E1") or {}
        for c, cell in (e1.get("by_condition") or {}).items():
            for m in ("source_named", "reliability_named"):
                d, t = cell["detached"].get(m), cell["twin"].get(m)
                if d and t:
                    L.append(f"| `{sid}` | {c} | {m} | {d['R_first']:.3f} → {d['R_last']:.3f} ({d['loss']:+.3f}) | {t['R_first']:.3f} → {t['R_last']:.3f} ({t['loss']:+.3f}) | {cell['marker_verdicts'][m]} |")
    if r.get("drift_gauge"):
        g = r["drift_gauge"]
        L += ["", f"## Drift gauge: contemporary ring vs archived Gate 3A ring, same worlds: **{g['status']}**", "",
              f"Contemporary dates {g['contemporary_dates']}; historical dates {g['historical_dates']}. {g['wording'].capitalize()}.", "",
              "| Position | Contemporary LINEAGE deviations | Historical | Difference | Within 4 |", "|---|---:|---:|---:|---|"]
        for agent, p in g["positions_lineage_deviation_counts"].items():
            L.append(f"| {agent} | {p['contemporary']} | {p['historical']} | {p['difference']:+d} | {'yes' if p['within_tolerance'] else 'no'} |")
        L.append("")
        L.append("Worlds with paired mean excess within .02: " + ", ".join(f"{c} {n}/{len(g['per_world'][c])}" for c, n in g["worlds_within_tolerance"].items()))
    L += ["", "## Secondary: origin firings by whether the inbound message named the sensor (descriptive, no verdict)", "",
          "| Set | Condition | Inbound | Firings | Inflation | Discount | Events > .01 | FIS>0 | Mean excess |", "|---|---|---|---:|---:|---:|---:|---:|---:|"]
    for sid, e in r["arms"].items():
        for c, tab in (e.get("origin_inbound") or {}).items():
            for k, v in tab.items():
                L.append(f"| `{sid}` | {c} | {k} | {v['firings']} | {v['inflation']} | {v['discount']} | {v['events_over_threshold']} | {v['fis_positive']} | {_f(v['mean_certainty_excess'])} |")
    L += ["", "## MACRO stopping boundary", "", "| Set | Seed | Stop event | MACRO events | Responses reused |", "|---|---:|---|---:|---|"]
    for row in r["macro_boundary"]:
        L.append(f"| `{row['set']}` | {row['seed']} | {row['stop_event']} | {row['macro_events']} | {row['all_responses_reused']} |")
    L += ["", "## Problems", ""] + ([f"- {p}" for p in r["problems"]] or ["None."]) + ["", "## Boundary", "", r["boundary"], ""]
    L.append("Within-agent trajectories, per-world paired sequences and retention by depth are in the JSON record under `arms.<set>.within_agent`, `arms.<set>.paired.<condition>.worlds` and `arms.<set>.retention`.")
    return "\n".join(L)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=EXP003 / "GATE_3C_PLAN_v0.1.json")
    parser.add_argument("--stage", required=True)
    parser.add_argument("--archive-root", type=Path, default=None)
    parser.add_argument("--corpus-audit", type=Path, default=None)
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()
    plan = load_plan(args.plan)
    gate = plan["gate"]
    archive_root = args.archive_root or DEFAULT_ARCHIVE_ROOT
    out_dir = args.out_dir or (AUDITS / f"gate_{gate.lower()}")
    corpus_file = args.corpus_audit or corpus_audit_path(gate, args.stage, args.out_dir)
    report = audit_stage(args.plan, args.stage, archive_root, corpus_file)   # refuses before anything is written
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path, md_path = output_paths(out_dir / f"EXP_003_GATE_{gate.upper()}_{args.stage.upper()}_PRIMARY_OUTCOME_AUDIT_v0.1")
    json_path.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    verdicts = ", ".join(f"{k}={report['expectations'][k]['verdict']}" for k in ("E1", "E2", "E3a", "E3b", "E4", "E5", "E6"))
    gauge = f"; drift gauge {report['drift_gauge']['status']}" if report.get("drift_gauge") else ""
    print(f"{report['status']}: {sum(e['worlds'] for e in report['arms'].values())} worlds; {verdicts}{gauge}")
    print(f"wrote {json_path} and {md_path}")
    if report["problems"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
