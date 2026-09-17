# Q2 Publication — Executive Report

**Date:** 2026-09-17  
**API calls this task:** **0**  
**Frozen evidence modified:** **No** (pre/post hashes recorded in stats JSON)

## 1. Current scientific contribution
Detector behavior can be experimentally isolated from downstream intervention policy under a controlled agent-security protocol, and the observed detector-related Tool-HASR effect remains **directionally consistent** across independently selected targets T1–T3 (relative to T0).

## 2. Strongest evidence
- Stage-B T0 PHASE1-CORE Δ: D1/D2/D4 = −0.6875 / −0.25 / −0.5625  
- Q2: **432/432** arms, **$0.152885**, integrity/forensic **PASS**  
- **9/9** sign agreements; S2 sensitivity also **9/9**, **0** S0→S2 sign flips  
- M3=108, M4=3 on T1–T3 (Tool-HASR ≠ Judge-ASR)

## 3. Main weaknesses
- Pilot n (16 attacks/cell); wide CIs  
- `scientific_evidence=false` on P3/Q2  
- No fair external baselines on same pack  
- INVALID frequent; D3 deferred; limited model diversity; C4 out of scope  
- Manuscript/figures not yet written (package provides blueprint only)

## 4. Required paper revisions
See readiness gate: draft MS, verified related work, render figs/tables from JSON, pilot framing, baseline gap, limitations, purge RED claims.

## 5. Claims that must not appear
Do not assert unbounded generalization, guarantees, detector ranking, production readiness, monetary cost optimality, multi-model proof, or that Judge-ASR is invalid. Use `q2_claims_audit_standardization.md`.

## 6. Tables/figures still required
Tables 1–7 and Figures 1–5 per `q2_paper_blueprint.md` — **specifications done; rendering pending** (no misleading plots created).

## 7. Q2 readiness verdict
**READY_WITH_MAJOR_REVISIONS** (see `q2_standardization_audit.md`). Prior packaging used READY_WITH_REQUIRED_REVISIONS for the same class of writing/citation/baseline gaps.

## 8. Exact files created
- `/opt/cursor/artifacts/q2_claims_audit.json`
- `/opt/cursor/artifacts/q2_claims_audit.md`
- `/opt/cursor/artifacts/q2_claims_matrix.md`
- `/opt/cursor/artifacts/q2_final_statistics.json`
- `/opt/cursor/artifacts/q2_final_statistics.md`
- `/opt/cursor/artifacts/q2_invalid_args_analysis.json`
- `/opt/cursor/artifacts/q2_invalid_args_analysis.md`
- `/opt/cursor/artifacts/q2_judge_tool_forensics.md`
- `/opt/cursor/artifacts/q2_limitations.md`
- `/opt/cursor/artifacts/q2_novelty_audit.md`
- `/opt/cursor/artifacts/q2_paper_blueprint.md`
- `/opt/cursor/artifacts/q2_publication_evidence_inventory.json`
- `/opt/cursor/artifacts/q2_publication_evidence_inventory.md`
- `/opt/cursor/artifacts/q2_publication_executive_report.md`
- `/opt/cursor/artifacts/q2_publication_readiness_gate.md`

## 9. Confirmation: API calls = 0
Yes. This task performed offline recompute/read-only analysis only.

## 10. Confirmation: frozen evidence not modified
Yes. P1/P2 packs, Stage-B predictions, and Q2 predictions/traces were read, not written.
