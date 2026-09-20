# Next Steps

## Gate 0 — Harness validation
- Run unit tests.
- Run EXP-001 synthetic worlds.
- Inspect `events.jsonl` and `summary.csv`.
- Confirm actual roots and perceived roots behave as intended.

## Gate 1 — Real-model adapter
Replace `SyntheticAgent` with an adapter that:
1. receives the exact same world evidence and messages;
2. returns a claim, confidence, and perceived evidence roots;
3. does not see the hidden ground-truth lineage graph.

Run the same three conditions.

## Gate 2 — Replication
- multiple models
- multiple temperatures / seeds
- 30–50 trials minimum per condition
- fixed topology first
- pre-register metrics and stopping rules

## Gate 3 — Architecture intervention
Only after observing the phenomenon in real-model runs:
- test lineage-aware handoffs;
- test macro stopping conditions;
- compare calibration and accuracy;
- test whether the intervention merely suppresses confidence or genuinely improves epistemic quality.
