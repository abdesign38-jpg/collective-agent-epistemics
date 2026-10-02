from __future__ import annotations

from .models import AgentMessage, AgentObservation

PROMPT_VERSION = "exp003-v0.1"

BASE_TASK = """You are Agent {agent_id}.

Determine whether hidden state A or B is more likely using only the information provided in this request.

Return your selected state, your confidence between 0 and 1, and a concise message for the next agent.
"""

BASE_TASK_WITH_PROBE = """You are Agent {agent_id}.

Determine whether hidden state A or B is more likely using only the information provided in this request.

Return your selected state, your confidence between 0 and 1, the number of distinct original sources (for example, separate sensors) that you believe your conclusion rests on, and a concise message for the next agent.
"""


def render_agent_input(
    agent_id: str,
    observation: AgentObservation,
    received_messages: tuple[AgentMessage, ...],
    probe: bool = True,
) -> str:
    task = BASE_TASK_WITH_PROBE if probe else BASE_TASK
    sections = [task.format(agent_id=agent_id).strip()]
    if observation.evidence:
        direct_lines = ["Direct observation:"]
        for evidence in observation.evidence:
            direct_lines.extend(
                (
                    f"Source: {evidence.source}",
                    f"Observed state: {evidence.observed_state}",
                    f"Reported reliability: {evidence.reliability:.2f}",
                )
            )
        sections.append("\n".join(direct_lines))
    else:
        sections.append("Direct observation: none")

    if not received_messages:
        # Same wording as EXP-002 so single-inbound, probe-off prompts are byte-identical.
        sections.append("Received message: none")
    else:
        total = len(received_messages)
        for index, received in enumerate(received_messages, start=1):
            header = "Received message:" if total == 1 else f"Received message {index} of {total}:"
            message_lines = [
                header,
                f"Sender: Agent {received.sender}",
                f"Message: {received.content}",
            ]
            if received.envelope is not None:
                envelope = received.envelope
                derived = ", ".join(envelope.derived_from) if envelope.derived_from else "none"
                message_lines.extend(
                    (
                        "Message metadata:",
                        f"Evidence roots: [{', '.join(envelope.actual_roots)}]",
                        f"Derived from: {derived}",
                        f"Inference depth: {envelope.inference_depth}",
                        f"New external evidence: {str(envelope.new_external_evidence).lower()}",
                    )
                )
            sections.append("\n".join(message_lines))
    return "\n\n".join(sections)
