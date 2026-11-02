# EXP-003 Gate 3C Set 002 Corpus Integrity Audit v0.1

## Status

**PASS**

Read-only corpus/provenance audit. Scientific interpretation was **not performed**.

## Provenance

- Plan: `GATE_3C_PLAN_v0.1` (status `FROZEN`, sha256 `91fa8f97d553a443b14624b8e8e04d17e278b13270318ec696c8f7edbb0272d0`)
- Frozen runtime: `c54563bbb3f17e49c70e8e4f2e3a0369910d3c15`; protocol tag `exp-003-protocol-v0.1`
- Plan freeze commit: `afa05a8fd4669567991cc70fa4763b328cb69888`
- Derivation anchor: `d1250663ec206539f2d64c9c8cdcd10c87e5b9af|exp-003-protocol-v0.1|GATE_3C_PLAN_v0.1`
- HEAD at audit time: `c0fcf35afccdcb7e0b7d88c1f91a624e42f7657d`
- Frozen runtime drift: none
- Expected run class: `gate_3c_real_model`; model `gpt-5.6-sol`; effort `medium`; paired; reliability `0.7`

## Corpus shape

| Set | Topology | Rounds | Probe | Manifest sha256 | Planned | Complete | Calls/world | Events/world | Actual calls | Tokens |
|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|
| `ring_detached_set_002` | ring_detached | 4 | off | `17a2d8eb249d…` | 12 | 12 | 25 | 30 | 300 | 96262 |
| `solo_detached_set_002` | solo_detached | 12 | off | `7847fe2d51aa…` | 12 | 12 | 25 | 28 | 300 | 99011 |
| `dyad_detached_set_002` | dyad_detached | 6 | off | `7dd35187fe7d…` | 12 | 12 | 25 | 29 | 300 | 98521 |
| `bounce_detached_set_002` | bounce_detached | 3 | off | `4aa1a0a395e9…` | 12 | 12 | 25 | 31 | 300 | 97182 |
| `diamond_detached_set_002` | diamond_detached | 4 | on | `4747fa32b228…` | 12 | 12 | 33 | 39 | 396 | 131996 |

Totals: planned 60, complete 60, actual provider calls 1596, tokens 522972, technical failure records 0.

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

### `ring_detached_set_002`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3C_RINGDET002_seed_818285910` | A/A | attempt_001 | attempt_001 | `ab5dccadd3a9` | `716ec74a57ef` | `2ea874d30031` |
| 2 | `E3_G3C_RINGDET002_seed_588710334` | B/B | attempt_001 | attempt_001 | `a5a9690784de` | `0574f96ce8aa` | `ff9effe3cbff` |
| 3 | `E3_G3C_RINGDET002_seed_1246964244` | A/A | attempt_001 | attempt_001 | `2e3eed98969c` | `bf5b273c9100` | `95e47c0d6fa1` |
| 4 | `E3_G3C_RINGDET002_seed_1138823197` | A/B | attempt_001 | attempt_001 | `6c714d5631de` | `028066632c3b` | `00ac8af37ffa` |
| 5 | `E3_G3C_RINGDET002_seed_882867208` | A/A | attempt_001 | attempt_001 | `e57d63d90580` | `ff0db8cf38b6` | `e3cd44207f2d` |
| 6 | `E3_G3C_RINGDET002_seed_1468093150` | B/A | attempt_001 | attempt_001 | `2ba4390c4a5b` | `f6b2e35b5ef3` | `2435586aa460` |
| 7 | `E3_G3C_RINGDET002_seed_1032002992` | A/A | attempt_001 | attempt_001 | `30c9f5485c74` | `0a9ae25d7041` | `b6d213c814c5` |
| 8 | `E3_G3C_RINGDET002_seed_245389550` | A/A | attempt_001 | attempt_001 | `8564ed9a9073` | `bd8211b152de` | `c3f4480cea0a` |
| 9 | `E3_G3C_RINGDET002_seed_652866105` | A/A | attempt_001 | attempt_001 | `bc058f708b7d` | `1b1e4716a755` | `4b7adb5bef1c` |
| 10 | `E3_G3C_RINGDET002_seed_28092603` | A/A | attempt_001 | attempt_001 | `63026156ec5d` | `120a6d69afbb` | `85e0cd132551` |
| 11 | `E3_G3C_RINGDET002_seed_1582931821` | A/A | attempt_001 | attempt_001 | `ac51c2fad514` | `19d1d0b3dd1a` | `7f630bc680db` |
| 12 | `E3_G3C_RINGDET002_seed_1792403557` | A/B | attempt_001 | attempt_001 | `7381d42001ab` | `ef02a0a21696` | `db2a8ad3758e` |

### `solo_detached_set_002`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3C_SOLODET002_seed_818285910` | A/A | attempt_001 | attempt_001 | `51490bd7a18f` | `bbcacfabf15f` | `32c064ba6ab3` |
| 2 | `E3_G3C_SOLODET002_seed_588710334` | B/B | attempt_001 | attempt_001 | `8d119f672b1d` | `e2b0762466b4` | `e718e4c3ec2e` |
| 3 | `E3_G3C_SOLODET002_seed_1246964244` | A/A | attempt_001 | attempt_001 | `79e06a7188a8` | `736591cabd45` | `59224a279e48` |
| 4 | `E3_G3C_SOLODET002_seed_1138823197` | A/B | attempt_001 | attempt_001 | `25af5aef207e` | `d1f641c4c757` | `7385792556b9` |
| 5 | `E3_G3C_SOLODET002_seed_882867208` | A/A | attempt_001 | attempt_001 | `3dec33d01aeb` | `b5311cc38e3f` | `a2a878d1e6c3` |
| 6 | `E3_G3C_SOLODET002_seed_1468093150` | B/A | attempt_001 | attempt_001 | `faa49279803c` | `3fbcc0590ad1` | `45297979db35` |
| 7 | `E3_G3C_SOLODET002_seed_1032002992` | A/A | attempt_001 | attempt_001 | `acfb39294893` | `a42101db19fb` | `1b898ef2451f` |
| 8 | `E3_G3C_SOLODET002_seed_245389550` | A/A | attempt_001 | attempt_001 | `81d1483824f5` | `cf6e70c39d6a` | `09610c24bb7e` |
| 9 | `E3_G3C_SOLODET002_seed_652866105` | A/A | attempt_001 | attempt_001 | `b87aede9148f` | `fccb243b31da` | `e91e7c649c6c` |
| 10 | `E3_G3C_SOLODET002_seed_28092603` | A/A | attempt_001 | attempt_001 | `5926370c406c` | `64ce76bc6c35` | `ef544a552713` |
| 11 | `E3_G3C_SOLODET002_seed_1582931821` | A/A | attempt_001 | attempt_001 | `52fcfbf8a7a3` | `fa161a0f7526` | `a50fa263de5b` |
| 12 | `E3_G3C_SOLODET002_seed_1792403557` | A/B | attempt_001 | attempt_001 | `c7e450bc592d` | `8ceb2efaea06` | `d482e8444c30` |

### `dyad_detached_set_002`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3C_DYADDET002_seed_818285910` | A/A | attempt_001 | attempt_001 | `a50b06cee95b` | `2572be956117` | `6fb4643d5984` |
| 2 | `E3_G3C_DYADDET002_seed_588710334` | B/B | attempt_001 | attempt_001 | `f2196a6599d1` | `5598912d8003` | `5a7941b199a2` |
| 3 | `E3_G3C_DYADDET002_seed_1246964244` | A/A | attempt_001 | attempt_001 | `78984726b81c` | `fba75fa848cc` | `aa10c0d1faea` |
| 4 | `E3_G3C_DYADDET002_seed_1138823197` | A/B | attempt_001 | attempt_001 | `5fd5b14b3b17` | `8ad60f0af14a` | `7c5e6f6cb410` |
| 5 | `E3_G3C_DYADDET002_seed_882867208` | A/A | attempt_001 | attempt_001 | `4617d19f6ef9` | `7cf808173ae4` | `27c2a3e758b7` |
| 6 | `E3_G3C_DYADDET002_seed_1468093150` | B/A | attempt_001 | attempt_001 | `da94da35bbeb` | `76f161f850ee` | `537fc29c7ae2` |
| 7 | `E3_G3C_DYADDET002_seed_1032002992` | A/A | attempt_001 | attempt_001 | `0331ece345d5` | `57172acbba7d` | `9b7f976df221` |
| 8 | `E3_G3C_DYADDET002_seed_245389550` | A/A | attempt_001 | attempt_001 | `58c184b471cb` | `9028302bf8f1` | `83a1bd16ff07` |
| 9 | `E3_G3C_DYADDET002_seed_652866105` | A/A | attempt_001 | attempt_001 | `22375139ebf1` | `ef1ad066cd89` | `9e3c6494b1a3` |
| 10 | `E3_G3C_DYADDET002_seed_28092603` | A/A | attempt_001 | attempt_001 | `57a40bd9a5c7` | `3f8e826fa306` | `4717dc34e681` |
| 11 | `E3_G3C_DYADDET002_seed_1582931821` | A/A | attempt_001 | attempt_001 | `185587f8051d` | `efd5256e374c` | `5b489688fc2c` |
| 12 | `E3_G3C_DYADDET002_seed_1792403557` | A/B | attempt_001 | attempt_001 | `1fe880080ebf` | `7cc0c1a02a22` | `bcc4847cf337` |

### `bounce_detached_set_002`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3C_BOUNCEDET002_seed_818285910` | A/A | attempt_001 | attempt_001 | `e4290068fc3c` | `feb6d5a3ac9b` | `1b1f31442ecb` |
| 2 | `E3_G3C_BOUNCEDET002_seed_588710334` | B/B | attempt_001 | attempt_001 | `6b3e059eeb54` | `32bf276fe911` | `74f82f42fc30` |
| 3 | `E3_G3C_BOUNCEDET002_seed_1246964244` | A/A | attempt_001 | attempt_001 | `6b152e15b9b8` | `6f0f9fd510ac` | `48421241dfdd` |
| 4 | `E3_G3C_BOUNCEDET002_seed_1138823197` | A/B | attempt_001 | attempt_001 | `3bea1b6fabee` | `cba1357d328e` | `f58d62d30b2e` |
| 5 | `E3_G3C_BOUNCEDET002_seed_882867208` | A/A | attempt_001 | attempt_001 | `8f8c835451b2` | `f6f97bb2c795` | `cb29fa9244fa` |
| 6 | `E3_G3C_BOUNCEDET002_seed_1468093150` | B/A | attempt_001 | attempt_001 | `e0ddbe2af7d2` | `3c080751c506` | `58ce3968ce19` |
| 7 | `E3_G3C_BOUNCEDET002_seed_1032002992` | A/A | attempt_001 | attempt_001 | `02ad61729d3a` | `9d8fd1fcfca6` | `3631797373d8` |
| 8 | `E3_G3C_BOUNCEDET002_seed_245389550` | A/A | attempt_001 | attempt_001 | `87470d7e3d6f` | `b17a50da2b9a` | `a326c764a03e` |
| 9 | `E3_G3C_BOUNCEDET002_seed_652866105` | A/A | attempt_001 | attempt_001 | `1be46b403ec7` | `e18fb65b4e05` | `71db88ef6214` |
| 10 | `E3_G3C_BOUNCEDET002_seed_28092603` | A/A | attempt_001 | attempt_001 | `39ce401fb174` | `f9e5fc5cf883` | `7d313d025986` |
| 11 | `E3_G3C_BOUNCEDET002_seed_1582931821` | A/A | attempt_001 | attempt_001 | `4b9f1c2f06e2` | `36737ffc7161` | `72d4e0b233a6` |
| 12 | `E3_G3C_BOUNCEDET002_seed_1792403557` | A/B | attempt_001 | attempt_001 | `689ac651177c` | `437b49657296` | `1950a495a798` |

### `diamond_detached_set_002`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3C_DIAMONDDET002_seed_316127362` | B/A | attempt_001 | attempt_001 | `2772df6ca8de` | `acb882a57b8e` | `981a9516d273` |
| 2 | `E3_G3C_DIAMONDDET002_seed_710597220` | B/A | attempt_001 | attempt_001 | `5806ca4f1071` | `8acb63c1156e` | `4d21519af830` |
| 3 | `E3_G3C_DIAMONDDET002_seed_962632369` | A/A | attempt_001 | attempt_001 | `094d59e9123c` | `f0867a7fda1a` | `4d223b6d076d` |
| 4 | `E3_G3C_DIAMONDDET002_seed_241955308` | B/B | attempt_001 | attempt_001 | `4e6cc1d26be0` | `2968e9c9d477` | `4dd15a3ca0e9` |
| 5 | `E3_G3C_DIAMONDDET002_seed_723648650` | A/B | attempt_001 | attempt_001 | `8f04a04be15c` | `7d26aa604956` | `b6224abe51d8` |
| 6 | `E3_G3C_DIAMONDDET002_seed_1054956113` | B/A | attempt_001 | attempt_001 | `6311a1445f2c` | `b35e91e81589` | `26f0a3b08494` |
| 7 | `E3_G3C_DIAMONDDET002_seed_1831325112` | B/B | attempt_001 | attempt_001 | `74623123ca5d` | `a4344ac10696` | `62271986d708` |
| 8 | `E3_G3C_DIAMONDDET002_seed_374607106` | B/B | attempt_001 | attempt_001 | `2c6c648a4c98` | `6dcd9e5426aa` | `ad662d556b8c` |
| 9 | `E3_G3C_DIAMONDDET002_seed_443947794` | B/B | attempt_001 | attempt_001 | `c66ba28c8b22` | `4cc704190578` | `1d35c99905d0` |
| 10 | `E3_G3C_DIAMONDDET002_seed_533125286` | A/B | attempt_001 | attempt_001 | `a85a91533067` | `960cdfaa77b5` | `ff4d7de022a6` |
| 11 | `E3_G3C_DIAMONDDET002_seed_633201644` | B/B | attempt_001 | attempt_001 | `20c22b69c83e` | `c540ce67818a` | `fb608af9c1d7` |
| 12 | `E3_G3C_DIAMONDDET002_seed_1092129420` | B/A | attempt_001 | attempt_001 | `33dfb50461bc` | `1fc97ccacca9` | `e08e84ece804` |

## Scientific boundary

No answer, confidence, P(A), Brier, message, provenance mark, excess, FIS, DSCD, FREE/LINEAGE comparison or any other outcome was read, computed or reported. This audit establishes that data collection for the stage is complete and technically sound. It is not an interpretation.

## Replication start condition

A PASS here means this stage's data collection is complete. Under the frozen plan, the replication stage (Set 002) starts after Set 001 passes this audit and before any primary-outcome audit of Set 001, so that Set 002 runs regardless of what Set 001 shows. Gate closure requires both stages.
