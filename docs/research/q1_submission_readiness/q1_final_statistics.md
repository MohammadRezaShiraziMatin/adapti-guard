# Q1 Final Statistics Package (existing evidence only)

**JSON:** `/opt/cursor/artifacts/q1_final_statistics.json`  
**No significance fishing. No new live runs.**

## Evidence labeling

| Source | Label |
| --- | --- |
| P1 L1 `l1_p1m_full_20260915T160302Z_ef2e98c3` | Confirmatory for L1 judge-aliased HASR protocol; **not** Tool-HASR |
| P2 Stage-B `p2_agentic_stage_b_20260916T165133Z_2bb84aa7` | Pilot confirmatory for Tool-HASR protocol (`scientific_evidence=true` in run; pack self-states pilot-scale) |
| P3 Stage-B `p3_stage_b_20260916T235438Z_7e401714` | Pre-registered structure; `scientific_evidence=false`; exploratory detector comparison |
| P3 Q2 `p3_stage_c_q2_20260917T123855Z_b075df0f` | Pre-registered RQ-C2; `scientific_evidence=false` |
| S1/S2 INVALID | Pre-registered sensitivity IDs; post-hoc application to traces; not official replacement |
| Cost weight alternatives | Post-hoc offline diagnostic |

## P3 Stage-B PHASE1-CORE Tool-HASR (Wilson 95%)

| Det | n_success/n | rate | Wilson 95% CI |
| --- | ---: | ---: | --- |
| D0 | 13/16 | 0.8125 | [0.570, 0.934] |
| D1 | 2/16 | 0.125 | [0.035, 0.360] |
| D2 | 9/16 | 0.5625 | [0.332, 0.769] |
| D4 | 4/16 | 0.250 | [0.102, 0.495] |

**Δ vs D0:** D1 −0.6875 · D2 −0.25 · D4 −0.5625

## P3 Stage-B overall (all policies)

| Metric | Value |
| --- | --- |
| Tool-HASR | 124/192 ≈ 0.646 |
| Judge-ASR | 163/192 ≈ 0.849 |
| M3 / M4 | 61 / 22 |
| INVALID_TOOL_ARGS | 231 |
| Mean intervention cost (official weights) | 0.078125 |

## Q2 primary (PHASE1-CORE × T0–T3)

- Sign agreement: **9/9** (see `q1_model_generalization_analysis.md`)
- Live Judge-ASR (T1–T3): 186/192 = 0.96875
- M3 / M4 / INVALID (T1–T3): 108 / 3 / 192
- Actual token-USD: $0.152885 / $10 cap
- Verdict: **supported**

## Paired episode analysis

Valid pairing key: `trajectory_id × detector_id × policy_id` across targets (Q2).  
Do not treat raw legacy Stage-B event_ids as cross-target identities.

## INVALID sensitivity

- S0→S2 within-target sign flips: **none**
- S2 cross-target sign agreement: **9/9**
- Official denominators unchanged

## Cost sensitivity

Mean intervention cost moves with alternate weights; Tool-HASR/Δ unchanged (accounting overlay only).

## What is *not* included

- Post-hoc p-value shopping across detectors/targets
- Pooled estimands across P1/P2/P3/Smoke
- Fabricated external baseline statistics
