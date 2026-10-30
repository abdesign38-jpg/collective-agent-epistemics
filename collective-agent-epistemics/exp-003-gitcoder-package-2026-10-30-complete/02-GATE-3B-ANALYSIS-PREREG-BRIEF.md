# Brief: pre-register the Gate 3B analysis (spec, tool, tests) before any Gate 3B model call

Audience: the coding agent, on `main` after `01-GATE-3B-FREEZE-BRIEF.md` reported COMPLETED (Parts 1 and 2). Read `00-README-FIRST.md` in this package before this file.

Purpose: commit the owner-confirmed analysis specification for Gate 3B together with the tool that implements it and that tool's tests, so that git history shows every verdict rule existed before any Gate 3B value did. This brief makes **no real-model call**, reads **no archive**, and writes nothing under `results/` or `audits/`.

Verified by the owner's assistant on a clean clone of `1daa069af7000613ba06af35714bc22764c1f409` with the freeze brief's patches 006, 008, 009 and 010 applied: the patch applies, the suite passes (145 tests), and the tool refuses to run when no corpus audit record exists.

## Conventions

**Repository root** holds the top-level `README.md` and `collective-agent-epistemics/`. `<py>` is `python3` if 3.10 or newer, else `python`. Steps 1 to 3 and 6 run from the repository root; steps 4 and 5 from inside `collective-agent-epistemics/`. Every step ends with a success condition; the first unmet condition is a stop: send the report with the command and its full output, verbatim. Never try an alternative.

---

## Steps

1. Be on current `main`, clean, with the freeze landed and no Gate 3B data anywhere.
   ```bash
   git fetch origin && git checkout main && git pull --ff-only origin main && git rev-parse HEAD && git status --short
   <py> -c "import json;p=json.load(open('collective-agent-epistemics/experiments/EXP_003/GATE_3B_PLAN_v0.1.json'));print(p['status'], p['anchors']['plan_freeze_commit'])"
   grep -c inherit_first collective-agent-epistemics/experiments/EXP_003/manifest.py
   ls collective-agent-epistemics/experiments/EXP_003/results/archive/gate_3b collective-agent-epistemics/experiments/EXP_003/audits/gate_3b 2>&1
   ```
   Success: status prints nothing, or only `??` lines for `*.patch`, `*.zip`, `*.md` package files at the root; the second command prints `FROZEN` followed by a 40-character SHA; the third prints a number of 1 or more; the fourth prints two `No such file or directory` lines and nothing else. Record HEAD. If the plan status is not `FROZEN`, or either directory exists, stop: the freeze brief has not completed, or a Gate 3B call has already been made, and the owner must decide.

2. Verify the patch hash.
   ```bash
   sha256sum exp-003-patch-011-gate3b-analysis-prereg.patch
   ```
   Success: `88f1408e265a3bdc26c69d23b07cb5478e2b6484aeb1e998ee07c316c38af92d`. Any other value: stop.

3. Apply the patch and verify the three new files.
   ```bash
   git apply --check exp-003-patch-011-gate3b-analysis-prereg.patch && git apply exp-003-patch-011-gate3b-analysis-prereg.patch && git status --short
   sha256sum collective-agent-epistemics/experiments/EXP_003/GATE_3B_PRIMARY_OUTCOME_AUDIT_SPEC_v0.1.md collective-agent-epistemics/experiments/EXP_003/tools/gate3b_primary_outcome_audit.py collective-agent-epistemics/tests/test_exp003_gate3b_primary_outcome_audit.py
   ```
   Success: status shows exactly these three new lines (plus any package files from step 1) and no ` M` line:
   ```
   ?? collective-agent-epistemics/experiments/EXP_003/GATE_3B_PRIMARY_OUTCOME_AUDIT_SPEC_v0.1.md
   ?? collective-agent-epistemics/experiments/EXP_003/tools/gate3b_primary_outcome_audit.py
   ?? collective-agent-epistemics/tests/test_exp003_gate3b_primary_outcome_audit.py
   ```
   and the hashes are, in order:
   `c7c60953a8139104f15e617fbe3b4d2b6896a51c641144a27da914257f2ca1c7`,
   `6fde748d27612ed559f4ecfdb6395da8e1ec1957a2a2f4f7814e54c9f3f1c086`,
   `b4a6a0a0ba7ca747dcf37e5ffb36f2104cec64dc4138a4c34b0347529df83601`.

4. Run the whole suite (inside `collective-agent-epistemics/`). The new tests run the tool on deterministic stub data only.
   ```bash
   cd collective-agent-epistemics && <py> -m unittest discover -s tests 2>&1 | tail -3
   ```
   Success: `Ran 145 tests`, then `OK`. Any failure or error: stop; do not edit anything.

5. Confirm the tool refuses to run against the empty gate (still inside `collective-agent-epistemics/`). This reads nothing and writes nothing.
   ```bash
   <py> -m experiments.EXP_003.tools.gate3b_primary_outcome_audit --stage set_001; echo "exit $?"
   ls experiments/EXP_003/audits/
   git status --short
   ```
   Success: one line starting `corpus audit record missing:` and ending `run corpus_audit first`, then `exit 1`; the listing prints only `gate_3a`; status is unchanged from step 3 (no new directory or file appeared).

6. Commit and push (from the repository root).
   ```bash
   cd .. && git add collective-agent-epistemics/experiments/EXP_003/GATE_3B_PRIMARY_OUTCOME_AUDIT_SPEC_v0.1.md collective-agent-epistemics/experiments/EXP_003/tools/gate3b_primary_outcome_audit.py collective-agent-epistemics/tests/test_exp003_gate3b_primary_outcome_audit.py
   git commit -m "EXP-003 Gate 3B: pre-register the primary-outcome analysis (spec v0.1, tool, tests)" -m "Owner-confirmed items D1-D5 on 2026-10-30, before any Gate 3B model call. The spec turns the frozen plan's primary outcomes and expectations E1-E7 into mechanical rules over archived fields: the Gate 3A direction rule for single-root arms; for the dual-root arm a favored-state certainty excess when the reference is not .5 and a signed departure from even with no discount/inflation label when it is, agreeing and conflicting strata never pooled; E7 assessed only in the synthesis. tools/gate3b_primary_outcome_audit.py computes exactly those tables and verdicts, requires a PASS corpus audit, cross-checks stored metrics against raw output with the frozen runtime's functions, and writes repository-relative paths only. Tests run on deterministic stub data. No plan, manifest, archive or runtime file changed."
   git push origin main && git rev-parse HEAD && git status --short
   ```
   Success: the push is accepted, a SHA prints, and status prints nothing (or only the package files). Record the SHA; it is the Gate 3B analysis pre-registration commit and must precede any commit under `results/archive/gate_3b/`.

7. Stop and report. Do not run anything with `--live`. Gate 3B execution still needs the owner's line `RUN GATE 3B SET 001 N=<integer>` and `03-GATE-3B-SET-001-EXECUTION-BRIEF.md`.

## Never

- Never edit the patch, or any file it creates, or any file under `experiments/EXP_003/` that it does not create.
- Never pass `--live` or `--adapter openai`; never run the audit tool with `--archive-root` pointing at anything; never run any command under `experiments/EXP_002/`.
- Never create or move a tag in this brief.
- Never touch `results/archive/`, `audits/gate_3a/`, any Gate 3A file, `GATE_3B_PLAN_v0.1.{md,json}`, any manifest, or the frozen runtime.

## Report back

```
Outcome: COMPLETED | STOPPED AT STEP <n>
main HEAD before (1): <sha>   Plan status (1): <FROZEN sha>   gate_3b dirs (1): absent | PRESENT
Patch hash (2): MATCH | <value>
File hashes (3): MATCH ALL THREE | <which differ>
Tests (4): <last two lines>
Refusal check (5): <first line> / exit <code> / audits listing: <output>
Pre-registration commit (6): <sha>
If stopped: the command and its full output, verbatim.
```
