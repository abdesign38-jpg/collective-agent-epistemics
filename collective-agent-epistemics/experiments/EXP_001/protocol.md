# EXP-001 — Minimal Three-Agent Epistemic Loop

## Purpose

Validate the measurement harness before using real LLMs.

This experiment does **not** establish that real LLM agents behave like the synthetic
agent. The synthetic agent is a transparent mechanism used to verify that the protocol
can detect:

- confidence changes without new independent evidence;
- divergence between actual and perceived lineage;
- false-independent-support;
- inference depth;
- macro stopping conditions.

## Topology

Ring:

```text
A -> B -> C -> A
```

The topology is fixed across conditions.

## Conditions

### A. free

Messages do not expose true evidence roots. The synthetic receiver naively treats each
received claim as a fresh social evidence unit.

### B. lineage

Each message exposes its true evidence roots. A root contributes evidential weight at
most once per agent.

### C. macro

Same as `lineage`, plus a global lineage tracker. After a complete A->B->C->A cycle, the
macro tracker stops the run if the cycle introduced no previously unseen evidence root.

## Worlds

- W1: one evidence root
- W2: two independent supporting roots
- W3: conflicting independent roots
- W4: one misleading evidence root (ground truth is the opposite state)

## Primary outputs

- accuracy
- Brier score
- confidence
- independent root count
- perceived root count
- false-independent-support
- inference depth
- number of completed cycles

## Interpretation guardrail

A finding in the synthetic condition is only an engineering validation of the harness.
The research hypothesis begins to receive empirical support only after repeating the
protocol with real model agents.
