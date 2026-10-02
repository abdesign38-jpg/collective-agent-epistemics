# EXP-003 Protocol v0.1

**Status:** DRAFT / NOT FROZEN / NOT EXECUTED

EXP-003 is a new experiment, not a new EXP-002 gate, because it changes network topology, the number of independent evidence roots, and source re-grounding. Under [REPOSITORY_RESEARCH_STRUCTURE_v0.2](../../research/REPOSITORY_RESEARCH_STRUCTURE_v0.2.md) each of those changes requires a new experiment number. The frozen EXP-002 v0.1 runtime is not modified.

## Research question

When an agent receives more than one message descended from the same external evidence, does its reported probability exceed what that evidence alone supports, and does an explicit lineage envelope change that?

This is the fan-in form of the umbrella question in [framework_v0.1](../../research/framework_v0.1.md). EXP-002's ring topology never gave any agent two inbound messages, so the candidate mechanism (recursion, correlation, lineage loss, double counting, distortion) had no structural opportunity to occur there.

## Conditions

Unchanged from EXP-002 in meaning:

- **FREE:** natural-language messages only; no envelope.
- **LINEAGE:** every received message carries the structured lineage envelope; no stopping rule.
- **MACRO:** same envelope as LINEAGE; the harness stops after a complete recursive cycle that adds no new independent root. MACRO reuses the paired LINEAGE responses and makes no independent model calls.

## Topologies

A topology is a seed cycle and a recursive cycle of **firings**. A firing is one model call by one agent whose message is delivered unchanged to every listed receiver. An agent consumes every message in its inbox when it fires; the inbox is then empty.

| Name | Gate | Agents | Seed cycle | Recursive cycle | Rounds to depth 12 | Re-grounding | Focal agent |
|---|---|---|---|---|---|---|---|
| `solo` | 3A | A | A→A | A→A | 12 | yes | A |
| `dyad` | 3A | A B | A→B | B→A, A→B | 6 | yes | B |
| `ring` | 3A (and EXP-002) | A B C | A→B | B→C, C→A, A→B | 4 | yes | C |
| `bounce` | 3A | A B C | A→B | B→C, C→B, B→A, A→B | 3 | yes | C |
| `diamond` | 3B | A B C D | A→{B,C} | B→D, C→D, D→A, A→{B,C} | 4 | yes | D |
| `*_detached` | 3C | as above | as above | as above | as above | no | as above |
| `hives_bridged` | 3D | A1..D1, A2..D2 | A1→{B1,C1}, A2→{B2,C2} | B1→D1, C1→D1, B2→D2, C2→D2, D1→{A1,A2}, D2→{A2,A1}, A1→{B1,C1}, A2→{B2,C2} | 4 | yes | A1 |
| `hives_isolated` | 3D control | same | same | same minus D1→A2 and D2→A1 | 4 | yes | A1 |

`ring` is the EXP-002 shape; it is run again contemporaneously in Gate 3A so the four Gate 3A shapes are paired on the same model on the same day. `ROUNDS_FOR_DEPTH_12` in `topology.py` records the rounds that bring every shape to inference depth 12, so rungs differ in structure, never in circulation time.

**Ladder.** Each rung changes one thing relative to the one before: solo (no interaction) → dyad (one other mind, direct contact with the source) → ring (a distal position, everyone still reaches the source) → bounce (the return path reverses; an isolated end and a two-way relay) → diamond (two relays of one root converge on an agent with no evidence) → detached (re-grounding removed) → bridged hives (subnetworks replicated and connected, with unbridged twins as controls). With the probe off, EXP-003 prompts are byte-identical to EXP-002's for the same inputs (locked by a unit test); the 36 archived EXP-002 ring runs are retrospective evidence and the contemporary ring against them is a model-drift observation, never a primary comparison.

**Stages.** Each gate pre-registers a discovery set (Set 001) and, where stated, a same-size replication set (Set 002) on new worlds. Set 002 runs regardless of Set 001 results and only after Set 001 closes. A gate is never redesigned after its results are seen.

**Re-grounding.** With re-grounding on, an agent sees its direct evidence every time it fires (EXP-002 semantics). With it off, direct evidence is shown only at the agent's first firing; hidden lineage is unchanged.

**Fan-in.** In `ring`, `dyad` and `bounce`, every agent receives exactly one inbound message; the only redundancy is the source holder re-reading E1 while receiving a descendant of E1. In `diamond`, D always receives two inbound messages (from B and from C) that descend from the same root set. In `hives_bridged`, each A receives one inbound from its own hive's D and one from the other hive's D.

## Root modes

| Mode | Evidence | Holders |
|---|---|---|
| `single` | E1 | the topology's primary sources (diamond: A; hives: A1) |
| `shared` | E1 | primary and secondary sources (hives: A1 and A2 hold the same physical sensor) |
| `dual` | E1, E2 | E1 to primary (A / A1); E2 to secondary (diamond: C; hives: A2). E2 is an independent draw at the same reliability. |

For a given seed, `single`, `shared` and `dual` worlds share truth and E1; `dual` adds one further draw. World cells are `truth/E1` or `truth/E1/E2`.

## Hidden lineage

The harness maintains a multi-parent DAG. A message's actual roots are the union of its direct evidence and all inbound messages' roots; its depth is one more than its deepest parent. The envelope shown in LINEAGE and MACRO lists roots, the visible ids it was derived from, depth, and whether new external evidence entered. It does not carry per-root observed states or reliabilities.

**Redundant root exposures** is a harness-side count: total root mentions across direct evidence and inbound messages minus distinct roots. It is the structural opportunity for double counting at that firing. In EXP-002 it was at most 1 (A re-reading E1 while receiving a descendant of E1). In `diamond` it is 1 at D and 1 at A; in `hives_bridged` it reaches 2 at each A.

## Perceived-source probe

Every response carries `distinct_source_count`: the number of distinct original sources (for example, separate sensors) the agent believes its conclusion rests on. The prompt wording is neutral and identical across conditions; it does not use the words lineage, provenance, independence, evidence roots or double counting.

**False independent support (FIS)** = max(0, reported distinct sources − actual roots). This is the first runtime measurement of the "agent-perceived dependency" dimension listed in the framework.

The probe is a possible reactivity risk: asking the question may itself reduce double counting. It can be switched off (`--no-probe`), and each gate plan states how reactivity is checked.

## Normative reference

For each event the harness computes **reference P(A)**: the probability obtained by combining the actual independent roots in that message's lineage with a uniform prior, each root contributing odds r/(1−r) toward its observed state. With one .70 root it is .70 (or .30). With two agreeing .70 roots it is about .845; with two conflicting roots it is .50.

**Excess over reference** = P(A) − reference. Positive excess with unchanged roots is the numerical signature of counting shared evidence more than once. Negative excess is discounting. Excess is defined at every event, so it does not depend on choosing a baseline event, which was the source of the EXP-002 Set 001 analysis bug.

## Provenance marks

Every message is scored mechanically with regular expressions on the visible text only: whether the sensor id is named, whether the reliability value is named, whether the observed state is named, whether relay/indirection language is present, whether evidence is attributed through an agent, and **agent-as-source** (the agent is presented as the owner of the evidence, or the evidence is attributed through an agent while the sensor is no longer named). **Erosion** counts facts that were present in at least one inbound message and are absent from the outgoing one.

These marks are literal and conservative. They measure wording, not reasoning. The tool `tools/erosion_retrospective.py` applies the same marks to the archived EXP-002 runs without model calls.

## Primary measurements

The EXP-002 family: answer, confidence, P(A), Brier, accuracy, independent roots, inference depth, P(A) delta without new evidence.

Added in EXP-003: reference P(A), excess over reference, reported distinct source count, false independent support, redundant root exposures, provenance marks and erosion. Focal-agent trajectories are recorded separately.

## Paired execution and accounting

Seed-cycle firings have no inbound messages, so their prompts are condition-independent; each is called once and shared across FREE, LINEAGE and MACRO. FREE and LINEAGE make independent post-seed calls. MACRO reuses LINEAGE responses by firing index and verifies the prompt is identical before reuse.

Calls per world with `rounds = 4`:

| Topology (rounds to depth 12) | Seed | FREE | LINEAGE | Total actual |
|---|---:|---:|---:|---:|
| `ring` (4), `bounce` (3), `dyad` (6), `solo` (12), and their detached forms | 1 | 12 | 12 | 25 |
| `diamond` / `diamond_detached` (4) | 1 | 16 | 16 | 33 |
| `hives_bridged` / `hives_isolated` (4) | 2 | 32 | 32 | 66 |

## Model layer

The model is a factor of its own, orthogonal to gate, topology, root mode and probe. It is bound at run time through `adapters/registry.py` and nothing else in the harness depends on which provider is bound. Two providers are implemented:

| Provider | Adapter | Structured output | Effort control | Retries | Fallbacks |
|---|---|---|---|---|---|
| `openai` | Responses API, `responses.parse` | Pydantic schema | `reasoning.effort` | 0 | none |
| `anthropic` | Messages API, `messages.parse` | same Pydantic schema | `output_config.effort`, adaptive thinking | 0 | technical-only, off by default |

Both adapters render the identical prompt, use the identical response schema and probe, and record provider, requested model, served model, response id, usage and latency per event.

**Refusal fallbacks are technical, never scientific.** In a scientific set a refusal or truncation is a technical failure and is retried under the retry policy with the same seed; the served model must equal the requested model on every event. The Anthropic adapter can opt into Anthropic's server-side `fallbacks: "default"`, which re-runs a declined request on a substitute model inside the same call, but only in a run whose class is `smoke_technical` (`--smoke --fallbacks`). The registry refuses the flag for any other run class, the runner refuses to return a run that contains a fallback-served event outside that class, every event records `fallback_ran` and `served_model`, and `fallbacks` and `run_class` are factors on the ledger. Smoke runs are for checking plumbing and prompts; they are never archived as a set and never enter an audit denominator.

**Model sets.** Any gate arm may be executed under a second provider as a separate set with the same manifest, the same seeds and the same execution order. Such a set is named `<set>_<provider>` (for example `generalization_set_001_anthropic`) and archived beside the first. Its ledger row differs from the first set's in exactly two factors, `provider` and `model`, and in nothing else. Model sets are reported separately and never pooled.

**Factor ledger.** `factors.py` reduces any run's metadata, including archived EXP-002 runs, to one row of canonical factors (experiment, gate, set, topology, regrounding, root mode, probe, provider, model, effort, rounds, reliability, execution policy, prompt and schema versions, conditions). `factors diff A B` lists exactly which factors differ between two runs; `factors ledger DIR ...` tabulates every run under the given directories. A comparison across gates or across models is valid only when the ledger shows the intended factors, and only those, as different.

## Execution and archival

The research chain in [REPOSITORY_RESEARCH_STRUCTURE_v0.2](../../research/REPOSITORY_RESEARCH_STRUCTURE_v0.2.md) is prospective design → execution → immutable archive → audit → synthesis → checkpoint. `gate_orchestrator.py` implements the execution and archive steps and nothing after them.

**Sources of truth.** A gate's configuration (provider, model, effort, execution policy, reliability, and per arm: topology, root mode, rounds, probe, world count) lives only in `GATE_3x_PLAN_v0.1.json`. World membership and execution order live only in the arm's manifest, derived by `manifest.py` with zero model calls. The orchestrator takes neither from the command line.

**Freeze.** A plan is executable live only when its status is `FROZEN`, every anchor (frozen runtime SHA, protocol tag, plan freeze commit, derivation anchor) is filled, the plan and every manifest are committed and byte-identical to HEAD, the manifest anchors equal the plan's derivation anchor, and the runtime files match the frozen SHA. Any of these failing stops execution before the first call.

**Order and immutability.** Worlds execute in manifest order. A complete attempt is never re-executed; a re-run resumes. Archived files are never overwritten. Every attempt carries SHA-256 hashes and `archive_metadata.json` with its factor-ledger row.

**Technical failures.** A provider, schema or integrity failure writes `failure_metadata.json`, stops the campaign, and requires `--authorize-retry` for the next attempt of the same seed. A behavioral result is never a retry reason.

**Pacing is not stopping.** `--max-worlds` limits how many new executions one invocation may start. It is blind to results, preserves frozen order on resume, and leaves the set incomplete: `campaign_status.json` records complete/failed/pending per set, and a set with any pending or failed world may not be audited, pooled or reported. The Gate 2B rule stands: once frozen, every planned world runs.

**Preflight.** `--preflight` executes a whole plan with the stub adapter into `results/preflight/` (Git-ignored, never an archive) under run class `gate_3x_preflight`, so the plan, manifests, archive layout, hashes and ledger rows are exercised end to end before any call.

**Run classes.** Live executions carry `gate_3x_real_model`, as Gate 2B carried `gate_2b_real_model`. The smoke class and refusal fallbacks cannot be reached from the orchestrator.

## Deterministic stubs

Two stubs exist to validate measurement, as EXP-001 did for EXP-002. `naive` multiplies odds from every inbound message and reports each as a source; under fan-in it reaches about .845 at D with one root. `dedup` covers each root once when envelopes are visible and falls back to naive without them. Stub results never bear on the hypothesis.

## Interpretation rule

Stub or infrastructure output is not evidence for the research question. Real-model results are exploratory until a prospectively frozen gate plan, manifest and closure exist for them. Positive excess demonstrates a numerical departure from the single-root reference; it is evidence of double counting only together with the reported source count and the message wording, and it is never by itself a causal claim.
