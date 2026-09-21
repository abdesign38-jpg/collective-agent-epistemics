# EXP-002 Secondary Observation Spec v0.1

## Depth-Sensitive Confidence Discounting (DSCD)

**Status:** candidate secondary construct; exploratory; not established.

DSCD is a candidate observation in which increasing inference depth or indirectness is associated with reduced confidence or epistemic certainty even though the external evidence base remains unchanged. It is not the primary EXP-002 hypothesis and must not redefine replication success.

## Strict criteria

A recorded event qualifies as a strict DSCD candidate only when all of the following hold. The event-level numerical baseline is always the immediately preceding event in the same condition; it must not be selected after inspecting results.

1. No new independent evidence enters the network.
2. Actual evidence roots remain unchanged.
3. Confidence and epistemic certainty are reduced relative to the immediately preceding event.
4. The visible model message explicitly attributes caution to depth, indirectness, dependency, relay structure, or lack of independent corroboration.

A message or confidence change that fails any criterion may be reported as a related exploratory observation, but not as strict DSCD.

## Event-level calculations

For an event at position `t`, calculate against the immediately preceding event at `t-1` in the same condition:

```text
delta_confidence_transition = confidence_t - confidence_(t-1)
delta_p_a_transition = P(A)_t - P(A)_(t-1)
epistemic_certainty_t = abs(P(A)_t - 0.5)
```

The numerical confidence discount requires both:

```text
confidence_t < confidence_(t-1)
epistemic_certainty_t < epistemic_certainty_(t-1)
```

This remains valid if the selected answer changes from A to B.

## Post-boundary trajectory

Separately from event-level DSCD, preserve the paired MACRO stopping boundary at LINEAGE `M04`. For every LINEAGE event `M05` through `M13`, calculate:

```text
delta_confidence_from_M04
delta_p_a_from_M04
delta_brier_from_M04
delta_certainty_from_M04
delta_depth_from_M04
delta_roots_from_M04
```

This is a post-boundary trajectory measurement. It must not replace the event-level transition rule or serve as the DSCD baseline.

## Strict event labels

Use these labels mechanically:

- **DSCD-STRICT:** A-D all hold: zero new independent evidence; unchanged actual root set; both numerical reductions above; and explicit dependency/depth caution in the visible recorded message.
- **DSCD-NUMERIC:** A-C hold but the message does not explicitly provide criterion D.
- **DSCD-LANGUAGE-ONLY:** dependency/depth caution is explicit, but numerical epistemic certainty does not decrease.
- **DSCD-NONE:** no candidate event.

Criterion D must be present in the recorded output. Do not infer hidden reasoning. Relevant concepts include depth, inference steps, indirectness, relay/retransmission, shared root, dependency, lack of independent corroboration, or lack of new evidence.

## Specificity

Event classification and condition specificity are separate dimensions. For each run, report one of:

- **LINEAGE_ONLY** — numerical or strict candidate events occurred only in LINEAGE.
- **FREE_ONLY** — numerical or strict candidate events occurred only in FREE.
- **BOTH** — numerical or strict candidate events occurred in both conditions.
- **NONE** — no numerical or strict candidate events occurred in either condition.

Do not describe an event as lineage-specific merely because it occurred in LINEAGE if FREE shows the same behavior.

## Separate secondary observations

Audits must track these separately from DSCD:

- **Agent-perceived dependency:** dependency inferable by an agent from natural-language content, distinct from structured actual lineage.
- **Agent A periodic re-grounding:** Agent A receives its direct observation again whenever it participates in the current EXP-002 topology. This is re-grounding in an existing root, not new independent evidence.
- **Message-content transformations:** changes in wording, source detail, relay descriptions, justification, or explicit anti-double-counting language.

These constructs are extracted from recorded events during audit. They are not runtime metrics and must not be added to EXP-002 code by this specification.

## Interpretation rule

DSCD and the related secondary observations are exploratory labels. They do not establish causality, recursive degradation, calibration change, or superiority of one condition. Every stable and unstable run remains reportable.
