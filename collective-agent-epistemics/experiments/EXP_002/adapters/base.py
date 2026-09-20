from __future__ import annotations

from typing import Protocol

from ..models import AgentMessage, AgentObservation, AgentResponse


class AgentAdapter(Protocol):
    def respond(
        self,
        agent_id: str,
        observation: AgentObservation,
        received_message: AgentMessage | None,
        condition: str,
    ) -> AgentResponse:
        ...
