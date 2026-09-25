# Repository Research Structure v0.2

## Purpose

This document defines the repository model that preserves the scientific hierarchy without treating Git branches as scientific identities.

## Canonical research hierarchy

```text
Scientific question
    ↓
Prospective design
    ↓
Execution
    ↓
Immutable evidence archive
    ↓
Audit / forensic evaluation
    ↓
Synthesis
    ↓
Checkpoint tag + commit SHA
    ↓
Next prospective question
```

## Main branch

The `main` branch is the canonical integrated history of the repository. It is not itself a frozen experiment or a scientific identity.

## Working branches

Temporary work lives in branches such as:

```text
experiment/*
fix/*
chore/*
docs/*
```

These branches are operational workspaces. They do not define scientific status.

## Experimental samples and data identities

The repository must not create branches per:

```text
run
replication
seed
world
attempt
agent
```

Those are scientific or data identities and belong in manifests, archives, audits, and checkpoint metadata rather than in long-lived Git branch names.

## Scientific checkpoints

Completed scientific states are identified by:

```text
commit SHA
+
annotated Git tag
```

Not by a persistent working branch.

This preserves the distinction between:

```text
exp-001-baseline-v0.1
    ↓
synthetic harness baseline

exp-002-protocol-v0.1
    ↓
frozen EXP-002 protocol/runtime used for real-model work

exp-002-gate2a-closed-v0.1
    ↓
same-world stochastic replication closure

exp-002-gate2b-closed-v0.1
    ↓
prospective multi-world Gate 2B closure
```

Protocol freeze and evidence closure are distinct scientific concepts and must not be collapsed.

## Immutable archives

Once archived and audited, empirical execution artifacts remain at their committed paths. Historical raw archives are provenance records and are not moved or cleaned as a matter of convenience. This includes archived runs, manifests, audit files, and synthesis outputs that are already committed.

## Versioning rules

If scientific semantics materially change, the repository creates:

```text
new protocol version
```

or:

```text
new experiment
```

It does not silently mutate an already frozen protocol.

## Historical documents

Versioned historical documents remain unchanged. New conceptual updates receive a new version number rather than overwriting previous findings.

## Formal folder/scientific relationship

```text
experiments/
    EXP_XXX/
        prospective plans
        manifests
        protocol
        runtime

        results/
            archive/
                empirical execution evidence

        audits/
            forensic / aggregate evaluation

research/
    framework
    hypothesis
    observations
```

Interpretation:

```text
experiments/
    = what was designed and executed

results/archive/
    = what actually happened

audits/
    = what was mechanically or analytically found

research/
    = how those findings relate to the larger scientific question
```

These layers must remain distinct and must not collapse into each other.

## Future gate growth

A future gate remains in the same experiment directory when it is scientifically part of the same experiment.

```text
experiments/EXP_002/
├── GATE_2C_PLAN_v0.1.*
├── GATE_2C_MANIFEST_v0.1.*
│
├── results/
│   └── archive/
│       └── gate_2c/
│
└── audits/
    └── gate_2c/
```

Gate 2A and Gate 2B remain in their current locations. The historical path is more important than cosmetic symmetry.

When Gate 2C closes:

```text
merge → main
```

Then:

```text
exp-002-gate2c-closed-v0.1
```

points to the closure commit, and the temporary working branch for Gate 2C may be deleted.

## When a new experiment is required

A new experiment number is created only when the scientific design materially changes, not merely because repository organization needs additional space. Examples that require explicit scientific review include:

```text
number of independent evidence roots
network topology
source re-grounding
source-detached recursion
information visibility
lineage intervention semantics
MACRO intervention semantics
non-interaction control
agent population structure
```

## Governance principle

The repository exists to preserve the chain:

```text
scientific question
    ↓
prospective design
    ↓
execution
    ↓
immutable evidence
    ↓
audit
    ↓
synthesis
    ↓
checkpoint
    ↓
next prospective question
```

Git preserves that chain without reshaping it retroactively.
