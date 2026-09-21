# EXP-002 Results Contract

## Active result files

The runner writes transient/latest outputs to:

- `results/events.jsonl`
- `results/summary.csv`
- `results/run_metadata.json`

These active result files remain ignored by Git and may be replaced by a later run.

## Archive hierarchy

```text
results/
├── latest transient runner output
└── archive/
	├── pilots/
	└── replication_sets/
```

### Active/latest results

The root-level result files are transient/latest runner output and remain Git-ignored.

### Pilots

Exploratory runs executed before formal replication sets live under `results/archive/pilots/<run_id>/`.

### Replication sets

Predefined collections of equivalent stochastic runs live under
`results/archive/replication_sets/<replication_set_id>/`. Each set contains metadata
such as `manifest.json` and its archived run directories.

### Run immutability

Once archived, a run's result files must not be overwritten. Every archived run must contain:

- `events.jsonl`
- `summary.csv`
- `run_metadata.json`

Each archived run must receive SHA-256 hashes during its audit.

## Naming convention

- `pilot_<NNN>_seed<seed>_r<rounds>`
- `rep_<SET>_<NNN>_seed<seed>_r<rounds>`

For replication set 001, use for example:

- `replication_sets/replication_set_001/rep_001/`
- `replication_sets/replication_set_001/rep_002/`
- `replication_sets/replication_set_001/rep_003/`
- `replication_sets/replication_set_001/rep_004/`
- `replication_sets/replication_set_001/rep_005/`

Individual stochastic reruns are replications of EXP-002 v0.1, not new experiments.
