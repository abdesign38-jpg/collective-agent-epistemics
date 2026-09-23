# EXP-002 Gate 2B Stress Set 001 Primary Outcome Audit v0.1

## Status

**COMPLETE**: read-only primary-outcome audit. No OpenAI calls, no raw-data changes, no secondary analysis, no statistical tests.

## Scope and provenance

- Starting HEAD: `4318219d793d87fcee7e95ee4a432c110a62d462`
- Raw-data commit: `5fb6ddde3cb7398b3cb5e1dd6e58f02ac0cc0c53`
- Corpus audit commit: `9713dac336eba57ff5df5639149209c729724c05`
- Runtime: `7e9aed1b7093baae10ae30f27e0b6a2b932f92f5`
- Protocol: `exp-002-protocol-v0.1`
- Generalization analyzed: no

## Stress set composition and priority

This set is prospectively balanced: A/A=2, B/B=2, A/B=2, B/A=2. The authoritative interpretation is cell-conditional. Alignment summaries are secondary descriptive bookkeeping; the all-8 total is not a prevalence or generalization estimate.

## Primary outcome table by world

| Order | World | Cell | Alignment | FREE final | LINEAGE final | MACRO M04 | FREE Brier | LINEAGE Brier |
|---:|---|---|---|---|---|---:|---:|---:|
| 1 | G2B_STRESS001_seed_1211074116 | B/B | aligned | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | 0.09 | 0.09 |
| 2 | G2B_STRESS001_seed_945922859 | B/B | aligned | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | 0.09 | 0.09 |
| 3 | G2B_STRESS001_seed_319975066 | B/A | misleading | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | 0.49 | 0.49 |
| 4 | G2B_STRESS001_seed_1531843854 | A/B | misleading | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | 0.49 | 0.49 |
| 5 | G2B_STRESS001_seed_515022515 | B/A | misleading | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | 0.49 | 0.49 |
| 6 | G2B_STRESS001_seed_217181935 | A/A | aligned | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | 0.09 | 0.09 |
| 7 | G2B_STRESS001_seed_1247992891 | A/A | aligned | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | 0.09 | 0.09 |
| 8 | G2B_STRESS001_seed_1523495488 | A/B | misleading | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | 0.49 | 0.49 |

## Answer trajectories

All eight world records preserve complete FREE, LINEAGE, and MACRO answer trajectories in JSON. Final answers agree across conditions within every cell/world. The full trajectories remain authoritative; final agreement does not erase transient trajectory differences.

## Confidence and P(A) trajectories

A/A, B/B, and A/B cells show equal final confidence/P(A) across conditions. B/A shows the clearest transient FREE/LINEAGE divergences in some worlds, including non-identical intermediate LINEAGE values, while final values return to the same recorded endpoint. These are primary trajectory observations, not secondary labels.

## Brier / calibration

Cell-level final Brier is .09 for aligned A/A and B/B, and .49 for misleading A/B and B/A across all conditions. This is descriptive ex-post performance under the known truth; it does not establish a mechanism or ranking.

## Roots, depth, and P(A) deltas

Every valid world remains rooted in E1 with one independent root. FREE/LINEAGE reach depth 12; MACRO reaches depth 3 and stops at M04. Complete P(A)-delta-without-new-independent-evidence trajectories are preserved per world in JSON and are not relabeled as secondary phenomena.

## FREE versus LINEAGE

Final FREE/LINEAGE answer, confidence, P(A), and Brier agree in all eight worlds. Some worlds show transient trajectory divergence, especially in B/B and B/A, but the divergence is not a uniform final architecture difference.

## MACRO stopping boundary

MACRO is a stopping architecture, not an independent model trajectory. Its M01-M04 values reuse the paired/shared trajectory. Each world record compares the M04 stopping outcome descriptively with continued LINEAGE M13 and FREE M13. No causal claim that MACRO improved, degraded, corrected, or prevented anything is made.

## Fixed message-transformation checkpoints

For FREE and LINEAGE, qualitative message observations use only M01, M04, and M13. The JSON preserves exact messages, actors, and event IDs at those checkpoints. The complete event sequence remains available for inspection, but no intermediate event was selected as a semantic checkpoint. Similar checkpoint wording does not prove intermediate language invariance; objectively identifiable factual mutations outside the checkpoints would be reported by exact event ID. MACRO has no independent semantic trajectory analysis.

## Cell-conditional results

| Cell | n | Condition | Accuracy | Mean final confidence | Mean final P(A) | Mean final Brier |
|---|---:|---|---:|---:|---:|---:|
| A/A | 2 | free | 2/2 | 0.7 | 0.7 | 0.09 |
| A/A | 2 | lineage | 2/2 | 0.7 | 0.7 | 0.09 |
| A/A | 2 | macro | 2/2 | 0.7 | 0.7 | 0.09 |
| B/B | 2 | free | 2/2 | 0.7 | 0.3 | 0.09 |
| B/B | 2 | lineage | 2/2 | 0.7 | 0.3 | 0.09 |
| B/B | 2 | macro | 2/2 | 0.7 | 0.3 | 0.09 |
| A/B | 2 | free | 0/2 | 0.7 | 0.3 | 0.49 |
| A/B | 2 | lineage | 0/2 | 0.7 | 0.3 | 0.49 |
| A/B | 2 | macro | 0/2 | 0.7 | 0.3 | 0.49 |
| B/A | 2 | free | 0/2 | 0.7 | 0.7 | 0.49 |
| B/A | 2 | lineage | 0/2 | 0.7 | 0.7 | 0.49 |
| B/A | 2 | macro | 0/2 | 0.7 | 0.7 | 0.49 |

## Alignment stratification

Alignment is reported only after the cell analysis: aligned=A/A+B/B; misleading=A/B+B/A. Each alignment stratum is descriptive and does not override cell-specific results.

## DESCRIPTIVE BALANCED-STRESS SUMMARY

The all-8 arithmetic summary is included only for transparent bookkeeping of the prospectively balanced 2/2/2/2 design. It is not a population prevalence, generalization estimate, probability of an effect, or representative-world frequency. Mean P(A) is not used for interpretation because truth direction differs across cells.

| Condition | Accuracy | Mean final confidence | Mean final P(A) | Mean final Brier |
|---|---:|---:|---:|---:|
| free | 4/8 | 0.7 | not interpreted | 0.29 |
| lineage | 4/8 | 0.7 | not interpreted | 0.29 |
| macro | 4/8 | 0.7 | not interpreted | 0.29 |

## Known from execution

- Eight prospectively balanced Stress worlds were analyzed; no Generalization worlds or W01 denominator were included.
- Every valid world has one E1 root, the frozen depth structure, and a MACRO M04 boundary.
- No raw data changed and no OpenAI calls occurred.

## Descriptive Stress observations

**[DESCRIPTIVE STRESS OBSERVATION]** Under the controlled four-cell design, final primary outcomes are identical across FREE, LINEAGE, and the M04 MACRO stopping outcome within each cell. Transient trajectory differences occur in some worlds, with the clearest variation in B/A and some B/B worlds.

## Boundary conditions

**[BOUNDARY CONDITION]** Cell identity is more informative than the broader alignment label in this balanced design: aligned cells A/A and B/B and misleading cells A/B and B/A must remain visible separately.

## No effect observed

**[NO EFFECT OBSERVED]** No final answer, accuracy, confidence, P(A), or Brier difference between FREE and LINEAGE is observed within the eight Stress worlds.

## Falsification evidence

**[FALSIFICATION EVIDENCE]** The balanced Stress data do not show a uniform final architecture difference. Any interpretation based only on an all-8 aggregate would conceal the cell structure and is not used.

## Open questions

**[OPEN QUESTION]** Why some cells/worlds show transient trajectory divergence while final primary values coincide remains unresolved; this audit does not test a causal mechanism.

## Primary Stress interpretation

Across the four prospectively balanced truth x observation cells, final primary outcomes are architecture-equal within every observed Stress world. Transient FREE/LINEAGE trajectory differences occur in some worlds, especially within B/B and B/A, and are world/cell-dependent. Stress therefore shows no observed final-state architecture difference while preserving conditional transient trajectory variation. The result is descriptive and cell-conditional, not a population claim.

## Limits and gate status

No significance tests, thresholds, semantic taxonomy, secondary exploratory analysis, causal inference, or cross-set synthesis were performed.

Gate 2B data collection: COMPLETE  \nGate 2B corpus integrity: VERIFIED  \nGeneralization primary-outcome audit: COMPLETE  \nStress primary-outcome audit: COMPLETE  \nGate 2B synthesis: PENDING  \nGate 2B scientific closure: NOT YET COMPLETE
