# EXP-003 Gate 3A Set 001 Corpus Integrity Audit v0.1

## Status

**PASS**

Read-only corpus/provenance audit. Scientific interpretation was **not performed**.

## Provenance

- Plan: `GATE_3A_PLAN_v0.1` (status `FROZEN`, sha256 `4b1fd78b06a6f7f489a37e970ab5bec8f899ada90779fabcf18e421e5434600d`)
- Frozen runtime: `c54563bbb3f17e49c70e8e4f2e3a0369910d3c15`; protocol tag `exp-003-protocol-v0.1`
- Plan freeze commit: `fe5e025468f6b912677fc7074a8f4afb44f2d756`
- Derivation anchor: `80d6db044118965c5e763c9a876e04ef45239ef3|exp-003-protocol-v0.1|GATE_3A_PLAN_v0.1`
- HEAD at audit time: `7f12ba4ea9f8a4fa27463f91df8579f158ef004f`
- Frozen runtime drift: none
- Expected run class: `gate_3a_real_model`; model `gpt-5.6-sol`; effort `medium`; paired; reliability `0.7`

## Corpus shape

| Set | Topology | Rounds | Probe | Manifest sha256 | Planned | Complete | Calls/world | Events/world | Actual calls | Tokens |
|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|
| `ring_control_set_001` | ring | 4 | off | `3350f4efc815…` | 12 | 12 | 25 | 30 | 300 | 100650 |
| `solo_control_set_001` | solo | 12 | off | `1504bcc24836…` | 12 | 12 | 25 | 28 | 300 | 96541 |
| `dyad_set_001` | dyad | 6 | off | `eaa74865ed2e…` | 12 | 12 | 25 | 29 | 300 | 99844 |
| `bounce_set_001` | bounce | 3 | off | `a0f0a130eae1…` | 12 | 12 | 25 | 31 | 300 | 99668 |

Totals: planned 48, complete 48, actual provider calls 1200, tokens 396703, technical failure records 2.

## Technical failures (preserved, excluded from scientific N)

| Set | World | Attempt | Exception | Message | Timestamp |
|---|---|---|---|---|---|
| `ring_control_set_001` | `E3_G3A_RING001_seed_1146035841` | attempt_001 | `OpenAIAdapterError` | OpenAI Responses request failed | 2026-10-02T20:04:22.946466+00:00 |
| `dyad_set_001` | `E3_G3A_DYAD001_seed_1117385864` | attempt_001 | `OpenAIAdapterError` | OpenAI Responses request failed | 2026-10-02T20:51:55.647004+00:00 |

## Mechanical verification

- Archived worlds equal the manifest's worlds for every set: PASS
- Exactly one complete attempt per world: PASS
- Raw file SHA-256 hashes match archive records: PASS
- Run class, provider, model, effort, probe, topology, root mode, rounds, call count, fallbacks, frozen runtime, plan freeze commit, manifest hash, seed and cell per attempt: PASS
- Event structure (count, three conditions, max depth, root set, served model on every event, no fallback-served event): PASS
- Frozen runtime drift: none

## Per-world raw hashes

### `ring_control_set_001`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3A_RING001_seed_1146035841` | B/B | attempt_001, attempt_002 | attempt_002 | `1d303e6ad645` | `184e57e876fa` | `0251f6495f13` |
| 2 | `E3_G3A_RING001_seed_1265697921` | B/B | attempt_001 | attempt_001 | `8b419bf31dd5` | `0dce767c0469` | `718373ff02b0` |
| 3 | `E3_G3A_RING001_seed_154869395` | B/B | attempt_001 | attempt_001 | `1ce618c93014` | `38d941efc9b0` | `c2707c5b6a43` |
| 4 | `E3_G3A_RING001_seed_1280872600` | B/B | attempt_001 | attempt_001 | `8ac12070320f` | `cd4f5db20b77` | `425e53cf58c1` |
| 5 | `E3_G3A_RING001_seed_1117385864` | B/A | attempt_001 | attempt_001 | `89c476312683` | `66a058ce34fa` | `69450cd0c963` |
| 6 | `E3_G3A_RING001_seed_1779995607` | B/A | attempt_001 | attempt_001 | `e3d290612b94` | `99480ac2634c` | `b6a418c8be6b` |
| 7 | `E3_G3A_RING001_seed_961840741` | A/B | attempt_001 | attempt_001 | `477c22346c47` | `bdcf951e390c` | `fb7c078a5f58` |
| 8 | `E3_G3A_RING001_seed_1813269025` | B/B | attempt_001 | attempt_001 | `b22a1d67f908` | `d9d72e26380f` | `6382ecb5666e` |
| 9 | `E3_G3A_RING001_seed_683505103` | A/A | attempt_001 | attempt_001 | `719debc2ec46` | `9b72d6f095f8` | `29a02d56ed62` |
| 10 | `E3_G3A_RING001_seed_1296650177` | B/B | attempt_001 | attempt_001 | `7277e9e74fa9` | `79f8785369a1` | `f000ccdf7f84` |
| 11 | `E3_G3A_RING001_seed_950201606` | A/A | attempt_001 | attempt_001 | `874c84e8ac8e` | `f238f87c2625` | `6ce5fe2dfff0` |
| 12 | `E3_G3A_RING001_seed_652310877` | B/B | attempt_001 | attempt_001 | `803ab410939e` | `a496164938e9` | `5d45bd800adb` |

### `solo_control_set_001`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3A_SOLO001_seed_1146035841` | B/B | attempt_001 | attempt_001 | `edc98250bde4` | `3a576e7ed7a6` | `8a95830f2bf5` |
| 2 | `E3_G3A_SOLO001_seed_1265697921` | B/B | attempt_001 | attempt_001 | `da11076eaa40` | `3a576e7ed7a6` | `fefe49b93087` |
| 3 | `E3_G3A_SOLO001_seed_154869395` | B/B | attempt_001 | attempt_001 | `22b380fae762` | `e2808d1548e3` | `3a65a2690dd1` |
| 4 | `E3_G3A_SOLO001_seed_1280872600` | B/B | attempt_001 | attempt_001 | `3c9b40e0425c` | `5babb2b6ba99` | `e7de4f7c9e0e` |
| 5 | `E3_G3A_SOLO001_seed_1117385864` | B/A | attempt_001 | attempt_001 | `1f69a0753de5` | `b7f47fe49d8c` | `f1191c717178` |
| 6 | `E3_G3A_SOLO001_seed_1779995607` | B/A | attempt_001 | attempt_001 | `45182c65490c` | `1f7dea9302f7` | `67057e5ab0b1` |
| 7 | `E3_G3A_SOLO001_seed_961840741` | A/B | attempt_001 | attempt_001 | `f2b78797dd5c` | `246eb8c702c7` | `c8629ca6cf87` |
| 8 | `E3_G3A_SOLO001_seed_1813269025` | B/B | attempt_001 | attempt_001 | `43938f5e56cd` | `2be538b74f02` | `24e681b5bea7` |
| 9 | `E3_G3A_SOLO001_seed_683505103` | A/A | attempt_001 | attempt_001 | `3e88a7edc8c2` | `7c6413b06bf6` | `32ceda01ec0c` |
| 10 | `E3_G3A_SOLO001_seed_1296650177` | B/B | attempt_001 | attempt_001 | `35773a659dbe` | `88c3a80f0263` | `8d55167d71e6` |
| 11 | `E3_G3A_SOLO001_seed_950201606` | A/A | attempt_001 | attempt_001 | `dba6b0ae7c95` | `7c6413b06bf6` | `ca43ca7ff3b2` |
| 12 | `E3_G3A_SOLO001_seed_652310877` | B/B | attempt_001 | attempt_001 | `0baeaa819cbf` | `5babb2b6ba99` | `1d9cb8cfd7af` |

### `dyad_set_001`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3A_DYAD001_seed_1146035841` | B/B | attempt_001 | attempt_001 | `3acc29f3f2c4` | `d39447cfa9f8` | `5b81f50e454c` |
| 2 | `E3_G3A_DYAD001_seed_1265697921` | B/B | attempt_001 | attempt_001 | `5f7d01bdf1fa` | `6b356474082e` | `f45fa80873bd` |
| 3 | `E3_G3A_DYAD001_seed_154869395` | B/B | attempt_001 | attempt_001 | `7a1af39c731f` | `46b7fb4324df` | `c21bb608e39e` |
| 4 | `E3_G3A_DYAD001_seed_1280872600` | B/B | attempt_001 | attempt_001 | `772827896d58` | `6a21625a7f97` | `caf99a1e8c5d` |
| 5 | `E3_G3A_DYAD001_seed_1117385864` | B/A | attempt_001, attempt_002 | attempt_002 | `aa481fca8ecd` | `6c982c1d05c2` | `711e85959946` |
| 6 | `E3_G3A_DYAD001_seed_1779995607` | B/A | attempt_001 | attempt_001 | `993c53c028f7` | `e9e1a250c0da` | `55650dece347` |
| 7 | `E3_G3A_DYAD001_seed_961840741` | A/B | attempt_001 | attempt_001 | `223e78bb9b45` | `fbd91956e193` | `a9a1ec6ab2b3` |
| 8 | `E3_G3A_DYAD001_seed_1813269025` | B/B | attempt_001 | attempt_001 | `66e77c36b3cc` | `7a419dac1cfc` | `61d09b230c82` |
| 9 | `E3_G3A_DYAD001_seed_683505103` | A/A | attempt_001 | attempt_001 | `ae99d72684d0` | `6fc5800c0e0e` | `9361d532d524` |
| 10 | `E3_G3A_DYAD001_seed_1296650177` | B/B | attempt_001 | attempt_001 | `ec2ae52ffb46` | `58e7193482b1` | `6a4a3c55a0f7` |
| 11 | `E3_G3A_DYAD001_seed_950201606` | A/A | attempt_001 | attempt_001 | `8ebc86f7cf7e` | `af0ea70dc640` | `64cfa1357ded` |
| 12 | `E3_G3A_DYAD001_seed_652310877` | B/B | attempt_001 | attempt_001 | `daa5213f6966` | `173277d19b04` | `da7923e355ee` |

### `bounce_set_001`

| Order | World | Cell | Attempts | Complete | events.jsonl | summary.csv | run_metadata.json |
|---:|---|---|---|---|---|---|---|
| 1 | `E3_G3A_BOUNCE001_seed_1146035841` | B/B | attempt_001 | attempt_001 | `e34e4e4ced43` | `e675685acc31` | `a095f356837a` |
| 2 | `E3_G3A_BOUNCE001_seed_1265697921` | B/B | attempt_001 | attempt_001 | `d74ce1ebabda` | `fdf86b3ee4e7` | `e6f7ae669070` |
| 3 | `E3_G3A_BOUNCE001_seed_154869395` | B/B | attempt_001 | attempt_001 | `cd30de710a83` | `7e5c60dace71` | `1534c41f5fc9` |
| 4 | `E3_G3A_BOUNCE001_seed_1280872600` | B/B | attempt_001 | attempt_001 | `771519bfa4f0` | `f7717cc2366b` | `4bef11a98fec` |
| 5 | `E3_G3A_BOUNCE001_seed_1117385864` | B/A | attempt_001 | attempt_001 | `bae07bdd8c0a` | `b75022ab421e` | `b4fc14877b86` |
| 6 | `E3_G3A_BOUNCE001_seed_1779995607` | B/A | attempt_001 | attempt_001 | `299a8254511b` | `fdfb13c975ee` | `55f956ea956c` |
| 7 | `E3_G3A_BOUNCE001_seed_961840741` | A/B | attempt_001 | attempt_001 | `5c3e1199e3af` | `cc1af3f209e9` | `00cdd4203d5c` |
| 8 | `E3_G3A_BOUNCE001_seed_1813269025` | B/B | attempt_001 | attempt_001 | `248a0cc85ea9` | `1c0f70881004` | `400417766e4a` |
| 9 | `E3_G3A_BOUNCE001_seed_683505103` | A/A | attempt_001 | attempt_001 | `a9821691e3df` | `589bd7e288c4` | `eb258f2d14b6` |
| 10 | `E3_G3A_BOUNCE001_seed_1296650177` | B/B | attempt_001 | attempt_001 | `9eec1199e2d5` | `6bdea8f5792a` | `77bbd0d5dca5` |
| 11 | `E3_G3A_BOUNCE001_seed_950201606` | A/A | attempt_001 | attempt_001 | `940704c38123` | `86d7d0e7d6cd` | `82bdba9da1d2` |
| 12 | `E3_G3A_BOUNCE001_seed_652310877` | B/B | attempt_001 | attempt_001 | `f8a31724eac0` | `ff3fac2ef6d6` | `57334537885f` |

## Scientific boundary

No answer, confidence, P(A), Brier, message, provenance mark, excess, FIS, DSCD, FREE/LINEAGE comparison or any other outcome was read, computed or reported. This audit establishes that data collection for the stage is complete and technically sound. It is not an interpretation.

## Replication start condition

A PASS here means this stage's data collection is complete. Under the frozen plan, the replication stage (Set 002) starts after Set 001 passes this audit and before any primary-outcome audit of Set 001, so that Set 002 runs regardless of what Set 001 shows. Gate closure requires both stages.
