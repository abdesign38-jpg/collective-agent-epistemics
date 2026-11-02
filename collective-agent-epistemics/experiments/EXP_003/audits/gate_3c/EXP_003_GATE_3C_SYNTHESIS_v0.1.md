# EXP-003 Gate 3C Synthesis v0.1

## Status

**SYNTHESIS** (mechanical, cross-stage)

Mechanical cross-stage placement of two pre-registered audits. No pooling of stages or arms, no test, no threshold beyond the spec's flat band, no drift correction, no causal or mechanism claim, nothing on H2. The relation to the hypothesis is written separately under research/observations/.

## Sources

- set_001: `experiments/EXP_003/audits/gate_3c/EXP_003_GATE_3C_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1.json` (sha256 `7ca623fc362ae8b05750d232bd05e79aa813388d903454ae8e83b807e95b2053`)
- set_001_corpus: `experiments/EXP_003/audits/gate_3c/EXP_003_GATE_3C_SET_001_CORPUS_AUDIT_v0.1.json` (sha256 `b4f6ef16c6cd27fb3eceec96706b43530026c6395b93848893e55528cdcff9b7`)
- set_002: `experiments/EXP_003/audits/gate_3c/EXP_003_GATE_3C_SET_002_PRIMARY_OUTCOME_AUDIT_v0.1.json` (sha256 `f76eb5198db7733c5986141c8651eab7f2e92524a8bc7267d704ee8ee1099b9f`)
- set_002_corpus: `experiments/EXP_003/audits/gate_3c/EXP_003_GATE_3C_SET_002_CORPUS_AUDIT_v0.1.json` (sha256 `444d5a6f81fb3933d5cb10fcb274a4aaf791d50b6c256d524ccbb0c5624bc92b`)
- HEAD at synthesis time: `ae0519861c3b552da9a0d1c18998c0ad08452961`

## Pre-registered expectations, both stages

| Id | set_001 | set_002 | Agree | Standing |
|---|---|---|---|---|
| E1 | **contradicted** | **contradicted** | yes | set_001: primary (same-window twins); set_002: qualified (historical twins) |
| E2 | **contradicted** | **contradicted** | yes | set_001: primary (within-detached); set_002: primary (within-detached) |
| E3a | **contradicted** | **contradicted** | yes | set_001: primary (same-window twins); set_002: qualified (historical twins) |
| E3b | **consistent** | **contradicted** | no | set_001: primary (same-window twins); set_002: qualified (historical twins) |
| E4 | **contradicted** | **contradicted** | yes | set_001: primary (within-detached); set_002: primary (within-detached) |
| E5 | **contradicted** | **contradicted** | yes | set_001: primary (within-detached); set_002: primary (within-detached) |
| E6 | **contradicted** | **contradicted** | yes | set_001: primary (within-detached); set_002: primary (within-detached) |
| E7 | cross-stage | cross-stage | **consistent** | within-detached |

E7 cells (stage mean certainty excess at the far position; flat band ±0.005):

| Cell | set_001 | set_002 | Signs | Reversed |
|---|---:|---:|---|---|
| ring_free | -0.018 | -0.018 | negative / negative | no |
| ring_lineage | -0.056 | -0.055 | negative / negative | no |
| solo_free | -0.019 | -0.021 | negative / negative | no |
| solo_lineage | -0.060 | -0.055 | negative / negative | no |
| dyad_free | -0.046 | -0.027 | negative / negative | no |
| dyad_lineage | -0.061 | -0.054 | negative / negative | no |
| bounce_free | -0.008 | -0.021 | negative / negative | no |
| bounce_lineage | -0.069 | -0.057 | negative / negative | no |
| diamond_free | +0.006 | +0.002 | positive / flat | no |
| diamond_lineage | -0.049 | -0.043 | negative / negative | no |

## Descriptive replication (no verdict)

| Quantity | Shape | Condition | set_001 | set_002 |
|---|---|---|---|---|
| far-agent compounding (mean last − first) | ring | free | +0.043 | +0.043 |
| far-agent compounding (mean last − first) | ring | lineage | +0.131 | +0.128 |
| E6 strict verdict | ring | lineage | consistent | consistent |
| far-agent compounding (mean last − first) | solo | free | +0.052 | +0.043 |
| far-agent compounding (mean last − first) | solo | lineage | +0.114 | +0.121 |
| far-agent compounding (mean last − first) | dyad | free | +0.105 | +0.052 |
| far-agent compounding (mean last − first) | dyad | lineage | +0.138 | +0.114 |
| far-agent compounding (mean last − first) | bounce | free | +0.023 | +0.054 |
| far-agent compounding (mean last − first) | bounce | lineage | +0.140 | +0.118 |
| E6 strict verdict | bounce | lineage | consistent | consistent |
| far-agent compounding (mean last − first) | diamond | free | +0.024 | +0.018 |
| far-agent compounding (mean last − first) | diamond | lineage | +0.107 | +0.089 |
| E6 strict verdict | diamond | lineage | contradicted | contradicted |

## Set 002 paired verdicts (historical controls, qualified)

Set 002 pairs are against historical controls and are not same-window evidence; never pooled with Set 001, never corrected by the gauge.

| Stage | E1 | E3a | E3b | Set 001 drift gauge |
|---|---|---|---|---|
| set_002 | contradicted | contradicted | contradicted | FAIL |

## Twins and temporal gaps

| Stage | Set | Twin | Kind | Twin dates | Max gap (days) |
|---|---|---|---|---|---:|
| set_001 | `ring_detached_set_001` | ring_contemporary_set_001 | contemporary | 2026-11-02 | 1 |
| set_001 | `solo_detached_set_001` | solo_contemporary_set_001 | contemporary | 2026-11-02 | 1 |
| set_001 | `dyad_detached_set_001` | dyad_contemporary_set_001 | contemporary | 2026-11-02 | 1 |
| set_001 | `bounce_detached_set_001` | bounce_contemporary_set_001 | contemporary | 2026-11-02 | 1 |
| set_001 | `diamond_detached_set_001` | diamond_set_001 | historical | 2026-10-30 | 2 |
| set_001 | `ring_contemporary_set_001` | ring_control_set_001 | historical |  |  |
| set_002 | `ring_detached_set_002` | ring_control_set_002 | historical | 2026-10-02 | 30 |
| set_002 | `solo_detached_set_002` | solo_control_set_002 | historical | 2026-10-02 | 30 |
| set_002 | `dyad_detached_set_002` | dyad_set_002 | historical | 2026-10-02 | 30 |
| set_002 | `bounce_detached_set_002` | bounce_set_002 | historical | 2026-10-02 | 30 |
| set_002 | `diamond_detached_set_002` | diamond_set_002 | historical | 2026-10-31 | 1 |

## Closure rule

| Requirement | Status |
|---|---|
| both stages' manifests prospectively frozen | yes: plan status FROZEN |
| every world in all fourteen arms has a valid archived execution or a documented technical failure | yes: corpus audits set_001: PASS; set_002: PASS, 168/168 complete, 1 technical failure record(s) preserved |
| raw outputs immutable | yes: SHA-256 per raw file recorded in each corpus audit and re-checked by each primary-outcome audit, twins included |
| manipulation check passed in every detached arm | yes |
| predefined primary outcomes audited | yes: 2 stage audit(s) under EXP-003-GATE-3C-PRIMARY-OUTCOME-AUDIT-SPEC-v0.1 |
| arms, stages, conditions and agents reported separately; twins dated | yes: per-arm tables in each stage audit; this synthesis keeps one column per stage |
| drift gauge recorded | yes: FAIL (observed behavior differed across execution windows under the same nominal model configuration) |
| Set 002 paired verdicts qualified as historical-control evidence, never pooled or corrected | yes |
| negative results retained | yes: 13 contradicted single-stage expectation verdict(s) stand as written |

## Boundary

Mechanical cross-stage placement of two pre-registered audits. No pooling of stages or arms, no test, no threshold beyond the spec's flat band, no drift correction, no causal or mechanism claim, nothing on H2. The relation to the hypothesis is written separately under research/observations/.
