# Q2 reproducibility audit

**API calls this task:** 0. Missing fields listed; none invented.

## Present (verified this checkout)

| Field | Value / pointer |
| --- | --- |
| Q2 run_id | `p3_stage_c_q2_20260917T123855Z_b075df0f` |
| Q2 git_commit (manifest) | `b075df0f5ec5ad11ede76ac4e4079cade15208f1` |
| Harness | `p3.0.0-live-stage-c-q2` |
| Design | `B_REDUCED_Q2` |
| Benchmark | `p2_agentic_v0.1.0` |
| P1 SHA-256 | `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` (file match) |
| P2 SHA-256 | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` (file match) |
| Q2 predictions SHA-256 | `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6` (file match) |
| Targets | T0 `qwen/qwen-2.5-7b-instruct`; T1 `qwen/qwen3-30b-a3b`; T2 `google/gemma-3-27b-it`; T3 `qwen/qwen3.5-35b-a3b` |
| Judge | `qwen/qwen-2.5-72b-instruct` |
| Detectors | D0 `p3.d0.1`; D1 `p3.d1.evidence_phase1.0`; D2 `p3.d2.heuristic.1`; D4 `p3.d4.structured.1` |
| Detector config hashes | D0 `9cb8fa1f…`; D1 `489fff17…`; D2 `5936a6c1…`; D4 `1fff765c…`; bundle `9e83b69f…` |
| D3 | deferred (`DEFERRED_NO_OFFLINE_IMPL`) |
| Policy | PHASE1-CORE; version `p2_primary_arms_v1`; hash in `build_q2_fixed_locks` |
| Thresholds | is_injection 0.25; risk medium 0.25 / high 0.60 |
| Action costs | A0=0, A1=0.10, A2=0.25, A3=0.50 |
| Temperature | 0.0 |
| Cache | false |
| Seed | 42 (providers may remain nondeterministic) |
| LIVE_EVAL (historical run) | true |
| scientific_evidence | false |
| Budget cap | $10.0 |
| Actual token-USD | $0.152885 |
| API calls (historical live) | 2061 |
| Arms | 432/432 completed, 0 failed |
| Integrity / forensic | PASS / PASS |
| Raw traces | `…/predictions.jsonl`, `event_trace.jsonl`, `disagreement_ledger.jsonl` |
| Analysis scripts | `p3_stage_c_q2.py`, `p3_stage_c_q2_live.py`, `p3_stage_c_q2_lock.py`, `generate_tables_figures.py` |
| Derived artifacts | `q2_final_statistics.json`, this package `derived/` |

User-facing commit typo `…edeaf4c…` is **not** used; evidence commit is `…ede76ac…`.

## Missing / incomplete (do not invent)

| Field | Status |
| --- | --- |
| Stage-B `predictions.jsonl` / traces for `p3_stage_b_20260916T235438Z_7e401714` | **ABSENT from this branch.** T0 metrics live in Q2 report JSON + prior derived INVALID JSON. Hash recorded in `q2_final_statistics.json` `hashes.stage_b_predictions_sha256` but file not here to re-hash |
| matplotlib figure PNGs | **Not rendered** (module unavailable; no network install). Specs + script only |
| Verified related-work bibliography | **Missing** (no invented cites) |
| Full manuscript | Blueprint only |
| Fair external baseline runs | **Missing** (`BASELINE_GAP.md`) |
| D3 implementation / scores | Deferred; no numbers |
| Open C4 adaptive-attacker eval | Out of scope; no numbers |
| Δ 95% CI | **Not pre-registered**; not fabricated |
| Human red-team log | None |
| Exact per-call cache keys / provider request IDs | Not required by protocol; not synthesized |

## Integrity reminder

Do not modify `datasets/frozen/**` or Q2 raw traces to “complete” missing Stage-B packaging. Copying Stage-B traces onto a docs branch, if they exist elsewhere, is a separate human-approved artifact task.
