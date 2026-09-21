# EXP-002 Pilot Observations v0.1

## Scope

These are conservative observations from real-model Pilot 002 (`seed=42`, `rounds=4`, `gpt-5.6-sol`, paired execution). They are exploratory observations, not a revised primary hypothesis and not confirmatory evidence. The full forensic audit is archived under `experiments/EXP_002/audits/`.

## Recorded observations

- **[MANIPULATION CHECK]** MACRO stopped after one recursive cycle while LINEAGE continued through four cycles. The paired boundary was M04; no new independent root entered during the completed recursive cycle.
- **[OBSERVATION — PILOT]** LINEAGE showed a transient confidence and `P(A)` decrease at M09 from `0.70` to `0.62`, with no new independent evidence; it returned to `0.70` at M10.
- **[NO EFFECT OBSERVED — PILOT]** No confidence inflation occurred. No recorded confidence exceeded the initial `.70` sensor reliability.
- **[NO EFFECT OBSERVED — PILOT]** No answer flip occurred. Recorded answers remained `A`.
- **[NO EFFECT OBSERVED — PILOT]** FREE remained numerically stable across M01-M13: answer `A`, confidence `.70`, `P(A)=.70`, and Brier `.09`.
- **[OBSERVATION — PILOT]** FREE natural-language messages recognized duplicate or relayed evidence despite having no structured lineage envelope visible to the agents.

## Scope clarification: re-grounding

- **[INVALID ASSUMPTION / SCOPE CLARIFICATION]** EXP-002 is not a fully source-detached relay chain.
- Agent A receives its original observation again whenever A participates, because the runner constructs each agent's observation from the world's evidence on every step.
- Therefore the current experiment includes periodic re-grounding in `E1` while introducing no new independent evidence.

This clarification describes the exact experiment executed. It does not modify EXP-002 v0.1, its code, metrics, prompts, or protocol.

## Interpretation boundary

Pilot 002 does not establish that lineage causes the transient M09 change, that MACRO is better, or that recursion generally degrades epistemic quality. The observation registry preserves both stability and deviation, including the fact that FREE was numerically stable in this run.
