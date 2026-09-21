# EXP-002 Replication Set 002 Audit v0.1

## Scope

This audit covers **replication_set_002 only**. It does not synthesize Set 001 or Pilot 002, and it does not create a research observation. The ten runs used the same frozen EXP-002 v0.1 configuration:

- Execution HEAD: `19d9485031ce29216fc77e81827a5dcc4c1a678c`
- Frozen runtime: `7e9aed1b7093baae10ae30f27e0b6a2b932f92f5`
- Protocol tag: `exp-002-protocol-v0.1`
- Model: `gpt-5.6-sol`; reasoning effort: `medium`
- Paired execution; trials `1`; rounds `4`; seed `42`; world `EXP_002_W01`

## Collection integrity

All ten runs passed the technical gate:

- valid runs: `10/10`;
- provider calls: `250` total, `25` per run;
- reused responses: `4` per run;
- event counts: FREE `13`, LINEAGE `13`, MACRO `4`;
- cycles: FREE `4`, LINEAGE `4`, MACRO `1`;
- MACRO stopped with `macro_stop_triggered=true` and `no_new_independent_roots_after_cycle`;
- LINEAGE/MACRO M01-M04 prefix matched on answer, confidence, `P(A)`, Brier, message, and provider response ID.

The manifest is [manifest.json](../../../results/archive/replication_sets/replication_set_002/manifest.json), with status `completed`.

## Archived runs and hashes

| Run | events SHA-256 | summary SHA-256 | metadata SHA-256 |
|---|---|---|---|
| rep_001 | `952971ab6e98930fc7b9853d427c21350694752ae8a46198700503c66b737918` | `9af364343938b71d0f1a44f34659a8a496a0f19aea8df18cd661e5110f92a9aa` | `92c999805f4178721b8b530547a8476e7c161e4cb04c6a8984c9dacace089216` |
| rep_002 | `fcc138f34bbd4b729b25eb82558b347bed50d2643b919e9e33fe83f8d4e02302` | `e1cf5e712e4f254cab28c2bc7157f3abca777eabce1b861addc0096400fea398` | `1995d03721c321f2a464df04f22272deb76b50500969ca3ca5a0ecd78d48c229` |
| rep_003 | `50d1db8b0617ac90ff1a3e3f4f4459f05ad97a8ca647cccea58a8c39dfee4fd0` | `d716897313421d74ad99c0ce30b2fc2811eb1f3c6e17d81acc4922c766df853f` | `43ba3eb040162dedfd425a2993ac5e1707f7d5535140959beb86c38dbb2d25c0` |
| rep_004 | `794192863b7e3174ac004db3776e99a12bc202d3c75816010f1d5829674d335d` | `e1cf5e712e4f254cab28c2bc7157f3abca777eabce1b861addc0096400fea398` | `7a7e241e79f96b79a061ccaf127c24f495ada5b2b600b505c7f5f8914ff79ddd` |
| rep_005 | `f0a20d4dda3193956812c454cc212cf0ad5a8b481589ad2b95e0af31661eef0d` | `ab7952741990853e5903058f666e25b428af8ff556b3db2c021abebf480c147` | `e605ab64dd494df5b7ccb4ab2ba048ff551cb7d9f0ed65af8180c8cbb2358aaa` |
| rep_006 | `fb9bab39342c008313625ba985be45fd101ce7e4d2994344b1337e7c803d61a3` | `955c0ac393ecf5211454ffe824e6c9fa5ca95468dc2c429071580582c729ddb7` | `650d179928f2e5fdcd14fbaec9c87313d183d6af1e79a1ef0fc4c3bb35a95d86` |
| rep_007 | `7af031a9c04f5ccc4e8ab7312ac629654dba532a03d198674819e29429bca240` | `cf18bff62f77a4791d8828dc6a77117c590dd69f71cac1b43421655f5404e339` | `173973a8afc6787abe1f08f8a5353088c309498ddc90b054bbec073ac04222db` |
| rep_008 | `0d4ccf21611c33030ae453bb94abc8bfde1aa2281ee8c1e58f0d3a9b1243ab9c` | `d5c3f5d561b0ea872474c1f9d98a00cfc93d2e3ad8e53dd78d51ce459bd7664c` | `921e82f01b64bef83104c39af112b860b94a0ecd1a8db97669beb442dbc15811` |
| rep_009 | `8799e427ee7b8ae64c14f9a01c9b37229dcb0f33d8648c108697e203fd70c100` | `5280de5383464b5a4499e09bd1072e9d4d89e3d71eeb86f8ce70fab360c382e0` | `73d7f42705e5a2b5194ccb9534a758b52be62d614f5c0807051a7b31bb95e7a7` |
| rep_010 | `b5ef5a1c415b39738cf5ce0e0b1343af39e8f0a7b9df25f18146d067649e98a0` | `3782f9c1bf3495f26d7fd9deb6f9b815057395f40c55555f3fe346d222450007` | `73a7e971763862d5b109a840e3bd982a533bd225165a4826d30efda5f1b3d68f` |

## Primary EXP-002 trajectories

All ten runs had truth `A`, final answer `A`, accuracy `1`, one actual root `E1`, and final confidence/`P(A)` `.70`. FREE was numerically stable in all ten runs: `P(A)=.70` at M01-M13, depth `0..12`, new evidence `1` at M01 and `0` thereafter. MACRO contained M01-M04 and stopped after the first recursive cycle in all ten runs.

LINEAGE `P(A)` trajectories, M01-M13:

| Run | LINEAGE `P(A)` trajectory |
|---|---|
| rep_001 | `.70 .70 .70 .70 .70 .70 .70 .70 .67 .70 .70 .70 .70` |
| rep_002 | `.70 .70 .70 .70 .70 .70 .70 .70 .70 .70 .70 .70 .70` |
| rep_003 | `.70 .70 .70 .70 .70 .70 .70 .70 .70 .70 .70 .65 .70` |
| rep_004 | `.70 .70 .70 .70 .70 .70 .70 .70 .70 .70 .70 .70 .70` |
| rep_005 | `.70 .70 .70 .70 .70 .70 .70 .62 .60 .70 .70 .70 .70` |
| rep_006 | `.70 .70 .70 .70 .70 .70 .70 .70 .70 .70 .62 .60 .70` |
| rep_007 | `.70 .70 .70 .70 .70 .70 .70 .63 .64 .70 .70 .70 .70` |
| rep_008 | `.70 .70 .70 .70 .70 .70 .70 .62 .65 .70 .70 .70 .70` |
| rep_009 | `.70 .70 .70 .70 .70 .70 .70 .70 .62 .70 .70 .70 .70` |
| rep_010 | `.70 .70 .70 .70 .70 .70 .70 .70 .70 .70 .62 .70 .70` |

The JSON audit preserves the corresponding Brier trajectories and run-level data.

## Required aggregates

- Runs with at least one DSCD-STRICT: `3/10`.
- Runs with any LINEAGE numerical discount: `8/10`.
- Runs with FREE numerical drift: `0/10`.
- Total DSCD-STRICT events: `4`.
- Total DSCD-NUMERIC events: `6`.
- Total DSCD-LANGUAGE-ONLY events: `3`.
- Discounts by actor: A `0`, B `5`, C `5`.
- Runs with Agent A RESTORE: `7/10`.
- Runs with explicit FREE dependency recognition: `10/10`.
- Confidence inflation events: `0`.
- Confidence deflation events: `10`.
- Answer flips: `0`.

## DSCD events and source-holder stratification

The locked event baseline was the immediately preceding event in the same condition; actor is `event.sender`; certainty is `abs(P(A)-0.5)`.

| Run | Event | Actor | Receiver | Direct observation | Depth | Transition | Classification |
|---|---|---|---|---|---:|---|---|
| rep_001 | M09 | C | A | no | 8 | `.70 -> .67` | DSCD-NUMERIC |
| rep_003 | M12 | C | A | no | 11 | `.70 -> .65` | DSCD-STRICT |
| rep_005 | M08 | B | C | no | 7 | `.70 -> .62` | DSCD-STRICT |
| rep_005 | M09 | C | A | no | 8 | `.62 -> .60` | DSCD-STRICT |
| rep_006 | M11 | B | C | no | 10 | `.70 -> .62` | DSCD-NUMERIC |
| rep_006 | M12 | C | A | no | 11 | `.62 -> .60` | DSCD-STRICT |
| rep_007 | M08 | B | C | no | 7 | `.70 -> .63` | DSCD-NUMERIC |
| rep_008 | M08 | B | C | no | 7 | `.70 -> .62` | DSCD-NUMERIC |
| rep_009 | M09 | C | A | no | 8 | `.70 -> .62` | DSCD-NUMERIC |
| rep_010 | M11 | B | C | no | 10 | `.70 -> .62` | DSCD-NUMERIC |

No numerical discount was produced by Agent A. This is descriptive only; no causal claim is made.

## Agent A re-grounding

Agent A events M04, M07, M10, and M13 were tracked numerically. `RESTORE` means the next A event returned toward `.70`; `PRESERVE` means no numerical change. RESTORE occurred in rep_001, rep_003, rep_005, rep_006, rep_007, rep_008, and rep_009. No claim is made that direct observation caused restoration. The relevant direct-observation access is a structural feature of the frozen topology.

## FREE dependency recognition

All ten runs contained explicit FREE messages recognizing dependency concepts. Examples include:

- “Agent C’s message ... relay ... should not be treated as independent confirmation.”
- “Agent C’s repetition is correlated and should not add evidence.”
- “Agent C’s message repeats the same evidence and should not be double-counted.”

The JSON audit records event IDs per run. This is explicit recorded language, not inferred hidden reasoning.

## Falsification findings

- DSCD-STRICT was not `0/10`, but occurred in only `3/10` runs and totaled `4` events.
- FREE did not develop numerical drift: `0/10` runs.
- Agent A produced no numerical discounts.
- LINEAGE was stable in `2/10` runs and showed a numerical discount in `8/10`.
- Confidence inflation was absent in all ten runs.
- Answer flips were absent in all ten runs.
- FREE dependency recognition did not disappear; it appeared in all ten runs.
- Agent A did not restore every run because some runs had no downstream deviation; among runs with deviations, the recorded A behavior is preserved in the JSON audit.

These are descriptive results for one frozen world/model/configuration. They do not establish causality, generalization, or that recursion alone produces DSCD. No significance tests were performed and no cross-set synthesis was performed.

## Files

- Structured audit: [EXP_002_REPLICATION_SET_002_AUDIT_v0.1.json](EXP_002_REPLICATION_SET_002_AUDIT_v0.1.json)
- Completed manifest: [manifest.json](../../../results/archive/replication_sets/replication_set_002/manifest.json)

No runtime, protocol, research, Set 001, or pilot files were modified. No OpenAI calls occurred after collection.
