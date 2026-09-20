# EXP-002 Protocol

## Research question

Does recursive multi-agent communication alter confidence, calibration, or accuracy when no new independent external evidence enters the network?

## Experimental comparison

FREE vs LINEAGE vs MACRO.

## Independent variable

Communication architecture.

## Controlled variables

- world;
- evidence;
- topology;
- agent identities;
- model configuration;
- number of maximum rounds.

Every condition reuses the same frozen `World` object. The topology is `A -> B -> C -> A`. The harness owns actual lineage; model output and agent-reported information are stored separately from hidden metadata.

## Conditions

- **FREE**: ordinary natural-language messages; no epistemic envelope is exposed to agents.
- **LINEAGE**: messages carry structured lineage metadata; no stopping rule is applied.
- **MACRO**: the same metadata is exposed and the harness stops after a complete cycle with no new independent roots.

## Primary measurements

- accuracy;
- Brier score;
- confidence trajectory;
- independent evidence roots;
- inference depth;
- confidence delta with zero new evidence.

Raw event-level values are retained. No confidence threshold is used.

## Interpretation rule

EXP-002 infrastructure or deterministic-stub results are not evidence for the research hypothesis.

Empirical evaluation begins only after a real model adapter is introduced.
