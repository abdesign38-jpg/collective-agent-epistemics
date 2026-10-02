# EXP-003 Gate 3A Historical Ring Observation v0.1 (secondary)

## Status

**SECONDARY OBSERVATION**

Secondary observation only. Same prompts, same model name, different dates; any difference is model drift over time and is recorded, never used to adjust a Gate 3A outcome. Sixteen of the historical runs are repeated executions of one world (seed 42); they are shown pooled and with the Gate 2B worlds alone. No test, no threshold.

## Provenance

- Contemporary set: `ring_control_set_001` (12 worlds); corpus audit `experiments/EXP_003/audits/gate_3a/EXP_003_GATE_3A_SET_001_CORPUS_AUDIT_v0.1.json` (PASS)
- Historical archive: `experiments/EXP_002/results/archive`: 36 runs, 21 distinct seeds, run classes {'gate_2b_real_model': 20, 'pilot_real_model': 16}, cells {'B/A': 6, 'A/A': 20, 'B/B': 5, 'A/B': 5}
- Factor ledger difference (contemporary vs historical): `{"experiment": ["EXP-003", "EXP-002"], "gate": ["3A", "2B"], "set": ["ring_control_set_001", "generalization_set_001"], "run_class": ["gate_3a_real_model", "gate_2b_real_model"], "prompt_version": ["exp003-v0.1", "exp002-v0.1"], "schema_version": ["exp003-agent-response-v0.1", "exp002-agent-response-v0.1"]}`
- HEAD at audit time: `12bbbabfe99945096ac6e808b90c161e824a3d4c`

## Per-position summary (post-seed events; d = discount, i = inflation, r = at reference)

| Corpus | Condition | Runs | A | B | C | A restoration | Sustained A deviation |
|---|---|---:|---|---|---|---:|---:|
| contemporary | free | 12 | 0d/0i/48r of 48 (|x̄| 0.000) | 1d/0i/47r of 48 (|x̄| 0.000) | 4d/1i/43r of 48 (|x̄| 0.003) | 1.000 | 0 |
| contemporary | lineage | 12 | 0d/8i/40r of 48 (|x̄| 0.011) | 8d/1i/39r of 48 (|x̄| 0.010) | 17d/0i/31r of 48 (|x̄| 0.027) | +0.833 | 1 |
| historical | free | 36 | 0d/1i/143r of 144 (|x̄| 0.001) | 0d/0i/144r of 144 (|x̄| 0.000) | 3d/0i/141r of 144 (|x̄| 0.001) | +0.993 | 0 |
| historical | lineage | 36 | 0d/0i/144r of 144 (|x̄| 0.000) | 18d/0i/126r of 144 (|x̄| 0.009) | 25d/0i/119r of 144 (|x̄| 0.014) | 1.000 | 0 |
| historical_gate_2b_only | free | 20 | 0d/1i/79r of 80 (|x̄| 0.002) | 0d/0i/80r of 80 (|x̄| 0.000) | 3d/0i/77r of 80 (|x̄| 0.002) | +0.988 | 0 |
| historical_gate_2b_only | lineage | 20 | 0d/0i/80r of 80 (|x̄| 0.000) | 11d/0i/69r of 80 (|x̄| 0.009) | 11d/0i/69r of 80 (|x̄| 0.014) | 1.000 | 0 |

## Boundary

Secondary observation only. Same prompts, same model name, different dates; any difference is model drift over time and is recorded, never used to adjust a Gate 3A outcome. Sixteen of the historical runs are repeated executions of one world (seed 42); they are shown pooled and with the Gate 2B worlds alone. No test, no threshold.
