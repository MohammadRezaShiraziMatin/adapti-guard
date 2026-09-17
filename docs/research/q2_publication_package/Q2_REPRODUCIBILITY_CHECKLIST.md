# Q2 reproducibility checklist

**This packaging:** API=0, LLM=0, NETWORK=0, LIVE_EVAL=false.  
**REPRODUCIBILITY_STATUS = PARTIAL**  
Do not claim full reproducibility while Stage-B raw traces remain missing.

Missing fields labeled **MISSING**. Nothing inferred.

## A. Frozen primary evidence

| Field | Status | Value |
| --- | --- | --- |
| Q2 evidence commit | VERIFIED | `b075df0f5ec5ad11ede76ac4e4079cade15208f1` (user typo `…edeaf4c…` is **not** a git object) |
| Q2 run ID | VERIFIED | `p3_stage_c_q2_20260917T123855Z_b075df0f` |
| Stage-B run ID | VERIFIED pointer | `p3_stage_b_20260916T235438Z_7e401714` |
| P1 SHA-256 | VERIFIED file match | `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` |
| P2 SHA-256 | VERIFIED file match | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` |
| Q2 predictions SHA-256 | VERIFIED file match | `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6` |
| T0 | VERIFIED lock | `qwen/qwen-2.5-7b-instruct` (not re-run) |
| T1 | VERIFIED lock | `qwen/qwen3-30b-a3b` |
| T2 | VERIFIED lock | `google/gemma-3-27b-it` |
| T3 | VERIFIED lock | `qwen/qwen3.5-35b-a3b` |
| judge | VERIFIED lock | `qwen/qwen-2.5-72b-instruct` |
| detectors | VERIFIED lock | D0/D1/D2/D4; D3 deferred |
| policy | VERIFIED lock | PHASE1-CORE |
| benchmark | VERIFIED | `p2_agentic_v0.1.0` |
| temperature | VERIFIED | 0.0 |
| cache | VERIFIED | false |
| seed | VERIFIED | 42 |
| budget cap | VERIFIED | $10.0 |
| actual historical spend | VERIFIED | $0.152885 |
| historical live API | VERIFIED | 2061 |
| LIVE_EVAL historical run | VERIFIED | true |
| scientific_evidence | VERIFIED | false |

P1/P2/Q2 raw traces were **not modified** this turn.

## B. Derived evidence

| Field | Status | Value |
| --- | --- | --- |
| figure source scripts | VERIFIED | `render_figures_offline.py`, `generate_tables_figures.py` |
| figure3 SHA-256 | VERIFIED file | `cc8ee54afa73af8d0d6ca6025fe9e403d13e335cd2dd9478f2fb00dbbd124a0a` |
| figure4 SHA-256 | VERIFIED file | `747f1b807fd18d2cf9c44a717363ff44b4e9c6ab36eb31b1d0dac0ffa1445304` |
| figure5 SHA-256 | VERIFIED file | `f737805f97fab25bbb302bbeccdf37f731e753c7cba554232c7da104bfb1f21a` |
| statistics JSON | VERIFIED | `q2_final_statistics.json` |
| INVALID recompute | VERIFIED on Q2 live traces | 192 events / 136 arms |
| S2 sign agreement | VERIFIED derived | 9/9 |
| T0 PHASE1-CORE packaged rates | DERIVED from Q2 live report, not raw Stage-B recompute | Tool-HASR 28/64; Judge-ASR 55/64; M3=33; M4=6 |

## C. Documentation

| Field | Status | Value |
| --- | --- | --- |
| packaging branch | documentation | `cursor/q2-publication-hardening-f6f3` |
| LIVE_EVAL this packaging | VERIFIED | false |
| manuscript | documentation | `MANUSCRIPT_V1.md` |
| manuscript SHA-256 | VERIFIED this pass | `e163f709ed4d5b24973ec2958b75466b68e2875526361d0911e72251d6bfaf79` |
| novelty class | documentation | PARTIAL_GAP |
| venue decision | documentation | `VENUE_DECISION_MATRIX.md` (deadlines UNVERIFIED) |

## D. Missing local artifacts

| Field | Status | Value |
| --- | --- | --- |
| Stage-B `predictions.jsonl` | **MISSING** | `STAGE_B_TRACE_STATUS=MISSING_LOCALLY` |
| Stage-B `metrics.json` / `manifest.json` as run dir | **MISSING** | not on this checkout |
| recorded Stage-B pred SHA | RECORDED, not re-hashed | `7b0b72d942dae988d87acf238424c9f2d331b62d5ec582c9ba7d9bfbb293c214` |
| operator-stated Stage-B 124/192 | NOT_FOUND_ON_THIS_CHECKOUT | recorded in `STAGE_B_EVIDENCE_STATUS.md` only; not used as locally verified manuscript rates |
| matplotlib | **MISSING** | stdlib zlib PNG used instead (no network install) |
| bibliography venues/DOI (most) | **UNVERIFIED** | AgentDojo/BIPIA operator-supplied, not re-fetched |
| Q2 p-values | **MISSING** (not pre-registered) | not manufactured |

Classes: **frozen** (immutable evidence) · **derived** (computed after the run) · **documentation** · **missing locally**.
