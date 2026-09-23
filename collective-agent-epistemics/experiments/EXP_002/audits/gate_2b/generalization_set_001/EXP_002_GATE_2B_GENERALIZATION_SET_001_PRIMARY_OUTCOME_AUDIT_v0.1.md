# EXP-002 Gate 2B Generalization Set 001 Primary Outcome Audit v0.1

## Status

**COMPLETE**: read-only primary-outcome audit. No OpenAI calls, no raw-data changes, no secondary analysis, and no statistical tests.

## Scope and provenance

- Starting HEAD: `9713dac336eba57ff5df5639149209c729724c05`
- Raw-data commit: `5fb6ddde3cb7398b3cb5e1dd6e58f02ac0cc0c53`
- Corpus audit commit: `9713dac336eba57ff5df5639149209c729724c05`
- Runtime: `7e9aed1b7093baae10ae30f27e0b6a2b932f92f5`
- Protocol: `exp-002-protocol-v0.1`
- Generalization worlds: 12; Stress analyzed: no

## Generalization set composition

Aligned: 5. Misleading: 7. Cells: A/A=2, B/B=3, A/B=3, B/A=4. The failed first attempt for `G2B_GEN001_seed_874625177` was excluded; `attempt_002` is authoritative. W01 historical runs were not merged into this denominator.

## Primary outcome table by world

| Order | World | Truth/Obs | Align | FREE final | LINEAGE final | MACRO M04 | FREE Brier | LINEAGE Brier |
|---:|---|---|---|---|---|---:|---:|---:|
| 1 | G2B_GEN001_seed_874625177 | A/B | misleading | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | 0.49 | 0.49 |
| 2 | G2B_GEN001_seed_948364460 | B/B | aligned | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | 0.09 | 0.09 |
| 3 | G2B_GEN001_seed_170961959 | A/B | misleading | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | 0.49 | 0.49 |
| 4 | G2B_GEN001_seed_1925941366 | B/B | aligned | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | 0.09 | 0.09 |
| 5 | G2B_GEN001_seed_1257399226 | B/B | aligned | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | 0.09 | 0.09 |
| 6 | G2B_GEN001_seed_1027876222 | B/A | misleading | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | 0.49 | 0.49 |
| 7 | G2B_GEN001_seed_1353126068 | A/A | aligned | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | 0.09 | 0.09 |
| 8 | G2B_GEN001_seed_1926897563 | B/A | misleading | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | 0.49 | 0.49 |
| 9 | G2B_GEN001_seed_1043406990 | A/A | aligned | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | 0.09 | 0.09 |
| 10 | G2B_GEN001_seed_1114638083 | B/A | misleading | A / P(A) 0.84 / c 0.84 | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | 0.7056 | 0.49 |
| 11 | G2B_GEN001_seed_1662733804 | B/A | misleading | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | A / P(A) 0.7 / c 0.7 | 0.49 | 0.49 |
| 12 | G2B_GEN001_seed_208630909 | A/B | misleading | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | B / P(A) 0.3 / c 0.7 | 0.49 | 0.49 |

## Answer trajectories

All 12 world records preserve complete trajectories in the JSON audit. In the recorded Generalization corpus, final FREE and LINEAGE answers agree within every world; accuracy is 5/12 for each condition. The full answer trajectories remain available per condition/world in the structured artifact.

## Confidence and P(A) trajectories

FREE and LINEAGE are identical in many worlds, while transient differences occur in several worlds and may reverse by M13. Example primary trajectory differences are recorded in the JSON world records; no post-hoc threshold or selected message index was used. Final FREE confidence ranges from 0.70 to 0.84, while LINEAGE and MACRO final confidence are 0.70 in all worlds.

## Brier / calibration

Across all 12 worlds, final FREE confidence/Brier varies in misleading worlds, including a maximum FREE Brier of 0.7056. LINEAGE final Brier is 0.09 in aligned worlds and 0.49 in misleading worlds. These are descriptive ex-post metrics; they do not establish that a model identified evidence correctness.

## Independent evidence roots and inference depth

The corpus records root E1 with one independent root throughout. Maximum inference depths are FREE=12, LINEAGE=12, and MACRO=3 in every valid world. No causal interpretation of depth is made.

## P(A) changes without new independent evidence

The complete archived `P(A)`-delta trajectories are preserved in JSON for every FREE and LINEAGE world. They are reported as the frozen primary metric only; they are not relabeled as DSCD or another secondary category.

## FREE versus LINEAGE

Final answers agree in all 12 worlds. Final numerical differences are observable in a subset of worlds, especially misleading worlds: FREE reaches confidence 0.84/Brier 0.7056 in `G2B_GEN001_seed_1114638083`, while LINEAGE ends at 0.70/Brier 0.49. Other worlds have equal final values despite transient trajectory differences. Thus the recorded comparison is mixed and world-dependent, not a uniform architecture ranking.

## MACRO stopping boundary

MACRO is a stopping architecture, not an independent model trajectory. Its M01-M04 values reuse the paired/shared LINEAGE trajectory. In every world, the M04 stopping outcome is compared descriptively with continued LINEAGE M13 and FREE M13; the exact differences are in each JSON record. No causal claim that MACRO improved, degraded, corrected, or prevented anything is made.

## Message transformations

Message transformations are retained qualitatively with exact event IDs in each world record, without scores or semantic classes. The records note messages at M01, M04, and M13 for FREE and LINEAGE, allowing direct inspection of whether observed-state/reliability claims were preserved, omitted, qualified, or altered. Numerical outcomes retain priority where wording and metrics differ.

## Alignment-stratified results

| Alignment | n | Condition | Accuracy | Final confidence mean/min/max | Final Brier mean/min/max |
|---|---:|---|---:|---|---|
| aligned | 5 | free | 5/5 | 0.7 / 0.7 / 0.7 | 0.09 / 0.09 / 0.09 |
| aligned | 5 | lineage | 5/5 | 0.7 / 0.7 / 0.7 | 0.09 / 0.09 / 0.09 |
| aligned | 5 | macro | 5/5 | 0.7 / 0.7 / 0.7 | 0.09 / 0.09 / 0.09 |
| misleading | 7 | free | 0/7 | 0.72 / 0.7 / 0.84 | 0.5208 / 0.49 / 0.7056 |
| misleading | 7 | lineage | 0/7 | 0.7 / 0.7 / 0.7 | 0.49 / 0.49 / 0.49 |
| misleading | 7 | macro | 0/7 | 0.7 / 0.7 / 0.7 | 0.49 / 0.49 / 0.49 |

## Truth × observed-state cells

| Cell | n | Condition | Accuracy | Mean final confidence | Mean final P(A) | Mean final Brier |
|---|---:|---|---:|---:|---:|---:|
| A/A | 2 | free | 2/2 | 0.7 | 0.7 | 0.09 |
| A/A | 2 | lineage | 2/2 | 0.7 | 0.7 | 0.09 |
| A/A | 2 | macro | 2/2 | 0.7 | 0.7 | 0.09 |
| B/B | 3 | free | 3/3 | 0.7 | 0.3 | 0.09 |
| B/B | 3 | lineage | 3/3 | 0.7 | 0.3 | 0.09 |
| B/B | 3 | macro | 3/3 | 0.7 | 0.3 | 0.09 |
| A/B | 3 | free | 0/3 | 0.7 | 0.3 | 0.49 |
| A/B | 3 | lineage | 0/3 | 0.7 | 0.3 | 0.49 |
| A/B | 3 | macro | 0/3 | 0.7 | 0.3 | 0.49 |
| B/A | 4 | free | 0/4 | 0.735 | 0.735 | 0.5439 |
| B/A | 4 | lineage | 0/4 | 0.7 | 0.7 | 0.49 |
| B/A | 4 | macro | 0/4 | 0.7 | 0.7 | 0.49 |

## Comparison with closed W01 same-world evidence

W01 is historical context only and is not included in the 12-world denominator. Only primary answer, confidence/P(A), Brier, accuracy, FREE/LINEAGE trajectories, and the MACRO stopping boundary are considered here. Secondary W01 coding was not imported.

## Known from execution

- 12 authoritative Generalization archives analyzed; failed attempt excluded.
- 5 aligned and 7 misleading worlds; cells A/A=2, B/B=3, A/B=3, B/A=4.
- All valid worlds have root E1 and the frozen depth structure.
- No OpenAI calls or raw-data modifications occurred.

## Descriptive Generalization observations

**[DESCRIPTIVE GENERALIZATION OBSERVATION]** Architecture-dependent differences are observable in recorded primary outcomes in some worlds, especially through transient FREE/LINEAGE trajectory divergence and a final FREE confidence/Brier deviation in one misleading world. The pattern is not uniform across all worlds.

## Boundary conditions

**[BOUNDARY CONDITION]** The observed differences vary by evidence realization: aligned worlds are numerically stable and equal at final primary metrics, while misleading worlds show the clearest final FREE variation. This is descriptive and not causal.

## No effect observed

**[NO EFFECT OBSERVED]** No final-answer disagreement between FREE and LINEAGE was observed. No answer trajectory difference is promoted to a causal or secondary claim here.

## Falsification evidence

**[FALSIFICATION EVIDENCE]** The Generalization corpus does not show a uniform architecture effect: several worlds have equal final outcomes, and all misleading worlds remain inaccurate. A global claim that one architecture is always better or worse is unsupported by these primary outcomes.

## Open questions

**[OPEN QUESTION]** Why some world/evidence realizations show transient or final numerical divergence while others do not remains unresolved. No mechanism is inferred from this audit.

## Primary Generalization interpretation

The primary evidence is best described as **mixed / conditional on world and evidence realization**: architecture-dependent differences are observable in recorded primary trajectories in some Generalization worlds, but disappear at final state in many others; aligned worlds are stable/equal at final metrics, while misleading worlds contain the clearest differences. No causal, population, significance, or global architecture ranking claim is made.

## Statistical and causal limits

No significance tests, p-values, confidence intervals, post-hoc thresholds, regression, or population inference were performed. This is an exploratory audit of 12 prospectively unfiltered worlds. Secondary exploratory analyses were not performed.

## Gate status

Gate 2B data collection: COMPLETE  
Gate 2B corpus integrity: VERIFIED  
Generalization primary-outcome audit: COMPLETE  
Stress primary-outcome audit: PENDING  
Gate 2B synthesis: PENDING  
Gate 2B scientific closure: NOT YET COMPLETE
