# EXP-002 Same-World Synthesis v0.1

## Scope and denominator

This synthesis combines the corrected mechanical audits for formal Replication Set 001 (`5` runs) and Set 002 (`10` runs): **15 formal runs**. Pilot 002 remains separate historical exploratory context and is not included in the formal denominator.

All 15 formal runs share one frozen configuration: model `gpt-5.6-sol`, reasoning effort `medium`, world `EXP_002_W01`, seed `42`, sensor reliability `.70`, truth `A`, observed state `A`, paired execution, rounds `4`, and protocol EXP-002 v0.1.

This therefore addresses same-world, same-model, same-protocol stochastic reproducibility only. It does not address generalization across worlds, models, or configurations.

## KNOWN FROM EXECUTION

- Set 001: 5 valid runs; Set 002: 10 valid runs.
- All 15 runs passed technical integrity checks.
- FREE had numerical drift in `0/15` runs.
- LINEAGE had numerical discount events in `12/15` runs, totaling `17` events.
- Discount actors across all events: A `0`, B `7`, C `10`.
- Confidence inflation events: `0`.
- Answer flips: `0`.
- Explicit FREE dependency recognition occurred in `15/15` runs.
- MACRO stopped after one recursive cycle with `no_new_independent_roots_after_cycle` in `15/15` runs.
- Agent A returned to `.70` following downstream deviations in `11/15` runs, as a numerical pattern only.

## Set-level mechanical results

| Set | Runs | LINEAGE discount runs | FREE drift runs | LINEAGE discount events | Actors A/B/C |
|---|---:|---:|---:|---:|---|
| Set 001 | 5 | 4/5 | 0/5 | 7 | 0 / 2 / 5 |
| Set 002 | 10 | 8/10 | 0/10 | 10 | 0 / 5 / 5 |
| Formal combined | 15 | 12/15 | 0/15 | 17 | 0 / 7 / 10 |

These are descriptive same-world totals, not population estimates and not significance tests.

## MANIPULATION CHECK

**[MANIPULATION CHECK]** MACRO consistently truncated the trajectory after one recursive cycle, before later LINEAGE-only events could occur. This confirms the intended stopping boundary. It does not establish that MACRO improves accuracy or calibration.

## OBSERVATION — SAME-WORLD

Under the frozen EXP-002 configuration, transient numerical confidence discounting in LINEAGE was stochastically reproducible across both formal replication sets: `12/15` runs and `17` events. FREE remained numerically stable in `15/15` runs. All numerical discount events occurred in non-source agents B/C; none occurred in Agent A.

FREE nevertheless repeatedly expressed natural-language recognition of evidence dependency without structured lineage metadata. This does not prove complete lineage preservation by FREE.

The mechanical result has higher evidentiary priority than semantic DSCD labels. Under the locked criterion-D review, Set 001 contained 6 strict and 1 numeric event; Set 002 contained 3 strict and 7 numeric events. These semantic counts are secondary coding outcomes, not replacements for the numerical result.

## NO EFFECT OBSERVED

**[NO EFFECT OBSERVED — SAME-WORLD]** No confidence inflation was observed across the 15 formal runs.

**[NO EFFECT OBSERVED — SAME-WORLD]** No answer flips were observed.

**[NO EFFECT OBSERVED — SAME-WORLD]** FREE showed no numerical drift in any formal run.

## FALSIFICATION EVIDENCE

**[FALSIFICATION EVIDENCE]** The strong formulation that recursion without new evidence necessarily produces confidence inflation is not supported by these 15 formal runs. The broader research framework and historical hypothesis are not thereby falsified.

FREE dependency recognition was not absent; it occurred in every formal run. LINEAGE was not unstable in every run: `3/15` formal runs had no numerical discount. Agent A produced no numerical discounts under this topology.

## HYPOTHESIS / OPEN QUESTION

**[HYPOTHESIS / OPEN QUESTION]** A candidate interaction for future testing is:

```text
explicit lineage/dependency representation
× inference depth
× direct access to original evidence
```

This is an emerging question, not a causal result. The open question is whether explicit dependency representation changes evidence valuation as inferential distance grows, and whether periodic direct evidence access is responsible for the observed source/non-source difference.

The synthesis must not be read as claiming that LINEAGE causes discounting, depth causes discounting, direct evidence prevents degradation, MACRO solves the problem, recursive systems generally behave this way, or that the original hypothesis is confirmed.

## Historical Pilot 002 context

Pilot 002 is excluded from the formal denominator. Under the same mechanical and semantic review it contains one LINEAGE DSCD-STRICT event at M09, actor C, `.70 -> .62`. It is directionally consistent with the later formal same-world replication sets, but it is not merged into the formal headline and does not create a statistical sample.
