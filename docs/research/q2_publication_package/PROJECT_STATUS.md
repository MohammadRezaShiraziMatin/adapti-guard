# Q2 publication package — project status

**Date:** 2026-09-17  
**This phase:** literature → novelty → evidence synthesis → tables/figures → manuscript → claims audit → reproducibility audit.  
**Not an experimental phase.**

| Lock | Value |
| --- | --- |
| LIVE_EVAL (this packaging) | FALSE |
| API_CALLS (this packaging) | 0 |
| LLM_CALLS | FALSE |
| NETWORK_EXPERIMENTS | FALSE |
| NEW_EXPERIMENTS | FALSE |
| BUDGET_SPEND | $0 |
| Frozen P1 / P2 / Q2 raw traces | **not modified** |

Historical Q2 live spend ($0.152885, 2061 API calls) is **prior evidence**, not this task.

## Evidence classes

| Class | Meaning |
| --- | --- |
| **VERIFIED** | Recomputed or hashed on this checkout, or copied from locked Q2/Stage-B reports that match hashes |
| **DERIVED** | Computed from VERIFIED traces after the run (S1/S2, Wilson CIs, tables) |
| **UNAVAILABLE** | Required for independent recompute but not present on this checkout |
| **NOT CLAIMABLE** | Would require new experiments, unverified citations, or forbidden wording |

## VERIFIED

| Item | Value / pointer |
| --- | --- |
| Q2 run ID | `p3_stage_c_q2_20260917T123855Z_b075df0f` |
| Evidence commit | `b075df0f5ec5ad11ede76ac4e4079cade15208f1` |
| Arms | 432/432 completed, 0 failed |
| Design | `B_REDUCED_Q2`; policy PHASE1-CORE; `scientific_evidence=false` |
| Historical token-USD | $0.152885 / cap $10 |
| Δ sign agreement | 9/9 (D1/D2/D4 × T1–T3 vs T0) |
| D1/D2/D4 vs D0 | NEG on T0, T1, T2, T3 |
| Q2 predictions SHA-256 | `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6` |
| P1 SHA-256 | `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` |
| P2 SHA-256 | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` |
| INVALID_TOOL_ARGS (Q2 live) | 192 unique events, 136 arms (matches official `metrics.json`) |
| Q2 live Tool-HASR | 81/192 (T1–T3 attack arms) |
| Q2 live Judge-ASR | 186/192 |
| M3 / M4 (T1–T3) | 108 / 3 |
| Integrity / forensic | PASS / PASS |
| Related-work arXiv metadata | 21 papers; title/authors/year/id from Hugging Face Hub |

## DERIVED

- Wilson 95% CIs on binomial rates (`q2_final_statistics.json`)
- Δ(d,t), Δ-change, sign agreement
- S1/S2 INVALID sensitivity (`derived_after_run`; not official)
- Table/figure specifications and `generate_tables_figures.py` outputs
- Manuscript claims matrix and peer-review simulation

## UNAVAILABLE

| Item | Status |
| --- | --- |
| Stage-B `predictions.jsonl` for `p3_stage_b_20260916T235438Z_7e401714` | **ABSENT** on this checkout. T0 rates come from Q2 live report JSON. T0 INVALID cited from prior derived JSON. Stage-B SHA recorded as `7b0b72d9…93c214` but file not here to re-hash |
| matplotlib PNGs | Module unavailable; no network install. Specs + mermaid + script only |
| Venue / DOI for related work | Hub metadata did not include venue; marked UNVERIFIED |
| Exhaustive literature proof of “first isolation study” | Not obtainable from a finite Hub search |
| Fair external baseline numbers on this pack | Not run (see `BASELINE_GAP.md`) |
| D3 scores | `DEFERRED_NO_OFFLINE_IMPL` |
| Open adaptive-attacker (C4) eval | Out of claim scope |

## Frozen artifacts (do not edit)

- `datasets/frozen/p1_mechanism_v1.0.0/**`
- `datasets/frozen/p2_agentic_v0.1.0/**`
- `experiments/real_llm_eval/P3_DETECTOR_COMPARISON/p3_stage_c_q2_20260917T123855Z_b075df0f/**` including `predictions.jsonl`
- Dual-track AUDIT folders (Track A FAIL; Track B Phase-1 LIVE)

## Publication artifacts (this package)

See directory listing in `README.md`. Headline deliverables:

- `MANUSCRIPT_V1.md`
- `RELATED_WORK_MATRIX.md` / `.json`
- `NOVELTY_AUDIT.md`
- `CLAIM_EVIDENCE_MATRIX.md`
- `FIGURES_AND_TABLES.md`
- `PUBLICATION_PREPARATION_FINAL.md` / `.json`

## Known limitations (not closed by this phase)

- n=16 attack arms per cell; Wilson CIs wide
- Four targets; Qwen-heavy; OpenRouter runtime
- Frequent INVALID_TOOL_ARGS
- Large M3 (Judge-ASR ≫ Tool-HASR)
- No external baseline on this pack
- D3 deferred; open C4 out of scope
- T0 reused from Stage-B; traces not in this tree
- `scientific_evidence=false` (protocol-complete pilot, not confirmatory)

## Current blockers (publication, not live eval)

1. **MAJOR:** Stage-B raw traces not packaged on this checkout → independent T0 INVALID recompute blocked.
2. **MAJOR:** Related-work venues/DOIs UNVERIFIED → camera-ready bibliography incomplete.
3. **MAJOR:** Figures not rasterized (matplotlib missing).
4. **MAJOR:** No matched external baseline experiment (documented; not fabricated).
5. **MINOR:** No LaTeX/camera-ready formatting; manuscript is Markdown V1.
6. **MINOR:** Finite literature survey; novelty is PARTIAL GAP, not CLEAR GAP.

None of these require re-running Q2.

## Recommended next actions (no live spend unless a human later opens rule 6)

1. Human: attach Stage-B traces as a read-only artifact (do not rewrite).
2. Human: verify venues/DOIs for the 21 arXiv records before submission.
3. Render figures when matplotlib (or equivalent) is available offline.
4. Convert `MANUSCRIPT_V1.md` to venue template after venue category is chosen.
5. Optional future **new** study (not this run): matched external baselines; larger n; more model families; D3 after offline embedding lock.

## NOT CLAIMABLE from current evidence

- SOTA / best / superior / production-ready / universal robustness
- Q2 as confirmatory multi-model study
- Detector ranking
- Judge-ASR invalid
- INVALID negligible
- Track B reverses Track A, or Q2 reverses VNEXT FAIL
- Causal identification in deployment
- Adaptive-attacker robustness

## Readiness

**Q2_STANDARDIZATION_STATUS (prior):** READY_WITH_MAJOR_REVISIONS  
**Q2_PUBLICATION_PREPARATION_STATUS (this phase):** READY_WITH_MAJOR_REVISIONS  

Manuscript V1 exists. Critical evidence is frozen and internally consistent. Remaining blockers are bibliographic verification, missing Stage-B traces, unrendered figures, and the documented baseline gap — not missing Q2 arms.
