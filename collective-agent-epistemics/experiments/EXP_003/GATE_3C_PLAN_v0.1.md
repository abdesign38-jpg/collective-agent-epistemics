# EXP-003 Gate 3C Prospective Plan v0.1: Source Detachment

## Status

**PLAN DRAFT / NOT FROZEN / NOT EXECUTED**

Gate 3C may be frozen only after Gates 3A and 3B are closed. It reuses their Set 001 worlds so that the only difference is re-grounding.

## Gate 3C question

> When the source holder sees its evidence once and thereafter only receives relays, does deviation from the reference compound across cycles instead of resetting, and does the lineage envelope change the slope?

## Why this gate exists

EXP-002, Gate 3A and Gate 3B all re-ground A in E1 at every firing. In the ring, A returned to the reference in 24 of 24 LINEAGE runs with a deviation; the audits did not claim the direct evidence caused that. Gate 3C removes the reset. If transient deviations become persistent or cumulative, periodic direct evidence was the stabilizer. If they do not, the model's own behavior is.

## Arms

Every Gate 3A Set 001 shape and the Gate 3B diamond, each paired world by world with its re-grounded execution:

| Arm | Topology | Seeds | Rounds | Probe | Pairs with |
|---|---|---|---|---|---|
| `ring_detached_set_001` | `ring_detached` | 3A `ring_control_set_001` | 4 | off | 3A ring |
| `solo_detached_set_001` | `solo_detached` | same | 12 | off | 3A solo |
| `dyad_detached_set_001` | `dyad_detached` | same | 6 | off | 3A dyad |
| `bounce_detached_set_001` | `bounce_detached` | same | 3 | off | 3A bounce |
| `diamond_detached_set_001` | `diamond_detached` | 3B `diamond_set_001` | 4 | on | 3B diamond |

Each arm's partner is the re-grounded execution of the identical world, so every comparison is a per-world, per-event paired difference with exactly one factor changed (`regrounding`, which the ledger reports together with the `topology` name).

## Primary outcomes

The partner gate's outcome family, plus: cycle-over-cycle excess at each agent; A's trajectory after its single direct observation; erosion of sensor id and reliability in A's own messages by depth; paired difference with the partner set at matched event positions.

## Pre-registered directional expectations

| Id | Expectation | Would be contradicted by |
|---|---|---|
| E1 | Without re-grounding, A's messages lose the sensor id and reliability faster with depth than in the partner set | Equal or slower erosion |
| E2 | Excess (or discount) magnitude at the far agent (C or D) is larger at the last cycle than at the first | No compounding |
| E3 | Detached and re-grounded trajectories of the same world diverge more with depth | They stay within `.01` throughout |
| E4 | Solo detached shows no excess | Solo drift |
| E5 | The detachment effect, if any, is ordered across the ladder the same way the Gate 3A discount rates were | A different ordering |

## Seeds, accounting, archival

No new derivation; anchor `<gate3b closure sha>|exp-003-protocol-v0.1|GATE_3C_PLAN_v0.1` for order keys only. Manifests named in `GATE_3C_PLAN_v0.1.json`.

| Arm | Worlds | Calls per world | Calls |
|---|---:|---:|---:|
| ring detached | 12 | 25 | 300 |
| solo detached | 12 | 25 | 300 |
| dyad detached | 12 | 25 | 300 |
| bounce detached | 12 | 25 | 300 |
| diamond detached | 12 | 33 | 396 |
| **Total** | | | **1596** |

Archive under `results/archive/gate_3c/`. Gate 3A rules for execution, retries, analysis and closure, with the Gate 3A and 3B closure SHAs recorded before freeze. A gate is not redesigned after its results are seen.
