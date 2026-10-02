from __future__ import annotations

from typing import Any

from .models import AgentResponse, EpistemicEnvelope, Evidence, State


def accuracy(answer: State, truth: State) -> int:
    return int(answer == truth)


def probability_of_a(answer: State, confidence: float) -> float:
    return round(confidence if answer == "A" else 1.0 - confidence, 6)


def brier_score(answer: State, confidence: float, truth: State) -> float:
    p_a = probability_of_a(answer, confidence)
    truth_a = 1 if truth == "A" else 0
    return round((p_a - truth_a) ** 2, 6)


def reference_probability_of_a(roots: tuple[Evidence, ...]) -> float:
    """Normative P(A) from combining the actual independent roots with a uniform prior.

    Each root contributes odds r/(1-r) toward its observed state. This is the value a
    perfectly lineage-aware agent would report given exactly those roots and nothing
    else. It is the fixed reference against which excess (double counting) or discount
    is measured. With one root at reliability .70 it is .70 for observed A, .30 for
    observed B. With two agreeing roots at .70 it is about .845; with two conflicting
    roots at .70 it is .50.
    """
    odds = 1.0
    for evidence in roots:
        r = min(max(evidence.reliability, 1e-9), 1 - 1e-9)
        ratio = r / (1.0 - r)
        odds *= ratio if evidence.observed_state == "A" else 1.0 / ratio
    return round(odds / (1.0 + odds), 6)


def p_a_delta_without_new_evidence(
    previous_p_a: float | None,
    current_p_a: float,
    new_independent_evidence: int,
) -> float | None:
    if previous_p_a is None or new_independent_evidence != 0:
        return None
    return round(current_p_a - previous_p_a, 6)


def false_independent_support(
    reported_distinct_sources: int | None, actual_root_count: int
) -> int | None:
    """How many more distinct sources the agent believes it has than actually exist."""
    if reported_distinct_sources is None:
        return None
    return max(0, reported_distinct_sources - actual_root_count)


def event_metrics(
    response: AgentResponse,
    truth: State,
    envelope: EpistemicEnvelope,
    root_evidence: tuple[Evidence, ...],
    new_independent_evidence: int,
    previous_response: AgentResponse | None,
) -> dict[str, Any]:
    p_a = probability_of_a(response.answer, response.confidence)
    previous_p_a = (
        probability_of_a(previous_response.answer, previous_response.confidence)
        if previous_response
        else None
    )
    reference = reference_probability_of_a(root_evidence)
    actual_root_count = len(envelope.actual_roots)
    return {
        "accuracy": accuracy(response.answer, truth),
        "reported_confidence": response.confidence,
        "confidence": response.confidence,
        "p_a": p_a,
        "brier_score": brier_score(response.answer, response.confidence, truth),
        "reference_p_a": reference,
        "p_a_excess_over_reference": round(p_a - reference, 6),
        "independent_evidence_root_count": actual_root_count,
        "inference_depth": envelope.inference_depth,
        "redundant_root_exposures": envelope.redundant_root_exposures,
        "new_independent_evidence": new_independent_evidence,
        "p_a_delta_without_new_evidence": p_a_delta_without_new_evidence(
            previous_p_a, p_a, new_independent_evidence
        ),
        "reported_distinct_source_count": response.distinct_source_count,
        "false_independent_support": false_independent_support(
            response.distinct_source_count, actual_root_count
        ),
    }
