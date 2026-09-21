# EXP-002 Protocol Lock v0.1

**Protocol version:** EXP-002 v0.1
**Status:** FROZEN FOR REPLICATION

This document records the implementation actually used for real-model Pilot 002. It does not alter the implementation.

## Research question

Does recursive multi-agent communication alter confidence, calibration, or accuracy when no new independent external evidence enters the network?

## Conditions

- **FREE:** ordinary natural-language messages; no structured epistemic envelope is exposed to agents.
- **LINEAGE:** messages expose structured lineage metadata; no stopping rule is applied.
- **MACRO:** messages expose the same lineage metadata as LINEAGE; the harness stops after a complete cycle with no new independent roots.

The condition comparison is FREE vs LINEAGE vs MACRO. Conditions use the same frozen `World` object for each trial.

## Topology and world semantics

The message topology is the sequential cycle `A -> B -> C -> A -> B`, repeated once per recursive cycle after the seed message `A -> B`. The current W01 world has one independent external evidence root `E1`, assigned to Agent A. With seed `42`, the generated world is `EXP_002_W01`, truth `A`, observed state `A`, source `sensor_1`, and reported reliability `0.70`.

World generation draws truth and sensor observation from a seeded local RNG. Recursive messages do not create external evidence roots. Agent A receives its direct observation again whenever A participates; this is periodic re-grounding in E1, not new independent evidence.

## Runtime semantics

- The seed response is shared across conditions under paired execution.
- FREE and LINEAGE make independent post-seed model calls.
- MACRO reuses the LINEAGE responses by visible message position; it makes no independent post-seed model calls.
- For Pilot 002, the paired accounting was one shared seed call, 12 FREE post-seed calls, 12 LINEAGE post-seed calls, and 0 independent MACRO calls: 25 actual calls and 4 reused responses.
- `rounds` is the maximum number of recursive cycles after the seed cycle.
- FREE and LINEAGE exhaust the maximum when no stopping rule applies.
- MACRO evaluates its stopping criterion after each complete recursive cycle. It stops when that cycle adds no new independent root. The explicit summary state is `macro_stop_triggered`.

## Lineage semantics

The harness maintains hidden actual lineage. Each message inherits its parent's actual roots and increments inference depth. The hidden graph tracks the set of seen roots and roots newly seen during the current cycle. In LINEAGE and MACRO, model-visible messages include the structured envelope; FREE messages do not. Model output and agent-reported information remain separate from hidden actual lineage.

## Metrics

Event metrics include:

- accuracy;
- reported confidence;
- `P(A)` derived from answer and confidence;
- Brier score;
- independent evidence root count;
- inference depth;
- new independent evidence;
- `P(A)` delta without new independent evidence.

Summaries additionally record trajectories, completed cycles, stopping reason, and `macro_stop_triggered`.

## Frozen implementation identity

The implementation used for Pilot 002 is commit:

`7e9aed1b7093baae10ae30f27e0b6a2b932f92f5`

The immutable protocol tag `exp-002-protocol-v0.1` points to that exact commit. Documentation added after the run records the implementation; it does not change the frozen code.
