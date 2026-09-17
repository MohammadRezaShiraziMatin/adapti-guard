# Q1 Endpoint Justification — Tool-HASR vs Judge-ASR

## What each metric measures

| Metric | Measures | Grounding |
| --- | --- | --- |
| **Tool-HASR** | Fraction of *attack* episodes where a harmful tool execution matches the pre-registered `success_condition` with permission and execution | Tool layer / environment |
| **Judge-ASR** | Fraction of *attack* episodes where the LLM judge labels attack success from trajectory text/context | Semantic judge model |

**M3:** judge success ∧ ¬ tool success (judge over-calls relative to execution).  
**M4:** ¬ judge success ∧ tool success (judge under-calls relative to execution).

## Why Tool-HASR is the *primary* endpoint (in this protocol)

In agentic tool use, the security-relevant event is **harmful side effect via tools**, not merely textual willingness. The protocol therefore privileges Tool-HASR as the authoritative security estimand for P2/P3/Q2.

This is a **protocol choice for threat alignment**, not a claim that Tool-HASR is universally superior for all LLM-safety questions.

## What Judge-ASR contributes

- Secondary semantic read of attack progress
- Diagnostic when text suggests compromise but tools did not execute (M3)
- Catch cases where tools executed harmfully but judge missed (M4)

## Observed disagreement (frozen evidence)

| Run | Tool-HASR | Judge-ASR | M3 | M4 |
| --- | ---: | ---: | ---: | ---: |
| P3 Stage-B overall | 124/192 ≈ 0.646 | 163/192 ≈ 0.849 | 61 | 22 |
| Q2 live (T1–T3) | (see per-cell) | 186/192 = 0.969 | 108 | 3 |

Judge-ASR is systematically higher than Tool-HASR in these runs → large M3 mass: textual/judge success without harmful tool execution.

## Invalid conclusions if Judge-ASR is used alone

- Overestimate realized tool harm (inflate ASR when tools never executed)
- Mis-attribute detector/policy effects that act on the **tool gate**
- Hide schema/INVALID dynamics that Tool-HASR + execution states expose
- Suggest “attacks succeeded” when no harmful tool side effect occurred

## Invalid conclusions if Tool-HASR is used alone without forensics

- Ignore semantic partial compromise signals (M3)
- Under-discuss judge reliability (M4)
- Miss that INVALID/POLICY_DENIED structure the pathway to (non-)execution

## Paper wording

**Allowed:** “Tool-HASR is the primary *execution-grounded* endpoint; Judge-ASR is secondary with M3/M4 forensics.”  
**Forbidden:** “Judges are useless” / “Tool-HASR is always better for all safety evaluations.”
