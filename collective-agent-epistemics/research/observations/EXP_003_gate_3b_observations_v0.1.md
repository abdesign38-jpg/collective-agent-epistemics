# EXP-003 Gate 3B Observations v0.1

**Status:** OBSERVATION RECORD. Written after both stage primary-outcome audits and the synthesis were committed (`62761dd`, `cd2d05d`), by rules committed before any Gate 3B value existed (`bcb84d3`, `e58b253`). Every number below is copied from those committed files (`experiments/EXP_003/audits/gate_3b/`). This record relates the findings to the hypothesis; it changes nothing in Gate 3B and proposes nothing for Gate 3B. Anything it motivates belongs to a separately versioned later gate.

## What Gate 3B asked

The first fan-in. In the diamond, A sends to B and C, both send to D in the same round, and D sends back to A, so D receives two messages descended from one root at once. On 12 worlds per stage (Arm 1, probe on), does D report more certainty than the single root supports, and does it report more than one distinct source? Does the LINEAGE envelope change that without suppressing evidence that is really independent (Arm 2, a second sensor read by C, 16 worlds per stage, stratified into agreeing and conflicting halves)? The probe (`reported_distinct_source_count`) was on for the first time, with a probe-off arm on the first four Arm 1 worlds (Arm 4) and a probe-on solo control (Arm 3). Same model (`gpt-5.6-sol`, effort `medium`), paired execution, depth 12, 33 calls per diamond world and 25 per solo world. Set 002 (12 + 16 new worlds) ran after Set 001 passed its corpus audit and before any Set 001 outcome was read. 72 of 72 worlds archived (2280 calls); three technical failure records preserved in Set 001, each world completed on one retry under the frozen rule; zero in Set 002.

## Pre-registered expectations, both stages

| Id | Expectation (short) | Set 001 | Set 002 |
|---|---|---|---|
| E1 | FREE D shows positive certainty excess in at least some Arm 1 worlds | consistent | consistent |
| E2 | LINEAGE D excess not greater than FREE D excess in the same world | consistent | consistent |
| E3 | positive excess at D co-occurs with FIS > 0 | contradicted | contradicted |
| E4 | inbound agent-as-source wording precedes positive excess more often than clean wording | contradicted | contradicted |
| E5 | Arm 2 D approaches the two-root reference under both conditions (agreeing stratum) | consistent | consistent |
| E6 | Arm 4 excess at D within .02 of Arm 1 in the same worlds | contradicted | not assessable (no probe-off arm in Set 002, by plan) |
| E7 | Set 002 reproduces the Set 001 direction in every matrix cell | no reversed cell among six: consistent |

Every single-stage expectation that could be assessed in both stages received the same verdict in both. The six matrix cells kept their direction.

## Descriptive observations

**[DESCRIPTIVE OBSERVATION] The fan-in did not double count.** Under FREE, D sat at the single-root reference in 45 of 48 and 43 of 48 firings (Set 001 / Set 002); its stage means of certainty excess were +.003 and +.008. E1 reads consistent because 2 and 4 of the 12 worlds contained at least one FREE D firing above .01, which is the letter of the pre-registered rule. The plan's own fallback sentence, that fan-in alone with one root does not produce double counting in this model at this depth, is the closer description of the data. The effect is present, near zero in size, and intermittent.

**[DESCRIPTIVE OBSERVATION] D's source count was correct at every firing.** FIS at D was 0 in all 192 Arm 1 D firings across both stages and both conditions, and 0 in all 32 probe-off D firings where it was not asked. The few FREE D excess events (3 and 5) had the correct source count. This is why E3 is contradicted: excess without FIS was the only non-concordant class, and the concordant class was empty. Whatever moved D's probability in those few firings, it was not a miscount of sources.

**[DESCRIPTIVE OBSERVATION] Under LINEAGE, D discounted.** 9 discounts against 2 inflations in Set 001, 7 against 3 in Set 002, stage means −.011 and −.006. E2 is consistent in the stronger sense: the envelope moved the fan-in bee in the same direction it moved the distal agents of Gate 3A. In a single-root world this caution costs nothing.

**[DESCRIPTIVE OBSERVATION] Origin inflation appeared again, in a fourth topology, only under LINEAGE, and now with the probe showing the miscount.** A, receiving D's message (its own lineage after three hops) while re-reading E1, inflated at 8 of 48 LINEAGE firings in Set 001 and 7 of 48 in Set 002, and at 5 of 16 in the probe-off arm; 0 of 48, 0 of 48 and 0 of 16 under FREE; 0 discounts anywhere at A. In the probe-on arms, FIS > 0 at A occurred at exactly 8 and 7 firings: the same firings. The origin reported two distinct sources where it had one, in precisely the moments it rose above the reference. The Gate 3A pattern (ring 8 and 8 of 48, bounce 3 and 2 of 36, dyad 0, solo 0) is reproduced in shape and rate by a structure that did not exist in Gate 3A.

**[DESCRIPTIVE OBSERVATION] Every origin inflation followed an inbound message that did not name the sensor.** Secondary table (pre-registered as descriptive, no verdict): A's LINEAGE firings whose inbound message carried `source_named = false` inflated at 8 of 26 (Set 001), 7 of 22 (Set 002) and 5 of 10 (probe-off); those whose inbound message named the sensor inflated at 0 of 22, 0 of 26 and 0 of 6. Together with the 21 of 21 events of Gate 3A observations v0.2, that is 41 of 41 origin inflations after an unnamed sensor and 0 of 108 after a named one, across four topologies, two gates and two stages each. The pattern is descriptive and strong; it is not a causal finding, and it is not yet a mechanism.

**[DESCRIPTIVE OBSERVATION] The envelope has a cost when a second root is real.** Agreeing stratum, D with two roots: under FREE the modal class was the two-root reference (22 and 23 of 32 firings within .01 of .845), so E5 is consistent as pre-registered. Under LINEAGE the stage means were −.042 and −.043 relative to the two-root reference (21 and 20 discounts of 32), and in Set 002 the modal class was "other" (13 of 32, between the single-root and two-root references) rather than two-root (12). The LINEAGE envelope partly discounted evidence that was independent. E5 does not read contradicted because the contradiction classes were "single root" and "over", and neither was modal. This is the first observed cost of lineage tagging in EXP-003.

**[DESCRIPTIVE OBSERVATION] In conflict, LINEAGE moved the origin toward its own sensor.** Conflicting stratum (two-root reference .50, no direction label): D stayed near even under both conditions (mean departure toward E1 −.049 and −.018 under FREE, −.010 and −.008 under LINEAGE). A, after D's message, was near even under FREE (−.015, +.017) and leaned toward its own sensor under LINEAGE (+.135, +.120), with FIS > 0 at 10 and 15 of 32 of those firings. Not a pre-registered expectation; recorded without a verdict.

**[DESCRIPTIVE OBSERVATION] The probe is reactive.** Arm 4 (probe off) against Arm 1 (probe on) on the same four worlds: 4 of 8 comparisons differed in mean D certainty excess by more than .02 (gaps .025 to .050), in both directions. E6 is contradicted in Set 001 and could not be assessed in Set 002, which has no probe-off arm by plan. Asking an agent to count its sources changed what it reported by a few points. Gate 3A (probe off) and Gate 3B (probe on) are comparable only through Arm 4. Four worlds is a small basis; the verdict stands as written.

**[DESCRIPTIVE OBSERVATION] The agent-as-source wording did not precede D's excess.** E4 contradicted in both stages: FREE D excess rate .000 after marked inbound (16 and 9 firings) against .063 and .128 after clean inbound; LINEAGE .000 and .200 against .048 and .047. In three of the four cells the marked rate was below the clean rate; the one exception (Set 002 LINEAGE) rests on one event in five marked firings. As in Gate 3A, the mark explains little here.

**[NO EFFECT OBSERVED] The solo control is clean with the probe on.** 288 post-seed firings across FREE and LINEAGE in Set 001 (the only stage with a solo arm, by plan), every one at the reference, FIS 0 throughout. The probe does not by itself produce deviation or miscounting in an agent alone with its evidence.

**[NO EFFECT OBSERVED] Final answers followed the sensors; MACRO stopped after one cycle.** In every single-root world×condition the final answer equalled E1's reading (accuracy 88 of 93 aligned and 5 of 39 misleading records in Set 001; 41 of 42 and 3 of 42 in Set 002, counting all arms). Final answers differed from E1 only in conflicting dual-root worlds (10 and 4 records), where a second reading exists. MACRO stopped after one cycle in all 72 worlds and reused every paired response.

**[BOUNDARY CONDITION] Three transient provider failures in Set 001**, on three unrelated seeds across three arms, each world completed on one retry as `attempt_002` with the failed attempt's record preserved; zero in Set 002. The failure records name only the adapter's wrapper ("OpenAI Responses request failed"); the underlying error class was not recorded by the orchestrator at the time. A tooling change recording the cause chain was prepared and not applied during the gate.

**[BOUNDARY CONDITION] Reproducibility across Python versions.** Re-running both stage audits on a clean checkout on a different Python version reproduced every count and verdict; a few event-weighted means differed by one unit in the sixth decimal (floating-point summation order). The synthesis, which copies values, reproduced byte for byte. Means are reported to six decimals; differences at that digit are not findings.

**[FALSIFICATION EVIDENCE] against the strong form of the hypothesis, again.** Recursive communication without new evidence did not raise confidence through the network. Under FREE, 192 fan-in firings and 96 origin firings sat at calibration almost without exception. Under LINEAGE the dominant movement at every non-origin position was downward. The one upward movement is the origin's, intermittent, small (+.02 to +.145), and self-correcting, as in Gate 3A.

**[FALSIFICATION EVIDENCE] against "fan-in is where double counting happens".** The pre-registered reason for Gate 3B was that two copies of one dance arriving together should be read as corroboration. They were not: D counted one source in every firing and its probability sat at the reference. The double counting that exists in this experiment happens at the origin, under the envelope, when the origin's own evidence returns under a name it does not recognise.

**[OPEN QUESTION] Is the identity gap the mechanism?** The envelope names the root "E1"; the origin knows its reading as "sensor_1"; every inflation followed a message that did not use the sensor's name, and in every one the origin reported two sources. The reading consistent with all of this is that two descriptions of one fact are being filed as two facts. Gate 3B cannot establish it. Gate 3C, where the origin no longer re-reads its sensor, is the pre-registered structure that can: if the inflation vanishes when the origin sees only the envelope and not the sensor, the two-names reading is supported; if it persists, the mechanism is elsewhere.

**[OPEN QUESTION] What does lineage tagging cost?** Gate 3B gives the first measurement: about four points of discount against a real second root in the agreeing stratum, and a lean toward the origin's own evidence in conflict. Neither was pre-registered as an expectation; both are candidates for one in a later gate.

**[OPEN QUESTION] Generality.** One model, one effort setting, one prompt version, twelve worlds per stage, four probe-off worlds. The EXP-002 ring under the same model name showed none of the origin inflation. Nothing here is evidence about other models until the same frozen plans are run on one.

## What this does not say

No significance test was run and none is implied by any count above. No causal claim is made. Set 001 and Set 002 were never pooled; the agreeing and conflicting strata were never pooled; every number above is given per stage and per stratum. The pre-registered expectations that were contradicted stand contradicted. E1 is reported as consistent because that is what its rule returns; the size of the effect is reported beside it so that the verdict is not read as more than it is.

## Gate status

Gate 3B data collection: COMPLETE (72 of 72 worlds, both stages). Corpus integrity: VERIFIED (both stages, drift none). Analysis rules: PRE-REGISTERED (`bcb84d3`, `e58b253`). Primary-outcome audits: COMPLETE (both stages). Synthesis: COMPLETE (E7 consistent). Closure tag target: `exp-003-gate3b-closed-v0.1`.
