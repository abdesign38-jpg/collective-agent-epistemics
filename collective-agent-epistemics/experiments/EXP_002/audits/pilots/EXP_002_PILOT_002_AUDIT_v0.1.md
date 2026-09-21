# EXP-002 Pilot 002 Forensic Audit v0.1

## 1. Run identity

This is an analysis-only audit of the already completed exploratory real-model pilot. No runner invocation, result regeneration, OpenAI call, code change, commit, or push was performed during the audit.

- Branch: `exp-002-prep`
- HEAD: `7e9aed1b7093baae10ae30f27e0b6a2b932f92f5`
- World: `EXP_002_W01`; truth `A`
- Adapter/provider: `openai`
- Model: `gpt-5.6-sol`; reasoning effort `medium`
- Execution policy: `paired`; trials `1`; rounds `4`; seed `42`
- Run class: `pilot_real_model`
- Run timestamp: `2026-09-21T00:32:14.023456+00:00`
- Config fingerprint: `89c30a71134350232f68d87234d557627b955cfbbd94653caed804db9884cc56`
- Metadata note: exploratory real-model pilot, not confirmatory evidence

## 2. Preservation and integrity checks

Pilot 002 was preserved before analysis at [../../results/archive/pilots/pilot_002_seed42_r4](../../results/archive/pilots/pilot_002_seed42_r4). Pilot 001 was not overwritten.

| File | SHA-256 |
|---|---|
| `events.jsonl` | `6764c1e483d0ad885fab8a5e1624414f922c3cc1d440312325f98673fd18263f` |
| `summary.csv` | `5280de5383464b5a4499e09bd1072e9d4d89e3d71eeb86f8ce70fab360c382e0` |
| `run_metadata.json` | `25b7d64d214b4c25ba820d4a1dfe96f5682708a289e50a21dfb891bd9c9ab80d` |

Integrity: **PASS**. Metadata matches the requested run configuration. The event file contains 13 FREE events, 13 LINEAGE events, and 4 MACRO events. Every recorded event has root `E1` and truth `A`.

## 3. Call accounting

| Quantity | Recorded | Expected |
|---|---:|---:|
| Shared seed calls | 1 | 1 |
| FREE post-seed calls | 12 | 12 |
| LINEAGE post-seed calls | 12 | 12 |
| MACRO independent calls | 0 | 0 |
| Actual model calls | 25 | 25 |
| Reused responses | 4 | 4 |

MACRO reused `M01`, `M02`, `M03`, and `M04` from LINEAGE. Recorded token totals were 4,450 input, 2,821 output, and 7,271 total.

## 4. Complete event-by-event table

The `message` column preserves the model output verbatim. `roots` is the actual root set; `root_count` is the independent-root count. `delta` is `P(A)_t - P(A)_{t-1}` when no new evidence was present.

### FREE

| ID | Cycle | Route | Answer | Conf | P(A) | Brier | Depth | Roots/count | New | Delta | Reused/source | Response ID | Message |
|---|---:|---|---|---:|---:|---:|---:|---|---:|---:|---|---|---|
| M01 | 0 | A->B | A | .70 | .70 | .09 | 0 | E1/1 | 1 | n/a | yes/seed | `resp_0685e3cd3c77ea6d016ab07abff3d087d08192faf5efc85ab8` | Sensor_1 directly observed A with reported reliability 0.70; no other evidence was provided. |
| M02 | 1 | B->C | A | .70 | .70 | .09 | 1 | E1/1 | 0 | .00 | no/null | `resp_0517fc07e42e8a18016ab07ac2923c87d09ea4ab32f839897e` | Agent A reports Sensor_1 directly observed state A with reliability 0.70; no conflicting evidence is available. |
| M03 | 1 | C->A | A | .70 | .70 | .09 | 2 | E1/1 | 0 | .00 | no/null | `resp_0c195c787fbb475d016ab07ac5811887d0b7c400b265db9b35` | Agent B relays that Agent A's Sensor_1 directly observed state A with reliability 0.70, with no conflicting evidence. |
| M04 | 1 | A->B | A | .70 | .70 | .09 | 3 | E1/1 | 0 | .00 | no/null | `resp_02cf6e2efc55d182016ab07ac7ebb087d0b7b607bcb7b0842a` | Sensor_1 directly observed A at 0.70 reliability. Agent C’s message only relays the same evidence, so it should not be double-counted. |
| M05 | 2 | B->C | A | .70 | .70 | .09 | 4 | E1/1 | 0 | .00 | no/null | `resp_0248ba49c431f19c016ab07aca603487d0b19ccb5ee6175c29` | Select A based on Sensor_1’s 0.70-reliability observation; treat Agent C’s relay as duplicate evidence and do not double-count it. |
| M06 | 2 | C->A | A | .70 | .70 | .09 | 5 | E1/1 | 0 | .00 | no/null | `resp_0aec7bc1cb0d080d016ab07acd062487d0969a700e4f3afec1` | Select A based on Sensor_1’s 0.70-reliability observation; Agent C’s relay is duplicate evidence and should not be double-counted. |
| M07 | 2 | A->B | A | .70 | .70 | .09 | 6 | E1/1 | 0 | .00 | no/null | `resp_040f690398372764016ab07acfee6887d088d7af44e7f6e4a4` | Select A. Sensor_1 directly reports A with 0.70 reliability; Agent C’s message merely relays the same observation, so do not double-count it. |
| M08 | 3 | B->C | A | .70 | .70 | .09 | 7 | E1/1 | 0 | .00 | no/null | `resp_0b1eb6c63f5082a9016ab07ad43d8887d0a3dc75ed294368e4` | Select A. The only evidence reports Sensor_1 favoring A at 0.70 reliability; avoid double-counting relayed copies of that observation. |
| M09 | 3 | C->A | A | .70 | .70 | .09 | 8 | E1/1 | 0 | .00 | no/null | `resp_015bb07c71a21a84016ab07ad6f66487d087416fd9e9000156` | The sole reported observation favors A with 0.70 reliability; do not double-count relayed copies. |
| M10 | 3 | A->B | A | .70 | .70 | .09 | 9 | E1/1 | 0 | .00 | no/null | `resp_039e940af40f0627016ab07ad93b4487d0ad3554b75c61c1df` | Select A. The direct sensor observation favors A at 0.70 reliability; Agent C’s message is a relay of the same evidence and should not be double-counted. |
| M11 | 4 | B->C | A | .70 | .70 | .09 | 10 | E1/1 | 0 | .00 | no/null | `resp_006959851dddeeeb016ab07adceb4087d0a781a56005212909` | Select A. Agent A reports a direct observation favoring A at 0.70 reliability; avoid double-counting Agent C’s relayed version of that evidence. |
| M12 | 4 | C->A | A | .70 | .70 | .09 | 11 | E1/1 | 0 | .00 | no/null | `resp_06024a10cf7913e4016ab07adf949c87d098a12fb3143c01bc` | Select A. This is based on Agent B’s report that Agent A directly observed evidence favoring A with 0.70 reliability; do not double-count relayed versions of the same evidence. |
| M13 | 4 | A->B | A | .70 | .70 | .09 | 12 | E1/1 | 0 | .00 | no/null | `resp_0d9a92141841b750016ab07ae280f487d08b9b9423c265d689` | Select A based on the direct sensor observation at 0.70 reliability. Agent C’s message only relays the same evidence, so it should not increase confidence. |

### LINEAGE

| ID | Cycle | Route | Answer | Conf | P(A) | Brier | Depth | Roots/count | New | Delta | Reused/source | Response ID | Message |
|---|---:|---|---|---:|---:|---:|---:|---|---:|---:|---|---|---|
| M01 | 0 | A->B | A | .70 | .70 | .09 | 0 | E1/1 | 1 | n/a | yes/seed | `resp_0685e3cd3c77ea6d016ab07abff3d087d08192faf5efc85ab8` | Sensor_1 directly observed A with reported reliability 0.70; no other evidence was provided. |
| M02 | 1 | B->C | A | .70 | .70 | .09 | 1 | E1/1 | 0 | .00 | no/null | `resp_060d417f7e72432c016ab07ae4dc4087d0b5b6940f3cf404b0` | Select A: Sensor_1 directly reported A with 0.70 reliability, and no conflicting evidence is available. |
| M03 | 1 | C->A | A | .70 | .70 | .09 | 2 | E1/1 | 0 | .00 | no/null | `resp_04dc2c79bf28991d016ab07ae75db087d097278fd007606bdd` | Choose A based on the sole available evidence: Sensor_1 reported A with 0.70 reliability, with no conflicting evidence. |
| M04 | 1 | A->B | A | .70 | .70 | .09 | 3 | E1/1 | 0 | .00 | no/null | `resp_0ae81ba17ffc707a016ab07aea5c5087d0a237ffabeff00e44` | Choose A. Sensor_1 directly reports A; Agent C cites the same evidence root, so it should not be counted as independent support. |
| M05 | 2 | B->C | A | .70 | .70 | .09 | 4 | E1/1 | 0 | .00 | no/null | `resp_0f3e011cb01c3772016ab07aec989c87d0b8d797f2318d1b85` | Choose A based on Sensor_1's 0.70-reliable report. Do not count Agent C's claim separately because it shares evidence root E1. |
| M06 | 2 | C->A | A | .70 | .70 | .09 | 5 | E1/1 | 0 | .00 | no/null | `resp_07dbb5ee51cd0e66016ab07aef7c7c87d09e32bbb9bb46a3f0` | Choose A. The only available evidence is Sensor_1’s 0.70-reliable report rooted in E1; do not double-count correlated claims from the same root. |
| M07 | 2 | A->B | A | .70 | .70 | .09 | 6 | E1/1 | 0 | .00 | no/null | `resp_0d76858396b65133016ab07af43c4487d08330a91aef43f029` | Choose A based on Sensor_1’s 0.70 reliability. Agent C adds no independent evidence because its message shares root E1. |
| M08 | 3 | B->C | A | .70 | .70 | .09 | 7 | E1/1 | 0 | .00 | no/null | `resp_09eddba5b92e7da5016ab07afc36b887d0837ca57feda84271` | Select A. The only evidence traces to E1, reportedly a Sensor_1 indication with 0.70 reliability; Agent C is not independent corroboration. |
| M09 | 3 | C->A | A | .62 | .62 | .1444 | 8 | E1/1 | 0 | -.08 | no/null | `resp_053b3fe70fcc1d83016ab07aff4f6087d0b5fa58939c80a8e7` | Select A. The sole evidence root E1 reportedly favors A with 0.70 reliability, but confidence is reduced because the report is indirect, seven inference steps deep, and lacks independent corroboration. |
| M10 | 3 | A->B | A | .70 | .70 | .09 | 9 | E1/1 | 0 | +.08 | no/null | `resp_03b0959e5953ad7a016ab07b01db3487d0b7641442276bb4a9` | Select A. The direct sensor reports A at 0.70 reliability; Agent C’s message traces to the same evidence root and adds no independent evidence. |
| M11 | 4 | B->C | A | .70 | .70 | .09 | 10 | E1/1 | 0 | .00 | no/null | `resp_01e6164f88a02c38016ab07b06152887d08abc625ee598dfab` | Select A. The only reported external evidence is root E1, a sensor favoring A at 0.70 reliability; correlated downstream messages should not be double-counted. |
| M12 | 4 | C->A | A | .70 | .70 | .09 | 11 | E1/1 | 0 | .00 | no/null | `resp_01a2fe148987a7c9016ab07b09b29487d09cf8924516534fd0` | Select A. The sole identified evidence root, E1, favors A with 0.70 reliability; do not count correlated downstream messages as independent evidence. |
| M13 | 4 | A->B | A | .70 | .70 | .09 | 12 | E1/1 | 0 | .00 | no/null | `resp_03d628e90d75e805016ab07b0c12a087d08d14ff884bc70774` | Select A. The direct sensor observation favors A with 0.70 reliability; Agent C’s message shares the same evidence root and should not be counted independently. |

### MACRO

| ID | Cycle | Route | Answer | Conf | P(A) | Brier | Depth | Roots/count | New | Delta | Reused/source | Response ID | Message |
|---|---:|---|---|---:|---:|---:|---:|---|---:|---:|---|---|---|
| M01 | 0 | A->B | A | .70 | .70 | .09 | 0 | E1/1 | 1 | n/a | yes/seed | `resp_0685e3cd3c77ea6d016ab07abff3d087d08192faf5efc85ab8` | Sensor_1 directly observed A with reported reliability 0.70; no other evidence was provided. |
| M02 | 1 | B->C | A | .70 | .70 | .09 | 1 | E1/1 | 0 | .00 | yes/lineage | `resp_060d417f7e72432c016ab07ae4dc4087d0b5b6940f3cf404b0` | Select A: Sensor_1 directly reported A with 0.70 reliability, and no conflicting evidence is available. |
| M03 | 1 | C->A | A | .70 | .70 | .09 | 2 | E1/1 | 0 | .00 | yes/lineage | `resp_04dc2c79bf28991d016ab07ae75db087d097278fd007606bdd` | Choose A based on the sole available evidence: Sensor_1 reported A with 0.70 reliability, with no conflicting evidence. |
| M04 | 1 | A->B | A | .70 | .70 | .09 | 3 | E1/1 | 0 | .00 | yes/lineage | `resp_0ae81ba17ffc707a016ab07aea5c5087d0a237ffabeff00e44` | Choose A. Sensor_1 directly reports A; Agent C cites the same evidence root, so it should not be counted as independent support. |

## 5. Paired-prefix validation

**Paired prefix integrity: PASS.** LINEAGE and MACRO match exactly for M01-M04 on answer, confidence, message, `P(A)`, Brier score, and provider `response_id`. MACRO is therefore the recorded paired prefix through the stopping boundary, not an independently sampled alternative.

## 6. State at the MACRO stopping boundary

The boundary is LINEAGE M04 / MACRO M04:

- Answer: `A`
- Reported confidence: `0.70`
- `P(A)`: `0.70`
- Brier: `0.09`
- Inference depth: `3`
- Actual roots: `[E1]`; independent root count: `1`
- New independent evidence at M04: `0`
- New independent roots during the completed recursive cycle: `0`
- `macro_stop_triggered`: `true`
- Boundary message: “Choose A. Sensor_1 directly reports A; Agent C cites the same evidence root, so it should not be counted as independent support.”

This is a **[MANIPULATION CHECK]**: the architecture produced MACRO at one completed recursive cycle while LINEAGE continued to four.

## 7. LINEAGE post-boundary trajectory

| Event | P(A) | Confidence | Brier | Depth | Roots | New evidence | Answer |
|---|---:|---:|---:|---:|---:|---:|---|
| M05 | .70 | .70 | .09 | 4 | 1 | 0 | A |
| M06 | .70 | .70 | .09 | 5 | 1 | 0 | A |
| M07 | .70 | .70 | .09 | 6 | 1 | 0 | A |
| M08 | .70 | .70 | .09 | 7 | 1 | 0 | A |
| M09 | .62 | .62 | .1444 | 8 | 1 | 0 | A |
| M10 | .70 | .70 | .09 | 9 | 1 | 0 | A |
| M11 | .70 | .70 | .09 | 10 | 1 | 0 | A |
| M12 | .70 | .70 | .09 | 11 | 1 | 0 | A |
| M13 | .70 | .70 | .09 | 12 | 1 | 0 | A |

Quantitative deltas from M04 to M13:

- Delta confidence: `0.70 - 0.70 = 0.00`
- Delta `P(A)`: `0.70 - 0.70 = 0.00`
- Delta Brier: `0.09 - 0.09 = 0.00`
- Delta depth: `12 - 3 = +9`
- Delta roots: `1 - 1 = 0`
- Post-M04 minimum/maximum `P(A)`: `0.62 / 0.70`
- Post-M04 minimum/maximum confidence: `0.62 / 0.70`
- Answer flips after M04: `0`
- `P(A)` changes without new evidence: `2` transitions, M09 down `0.08` and M10 up `0.08`

This is a **[OBSERVATION — PILOT]** for transient confidence deflation at M09 and temporary Brier worsening. The final stable state is a **[NO EFFECT OBSERVED — PILOT]** for final answer, final confidence, final `P(A)`, and final Brier relative to M04.

## 8. FREE versus LINEAGE

| Message | FREE P(A) | LINEAGE P(A) | Delta | FREE conf | LINEAGE conf | Answers |
|---|---:|---:|---:|---:|---:|---|
| M01 | .70 | .70 | +.00 | .70 | .70 | A/A |
| M02 | .70 | .70 | +.00 | .70 | .70 | A/A |
| M03 | .70 | .70 | +.00 | .70 | .70 | A/A |
| M04 | .70 | .70 | +.00 | .70 | .70 | A/A |
| M05 | .70 | .70 | +.00 | .70 | .70 | A/A |
| M06 | .70 | .70 | +.00 | .70 | .70 | A/A |
| M07 | .70 | .70 | +.00 | .70 | .70 | A/A |
| M08 | .70 | .70 | +.00 | .70 | .70 | A/A |
| M09 | .70 | .62 | -.08 | .70 | .62 | A/A |
| M10 | .70 | .70 | +.00 | .70 | .70 | A/A |
| M11 | .70 | .70 | +.00 | .70 | .70 | A/A |
| M12 | .70 | .70 | +.00 | .70 | .70 | A/A |
| M13 | .70 | .70 | +.00 | .70 | .70 | A/A |

The first output divergence is message text at M02. The first numerical divergence is M09. The first answer divergence does not occur. Maximum absolute `P(A)` and confidence differences are both `0.08`; maximum absolute Brier difference is `0.0544` at M09. FREE itself remains numerically stable across M01-M13.

## 9. Natural-language message transformations

These are descriptive observations of recorded text, not subjective quality scores:

- Claim repeated: all conditions repeatedly retain the claim that Sensor_1 favors A at `0.70` reliability.
- Confidence language strengthened/weakened: LINEAGE M09 explicitly says confidence is “reduced”; M10 returns to the direct sensor framing. No such weakening appears in FREE.
- New justification introduced: LINEAGE M09 introduces “the report is indirect, seven inference steps deep, and lacks independent corroboration.”
- Previous information compressed: later messages shorten the wording while preserving E1 and the sensor reliability.
- Source/reliability detail preserved: Sensor_1 and `0.70` remain present throughout the recorded messages.
- Lineage information referenced: LINEAGE messages increasingly mention the shared root, correlated claims, relays, and independent support. FREE also mentions relays and duplicate evidence, but has no visible envelope.
- Unsupported new factual content: none identified in the recorded messages; the added claims concern the recorded topology/root metadata.

## 10. Falsification checks

- Did depth increase while `P(A)`, confidence, and answer remained stable? **Yes for FREE throughout; yes for LINEAGE at all positions except transient M09.** Depth rose from 3 at M04 to 12 at M13 while final values returned to their boundary values.
- Did continued recursion improve calibration? **Not established.** Final Brier stayed at `0.09`; M09 temporarily worsened to `0.1444`.
- Did confidence move closer to the sensor reliability? **At M09 it moved away from the recorded `0.70` reliability; it returned at M10.**
- Did lineage prevent drift? **Not as a universal claim.** LINEAGE had a transient M09 confidence/P(A) decrease; FREE had no numerical drift in this pilot.
- Did FREE remain just as stable as LINEAGE? **Numerically, yes in this run.** FREE remained at answer A, confidence/P(A) .70, and Brier .09 for all 13 events.

## 11. Hypothesis-specific audit

| Phenomenon | Result | Supporting events |
|---|---|---|
| Confidence inflation | Not observed | No confidence exceeded .70. |
| Confidence deflation | Observed in this pilot | LINEAGE M09: .70 to .62; M10 returned to .70. |
| Belief drift | Not observed as final drift; transient numerical drift observed | LINEAGE M09 P(A)=.62, M10-M13=.70; answer stayed A. |
| Answer flipping | Not observed | All FREE, LINEAGE, and MACRO answers are A. |
| Recursive stability | Observed for final answer and final metrics, with transient LINEAGE M09 deviation | LINEAGE M04 versus M13; FREE M01-M13. |
| Calibration improvement/degradation | Not testable as a general effect from one pilot | Brier was .09 at boundary/final and .1444 at LINEAGE M09. |
| Message-content drift | Observed | Wording changes from direct reports to explicit root/relay and double-counting language. |

## 12. Pilot observations and classifications

- **[MANIPULATION CHECK]** MACRO stopped after one recursive cycle with zero new independent roots; LINEAGE continued through four cycles.
- **[MANIPULATION CHECK]** Paired prefix reuse was exact through M04, including provider response IDs.
- **[OBSERVATION — PILOT]** LINEAGE M09 produced transient confidence deflation and Brier worsening without new independent evidence.
- **[NO EFFECT OBSERVED — PILOT]** No answer flip, no final confidence drift, no final `P(A)` drift, and no final Brier change from M04 to M13.
- **[NO EFFECT OBSERVED — PILOT]** FREE showed no numerical recursive drift across M01-M13.

## 13. What this pilot does not establish

This single exploratory run does not confirm a general hypothesis, establish that MACRO is better, demonstrate recursive epistemic degradation, establish causality for visible lineage, or support population-level calibration claims. It does not reveal hidden reasoning or chain of thought. The results are limited to recorded outputs, lineage fields, and computed metrics for this one world, seed, model, and prompt configuration.

## 14. Anomalies

No integrity anomaly was found. The notable empirical anomaly is LINEAGE M09: confidence and `P(A)` decreased to `.62` despite zero new independent evidence, then returned to `.70` at M10. The message explicitly attributes the reduction to indirectness, depth, and lack of independent corroboration.

## 15. Audit files and execution confirmation

- [EXP_002_PILOT_002_AUDIT_v0.1.md](EXP_002_PILOT_002_AUDIT_v0.1.md)
- [EXP_002_PILOT_002_AUDIT_v0.1.json](EXP_002_PILOT_002_AUDIT_v0.1.json)
- Preserved run: [../../results/archive/pilots/pilot_002_seed42_r4](../../results/archive/pilots/pilot_002_seed42_r4)

Audit-time OpenAI calls: `0`.

Experiment code modified during audit: `false`.

Results regenerated or overwritten during audit: `false`.
