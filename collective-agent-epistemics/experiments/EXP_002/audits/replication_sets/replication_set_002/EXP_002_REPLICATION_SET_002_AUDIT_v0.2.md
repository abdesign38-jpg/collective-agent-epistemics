# EXP-002 Replication Set 002 Audit v0.2

## Status

**[BUG / CODING AMBIGUITY — SECONDARY SEMANTIC CLASSIFICATION ONLY]**

The Set 002 raw runs are valid and unchanged. This correction affects only criterion-D semantic labels. Numerical transitions, root tracking, actor identity, integrity, FREE stability, and provider accounting are unchanged from v0.1.

The v0.1 audit is preserved. This v0.2 audit supersedes it only for DSCD-STRICT versus DSCD-NUMERIC classification.

## Mechanical result

From raw events, using the immediately preceding message in the same condition, actor=`sender`, and certainty `abs(P(A)-0.5)`:

- LINEAGE numerical discount runs: `8/10`.
- LINEAGE numerical discount events: `10`.
- FREE numerical drift runs: `0/10`.
- Discount actors: A `0`, B `5`, C `5`.
- Confidence inflation events: `0` above the fixed `.70` baseline.
- Answer flips: `0`.
- FREE explicit dependency recognition: `10/10` runs.

This mechanical result has higher evidentiary priority than semantic DSCD labels.

## Criterion-D semantic correction

Criterion D requires that the current message explicitly connect caution or reduced confidence to depth, inference chain, indirectness, relay depth, dependency, lack of direct observation, lack of independent corroboration, or lack of new independent evidence. Merely saying “same root,” “correlated,” or “do not double-count” is insufficient unless connected to confidence or caution.

The only classification change from v0.1 is:

- `rep_003 LINEAGE M12`: `DSCD-STRICT` -> `DSCD-NUMERIC`.
- Message: “Favor A: the only reported evidence is root E1 from Sensor 1 (reliability 0.70). Treat the deeply relayed message as a single evidence source, with no independent corroboration.”
- Reason: dependency is stated, but the message does not explicitly connect it to reduced or cautious confidence.

Corrected semantic totals:

- DSCD-STRICT: `3` events.
- DSCD-NUMERIC: `7` events.
- DSCD-LANGUAGE-ONLY: `3` events.

## All numerical events

| Run | Event | Actor | Receiver | Depth | Confidence transition | P(A) transition | Criterion D | Classification |
|---|---|---:|---:|---:|---|---|---|---|
| rep_001 | M09 | C | A | 8 | `.70 -> .67` | `.70 -> .67` | false | DSCD-NUMERIC |
| rep_003 | M12 | C | A | 11 | `.70 -> .65` | `.70 -> .65` | false | DSCD-NUMERIC |
| rep_005 | M08 | B | C | 7 | `.70 -> .62` | `.70 -> .62` | true | DSCD-STRICT |
| rep_005 | M09 | C | A | 8 | `.62 -> .60` | `.62 -> .60` | true | DSCD-STRICT |
| rep_006 | M11 | B | C | 10 | `.70 -> .62` | `.70 -> .62` | true | DSCD-STRICT |
| rep_006 | M12 | C | A | 11 | `.62 -> .60` | `.62 -> .60` | true | DSCD-STRICT |
| rep_007 | M08 | B | C | 7 | `.70 -> .63` | `.70 -> .63` | false | DSCD-NUMERIC |
| rep_008 | M08 | B | C | 7 | `.70 -> .62` | `.70 -> .62` | false | DSCD-NUMERIC |
| rep_009 | M09 | C | A | 8 | `.70 -> .62` | `.70 -> .62` | false | DSCD-NUMERIC |
| rep_010 | M11 | B | C | 10 | `.70 -> .62` | `.70 -> .62` | false | DSCD-NUMERIC |

All ten events had unchanged root set `[E1]` and zero new independent evidence. No discount was produced by direct evidence holder A.

## Re-grounding and FREE dependency

Agent A was checked at M04, M07, M10 and M13. A returned to `.70` after downstream deviations in `7/10` runs. This is a numerical observation only; direct evidence is not claimed to cause restoration.

All `10/10` runs contained explicit FREE messages recognizing relays, duplicates, correlated evidence, or non-independence. This does not prove that FREE preserved complete epistemic lineage.

## Primary interpretation

The primary Set 002 result is mechanical: LINEAGE numerical discounting occurred transiently in `8/10` runs, while FREE remained numerically stable in `10/10`. The semantic DSCD labels are secondary and partly interpretive. No causal claim is made about lineage or depth, and no generalization beyond this frozen world/model/configuration is supported.

The full per-run hashes, trajectories, and metadata remain in the v0.1 JSON audit and archived raw directories. This v0.2 document corrects the semantic label only; it does not rewrite empirical output.
