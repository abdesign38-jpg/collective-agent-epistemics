# EXP-003 Gate 3C Primary-Outcome Audit: Specification v0.1 (pre-registered)

**Status:** CONFIRMED by the project owner (items D1 to D6, section 12) on 2026-11-02, before any Gate 3C model call. Binding once committed to `main` together with the tool that implements it (`tools/gate3c_primary_outcome_audit.py`, `tools/gate3c_synthesis.py`) and their tests on stub data, in a commit that precedes any Gate 3C archive. The Gate 3C plan is not altered by this document; this document turns the plan's outcomes and expectations E1 to E7 into mechanical rules over fields the frozen runtime archives. Every expectation is given as a trace: hypothesis → archived input fields → calculation → decision rule → verdict → interpretation boundary.

## 1. What Gate 3C tests, and what this spec must not do

Gate 3C removes re-grounding: the origin A sees its direct observation at its first firing only. On worlds that have a re-grounded twin (contemporary in Set 001 for the Gate 3A shapes, archived for the diamond and for Set 002), it asks whether deviations from the single-root reference persist, compound or change, under FREE and LINEAGE, in five shapes; and whether origin inflation under LINEAGE occurs without the direct observation in the prompt (H1, strict necessity).

Forbidden: pooling stages, arms or probe settings; any significance test or threshold chosen after inspection; any correction of a historical twin by the drift gauge; any claim about H2, recognition, continuity, attribution, what a FIS event counted, or semantic preservation; altering a rule after a value is seen.

## 2. Inputs

Gate 3C archive per world and attempt: `events.jsonl`, `summary.csv`, `run_metadata.json`; the stage's corpus audit (required PASS; file hashes re-checked). Twin archives: Gate 3A `results/archive/gate_3a/{ring_control,solo_control,dyad,bounce}_set_00{1,2}` and Gate 3B `results/archive/gate_3b/diamond_set_00{1,2}`, every file re-checked against the hash recorded in the committed Gate 3A and 3B corpus audits; contemporary twins in Gate 3C's own archive. Archived per event and used here: `sender`, `receivers`, `cycle`, `visible_message_id`, `model_visible_input`, `agent_reported_information` (message text), `p_a`, `reference_p_a`, `p_a_excess_over_reference`, `p_a_delta_without_new_evidence`, `reported_distinct_source_count`, `false_independent_support`, `independent_evidence_root_count`, `inference_depth`, `redundant_root_exposures`, `provenance.{source_named, reliability_named, erosion_count, eroded_fields, agent_as_source, inbound_agent_as_source}`, `response_reused`. Stored metrics are cross-checked against the raw answer, confidence and roots with the frozen runtime's functions, as the Gate 3A and 3B tools do; any mismatch is a Problem. Nothing is re-measured.

## 3. Direction rule (single-root arms only; D1)

Gate 3A spec 4.1 unchanged: `certainty_excess = p_observed − reference_observed`, `p_observed = p_a` if E1 observed A else `1 − p_a`, `reference_observed = max(reference_p_a, 1 − reference_p_a)` (= .70 throughout, one root), tolerance τ = 1e-6 for the kind labels at reference / discount / inflation. Event thresholds (.01) are stated per rule below.

## 4. Positions (D2)

Firing sequences are identical in each detached topology and its twin (frozen `topology.py`), so matched positions are matched `visible_message_id`. Post-seed firings only unless stated.

| Shape | Seed | Cycle firings (K cycles) | Far agent | A post-seed ids | Relay positions (E1) |
|---|---|---|---|---|---|
| ring, ring_detached | M01 A→B | B→C, C→A, A→B (K=4) | C: M03, M06, M09, M12 | M04, M07, M10, M13 | B: M02, M05, M08, M11; C as above |
| bounce, bounce_detached | M01 A→B | B→C, C→B, B→A, A→B (K=3) | C: M03, M07, M11 | M05, M09, M13 | B outward M02, M06, M10; B return M04, M08, M12; C as above |
| dyad, dyad_detached | M01 A→B | B→A, A→B (K=6) | B: M02, M04, M06, M08, M10, M12 | M03, M05, M07, M09, M11, M13 | B as above |
| solo, solo_detached | M01 A→A | A→A (K=12) | A: M02 … M13 | M02 … M13 | none (E1 not assessable) |
| diamond, diamond_detached | M01 A→{B,C} | B→D, C→D, D→A, A→{B,C} (K=4) | D: M04, M08, M12, M16 | M05, M09, M13, M17 | B: M02, M06, M10, M14; C: M03, M07, M11, M15; D as above |

Positions are read from the archived structural fields (`sender`, `cycle`, `visible_message_id`), never from an outcome value. The tool asserts that each detached event's `sender` and `cycle` equal its twin's at the same id, and lists any mismatch as a Problem.

## 5. Integrity-level checks (read no outcome value)

5.1 **Corpus audit** per stage, as Gates 3A and 3B (existing tool; it already handles detached topologies).

5.2 **Manipulation check** (contract Point D). For every detached-arm world: every post-seed firing of A has `model_visible_input` containing the line `Direct observation: none`; the seed firing contains `Direct observation:` followed by `Source: sensor_1`. For every twin world: every A firing contains the direct-observation block. For every matched pair at the same id: the sections of the two prompts other than the direct-observation block have the same structure (same headers in the same order; message contents differ because they are model outputs). Any failure is a Problem and the stage audit refuses to produce verdicts.

5.3 **Baseline comparability at the seed firing** (contract C1). The seed firing M01 has an identical prompt in detached and twin executions of a world and is sampled separately. Per world: `p_a` detached, `p_a` twin, their absolute difference, and whether `agent_reported_information` is byte-identical. Reported as a table and as the distribution of the absolute difference (count of worlds with difference 0, ≤ .01, ≤ .05, > .05). This is the gate's estimate of sampling variance under an identical prompt; it carries no verdict, excludes no world, and is printed above every paired table.

## 6. Definitions

- `d(w, c, id)`: paired difference at matched id in world w, condition c: `certainty_excess_detached − certainty_excess_twin`. Post-seed ids only.
- `Ā_w(c)`: mean of `|d|` over all post-seed matched ids of world w, condition c.
- `C_k(w, c)`: mean of `|d|` over the firings of cycle k in world w, condition c, k = 1 … K.
- Within-agent trajectory: for agent g in world w, condition c, the ordered list of its own firings with `p_a`, `certainty_excess`, kind, `reported_distinct_source_count`, FIS; and the within-agent delta `Δ_g = certainty_excess(this firing) − certainty_excess(g's previous firing)`, reported beside the archived `p_a_delta_without_new_evidence` (which is the delta from the previous firing of any agent) with the definition difference stated once.
- Far-agent magnitude in cycle k: `|certainty_excess|` at the far agent's firing in cycle k (one firing per cycle in every shape).
- Retention: for marker m ∈ {`source_named`, `reliability_named`} and a set of messages S, `R_m(S)` = share of messages in S with m true.
- LINEAGE deviation and discount rates for an arm and stage: over all post-seed firings of all agents, the share with kind ≠ at_reference (deviation) and the share with kind = discount (discount), τ = 1e-6, as Gate 3A's E6 quantity.
- Flat band for signs: a stage mean within ±.005 of zero counts as flat (Gate 3B E7 convention).
- Majority of 12 worlds: at least 7 (a strict majority of the paired worlds; the tool computes it as n // 2 + 1 so that stub tests on fewer worlds use the same rule). Ties count as not greater, throughout.

## 7. Pre-registered expectations: traces (D3)

### E1, relay-position marker loss

- *Hypothesis:* relay positions in detached arms lose the literal source id and reliability markers faster with depth than in twins.
- *Inputs:* `provenance.source_named`, `provenance.reliability_named`, `cycle`, `sender` at relay positions (section 4); both conditions.
- *Calculation:* per arm, condition, marker m: `R_m(first cycle relays)` and `R_m(last cycle relays)` across the 12 worlds; loss `L_m = R_m(first) − R_m(last)`, for detached and for twin.
- *Rule:* consistent if `L_m(detached) > L_m(twin)` for both markers; contradicted if `L_m(detached) ≤ L_m(twin)` for either marker; not assessable for a marker if `R_m(first) = 0` in both executions (nothing to lose). Verdict per condition; arm verdict consistent only if consistent in both conditions.
- *Boundary:* literal markers measure wording, not meaning. A is excluded from E1 (manipulation-check position); its marker trajectory is reported descriptively. Solo: not assessable (no relay). In Set 002 the twin is historical: verdict reported with the qualification of section 10. Retention by depth and position is tabulated in full as a secondary table (section 8.1).

### E2, far-agent compounding

- *Hypothesis:* excess or discount magnitude at the far agent is larger at the last cycle than at the first.
- *Inputs:* far-agent firings (section 4), `certainty_excess`.
- *Calculation:* per world and condition, `M_last − M_first` where `M_k` is the far-agent magnitude in cycle k.
- *Rule:* world class increasing if `> .01`, decreasing if `< −.01`, stable otherwise; consistent if increasing is the modal class of the 12 worlds; contradicted otherwise (a tie for modal counts as not greater). Per condition; arm consistent only if consistent in both conditions.
- *Boundary:* magnitude only; direction reported beside it. Within-detached; no twin used; same standing in both stages.

### E3a, paired displacement (contract Point B)

- *Hypothesis:* detached and twin trajectories of the same world differ at matched positions.
- *Inputs:* `certainty_excess` at matched post-seed ids in both executions.
- *Calculation:* `Ā_w(c)` per world and condition; signed mean of `d` per world beside it.
- *Rule:* a world shows material displacement if `Ā_w > .01`; consistent if at least 7 of 12 worlds do; contradicted otherwise. Per condition; arm consistent only if consistent in both.
- *Boundary:* primary in Set 001; qualified in Set 002 (section 10). The seed-firing sampling-variance table (5.3) is printed above it. Direction carries no verdict.

### E3b, progressive divergence

- *Hypothesis:* the paired difference grows with cycle.
- *Inputs:* as E3a.
- *Calculation:* `C_k(w, c)`; `C_K − C_1` per world.
- *Rule:* world class increasing if `> .01`, decreasing if `< −.01`, stable otherwise; non-monotonic flag (no verdict) if any intermediate `C_k` lies more than .01 outside the closed interval between `C_1` and `C_K`; consistent if increasing is modal; contradicted if stable or decreasing is modal (tie counts as not greater). Per condition; arm consistent only if consistent in both.
- *Boundary:* as E3a.

### E4, solo detached null

- *Hypothesis:* solo detached shows no excess in either direction.
- *Inputs:* all post-seed A firings of `solo_detached_set_00N`, `certainty_excess`, kind.
- *Calculation:* count of firings with kind ≠ at_reference (τ) per condition; count with `|certainty_excess| > .01` beside it.
- *Rule:* consistent if the τ-count is 0 in both conditions; contradicted otherwise.
- *Boundary:* within-detached; same standing in both stages. The contemporary solo twin is reported beside it (Set 001) for comparison without verdict.

### E5, ladder ordering (contract C3)

- *Hypothesis:* the within-detached LINEAGE discount rate orders across the ladder as Gate 3A's did: ring > bounce > dyad > solo.
- *Inputs:* all post-seed firings, LINEAGE condition, of the four detached Gate 3A shapes; kind.
- *Calculation:* discount rate per arm (section 6); the LINEAGE inflation rate and the detached-minus-twin difference of the discount rate are tabulated beside it without verdict.
- *Rule:* consistent if `ring > bounce > dyad > solo` strictly; contradicted otherwise (any equality or inversion).
- *Boundary:* the quantity is the within-detached discount rate, chosen to be the same quantity Gate 3A's E6 ordered, so the claim is "the detached ladder orders like the re-grounded one"; it is not a claim about the size of the detachment effect, and it does not use the twins, so its standing is the same in both stages. The diamond is outside the ladder and is excluded from E5.

### E6, direct-observation necessity (H1, strict; contract Point A)

- *Hypothesis:* origin inflation under LINEAGE requires the direct observation in the prompt.
- *Inputs:* post-seed A firings under LINEAGE in `ring_detached`, `bounce_detached`, `diamond_detached` (every such firing receives a descendant of A's own lineage), `certainty_excess`; the same firings under FREE; `false_independent_support` at those firings in the diamond; the twin's A firings at the same ids.
- *Calculation:* event = `certainty_excess > .01`. Per arm and stage: event count, firings, per-firing rate, mean and max magnitude, worlds containing an event, worlds with events at consecutive A firings; the same for the twin; the same for detached FREE; FIS > 0 count at detached event firings (diamond).
- *Rule (binary, strict necessity):* consistent if the detached LINEAGE event count is 0; contradicted if ≥ 1. *Frequency tier (descriptive, no verdict):* (1) no detached event; (2) detached rate below the twin's; (3) detached rate equal to or above the twin's.
- *Boundary:* a consistent verdict is consistent with H1 and is not evidence for a mechanism; tiers characterize frequency and are never labelled as showing the observation relevant or irrelevant; nothing bears on H2; a detached FREE event rate above zero is printed beside the tier as a qualification (the envelope is then not the only active ingredient). Primary in both stages; the twin rate in Set 002 is historical and is labelled so.

### E7, within-detached directional replication (contract Point C)

- *Hypothesis:* Set 002 keeps the direction of every declared within-detached cell of Set 001.
- *Inputs:* far-agent post-seed firings of the five detached arms, both conditions, `certainty_excess`.
- *Calculation:* ten cells: for each detached arm and condition, the sign of the stage mean of `certainty_excess` at the far position (flat band ±.005).
- *Rule:* contradicted if any cell is positive in one stage and negative in the other; consistent otherwise.
- *Boundary:* assessed only in the synthesis, never in a single-stage audit. Compounding direction (sign of `C_K − C_1` at the far agent per arm and condition, flat band) and the E6 binary verdict per arm are reported beside the cells as descriptive replication without verdict. Set 002 paired-effect quantities are a separate qualified table (section 10) and never enter E7.

## 8. Secondary tables (descriptive, no verdict)

8.1 Retention by depth and position: `R_source_named`, `R_reliability_named`, mean `erosion_count`, per shape, condition, position, cycle; detached and twin side by side; A included here.
8.2 Return-message provenance at the origin: A's post-seed firings split by whether the inbound message's `source_named` is true, with excess, kind, FIS where probed, and inbound `inference_depth`; detached and twin. Under detachment this table also shows the only route by which the sensor's name reaches A.
8.3 Within-agent trajectories, every agent, every world, both conditions, with `Δ_g` and the archived sequential delta side by side.
8.4 Set 002 paired-effect table (section 10).
8.5 MACRO stopping boundary; EXP-002 family per world (final answer, accuracy, Brier, depth, roots, erosion, agent-as-source).

## 9. Drift gauge (Set 001; D4)

- *Inputs:* `ring_contemporary_set_001` and Gate 3A `ring_control_set_001`, same 12 worlds, all post-seed firings, both conditions.
- *Calculation:* per position A, B, C and condition: LINEAGE deviation counts (kind ≠ at_reference) in each execution; per world and condition: mean over matched post-seed ids of `certainty_excess_contemporary − certainty_excess_historical`.
- *Declared operational tolerances (not derived from a variance model):* gauge PASS if, under LINEAGE, no position's deviation count differs by more than 4 of 48 between the executions, and the per-world paired mean excess is within .02 in at least 10 of 12 worlds (five sixths of the paired worlds, rounded up) under each condition. Otherwise FAIL.
- *Consequence:* execution never changes. On FAIL every paired verdict (E3a, E3b, E1 twin comparisons, E6 tiers) in both stages is printed with "not attributable to detachment; drift gauge FAIL" and the gauge table; the recorded contingency is a later, separately frozen stage with contemporary twins. On PASS the Set 001 paired verdicts stand as primary; Set 002 paired verdicts remain qualified (section 10) because the gauge measures one shape over one interval.
- *Wording:* differences are reported as "observed behavior differed across execution windows under the same nominal model configuration" (contract C4).

## 10. Temporal comparability and the Set 002 paired table

Every paired quantity is labelled with its twin's execution date and the gap in days. Set 001: ring, solo, dyad, bounce twins contemporary (same freeze, same frozen order); diamond twin Gate 3B Set 001 (2026-10-30/31), gap recorded. Set 002: all twins historical (Gate 3A Set 002, 2026-10-02; Gate 3B Set 002, 2026-10-31), gap recorded. Set 002's E1, E3a and E3b verdicts are computed by the identical rules, placed in a table headed "paired, historical control, qualified", with the Set 001 drift gauge result printed in the same table, and never pooled with Set 001 or corrected by the gauge.

## 11. Outputs and order of operations (D5)

Under `experiments/EXP_003/audits/gate_3c/`, written by the tools: `EXP_003_GATE_3C_SET_00{1,2}_CORPUS_AUDIT_v0.1.{json,md}`; `EXP_003_GATE_3C_SET_00{1,2}_PRIMARY_OUTCOME_AUDIT_v0.1.{json,md}`; `EXP_003_GATE_3C_SYNTHESIS_v0.1.{json,md}` (E7, the two stages side by side, the drift gauge, the qualified Set 002 table, closure rule computed from the records). Order: this spec, the tool and its tests committed; Set 001 runs in frozen order; Set 001 corpus audit; Set 002 runs; Set 002 corpus audit; then one primary audit per stage, then the synthesis, then observations and tag. No behavioral value is read before both corpus audits pass. Records carry the plan hash, both corpus-audit hashes, the twin corpus-audit hashes, HEAD at audit time and repository-relative paths only.

## 12. Items confirmed by the owner (2026-11-02)

- **D1** Direction rule identical to Gate 3A (section 3); .01 as the event and displacement threshold, τ for kinds.
- **D2** Positions as tabulated (section 4), read from structural fields.
- **D3** The E1 to E7 traces as written: E1 at relay positions with loss `L_m` and both markers required; E2 and E3b world classes by ±.01 with modal rule; E3a majority of 12; E4 τ-count zero; E5 as the within-detached LINEAGE discount rate (confirmed by the owner 2026-11-02; inflation tabulated beside it, never combined), strictly ordered; E6 strict binary plus descriptive tiers; E7 ten far-position cells with ±.005.
- **D4** Drift gauge tolerances (4 of 48; .02 in 10 of 12) as declared operational tolerances, and the FAIL consequence.
- **D5** Output names, the synthesis as the only place E7 is assessed, and the integrity-level checks (manipulation check refuses; seed comparability excludes nothing).
- **D6** The statistical unit is the world; arms, stages, conditions and agents are reported separately; no significance test; no pooling; no drift correction.
