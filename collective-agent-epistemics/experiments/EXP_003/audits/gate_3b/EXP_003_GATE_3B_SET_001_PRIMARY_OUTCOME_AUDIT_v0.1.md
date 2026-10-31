# EXP-003 Gate 3B Set 001 Primary-Outcome Audit v0.1

## Status

**COMPLETE**

Descriptive and pre-registered. Rates are counts over events; the only tolerances are those the frozen plan states in words. This stage is reported alone; strata are reported alone. Expectation verdicts restate the plan's 'would be contradicted by' column. The secondary inbound-naming table carries no verdict. Negative results stand.

## Provenance

- Specification: `EXP-003-GATE-3B-PRIMARY-OUTCOME-AUDIT-SPEC-v0.1`
- Plan: `GATE_3B_PLAN_v0.1` (status `FROZEN`, sha256 `5cea3ad5959b1ecfa9080f3bfad834b75366d9841fa6739e965bf69e0036a672`)
- Frozen runtime: `c54563bbb3f17e49c70e8e4f2e3a0369910d3c15`; Gate 3A checkpoint `1daa069af7000613ba06af35714bc22764c1f409`
- Corpus audit: `experiments/EXP_003/audits/gate_3b/EXP_003_GATE_3B_SET_001_CORPUS_AUDIT_v0.1.json` (status PASS, sha256 `69fce27cd911bf884488498e0f1b6e7f08ca52022efbb3528102ae2c85e24dfd`)
- HEAD at audit time: `e58b253f11e1c539e65fc8186fd63b6b82e1b1d3`
- Tolerances: `{"direction": 1e-06, "E1": 0.01, "E2_majority_of_12": 7, "E5": 0.01, "E6": 0.02}`

## Sets

| Set | Topology | Root mode | Probe | Rounds | Worlds | Cells | Strata |
|---|---|---|---|---:|---:|---|---|
| `diamond_set_001` | diamond | single | on | 4 | 12 | A/A: 8, A/B: 1, B/A: 1, B/B: 2 | None: 12 |
| `dual_root_set_001` | diamond | dual | on | 4 | 16 | A/A/A: 2, A/A/B: 2, A/B/A: 2, A/B/B: 2, B/A/A: 2, B/A/B: 2, B/B/A: 2, B/B/B: 2 | agreeing: 8, conflicting: 8 |
| `solo_control_set_003` | solo | single | on | 12 | 12 | A/A: 8, A/B: 1, B/A: 1, B/B: 2 | None: 12 |
| `probe_off_set_001` | diamond | single | off | 4 | 4 | A/A: 2, A/B: 1, B/B: 1 | None: 4 |

## Arm aggregates (d = discount, i = inflation, r = at reference; strata separate)

| Set | Condition | Stratum | D | A post-seed |
|---|---|---|---|---|
| `diamond_set_001` | free | None | 1d/2i/45r of 48; FIS>0 at 0; x̄ +0.003 | 0d/0i/48r of 48; FIS>0 at 0; x̄ +0.000 |
| `diamond_set_001` | lineage | None | 9d/2i/37r of 48; FIS>0 at 0; x̄ -0.011 | 0d/8i/40r of 48; FIS>0 at 8; x̄ +0.015 |
| `dual_root_set_001` | free | agreeing | 14d/18i/0r of 32; FIS>0 at 2; x̄ -0.020 | 16d/16i/0r of 32; FIS>0 at 3; x̄ -0.027 |
| `dual_root_set_001` | free | conflicting | 0d/0i/0r of 32 (+32 even-reference; mean dep -0.049); FIS>0 at 10; x̄ n/a | 0d/0i/0r of 32 (+32 even-reference; mean dep -0.015); FIS>0 at 13; x̄ n/a |
| `dual_root_set_001` | lineage | agreeing | 21d/11i/0r of 32; FIS>0 at 0; x̄ -0.042 | 18d/14i/0r of 32; FIS>0 at 15; x̄ -0.014 |
| `dual_root_set_001` | lineage | conflicting | 0d/0i/0r of 32 (+32 even-reference; mean dep -0.010); FIS>0 at 0; x̄ n/a | 0d/0i/0r of 32 (+32 even-reference; mean dep +0.135); FIS>0 at 10; x̄ n/a |
| `solo_control_set_003` | free | None | n/a | 0d/0i/144r of 144; FIS>0 at 0; x̄ +0.000 |
| `solo_control_set_003` | lineage | None | n/a | 0d/0i/144r of 144; FIS>0 at 0; x̄ +0.000 |
| `probe_off_set_001` | free | None | 0d/2i/14r of 16; FIS>0 at 0; x̄ +0.013 | 0d/0i/16r of 16; FIS>0 at 0; x̄ +0.000 |
| `probe_off_set_001` | lineage | None | 6d/1i/9r of 16; FIS>0 at 0; x̄ -0.021 | 0d/5i/11r of 16; FIS>0 at 5; x̄ +0.023 |

## Pre-registered expectations

| Id | Verdict | Quantities |
|---|---|---|
| E1 | **consistent** | `{"arm1_worlds_with_FREE_D_excess_above_tolerance": 2, "worlds": 12, "tolerance": 0.01}` |
| E2 | **consistent** | `{"worlds_where_LINEAGE_mean_D_excess_exceeds_FREE": 1, "worlds": 12, "majority": 7}` |
| E3 | **contradicted** | `{"by_condition": {"free": {"concordant": 0, "excess_without_FIS": 2, "FIS_without_excess": 0, "D_firings": 48}, "lineage": {"concordant": 0, "excess_without_FIS": 2, "FIS_without_excess": 0, "D_firings": 48}}}` |
| E4 | **contradicted** | `{"by_condition": {"free": {"marked_firings": 16, "excess_rate_marked": 0.0, "clean_firings": 32, "excess_rate_clean": 0.0625}, "lineage": {"marked_firings": 6, "excess_rate_marked": 0.0, "clean_firings": 42, "excess_rate_clean": 0.047619}}}` |
| E5 | **consistent** | `{"agreeing_worlds": 8, "conflicting_worlds": 8, "tolerance": 0.01, "free": {"classes": {"two_root": 22, "single_root": 4, "other": 3, "over": 3}, "modal": "two_root"}, "lineage": {"classes": {"two_root": 14, "single_root": 4, "other": 10, "over": 4}, "modal": "two_root"}, "conflicting_stratum_departure": {"free": -0.049063, "lineage": -0.010313}}` |
| E6 | **contradicted** | `{"comparisons": 8, "gaps_over_tolerance": 4, "tolerance": 0.02}` |
| E7 | **assessed in the synthesis across Set 001 and Set 002, not in a single-stage audit** | `{}` |

## Matrix by world (mean D certainty excess, or mean departure toward E1 for the conflicting stratum)

| Set | Seed | Cell | Stratum | FREE | LINEAGE | FIS>0 FREE / LINEAGE |
|---|---:|---|---|---:|---:|---|
| `diamond_set_001` | 1672462843 | A/A | single | +0.000 | +0.000 | 0 / 0 |
| `diamond_set_001` | 63901144 | A/B | single | +0.000 | -0.015 | 0 / 0 |
| `diamond_set_001` | 323832400 | A/A | single | +0.000 | -0.015 | 0 / 0 |
| `diamond_set_001` | 1566825802 | B/B | single | +0.020 | -0.005 | 0 / 0 |
| `diamond_set_001` | 277459948 | A/A | single | +0.000 | -0.030 | 0 / 0 |
| `diamond_set_001` | 743291108 | A/A | single | +0.000 | -0.030 | 0 / 0 |
| `diamond_set_001` | 2020380812 | B/B | single | +0.020 | -0.013 | 0 / 0 |
| `diamond_set_001` | 1292406070 | A/A | single | -0.007 | -0.013 | 0 / 0 |
| `diamond_set_001` | 187031691 | A/A | single | +0.000 | +0.000 | 0 / 0 |
| `diamond_set_001` | 1476859861 | A/A | single | +0.000 | +0.005 | 0 / 0 |
| `diamond_set_001` | 745425377 | B/A | single | +0.000 | +0.000 | 0 / 0 |
| `diamond_set_001` | 1686133698 | A/A | single | +0.000 | -0.013 | 0 / 0 |
| `dual_root_set_001` | 617684863 | A/A/B | conflicting | dep -0.117 | dep -0.015 | 3 / 0 |
| `dual_root_set_001` | 1230824526 | B/B/B | agreeing | -0.040 | -0.080 | 0 / 0 |
| `dual_root_set_001` | 1430476680 | B/B/B | agreeing | -0.012 | +0.041 | 0 / 0 |
| `dual_root_set_001` | 786534487 | B/A/A | agreeing | -0.075 | -0.029 | 0 / 0 |
| `dual_root_set_001` | 452662356 | B/B/A | conflicting | dep -0.100 | dep -0.050 | 2 / 0 |
| `dual_root_set_001` | 1703800204 | B/A/A | agreeing | -0.021 | -0.075 | 0 / 0 |
| `dual_root_set_001` | 805591371 | A/A/B | conflicting | dep -0.055 | dep -0.005 | 0 / 0 |
| `dual_root_set_001` | 2105050229 | B/B/A | conflicting | dep +0.000 | dep +0.033 | 0 / 0 |
| `dual_root_set_001` | 503343741 | A/B/A | conflicting | dep -0.050 | dep +0.000 | 1 / 0 |
| `dual_root_set_001` | 1074206943 | A/A/A | agreeing | +0.000 | -0.024 | 0 / 0 |
| `dual_root_set_001` | 1975068904 | B/A/B | conflicting | dep -0.043 | dep -0.033 | 1 / 0 |
| `dual_root_set_001` | 1617711318 | A/B/B | agreeing | +0.000 | -0.045 | 0 / 0 |
| `dual_root_set_001` | 264003842 | A/B/A | conflicting | dep +0.000 | dep -0.013 | 0 / 0 |
| `dual_root_set_001` | 153299879 | B/A/B | conflicting | dep -0.028 | dep +0.000 | 3 / 0 |
| `dual_root_set_001` | 2036696995 | A/A/A | agreeing | -0.024 | -0.099 | 1 / 0 |
| `dual_root_set_001` | 2106030015 | A/B/B | agreeing | +0.014 | -0.031 | 1 / 0 |

## Probe reactivity (Arm 4 vs Arm 1, shared worlds)

| Seed | Condition | Probe on | Probe off | Gap | Within .02 |
|---:|---|---:|---:|---:|---|
| 1672462843 | free | +0.000 | +0.000 | +0.000 | yes |
| 1672462843 | lineage | +0.000 | -0.045 | +0.045 | no |
| 63901144 | free | +0.000 | +0.050 | +0.050 | no |
| 63901144 | lineage | -0.015 | +0.010 | +0.025 | no |
| 323832400 | free | +0.000 | +0.000 | +0.000 | yes |
| 323832400 | lineage | -0.015 | -0.050 | +0.035 | no |
| 1566825802 | free | +0.020 | +0.000 | +0.020 | yes |
| 1566825802 | lineage | -0.005 | +0.000 | +0.005 | yes |

## Solo control (probe on)

| Seed | Condition | certainty excess per firing | Any deviation | FIS>0 |
|---:|---|---|---|---:|
| 1672462843 | free | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 1672462843 | lineage | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 63901144 | free | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 63901144 | lineage | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 323832400 | free | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 323832400 | lineage | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 1566825802 | free | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 1566825802 | lineage | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 277459948 | free | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 277459948 | lineage | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 743291108 | free | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 743291108 | lineage | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 2020380812 | free | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 2020380812 | lineage | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 1292406070 | free | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 1292406070 | lineage | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 187031691 | free | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 187031691 | lineage | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 1476859861 | free | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 1476859861 | lineage | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 745425377 | free | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 745425377 | lineage | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 1686133698 | free | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |
| 1686133698 | lineage | +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000, +0.000 | no | 0 |

## Secondary: inbound messages naming the sensor (descriptive, no verdict)

| Set | Condition | Stratum | Position | Inbound naming the sensor | Counts |
|---|---|---|---|---:|---|
| `diamond_set_001` | free | None | D | 0 | 0d/0i/14r of 14; FIS>0 at 0; x̄ +0.000 |
| `diamond_set_001` | free | None | D | 1 | 0d/0i/3r of 3; FIS>0 at 0; x̄ +0.000 |
| `diamond_set_001` | free | None | D | 2 | 1d/2i/28r of 31; FIS>0 at 0; x̄ +0.004 |
| `diamond_set_001` | free | None | A | 0 | 0d/0i/15r of 15; FIS>0 at 0; x̄ +0.000 |
| `diamond_set_001` | free | None | A | 1 | 0d/0i/33r of 33; FIS>0 at 0; x̄ +0.000 |
| `diamond_set_001` | lineage | None | D | 0 | 8d/1i/14r of 23; FIS>0 at 0; x̄ -0.022 |
| `diamond_set_001` | lineage | None | D | 1 | 0d/1i/2r of 3; FIS>0 at 0; x̄ +0.007 |
| `diamond_set_001` | lineage | None | D | 2 | 1d/0i/21r of 22; FIS>0 at 0; x̄ -0.001 |
| `diamond_set_001` | lineage | None | A | 0 | 0d/8i/18r of 26; FIS>0 at 8; x̄ +0.028 |
| `diamond_set_001` | lineage | None | A | 1 | 0d/0i/22r of 22; FIS>0 at 0; x̄ +0.000 |
| `dual_root_set_001` | free | agreeing | D | 0 | 0d/1i/0r of 1; FIS>0 at 0; x̄ +0.000 |
| `dual_root_set_001` | free | agreeing | D | 1 | 4d/5i/0r of 9; FIS>0 at 0; x̄ -0.033 |
| `dual_root_set_001` | free | agreeing | D | 2 | 10d/12i/0r of 22; FIS>0 at 2; x̄ -0.015 |
| `dual_root_set_001` | free | agreeing | A | 0 | 3d/4i/0r of 7; FIS>0 at 1; x̄ -0.014 |
| `dual_root_set_001` | free | agreeing | A | 1 | 13d/12i/0r of 25; FIS>0 at 2; x̄ -0.030 |
| `dual_root_set_001` | free | conflicting | D | 0 | 0d/0i/0r of 6 (+6 even-reference; mean dep -0.095); FIS>0 at 3; x̄ n/a |
| `dual_root_set_001` | free | conflicting | D | 1 | 0d/0i/0r of 15 (+15 even-reference; mean dep -0.059); FIS>0 at 4; x̄ n/a |
| `dual_root_set_001` | free | conflicting | D | 2 | 0d/0i/0r of 11 (+11 even-reference; mean dep -0.010); FIS>0 at 3; x̄ n/a |
| `dual_root_set_001` | free | conflicting | A | 0 | 0d/0i/0r of 17 (+17 even-reference; mean dep -0.016); FIS>0 at 9; x̄ n/a |
| `dual_root_set_001` | free | conflicting | A | 1 | 0d/0i/0r of 15 (+15 even-reference; mean dep -0.014); FIS>0 at 4; x̄ n/a |
| `dual_root_set_001` | lineage | agreeing | D | 0 | 2d/0i/0r of 2; FIS>0 at 0; x̄ -0.005 |
| `dual_root_set_001` | lineage | agreeing | D | 1 | 7d/5i/0r of 12; FIS>0 at 0; x̄ -0.049 |
| `dual_root_set_001` | lineage | agreeing | D | 2 | 12d/6i/0r of 18; FIS>0 at 0; x̄ -0.043 |
| `dual_root_set_001` | lineage | agreeing | A | 0 | 6d/10i/0r of 16; FIS>0 at 14; x̄ +0.021 |
| `dual_root_set_001` | lineage | agreeing | A | 1 | 12d/4i/0r of 16; FIS>0 at 1; x̄ -0.048 |
| `dual_root_set_001` | lineage | conflicting | D | 0 | 0d/0i/0r of 2 (+2 even-reference; mean dep -0.025); FIS>0 at 0; x̄ n/a |
| `dual_root_set_001` | lineage | conflicting | D | 1 | 0d/0i/0r of 17 (+17 even-reference; mean dep -0.015); FIS>0 at 0; x̄ n/a |
| `dual_root_set_001` | lineage | conflicting | D | 2 | 0d/0i/0r of 13 (+13 even-reference; mean dep -0.002); FIS>0 at 0; x̄ n/a |
| `dual_root_set_001` | lineage | conflicting | A | 0 | 0d/0i/0r of 21 (+21 even-reference; mean dep +0.189); FIS>0 at 10; x̄ n/a |
| `dual_root_set_001` | lineage | conflicting | A | 1 | 0d/0i/0r of 11 (+11 even-reference; mean dep +0.032); FIS>0 at 0; x̄ n/a |
| `probe_off_set_001` | free | None | D | 0 | 0d/0i/4r of 4; FIS>0 at 0; x̄ +0.000 |
| `probe_off_set_001` | free | None | D | 2 | 0d/2i/10r of 12; FIS>0 at 0; x̄ +0.017 |
| `probe_off_set_001` | free | None | A | 0 | 0d/0i/4r of 4; FIS>0 at 0; x̄ +0.000 |
| `probe_off_set_001` | free | None | A | 1 | 0d/0i/12r of 12; FIS>0 at 0; x̄ +0.000 |
| `probe_off_set_001` | lineage | None | D | 0 | 5d/1i/4r of 10; FIS>0 at 0; x̄ -0.029 |
| `probe_off_set_001` | lineage | None | D | 2 | 1d/0i/5r of 6; FIS>0 at 0; x̄ -0.008 |
| `probe_off_set_001` | lineage | None | A | 0 | 0d/5i/5r of 10; FIS>0 at 5; x̄ +0.037 |
| `probe_off_set_001` | lineage | None | A | 1 | 0d/0i/6r of 6; FIS>0 at 0; x̄ +0.000 |

## MACRO stopping boundary

| Set | Seed | Stop event | MACRO events | Stop triggered | Responses reused |
|---|---:|---|---:|---|---|
| `diamond_set_001` | 1672462843 | M05 | 5 | True | True |
| `diamond_set_001` | 63901144 | M05 | 5 | True | True |
| `diamond_set_001` | 323832400 | M05 | 5 | True | True |
| `diamond_set_001` | 1566825802 | M05 | 5 | True | True |
| `diamond_set_001` | 277459948 | M05 | 5 | True | True |
| `diamond_set_001` | 743291108 | M05 | 5 | True | True |
| `diamond_set_001` | 2020380812 | M05 | 5 | True | True |
| `diamond_set_001` | 1292406070 | M05 | 5 | True | True |
| `diamond_set_001` | 187031691 | M05 | 5 | True | True |
| `diamond_set_001` | 1476859861 | M05 | 5 | True | True |
| `diamond_set_001` | 745425377 | M05 | 5 | True | True |
| `diamond_set_001` | 1686133698 | M05 | 5 | True | True |
| `dual_root_set_001` | 617684863 | M09 | 9 | True | True |
| `dual_root_set_001` | 1230824526 | M09 | 9 | True | True |
| `dual_root_set_001` | 1430476680 | M09 | 9 | True | True |
| `dual_root_set_001` | 786534487 | M09 | 9 | True | True |
| `dual_root_set_001` | 452662356 | M09 | 9 | True | True |
| `dual_root_set_001` | 1703800204 | M09 | 9 | True | True |
| `dual_root_set_001` | 805591371 | M09 | 9 | True | True |
| `dual_root_set_001` | 2105050229 | M09 | 9 | True | True |
| `dual_root_set_001` | 503343741 | M09 | 9 | True | True |
| `dual_root_set_001` | 1074206943 | M09 | 9 | True | True |
| `dual_root_set_001` | 1975068904 | M09 | 9 | True | True |
| `dual_root_set_001` | 1617711318 | M09 | 9 | True | True |
| `dual_root_set_001` | 264003842 | M09 | 9 | True | True |
| `dual_root_set_001` | 153299879 | M09 | 9 | True | True |
| `dual_root_set_001` | 2036696995 | M09 | 9 | True | True |
| `dual_root_set_001` | 2106030015 | M09 | 9 | True | True |
| `solo_control_set_003` | 1672462843 | M02 | 2 | True | True |
| `solo_control_set_003` | 63901144 | M02 | 2 | True | True |
| `solo_control_set_003` | 323832400 | M02 | 2 | True | True |
| `solo_control_set_003` | 1566825802 | M02 | 2 | True | True |
| `solo_control_set_003` | 277459948 | M02 | 2 | True | True |
| `solo_control_set_003` | 743291108 | M02 | 2 | True | True |
| `solo_control_set_003` | 2020380812 | M02 | 2 | True | True |
| `solo_control_set_003` | 1292406070 | M02 | 2 | True | True |
| `solo_control_set_003` | 187031691 | M02 | 2 | True | True |
| `solo_control_set_003` | 1476859861 | M02 | 2 | True | True |
| `solo_control_set_003` | 745425377 | M02 | 2 | True | True |
| `solo_control_set_003` | 1686133698 | M02 | 2 | True | True |
| `probe_off_set_001` | 1672462843 | M05 | 5 | True | True |
| `probe_off_set_001` | 63901144 | M05 | 5 | True | True |
| `probe_off_set_001` | 323832400 | M05 | 5 | True | True |
| `probe_off_set_001` | 1566825802 | M05 | 5 | True | True |

## Primary outcome table by world (EXP-002 family)

| Set | Order | Seed | Cell | Condition | Final | Acc | Conf | P(A) | Ref | Kind | Brier | Roots | Depth | FIS>0 | agent-as-source |
|---|---:|---:|---|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|
| `diamond_set_001` | 1 | 1672462843 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `diamond_set_001` | 1 | 1672462843 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `diamond_set_001` | 1 | 1672462843 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `diamond_set_001` | 2 | 63901144 | A/B | free | B | 0 | 0.70 | 0.300 | 0.300 | at_reference | 0.490 | 1 | 12 | 0 | 5 |
| `diamond_set_001` | 2 | 63901144 | A/B | lineage | B | 0 | 0.78 | 0.220 | 0.300 | inflation | 0.608 | 1 | 12 | 1 | 0 |
| `diamond_set_001` | 2 | 63901144 | A/B | macro | B | 0 | 0.70 | 0.300 | 0.300 | at_reference | 0.490 | 1 | 3 | 0 | 0 |
| `diamond_set_001` | 3 | 323832400 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 1 |
| `diamond_set_001` | 3 | 323832400 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 1 | 0 |
| `diamond_set_001` | 3 | 323832400 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `diamond_set_001` | 4 | 1566825802 | B/B | free | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 0 | 2 |
| `diamond_set_001` | 4 | 1566825802 | B/B | lineage | B | 1 | 0.74 | 0.260 | 0.300 | inflation | 0.068 | 1 | 12 | 1 | 1 |
| `diamond_set_001` | 4 | 1566825802 | B/B | macro | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `diamond_set_001` | 5 | 277459948 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 5 |
| `diamond_set_001` | 5 | 277459948 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `diamond_set_001` | 5 | 277459948 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `diamond_set_001` | 6 | 743291108 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 1 |
| `diamond_set_001` | 6 | 743291108 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `diamond_set_001` | 6 | 743291108 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `diamond_set_001` | 7 | 2020380812 | B/B | free | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 0 | 1 |
| `diamond_set_001` | 7 | 2020380812 | B/B | lineage | B | 1 | 0.75 | 0.250 | 0.300 | inflation | 0.062 | 1 | 12 | 1 | 1 |
| `diamond_set_001` | 7 | 2020380812 | B/B | macro | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `diamond_set_001` | 8 | 1292406070 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 5 |
| `diamond_set_001` | 8 | 1292406070 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 1 | 0 |
| `diamond_set_001` | 8 | 1292406070 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `diamond_set_001` | 9 | 187031691 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 2 |
| `diamond_set_001` | 9 | 187031691 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 1 | 2 |
| `diamond_set_001` | 9 | 187031691 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `diamond_set_001` | 10 | 1476859861 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `diamond_set_001` | 10 | 1476859861 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `diamond_set_001` | 10 | 1476859861 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `diamond_set_001` | 11 | 745425377 | B/A | free | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 12 | 0 | 4 |
| `diamond_set_001` | 11 | 745425377 | B/A | lineage | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 12 | 0 | 2 |
| `diamond_set_001` | 11 | 745425377 | B/A | macro | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 3 | 0 | 1 |
| `diamond_set_001` | 12 | 1686133698 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `diamond_set_001` | 12 | 1686133698 | A/A | lineage | A | 1 | 0.84 | 0.840 | 0.700 | inflation | 0.026 | 1 | 12 | 2 | 1 |
| `diamond_set_001` | 12 | 1686133698 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `dual_root_set_001` | 1 | 617684863 | A/A/B | free | B | 0 | 0.60 | 0.400 | 0.500 | departure_from_even | 0.360 | 2 | 12 | 12 | 1 |
| `dual_root_set_001` | 1 | 617684863 | A/A/B | lineage | A | 1 | 0.62 | 0.620 | 0.500 | departure_from_even | 0.144 | 2 | 12 | 2 | 0 |
| `dual_root_set_001` | 1 | 617684863 | A/A/B | macro | A | 1 | 0.70 | 0.700 | 0.500 | departure_from_even | 0.090 | 2 | 6 | 1 | 0 |
| `dual_root_set_001` | 2 | 1230824526 | B/B/B | free | B | 1 | 0.70 | 0.300 | 0.155 | discount | 0.090 | 2 | 12 | 0 | 0 |
| `dual_root_set_001` | 2 | 1230824526 | B/B/B | lineage | B | 1 | 0.90 | 0.100 | 0.155 | inflation | 0.010 | 2 | 12 | 5 | 0 |
| `dual_root_set_001` | 2 | 1230824526 | B/B/B | macro | B | 1 | 0.90 | 0.100 | 0.155 | inflation | 0.010 | 2 | 6 | 1 | 0 |
| `dual_root_set_001` | 3 | 1430476680 | B/B/B | free | B | 1 | 0.84 | 0.155 | 0.155 | inflation | 0.024 | 2 | 12 | 0 | 0 |
| `dual_root_set_001` | 3 | 1430476680 | B/B/B | lineage | B | 1 | 0.85 | 0.150 | 0.155 | inflation | 0.022 | 2 | 12 | 5 | 1 |
| `dual_root_set_001` | 3 | 1430476680 | B/B/B | macro | B | 1 | 0.70 | 0.300 | 0.155 | discount | 0.090 | 2 | 6 | 2 | 1 |
| `dual_root_set_001` | 4 | 786534487 | B/A/A | free | A | 0 | 0.84 | 0.840 | 0.845 | discount | 0.706 | 2 | 12 | 0 | 0 |
| `dual_root_set_001` | 4 | 786534487 | B/A/A | lineage | A | 0 | 0.82 | 0.820 | 0.845 | discount | 0.672 | 2 | 12 | 2 | 0 |
| `dual_root_set_001` | 4 | 786534487 | B/A/A | macro | A | 0 | 0.78 | 0.780 | 0.845 | discount | 0.608 | 2 | 6 | 0 | 0 |
| `dual_root_set_001` | 5 | 452662356 | B/B/A | free | A | 0 | 0.70 | 0.700 | 0.500 | departure_from_even | 0.490 | 2 | 12 | 7 | 3 |
| `dual_root_set_001` | 5 | 452662356 | B/B/A | lineage | B | 1 | 0.50 | 0.500 | 0.500 | departure_from_even | 0.250 | 2 | 12 | 1 | 0 |
| `dual_root_set_001` | 5 | 452662356 | B/B/A | macro | B | 1 | 0.70 | 0.300 | 0.500 | departure_from_even | 0.090 | 2 | 6 | 1 | 0 |
| `dual_root_set_001` | 6 | 1703800204 | B/A/A | free | A | 0 | 0.85 | 0.850 | 0.845 | inflation | 0.723 | 2 | 12 | 0 | 0 |
| `dual_root_set_001` | 6 | 1703800204 | B/A/A | lineage | A | 0 | 0.80 | 0.800 | 0.845 | discount | 0.640 | 2 | 12 | 1 | 0 |
| `dual_root_set_001` | 6 | 1703800204 | B/A/A | macro | A | 0 | 0.76 | 0.760 | 0.845 | discount | 0.578 | 2 | 6 | 1 | 0 |
| `dual_root_set_001` | 7 | 805591371 | A/A/B | free | B | 0 | 0.58 | 0.420 | 0.500 | departure_from_even | 0.336 | 2 | 12 | 0 | 3 |
| `dual_root_set_001` | 7 | 805591371 | A/A/B | lineage | B | 0 | 0.51 | 0.490 | 0.500 | departure_from_even | 0.260 | 2 | 12 | 2 | 0 |
| `dual_root_set_001` | 7 | 805591371 | A/A/B | macro | A | 1 | 0.70 | 0.700 | 0.500 | departure_from_even | 0.090 | 2 | 6 | 1 | 0 |
| `dual_root_set_001` | 8 | 2105050229 | B/B/A | free | A | 0 | 0.50 | 0.500 | 0.500 | departure_from_even | 0.250 | 2 | 12 | 1 | 1 |
| `dual_root_set_001` | 8 | 2105050229 | B/B/A | lineage | B | 1 | 0.71 | 0.290 | 0.500 | departure_from_even | 0.084 | 2 | 12 | 4 | 1 |
| `dual_root_set_001` | 8 | 2105050229 | B/B/A | macro | B | 1 | 0.62 | 0.380 | 0.500 | departure_from_even | 0.144 | 2 | 6 | 1 | 0 |
| `dual_root_set_001` | 9 | 503343741 | A/B/A | free | A | 1 | 0.70 | 0.700 | 0.500 | departure_from_even | 0.090 | 2 | 12 | 3 | 1 |
| `dual_root_set_001` | 9 | 503343741 | A/B/A | lineage | A | 1 | 0.50 | 0.500 | 0.500 | departure_from_even | 0.250 | 2 | 12 | 3 | 0 |
| `dual_root_set_001` | 9 | 503343741 | A/B/A | macro | B | 0 | 0.70 | 0.300 | 0.500 | departure_from_even | 0.490 | 2 | 6 | 3 | 0 |
| `dual_root_set_001` | 10 | 1074206943 | A/A/A | free | A | 1 | 0.84 | 0.845 | 0.845 | inflation | 0.024 | 2 | 12 | 1 | 2 |
| `dual_root_set_001` | 10 | 1074206943 | A/A/A | lineage | A | 1 | 0.93 | 0.930 | 0.845 | inflation | 0.005 | 2 | 12 | 1 | 0 |
| `dual_root_set_001` | 10 | 1074206943 | A/A/A | macro | A | 1 | 0.84 | 0.840 | 0.845 | discount | 0.026 | 2 | 6 | 0 | 0 |
| `dual_root_set_001` | 11 | 1975068904 | B/A/B | free | B | 1 | 0.70 | 0.300 | 0.500 | departure_from_even | 0.090 | 2 | 12 | 3 | 3 |
| `dual_root_set_001` | 11 | 1975068904 | B/A/B | lineage | A | 0 | 0.70 | 0.700 | 0.500 | departure_from_even | 0.490 | 2 | 12 | 0 | 0 |
| `dual_root_set_001` | 11 | 1975068904 | B/A/B | macro | A | 0 | 0.70 | 0.700 | 0.500 | departure_from_even | 0.490 | 2 | 6 | 0 | 0 |
| `dual_root_set_001` | 12 | 1617711318 | A/B/B | free | B | 0 | 0.80 | 0.200 | 0.155 | discount | 0.640 | 2 | 12 | 0 | 0 |
| `dual_root_set_001` | 12 | 1617711318 | A/B/B | lineage | B | 0 | 0.84 | 0.160 | 0.155 | discount | 0.706 | 2 | 12 | 3 | 1 |
| `dual_root_set_001` | 12 | 1617711318 | A/B/B | macro | B | 0 | 0.82 | 0.180 | 0.155 | discount | 0.672 | 2 | 6 | 2 | 1 |
| `dual_root_set_001` | 13 | 264003842 | A/B/A | free | A | 1 | 0.50 | 0.500 | 0.500 | departure_from_even | 0.250 | 2 | 12 | 0 | 1 |
| `dual_root_set_001` | 13 | 264003842 | A/B/A | lineage | B | 0 | 0.58 | 0.420 | 0.500 | departure_from_even | 0.336 | 2 | 12 | 1 | 1 |
| `dual_root_set_001` | 13 | 264003842 | A/B/A | macro | B | 0 | 0.56 | 0.440 | 0.500 | departure_from_even | 0.314 | 2 | 6 | 1 | 0 |
| `dual_root_set_001` | 14 | 153299879 | B/A/B | free | B | 1 | 0.53 | 0.470 | 0.500 | departure_from_even | 0.221 | 2 | 12 | 13 | 1 |
| `dual_root_set_001` | 14 | 153299879 | B/A/B | lineage | A | 0 | 0.70 | 0.700 | 0.500 | departure_from_even | 0.490 | 2 | 12 | 1 | 2 |
| `dual_root_set_001` | 14 | 153299879 | B/A/B | macro | A | 0 | 0.70 | 0.700 | 0.500 | departure_from_even | 0.490 | 2 | 6 | 1 | 0 |
| `dual_root_set_001` | 15 | 2036696995 | A/A/A | free | A | 1 | 0.84 | 0.845 | 0.845 | inflation | 0.024 | 2 | 12 | 7 | 1 |
| `dual_root_set_001` | 15 | 2036696995 | A/A/A | lineage | A | 1 | 0.80 | 0.800 | 0.845 | discount | 0.040 | 2 | 12 | 6 | 1 |
| `dual_root_set_001` | 15 | 2036696995 | A/A/A | macro | A | 1 | 0.85 | 0.850 | 0.845 | inflation | 0.022 | 2 | 6 | 2 | 1 |
| `dual_root_set_001` | 16 | 2106030015 | A/B/B | free | B | 0 | 0.90 | 0.100 | 0.155 | inflation | 0.810 | 2 | 12 | 3 | 1 |
| `dual_root_set_001` | 16 | 2106030015 | A/B/B | lineage | B | 0 | 0.82 | 0.180 | 0.155 | discount | 0.672 | 2 | 12 | 3 | 0 |
| `dual_root_set_001` | 16 | 2106030015 | A/B/B | macro | B | 0 | 0.70 | 0.300 | 0.155 | discount | 0.490 | 2 | 6 | 2 | 0 |
| `solo_control_set_003` | 1 | 1672462843 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 1 | 1672462843 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 1 | 1672462843 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 1 | 0 | 0 |
| `solo_control_set_003` | 2 | 63901144 | A/B | free | B | 0 | 0.70 | 0.300 | 0.300 | at_reference | 0.490 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 2 | 63901144 | A/B | lineage | B | 0 | 0.70 | 0.300 | 0.300 | at_reference | 0.490 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 2 | 63901144 | A/B | macro | B | 0 | 0.70 | 0.300 | 0.300 | at_reference | 0.490 | 1 | 1 | 0 | 0 |
| `solo_control_set_003` | 3 | 323832400 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 3 | 323832400 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 3 | 323832400 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 1 | 0 | 0 |
| `solo_control_set_003` | 4 | 1566825802 | B/B | free | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 4 | 1566825802 | B/B | lineage | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 4 | 1566825802 | B/B | macro | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 1 | 0 | 0 |
| `solo_control_set_003` | 5 | 277459948 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 5 | 277459948 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 5 | 277459948 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 1 | 0 | 0 |
| `solo_control_set_003` | 6 | 743291108 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 6 | 743291108 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 6 | 743291108 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 1 | 0 | 0 |
| `solo_control_set_003` | 7 | 2020380812 | B/B | free | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 7 | 2020380812 | B/B | lineage | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 7 | 2020380812 | B/B | macro | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 1 | 0 | 0 |
| `solo_control_set_003` | 8 | 1292406070 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 8 | 1292406070 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 8 | 1292406070 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 1 | 0 | 0 |
| `solo_control_set_003` | 9 | 187031691 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 9 | 187031691 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 9 | 187031691 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 1 | 0 | 0 |
| `solo_control_set_003` | 10 | 1476859861 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 10 | 1476859861 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 10 | 1476859861 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 1 | 0 | 0 |
| `solo_control_set_003` | 11 | 745425377 | B/A | free | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 11 | 745425377 | B/A | lineage | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 11 | 745425377 | B/A | macro | A | 0 | 0.70 | 0.700 | 0.700 | at_reference | 0.490 | 1 | 1 | 0 | 0 |
| `solo_control_set_003` | 12 | 1686133698 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 12 | 1686133698 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `solo_control_set_003` | 12 | 1686133698 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 1 | 0 | 0 |
| `probe_off_set_001` | 1 | 1672462843 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 2 |
| `probe_off_set_001` | 1 | 1672462843 | A/A | lineage | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 1 | 0 |
| `probe_off_set_001` | 1 | 1672462843 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `probe_off_set_001` | 2 | 63901144 | A/B | free | B | 0 | 0.70 | 0.300 | 0.300 | at_reference | 0.490 | 1 | 12 | 0 | 0 |
| `probe_off_set_001` | 2 | 63901144 | A/B | lineage | B | 0 | 0.78 | 0.220 | 0.300 | inflation | 0.608 | 1 | 12 | 1 | 4 |
| `probe_off_set_001` | 2 | 63901144 | A/B | macro | B | 0 | 0.70 | 0.300 | 0.300 | at_reference | 0.490 | 1 | 3 | 0 | 0 |
| `probe_off_set_001` | 3 | 323832400 | A/A | free | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 12 | 0 | 0 |
| `probe_off_set_001` | 3 | 323832400 | A/A | lineage | A | 1 | 0.76 | 0.760 | 0.700 | inflation | 0.058 | 1 | 12 | 2 | 0 |
| `probe_off_set_001` | 3 | 323832400 | A/A | macro | A | 1 | 0.70 | 0.700 | 0.700 | at_reference | 0.090 | 1 | 3 | 0 | 0 |
| `probe_off_set_001` | 4 | 1566825802 | B/B | free | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 0 | 3 |
| `probe_off_set_001` | 4 | 1566825802 | B/B | lineage | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 12 | 1 | 1 |
| `probe_off_set_001` | 4 | 1566825802 | B/B | macro | B | 1 | 0.70 | 0.300 | 0.300 | at_reference | 0.090 | 1 | 3 | 0 | 0 |

## Problems

None.

## Boundary

Descriptive and pre-registered. Rates are counts over events; the only tolerances are those the frozen plan states in words. This stage is reported alone; strata are reported alone. Expectation verdicts restate the plan's 'would be contradicted by' column. The secondary inbound-naming table carries no verdict. Negative results stand.
