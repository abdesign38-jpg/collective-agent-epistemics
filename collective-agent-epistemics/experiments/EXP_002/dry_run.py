from __future__ import annotations

from dataclasses import dataclass

from .adapters.deterministic_stub import DeterministicStubAdapter
from .lineage import LineageGraph
from .models import AgentMessage, AgentObservation, World
from .prompting import render_agent_input


@dataclass(frozen=True)
class DryRunInput:
    world_id: str
    condition: str
    agent_id: str
    rendered_input: str


def build_dry_run_inputs(world: World) -> tuple[DryRunInput, ...]:
    observation_a = AgentObservation(
        agent_id="A",
        evidence=tuple(e for e in world.evidence if e.assigned_to == "A"),
    )
    seed_response = DeterministicStubAdapter().respond("A", observation_a, None, "free")
    graph = LineageGraph()
    lineage = graph.record_message("A_01", None, {e.evidence_id for e in observation_a.evidence})
    inputs = [
        DryRunInput(world.world_id, "FREE", "A", render_agent_input("A", observation_a, None)),
    ]
    for condition, envelope in (("FREE", None), ("LINEAGE", lineage), ("MACRO", lineage)):
        message = AgentMessage(
            message_id="A_01",
            sender="A",
            receiver="B",
            content=seed_response.message,
            envelope=envelope,
        )
        observation_b = AgentObservation(agent_id="B", evidence=())
        inputs.append(
            DryRunInput(
                world.world_id,
                condition,
                "B",
                render_agent_input("B", observation_b, message),
            )
        )
    return tuple(inputs)


def print_dry_run(inputs: tuple[DryRunInput, ...]) -> None:
    for item in inputs:
        print(f"\nWorld 1 / {item.condition} / Agent {item.agent_id}\n")
        print(item.rendered_input)
        print("\n" + "=" * 72)
