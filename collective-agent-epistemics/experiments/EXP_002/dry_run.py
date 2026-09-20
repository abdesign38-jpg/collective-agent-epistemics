from __future__ import annotations

from dataclasses import dataclass

from .adapters.deterministic_stub import DeterministicStubAdapter
from .lineage import LineageGraph
from .models import AgentMessage, AgentObservation, World
from .prompting import render_agent_input

SEED_EDGE = ("A", "B")
RECURSIVE_SEQUENCE = (("B", "C"), ("C", "A"), ("A", "B"))


@dataclass(frozen=True)
class DryRunInput:
    world_id: str
    condition: str
    agent_id: str
    step: int
    rendered_input: str


def print_dry_run_configuration(config: dict[str, object]) -> None:
    print("EXP-002 OpenAI dry-run configuration")
    for key in (
        "provider",
        "requested_model",
        "reasoning_effort",
        "prompt_version",
        "schema_version",
    ):
        print(f"{key}: {config[key]}")
    print("live: false\n")


def build_dry_run_inputs(
    world: World,
    execution_policy: str = "paired",
) -> tuple[DryRunInput, ...]:
    observation_a = AgentObservation(
        agent_id="A",
        evidence=tuple(e for e in world.evidence if e.assigned_to == "A"),
    )
    seed_response = DeterministicStubAdapter().respond("A", observation_a, None, "free")
    inputs: list[DryRunInput] = []
    for condition in ("FREE", "LINEAGE", "MACRO"):
        graph = LineageGraph()
        received_message = None
        sequence = (SEED_EDGE, *RECURSIVE_SEQUENCE)
        for index, (sender, receiver) in enumerate(sequence, start=1):
            observation = AgentObservation(
                agent_id=sender,
                evidence=tuple(e for e in world.evidence if e.assigned_to == sender),
            )
            inputs.append(
                DryRunInput(
                    world.world_id,
                    condition,
                    sender,
                    index,
                    render_agent_input(sender, observation, received_message),
                )
            )
            visible_id = f"M{index:02d}"
            internal_id = f"dry_{condition.lower()}_{visible_id}"
            actual = graph.record_message(
                internal_id,
                received_message.message_id if received_message else None,
                {e.evidence_id for e in observation.evidence},
                visible_message_id=visible_id,
                visible_parent_message_id=(received_message.visible_message_id if received_message else None),
            )
            received_message = AgentMessage(
                message_id=internal_id,
                sender=sender,
                receiver=receiver,
                content=seed_response.message,
                envelope=actual if condition != "FREE" else None,
                visible_message_id=visible_id,
            )
    return tuple(inputs)


def print_dry_run(inputs: tuple[DryRunInput, ...], execution_policy: str) -> None:
    print(f"execution_policy: {execution_policy}\n")
    for item in inputs:
        print(f"\nWorld 1 / {item.condition} / Agent {item.agent_id} (M{item.step:02d})\n")
        print(item.rendered_input)
        print("\n" + "=" * 72)
