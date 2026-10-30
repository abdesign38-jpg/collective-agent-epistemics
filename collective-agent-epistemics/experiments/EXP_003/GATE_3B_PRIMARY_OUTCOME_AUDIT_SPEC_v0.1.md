# EXP-003 Gate 3B Primary-Outcome Audit: Specification v0.1 (pre-registered)

**Status:** CONFIRMED by the project owner (items D1 to D5 below) on 2026-10-30, before any Gate 3B model call was made and before any Gate 3B outcome value existed. This file is committed to `main` together with the tool that implements it (`tools/gate3b_primary_outcome_audit.py`) and that tool's tests (`tests/test_exp003_gate3b_primary_outcome_audit.py`, stub data only), in a commit that precedes the commit carrying any Gate 3B archive or audit output. The tool computes exactly what this specification says and nothing else.

**What this document is.** The frozen plan (`GATE_3B_PLAN_v0.1.md`, "Primary outcomes" and expectations E1 to E7) names what is computed but phrases several items narratively. This specification turns each item into one mechanical rule over fields the frozen runtime already archives, so that a reviewer can check from git history that no rule was chosen after inspection. It adds no measurement, no threshold, no test. The plan is frozen and is not altered by this document.

## 1. What Gate 3B measures, and what this spec must not do

Gate 3B is the first fan-in: D receives two messages descended from the same root through B and C. The plan's question is whether D's reported P(A) exceeds the single-root reference, whether D reports more than one distinct source, and whether the lineage envelope changes either without suppressing evidence that really is independent (the dual-root positive control). The probe is on, so `reported_distinct_source_count` and `false_independent_support` (FIS) are primary outcomes for the first time.

Forbidden, as in Gate 3A: pooling Set 001 with Set 002; any significance test, threshold or event selected after inspection; comparing against Gate 3A arms as a primary outcome (the plan names those comparisons descriptive and secondary, and the probe setting differs); altering a verdict rule after a value is seen.

## 2. Inputs

Per world and attempt: `events.jsonl`, `summary.csv`, `run_metadata.json` (for the world's evidence list), and the stage's corpus integrity audit (required PASS; file hashes re-checked). Archived per event: `p_a`, `reference_p_a`, `p_a_excess_over_reference`, `reported_distinct_source_count`, `false_independent_support`, `independent_evidence_root_count`, `redundant_root_exposures`, `inference_depth`, `provenance.*` (including `source_named`, `agent_as_source`, `inbound_agent_as_source`, `erosion_count`), `receivers`, `cycle`, `response_reused`. Stored metrics are cross-checked against the raw answer, confidence and roots with the frozen runtime's own functions, exactly as the Gate 3A tool does; any mismatch is listed under Problems. Nothing is re-measured.

## 3. Direction rules

### 3.1 Single-root arms (`diamond_set_00N`, `solo_control_set_003`, `probe_off_set_001`) — D1

Identical to Gate 3A spec 4.1: `certainty_excess = p_observed − reference_observed` with `p_observed = p_a` if E1 observed A else `1 − p_a`, `reference_observed = max(reference_p_a, 1 − reference_p_a)`, tolerance τ = 1e-6. Terms: at reference, discount, inflation, magnitude.

### 3.2 Dual-root arm (`dual_root_set_00N`) — D2

The runtime archives `reference_p_a` per event from the roots actually in that message's lineage, so the reference changes as E2 enters (A's and B's messages carry E1 only; C's and D's carry E1 and E2). Two strata, pre-declared in the plan: **agreeing** (E1 and E2 observed the same state; two-root reference ≈ .845 toward it) and **conflicting** (opposite states; two-root reference = .50). The stratum is read from the world's evidence list in `run_metadata.json`, never from any outcome.

- When `reference_p_a ≠ .5` (all single-root events, and all two-root events in the agreeing stratum): the favored state is the one the reference points to; `certainty_excess = P(favored) − max(reference_p_a, 1 − reference_p_a)`; terms as in 3.1.
- When `reference_p_a = .5` (two-root events in the conflicting stratum): no favored state exists, so discount and inflation are undefined. The event is recorded with kind `departure_from_even`, the signed field `departure_toward_e1` (`p_a − .5` when E1 observed A, `.5 − p_a` when E1 observed B) and its magnitude; tables for this stratum report that signed value and never label it discount or inflation.

Both strata are reported separately and never pooled (8 worlds each per stage), in every table including the secondary table 7.

### 3.3 False independent support

`false_independent_support = max(0, reported_distinct_source_count − independent_evidence_root_count)`, as archived. "FIS > 0" means the agent reported more distinct sources than its lineage contains.

## 4. Positions

| Arm | Firing order (depth 12) | D firings | A post-seed firings |
|---|---|---|---|
| diamond, dual-root, probe-off (4 rounds) | M01 A; then per cycle B, C, D, A: M02 B, M03 C, M04 D, M05 A, … M17 A | M04, M08, M12, M16 | M05, M09, M13, M17 (4 hops each) |
| solo (12 rounds) | M01…M13, all A | none | M02…M13 (1 hop each) |

D receives two inbound messages at every firing (from B and from C of the same cycle); A receives one (from D). Positions are read from the archived structural fields (sender, cycle, receivers, message order), never from any outcome value.

## 5. Tables

All per condition (FREE and LINEAGE separately; MACRO as stopping boundary), per world, per stage, paired by seed across arms where seeds are shared (Arm 1 with Arms 3 and 4).

1. **D at every firing** (Arm 1 and Arm 2): `p_a`, `reference_p_a`, `certainty_excess` or `departure_toward_e1`, `reported_distinct_source_count`, `independent_evidence_root_count`, FIS, `redundant_root_exposures`, and for each of the two inbound messages its `source_named` and `agent_as_source` marks.
2. **A at every post-seed firing** (all arms): as Gate 3A table 4, plus the inbound `source_named` mark.
3. **The matrix by world**: for each Arm 1 and Arm 2 world, mean D `certainty_excess` (or mean `departure_toward_e1`, conflicting stratum) under FREE and under LINEAGE; D FIS events under each.
4. **Per-agent finals**: final P(A), max and min excess per agent, from `summary.csv`.
5. **Probe reactivity (Arm 4 vs Arm 1)**: the four shared worlds, mean D `certainty_excess` under probe off and probe on, both conditions, and the gap.
6. **Solo control 003**: as Gate 3A table 5 (probe on this time).
7. **Secondary, motivated by Gate 3A observations v0.2**: at D and at A, per condition and per stratum, excess (or departure) and FIS against how many of the inbound messages named the sensor (`source_named`). Descriptive; not an expectation; carries no verdict.
8. **EXP-002 family per world** (final answer, accuracy, Brier, depth, roots, erosion, agent-as-source), with cells (`truth/E1` for single-root, `truth/E1/E2` for dual-root) and stratum on every row.

## 6. Pre-registered expectations, mechanical rules — D3

| Id | Plan wording (contradicted by) | Mechanical rule, per stage |
|---|---|---|
| E1 | FREE D shows positive excess in at least some Arm 1 worlds (contradicted: FREE D excess within .01 of zero in all 12 worlds) | contradicted if, in every Arm 1 world, every FREE D firing has `certainty_excess ≤ .01` |
| E2 | LINEAGE D excess not greater than FREE D excess in the same world (contradicted: LINEAGE exceeds FREE in a majority of worlds) | per Arm 1 world compare mean D `certainty_excess` LINEAGE vs FREE; contradicted if LINEAGE > FREE + τ in 7 or more of 12 worlds |
| E3 | positive excess at D co-occurs with FIS > 0 (contradicted: excess without FIS, or FIS without excess, dominates) | over Arm 1 D firings, each condition: count concordant (excess > τ and FIS > 0), discordant-A (excess > τ, FIS = 0), discordant-B (excess ≤ τ, FIS > 0); contradicted if discordant-A + discordant-B > concordant in either condition |
| E4 | inbound agent-as-source wording precedes positive excess more often than clean wording (contradicted: no association) | over Arm 1 D firings, each condition: rate of excess > τ when at least one inbound carries `agent_as_source` vs when neither does; contradicted if rate(marked) ≤ rate(unmarked) in either condition; not assessable if either group is empty |
| E5 | Arm 2 D approaches the two-root reference under both conditions (contradicted: D stays at .70 with two roots, or exceeds .845) | agreeing stratum, two-root D firings, each condition: classify `P(favored)` as `two_root` (within .01 of the two-root reference), `single_root` (within .01 of .70), `over` (> two-root reference + .01), `other`; contradicted if `single_root` or `over` is the modal class in either condition. Conflicting stratum: report `departure_toward_e1` only |
| E6 | Arm 4 excess at D within .02 of Arm 1 in the same worlds (contradicted: a larger gap, the probe is reactive) | for each of the 4 shared worlds and each condition: gap = \|mean D `certainty_excess` (probe off) − (probe on)\|; contradicted if any gap > .02 |
| E7 | Set 002 reproduces the Set 001 direction in every matrix cell (contradicted: a reversed cell) | synthesis only, never in a single-stage audit: per cell (Arm 1 FREE, Arm 1 LINEAGE, Arm 2 agreeing FREE, Arm 2 agreeing LINEAGE, Arm 2 conflicting FREE, Arm 2 conflicting LINEAGE) the sign of the stage mean (`certainty_excess`, or `departure_toward_e1` for the conflicting cells), with means within ±.005 of zero counted as flat; contradicted if any cell is positive in one stage and negative in the other |

Verdicts restate the plan's own contradiction column. Rates compared as plain numbers; ties count as "not greater". A single-stage audit prints E1 to E6 and marks E7 as deferred to the synthesis.

## 7. Secondary and descriptive comparisons (never primary)

- Gate 3B D and A positions beside Gate 3A bounce and ring positions (same model, one added agent), noting that Gate 3A ran probe off; the probe-off arm (table 5) is the only like-for-like bridge.
- Table 7 (inbound `source_named`), motivated by the Gate 3A observation that all 21 origin-inflation events followed an inbound message that did not name the sensor. Pre-registered here as descriptive; if the pattern recurs at D, it becomes a candidate expectation for Gate 3C's plan, not a change to this gate.

## 8. Outputs — D4

Under `experiments/EXP_003/audits/gate_3b/`, written by the tool, never by hand:

- `EXP_003_GATE_3B_SET_001_CORPUS_AUDIT_v0.1.{json,md}` and `EXP_003_GATE_3B_SET_002_CORPUS_AUDIT_v0.1.{json,md}` (from `tools/corpus_audit.py`; a PASS is a precondition of the primary audit of that stage).
- `EXP_003_GATE_3B_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1.{json,md}` and `EXP_003_GATE_3B_SET_002_PRIMARY_OUTCOME_AUDIT_v0.1.{json,md}` (from `tools/gate3b_primary_outcome_audit.py`).
- `EXP_003_GATE_3B_SYNTHESIS_v0.1.{json,md}` (E7, stages kept separate), then observations under `research/observations/`, then tag `exp-003-gate3b-closed-v0.1`.

Every record carries the plan hash, the corpus audit hash, the HEAD commit at audit time and repository-relative paths only.

## 9. Order of operations

1. Owner confirms D1 to D5; this spec, the tool and its tests (stub preflight data only) are committed together, before any Gate 3B value is read.
2. Set 001's corpus audit passes before Set 002 runs (Gate 3A rule). No primary-outcome audit of either stage runs until both corpus audits pass; then one run per stage, outputs committed in a later commit.
3. Synthesis, observations, tag.

## 10. Items confirmed by the owner (2026-10-30)

- **D1** Single-root direction rule identical to Gate 3A (section 3.1).
- **D2** Dual-root rule: favored-state certainty excess when the reference is not .5; signed departure from even with no discount/inflation label when it is .5; strata never pooled (section 3.2).
- **D3** The E1 to E7 rules as written, with the stated tolerances (.01 for E1 and E5, .02 for E6, .005 flat band for E7, majority = 7 of 12 for E2).
- **D4** Output names and the separate synthesis step.
- **D5** Table 7 is included as a descriptive secondary table and nothing more.
