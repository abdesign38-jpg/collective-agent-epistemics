# EXP-003 Gate 3A Primary-Outcome Audit: Specification v0.1 (pre-registered)

**Status:** CONFIRMED by the project owner (items D1 to D4 below) on 2026-10-02, before any Gate 3A outcome value was read by anyone. This file is committed to `main` together with the tool that implements it (`tools/primary_outcome_audit.py`) and that tool's tests, in a commit that precedes the commit carrying any audit output. The tool computes exactly what this specification says and nothing else.

**What this document is.** The frozen plan (`GATE_3A_PLAN_v0.1.md`, "Primary outcomes") names what is computed but phrases several items narratively. This specification turns each item into one mechanical rule over fields the frozen runtime already archives, so that a reviewer can check from git history that no rule was chosen after inspection. It adds no measurement, no threshold, no test.

---

## 1. Chain-of-structure check

The repository structure (`research/REPOSITORY_RESEARCH_STRUCTURE_v0.2.md`) fixes the chain: question → prospective design → execution → immutable archive → audit → synthesis → checkpoint.

| Link | Gate 3A state | Evidence |
|---|---|---|
| Scientific question | Hypothesis v0.1; EXP-003 fan-in question; Gate 3A question (four structures, where deviation occurs, whether the origin corrects it) | `research/hypothesis_v0.1.md`, `protocol.md`, `GATE_3A_PLAN_v0.1.md` |
| Prospective design | Plan FROZEN at `fe5e025`; eight manifests at `addfb5e`; expectations E1 to E6 pre-registered | plan anchors; corpus audits |
| Execution | Both stages run under `gate_3a_real_model`, probe off, fallbacks off, frozen runtime `c54563b` | archive metadata, verified by the corpus audits |
| Immutable archive | 96 worlds at `results/archive/gate_3a/*/attempt_*`; raw hashes recorded | commits `7f12ba4` (Set 001), `1288b7d` (Set 002) |
| Audit, corpus half | PASS for both stages | `7d262ee`, `3a72efa` |
| **Audit, primary-outcome half** | **this specification, then the tool, then one run per stage** | this commit and the next |
| Synthesis | Set 001 and Set 002 reported separately; E6 compares their orderings | after both stage audits |
| Checkpoint | `exp-003-gate3a-closed-v0.1` on the closure commit | after synthesis |

The layers stay distinct: the tool lives in `experiments/EXP_003/tools/` (outside the frozen runtime), its output in `experiments/EXP_003/audits/gate_3a/`, and the relation to the hypothesis in `research/observations/` later. The plan's closure rule requires "the predefined primary outcomes are audited, arms and stages are reported separately, the historical comparison is recorded as a secondary observation, and negative results are retained." Each of those is a section below.

## 2. Purpose check

The hypothesis predicts that, without new independent evidence, confidence may rise through recirculation because derived claims are treated as independent support. The protocol's instrument for that is excess over reference: P(A) minus the normative P(A) from the actual roots, defined at every event. The Gate 3A question is where (which agent, which position) deviation from the single-root reference occurs under four structures, and whether the origin A corrects it. The audit's core object is therefore the per-event excess, by agent, by position in the cycle, by condition, by arm, paired by world.

What the plan forbids, and the tool therefore cannot do: pool Set 001 with Set 002; compare any Gate 3A arm against the 36 historical ring runs as a primary outcome; introduce a significance test, a threshold or a selected event after inspection; use the probe (off in Gate 3A; FIS fields are null and are reported as null); relabel a trajectory observation as secondary.

## 3. Inputs the tool reads

Per world and attempt: `events.jsonl`, `summary.csv`, and the stage's corpus integrity audit record, which names the complete attempt and the raw-file hashes. The tool refuses to run unless that record exists, reads PASS, and the files it opens hash to what the record says. No field is re-measured: every quantity below is an archived metric or arithmetic over archived metrics, and where a function is needed (the reference probability for EXP-002 runs, the provenance marks) the frozen runtime's own function is imported.

## 4. Operational definitions (confirmed)

### 4.1 Reference, deviation, direction (D1)

Gate 3A worlds are single-root, so `reference_p_a` is .70 when E1 observed A and .30 when E1 observed B. Raw `p_a_excess_over_reference` is on the P(A) scale, so its sign does not say "more certain" in B-observed worlds. The audit derives, per event:

- `p_observed = p_a` if E1 observed A, else `1 − p_a`;
- `reference_observed = max(reference_p_a, 1 − reference_p_a)` (.70 for every Gate 3A event);
- **`certainty_excess = p_observed − reference_observed`**.

With tolerance τ = 1e-6 (the rounding scale of the archived metrics):

| Term | Rule |
|---|---|
| at reference | \|certainty_excess\| ≤ τ |
| deviation | \|certainty_excess\| > τ |
| discount | certainty_excess < −τ |
| inflation (above reference) | certainty_excess > +τ |
| magnitude | \|certainty_excess\| |

Raw excess is kept beside `certainty_excess` in every row; the directional terms are defined on `certainty_excess` only.

### 4.2 Positions and firings

Firing order is fixed by the topology and recorded as `visible_message_id` (M01 seed, M02…M13). Positions are identified by `sender` and `receivers`:

| Arm | Post-seed A firings (hops since A's previous firing) | B firings | C firings |
|---|---|---|---|
| solo (12 rounds) | M02…M13, 1 hop each | none | none |
| dyad (6 rounds) | M03, M05, …, M13, 2 hops each | M02, M04, …, M12 (B→A) | none |
| ring (4 rounds) | M04, M07, M10, M13, 3 hops each | M02, M05, M08, M11 (B→C) | M03, M06, M09, M12 (C→A) |
| bounce (3 rounds) | M05, M09, M13, 4 hops each | outward B→C: M02, M06, M10; return B→A: M04, M08, M12 | M03, M07, M11 (C→B) |

"Echoes of 1, 2, 3 and 4 hops" in the plan maps onto solo, dyad, ring, bounce. Hops are computed from the firing sequence, never from the data.

### 4.3 The five focal comparisons (D2 for table 4)

Each per condition (FREE and LINEAGE separately; MACRO as its stopping boundary, 4.5), per world paired by seed across arms, per set.

1. **B in dyad vs ring vs bounce.** Per world: B's discount rate, inflation rate, mean magnitude, and the sequence of certainty_excess per B firing, in each arm.
2. **C in ring vs bounce.** The same for C.
3. **Bounce B outward (B→C) vs return (B→A).** Per world, per cycle: certainty_excess at both legs, their difference, and whether the return magnitude is smaller, equal or larger.
4. **A at every post-seed firing, all four arms.** Per A firing: certainty_excess, `at reference` flag, hops, and whether the inbound message carried the `agent_as_source` mark. Derived: **restoration rate** = A firings at reference / A post-seed firings; **sustained deviation** = two consecutive A firings both deviating with the same sign (the plan's E4 contradiction condition).
5. **Solo A at every step.** Per firing: certainty_excess and flag; derived: any deviation at all.

### 4.4 Per-world primary table (the EXP-002 family)

Per world, per condition: final answer, accuracy, final confidence, final P(A), final reference, final raw excess, final certainty_excess, Brier, root count, max depth, `p_a_delta_without_new_evidence` trajectory, max redundant root exposures, erosion trajectory, `agent_as_source` events and first such event, per-agent final P(A) and per-agent max/min excess from `summary.csv`. Cell (truth/E1) on every row; cell-conditional sub-tables follow; mean P(A) is never averaged across cells; certainty_excess is the cross-cell quantity.

### 4.5 MACRO

Reported as a stopping boundary, not an independent trajectory: `macro_stop_triggered`, `stop_reason`, the stopping event, the LINEAGE value at the same event and at LINEAGE's end, and whether every post-seed MACRO response was a reused LINEAGE response.

### 4.6 Pre-registered expectations (D3)

| Id | Mechanical rule |
|---|---|
| E1 | contradicted if ring A has any discount event (FREE or LINEAGE), or ring FREE has any deviation event, or ring LINEAGE has zero discount events at B and C combined |
| E2 | contradicted if bounce C's discount rate < ring C's (LINEAGE), or bounce B's mean return magnitude ≥ mean outward magnitude (LINEAGE); FREE printed beside |
| E3 | contradicted if dyad B's discount rate ≥ ring B's (LINEAGE); FREE printed beside |
| E4 | contradicted if any arm has a sustained deviation at A in either condition, or any arm's A restoration rate is below the ring's in the same condition |
| E5 | contradicted if solo has any deviation event in either condition |
| E6 | assessed in the synthesis across the two stages; each stage audit prints its own ordering of the four arms by LINEAGE discount rate |

Rates compared as plain numbers; ties count as "not below". A verdict restates the plan's own column; it is not an interpretation.

### 4.7 Secondary observation

`ring_control_set_001` against the 36 archived EXP-002 ring runs: the same per-position summary computed on both corpora by the same code, written to a separate file labelled secondary, with the factor-ledger difference printed. Sixteen of the historical runs are repeated executions of one world (seed 42); the summary is shown pooled and with the twenty Gate 2B worlds alone. The truth and E1 of each historical world are reproduced from its seed by the frozen EXP-003 generator and checked against the archived truth. Not placed in any primary table; no Gate 3A value is adjusted by it.

## 5. Outputs (D4)

Under `experiments/EXP_003/audits/gate_3a/`:

- `EXP_003_GATE_3A_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1.{json,md}`
- `EXP_003_GATE_3A_SET_002_PRIMARY_OUTCOME_AUDIT_v0.1.{json,md}`
- `EXP_003_GATE_3A_HISTORICAL_RING_OBSERVATION_v0.1.{json,md}` (secondary)
- then, separately: `EXP_003_GATE_3A_SYNTHESIS_v0.1.{json,md}` (E6, separate reporting, negative results retained), followed by the tag.

Each JSON carries the plan hash, anchors, the corpus audit record it depends on, HEAD at audit time, this specification's version, and the per-event rows it used, so every table is re-derivable.

## 6. Order of operations

1. This specification, the tool and its tests are committed together (pre-registration commit). The tests exercise the tool on deterministic-stub preflight data only; the stubs reproduce the shapes and never bear on the hypothesis.
2. One invocation per stage on the archive, then the historical observation; outputs committed. The first time any Gate 3A number is seen by anyone is in those files.
3. Synthesis, then checkpoint tag `exp-003-gate3a-closed-v0.1`.
4. Anything learned goes to `research/observations/`; any design change goes to a separately versioned later gate, never back into Gate 3A.
