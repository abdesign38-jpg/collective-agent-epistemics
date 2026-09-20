from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .adapters.base import AgentAdapter
from .adapters.deterministic_stub import DeterministicStubAdapter
from .lineage import LineageGraph
from .metrics import event_metrics
from .models import (
    AgentMessage,
    AgentObservation,
    AgentResponse,
    TrialEvent,
    World,
)
from .world_generator import WorldGenerator

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
CONDITIONS = ("free", "lineage", "macro")
SEED_EDGE = ("A", "B")
RECURSIVE_SEQUENCE = (("B", "C"), ("C", "A"), ("A", "B"))


@dataclass(frozen=True)
class ConditionRun:
    world: World
    condition: str
    events: tuple[TrialEvent, ...]
    summary: dict[str, object]


@dataclass(frozen=True)
class ExperimentRun:
    worlds: tuple[World, ...]
    condition_runs: tuple[ConditionRun, ...]
    adapter_name: str = "deterministic_stub"
    adapter_metadata: dict[str, object] = field(default_factory=dict)
    rounds: int = 0
    seed: int = 0


def run_condition(
    world: World,
    condition: str,
    rounds: int,
    adapter: AgentAdapter | None = None,
    trial_id: str | None = None,
) -> ConditionRun:
    if condition not in CONDITIONS:
        raise ValueError(f"unknown condition: {condition}")
    if rounds < 0:
        raise ValueError("rounds must be non-negative")

    adapter = adapter or DeterministicStubAdapter()
    graph = LineageGraph()
    events: list[TrialEvent] = []
    received_message: AgentMessage | None = None
    previous_response: AgentResponse | None = None
    message_number = 0
    completed_cycles = 0
    run_id = trial_id or world.world_id

    for cycle in range(0, rounds + 1):
        if cycle > 0 and condition == "macro":
            graph.start_cycle()

        steps = (SEED_EDGE,) if cycle == 0 else RECURSIVE_SEQUENCE
        for sender, receiver in steps:
            message_number += 1
            observation = AgentObservation(
                agent_id=sender,
                evidence=tuple(e for e in world.evidence if e.assigned_to == sender),
            )
            if received_message is not None and received_message.receiver != sender:
                raise RuntimeError(
                    f"message {received_message.message_id} addressed to "
                    f"{received_message.receiver}, not {sender}"
                )
            response = adapter.respond(sender, observation, received_message, condition)
            message_id = f"{run_id}_{condition}_M{message_number:02d}"
            parent_id = received_message.message_id if received_message else None
            external_roots = {e.evidence_id for e in observation.evidence}
            actual_lineage = graph.record_message(message_id, parent_id, external_roots)
            visible_envelope = actual_lineage if condition in ("lineage", "macro") else None
            message = AgentMessage(
                message_id=message_id,
                sender=sender,
                receiver=receiver,
                content=response.message,
                envelope=visible_envelope,
            )
            new_root_count = len(graph.last_new_roots)
            metrics = event_metrics(
                response=response,
                truth=world.truth,
                envelope=actual_lineage,
                new_independent_evidence=new_root_count,
                previous_response=previous_response,
            )
            events.append(
                TrialEvent(
                    trial_id=run_id,
                    condition=condition,
                    cycle=cycle,
                    sender=sender,
                    receiver=receiver,
                    message_id=message_id,
                    model_output=response,
                    agent_message=message,
                    actual_lineage=actual_lineage,
                    agent_reported_information=response.message,
                    metrics=metrics,
                )
            )
            received_message = message
            previous_response = response

        if cycle > 0:
            completed_cycles += 1
            if condition == "macro" and graph.should_stop_after_cycle():
                break

    stop_reason = "max_rounds"
    if condition == "macro" and completed_cycles < rounds:
        stop_reason = "no_new_independent_roots_after_cycle"
    final_event = events[-1]
    summary = {
        "world_id": world.world_id,
        "condition": condition,
        "truth": world.truth,
        "final": final_event.model_output.answer,
        "accuracy": final_event.metrics["accuracy"],
        "final_confidence": final_event.model_output.confidence,
        "final_brier_score": final_event.metrics["brier_score"],
        "final_p_a": final_event.metrics["p_a"],
        "completed_cycles": completed_cycles,
        "independent_evidence_root_count": graph.independent_root_count,
        "max_inference_depth": max(e.actual_lineage.inference_depth for e in events),
        "new_independent_evidence_count": sum(
            int(e.metrics["new_independent_evidence"]) for e in events
        ),
        "reported_confidence_trajectory": [e.metrics["reported_confidence"] for e in events],
        "p_a_trajectory": [e.metrics["p_a"] for e in events],
        "p_a_delta_without_new_evidence": [
            e.metrics["p_a_delta_without_new_evidence"] for e in events
        ],
        "stop_reason": stop_reason,
    }
    return ConditionRun(world, condition, tuple(events), summary)


def run_experiment(
    trials: int,
    rounds: int,
    seed: int,
    adapter_factory: Callable[[], AgentAdapter] | None = None,
    adapter_name: str = "deterministic_stub",
    adapter_metadata: dict[str, object] | None = None,
) -> ExperimentRun:
    if trials < 1:
        raise ValueError("trials must be at least 1")
    factory = adapter_factory or DeterministicStubAdapter
    worlds = tuple(WorldGenerator(seed).generate_many(trials))
    condition_runs: list[ConditionRun] = []
    for world in worlds:
        for condition in CONDITIONS:
            condition_runs.append(
                run_condition(
                    world=world,
                    condition=condition,
                    rounds=rounds,
                    adapter=factory(),
                    trial_id=world.world_id,
                )
            )
    return ExperimentRun(
        worlds,
        tuple(condition_runs),
        adapter_name=adapter_name,
        adapter_metadata=adapter_metadata or {},
        rounds=rounds,
        seed=seed,
    )


def write_results(experiment: ExperimentRun) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    with (RESULTS / "events.jsonl").open("w", encoding="utf-8") as output:
        for condition_run in experiment.condition_runs:
            for event in condition_run.events:
                output.write(json.dumps(event.to_record(), sort_keys=True) + "\n")

    summaries = [condition_run.summary for condition_run in experiment.condition_runs]
    fields = [
        "world_id",
        "condition",
        "truth",
        "final",
        "accuracy",
        "final_confidence",
        "final_brier_score",
        "completed_cycles",
        "independent_evidence_root_count",
        "max_inference_depth",
        "new_independent_evidence_count",
        "final_p_a",
        "reported_confidence_trajectory",
        "p_a_trajectory",
        "p_a_delta_without_new_evidence",
        "stop_reason",
    ]
    with (RESULTS / "summary.csv").open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for summary in summaries:
            writer.writerow({field: summary[field] for field in fields})

    metadata = {
        "experiment": "EXP-002",
        "world_count": len(experiment.worlds),
        "adapter_name": experiment.adapter_name,
        "trial_count": len(experiment.worlds),
        "rounds": experiment.rounds,
        "seed": experiment.seed,
        "conditions": list(CONDITIONS),
        "topology": [list(SEED_EDGE), *[list(edge) for edge in RECURSIVE_SEQUENCE]],
        "note": "Infrastructure validation only; not evidence for the research hypothesis.",
    }
    metadata.update(experiment.adapter_metadata)
    (RESULTS / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )


def print_results(experiment: ExperimentRun) -> None:
    print("\nEXP-002 deterministic smoke test\n")
    print(
        f"{'WORLD':24} {'CONDITION':10} {'TRUTH':>5} {'FINAL':>5} "
        f"{'ACCURACY':>8} {'CONFIDENCE':>10} {'CYCLES':>6} "
        f"{'ROOTS':>5} {'DEPTH':>5} {'BRIER':>8} {'STOP_REASON':>38}"
    )
    print("-" * 139)
    for condition_run in experiment.condition_runs:
        summary = condition_run.summary
        print(
            f"{summary['world_id']:24} {summary['condition']:10} "
            f"{summary['truth']:>5} {summary['final']:>5} "
            f"{summary['accuracy']:8d} {summary['final_confidence']:10.3f} "
            f"{summary['completed_cycles']:6d} "
            f"{summary['independent_evidence_root_count']:5d} "
            f"{summary['max_inference_depth']:5d} "
            f"{summary['final_brier_score']:8.3f} "
            f"{summary['stop_reason']:>38}"
        )
    print(f"\nResults: {RESULTS}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the EXP-002 infrastructure scaffold")
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--rounds", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--adapter", choices=("deterministic_stub",), default="deterministic_stub")
    args = parser.parse_args()

    experiment = run_experiment(
        args.trials,
        args.rounds,
        args.seed,
        adapter_name=args.adapter,
    )
    write_results(experiment)
    print_results(experiment)


if __name__ == "__main__":
    main()
