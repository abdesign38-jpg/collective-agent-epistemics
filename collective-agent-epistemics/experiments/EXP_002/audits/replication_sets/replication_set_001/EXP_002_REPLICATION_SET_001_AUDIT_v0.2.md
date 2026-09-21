# EXP-002 Replication Set 001 Audit v0.2

## Status and correction

**[BUG — AUDIT ANALYSIS ONLY]**

This v0.2 audit corrects the DSCD analysis in v0.1. The archived empirical runs are not corrupted and remain byte-for-byte unchanged. v0.1 is preserved as the historical original audit; v0.2 supersedes it only for DSCD event classification and agent attribution.

The bug had two parts:

1. Some transitions were not aligned strictly to the immediately preceding numeric `visible_message_id` within the same condition.
2. Some records labeled the receiving agent instead of the response-generating agent.

The corrected fields are `actor = event.sender` and `receiver = event.receiver`. For example, `rep_001 LINEAGE` has M07 `.70`, M08 `.62`, M09 `.68`; therefore M08 is `.70 -> .62` and M09 is `.62 -> .68`.

## Frozen analysis rule

For each condition, events were sorted numerically M01 through M13. Each Mxx baseline was M(xx-1) in the same condition. Certainty was `abs(P(A)-0.5)`. Criterion D was evaluated only from the current event's visible model message. M04 was used only for the separate post-boundary trajectory, never as the event-level DSCD baseline.

## Corrected formal counts

- DSCD-STRICT: `6`
- DSCD-NUMERIC: `1`
- Runs with at least one strict event: `4/5`
- Runs with any numerical LINEAGE discount: `4/5`
- Runs with numerical FREE drift: `0/5`
- Agent A numerical discounts: `0`

## Corrected events

| Run | Condition | Event | Actor | Receiver | Direct observation | Depth | Transition confidence | Transition P(A) | Classification |
|---|---|---|---|---|---|---:|---|---|---|
| rep_001 | LINEAGE | M08 | B | C | no | 7 | `.70 -> .62` | `.70 -> .62` | DSCD-STRICT |
| rep_001 | LINEAGE | M12 | C | A | no | 11 | `.70 -> .62` | `.70 -> .62` | DSCD-STRICT |
| rep_002 | LINEAGE | M09 | C | A | no | 8 | `.70 -> .64` | `.70 -> .64` | DSCD-STRICT |
| rep_002 | LINEAGE | M12 | C | A | no | 11 | `.70 -> .67` | `.70 -> .67` | DSCD-NUMERIC |
| rep_003 | LINEAGE | M09 | C | A | no | 8 | `.70 -> .62` | `.70 -> .62` | DSCD-STRICT |
| rep_005 | LINEAGE | M08 | B | C | no | 7 | `.70 -> .65` | `.70 -> .65` | DSCD-STRICT |
| rep_005 | LINEAGE | M09 | C | A | no | 8 | `.65 -> .62` | `.65 -> .62` | DSCD-STRICT |

No numerical FREE discount occurred. `rep_004` contained no numerical discount.

Criterion D is absent for `rep_002 M12`: the message mentions correlated repetitions but does not explicitly attribute caution or reduced confidence. It is therefore DSCD-NUMERIC, not DSCD-STRICT.

## Per-run corrected counts and re-grounding

| Run | FREE numerical drift | LINEAGE strict | LINEAGE numeric | First strict event | Agent A M04/M07/M10/M13 | A returns to .70 |
|---|---|---:|---:|---|---|---|
| rep_001 | no | 2 | 0 | M08 | PRESERVE / PRESERVE / RESTORE / RESTORE | yes |
| rep_002 | no | 1 | 1 | M09 | PRESERVE / PRESERVE / RESTORE / RESTORE | yes |
| rep_003 | no | 1 | 0 | M09 | PRESERVE / PRESERVE / RESTORE / PRESERVE | yes |
| rep_004 | no | 0 | 0 | none | PRESERVE / PRESERVE / PRESERVE / PRESERVE | yes |
| rep_005 | no | 2 | 0 | M08 | PRESERVE / PRESERVE / RESTORE / PRESERVE | yes |

These are numerical labels only. They do not infer that direct evidence caused restoration.

## Source-holder stratification

For this topology, Agent A is the direct evidence holder and B/C are non-source agents. The seven numerical discounts were produced by:

- Agent B: `rep_001 M08`, `rep_005 M08`;
- Agent C: `rep_001 M12`, `rep_002 M09`, `rep_002 M12`, `rep_003 M09`, `rep_005 M09`;
- Agent A: none.

This is a descriptive stratification, not a causal result.

## Primary EXP-002 interpretation

The five formal runs all used the same frozen world/model/configuration and all passed the execution gates. FREE had no numerical drift in any run. LINEAGE had transient numerical discounts in four runs and was numerically stable in `rep_004`. MACRO stopped after one cycle in every run. Answers remained `A`, no answer flips occurred, and final M13 values returned to the M04 boundary.

This supports a statement about stochastic reproducibility under one frozen world/model/configuration only. It does not establish generalization across worlds, models, or configurations; it does not establish causality; and it does not establish that recursion alone produces DSCD. The descriptive separation remains: FREE recursion, LINEAGE explicit lineage/depth, and Agent A periodic direct-evidence access.

## Historical Pilot 002 comparison

Pilot 002 is excluded from the formal denominator. Applying the same v0.1 rule to its archived raw events yields one DSCD-STRICT event:

- Pilot 002 LINEAGE M09, actor C, receiver A, depth 8, `.70 -> .62`, `P(A) .70 -> .62`, roots unchanged `[E1]`, new evidence `0`.
- Recorded wording: “Select A. The sole evidence root E1 reportedly favors A with 0.70 reliability, but confidence is reduced because the report is indirect, seven inference steps deep, and lacks independent corroboration.”

Formal replication set: `6` strict events across `5` runs. Historical Pilot 002 plus formal runs: `7` strict events across `6` runs. The latter is descriptive context, not a statistical sample.

## Replication-set deliverables

- Historical v0.1 audit: [EXP_002_REPLICATION_SET_001_AUDIT_v0.1.md](EXP_002_REPLICATION_SET_001_AUDIT_v0.1.md)
- Corrected JSON: [EXP_002_REPLICATION_SET_001_AUDIT_v0.2.json](EXP_002_REPLICATION_SET_001_AUDIT_v0.2.json)
- Errata: [EXP_002_REPLICATION_SET_001_ERRATA_v0.1.md](EXP_002_REPLICATION_SET_001_ERRATA_v0.1.md)
- Replication set 001 manifest: [manifest.json](../../../results/archive/replication_sets/replication_set_001/manifest.json)

No significance tests were performed. No OpenAI calls were made during correction. No archived empirical file or EXP-002 runtime file was modified.
