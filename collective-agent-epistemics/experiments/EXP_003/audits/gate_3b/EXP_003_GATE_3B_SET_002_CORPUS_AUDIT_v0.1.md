# EXP-003 Gate 3B Set 002 Corpus Integrity Audit v0.1

## Status

**PASS**

Read-only corpus/provenance audit. Scientific interpretation was **not performed**.

## Provenance

- Plan: `GATE_3B_PLAN_v0.1` (status `FROZEN`, sha256 `5cea3ad5959b1ecfa9080f3bfad834b75366d9841fa6739e965bf69e0036a672`)
- Frozen runtime: `c54563bbb3f17e49c70e8e4f2e3a0369910d3c15`; protocol tag `exp-003-protocol-v0.1`
- Plan freeze commit: `e4526dfd3b3bc58fe2334bb85b106b45423a6a03`
- Derivation anchor: `1daa069af7000613ba06af35714bc22764c1f409|exp-003-protocol-v0.1|GATE_3B_PLAN_v0.1`
- HEAD at audit time: `b31f992a5cd17b73cd35978ce82da37bdae00908`
- Frozen runtime drift: none
- Expected run class: `gate_3b_real_model`; model `gpt-5.6-sol`; effort `medium`; paired; reliability `0.7`

## Corpus shape

| Set | Topology | Rounds | Probe | Manifest sha256 | Planned | Complete | Calls/world | Events/world | Actual calls | Tokens |
|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|
| `diamond_set_002` | diamond | 4 | on | `2449fcb65562…` | 12 | 12 | 33 | 39 | 396 | 138975 |
| `dual_root_set_002` | diamond | 4 | on | `26f224f13df3…` | 16 | 16 | 33 | 43 | 528 | 232758 |

Totals: planned 28, complete 28, actual provider calls 924, tokens 371733, technical failure records 0.

## Technical failures (preserved, excluded from scientific N)

None.

## Mechanical verification

- Archived worlds equal the manifest's worlds for every set: PASS
- Exactly one complete attempt per world: PASS
- Raw file SHA-256 hashes match archive records: PASS
- Run class, provider, model, effort, probe, topology, root mode, rounds, call count, fallbacks, frozen runtime, plan freeze commit, manifest hash, seed and cell per attempt: PASS
- Event structure (count, three conditions, max depth, root set, served model on every event, no fallback-served event): PASS
- Frozen runtime drift: none

## Per-world raw hashes

### `diamond_set_002`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3B_GEN002_seed_316127362` | B/A | attempt_001 | attempt_001 | `aa12f127df11` | `fc251e74c754` | `c12601147af3` |
| 2 | `E3_G3B_GEN002_seed_710597220` | B/A | attempt_001 | attempt_001 | `eebece2f8bd1` | `b23596b9009f` | `8ff867431176` |
| 3 | `E3_G3B_GEN002_seed_962632369` | A/A | attempt_001 | attempt_001 | `3c6c1fdb964c` | `f7601c5e19a1` | `e01b97d26155` |
| 4 | `E3_G3B_GEN002_seed_241955308` | B/B | attempt_001 | attempt_001 | `3000d3b0c757` | `d3fa879f9b2c` | `b03a9dfeb717` |
| 5 | `E3_G3B_GEN002_seed_723648650` | A/B | attempt_001 | attempt_001 | `af9a49955998` | `c479a707c777` | `83d89b3b755d` |
| 6 | `E3_G3B_GEN002_seed_1054956113` | B/A | attempt_001 | attempt_001 | `da9b25171614` | `76114897789c` | `fa19b3f24758` |
| 7 | `E3_G3B_GEN002_seed_1831325112` | B/B | attempt_001 | attempt_001 | `d11056fc968a` | `182e005c186f` | `b41296585124` |
| 8 | `E3_G3B_GEN002_seed_374607106` | B/B | attempt_001 | attempt_001 | `6d9e7c775336` | `c6fc46cd9eb3` | `0caac61712fc` |
| 9 | `E3_G3B_GEN002_seed_443947794` | B/B | attempt_001 | attempt_001 | `535bc80d57f5` | `fce507691e85` | `648647b011ee` |
| 10 | `E3_G3B_GEN002_seed_533125286` | A/B | attempt_001 | attempt_001 | `285c50a0cd4c` | `06b3952393ad` | `89ee36067049` |
| 11 | `E3_G3B_GEN002_seed_633201644` | B/B | attempt_001 | attempt_001 | `3b58f8e48799` | `8f7d1eac2bd2` | `966d52bb39c7` |
| 12 | `E3_G3B_GEN002_seed_1092129420` | B/A | attempt_001 | attempt_001 | `b23f76706f77` | `e121aef38976` | `87fe80ed7e20` |

### `dual_root_set_002`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3B_DUAL002_seed_1761851777` | A/B/B | attempt_001 | attempt_001 | `c75f2f43c0cb` | `c5ff36f428f0` | `859116a0ee31` |
| 2 | `E3_G3B_DUAL002_seed_1516256562` | B/A/A | attempt_001 | attempt_001 | `09d9668c0b26` | `cb614bbd1333` | `11d69101993a` |
| 3 | `E3_G3B_DUAL002_seed_1614821534` | B/A/A | attempt_001 | attempt_001 | `847be837f8e8` | `7fc267bf1a90` | `4833459ea82b` |
| 4 | `E3_G3B_DUAL002_seed_1943818421` | B/A/B | attempt_001 | attempt_001 | `3a8dad883087` | `6570bf1a4e7b` | `2cdfcf1a309f` |
| 5 | `E3_G3B_DUAL002_seed_2082756798` | B/B/B | attempt_001 | attempt_001 | `0fcd61c2a0cf` | `51ab1f1015db` | `684181ae6d79` |
| 6 | `E3_G3B_DUAL002_seed_1068989073` | B/B/B | attempt_001 | attempt_001 | `2f9bb6b42892` | `cd5cee92e8d5` | `2e5bacd4a711` |
| 7 | `E3_G3B_DUAL002_seed_1150363503` | B/B/A | attempt_001 | attempt_001 | `6fd5fd7afb92` | `6d6f7c2bc3c1` | `d8740c16788d` |
| 8 | `E3_G3B_DUAL002_seed_1587692757` | A/A/B | attempt_001 | attempt_001 | `da579b252f3a` | `5c83ae18d3bc` | `03f13f8a2e4d` |
| 9 | `E3_G3B_DUAL002_seed_1264392180` | A/A/B | attempt_001 | attempt_001 | `16a92ee9bee7` | `095123e0791b` | `35bc43bccff6` |
| 10 | `E3_G3B_DUAL002_seed_2017093923` | A/A/A | attempt_001 | attempt_001 | `5d3c0753f0d1` | `1f70048122f0` | `6fbda6401c4b` |
| 11 | `E3_G3B_DUAL002_seed_216987976` | A/B/A | attempt_001 | attempt_001 | `cf921d6dd445` | `c63037da785f` | `a2044569c578` |
| 12 | `E3_G3B_DUAL002_seed_1119880167` | A/B/B | attempt_001 | attempt_001 | `c3911c696243` | `671f08c7460f` | `56fc747ce77e` |
| 13 | `E3_G3B_DUAL002_seed_1629652161` | A/A/A | attempt_001 | attempt_001 | `2e6b59300f1d` | `e0513f587f08` | `b5ee2a591317` |
| 14 | `E3_G3B_DUAL002_seed_1322584095` | A/B/A | attempt_001 | attempt_001 | `b25449986289` | `c1a287b5b744` | `7d870c92da7d` |
| 15 | `E3_G3B_DUAL002_seed_80913935` | B/A/B | attempt_001 | attempt_001 | `e6999646649a` | `4f3677e2e130` | `bc37b24cb76a` |
| 16 | `E3_G3B_DUAL002_seed_479525595` | B/B/A | attempt_001 | attempt_001 | `3acdb2c737cb` | `e00b4c6b7332` | `13a22a18a3fa` |

## Scientific boundary

No answer, confidence, P(A), Brier, message, provenance mark, excess, FIS, DSCD, FREE/LINEAGE comparison or any other outcome was read, computed or reported. This audit establishes that data collection for the stage is complete and technically sound. It is not an interpretation.

## Replication start condition

A PASS here means this stage's data collection is complete. Under the frozen plan, the replication stage (Set 002) starts after Set 001 passes this audit and before any primary-outcome audit of Set 001, so that Set 002 runs regardless of what Set 001 shows. Gate closure requires both stages.
