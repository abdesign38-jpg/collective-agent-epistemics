# EXP-003 Gate 3C Set 001 Primary-Outcome Audit v0.1

## Status

**COMPLETE**

Descriptive and pre-registered. Worlds are the unit; arms, stages, conditions and agents are reported separately. Paired quantities carry their twin's execution dates and are never corrected for drift. E6 tiers are frequency descriptions, not mechanism labels; nothing here bears on H2. Negative results stand.

## Provenance

- Specification: `EXP-003-GATE-3C-PRIMARY-OUTCOME-AUDIT-SPEC-v0.1`
- Plan: `GATE_3C_PLAN_v0.1` (status `FROZEN`, sha256 `91fa8f97d553a443b14624b8e8e04d17e278b13270318ec696c8f7edbb0272d0`)
- Corpus audit: `experiments/EXP_003/audits/gate_3c/EXP_003_GATE_3C_SET_001_CORPUS_AUDIT_v0.1.json` (status PASS, sha256 `b4f6ef16c6cd27fb3eceec96706b43530026c6395b93848893e55528cdcff9b7`)
- Twin corpus audit for `ring_detached_set_001`: `experiments/EXP_003/audits/gate_3c/EXP_003_GATE_3C_SET_001_CORPUS_AUDIT_v0.1.json` (sha256 `b4f6ef16c6cd27fb3eceec96706b43530026c6395b93848893e55528cdcff9b7`)
- Twin corpus audit for `solo_detached_set_001`: `experiments/EXP_003/audits/gate_3c/EXP_003_GATE_3C_SET_001_CORPUS_AUDIT_v0.1.json` (sha256 `b4f6ef16c6cd27fb3eceec96706b43530026c6395b93848893e55528cdcff9b7`)
- Twin corpus audit for `dyad_detached_set_001`: `experiments/EXP_003/audits/gate_3c/EXP_003_GATE_3C_SET_001_CORPUS_AUDIT_v0.1.json` (sha256 `b4f6ef16c6cd27fb3eceec96706b43530026c6395b93848893e55528cdcff9b7`)
- Twin corpus audit for `bounce_detached_set_001`: `experiments/EXP_003/audits/gate_3c/EXP_003_GATE_3C_SET_001_CORPUS_AUDIT_v0.1.json` (sha256 `b4f6ef16c6cd27fb3eceec96706b43530026c6395b93848893e55528cdcff9b7`)
- Twin corpus audit for `diamond_detached_set_001`: `experiments/EXP_003/audits/gate_3b/EXP_003_GATE_3B_SET_001_CORPUS_AUDIT_v0.1.json` (sha256 `69fce27cd911bf884488498e0f1b6e7f08ca52022efbb3528102ae2c85e24dfd`)
- Twin corpus audit for `ring_contemporary_set_001`: `experiments/EXP_003/audits/gate_3a/EXP_003_GATE_3A_SET_001_CORPUS_AUDIT_v0.1.json` (sha256 `b24dfb7b4b28bcd9d990d821f05f9fbbd65e207eba7d8e7875e36bb3efa8ae8a`)
- HEAD at audit time: `77af3df1c3eaeb581cc8cdd8115f28de43f55bb8`
- Tolerances: `{"kind": 1e-06, "threshold": 0.01, "flat_band": 0.005, "majority_of_12": 7, "gauge": {"count": 4, "per_world_mean_excess": 0.02, "worlds_required": 10}}`

## Arms and twins

| Set | Topology | Probe | Worlds | Twin | Twin kind | Twin dates | Max gap (days) |
|---|---|---|---:|---|---|---|---:|
| `ring_detached_set_001` | ring_detached | off | 12 | ring_contemporary_set_001 | contemporary | 2026-11-02 | 1 |
| `solo_detached_set_001` | solo_detached | off | 12 | solo_contemporary_set_001 | contemporary | 2026-11-02 | 1 |
| `dyad_detached_set_001` | dyad_detached | off | 12 | dyad_contemporary_set_001 | contemporary | 2026-11-02 | 1 |
| `bounce_detached_set_001` | bounce_detached | off | 12 | bounce_contemporary_set_001 | contemporary | 2026-11-02 | 1 |
| `diamond_detached_set_001` | diamond_detached | on | 12 | diamond_set_001 | historical | 2026-10-30 | 2 |
| `ring_contemporary_set_001` | ring | off | 12 | ring_control_set_001 | historical |  |  |
| `solo_contemporary_set_001` | solo | off | 12 | none |  |  |  |
| `dyad_contemporary_set_001` | dyad | off | 12 | none |  |  |  |
| `bounce_contemporary_set_001` | bounce | off | 12 | none |  |  |  |

## Integrity-level checks

| Set | Manipulation check | Seed firing: identical p(A) / ≤.01 / ≤.05 / >.05 | Identical seed message |
|---|---|---|---:|
| `ring_detached_set_001` | PASS (0 failures) | 12 / 0 / 0 / 0 | 4/12 |
| `solo_detached_set_001` | PASS (0 failures) | 12 / 0 / 0 / 0 | 3/12 |
| `dyad_detached_set_001` | PASS (0 failures) | 12 / 0 / 0 / 0 | 4/12 |
| `bounce_detached_set_001` | PASS (0 failures) | 12 / 0 / 0 / 0 | 2/12 |
| `diamond_detached_set_001` | PASS (0 failures) | 12 / 0 / 0 / 0 | 1/12 |

The seed firing has an identical prompt in both executions and is sampled separately; its difference measures sampling variance, not detachment.

## Pre-registered expectations (this stage)

| Id | Verdict | By arm / quantities |
|---|---|---|
| E1 | **contradicted** | `{"by_arm": {"ring_detached_set_001": "contradicted", "solo_detached_set_001": "not assessable", "dyad_detached_set_001": "consistent", "bounce_detached_set_001": "consistent", "diamond_detached_set_001": "contradicted"}}` |
| E2 | **contradicted** | `{"by_arm": {"ring_detached_set_001": "consistent", "solo_detached_set_001": "consistent", "dyad_detached_set_001": "consistent", "bounce_detached_set_001": "consistent", "diamond_detached_set_001": "contradicted"}}` |
| E3a | **contradicted** | `{"by_arm": {"ring_detached_set_001": "consistent", "solo_detached_set_001": "consistent", "dyad_detached_set_001": "consistent", "bounce_detached_set_001": "consistent", "diamond_detached_set_001": "contradicted"}}` |
| E3b | **consistent** | `{"by_arm": {"ring_detached_set_001": "consistent", "solo_detached_set_001": "consistent", "dyad_detached_set_001": "consistent", "bounce_detached_set_001": "consistent", "diamond_detached_set_001": "consistent"}}` |
| E4 | **contradicted** | `{"by_arm": {"solo_detached_set_001": "contradicted"}}` |
| E5 | **contradicted** | `{"lineage_discount_rate_by_shape": {"ring": 0.472222, "solo": 0.5, "dyad": 0.520833, "bounce": 0.541667}, "required_order": ["ring", "bounce", "dyad", "solo"]}` |
| E6 | **contradicted** | `{"by_arm": {"ring_detached_set_001": "consistent", "bounce_detached_set_001": "consistent", "diamond_detached_set_001": "contradicted"}, "tiers": {"ring_detached_set_001": 1, "bounce_detached_set_001": 1, "diamond_detached_set_001": 2}}` |
| E7 | **assessed in the synthesis across Set 001 and Set 002, not in a single-stage audit** | `{}` |

## Paired displacement and divergence by arm (E3a, E3b)

| Set | Condition | Worlds with Ā > .01 | E3a | Divergence modal class | Tie | Non-monotonic worlds | E3b |
|---|---|---:|---|---|---|---:|---|
| `ring_detached_set_001` | free | 8/12 | consistent | increasing | no | 3 | consistent |
| `ring_detached_set_001` | lineage | 12/12 | consistent | increasing | no | 3 | consistent |
| `solo_detached_set_001` | free | 7/12 | consistent | increasing | no | 2 | consistent |
| `solo_detached_set_001` | lineage | 11/12 | consistent | increasing | no | 6 | consistent |
| `dyad_detached_set_001` | free | 10/12 | consistent | increasing | no | 4 | consistent |
| `dyad_detached_set_001` | lineage | 11/12 | consistent | increasing | no | 1 | consistent |
| `bounce_detached_set_001` | free | 7/12 | consistent | increasing | no | 2 | consistent |
| `bounce_detached_set_001` | lineage | 12/12 | consistent | increasing | no | 2 | consistent |
| `diamond_detached_set_001` | free | 6/12 | contradicted | increasing | no | 3 | consistent |
| `diamond_detached_set_001` | lineage | 12/12 | consistent | increasing | no | 3 | consistent |

## Far-agent compounding by arm (E2) and within-detached LINEAGE rates (E5 quantity)

| Set | Far agent | Condition | Modal class | E2 | Stage mean excess (far) | Mean last − first | LINEAGE discount rate | LINEAGE inflation rate | Twin discount rate |
|---|---|---|---|---|---:|---:|---:|---:|---:|
| `ring_detached_set_001` | C | free | increasing | consistent | -0.018 | +0.043 | +0.472 | +0.007 | +0.167 |
| `ring_detached_set_001` | C | lineage | increasing | consistent | -0.056 | +0.131 | +0.472 | +0.007 | +0.167 |
| `solo_detached_set_001` | A | free | increasing | consistent | -0.019 | +0.052 | +0.500 | +0.007 | +0.000 |
| `solo_detached_set_001` | A | lineage | increasing | consistent | -0.060 | +0.114 | +0.500 | +0.007 | +0.000 |
| `dyad_detached_set_001` | B | free | increasing | consistent | -0.046 | +0.105 | +0.521 | +0.000 | +0.014 |
| `dyad_detached_set_001` | B | lineage | increasing | consistent | -0.061 | +0.138 | +0.521 | +0.000 | +0.014 |
| `bounce_detached_set_001` | C | free | increasing | consistent | -0.008 | +0.023 | +0.542 | +0.000 | +0.167 |
| `bounce_detached_set_001` | C | lineage | increasing | consistent | -0.069 | +0.140 | +0.542 | +0.000 | +0.167 |
| `diamond_detached_set_001` | D | free | stable | contradicted | +0.006 | +0.024 | +0.594 | +0.094 | +0.104 |
| `diamond_detached_set_001` | D | lineage | increasing | consistent | -0.049 | +0.107 | +0.594 | +0.094 | +0.104 |

## Origin after lineage return (E6, strict H1) with descriptive frequency tiers

| Set | Verdict | Tier | Detached LINEAGE events / firings | Mean, max magnitude | Worlds with event | Consecutive | Twin LINEAGE events / firings | Detached FREE events | FIS>0 at events |
|---|---|---|---|---|---:|---:|---|---:|---|
| `ring_detached_set_001` | **consistent** | 1 (no qualifying detached event) | 0 / 48 | n/a, n/a | 0 | 0 | 11 / 48 | 5 | not probed |
| `bounce_detached_set_001` | **consistent** | 1 (no qualifying detached event) | 0 / 36 | n/a, n/a | 0 | 0 | 7 / 36 | 1 | not probed |
| `diamond_detached_set_001` | **contradicted** | 2 (detached rate below the twin's) | 5 / 48 | +0.028, +0.060 | 5 | 0 | 8 / 48 | 10 | 0 |

## Relay-position marker loss (E1)

| Set | Condition | Marker | Detached R first → last (loss) | Twin R first → last (loss) | Marker verdict |
|---|---|---|---|---|---|
| `ring_detached_set_001` | free | source_named | 1.000 → 0.833 (+0.167) | 1.000 → 0.917 (+0.083) | consistent |
| `ring_detached_set_001` | free | reliability_named | 1.000 → 0.250 (+0.750) | 0.958 → 0.708 (+0.250) | consistent |
| `ring_detached_set_001` | lineage | source_named | 0.875 → 0.292 (+0.583) | 0.917 → 0.333 (+0.583) | contradicted |
| `ring_detached_set_001` | lineage | reliability_named | 1.000 → 0.083 (+0.917) | 1.000 → 0.167 (+0.833) | consistent |
| `dyad_detached_set_001` | free | source_named | 0.917 → 0.750 (+0.167) | 1.000 → 1.000 (+0.000) | consistent |
| `dyad_detached_set_001` | free | reliability_named | 1.000 → 0.000 (+1.000) | 0.917 → 0.667 (+0.250) | consistent |
| `dyad_detached_set_001` | lineage | source_named | 1.000 → 0.250 (+0.750) | 0.917 → 0.667 (+0.250) | consistent |
| `dyad_detached_set_001` | lineage | reliability_named | 1.000 → 0.083 (+0.917) | 1.000 → 0.750 (+0.250) | consistent |
| `bounce_detached_set_001` | free | source_named | 1.000 → 1.000 (+0.000) | 0.917 → 1.000 (-0.083) | consistent |
| `bounce_detached_set_001` | free | reliability_named | 0.944 → 0.333 (+0.611) | 0.972 → 0.611 (+0.361) | consistent |
| `bounce_detached_set_001` | lineage | source_named | 0.917 → 0.194 (+0.722) | 0.917 → 0.639 (+0.278) | consistent |
| `bounce_detached_set_001` | lineage | reliability_named | 0.944 → 0.167 (+0.778) | 0.917 → 0.583 (+0.333) | consistent |
| `diamond_detached_set_001` | free | source_named | 1.000 → 0.917 (+0.083) | 0.917 → 0.722 (+0.194) | contradicted |
| `diamond_detached_set_001` | free | reliability_named | 0.944 → 0.361 (+0.583) | 0.917 → 0.917 (+0.000) | consistent |
| `diamond_detached_set_001` | lineage | source_named | 0.944 → 0.222 (+0.722) | 0.944 → 0.250 (+0.694) | consistent |
| `diamond_detached_set_001` | lineage | reliability_named | 0.944 → 0.000 (+0.944) | 0.944 → 0.333 (+0.611) | consistent |

## Drift gauge: contemporary ring vs archived Gate 3A ring, same worlds: **FAIL**

Contemporary dates ['2026-11-02']; historical dates ['2026-10-02']. Observed behavior differed across execution windows under the same nominal model configuration.

| Position | Contemporary LINEAGE deviations | Historical | Difference | Within 4 |
|---|---:|---:|---:|---|
| A | 11 | 8 | +3 | yes |
| B | 3 | 9 | -6 | no |
| C | 24 | 17 | +7 | no |

Worlds with paired mean excess within .02: free 12/12, lineage 11/12

## Secondary: origin firings by whether the inbound message named the sensor (descriptive, no verdict)

| Set | Condition | Inbound | Firings | Inflation | Discount | Events > .01 | FIS>0 | Mean excess |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `ring_detached_set_001` | free | inbound_named_sensor | 43 | 5 | 14 | 5 | 0 | -0.015 |
| `ring_detached_set_001` | free | inbound_unnamed | 5 | 0 | 2 | 0 | 0 | -0.040 |
| `ring_detached_set_001` | lineage | inbound_named_sensor | 26 | 0 | 6 | 0 | 0 | -0.022 |
| `ring_detached_set_001` | lineage | inbound_unnamed | 22 | 0 | 18 | 0 | 0 | -0.116 |
| `dyad_detached_set_001` | free | inbound_named_sensor | 62 | 0 | 26 | 0 | 0 | -0.038 |
| `dyad_detached_set_001` | free | inbound_unnamed | 10 | 0 | 10 | 0 | 0 | -0.187 |
| `dyad_detached_set_001` | lineage | inbound_named_sensor | 41 | 0 | 13 | 0 | 0 | -0.030 |
| `dyad_detached_set_001` | lineage | inbound_unnamed | 31 | 0 | 29 | 0 | 0 | -0.133 |
| `bounce_detached_set_001` | free | inbound_named_sensor | 36 | 1 | 9 | 1 | 0 | -0.013 |
| `bounce_detached_set_001` | free | inbound_unnamed | 0 | 0 | 0 | 0 | 0 | n/a |
| `bounce_detached_set_001` | lineage | inbound_named_sensor | 18 | 0 | 7 | 0 | 0 | -0.036 |
| `bounce_detached_set_001` | lineage | inbound_unnamed | 18 | 0 | 17 | 0 | 0 | -0.148 |
| `diamond_detached_set_001` | free | inbound_named_sensor | 46 | 9 | 7 | 9 | 0 | +0.006 |
| `diamond_detached_set_001` | free | inbound_unnamed | 2 | 1 | 1 | 1 | 0 | -0.015 |
| `diamond_detached_set_001` | lineage | inbound_named_sensor | 22 | 4 | 8 | 4 | 0 | -0.025 |
| `diamond_detached_set_001` | lineage | inbound_unnamed | 26 | 1 | 23 | 1 | 0 | -0.078 |
| `ring_contemporary_set_001` | free | inbound_named_sensor | 45 | 0 | 0 | 0 | 0 | +0.000 |
| `ring_contemporary_set_001` | free | inbound_unnamed | 3 | 0 | 0 | 0 | 0 | +0.000 |
| `ring_contemporary_set_001` | lineage | inbound_named_sensor | 23 | 0 | 0 | 0 | 0 | +0.000 |
| `ring_contemporary_set_001` | lineage | inbound_unnamed | 25 | 11 | 0 | 11 | 12 | +0.029 |
| `dyad_contemporary_set_001` | free | inbound_named_sensor | 71 | 0 | 0 | 0 | 0 | +0.000 |
| `dyad_contemporary_set_001` | free | inbound_unnamed | 1 | 0 | 0 | 0 | 0 | +0.000 |
| `dyad_contemporary_set_001` | lineage | inbound_named_sensor | 54 | 0 | 0 | 0 | 0 | +0.000 |
| `dyad_contemporary_set_001` | lineage | inbound_unnamed | 18 | 3 | 0 | 3 | 3 | +0.014 |
| `bounce_contemporary_set_001` | free | inbound_named_sensor | 35 | 0 | 0 | 0 | 0 | +0.000 |
| `bounce_contemporary_set_001` | free | inbound_unnamed | 1 | 0 | 0 | 0 | 0 | +0.000 |
| `bounce_contemporary_set_001` | lineage | inbound_named_sensor | 25 | 0 | 0 | 0 | 0 | +0.000 |
| `bounce_contemporary_set_001` | lineage | inbound_unnamed | 11 | 7 | 0 | 7 | 7 | +0.035 |

## MACRO stopping boundary

| Set | Seed | Stop event | MACRO events | Responses reused |
|---|---:|---|---:|---|
| `ring_detached_set_001` | 1146035841 | M04 | 4 | True |
| `ring_detached_set_001` | 1265697921 | M04 | 4 | True |
| `ring_detached_set_001` | 154869395 | M04 | 4 | True |
| `ring_detached_set_001` | 1280872600 | M04 | 4 | True |
| `ring_detached_set_001` | 1117385864 | M04 | 4 | True |
| `ring_detached_set_001` | 1779995607 | M04 | 4 | True |
| `ring_detached_set_001` | 961840741 | M04 | 4 | True |
| `ring_detached_set_001` | 1813269025 | M04 | 4 | True |
| `ring_detached_set_001` | 683505103 | M04 | 4 | True |
| `ring_detached_set_001` | 1296650177 | M04 | 4 | True |
| `ring_detached_set_001` | 950201606 | M04 | 4 | True |
| `ring_detached_set_001` | 652310877 | M04 | 4 | True |
| `solo_detached_set_001` | 1146035841 | M02 | 2 | True |
| `solo_detached_set_001` | 1265697921 | M02 | 2 | True |
| `solo_detached_set_001` | 154869395 | M02 | 2 | True |
| `solo_detached_set_001` | 1280872600 | M02 | 2 | True |
| `solo_detached_set_001` | 1117385864 | M02 | 2 | True |
| `solo_detached_set_001` | 1779995607 | M02 | 2 | True |
| `solo_detached_set_001` | 961840741 | M02 | 2 | True |
| `solo_detached_set_001` | 1813269025 | M02 | 2 | True |
| `solo_detached_set_001` | 683505103 | M02 | 2 | True |
| `solo_detached_set_001` | 1296650177 | M02 | 2 | True |
| `solo_detached_set_001` | 950201606 | M02 | 2 | True |
| `solo_detached_set_001` | 652310877 | M02 | 2 | True |
| `dyad_detached_set_001` | 1146035841 | M03 | 3 | True |
| `dyad_detached_set_001` | 1265697921 | M03 | 3 | True |
| `dyad_detached_set_001` | 154869395 | M03 | 3 | True |
| `dyad_detached_set_001` | 1280872600 | M03 | 3 | True |
| `dyad_detached_set_001` | 1117385864 | M03 | 3 | True |
| `dyad_detached_set_001` | 1779995607 | M03 | 3 | True |
| `dyad_detached_set_001` | 961840741 | M03 | 3 | True |
| `dyad_detached_set_001` | 1813269025 | M03 | 3 | True |
| `dyad_detached_set_001` | 683505103 | M03 | 3 | True |
| `dyad_detached_set_001` | 1296650177 | M03 | 3 | True |
| `dyad_detached_set_001` | 950201606 | M03 | 3 | True |
| `dyad_detached_set_001` | 652310877 | M03 | 3 | True |
| `bounce_detached_set_001` | 1146035841 | M05 | 5 | True |
| `bounce_detached_set_001` | 1265697921 | M05 | 5 | True |
| `bounce_detached_set_001` | 154869395 | M05 | 5 | True |
| `bounce_detached_set_001` | 1280872600 | M05 | 5 | True |
| `bounce_detached_set_001` | 1117385864 | M05 | 5 | True |
| `bounce_detached_set_001` | 1779995607 | M05 | 5 | True |
| `bounce_detached_set_001` | 961840741 | M05 | 5 | True |
| `bounce_detached_set_001` | 1813269025 | M05 | 5 | True |
| `bounce_detached_set_001` | 683505103 | M05 | 5 | True |
| `bounce_detached_set_001` | 1296650177 | M05 | 5 | True |
| `bounce_detached_set_001` | 950201606 | M05 | 5 | True |
| `bounce_detached_set_001` | 652310877 | M05 | 5 | True |
| `diamond_detached_set_001` | 1672462843 | M05 | 5 | True |
| `diamond_detached_set_001` | 63901144 | M05 | 5 | True |
| `diamond_detached_set_001` | 323832400 | M05 | 5 | True |
| `diamond_detached_set_001` | 1566825802 | M05 | 5 | True |
| `diamond_detached_set_001` | 277459948 | M05 | 5 | True |
| `diamond_detached_set_001` | 743291108 | M05 | 5 | True |
| `diamond_detached_set_001` | 2020380812 | M05 | 5 | True |
| `diamond_detached_set_001` | 1292406070 | M05 | 5 | True |
| `diamond_detached_set_001` | 187031691 | M05 | 5 | True |
| `diamond_detached_set_001` | 1476859861 | M05 | 5 | True |
| `diamond_detached_set_001` | 745425377 | M05 | 5 | True |
| `diamond_detached_set_001` | 1686133698 | M05 | 5 | True |
| `ring_contemporary_set_001` | 1146035841 | M04 | 4 | True |
| `ring_contemporary_set_001` | 1265697921 | M04 | 4 | True |
| `ring_contemporary_set_001` | 154869395 | M04 | 4 | True |
| `ring_contemporary_set_001` | 1280872600 | M04 | 4 | True |
| `ring_contemporary_set_001` | 1117385864 | M04 | 4 | True |
| `ring_contemporary_set_001` | 1779995607 | M04 | 4 | True |
| `ring_contemporary_set_001` | 961840741 | M04 | 4 | True |
| `ring_contemporary_set_001` | 1813269025 | M04 | 4 | True |
| `ring_contemporary_set_001` | 683505103 | M04 | 4 | True |
| `ring_contemporary_set_001` | 1296650177 | M04 | 4 | True |
| `ring_contemporary_set_001` | 950201606 | M04 | 4 | True |
| `ring_contemporary_set_001` | 652310877 | M04 | 4 | True |
| `solo_contemporary_set_001` | 1146035841 | M02 | 2 | True |
| `solo_contemporary_set_001` | 1265697921 | M02 | 2 | True |
| `solo_contemporary_set_001` | 154869395 | M02 | 2 | True |
| `solo_contemporary_set_001` | 1280872600 | M02 | 2 | True |
| `solo_contemporary_set_001` | 1117385864 | M02 | 2 | True |
| `solo_contemporary_set_001` | 1779995607 | M02 | 2 | True |
| `solo_contemporary_set_001` | 961840741 | M02 | 2 | True |
| `solo_contemporary_set_001` | 1813269025 | M02 | 2 | True |
| `solo_contemporary_set_001` | 683505103 | M02 | 2 | True |
| `solo_contemporary_set_001` | 1296650177 | M02 | 2 | True |
| `solo_contemporary_set_001` | 950201606 | M02 | 2 | True |
| `solo_contemporary_set_001` | 652310877 | M02 | 2 | True |
| `dyad_contemporary_set_001` | 1146035841 | M03 | 3 | True |
| `dyad_contemporary_set_001` | 1265697921 | M03 | 3 | True |
| `dyad_contemporary_set_001` | 154869395 | M03 | 3 | True |
| `dyad_contemporary_set_001` | 1280872600 | M03 | 3 | True |
| `dyad_contemporary_set_001` | 1117385864 | M03 | 3 | True |
| `dyad_contemporary_set_001` | 1779995607 | M03 | 3 | True |
| `dyad_contemporary_set_001` | 961840741 | M03 | 3 | True |
| `dyad_contemporary_set_001` | 1813269025 | M03 | 3 | True |
| `dyad_contemporary_set_001` | 683505103 | M03 | 3 | True |
| `dyad_contemporary_set_001` | 1296650177 | M03 | 3 | True |
| `dyad_contemporary_set_001` | 950201606 | M03 | 3 | True |
| `dyad_contemporary_set_001` | 652310877 | M03 | 3 | True |
| `bounce_contemporary_set_001` | 1146035841 | M05 | 5 | True |
| `bounce_contemporary_set_001` | 1265697921 | M05 | 5 | True |
| `bounce_contemporary_set_001` | 154869395 | M05 | 5 | True |
| `bounce_contemporary_set_001` | 1280872600 | M05 | 5 | True |
| `bounce_contemporary_set_001` | 1117385864 | M05 | 5 | True |
| `bounce_contemporary_set_001` | 1779995607 | M05 | 5 | True |
| `bounce_contemporary_set_001` | 961840741 | M05 | 5 | True |
| `bounce_contemporary_set_001` | 1813269025 | M05 | 5 | True |
| `bounce_contemporary_set_001` | 683505103 | M05 | 5 | True |
| `bounce_contemporary_set_001` | 1296650177 | M05 | 5 | True |
| `bounce_contemporary_set_001` | 950201606 | M05 | 5 | True |
| `bounce_contemporary_set_001` | 652310877 | M05 | 5 | True |

## Problems

None.

## Boundary

Descriptive and pre-registered. Worlds are the unit; arms, stages, conditions and agents are reported separately. Paired quantities carry their twin's execution dates and are never corrected for drift. E6 tiers are frequency descriptions, not mechanism labels; nothing here bears on H2. Negative results stand.

Within-agent trajectories, per-world paired sequences and retention by depth are in the JSON record under `arms.<set>.within_agent`, `arms.<set>.paired.<condition>.worlds` and `arms.<set>.retention`.