# EXP-002 Replication Set 002 Plan v0.1

## Status

Pre-registered descriptive analysis plan. Set 002 is planned and has not been executed.

## Frozen configuration

Set 002 uses the exact EXP-002 v0.1 configuration:

```text
experiment: EXP-002
protocol: v0.1
model: gpt-5.6-sol
reasoning_effort: medium
execution_policy: paired
trials: 1
rounds: 4
seed: 42
world: EXP_002_W01
```

Ten runs are planned as `rep_001` through `rep_010` under:

```text
experiments/EXP_002/results/archive/replication_sets/replication_set_002/
```

No protocol, runtime, prompt, metric, model, reasoning effort, seed, round count, or execution policy change is introduced.

## Primary outcomes

The primary EXP-002 question remains:

> When recursive communication continues without new independent evidence, what happens to epistemic outputs, and how does this differ across FREE, LINEAGE, and MACRO?

Primary metrics remain the frozen EXP-002 metrics:

- answer trajectory;
- confidence trajectory;
- `P(A)` trajectory;
- Brier trajectory;
- accuracy;
- actual evidence roots;
- new independent evidence;
- inference depth;
- `P(A)` changes without new independent evidence;
- FREE versus LINEAGE behavior;
- MACRO stopping behavior.

## Secondary descriptive outcomes

For every archived run, derive these from raw events only. They are not runtime metrics:

- run-level presence of `DSCD-STRICT`;
- run-level presence of any numerical LINEAGE discount;
- run-level FREE numerical drift;
- number of strict events;
- actor producing each discount, using `event.sender`;
- depth of first strict event;
- Agent A direct-observation events;
- return-to-`.70` behavior after downstream discount;
- FREE explicit dependency recognition.

Use the locked DSCD v0.1 transition rule: baseline `Mxx-1` in the same condition, certainty `abs(P(A)-0.5)`, and criterion D evaluated only from the current visible model message. Do not use M04 as the event-level DSCD baseline.

## Reporting and interpretation

Archive every run before the next execution and record SHA-256 hashes. Report all runs, including stable runs. Do not define success around M09 or any single Pilot 002 trajectory. Do not merge historical Pilot 002 into the formal set 002 denominator. Do not perform significance tests in the run audit. These observations do not establish causality or generalization across worlds, models, or configurations.
