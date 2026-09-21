# Repository Research Structure v0.1

## Hierarchy

The repository follows this research hierarchy:

```text
Research framework
    ↓
Hypothesis
    ↓
Experiment
    ↓
Protocol version
    ↓
Replication set
    ↓
Individual runs
    ↓
Aggregate audit
    ↓
Research observations
```

## Roles

- **Framework:** the stable umbrella theory, question, null, and research dimensions.
- **Hypothesis:** a falsifiable working proposition; it is not silently rewritten by a pilot.
- **Experiment:** a scientifically distinct design or intervention. A new experiment generally changes a causal intervention, evidence structure, topology, information availability, treatment definition, or protocol.
- **Protocol:** a frozen implementation and configuration of an experiment.
- **Replication set:** a predefined group of equivalent runs using one protocol and configuration.
- **Run:** one execution/sample of a frozen protocol. A stochastic rerun is not a new experiment.
- **Audit:** post-run forensic or aggregate analysis that does not modify experiment semantics.
- **Observation:** a conservative empirical finding derived from recorded runs; observations do not silently rewrite the hypothesis or protocol.

## Branching and naming policy

The current working branch `exp-002-prep` is the working branch for EXP-002 v0.1 replication.

A new stochastic run maps to a new run directory:

```text
New stochastic run
→ new run directory

New replication group
→ new replication_set directory

New interpretation
→ audit / observation document

Protocol implementation change
→ new protocol version

Scientifically distinct experimental intervention
→ new experiment and usually new branch
```

One Git branch per run is prohibited/rejected as a repository convention. Individual runs are data samples, not implementation variants.

Do not create branches for `rep_001`, `rep_002`, `rep_003`, `rep_004`, or `rep_005`. Future branches should correspond to meaningful protocol or experiment work. Conceptual examples only are:

- `experiment/exp-003-source-detached`
- `experiment/exp-004-misleading-evidence`
- `experiment/exp-005-multi-root`

Those example branches are not created by this policy.

## EXP-002 mapping

- Framework: `research/framework_v0.1.md`
- Hypothesis: `research/hypothesis_v0.1.md`
- Experiment: `experiments/EXP_002/`
- Protocol version: `experiments/EXP_002/PROTOCOL_LOCK_v0.1.md`, tag `exp-002-protocol-v0.1`
- Replication set: `experiments/EXP_002/results/archive/replication_sets/replication_set_001/`
- Runs: `rep_001` through `rep_005` within that set, created only when executed and archived
- Pilot audit: `experiments/EXP_002/audits/pilots/`
- Replication-set audit: `experiments/EXP_002/audits/replication_sets/replication_set_001/`, created before audit content exists
- Observations: `research/observations/`
