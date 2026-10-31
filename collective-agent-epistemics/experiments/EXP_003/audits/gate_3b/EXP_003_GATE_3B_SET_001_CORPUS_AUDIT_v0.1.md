# EXP-003 Gate 3B Set 001 Corpus Integrity Audit v0.1

## Status

**PASS**

Read-only corpus/provenance audit. Scientific interpretation was **not performed**.

## Provenance

- Plan: `GATE_3B_PLAN_v0.1` (status `FROZEN`, sha256 `5cea3ad5959b1ecfa9080f3bfad834b75366d9841fa6739e965bf69e0036a672`)
- Frozen runtime: `c54563bbb3f17e49c70e8e4f2e3a0369910d3c15`; protocol tag `exp-003-protocol-v0.1`
- Plan freeze commit: `e4526dfd3b3bc58fe2334bb85b106b45423a6a03`
- Derivation anchor: `1daa069af7000613ba06af35714bc22764c1f409|exp-003-protocol-v0.1|GATE_3B_PLAN_v0.1`
- HEAD at audit time: `b7cc4809b4210d5f6e236a39b61697c7e520ae58`
- Frozen runtime drift: none
- Expected run class: `gate_3b_real_model`; model `gpt-5.6-sol`; effort `medium`; paired; reliability `0.7`

## Corpus shape

| Set | Topology | Rounds | Probe | Manifest sha256 | Planned | Complete | Calls/world | Events/world | Actual calls | Tokens |
|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|
| `diamond_set_001` | diamond | 4 | on | `f607a0365e20…` | 12 | 12 | 33 | 39 | 396 | 139873 |
| `dual_root_set_001` | diamond | 4 | on | `956f555d49d2…` | 16 | 16 | 33 | 43 | 528 | 231953 |
| `solo_control_set_003` | solo | 12 | on | `5d34fb7e3986…` | 12 | 12 | 25 | 28 | 300 | 96568 |
| `probe_off_set_001` | diamond | 4 | off | `59b5edd09712…` | 4 | 4 | 33 | 39 | 132 | 46626 |

Totals: planned 44, complete 44, actual provider calls 1356, tokens 515020, technical failure records 3.

## Technical failures (preserved, excluded from scientific N)

| Set | World | Attempt | Exception | Message | Timestamp |
|---|---|---|---|---|---|
| `diamond_set_001` | `E3_G3B_GEN001_seed_745425377` | attempt_001 | `OpenAIAdapterError` | OpenAI Responses request failed | 2026-10-30T21:45:45.430674+00:00 |
| `dual_root_set_001` | `E3_G3B_DUAL001_seed_617684863` | attempt_001 | `OpenAIAdapterError` | OpenAI Responses request failed | 2026-10-30T22:05:26.306161+00:00 |
| `solo_control_set_003` | `E3_G3B_SOLO003_seed_1476859861` | attempt_001 | `OpenAIAdapterError` | OpenAI Responses request failed | 2026-10-30T22:53:31.268196+00:00 |

## Mechanical verification

- Archived worlds equal the manifest's worlds for every set: PASS
- Exactly one complete attempt per world: PASS
- Raw file SHA-256 hashes match archive records: PASS
- Run class, provider, model, effort, probe, topology, root mode, rounds, call count, fallbacks, frozen runtime, plan freeze commit, manifest hash, seed and cell per attempt: PASS
- Event structure (count, three conditions, max depth, root set, served model on every event, no fallback-served event): PASS
- Frozen runtime drift: none

## Per-world raw hashes

### `diamond_set_001`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3B_GEN001_seed_1672462843` | A/A | attempt_001 | attempt_001 | `2cf7142416de` | `89cdf5c0dbed` | `27dd5fc33b1e` |
| 2 | `E3_G3B_GEN001_seed_63901144` | A/B | attempt_001 | attempt_001 | `5d03722c646e` | `0a4d1951bb97` | `337925ca7cac` |
| 3 | `E3_G3B_GEN001_seed_323832400` | A/A | attempt_001 | attempt_001 | `e3855e12602d` | `dd1250f47525` | `faa8bf057a5e` |
| 4 | `E3_G3B_GEN001_seed_1566825802` | B/B | attempt_001 | attempt_001 | `aec8fa488aff` | `0997decdce1a` | `36f63cfd5c01` |
| 5 | `E3_G3B_GEN001_seed_277459948` | A/A | attempt_001 | attempt_001 | `4f53c1060f09` | `e220e40f071c` | `f4a3f4c5768f` |
| 6 | `E3_G3B_GEN001_seed_743291108` | A/A | attempt_001 | attempt_001 | `0db5f31262cb` | `b5dbd2fce10d` | `dd3615d94d29` |
| 7 | `E3_G3B_GEN001_seed_2020380812` | B/B | attempt_001 | attempt_001 | `229932f6008d` | `beb975a51482` | `82d8759fc2f1` |
| 8 | `E3_G3B_GEN001_seed_1292406070` | A/A | attempt_001 | attempt_001 | `ac493948d86e` | `9d2cfaa4eb88` | `835c3529a399` |
| 9 | `E3_G3B_GEN001_seed_187031691` | A/A | attempt_001 | attempt_001 | `1624b5ec7599` | `4e9af21c4852` | `0e2646c1ecc6` |
| 10 | `E3_G3B_GEN001_seed_1476859861` | A/A | attempt_001 | attempt_001 | `2f1699f9cc04` | `009d8e7bceb2` | `a6bef526636e` |
| 11 | `E3_G3B_GEN001_seed_745425377` | B/A | attempt_001, attempt_002 | attempt_002 | `f2bae792b7b5` | `c5d23e0c6e66` | `cfbbc4d9d1e0` |
| 12 | `E3_G3B_GEN001_seed_1686133698` | A/A | attempt_001 | attempt_001 | `059b6b4d60a8` | `e4dfedbc2642` | `2be3a208da68` |

### `dual_root_set_001`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3B_DUAL001_seed_617684863` | A/A/B | attempt_001, attempt_002 | attempt_002 | `9c31c492d105` | `bff6206fef11` | `f2fd72b2594d` |
| 2 | `E3_G3B_DUAL001_seed_1230824526` | B/B/B | attempt_001 | attempt_001 | `24e8c440a674` | `ba96a2b0c02c` | `508bb61f3d1e` |
| 3 | `E3_G3B_DUAL001_seed_1430476680` | B/B/B | attempt_001 | attempt_001 | `9cec5db8e234` | `44e2d11a27ff` | `f194b1b9fd2c` |
| 4 | `E3_G3B_DUAL001_seed_786534487` | B/A/A | attempt_001 | attempt_001 | `ed43c18d0ac5` | `2736728776ce` | `e21c8acf43d4` |
| 5 | `E3_G3B_DUAL001_seed_452662356` | B/B/A | attempt_001 | attempt_001 | `7edaa64bf443` | `d2de941b2584` | `0c63f1b229fc` |
| 6 | `E3_G3B_DUAL001_seed_1703800204` | B/A/A | attempt_001 | attempt_001 | `7165d32e1b0c` | `be31ed3d7a20` | `f55291507f3b` |
| 7 | `E3_G3B_DUAL001_seed_805591371` | A/A/B | attempt_001 | attempt_001 | `3503785dc9d0` | `f932f59e217c` | `a66b79544d6a` |
| 8 | `E3_G3B_DUAL001_seed_2105050229` | B/B/A | attempt_001 | attempt_001 | `1665a5965866` | `9295a13cae04` | `6ab45f5bb929` |
| 9 | `E3_G3B_DUAL001_seed_503343741` | A/B/A | attempt_001 | attempt_001 | `5a032df22a9d` | `6a2812a2acd2` | `7e4ddc69305e` |
| 10 | `E3_G3B_DUAL001_seed_1074206943` | A/A/A | attempt_001 | attempt_001 | `cb30e89aaf32` | `4f7ade239e0f` | `0ae33d5d0f79` |
| 11 | `E3_G3B_DUAL001_seed_1975068904` | B/A/B | attempt_001 | attempt_001 | `4b86e72f5896` | `d1e89e0aa68c` | `5edda0584604` |
| 12 | `E3_G3B_DUAL001_seed_1617711318` | A/B/B | attempt_001 | attempt_001 | `eec6336f6bfc` | `4f3ae855c9a1` | `660ca70c9108` |
| 13 | `E3_G3B_DUAL001_seed_264003842` | A/B/A | attempt_001 | attempt_001 | `f65a1ba9cedb` | `c5295d339b4d` | `e095a935c2be` |
| 14 | `E3_G3B_DUAL001_seed_153299879` | B/A/B | attempt_001 | attempt_001 | `52afa1caf9fd` | `f60bbdadddf1` | `b9a31538782b` |
| 15 | `E3_G3B_DUAL001_seed_2036696995` | A/A/A | attempt_001 | attempt_001 | `1911f019403e` | `27b12c3ea1ea` | `9beea987981c` |
| 16 | `E3_G3B_DUAL001_seed_2106030015` | A/B/B | attempt_001 | attempt_001 | `a4dcc84bf4f2` | `1109c65da491` | `13a8b3be5e37` |

### `solo_control_set_003`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3B_SOLO003_seed_1672462843` | A/A | attempt_001 | attempt_001 | `ce09cc5bcd90` | `7c6413b06bf6` | `424d3bcf933b` |
| 2 | `E3_G3B_SOLO003_seed_63901144` | A/B | attempt_001 | attempt_001 | `5e114803c93a` | `6aa2f4c3cd0b` | `d0419c9213ea` |
| 3 | `E3_G3B_SOLO003_seed_323832400` | A/A | attempt_001 | attempt_001 | `6df10da84e91` | `fcc95f0463f2` | `fc450307d633` |
| 4 | `E3_G3B_SOLO003_seed_1566825802` | B/B | attempt_001 | attempt_001 | `70944343599a` | `e61e3e7479a3` | `284e62ff2ed9` |
| 5 | `E3_G3B_SOLO003_seed_277459948` | A/A | attempt_001 | attempt_001 | `3c5d86eea20d` | `eff47a645240` | `b14d568c54ed` |
| 6 | `E3_G3B_SOLO003_seed_743291108` | A/A | attempt_001 | attempt_001 | `c84ae3e977a6` | `357c1e210710` | `22d05b7cab4c` |
| 7 | `E3_G3B_SOLO003_seed_2020380812` | B/B | attempt_001 | attempt_001 | `faf72739e771` | `4e4410ecb308` | `9a44fd949870` |
| 8 | `E3_G3B_SOLO003_seed_1292406070` | A/A | attempt_001 | attempt_001 | `36a52ede35ce` | `7c6413b06bf6` | `ae6d9d0be932` |
| 9 | `E3_G3B_SOLO003_seed_187031691` | A/A | attempt_001 | attempt_001 | `cda350182298` | `7c6413b06bf6` | `b45a3693b8a0` |
| 10 | `E3_G3B_SOLO003_seed_1476859861` | A/A | attempt_001, attempt_002 | attempt_002 | `e6f310288c4a` | `7c6413b06bf6` | `492553b29d77` |
| 11 | `E3_G3B_SOLO003_seed_745425377` | B/A | attempt_001 | attempt_001 | `5938dbb7fdfc` | `b7f47fe49d8c` | `16391c14a012` |
| 12 | `E3_G3B_SOLO003_seed_1686133698` | A/A | attempt_001 | attempt_001 | `a5213a5714d6` | `2c5d2851b37b` | `afedfd314d61` |

### `probe_off_set_001`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3B_PROBEOFF001_seed_1672462843` | A/A | attempt_001 | attempt_001 | `f2cc4a00157e` | `2420a3732ab7` | `b626ad9fa8e1` |
| 2 | `E3_G3B_PROBEOFF001_seed_63901144` | A/B | attempt_001 | attempt_001 | `6992d1dcc34b` | `a25648d8c2d8` | `52134f03b981` |
| 3 | `E3_G3B_PROBEOFF001_seed_323832400` | A/A | attempt_001 | attempt_001 | `1830b1590e78` | `293cc17ea46f` | `fb47ebc0a91d` |
| 4 | `E3_G3B_PROBEOFF001_seed_1566825802` | B/B | attempt_001 | attempt_001 | `ecf39a9cbb14` | `675042cc34ce` | `1f364581b520` |

## Scientific boundary

No answer, confidence, P(A), Brier, message, provenance mark, excess, FIS, DSCD, FREE/LINEAGE comparison or any other outcome was read, computed or reported. This audit establishes that data collection for the stage is complete and technically sound. It is not an interpretation.

## Replication start condition

A PASS here means this stage's data collection is complete. Under the frozen plan, the replication stage (Set 002) starts after Set 001 passes this audit and before any primary-outcome audit of Set 001, so that Set 002 runs regardless of what Set 001 shows. Gate closure requires both stages.
