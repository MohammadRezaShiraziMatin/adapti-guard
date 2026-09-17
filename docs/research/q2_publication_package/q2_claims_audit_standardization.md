# Q2 claims audit (standardization)

GREEN=supported by locked evidence · YELLOW=qualify · RED=must not appear as an assertion  
**API=0.** Numerical results are not weakened.

Banned-term grep over `docs/research/q2_publication_package/` found **51** hits; **all** were meta (listing forbidden phrases in audit/limitations/novelty notes), not asserted SOTA/best claims in results text. Frozen Q2 `manifest.json` research_question uses “generalize (same sign)” — **do not edit that file**; publication prose should say **directionally consistent**.

## Claim table

| ID | Claim | Status | Publication-safe | Forbidden |
| --- | --- | --- | --- | --- |
| A1 | Detector-related Tool-HASR effect vs D0 is NEG on T0 PHASE1-CORE | **GREEN** | Observed Δ(D1/D2/D4)=−0.6875/−0.25/−0.5625, n=16 | Detectors guarantee security |
| A2 | Δ sign consistent on T1–T3 (9/9) | **GREEN** | Directionally consistent on evaluated T0–T3 | Universally effective / all LLMs |
| A3 | Protocol isolates detector from policy | **GREEN** | Experimental isolation under fixed PHASE1-CORE | Full causal ID in production |
| A4 | Tool-HASR ≠ Judge-ASR | **GREEN** | M3=108 on T1–T3; dual endpoints | Judge-ASR is invalid |
| A5 | INVALID does not overturn primary signs | **GREEN** | S0 official; S2 9/9, 0 sign flips | INVALID negligible |
| A6 | Production-ready / SOTA | **RED** | (omit) | production-ready / SOTA / best |
| A7 | Proves robust generalization | **RED** | Bounded directional consistency, four models | proves / robust / all LLMs |
| A8 | Cost-optimal defense | **RED** | Normalized weights; $0.152885 token-USD | cost-optimal |
| A9 | D1 superior to D2/D4 | **RED** | Report each Δ vs D0; no ranking | best / superior |
| A10 | Adaptive C4 handled | **RED** | Out of claim scope | robust to adaptive attacks |
| A11 | Q2 confirmatory | **YELLOW** | Protocol-complete pilot; `scientific_evidence=false` | confirmatory multi-model proof |
| A12 | Novelty of isolation protocol | **YELLOW** | Methodological contribution pending verified cites | first/only breakthrough |

## Replacements applied in this package

New prose files use: controlled study; observed; under the locked protocol; directionally consistent; pilot-scale; target-model sensitivity; detector-related effect; evidence is consistent with; does not establish universal generalization.

`q2_limitations.md` / executive “claims to weaken” lists remain as **forbidden-example** notes, not results.

## Frozen files not rewritten

`experiments/real_llm_eval/P3_DETECTOR_COMPARISON/p3_stage_c_q2_20260917T123855Z_b075df0f/**` including live report and manifest. Publication layer must paraphrase, not silently “fix” frozen wording.
