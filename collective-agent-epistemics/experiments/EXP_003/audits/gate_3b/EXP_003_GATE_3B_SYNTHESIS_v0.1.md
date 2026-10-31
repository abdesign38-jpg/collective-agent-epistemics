# EXP-003 Gate 3B Synthesis v0.1

## Status

**SYNTHESIS** (mechanical, cross-stage)

Mechanical cross-stage placement of two pre-registered audits. No pooling of stages or strata, no test, no threshold beyond the spec's E7 flat band, no causal claim. The Gate 3A placement is secondary and carries no verdict. The relation to the hypothesis is written separately under research/observations/.

## Sources

- set_001: `experiments/EXP_003/audits/gate_3b/EXP_003_GATE_3B_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1.json` (sha256 `6b2fd641bd8a91c3b94707648e1e6360e535a1ff93bc80a4fb00186f0724ff5d`)
- set_001_corpus: `experiments/EXP_003/audits/gate_3b/EXP_003_GATE_3B_SET_001_CORPUS_AUDIT_v0.1.json` (sha256 `69fce27cd911bf884488498e0f1b6e7f08ca52022efbb3528102ae2c85e24dfd`)
- set_002: `experiments/EXP_003/audits/gate_3b/EXP_003_GATE_3B_SET_002_PRIMARY_OUTCOME_AUDIT_v0.1.json` (sha256 `75b231927edd76cc104331b1ac9157b5ddeaea834bf3cf5c66acd642ae5ddda4`)
- set_002_corpus: `experiments/EXP_003/audits/gate_3b/EXP_003_GATE_3B_SET_002_CORPUS_AUDIT_v0.1.json` (sha256 `1ad6ffa30765eb8ecad65133dc5f9fd9e7558f87ca9962bbd2384c16aa7116c1`)
- gate3a_set_001: `experiments/EXP_003/audits/gate_3a/EXP_003_GATE_3A_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1.json` (sha256 `f43e47fc82867184ad2782f1f14e03510ce3334168ba52e2cd82c96adba37367`)
- gate3a_set_002: `experiments/EXP_003/audits/gate_3a/EXP_003_GATE_3A_SET_002_PRIMARY_OUTCOME_AUDIT_v0.1.json` (sha256 `c3a1ccd9ea0d9c2e13f1ad621d269de608134ad87de67db552087eba72ad3cc1`)
- HEAD at synthesis time: `62761dde2337980960e06276f564e1d5e8d54745`

## Pre-registered expectations, both stages

| Id | set_001 | set_002 | Agree |
|---|---|---|---|
| E1 | **consistent** | **consistent** | yes |
| E2 | **consistent** | **consistent** | yes |
| E3 | **contradicted** | **contradicted** | yes |
| E4 | **contradicted** | **contradicted** | yes |
| E5 | **consistent** | **consistent** | yes |
| E6 | **contradicted** | **not assessable** | no |
| E7 | cross-stage | cross-stage | **consistent** |

E7 by matrix cell (stage mean of the cell quantity; flat band ±0.005):

| Cell | Quantity | set_001 | set_002 | Signs | Reversed |
|---|---|---:|---:|---|---|
| Arm 1 FREE | mean_certainty_excess | +0.003 | +0.008 | flat / positive | no |
| Arm 1 LINEAGE | mean_certainty_excess | -0.011 | -0.006 | negative / negative | no |
| Arm 2 agreeing FREE | mean_certainty_excess | -0.020 | -0.026 | negative / negative | no |
| Arm 2 agreeing LINEAGE | mean_certainty_excess | -0.042 | -0.043 | negative / negative | no |
| Arm 2 conflicting FREE | mean_departure_toward_e1 | -0.049 | -0.018 | negative / negative | no |
| Arm 2 conflicting LINEAGE | mean_departure_toward_e1 | -0.010 | -0.008 | negative / negative | no |

Quantities behind each stage verdict:

- E1 set_001: `{"arm1_worlds_with_FREE_D_excess_above_tolerance": 2, "worlds": 12, "tolerance": 0.01}`
- E1 set_002: `{"arm1_worlds_with_FREE_D_excess_above_tolerance": 4, "worlds": 12, "tolerance": 0.01}`
- E2 set_001: `{"worlds_where_LINEAGE_mean_D_excess_exceeds_FREE": 1, "worlds": 12, "majority": 7}`
- E2 set_002: `{"worlds_where_LINEAGE_mean_D_excess_exceeds_FREE": 2, "worlds": 12, "majority": 7}`
- E3 set_001: `{"by_condition": {"free": {"concordant": 0, "excess_without_FIS": 2, "FIS_without_excess": 0, "D_firings": 48}, "lineage": {"concordant": 0, "excess_without_FIS": 2, "FIS_without_excess": 0, "D_firings": 48}}}`
- E3 set_002: `{"by_condition": {"free": {"concordant": 0, "excess_without_FIS": 5, "FIS_without_excess": 0, "D_firings": 48}, "lineage": {"concordant": 0, "excess_without_FIS": 3, "FIS_without_excess": 0, "D_firings": 48}}}`
- E4 set_001: `{"by_condition": {"free": {"marked_firings": 16, "excess_rate_marked": 0.0, "clean_firings": 32, "excess_rate_clean": 0.0625}, "lineage": {"marked_firings": 6, "excess_rate_marked": 0.0, "clean_firings": 42, "excess_rate_clean": 0.047619}}}`
- E4 set_002: `{"by_condition": {"free": {"marked_firings": 9, "excess_rate_marked": 0.0, "clean_firings": 39, "excess_rate_clean": 0.128205}, "lineage": {"marked_firings": 5, "excess_rate_marked": 0.2, "clean_firings": 43, "excess_rate_clean": 0.046512}}}`
- E5 set_001: `{"agreeing_worlds": 8, "conflicting_worlds": 8, "tolerance": 0.01, "free": {"classes": {"two_root": 22, "single_root": 4, "other": 3, "over": 3}, "modal": "two_root"}, "lineage": {"classes": {"two_root": 14, "single_root": 4, "other": 10, "over": 4}, "modal": "two_root"}, "conflicting_stratum_departure": {"free": -0.049063, "lineage": -0.010313}}`
- E5 set_002: `{"agreeing_worlds": 8, "conflicting_worlds": 8, "tolerance": 0.01, "free": {"classes": {"two_root": 23, "single_root": 5, "other": 3, "over": 1}, "modal": "two_root"}, "lineage": {"classes": {"two_root": 12, "other": 13, "single_root": 4, "over": 3}, "modal": "other"}, "conflicting_stratum_departure": {"free": -0.0175, "lineage": -0.007812}}`
- E6 set_001: `{"comparisons": 8, "gaps_over_tolerance": 4, "tolerance": 0.02}`
- E6 set_002: `{}`

## Arm aggregates by stage (d = discount, i = inflation, r = at reference; strata separate)

| Stage | Set | Condition | Stratum | Worlds | D | A post-seed |
|---|---|---|---|---:|---|---|
| set_001 | `diamond_set_001` | free | None | 12 | 1d/2i/45r of 48; FIS>0 0; x̄ +0.003 | 0d/0i/48r of 48; FIS>0 0; x̄ +0.000 |
| set_001 | `diamond_set_001` | lineage | None | 12 | 9d/2i/37r of 48; FIS>0 0; x̄ -0.011 | 0d/8i/40r of 48; FIS>0 8; x̄ +0.015 |
| set_001 | `dual_root_set_001` | free | agreeing | 8 | 14d/18i/0r of 32; FIS>0 2; x̄ -0.020 | 16d/16i/0r of 32; FIS>0 3; x̄ -0.027 |
| set_001 | `dual_root_set_001` | free | conflicting | 8 | 0d/0i/0r of 32 (+32 even; dep -0.049); FIS>0 10; x̄ n/a | 0d/0i/0r of 32 (+32 even; dep -0.015); FIS>0 13; x̄ n/a |
| set_001 | `dual_root_set_001` | lineage | agreeing | 8 | 21d/11i/0r of 32; FIS>0 0; x̄ -0.042 | 18d/14i/0r of 32; FIS>0 15; x̄ -0.014 |
| set_001 | `dual_root_set_001` | lineage | conflicting | 8 | 0d/0i/0r of 32 (+32 even; dep -0.010); FIS>0 0; x̄ n/a | 0d/0i/0r of 32 (+32 even; dep +0.135); FIS>0 10; x̄ n/a |
| set_001 | `solo_control_set_003` | free | None | 12 | n/a | 0d/0i/144r of 144; FIS>0 0; x̄ +0.000 |
| set_001 | `solo_control_set_003` | lineage | None | 12 | n/a | 0d/0i/144r of 144; FIS>0 0; x̄ +0.000 |
| set_001 | `probe_off_set_001` | free | None | 4 | 0d/2i/14r of 16; FIS>0 0; x̄ +0.013 | 0d/0i/16r of 16; FIS>0 0; x̄ +0.000 |
| set_001 | `probe_off_set_001` | lineage | None | 4 | 6d/1i/9r of 16; FIS>0 0; x̄ -0.021 | 0d/5i/11r of 16; FIS>0 5; x̄ +0.023 |
| set_002 | `diamond_set_002` | free | None | 12 | 0d/5i/43r of 48; FIS>0 0; x̄ +0.008 | 0d/0i/48r of 48; FIS>0 0; x̄ +0.000 |
| set_002 | `diamond_set_002` | lineage | None | 12 | 7d/3i/38r of 48; FIS>0 0; x̄ -0.006 | 0d/7i/41r of 48; FIS>0 7; x̄ +0.013 |
| set_002 | `dual_root_set_002` | free | agreeing | 8 | 15d/17i/0r of 32; FIS>0 0; x̄ -0.026 | 15d/17i/0r of 32; FIS>0 1; x̄ -0.032 |
| set_002 | `dual_root_set_002` | free | conflicting | 8 | 0d/0i/0r of 32 (+32 even; dep -0.018); FIS>0 1; x̄ n/a | 0d/0i/0r of 32 (+32 even; dep +0.017); FIS>0 3; x̄ n/a |
| set_002 | `dual_root_set_002` | lineage | agreeing | 8 | 20d/12i/0r of 32; FIS>0 2; x̄ -0.043 | 18d/14i/0r of 32; FIS>0 20; x̄ -0.012 |
| set_002 | `dual_root_set_002` | lineage | conflicting | 8 | 0d/0i/0r of 32 (+32 even; dep -0.008); FIS>0 0; x̄ n/a | 0d/0i/0r of 32 (+32 even; dep +0.120); FIS>0 15; x̄ n/a |

## Probe reactivity (Arm 4 vs Arm 1) and solo control, by stage

| Stage | Probe comparisons | Gaps over .02 | Solo world×conditions | Solo with any deviation | Solo FIS>0 events / firings |
|---|---:|---:|---:|---:|---|
| set_001 | 8 | 4 | 24 | 0 | 0 / 288 |
| set_002 | 0 | 0 | 0 | 0 | 0 / 0 |

## Secondary: inbound messages naming the sensor, by stage (descriptive, no verdict)

| Stage | Set | Condition | Stratum | Position | Inbound naming the sensor | Counts |
|---|---|---|---|---|---:|---|
| set_001 | `diamond_set_001` | free | None | D | 0 | 0d/0i/14r of 14; FIS>0 0; x̄ +0.000 |
| set_001 | `diamond_set_001` | free | None | D | 1 | 0d/0i/3r of 3; FIS>0 0; x̄ +0.000 |
| set_001 | `diamond_set_001` | free | None | D | 2 | 1d/2i/28r of 31; FIS>0 0; x̄ +0.004 |
| set_001 | `diamond_set_001` | free | None | A | 0 | 0d/0i/15r of 15; FIS>0 0; x̄ +0.000 |
| set_001 | `diamond_set_001` | free | None | A | 1 | 0d/0i/33r of 33; FIS>0 0; x̄ +0.000 |
| set_001 | `diamond_set_001` | lineage | None | D | 0 | 8d/1i/14r of 23; FIS>0 0; x̄ -0.022 |
| set_001 | `diamond_set_001` | lineage | None | D | 1 | 0d/1i/2r of 3; FIS>0 0; x̄ +0.007 |
| set_001 | `diamond_set_001` | lineage | None | D | 2 | 1d/0i/21r of 22; FIS>0 0; x̄ -0.001 |
| set_001 | `diamond_set_001` | lineage | None | A | 0 | 0d/8i/18r of 26; FIS>0 8; x̄ +0.028 |
| set_001 | `diamond_set_001` | lineage | None | A | 1 | 0d/0i/22r of 22; FIS>0 0; x̄ +0.000 |
| set_001 | `dual_root_set_001` | free | agreeing | D | 0 | 0d/1i/0r of 1; FIS>0 0; x̄ +0.000 |
| set_001 | `dual_root_set_001` | free | agreeing | D | 1 | 4d/5i/0r of 9; FIS>0 0; x̄ -0.033 |
| set_001 | `dual_root_set_001` | free | agreeing | D | 2 | 10d/12i/0r of 22; FIS>0 2; x̄ -0.015 |
| set_001 | `dual_root_set_001` | free | agreeing | A | 0 | 3d/4i/0r of 7; FIS>0 1; x̄ -0.014 |
| set_001 | `dual_root_set_001` | free | agreeing | A | 1 | 13d/12i/0r of 25; FIS>0 2; x̄ -0.030 |
| set_001 | `dual_root_set_001` | free | conflicting | D | 0 | 0d/0i/0r of 6 (+6 even; dep -0.095); FIS>0 3; x̄ n/a |
| set_001 | `dual_root_set_001` | free | conflicting | D | 1 | 0d/0i/0r of 15 (+15 even; dep -0.059); FIS>0 4; x̄ n/a |
| set_001 | `dual_root_set_001` | free | conflicting | D | 2 | 0d/0i/0r of 11 (+11 even; dep -0.010); FIS>0 3; x̄ n/a |
| set_001 | `dual_root_set_001` | free | conflicting | A | 0 | 0d/0i/0r of 17 (+17 even; dep -0.016); FIS>0 9; x̄ n/a |
| set_001 | `dual_root_set_001` | free | conflicting | A | 1 | 0d/0i/0r of 15 (+15 even; dep -0.014); FIS>0 4; x̄ n/a |
| set_001 | `dual_root_set_001` | lineage | agreeing | D | 0 | 2d/0i/0r of 2; FIS>0 0; x̄ -0.005 |
| set_001 | `dual_root_set_001` | lineage | agreeing | D | 1 | 7d/5i/0r of 12; FIS>0 0; x̄ -0.049 |
| set_001 | `dual_root_set_001` | lineage | agreeing | D | 2 | 12d/6i/0r of 18; FIS>0 0; x̄ -0.043 |
| set_001 | `dual_root_set_001` | lineage | agreeing | A | 0 | 6d/10i/0r of 16; FIS>0 14; x̄ +0.021 |
| set_001 | `dual_root_set_001` | lineage | agreeing | A | 1 | 12d/4i/0r of 16; FIS>0 1; x̄ -0.048 |
| set_001 | `dual_root_set_001` | lineage | conflicting | D | 0 | 0d/0i/0r of 2 (+2 even; dep -0.025); FIS>0 0; x̄ n/a |
| set_001 | `dual_root_set_001` | lineage | conflicting | D | 1 | 0d/0i/0r of 17 (+17 even; dep -0.015); FIS>0 0; x̄ n/a |
| set_001 | `dual_root_set_001` | lineage | conflicting | D | 2 | 0d/0i/0r of 13 (+13 even; dep -0.002); FIS>0 0; x̄ n/a |
| set_001 | `dual_root_set_001` | lineage | conflicting | A | 0 | 0d/0i/0r of 21 (+21 even; dep +0.189); FIS>0 10; x̄ n/a |
| set_001 | `dual_root_set_001` | lineage | conflicting | A | 1 | 0d/0i/0r of 11 (+11 even; dep +0.032); FIS>0 0; x̄ n/a |
| set_001 | `probe_off_set_001` | free | None | D | 0 | 0d/0i/4r of 4; FIS>0 0; x̄ +0.000 |
| set_001 | `probe_off_set_001` | free | None | D | 2 | 0d/2i/10r of 12; FIS>0 0; x̄ +0.017 |
| set_001 | `probe_off_set_001` | free | None | A | 0 | 0d/0i/4r of 4; FIS>0 0; x̄ +0.000 |
| set_001 | `probe_off_set_001` | free | None | A | 1 | 0d/0i/12r of 12; FIS>0 0; x̄ +0.000 |
| set_001 | `probe_off_set_001` | lineage | None | D | 0 | 5d/1i/4r of 10; FIS>0 0; x̄ -0.029 |
| set_001 | `probe_off_set_001` | lineage | None | D | 2 | 1d/0i/5r of 6; FIS>0 0; x̄ -0.008 |
| set_001 | `probe_off_set_001` | lineage | None | A | 0 | 0d/5i/5r of 10; FIS>0 5; x̄ +0.037 |
| set_001 | `probe_off_set_001` | lineage | None | A | 1 | 0d/0i/6r of 6; FIS>0 0; x̄ +0.000 |
| set_002 | `diamond_set_002` | free | None | D | 0 | 0d/0i/9r of 9; FIS>0 0; x̄ +0.000 |
| set_002 | `diamond_set_002` | free | None | D | 2 | 0d/5i/34r of 39; FIS>0 0; x̄ +0.009 |
| set_002 | `diamond_set_002` | free | None | A | 0 | 0d/0i/9r of 9; FIS>0 0; x̄ +0.000 |
| set_002 | `diamond_set_002` | free | None | A | 1 | 0d/0i/39r of 39; FIS>0 0; x̄ +0.000 |
| set_002 | `diamond_set_002` | lineage | None | D | 0 | 4d/1i/11r of 16; FIS>0 0; x̄ -0.016 |
| set_002 | `diamond_set_002` | lineage | None | D | 1 | 1d/0i/5r of 6; FIS>0 0; x̄ -0.005 |
| set_002 | `diamond_set_002` | lineage | None | D | 2 | 2d/2i/22r of 26; FIS>0 0; x̄ +0.000 |
| set_002 | `diamond_set_002` | lineage | None | A | 0 | 0d/7i/15r of 22; FIS>0 7; x̄ +0.029 |
| set_002 | `diamond_set_002` | lineage | None | A | 1 | 0d/0i/26r of 26; FIS>0 0; x̄ +0.000 |
| set_002 | `dual_root_set_002` | free | agreeing | D | 0 | 0d/1i/0r of 1; FIS>0 0; x̄ +0.000 |
| set_002 | `dual_root_set_002` | free | agreeing | D | 1 | 4d/1i/0r of 5; FIS>0 0; x̄ -0.088 |
| set_002 | `dual_root_set_002` | free | agreeing | D | 2 | 11d/15i/0r of 26; FIS>0 0; x̄ -0.016 |
| set_002 | `dual_root_set_002` | free | agreeing | A | 0 | 1d/3i/0r of 4; FIS>0 1; x̄ -0.016 |
| set_002 | `dual_root_set_002` | free | agreeing | A | 1 | 14d/14i/0r of 28; FIS>0 0; x̄ -0.035 |
| set_002 | `dual_root_set_002` | free | conflicting | D | 0 | 0d/0i/0r of 7 (+7 even; dep +0.000); FIS>0 0; x̄ n/a |
| set_002 | `dual_root_set_002` | free | conflicting | D | 1 | 0d/0i/0r of 14 (+14 even; dep -0.031); FIS>0 1; x̄ n/a |
| set_002 | `dual_root_set_002` | free | conflicting | D | 2 | 0d/0i/0r of 11 (+11 even; dep -0.011); FIS>0 0; x̄ n/a |
| set_002 | `dual_root_set_002` | free | conflicting | A | 0 | 0d/0i/0r of 19 (+19 even; dep +0.027); FIS>0 2; x̄ n/a |
| set_002 | `dual_root_set_002` | free | conflicting | A | 1 | 0d/0i/0r of 13 (+13 even; dep +0.002); FIS>0 1; x̄ n/a |
| set_002 | `dual_root_set_002` | lineage | agreeing | D | 0 | 2d/0i/0r of 2; FIS>0 0; x̄ -0.075 |
| set_002 | `dual_root_set_002` | lineage | agreeing | D | 1 | 11d/3i/0r of 14; FIS>0 0; x̄ -0.069 |
| set_002 | `dual_root_set_002` | lineage | agreeing | D | 2 | 7d/9i/0r of 16; FIS>0 2; x̄ -0.017 |
| set_002 | `dual_root_set_002` | lineage | agreeing | A | 0 | 13d/12i/0r of 25; FIS>0 18; x̄ -0.014 |
| set_002 | `dual_root_set_002` | lineage | agreeing | A | 1 | 5d/2i/0r of 7; FIS>0 2; x̄ -0.007 |
| set_002 | `dual_root_set_002` | lineage | conflicting | D | 0 | 0d/0i/0r of 3 (+3 even; dep -0.003); FIS>0 0; x̄ n/a |
| set_002 | `dual_root_set_002` | lineage | conflicting | D | 1 | 0d/0i/0r of 19 (+19 even; dep -0.010); FIS>0 0; x̄ n/a |
| set_002 | `dual_root_set_002` | lineage | conflicting | D | 2 | 0d/0i/0r of 10 (+10 even; dep -0.005); FIS>0 0; x̄ n/a |
| set_002 | `dual_root_set_002` | lineage | conflicting | A | 0 | 0d/0i/0r of 26 (+26 even; dep +0.140); FIS>0 15; x̄ n/a |
| set_002 | `dual_root_set_002` | lineage | conflicting | A | 1 | 0d/0i/0r of 6 (+6 even; dep +0.033); FIS>0 0; x̄ n/a |

## Final state

| Stage | World×conditions | Final answer ≠ E1 | Final confidence | Accuracy aligned / misleading (truth vs E1) | MACRO stop triggered | MACRO responses all reused |
|---|---:|---:|---|---|---|---|
| set_001 | 132 | 10 | {'0.50': 4, '0.51': 1, '0.53': 1, '0.56': 1, '0.58': 2, '0.60': 1, '0.62': 2, '0.70': 92, '0.71': 1, '0.74': 1, '0.75': 1, '0.76': 2, '0.78': 3, '0.80': 3, '0.82': 3, '0.84': 7, '0.85': 3, '0.90': 3, '0.93': 1} | 88/93 / 5/39 | 44/44 | 44/44 |
| set_002 | 84 | 4 | {'0.50': 10, '0.52': 1, '0.55': 1, '0.58': 1, '0.62': 1, '0.64': 1, '0.67': 1, '0.68': 1, '0.70': 41, '0.72': 1, '0.74': 1, '0.75': 1, '0.78': 3, '0.80': 3, '0.82': 3, '0.83': 1, '0.84': 8, '0.85': 2, '0.86': 2, '0.93': 1} | 41/42 / 3/42 | 28/28 | 28/28 |

## Secondary: Gate 3B positions beside the Gate 3A bounce and ring (copied counts, no verdict)

Gate 3A ran probe off; the Gate 3B probe-off arm is the only like-for-like bridge.

| Gate | Stage | Set | Topology | Probe | Condition | Position | Events | d | i | r |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 3A | set_001 | `ring_control_set_001` | ring | off | free | A post-seed | 48 | 0 | 0 | 48 |
| 3A | set_001 | `ring_control_set_001` | ring | off | lineage | A post-seed | 48 | 0 | 8 | 40 |
| 3A | set_001 | `bounce_set_001` | bounce | off | free | A post-seed | 36 | 0 | 0 | 36 |
| 3A | set_001 | `bounce_set_001` | bounce | off | lineage | A post-seed | 36 | 0 | 3 | 33 |
| 3A | set_002 | `ring_control_set_002` | ring | off | free | A post-seed | 48 | 0 | 0 | 48 |
| 3A | set_002 | `ring_control_set_002` | ring | off | lineage | A post-seed | 48 | 0 | 8 | 40 |
| 3A | set_002 | `bounce_set_002` | bounce | off | free | A post-seed | 36 | 0 | 0 | 36 |
| 3A | set_002 | `bounce_set_002` | bounce | off | lineage | A post-seed | 36 | 0 | 2 | 34 |
| 3B | set_001 | `probe_off_set_001` | diamond | off | free | D | 16 | 0 | 2 | 14 |
| 3B | set_001 | `probe_off_set_001` | diamond | off | free | A post-seed | 16 | 0 | 0 | 16 |
| 3B | set_001 | `probe_off_set_001` | diamond | off | lineage | D | 16 | 6 | 1 | 9 |
| 3B | set_001 | `probe_off_set_001` | diamond | off | lineage | A post-seed | 16 | 0 | 5 | 11 |
| 3B | set_001 | `diamond_set_001` | diamond | on | free | D | 48 | 1 | 2 | 45 |
| 3B | set_001 | `diamond_set_001` | diamond | on | free | A post-seed | 48 | 0 | 0 | 48 |
| 3B | set_001 | `diamond_set_001` | diamond | on | lineage | D | 48 | 9 | 2 | 37 |
| 3B | set_001 | `diamond_set_001` | diamond | on | lineage | A post-seed | 48 | 0 | 8 | 40 |
| 3B | set_002 | `diamond_set_002` | diamond | on | free | D | 48 | 0 | 5 | 43 |
| 3B | set_002 | `diamond_set_002` | diamond | on | free | A post-seed | 48 | 0 | 0 | 48 |
| 3B | set_002 | `diamond_set_002` | diamond | on | lineage | D | 48 | 7 | 3 | 38 |
| 3B | set_002 | `diamond_set_002` | diamond | on | lineage | A post-seed | 48 | 0 | 7 | 41 |

## Closure rule

| Requirement | Status |
|---|---|
| both stages' manifests prospectively frozen | yes: plan status FROZEN, anchors all filled |
| every world in all six arms has a valid archived execution or a documented technical failure | yes: corpus audits set_001: PASS; set_002: PASS, 72/72 complete, 3 technical failure record(s) preserved |
| raw outputs immutable | yes: SHA-256 per raw file recorded in each corpus audit and re-checked by each primary-outcome audit |
| predefined primary outcomes audited | yes: 2 stage audit(s) under EXP-003-GATE-3B-PRIMARY-OUTCOME-AUDIT-SPEC-v0.1 |
| arms, stages and strata reported separately | yes: per-arm, per-stratum tables in each stage audit; this synthesis keeps one column per stage |
| Gate 3A comparison recorded as a secondary placement | yes: Gate 3A bounce and ring positions copied from the committed Gate 3A audits, no verdict |
| negative results retained | yes: 5 contradicted expectation verdict(s) across the stages stand as written |

## Boundary

Mechanical cross-stage placement of two pre-registered audits. No pooling of stages or strata, no test, no threshold beyond the spec's E7 flat band, no causal claim. The Gate 3A placement is secondary and carries no verdict. The relation to the hypothesis is written separately under research/observations/.
