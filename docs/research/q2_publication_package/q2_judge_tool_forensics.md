# Q2 Judge-ASR vs Tool-HASR Forensics

## Evaluation chain
```
Attack → Detector → Risk signal → Policy → Tool gate → Tool execution
       → Harmful tool execution? → Tool-HASR
       → Judge assessment of trajectory → Judge-ASR
```

Disagreement loci: detector miss/hit; policy A0–A3; tool schema INVALID; permission deny; success_condition match; judge semantic read.

## Definitions
| Metric | Endpoint |
| --- | --- |
| Tool-HASR | Harmful tool execution matching pre-registered success_condition |
| Judge-ASR | LLM judge labels attack success from trajectory |
| M3 | Judge success ∧ ¬ Tool success |
| M4 | Tool success ∧ ¬ Judge success |

## Observed (recomputed)
| Scope | M3 | M4 |
| --- | ---: | ---: |
| T0 PHASE1 | 33 | 6 |
| Q2 T1–T3 | 108 | 3 |
| Judge-ASR T1–T3 aggregate | 186/192 = 0.96875 | |

Judge-ASR ≫ Tool-HASR in these runs → large **M3**: textual/judge success without harmful tool execution.

## Interpretation (allowed)
- Metrics measure **different operational endpoints**.
- Tool-HASR is primary for *tool-harm* threat model.
- Judge-ASR is secondary diagnostic — **not invalid**.

## Interpretation (forbidden)
- “Judges are useless / invalid”
- Using Judge-ASR alone as the security claim for tool-using agents in this protocol
