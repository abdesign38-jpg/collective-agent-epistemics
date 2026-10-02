from __future__ import annotations

import re

from ..models import AgentMessage, AgentObservation, AgentResponse, State

MESSAGE_PATTERN = re.compile(
    r"State (?P<answer>[AB]) is favored with confidence (?P<confidence>\d\.\d+) based on (?P<count>\d+) source"
)


class DeterministicStubAdapter:
    """Auditable stand-in agents used to validate that the harness can detect double counting.

    mode="naive":  treats every inbound message as one more independent source and
                   multiplies odds. This is the behavior the hypothesis predicts a
                   lineage-blind agent would show. Under fan-in it inflates.
    mode="dedup":  when envelopes are visible, covers each evidence root once, preferring
                   the message with the largest root set (a message that already folds in
                   E1 replaces the direct E1 reading instead of stacking on it); without
                   envelopes (FREE) it cannot deduplicate and behaves like "naive".

    Neither stub is a model of an LLM. A stub result validates measurement, never the
    hypothesis, exactly as in EXP-001.
    """

    def __init__(self, mode: str = "naive") -> None:
        if mode not in ("naive", "dedup"):
            raise ValueError("mode must be naive or dedup")
        self.mode = mode

    def respond(
        self,
        agent_id: str,
        observation: AgentObservation,
        received_messages: tuple[AgentMessage, ...],
        condition: str,
    ) -> AgentResponse:
        del agent_id, condition
        # Each item is (root set, odds toward A). Direct evidence is one item per root;
        # each inbound message is one item whose roots come from its envelope when visible.
        items: list[tuple[frozenset[str], float]] = [
            (frozenset({e.evidence_id}), _odds_for(e.observed_state, e.reliability))
            for e in observation.evidence
        ]
        envelopes_visible = True
        for message in received_messages:
            parsed = MESSAGE_PATTERN.search(message.content)
            if parsed is None:
                continue
            answer: State = parsed.group("answer")  # type: ignore[assignment]
            odds_m = _odds_for(answer, float(parsed.group("confidence")))
            if message.envelope is None:
                envelopes_visible = False
                items.append((frozenset(), odds_m))
            else:
                items.append((frozenset(message.envelope.actual_roots), odds_m))

        odds = 1.0
        count = 0
        if self.mode == "dedup" and envelopes_visible:
            # Greedy cover: take the item with the largest root set first and skip any
            # item whose roots are already covered. A message that already folds in E1
            # therefore replaces the direct E1 reading rather than stacking on it.
            counted: set[str] = set()
            for roots, odds_i in sorted(items, key=lambda it: -len(it[0])):
                if roots and roots <= counted:
                    continue
                counted |= roots
                odds *= odds_i
            count = len(counted)
        else:
            for _, odds_i in items:
                odds *= odds_i
            count = len(items)

        p_a = odds / (1.0 + odds)
        answer_out: State = "A" if p_a >= 0.5 else "B"
        confidence_out = round(max(p_a, 1.0 - p_a), 4)
        return AgentResponse(
            answer=answer_out,
            confidence=confidence_out,
            message=(
                f"State {answer_out} is favored with confidence {confidence_out:.4f} "
                f"based on {count} source(s)."
            ),
            distinct_source_count=count,
        )


def _odds_for(state: State, confidence: float) -> float:
    c = min(max(confidence, 1e-6), 1 - 1e-6)
    ratio = c / (1.0 - c)
    return ratio if state == "A" else 1.0 / ratio
