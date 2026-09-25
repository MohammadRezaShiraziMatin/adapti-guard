# Evidence ledger (numbers from committed artifacts only)

| ID | Tier | Artifact | Manuscript hook | Key metrics |
|----|------|----------|-----------------|-------------|
| Track A VNEXT | confirmatory FAIL | `experiments/real_llm_eval/VNEXT_CONFIRM/20260914-133147/comparison.json` | workshop VNEXT Results | B0 ASR≈0.951, VNEXT-ADAPT ASR≈0.869, n_attack=122, McNemar in file |
| Track B Layer A v3 | historical | `experiments/real_llm_eval/LAYER_A_V3_INTERVENTION/20260913-200544/` | Layer A diagnostic archive | see `comparison.json` in tree |
| Track B Layer A v4 | historical | `experiments/real_llm_eval/LAYER_A_V4_INTERVENTION/20260914-101700/` | Layer A v4 note | see `comparison.json` |
| Layer A v1 | PR18 / frozen | `datasets/frozen` + PR18 artifacts (hub) | Layer A v1 section | not re-derived here |
| Layer A v2 | PR19 / frozen | `datasets/frozen/layer_a_v2` | Layer A v2 section | pack hash in frozen manifest |
| DIAG-B0-B1 | diagnostic | `experiments/.../DIAGNOSTIC_B0_B1/DIAG-B0-B1-LAYER-A-V2-20260924/` | **not** Results | qwen-2.5-7b target_2, 20+20, seed 42 |
| DIAG-MULTI-TARGET | diagnostic | `.../DIAGNOSTIC_MULTI_TARGET/DIAG-MULTI-TARGET-20260924/SUMMARY.json` | **not** Results | qwen B0/B1 0.55/0.45; llama 0.40/0.45; qwen3 0.60/0.60; gpt-oss 0.80/0.75; spend≈$0.201 |
| LIVE-PRO-PI pilots | noncanonical pilot | untracked `LIVE-PRO-PI-*` on workspace | **not citable** | B0/B1 single-turn PI evals |
| B2 campaign MAIN | pilot/diagnostic | `LIVE-PRO-PI-B2-CAMPAIGN-20260924-MAIN/` (local) | B2 mechanism | 5/5 episodes, `final_state_success`, not B1-comparable |
| B2 pilot metrics | pilot | `LIVE-PRO-PI-B2-EVAL-.../derived/metrics.json` + `PILOT_NOT_EVIDENCE.md` | infra pin only | SHA pinned in tests |
| B2 matrix / attack-mode | pilot | `B2-ATTACK-MODE-*` (local) | Fixed vs Adaptive exploratory | not confirmatory |
| MT1 r1+ | *planned* | `experiments/real_llm_eval/MT1/r1/` | future MT1 section | pre-registered in `PROTOCOL_MT1.md` |

**Rules:** Do not promote diagnostic or pilot rows to paper Results without tier upgrade. VNEXT FAIL verdict is immutable.
