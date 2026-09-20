from __future__ import annotations

from dataclasses import dataclass
from src.models import AgentState, Claim
from src.math_utils import confidence_for_a, signed_weight

@dataclass
class SyntheticAgent:
    state: AgentState

    def _base_weights(self) -> list[float]:
        weights = []
        for ev in self.state.evidence:
            weights.append(signed_weight(ev.supports_state, ev.reliability))
        return weights

    def make_claim(self, condition: str, claim_id: str, derived_from: str | None = None) -> Claim:
        weights = self._base_weights()
        actual_roots = {ev.evidence_id for ev in self.state.evidence}
        perceived_roots = set(actual_roots)
        depth = 0

        if condition == "free":
            # Naive baseline: each received claim is treated as a new social evidence unit.
            # This is intentionally explicit and is only for validating instrumentation.
            for incoming in self.state.received:
                direction = 1.0 if incoming.supports_state == "A" else -1.0
                from src.math_utils import logit
                weights.append(direction * logit(incoming.confidence))
                actual_roots.update(incoming.actual_roots)
                # In free mode the receiver does not know the true roots and treats
                # the incoming claim itself as an independent support token.
                perceived_roots.add(incoming.claim_id)
                depth = max(depth, incoming.inference_depth + 1)

        elif condition in {"lineage", "macro"}:
            # Structured baseline: a root can contribute at most once to evidential weight.
            # Incoming claims can transmit roots, but do not magically create new ones.
            root_evidence = {ev.evidence_id: ev for ev in self.state.evidence}
            seen = set(root_evidence.keys())

            for incoming in self.state.received:
                actual_roots.update(incoming.actual_roots)
                perceived_roots.update(incoming.actual_roots)
                depth = max(depth, incoming.inference_depth + 1)

                # If this agent does not directly possess a root, adopt the sender's
                # posterior as a representation of that root set only once.
                unseen = set(incoming.actual_roots) - seen
                if unseen:
                    # One aggregate social update for the newly introduced root set.
                    from src.math_utils import logit
                    direction = 1.0 if incoming.supports_state == "A" else -1.0
                    weights.append(direction * logit(incoming.confidence))
                    seen.update(unseen)

        p_a = confidence_for_a(weights)
        supports = "A" if p_a >= 0.5 else "B"
        confidence = p_a if supports == "A" else 1.0 - p_a

        return Claim(
            claim_id=claim_id,
            sender=self.state.name,
            supports_state=supports,
            confidence=confidence,
            actual_roots=frozenset(actual_roots),
            perceived_roots=frozenset(perceived_roots),
            inference_depth=depth,
            derived_from=derived_from,
        )

    def receive(self, claim: Claim) -> None:
        self.state.received.append(claim)
