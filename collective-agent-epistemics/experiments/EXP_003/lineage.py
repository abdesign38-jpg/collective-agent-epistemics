from __future__ import annotations

from dataclasses import dataclass, field

from .models import EpistemicEnvelope


@dataclass(frozen=True)
class LineageNode:
    message_id: str
    visible_message_id: str
    parent_message_ids: tuple[str, ...]
    evidence_roots: frozenset[str]
    inference_depth: int


@dataclass
class LineageGraph:
    """Hidden multi-parent lineage DAG maintained by the harness.

    Compared with EXP-002 this graph accepts several parents per message, which is
    what fan-in topologies need. Roots are the union over parents and direct
    evidence; depth is one more than the deepest parent.
    """

    nodes: dict[str, LineageNode] = field(default_factory=dict)
    seen_roots: set[str] = field(default_factory=set)
    cycle_new_roots: set[str] = field(default_factory=set)
    last_new_roots: frozenset[str] = field(default_factory=frozenset)

    def start_cycle(self) -> None:
        self.cycle_new_roots = set()

    def record_message(
        self,
        message_id: str,
        parent_message_ids: tuple[str, ...] = (),
        external_roots: set[str] | frozenset[str] = frozenset(),
        visible_message_id: str | None = None,
        visible_parent_message_ids: tuple[str, ...] = (),
    ) -> EpistemicEnvelope:
        if message_id in self.nodes:
            raise ValueError(f"message already recorded: {message_id}")
        parents: list[LineageNode] = []
        for parent_id in parent_message_ids:
            parent = self.nodes.get(parent_id)
            if parent is None:
                raise ValueError(f"unknown parent message: {parent_id}")
            parents.append(parent)

        roots = set(external_roots)
        exposures = len(roots)
        depth = 0
        for parent in parents:
            roots.update(parent.evidence_roots)
            exposures += len(parent.evidence_roots)
            depth = max(depth, parent.inference_depth + 1)
        redundant = exposures - len(roots)

        new_roots = roots - self.seen_roots
        self.seen_roots.update(roots)
        self.cycle_new_roots.update(new_roots)
        self.last_new_roots = frozenset(new_roots)
        self.nodes[message_id] = LineageNode(
            message_id=message_id,
            visible_message_id=visible_message_id or message_id,
            parent_message_ids=tuple(parent_message_ids),
            evidence_roots=frozenset(roots),
            inference_depth=depth,
        )
        return EpistemicEnvelope(
            actual_roots=tuple(sorted(roots)),
            derived_from=tuple(visible_parent_message_ids or parent_message_ids),
            inference_depth=depth,
            new_external_evidence=bool(new_roots),
            redundant_root_exposures=redundant,
        )

    def should_stop_after_cycle(self) -> bool:
        return not self.cycle_new_roots

    @property
    def independent_root_count(self) -> int:
        return len(self.seen_roots)

    def ancestry(self, message_id: str) -> list[str]:
        """All ancestor ids in topological order (oldest first), each once."""
        seen: set[str] = set()
        order: list[str] = []

        def visit(current_id: str) -> None:
            node = self.nodes.get(current_id)
            if node is None or current_id in seen:
                return
            seen.add(current_id)
            for parent_id in node.parent_message_ids:
                visit(parent_id)
            order.append(current_id)

        visit(message_id)
        return order
