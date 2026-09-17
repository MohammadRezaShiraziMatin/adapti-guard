# Q2 High Final Audit

**Single comprehensive publication-hardening pass.**
**Date:** 2026-09-17
**Branch:** `cursor/q2-publication-hardening-f6f3` · **Head:** `96e1282be649ffb154d5b80805038a77fb5d7b3`
**API_CALLS=0 · LLM_CALLS=0 · NETWORK_CALLS=0 · LIVE_EVAL=false · Q2_RERUN=false.**

Uses only existing evidence. No new live experiment; no frozen evidence modified.

## 1. Evidence map (claim → evidence → artifact → status)

| Claim | Exact evidence | Artifact | Status |
| --- | --- | --- | --- |
| 432/432 arms completed | `n_results=432`, `n_expected_arms=432` | `metrics.json` | VERIFIED |
| Historical spend $0.152885 | spend record | `spend.json` | VERIFIED |
| 9/9 directional sign agreements | 3 detectors × 3 secondary targets, all NEG vs T0 | `q2_final_statistics.json` | VERIFIED (derived) |
| All D1/D2/D4 Δ NEG on T0–T3 | Δ table | `q2_final_statistics.json` | VERIFIED (derived) |
| T1–T3 Tool-HASR 81/192 | pooled attack arms | `metrics.json` / `q2_final_statistics.json` | VERIFIED |
| T1–T3 Judge-ASR 186/192 | pooled attack arms | same | VERIFIED |
| M3=108, M4=3 | discordant counts | same | VERIFIED |
| INVALID 192 events / 136 arms | `invalid_tool_args_count=192` | `metrics.json` + recompute | VERIFIED |
| n=16 per cell | attack episode-arm unit | manifest | VERIFIED |
| `scientific_evidence=false` | protocol flag | `metrics.json` | VERIFIED |
| Stage-B raw trace | `predictions.jsonl` for `p3_stage_b_20260916T235438Z_7e401714` | git objects / workspace | **MISSING_LOCALLY** |
| Bibliography venues/DOI | publisher pages | n/a (NETWORK=0) | PARTIAL / UNVERIFIED |

## 2. Frozen evidence integrity (this pass)

| Artifact | Expected SHA-256 | Match |
| --- | --- | --- |
| P1 `datasets/frozen/p1_mechanism_v1.0.0/dataset.jsonl` | `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` | True |
| P2 `datasets/frozen/p2_agentic_v0.1.0/dataset.jsonl` | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` | True |
| Q2 `predictions.jsonl` | `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6` | True |

P1_MODIFIED=false. P2_MODIFIED=false. Q2_EVIDENCE_MODIFIED=false. Historical metrics not altered.

## 3. Stage-B trace investigation

Searched: workspace tree, `git log --all --full-history` for `*p3_stage_b_20260916*`, `git rev-list --objects --all` for the run directory, branches, tags, `/opt/cursor`, known artifact dirs.

Result: **0** git object-path hits for `p3_stage_b_20260916T235438Z_7e401714`; no `predictions.jsonl`, `metrics.json`, or `manifest.json` as a standalone Stage-B run dir. Git history contains Stage-B *code* (`7e40171`) and Q2 `predictions.jsonl`, but not Stage-B raw traces.

`STAGE_B_TRACE_STATUS = MISSING_LOCALLY`. Not reconstructed. Not fabricated. Official packaged T0 PHASE1-CORE rates in the Q2 live report (Tool-HASR 28/64; Judge-ASR 55/64; M3=33; M4=6) remain the manuscript T0 source, explicitly distinguished from independent local recomputation. See `STAGE_B_EVIDENCE_STATUS.md`.

## 4. Issue classification

### CRITICAL
None. No official Q2 number is contradicted; no frozen evidence modified; no unsupported major claim remains in `MANUSCRIPT_FINAL.md`.

### MAJOR (documentation/provenance, not fixable without new science or network)
- M1. Stage-B raw traces MISSING_LOCALLY — provenance hole for independent T0 recompute.
- M2. Bibliography PARTIAL — 21/21 identities IDENTITY_VERIFIED; most venue/DOI UNVERIFIED; AgentDojo/BIPIA operator-supplied not re-checked.

### MINOR
- m1. n=16 per cell — pilot-scale; documented, not fixable without a new run.
- m2. Qwen-heavy target set — documented; not fixable without new targets.
- m3. Tool-HASR vs Judge-ASR disagreement (81/192 vs 186/192; M3=108) — diagnostic, not causally explained.
- m4. INVALID_TOOL_ARGS confounder (192/136) — retained, not discarded; not proven negligible.
- m5. No venue selected; deadlines/page limits UNVERIFIED.

### INFORMATIONAL
- i1. matplotlib unavailable; figures rendered with stdlib zlib PNG (no network install).
- i2. CI 2/2 PASS is software-integrity only, not publication acceptance.

## 5. FIX NOW (this pass, documentation only)

- Manuscript rewritten to 14 sections with Tables 1–6.
- Abstract: 432/432, n=16, 9/9, Tool-HASR vs Judge-ASR distinct, pilot-scale; no internal `scientific_evidence=false` string.
- Introduction five-beat (Problem/Gap/Approach/Result/Qualification).
- n=16 stated as pilot-scale with limited precision/power.
- Qwen-heavy target set explicit; not called diverse without qualification.
- INVALID_TOOL_ARGS treated as canonical execution-state category; not automatic success/failure/harmlessness/detector failure.
- Tool-HASR and Judge-ASR kept as distinct measurements.
- D3 deferred (embedding dependency not in locked offline protocol); C4 / open adaptive attackers out of scope.
- External numerical baselines excluded as methodological scope.
- Claim matrix uses SUPPORTED / PARTIALLY_SUPPORTED / NOT_ESTABLISHED; central claim PARTIALLY_SUPPORTED / PILOT-SCALE.
- Reviewer A–D matrix with DOCUMENTATION_FIX / FUTURE_STUDY.
- Bibliography 21-row verification table; extra named papers NOT_IN_PACKAGE.
- Reproducibility checklist split FROZEN / DERIVED / INTERPRETIVE.
- Forbidden-word assertions removed from the live manuscript.

## 6. CANNOT FIX WITHOUT NEW SCIENCE (converted to limitations/future work)

- Sample size (n=16) → pilot-scale limitation; larger n is FUTURE_STUDY.
- Model diversity (Qwen-heavy) → limitation; more families is FUTURE_STUDY.
- D3 → deferred; offline embedding lock + new run is FUTURE_STUDY.
- C4 / open adaptive attacker → out of scope; FUTURE_STUDY.
- External baseline → no matched comparison; FUTURE_STUDY only if a ranking claim is later desired.
- Stage-B raw traces → provenance hole; FUTURE_STUDY to package original bytes read-only.

## 7. Final classification

`Q2_HIGH_STATUS = READY_WITH_MAJOR_REVISIONS`

Not READY: bibliography is PARTIAL and Stage-B raw traces are MISSING_LOCALLY. Not BLOCKED: official Q2 numbers are internally consistent, claims are evidence-aligned, and no unsupported major claim remains. The two MAJOR items are documentation/provenance, not scientific contradictions; no new experiment is required to finish this package.

Machine-readable: `Q2_HIGH_FINAL_AUDIT.json`. Companion files: `Q2_NOVELTY_AUDIT.md`, `Q2_CLAIM_AUDIT.md`, `Q2_REPRODUCIBILITY_AUDIT.md`, `Q2_REVIEWER_ATTACK.md`.
