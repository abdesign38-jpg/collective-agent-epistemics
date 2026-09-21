# Research Framework v0.1

## Status
Stable umbrella framework for EXP-002 replication. The framework is broader than any single pilot observation and is not itself a claim that the mechanism below is established.

## Core problem
Local agent competence does not guarantee global epistemic reliability. A network can transmit locally reasonable messages while the network-level evidence state becomes difficult to trace or incorrectly treated as independent support.

The project distinguishes three objects:

- **Agent epistemic state:** what an agent currently believes and how confident it is.
- **Message transmitted:** the claim, confidence, and natural-language content passed to the next agent.
- **Network evidence state:** the actual set of independent external evidence roots and their derivation structure.

These are not interchangeable. In general, $S_A \\ne M_{A\\to B}$.

## Candidate mechanism

The following is a candidate causal chain, not established fact:

```text
Recursion
→ Correlation
→ Lineage Loss
→ Evidence Double Counting
→ Confidence / Consensus Distortion
```

Recursion is not inherently harmful, and repeated communication is not automatically degradation. Possible empirical outcomes include confidence inflation, confidence deflation, instability, belief drift, false consensus, calibration changes, or no measurable effect. Confidence inflation is one possible outcome, not the definition of degradation.

## Primary research question

> As inference depth and inter-agent recursion increase without new independent evidence, what happens to epistemic lineage, calibration, confidence, and convergence?

## Working hypothesis

Repeated transformation and recirculation may reduce effective evidence independence and traceability. If dependency is not preserved, derived information may be treated as independent support.

This remains a falsifiable working proposition and has not been established by EXP-002 Pilot 002.

## Null

Interaction adds no meaningful network-level epistemic failure beyond individual-agent behavior.

## Research dimensions

- actual lineage;
- visible/explicit lineage;
- agent-perceived dependency;
- independent evidence roots;
- inference depth;
- confidence;
- `P(A)`;
- calibration;
- accuracy;
- message transformation;
- stopping behavior.

Agent-perceived dependency is a conceptual variable motivated by the distinction between structured lineage and dependency inferable from natural language. It is not added to EXP-002 code or metrics by this framework document.

## Experimental sequence

1. **EXP-001 — synthetic harness validation.** Validate world generation, topology, lineage tracking, metrics, and stopping instrumentation.
2. **EXP-002 — real-model recursive communication experiment.** Apply the frozen communication architectures with a real model adapter.
3. **Replication — same frozen EXP-002 configuration first.** Replicate before changing worlds, models, or architecture.
4. **Future experiments — only after EXP-002 replication/audit.** Broader interventions and configurations remain future work.
