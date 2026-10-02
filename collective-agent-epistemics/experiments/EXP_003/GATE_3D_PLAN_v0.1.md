# EXP-003 Gate 3D Prospective Plan v0.1: Connected Hives

## Status

**PLAN DRAFT / NOT FROZEN / NOT EXECUTED**

Gate 3D may be frozen only after Gate 3B is closed and Gate 3C is closed or explicitly deferred with a recorded reason. Each single hive must be a characterized unit before two are connected; otherwise a multi-hive result cannot be attributed.

## Gate 3D question

> When two hives exchange messages, does cross-hive fan-in at the source holders produce excess over reference, and does the answer depend on whether the hives share one physical root, hold two independent roots that agree, or hold two that conflict? And is any effect attributable to the bridge itself rather than to there being two hives?

## Design principle

Connecting hives changes several things at once if done naively: a second root, possibly a conflicting one, cross-hive fan-in, and the mere existence of a second hive. Gate 3D separates them: every bridged arm has an unbridged twin on the same worlds, so the bridge is an isolable intervention.

## Topologies

`hives_bridged`: two diamonds; after each hive's D fires, D1 sends to A1 and A2, and D2 sends to A2 and A1. `hives_isolated`: the same two diamonds with D1 → A1 and D2 → A2 only. The two differ in exactly two edges.

## Arms

| Arm | Topology | Root mode | Worlds | Seeds | Isolates |
|---|---|---|---|---|---|
| `shared_root_set_001` | bridged | shared (E1 to A1 and A2) | 8 unfiltered | derived | one physical root seen through two hives |
| `isolated_shared_root_set_001` | isolated | shared | 8 | inherited | control: two hives, no bridge; also a stochastic replicate pair of the diamond |
| `dual_root_set_001` | bridged | dual (E1 to A1, E2 to A2) | 16, 2 per cell | derived | agreeing cells: genuine corroboration; conflicting cells: contradiction |
| `isolated_dual_root_set_001` | isolated | dual | 16 | inherited | control: each hive a single-root diamond on its own sensor |

The dual-root arms are reported by cell: agreeing cells (reference about `.845` where both roots are in lineage) and conflicting cells (reference `.50`) are separate strata and are never pooled with the shared-root arms.

## Controlled configuration

Same model, effort, execution policy, prompts, schema, rounds `4`, metrics and probe setting (on) as Gate 3B. Re-grounding on, so the only new variables relative to Gate 3B are the second hive and the bridge, separated by the isolated controls. A detached variant is future work.

## Primary outcomes

The Gate 3B outcome family for every agent, plus: A1 and A2 at every post-seed firing (P(A), excess, FIS, redundant exposures); D1 and D2 at every firing, comparable to Gate 3B D; hive agreement (final answer and P(A)) by cell; provenance across the bridge (whether the other hive's sensor is named; agent-as-source rates for cross-hive versus within-hive messages); paired difference bridged minus isolated per world.

## Pre-registered directional expectations

| Id | Expectation | Would be contradicted by |
|---|---|---|
| E1 | Bridged shared-root A1/A2 excess exceeds isolated shared-root A1/A2 excess on the same worlds | No bridge effect |
| E2 | Bridged agreeing dual-root rises toward `.845` and does not exceed it; isolated stays at its own single-root reference | Bridged stays at `.70`, exceeds `.845`, or isolated rises without a bridge |
| E3 | Bridged conflicting dual-root moves toward `.50` at agents holding both roots | Hives hold `.70` for their own root, or flip past `.50` |
| E4 | LINEAGE reduces excess in the shared-root arm and does not prevent combination in the agreeing dual-root arm | LINEAGE suppresses both |
| E5 | Cross-hive messages lose the sensor id more often than within-hive messages | No difference |

## Seeds and accounting

Anchor `<gate3b closure sha>|<gate3c closure or deferral sha>|exp-003-protocol-v0.1|GATE_3D_PLAN_v0.1`. Exclusions: `42`, the 20 Gate 2B seeds, all Gate 3A/3B/3C seeds. Shared-root seeds via `candidate_seed("G3D_SHARED001", ordinal, nonce)`; dual-root via one stratified scan `candidate_seed("G3D_DUAL001", scan_index, 0)` with `--per-cell 2` over the 8 cells; isolated arms inherit. Manifests named in `GATE_3D_PLAN_v0.1.json`.

| Arm | Worlds | Calls per world | Calls |
|---|---:|---:|---:|
| shared root, bridged | 8 | 66 | 528 |
| shared root, isolated | 8 | 66 | 528 |
| dual root, bridged | 16 | 66 | 1056 |
| dual root, isolated | 16 | 66 | 1056 |
| **Total** | 48 | | **3168** |

## Execution, archival, analysis, closure

Gate 3A rules. Archive under `results/archive/gate_3d/`. Report each arm separately and each bridged arm against its isolated twin per world; dual-root arms by cell first, then by agreeing/conflicting stratum. Closure as Gate 3A, with the Gate 3B and 3C SHAs recorded. A gate is not redesigned after its results are seen.

## After Gate 3D

Only then may the project consider a second model as a primary arm, alternative reliabilities, verbal rather than numeric reliability, an ask-back channel (a receiver may ask one question before answering), or larger populations. Each would be a separately versioned prospective plan.
