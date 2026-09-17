# FINAL Results Tables

All values from `q2_final_statistics.json` (recomputed from traces; matches `metrics.json`). Wilson 95% CIs on rates, derived from locked counts.

## Table 1 — Study design

| Field | Value |
| --- | --- |
| Run ID | `p3_stage_c_q2_20260917T123855Z_b075df0f` |
| Evidence commit | `b075df0f5ec5ad11ede76ac4e4079cade15208f1` |
| Pack | `p2_agentic_v0.1.0` SHA `32b40e3b…8d64dd` |
| Q2 predictions SHA | `2a2c2f31…886cc6` |
| Detectors | D0, D1, D2, D4 (D3 deferred) |
| Policy | PHASE1-CORE |
| Completed | 432/432 |
| n per cell | 16 attack arms |
| Cost | $0.152885 |
| Temperature/cache/seed | 0.0 / false / 42 |

## Table 2 — Target and judge models

| Slot | Model ID | Family | Role |
| --- | --- | --- | --- |
| T0 | qwen/qwen-2.5-7b-instruct | Qwen-2.5 dense | reference, not re-run |
| T1 | qwen/qwen3-30b-a3b | Qwen3 MoE | secondary |
| T2 | google/gemma-3-27b-it | Gemma-3 | secondary |
| T3 | qwen/qwen3.5-35b-a3b | Qwen3.5 MoE | secondary |
| Judge | qwen/qwen-2.5-72b-instruct | Qwen-2.5 dense | locked |

## Table 3 — Primary Δ (Tool-HASR vs D0)

| Target | D1 | D2 | D4 | Signs |
| --- | ---: | ---: | ---: | --- |
| T0 | −0.6875 | −0.2500 | −0.5625 | NEG, NEG, NEG |
| T1 | −0.7500 | −0.3125 | −0.6250 | NEG, NEG, NEG |
| T2 | −0.6875 | −0.2500 | −0.5625 | NEG, NEG, NEG |
| T3 | −0.5625 | −0.1875 | −0.5000 | NEG, NEG, NEG |

9/9 directional agreements. All Δ NEG. T1-T3 pooled Tool-HASR: 81/192 = 0.421875.

## Table 4 — Tool-HASR vs Judge-ASR (T1-T3)

| Scope | Tool-HASR | Judge-ASR | M3 | M4 |
| --- | --- | --- | ---: | ---: |
| T1-T3 pooled | 81/192 = 0.421875 | 186/192 = 0.96875 | 108 | 3 |

## Table 5 — INVALID diagnostics

| Metric | S0 | S1 | S2 |
| --- | --- | --- | --- |
| Events | 192 (retained) | 192 (stratified) | same events on excluded arms |
| Arms | 136/432 | same 136 | excluded: T0=14,T1=19,T2=22,T3=21 |
| Sign agreement | 9/9 | NEG in both strata | 9/9; 0 flips |

## Table 6 — Limitations (19 items)

See `MANUSCRIPT_FINAL.md` Table 6.
