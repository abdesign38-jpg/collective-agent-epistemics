# Collective Agent Epistemics

A minimal research harness for testing whether recursive multi-agent communication can
increase apparent confidence or informational volume without a corresponding increase
in independent evidence.

## Research question

> As inference depth and inter-agent recursion increase without new independent evidence,
> what happens to epistemic lineage, calibration, confidence, and convergence?

This repository begins with **EXP-001**, a controlled synthetic experiment. It is not
evidence that LLMs necessarily behave this way. Its purpose is to validate the
instrumentation, lineage model, metrics, and experimental protocol before replacing
the synthetic agent with real model adapters.

## EXP-001 conditions

1. **free** — agents exchange ordinary claims and may naively treat received claims as
   new support.
2. **lineage** — claims carry explicit evidence roots and derivation metadata.
3. **macro** — the same lineage-aware claims are tracked by a macro layer that can stop
   recursion when a full cycle adds no independent evidence.

All three conditions use the same synthetic worlds and same agent topology. The worlds include a misleading-evidence control so the harness can expose confidently-wrong amplification, not only confidence growth on correct trials.

## Quick start

Requires Python 3.10+ and no external packages.

```bash
python -m experiments.EXP_001.run --world all --rounds 4
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

Outputs are written to:

```text
experiments/EXP_001/results/
```

including:

- `summary.csv`
- `events.jsonl`
- `run_metadata.json`

## Important methodological note

The built-in synthetic agent intentionally uses simple, explicit update rules so the
harness can be audited. A result from this synthetic agent does **not** validate the
research hypothesis. It validates that we can measure:

- actual evidence lineage
- perceived lineage
- false independent support
- inference depth
- confidence change without new independent evidence
- macro stopping behavior

The next research phase should replace the synthetic agent with one or more real LLM
adapters while preserving the same protocol and event schema.
