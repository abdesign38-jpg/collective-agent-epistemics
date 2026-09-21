# EXP-002 Results Contract

## Active result files

The runner writes transient/latest outputs to:

- `results/events.jsonl`
- `results/summary.csv`
- `results/run_metadata.json`

These active result files remain ignored by Git and may be replaced by a later run.

## Preserved empirical runs

Immutable snapshots live under `results/archive/<run_id>/`. Each archived run must contain:

- `events.jsonl`
- `summary.csv`
- `run_metadata.json`

Each archived run must receive SHA-256 hashes during its audit. Archived runs must not be overwritten.

## Naming convention

- `pilot_<NNN>_seed<seed>_r<rounds>`
- `rep_<SET>_<NNN>_seed<seed>_r<rounds>`

For the next replication set, use for example:

- `rep_001_001_seed42_r4`
- `rep_001_002_seed42_r4`
- `rep_001_003_seed42_r4`
- `rep_001_004_seed42_r4`
- `rep_001_005_seed42_r4`

Individual stochastic reruns are replications of EXP-002 v0.1, not new experiments.
