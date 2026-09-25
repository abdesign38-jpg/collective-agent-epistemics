# Visualization Domain

This directory hosts downstream, non-authoritative representations of committed scientific evidence.

```text
collective-agent-epistemics/
├── experiments/
├── research/
├── schemas/
├── src/
├── tests/
└── visualization/
    └── epistemic-hive/
```

## Invariants

1. Visualization may read authoritative committed scientific artifacts.
2. Visualization may transform those artifacts into display-oriented snapshots.
3. Visualization may never write to scientific artifacts.
4. A visualization snapshot is not empirical evidence.
5. Visualization must preserve lineage to its authoritative source.
6. A visualization failure cannot invalidate a scientific result.
7. Scientific execution cannot depend on visualization code.
8. The scientific repository remains valid if the visualization domain is removed.
9. Future visualizations may evolve as new scientific gates close.
10. Future scientific gates may not depend on visualization behavior.

> Epistemic Hive is a downstream observer of committed research artifacts. It is never an input to experimental execution.
