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
- **EXP-003 v0.1** — frozen (tag `exp-003-protocol-v0.1`); a topology ladder (Gates 3A matched topologies, 3B diamond, 3C detached, 3D hives). See [experiments/EXP_003/README.md](experiments/EXP_003/README.md).
- **Gate 3A** — closed under the frozen EXP-003 v0.1 design (tag `exp-003-gate3a-closed-v0.1`): ring, solo, dyad and bounce on the same worlds, two pre-registered stages, 96 worlds archived and audited. Findings are recorded in [research/observations/EXP_003_gate_3a_observations_v0.1.md](research/observations/EXP_003_gate_3a_observations_v0.1.md).
- **Gate 3B** — closed under the frozen EXP-003 v0.1 design (tag `exp-003-gate3b-closed-v0.1`): the diamond fan-in with a two-root positive control, a probe-off arm and a probe-on solo control, two pre-registered stages, 72 worlds archived and audited, analysis rules committed before any value existed. Findings are recorded in [research/observations/EXP_003_gate_3b_observations_v0.1.md](research/observations/EXP_003_gate_3b_observations_v0.1.md).
- **Gate 3C** — closed under the frozen EXP-003 v0.1 design (tag `exp-003-gate3c-closed-v0.1`): the five Gate 3A and 3B shapes without re-grounding on the same worlds, with same-day re-grounded twins and a drift gauge in Set 001 and historical twins in Set 002, 168 worlds archived and audited, analysis rules committed before any value existed. Findings are recorded in [research/observations/EXP_003_gate_3c_observations_v0.1.md](research/observations/EXP_003_gate_3c_observations_v0.1.md).
- **Gate 3D** — prospective plan drafted; not frozen; no real-model calls made.

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

EXP-002 replication and audit are complete (Gate 2B). EXP-003 Gates 3A, 3B and 3C are closed.
Gate 3D (bridged hives) remains drafted and not frozen; its execution is deferred as a sequencing
preference, not for a scientific reason. Any gate runs only after its plan is frozen and its
manifests committed; no gate is redesigned after its results are seen.
