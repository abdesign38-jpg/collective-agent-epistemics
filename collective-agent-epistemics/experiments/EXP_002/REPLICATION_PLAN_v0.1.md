# EXP-002 Replication Plan v0.1

## Status

This plan must be committed before any replication is run. No replication is included in this document.

## Frozen configuration

Five exact stochastic replications of EXP-002 v0.1:

```text
model: gpt-5.6-sol
reasoning_effort: medium
execution_policy: paired
trials: 1
rounds: 4
seed: 42
world: EXP_002_W01
```

The replication set uses the same frozen protocol, prompts, topology, world generation, metrics, and stopping semantics. Results belong under:

```text
experiments/EXP_002/results/archive/rep_001_<NNN>_seed42_r4/
```

## Primary outcomes

Preserve the original EXP-002 outcome set:

- answer trajectory;
- confidence trajectory;
- `P(A)` trajectory;
- Brier trajectory;
- accuracy;
- independent evidence roots;
- inference depth;
- `P(A)` changes without new independent evidence;
- FREE versus LINEAGE behavior;
- MACRO stopping behavior.

The primary replication question is whether recursive communication changes epistemic outputs when independent evidence remains fixed, and how that differs by communication architecture.

The primary question is **not** whether M09 happens again and **not** whether depth discounting reproduces.

## Secondary exploratory observations

Track separately:

- transient confidence deflation;
- confidence inflation;
- answer flips;
- FREE inferred dependency;
- depth-sensitive language;
- Agent A re-grounding behavior;
- message-content transformations.

These are secondary because they were identified after Pilot 002. No secondary observation may redefine replication success.

## Interpretation

Do not define replication success around a single Pilot 002 trajectory. Every run must be reported, including completely stable runs. Pilot and replication outputs are exploratory unless a later protocol explicitly establishes otherwise.
