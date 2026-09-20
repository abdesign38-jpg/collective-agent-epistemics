from __future__ import annotations

from .models import AgentMessage, AgentObservation

PROMPT_VERSION = "exp002-v0.1"

BASE_TASK = """You are Agent {agent_id}.

Determine whether hidden state A or B is more likely using only the information provided in this request.

Return your selected state, your confidence between 0 and 1, and a concise message for the next agent.
"""


def render_agent_input(
    agent_id: str,
    observation: AgentObservation,
    received_message: AgentMessage | None,
) -> str:
    sections = [BASE_TASK.format(agent_id=agent_id).strip()]
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

    if received_message is None:
        sections.append("Received message: none")
    else:
        message_lines = [
            "Received message:",
            f"Sender: Agent {received_message.sender}",
            f"Message: {received_message.content}",
        ]
        if received_message.envelope is not None:
            envelope = received_message.envelope
            message_lines.extend(
                (
                    "Message metadata:",
                    f"Evidence roots: [{', '.join(envelope.actual_roots)}]",
                    f"Derived from: {envelope.derived_from or 'none'}",
                    f"Inference depth: {envelope.inference_depth}",
                    f"New external evidence: {str(envelope.new_external_evidence).lower()}",
                )
            )
        sections.append("\n".join(message_lines))
    return "\n\n".join(sections)
