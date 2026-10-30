# Brief: housekeeping commits and the Gate 3B freeze

Audience: the coding agent, on `main` at `1daa069af7000613ba06af35714bc22764c1f409` (Gate 3A closure). Read `00-README-FIRST.md` before this file.

Verified by the owner's assistant on a clean clone of that commit: every patch applies in this order, the suite passes (140 tests after step 5), the six Gate 3B manifests derive deterministically to the hashes in step 11, and the stub preflight of both stages passes.

No real-model call is made anywhere in this brief.

## Conventions

**Repository root** holds the top-level `README.md` and `collective-agent-epistemics/`. `<py>` is `python3` if 3.10 or newer, else `python`. Part 1 runs from the repository root; Part 2 from inside `collective-agent-epistemics/`. Every step ends with a success condition; the first unmet condition is a stop: send the report with the command and its full output, verbatim.

---

## Part 1: housekeeping commits (repository root)

1. Be on current `main`, clean.
   ```bash
   git fetch origin && git checkout main && git pull --ff-only origin main && git rev-parse HEAD && git status --short
   ```
   Success: HEAD prints `1daa069af7000613ba06af35714bc22764c1f409`; status prints nothing, or only `??` lines for `*.patch`, `*.zip`, `*.md` package files at the root. If HEAD differs, stop and report.
2. Verify every patch hash.
   ```bash
   sha256sum exp-003-patch-006-docs.patch exp-003-patch-008-manifest-inherit-first.patch exp-003-patch-009-origin-inbound-naming.patch exp-003-patch-010-observations-v0.2.patch
   ```
   Success, in order: `cd3c671fe17a9f26931a451ba16ce25481d4735bf6a340c21a32adde7785ae6c`, `25334518a5cafd606dfa0cc0e9dbecfa0118d2c1b12a0955e37b53b5a0251736`, `5910053f8cb67095a2b21e4956c14f12f1dd846dcc0778c9041c4f8298a4e0dd`, `d2c29d7b2410cb96f65d841f0e83c516cbd4cbffc79dc5f18b3b4496a98c302b`. Any mismatch: stop.
3. Docs commit.
   ```bash
   git apply --check exp-003-patch-006-docs.patch && git apply exp-003-patch-006-docs.patch && git diff --stat | tail -1
   ```
   Success: `5 files changed, 45 insertions(+), 13 deletions(-)`.
   ```bash
   git add README.md collective-agent-epistemics/README.md collective-agent-epistemics/experiments/EXP_003/README.md collective-agent-epistemics/experiments/EXP_003/protocol.md collective-agent-epistemics/research/README.md
   git commit -m "docs: record EXP-003 protocol freeze and Gate 3A closure in the indexes" -m "Status lines and index entries still described EXP-003 as a draft with no real-model calls. They now name the protocol tag, the Gate 3A closure tag and the committed archive, audits, synthesis and observations, and state that Gates 3B-3D remain draft. Markdown only; the protocol's content below its status line is unchanged."
   git push origin main && git rev-parse HEAD
   ```
   Success: push exits 0. Record the SHA.
4. Manifest tool commit.
   ```bash
   git apply --check exp-003-patch-008-manifest-inherit-first.patch && git apply exp-003-patch-008-manifest-inherit-first.patch && git diff --stat | tail -1
   ```
   Success: `2 files changed, 40 insertions(+), 5 deletions(-)`.
   ```bash
   git add collective-agent-epistemics/experiments/EXP_003/manifest.py collective-agent-epistemics/tests/test_exp003_orchestrator.py
   git commit -m "EXP-003 manifest: --inherit-first N for inherited sets" -m "Gate 3B's probe-off arm is 'the first 4 Arm 1 worlds in execution order'. build_manifest and the CLI gain inherit_first: with --seeds-from, take only the first N source worlds, verbatim seeds and order, recorded as selection.first. Without the flag nothing changes. manifest.py is a derivation tool outside the frozen runtime. Test added."
   git push origin main && git rev-parse HEAD
   ```
5. Origin-naming tool commit.
   ```bash
   git apply --check exp-003-patch-009-origin-inbound-naming.patch && git apply exp-003-patch-009-origin-inbound-naming.patch && git status --short | grep -c '^??'
   ```
   Success: prints `2` (two new files, nothing modified). Then run the suite from inside the project:
   ```bash
   (cd collective-agent-epistemics && <py> -m unittest discover -s tests 2>&1 >/dev/null | tail -3)
   ```
   Success: `Ran 140 tests` and `OK`.
   ```bash
   git add collective-agent-epistemics/experiments/EXP_003/tools/origin_inbound_naming.py collective-agent-epistemics/tests/test_exp003_origin_inbound_naming.py
   git commit -m "EXP-003 tools: tabulate origin firings against whether the inbound message named the sensor" -m "Read-only descriptive tool behind research/observations/EXP_003_gate_3a_observations_v0.2: for every post-seed firing of the source agent A in the Gate 3A archive, the archived provenance mark source_named of the inbound message against A's direction under the Gate 3A analysis rules. No test, no threshold; stages separate. Test on stub preflight data."
   git push origin main && git rev-parse HEAD
   ```
6. Observations v0.2 commit.
   ```bash
   git apply --check exp-003-patch-010-observations-v0.2.patch && git apply exp-003-patch-010-observations-v0.2.patch && git status --short
   ```
   Success: exactly one `??` line, `collective-agent-epistemics/research/observations/EXP_003_gate_3a_observations_v0.2_origin_messages.md`.
   ```bash
   git add collective-agent-epistemics/research/observations/EXP_003_gate_3a_observations_v0.2_origin_messages.md
   git commit -m "research: Gate 3A observations v0.2, the origin's inbound message and the sensor's name" -m "Qualitative reading of the 16 origin-inflation messages and 16 matched calibrated ones, plus the mechanical table over all 624 post-seed origin firings (tools/origin_inbound_naming.py): all 21 origin-inflation events followed an inbound message that did not name the sensor; 0 of 235 that did. Descriptive; changes nothing in Gate 3A; motivates one pre-registered secondary table in the Gate 3B analysis spec."
   git push origin main && git rev-parse HEAD
   ```
7. **Optional, visualization only. Skip unless the owner's instructions for this run say to apply patch 007.** If and only if they do: verify `c85103883345bed6a15fe42a3b04b7a0fe7b679eeffddee9dfbb8bad9a1bf1e7`, `git apply` it, confirm `git status --short | grep -c '^??'` prints `2`, regenerate with `(cd collective-agent-epistemics && <py> visualization/epistemic-hive/tools/build_gate3a_snapshot.py && git status --short | grep -v '^??' | wc -l)` expecting `wrote 9 files …` and `0`, then `git add collective-agent-epistemics/visualization/epistemic-hive/tools/build_gate3a_snapshot.py collective-agent-epistemics/visualization/epistemic-hive/public/data/gate3a`, commit with message `visualization: Gate 3A replay snapshots and research-index entry`, push.
8. Frozen runtime still intact (no output means intact):
   ```bash
   git diff --stat exp-003-protocol-v0.1 HEAD -- collective-agent-epistemics/experiments/EXP_003/run.py collective-agent-epistemics/experiments/EXP_003/world_generator.py collective-agent-epistemics/experiments/EXP_003/lineage.py collective-agent-epistemics/experiments/EXP_003/metrics.py collective-agent-epistemics/experiments/EXP_003/models.py collective-agent-epistemics/experiments/EXP_003/prompting.py collective-agent-epistemics/experiments/EXP_003/provenance.py collective-agent-epistemics/experiments/EXP_003/topology.py collective-agent-epistemics/experiments/EXP_003/adapters collective-agent-epistemics/experiments/EXP_003/prompts
   ```

---

## Part 2: freeze Gate 3B (inside `collective-agent-epistemics/`)

The plan `GATE_3B_PLAN_v0.1.{md,json}` is **not edited** except for its anchors and status, by the scripts below, exactly as Gate 3A was frozen. Arms, worlds, matrix, expectations and accounting stay as committed.

9. Anchor-fill commit (anchors only; status stays DRAFT in this commit).
   ```bash
   cd collective-agent-epistemics
   <py> - <<'EOF'
   import json
   path = "experiments/EXP_003/GATE_3B_PLAN_v0.1.json"
   p = json.load(open(path))
   assert p["status"] == "DRAFT" and p["anchors"]["plan_freeze_commit"] is None
   p["anchors"]["gate3a_closure_checkpoint"] = "1daa069af7000613ba06af35714bc22764c1f409"
   p["anchors"]["frozen_runtime"] = "c54563bbb3f17e49c70e8e4f2e3a0369910d3c15"
   p["anchors"]["derivation_anchor"] = "1daa069af7000613ba06af35714bc22764c1f409|exp-003-protocol-v0.1|GATE_3B_PLAN_v0.1"
   open(path, "w").write(json.dumps(p, indent=2) + "\n")
   EOF
   git diff --stat | tail -1
   git show HEAD:experiments/EXP_003/GATE_3B_PLAN_v0.1.json | <py> -c "import json,sys; a=json.load(sys.stdin); b=json.load(open('experiments/EXP_003/GATE_3B_PLAN_v0.1.json')); a.pop('anchors'); b.pop('anchors'); print('IDENTICAL APART FROM ANCHORS' if a==b else 'DIFFER')"
   ```
   Success: the stat names only `GATE_3B_PLAN_v0.1.json` (the file is re-serialized with two-space indentation, so the line count is large; that is expected) and the comparison prints `IDENTICAL APART FROM ANCHORS`. Then:
   ```bash
   git add experiments/EXP_003/GATE_3B_PLAN_v0.1.json
   git commit -m "EXP-003 Gate 3B: fill plan anchors (Gate 3A closure 1daa069, runtime c54563b, derivation anchor)" -m "Anchors only; status remains DRAFT until the next commit names this one as plan_freeze_commit. No arm, world count, matrix line or expectation changed."
   git push origin main && FREEZE=$(git rev-parse HEAD) && echo "anchor-fill commit: $FREEZE"
   ```
10. Status-flip commit naming the anchor-fill commit.
    ```bash
    <py> - "$FREEZE" <<'EOF'
    import json, sys
    path = "experiments/EXP_003/GATE_3B_PLAN_v0.1.json"
    p = json.load(open(path))
    p["anchors"]["plan_freeze_commit"] = sys.argv[1]
    p["status"] = "FROZEN"
    assert all(p["anchors"].values())
    open(path, "w").write(json.dumps(p, indent=2) + "\n")
    md = "experiments/EXP_003/GATE_3B_PLAN_v0.1.md"
    t = open(md).read()
    old = "**PLAN DRAFT / NOT FROZEN / NOT EXECUTED**\n\nGate 3B may be frozen only after Gate 3A is closed. It adds the fourth agent."
    new = ("**FROZEN.** Anchors filled and JSON twin set to `FROZEN` in the freeze commits (anchor fill `" + sys.argv[1]
           + "`; this status flip names that commit as `plan_freeze_commit`). Gate 3A is closed (`exp-003-gate3a-closed-v0.1`). "
           "No Gate 3B real-model call had been made before this commit.")
    assert t.count(old) == 1
    open(md, "w").write(t.replace(old, new))
    EOF
    git show HEAD:experiments/EXP_003/GATE_3B_PLAN_v0.1.json | <py> -c "import json,sys; a=json.load(sys.stdin); b=json.load(open('experiments/EXP_003/GATE_3B_PLAN_v0.1.json')); [d.pop(k) for d in (a,b) for k in ('anchors','status')]; print('IDENTICAL APART FROM ANCHORS AND STATUS' if a==b else 'DIFFER')"
    git add experiments/EXP_003/GATE_3B_PLAN_v0.1.json experiments/EXP_003/GATE_3B_PLAN_v0.1.md
    git commit -m "EXP-003 Gate 3B: plan status FROZEN" -m "plan_freeze_commit names the anchor-fill commit. The Markdown status block is updated to match; no other line of the plan changed."
    git push origin main && git rev-parse HEAD
    ```
    Success: the comparison prints `IDENTICAL APART FROM ANCHORS AND STATUS`; push exits 0.
11. Derive the six manifests. Zero model calls. Exclusions: seed 42, the 20 Gate 2B seeds, all 24 Gate 3A seeds (45 in total); Set 002 additionally excludes every Set 001 seed (73 in total). Dual-root stratification: 2 worlds per `truth/E1/E2` cell over the 8 cells.
    ```bash
    ANCHOR="1daa069af7000613ba06af35714bc22764c1f409|exp-003-protocol-v0.1|GATE_3B_PLAN_v0.1"
    EXCL="42 $(<py> -c "import json;m=json.load(open('experiments/EXP_002/GATE_2B_WORLD_MANIFEST_v0.1.json'));print(' '.join(str(w['seed']) for s in ('generalization_set_001','stress_set_001') for w in m[s]['worlds']))") $(<py> -c "import json;print(' '.join(str(w['seed']) for f in ('RING001','RING002') for w in json.load(open(f'experiments/EXP_003/GATE_3A_MANIFEST_{f}_v0.1.json'))['worlds']))")"
    echo "$EXCL" | wc -w
    M=experiments/EXP_003/GATE_3B_MANIFEST
    CELLS="A/A/A A/A/B A/B/A A/B/B B/A/A B/A/B B/B/A B/B/B"
    <py> -m experiments.EXP_003.manifest --anchor "$ANCHOR" --set-id G3B_GEN001 --topology diamond --root-mode single --count 12 --exclude $EXCL --out ${M}_GEN001_v0.1
    <py> -m experiments.EXP_003.manifest --anchor "$ANCHOR" --set-id G3B_DUAL001 --topology diamond --root-mode dual --per-cell 2 --cells $CELLS --exclude $EXCL --out ${M}_DUAL001_v0.1
    <py> -m experiments.EXP_003.manifest --anchor "$ANCHOR" --set-id G3B_SOLO003 --topology solo --root-mode single --seeds-from ${M}_GEN001_v0.1.json --out ${M}_SOLO003_v0.1
    <py> -m experiments.EXP_003.manifest --anchor "$ANCHOR" --set-id G3B_PROBEOFF001 --topology diamond --root-mode single --seeds-from ${M}_GEN001_v0.1.json --inherit-first 4 --out ${M}_PROBEOFF001_v0.1
    EXCL2="$EXCL $(<py> -c "import json;print(' '.join(str(w['seed']) for f in ('GEN001','DUAL001') for w in json.load(open(f'experiments/EXP_003/GATE_3B_MANIFEST_{f}_v0.1.json'))['worlds']))")"
    echo "$EXCL2" | wc -w
    <py> -m experiments.EXP_003.manifest --anchor "$ANCHOR" --set-id G3B_GEN002 --topology diamond --root-mode single --count 12 --exclude $EXCL2 --out ${M}_GEN002_v0.1
    <py> -m experiments.EXP_003.manifest --anchor "$ANCHOR" --set-id G3B_DUAL002 --topology diamond --root-mode dual --per-cell 2 --cells $CELLS --exclude $EXCL2 --out ${M}_DUAL002_v0.1
    sha256sum ${M}_GEN001_v0.1.json ${M}_DUAL001_v0.1.json ${M}_SOLO003_v0.1.json ${M}_PROBEOFF001_v0.1.json ${M}_GEN002_v0.1.json ${M}_DUAL002_v0.1.json
    ```
    Success: the two counts print `45` and `73`; each derivation prints `wrote …`; the six JSON hashes are, in order:
    ```
    f607a0365e20d50077831e03d268fae262f6aeb18af83f79cdd304fb8cf6d9aa  GEN001      (12 worlds, unfiltered)
    956f555d49d2b32e4cf7790467709f330f1247895335b814d2074398a17c8eb1  DUAL001     (16 worlds, 2 per cell)
    5d34fb7e3986398a4354a09e45c5699d9dc145aaa5592d44703d76bbf908bee2  SOLO003     (12 worlds, inherited from GEN001)
    59b5edd097120e1c0532699570a4a0b0a4ae1d3fc0fbf7b1c964be310c2dc015  PROBEOFF001 (4 worlds, inherited, first 4)
    2449fcb6556202c2d1e0cc0d375efb5e0f55dca2a5a8a82f52a794cb20c1f041  GEN002      (12 worlds, unfiltered)
    26f224f13df358b60995e1554b9b72a120ead5406c04e991a9f91daddefbda2c  DUAL002     (16 worlds, 2 per cell)
    ```
    Any hash differing: stop and report; do not commit. The derivation is deterministic from the anchor and the exclusions, so a difference means an input differs.
12. Commit the manifests; run the suite, both preflights, and the preflight corpus audit.
    ```bash
    git add experiments/EXP_003/GATE_3B_MANIFEST_*
    git commit -m "EXP-003 Gate 3B: freeze the six world manifests (Set 001 and Set 002)" -m "Derived with manifest.py from anchor 1daa069…|exp-003-protocol-v0.1|GATE_3B_PLAN_v0.1 with zero model calls. Exclusions: 42, the 20 Gate 2B seeds, all 24 Gate 3A seeds; Set 002 also excludes every Set 001 seed. GEN001/GEN002 unfiltered 12; DUAL001/DUAL002 stratified 2 per truth/E1/E2 cell, 16; SOLO003 inherits GEN001; PROBEOFF001 inherits the first 4 GEN001 worlds."
    git push origin main && git rev-parse HEAD
    <py> -m unittest discover -s tests 2>&1 >/dev/null | tail -3
    <py> -m experiments.EXP_003.gate_orchestrator --plan experiments/EXP_003/GATE_3B_PLAN_v0.1.json --preflight --stage set_001 2>&1 | grep -v "order=" | tail -5
    <py> -m experiments.EXP_003.gate_orchestrator --plan experiments/EXP_003/GATE_3B_PLAN_v0.1.json --preflight --stage set_002 2>&1 | grep -v "order=" | tail -3
    <py> -m experiments.EXP_003.tools.corpus_audit --plan experiments/EXP_003/GATE_3B_PLAN_v0.1.json --stage set_001 --preflight --out-dir /tmp/g3b-preflight-audit | head -1
    git status --short
    ```
    Success: `Ran 140 tests`, `OK`; the first preflight lists `diamond_set_001` 12 worlds / `dual_root_set_001` 16 / `solo_control_set_003` 12 / `probe_off_set_001` 4 with no `GateIntegrityError`; the second lists `diamond_set_002` 12 / `dual_root_set_002` 16; the audit prints `PASS: 44/44 worlds complete, 1356 calls, 0 failure record(s)`; final status prints nothing (preflight output is Git-ignored).
13. Stop and report. Do not run anything with `--live`. Gate 3B execution needs its own brief and the owner's line `RUN GATE 3B SET 001 N=<integer>`.

## Never

- Never edit any line of `GATE_3B_PLAN_v0.1.{md,json}` other than the anchors and the status block as scripted above.
- Never pass `--live` or `--adapter openai`; never run any command under `experiments/EXP_002/`.
- Never create or move a tag in this brief.
- Never touch `results/archive/`, any Gate 3A file, or the frozen runtime.

## Report back

```
Outcome: COMPLETED | STOPPED AT STEP <n>
main HEAD before (1): <sha>
Commits: docs (3) <sha> · manifest tool (4) <sha> · origin tool (5) <sha> · observations (6) <sha> · visualization (7) <sha or SKIPPED>
Runtime drift check (8): <"no output" or verbatim>
Anchor-fill commit (9): <sha>   Status-flip commit (10): <sha>
Exclusion counts (11): <45> <73>   Manifest hashes (11): MATCH ALL SIX | <which differ>
Manifests commit (12): <sha>   Tests: <last two lines>   Preflight set_001 / set_002: OK | <output>   Preflight corpus audit: <first line>
If stopped: the command and its full output, verbatim.
```
