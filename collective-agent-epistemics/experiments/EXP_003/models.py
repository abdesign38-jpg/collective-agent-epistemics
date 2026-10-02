from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

State = Literal["A", "B"]


@dataclass(frozen=True)
class Evidence:
    """One independent external evidence root (a sensor reading)."""

    evidence_id: str
    observed_state: State
    source: str
    reliability: float
    assigned_to: tuple[str, ...]


@dataclass(frozen=True)
class World:
    world_id: str
    seed: int
    truth: State
    evidence: tuple[Evidence, ...]
    topology: str
    root_mode: str

    def evidence_for(self, agent_id: str) -> tuple[Evidence, ...]:
        return tuple(e for e in self.evidence if agent_id in e.assigned_to)

    def evidence_by_id(self) -> dict[str, Evidence]:
        return {e.evidence_id: e for e in self.evidence}


@dataclass(frozen=True)
class EpistemicEnvelope:
    """Harness-owned actual lineage. Multi-parent because fan-in is allowed."""

    actual_roots: tuple[str, ...]
    derived_from: tuple[str, ...]
    inference_depth: int
    new_external_evidence: bool
    redundant_root_exposures: int


@dataclass(frozen=True)
class AgentMessage:
    message_id: str
    sender: str
    receiver: str
    content: str
    envelope: EpistemicEnvelope | None = None
    visible_message_id: str = ""


@dataclass(frozen=True)
class AgentObservation:
    agent_id: str
    evidence: tuple[Evidence, ...]


@dataclass(frozen=True)
class AgentResponse:
    answer: State
    confidence: float
    message: str
    distinct_source_count: int | None = None


@dataclass(frozen=True)
class TrialEvent:
    trial_id: str
    condition: str
    cycle: int
    sender: str
    receivers: tuple[str, ...]
    message_id: str
    visible_message_id: str
    model_output: AgentResponse
    agent_message: AgentMessage
    actual_lineage: EpistemicEnvelope
    agent_reported_information: str
    metrics: dict[str, Any]
    provenance: dict[str, Any]
    inbound_message_ids: tuple[str, ...] = ()
    provider_metadata: dict[str, Any] | None = None
    response_reused: bool = False
    source_condition: str | None = None
    model_visible_input: str = ""

    def to_record(self) -> dict[str, Any]:
        return {
            "trial_id": self.trial_id,
            "condition": self.condition,
            "cycle": self.cycle,
            "sender": self.sender,
            "receivers": list(self.receivers),
            "message_id": self.message_id,
            "visible_message_id": self.visible_message_id,
            "model_output": {
                "answer": self.model_output.answer,
                "confidence": self.model_output.confidence,
                "distinct_source_count": self.model_output.distinct_source_count,
                "message": self.model_output.message,
            },
            "agent_message": {
                "message_id": self.agent_message.message_id,
                "sender": self.agent_message.sender,
                "receivers": list(self.receivers),
                "content": self.agent_message.content,
                "envelope": _envelope_record(self.agent_message.envelope),
            },
            "actual_lineage": _envelope_record(self.actual_lineage),
            "inbound_message_ids": list(self.inbound_message_ids),
            "agent_reported_information": self.agent_reported_information,
            "metrics": self.metrics,
            "provenance": self.provenance,
            "provider_metadata": self.provider_metadata,
            "response_reused": self.response_reused,
            "source_condition": self.source_condition,
            "model_visible_input": self.model_visible_input,
        }


def _envelope_record(envelope: EpistemicEnvelope | None) -> dict[str, Any] | None:
    if envelope is None:
        return None
    return {
        "actual_roots": list(envelope.actual_roots),
        "derived_from": list(envelope.derived_from),
        "inference_depth": envelope.inference_depth,
        "new_external_evidence": envelope.new_external_evidence,
        "redundant_root_exposures": envelope.redundant_root_exposures,
    }
