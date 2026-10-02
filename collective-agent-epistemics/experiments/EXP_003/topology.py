from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Firing:
    """One model call: `sender` fires and the same message goes to every receiver."""

    sender: str
    receivers: tuple[str, ...]


@dataclass(frozen=True)
class Topology:
    name: str
    agents: tuple[str, ...]
    seed_cycle: tuple[Firing, ...]
    recursive_cycle: tuple[Firing, ...]
    regrounding: bool
    primary_sources: tuple[str, ...]
    secondary_sources: tuple[str, ...]
    focal_agent: str
    description: str

    def edges(self) -> list[list[str]]:
        rows: list[list[str]] = []
        for firing in (*self.seed_cycle, *self.recursive_cycle):
            for receiver in firing.receivers:
                rows.append([firing.sender, receiver])
        return rows

    def firings_per_round(self) -> int:
        return len(self.recursive_cycle)

    def seed_firings(self) -> int:
        return len(self.seed_cycle)


# EXP-002 reference topology, reproduced here only so EXP-003 can be checked against it.
RING = Topology(
    name="ring",
    agents=("A", "B", "C"),
    seed_cycle=(Firing("A", ("B",)),),
    recursive_cycle=(Firing("B", ("C",)), Firing("C", ("A",)), Firing("A", ("B",))),
    regrounding=True,
    primary_sources=("A",),
    secondary_sources=(),
    focal_agent="C",
    description="EXP-002 linear ring A->B->C->A. No agent ever receives two inbound messages.",
)

# Rung 1. Two agents; B sends straight back to A. Every agent talks to the source every cycle.
DYAD = Topology(
    name="dyad",
    agents=("A", "B"),
    seed_cycle=(Firing("A", ("B",)),),
    recursive_cycle=(Firing("B", ("A",)), Firing("A", ("B",))),
    regrounding=True,
    primary_sources=("A",),
    secondary_sources=("B",),
    focal_agent="B",
    description="Dyad A<->B. Minimal interaction: one other mind transforms the message and returns it.",
)

DYAD_DETACHED = Topology(
    name="dyad_detached",
    agents=DYAD.agents,
    seed_cycle=DYAD.seed_cycle,
    recursive_cycle=DYAD.recursive_cycle,
    regrounding=False,
    primary_sources=DYAD.primary_sources,
    secondary_sources=DYAD.secondary_sources,
    focal_agent="B",
    description="Dyad with source detachment: A sees E1 at the seed firing only.",
)

# Rung 2 (Gate 3A primary). A->B->C then C->B->A. Same agents, calls and depth as the EXP-002 ring;
# the return path reverses instead of closing the loop. C never sends to A; B relays both ways.
BOUNCE = Topology(
    name="bounce",
    agents=("A", "B", "C"),
    seed_cycle=(Firing("A", ("B",)),),
    recursive_cycle=(
        Firing("B", ("C",)),
        Firing("C", ("B",)),
        Firing("B", ("A",)),
        Firing("A", ("B",)),
    ),
    regrounding=True,
    primary_sources=("A",),
    secondary_sources=("C",),
    focal_agent="C",
    description=(
        "Bounce A->B->C->B->A. C is an isolated end two hops from E1 that only ever talks to B; "
        "B relays in both directions and sees its own echo after two hops; A's echo returns after four."
    ),
)

BOUNCE_DETACHED = Topology(
    name="bounce_detached",
    agents=BOUNCE.agents,
    seed_cycle=BOUNCE.seed_cycle,
    recursive_cycle=BOUNCE.recursive_cycle,
    regrounding=False,
    primary_sources=BOUNCE.primary_sources,
    secondary_sources=BOUNCE.secondary_sources,
    focal_agent="C",
    description="Bounce with source detachment: A sees E1 at the seed firing only.",
)

# Rung 3 (Gate 3B). A holds E1 and re-observes it every time it fires. D receives from B and C.
DIAMOND = Topology(
    name="diamond",
    agents=("A", "B", "C", "D"),
    seed_cycle=(Firing("A", ("B", "C")),),
    recursive_cycle=(
        Firing("B", ("D",)),
        Firing("C", ("D",)),
        Firing("D", ("A",)),
        Firing("A", ("B", "C")),
    ),
    regrounding=True,
    primary_sources=("A",),
    secondary_sources=("C",),
    focal_agent="D",
    description=(
        "Fan-in diamond. A -> {B, C}; B -> D; C -> D; D -> A. D always receives two "
        "descendants of the same root set. A is re-grounded in its direct evidence on every firing."
    ),
)

# Gate 3B. Same graph, but A sees its direct evidence only on its first firing.
DIAMOND_DETACHED = Topology(
    name="diamond_detached",
    agents=DIAMOND.agents,
    seed_cycle=DIAMOND.seed_cycle,
    recursive_cycle=DIAMOND.recursive_cycle,
    regrounding=False,
    primary_sources=DIAMOND.primary_sources,
    secondary_sources=DIAMOND.secondary_sources,
    focal_agent="D",
    description="Fan-in diamond with source detachment: direct evidence is shown once, at the seed firing only.",
)

# Non-interaction control: one agent re-prompted with its own previous message.
SOLO = Topology(
    name="solo",
    agents=("A",),
    seed_cycle=(Firing("A", ("A",)),),
    recursive_cycle=(Firing("A", ("A",)),),
    regrounding=True,
    primary_sources=("A",),
    secondary_sources=(),
    focal_agent="A",
    description="Non-interaction control. A re-reads its own previous message plus its direct evidence.",
)

SOLO_DETACHED = Topology(
    name="solo_detached",
    agents=SOLO.agents,
    seed_cycle=SOLO.seed_cycle,
    recursive_cycle=SOLO.recursive_cycle,
    regrounding=False,
    primary_sources=("A",),
    secondary_sources=(),
    focal_agent="A",
    description="Non-interaction control without re-grounding: A sees its evidence once, then only its own prior message.",
)

# Gate 3C. Two diamonds whose D agents cross-feed the other hive's A.
HIVES_BRIDGED = Topology(
    name="hives_bridged",
    agents=("A1", "B1", "C1", "D1", "A2", "B2", "C2", "D2"),
    seed_cycle=(Firing("A1", ("B1", "C1")), Firing("A2", ("B2", "C2"))),
    recursive_cycle=(
        Firing("B1", ("D1",)),
        Firing("C1", ("D1",)),
        Firing("B2", ("D2",)),
        Firing("C2", ("D2",)),
        Firing("D1", ("A1", "A2")),
        Firing("D2", ("A2", "A1")),
        Firing("A1", ("B1", "C1")),
        Firing("A2", ("B2", "C2")),
    ),
    regrounding=True,
    primary_sources=("A1",),
    secondary_sources=("A2",),
    focal_agent="A1",
    description=(
        "Two diamonds bridged at the D agents: D1 -> {A1, A2}, D2 -> {A2, A1}. Each A receives one "
        "inbound from its own hive and one from the other hive every cycle."
    ),
)

RING_DETACHED = Topology(
    name="ring_detached",
    agents=RING.agents,
    seed_cycle=RING.seed_cycle,
    recursive_cycle=RING.recursive_cycle,
    regrounding=False,
    primary_sources=RING.primary_sources,
    secondary_sources=RING.secondary_sources,
    focal_agent="C",
    description="EXP-002 ring with source detachment: A sees E1 at the seed firing only.",
)

# Gate 3D control: two diamonds that never exchange messages. Pairs with hives_bridged so the
# bridge is the only difference. Under a shared root this is also a stochastic replicate pair.
HIVES_ISOLATED = Topology(
    name="hives_isolated",
    agents=HIVES_BRIDGED.agents,
    seed_cycle=HIVES_BRIDGED.seed_cycle,
    recursive_cycle=(
        Firing("B1", ("D1",)),
        Firing("C1", ("D1",)),
        Firing("B2", ("D2",)),
        Firing("C2", ("D2",)),
        Firing("D1", ("A1",)),
        Firing("D2", ("A2",)),
        Firing("A1", ("B1", "C1")),
        Firing("A2", ("B2", "C2")),
    ),
    regrounding=True,
    primary_sources=HIVES_BRIDGED.primary_sources,
    secondary_sources=HIVES_BRIDGED.secondary_sources,
    focal_agent="A1",
    description="Two diamonds with no bridge: D1 -> A1 and D2 -> A2 only. Same firings as hives_bridged minus the cross-hive edges.",
)

TOPOLOGIES: dict[str, Topology] = {
    t.name: t
    for t in (
        RING, RING_DETACHED, SOLO, SOLO_DETACHED, DYAD, DYAD_DETACHED, BOUNCE, BOUNCE_DETACHED,
        DIAMOND, DIAMOND_DETACHED, HIVES_BRIDGED, HIVES_ISOLATED,
    )
}

# Rounds that bring every topology to inference depth 12, so rungs differ in structure only.
ROUNDS_FOR_DEPTH_12: dict[str, int] = {
    "ring": 4, "ring_detached": 4, "solo": 12, "solo_detached": 12, "dyad": 6, "dyad_detached": 6,
    "bounce": 3, "bounce_detached": 3, "diamond": 4, "diamond_detached": 4,
    "hives_bridged": 4, "hives_isolated": 4,
}


def get_topology(name: str) -> Topology:
    try:
        return TOPOLOGIES[name]
    except KeyError as exc:
        raise ValueError(f"unknown topology: {name}; known: {', '.join(sorted(TOPOLOGIES))}") from exc
