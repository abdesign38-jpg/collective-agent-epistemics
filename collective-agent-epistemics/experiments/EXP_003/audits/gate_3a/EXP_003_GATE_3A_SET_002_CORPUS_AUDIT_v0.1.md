# EXP-003 Gate 3A Set 002 Corpus Integrity Audit v0.1

## Status

**PASS**

Read-only corpus/provenance audit. Scientific interpretation was **not performed**.

## Provenance

- Plan: `GATE_3A_PLAN_v0.1` (status `FROZEN`, sha256 `4b1fd78b06a6f7f489a37e970ab5bec8f899ada90779fabcf18e421e5434600d`)
- Frozen runtime: `c54563bbb3f17e49c70e8e4f2e3a0369910d3c15`; protocol tag `exp-003-protocol-v0.1`
- Plan freeze commit: `fe5e025468f6b912677fc7074a8f4afb44f2d756`
- Derivation anchor: `80d6db044118965c5e763c9a876e04ef45239ef3|exp-003-protocol-v0.1|GATE_3A_PLAN_v0.1`
- HEAD at audit time: `1288b7d35cf163448784cd77484a5b3dd7ef2d53`
- Frozen runtime drift: none
- Expected run class: `gate_3a_real_model`; model `gpt-5.6-sol`; effort `medium`; paired; reliability `0.7`

## Corpus shape

| Set | Topology | Rounds | Probe | Manifest sha256 | Planned | Complete | Calls/world | Events/world | Actual calls | Tokens |
|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|
| `ring_control_set_002` | ring | 4 | off | `a2ea39ce9a79…` | 12 | 12 | 25 | 30 | 300 | 101648 |
| `solo_control_set_002` | solo | 12 | off | `1c007e9badee…` | 12 | 12 | 25 | 28 | 300 | 97167 |
| `dyad_set_002` | dyad | 6 | off | `120ff036ecb6…` | 12 | 12 | 25 | 29 | 300 | 99984 |
| `bounce_set_002` | bounce | 3 | off | `1d7ab00d2c66…` | 12 | 12 | 25 | 31 | 300 | 99616 |

Totals: planned 48, complete 48, actual provider calls 1200, tokens 398415, technical failure records 0.

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

### `ring_control_set_002`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3A_RING002_seed_818285910` | A/A | attempt_001 | attempt_001 | `1aa4f9f44610` | `2975776544dd` | `7af7cf54bbd0` |
| 2 | `E3_G3A_RING002_seed_588710334` | B/B | attempt_001 | attempt_001 | `806874f33cbc` | `39a7ca612ddd` | `5d9c337ca56e` |
| 3 | `E3_G3A_RING002_seed_1246964244` | A/A | attempt_001 | attempt_001 | `87f18604a591` | `efd235ae4381` | `70597ec7640e` |
| 4 | `E3_G3A_RING002_seed_1138823197` | A/B | attempt_001 | attempt_001 | `138227dc23de` | `798f2df675e0` | `cc99c22813eb` |
| 5 | `E3_G3A_RING002_seed_882867208` | A/A | attempt_001 | attempt_001 | `616e213dee29` | `955164e5d4b6` | `63347168d5cc` |
| 6 | `E3_G3A_RING002_seed_1468093150` | B/A | attempt_001 | attempt_001 | `6d646eca13ff` | `fd478ccd070a` | `9cc7429271ba` |
| 7 | `E3_G3A_RING002_seed_1032002992` | A/A | attempt_001 | attempt_001 | `e288d5a0c530` | `9c3afaafc0e9` | `eb5a7490da78` |
| 8 | `E3_G3A_RING002_seed_245389550` | A/A | attempt_001 | attempt_001 | `0ead3002c807` | `7ae2d654fffb` | `43a3c264914e` |
| 9 | `E3_G3A_RING002_seed_652866105` | A/A | attempt_001 | attempt_001 | `c5d4932264e9` | `82b7dbcaa85d` | `fe551c8143a5` |
| 10 | `E3_G3A_RING002_seed_28092603` | A/A | attempt_001 | attempt_001 | `e6c23a4df238` | `39ecb54731a1` | `1fb89a43aa87` |
| 11 | `E3_G3A_RING002_seed_1582931821` | A/A | attempt_001 | attempt_001 | `59d505365454` | `f35f259841ef` | `87dc5639f8b2` |
| 12 | `E3_G3A_RING002_seed_1792403557` | A/B | attempt_001 | attempt_001 | `0d531d7d13de` | `26c1b369ba6e` | `5da937f1cd09` |

### `solo_control_set_002`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3A_SOLO002_seed_818285910` | A/A | attempt_001 | attempt_001 | `cb8fac8d0bfe` | `2d4d00a13baf` | `e12a40a9019d` |
| 2 | `E3_G3A_SOLO002_seed_588710334` | B/B | attempt_001 | attempt_001 | `c093e1b358d3` | `58a52600bfae` | `c6d7a1ab6836` |
| 3 | `E3_G3A_SOLO002_seed_1246964244` | A/A | attempt_001 | attempt_001 | `984af27d716f` | `7c6413b06bf6` | `e45f5447321d` |
| 4 | `E3_G3A_SOLO002_seed_1138823197` | A/B | attempt_001 | attempt_001 | `4d8fb4614c78` | `ec1591059efc` | `a1164ad20cba` |
| 5 | `E3_G3A_SOLO002_seed_882867208` | A/A | attempt_001 | attempt_001 | `ee61c6dd647d` | `d69e34cb5ea3` | `b5665beeccd7` |
| 6 | `E3_G3A_SOLO002_seed_1468093150` | B/A | attempt_001 | attempt_001 | `be1df690ff0c` | `7473b40de8df` | `e9b3d9400bec` |
| 7 | `E3_G3A_SOLO002_seed_1032002992` | A/A | attempt_001 | attempt_001 | `d12cf14108ac` | `b90ae11b261e` | `f32d73fbe693` |
| 8 | `E3_G3A_SOLO002_seed_245389550` | A/A | attempt_001 | attempt_001 | `1b927bf028ce` | `7c6413b06bf6` | `3a545b90a9ed` |
| 9 | `E3_G3A_SOLO002_seed_652866105` | A/A | attempt_001 | attempt_001 | `e24a850d0738` | `2ec0a8a91301` | `7300ae24b8eb` |
| 10 | `E3_G3A_SOLO002_seed_28092603` | A/A | attempt_001 | attempt_001 | `920f5784d50e` | `7c6413b06bf6` | `a16ca26f100f` |
| 11 | `E3_G3A_SOLO002_seed_1582931821` | A/A | attempt_001 | attempt_001 | `bb51d3d61c16` | `08b414f795db` | `8021f21ae061` |
| 12 | `E3_G3A_SOLO002_seed_1792403557` | A/B | attempt_001 | attempt_001 | `22a3259215ca` | `055fca3d29ec` | `b77eae14e891` |

### `dyad_set_002`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3A_DYAD002_seed_818285910` | A/A | attempt_001 | attempt_001 | `872f435e928f` | `4c4d33b372a3` | `5d04e302680f` |
| 2 | `E3_G3A_DYAD002_seed_588710334` | B/B | attempt_001 | attempt_001 | `6847e5a05f26` | `2f7453cf81dc` | `88b5b9251019` |
| 3 | `E3_G3A_DYAD002_seed_1246964244` | A/A | attempt_001 | attempt_001 | `ef3acadf2bcd` | `e27f7dcad1ef` | `fb4063dd7335` |
| 4 | `E3_G3A_DYAD002_seed_1138823197` | A/B | attempt_001 | attempt_001 | `7e8c9e500d7a` | `fcd5da8e2d29` | `a7ecdcb7b5b8` |
| 5 | `E3_G3A_DYAD002_seed_882867208` | A/A | attempt_001 | attempt_001 | `9d93839af038` | `bd28cc6806b6` | `5437d63f1fba` |
| 6 | `E3_G3A_DYAD002_seed_1468093150` | B/A | attempt_001 | attempt_001 | `920fb1e52944` | `303ce439790f` | `cbff05e4240e` |
| 7 | `E3_G3A_DYAD002_seed_1032002992` | A/A | attempt_001 | attempt_001 | `f8688e804dd8` | `a6f0bddb1740` | `73f5d219e510` |
| 8 | `E3_G3A_DYAD002_seed_245389550` | A/A | attempt_001 | attempt_001 | `265783ba59a4` | `c1a4491b496c` | `1676ad914174` |
| 9 | `E3_G3A_DYAD002_seed_652866105` | A/A | attempt_001 | attempt_001 | `887ff443213a` | `d3813752bbf7` | `19f911c05fac` |
| 10 | `E3_G3A_DYAD002_seed_28092603` | A/A | attempt_001 | attempt_001 | `7da6d466c0e9` | `f110f92aa10f` | `99686ef2ff87` |
| 11 | `E3_G3A_DYAD002_seed_1582931821` | A/A | attempt_001 | attempt_001 | `4534b1a9088e` | `da345333f1db` | `b6a593e18639` |
| 12 | `E3_G3A_DYAD002_seed_1792403557` | A/B | attempt_001 | attempt_001 | `929bfc50ebcd` | `eea955cf1fd1` | `57b81248dc8c` |

### `bounce_set_002`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3A_BOUNCE002_seed_818285910` | A/A | attempt_001 | attempt_001 | `9adaf040ada8` | `9e56388cfdb5` | `87425d914072` |
| 2 | `E3_G3A_BOUNCE002_seed_588710334` | B/B | attempt_001 | attempt_001 | `34a39cb49cce` | `1472ec661a33` | `3a3b5fb22856` |
| 3 | `E3_G3A_BOUNCE002_seed_1246964244` | A/A | attempt_001 | attempt_001 | `5333b024ae4c` | `95fcdf1bc020` | `6b5a93440708` |
| 4 | `E3_G3A_BOUNCE002_seed_1138823197` | A/B | attempt_001 | attempt_001 | `05fa7e85dcab` | `e8f452a7e5ae` | `639d9ec5e42f` |
| 5 | `E3_G3A_BOUNCE002_seed_882867208` | A/A | attempt_001 | attempt_001 | `c1bc5607e617` | `49728a5f5c74` | `2900896af93a` |
| 6 | `E3_G3A_BOUNCE002_seed_1468093150` | B/A | attempt_001 | attempt_001 | `a9cd5bc6a8f4` | `903d04ab0c70` | `4503c1bb9529` |
| 7 | `E3_G3A_BOUNCE002_seed_1032002992` | A/A | attempt_001 | attempt_001 | `b966ff98366d` | `9bee08e6b07a` | `c45ed31cd8f2` |
| 8 | `E3_G3A_BOUNCE002_seed_245389550` | A/A | attempt_001 | attempt_001 | `fa37c8f44c77` | `6e7cbcd5a855` | `0b0467448b96` |
| 9 | `E3_G3A_BOUNCE002_seed_652866105` | A/A | attempt_001 | attempt_001 | `58f345bc6260` | `9c40bb280556` | `66acf4defcf5` |
| 10 | `E3_G3A_BOUNCE002_seed_28092603` | A/A | attempt_001 | attempt_001 | `9f91a9446471` | `70eb44469588` | `5cfe7654a71f` |
| 11 | `E3_G3A_BOUNCE002_seed_1582931821` | A/A | attempt_001 | attempt_001 | `17d91bf47c36` | `7a3f4328a210` | `029f0d7f60b7` |
| 12 | `E3_G3A_BOUNCE002_seed_1792403557` | A/B | attempt_001 | attempt_001 | `c7be11964ba0` | `08b76d4b42e9` | `e2dd1f6a3b86` |

## Scientific boundary

No answer, confidence, P(A), Brier, message, provenance mark, excess, FIS, DSCD, FREE/LINEAGE comparison or any other outcome was read, computed or reported. This audit establishes that data collection for the stage is complete and technically sound. It is not an interpretation.

## Replication start condition

A PASS here means this stage's data collection is complete. Under the frozen plan, the replication stage (Set 002) starts after Set 001 passes this audit and before any primary-outcome audit of Set 001, so that Set 002 runs regardless of what Set 001 shows. Gate closure requires both stages.
