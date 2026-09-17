# ADAPTI-GUARD Reproducibility Audit

**Date:** 2026-09-17. **API_CALLS=0. LLM_CALLS=0. LIVE_EVAL=false.**

## REPRODUCIBILITY_STATUS = PARTIAL_WITH_EXPLICIT_PROVENANCE_LIMITATION

Full reproducibility is not claimed while Stage-B raw traces remain MISSING_LOCALLY.

## FROZEN evidence (immutable, rechecked this pass)

| Artifact | SHA-256 | Match |
| --- | --- | --- |
| P1 `datasets/frozen/p1_mechanism_v1.0.0/dataset.jsonl` | `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` | True |
| P2 `datasets/frozen/p2_agentic_v0.1.0/dataset.jsonl` | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` | True |
| Q2 `predictions.jsonl` | `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6` | True |
| Q2 evidence commit | `b075df0f5ec5ad11ede76ac4e4079cade15208f1` | — |
| Q2 run ID | `p3_stage_c_q2_20260917T123855Z_b075df0f` | — |
| Stage-B run ID (pointer) | `p3_stage_b_20260916T235438Z_7e401714` | — |

Environment: Python 3.12.3. Backend: OpenRouter (historical). Temperature=0.0, cache=false, seed=42.

## DERIVED evidence

| Artifact | Status |
| --- | --- |
| `q2_final_statistics.json` | VERIFIED (recomputed from traces) |
| Figures 3-5 (stdlib zlib PNG) | VERIFIED (SHA-stable) |
| Wilson 95% CI on rates | DERIVED from locked counts (not preregistered Δ CI) |
| INVALID recompute 192/136 | VERIFIED (matches metrics.json) |
| S2 sign agreement 9/9 | VERIFIED (derived) |

## INTERPRETIVE documentation

Manuscript, claim matrix, novelty audit, limitations, reviewer responses.

## MISSING

| Artifact | Status |
| --- | --- |
| Stage-B `predictions.jsonl` | **MISSING_LOCALLY** (0 git object hits; not reconstructed) |
| Stage-B `metrics.json`/`manifest.json` as run dir | MISSING |
| matplotlib | MISSING (stdlib PNG used) |
| Q2 p-values | MISSING (not preregistered; not manufactured) |

Official Stage-B reported T0 PHASE1-CORE (Tool-HASR 28/64; Judge-ASR 55/64; M3=33; M4=6) is reused from the Q2 live report, explicitly distinguished from independent local recomputation.

Detailed checklist: `docs/research/q2_publication_package/Q2_REPRODUCIBILITY_CHECKLIST.md`.
