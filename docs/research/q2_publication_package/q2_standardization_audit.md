# Q2 publication standardization audit

**Date:** 2026-09-17  
**Run:** `p3_stage_c_q2_20260917T123855Z_b075df0f`  
**Commit (evidence):** `b075df0f5ec5ad11ede76ac4e4079cade15208f1`  
**API calls this task:** **0**  
**Frozen P1/P2/Q2 traces modified:** **No**  
**Q2_STANDARDIZATION_STATUS:** **READY_WITH_MAJOR_REVISIONS**  
**Live experiments required to finish this standardization:** **No**

Primary scientific story audited: how much of observed agent-security behavior is attributable to detector behavior versus downstream intervention policy? Q2 tests directional consistency of the Stage-B detector-related Tool-HASR effect across T1–T3.

## Issue register

| ID | Sev | Topic | Finding | Action |
| --- | --- | --- | --- | --- |
| C1 | **CRITICAL** | Claim strength | A SOTA/best/universal-defense paper would be unsupported. Current package results text does **not** assert those (grep hits are meta). | Keep RED list; manuscript must not introduce them |
| C2 | **CRITICAL** | Novelty citations | No verified external bibliography. Inventing cites is forbidden. | Human literature pass before submit |
| M1 | **MAJOR** | Manuscript | Full paper not drafted (blueprint only) | Write from `MANUSCRIPT_BLUEPRINT.md` |
| M2 | **MAJOR** | Benchmark size | n=16 attack/cell; wide Wilson CIs; `scientific_evidence=false` | Pilot framing in abstract |
| M3 | **MAJOR** | External baselines | None on this pack | `BASELINE_GAP.md`; never SOTA |
| M4 | **MAJOR** | Model diversity | 4 targets, Qwen-heavy, OpenRouter only | `LIMITATIONS.md` |
| M5 | **MAJOR** | INVALID_TOOL_ARGS | 192/136 on T1–T3; can affect interpretation diagnostically; S0 unchanged; S2 9/9 | Report as limitation + sensitivity |
| M6 | **MAJOR** | Reproducibility of T0 | Stage-B `predictions.jsonl` absent this checkout | Do not invent; package traces separately |
| M7 | **MAJOR** | Tool-HASR vs Judge-ASR | Judge-ASR 186/192 vs Tool-HASR 81/192; M3=108 | Dual-metric mandatory |
| m1 | **MINOR** | D3 | Deferred, no impl | `D3_AND_C4.md` |
| m2 | **MINOR** | C4 | Open adaptive attacker out of scope; P2 has C4-mini templates only | Do not claim robustness |
| m3 | **MINOR** | Figures | matplotlib unavailable; specs+script only | Render offline later from JSON |
| m4 | **MINOR** | Cost reporting | Token-USD vs normalized weights easy to conflate | Table 7 + STATISTICAL_REPORTING |
| m5 | **MINOR** | Frozen wording | Manifest says “generalize (same sign)” | Paraphrase in paper; don’t edit traces |
| m6 | **MINOR** | Δ CI | Not pre-registered | Do not fabricate |
| O1 | **OPTIONAL** | P3 taxonomy phrasing | `P3_DETECTOR_TAXONOMY.md` calls D1 a “production/scientific baseline” | Qualify if cited |
| O2 | **OPTIONAL** | Q2 policy coverage | B0/STATIC not in 432 live arms | Disclose reduced design |

## Focus checklist

1. **Benchmark size** — MAJOR (M2). Pilot n=16.
2. **External baseline gap** — MAJOR (M3). Documented, no invented numbers.
3. **INVALID_TOOL_ARGS** — MAJOR diagnostic (M5). Recompute matches official 192/136.
4. **Model diversity** — MAJOR (M4). Four models; not universal.
5. **D3 deferred** — MINOR (m1). No fake results.
6. **C4 scope** — MINOR (m2). Out of claim scope.
7. **Statistical reporting** — numerators/denominators/Wilson on rates present; Δ CI absent by design; no significance fishing.
8. **Novelty/related work** — CRITICAL for submission (C2) until cites verified; methodological contribution is defensible if bounded.
9. **Claim strength** — results package GREEN for scoped Δ/sign; RED for SOTA/best.
10. **Reproducibility** — SHAs match; Stage-B traces missing this tree (M6).
11. **Figures/tables** — specs generated from JSON; PNGs not rendered.
12. **Cost reporting** — $0.152885 historical live; weights ≠ USD.
13. **Tool-HASR vs Judge-ASR** — different endpoints; Tool-HASR primary.

## Verdict rationale

Evidence is internally consistent (432/432, hashes, 9/9 signs, INVALID recompute). The study is **not journal-submit-ready** until a manuscript exists, citations are verified, T0 traces are packaged or the gap is accepted, and pilot/baseline/diversity limits stay in the abstract. No new live LLM work is required for those revisions.
