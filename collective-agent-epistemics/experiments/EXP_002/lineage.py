from __future__ import annotations

from dataclasses import dataclass, field

from .models import EpistemicEnvelope


@dataclass(frozen=True)
class LineageNode:
    message_id: str
    parent_message_id: str | None
    evidence_roots: frozenset[str]
    inference_depth: int


@dataclass
class LineageGraph:
    """Deterministic hidden lineage DAG maintained by the harness."""

    nodes: dict[str, LineageNode] = field(default_factory=dict)
    seen_roots: set[str] = field(default_factory=set)
    cycle_new_roots: set[str] = field(default_factory=set)
    last_new_roots: frozenset[str] = field(default_factory=frozenset)

    def start_cycle(self) -> None:
        self.cycle_new_roots = set()

    def record_message(
        self,
        message_id: str,
        parent_message_id: str | None,
        external_roots: set[str] | frozenset[str] = frozenset(),
    ) -> EpistemicEnvelope:
        if message_id in self.nodes:
            raise ValueError(f"message already recorded: {message_id}")
        parent = self.nodes.get(parent_message_id) if parent_message_id else None
        if parent_message_id and parent is None:
            raise ValueError(f"unknown parent message: {parent_message_id}")

        roots = set(external_roots)
        depth = 0
        if parent is not None:
            roots.update(parent.evidence_roots)
            depth = parent.inference_depth + 1

        new_roots = roots - self.seen_roots
        self.seen_roots.update(roots)
        self.cycle_new_roots.update(new_roots)
        self.last_new_roots = frozenset(new_roots)
        self.nodes[message_id] = LineageNode(
            message_id=message_id,
            parent_message_id=parent_message_id,
            evidence_roots=frozenset(roots),
            inference_depth=depth,
        )
        return EpistemicEnvelope(
            actual_roots=tuple(sorted(roots)),
            derived_from=parent_message_id,
            inference_depth=depth,
            new_external_evidence=bool(new_roots),
        )

    def should_stop_after_cycle(self) -> bool:
        return not self.cycle_new_roots

    @property
    def independent_root_count(self) -> int:
        return len(self.seen_roots)

    def ancestry(self, message_id: str) -> list[str]:
        ancestry: list[str] = []
        current = self.nodes.get(message_id)
        while current is not None:
            ancestry.append(current.message_id)
            current = self.nodes.get(current.parent_message_id) if current.parent_message_id else None
        return list(reversed(ancestry))
