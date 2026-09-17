# Q2 reproducibility checklist

**This packaging:** API=0, LLM=0, NETWORK=0, LIVE_EVAL=false.  
Missing fields labeled **MISSING**. Nothing inferred.

| Field | Class | Status | Value |
| --- | --- | --- | --- |
| packaging branch | documentation | VERIFIED | `cursor/q2-final-publication-packaging-f6f3` |
| Q2 evidence commit | frozen | VERIFIED | `b075df0f5ec5ad11ede76ac4e4079cade15208f1` (user typo `…edeaf4c…` is **not** a git object) |
| Q2 run ID | frozen | VERIFIED | `p3_stage_c_q2_20260917T123855Z_b075df0f` |
| Stage-B run ID | frozen pointer | VERIFIED | `p3_stage_b_20260916T235438Z_7e401714` |
| Stage-B `predictions.jsonl` | missing locally | **MISSING** | `STAGE_B_TRACE_STATUS=MISSING_LOCALLY` |
| recorded Stage-B pred SHA | derived record | RECORDED, not re-hashed | `7b0b72d942dae988d87acf238424c9f2d331b62d5ec582c9ba7d9bfbb293c214` |
| P1 SHA-256 | frozen | VERIFIED file match | `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` |
| P2 SHA-256 | frozen | VERIFIED file match | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` |
| Q2 predictions SHA-256 | frozen | VERIFIED file match | `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6` |
| T0 | frozen lock | VERIFIED | `qwen/qwen-2.5-7b-instruct` (not re-run) |
| T1 | frozen lock | VERIFIED | `qwen/qwen3-30b-a3b` |
| T2 | frozen lock | VERIFIED | `google/gemma-3-27b-it` |
| T3 | frozen lock | VERIFIED | `qwen/qwen3.5-35b-a3b` |
| judge | frozen lock | VERIFIED | `qwen/qwen-2.5-72b-instruct` |
| detectors | frozen lock | VERIFIED | D0/D1/D2/D4; D3 deferred |
| policy | frozen lock | VERIFIED | PHASE1-CORE |
| benchmark | frozen | VERIFIED | `p2_agentic_v0.1.0` |
| temperature | frozen | VERIFIED | 0.0 |
| cache | frozen | VERIFIED | false |
| seed | frozen | VERIFIED | 42 |
| budget cap | frozen | VERIFIED | $10.0 |
| actual historical spend | frozen | VERIFIED | $0.152885 |
| historical live API | frozen | VERIFIED | 2061 |
| LIVE_EVAL historical run | frozen | VERIFIED | true |
| LIVE_EVAL this packaging | documentation | VERIFIED | false |
| scientific_evidence | frozen | VERIFIED | false |
| figure source | derived | VERIFIED | `render_figures_offline.py` from `q2_final_statistics.json` + `q2_invalid_args_analysis.json` |
| figure PNGs | derived | VERIFIED | `docs/research/q2_publication_package/figures/figure{3,4,5}_*.png` |
| matplotlib | missing locally | **MISSING** | stdlib zlib PNG used instead (no network install) |
| manuscript version | documentation | VERIFIED | `MANUSCRIPT_V1.md` |
| bibliography venues/DOI | missing | **MISSING** / UNVERIFIED | arXiv fields from existing package records |
| Q2 p-values | not pre-registered | **MISSING** | not manufactured |

Classes: **frozen** (immutable evidence) · **derived** (computed after the run) · **documentation** · **missing locally**.
