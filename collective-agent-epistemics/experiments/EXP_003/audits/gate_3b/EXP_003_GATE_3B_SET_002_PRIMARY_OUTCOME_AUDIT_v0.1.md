# EXP-003 Gate 3B Set 002 Primary-Outcome Audit v0.1

## Status

**COMPLETE**

Descriptive and pre-registered. Rates are counts over events; the only tolerances are those the frozen plan states in words. This stage is reported alone; strata are reported alone. Expectation verdicts restate the plan's 'would be contradicted by' column. The secondary inbound-naming table carries no verdict. Negative results stand.

## Provenance

- Specification: `EXP-003-GATE-3B-PRIMARY-OUTCOME-AUDIT-SPEC-v0.1`
- Plan: `GATE_3B_PLAN_v0.1` (status `FROZEN`, sha256 `5cea3ad5959b1ecfa9080f3bfad834b75366d9841fa6739e965bf69e0036a672`)
- Frozen runtime: `c54563bbb3f17e49c70e8e4f2e3a0369910d3c15`; Gate 3A checkpoint `1daa069af7000613ba06af35714bc22764c1f409`
- Corpus audit: `experiments/EXP_003/audits/gate_3b/EXP_003_GATE_3B_SET_002_CORPUS_AUDIT_v0.1.json` (status PASS, sha256 `1ad6ffa30765eb8ecad65133dc5f9fd9e7558f87ca9962bbd2384c16aa7116c1`)
- HEAD at audit time: `e58b253f11e1c539e65fc8186fd63b6b82e1b1d3`
- Tolerances: `{"direction": 1e-06, "E1": 0.01, "E2_majority_of_12": 7, "E5": 0.01, "E6": 0.02}`

## Sets

| Set | Topology | Root mode | Probe | Rounds | Worlds | Cells | Strata |
|---|---|---|---|---:|---:|---|---|
| `diamond_set_002` | diamond | single | on | 4 | 12 | A/A: 1, A/B: 2, B/A: 4, B/B: 5 | None: 12 |
| `dual_root_set_002` | diamond | dual | on | 4 | 16 | A/A/A: 2, A/A/B: 2, A/B/A: 2, A/B/B: 2, B/A/A: 2, B/A/B: 2, B/B/A: 2, B/B/B: 2 | agreeing: 8, conflicting: 8 |

## Arm aggregates (d = discount, i = inflation, r = at reference; strata separate)

| Set | Condition | Stratum | D | A post-seed |
|---|---|---|---|---|
| `diamond_set_002` | free | None | 0d/5i/43r of 48; FIS>0 at 0; x̄ +0.008 | 0d/0i/48r of 48; FIS>0 at 0; x̄ +0.000 |
| `diamond_set_002` | lineage | None | 7d/3i/38r of 48; FIS>0 at 0; x̄ -0.006 | 0d/7i/41r of 48; FIS>0 at 7; x̄ +0.013 |
| `dual_root_set_002` | free | agreeing | 15d/17i/0r of 32; FIS>0 at 0; x̄ -0.026 | 15d/17i/0r of 32; FIS>0 at 1; x̄ -0.032 |
| `dual_root_set_002` | free | conflicting | 0d/0i/0r of 32 (+32 even-reference; mean dep -0.018); FIS>0 at 1; x̄ n/a | 0d/0i/0r of 32 (+32 even-reference; mean dep +0.017); FIS>0 at 3; x̄ n/a |
| `dual_root_set_002` | lineage | agreeing | 20d/12i/0r of 32; FIS>0 at 2; x̄ -0.043 | 18d/14i/0r of 32; FIS>0 at 20; x̄ -0.012 |
| `dual_root_set_002` | lineage | conflicting | 0d/0i/0r of 32 (+32 even-reference; mean dep -0.008); FIS>0 at 0; x̄ n/a | 0d/0i/0r of 32 (+32 even-reference; mean dep +0.120); FIS>0 at 15; x̄ n/a |

## Pre-registered expectations

| Id | Verdict | Quantities |
|---|---|---|
| E1 | **consistent** | `{"arm1_worlds_with_FREE_D_excess_above_tolerance": 4, "worlds": 12, "tolerance": 0.01}` |
| E2 | **consistent** | `{"worlds_where_LINEAGE_mean_D_excess_exceeds_FREE": 2, "worlds": 12, "majority": 7}` |
| E3 | **contradicted** | `{"by_condition": {"free": {"concordant": 0, "excess_without_FIS": 5, "FIS_without_excess": 0, "D_firings": 48}, "lineage": {"concordant": 0, "excess_without_FIS": 3, "FIS_without_excess": 0, "D_firings": 48}}}` |
| E4 | **contradicted** | `{"by_condition": {"free": {"marked_firings": 9, "excess_rate_marked": 0.0, "clean_firings": 39, "excess_rate_clean": 0.128205}, "lineage": {"marked_firings": 5, "excess_rate_marked": 0.2, "clean_firings": 43, "excess_rate_clean": 0.046512}}}` |
| E5 | **consistent** | `{"agreeing_worlds": 8, "conflicting_worlds": 8, "tolerance": 0.01, "free": {"classes": {"two_root": 23, "single_root": 5, "other": 3, "over": 1}, "modal": "two_root"}, "lineage": {"classes": {"two_root": 12, "other": 13, "single_root": 4, "over": 3}, "modal": "other"}, "conflicting_stratum_departure": {"free": -0.0175, "lineage": -0.007812}}` |
| E6 | **not assessable** | `{}` |
| E7 | **assessed in the synthesis across Set 001 and Set 002, not in a single-stage audit** | `{}` |

## Matrix by world (mean D certainty excess, or mean departure toward E1 for the conflicting stratum)

| Set | Seed | Cell | Stratum | FREE | LINEAGE | FIS>0 FREE / LINEAGE |
|---|---:|---|---|---:|---:|---|
| `diamond_set_002` | 316127362 | B/A | single | +0.000 | +0.000 | 0 / 0 |
| `diamond_set_002` | 710597220 | B/A | single | +0.000 | -0.005 | 0 / 0 |
| `diamond_set_002` | 962632369 | A/A | single | +0.000 | -0.007 | 0 / 0 |
| `diamond_set_002` | 241955308 | B/B | single | +0.005 | -0.013 | 0 / 0 |
| `diamond_set_002` | 723648650 | A/B | single | +0.000 | +0.025 | 0 / 0 |
| `diamond_set_002` | 1054956113 | B/A | single | +0.013 | +0.000 | 0 / 0 |
| `diamond_set_002` | 1831325112 | B/B | single | +0.000 | +0.000 | 0 / 0 |
| `diamond_set_002` | 374607106 | B/B | single | +0.045 | -0.030 | 0 / 0 |
| `diamond_set_002` | 443947794 | B/B | single | +0.000 | -0.035 | 0 / 0 |
| `diamond_set_002` | 533125286 | A/B | single | +0.030 | -0.010 | 0 / 0 |
| `diamond_set_002` | 633201644 | B/B | single | +0.000 | +0.000 | 0 / 0 |
| `diamond_set_002` | 1092129420 | B/A | single | +0.000 | +0.005 | 0 / 0 |
| `dual_root_set_002` | 1761851777 | A/B/B | agreeing | -0.002 | -0.040 | 0 / 0 |
| `dual_root_set_002` | 1516256562 | B/A/A | agreeing | -0.059 | -0.011 | 0 / 0 |
| `dual_root_set_002` | 1614821534 | B/A/A | agreeing | -0.047 | -0.059 | 0 / 2 |
| `dual_root_set_002` | 1943818421 | B/A/B | conflicting | dep +0.000 | dep -0.028 | 0 / 0 |
| `dual_root_set_002` | 2082756798 | B/B/B | agreeing | +0.013 | -0.074 | 0 / 0 |
| `dual_root_set_002` | 1068989073 | B/B/B | agreeing | -0.044 | -0.094 | 0 / 0 |
| `dual_root_set_002` | 1150363503 | B/B/A | conflicting | dep +0.000 | dep +0.000 | 0 / 0 |
| `dual_root_set_002` | 1587692757 | A/A/B | conflicting | dep -0.100 | dep -0.025 | 0 / 0 |
| `dual_root_set_002` | 1264392180 | A/A/B | conflicting | dep +0.010 | dep +0.018 | 1 / 0 |
| `dual_root_set_002` | 2017093923 | A/A/A | agreeing | +0.000 | -0.034 | 0 / 0 |
| `dual_root_set_002` | 216987976 | A/B/A | conflicting | dep +0.000 | dep -0.022 | 0 / 0 |
| `dual_root_set_002` | 1119880167 | A/B/B | agreeing | -0.035 | +0.001 | 0 / 0 |
| `dual_root_set_002` | 1629652161 | A/A/A | agreeing | -0.037 | -0.039 | 0 / 0 |
| `dual_root_set_002` | 1322584095 | A/B/A | conflicting | dep +0.000 | dep -0.005 | 0 / 0 |
| `dual_root_set_002` | 80913935 | B/A/B | conflicting | dep -0.050 | dep +0.000 | 0 / 0 |
| `dual_root_set_002` | 479525595 | B/B/A | conflicting | dep +0.000 | dep +0.000 | 0 / 0 |

## Secondary: inbound messages naming the sensor (descriptive, no verdict)

| Set | Condition | Stratum | Position | Inbound naming the sensor | Counts |
|---|---|---|---|---:|---|
| `diamond_set_002` | free | None | D | 0 | 0d/0i/9r of 9; FIS>0 at 0; x̄ +0.000 |
| `diamond_set_002` | free | None | D | 2 | 0d/5i/34r of 39; FIS>0 at 0; x̄ +0.009 |
| `diamond_set_002` | free | None | A | 0 | 0d/0i/9r of 9; FIS>0 at 0; x̄ +0.000 |
| `diamond_set_002` | free | None | A | 1 | 0d/0i/39r of 39; FIS>0 at 0; x̄ +0.000 |
| `diamond_set_002` | lineage | None | D | 0 | 4d/1i/11r of 16; FIS>0 at 0; x̄ -0.016 |
| `diamond_set_002` | lineage | None | D | 1 | 1d/0i/5r of 6; FIS>0 at 0; x̄ -0.005 |
| `diamond_set_002` | lineage | None | D | 2 | 2d/2i/22r of 26; FIS>0 at 0; x̄ +0.000 |
| `diamond_set_002` | lineage | None | A | 0 | 0d/7i/15r of 22; FIS>0 at 7; x̄ +0.029 |
| `diamond_set_002` | lineage | None | A | 1 | 0d/0i/26r of 26; FIS>0 at 0; x̄ +0.000 |
| `dual_root_set_002` | free | agreeing | D | 0 | 0d/1i/0r of 1; FIS>0 at 0; x̄ +0.000 |
| `dual_root_set_002` | free | agreeing | D | 1 | 4d/1i/0r of 5; FIS>0 at 0; x̄ -0.088 |
| `dual_root_set_002` | free | agreeing | D | 2 | 11d/15i/0r of 26; FIS>0 at 0; x̄ -0.016 |
| `dual_root_set_002` | free | agreeing | A | 0 | 1d/3i/0r of 4; FIS>0 at 1; x̄ -0.016 |
| `dual_root_set_002` | free | agreeing | A | 1 | 14d/14i/0r of 28; FIS>0 at 0; x̄ -0.035 |
| `dual_root_set_002` | free | conflicting | D | 0 | 0d/0i/0r of 7 (+7 even-reference; mean dep +0.000); FIS>0 at 0; x̄ n/a |
| `dual_root_set_002` | free | conflicting | D | 1 | 0d/0i/0r of 14 (+14 even-reference; mean dep -0.031); FIS>0 at 1; x̄ n/a |
| `dual_root_set_002` | free | conflicting | D | 2 | 0d/0i/0r of 11 (+11 even-reference; mean dep -0.011); FIS>0 at 0; x̄ n/a |
| `dual_root_set_002` | free | conflicting | A | 0 | 0d/0i/0r of 19 (+19 even-reference; mean dep +0.027); FIS>0 at 2; x̄ n/a |
| `dual_root_set_002` | free | conflicting | A | 1 | 0d/0i/0r of 13 (+13 even-reference; mean dep +0.002); FIS>0 at 1; x̄ n/a |
| `dual_root_set_002` | lineage | agreeing | D | 0 | 2d/0i/0r of 2; FIS>0 at 0; x̄ -0.075 |
| `dual_root_set_002` | lineage | agreeing | D | 1 | 11d/3i/0r of 14; FIS>0 at 0; x̄ -0.069 |
| `dual_root_set_002` | lineage | agreeing | D | 2 | 7d/9i/0r of 16; FIS>0 at 2; x̄ -0.017 |
| `dual_root_set_002` | lineage | agreeing | A | 0 | 13d/12i/0r of 25; FIS>0 at 18; x̄ -0.014 |
| `dual_root_set_002` | lineage | agreeing | A | 1 | 5d/2i/0r of 7; FIS>0 at 2; x̄ -0.007 |
| `dual_root_set_002` | lineage | conflicting | D | 0 | 0d/0i/0r of 3 (+3 even-reference; mean dep -0.003); FIS>0 at 0; x̄ n/a |
| `dual_root_set_002` | lineage | conflicting | D | 1 | 0d/0i/0r of 19 (+19 even-reference; mean dep -0.010); FIS>0 at 0; x̄ n/a |
| `dual_root_set_002` | lineage | conflicting | D | 2 | 0d/0i/0r of 10 (+10 even-reference; mean dep -0.005); FIS>0 at 0; x̄ n/a |
| `dual_root_set_002` | lineage | conflicting | A | 0 | 0d/0i/0r of 26 (+26 even-reference; mean dep +0.140); FIS>0 at 15; x̄ n/a |
| `dual_root_set_002` | lineage | conflicting | A | 1 | 0d/0i/0r of 6 (+6 even-reference; mean dep +0.033); FIS>0 at 0; x̄ n/a |

## MACRO stopping boundary

| Set | Seed | Stop event | MACRO events | Stop triggered | Responses reused |
|---|---:|---|---:|---|---|
| `diamond_set_002` | 316127362 | M05 | 5 | True | True |
| `diamond_set_002` | 710597220 | M05 | 5 | True | True |
| `diamond_set_002` | 962632369 | M05 | 5 | True | True |
| `diamond_set_002` | 241955308 | M05 | 5 | True | True |
| `diamond_set_002` | 723648650 | M05 | 5 | True | True |
| `diamond_set_002` | 1054956113 | M05 | 5 | True | True |
| `diamond_set_002` | 1831325112 | M05 | 5 | True | True |
| `diamond_set_002` | 374607106 | M05 | 5 | True | True |
| `diamond_set_002` | 443947794 | M05 | 5 | True | True |
| `diamond_set_002` | 533125286 | M05 | 5 | True | True |
| `diamond_set_002` | 633201644 | M05 | 5 | True | True |
| `diamond_set_002` | 1092129420 | M05 | 5 | True | True |
| `dual_root_set_002` | 1761851777 | M09 | 9 | True | True |
| `dual_root_set_002` | 1516256562 | M09 | 9 | True | True |
| `dual_root_set_002` | 1614821534 | M09 | 9 | True | True |
| `dual_root_set_002` | 1943818421 | M09 | 9 | True | True |
| `dual_root_set_002` | 2082756798 | M09 | 9 | True | True |
| `dual_root_set_002` | 1068989073 | M09 | 9 | True | True |
| `dual_root_set_002` | 1150363503 | M09 | 9 | True | True |
| `dual_root_set_002` | 1587692757 | M09 | 9 | True | True |
| `dual_root_set_002` | 1264392180 | M09 | 9 | True | True |
| `dual_root_set_002` | 2017093923 | M09 | 9 | True | True |
| `dual_root_set_002` | 216987976 | M09 | 9 | True | True |
| `dual_root_set_002` | 1119880167 | M09 | 9 | True | True |
| `dual_root_set_002` | 1629652161 | M09 | 9 | True | True |
| `dual_root_set_002` | 1322584095 | M09 | 9 | True | True |
| `dual_root_set_002` | 80913935 | M09 | 9 | True | True |
| `dual_root_set_002` | 479525595 | M09 | 9 | True | True |

## Primary outcome table by world (EXP-002 family)

| Set | Order | Seed | Cell | Condition | Final | Acc | Conf | P(A) | Ref | Kind | Brier | Roots | Depth | FIS>0 | agent-as-source |
|---|---:|---:|---|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|
| `diamond_set_002` | 1 | 316127362 | B/A | free | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 12 | 0 | 0 |
| `diamond_set_002` | 1 | 316127362 | B/A | lineage | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 12 | 0 | 1 |
| `diamond_set_002` | 1 | 316127362 | B/A | macro | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 3 | 0 | 0 |
| `diamond_set_002` | 2 | 710597220 | B/A | free | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 12 | 0 | 2 |
| `diamond_set_002` | 2 | 710597220 | B/A | lineage | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 12 | 2 | 0 |
| `diamond_set_002` | 2 | 710597220 | B/A | macro | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 3 | 0 | 0 |
| `diamond_set_002` | 3 | 962632369 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 1 |
| `diamond_set_002` | 3 | 962632369 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 1 | 0 |
| `diamond_set_002` | 3 | 962632369 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `diamond_set_002` | 4 | 241955308 | B/B | free | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 0 | 2 |
| `diamond_set_002` | 4 | 241955308 | B/B | lineage | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `diamond_set_002` | 4 | 241955308 | B/B | macro | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `diamond_set_002` | 5 | 723648650 | A/B | free | B | 0 | 0.70 | 0.300 | 0.300 | at_reference | 0.490 | 1 | 12 | 0 | 0 |
| `diamond_set_002` | 5 | 723648650 | A/B | lineage | B | 0 | 0.82 | 0.180 | 0.300 | inflation | 0.672 | 1 | 12 | 2 | 1 |
| `diamond_set_002` | 5 | 723648650 | A/B | macro | B | 0 | 0.70 | 0.300 | 0.300 | at_reference | 0.490 | 1 | 3 | 0 | 0 |
| `diamond_set_002` | 6 | 1054956113 | B/A | free | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 12 | 0 | 3 |
| `diamond_set_002` | 6 | 1054956113 | B/A | lineage | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 12 | 0 | 2 |
| `diamond_set_002` | 6 | 1054956113 | B/A | macro | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 3 | 0 | 0 |
| `diamond_set_002` | 7 | 1831325112 | B/B | free | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `diamond_set_002` | 7 | 1831325112 | B/B | lineage | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `diamond_set_002` | 7 | 1831325112 | B/B | macro | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `diamond_set_002` | 8 | 374607106 | B/B | free | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `diamond_set_002` | 8 | 374607106 | B/B | lineage | B | 1 | 0.74 | 0.260 | 0.300 | inflation | 0.068 | 1 | 12 | 1 | 0 |
| `diamond_set_002` | 8 | 374607106 | B/B | macro | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `diamond_set_002` | 9 | 443947794 | B/B | free | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `diamond_set_002` | 9 | 443947794 | B/B | lineage | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 0 | 1 |
| `diamond_set_002` | 9 | 443947794 | B/B | macro | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `diamond_set_002` | 10 | 533125286 | A/B | free | B | 0 | 0.70 | 0.300 | 0.300 | at_reference | 0.490 | 1 | 12 | 0 | 0 |
| `diamond_set_002` | 10 | 533125286 | A/B | lineage | B | 0 | 0.70 | 0.300 | 0.300 | at_reference | 0.490 | 1 | 12 | 0 | 0 |
| `diamond_set_002` | 10 | 533125286 | A/B | macro | B | 0 | 0.70 | 0.300 | 0.300 | at_reference | 0.490 | 1 | 3 | 0 | 0 |
| `diamond_set_002` | 11 | 633201644 | B/B | free | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 0 | 5 |
| `diamond_set_002` | 11 | 633201644 | B/B | lineage | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `diamond_set_002` | 11 | 633201644 | B/B | macro | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `diamond_set_002` | 12 | 1092129420 | B/A | free | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 12 | 0 | 0 |
| `diamond_set_002` | 12 | 1092129420 | B/A | lineage | A | 0 | 0.78 | 0.780 | 0.700 | inflation | 0.608 | 1 | 12 | 2 | 0 |
| `diamond_set_002` | 12 | 1092129420 | B/A | macro | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 3 | 0 | 0 |
| `dual_root_set_002` | 1 | 1761851777 | A/B/B | free | B | 0 | 0.84 | 0.155 | 0.155 | inflation | 0.714 | 2 | 12 | 0 | 0 |
| `dual_root_set_002` | 1 | 1761851777 | A/B/B | lineage | B | 0 | 0.78 | 0.220 | 0.155 | discount | 0.608 | 2 | 12 | 5 | 1 |
| `dual_root_set_002` | 1 | 1761851777 | A/B/B | macro | B | 0 | 0.78 | 0.220 | 0.155 | discount | 0.608 | 2 | 6 | 1 | 1 |
| `dual_root_set_002` | 2 | 1516256562 | B/A/A | free | A | 0 | 0.84 | 0.845 | 0.845 | inflation | 0.714 | 2 | 12 | 3 | 1 |
| `dual_root_set_002` | 2 | 1516256562 | B/A/A | lineage | A | 0 | 0.93 | 0.930 | 0.845 | inflation | 0.865 | 2 | 12 | 2 | 0 |
| `dual_root_set_002` | 2 | 1516256562 | B/A/A | macro | A | 0 | 0.70 | 0.700 | 0.845 | discount | 0.490 | 2 | 6 | 1 | 0 |
| `dual_root_set_002` | 3 | 1614821534 | B/A/A | free | A | 0 | 0.84 | 0.845 | 0.845 | inflation | 0.714 | 2 | 12 | 0 | 2 |
| `dual_root_set_002` | 3 | 1614821534 | B/A/A | lineage | A | 0 | 0.75 | 0.750 | 0.845 | discount | 0.562 | 2 | 12 | 11 | 1 |
| `dual_root_set_002` | 3 | 1614821534 | B/A/A | macro | A | 0 | 0.86 | 0.860 | 0.845 | inflation | 0.740 | 2 | 6 | 5 | 1 |
| `dual_root_set_002` | 4 | 1943818421 | B/A/B | free | A | 0 | 0.50 | 0.500 | 0.500 | departure_from_even | 0.250 | 2 | 12 | 0 | 2 |
| `dual_root_set_002` | 4 | 1943818421 | B/A/B | lineage | A | 0 | 0.50 | 0.500 | 0.500 | departure_from_even | 0.250 | 2 | 12 | 1 | 0 |
| `dual_root_set_002` | 4 | 1943818421 | B/A/B | macro | A | 0 | 0.52 | 0.520 | 0.500 | departure_from_even | 0.270 | 2 | 6 | 1 | 0 |
| `dual_root_set_002` | 5 | 2082756798 | B/B/B | free | B | 1 | 0.80 | 0.200 | 0.155 | discount | 0.040 | 2 | 12 | 0 | 0 |
| `dual_root_set_002` | 5 | 2082756798 | B/B/B | lineage | B | 1 | 0.70 | 0.300 | 0.155 | discount | 0.090 | 2 | 12 | 3 | 3 |
| `dual_root_set_002` | 5 | 2082756798 | B/B/B | macro | B | 1 | 0.82 | 0.180 | 0.155 | discount | 0.032 | 2 | 6 | 3 | 1 |
| `dual_root_set_002` | 6 | 1068989073 | B/B/B | free | B | 1 | 0.85 | 0.150 | 0.155 | inflation | 0.022 | 2 | 12 | 0 | 0 |
| `dual_root_set_002` | 6 | 1068989073 | B/B/B | lineage | B | 1 | 0.84 | 0.160 | 0.155 | discount | 0.026 | 2 | 12 | 2 | 0 |
| `dual_root_set_002` | 6 | 1068989073 | B/B/B | macro | B | 1 | 0.80 | 0.200 | 0.155 | discount | 0.040 | 2 | 6 | 2 | 0 |
| `dual_root_set_002` | 7 | 1150363503 | B/B/A | free | B | 1 | 0.50 | 0.500 | 0.500 | departure_from_even | 0.250 | 2 | 12 | 0 | 2 |
| `dual_root_set_002` | 7 | 1150363503 | B/B/A | lineage | B | 1 | 0.70 | 0.300 | 0.500 | departure_from_even | 0.090 | 2 | 12 | 2 | 1 |
| `dual_root_set_002` | 7 | 1150363503 | B/B/A | macro | B | 1 | 0.70 | 0.300 | 0.500 | departure_from_even | 0.090 | 2 | 6 | 1 | 1 |
| `dual_root_set_002` | 8 | 1587692757 | A/A/B | free | A | 1 | 0.50 | 0.500 | 0.500 | departure_from_even | 0.250 | 2 | 12 | 2 | 1 |
| `dual_root_set_002` | 8 | 1587692757 | A/A/B | lineage | A | 1 | 0.67 | 0.670 | 0.500 | departure_from_even | 0.109 | 2 | 12 | 4 | 2 |
| `dual_root_set_002` | 8 | 1587692757 | A/A/B | macro | A | 1 | 0.64 | 0.640 | 0.500 | departure_from_even | 0.130 | 2 | 6 | 2 | 1 |
| `dual_root_set_002` | 9 | 1264392180 | A/A/B | free | A | 1 | 0.70 | 0.700 | 0.500 | departure_from_even | 0.090 | 2 | 12 | 4 | 0 |
| `dual_root_set_002` | 9 | 1264392180 | A/A/B | lineage | A | 1 | 0.55 | 0.550 | 0.500 | departure_from_even | 0.203 | 2 | 12 | 3 | 0 |
| `dual_root_set_002` | 9 | 1264392180 | A/A/B | macro | A | 1 | 0.72 | 0.720 | 0.500 | departure_from_even | 0.078 | 2 | 6 | 3 | 0 |
| `dual_root_set_002` | 10 | 2017093923 | A/A/A | free | A | 1 | 0.84 | 0.840 | 0.845 | discount | 0.026 | 2 | 12 | 0 | 0 |
| `dual_root_set_002` | 10 | 2017093923 | A/A/A | lineage | A | 1 | 0.82 | 0.820 | 0.845 | discount | 0.032 | 2 | 12 | 8 | 0 |
| `dual_root_set_002` | 10 | 2017093923 | A/A/A | macro | A | 1 | 0.86 | 0.860 | 0.845 | inflation | 0.020 | 2 | 6 | 4 | 0 |
| `dual_root_set_002` | 11 | 216987976 | A/B/A | free | A | 1 | 0.50 | 0.500 | 0.500 | departure_from_even | 0.250 | 2 | 12 | 0 | 4 |
| `dual_root_set_002` | 11 | 216987976 | A/B/A | lineage | B | 0 | 0.62 | 0.380 | 0.500 | departure_from_even | 0.384 | 2 | 12 | 2 | 1 |
| `dual_root_set_002` | 11 | 216987976 | A/B/A | macro | B | 0 | 0.68 | 0.320 | 0.500 | departure_from_even | 0.462 | 2 | 6 | 2 | 1 |
| `dual_root_set_002` | 12 | 1119880167 | A/B/B | free | B | 0 | 0.84 | 0.155 | 0.155 | inflation | 0.714 | 2 | 12 | 0 | 0 |
| `dual_root_set_002` | 12 | 1119880167 | A/B/B | lineage | B | 0 | 0.85 | 0.150 | 0.155 | inflation | 0.723 | 2 | 12 | 6 | 1 |
| `dual_root_set_002` | 12 | 1119880167 | A/B/B | macro | B | 0 | 0.83 | 0.170 | 0.155 | discount | 0.689 | 2 | 6 | 3 | 1 |
| `dual_root_set_002` | 13 | 1629652161 | A/A/A | free | A | 1 | 0.84 | 0.845 | 0.845 | inflation | 0.024 | 2 | 12 | 0 | 0 |
| `dual_root_set_002` | 13 | 1629652161 | A/A/A | lineage | A | 1 | 0.80 | 0.800 | 0.845 | discount | 0.040 | 2 | 12 | 3 | 1 |
| `dual_root_set_002` | 13 | 1629652161 | A/A/A | macro | A | 1 | 0.84 | 0.845 | 0.845 | inflation | 0.024 | 2 | 6 | 0 | 1 |
| `dual_root_set_002` | 14 | 1322584095 | A/B/A | free | A | 1 | 0.50 | 0.500 | 0.500 | departure_from_even | 0.250 | 2 | 12 | 0 | 2 |
| `dual_root_set_002` | 14 | 1322584095 | A/B/A | lineage | B | 0 | 0.58 | 0.420 | 0.500 | departure_from_even | 0.336 | 2 | 12 | 2 | 1 |
| `dual_root_set_002` | 14 | 1322584095 | A/B/A | macro | A | 1 | 0.50 | 0.500 | 0.500 | departure_from_even | 0.250 | 2 | 6 | 1 | 1 |
| `dual_root_set_002` | 15 | 80913935 | B/A/B | free | A | 0 | 0.50 | 0.500 | 0.500 | departure_from_even | 0.250 | 2 | 12 | 0 | 2 |
| `dual_root_set_002` | 15 | 80913935 | B/A/B | lineage | A | 0 | 0.70 | 0.700 | 0.500 | departure_from_even | 0.490 | 2 | 12 | 3 | 1 |
| `dual_root_set_002` | 15 | 80913935 | B/A/B | macro | A | 0 | 0.50 | 0.500 | 0.500 | departure_from_even | 0.250 | 2 | 6 | 1 | 0 |
| `dual_root_set_002` | 16 | 479525595 | B/B/A | free | A | 0 | 0.50 | 0.500 | 0.500 | departure_from_even | 0.250 | 2 | 12 | 0 | 1 |
| `dual_root_set_002` | 16 | 479525595 | B/B/A | lineage | B | 1 | 0.70 | 0.300 | 0.500 | departure_from_even | 0.090 | 2 | 12 | 3 | 1 |
| `dual_root_set_002` | 16 | 479525595 | B/B/A | macro | B | 1 | 0.70 | 0.300 | 0.500 | departure_from_even | 0.090 | 2 | 6 | 2 | 1 |

## Problems

None.

## Boundary

Descriptive and pre-registered. Rates are counts over events; the only tolerances are those the frozen plan states in words. This stage is reported alone; strata are reported alone. Expectation verdicts restate the plan's 'would be contradicted by' column. The secondary inbound-naming table carries no verdict. Negative results stand.
