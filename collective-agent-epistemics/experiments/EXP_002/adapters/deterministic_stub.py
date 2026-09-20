from __future__ import annotations

import re

from ..models import AgentMessage, AgentObservation, AgentResponse, State


class DeterministicStubAdapter:
    """Minimal orchestration stub; it does not inspect hidden lineage metadata."""

    def respond(
        self,
        agent_id: str,
        observation: AgentObservation,
        received_message: AgentMessage | None,
        condition: str,
    ) -> AgentResponse:
        del agent_id, condition
        if observation.evidence:
            evidence = observation.evidence[0]
            answer = evidence.observed_state
            confidence = evidence.reliability
        else:
            answer = _answer_from_message(received_message) if received_message else "A"
            confidence = 0.60
        return AgentResponse(
            answer=answer,
            confidence=confidence,
            message=f"State {answer} is favored.",
        )


def _answer_from_message(message: AgentMessage) -> State:
    match = re.search(r"State ([AB]) is favored", message.content)
    return match.group(1) if match else "A"
