# EXP-003 Gate 3B Prospective Plan v0.1: Diamond (first fan-in)

## Status

**PLAN DRAFT / NOT FROZEN / NOT EXECUTED**

Gate 3B may be frozen only after Gate 3A is closed. It adds the fourth agent.

## Scientific anchors (to fill at freeze)

- Gate 3A closure checkpoint: `<sha>`
- Frozen EXP-003 runtime: `<sha>` (unchanged from Gate 3A unless a versioned protocol change is recorded)
- Model: `gpt-5.6-sol`, effort `medium`, paired, reliability `0.70`
- Rounds: `4` (diamond), `12` (solo)
- Probe: **on** except in the probe-off arm

## Gate 3B question

> When an agent with no evidence receives two messages descended from the same root through two different agents, does its reported P(A) exceed the single-root reference, does it report more than one distinct source, and does the lineage envelope change either, without suppressing evidence that really is independent?

This is the hypothesis's central step. No three-agent shape can produce it: in the ring and the bounce every agent receives exactly one inbound message.

## What changes versus Gate 3A

One thing: D is added. A sends to B and C; B and C both send to D; D sends to A. The probe is switched on because D's reported source count is a primary outcome here; the probe-off arm measures what switching it on costs.

## The matrix

The decisive comparison is a two-by-two. Rows are arms; the FREE and LINEAGE columns come from paired execution inside each arm.

| D receives | Actual roots | Condition | Reference at D | What it tests |
|---|---|---|---|---|
| B and C | 1 (E1 via both) | FREE | `.70` | does D mistake redundancy for independence |
| B and C | 1 (E1 via both) | LINEAGE | `.70` | does the envelope correct the dependency |
| B and C | 2 (E1 via B, E2 via C) | FREE | `.845` agreeing, `.50` conflicting | positive control: genuine corroboration raises D toward the two-root reference |
| B and C | 2 (E1 via B, E2 via C) | LINEAGE | same | the envelope must not suppress genuinely independent evidence |

The result that would matter most: LINEAGE holds `.70` with one root **and** rises toward `.845` with two. The opposite failure, LINEAGE flattening both, means the lineage mechanism over-corrects, which is equally important to know.

## Stages

**Set 001, discovery.** Arms 1 to 4 below. **Set 002, replication.** Arms 1 and 2 on new worlds, same size, pre-registered, run regardless of Set 001 and only after it closes, reported separately.

## Arms

### Arm 1: `diamond_set_001` (primary)

- Topology `diamond`, root mode `single`, 12 prospectively unfiltered worlds, probe on. D receives from B and C every cycle: two inbound messages, one root.

### Arm 2: `dual_root_set_001` (positive control)

- Topology `diamond`, root mode `dual`: E1 held by A, E2 held by C, independent draws. Stratified: **2 worlds per `truth/E1/E2` cell, 8 cells, 16 worlds**, so the agreeing stratum and the conflicting stratum each have 8 worlds.

### Arm 3: `solo_control_set_003`

- Topology `solo`, rounds 12, probe on, the Arm 1 seeds. The Gate 3A solo controls were probe-off; this one matches Arm 1's probe setting.

### Arm 4: `probe_off_set_001` (reactivity check)

- Topology `diamond`, root mode `single`, probe off, the first 4 Arm 1 worlds in execution order. If probe-off excess at D differs materially from probe-on excess in the same worlds, the probe is reactive and is reported as a manipulation in every later gate.

### Set 002: `diamond_set_002`, `dual_root_set_002`

- Same design as Arms 1 and 2 on 12 and 16 new worlds.

## Primary outcomes

The Gate 3A outcome family plus reported distinct source count and false independent support (FIS). Focal: D at every firing (P(A), excess, FIS); A at every post-seed firing; per-agent final P(A) and excess range; the four matrix cells by world.

## Pre-registered directional expectations

| Id | Expectation | Would be contradicted by |
|---|---|---|
| E1 | FREE D shows positive excess in at least some Arm 1 worlds | FREE D excess within `.01` of zero in all 12 worlds |
| E2 | LINEAGE D excess is not greater than FREE D excess in the same world | LINEAGE D exceeds FREE D in a majority of worlds |
| E3 | Positive excess at D co-occurs with FIS > 0 | Excess without FIS, or FIS without excess, dominates |
| E4 | Inbound agent-as-source wording precedes positive excess more often than clean wording does | No association |
| E5 | Arm 2 D approaches the two-root reference under both conditions; LINEAGE does not hold it at the one-root value | D stays at `.70` with two roots (under-combination or over-correction) or exceeds `.845` (over-combination) |
| E6 | Arm 4 excess at D is within `.02` of Arm 1 in the same worlds | A larger gap: the probe is reactive |
| E7 | Set 002 reproduces the Set 001 direction in every matrix cell | A reversed cell |

If E1 fails, fan-in alone with one root does not produce double counting in this model at this depth, which narrows the hypothesis again and is reported as such.

## Seeds and accounting

Anchor `<gate3a closure sha>|exp-003-protocol-v0.1|GATE_3B_PLAN_v0.1`. Exclusions: `42`, the 20 Gate 2B seeds, all Gate 3A seeds; Set 002 also excludes every Set 001 seed. Arm 1 via `candidate_seed("G3B_GEN001", ordinal, nonce)`, unfiltered; Arm 2 via a stratified scan `candidate_seed("G3B_DUAL001", scan_index, 0)` with `--per-cell 2` over the 8 `truth/E1/E2` cells; Arms 3 and 4 inherit Arm 1 seeds; Set 002 uses labels `G3B_GEN002` and `G3B_DUAL002`. Manifests named in `GATE_3B_PLAN_v0.1.json`.

| Stage | Arm | Worlds | Calls per world | Calls |
|---|---|---:|---:|---:|
| Set 001 | diamond | 12 | 33 | 396 |
| Set 001 | dual-root | 16 | 33 | 528 |
| Set 001 | solo control | 12 | 25 | 300 |
| Set 001 | probe-off | 4 | 33 | 132 |
| Set 002 | diamond | 12 | 33 | 396 |
| Set 002 | dual-root | 16 | 33 | 528 |
| **Total** | | | | **2280** (1356 in Set 001) |

## Execution, archival, analysis, closure

Gate 3A rules. Archive under `results/archive/gate_3b/`. Report each arm and stage separately, first against the Gate 3A bounce (same model, one added agent) and then against the Gate 3A ring. Closure as Gate 3A. A gate is not redesigned after its results are seen.
