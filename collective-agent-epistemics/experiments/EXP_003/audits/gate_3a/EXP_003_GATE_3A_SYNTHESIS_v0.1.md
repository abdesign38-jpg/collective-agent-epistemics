# EXP-003 Gate 3A Synthesis v0.1

## Status

**SYNTHESIS** (mechanical, cross-stage)

Mechanical cross-stage placement of two pre-registered audits. No pooling, no test, no threshold, no causal claim. The relation to the hypothesis is written separately under research/observations/.

## Sources

- set_001: `experiments/EXP_003/audits/gate_3a/EXP_003_GATE_3A_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1.json` (sha256 `f43e47fc82867184ad2782f1f14e03510ce3334168ba52e2cd82c96adba37367`)
- set_001_corpus: `experiments/EXP_003/audits/gate_3a/EXP_003_GATE_3A_SET_001_CORPUS_AUDIT_v0.1.json` (sha256 `b24dfb7b4b28bcd9d990d821f05f9fbbd65e207eba7d8e7875e36bb3efa8ae8a`)
- set_002: `experiments/EXP_003/audits/gate_3a/EXP_003_GATE_3A_SET_002_PRIMARY_OUTCOME_AUDIT_v0.1.json` (sha256 `c3a1ccd9ea0d9c2e13f1ad621d269de608134ad87de67db552087eba72ad3cc1`)
- set_002_corpus: `experiments/EXP_003/audits/gate_3a/EXP_003_GATE_3A_SET_002_CORPUS_AUDIT_v0.1.json` (sha256 `9772e6c7f51a86dac3ca72b9c4c32abd6f832abdd4a9bce172df1af478a27241`)
- historical: `experiments/EXP_003/audits/gate_3a/EXP_003_GATE_3A_HISTORICAL_RING_OBSERVATION_v0.1.json` (sha256 `0e1604da4bde9d47e06e746cf48d13c8158d6eeba7134957da0dcbfa1c4f3f0c`)
- HEAD at synthesis time: `c8a7eeaee4e5a449f21f4ab5ad47638c8b2db027`

## Pre-registered expectations, both stages

| Id | set_001 | set_002 | Agree |
|---|---|---|---|
| E1 | **contradicted** | **contradicted** | yes |
| E2 | **contradicted** | **contradicted** | yes |
| E3 | **consistent** | **consistent** | yes |
| E4 | **contradicted** | **consistent** | no |
| E5 | **consistent** | **consistent** | yes |
| E6 | ring→bounce→dyad→solo | ring→bounce→dyad→solo | **consistent** |

E6 rates (LINEAGE discount rate over all post-seed events, by arm):

| Stage | solo | dyad | ring | bounce |
|---|---:|---:|---:|---:|
| set_001 | 0.000 | 0.021 | 0.174 | 0.097 |
| set_002 | 0.000 | 0.014 | 0.215 | 0.104 |

Quantities behind each verdict:

- E1 set_001: `{"ring_A_discount_events": 0, "ring_FREE_deviation_events": 6, "ring_LINEAGE_B_plus_C_discount_events": 25}`
- E1 set_002: `{"ring_A_discount_events": 0, "ring_FREE_deviation_events": 5, "ring_LINEAGE_B_plus_C_discount_events": 31}`
- E2 set_001: `{"bounce_C_discount_rate_LINEAGE": 0.166667, "ring_C_discount_rate_LINEAGE": 0.354167, "bounce_B_return_mean_magnitude_LINEAGE": 0.023056, "bounce_B_outward_mean_magnitude_LINEAGE": 0.003889, "FREE": {"bounce_C_discount_rate": 0.055556, "ring_C_discount_rate": 0.083333}}`
- E2 set_002: `{"bounce_C_discount_rate_LINEAGE": 0.166667, "ring_C_discount_rate_LINEAGE": 0.458333, "bounce_B_return_mean_magnitude_LINEAGE": 0.021111, "bounce_B_outward_mean_magnitude_LINEAGE": 0.002222, "FREE": {"bounce_C_discount_rate": 0.055556, "ring_C_discount_rate": 0.020833}}`
- E3 set_001: `{"dyad_B_discount_rate_LINEAGE": 0.041667, "ring_B_discount_rate_LINEAGE": 0.166667, "FREE": {"dyad_B_discount_rate": 0.0, "ring_B_discount_rate": 0.020833}}`
- E3 set_002: `{"dyad_B_discount_rate_LINEAGE": 0.027778, "ring_B_discount_rate_LINEAGE": 0.1875, "FREE": {"dyad_B_discount_rate": 0.0, "ring_B_discount_rate": 0.0}}`
- E4 set_001: `{"arms": {"solo/free": {"A_restoration_rate": 1.0, "worlds_with_sustained_A_deviation": 0}, "dyad/free": {"A_restoration_rate": 1.0, "worlds_with_sustained_A_deviation": 0}, "ring/free": {"A_restoration_rate": 1.0, "worlds_with_sustained_A_deviation": 0}, "bounce/free": {"A_restoration_rate": 1.0, "worlds_with_sustained_A_deviation": 0}, "solo/lineage": {"A_restoration_rate": 1.0, "worlds_with_sustained_A_deviation": 0}, "dyad/lineage": {"A_restoration_rate": 1.0, "worlds_with_sustained_A_deviation": 0}, "ring/lineage": {"A_restoration_rate": 0.833333, "worlds_with_sustained_A_deviation": 1}, "bounce/lineage": {"A_restoration_rate": 0.916667, "worlds_with_sustained_A_deviation": 0}}}`
- E4 set_002: `{"arms": {"solo/free": {"A_restoration_rate": 1.0, "worlds_with_sustained_A_deviation": 0}, "dyad/free": {"A_restoration_rate": 1.0, "worlds_with_sustained_A_deviation": 0}, "ring/free": {"A_restoration_rate": 1.0, "worlds_with_sustained_A_deviation": 0}, "bounce/free": {"A_restoration_rate": 1.0, "worlds_with_sustained_A_deviation": 0}, "solo/lineage": {"A_restoration_rate": 1.0, "worlds_with_sustained_A_deviation": 0}, "dyad/lineage": {"A_restoration_rate": 1.0, "worlds_with_sustained_A_deviation": 0}, "ring/lineage": {"A_restoration_rate": 0.833333, "worlds_with_sustained_A_deviation": 0}, "bounce/lineage": {"A_restoration_rate": 0.944444, "worlds_with_sustained_A_deviation": 0}}}`
- E5 set_001: `{"solo_deviation_events_FREE_plus_LINEAGE": 0}`
- E5 set_002: `{"solo_deviation_events_FREE_plus_LINEAGE": 0}`

## Position summary (post-seed events; d = discount, i = inflation, r = at reference)

| Stage | Topology | Condition | A | B | C | A restoration | Sustained A deviation (worlds) |
|---|---|---|---|---|---|---:|---:|
| set_001 | solo | free | 0d/0i/144r of 144 | n/a | n/a | 1.0 | 0/12 |
| set_001 | solo | lineage | 0d/0i/144r of 144 | n/a | n/a | 1.0 | 0/12 |
| set_001 | dyad | free | 0d/0i/72r of 72 | 0d/2i/70r of 72 | n/a | 1.0 | 0/12 |
| set_001 | dyad | lineage | 0d/0i/72r of 72 | 3d/1i/68r of 72 | n/a | 1.0 | 0/12 |
| set_001 | ring | free | 0d/0i/48r of 48 | 1d/0i/47r of 48 | 4d/1i/43r of 48 | 1.0 | 0/12 |
| set_001 | ring | lineage | 0d/8i/40r of 48 | 8d/1i/39r of 48 | 17d/0i/31r of 48 | 0.833333 | 1/12 |
| set_001 | bounce | free | 0d/0i/36r of 36 | 7d/3i/62r of 72 | 2d/4i/30r of 36 | 1.0 | 0/12 |
| set_001 | bounce B legs | free | outward 0d/2i of 36 | return 7d/1i of 36 | | | |
| set_001 | bounce | lineage | 0d/3i/33r of 36 | 8d/2i/62r of 72 | 6d/1i/29r of 36 | 0.916667 | 0/12 |
| set_001 | bounce B legs | lineage | outward 0d/2i of 36 | return 8d/0i of 36 | | | |
| set_002 | solo | free | 0d/0i/144r of 144 | n/a | n/a | 1.0 | 0/12 |
| set_002 | solo | lineage | 0d/0i/144r of 144 | n/a | n/a | 1.0 | 0/12 |
| set_002 | dyad | free | 0d/0i/72r of 72 | 0d/0i/72r of 72 | n/a | 1.0 | 0/12 |
| set_002 | dyad | lineage | 0d/0i/72r of 72 | 2d/0i/70r of 72 | n/a | 1.0 | 0/12 |
| set_002 | ring | free | 0d/0i/48r of 48 | 0d/0i/48r of 48 | 1d/4i/43r of 48 | 1.0 | 0/12 |
| set_002 | ring | lineage | 0d/8i/40r of 48 | 9d/0i/39r of 48 | 22d/2i/24r of 48 | 0.833333 | 0/12 |
| set_002 | bounce | free | 0d/0i/36r of 36 | 5d/2i/65r of 72 | 2d/1i/33r of 36 | 1.0 | 0/12 |
| set_002 | bounce B legs | free | outward 1d/0i of 36 | return 4d/2i of 36 | | | |
| set_002 | bounce | lineage | 0d/2i/34r of 36 | 9d/1i/62r of 72 | 6d/0i/30r of 36 | 0.944444 | 0/12 |
| set_002 | bounce B legs | lineage | outward 1d/0i of 36 | return 8d/1i of 36 | | | |

## Origin (A) deviations after each echo, by firing and by the inbound agent-as-source mark

| Stage | Topology | Condition | A post-seed events | Deviations by firing | deviating & marked | deviating & unmarked | at reference & marked | at reference & unmarked |
|---|---|---|---:|---|---:|---:|---:|---:|
| set_001 | solo | lineage | 144 | {} | 0 | 0 | 0 | 144 |
| set_001 | dyad | lineage | 72 | {} | 0 | 0 | 0 | 72 |
| set_001 | ring | lineage | 48 | {"M07": 1, "M10": 2, "M13": 5} | 1 | 7 | 0 | 40 |
| set_001 | bounce | lineage | 36 | {"M09": 1, "M13": 2} | 2 | 1 | 1 | 32 |
| set_002 | solo | lineage | 144 | {} | 0 | 0 | 0 | 144 |
| set_002 | dyad | lineage | 72 | {} | 0 | 0 | 1 | 71 |
| set_002 | ring | lineage | 48 | {"M10": 2, "M07": 4, "M13": 2} | 3 | 5 | 0 | 40 |
| set_002 | bounce | lineage | 36 | {"M13": 2} | 1 | 1 | 0 | 34 |

(FREE rows with no A deviation are omitted.)

## Final state

| Stage | World×conditions | Final answer ≠ E1 | Final confidence | Accuracy aligned / misleading | MACRO stopped after cycle 1 | MACRO responses all reused | Cells |
|---|---:|---:|---|---|---|---|---|
| set_001 | 144 | 0 | {'0.70': 137, '0.72': 2, '0.75': 1, '0.76': 1, '0.78': 2, '0.80': 1} | 108/108 / 0/36 | 48/48 | 48/48 | {'B/B': 7, 'B/A': 2, 'A/B': 1, 'A/A': 2} |
| set_002 | 144 | 0 | {'0.70': 140, '0.72': 1, '0.75': 1, '0.82': 1, '0.84': 1} | 108/108 / 0/36 | 48/48 | 48/48 | {'A/A': 8, 'B/B': 1, 'A/B': 2, 'B/A': 1} |

## Secondary: contemporary ring (Set 001) vs the archived EXP-002 ring

Historical: 36 runs, 21 distinct seeds, run classes {'gate_2b_real_model': 20, 'pilot_real_model': 16}. Factor ledger difference: `{"experiment": ["EXP-003", "EXP-002"], "gate": ["3A", "2B"], "set": ["ring_control_set_001", "generalization_set_001"], "run_class": ["gate_3a_real_model", "gate_2b_real_model"], "prompt_version": ["exp003-v0.1", "exp002-v0.1"], "schema_version": ["exp003-agent-response-v0.1", "exp002-agent-response-v0.1"]}`.

| Corpus | Condition | Runs | A | B | C | A restoration |
|---|---|---:|---|---|---|---:|
| contemporary | free | 12 | 0d/0i/48r of 48 | 1d/0i/47r of 48 | 4d/1i/43r of 48 | 1.0 |
| contemporary | lineage | 12 | 0d/8i/40r of 48 | 8d/1i/39r of 48 | 17d/0i/31r of 48 | 0.833333 |
| historical | free | 36 | 0d/1i/143r of 144 | 0d/0i/144r of 144 | 3d/0i/141r of 144 | 0.993056 |
| historical | lineage | 36 | 0d/0i/144r of 144 | 18d/0i/126r of 144 | 25d/0i/119r of 144 | 1.0 |
| historical_gate_2b_only | free | 20 | 0d/1i/79r of 80 | 0d/0i/80r of 80 | 3d/0i/77r of 80 | 0.9875 |
| historical_gate_2b_only | lineage | 20 | 0d/0i/80r of 80 | 11d/0i/69r of 80 | 11d/0i/69r of 80 | 1.0 |

## Closure rule

| Requirement | Status |
|---|---|
| both stages' manifests prospectively frozen | yes: plan status FROZEN, anchors all filled |
| every world in all eight arms has a valid archived execution or a documented technical failure | yes: corpus audits set_001: PASS; set_002: PASS, 96/96 complete, 2 technical failure record(s) preserved |
| raw outputs immutable | yes: SHA-256 per raw file recorded in each corpus audit and re-checked by each primary-outcome audit |
| predefined primary outcomes audited | yes: 2 stage audit(s) under EXP-003-GATE-3A-PRIMARY-OUTCOME-AUDIT-SPEC-v0.1 |
| arms and stages reported separately | yes: per-arm tables in each stage audit; this synthesis keeps one column per stage |
| historical comparison recorded as a secondary observation | yes: separate observation file (36 historical runs), adjusts nothing |
| negative results retained | yes: 5 contradicted expectation verdict(s) across the stages stand as written |

## Boundary

Mechanical cross-stage placement of two pre-registered audits. No pooling, no test, no threshold, no causal claim. The relation to the hypothesis is written separately under research/observations/.
