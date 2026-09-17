# Q2 manuscript blueprint

Controlled empirical / methodological study. **Not** a claim of a universally effective defense.  
`scientific_evidence=false`. Do not use “confirmatory” unless quoting another track’s locked protocol.

**Central sentence:** A controlled framework for isolating detector-related effects from downstream intervention policy in LLM-agent security.

Numbers must be copied from `FIGURES_AND_TABLES.md` / `q2_final_statistics.json`. Related-work citations: **unverified — do not invent**.

## 1. Abstract (skeleton)

- Problem: tool-using agents; harm is execution-grounded.
- Method: lock policy/thresholds/pack/judge; vary detector (D0 vs D1/D2/D4); primary Tool-HASR; secondary Judge-ASR.
- Q2 question: is the Stage-B (T0) detector-related Δ **directionally consistent** on independently selected T1–T3?
- Observed: 432/432 Q2 arms; $0.152885 historical token-USD; 9/9 Δ sign agreements; D1/D2/D4 NEG vs D0 on T0–T3; n=16/cell; INVALID 192/136 on T1–T3; M3=108.
- Limits: pilot-scale; four targets; no external baseline; D3 deferred; C4 open attacker out of scope.
- Not claimed: SOTA, production-ready, all-LLM generalization.

## 2. Introduction

Lead with attribution: how much of observed agent-security behavior is detector vs downstream policy? Motivate Tool-HASR vs text ASR. One contribution, not a product pitch. Point to dual-track honesty: this paper does not reverse Track A VNEXT FAIL or restate Track B as Q2.

## 3. Related work

Structure as **categories** until citations are verified (`BASELINE_GAP.md`, `q2_novelty_audit.md`):

- Prompt injection and agent tool misuse
- Guardrail stacks (detection entangled with policy)
- Agent security benchmarks and success metrics
- Cost-aware / adaptive policies (established; not claimed as invented here)

Explicit: missing implementation in this repo ≠ novelty. No “first/only” without verification.

## 4. Research question

RQ-C2 (protocol): Does the detector-related security effect observed under the locked Stage-B target remain directionally consistent when evaluated against independently selected secondary target models?

Factor: `target_model_id ∈ {T0,T1,T2,T3}`. Policy locked to PHASE1-CORE in Q2 live.

## 5. Experimental design

Table 1 + Table 2 + Table 7. Pack SHA `32b40e3b…`. T0 reused from Stage-B. B_REDUCED_Q2 = 36×4×1×3 = 432. Seed 42, T=0, cache off. Figure 1.

## 6. Detector-policy decomposition

Figure 2. D0 isolates policy without detector hits. D1/D2/D4 share `P3Detector` contract. Thresholds 0.25/0.60; costs A0–A3. D3 deferred. No ranking.

## 7. Results

Table 3 primary Δ; Wilson CIs on rates. Report n/N. No detector crowns. Stage-B T0 Δ as reference, Q2 as cross-target.

## 8. Cross-target analysis

Figure 3. 9/9 sign agreement. Δ_change is descriptive. Language: **directionally consistent on the selected set**, not “validates all LLMs.”

## 9. Diagnostic analysis

Table 4–6, Figures 4–5. Tool-HASR vs Judge-ASR; M3/M4; INVALID S0 vs S1/S2. Keep PRIMARY vs SENSITIVITY vs LIMITATION labels.

## 10. Limitations

Copy `LIMITATIONS.md` (model diversity, n, INVALID, baselines, D3, C4, T0 trace packaging).

## 11. Threats to validity

Internal: small n, INVALID, T0 harness reuse. External: four models, mock tools, OpenRouter. Construct: Tool-HASR vs Judge-ASR. See limitations table.

## 12. Reproducibility

Table 7. SHAs, run_id, commit `b075df0f5ec5ad11ede76ac4e4079cade15208f1`, spend, scripts. Disclose Stage-B predictions missing from this checkout. Historical live API count 2061; this packaging API=0.

## 13. Conclusion

Restate bounded contribution. Future work = new studies (baselines, D3, larger n, more families, open C4) — not silent extensions of this run.

## Banned language (replace if it appears)

| Do not write | Write |
| --- | --- |
| best / superior / SOTA | observed Δ vs D0 under the locked protocol |
| robust / guaranteed / production-ready | pilot-scale; target-model sensitivity |
| proves / confirms for all LLMs | evidence is consistent with directional Δ sign on T0–T3 |
| cost-optimal | normalized action weights; token-USD reported separately |
| solves prompt injection | does not establish universal generalization |
