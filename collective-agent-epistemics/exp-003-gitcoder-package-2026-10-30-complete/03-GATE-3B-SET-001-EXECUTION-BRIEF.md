# Execution brief: run EXP-003 Gate 3B, Set 001

Audience: the coding agent, after `01-GATE-3B-FREEZE-BRIEF.md` and `02-GATE-3B-ANALYSIS-PREREG-BRIEF.md` have both reported `COMPLETED` (plan FROZEN, six manifests committed, preflights passing, analysis spec and tool committed). Use only when the owner has sent, in writing, a line of exactly this form: `RUN GATE 3B SET 001 N=<integer>` (optionally `… RETRY <canonical world id>`). Never infer `N`.

This brief spends real money (OpenAI API calls) and produces scientific data. Follow it literally; every step states its success condition; stop at the first failure and report.

## What Set 001 is

Four arms in frozen order: `diamond_set_001` (12 worlds, probe on), `dual_root_set_001` (16 worlds, two roots, probe on), `solo_control_set_003` (12 worlds, probe on), `probe_off_set_001` (4 worlds, probe off). 44 worlds, 1356 provider calls. Set 002 (28 worlds, 924 calls) has its own brief and runs only after Set 001 passes its corpus audit and before any Set 001 outcome is read.

## Conventions

As in the Gate 3A execution brief: commands run from inside `collective-agent-epistemics/`; `<py>` as before; the key is never printed.

## Preconditions (stop and report the first that fails)

1. `git fetch origin && git checkout main && git pull --ff-only origin main && git status --short` prints nothing (or only root `*.patch`/`*.zip`/`*.md` package files).
2. Plan frozen: `<py> -c "import json; p=json.load(open('experiments/EXP_003/GATE_3B_PLAN_v0.1.json')); print(p['status'], [k for k,v in p['anchors'].items() if not v])"` prints `FROZEN []`.
3. Manifests committed and clean: `git ls-files experiments/EXP_003/GATE_3B_MANIFEST_*_v0.1.json | wc -l` prints `6`; `git status --short experiments/EXP_003/` prints nothing.
4. Analysis pre-registered before any call: `git log --oneline -1 -- experiments/EXP_003/GATE_3B_PRIMARY_OUTCOME_AUDIT_SPEC_v0.1.md experiments/EXP_003/tools/gate3b_primary_outcome_audit.py` prints one commit line. If it prints nothing, stop: brief 02 has not landed and no Gate 3B call may be made.
5. No Gate 3B data yet (first invocation only; on a later invocation after `PAUSED AT CAP` or a `RETRY` line, skip this check): `ls experiments/EXP_003/results/archive/gate_3b 2>&1` prints `No such file or directory`.
6. `git tag --list exp-003-protocol-v0.1` prints the tag.
7. `<py> -m unittest discover -s tests 2>&1 >/dev/null | tail -3` ends with `OK` (expect `Ran 145 tests`).
8. `<py> -c "import os; print('set' if os.getenv('OPENAI_API_KEY') else 'missing')"` prints `set`.
9. You hold the owner's instruction line. Record `N`.

## Steps

1. Preflight (no calls): `<py> -m experiments.EXP_003.gate_orchestrator --plan experiments/EXP_003/GATE_3B_PLAN_v0.1.json --preflight --stage set_001`. Success: exit 0, no `GateIntegrityError`.
2. Status before: `<py> -m experiments.EXP_003.gate_orchestrator --plan experiments/EXP_003/GATE_3B_PLAN_v0.1.json --status`. Keep the JSON.
3. Execute, capped at `N` new worlds, frozen order:
   ```bash
   <py> -m experiments.EXP_003.gate_orchestrator --plan experiments/EXP_003/GATE_3B_PLAN_v0.1.json \
     --stage set_001 --adapter openai --live --max-worlds N
   ```
   Outcomes as in Gate 3A: a pause line is expected; `GateIntegrityError` with `technical failure` means stop, commit what was archived (step 4), report the `failure_metadata.json` verbatim, and wait for a `RETRY` line; any other `GateIntegrityError` means nothing was spent, stop and report verbatim. Add `--authorize-retry` only when the owner's line carries `RETRY <id>` and the status shows exactly that one world failed.
4. Status after, then commit the archive:
   ```bash
   <py> -m experiments.EXP_003.gate_orchestrator --plan experiments/EXP_003/GATE_3B_PLAN_v0.1.json --status
   git add experiments/EXP_003/results/archive/gate_3b/
   git status --short
   ```
   Success: every staged path is under `experiments/EXP_003/results/archive/gate_3b/`; nothing under `gate_3a/` or outside `archive/` appears. Commit message: `EXP-003 Gate 3B Set 001: archive <n> world(s) in <sets>` with the body `Immutable attempt records written by gate_orchestrator under results/archive/gate_3b/. Frozen plan GATE_3B_PLAN_v0.1.json; no plan, manifest or runtime file changed.` Push; record the SHA.
5. If the status shows all four Set 001 sets `closable` and `all_required_sets_complete` is false only because Set 002 is pending, run the Set 001 corpus audit and commit it:
   ```bash
   <py> -m experiments.EXP_003.tools.corpus_audit --plan experiments/EXP_003/GATE_3B_PLAN_v0.1.json --stage set_001
   ```
   Success: `PASS: 44/44 worlds complete, 1356 calls, <k> failure record(s)`, exit 0. Commit the two files under `audits/gate_3b/` with message `EXP-003 Gate 3B Set 001: corpus integrity audit PASS (44/44 worlds, 1356 calls)`. Push. If `FAIL`: stop, report the problems, commit nothing.
6. Stop. Never run `--stage set_002` or a second `--stage set_001` without a new owner line. Never run `tools/gate3b_primary_outcome_audit.py` in this brief: it runs only under a later brief, after both Set 001 and Set 002 are archived and have passed their corpus audits.

## Never

- Never pass `--smoke`, `--fallbacks`, `--model`, `--reasoning-effort`, `--archive-root`, or `--arm`.
- Never edit the plan, a manifest, or any file under `experiments/EXP_003/` during or after execution.
- Never open an `events.jsonl` or `summary.csv`; never run analysis, summaries or audits other than the corpus audit in step 5.
- Never touch `results/archive/gate_3a/` or any Gate 3A audit.

## Report back

```
Outcome: PAUSED AT CAP | SET 001 COMPLETE | STOPPED AT STEP <n>
Owner instruction used: RUN GATE 3B SET 001 N=<integer>[ RETRY <id>]
Status before / after (JSON verbatim): <...>
Worlds executed this invocation: <canonical id -> archive path, one per line>
Sum of actual_model_call_count over those worlds: <integer>
Archive commit SHA: <sha>
Set 001 corpus audit (step 5): NOT RUN (not closable) | <first line verbatim> | commit <sha>
If a technical failure occurred: world id and the full failure_metadata.json, verbatim.
```
