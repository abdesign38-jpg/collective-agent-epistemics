# EXP-002 Gate 2B Corpus Integrity Audit v0.1

## Status

**PASS WITH DOCUMENTED TECHNICAL HISTORY**

This is a read-only corpus/provenance audit. Scientific interpretation was **not performed**.

## Provenance

- Pre-live checkpoint: `a5a0910691fc51dbbefdf0193c826ba7357af461`
- Technical-stop commit: `68fa27cd55e61254113849cec0f9fe064d72a8fa`
- Raw-data commit: `5fb6ddde3cb7398b3cb5e1dd6e58f02ac0cc0c53`
- Frozen runtime: `7e9aed1b7093baae10ae30f27e0b6a2b932f92f5`
- Protocol: `exp-002-protocol-v0.1`
- Plan freeze: `ecbcbc77d0832b82ea9da2abc3d800db759c238c`
- Canonical manifest commit: `1cd749c0cb8f04d64d7581d44364c8875e9799a2`
- Current plan SHA-256: `aa1152cce5705a422e004efe63ff2b5f4b87052f76798cd17bc8ff2262ceeaaa`
- Current manifest SHA-256: `a023e3338ace04e601f6478983cd21e3c762d842aabf30aef8be68ae475a48cf`

Commit chain: `a5a0910... -> 68fa27c... -> 5fb6ddd...` verified. The technical-stop commit contains only the preserved failure record. The raw-data commit is restricted to `results/archive/gate_2b/`.

## Corpus shape

| Set | Valid worlds | Expected | Valid attempts |
|---|---:|---:|---:|
| Generalization Set 001 | 12 | 12 | 12 |
| Stress Set 001 | 8 | 8 | 8 |
| Total scientific N | 20 | 20 | 20 |

Execution history contains `21` attempt directories: `20` valid scientific attempts and `1` technical failure attempt. The special world `G2B_GEN001_seed_874625177` has failed `attempt_001` and valid same-seed `attempt_002`. The other 19 valid attempts are `attempt_001`. No `attempt_003` exists.

## Technical failure

The preserved failure is under `generalization_set_001/G2B_GEN001_seed_874625177/attempt_001/failure_metadata.json`:

- status: `technical_failure`
- exception: `OpenAIAdapterError`
- seed: `874625177`
- config: rounds `4`, model `gpt-5.6-sol`, reasoning `medium`, paired
- failed-request count: `NOT DETERMINABLE FROM PRESERVED METADATA`
- excluded from scientific N: yes

No replacement world was introduced.

## Mechanical verification

- Plan/manifest bytes: PASS.
- Frozen runtime drift: PASS, no differences from `7e9aed1b...`.
- Manifest reconciliation and deterministic world reproduction: PASS for all 20 worlds.
- Canonical identity/path/seed/set/attempt metadata: PASS.
- Raw hash integrity: PASS, `0` mismatches across 20 valid attempts.
- Valid file counts: 20 each of `events.jsonl`, `summary.csv`, `run_metadata.json`, and `archive_metadata.json`; 1 `failure_metadata.json`.
- Configuration and fingerprints: PASS for all valid runs.
- Call accounting: 300 Generalization + 200 Stress = 500 valid provider calls; 80 reused responses.
- Event structure: 30 events per valid world, 600 total; FREE 13, LINEAGE 13, MACRO 4.
- Paired-response reuse: PASS.
- Actual-lineage invariants: PASS; root E1, count 1, depths FREE/LINEAGE 12 and MACRO 3.
- Summary/event consistency: PASS.
- Execution order: Generalization PASS; Stress PASS; retry failure timestamp precedes retry success timestamp.
- Runtime-emitted ID: `EXP_002_W01` in every valid archive; canonical manifest/archive IDs remain authoritative. This is expected frozen-runner identity mapping, not a mismatch.

## Scientific boundary

No DSCD, confidence, inflation, answer-flip, accuracy, Brier, FREE/LINEAGE, alignment, actor, dependency, message, causal, or hypothesis analysis was performed. Generalization and Stress were not scientifically pooled.

## Audit files

- Structured audit: `EXP_002_GATE_2B_CORPUS_AUDIT_v0.1.json`
- This report: `EXP_002_GATE_2B_CORPUS_AUDIT_v0.1.md`

Gate 2B data collection: **COMPLETE**  
Gate 2B corpus integrity: **VERIFIED**  
Gate 2B primary-outcome audit: **PENDING**  
Gate 2B scientific closure: **NOT YET COMPLETE**
