# EXP-003 Gate 3A Prospective Plan v0.1: Matched Topologies (ring, solo, dyad, bounce)

## Status

**PLAN DRAFT / NOT FROZEN / NOT EXECUTED**

This document becomes a frozen plan only when it is committed together with the runtime commit it names, the protocol tag `exp-003-protocol-v0.1`, and the anchors below filled in, with its machine-readable twin `GATE_3A_PLAN_v0.1.json` set to `FROZEN` in the same commit. Until then it is a design. No Gate 3A real-model call may be made before that commit.

Gate 3A does not modify EXP-002, its frozen runtime, its archives or its audits.

## Scientific anchors (to fill at freeze)

- EXP-002 Gate 2B closure checkpoint: `<sha of exp-002-gate2b-closed-v0.1>`
- Frozen EXP-003 runtime: `<sha>`
- Frozen protocol tag: `exp-003-protocol-v0.1`
- Model: `gpt-5.6-sol`, the EXP-002 model
- Reasoning effort: `medium`
- Execution policy: `paired`
- Rounds: `4` (ring), `12` (solo), `6` (dyad), `3` (bounce); all reach inference depth 12
- Sensor reliability: `0.70`
- Probe: **off** in every Gate 3A arm, so every prompt is byte-identical to the EXP-002 prompt for the same inputs (locked by a unit test)

## What Gate 3A starts from

The 36 archived EXP-002 ring runs, read mechanically against the preceding event in the same condition:

| Agent | Certainty down, FREE / LINEAGE | Events above the single-root reference |
|---|---|---|
| A, holds E1 | 0 / 0 | 1 (FREE, `.70 -> .84`, after a relay attributed E1 to another agent) |
| B, one hop | 0 / 18 | 0 |
| C, two hops | 3 / 21 | 0 |

A returned to its seed value after a downstream deviation in 24 of 24 LINEAGE runs and 3 of 4 FREE runs. FREE and LINEAGE ended equal in 35 of 36 runs. MACRO stopped after one cycle in all 36.

These runs are **retrospective evidence**. They are not a Gate 3A denominator and no Gate 3A arm is compared against them as a primary outcome. The reason is time: the model behind the API name may have changed since they were run, and nothing in the ledger can see that. Gate 3A therefore runs its own ring.

## Gate 3A question

> On the same worlds, the same model on the same day, the same calls and the same depth, how do four communication structures differ in where deviation from the single-root reference occurs and whether the origin corrects it: one agent alone (solo), two agents in direct contact (dyad), three in a loop where everyone reaches the source (ring), and three where the far agent never does (bounce)?

## The ladder

Each rung adds one structural thing to the one before:

```text
SOLO     1 agent, self-recursion                       the null: no interaction
  ↓ add another agent
DYAD     2 agents, everyone reconnects to the source   one other mind transforms and returns the message
  ↓ add a distal position
RING     3 agents, loop, everyone reaches the source   the EXP-002 shape, run contemporaneously
  ↓ change the return path
BOUNCE   3 agents, terminal C, two-way relay B         an agent that never meets the source; drift becomes localizable
```

Gate 3B adds redundant convergence (diamond); Gate 3C removes re-grounding; Gate 3D replicates and connects subnetworks.

## Stages

**Set 001, discovery.** Four arms on 12 prospectively unfiltered worlds. The ring arm derives the seeds; the other three inherit them verbatim with the same execution order, so each world has exactly one execution per topology.

**Set 002, replication.** The same four arms on 12 new unfiltered worlds, derived with the same procedure and excluding every Set 001 seed. Set 002 is pre-registered here, is the same size as Set 001, runs **regardless of what Set 001 shows**, and starts only after Set 001 is closed. It is reported separately and never pooled with Set 001. This is the EXP-002 pattern (Set 001 then Set 002) applied prospectively.

## Arms (identical in both stages)

| Arm | Topology | Rounds | Seeds | Calls per world | What it isolates |
|---|---|---|---|---|---|
| `ring_control_set_00N` | `ring` | 4 | derived | 25 | contemporary baseline; paired reference for the other three |
| `solo_control_set_00N` | `solo` | 12 | inherited | 25 | individual drift without interaction |
| `dyad_set_00N` | `dyad` | 6 | inherited | 25 | direct contact with the source every cycle |
| `bounce_set_00N` | `bounce` | 3 | inherited | 25 | an isolated end (C), a two-way relay (B), a four-hop echo at the origin (A) |

Every arm is required. No arm is optional.

## Controlled configuration

Unchanged across arms and unchanged from EXP-002: model and effort, paired execution, prompt text, response schema shape (probe off), conditions, hidden lineage semantics, visible envelope semantics, EXP-002 metrics, MACRO stop semantics and reuse, maximum depth 12.

Varied by arm only: topology. The factor ledger must show `topology` as the only factor differing between any two Set 001 arms, and `set` as the only factor differing between an arm and its Set 002 counterpart.

## Primary outcomes

Per world, per condition, per event: the EXP-002 family (answer, confidence, P(A), Brier, accuracy, roots, depth, P(A) delta without new evidence) plus reference P(A), excess over reference, redundant root exposures, provenance marks and erosion. Per agent: final P(A), maximum and minimum excess over the run.

Focal, paired by world across arms:

- **B in dyad versus B in ring versus B in bounce:** does direct contact with the source change B's discounting?
- **C in ring versus C in bounce:** does never meeting the source change C's discounting?
- **B's outward firing (B→C) versus return firing (B→A) in bounce.**
- **A at every post-seed firing in all four arms:** restoration to the reference after echoes of 1, 2, 3 and 4 hops.
- **Solo A at every step.**

## Secondary observation

`ring_control_set_001` against the 36 historical ring runs: same prompts, same model name, different date. Any difference is model drift over time. Recorded as an observation; never used to adjust any Gate 3A outcome.

## Pre-registered directional expectations

| Id | Expectation | Would be contradicted by |
|---|---|---|
| E1 | Contemporary ring reproduces the historical pattern: discounts at B and C under LINEAGE, none at A, FREE at the reference | A discounts, or FREE deviates, or no LINEAGE discounts at all |
| E2 | Bounce C discounts at least as often as ring C; bounce B's return firing carries smaller excess magnitude than its outward firing | C discounts less in bounce, or no outward/return difference at B |
| E3 | Dyad B discounts less per event than ring B | Dyad B discounts as much or more |
| E4 | A returns to the reference after each echo in every topology, at a rate not below the ring's | A sustains a deviation across two consecutive firings in any arm |
| E5 | Solo shows no excess in either direction | Solo drifts |
| E6 | Set 002 reproduces the Set 001 ordering of discount rates across the four arms | A different ordering |

## Seed derivation

Anchor (exact ASCII, filled at freeze):

```text
<gate2b closure sha>|exp-003-protocol-v0.1|GATE_3A_PLAN_v0.1
```

`candidate_seed` and `order_key` are the Gate 2B functions, implemented in `manifest.py`. Exclusions: seed `42` and the 20 Gate 2B seeds, because `single` generation reproduces those truth/E1 realizations exactly. Set 001 ring seeds come from `candidate_seed("G3A_RING001", ordinal, nonce)`, ordinals 1..12, unfiltered; the other Set 001 arms inherit them (`--seeds-from`). Set 002 ring seeds come from `candidate_seed("G3A_RING002", ordinal, nonce)` with every Set 001 seed added to the exclusions; the other Set 002 arms inherit them. All eight manifests are derived with zero model calls and committed before the first call. Set 002 manifests may be derived at freeze or at Set 001 closure, but their derivation rule is fixed here.

## Model-call accounting

| Stage | Arms | Worlds each | Calls per world | Calls |
|---|---|---:|---:|---:|
| Set 001 | 4 | 12 | 25 | 1200 |
| Set 002 | 4 | 12 | 25 | 1200 |
| **Total** | | | | **2400** |

## Model layer (optional, separately versioned)

Any arm may later be replicated under the second provider as `<set>_anthropic` with the same seeds and order. Not part of this plan's freeze; it would be its own versioned plan after Gate 3A closes.

## Frozen configuration file and manifests

The orchestrator reads configuration only from `GATE_3A_PLAN_v0.1.json` and world membership only from the committed manifests named there. The JSON plan's status becomes `FROZEN` in the same commit that fills its anchors; the orchestrator refuses live execution otherwise. See the README for the freeze procedure.

## Execution order, retries, archival, analysis

Gate 2B rules: order frozen by `order_key`; no early stopping, extension, replacement or reordering after any model result; technical retries only for provider/schema/interrupt failures, same seed, next `attempt_<NNN>`, manually authorized; archives under `results/archive/gate_3a/<set>/<canonical_id>/attempt_<NNN>/`, never overwritten. A budget pause (`--max-worlds`) is a pacing device blind to results: the paused set is incomplete, may not be audited or reported, and execution resumes in frozen order until every world is archived. Report each arm separately, by world, condition and cell; primary tables are paired by world across arms. Descriptive only; no significance test, threshold or selected event introduced after inspection.

## Falsification and break conditions

Acceptable outcomes that must not alter execution: no deviation anywhere; deviation at B rather than C; A sustaining deviation; FREE deviating; solo drift; dyad discounting as much as the ring; the contemporary ring differing from the historical ring; Set 002 not reproducing Set 001; answer flips.

## The one rule above all others

A gate is not redesigned after its results are seen. Set 002 runs as frozen whatever Set 001 shows. Anything learned in Gate 3A goes into an observation record and, if it motivates a change, into a separately versioned plan for a later gate.

## Closure rule

Gate 3A closes when both stages' manifests were prospectively frozen, every world in all eight arms has a valid archived execution or a documented technical failure, raw outputs are immutable, the predefined primary outcomes are audited, arms and stages are reported separately, the historical comparison is recorded as a secondary observation, and negative results are retained.

## Pre-execution checklist

- this plan committed with anchors filled, JSON twin `FROZEN` in the same commit;
- runtime SHA recorded and tagged `exp-003-protocol-v0.1`;
- Set 001 manifests committed, seeds and execution order frozen, exclusions recorded;
- `python -m unittest discover -s tests` passes, including the EXP-002 prompt-identity test;
- `gate_orchestrator --preflight` completes for the plan;
- every archived run will carry `run_class = gate_3a_real_model`, `fallbacks = false`, `probe = false`;
- no hypothesis text rewritten.
