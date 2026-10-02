from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Literal

from .adapters.base import AgentAdapter
from .adapters.deterministic_stub import DeterministicStubAdapter
from .adapters.openai_responses import SCHEMA_VERSION
from .adapters.registry import PROVIDERS, RUN_CLASS_SMOKE, build_provider
from .lineage import LineageGraph
from .metrics import event_metrics
from .models import AgentMessage, AgentObservation, AgentResponse, TrialEvent, World
from .prompting import PROMPT_VERSION, render_agent_input
from .provenance import provenance_record
from .topology import Topology, get_topology
from .world_generator import WorldGenerator, alignment, world_cell

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
CONDITIONS = ("free", "lineage", "macro")
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
    topology: Topology
    root_mode: str
    adapter_name: str = "deterministic_stub"
    adapter_metadata: dict[str, object] = field(default_factory=dict)
    rounds: int = 0
    seed: int = 0
    run_class: str = "infrastructure"
    execution_policy: ExecutionPolicy = "paired"
    probe: bool = True
    sensor_reliability: float = 0.70
    execution_metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class SeedResponse:
    response: AgentResponse
    provider_metadata: dict[str, object] | None


def _provider_metadata(adapter: AgentAdapter) -> dict[str, object] | None:
    metadata = getattr(adapter, "last_call_metadata", None)
    return dict(metadata) if metadata else None


def run_condition(
    world: World,
    condition: str,
    rounds: int,
    topology: Topology | None = None,
    adapter: AgentAdapter | None = None,
    trial_id: str | None = None,
    seed: dict[int, SeedResponse] | None = None,
    reused_events: dict[int, TrialEvent] | None = None,
    probe: bool = True,
) -> ConditionRun:
    if condition not in CONDITIONS:
        raise ValueError(f"unknown condition: {condition}")
    if rounds < 0:
        raise ValueError("rounds must be non-negative")

    topology = topology or get_topology(world.topology)
    adapter = adapter or DeterministicStubAdapter()
    graph = LineageGraph()
    evidence_by_id = world.evidence_by_id()
    events: list[TrialEvent] = []
    inbox: dict[str, list[AgentMessage]] = defaultdict(list)
    marks_by_message: dict[str, dict[str, Any]] = {}
    fired: set[str] = set()
    previous_response: AgentResponse | None = None
    firing_number = 0
    completed_cycles = 0
    macro_stop_triggered = False
    run_id = trial_id or world.world_id

    for cycle in range(0, rounds + 1):
        if cycle > 0 and condition == "macro":
            graph.start_cycle()

        firings = topology.seed_cycle if cycle == 0 else topology.recursive_cycle
        for firing in firings:
            firing_number += 1
            sender = firing.sender
            show_evidence = topology.regrounding or sender not in fired
            observation = AgentObservation(
                agent_id=sender,
                evidence=world.evidence_for(sender) if show_evidence else (),
            )
            inbound = tuple(inbox.pop(sender, []))
            for message in inbound:
                if message.receiver != sender:
                    raise RuntimeError(
                        f"message {message.message_id} addressed to {message.receiver}, not {sender}"
                    )
            if cycle == 0 and inbound:
                raise RuntimeError("seed-cycle firings must not have inbound messages")

            visible_message_id = f"M{firing_number:02d}"
            model_visible_input = render_agent_input(sender, observation, inbound, probe=probe)
            reused = reused_events.get(firing_number) if reused_events else None
            if cycle == 0 and seed is not None and firing_number in seed:
                response = seed[firing_number].response
                provider_metadata = (
                    dict(seed[firing_number].provider_metadata)
                    if seed[firing_number].provider_metadata
                    else None
                )
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
                response = adapter.respond(sender, observation, inbound, condition)
                provider_metadata = _provider_metadata(adapter)
                response_reused = False
                source_condition = None

            message_id = f"{run_id}_{condition}_{visible_message_id}"
            parent_ids = tuple(m.message_id for m in inbound)
            visible_parent_ids = tuple(m.visible_message_id for m in inbound)
            external_roots = {e.evidence_id for e in observation.evidence}
            actual_lineage = graph.record_message(
                message_id,
                parent_ids,
                external_roots,
                visible_message_id=visible_message_id,
                visible_parent_message_ids=visible_parent_ids,
            )
            visible_envelope = actual_lineage if condition in ("lineage", "macro") else None
            outgoing = AgentMessage(
                message_id=message_id,
                sender=sender,
                receiver=firing.receivers[0] if firing.receivers else "",
                content=response.message,
                envelope=visible_envelope,
                visible_message_id=visible_message_id,
            )
            for receiver in firing.receivers:
                inbox[receiver].append(
                    AgentMessage(
                        message_id=message_id,
                        sender=sender,
                        receiver=receiver,
                        content=response.message,
                        envelope=visible_envelope,
                        visible_message_id=visible_message_id,
                    )
                )

            root_evidence = tuple(evidence_by_id[r] for r in actual_lineage.actual_roots)
            new_root_count = len(graph.last_new_roots)
            metrics = event_metrics(
                response=response,
                truth=world.truth,
                envelope=actual_lineage,
                root_evidence=root_evidence,
                new_independent_evidence=new_root_count,
                previous_response=previous_response,
            )
            parent_marks = [marks_by_message[pid] for pid in parent_ids if pid in marks_by_message]
            provenance = provenance_record(response.message, root_evidence, parent_marks)
            marks_by_message[message_id] = provenance
            events.append(
                TrialEvent(
                    trial_id=run_id,
                    condition=condition,
                    cycle=cycle,
                    sender=sender,
                    receivers=firing.receivers,
                    message_id=message_id,
                    visible_message_id=visible_message_id,
                    model_output=response,
                    agent_message=outgoing,
                    actual_lineage=actual_lineage,
                    agent_reported_information=response.message,
                    metrics=metrics,
                    provenance=provenance,
                    inbound_message_ids=parent_ids,
                    provider_metadata=provider_metadata,
                    response_reused=response_reused,
                    source_condition=source_condition,
                    model_visible_input=model_visible_input,
                )
            )
            fired.add(sender)
            previous_response = response

        if cycle > 0:
            completed_cycles += 1
            if condition == "macro" and graph.should_stop_after_cycle():
                macro_stop_triggered = True
                break

    stop_reason = "no_new_independent_roots_after_cycle" if macro_stop_triggered else "max_rounds"
    final_event = events[-1]
    focal_events = [e for e in events if e.sender == topology.focal_agent]
    focal_final = focal_events[-1] if focal_events else None
    fis_values = [
        e.metrics["false_independent_support"]
        for e in events
        if e.metrics["false_independent_support"] is not None
    ]
    per_agent_final_p_a: dict[str, float] = {}
    per_agent_max_excess: dict[str, float] = {}
    per_agent_min_excess: dict[str, float] = {}
    for agent in topology.agents:
        agent_events = [e for e in events if e.sender == agent]
        if not agent_events:
            continue
        per_agent_final_p_a[agent] = agent_events[-1].metrics["p_a"]
        excess = [e.metrics["p_a_excess_over_reference"] for e in agent_events]
        per_agent_max_excess[agent] = max(excess)
        per_agent_min_excess[agent] = min(excess)
    summary: dict[str, object] = {
        "world_id": world.world_id,
        "topology": topology.name,
        "root_mode": world.root_mode,
        "condition": condition,
        "truth": world.truth,
        "cell": world_cell(world),
        "alignment": alignment(world),
        "final": final_event.model_output.answer,
        "accuracy": final_event.metrics["accuracy"],
        "final_confidence": final_event.model_output.confidence,
        "final_brier_score": final_event.metrics["brier_score"],
        "final_p_a": final_event.metrics["p_a"],
        "final_reference_p_a": final_event.metrics["reference_p_a"],
        "final_p_a_excess_over_reference": final_event.metrics["p_a_excess_over_reference"],
        "focal_agent": topology.focal_agent,
        "focal_final_p_a": focal_final.metrics["p_a"] if focal_final else None,
        "focal_final_reference_p_a": focal_final.metrics["reference_p_a"] if focal_final else None,
        "focal_final_p_a_excess_over_reference": (
            focal_final.metrics["p_a_excess_over_reference"] if focal_final else None
        ),
        "focal_p_a_trajectory": [e.metrics["p_a"] for e in focal_events],
        "per_agent_final_p_a": per_agent_final_p_a,
        "per_agent_max_excess": per_agent_max_excess,
        "per_agent_min_excess": per_agent_min_excess,
        "completed_cycles": completed_cycles,
        "independent_evidence_root_count": graph.independent_root_count,
        "max_inference_depth": max(e.actual_lineage.inference_depth for e in events),
        "max_redundant_root_exposures": max(
            e.actual_lineage.redundant_root_exposures for e in events
        ),
        "new_independent_evidence_count": sum(
            int(e.metrics["new_independent_evidence"]) for e in events
        ),
        "reported_confidence_trajectory": [e.metrics["reported_confidence"] for e in events],
        "p_a_trajectory": [e.metrics["p_a"] for e in events],
        "p_a_excess_trajectory": [e.metrics["p_a_excess_over_reference"] for e in events],
        "p_a_delta_without_new_evidence": [
            e.metrics["p_a_delta_without_new_evidence"] for e in events
        ],
        "distinct_source_count_trajectory": [
            e.metrics["reported_distinct_source_count"] for e in events
        ],
        "false_independent_support_trajectory": [
            e.metrics["false_independent_support"] for e in events
        ],
        "max_false_independent_support": max(fis_values) if fis_values else None,
        "false_independent_support_events": sum(1 for v in fis_values if v > 0),
        "erosion_trajectory": [e.provenance["erosion_count"] for e in events],
        "agent_as_source_events": sum(1 for e in events if e.provenance["agent_as_source"]),
        "first_agent_as_source_event": next(
            (e.visible_message_id for e in events if e.provenance["agent_as_source"]), None
        ),
        "macro_stop_triggered": macro_stop_triggered,
        "stop_reason": stop_reason,
    }
    return ConditionRun(world, condition, tuple(events), summary)


def run_experiment(
    trials: int,
    rounds: int,
    seed: int,
    topology: str = "diamond",
    root_mode: str = "single",
    adapter_factory: Callable[[], AgentAdapter] | None = None,
    adapter_name: str = "deterministic_stub",
    adapter_metadata: dict[str, object] | None = None,
    run_class: str = "infrastructure",
    execution_policy: ExecutionPolicy = "paired",
    probe: bool = True,
    sensor_reliability: float = 0.70,
) -> ExperimentRun:
    if trials < 1:
        raise ValueError("trials must be at least 1")
    if execution_policy not in ("paired", "independent"):
        raise ValueError("execution_policy must be paired or independent")
    topo = get_topology(topology)
    factory = adapter_factory or DeterministicStubAdapter
    worlds = tuple(WorldGenerator(seed, topo, root_mode, sensor_reliability).generate_many(trials))
    condition_runs: list[ConditionRun] = []
    actual_model_call_count = 0
    reused_response_count = 0

    for world in worlds:
        if execution_policy == "independent":
            for condition in CONDITIONS:
                condition_run = run_condition(
                    world, condition, rounds, topo, adapter=factory(), trial_id=world.world_id, probe=probe
                )
                actual_model_call_count += len(condition_run.events)
                condition_runs.append(condition_run)
            continue

        # Paired execution: every seed-cycle firing is shared across conditions. Seed firings
        # have no inbound messages, so their prompts are condition-independent by construction.
        seed_adapter = factory()
        shared_seed: dict[int, SeedResponse] = {}
        for index, firing in enumerate(topo.seed_cycle, start=1):
            observation = AgentObservation(firing.sender, world.evidence_for(firing.sender))
            response = seed_adapter.respond(firing.sender, observation, (), "seed")
            shared_seed[index] = SeedResponse(response, _provider_metadata(seed_adapter))
            actual_model_call_count += 1

        free_run = run_condition(
            world, "free", rounds, topo, adapter=factory(), trial_id=world.world_id,
            seed=shared_seed, probe=probe,
        )
        actual_model_call_count += len(free_run.events) - len(shared_seed)
        lineage_run = run_condition(
            world, "lineage", rounds, topo, adapter=factory(), trial_id=world.world_id,
            seed=shared_seed, probe=probe,
        )
        actual_model_call_count += len(lineage_run.events) - len(shared_seed)
        lineage_events = {index + 1: event for index, event in enumerate(lineage_run.events)}
        macro_run = run_condition(
            world, "macro", rounds, topo, adapter=factory(), trial_id=world.world_id,
            seed=shared_seed, reused_events=lineage_events, probe=probe,
        )
        reused_response_count += len(macro_run.events)
        condition_runs.extend((free_run, lineage_run, macro_run))

    actual_input_tokens = actual_output_tokens = actual_total_tokens = 0
    fallback_events = 0
    served_models: set[str] = set()
    seen_response_ids: set[str] = set()
    for condition_run in condition_runs:
        for event in condition_run.events:
            if event.provider_metadata is None:
                continue
            if event.provider_metadata.get("fallback_ran"):
                fallback_events += 1
            served = event.provider_metadata.get("served_model") or event.provider_metadata.get("returned_model")
            if served:
                served_models.add(str(served))
            response_id = event.provider_metadata.get("response_id")
            if response_id and response_id in seen_response_ids:
                continue
            if response_id:
                seen_response_ids.add(response_id)
            usage = event.provider_metadata.get("usage", {})
            actual_input_tokens += int(usage.get("input_tokens") or 0)
            actual_output_tokens += int(usage.get("output_tokens") or 0)
            actual_total_tokens += int(usage.get("total_tokens") or 0)

    # Defense in depth: a scientific run must never contain a fallback-served response.
    if fallback_events and run_class != RUN_CLASS_SMOKE:
        raise RuntimeError(
            f"{fallback_events} fallback-served event(s) in run class {run_class!r}; "
            "fallbacks are permitted only in smoke_technical runs"
        )

    return ExperimentRun(
        worlds,
        tuple(condition_runs),
        topology=topo,
        root_mode=root_mode,
        adapter_name=adapter_name,
        adapter_metadata=adapter_metadata or {},
        rounds=rounds,
        seed=seed,
        run_class=run_class,
        execution_policy=execution_policy,
        probe=probe,
        sensor_reliability=sensor_reliability,
        execution_metadata={
            "actual_model_call_count": actual_model_call_count,
            "reused_response_count": reused_response_count,
            "input_tokens_actual": actual_input_tokens,
            "output_tokens_actual": actual_output_tokens,
            "total_tokens_actual": actual_total_tokens,
            "fallback_events": fallback_events,
            "served_models": sorted(served_models),
        },
    )


SUMMARY_FIELDS = [
    "world_id", "topology", "root_mode", "condition", "truth", "cell", "alignment",
    "final", "accuracy", "final_confidence", "final_brier_score", "final_p_a",
    "final_reference_p_a", "final_p_a_excess_over_reference",
    "focal_agent", "focal_final_p_a", "focal_final_reference_p_a",
    "focal_final_p_a_excess_over_reference", "focal_p_a_trajectory",
    "per_agent_final_p_a", "per_agent_max_excess", "per_agent_min_excess",
    "completed_cycles", "independent_evidence_root_count", "max_inference_depth",
    "max_redundant_root_exposures", "new_independent_evidence_count",
    "reported_confidence_trajectory", "p_a_trajectory", "p_a_excess_trajectory",
    "p_a_delta_without_new_evidence", "distinct_source_count_trajectory",
    "false_independent_support_trajectory", "max_false_independent_support",
    "false_independent_support_events", "erosion_trajectory", "agent_as_source_events",
    "first_agent_as_source_event", "macro_stop_triggered", "stop_reason",
]


def build_metadata(experiment: ExperimentRun) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "experiment": "EXP-003",
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
        "probe": experiment.probe,
        "fallbacks": bool(experiment.adapter_metadata.get("fallbacks", False)),
        "prompt_version": experiment.adapter_metadata.get("prompt_version", PROMPT_VERSION),
        "schema_version": experiment.adapter_metadata.get("schema_version", SCHEMA_VERSION),
        "python_version": platform.python_version(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "trial_count": len(experiment.worlds),
        "rounds": experiment.rounds,
        "seed": experiment.seed,
        "conditions": list(CONDITIONS),
        "topology_name": experiment.topology.name,
        "topology": experiment.topology.edges(),
        "regrounding": experiment.topology.regrounding,
        "focal_agent": experiment.topology.focal_agent,
        "root_mode": experiment.root_mode,
        "sensor_reliability": experiment.sensor_reliability,
        "worlds": [
            {
                "world_id": w.world_id,
                "seed": w.seed,
                "truth": w.truth,
                "cell": world_cell(w),
                "alignment": alignment(w),
                "evidence": [
                    {
                        "evidence_id": e.evidence_id,
                        "observed_state": e.observed_state,
                        "source": e.source,
                        "reliability": e.reliability,
                        "assigned_to": list(e.assigned_to),
                    }
                    for e in w.evidence
                ],
            }
            for w in experiment.worlds
        ],
        "adapter_metadata": experiment.adapter_metadata,
        "execution_metadata": experiment.execution_metadata,
        "note": (
            "Technical smoke test. Never scientific evidence; never archived as a set."
            if experiment.run_class == RUN_CLASS_SMOKE
            else "Exploratory real-model run. Not confirmatory evidence."
            if experiment.run_class.endswith("real_model")
            else "Infrastructure validation only. Stub results validate measurement, not the hypothesis."
        ),
    }
    fingerprint_keys = (
        "experiment", "run_class", "provider", "requested_model", "reasoning_effort",
        "sdk_version", "python_version", "timeout_seconds", "store", "max_retries", "probe", "fallbacks",
        "conditions", "topology_name", "topology", "regrounding", "root_mode",
        "sensor_reliability", "rounds", "seed", "trial_count", "execution_policy",
        "prompt_version", "schema_version",
    )
    fingerprint_input = {key: metadata[key] for key in fingerprint_keys}
    metadata["config_fingerprint"] = hashlib.sha256(
        json.dumps(fingerprint_input, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return metadata


def write_results(experiment: ExperimentRun, results_dir: Path | None = None) -> Path:
    results_dir = results_dir or RESULTS
    results_dir.mkdir(parents=True, exist_ok=True)
    with (results_dir / "events.jsonl").open("w", encoding="utf-8") as output:
        for condition_run in experiment.condition_runs:
            for event in condition_run.events:
                output.write(json.dumps(event.to_record(), sort_keys=True) + "\n")
    with (results_dir / "summary.csv").open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=SUMMARY_FIELDS)
        writer.writeheader()
        for condition_run in experiment.condition_runs:
            writer.writerow({f: condition_run.summary[f] for f in SUMMARY_FIELDS})
    (results_dir / "run_metadata.json").write_text(
        json.dumps(build_metadata(experiment), indent=2) + "\n", encoding="utf-8"
    )
    return results_dir


def print_results(experiment: ExperimentRun) -> None:
    print(
        f"\nEXP-003 run\nTopology: {experiment.topology.name} (regrounding={experiment.topology.regrounding})"
        f"\nRoot mode: {experiment.root_mode}\nAdapter: {experiment.adapter_name}"
        f"\nExecution policy: {experiment.execution_policy}\nProbe: {experiment.probe}"
    )
    model = experiment.adapter_metadata.get("requested_model")
    if model:
        print(f"Model: {model}")
    print()
    print(
        f"{'WORLD':14} {'COND':8} {'CELL':8} {'FINAL':>5} {'ACC':>3} {'CONF':>6} "
        f"{'FOCAL_PA':>8} {'REF_PA':>6} {'EXCESS':>7} {'ROOTS':>5} {'DEPTH':>5} "
        f"{'REDUND':>6} {'MAXFIS':>6} {'CYC':>3} {'STOP':>34}"
    )
    print("-" * 140)
    for run in experiment.condition_runs:
        s = run.summary
        fis = s["max_false_independent_support"]
        print(
            f"{s['world_id']:14} {s['condition']:8} {s['cell']:8} {s['final']:>5} "
            f"{s['accuracy']:3d} {s['final_confidence']:6.3f} "
            f"{(s['focal_final_p_a'] if s['focal_final_p_a'] is not None else float('nan')):8.3f} "
            f"{(s['focal_final_reference_p_a'] if s['focal_final_reference_p_a'] is not None else float('nan')):6.3f} "
            f"{(s['focal_final_p_a_excess_over_reference'] if s['focal_final_p_a_excess_over_reference'] is not None else float('nan')):7.3f} "
            f"{s['independent_evidence_root_count']:5d} {s['max_inference_depth']:5d} "
            f"{s['max_redundant_root_exposures']:6d} {(fis if fis is not None else -1):6d} "
            f"{s['completed_cycles']:3d} {s['stop_reason']:>34}"
        )
    calls = experiment.execution_metadata["actual_model_call_count"]
    reused = experiment.execution_metadata["reused_response_count"]
    print(f"\nActual model calls: {calls}; reused responses: {reused}")
    fallbacks = experiment.execution_metadata.get("fallback_events", 0)
    if experiment.run_class == RUN_CLASS_SMOKE:
        served = ", ".join(experiment.execution_metadata.get("served_models", [])) or "n/a"
        print(f"SMOKE TEST: fallback-served events: {fallbacks}; served models: {served}. Not scientific evidence.")
    print(f"Results: {RESULTS}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the EXP-003 fan-in harness")
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--rounds", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--topology", default="diamond")
    parser.add_argument("--root-mode", choices=("single", "shared", "dual"), default="single")
    parser.add_argument("--adapter", choices=PROVIDERS, default="deterministic_stub",
                        help="model layer: deterministic_stub, openai or anthropic")
    parser.add_argument("--stub-mode", choices=("naive", "dedup"), default="naive")
    parser.add_argument("--model", default=None)
    parser.add_argument("--reasoning-effort", default=None)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--reliability", type=float, default=0.70)
    parser.add_argument("--no-probe", action="store_true", help="omit the distinct-source probe")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--execution-policy", choices=("paired", "independent"), default=None)
    parser.add_argument("--smoke", action="store_true",
                        help="technical smoke test: run class smoke_technical, never a scientific set")
    parser.add_argument("--fallbacks", action="store_true",
                        help="anthropic only, requires --smoke: opt into server-side refusal fallbacks")
    args = parser.parse_args()
    probe = not args.no_probe

    binding = build_provider(
        args.adapter, model=args.model, reasoning_effort=args.reasoning_effort,
        probe=probe, timeout_seconds=args.timeout, stub_mode=args.stub_mode,
        smoke=args.smoke, fallbacks=args.fallbacks,
    )
    if binding.live:
        if not args.live:
            raise SystemExit(f"{args.adapter} adapter requires --live; no network call made")
        if args.execution_policy is None:
            raise SystemExit("real-model runs require --execution-policy paired or independent")
    elif args.live:
        raise SystemExit("--live is only valid with a real-model adapter")

    experiment = run_experiment(
        args.trials, args.rounds, args.seed,
        topology=args.topology, root_mode=args.root_mode,
        adapter_factory=binding.factory, adapter_name=binding.adapter_name,
        adapter_metadata=binding.metadata, run_class=binding.run_class,
        execution_policy=args.execution_policy or "paired", probe=probe,
        sensor_reliability=args.reliability,
    )
    write_results(experiment)
    print_results(experiment)


if __name__ == "__main__":
    main()
