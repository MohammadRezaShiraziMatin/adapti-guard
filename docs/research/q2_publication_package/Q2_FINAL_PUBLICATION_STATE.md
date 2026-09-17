# Q2 Final Publication State

**Date:** 2026-09-17  
**Branch:** `cursor/q2-publication-hardening-f6f3`  
**Head:** `24af165` → this pass  
**API_CALLS=0 · LLM_CALLS=0 · NETWORK_CALLS=0 · LIVE_EVAL=false · Q2_RERUN=false.**

This is the single authoritative state document for the Q2 publication package after the final rewrite/hardening pass. It consolidates status, integrity, and remaining work. No new science was performed; no frozen evidence was modified.

## 1. Final status

`Q2_FINAL_REWRITE_STATUS = READY_WITH_MAJOR_REVISIONS`

Not READY_WITH_MINOR_REVISIONS: bibliography is PARTIAL (21/21 identities VERIFIED; most venue/DOI UNVERIFIED) and Stage-B raw traces are MISSING_LOCALLY. These are documentation/provenance blockers, not scientific contradictions. No new experiment is required to finish this package.

## 2. Integrity flags

| Flag | Value |
| --- | --- |
| NEW_LIVE_EXPERIMENTS | 0 |
| Q2_RERUN | false |
| API_CALLS | 0 |
| LLM_CALLS | 0 |
| NETWORK_CALLS | 0 |
| LIVE_EVAL | false |
| P1_MODIFIED | false |
| P2_MODIFIED | false |
| Q2_EVIDENCE_MODIFIED | false |

## 3. Frozen evidence (rechecked this pass)

| Artifact | SHA-256 | Match |
| --- | --- | --- |
| P1 `datasets/frozen/p1_mechanism_v1.0.0/dataset.jsonl` | `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` | True |
| P2 `datasets/frozen/p2_agentic_v0.1.0/dataset.jsonl` | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` | True |
| Q2 `predictions.jsonl` | `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6` | True |
| Q2 evidence commit | `b075df0f5ec5ad11ede76ac4e4079cade15208f1` | — |

## 4. Authoritative numbers (unchanged)

432/432 · $0.152885 · 9/9 · Tool-HASR 81/192 = 0.421875 · Judge-ASR 186/192 = 0.96875 · M3=108 · M4=3 · INVALID 192/136 · n=16/cell

Δ vs D0: T0 −0.6875/−0.2500/−0.5625; T1 −0.7500/−0.3125/−0.6250; T2 −0.6875/−0.2500/−0.5625; T3 −0.5625/−0.1875/−0.5000.

## 5. Status summary

| Dimension | Status |
| --- | --- |
| NOVELTY_STATUS | PARTIAL_GAP |
| STAGE_B_TRACE_STATUS | MISSING_LOCALLY |
| BIBLIOGRAPHY_STATUS | PARTIAL |
| MANUSCRIPT_STATUS | INTERNALLY_CONSISTENT_14_SECTIONS_TABLES_1_TO_6 |
| REPRODUCIBILITY_STATUS | PARTIAL |
| CENTRAL_CLAIM | PARTIALLY_SUPPORTED / PILOT-SCALE |
| VENUE_STATUS | NOT_SELECTED |

## 6. Issue classification

### CRITICAL
None. No official Q2 number is contradicted; no frozen evidence modified; no unsupported major claim remains.

### MAJOR
- M1. Stage-B raw traces MISSING_LOCALLY — provenance hole for independent T0 recompute.
- M2. Bibliography PARTIALLY_VERIFIED — 21/21 identities VERIFIED from arXiv API; 3/21 FULLY_VERIFIED (BIPIA, AgentDojo, InjecAgent with DOI from official source); 2/21 venue from official conference page; 1/21 from author page; 7/21 from arXiv comment; 8/21 preprint-only.

### MINOR
- m1. n=16 per cell — pilot-scale; not fixable without a new run.
- m2. Qwen-heavy target set — not fixable without new targets.
- m3. Tool-HASR vs Judge-ASR disagreement (81/192 vs 186/192; M3=108) — diagnostic, not causally explained.
- m4. INVALID_TOOL_ARGS confounder (192/136) — retained, not discarded; not proven negligible.
- m5. No venue selected; deadlines/page limits UNVERIFIED.

## 7. Fixed in this pass

- Abstract now explicitly states the Q2 research question; retains 432/432, n=16, 9/9, Tool-HASR vs Judge-ASR, pilot-scale; no internal `scientific_evidence=false` jargon.
- §7 Method now includes a visual control-structure flow diagram (Detector → signal → PHASE1-CORE → intervention → tool execution → Tool-HASR) with varied/locked labels.
- All prior hardening from previous passes retained: 14 sections, Tables 1–6, five-beat introduction, n=16/power, Qwen-heavy, INVALID canonical, Tool-vs-Judge distinct, D3/C4/future-work, external-baseline scope, claim matrix, reviewer matrix, bibliography table, reproducibility FROZEN/DERIVED/INTERPRETIVE, forbidden-word cleanup.

## 8. Remaining limitations

- Stage-B raw traces MISSING_LOCALLY.
- Bibliography: 8/21 remain preprint-only (VENUE_UNVERIFIED); 7/21 venues from arXiv comment (not official proceedings page).
- n=16 pilot-scale.
- Qwen-heavy target set.
- D3 deferred.
- C4 / open adaptive attacker out of scope.
- No matched external baseline.
- INVALID_TOOL_ARGS confounder.
- Tool-HASR vs Judge-ASR disagreement not causally explained.

## 9. Final recommendation

The package is internally consistent and evidence-aligned at pilot scale. Remaining work is provenance (Stage-B traces) and bibliography/venue metadata, not new science. No new experiment is required to finish this package. Keep READY_WITH_MAJOR_REVISIONS until Stage-B traces are packaged read-only or accepted as a documented hole, and venue/DOI verification is completed under a later human-authorized pass.

## 10. Package file index

| File | Role |
| --- | --- |
| `MANUSCRIPT_FINAL.md` | 14-section manuscript (Tables 1–6) |
| `Q2_FINAL_PUBLICATION_STATE.md` | This file |
| `Q2_HIGH_FINAL_AUDIT.md` / `.json` | Comprehensive audit |
| `Q2_NOVELTY_AUDIT.md` | Novelty PARTIAL_GAP |
| `Q2_CLAIM_AUDIT.md` | Claim status table |
| `Q2_REPRODUCIBILITY_AUDIT.md` | FROZEN/DERIVED/INTERPRETIVE |
| `Q2_REPRODUCIBILITY_CHECKLIST.md` | Reproducibility checklist |
| `REVIEWER_RESPONSE_MATRIX.md` | Reviewer A–D responses |
| `CLAIM_EVIDENCE_MATRIX.md` | Full claim matrix |
| `BIBLIOGRAPHY_VERIFICATION.md` | 21-row verification table |
| `VENUE_DECISION_MATRIX.md` | NOT_SELECTED |
| `STAGE_B_EVIDENCE_STATUS.md` | MISSING_LOCALLY |
| `WEAKNESS_CLOSURE_AUDIT.md` / `.json` | Weakness closure |
| `FINAL_SUBMISSION_READINESS.md` / `.json` | Readiness gate |
| `figures/figure3_delta_across_targets.png` | Δ vs D0 |
| `figures/figure4_toolhasr_vs_judgeasr.png` | Tool-HASR vs Judge-ASR |
| `figures/figure5_invalid_tool_args.png` | INVALID diagnostic |
