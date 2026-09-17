# Final submission readiness (Q2)

**Date:** 2026-09-17  
**Branch:** `cursor/q2-publication-hardening-f6f3`  
**CI:** 2/2 PASS (software-integrity signal only; not publication acceptance)

## STATUS: READY_WITH_MAJOR_REVISIONS

Not `SUBMISSION_READY`: bibliography metadata is not sufficiently verified for camera-ready submission, and Stage-B raw traces remain a scientific-integrity/reproducibility hole. Not `BLOCKED`: the methods+pilot package is internally consistent, claims are evidence-aligned, figures/tables exist, and no new experiment is required to finish this package.

CI PASS is **not** treated as submission readiness.

## Gate checklist

| Gate | Met? | Note |
| --- | --- | --- |
| Manuscript internally consistent | Yes | Authoritative Δ and n/N match `q2_final_statistics.json` |
| Claims evidence-aligned | Yes | Scoped to pilot directional consistency; `scientific_evidence=false` |
| Bibliography sufficiently verified | **No** | 21/21 identities VERIFIED; most venue/DOI UNVERIFIED; 2 operator-supplied not re-fetched |
| Figures/tables present | Yes | Figures 3–5 PNG; Tables 1–7 in `MANUSCRIPT_FINAL.md` |
| Reproducibility complete enough | **Partial** | Frozen P1/P2/Q2 hashes rechecked; Stage-B raw traces MISSING |
| No unresolved critical integrity issue | **No** | Stage-B `predictions.jsonl` absent; T0 not independently recomputed |

## Flags

| Flag | Value |
| --- | --- |
| API_CALLS | 0 |
| LLM_CALLS | 0 |
| NETWORK_CALLS | 0 |
| LIVE_EVAL | false |
| Q2_RERUN | false |
| P1_MODIFIED | false |
| P2_MODIFIED | false |
| Q2_TRACE_MODIFIED | false |
| novelty_class | PARTIAL_GAP |
| venue_status | NOT_SELECTED |
| bibliography_status | PARTIAL |
| stage_b_raw_trace | MISSING_LOCALLY |
| scientific_evidence | false |

## Authoritative numbers (unchanged)

432/432 · $0.152885 · 9/9 · T1–T3 Tool-HASR 81/192 = 0.421875 · Judge-ASR 186/192 = 0.96875 · M3=108 · M4=3 · INVALID 192/136 · n=16/cell

Δ vs D0: T0 −0.6875/−0.2500/−0.5625; T1 −0.7500/−0.3125/−0.6250; T2 −0.6875/−0.2500/−0.5625; T3 −0.5625/−0.1875/−0.5000.

P1 `1a0b0053…dd235` · P2 `32b40e3b…8d64dd` · Q2 pred `2a2c2f31…886cc6` · commit `b075df0f5ec5ad11ede76ac4e4079cade15208f1` — local file hashes rechecked this pass.

## Required for submission (not new science)

1. Package Stage-B traces read-only, or accept MISSING_LOCALLY as a documented hole in the submitted PDF.
2. Verify remaining venues/DOIs from official publisher pages (network allowed only under a later human-authorized bibliography pass).
3. Human venue selection after `VENUE_DECISION_MATRIX.md`; apply that venue’s template.
4. Keep `scientific_evidence=false` and n=16 in the public abstract.

## Future-study recommendations (not required to submit this package)

Matched external baselines; larger n; more model families; D3 after an offline embedding lock; open adaptive attacker (C4). Those are new studies (MASTER_PROMPT rule 6).

Machine-readable: `FINAL_SUBMISSION_READINESS.json`.
