from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

State = Literal["A", "B"]


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    observed_state: State
    source: str
    reliability: float
    assigned_to: str


@dataclass(frozen=True)
class World:
    world_id: str
    seed: int
    truth: State
    evidence: tuple[Evidence, ...]


@dataclass(frozen=True)
class EpistemicEnvelope:
    actual_roots: tuple[str, ...]
    derived_from: str | None
    inference_depth: int
    new_external_evidence: bool


@dataclass(frozen=True)
class AgentMessage:
    message_id: str
    sender: str
    receiver: str
    content: str
    envelope: EpistemicEnvelope | None = None


@dataclass(frozen=True)
class AgentObservation:
    agent_id: str
    evidence: tuple[Evidence, ...]


@dataclass(frozen=True)
class AgentResponse:
    answer: State
    confidence: float
    message: str


@dataclass(frozen=True)
class TrialEvent:
    trial_id: str
    condition: str
    cycle: int
    sender: str
    receiver: str
    message_id: str
    model_output: AgentResponse
    agent_message: AgentMessage
    actual_lineage: EpistemicEnvelope
    agent_reported_information: str
    metrics: dict[str, Any]

    def to_record(self) -> dict[str, Any]:
        return {
            "trial_id": self.trial_id,
            "condition": self.condition,
            "cycle": self.cycle,
            "sender": self.sender,
            "receiver": self.receiver,
            "message_id": self.message_id,
            "model_output": {
                "answer": self.model_output.answer,
                "confidence": self.model_output.confidence,
                "message": self.model_output.message,
            },
            "agent_message": {
                "message_id": self.agent_message.message_id,
                "sender": self.agent_message.sender,
                "receiver": self.agent_message.receiver,
                "content": self.agent_message.content,
                "envelope": _envelope_record(self.agent_message.envelope),
            },
            "actual_lineage": _envelope_record(self.actual_lineage),
            "agent_reported_information": self.agent_reported_information,
            "metrics": self.metrics,
        }


def _envelope_record(envelope: EpistemicEnvelope | None) -> dict[str, Any] | None:
    if envelope is None:
        return None
    return {
        "actual_roots": list(envelope.actual_roots),
        "derived_from": envelope.derived_from,
        "inference_depth": envelope.inference_depth,
        "new_external_evidence": envelope.new_external_evidence,
    }
