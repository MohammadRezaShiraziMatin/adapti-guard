# Q2 Publication Evidence Inventory

**Generated:** 2026-09-17 · **API calls this task:** 0 · **Frozen evidence modified:** No

| ID | Path | Status | Role | Primary/Supporting |
| --- | --- | --- | --- | --- |
| P1_PACK | `datasets/frozen/p1_mechanism_v1.0.0` | FROZEN | mechanism benchmark | supporting |
| P2_PACK | `datasets/frozen/p2_agentic_v0.1.0` | FROZEN | agentic tool benchmark for P3/Q2 | primary_benchmark |
| L1 | `experiments/real_llm_eval/P1_MECHANISM_L1/l1_p1m_full_20260915T160302Z_ef2e98c3` | LIVE_COMPLETE | policy pilot on P1 (judge-aliased HASR) | supporting |
| P2_STAGE_B | `experiments/real_llm_eval/P2_AGENTIC_L2/p2_agentic_stage_b_20260916T165133Z_2bb84aa7` | LIVE_COMPLETE | Tool-HASR protocol pilot | supporting |
| P3_STAGE_A | `experiments/real_llm_eval/P3_DETECTOR_COMPARISON/p3_stage_a_smoke_20260916T212910Z_964ae7fe` | LIVE_SMOKE | infra smoke | supporting_non_scientific |
| P3_STAGE_B | `experiments/real_llm_eval/P3_DETECTOR_COMPARISON/p3_stage_b_20260916T235438Z_7e401714` | LIVE_COMPLETE_FORENSIC_PASS | T0 reference detector×policy; Δ_T0 source | primary_for_T0 |
| P3_DIAGNOSTIC_CLOSURE | `tests/test_p3_diagnostic_closure.py + Stage-B verify_recompute` | OFFLINE_COMPLETE | forensic/integrity closure | supporting |
| Q2_PROTOCOL | `src/adapti_guard/experiments/p3_stage_c_q2.py` | FROZEN_PROTOCOL | RQ-C2 design locks | primary_protocol |
| Q2_MODEL_LOCK | `src/adapti_guard/experiments/p3_stage_c_q2_lock.py` | FROZEN_LOCK | T1–T3 selection + pricing + budget | primary_protocol |
| Q2_LIVE | `experiments/real_llm_eval/P3_DETECTOR_COMPARISON/p3_stage_c_q2_20260917T123855Z_b075df0f` | LIVE_COMPLETE | cross-target Δ consistency | primary |
| Q2_FORENSIC | `experiments/real_llm_eval/P3_DETECTOR_COMPARISON/p3_stage_c_q2_20260917T123855Z_b075df0f/p3_q2_forensic_audit.json` | PASS | integrity audit | primary_integrity |
| Q2_RAW | `experiments/real_llm_eval/P3_DETECTOR_COMPARISON/p3_stage_c_q2_20260917T123855Z_b075df0f/predictions.jsonl` | RETAINED | raw traces for recompute | primary_raw |
| Q2_RECOMPUTE | `experiments/real_llm_eval/P3_DETECTOR_COMPARISON/p3_stage_c_q2_20260917T123855Z_b075df0f/recompute.json` | DERIVED | post-run independent metrics | supporting |
| TRACK_A_SMOKE | `experiments/real_llm_eval/TRACK_A_PHASE2_SMOKE/20260917-120226` | PASS_SEPARATE | pipeline smoke | NOT_scientific_NOT_pooled |

## Notes
- Track-A / Stage-A smoke are **not** scientific evidence and must not be pooled.
- P3 Stage-B and Q2 retain `scientific_evidence=false`; frame as protocol-complete pilot consistency.
- T0 Tool-HASR/Δ reused from Stage-B; not re-run under Q2 harness.

## Integrity hashes (read-only check)

- `q2_predictions_sha256`: `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6`
- `stage_b_predictions_sha256`: `7b0b72d942dae988d87acf238424c9f2d331b62d5ec582c9ba7d9bfbb293c214`
- `p1_pack_sha256`: `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235`
- `p2_pack_sha256`: `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd`
