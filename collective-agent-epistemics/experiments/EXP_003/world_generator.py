from __future__ import annotations

import random

from .models import Evidence, State, World
from .topology import Topology, get_topology

ROOT_MODES = ("single", "shared", "dual")


class WorldGenerator:
    """Generate reproducible worlds for a given topology and root mode.

    single: one sensor E1, held by the topology's primary source agents.
    shared: one sensor E1, held by primary and secondary source agents (same physical root).
    dual:   two sensors E1 (primary) and E2 (secondary), each an independent draw.
    """

    def __init__(
        self,
        seed: int,
        topology: str | Topology = "diamond",
        root_mode: str = "single",
        sensor_reliability: float = 0.70,
    ) -> None:
        if not 0.0 <= sensor_reliability <= 1.0:
            raise ValueError("sensor_reliability must be between 0 and 1")
        if root_mode not in ROOT_MODES:
            raise ValueError(f"root_mode must be one of {ROOT_MODES}")
        self.seed = seed
        self.topology = topology if isinstance(topology, Topology) else get_topology(topology)
        self.root_mode = root_mode
        self.sensor_reliability = sensor_reliability
        if root_mode in ("shared", "dual") and not self.topology.secondary_sources:
            raise ValueError(
                f"root_mode {root_mode} requires a topology with secondary sources; "
                f"{self.topology.name} has none"
            )

    def generate(self, world_id: str | None = None, seed: int | None = None) -> World:
        world_seed = self.seed if seed is None else seed
        rng = random.Random(world_seed)
        truth: State = rng.choice(("A", "B"))
        # The first draw is always E1 so that single/shared/dual worlds with the same seed
        # share truth and E1; E2 is a second, independent draw from the same stream.
        e1_state = _draw(rng, truth, self.sensor_reliability)
        topology = self.topology
        if self.root_mode == "single":
            holders = topology.primary_sources
            evidence = (_evidence("E1", e1_state, "sensor_1", self.sensor_reliability, holders),)
        elif self.root_mode == "shared":
            holders = (*topology.primary_sources, *topology.secondary_sources)
            evidence = (_evidence("E1", e1_state, "sensor_1", self.sensor_reliability, holders),)
        else:
            e2_state = _draw(rng, truth, self.sensor_reliability)
            evidence = (
                _evidence("E1", e1_state, "sensor_1", self.sensor_reliability, topology.primary_sources),
                _evidence("E2", e2_state, "sensor_2", self.sensor_reliability, topology.secondary_sources),
            )
        return World(
            world_id=world_id or f"EXP_003_W_{world_seed}",
            seed=world_seed,
            truth=truth,
            evidence=evidence,
            topology=topology.name,
            root_mode=self.root_mode,
        )

    def generate_many(self, count: int) -> list[World]:
        return [
            self.generate(world_id=f"EXP_003_W{i + 1:02d}", seed=self.seed + i)
            for i in range(count)
        ]


def _draw(rng: random.Random, truth: State, reliability: float) -> State:
    return truth if rng.random() < reliability else _opposite(truth)


def _evidence(
    evidence_id: str, state: State, source: str, reliability: float, holders: tuple[str, ...]
) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        observed_state=state,
        source=source,
        reliability=reliability,
        assigned_to=tuple(holders),
    )


def _opposite(state: State) -> State:
    return "B" if state == "A" else "A"


def generate_world(
    seed: int,
    topology: str = "diamond",
    root_mode: str = "single",
    world_id: str | None = None,
    sensor_reliability: float = 0.70,
) -> World:
    return WorldGenerator(seed, topology, root_mode, sensor_reliability).generate(world_id=world_id)


def world_cell(world: World) -> str:
    """Truth/observation cell label. single/shared: T/E1. dual: T/E1/E2."""
    parts = [world.truth, *(e.observed_state for e in world.evidence)]
    return "/".join(parts)


def alignment(world: World) -> str:
    """aligned if every root agrees with truth, misleading if none does, mixed otherwise."""
    agree = [e.observed_state == world.truth for e in world.evidence]
    if all(agree):
        return "aligned"
    if not any(agree):
        return "misleading"
    return "mixed"
