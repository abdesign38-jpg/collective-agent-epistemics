# Hypothesis v0.1

## Status
ACTIVE / FALSIFIABLE / NOT ESTABLISHED

## Core hypothesis

Repeated transformation and recirculation of information between agents may reduce
effective evidence independence and epistemic traceability. If the network fails to
preserve epistemic lineage, derived information may be treated as independent support,
allowing confidence or consensus to increase without a corresponding increase in
independently grounded evidence.

## Null hypothesis

Observed multi-agent failures are sufficiently explained by individual-agent error;
interaction does not introduce an additional degradation mechanism related to evidence
dependency or lineage.

## Primary variables

- Independent evidence roots
- Inference depth
- Epistemic lineage retention
- False-independent-support count
- Confidence / calibration
- Accuracy
- Stopping behavior

## EXP-001 prediction

If a network naively treats descendant claims as independent support, confidence may
increase across recursive communication even when the set of independent evidence roots
does not change.

A lineage-aware representation should make this inflation observable and may reduce it.

A macro layer should be able to detect a complete cycle that added no independent
evidence and stop further recursion.

## Falsification cues

The hypothesis should be weakened or revised if, under real-model experiments:

1. confidence does not systematically increase without new independent evidence;
2. models already preserve source dependency well enough that lineage metadata adds no value;
3. recursive interaction improves calibration even when evidence roots remain fixed;
4. observed errors are better predicted by individual-agent quality than by network lineage variables.
