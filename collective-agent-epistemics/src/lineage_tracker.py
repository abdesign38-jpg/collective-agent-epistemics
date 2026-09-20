from dataclasses import dataclass, field

@dataclass
class MacroLineageTracker:
    seen_roots: set[str] = field(default_factory=set)
    cycle_new_roots: set[str] = field(default_factory=set)

    def observe_claim(self, roots: set[str]) -> int:
        new_roots = set(roots) - self.seen_roots
        self.seen_roots.update(roots)
        self.cycle_new_roots.update(new_roots)
        return len(new_roots)

    def start_cycle(self) -> None:
        self.cycle_new_roots = set()

    def should_stop_after_cycle(self) -> bool:
        return len(self.cycle_new_roots) == 0
