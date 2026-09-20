from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Literal

from .adapters.base import AgentAdapter
from .adapters.deterministic_stub import DeterministicStubAdapter
from .adapters.openai_responses import OpenAIAdapterConfig, OpenAIResponsesAdapter
from .dry_run import build_dry_run_inputs, print_dry_run, print_dry_run_configuration
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
from .adapters.openai_responses import SCHEMA_VERSION
from .prompting import PROMPT_VERSION
from .prompting import render_agent_input

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
CONDITIONS = ("free", "lineage", "macro")
SEED_EDGE = ("A", "B")
RECURSIVE_SEQUENCE = (("B", "C"), ("C", "A"), ("A", "B"))
ExecutionPolicy = Literal["paired", "independent"]


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
    run_class: str = "infrastructure"
    execution_policy: ExecutionPolicy = "paired"
    execution_metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class SeedResponse:
    response: AgentResponse
    provider_metadata: dict[str, object] | None


def run_condition(
    world: World,
    condition: str,
    rounds: int,
    adapter: AgentAdapter | None = None,
    trial_id: str | None = None,
    seed: SeedResponse | None = None,
    reused_events: dict[int, TrialEvent] | None = None,
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
            visible_message_id = f"M{message_number:02d}"
            model_visible_input = render_agent_input(sender, observation, received_message)
            reused = reused_events.get(message_number) if reused_events else None
            if cycle == 0 and seed is not None:
                response = seed.response
                provider_metadata = dict(seed.provider_metadata) if seed.provider_metadata else None
                response_reused = True
                source_condition = "seed"
            elif reused is not None:
                if reused.model_visible_input != model_visible_input:
                    raise RuntimeError("paired reuse prompt mismatch")
                response = reused.model_output
                provider_metadata = dict(reused.provider_metadata) if reused.provider_metadata else None
                response_reused = True
                source_condition = "lineage"
            else:
                response = adapter.respond(sender, observation, received_message, condition)
                provider_metadata = (
                    dict(getattr(adapter, "last_call_metadata"))
                    if getattr(adapter, "last_call_metadata", None)
                    else None
                )
                response_reused = False
                source_condition = None
            message_id = f"{run_id}_{condition}_M{message_number:02d}"
            parent_id = received_message.message_id if received_message else None
            visible_parent_id = received_message.visible_message_id if received_message else None
            external_roots = {e.evidence_id for e in observation.evidence}
            actual_lineage = graph.record_message(
                message_id,
                parent_id,
                external_roots,
                visible_message_id=visible_message_id,
                visible_parent_message_id=visible_parent_id,
            )
            visible_envelope = actual_lineage if condition in ("lineage", "macro") else None
            message = AgentMessage(
                message_id=message_id,
                sender=sender,
                receiver=receiver,
                content=response.message,
                envelope=visible_envelope,
                visible_message_id=visible_message_id,
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
                    visible_message_id=visible_message_id,
                    model_output=response,
                    agent_message=message,
                    actual_lineage=actual_lineage,
                    agent_reported_information=response.message,
                    metrics=metrics,
                    provider_metadata=provider_metadata,
                    response_reused=response_reused,
                    source_condition=source_condition,
                    model_visible_input=model_visible_input,
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
    run_class: str = "infrastructure",
    execution_policy: ExecutionPolicy = "paired",
) -> ExperimentRun:
    if trials < 1:
        raise ValueError("trials must be at least 1")
    if execution_policy not in ("paired", "independent"):
        raise ValueError("execution_policy must be paired or independent")
    factory = adapter_factory or DeterministicStubAdapter
    worlds = tuple(WorldGenerator(seed).generate_many(trials))
    condition_runs: list[ConditionRun] = []
    actual_model_call_count = 0
    reused_response_count = 0
    for world in worlds:
        if execution_policy == "independent":
            for condition in CONDITIONS:
                condition_run = run_condition(
                    world=world,
                    condition=condition,
                    rounds=rounds,
                    adapter=factory(),
                    trial_id=world.world_id,
                )
                actual_model_call_count += len(condition_run.events)
                condition_runs.append(condition_run)
            continue

        seed_adapter = factory()
        seed_observation = AgentObservation(
            agent_id="A",
            evidence=tuple(e for e in world.evidence if e.assigned_to == "A"),
        )
        seed_response = seed_adapter.respond("A", seed_observation, None, "seed")
        seed_metadata = (
            dict(getattr(seed_adapter, "last_call_metadata"))
            if getattr(seed_adapter, "last_call_metadata", None)
            else None
        )
        shared_seed = SeedResponse(seed_response, seed_metadata)
        actual_model_call_count += 1

        free_run = run_condition(
            world, "free", rounds, adapter=factory(), trial_id=world.world_id, seed=shared_seed
        )
        actual_model_call_count += len(free_run.events) - 1
        lineage_run = run_condition(
            world, "lineage", rounds, adapter=factory(), trial_id=world.world_id, seed=shared_seed
        )
        actual_model_call_count += len(lineage_run.events) - 1
        lineage_events = {index + 1: event for index, event in enumerate(lineage_run.events)}
        macro_run = run_condition(
            world,
            "macro",
            rounds,
            adapter=factory(),
            trial_id=world.world_id,
            seed=shared_seed,
            reused_events=lineage_events,
        )
        reused_response_count += len(macro_run.events)
        condition_runs.extend((free_run, lineage_run, macro_run))
    actual_input_tokens = 0
    actual_output_tokens = 0
    actual_total_tokens = 0
    seen_response_ids: set[str] = set()
    for condition_run in condition_runs:
        for event in condition_run.events:
            if event.provider_metadata is None:
                continue
            response_id = event.provider_metadata.get("response_id")
            if response_id and response_id in seen_response_ids:
                continue
            if response_id:
                seen_response_ids.add(response_id)
            usage = event.provider_metadata.get("usage", {})
            actual_input_tokens += int(usage.get("input_tokens") or 0)
            actual_output_tokens += int(usage.get("output_tokens") or 0)
            actual_total_tokens += int(usage.get("total_tokens") or 0)

    return ExperimentRun(
        worlds,
        tuple(condition_runs),
        adapter_name=adapter_name,
        adapter_metadata=adapter_metadata or {},
        rounds=rounds,
        seed=seed,
        run_class=run_class,
        execution_policy=execution_policy,
        execution_metadata={
            "actual_model_call_count": actual_model_call_count,
            "reused_response_count": reused_response_count,
            "input_tokens_actual": actual_input_tokens,
            "output_tokens_actual": actual_output_tokens,
            "total_tokens_actual": actual_total_tokens,
        },
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
        "run_class": experiment.run_class,
        "execution_policy": experiment.execution_policy,
        "world_count": len(experiment.worlds),
        "adapter_name": experiment.adapter_name,
        "provider": experiment.adapter_metadata.get("provider", "local"),
        "requested_model": experiment.adapter_metadata.get("requested_model"),
        "reasoning_effort": experiment.adapter_metadata.get("reasoning_effort"),
        "sdk_version": experiment.adapter_metadata.get("sdk_version"),
        "timeout_seconds": experiment.adapter_metadata.get("timeout_seconds"),
        "store": False,
        "max_retries": 0,
        "prompt_version": experiment.adapter_metadata.get("prompt_version", PROMPT_VERSION),
        "schema_version": experiment.adapter_metadata.get("schema_version", SCHEMA_VERSION),
        "python_version": platform.python_version(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "trial_count": len(experiment.worlds),
        "rounds": experiment.rounds,
        "seed": experiment.seed,
        "conditions": list(CONDITIONS),
        "topology": [list(SEED_EDGE), *[list(edge) for edge in RECURSIVE_SEQUENCE]],
        "adapter_metadata": experiment.adapter_metadata,
        "execution_metadata": experiment.execution_metadata,
        "note": (
            "Exploratory real-model pilot. Not confirmatory evidence."
            if experiment.run_class == "pilot_real_model"
            else "Infrastructure validation only."
        ),
    }
    fingerprint_input = {
        key: metadata[key]
        for key in (
            "experiment", "run_class", "provider", "requested_model", "reasoning_effort",
            "sdk_version", "python_version", "timeout_seconds", "store", "max_retries",
            "conditions", "topology", "rounds", "seed", "trial_count", "execution_policy", "prompt_version",
            "schema_version",
        )
    }
    metadata["config_fingerprint"] = hashlib.sha256(
        json.dumps(fingerprint_input, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    (RESULTS / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )


def print_results(experiment: ExperimentRun) -> None:
    print(
        f"\nEXP-002 run\nAdapter: {experiment.adapter_name}"
        f"\nExecution policy: {experiment.execution_policy}"
    )
    model = experiment.adapter_metadata.get("requested_model")
    if model:
        print(f"Model: {model}")
    print()
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
    parser.add_argument("--adapter", choices=("deterministic_stub", "openai"), default="deterministic_stub")
    parser.add_argument("--model", default=None)
    parser.add_argument("--reasoning-effort", default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--execution-policy", choices=("paired", "independent"), default=None)
    args = parser.parse_args()

    if args.adapter == "openai":
        config = OpenAIAdapterConfig.from_environment(
            model=args.model,
            reasoning_effort=args.reasoning_effort,
        )
        if args.dry_run:
            world = WorldGenerator(args.seed).generate_many(args.trials)[0]
            if args.execution_policy is None:
                raise SystemExit("OpenAI runs require --execution-policy paired or independent")
            dry_config = {**config.metadata(), "execution_policy": args.execution_policy}
            print_dry_run_configuration(dry_config)
            print_dry_run(build_dry_run_inputs(world, args.execution_policy), args.execution_policy)
            return
        if not args.live:
            raise SystemExit("OpenAI adapter requires --live or --dry-run; no network call made")
        if args.execution_policy is None:
            raise SystemExit("OpenAI runs require --execution-policy paired or independent")
        factory = lambda: OpenAIResponsesAdapter(config)
        experiment = run_experiment(
            args.trials,
            args.rounds,
            args.seed,
            adapter_factory=factory,
            adapter_name="openai",
            adapter_metadata=config.metadata(),
            run_class="pilot_real_model",
            execution_policy=args.execution_policy,
        )
    else:
        if args.live:
            raise SystemExit("--live is only valid with --adapter openai")
        experiment = run_experiment(
            args.trials,
            args.rounds,
            args.seed,
            adapter_name="deterministic_stub",
            adapter_metadata={"provider": "local"},
            run_class="infrastructure",
            execution_policy=args.execution_policy or "paired",
        )
    write_results(experiment)
    print_results(experiment)


if __name__ == "__main__":
    main()
