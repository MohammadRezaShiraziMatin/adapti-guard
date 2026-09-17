# Q2 reproducibility checklist

**API calls this packaging:** 0. Missing fields labeled **MISSING**. Nothing inferred.

| Field | Status | Value / pointer |
| --- | --- | --- |
| repository commit (Q2 run) | VERIFIED | `b075df0f5ec5ad11ede76ac4e4079cade15208f1` (`manifest.json`) |
| Q2 run ID | VERIFIED | `p3_stage_c_q2_20260917T123855Z_b075df0f` |
| harness | VERIFIED | `p3.0.0-live-stage-c-q2` |
| design | VERIFIED | `B_REDUCED_Q2` |
| P1 SHA-256 | VERIFIED (file match) | `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` |
| P2 SHA-256 | VERIFIED (file match) | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` |
| Q2 predictions SHA-256 | VERIFIED (file match) | `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6` |
| Stage-B run ID | VERIFIED (pointer) | `p3_stage_b_20260916T235438Z_7e401714` |
| Stage-B predictions SHA | RECORDED, not re-hashed | `7b0b72d942dae988d87acf238424c9f2d331b62d5ec582c9ba7d9bfbb293c214` in `q2_final_statistics.json` |
| Stage-B `predictions.jsonl` | **MISSING** on this checkout | T0 rates from Q2 report JSON |
| T0 | VERIFIED | `qwen/qwen-2.5-7b-instruct` (not re-run) |
| T1 | VERIFIED | `qwen/qwen3-30b-a3b` |
| T2 | VERIFIED | `google/gemma-3-27b-it` |
| T3 | VERIFIED | `qwen/qwen3.5-35b-a3b` |
| judge | VERIFIED | `qwen/qwen-2.5-72b-instruct` |
| detectors | VERIFIED | D0 `p3.d0.1`; D1 `p3.d1.evidence_phase1.0`; D2 `p3.d2.heuristic.1`; D4 `p3.d4.structured.1` |
| detector config hashes | VERIFIED in prior audit | D0 `9cb8fa1f…`; D1 `489fff17…`; D2 `5936a6c1…`; D4 `1fff765c…`; bundle `9e83b69f…` |
| D3 | VERIFIED deferred | `DEFERRED_NO_OFFLINE_IMPL` |
| policy | VERIFIED | PHASE1-CORE |
| thresholds | VERIFIED | is_injection 0.25; risk 0.25 / 0.60 |
| action costs | VERIFIED | A0=0, A1=0.10, A2=0.25, A3=0.50 (normalized, not USD) |
| temperature | VERIFIED | 0.0 |
| cache | VERIFIED | false |
| seed | VERIFIED | 42 (providers may remain nondeterministic) |
| benchmark version | VERIFIED | `p2_agentic_v0.1.0` |
| LIVE_EVAL (historical run) | VERIFIED | true |
| scientific_evidence | VERIFIED | false |
| budget cap | VERIFIED | $10.0 |
| actual token-USD | VERIFIED | $0.152885 |
| API metadata (historical live) | VERIFIED | 2061 calls; per-target split in `spend.json` |
| API this packaging | VERIFIED | 0 |
| arms | VERIFIED | 432/432, 0 failed |
| integrity / forensic | VERIFIED | PASS / PASS |
| Q2 raw traces | VERIFIED present | `predictions.jsonl`, `event_trace.jsonl`, `disagreement_ledger.jsonl` |
| analysis scripts | VERIFIED present | `p3_stage_c_q2.py`, `p3_stage_c_q2_live.py`, `p3_stage_c_q2_lock.py`, `generate_tables_figures.py` |
| matplotlib PNGs | **MISSING** | module unavailable |
| related-work venues/DOI | **MISSING** | arXiv fields verified |
| human red-team log | **MISSING** | none |
| per-call provider request IDs | **MISSING** | not required by protocol; not synthesized |
| Δ 95% CI | **MISSING** | not pre-registered; not fabricated |

User-facing commit typo `…edeaf4c…` is **not** used. Evidence commit is `…ede76ac…`.

Do not modify frozen packs or Q2 raw traces to “complete” missing Stage-B packaging.
