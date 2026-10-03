# EXP-003 Gate 3A Observations v0.1

**Status:** OBSERVATION RECORD. Written after both stage audits and the historical observation were committed. It accompanies the Gate 3A synthesis in the closure commit. Every number below is copied from those committed files (`experiments/EXP_003/audits/gate_3a/`). This record relates the findings to the hypothesis; it changes nothing in Gate 3A and proposes nothing for Gate 3A. Anything it motivates belongs to a separately versioned later gate.

## What Gate 3A asked

On the same 24 worlds (12 per stage), the same model, the same day, the same 25 calls and depth 12 per world: how do four communication structures differ in where deviation from the single-root reference occurs, and whether the origin corrects it? Solo (no interaction), dyad (direct contact with the source), ring (a loop where everyone reaches the source), bounce (a far agent that never does).

## Pre-registered expectations, both stages

| Id | Expectation (short) | Set 001 | Set 002 |
|---|---|---|---|
| E1 | contemporary ring reproduces the historical pattern (LINEAGE discounts at B and C, none at A, FREE at reference) | contradicted | contradicted |
| E2 | bounce C discounts at least as often as ring C; bounce B's return firing carries smaller excess than its outward firing | contradicted | contradicted |
| E3 | dyad B discounts less per event than ring B | consistent | consistent |
| E4 | A returns to the reference after each echo in every topology, at a rate not below the ring's; no sustained deviation | contradicted | consistent |
| E5 | solo shows no excess in either direction | consistent | consistent |
| E6 | Set 002 reproduces Set 001's ordering of discount rates across the four arms | ring > bounce > dyad > solo in both stages: consistent |

Three of five single-stage expectations agree across stages; E4 differs by exactly one world (below). The arm ordering replicated exactly.

## Descriptive observations

**[DESCRIPTIVE OBSERVATION] The null control is clean.** Solo A, re-reading its own evidence and its own previous message twelve times, stayed at the reference at every one of 576 post-seed firings (288 per stage, FREE and LINEAGE). Whatever happens in the other arms is not something an agent does to itself.

**[DESCRIPTIVE OBSERVATION] Discounting scales with distance from the source, and only under LINEAGE.** LINEAGE discount rate over all post-seed events: ring .174 / .215, bounce .097 / .104, dyad .021 / .014, solo 0 / 0 (Set 001 / Set 002). Under FREE the same arms are nearly all at reference (ring 6 and 5 deviating events of 144; dyad 2 and 0 of 144; bounce 16 and 10 of 144). Discounting was concentrated under LINEAGE and increased with structural distance from the source, in both stages.

**[DESCRIPTIVE OBSERVATION] In the bounce, B discounts when it speaks back toward the source, not when it relays outward.** Bounce B outward firings (B→C): 0 and 1 discounts of 36 per stage. Return firings (B→A): 8 and 8 discounts of 36. This is the part of E2 that was contradicted: the return leg carries the larger excess magnitude, not the smaller. The pre-registered direction was wrong, in the same way in both stages.

**[DESCRIPTIVE OBSERVATION] The far agent that never meets the source discounts less than the far agent that does.** Bounce C (hears only B) discounted .167 of LINEAGE events in both stages; ring C (hears B, then reports to A) discounted .354 and .458. The other half of E2 was also contradicted, in the same direction, in both stages.

**[DESCRIPTIVE OBSERVATION] Inflation appears at the origin, only where the origin's inbound message comes from a distal agent, and only under LINEAGE.** Ring A inflated at 8 of 48 post-seed firings in each stage (magnitudes .02 to .145); bounce A at 3 and 2 of 36; dyad A at 0 of 72 in both; solo 0. Under FREE, A never inflated in any arm. These are the events where A re-reads E1 while receiving a descendant of E1 (redundant root exposure 1), and A's probability rose above what E1 alone supports. This is the numerical signature the protocol defines for counting shared evidence more than once. It did not occur in the historical EXP-002 ring (0 of 144 LINEAGE A firings).

**[DESCRIPTIVE OBSERVATION] Origin inflation is mostly transient.** In 23 of the 24 ring worlds no two consecutive A firings deviated in the same direction. One Set 001 world (seed 652310877) sustained inflation over three consecutive A firings (+.12, +.06, +.05); that single world is why E4 reads contradicted in Set 001 and consistent in Set 002. Ring A restoration rate was .833 in both stages.

**[DESCRIPTIVE OBSERVATION] The agent-as-source mark is present at some but not most inflation events.** Of the 16 ring A inflation events, 4 followed an inbound message that presented an agent as the owner of the evidence (1 in Set 001, 3 in Set 002); 12 did not. The wording mark and the numerical inflation co-occur sometimes; neither explains the other here.

**[NO EFFECT OBSERVED] Final answers never moved.** In all 288 world×condition records the final answer equalled the sensor's reading; accuracy was 100% in aligned cells and 0% in misleading cells in every arm and condition, as the single sensor dictates. Final confidence was .70 in 277 of 288 records; the 11 others (.72 to .84) are all ring or bounce A under LINEAGE at the last firing. No condition changed what the network concluded; the differences are entirely in how sure it said it was along the way.

**[NO EFFECT OBSERVED] MACRO stopped after one cycle in all 96 worlds**, reusing the paired LINEAGE responses in every case. The stopping rule fired exactly as designed and has no trajectory of its own.

**[BOUNDARY CONDITION] Cells were unbalanced.** Set 001 drew 7 B/B, 2 B/A, 2 A/A, 1 A/B; Set 002 drew 8 A/A, 2 A/B, 1 B/A, 1 B/B. Unfiltered worlds were the pre-registered choice; the directional quantity (certainty excess) is comparable across cells, mean P(A) is not and was not used.

**[FALSIFICATION EVIDENCE] against the strong form of the hypothesis.** Confidence did not systematically increase through recirculation. The dominant movement under LINEAGE was downward (discounting), and the one upward movement (origin inflation) was small, intermittent and self-correcting in 23 of 24 worlds. Within one root and depth 12, the network did not inflate itself.

**[FALSIFICATION EVIDENCE] against the null hypothesis as stated.** The null says interaction adds no mechanism beyond individual-agent error. Deviation was absent in the solo recursive control and appeared only in the multi-agent structures, with rates varying by topology (where B sat, whether C could reach A). What appeared was mostly caution, with occasional origin inflation.

**[OPEN QUESTION] Why does the origin inflate under LINEAGE but not under FREE?** Under FREE, A sees C's message as text and stays at .70. Under LINEAGE, A sees the same text plus an envelope stating the roots {E1} and depth, and sometimes rises. One possible reading is that the envelope's explicit root list is being read as corroboration rather than as a duplicate; another is that the depth or hop count is doing work. Gate 3A was not designed to separate these; Gate 3B (diamond, two relays of one root converging) and Gate 3C (re-grounding removed) are the pre-registered next structures.

**[OPEN QUESTION] Model drift.** The contemporary ring differs from the historical one at A (8/48 LINEAGE inflations vs 0/144) and at C (.354 vs .174 LINEAGE discount rate), under the same prompts and model name. The factor ledger shows only experiment, gate, set, run class and version labels differing. This is recorded as an observation and used for nothing.

## What this does not say

No significance test was run and none is implied by any count above. No causal claim is made. Set 001 and Set 002 were never pooled; every number above is given per stage. The pre-registered expectations that were contradicted stand contradicted; the plan's own falsification list named "deviation at B rather than C", "A sustaining deviation" and "dyad discounting as much as the ring" as acceptable outcomes that must not alter execution, and they did not.

## Gate status

Gate 3A data collection: COMPLETE. Corpus integrity: VERIFIED (both stages). Primary-outcome audits: COMPLETE (both stages). Historical comparison: RECORDED as secondary. Synthesis: COMPLETE. Closure tag target: `exp-003-gate3a-closed-v0.1`.
