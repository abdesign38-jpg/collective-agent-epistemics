# EXP-003 Gate 3A Observations v0.2: the origin's inbound message and the sensor's name

**Status:** OBSERVATION RECORD, qualitative and descriptive. Written after Gate 3A closed (`exp-003-gate3a-closed-v0.1`). It reads the archived messages and one archived provenance mark; it changes nothing in Gate 3A and proposes nothing for Gate 3A. It informs the pre-registered analysis rules of Gate 3B, which must be committed before any Gate 3B value is read.

## What was read

The sixteen ring LINEAGE firings at which the source agent A rose above the single-root reference (eight in Set 001, eight in Set 002; listed in `audits/gate_3a/EXP_003_GATE_3A_SYNTHESIS_v0.1.json`, `origin_deviations`), each with the message A had just received from C and the message A then sent; and, for each, one calibrated A firing at the same firing index in the same stage from another world, with its inbound and outgoing messages. Thirty-two pairs in all. Then one archived provenance mark, `source_named` (whether the message text names the sensor's source id, `sensor_1`; computed mechanically by the frozen runtime's `provenance.py` at run time), was tabulated against A's direction for every post-seed A firing in the dyad, ring and bounce arms, both conditions, both stages. The tabulation is reproducible with `python -m experiments.EXP_003.tools.origin_inbound_naming`.

## What the sixteen inflation messages have in common

In every one of the sixteen, the message A received from C named the evidence only as `E1` (the root id from the lineage envelope) and did not name `sensor_1`. In every one of the sixteen, A's own message then spoke of two sources: its direct observation by name (`sensor_1`) and C's support "via evidence root E1", "a separate root (E1)", "one additional root", "independently … via E1". Two of them say it outright: "sensor_1 and E1 appear to be two distinct original sources." A then raised its confidence modestly (72% to 84.5%), usually adding that the second source was "weak" or "deeply relayed".

In the matched calibrated firings, twelve of the sixteen inbound messages named the sensor together with the root ("sensor_1 (E1)", "E1/sensor_1"), and A's reply said "the same source" or "the same evidence root E1" in almost every case (74 of the 80 calibrated ring LINEAGE A messages across both stages use the word "same"; 0 of the 16 inflation messages do).

Nothing in the prompt ever states that `E1` and `sensor_1` are the same thing. The direct observation is labelled `Source: sensor_1`; the lineage envelope is labelled `Evidence roots: [E1]`. The agent can only infer the identity, and it reliably does so when the relayed text carries the sensor's name.

## The mechanical table

Post-seed firings of A, by whether the inbound message named the sensor, with A's direction by the Gate 3A analysis rules (certainty excess, tolerance 1e-6). Stages separate.

| Arm | Condition | Inbound names the sensor | A firings | inflation | at reference | discount |
|---|---|---|---:|---:|---:|---:|
| dyad Set 001 | LINEAGE | yes | 58 | 0 | 58 | 0 |
| dyad Set 001 | LINEAGE | no | 14 | 0 | 14 | 0 |
| dyad Set 002 | LINEAGE | yes | 62 | 0 | 62 | 0 |
| dyad Set 002 | LINEAGE | no | 10 | 0 | 10 | 0 |
| ring Set 001 | LINEAGE | yes | 38 | 0 | 38 | 0 |
| ring Set 001 | LINEAGE | no | 10 | **8** | 2 | 0 |
| ring Set 002 | LINEAGE | yes | 24 | 0 | 24 | 0 |
| ring Set 002 | LINEAGE | no | 24 | **8** | 16 | 0 |
| bounce Set 001 | LINEAGE | yes | 29 | 0 | 29 | 0 |
| bounce Set 001 | LINEAGE | no | 7 | **3** | 4 | 0 |
| bounce Set 002 | LINEAGE | yes | 24 | 0 | 24 | 0 |
| bounce Set 002 | LINEAGE | no | 12 | **2** | 10 | 0 |

Under FREE the inbound message named the sensor at 306 of 312 A firings across the three arms and A never inflated. Under LINEAGE the relayed message dropped the sensor's name far more often in the ring (10 and 24 of 48) and the bounce (7 and 12 of 36) than in the dyad (14 and 10 of 72).

**[DESCRIPTIVE OBSERVATION]** All 21 origin-inflation events in Gate 3A (16 ring, 5 bounce, LINEAGE, both stages) occurred at firings where the inbound message did not name the sensor. At the 235 LINEAGE A firings where the inbound message did name it, A inflated 0 times. The association holds in both stages and in both arms that show inflation.

**[DESCRIPTIVE OBSERVATION]** Not naming the sensor was necessary but not sufficient: in the ring, 18 of the 34 unnamed inbound firings and in the bounce 14 of 19 still left A at the reference. In the dyad, 24 unnamed inbound firings produced no inflation at all; there the inbound comes from B, one hop from A, and its wording nearly always kept "sensor_1" or "the same source".

**[OPEN QUESTION, candidate mechanism]** The lineage envelope gives the relaying agents an abstract root id. Relaying agents increasingly describe the evidence by that id and drop the sensor's name as the chain lengthens (provenance erosion, already a Gate 3A measurement). When the message returns to the origin carrying "E1" but not "sensor_1", the origin, which sees its own observation labelled "sensor_1", sometimes treats the two labels as two sources and combines them. This is the hypothesis's lineage-loss-to-double-counting step observed in its smallest form, mediated by a naming gap between the direct observation and the envelope. It is a reading of 16 events and one mark, not a test, and Gate 3A was not designed to separate it from alternatives (depth, hop count, phrasing of caution).

## What this changes

Nothing in Gate 3A. For Gate 3B's pre-registered analysis it motivates one additional mechanical table, built from marks the runtime already archives: at D (the fan-in agent, which has no direct observation and so no naming gap of its own) and at A (which has), excess and false independent support against whether each inbound message named the sensor. The Gate 3B plan is frozen and is not touched; the analysis spec is written before any Gate 3B value is read.

## Boundary

Descriptive. Thirty-two messages were read by a person; the table is mechanical over all 624 post-seed A firings. No significance test, no threshold, no causal claim. Stages reported separately.
