# EXP-003 Gate 3C Prospective Plan v0.1: Source Detachment

## Status

**FROZEN.** Anchors filled and JSON twin set to `FROZEN` in the freeze commits (anchor fill afa05a8fd4669567991cc70fa4763b328cb69888; this status flip names that commit as `plan_freeze_commit`). Gates 3A and 3B are closed (`exp-003-gate3a-closed-v0.1`, `exp-003-gate3b-closed-v0.1`). No Gate 3C real-model call had been made before this commit. It reuses their Set 001 and Set 002 worlds so that the only difference between a detached execution and its twin is re-grounding. This plan was amended before freeze under the Gate 3C scientific contract of 2026-11-01 (arms, stages, expectations and boundaries); the intervention is unchanged from the original draft.

## Gate 3C question

> When the source holder sees its evidence once and thereafter only receives relays, does deviation from the reference persist, compound, or otherwise change across cycles instead of resetting, and does the lineage envelope change that, in each of five network shapes?

## Why this gate exists

EXP-002, Gate 3A and Gate 3B all re-ground A in E1 at every firing. In the ring, A returned to the reference in 24 of 24 LINEAGE runs with a deviation; the audits did not claim the direct evidence caused that. Gate 3B found origin inflation under LINEAGE in a fourth topology, with the probe showing a source miscount at exactly those firings; it did not establish why. Gate 3C removes the reset. If transient deviations become persistent or cumulative, periodic direct evidence was the stabilizer. If they do not, the model's own behavior is. And if origin inflation under LINEAGE occurs without the direct observation in the prompt, the strict claim that it requires co-presence of observation and returned lineage (H1) is contradicted.

## Two hypotheses, one of which this gate addresses

- **H1, direct-observation co-presence (strict necessity):** origin inflation under LINEAGE requires the direct observation and the returned lineage to be in the same prompt. Gate 3C manipulates the presence of the direct observation and can contradict H1.
- **H2, source-identity equivalence:** an agent treats differently represented descendants of one evidence item as independent sources. Gate 3C does not manipulate representation and makes no claim about H2.

## Intervention

`regrounding = False`: with re-grounding off, an agent's direct observation is shown at its first firing only; every later firing of that agent reads `Direct observation: none` (frozen runtime, `run.py`). Messages, envelopes, probe setting, rounds, depth and the stopping rule are unchanged.

## Arms

Set 001: the five detached shapes on the Gate 3A ring Set 001 worlds (ring, solo, dyad, bounce) and the Gate 3B diamond Set 001 worlds (diamond), plus contemporary re-grounded twins of the four Gate 3A shapes on the same worlds. Set 002: the five detached shapes on the Gate 3A ring Set 002 and Gate 3B diamond Set 002 worlds, paired with the archived re-grounded executions.

| Stage | Arm | Topology | Probe | Rounds | Worlds | Seeds inherited from | Pairs with |
|---|---|---|---|---:|---:|---|---|
| set_001 | `ring_detached_set_001` | `ring_detached` | off | 4 | 12 | 3A `ring_control_set_001` | `ring_contemporary_set_001` |
| set_001 | `solo_detached_set_001` | `solo_detached` | off | 12 | 12 | same | `solo_contemporary_set_001` |
| set_001 | `dyad_detached_set_001` | `dyad_detached` | off | 6 | 12 | same | `dyad_contemporary_set_001` |
| set_001 | `bounce_detached_set_001` | `bounce_detached` | off | 3 | 12 | same | `bounce_contemporary_set_001` |
| set_001 | `diamond_detached_set_001` | `diamond_detached` | on | 4 | 12 | 3B `diamond_set_001` | 3B `diamond_set_001` (archived; temporal gap recorded) |
| set_001 | `ring_contemporary_set_001` | `ring` | off | 4 | 12 | 3A `ring_control_set_001` | control; also the drift gauge against 3A `ring_control_set_001` |
| set_001 | `solo_contemporary_set_001` | `solo` | off | 12 | 12 | same | control |
| set_001 | `dyad_contemporary_set_001` | `dyad` | off | 6 | 12 | same | control |
| set_001 | `bounce_contemporary_set_001` | `bounce` | off | 3 | 12 | same | control |
| set_002 | `ring_detached_set_002` | `ring_detached` | off | 4 | 12 | 3A `ring_control_set_002` | 3A `ring_control_set_002` (archived, historical) |
| set_002 | `solo_detached_set_002` | `solo_detached` | off | 12 | 12 | same | 3A `solo_control_set_002` (archived, historical) |
| set_002 | `dyad_detached_set_002` | `dyad_detached` | off | 6 | 12 | same | 3A `dyad_set_002` (archived, historical) |
| set_002 | `bounce_detached_set_002` | `bounce_detached` | off | 3 | 12 | same | 3A `bounce_set_002` (archived, historical) |
| set_002 | `diamond_detached_set_002` | `diamond_detached` | on | 4 | 12 | 3B `diamond_set_002` | 3B `diamond_set_002` (archived, historical) |

Probe settings are matched within every pair and never compared across pairs. The seed firing of a world has an identical prompt in every arm of that world; detached and twin executions sample it separately, so seed-firing differences measure sampling variance, not detachment (contract comment C1).

## Primary outcomes

Within-agent trajectories (each agent's own successive firings: P(A), certainty excess, reported distinct source count and false independent support where probed). Paired differences detached minus twin at matched visible message ids, in certainty excess against each event's own reference. Far-agent compounding (first versus last cycle). Origin behavior after lineage return under LINEAGE and FREE. Solo null. Drift gauge (contemporary ring against the archived Gate 3A ring on the same worlds). Baseline comparability at the seed firing (C1). Secondary: literal provenance retention by depth and relay position (markers measure wording, not meaning); return-message provenance at the origin; Set 002 paired differences (historical controls, qualified); MACRO stopping boundary.

## Pre-registered directional expectations

Mechanical rules, denominators, tie handling and traces are in `GATE_3C_PRIMARY_OUTCOME_AUDIT_SPEC_v0.1.md`, committed before any call. Per stage unless stated.

| Id | Expectation | Would be contradicted by | Standing |
|---|---|---|---|
| E1 | Relay positions in detached arms lose the literal source id and reliability markers faster with depth than in twins; A is a manipulation-check and trajectory position, not the E1 position | Equal or slower loss at relay positions | Primary |
| E2 | Excess or discount magnitude at the far agent (ring C, bounce C, dyad B, diamond D, solo A) is larger at the last cycle than at the first | No compounding | Primary, both stages |
| E3a | Detached and twin trajectories of the same world show material paired displacement at matched positions | Mean absolute paired difference within `.01` in 6 or more of 12 worlds | Primary Set 001; qualified Set 002 |
| E3b | The paired difference grows with cycle | Stable or decreasing as the modal world class | Primary Set 001; qualified Set 002 |
| E4 | Solo detached shows no excess | Solo drift | Primary, both stages |
| E5 | The within-detached LINEAGE deviation rate orders across the ladder as Gate 3A's discount rates did (ring > bounce > dyad > solo) | A different ordering | Primary, both stages |
| E6 | Origin inflation under LINEAGE requires the direct observation in the prompt (H1, strict) | Any detached LINEAGE A firing after lineage return with certainty excess `> .01`; frequency tiers reported descriptively without mechanism labels | Primary, both stages |
| E7 | Set 002 keeps the direction of every one of ten declared within-detached far-position cells of Set 001 | A reversed cell | Cross-stage, primary |

If E6 reads consistent in both stages, the result is consistent with H1 and is not evidence for any mechanism. If E2 and E3b read contradicted, deviations do not compound without re-grounding, which narrows the hypothesis and is reported as such.

## Replication and temporal comparability

Set 002 runs after Set 001 passes its corpus audit and before any Set 001 outcome is read. Within-detached quantities replicate across stages on equal footing. Paired quantities are same-window in Set 001 (four arms) or near-contemporary (diamond, gap recorded) and historical in Set 002; they are reported beside the measured drift gauge and are never pooled or numerically corrected. Differences across execution windows under the same nominal model configuration are reported as observed behavior differing across windows, not as proven model changes. If the drift gauge exceeds its declared operational tolerances, every paired verdict is reported as not attributable to detachment, execution does not change, and the recorded contingency is a later separately frozen stage with contemporary twins.

## Seeds, accounting, archival

No new seeds; every arm inherits. Anchor `d1250663ec206539f2d64c9c8cdcd10c87e5b9af|exp-003-protocol-v0.1|GATE_3C_PLAN_v0.1` for order keys only. Manifests named in `GATE_3C_PLAN_v0.1.json`.

| Stage | Arm | Worlds | Calls per world | Calls |
|---|---|---:|---:|---:|
| set_001 | ring detached | 12 | 25 | 300 |
| set_001 | solo detached | 12 | 25 | 300 |
| set_001 | dyad detached | 12 | 25 | 300 |
| set_001 | bounce detached | 12 | 25 | 300 |
| set_001 | diamond detached | 12 | 33 | 396 |
| set_001 | ring contemporary | 12 | 25 | 300 |
| set_001 | solo contemporary | 12 | 25 | 300 |
| set_001 | dyad contemporary | 12 | 25 | 300 |
| set_001 | bounce contemporary | 12 | 25 | 300 |
| **set_001** | | **108** | | **2796** |
| set_002 | ring detached | 12 | 25 | 300 |
| set_002 | solo detached | 12 | 25 | 300 |
| set_002 | dyad detached | 12 | 25 | 300 |
| set_002 | bounce detached | 12 | 25 | 300 |
| set_002 | diamond detached | 12 | 33 | 396 |
| **set_002** | | **60** | | **1596** |
| **Total** | 14 arms, 14 manifests | **168** | | **4392** |

Archive under `results/archive/gate_3c/`. Gate 3A rules for execution, retries, analysis and closure, with the Gate 3A and 3B closure SHAs recorded before freeze. Worlds are the statistical unit; arms, stages and agent trajectories are kept separate; no significance test. A gate is not redesigned after its results are seen.

## What Gate 3C refuses to conclude

Anything about H2, source recognition, agent continuity or authorship attribution; what any false-independent-support event counted; semantic preservation beyond literal markers; any causal comparison across probe settings or topologies; any pooled stage, arm or stratum; any drift-corrected historical value; any mechanism behind an E6 frequency tier; anything about other models.
