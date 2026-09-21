# EXP-002 Secondary Observation Spec v0.1

## Depth-Sensitive Confidence Discounting (DSCD)

**Status:** candidate secondary construct; exploratory; not established.

DSCD is a candidate observation in which increasing inference depth or indirectness is associated with reduced confidence or epistemic certainty even though the external evidence base remains unchanged. It is not the primary EXP-002 hypothesis and must not redefine replication success.

## Strict criteria

A recorded event qualifies as a strict DSCD candidate only when all of the following hold:

1. No new independent evidence enters the network.
2. Actual evidence roots remain unchanged.
3. Confidence and epistemic certainty are reduced relative to the relevant prior or boundary state.
4. The visible model message explicitly attributes caution to depth, indirectness, dependency, relay structure, or lack of independent corroboration.

A message or confidence change that fails any criterion may be reported as a related exploratory observation, but not as strict DSCD.

## Separate secondary observations

Audits must track these separately from DSCD:

- **Agent-perceived dependency:** dependency inferable by an agent from natural-language content, distinct from structured actual lineage.
- **Agent A periodic re-grounding:** Agent A receives its direct observation again whenever it participates in the current EXP-002 topology. This is re-grounding in an existing root, not new independent evidence.
- **Message-content transformations:** changes in wording, source detail, relay descriptions, justification, or explicit anti-double-counting language.

These constructs are extracted from recorded events during audit. They are not runtime metrics and must not be added to EXP-002 code by this specification.

## Interpretation rule

DSCD and the related secondary observations are exploratory labels. They do not establish causality, recursive degradation, calibration change, or superiority of one condition. Every stable and unstable run remains reportable.
