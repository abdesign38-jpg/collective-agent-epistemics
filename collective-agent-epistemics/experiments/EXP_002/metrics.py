from __future__ import annotations

from typing import Any

from .models import AgentResponse, EpistemicEnvelope, State


def accuracy(answer: State, truth: State) -> int:
    return int(answer == truth)


def probability_of_a(answer: State, confidence: float) -> float:
    return round(confidence if answer == "A" else 1.0 - confidence, 6)


def brier_score(answer: State, confidence: float, truth: State) -> float:
    p_a = probability_of_a(answer, confidence)
    truth_a = 1 if truth == "A" else 0
    return round((p_a - truth_a) ** 2, 6)


def p_a_delta_without_new_evidence(
    previous_p_a: float | None,
    current_p_a: float,
    new_independent_evidence: int,
) -> float | None:
    if previous_p_a is None or new_independent_evidence != 0:
        return None
    return round(current_p_a - previous_p_a, 6)


def event_metrics(
    response: AgentResponse,
    truth: State,
    envelope: EpistemicEnvelope,
    new_independent_evidence: int,
    previous_response: AgentResponse | None,
) -> dict[str, Any]:
    p_a = probability_of_a(response.answer, response.confidence)
    previous_p_a = (
        probability_of_a(previous_response.answer, previous_response.confidence)
        if previous_response
        else None
    )
    return {
        "accuracy": accuracy(response.answer, truth),
        "reported_confidence": response.confidence,
        "confidence": response.confidence,
        "p_a": p_a,
        "brier_score": brier_score(response.answer, response.confidence, truth),
        "independent_evidence_root_count": len(envelope.actual_roots),
        "inference_depth": envelope.inference_depth,
        "new_independent_evidence": new_independent_evidence,
        "p_a_delta_without_new_evidence": p_a_delta_without_new_evidence(
            previous_p_a,
            p_a,
            new_independent_evidence,
        ),
    }
