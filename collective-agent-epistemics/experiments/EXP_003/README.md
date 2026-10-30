# EXP-003: Fan-in and Connected Hives

**Status:** PROTOCOL v0.1 FROZEN (tag `exp-003-protocol-v0.1`, runtime `c54563b`) · GATE 3A CLOSED (tag `exp-003-gate3a-closed-v0.1`, commit `1daa069`) · GATES 3B, 3C, 3D DRAFT, NOT FROZEN, NO REAL-MODEL CALLS MADE

EXP-003 climbs a ladder of topologies, one structural change per rung: solo → dyad → ring → bounce → diamond → detached → bridged hives. It reuses the EXP-002 conditions, metrics and governance and adds the new shapes, a two-root positive control, non-interaction and unbridged controls, a perceived-source probe, mechanical provenance scoring, pre-registered replication sets, a second-provider model layer, a factor ledger and a gate orchestrator.

Read in this order:

1. [protocol.md](protocol.md): topologies, root modes, new metrics, model layer, execution and archival.
2. [GATE_3A_PLAN_v0.1.md](GATE_3A_PLAN_v0.1.md): four matched topologies (ring, solo, dyad, bounce) on the same worlds, same model, same day, with a pre-registered replication set. The EXP-002 ring runs are retrospective evidence only.
3. [GATE_3B_PLAN_v0.1.md](GATE_3B_PLAN_v0.1.md): diamond, the first fan-in, with the one-root versus two-root matrix, a probe reactivity check and a replication set.
4. [GATE_3C_PLAN_v0.1.md](GATE_3C_PLAN_v0.1.md): every 3A and 3B shape without re-grounding, paired by world.
5. [GATE_3D_PLAN_v0.1.md](GATE_3D_PLAN_v0.1.md): bridged hives with unbridged twins, shared and dual roots.
6. [results/README.md](results/README.md): archive contract.
7. [GATE_3A_PRIMARY_OUTCOME_AUDIT_SPEC_v0.1.md](GATE_3A_PRIMARY_OUTCOME_AUDIT_SPEC_v0.1.md): the pre-registered analysis rules for Gate 3A, committed before any outcome was read.

Each markdown plan has a JSON twin (`GATE_3x_PLAN_v0.1.json`) that the orchestrator reads. Gates run in order; each requires the previous one closed (3D accepts 3C deferred with a recorded reason). A gate is never redesigned after its results are seen.

## Gate 3A (closed)

Four arms (ring control, solo control, dyad, bounce) on the same 12 worlds per stage, model `gpt-5.6-sol`, effort `medium`, paired execution, probe off, depth 12, 25 calls per world. Set 001 (discovery) and Set 002 (replication, 12 new worlds) both ran as frozen; Set 002 started after Set 001 passed its corpus audit and before any outcome of Set 001 was read. 96 of 96 worlds archived; two technical failure records preserved and excluded from scientific N.

| Step | Where |
|---|---|
| Plan and manifests | `GATE_3A_PLAN_v0.1.{md,json}` (FROZEN), `GATE_3A_MANIFEST_{RING,SOLO,DYAD,BOUNCE}00{1,2}_v0.1.{json,md}` |
| Archive | `results/archive/gate_3a/<set>/<canonical_id>/attempt_<NNN>/` |
| Corpus audits | `audits/gate_3a/EXP_003_GATE_3A_SET_00{1,2}_CORPUS_AUDIT_v0.1.{json,md}` |
| Analysis rules (pre-registered) | `GATE_3A_PRIMARY_OUTCOME_AUDIT_SPEC_v0.1.md`, committed at `12bbbab` before any output |
| Primary-outcome audits | `audits/gate_3a/EXP_003_GATE_3A_SET_00{1,2}_PRIMARY_OUTCOME_AUDIT_v0.1.{json,md}` |
| Historical ring (secondary) | `audits/gate_3a/EXP_003_GATE_3A_HISTORICAL_RING_OBSERVATION_v0.1.{json,md}` |
| Synthesis | `audits/gate_3a/EXP_003_GATE_3A_SYNTHESIS_v0.1.{json,md}` |
| Observations | `../../research/observations/EXP_003_gate_3a_observations_v0.1.md` |

In one paragraph, descriptive only: the solo control showed zero deviation from the single-root reference in 576 firings. Under LINEAGE, discounting increased with structural distance from the source (ring > bounce > dyad > solo, the same ordering in both stages; E6 consistent). Under FREE nearly every event sat at the reference. Bounce B discounted on its return leg toward A, not outward, and bounce C discounted less than ring C (E2 contradicted in both stages). The origin A rose above the reference at 8 of 48 LINEAGE firings in each stage of the ring and at 3 and 2 of 36 in the bounce, never in the dyad or solo, never under FREE, and never in the historical EXP-002 ring. Final answers never changed; MACRO stopped after one cycle in all 96 worlds. Verdicts: E1 contradicted/contradicted, E2 contradicted/contradicted, E3 consistent/consistent, E4 contradicted/consistent, E5 consistent/consistent, E6 consistent. No significance test, no pooled stage, no causal claim.

The audit chain is mechanical and re-runnable (read-only; each step refuses to run unless the previous one passed):

```bash
python -m experiments.EXP_003.tools.corpus_audit --plan experiments/EXP_003/GATE_3A_PLAN_v0.1.json --stage set_001
python -m experiments.EXP_003.tools.primary_outcome_audit --plan experiments/EXP_003/GATE_3A_PLAN_v0.1.json --stage set_001
python -m experiments.EXP_003.tools.primary_outcome_audit --historical --set-id ring_control_set_001
python -m experiments.EXP_003.tools.gate_synthesis
```

## Quick start (no network)

```bash
# Gate 3A shapes, probe off, each reaching depth 12.
python -m experiments.EXP_003.run --topology bounce --rounds 3 --no-probe
python -m experiments.EXP_003.run --topology solo --rounds 12 --no-probe
python -m experiments.EXP_003.run --topology dyad --rounds 6 --no-probe

# Gate 3B: naive stub double counts at D; dedup stub holds the reference under LINEAGE.
python -m experiments.EXP_003.run --topology diamond --rounds 4 --stub-mode naive
python -m experiments.EXP_003.run --topology diamond --rounds 4 --stub-mode dedup
python -m experiments.EXP_003.run --topology diamond --root-mode dual --stub-mode dedup

# Gate 3C and 3D shapes.
python -m experiments.EXP_003.run --topology bounce_detached --rounds 3 --no-probe
python -m experiments.EXP_003.run --topology hives_bridged --root-mode shared --stub-mode dedup

# Derive a prospective world manifest (no model calls).
python -m experiments.EXP_003.manifest --anchor "<anchor>" --set-id G3A_GEN001 \
  --topology diamond --root-mode single --count 12 --exclude 42 --out experiments/EXP_003/GATE_3A_MANIFEST_GEN001_v0.1

# Score every archived EXP-002 message for provenance erosion (read-only).
python -m experiments.EXP_003.tools.erosion_retrospective
```

Real-model runs require `--live --execution-policy paired --model <id> --reasoning-effort <level>` and one of:

```bash
# Model layer, provider 1
OPENAI_API_KEY=... python -m experiments.EXP_003.run --adapter openai --model gpt-5.6-sol --reasoning-effort medium --live --execution-policy paired ...
# Model layer, provider 2 (same prompt, same schema, same probe; only provider and model change)
ANTHROPIC_API_KEY=... python -m experiments.EXP_003.run --adapter anthropic --model claude-opus-5 --reasoning-effort medium --live --execution-policy paired ...
```

No call is made without `--live`. See "Model layer" in [protocol.md](protocol.md).

Technical smoke test with refusal fallbacks (anthropic only; never a scientific set, never archived):

```bash
ANTHROPIC_API_KEY=... python -m experiments.EXP_003.run --adapter anthropic --model claude-opus-5 --reasoning-effort low \
  --live --execution-policy paired --smoke --fallbacks --rounds 1
```

## Freezing and executing a gate (owner's procedure)

Each gate has a markdown plan (the science) and a JSON plan (the frozen configuration the orchestrator reads). Nothing below makes a model call until the last step. This is the procedure that closed Gate 3A, written for 3A; for Gate 3B the derivation anchor names the Gate 3A closure commit (`1daa069…|exp-003-protocol-v0.1|GATE_3B_PLAN_v0.1`), the exclusions add every Gate 3A seed, and the analysis rules for two-root worlds are written and committed before any Gate 3B value is read.

```bash
cd collective-agent-epistemics

# 1. Record the runtime you are freezing and tag it.
git tag -a exp-003-protocol-v0.1 -m "EXP-003 protocol v0.1 frozen runtime"
RUNTIME=$(git rev-parse HEAD)

# 2. Fill the anchors in GATE_3A_PLAN_v0.1.json (frozen_runtime, gate2b_closure_checkpoint,
#    derivation_anchor = "<gate2b closure sha>|exp-003-protocol-v0.1|GATE_3A_PLAN_v0.1") and commit.
#    plan_freeze_commit is the SHA of that commit; add it and set status to FROZEN in one more commit.

# 3. Derive the Set 001 manifests with that exact anchor. Zero model calls. Exclude 42 and the 20 Gate 2B seeds.
#    The ring manifest derives the seeds; solo, dyad and bounce inherit them verbatim.
ANCHOR="<gate2b closure sha>|exp-003-protocol-v0.1|GATE_3A_PLAN_v0.1"
EXCL="42 $(python -c "import json;m=json.load(open('experiments/EXP_002/GATE_2B_WORLD_MANIFEST_v0.1.json'));print(' '.join(str(w['seed']) for s in ('generalization_set_001','stress_set_001') for w in m[s]['worlds']))")"
M=experiments/EXP_003/GATE_3A_MANIFEST
python -m experiments.EXP_003.manifest --anchor "$ANCHOR" --set-id G3A_RING001 --topology ring --root-mode single --count 12 --exclude $EXCL --out ${M}_RING001_v0.1
python -m experiments.EXP_003.manifest --anchor "$ANCHOR" --set-id G3A_SOLO001 --topology solo --root-mode single --seeds-from ${M}_RING001_v0.1.json --out ${M}_SOLO001_v0.1
python -m experiments.EXP_003.manifest --anchor "$ANCHOR" --set-id G3A_DYAD001 --topology dyad --root-mode single --seeds-from ${M}_RING001_v0.1.json --out ${M}_DYAD001_v0.1
python -m experiments.EXP_003.manifest --anchor "$ANCHOR" --set-id G3A_BOUNCE001 --topology bounce --root-mode single --seeds-from ${M}_RING001_v0.1.json --out ${M}_BOUNCE001_v0.1
#    Set 002 (replication): same procedure with label G3A_RING002 and every Set 001 seed added to --exclude.
#    May be derived now or at Set 001 closure; the rule is fixed in the plan.
git add experiments/EXP_003/GATE_3A_MANIFEST_*; git commit -m "EXP-003 Gate 3A: freeze Set 001 world manifests"

# 4. Preflight the frozen plan end to end with stub agents. No calls.
python -m experiments.EXP_003.gate_orchestrator --plan experiments/EXP_003/GATE_3A_PLAN_v0.1.json --preflight --stage set_001
python -m experiments.EXP_003.gate_orchestrator --plan experiments/EXP_003/GATE_3A_PLAN_v0.1.json --preflight --status

# 5. Execute live, in frozen order, with a pacing cap. Resume by re-running until --status says closable.
OPENAI_API_KEY=... python -m experiments.EXP_003.gate_orchestrator --plan experiments/EXP_003/GATE_3A_PLAN_v0.1.json \
  --stage set_001 --adapter openai --live --max-worlds 4
python -m experiments.EXP_003.gate_orchestrator --plan experiments/EXP_003/GATE_3A_PLAN_v0.1.json --status
```

The orchestrator refuses live execution if the plan is not `FROZEN`, any anchor is empty, the plan or a manifest is uncommitted or edited, the manifest anchor differs from the plan's, or the runtime files differ from the frozen SHA.

Factor ledger (what changed between any two runs, gates or experiments; EXP-002 archives included):

```bash
python -m experiments.EXP_003.factors diff <run_dir_a> <run_dir_b>
python -m experiments.EXP_003.factors ledger experiments/EXP_002/results/archive experiments/EXP_003/results/archive
```

Tests:

```bash
python -m unittest discover -s tests -v
```

## Guardrails

- The EXP-002 tree is never written to. The retrospective tool only reads it.
- The runtime is frozen at tag `exp-003-protocol-v0.1` (`run.py`, `world_generator.py`, `lineage.py`, `metrics.py`, `models.py`, `prompting.py`, `provenance.py`, `topology.py`, `adapters/`, `prompts/`); the orchestrator refuses live execution if any of them differs from that commit. `tools/` is outside the freeze and holds the read-only audit chain.
- A gate's analysis rules are committed before its first outcome is read, and its outputs are committed in a later commit; the first place any number appears is a committed audit file.
- Stub output validates measurement only.
- Active results under `results/` are transient and Git-ignored; archived runs go under `results/archive/gate_3x/...` and are immutable.
