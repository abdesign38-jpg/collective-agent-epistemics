from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from statistics import mean

from src.models import Evidence, AgentState
from src.synthetic_agent import SyntheticAgent
from src.lineage_tracker import MacroLineageTracker
from src.math_utils import brier

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"

def load_worlds():
    return json.loads((HERE / "synthetic_worlds.json").read_text(encoding="utf-8"))

def make_agents(world):
    agents = {}
    for name, evs in world["agents"].items():
        evidence = [Evidence(**e) for e in evs]
        agents[name] = SyntheticAgent(AgentState(name=name, evidence=evidence))
    return agents

def event_from_claim(world, condition, round_no, sender, receiver, claim, macro_new_roots=None):
    actual = set(claim.actual_roots)
    perceived = set(claim.perceived_roots)
    false_support = len(perceived - actual)
    p_a = claim.confidence if claim.supports_state == "A" else 1.0 - claim.confidence
    return {
        "trial_id": world["world_id"],
        "condition": condition,
        "round": round_no,
        "sender": sender,
        "receiver": receiver,
        "claim_id": claim.claim_id,
        "claim": f"State {claim.supports_state} is favored.",
        "confidence": round(claim.confidence, 6),
        "actual_roots": sorted(actual),
        "perceived_roots": sorted(perceived),
        "independent_root_count": len(actual),
        "perceived_root_count": len(perceived),
        "false_independent_support": false_support,
        "inference_depth": claim.inference_depth,
        "new_independent_roots": 0 if macro_new_roots is None else macro_new_roots,
        "brier_score": round(brier(p_a, world["truth"]), 6),
    }

def run_condition(world, condition, rounds):
    agents = make_agents(world)
    tracker = MacroLineageTracker()
    events = []
    last_claim = None
    completed_cycles = 0

    # Seed: Agent A produces the first claim from its own external evidence.
    claim_counter = 0
    claim_counter += 1
    seed = agents["A"].make_claim(condition, f"{condition}_C{claim_counter}")
    if condition == "macro":
        new_count = tracker.observe_claim(set(seed.actual_roots))
    else:
        new_count = len(seed.actual_roots)
    events.append(event_from_claim(world, condition, 0, "A", "B", seed, new_count))
    agents["B"].receive(seed)
    last_claim = seed

    sequence = [("B","C"), ("C","A"), ("A","B")]

    for cycle in range(1, rounds + 1):
        if condition == "macro":
            tracker.start_cycle()

        for sender, receiver in sequence:
            claim_counter += 1
            claim = agents[sender].make_claim(
                condition,
                f"{condition}_C{claim_counter}",
                derived_from=last_claim.claim_id if last_claim else None,
            )
            new_count = None
            if condition == "macro":
                new_count = tracker.observe_claim(set(claim.actual_roots))
            else:
                # Count roots new to the *network history* approximately from prior events.
                seen = set()
                for e in events:
                    seen.update(e["actual_roots"])
                new_count = len(set(claim.actual_roots) - seen)

            events.append(event_from_claim(world, condition, cycle, sender, receiver, claim, new_count))
            agents[receiver].receive(claim)
            last_claim = claim

        completed_cycles += 1

        if condition == "macro" and tracker.should_stop_after_cycle():
            break

    final = events[-1]
    correct = (final["claim"].startswith(f"State {world['truth']}"))
    summary = {
        "world_id": world["world_id"],
        "condition": condition,
        "truth": world["truth"],
        "completed_cycles": completed_cycles,
        "final_claim": final["claim"],
        "final_confidence": final["confidence"],
        "final_brier_score": final["brier_score"],
        "final_independent_roots": final["independent_root_count"],
        "final_perceived_roots": final["perceived_root_count"],
        "final_false_independent_support": final["false_independent_support"],
        "final_inference_depth": final["inference_depth"],
        "accuracy": 1 if correct else 0,
        "event_count": len(events),
    }
    return events, summary

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--world", default="all", help="all or a world_id")
    parser.add_argument("--rounds", type=int, default=4)
    args = parser.parse_args()

    RESULTS.mkdir(parents=True, exist_ok=True)
    worlds = load_worlds()
    if args.world != "all":
        worlds = [w for w in worlds if w["world_id"] == args.world]
        if not worlds:
            raise SystemExit(f"Unknown world: {args.world}")

    all_events = []
    summaries = []
    for world in worlds:
        for condition in ("free", "lineage", "macro"):
            events, summary = run_condition(world, condition, args.rounds)
            all_events.extend(events)
            summaries.append(summary)

    with (RESULTS / "events.jsonl").open("w", encoding="utf-8") as f:
        for e in all_events:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    fields = list(summaries[0].keys())
    with (RESULTS / "summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summaries)

    metadata = {
        "experiment": "EXP-001",
        "rounds_requested": args.rounds,
        "worlds": [w["world_id"] for w in worlds],
        "conditions": ["free","lineage","macro"],
        "note": "Synthetic harness validation only; not evidence about real LLM behavior."
    }
    (RESULTS / "run_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    print("\nEXP-001 complete\n")
    print(
        f"{'WORLD':28} {'COND':9} {'TRUTH':>5} {'FINAL':>7} "
        f"{'ACC':>4} {'CYCLES':>6} {'CONF':>8} {'ROOTS':>6} "
        f"{'FALSE+':>7} {'DEPTH':>6} {'BRIER':>8}"
    )
    print("-" * 88)
    for s in summaries:
        final_state = s["final_claim"].split()[1]

        print(
            f"{s['world_id']:28} {s['condition']:9} "
            f"{s['truth']:>5} {final_state:>7} "
            f"{s['accuracy']:4d} {s['completed_cycles']:6d} "
            f"{s['final_confidence']:8.3f} "
            f"{s['final_independent_roots']:6d} "
            f"{s['final_false_independent_support']:7d} "
            f"{s['final_inference_depth']:6d} "
            f"{s['final_brier_score']:8.3f}"
        )
    print(f"\nResults: {RESULTS}")

if __name__ == "__main__":
    main()
