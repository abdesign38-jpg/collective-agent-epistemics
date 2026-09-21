# EXP-002 Gate 2B World Manifest v0.1

## Status

**WORLD MANIFEST FROZEN / NOT YET EXECUTED**

This manifest was generated entirely from the deterministic derivation procedure defined in [GATE_2B_PLAN_v0.1.md](GATE_2B_PLAN_v0.1.md), executed locally against the frozen `WorldGenerator`. **Zero real-model calls were made to produce this manifest.**

After this manifest is committed, the world list, seeds, and execution order are immutable. Any future change requires a separately versioned plan.

## Anchors

- Research closure checkpoint: `de62984adc44566b513545feaf2d61fcc229e71c`
- Gate 2B plan freeze commit: `ecbcbc77d0832b82ea9da2abc3d800db759c238c`
- Frozen EXP-002 runtime: `7e9aed1b7093baae10ae30f27e0b6a2b932f92f5`
- Frozen protocol tag: `exp-002-protocol-v0.1`
- Derivation anchor: `de62984adc44566b513545feaf2d61fcc229e71c|exp-002-protocol-v0.1|GATE_2B_PLAN_v0.1`

## Exclusion registry

| Seed | Source | Source ref | Reason |
|---|---|---|---|
| 42 | GATE_2B_PLAN_v0.1.md section 2 | `de62984adc44566b513545feaf2d61fcc229e71c` | Seed 42 was inspected in Gate 2A / prior pilots before this plan was frozen |

Neither Generalization Set 001 nor Stress Set 001 selected seed `42`; no exclusion was actually triggered during selection.

## Generalization Set 001 (unfiltered, 12 worlds)

World selection used `candidate_seed("GEN001", ordinal, nonce)` for `ordinal = 1..12`, accepting the first candidate not excluded and not a duplicate. **No nonce escalation was required**: every ordinal's `nonce = 0` candidate was accepted directly, so the selection scan contains zero rejections.

Execution order is frozen by ascending `order_key = sha256(ANCHOR|ORDER|GEN001|seed)`.

| Order | Canonical ID | Seed | Internal world_id | Truth | Observed | Alignment |
|---:|---|---:|---|---|---|---|
| 1 | G2B_GEN001_seed_874625177 | 874625177 | EXP_002_W_874625177 | A | B | misleading |
| 2 | G2B_GEN001_seed_948364460 | 948364460 | EXP_002_W_948364460 | B | B | aligned |
| 3 | G2B_GEN001_seed_170961959 | 170961959 | EXP_002_W_170961959 | A | B | misleading |
| 4 | G2B_GEN001_seed_1925941366 | 1925941366 | EXP_002_W_1925941366 | B | B | aligned |
| 5 | G2B_GEN001_seed_1257399226 | 1257399226 | EXP_002_W_1257399226 | B | B | aligned |
| 6 | G2B_GEN001_seed_1027876222 | 1027876222 | EXP_002_W_1027876222 | B | A | misleading |
| 7 | G2B_GEN001_seed_1353126068 | 1353126068 | EXP_002_W_1353126068 | A | A | aligned |
| 8 | G2B_GEN001_seed_1926897563 | 1926897563 | EXP_002_W_1926897563 | B | A | misleading |
| 9 | G2B_GEN001_seed_1043406990 | 1043406990 | EXP_002_W_1043406990 | A | A | aligned |
| 10 | G2B_GEN001_seed_1114638083 | 1114638083 | EXP_002_W_1114638083 | B | A | misleading |
| 11 | G2B_GEN001_seed_1662733804 | 1662733804 | EXP_002_W_1662733804 | B | A | misleading |
| 12 | G2B_GEN001_seed_208630909 | 208630909 | EXP_002_W_208630909 | A | B | misleading |

All 12 worlds use evidence root `E1`, sensor reliability `0.70`, and the frozen paired EXP-002 v0.1 configuration. Truth/observed-state distribution across this unfiltered set: 5 aligned, 7 misleading (an emergent property, not a selection target).

## Stress Set 001 (targeted, prospectively stratified, 8 worlds)

World selection scanned `candidate_seed("STRESS001", scan_index, 0)` for `scan_index = 1, 2, 3, ...`, classifying each candidate's `truth/observed_state` cell and accepting until each of the four cells (`A/A`, `B/B`, `A/B`, `B/A`) held exactly 2 accepted worlds. The scan ran through `scan_index = 19` before all four cells were full.

Execution order is frozen by ascending `order_key = sha256(ANCHOR|ORDER|STRESS001|seed)`.

| Order | Canonical ID | Seed | Internal world_id | Truth | Observed | Cell | Alignment |
|---:|---|---:|---|---|---|---|---|
| 1 | G2B_STRESS001_seed_1211074116 | 1211074116 | EXP_002_W_1211074116 | B | B | B/B | aligned |
| 2 | G2B_STRESS001_seed_945922859 | 945922859 | EXP_002_W_945922859 | B | B | B/B | aligned |
| 3 | G2B_STRESS001_seed_319975066 | 319975066 | EXP_002_W_319975066 | B | A | B/A | misleading |
| 4 | G2B_STRESS001_seed_1531843854 | 1531843854 | EXP_002_W_1531843854 | A | B | A/B | misleading |
| 5 | G2B_STRESS001_seed_515022515 | 515022515 | EXP_002_W_515022515 | B | A | B/A | misleading |
| 6 | G2B_STRESS001_seed_217181935 | 217181935 | EXP_002_W_217181935 | A | A | A/A | aligned |
| 7 | G2B_STRESS001_seed_1247992891 | 1247992891 | EXP_002_W_1247992891 | A | A | A/A | aligned |
| 8 | G2B_STRESS001_seed_1523495488 | 1523495488 | EXP_002_W_1523495488 | A | B | A/B | misleading |

Final cell counts: `A/A = 2`, `B/B = 2`, `A/B = 2`, `B/A = 2`. This set is intentionally stratified and must not be read as an unbiased prevalence sample.

### Stress selection scan (including rejected candidates)

| Scan index | Candidate seed | Truth | Observed | Cell | Accepted | Reason if rejected |
|---:|---:|---|---|---|---|---|
| 1 | 1211074116 | B | B | B/B | yes | — |
| 2 | 945922859 | B | B | B/B | yes | — |
| 3 | 1247992891 | A | A | A/A | yes | — |
| 4 | 217181935 | A | A | A/A | yes | — |
| 5 | 1791476913 | A | A | A/A | no | cell_full |
| 6 | 2092598332 | A | A | A/A | no | cell_full |
| 7 | 1271319373 | A | A | A/A | no | cell_full |
| 8 | 1074218747 | B | B | B/B | no | cell_full |
| 9 | 37444839 | B | B | B/B | no | cell_full |
| 10 | 319975066 | B | A | B/A | yes | — |
| 11 | 1523495488 | A | B | A/B | yes | — |
| 12 | 1692118867 | B | B | B/B | no | cell_full |
| 13 | 1529813721 | A | A | A/A | no | cell_full |
| 14 | 1284154942 | B | B | B/B | no | cell_full |
| 15 | 993197738 | B | B | B/B | no | cell_full |
| 16 | 515022515 | B | A | B/A | yes | — |
| 17 | 475958240 | A | A | A/A | no | cell_full |
| 18 | 687885545 | A | A | A/A | no | cell_full |
| 19 | 1531843854 | A | B | A/B | yes | — |

No candidate was rejected for exclusion or duplication; all rejections in this scan were `cell_full`.

## Selection integrity checks

- Generalization Set 001 and Stress Set 001 share zero seeds.
- Seed `42` was not selected by either set.
- All 12 Generalization seeds are pairwise distinct; all 8 Stress seeds are pairwise distinct.
- No world membership, truth, observed state, or alignment was used to reject or replace any Generalization candidate.
- Stress candidates were rejected only for exclusion, duplication, or a full cell — never for truth, observed state pattern preference beyond the defined cell target, message content, or anticipated model behavior.

## Archival namespaces (to be used at execution time)

```text
experiments/EXP_002/results/archive/gate_2b/generalization_set_001/<canonical_world_id>/attempt_<NNN>/
experiments/EXP_002/results/archive/gate_2b/stress_set_001/<canonical_world_id>/attempt_<NNN>/
```

## Closure of this step

With this manifest committed:

- the 12 + 8 = 20 planned worlds are frozen;
- execution order per set is frozen;
- no Gate 2B model call has yet been made;
- Gate 2B execution may begin only after this commit, following the plan's pre-execution checklist.
