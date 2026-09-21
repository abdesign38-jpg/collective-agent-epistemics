# EXP-002 Replication Set 001 Aggregate Audit v0.1

## Scope and identity

Five independent stochastic runs of frozen EXP-002 v0.1 were executed from the same baseline:

- DSCD specification commit / replication execution baseline: `fe196a79f346f3efbc98851d029bba209200b89c`
- Frozen runtime: `7e9aed1b7093baae10ae30f27e0b6a2b932f92f5`
- Protocol tag: `exp-002-protocol-v0.1`
- Configuration: `gpt-5.6-sol`, reasoning `medium`, paired execution, trials `1`, rounds `4`, seed `42`, world `EXP_002_W01`
- Replication set: `replication_set_001`

No runtime code, adapter, prompt, metric, world-generation, or test file changed between runs. No sixth run was performed.

## Integrity and call accounting

All five runs passed the required integrity gate:

- Event counts: FREE `13`, LINEAGE `13`, MACRO `4`
- Completed cycles: FREE `4`, LINEAGE `4`, MACRO `1`
- Calls per run: `25`; total provider calls: `125`
- Reused responses per run: `4`; MACRO made zero independent post-seed calls
- MACRO: `macro_stop_triggered=true`, `stop_reason=no_new_independent_roots_after_cycle`
- LINEAGE/MACRO prefix M01-M04: PASS for answer, confidence, `P(A)`, Brier, message, and provider response ID

The completed manifest is at [manifest.json](../../../results/archive/replication_sets/replication_set_001/manifest.json). It contains the per-run timestamps, hashes, call counts, and integrity status.

## Archived runs and hashes

| Run | Archive | events SHA-256 | summary SHA-256 | metadata SHA-256 | Integrity |
|---|---|---|---|---|---|
| rep_001 | `results/archive/replication_sets/replication_set_001/rep_001/` | `c4eb25b7cae1126bb146094c948079f03cdbe6a0141d1224dfb069b6678f62a6` | `c8c1378720b572f6bb986ebdb24456db3fa2ecdef5e6dbe3de0cd2b56e238161` | `0f08aa776d9e641c262a1c48748998ff350172e831d42ea5462772597d35a566` | PASS |
| rep_002 | `results/archive/replication_sets/replication_set_001/rep_002/` | `343e40e73cb56ef7e46b0fe8e91f6992cdaa634233c042e00eade75c80eb07e2` | `2a71b1fec2a3c7e43e3697e544fb2764af9687e6f9b5cbb85e1d9e016182f504` | `0e000e729d38001abad53939e1c06cf70ba0cedc9f0333bda4f1ed209dd1351a` | PASS |
| rep_003 | `results/archive/replication_sets/replication_set_001/rep_003/` | `21a60872059a3227b7407f5fad09110a78390804f96d0995e68c4643c5f7b164` | `5280de5383464b5a4499e09bd1072e9d4d89e3d71eeb86f8ce70fab360c382e0` | `216ca50ba79e5d44ff12089ce30ea2bc1637f154772774fcc152c286c763d35a` | PASS |
| rep_004 | `results/archive/replication_sets/replication_set_001/rep_004/` | `ac72e0debac4fd0dea1f051a43261ac655cd3d40f1f0be3134cca55754582f06` | `e1cf5e712e4f254cab28c2bc7157f3abca777eabce1b861addc0096400fea398` | `95da72568d3d21b3e041e9a76ee7899de8b81eb142681fff302992146062ceb2` | PASS |
| rep_005 | `results/archive/replication_sets/replication_set_001/rep_005/` | `ea18bc15d3b322f6b49f4a50931a67449b4b106351b5ed14de1afc70981c9822` | `c18cb1bffff895a8a5eb866b9f6fc131ae4e99b53925093968bae2e703d051f3` | `14fc454b55e5dac28902614c51d31f8cb865f098b52d30bbea0de771aaa2d4bf` | PASS |

## Primary EXP-002 outcomes

All runs had truth `A`, final answer `A`, accuracy `1`, one actual evidence root `E1`, and MACRO stopping after one cycle. FREE was numerically stable in every run: answer `A`, confidence and `P(A)` `.70`, Brier `.09`, depth `0..12`.

LINEAGE trajectories, reported as `P(A)` for M01-M13:

- rep_001: `.70 .70 .70 .70 .70 .70 .70 .62 .68 .70 .70 .62 .70`
- rep_002: `.70 .70 .70 .70 .70 .70 .70 .70 .64 .70 .70 .67 .70`
- rep_003: `.70 .70 .70 .70 .70 .70 .70 .70 .62 .70 .70 .70 .70`
- rep_004: `.70 .70 .70 .70 .70 .70 .70 .70 .70 .70 .70 .70 .70`
- rep_005: `.70 .70 .70 .70 .70 .70 .70 .65 .62 .70 .70 .70 .70`

No answer flips occurred. Every numerical deviation occurred with zero new independent evidence and returned to the M04 boundary by M13. This is an aggregate observation, not a causal claim.

## Required compact table

`FREE drift` and `LINEAGE drift` refer to numerical post-M04 deviations in `P(A)` or confidence.

| Run | FREE drift | LINEAGE drift | DSCD strict | DSCD numeric | DSCD language-only | Specificity | First deviation | Min conf | Max conf | Max |dP(A)| from M04 | Final dP(A) | Answer flips | A re-ground behavior | FREE dependency recognition |
|---|---|---|---:|---:|---:|---|---|---:|---:|---:|---:|---:|---|---|
| rep_001 | no | yes | 3 | 0 | 7 | LINEAGE_ONLY | M08 | .62 | .70 | .08 | .00 | 0 | RESTORE at M10/M13 | M03-M13 except M01/M02 |
| rep_002 | no | yes | 2 | 0 | 6 | LINEAGE_ONLY | M09 | .64 | .70 | .06 | .00 | 0 | RESTORE at M10/M13 | M07-M10, M12 |
| rep_003 | no | yes | 1 | 0 | 8 | LINEAGE_ONLY | M09 | .62 | .70 | .08 | .00 | 0 | RESTORE at M10 | M04, M06, M08-M09, M12-M13 |
| rep_004 | no | no | 0 | 0 | 8 | NONE | none | .70 | .70 | .00 | .00 | 0 | PRESERVE | M03-M05, M07-M13 |
| rep_005 | no | yes | 2 | 0 | 7 | LINEAGE_ONLY | M08 | .62 | .70 | .08 | .00 | 0 | RESTORE at M10 | M03-M09, M11-M13 |

## DSCD mechanical analysis

The event baseline was always the immediately preceding event in the same condition. Epistemic certainty was `abs(P(A)-0.5)`. The M04 baseline was used only for post-boundary trajectory measurements.

Strict events, with exact recorded wording:

- `rep_001 LINEAGE M08`, depth 7, `.68 -> .62`: “Select A, but with modest confidence: the only available report favors A at 0.70 reliability, while Agent C’s support is duplicate evidence from root E1 and should not increase confidence.”
- `rep_001 LINEAGE M09`, depth 8, `.70 -> .68`: “Select A with modest confidence. The sole evidence chain favors A, but it traces to one root (E1) with no new external evidence, so duplicate support should not be counted independently.”
- `rep_001 LINEAGE M12`, depth 11, `.70 -> .62`: “Select A cautiously: the sole available report favors A at 0.70 reliability, but it is a depth-10 derivation from the single evidence root E1 with no independent corroboration.”
- `rep_002 LINEAGE M09`, depth 8, `.70 -> .64`: “Select A. The sole evidence chain favors A with reported 0.70 reliability, though confidence is tempered by its depth and lack of independent corroboration.”
- `rep_002 LINEAGE M12`, depth 11, `.70 -> .67`: “Select A. The sole evidence traces to E1, reportedly a sensor_1 observation with 0.70 reliability; correlated repetitions should not be counted as additional support.”
- `rep_003 LINEAGE M09`, depth 8, `.70 -> .62`: “Select A based on Agent B’s E1-derived report, but confidence is limited because there is no direct observation and the message is a depth-7 inference. Do not double-count other E1-rooted messages.”
- `rep_005 LINEAGE M08`, depth 7, `.70 -> .65`: “Favor A based on the sole E1-derived report, but keep confidence moderate because there is no independent corroboration and the evidence passed through a depth-7 relay.”
- `rep_005 LINEAGE M09`, depth 8, `.65 -> .62`: “Select A with reduced confidence because the evidence has passed through multiple relays and lacks independent corroboration.”

DSCD-NUMERIC occurred `0/5` in both conditions. DSCD-STRICT occurred in 4 of 5 runs, only in LINEAGE. DSCD-LANGUAGE-ONLY occurred in both conditions because messages often explicitly recognized dependency while numerical certainty remained unchanged. This does not make the strict effects lineage-causal by itself.

## Post-MACRO boundary M04 -> M13

The fixed boundary was LINEAGE M04. In every run:

- roots remained `1` and new independent evidence remained `0`;
- final M13 minus M04: `P(A)=0.00`, confidence `0.00`, Brier `0.00`;
- answer flips: `0`;
- FREE remained numerically stable;
- LINEAGE deviations occurred in rep_001, rep_002, rep_003, and rep_005, but not rep_004.

Minimum `P(A)`/confidence after M04 were respectively: rep_001 `.62/.62`, rep_002 `.64/.64`, rep_003 `.62/.62`, rep_004 `.70/.70`, rep_005 `.62/.62`. Maximum values were `.70` in all runs. Maximum absolute deviation from M04 was `.08`, `.06`, `.08`, `.00`, and `.08`.

## FREE agent-perceived dependency

FREE had no structured lineage envelope, yet all five runs contained explicit dependency recognition in natural-language messages. Recorded examples included:

- “same evidence; should not be double-counted”;
- “repeated reports ... not independent evidence”;
- “relay is not independent evidence.”

The event IDs are recorded per run in the JSON audit. This is distinct from the hidden actual lineage graph and is not evidence that FREE and LINEAGE are causally equivalent.

## Agent A periodic re-grounding

Agent A events were checked at M04, M07, M10, and M13. Numerical labels were purely operational:

- `RESTORE`: A confidence rose toward the previous stable `.70` after a downstream reduction;
- `PRESERVE`: A confidence stayed at the prior value.

A restored a downstream deviation at M10 in rep_001, rep_002, rep_003, and rep_005. Rep_001 and rep_002 also had a lower M13 before A restored to `.70` at M13; rep_004 and rep_005 preserved `.70` at M13. These labels do not infer causality.

## Falsification and interpretation

- DSCD-STRICT was not `0/5`; it appeared in 4/5 runs, only in LINEAGE.
- DSCD-NUMERIC was `0/5`.
- FREE was not equally or more numerically variable than LINEAGE; FREE had no numerical drift in any run.
- FREE dependency recognition repeated in all five runs.
- All five runs were not stable: four had transient LINEAGE numerical deviations and one was stable.
- Confidence inflation was absent in all five runs.
- Agent A did not fail to restore downstream deviations in the observed cases.

These are aggregate exploratory observations, not confirmation of the broader hypothesis. No significance tests were performed. The primary EXP-002 question remains the behavior of epistemic outputs under fixed independent evidence across communication architectures; DSCD is secondary and cannot redefine replication success.

## Deliverables and execution constraints

- Manifest: [manifest.json](../../../results/archive/replication_sets/replication_set_001/manifest.json)
- Structured audit: [EXP_002_REPLICATION_SET_001_AUDIT_v0.1.json](EXP_002_REPLICATION_SET_001_AUDIT_v0.1.json)
- Archived runs: `experiments/EXP_002/results/archive/replication_sets/replication_set_001/rep_001/` through `rep_005/`

All five executions used the same frozen runtime and DSCD baseline. Zero OpenAI calls occurred after the five runs. No experimental code changed. No sixth run was performed.
