# Q1 Paper Blueprint

Target venue class: trustworthy ML / AI security journal (Q1).  
Evidence-gated: every results claim maps to frozen run IDs.

---

## 1. Introduction

**Objective:** Motivate agent tool-harm ≠ textual jailbreak; state primary contribution.  
**Evidence required:** None (framing).  
**Results to include:** None.  
**Figures/Tables:** Fig 1 (architecture teaser optional).  
**Claims allowed:** Problem statement + contribution sentence from `q1_contribution_framework.md`.  
**Forbidden:** SOTA, universal robustness, ranking.

## 2. Related Work

**Objective:** Position vs prompt injection, guardrails, agent security eval, tool permissions.  
**Evidence required:** Verified citations only (`UNVERIFIED_EXTERNAL` until filled).  
**Claims allowed:** “Closest prior work differs by X (entangled detector/policy; text ASR; …).”  
**Forbidden:** Invented citations; “first ever” without verification.

## 3. Problem Formulation / Threat Model

**Objective:** Define agent, tools, attacker goals, assets, out-of-scope (C4, real network, white-box).  
**Evidence required:** P1/P2 threat docs.  
**Tables:** Threat vs out-of-scope checklist.  
**Claims allowed:** Scoped threat validity for authored multi-turn tool attacks in packs.

## 4. ADAPTI-GUARD

**Objective:** Describe detector → risk → policy → tool gate → execution.  
**Evidence required:** Architecture + action costs (as normalized weights).  
**Figures:** Fig 1 architecture; Fig 2 pipeline.  
**Claims allowed:** Systems description; cost weights labeled normalized.

## 5. Benchmark and Experimental Protocol

**Objective:** P1/P2 packs, SHAs, Tool-HASR definition, P3 isolation design, Q2 design, locks.  
**Evidence required:** Freeze docs; protocol docs; lock manifests.  
**Tables:** Benchmark composition; experimental configuration; detector definitions.  
**Claims allowed:** Reproducibility of protocol; pilot-scale honesty.

## 6. Experimental Results

**Objective:** Report P3 Stage-B Δ vs D0; policy strata as descriptive; no ranking.  
**Evidence required:** `p3_stage_b_20260916T235438Z_7e401714`.  
**Tables:** Primary results (Tool-HASR, Δ, Wilson CI, utility/FPR).  
**Claims allowed:** C1, C2 (safe wording).  
**Note:** Keep `scientific_evidence=false` framing unless editors accept “pilot confirmatory.”

## 7. Forensic Analysis

**Objective:** Tool-HASR vs Judge-ASR; M3/M4; INVALID S0/S1/S2; failure states.  
**Evidence required:** Stage-B + Q2 traces; sensitivity JSON.  
**Figures:** Fig 3 (HASR vs ASR); Fig 5 (forensic decomposition).  
**Tables:** Sensitivity analysis.  
**Claims allowed:** C3, C9 (safe wording).

## 8. Cross-Target Analysis

**Objective:** Q2 directional consistency.  
**Evidence required:** `p3_stage_c_q2_20260917T123855Z_b075df0f`.  
**Figures:** Fig 4 (Δ across T0–T3).  
**Tables:** Cross-target results; exact model IDs.  
**Claims allowed:** C4 safe wording only.

## 9. Discussion

**Objective:** What attribution the protocol enables; what it does not; utility tradeoffs.  
**Claims allowed:** Interpretation within ledger; baseline gap honesty.

## 10. Limitations

**Objective:** Full limitation dump from generalization + baseline + cost + C4 + n.  
**Tables:** Limitations summary.  
**Claims allowed:** None that expand scope.

## 11. Conclusion

**Objective:** Restate primary contribution + bounded secondaries.  
**Forbidden:** New claims; ranking; universal language.

---

# Figure / Table Plan

## Figures

| Fig | Title | Content rules |
| --- | --- | --- |
| 1 | ADAPTI-GUARD architecture | Boxes for detector, risk, policy, tools; no performance numbers |
| 2 | Detector → Risk → Policy → Tool Gate → Execution | Single pipeline; annotate locked vs varied (detector) |
| 3 | Tool-HASR vs Judge-ASR | Paired bars or scatter of episode-arm rates; show M3/M4 counts; no “winner” styling |
| 4 | Δ Tool-HASR across T0–T3 | Grouped bars for D1/D2/D4 Δ; annotate sign agreement 9/9; CI optional (wide) |
| 5 | Forensic decomposition | Stacked counts: EXECUTED / POLICY_DENIED / INVALID / tool-HASR success pathways |

**Plotting rules:** Use exact numerators/denominators; show Wilson CIs where rates appear; do not cherry-pick cells; do not smooth over INVALID.

## Tables

| Table | Content |
| --- | --- |
| T1 | Benchmark composition (P1/P2 counts, twins, HN, turns) |
| T2 | Experimental configuration (models, seeds, T=0, cache off, SHAs, run IDs) |
| T3 | Detector definitions (D0/D1/D2/D4; D3 deferred) |
| T4 | Primary Stage-B PHASE1-CORE results (Tool-HASR, Δ, CI, utility/FPR) |
| T5 | Cross-target Q2 Δ and sign agreement |
| T6 | INVALID S0/S1/S2 sensitivity summary |
| T7 | Limitations (quantified) |

## Run IDs to cite (only)

- P1: `l1_p1m_full_20260915T160302Z_ef2e98c3`
- P2: `p2_agentic_stage_b_20260916T165133Z_2bb84aa7`
- P3: `p3_stage_b_20260916T235438Z_7e401714`
- Q2: `p3_stage_c_q2_20260917T123855Z_b075df0f`
