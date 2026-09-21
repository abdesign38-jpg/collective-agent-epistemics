# EXP-002 Replication Set 001 Audit Errata v0.1

## Classification

**[BUG — AUDIT ANALYSIS ONLY]**

The archived empirical runs are not corrupted. EXP-002 runtime, prompts, metrics, and raw event files are unchanged.

## Correction

`EXP_002_REPLICATION_SET_001_AUDIT_v0.1.md` and `.json` contained an analysis-layer event-alignment bug for some DSCD events. The prior analysis did not consistently use the immediately preceding numeric `visible_message_id` within the same condition, and some records used the receiving agent rather than the response-generating agent.

The correct rules are:

- for `Mxx`, use `M(xx-1)` in the same condition as the event-level baseline;
- use `actor = event.sender` and `receiver = event.receiver`;
- apply the locked DSCD v0.1 criterion D only to the current event's visible model message.

Example: in `rep_001 LINEAGE`, `M07=.70`, `M08=.62`, `M09=.68`; therefore M08 is `.70 -> .62` and M09 is `.62 -> .68`.

## Historical status

The v0.1 audit remains preserved as the historical original audit. This errata and `EXP_002_REPLICATION_SET_001_AUDIT_v0.2.{md,json}` supersede v0.1 for DSCD event classification and agent attribution only. They do not replace or alter the archived raw data, primary experiment results, or the frozen protocol.
