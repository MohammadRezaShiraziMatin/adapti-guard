# Q2 reproducibility checklist

**This packaging:** API=0, LLM=0, NETWORK=0, LIVE_EVAL=false.  
**REPRODUCIBILITY_STATUS = PARTIAL**  
Do not claim full reproducibility while Stage-B raw traces remain missing.

Classes: **FROZEN** · **DERIVED** · **INTERPRETIVE**. Missing fields labeled **MISSING**. Nothing inferred.

## A. FROZEN primary evidence

| Field | Class | Status | Value |
| --- | --- | --- | --- |
| Repository | FROZEN | VERIFIED pointer | https://github.com/Mohammadreza583/adapti-guard |
| Packaging branch | INTERPRETIVE | documentation | `cursor/q2-publication-hardening-f6f3` |
| Q2 evidence commit | FROZEN | VERIFIED | `b075df0f5ec5ad11ede76ac4e4079cade15208f1` (user typo `…edeaf4c…` is **not** a git object) |
| Q2 run ID | FROZEN | VERIFIED | `p3_stage_c_q2_20260917T123855Z_b075df0f` |
| Stage-B run ID | FROZEN | VERIFIED pointer | `p3_stage_b_20260916T235438Z_7e401714` |
| P1 SHA-256 | FROZEN | VERIFIED file match | `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` |
| P2 SHA-256 | FROZEN | VERIFIED file match | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` |
| Q2 predictions SHA-256 | FROZEN | VERIFIED file match | `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6` |
| Benchmark version | FROZEN | VERIFIED | `p2_agentic_v0.1.0` |
| T0 | FROZEN | VERIFIED lock | `qwen/qwen-2.5-7b-instruct` (not re-run) |
| T1 | FROZEN | VERIFIED lock | `qwen/qwen3-30b-a3b` |
| T2 | FROZEN | VERIFIED lock | `google/gemma-3-27b-it` |
| T3 | FROZEN | VERIFIED lock | `qwen/qwen3.5-35b-a3b` |
| Judge | FROZEN | VERIFIED lock | `qwen/qwen-2.5-72b-instruct` |
| Detector identities | FROZEN | VERIFIED lock | D0/D1/D2/D4; D3 deferred |
| Policy | FROZEN | VERIFIED lock | PHASE1-CORE |
| Thresholds | FROZEN | VERIFIED | is_injection=0.25; risk 0.25/0.60 |
| Action costs | FROZEN | VERIFIED | A0=0, A1=0.10, A2=0.25, A3=0.50 (normalized, not USD) |
| Temperature | FROZEN | VERIFIED | 0.0 |
| Cache | FROZEN | VERIFIED | false |
| Seed | FROZEN | VERIFIED | 42 |
| Arm count (Q2 live) | FROZEN | VERIFIED | 432/432 |
| Sample size | FROZEN | VERIFIED | n=16 attack arms per cell |
| Historical cost | FROZEN | VERIFIED | $0.152885 |
| Historical live API | FROZEN | VERIFIED | 2061 |
| LIVE_EVAL historical run | FROZEN | VERIFIED | true |
| scientific_evidence | FROZEN | VERIFIED | false |

P1/P2/Q2 raw traces were **not modified** this turn. P1_MODIFIED=false. P2_MODIFIED=false. Q2_TRACE_MODIFIED=false. Q2_RERUN=false.

## B. DERIVED evidence

| Field | Class | Status | Value |
| --- | --- | --- | --- |
| figure source scripts | DERIVED | VERIFIED | `render_figures_offline.py`, `generate_tables_figures.py` |
| figure3 SHA-256 | DERIVED | VERIFIED file | `cc8ee54afa73af8d0d6ca6025fe9e403d13e335cd2dd9478f2fb00dbbd124a0a` |
| figure4 SHA-256 | DERIVED | VERIFIED file | `747f1b807fd18d2cf9c44a717363ff44b4e9c6ab36eb31b1d0dac0ffa1445304` |
| figure5 SHA-256 | DERIVED | VERIFIED file | `f737805f97fab25bbb302bbeccdf37f731e753c7cba554232c7da104bfb1f21a` |
| statistics JSON | DERIVED | VERIFIED | `q2_final_statistics.json` |
| Wilson 95% CI on rates | DERIVED | derived from locked counts | not a preregistered Δ CI |
| INVALID recompute | DERIVED | VERIFIED on Q2 live traces | 192 events / 136 arms |
| S2 sign agreement | DERIVED | VERIFIED | 9/9; 0 S0→S2 flips |
| T0 PHASE1-CORE packaged rates | DERIVED from Q2 live report, not raw Stage-B recompute | official reuse | Tool-HASR 28/64; Judge-ASR 55/64; M3=33; M4=6 |

## C. INTERPRETIVE documentation

| Field | Class | Status | Value |
| --- | --- | --- | --- |
| LIVE_EVAL this packaging | INTERPRETIVE | VERIFIED | false |
| manuscript FINAL | INTERPRETIVE | documentation | `MANUSCRIPT_FINAL.md` |
| manuscript FINAL SHA-256 | INTERPRETIVE | this pass | `9e4b7498997c1b6772894ef8a6dc70a1d25ac3d6ce9631830d890c3b779d1bce` |
| novelty class | INTERPRETIVE | documentation | PARTIAL_GAP |
| venue decision | INTERPRETIVE | documentation | `VENUE_STATUS = NOT_SELECTED` (deadlines UNVERIFIED) |
| central claim | INTERPRETIVE | documentation | PARTIALLY_SUPPORTED / PILOT-SCALE |
| raw trace availability | INTERPRETIVE of search | MISSING | Stage-B `predictions.jsonl` not in workspace, git objects, branches, or tags |

## D. Missing local artifacts

| Field | Status | Value |
| --- | --- | --- |
| Stage-B `predictions.jsonl` | **MISSING** | `STAGE_B_TRACE_STATUS=MISSING_LOCALLY` |
| Stage-B `metrics.json` / `manifest.json` as run dir | **MISSING** | not on this checkout; git object-path hits for that run dir: 0 |
| recorded Stage-B pred SHA | RECORDED, not re-hashed | `7b0b72d942dae988d87acf238424c9f2d331b62d5ec582c9ba7d9bfbb293c214` (pointer only) |
| operator-stated Stage-B 124/192 | NOT_FOUND_ON_THIS_CHECKOUT | recorded in `STAGE_B_EVIDENCE_STATUS.md` only; not used as locally verified manuscript rates |
| matplotlib | **MISSING** | stdlib zlib PNG used instead (no network install) |
| bibliography venues/DOI (most) | **UNVERIFIED** | AgentDojo/BIPIA operator-supplied, not re-fetched |
| Q2 p-values | **MISSING** (not pre-registered) | not manufactured |

**Official Stage-B reported result** (T0 PHASE1-CORE packaged in the Q2 live report) is distinct from **locally reproducible raw-trace availability** (MISSING_LOCALLY). Independent recomputation of T0 from locally available traces was **not performed**.
