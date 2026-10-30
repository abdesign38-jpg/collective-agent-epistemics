# EXP-003 complete package for the coding agent: housekeeping, Gate 3B freeze, analysis pre-registration, Set 001 execution

Read this file first. It says what is in the package, the exact order to use it, the rules that never bend, and where you must stop and wait for the owner. This package replaces every earlier EXP-003 package; if you hold an older one, discard it.

## Who decides what

- **You execute. You do not decide.** Every step in every brief has a literal success condition. If a step does not meet it, stop, do not try an alternative, and send the brief's report template filled in. "Close enough" is a stop.
- **The owner decides** anything that touches the science: which gate runs, when, how many worlds (`N`), whether a failed world is retried, whether a verdict or a rule is accepted. These decisions arrive only as written owner instruction lines quoted in the briefs. Never infer one.
- **Nothing in a frozen file is ever edited**: `GATE_3A_*`, `GATE_3B_PLAN_v0.1.{md,json}` beyond the two scripted anchor/status edits in brief 01, any manifest, anything under `results/archive/`, any `audits/` file already committed, the frozen runtime (`run.py`, `world_generator.py`, `lineage.py`, `metrics.py`, `models.py`, `prompting.py`, `provenance.py`, `topology.py`, `adapters/`, `prompts/`).
- **Patches are applied as given.** Verify the SHA-256 before applying; a mismatch is a stop. Never edit a patch, never hand-edit a file a patch touches, never resolve a conflict yourself.
- **No model call without an owner line** of the form `RUN GATE 3B SET 001 N=<integer>` (optionally `RETRY <canonical world id>`). Briefs 01 and 02 contain no live call at all.
- **Never read outcomes.** Do not open, print, quote or summarize `events.jsonl`, `summary.csv`, or any audit output beyond the single first line a brief tells you to report. The owner reads committed files.
- **Report verbatim.** Commands and outputs in reports are copied, not paraphrased.

## Order of use

| # | Brief | What it does | Needs an owner line? | Model calls | Then |
|---|---|---|---|---|---|
| 01 | `01-GATE-3B-FREEZE-BRIEF.md` | Part 1: four housekeeping commits (patches 006, 008, 009, 010; 007 only if the owner says so). Part 2: fill the Gate 3B plan anchors, flip the status to FROZEN, derive and commit the six manifests, run preflights. | No | None | Stop and report |
| 02 | `02-GATE-3B-ANALYSIS-PREREG-BRIEF.md` | Commit the owner-confirmed Gate 3B analysis spec, the tool that implements it and its tests (patch 011). Must land before the first Gate 3B model call. | No | None | Stop and report |
| 03 | `03-GATE-3B-SET-001-EXECUTION-BRIEF.md` | Run Set 001 (44 worlds, 1356 calls) capped at `N`, commit the archive, run the Set 001 corpus audit when all four sets are complete. | **Yes**: `RUN GATE 3B SET 001 N=<integer>` | Yes, paid | Stop and report after each invocation |

Each brief checks that the previous one landed; run them strictly in this order and never start the next until the previous one's report says COMPLETED and the owner has answered. After Set 001, the owner will send a separate brief for Set 002, and only after both stages are archived and corpus-audited will a further brief run the primary-outcome audits. None of that is in this package.

Why the order matters: the analysis rules in brief 02 must be in git before the first Gate 3B model call in brief 03, so that nobody, including the owner, can be suspected of choosing a rule after seeing a value.

## Package contents

| File | SHA-256 | Used by | Purpose |
|---|---|---|---|
| `00-README-FIRST.md` | (this file) | you | This file |
| `01-GATE-3B-FREEZE-BRIEF.md` | (this package) | step 1 | Housekeeping commits and the Gate 3B freeze |
| `02-GATE-3B-ANALYSIS-PREREG-BRIEF.md` | (this package) | step 2 | Analysis pre-registration commit |
| `03-GATE-3B-SET-001-EXECUTION-BRIEF.md` | (this package) | step 3 | Set 001 execution, only with the owner's line |
| `exp-003-patch-006-docs.patch` | `cd3c671fe17a9f26931a451ba16ce25481d4735bf6a340c21a32adde7785ae6c` | brief 01, Part 1 | 5 Markdown files; status lines and indexes |
| `exp-003-patch-008-manifest-inherit-first.patch` | `25334518a5cafd606dfa0cc0e9dbecfa0118d2c1b12a0955e37b53b5a0251736` | brief 01, Part 1 | manifest tool: `--inherit-first N` (+ test); required for the freeze and for patch 011's tests |
| `exp-003-patch-009-origin-inbound-naming.patch` | `5910053f8cb67095a2b21e4956c14f12f1dd846dcc0778c9041c4f8298a4e0dd` | brief 01, Part 1 | read-only tabulation tool (+ test) behind observations v0.2 |
| `exp-003-patch-010-observations-v0.2.patch` | `d2c29d7b2410cb96f65d841f0e83c516cbd4cbffc79dc5f18b3b4496a98c302b` | brief 01, Part 1 | `research/observations/EXP_003_gate_3a_observations_v0.2_origin_messages.md` |
| `exp-003-patch-007-hive-data.patch` | `c85103883345bed6a15fe42a3b04b7a0fe7b679eeffddee9dfbb8bad9a1bf1e7` | brief 01, Part 1, step 7 | **optional, visualization only**; apply only if the owner says so |
| `exp-003-patch-011-gate3b-analysis-prereg.patch` | `88f1408e265a3bdc26c69d23b07cb5478e2b6484aeb1e998ee07c316c38af92d` | brief 02 | Gate 3B analysis spec v0.1, `tools/gate3b_primary_outcome_audit.py`, its tests |

All patches were verified to apply in this order on a clean checkout of `main` at `1daa069af7000613ba06af35714bc22764c1f409` (the Gate 3A closure), with the full suite passing afterwards: 140 tests after brief 01, 145 after brief 02.

## Environment

Python 3.10 or newer. Once per machine: `pip install -r collective-agent-epistemics/requirements.txt`. The `OPENAI_API_KEY` environment variable is needed only by brief 03 and must never be printed, logged or written to a file. All patches are placed at the repository root (the directory containing the top-level `README.md` and `collective-agent-epistemics/`) and are never committed.
