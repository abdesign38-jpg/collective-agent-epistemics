from __future__ import annotations

import random

from .models import Evidence, State, World


class WorldGenerator:
    """Generate reproducible worlds before any condition is executed."""

    def __init__(self, seed: int, sensor_reliability: float = 0.70) -> None:
        if not 0.0 <= sensor_reliability <= 1.0:
            raise ValueError("sensor_reliability must be between 0 and 1")
        self.seed = seed
        self.sensor_reliability = sensor_reliability

    def generate(self, world_id: str | None = None, seed: int | None = None) -> World:
        world_seed = self.seed if seed is None else seed
        rng = random.Random(world_seed)
        truth: State = rng.choice(("A", "B"))
        observed_state: State = truth if rng.random() < self.sensor_reliability else _opposite(truth)
        return World(
            world_id=world_id or f"EXP_002_W_{world_seed}",
            seed=world_seed,
            truth=truth,
            evidence=(
                Evidence(
                    evidence_id="E1",
                    observed_state=observed_state,
                    source="sensor_1",
                    reliability=self.sensor_reliability,
                    assigned_to="A",
                ),
            ),
        )

    def generate_many(self, count: int) -> list[World]:
        return [
            self.generate(world_id=f"EXP_002_W{i + 1:02d}", seed=self.seed + i)
            for i in range(count)
        ]


def _opposite(state: State) -> State:
    return "B" if state == "A" else "A"


def generate_world(seed: int, world_id: str | None = None, sensor_reliability: float = 0.70) -> World:
    return WorldGenerator(seed, sensor_reliability).generate(world_id=world_id)
