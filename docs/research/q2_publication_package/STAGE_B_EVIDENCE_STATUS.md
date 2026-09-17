# Stage-B evidence status

**API_CALLS=0. LLM_CALLS=0. NETWORK_CALLS=0. LIVE_EVAL=false.**  
**Q2_RERUN=false. P1_MODIFIED=false. P2_MODIFIED=false. Q2_TRACE_MODIFIED=false.**  
**Search date:** 2026-09-17. **No reconstruction of missing traces.**

## Binding distinction

| Layer | Status |
| --- | --- |
| `STAGE_B_TRACE_STATUS` | **MISSING_LOCALLY** |
| `OFFICIAL_REPORTED_RESULT` | Operator-stated Stage-B aggregate (not found as a local file; not independently recomputed) |
| `LOCAL_RAW_TRACE` | **MISSING_LOCALLY** |
| Independent local recomputation of T0 Tool-HASR / INVALID | **NOT PERFORMED** (raw `predictions.jsonl` absent) |

This file does **not** claim that the operator-stated 124/192 aggregate was re-derived on this checkout.

## Search performed (local only)

Locations searched:

- workspace tree (`/workspace`)
- git objects / `git log --all --full-history` path filter
- git object paths containing `p3_stage_b_20260916`
- branches and tags (name scan)
- `/opt/cursor`
- known artifact dirs (`/tmp`, `/home/ubuntu`)
- Q2 live directory `experiments/real_llm_eval/P3_DETECTOR_COMPARISON/p3_stage_c_q2_20260917T123855Z_b075df0f/`

**Result:** no directory `p3_stage_b_20260916T235438Z_7e401714`, no Stage-B `predictions.jsonl`, no Stage-B `metrics.json` / `manifest.json` as standalone Stage-B run artifacts. Git object-path hits for that run directory: **0**. String `124/192` in the workspace (non-git-internals): **0**.

Therefore the original bytes were **not** preserved, **not** hashed, and **not** copied into this package. No file was fabricated to fill the gap.

## OFFICIAL_REPORTED_RESULT (operator-stated; not found on this checkout)

These numbers are recorded because the publication-hardening brief named them as the official Stage-B reported aggregate. They are **not** present as a hashed local trace. They are **not** used as independently recomputed T0 evidence. They are **not** copied into `MANUSCRIPT_V1.md` as locally verified rates.

| Metric | Operator-stated aggregate |
| --- | --- |
| Tool-HASR | 124/192 |
| Judge-ASR | 163/192 |
| M3 | 61 |
| M4 | 22 |

**Provenance:** operator brief (this packaging task).  
**Local file backing:** **NOT_FOUND_ON_THIS_CHECKOUT**.  
**Reconstruction:** not attempted.

A plausible reading (not proven here) is that 192 is a 16×4-detector×3-policy attack-arm pool from the Stage-B design, whereas Q2’s T0 reuse is **PHASE1-CORE only** (64 attack arms). That reading is **not** an independent recompute.

## LOCAL_RAW_TRACE

**MISSING_LOCALLY**

| Artifact | Present? |
| --- | --- |
| `predictions.jsonl` | No |
| `metrics.json` (Stage-B run dir) | No |
| `manifest.json` (Stage-B run dir) | No |
| SHA-256 of original predictions bytes | Not re-hashed (file absent) |
| Recorded SHA in Q2 derived docs | `7b0b72d942dae988d87acf238424c9f2d331b62d5ec582c9ba7d9bfbb293c214` (pointer only; bytes not on this checkout) |

## What *is* locally verified for T0 (Q2 reuse block; not a raw-trace recompute)

Q2 live report `p3_q2_live_report.json` / `q2_final_statistics.json` reuse Stage-B **PHASE1-CORE** cells for T0. Those cells are the numbers used in the manuscript. They are **official Q2-packaged T0 reuse**, not a local re-read of Stage-B `predictions.jsonl`.

| Metric | Locally packaged T0 PHASE1-CORE | Source |
| --- | --- | --- |
| Tool-HASR | 28/64 = 0.4375 | Q2 live report / `q2_final_statistics.json` (D0+D1+D2+D4 attack arms) |
| Judge-ASR | 55/64 = 0.859375 | same |
| M3 | 33 | same |
| M4 | 6 | same |
| Per-cell Tool-HASR | D0 13/16, D1 2/16, D2 9/16, D4 4/16 | same |
| Stage-B run ID pointer | `p3_stage_b_20260916T235438Z_7e401714` | Q2 manifest / live report |
| T0 re-run | false | live report |

Do **not** treat 28/64 and 124/192 as interchangeable. Do **not** claim independent local recomputation of T0.

## T0 INVALID

Prior derived JSON `q2_invalid_args_analysis.json` records T0 INVALID 61 events / 39 arms. That count is **derived-record**, not re-hashed from Stage-B `predictions.jsonl` on this checkout.

## Implications for reproducibility

`REPRODUCIBILITY_STATUS = PARTIAL`

Full reproducibility of T0 INVALID incidence and of any Stage-B policy arms beyond PHASE1-CORE **cannot** be claimed from this checkout. Q2 live T1–T3 (`predictions.jsonl` SHA `2a2c2f31…886cc6`) remains independently hash-verifiable.

Machine-readable: `STAGE_B_EVIDENCE_STATUS.json`.
