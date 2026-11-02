# EXP-003 Gate 3C Set 001 Corpus Integrity Audit v0.1

## Status

**PASS**

Read-only corpus/provenance audit. Scientific interpretation was **not performed**.

## Provenance

- Plan: `GATE_3C_PLAN_v0.1` (status `FROZEN`, sha256 `91fa8f97d553a443b14624b8e8e04d17e278b13270318ec696c8f7edbb0272d0`)
- Frozen runtime: `c54563bbb3f17e49c70e8e4f2e3a0369910d3c15`; protocol tag `exp-003-protocol-v0.1`
- Plan freeze commit: `afa05a8fd4669567991cc70fa4763b328cb69888`
- Derivation anchor: `d1250663ec206539f2d64c9c8cdcd10c87e5b9af|exp-003-protocol-v0.1|GATE_3C_PLAN_v0.1`
- HEAD at audit time: `b095b8356c2cb7593d890ed6a2aec092a0f5f27e`
- Frozen runtime drift: none
- Expected run class: `gate_3c_real_model`; model `gpt-5.6-sol`; effort `medium`; paired; reliability `0.7`

## Corpus shape

| Set | Topology | Rounds | Probe | Manifest sha256 | Planned | Complete | Calls/world | Events/world | Actual calls | Tokens |
|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|
| `ring_detached_set_001` | ring_detached | 4 | off | `4a366ea5ad5f…` | 12 | 12 | 25 | 30 | 300 | 95903 |
| `solo_detached_set_001` | solo_detached | 12 | off | `53e4302f9b79…` | 12 | 12 | 25 | 28 | 300 | 98264 |
| `dyad_detached_set_001` | dyad_detached | 6 | off | `d6cf805dedc7…` | 12 | 12 | 25 | 29 | 300 | 100671 |
| `bounce_detached_set_001` | bounce_detached | 3 | off | `38bdef276305…` | 12 | 12 | 25 | 31 | 300 | 96879 |
| `diamond_detached_set_001` | diamond_detached | 4 | on | `0a3f182fdcbe…` | 12 | 12 | 33 | 39 | 396 | 132155 |
| `ring_contemporary_set_001` | ring | 4 | off | `a09ed5a3835f…` | 12 | 12 | 25 | 30 | 300 | 102386 |
| `solo_contemporary_set_001` | solo | 12 | off | `621b2612c2c9…` | 12 | 12 | 25 | 28 | 300 | 95096 |
| `dyad_contemporary_set_001` | dyad | 6 | off | `f41006fbf3b6…` | 12 | 12 | 25 | 29 | 300 | 99799 |
| `bounce_contemporary_set_001` | bounce | 3 | off | `e50946e971aa…` | 12 | 12 | 25 | 31 | 300 | 99574 |

Totals: planned 108, complete 108, actual provider calls 2796, tokens 920727, technical failure records 1.

## Technical failures (preserved, excluded from scientific N)

| Set | World | Attempt | Exception | Message | Timestamp |
|---|---|---|---|---|---|
| `ring_detached_set_001` | `E3_G3C_RINGDET001_seed_1146035841` | attempt_001 | `OpenAIAdapterError` | OpenAI Responses request failed | 2026-11-02T01:05:05.564103+00:00 |

## Mechanical verification

- Archived worlds equal the manifest's worlds for every set: PASS
- Exactly one complete attempt per world: PASS
- Raw file SHA-256 hashes match archive records: PASS
- Run class, provider, model, effort, probe, topology, root mode, rounds, call count, fallbacks, frozen runtime, plan freeze commit, manifest hash, seed and cell per attempt: PASS
- Event structure (count, three conditions, max depth, root set, served model on every event, no fallback-served event): PASS
- Frozen runtime drift: none

## Per-world raw hashes

### `ring_detached_set_001`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3C_RINGDET001_seed_1146035841` | B/B | attempt_001, attempt_002 | attempt_002 | `7ec4655cb1dd` | `720b72d5bf13` | `f2623cbde2f0` |
| 2 | `E3_G3C_RINGDET001_seed_1265697921` | B/B | attempt_001 | attempt_001 | `3ea986eb917e` | `4a04609e0bcb` | `cf9c9a7b9cbd` |
| 3 | `E3_G3C_RINGDET001_seed_154869395` | B/B | attempt_001 | attempt_001 | `b9e5651e04ef` | `3d25014416ef` | `2a1d3cb8fba7` |
| 4 | `E3_G3C_RINGDET001_seed_1280872600` | B/B | attempt_001 | attempt_001 | `a74ef9b1f871` | `d346558795e1` | `7e4104e8f54d` |
| 5 | `E3_G3C_RINGDET001_seed_1117385864` | B/A | attempt_001 | attempt_001 | `e54bcd32e55f` | `8630798bc171` | `bd026eb87802` |
| 6 | `E3_G3C_RINGDET001_seed_1779995607` | B/A | attempt_001 | attempt_001 | `47feb914ce6d` | `4d9487d179df` | `c1156b805550` |
| 7 | `E3_G3C_RINGDET001_seed_961840741` | A/B | attempt_001 | attempt_001 | `840797ce3742` | `935b5f31c953` | `e5f7eaae12ad` |
| 8 | `E3_G3C_RINGDET001_seed_1813269025` | B/B | attempt_001 | attempt_001 | `efbe04e22cfe` | `104045b9d9e9` | `dd43e7f3217a` |
| 9 | `E3_G3C_RINGDET001_seed_683505103` | A/A | attempt_001 | attempt_001 | `88d63715aefe` | `a44b96f33ae3` | `2ebdaf070d66` |
| 10 | `E3_G3C_RINGDET001_seed_1296650177` | B/B | attempt_001 | attempt_001 | `7ce5c065f764` | `2e0b580f04b0` | `3278f7a737ed` |
| 11 | `E3_G3C_RINGDET001_seed_950201606` | A/A | attempt_001 | attempt_001 | `abd03ee37254` | `ae014c892ba9` | `ad5d5162af9b` |
| 12 | `E3_G3C_RINGDET001_seed_652310877` | B/B | attempt_001 | attempt_001 | `ed0ec1fd8a34` | `e16c56ab1f15` | `0a75742a4890` |

### `solo_detached_set_001`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3C_SOLODET001_seed_1146035841` | B/B | attempt_001 | attempt_001 | `e7607fa5b2ef` | `689c3a65a39b` | `6c0e4c484f85` |
| 2 | `E3_G3C_SOLODET001_seed_1265697921` | B/B | attempt_001 | attempt_001 | `d3b92fff0a6f` | `87fbb9bb28a3` | `d6e89a9b3930` |
| 3 | `E3_G3C_SOLODET001_seed_154869395` | B/B | attempt_001 | attempt_001 | `52ab389b2fd5` | `f0eb407edbdf` | `980c8b915dd4` |
| 4 | `E3_G3C_SOLODET001_seed_1280872600` | B/B | attempt_001 | attempt_001 | `d5b7a5ebfe25` | `1b20f8b579ae` | `8c74245b2945` |
| 5 | `E3_G3C_SOLODET001_seed_1117385864` | B/A | attempt_001 | attempt_001 | `de97c39812b1` | `68f87d36b8cf` | `0e634819b5a0` |
| 6 | `E3_G3C_SOLODET001_seed_1779995607` | B/A | attempt_001 | attempt_001 | `ede866a82413` | `80c2de1b29cf` | `9baa435eae88` |
| 7 | `E3_G3C_SOLODET001_seed_961840741` | A/B | attempt_001 | attempt_001 | `17d4088a5e95` | `fb5ecc0846ec` | `5b29838af5ed` |
| 8 | `E3_G3C_SOLODET001_seed_1813269025` | B/B | attempt_001 | attempt_001 | `8fdd7623618a` | `fd464d2ed45b` | `0a4925f0fc76` |
| 9 | `E3_G3C_SOLODET001_seed_683505103` | A/A | attempt_001 | attempt_001 | `598a38baadf9` | `b3ed7daf631a` | `4756a2f9369e` |
| 10 | `E3_G3C_SOLODET001_seed_1296650177` | B/B | attempt_001 | attempt_001 | `80622a053590` | `161a2bfadcaa` | `430e74cc333f` |
| 11 | `E3_G3C_SOLODET001_seed_950201606` | A/A | attempt_001 | attempt_001 | `ab4e64ef6db2` | `3a1bc7fdf03b` | `13d9234ce82e` |
| 12 | `E3_G3C_SOLODET001_seed_652310877` | B/B | attempt_001 | attempt_001 | `1e031d707052` | `97a0cd497761` | `59bab6c55dfa` |

### `dyad_detached_set_001`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3C_DYADDET001_seed_1146035841` | B/B | attempt_001 | attempt_001 | `8e4a6fe0302a` | `e6a8d08114d0` | `b0fdc1e1a2f6` |
| 2 | `E3_G3C_DYADDET001_seed_1265697921` | B/B | attempt_001 | attempt_001 | `4c7e83ee1b6c` | `38153ffd22e0` | `e2eb98a60472` |
| 3 | `E3_G3C_DYADDET001_seed_154869395` | B/B | attempt_001 | attempt_001 | `239530e54a7c` | `e99e65306e89` | `9f3390c6e5f1` |
| 4 | `E3_G3C_DYADDET001_seed_1280872600` | B/B | attempt_001 | attempt_001 | `5539c7bb8347` | `36979de15414` | `089bdd25375a` |
| 5 | `E3_G3C_DYADDET001_seed_1117385864` | B/A | attempt_001 | attempt_001 | `dadc2c1822a0` | `8781b61c56f0` | `d4dfbe00e158` |
| 6 | `E3_G3C_DYADDET001_seed_1779995607` | B/A | attempt_001 | attempt_001 | `b425264455cd` | `2bd6afcb3dd4` | `181d3bb4fa64` |
| 7 | `E3_G3C_DYADDET001_seed_961840741` | A/B | attempt_001 | attempt_001 | `446946ee2826` | `e2b1146d79a6` | `1f26c246111d` |
| 8 | `E3_G3C_DYADDET001_seed_1813269025` | B/B | attempt_001 | attempt_001 | `798034470148` | `e321dc437c80` | `ad6dfb101063` |
| 9 | `E3_G3C_DYADDET001_seed_683505103` | A/A | attempt_001 | attempt_001 | `77bd4363dbed` | `3c7cc5192276` | `455af57672a2` |
| 10 | `E3_G3C_DYADDET001_seed_1296650177` | B/B | attempt_001 | attempt_001 | `c3814d2bf7e5` | `fdb42b63a254` | `72d55e48d096` |
| 11 | `E3_G3C_DYADDET001_seed_950201606` | A/A | attempt_001 | attempt_001 | `72faac1e05bf` | `9da118d1ab8c` | `b561303e795c` |
| 12 | `E3_G3C_DYADDET001_seed_652310877` | B/B | attempt_001 | attempt_001 | `191421dc58b2` | `86a469110001` | `720a9508a865` |

### `bounce_detached_set_001`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3C_BOUNCEDET001_seed_1146035841` | B/B | attempt_001 | attempt_001 | `7c72942d0764` | `369ee2ea6010` | `36872c2994cd` |
| 2 | `E3_G3C_BOUNCEDET001_seed_1265697921` | B/B | attempt_001 | attempt_001 | `0282c9cd9cf2` | `cfead1a54276` | `fe6484dbc989` |
| 3 | `E3_G3C_BOUNCEDET001_seed_154869395` | B/B | attempt_001 | attempt_001 | `83243430b1f4` | `7df71709a186` | `7ce111e3b517` |
| 4 | `E3_G3C_BOUNCEDET001_seed_1280872600` | B/B | attempt_001 | attempt_001 | `ba4a8c4d61ec` | `aa86286dbf30` | `2e0149af468b` |
| 5 | `E3_G3C_BOUNCEDET001_seed_1117385864` | B/A | attempt_001 | attempt_001 | `d59ec771f035` | `0c5091f73cc7` | `4b9c7ac5ef47` |
| 6 | `E3_G3C_BOUNCEDET001_seed_1779995607` | B/A | attempt_001 | attempt_001 | `7e514c12272b` | `7ed47e5b2794` | `5684174160a1` |
| 7 | `E3_G3C_BOUNCEDET001_seed_961840741` | A/B | attempt_001 | attempt_001 | `dbd444e43955` | `b26cf59d91ae` | `d1ec2a0c7c1a` |
| 8 | `E3_G3C_BOUNCEDET001_seed_1813269025` | B/B | attempt_001 | attempt_001 | `7c7b2ce53d17` | `f0ce370bfd40` | `f03274f0eea0` |
| 9 | `E3_G3C_BOUNCEDET001_seed_683505103` | A/A | attempt_001 | attempt_001 | `a86aafd07caf` | `895d299a7256` | `65af3b2f8ad8` |
| 10 | `E3_G3C_BOUNCEDET001_seed_1296650177` | B/B | attempt_001 | attempt_001 | `ea221145f74c` | `8948623076b9` | `aab3ad42db5f` |
| 11 | `E3_G3C_BOUNCEDET001_seed_950201606` | A/A | attempt_001 | attempt_001 | `930a272868ef` | `f2cb4384b85a` | `ef4ad1f752c1` |
| 12 | `E3_G3C_BOUNCEDET001_seed_652310877` | B/B | attempt_001 | attempt_001 | `0d5abc276ce6` | `dbee3c105a1a` | `34ce02b644b2` |

### `diamond_detached_set_001`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3C_DIAMONDDET001_seed_1672462843` | A/A | attempt_001 | attempt_001 | `ae9af8e0e0af` | `85c5e91ee39a` | `e7531ebb2078` |
| 2 | `E3_G3C_DIAMONDDET001_seed_63901144` | A/B | attempt_001 | attempt_001 | `f4eac2675eda` | `c1e49bd7d243` | `f8d9e0875f98` |
| 3 | `E3_G3C_DIAMONDDET001_seed_323832400` | A/A | attempt_001 | attempt_001 | `701328554482` | `11ef55a30a13` | `9f9fc19d688e` |
| 4 | `E3_G3C_DIAMONDDET001_seed_1566825802` | B/B | attempt_001 | attempt_001 | `f9686f9f2206` | `f25ad9c8bf0c` | `78fad13d3ba9` |
| 5 | `E3_G3C_DIAMONDDET001_seed_277459948` | A/A | attempt_001 | attempt_001 | `c9cfb8f7365b` | `4b124dc60093` | `a0cb08f8be6e` |
| 6 | `E3_G3C_DIAMONDDET001_seed_743291108` | A/A | attempt_001 | attempt_001 | `8e771bc1e0b7` | `caf7fbf887e8` | `38b7770c0c12` |
| 7 | `E3_G3C_DIAMONDDET001_seed_2020380812` | B/B | attempt_001 | attempt_001 | `30a33d823f56` | `f428a45bb4d3` | `e841ac063d75` |
| 8 | `E3_G3C_DIAMONDDET001_seed_1292406070` | A/A | attempt_001 | attempt_001 | `325d2d456958` | `68e199982dc6` | `c003af0040a6` |
| 9 | `E3_G3C_DIAMONDDET001_seed_187031691` | A/A | attempt_001 | attempt_001 | `1d7a181b2455` | `793b95f24a23` | `4091541fda96` |
| 10 | `E3_G3C_DIAMONDDET001_seed_1476859861` | A/A | attempt_001 | attempt_001 | `ac658b6fa156` | `54f54eb2e06b` | `133a84139b1e` |
| 11 | `E3_G3C_DIAMONDDET001_seed_745425377` | B/A | attempt_001 | attempt_001 | `151deea72c30` | `fdc60199c74e` | `a02d406d55f2` |
| 12 | `E3_G3C_DIAMONDDET001_seed_1686133698` | A/A | attempt_001 | attempt_001 | `483b493b9789` | `d40c2345ae80` | `50c49211acb8` |

### `ring_contemporary_set_001`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3C_RINGCTL001_seed_1146035841` | B/B | attempt_001 | attempt_001 | `9483b053fa52` | `af69454599d4` | `1e93d003bf00` |
| 2 | `E3_G3C_RINGCTL001_seed_1265697921` | B/B | attempt_001 | attempt_001 | `e240c03cad06` | `ec220ff5374c` | `b54e39f40025` |
| 3 | `E3_G3C_RINGCTL001_seed_154869395` | B/B | attempt_001 | attempt_001 | `7e27526d623a` | `a4d73cec46b8` | `90b415804759` |
| 4 | `E3_G3C_RINGCTL001_seed_1280872600` | B/B | attempt_001 | attempt_001 | `7bc74ea9b0ea` | `8a9336c4b0f2` | `9297039de961` |
| 5 | `E3_G3C_RINGCTL001_seed_1117385864` | B/A | attempt_001 | attempt_001 | `6c10ae1408eb` | `5f7750e1117c` | `afbdb2588f96` |
| 6 | `E3_G3C_RINGCTL001_seed_1779995607` | B/A | attempt_001 | attempt_001 | `ae8074edb038` | `ad6c8a266254` | `2c11e7d137aa` |
| 7 | `E3_G3C_RINGCTL001_seed_961840741` | A/B | attempt_001 | attempt_001 | `1f92442ffcb6` | `ebb2384449ba` | `9661fbd7e446` |
| 8 | `E3_G3C_RINGCTL001_seed_1813269025` | B/B | attempt_001 | attempt_001 | `d479f74e6d3c` | `c7fde3c73ec2` | `65c139d0d310` |
| 9 | `E3_G3C_RINGCTL001_seed_683505103` | A/A | attempt_001 | attempt_001 | `45b492decc31` | `b68587586f85` | `3446c9fa8119` |
| 10 | `E3_G3C_RINGCTL001_seed_1296650177` | B/B | attempt_001 | attempt_001 | `9d0dfbcddcc7` | `5a1617e8abfa` | `746ec0a3d4c1` |
| 11 | `E3_G3C_RINGCTL001_seed_950201606` | A/A | attempt_001 | attempt_001 | `fa31d57a11e0` | `a52ca9e6598a` | `3dd3744c2e5d` |
| 12 | `E3_G3C_RINGCTL001_seed_652310877` | B/B | attempt_001 | attempt_001 | `99062be2eb21` | `9d682f945a6b` | `1fdf28f40b60` |

### `solo_contemporary_set_001`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3C_SOLOCTL001_seed_1146035841` | B/B | attempt_001 | attempt_001 | `b6d858f44bc7` | `3a576e7ed7a6` | `ba7b169e06e0` |
| 2 | `E3_G3C_SOLOCTL001_seed_1265697921` | B/B | attempt_001 | attempt_001 | `df37cadef4f9` | `3a576e7ed7a6` | `d7aa21afdb93` |
| 3 | `E3_G3C_SOLOCTL001_seed_154869395` | B/B | attempt_001 | attempt_001 | `7d689403c13a` | `5babb2b6ba99` | `cffa1f202666` |
| 4 | `E3_G3C_SOLOCTL001_seed_1280872600` | B/B | attempt_001 | attempt_001 | `51b1432c5f5e` | `3a576e7ed7a6` | `1d7b47c9ef5e` |
| 5 | `E3_G3C_SOLOCTL001_seed_1117385864` | B/A | attempt_001 | attempt_001 | `5847213d1a68` | `312d450ce155` | `5fb0ee89aae0` |
| 6 | `E3_G3C_SOLOCTL001_seed_1779995607` | B/A | attempt_001 | attempt_001 | `601f5dc2bfdc` | `5c4396ede22c` | `6ce0aadb35a9` |
| 7 | `E3_G3C_SOLOCTL001_seed_961840741` | A/B | attempt_001 | attempt_001 | `8b0e21f67d90` | `055fca3d29ec` | `fe8bec3b1541` |
| 8 | `E3_G3C_SOLOCTL001_seed_1813269025` | B/B | attempt_001 | attempt_001 | `8eaecb577c29` | `c5a7f3b51425` | `32e2d0f90e63` |
| 9 | `E3_G3C_SOLOCTL001_seed_683505103` | A/A | attempt_001 | attempt_001 | `aaa9b8485a75` | `4ac06ae1bf2e` | `ea04d159b550` |
| 10 | `E3_G3C_SOLOCTL001_seed_1296650177` | B/B | attempt_001 | attempt_001 | `d88111adb364` | `a705066b3a92` | `fa6306f1e00b` |
| 11 | `E3_G3C_SOLOCTL001_seed_950201606` | A/A | attempt_001 | attempt_001 | `9e95e1e77c8c` | `fafd5efefa87` | `f8a55ec3c458` |
| 12 | `E3_G3C_SOLOCTL001_seed_652310877` | B/B | attempt_001 | attempt_001 | `d168aa6fba23` | `3a576e7ed7a6` | `2ae7ee8cbb88` |

### `dyad_contemporary_set_001`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3C_DYADCTL001_seed_1146035841` | B/B | attempt_001 | attempt_001 | `fa9c0399612a` | `ddc8e3f91fbd` | `0275c1b8d275` |
| 2 | `E3_G3C_DYADCTL001_seed_1265697921` | B/B | attempt_001 | attempt_001 | `15abf42df936` | `fd6c3d7c5691` | `6b4690d18691` |
| 3 | `E3_G3C_DYADCTL001_seed_154869395` | B/B | attempt_001 | attempt_001 | `d9bf0aecd8d8` | `b5042785213d` | `86fc0d2f5f10` |
| 4 | `E3_G3C_DYADCTL001_seed_1280872600` | B/B | attempt_001 | attempt_001 | `dafe2155ec86` | `93b46c207240` | `5ba5c2766e63` |
| 5 | `E3_G3C_DYADCTL001_seed_1117385864` | B/A | attempt_001 | attempt_001 | `3666bfc8aee6` | `c9d7b0f57825` | `87d53088bc9d` |
| 6 | `E3_G3C_DYADCTL001_seed_1779995607` | B/A | attempt_001 | attempt_001 | `392bb65b1b7e` | `6cc11c82051a` | `c9bec25c0e95` |
| 7 | `E3_G3C_DYADCTL001_seed_961840741` | A/B | attempt_001 | attempt_001 | `fd3d299696c2` | `d3a6725da5a0` | `ed169f3f5460` |
| 8 | `E3_G3C_DYADCTL001_seed_1813269025` | B/B | attempt_001 | attempt_001 | `c7844deda440` | `4371a8dea591` | `69ba208b7775` |
| 9 | `E3_G3C_DYADCTL001_seed_683505103` | A/A | attempt_001 | attempt_001 | `fc199b03ace8` | `32b8a02e402c` | `0d9bd24ebaf2` |
| 10 | `E3_G3C_DYADCTL001_seed_1296650177` | B/B | attempt_001 | attempt_001 | `42ae475256af` | `d7d58c993a12` | `eb9feab228aa` |
| 11 | `E3_G3C_DYADCTL001_seed_950201606` | A/A | attempt_001 | attempt_001 | `347633d3cd79` | `f2cab2efaabd` | `a718dd1c8ebc` |
| 12 | `E3_G3C_DYADCTL001_seed_652310877` | B/B | attempt_001 | attempt_001 | `bb358bb59408` | `9806f69e77c5` | `35848a25c2cc` |

### `bounce_contemporary_set_001`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3C_BOUNCECTL001_seed_1146035841` | B/B | attempt_001 | attempt_001 | `3253b2049ff0` | `3057e48adfe5` | `3cd3d45f6a0c` |
| 2 | `E3_G3C_BOUNCECTL001_seed_1265697921` | B/B | attempt_001 | attempt_001 | `f61e6e33cb07` | `f07e93f74064` | `6ce7f3754f2a` |
| 3 | `E3_G3C_BOUNCECTL001_seed_154869395` | B/B | attempt_001 | attempt_001 | `e06abe4e84b5` | `316638754a9c` | `4eb0c3203bd3` |
| 4 | `E3_G3C_BOUNCECTL001_seed_1280872600` | B/B | attempt_001 | attempt_001 | `a8a7f58cdfbf` | `9cbaa3712940` | `658a08a36d08` |
| 5 | `E3_G3C_BOUNCECTL001_seed_1117385864` | B/A | attempt_001 | attempt_001 | `3804d5691068` | `9c7afa9596ec` | `a7687d4719d2` |
| 6 | `E3_G3C_BOUNCECTL001_seed_1779995607` | B/A | attempt_001 | attempt_001 | `d2e4ef963efe` | `ec50eef821f6` | `6a4f0b613997` |
| 7 | `E3_G3C_BOUNCECTL001_seed_961840741` | A/B | attempt_001 | attempt_001 | `592d1c0a0ce0` | `8142b63c5e7b` | `69ced86743a1` |
| 8 | `E3_G3C_BOUNCECTL001_seed_1813269025` | B/B | attempt_001 | attempt_001 | `afb8c1e4a6c3` | `38b495c0a91e` | `2a8b437ad818` |
| 9 | `E3_G3C_BOUNCECTL001_seed_683505103` | A/A | attempt_001 | attempt_001 | `a02c7fd9d16d` | `d9c450221336` | `8dd30cf1d6b5` |
| 10 | `E3_G3C_BOUNCECTL001_seed_1296650177` | B/B | attempt_001 | attempt_001 | `efec81cc1dea` | `f6e11478ee14` | `0ed18581e522` |
| 11 | `E3_G3C_BOUNCECTL001_seed_950201606` | A/A | attempt_001 | attempt_001 | `b08fb4900e40` | `bf6170a8c2a4` | `ece7c6b91b44` |
| 12 | `E3_G3C_BOUNCECTL001_seed_652310877` | B/B | attempt_001 | attempt_001 | `df1aa55ae77e` | `e495496987cd` | `94972c9b0248` |

## Scientific boundary

No answer, confidence, P(A), Brier, message, provenance mark, excess, FIS, DSCD, FREE/LINEAGE comparison or any other outcome was read, computed or reported. This audit establishes that data collection for the stage is complete and technically sound. It is not an interpretation.

## Replication start condition

A PASS here means this stage's data collection is complete. Under the frozen plan, the replication stage (Set 002) starts after Set 001 passes this audit and before any primary-outcome audit of Set 001, so that Set 002 runs regardless of what Set 001 shows. Gate closure requires both stages.
