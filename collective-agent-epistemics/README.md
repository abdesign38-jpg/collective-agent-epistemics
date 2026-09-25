# Collective Agent Epistemics

A minimal research harness for studying whether recursive multi-agent communication
changes epistemic lineage, calibration, confidence, or convergence without a
corresponding increase in independent evidence.

## Research question

> As inference depth and inter-agent recursion increase without new independent evidence,
> what happens to epistemic lineage, calibration, confidence, and convergence?

The project preserves a broad research frame rather than treating any single pilot
trajectory as confirmation. See the [research framework](research/framework_v0.1.md),
[historical hypothesis](research/hypothesis_v0.1.md), [protocol lock](experiments/EXP_002/PROTOCOL_LOCK_v0.1.md),
and [replication plan](experiments/EXP_002/REPLICATION_PLAN_v0.1.md).

## Current project state

- **EXP-001** — complete.
- **EXP-002 v0.1** — frozen.
- **Gate 2A** — closed under the frozen EXP-002 v0.1 design.
- **Gate 2B** — closed under the frozen EXP-002 v0.1 design.
- **Gate 2C** — future / not yet prospectively designed.
- **Gate 3** — future.

This documentation reflects the current repository state as committed. It does not introduce new scientific conclusions beyond the preserved gate closures and their audit artifacts.

## EXP-001 conditions

1. **free** — agents exchange ordinary claims and may naively treat received claims as
   new support.
2. **lineage** — claims carry explicit evidence roots and derivation metadata.
3. **macro** — the same lineage-aware claims are tracked by a macro layer that can stop
   recursion when a full cycle adds no independent evidence.

All three conditions use the same synthetic worlds and same agent topology. The worlds include a misleading-evidence control so the harness can expose confidently-wrong amplification, not only confidence growth on correct trials.

## EXP-002 conditions

EXP-002 compares FREE, LINEAGE, and MACRO under a shared seed and paired execution.
The real-model pilot and its forensic audit are exploratory, not confirmatory evidence.
Preserved runs live under `experiments/EXP_002/results/archive/`; see the
[results contract](experiments/EXP_002/results/README.md).

## Visualization boundary

Epistemic Hive is a downstream representation layer within the monorepo and is intentionally separated from the scientific evidence tree.

```text
collective-agent-epistemics/
├── experiments/
├── research/
├── schemas/
├── src/
├── tests/
└── visualization/
    └── epistemic-hive/
```

The visualization may read committed scientific artifacts for replay purposes, but it does not generate or validate experimental evidence.

## Quick start

Requires Python 3.10+ and no external packages.

```bash
python -m experiments.EXP_001.run --world all --rounds 4
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

Outputs are written to:

```text
experiments/EXP_001/results/
```

including:

- `summary.csv`
- `events.jsonl`
- `run_metadata.json`

## Important methodological note

The built-in synthetic agent intentionally uses simple, explicit update rules so the
harness can be audited. A result from this synthetic agent does **not** validate the
research hypothesis. It validates that we can measure:

- actual evidence lineage
- perceived lineage
- false independent support
- inference depth
- confidence change without new independent evidence
- macro stopping behavior

The next research phase is replication of the frozen EXP-002 configuration. Future
worlds, models, and architecture interventions remain gated until that replication
and audit are complete.
