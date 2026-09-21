# Next Steps

## Gate 0 — Harness validation — complete

EXP-001 instrumentation, lineage behavior, metrics, and tests are complete.

## Gate 1 — Real-model adapter — complete

EXP-002 v0.1 has a real-model adapter, paired execution, structured outputs, and a
frozen protocol record. Pilot 002 has been audited as exploratory evidence.

## Gate 2A — Exact same-world stochastic replication — complete

Gate 2A is closed at scientific checkpoint:

`de62984adc44566b513545feaf2d61fcc229e71c`

The formal same-world result covers 15 runs under the frozen W01 configuration.
Do not reopen Gate 2A unless a genuine data-integrity or protocol-invalidating issue is discovered.

## Gate 2B — Multiple worlds / misleading evidence — plan frozen / not yet executed

The prospective Gate 2B design is frozen in:

[GATE_2B_PLAN_v0.1.md](experiments/EXP_002/GATE_2B_PLAN_v0.1.md)

Before any Gate 2B real-model call, materialize and commit the exact deterministic
world manifest defined by the plan. Gate 2B changes world/evidence realization only;
the frozen EXP-002 runtime and protocol remain unchanged.

## Future gates

- **Gate 2C — Broader model/config replication** — not yet executed.
- **Gate 3 — Architecture intervention evaluation** — not yet executed.

Do not promote secondary Gate 2A or Gate 2B observations into new causal interventions
before the current gate is completed and audited.
