# EXP-002 Gate 2B Prospective Multi-World Plan v0.1

## Status

**PLAN FROZEN / NOT YET EXECUTED**

This document defines the prospective Gate 2B design before any Gate 2B real-model call is made.

Gate 2A remains closed. This plan does not modify the historical hypothesis, the frozen EXP-002 runtime, prompts, topology, metrics, lineage semantics, or stopping logic.

## Scientific anchors

- Research closure checkpoint: `de62984adc44566b513545feaf2d61fcc229e71c`
- Frozen EXP-002 runtime: `7e9aed1b7093baae10ae30f27e0b6a2b932f92f5`
- Frozen protocol tag: `exp-002-protocol-v0.1`
- Model: `gpt-5.6-sol`
- Reasoning effort: `medium`
- Execution policy: `paired`
- Rounds: `4`
- Sensor reliability: `0.70`

## Gate 2B question

> Do the architecture-dependent epistemic behaviors observed under W01 survive when the external world/evidence realization changes while the frozen EXP-002 communication protocol remains otherwise controlled?

Gate 2B changes the external world/evidence realization and nothing else.

It is **not** a DSCD experiment, a source-holder experiment, a depth intervention, a causal mechanism experiment, or a new architecture experiment.

The purpose is to determine whether W01-specific observations remain, disappear, reverse, or become condition-dependent across controlled changes in truth and evidence correctness.

## Relationship to the historical hypothesis

Gate 2B is informative whether the historical hypothesis is strengthened, weakened, narrowed, or contradicted.

The experiment is not designed to preserve the W01 effect.

Valid scientific outcomes include:

- architecture differences persisting across worlds;
- architecture differences disappearing;
- FREE developing numerical drift;
- confidence inflation appearing;
- answer flips appearing;
- source-holder patterns disappearing;
- LINEAGE improving calibration in some worlds;
- LINEAGE worsening calibration in some worlds;
- MACRO truncation becoming beneficial, harmful, or neutral depending on the world;
- no meaningful architecture difference surviving multi-world variation.

No result may trigger post-hoc world replacement, sample extension, threshold selection, or redefinition of replication success.

## Controlled configuration

The following remain unchanged from frozen EXP-002 v0.1:

- model and reasoning effort;
- paired execution policy;
- prompts and schema;
- agent identities;
- seed and recursive topology semantics;
- FREE / LINEAGE / MACRO definitions;
- hidden actual-lineage semantics;
- visible lineage envelope semantics;
- periodic direct re-grounding of Agent A in E1;
- maximum recursion rounds;
- metrics;
- MACRO stop semantics;
- MACRO reuse of LINEAGE responses.

The only intended experimental variation is the generated world:

- truth;
- sensor observation;
- therefore whether E1 is aligned with or misleading about truth.

## Primary outcomes

Preserve the original EXP-002 outcome family:

- answer trajectory;
- confidence trajectory;
- `P(A)` trajectory;
- Brier trajectory;
- accuracy;
- actual independent evidence roots;
- inference depth;
- `P(A)` changes without new independent evidence;
- message transformations;
- FREE versus LINEAGE behavior;
- MACRO stopping behavior.

Evidence alignment (`aligned` versus `misleading`) is a **predefined stratifier**, not a new endpoint.

## Secondary exploratory observations

Track separately and do not use them to define Gate 2B success:

- transient numerical confidence discounting / DSCD;
- confidence inflation;
- answer flips;
- FREE natural-language dependency recognition;
- source-holder / Agent A effects;
- re-grounding behavior;
- actor-specific numerical discount patterns;
- depth-sensitive language.

No secondary observation may alter the run plan while Gate 2B is in progress.

# 1. TWO-SET DESIGN

Gate 2B contains two scientifically distinct sets.

They must be analyzed and reported separately.

Their counts must **not** be pooled into a single headline prevalence such as `X/20`, because the two sets use different selection schemes.

## A. Generalization Set 001

**Purpose:** unfiltered multi-world generalization.

**Planned worlds:** 12.

World selection is independent of truth, observed state, evidence alignment, expected DSCD behavior, confidence behavior, and architecture behavior.

This is the primary Gate 2B generalization component.

## B. Stress Set 001

**Classification:** **TARGETED / PROSPECTIVELY STRATIFIED STRESS TEST**

**Purpose:** guarantee controlled coverage of the four possible truth × observation cells.

**Planned worlds:** 8 total, 2 per cell:

1. truth A / observation A;
2. truth B / observation B;
3. truth A / observation B;
4. truth B / observation A.

This set is intentionally stratified and must not be described as an unbiased population sample.

Its purpose is conditional robustness, not prevalence estimation.

# 2. PROSPECTIVE SEED DERIVATION

## Immutable derivation anchor

Use the exact ASCII anchor:

```text
de62984adc44566b513545feaf2d61fcc229e71c|exp-002-protocol-v0.1|GATE_2B_PLAN_v0.1
```

Define:

```python
MAX_SEED = 2_147_483_646

def candidate_seed(label: str, ordinal: int, nonce: int = 0) -> int:
    payload = f"{ANCHOR}|{label}|{ordinal}|{nonce}".encode("utf-8")
    digest = sha256(payload).digest()
    value = int.from_bytes(digest[:8], "big")
    return 1 + (value % MAX_SEED)
```

This produces seeds in `[1, 2_147_483_646]`.

## Pre-existing inspection exclusion

A seed is excluded from the unbiased Generalization Set if there is documentary evidence that the world was inspected before this plan was frozen.

Known baseline exclusion:

```text
42
```

Additional exclusions may be added before the world manifest is frozen **only** when there is verifiable documentation predating this plan showing that the seed/world had already been inspected.

Each such exclusion must record:

- seed;
- source;
- source timestamp or commit;
- reason.

A seed may not be excluded because its generated truth, observation, alignment, or anticipated model behavior appears inconvenient.

# 3. GENERALIZATION SET 001 SELECTION ALGORITHM

For ordinals `1..12`:

1. Set `nonce = 0`.
2. Compute `candidate_seed("GEN001", ordinal, nonce)`.
3. Reject only if the candidate:
   - is in the pre-existing inspection exclusion registry; or
   - duplicates an already accepted Generalization seed.
4. On rejection, increment `nonce` by 1 and repeat.
5. Accept the first candidate satisfying those constraints.
6. **Do not generate or inspect that world's truth or observed state as part of the acceptance decision.**

After all 12 seeds are selected, generate the worlds locally using the frozen `WorldGenerator`.

Truth and observed state are then recorded, but they do not change membership.

No world may be replaced because it is redundant, uninteresting, aligned, misleading, or fails to reproduce a prior observation.

# 4. STRESS SET 001 SELECTION ALGORITHM

Stress Set selection begins only after the 12 Generalization seeds are fixed.

Define a deterministic candidate stream:

```python
candidate_seed("STRESS001", scan_index, 0)
```

for `scan_index = 1, 2, 3, ...`.

For each candidate in order:

1. Reject if it:
   - is in the pre-existing inspection exclusion registry;
   - is already in Generalization Set 001;
   - duplicates an already evaluated Stress candidate.
2. Generate the world locally using the frozen `WorldGenerator`.
3. Classify it using **only**:
   - `truth`;
   - `observed_state`.
4. Map it to one of:
   - A/A;
   - B/B;
   - A/B;
   - B/A.
5. Accept the candidate if its cell has fewer than 2 accepted worlds.
6. Otherwise mark it `cell_full` and continue.
7. Stop when every cell contains exactly 2 accepted worlds.

No model output, expected confidence behavior, DSCD expectation, message content, or architecture behavior may be used during Stress selection.

The complete candidate scan, including rejected candidates and rejection reasons, must be recorded in the world manifest.

# 5. WORLD MANIFEST FREEZE

This plan commit precedes all Gate 2B world selection.

A second pre-execution artifact must then be created:

```text
experiments/EXP_002/GATE_2B_WORLD_MANIFEST_v0.1.md
experiments/EXP_002/GATE_2B_WORLD_MANIFEST_v0.1.json
```

The manifest step may execute the deterministic local `WorldGenerator`.

It must make **zero real-model calls**.

The manifest must contain the exact:

- set;
- canonical world identity;
- world seed;
- internal world_id;
- truth;
- observed state;
- evidence alignment;
- sensor reliability;
- evidence root;
- execution order key;
- selection/rejection provenance where applicable.

The manifest must be committed before the first Gate 2B model call.

After that commit, the world list is immutable.

# 6. CANONICAL WORLD IDENTITY

Do not rely on runtime `world_id` alone as the scientific identity.

Use:

```text
G2B_<SET_ID>_seed_<SEED>
```

Examples:

```text
G2B_GEN001_seed_123456
G2B_STRESS001_seed_987654
```

The canonical identity must be preserved in the manifest and archive path.

This avoids ambiguity if separate executions internally reuse names such as `EXP_002_W01`.

# 7. EXECUTION ORDER

Execution order must be frozen before model calls.

Within each set, define:

```python
order_key = sha256(
    f"{ANCHOR}|ORDER|{set_id}|{seed}".encode("utf-8")
).hexdigest()
```

Sort accepted worlds lexicographically by `order_key`.

Do not reorder after seeing any model result.

Generalization and Stress remain separate campaigns and separate denominators.

# 8. NO EARLY STOPPING OR SAMPLE EXTENSION

Once the world manifest is frozen:

- run every planned world;
- do not stop because an effect appears strong;
- do not stop because an effect disappears;
- do not add worlds because an effect is ambiguous;
- do not add worlds to rescue a prior observation;
- do not replace an unusual world.

Planned valid sample:

- Generalization Set 001: 12 worlds;
- Stress Set 001: 8 worlds.

Any future expansion requires a separately versioned prospective plan.

# 9. TECHNICAL FAILURE / RETRY POLICY

A retry is allowed only for a technical failure that prevents a valid archived execution, such as:

- provider/network failure;
- timeout;
- schema/parse failure;
- interrupted process;
- incomplete required raw output.

A behavioral result is never a retry reason.

For a technical retry:

- preserve the failed attempt;
- rerun the **same seed**;
- preserve the same frozen configuration;
- increment `attempt_<NNN>`;
- record the technical reason;
- never substitute a different world.

Technical retries do not increase the planned scientific N.

# 10. ARCHIVAL NAMESPACES

Use separate immutable namespaces:

```text
experiments/EXP_002/results/archive/gate_2b/generalization_set_001/<canonical_world_id>/attempt_<NNN>/
experiments/EXP_002/results/archive/gate_2b/stress_set_001/<canonical_world_id>/attempt_<NNN>/
```

Never overwrite archived:

- `events.jsonl`;
- `summary.csv`;
- `run_metadata.json`.

Each valid archived world must be recoverable to:

- Gate and set;
- canonical identity;
- seed;
- truth;
- observed state;
- reliability;
- evidence root;
- frozen runtime/protocol;
- config fingerprint.

# 11. ANALYSIS PLAN

## Primary reporting

Report Generalization Set and Stress Set separately.

For each set, report original EXP-002 outcomes by:

- world;
- condition;
- truth;
- evidence alignment;
- truth × observed-state cell.

For Generalization Set, descriptive aggregate summaries across its 12 prospectively unfiltered worlds are allowed.

For Stress Set, cell-conditional summaries are allowed, but the intentionally balanced design must remain explicit.

## Calibration

Use the already-frozen Brier metric descriptively.

Relevant questions include whether an architecture-associated confidence change:

- improves calibration under misleading evidence;
- worsens calibration under aligned evidence;
- behaves similarly regardless of correctness;
- disappears when the world changes.

These are interpretations of an existing primary metric, not new endpoints.

## No pooling across selection schemes

Do not report `X/20` as a prevalence or generalization estimate.

Cross-set comparison may be descriptive, but the selection mechanisms must remain visible.

## No post-hoc thresholding

Do not introduce after result inspection:

- a preferred inference-depth cutoff;
- a selected message index;
- a selected agent;
- a selected confidence delta;
- a selected subset of worlds.

## Statistical boundary

Gate 2B v0.1 is descriptive/exploratory multi-world generalization and stress testing.

No significance test or population-level inference is part of this plan.

Any confirmatory statistical analysis requires a separately justified and prospectively specified analysis plan.

# 12. FALSIFICATION / BREAK CONDITIONS

The following outcomes are explicitly acceptable and must not alter execution:

- LINEAGE numerical discounting disappears outside W01;
- FREE develops numerical drift;
- confidence inflation appears;
- answer flips appear;
- Agent A begins discounting;
- the source-holder pattern disappears;
- LINEAGE improves Brier score primarily when evidence is misleading;
- LINEAGE worsens Brier score when evidence is aligned;
- MACRO truncation helps some worlds and harms others;
- no architecture difference survives across worlds.

Gate 2B is intended to expose boundary conditions and falsification evidence, not protect the W01 observation.

# 13. GATE CLOSURE RULE

Gate 2B closes when:

1. the world manifest was prospectively frozen;
2. all 12 Generalization worlds have a valid archived execution or a transparently documented unresolved technical failure;
3. all 8 Stress worlds have a valid archived execution or a transparently documented unresolved technical failure;
4. immutable raw outputs are preserved;
5. the predefined primary outcomes are audited;
6. Generalization and Stress are reported separately;
7. deviations and negative results are retained.

A new interesting pattern discovered in Gate 2B does **not** justify extending Gate 2B.

It may motivate a later observation record, Gate 2C question, or Gate 3 causal intervention, but it cannot retroactively change this plan.

# 14. MODEL-CALL ACCOUNTING

Under frozen paired execution with `rounds=4`:

- 1 shared seed call per world;
- 12 FREE post-seed calls per world;
- 12 LINEAGE post-seed calls per world;
- 0 independent MACRO calls;
- nominal actual provider calls per valid world: **25**.

Planned no-retry accounting:

- Generalization Set 001: `12 × 25 = 300` provider calls;
- Stress Set 001: `8 × 25 = 200` provider calls;
- Gate 2B total: **500 actual provider calls**.

MACRO responses are reused from the shared seed / LINEAGE trajectory under the frozen protocol.

Technical retries, if any, are separately accounted and are not additions to scientific N.

# 15. PRE-EXECUTION CHECKLIST

Before the first Gate 2B model call:

- this plan is committed;
- frozen runtime SHA remains `7e9aed1b7093baae10ae30f27e0b6a2b932f92f5`;
- protocol tag remains `exp-002-protocol-v0.1`;
- world manifest is committed;
- exact 12 + 8 seeds are frozen;
- execution order is frozen;
- no world membership was selected from model behavior;
- archive destinations exist or are defined;
- no primary/secondary outcome definitions were changed;
- no hypothesis text was rewritten.

Only after those conditions hold may empirical Gate 2B execution begin.
