# EXP-003: Fan-in and Connected Hives

**Status:** DRAFT HARNESS AND PROSPECTIVE PLANS / NOT FROZEN / NO REAL-MODEL CALLS MADE

EXP-003 climbs a ladder of topologies, one structural change per rung: solo → dyad → ring → bounce → diamond → detached → bridged hives. It reuses the EXP-002 conditions, metrics and governance and adds the new shapes, a two-root positive control, non-interaction and unbridged controls, a perceived-source probe, mechanical provenance scoring, pre-registered replication sets, a second-provider model layer, a factor ledger and a gate orchestrator.

Read in this order:

1. [protocol.md](protocol.md): topologies, root modes, new metrics, model layer, execution and archival.
2. [GATE_3A_PLAN_v0.1.md](GATE_3A_PLAN_v0.1.md): four matched topologies (ring, solo, dyad, bounce) on the same worlds, same model, same day, with a pre-registered replication set. The EXP-002 ring runs are retrospective evidence only.
3. [GATE_3B_PLAN_v0.1.md](GATE_3B_PLAN_v0.1.md): diamond, the first fan-in, with the one-root versus two-root matrix, a probe reactivity check and a replication set.
4. [GATE_3C_PLAN_v0.1.md](GATE_3C_PLAN_v0.1.md): every 3A and 3B shape without re-grounding, paired by world.
5. [GATE_3D_PLAN_v0.1.md](GATE_3D_PLAN_v0.1.md): bridged hives with unbridged twins, shared and dual roots.
6. [results/README.md](results/README.md): archive contract.

Each markdown plan has a JSON twin (`GATE_3x_PLAN_v0.1.json`) that the orchestrator reads. Gates run in order; each requires the previous one closed (3D accepts 3C deferred with a recorded reason). A gate is never redesigned after its results are seen.

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

Each gate has a markdown plan (the science) and a JSON plan (the frozen configuration the orchestrator reads). Nothing below makes a model call until the last step.

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
- Nothing here is frozen. Freezing happens when the runtime commit is tagged `exp-003-protocol-v0.1` and a gate's manifest is committed, as in Gate 2B.
- Stub output validates measurement only.
- Active results under `results/` are transient and Git-ignored; archived runs go under `results/archive/gate_3x/...` and are immutable.
