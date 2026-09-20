from __future__ import annotations

from typing import Any

from .models import AgentResponse, EpistemicEnvelope, State


def accuracy(answer: State, truth: State) -> int:
    return int(answer == truth)


def brier_score(answer: State, confidence: float, truth: State) -> float:
    probability_of_truth = confidence if answer == truth else 1.0 - confidence
    return round((probability_of_truth - 1.0) ** 2, 6)


def confidence_delta_without_new_evidence(
    previous_confidence: float | None,
    current_confidence: float,
    new_independent_evidence: int,
) -> float | None:
    if previous_confidence is None or new_independent_evidence != 0:
        return None
    return round(current_confidence - previous_confidence, 6)


def event_metrics(
    response: AgentResponse,
    truth: State,
    envelope: EpistemicEnvelope,
    new_independent_evidence: int,
    previous_response: AgentResponse | None,
) -> dict[str, Any]:
    return {
        "accuracy": accuracy(response.answer, truth),
        "confidence": response.confidence,
        "brier_score": brier_score(response.answer, response.confidence, truth),
        "independent_evidence_root_count": len(envelope.actual_roots),
        "inference_depth": envelope.inference_depth,
        "new_independent_evidence": new_independent_evidence,
        "confidence_delta_without_new_evidence": confidence_delta_without_new_evidence(
            previous_response.confidence if previous_response else None,
            response.confidence,
            new_independent_evidence,
        ),
    }
