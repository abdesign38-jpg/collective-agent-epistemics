# EXP-003 Gate 3C Set 002 Primary-Outcome Audit v0.1

## Status

**COMPLETE**

Descriptive and pre-registered. Worlds are the unit; arms, stages, conditions and agents are reported separately. Paired quantities carry their twin's execution dates and are never corrected for drift. E6 tiers are frequency descriptions, not mechanism labels; nothing here bears on H2. Negative results stand.

## Provenance

- Specification: `EXP-003-GATE-3C-PRIMARY-OUTCOME-AUDIT-SPEC-v0.1`
- Plan: `GATE_3C_PLAN_v0.1` (status `FROZEN`, sha256 `91fa8f97d553a443b14624b8e8e04d17e278b13270318ec696c8f7edbb0272d0`)
- Corpus audit: `experiments/EXP_003/audits/gate_3c/EXP_003_GATE_3C_SET_002_CORPUS_AUDIT_v0.1.json` (status PASS, sha256 `444d5a6f81fb3933d5cb10fcb274a4aaf791d50b6c256d524ccbb0c5624bc92b`)
- Twin corpus audit for `ring_detached_set_002`: `experiments/EXP_003/audits/gate_3a/EXP_003_GATE_3A_SET_002_CORPUS_AUDIT_v0.1.json` (sha256 `9772e6c7f51a86dac3ca72b9c4c32abd6f832abdd4a9bce172df1af478a27241`)
- Twin corpus audit for `solo_detached_set_002`: `experiments/EXP_003/audits/gate_3a/EXP_003_GATE_3A_SET_002_CORPUS_AUDIT_v0.1.json` (sha256 `9772e6c7f51a86dac3ca72b9c4c32abd6f832abdd4a9bce172df1af478a27241`)
- Twin corpus audit for `dyad_detached_set_002`: `experiments/EXP_003/audits/gate_3a/EXP_003_GATE_3A_SET_002_CORPUS_AUDIT_v0.1.json` (sha256 `9772e6c7f51a86dac3ca72b9c4c32abd6f832abdd4a9bce172df1af478a27241`)
- Twin corpus audit for `bounce_detached_set_002`: `experiments/EXP_003/audits/gate_3a/EXP_003_GATE_3A_SET_002_CORPUS_AUDIT_v0.1.json` (sha256 `9772e6c7f51a86dac3ca72b9c4c32abd6f832abdd4a9bce172df1af478a27241`)
- Twin corpus audit for `diamond_detached_set_002`: `experiments/EXP_003/audits/gate_3b/EXP_003_GATE_3B_SET_002_CORPUS_AUDIT_v0.1.json` (sha256 `1ad6ffa30765eb8ecad65133dc5f9fd9e7558f87ca9962bbd2384c16aa7116c1`)
- HEAD at audit time: `77af3df1c3eaeb581cc8cdd8115f28de43f55bb8`
- Tolerances: `{"kind": 1e-06, "threshold": 0.01, "flat_band": 0.005, "majority_of_12": 7, "gauge": {"count": 4, "per_world_mean_excess": 0.02, "worlds_required": 10}}`

## Arms and twins

| Set | Topology | Probe | Worlds | Twin | Twin kind | Twin dates | Max gap (days) |
|---|---|---|---:|---|---|---|---:|
| `ring_detached_set_002` | ring_detached | off | 12 | ring_control_set_002 | historical | 2026-10-02 | 30 |
| `solo_detached_set_002` | solo_detached | off | 12 | solo_control_set_002 | historical | 2026-10-02 | 30 |
| `dyad_detached_set_002` | dyad_detached | off | 12 | dyad_set_002 | historical | 2026-10-02 | 30 |
| `bounce_detached_set_002` | bounce_detached | off | 12 | bounce_set_002 | historical | 2026-10-02 | 30 |
| `diamond_detached_set_002` | diamond_detached | on | 12 | diamond_set_002 | historical | 2026-10-31 | 1 |

## Integrity-level checks

| Set | Manipulation check | Seed firing: identical p(A) / ≤.01 / ≤.05 / >.05 | Identical seed message |
|---|---|---|---:|
| `ring_detached_set_002` | PASS (0 failures) | 12 / 0 / 0 / 0 | 3/12 |
| `solo_detached_set_002` | PASS (0 failures) | 12 / 0 / 0 / 0 | 1/12 |
| `dyad_detached_set_002` | PASS (0 failures) | 12 / 0 / 0 / 0 | 0/12 |
| `bounce_detached_set_002` | PASS (0 failures) | 12 / 0 / 0 / 0 | 1/12 |
| `diamond_detached_set_002` | PASS (0 failures) | 12 / 0 / 0 / 0 | 2/12 |

The seed firing has an identical prompt in both executions and is sampled separately; its difference measures sampling variance, not detachment.

## Pre-registered expectations (this stage)

| Id | Verdict | By arm / quantities |
|---|---|---|
| E1 | **contradicted** | `{"by_arm": {"ring_detached_set_002": "consistent", "solo_detached_set_002": "not assessable", "dyad_detached_set_002": "consistent", "bounce_detached_set_002": "consistent", "diamond_detached_set_002": "contradicted"}}` |
| E2 | **contradicted** | `{"by_arm": {"ring_detached_set_002": "consistent", "solo_detached_set_002": "consistent", "dyad_detached_set_002": "consistent", "bounce_detached_set_002": "consistent", "diamond_detached_set_002": "contradicted"}}` |
| E3a | **contradicted** | `{"by_arm": {"ring_detached_set_002": "consistent", "solo_detached_set_002": "consistent", "dyad_detached_set_002": "consistent", "bounce_detached_set_002": "consistent", "diamond_detached_set_002": "contradicted"}}` |
| E3b | **contradicted** | `{"by_arm": {"ring_detached_set_002": "consistent", "solo_detached_set_002": "consistent", "dyad_detached_set_002": "consistent", "bounce_detached_set_002": "consistent", "diamond_detached_set_002": "contradicted"}}` |
| E4 | **contradicted** | `{"by_arm": {"solo_detached_set_002": "contradicted"}}` |
| E5 | **contradicted** | `{"lineage_discount_rate_by_shape": {"ring": 0.465278, "solo": 0.458333, "dyad": 0.486111, "bounce": 0.513889}, "required_order": ["ring", "bounce", "dyad", "solo"]}` |
| E6 | **contradicted** | `{"by_arm": {"ring_detached_set_002": "consistent", "bounce_detached_set_002": "consistent", "diamond_detached_set_002": "contradicted"}, "tiers": {"ring_detached_set_002": 1, "bounce_detached_set_002": 1, "diamond_detached_set_002": 2}}` |
| E7 | **assessed in the synthesis across Set 001 and Set 002, not in a single-stage audit** | `{}` |

## Paired displacement and divergence by arm (E3a, E3b)

| Set | Condition | Worlds with Ā > .01 | E3a | Divergence modal class | Tie | Non-monotonic worlds | E3b |
|---|---|---:|---|---|---|---:|---|
| `ring_detached_set_002` | free | 7/12 | consistent | increasing | no | 2 | consistent |
| `ring_detached_set_002` | lineage | 12/12 | consistent | increasing | no | 1 | consistent |
| `solo_detached_set_002` | free | 7/12 | consistent | increasing | no | 5 | consistent |
| `solo_detached_set_002` | lineage | 10/12 | consistent | increasing | no | 3 | consistent |
| `dyad_detached_set_002` | free | 7/12 | consistent | increasing | no | 1 | consistent |
| `dyad_detached_set_002` | lineage | 10/12 | consistent | increasing | no | 1 | consistent |
| `bounce_detached_set_002` | free | 10/12 | consistent | increasing | no | 0 | consistent |
| `bounce_detached_set_002` | lineage | 12/12 | consistent | increasing | no | 0 | consistent |
| `diamond_detached_set_002` | free | 6/12 | contradicted | stable | no | 3 | contradicted |
| `diamond_detached_set_002` | lineage | 12/12 | consistent | increasing | no | 3 | consistent |

## Far-agent compounding by arm (E2) and within-detached LINEAGE rates (E5 quantity)

| Set | Far agent | Condition | Modal class | E2 | Stage mean excess (far) | Mean last − first | LINEAGE discount rate | LINEAGE inflation rate | Twin discount rate |
|---|---|---|---|---|---:|---:|---:|---:|---:|
| `ring_detached_set_002` | C | free | increasing | consistent | -0.018 | +0.043 | +0.465 | +0.007 | +0.215 |
| `ring_detached_set_002` | C | lineage | increasing | consistent | -0.055 | +0.128 | +0.465 | +0.007 | +0.215 |
| `solo_detached_set_002` | A | free | increasing | consistent | -0.021 | +0.043 | +0.458 | +0.014 | +0.000 |
| `solo_detached_set_002` | A | lineage | increasing | consistent | -0.055 | +0.121 | +0.458 | +0.014 | +0.000 |
| `dyad_detached_set_002` | B | free | increasing | consistent | -0.027 | +0.052 | +0.486 | +0.000 | +0.014 |
| `dyad_detached_set_002` | B | lineage | increasing | consistent | -0.054 | +0.114 | +0.486 | +0.000 | +0.014 |
| `bounce_detached_set_002` | C | free | increasing | consistent | -0.021 | +0.054 | +0.514 | +0.000 | +0.104 |
| `bounce_detached_set_002` | C | lineage | increasing | consistent | -0.057 | +0.118 | +0.514 | +0.000 | +0.104 |
| `diamond_detached_set_002` | D | free | stable | contradicted | +0.002 | +0.018 | +0.583 | +0.099 | +0.068 |
| `diamond_detached_set_002` | D | lineage | increasing | consistent | -0.043 | +0.089 | +0.583 | +0.099 | +0.068 |

## Origin after lineage return (E6, strict H1) with descriptive frequency tiers

| Set | Verdict | Tier | Detached LINEAGE events / firings | Mean, max magnitude | Worlds with event | Consecutive | Twin LINEAGE events / firings | Detached FREE events | FIS>0 at events |
|---|---|---|---|---|---:|---:|---|---:|---|
| `ring_detached_set_002` | **consistent** | 1 (no qualifying detached event) | 0 / 48 | n/a, n/a | 0 | 0 | 8 / 48 | 2 | not probed |
| `bounce_detached_set_002` | **consistent** | 1 (no qualifying detached event) | 0 / 36 | n/a, n/a | 0 | 0 | 2 / 36 | 2 | not probed |
| `diamond_detached_set_002` | **contradicted** | 2 (detached rate below the twin's) | 6 / 48 | +0.033, +0.080 | 6 | 0 | 7 / 48 | 4 | 0 |

## Relay-position marker loss (E1)

| Set | Condition | Marker | Detached R first → last (loss) | Twin R first → last (loss) | Marker verdict |
|---|---|---|---|---|---|
| `ring_detached_set_002` | free | source_named | 0.875 → 0.833 (+0.042) | 1.000 → 1.000 (+0.000) | consistent |
| `ring_detached_set_002` | free | reliability_named | 0.958 → 0.167 (+0.792) | 1.000 → 0.667 (+0.333) | consistent |
| `ring_detached_set_002` | lineage | source_named | 0.833 → 0.167 (+0.667) | 0.917 → 0.375 (+0.542) | consistent |
| `ring_detached_set_002` | lineage | reliability_named | 1.000 → 0.125 (+0.875) | 1.000 → 0.292 (+0.708) | consistent |
| `dyad_detached_set_002` | free | source_named | 0.833 → 0.833 (+0.000) | 0.917 → 1.000 (-0.083) | consistent |
| `dyad_detached_set_002` | free | reliability_named | 1.000 → 0.333 (+0.667) | 1.000 → 0.833 (+0.167) | consistent |
| `dyad_detached_set_002` | lineage | source_named | 0.917 → 0.167 (+0.750) | 0.917 → 0.917 (+0.000) | consistent |
| `dyad_detached_set_002` | lineage | reliability_named | 1.000 → 0.167 (+0.833) | 1.000 → 0.833 (+0.167) | consistent |
| `bounce_detached_set_002` | free | source_named | 1.000 → 0.917 (+0.083) | 1.000 → 1.000 (+0.000) | consistent |
| `bounce_detached_set_002` | free | reliability_named | 0.833 → 0.083 (+0.750) | 0.972 → 0.833 (+0.139) | consistent |
| `bounce_detached_set_002` | lineage | source_named | 1.000 → 0.194 (+0.806) | 0.833 → 0.611 (+0.222) | consistent |
| `bounce_detached_set_002` | lineage | reliability_named | 0.944 → 0.083 (+0.861) | 0.972 → 0.583 (+0.389) | consistent |
| `diamond_detached_set_002` | free | source_named | 0.972 → 0.694 (+0.278) | 1.000 → 0.667 (+0.333) | contradicted |
| `diamond_detached_set_002` | free | reliability_named | 0.972 → 0.444 (+0.528) | 1.000 → 0.972 (+0.028) | consistent |
| `diamond_detached_set_002` | lineage | source_named | 1.000 → 0.194 (+0.806) | 0.972 → 0.278 (+0.694) | consistent |
| `diamond_detached_set_002` | lineage | reliability_named | 0.972 → 0.000 (+0.972) | 0.944 → 0.417 (+0.528) | consistent |

## Secondary: origin firings by whether the inbound message named the sensor (descriptive, no verdict)

| Set | Condition | Inbound | Firings | Inflation | Discount | Events > .01 | FIS>0 | Mean excess |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `ring_detached_set_002` | free | inbound_named_sensor | 40 | 2 | 14 | 2 | 0 | -0.021 |
| `ring_detached_set_002` | free | inbound_unnamed | 8 | 0 | 7 | 0 | 0 | -0.065 |
| `ring_detached_set_002` | lineage | inbound_named_sensor | 23 | 0 | 4 | 0 | 0 | -0.018 |
| `ring_detached_set_002` | lineage | inbound_unnamed | 25 | 0 | 22 | 0 | 0 | -0.113 |
| `dyad_detached_set_002` | free | inbound_named_sensor | 60 | 0 | 18 | 0 | 0 | -0.018 |
| `dyad_detached_set_002` | free | inbound_unnamed | 12 | 0 | 6 | 0 | 0 | -0.100 |
| `dyad_detached_set_002` | lineage | inbound_named_sensor | 42 | 0 | 12 | 0 | 0 | -0.024 |
| `dyad_detached_set_002` | lineage | inbound_unnamed | 30 | 0 | 26 | 0 | 0 | -0.128 |
| `bounce_detached_set_002` | free | inbound_named_sensor | 34 | 2 | 20 | 2 | 0 | -0.032 |
| `bounce_detached_set_002` | free | inbound_unnamed | 2 | 0 | 1 | 0 | 0 | -0.040 |
| `bounce_detached_set_002` | lineage | inbound_named_sensor | 17 | 0 | 3 | 0 | 0 | -0.014 |
| `bounce_detached_set_002` | lineage | inbound_unnamed | 19 | 0 | 19 | 0 | 0 | -0.144 |
| `diamond_detached_set_002` | free | inbound_named_sensor | 41 | 4 | 5 | 4 | 0 | +0.000 |
| `diamond_detached_set_002` | free | inbound_unnamed | 7 | 0 | 2 | 0 | 0 | -0.013 |
| `diamond_detached_set_002` | lineage | inbound_named_sensor | 25 | 2 | 10 | 2 | 0 | -0.020 |
| `diamond_detached_set_002` | lineage | inbound_unnamed | 23 | 4 | 19 | 4 | 0 | -0.067 |

## MACRO stopping boundary

| Set | Seed | Stop event | MACRO events | Responses reused |
|---|---:|---|---:|---|
| `ring_detached_set_002` | 818285910 | M04 | 4 | True |
| `ring_detached_set_002` | 588710334 | M04 | 4 | True |
| `ring_detached_set_002` | 1246964244 | M04 | 4 | True |
| `ring_detached_set_002` | 1138823197 | M04 | 4 | True |
| `ring_detached_set_002` | 882867208 | M04 | 4 | True |
| `ring_detached_set_002` | 1468093150 | M04 | 4 | True |
| `ring_detached_set_002` | 1032002992 | M04 | 4 | True |
| `ring_detached_set_002` | 245389550 | M04 | 4 | True |
| `ring_detached_set_002` | 652866105 | M04 | 4 | True |
| `ring_detached_set_002` | 28092603 | M04 | 4 | True |
| `ring_detached_set_002` | 1582931821 | M04 | 4 | True |
| `ring_detached_set_002` | 1792403557 | M04 | 4 | True |
| `solo_detached_set_002` | 818285910 | M02 | 2 | True |
| `solo_detached_set_002` | 588710334 | M02 | 2 | True |
| `solo_detached_set_002` | 1246964244 | M02 | 2 | True |
| `solo_detached_set_002` | 1138823197 | M02 | 2 | True |
| `solo_detached_set_002` | 882867208 | M02 | 2 | True |
| `solo_detached_set_002` | 1468093150 | M02 | 2 | True |
| `solo_detached_set_002` | 1032002992 | M02 | 2 | True |
| `solo_detached_set_002` | 245389550 | M02 | 2 | True |
| `solo_detached_set_002` | 652866105 | M02 | 2 | True |
| `solo_detached_set_002` | 28092603 | M02 | 2 | True |
| `solo_detached_set_002` | 1582931821 | M02 | 2 | True |
| `solo_detached_set_002` | 1792403557 | M02 | 2 | True |
| `dyad_detached_set_002` | 818285910 | M03 | 3 | True |
| `dyad_detached_set_002` | 588710334 | M03 | 3 | True |
| `dyad_detached_set_002` | 1246964244 | M03 | 3 | True |
| `dyad_detached_set_002` | 1138823197 | M03 | 3 | True |
| `dyad_detached_set_002` | 882867208 | M03 | 3 | True |
| `dyad_detached_set_002` | 1468093150 | M03 | 3 | True |
| `dyad_detached_set_002` | 1032002992 | M03 | 3 | True |
| `dyad_detached_set_002` | 245389550 | M03 | 3 | True |
| `dyad_detached_set_002` | 652866105 | M03 | 3 | True |
| `dyad_detached_set_002` | 28092603 | M03 | 3 | True |
| `dyad_detached_set_002` | 1582931821 | M03 | 3 | True |
| `dyad_detached_set_002` | 1792403557 | M03 | 3 | True |
| `bounce_detached_set_002` | 818285910 | M05 | 5 | True |
| `bounce_detached_set_002` | 588710334 | M05 | 5 | True |
| `bounce_detached_set_002` | 1246964244 | M05 | 5 | True |
| `bounce_detached_set_002` | 1138823197 | M05 | 5 | True |
| `bounce_detached_set_002` | 882867208 | M05 | 5 | True |
| `bounce_detached_set_002` | 1468093150 | M05 | 5 | True |
| `bounce_detached_set_002` | 1032002992 | M05 | 5 | True |
| `bounce_detached_set_002` | 245389550 | M05 | 5 | True |
| `bounce_detached_set_002` | 652866105 | M05 | 5 | True |
| `bounce_detached_set_002` | 28092603 | M05 | 5 | True |
| `bounce_detached_set_002` | 1582931821 | M05 | 5 | True |
| `bounce_detached_set_002` | 1792403557 | M05 | 5 | True |
| `diamond_detached_set_002` | 316127362 | M05 | 5 | True |
| `diamond_detached_set_002` | 710597220 | M05 | 5 | True |
| `diamond_detached_set_002` | 962632369 | M05 | 5 | True |
| `diamond_detached_set_002` | 241955308 | M05 | 5 | True |
| `diamond_detached_set_002` | 723648650 | M05 | 5 | True |
| `diamond_detached_set_002` | 1054956113 | M05 | 5 | True |
| `diamond_detached_set_002` | 1831325112 | M05 | 5 | True |
| `diamond_detached_set_002` | 374607106 | M05 | 5 | True |
| `diamond_detached_set_002` | 443947794 | M05 | 5 | True |
| `diamond_detached_set_002` | 533125286 | M05 | 5 | True |
| `diamond_detached_set_002` | 633201644 | M05 | 5 | True |
| `diamond_detached_set_002` | 1092129420 | M05 | 5 | True |

## Problems

None.

## Boundary

Descriptive and pre-registered. Worlds are the unit; arms, stages, conditions and agents are reported separately. Paired quantities carry their twin's execution dates and are never corrected for drift. E6 tiers are frequency descriptions, not mechanism labels; nothing here bears on H2. Negative results stand.

Within-agent trajectories, per-world paired sequences and retention by depth are in the JSON record under `arms.<set>.within_agent`, `arms.<set>.paired.<condition>.worlds` and `arms.<set>.retention`.