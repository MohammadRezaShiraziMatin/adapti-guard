# Canonical Track L1 configuration (pre-live hygiene)

**Status:** documentation / config hygiene only — **API=0**  
**Does not authorize live evaluation.** See `LIVE_EVALUATION_GATE.md`.

---

## Canonical L1 path

```text
Frozen P1  datasets/frozen/p1_mechanism_v1.0.0/
           SHA-256 1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235
        →  target_2   (qwen/qwen-2.5-7b-instruct)   via OpenRouter
        →  policies   B0 / STATIC-A1 / PHASE1-CORE
        →  judge_fallback  (qwen/qwen-2.5-72b-instruct) via OpenRouter
```

| Role | Config key | Model ID | Provider |
| --- | --- | --- | --- |
| Target | `target_2` | `qwen/qwen-2.5-7b-instruct` | openrouter |
| Judge | `judge_fallback` | `qwen/qwen-2.5-72b-instruct` | openrouter |
| Undefended | `B0` | — | — |
| Static low | `STATIC-A1` (alias `L1`) | — | — |
| Adaptive | `PHASE1-CORE` | — | — |

**Backend:** `openrouter` only for L1 primary results. Do **not** use `AUTO` (may select Gemini), `groq`, or `gemini` for canonical L1 claims.

**Forbidden in primary L1 results:** `ORACLE_RISK`, `ORACLE_BLOCK` (diagnostic / label-using only), `groq_target`, `groq_judge`, `judge_primary` (Groq), `judge` (Claude Sonnet key), `cerebras_judge`, `gemini_*`.

---

## Runner audit

| Script | Role | Verdict |
| --- | --- | --- |
| `scripts/run_p1_mechanism_l1.py` | Locked Track L1 runner (`p1_mechanism_v1.0.0`, `target_2` + `judge_fallback`, arms B0/STATIC-A1/PHASE1-CORE) | **Canonical L1** — Stage 0 default (no API); Stage A/B require explicit flags + human gate for B |
| `src/adapti_guard/experiments/p1_mechanism_l1.py` | Pack/hash/preflight/scoring helpers for L1 | Shared library (no API) |
| `scripts/run_phase1_confirm.py` | Locked Track B confirm (`phase1_confirm_v1`, `target_2` + `judge_fallback`) | **Historical canonical** for Track B — not L1 pack |
| `scripts/run_vnext_confirm.py` | Locked Track A confirm (`vnext_confirm_v1`, same keys) | **Historical canonical** for Track A — not L1 pack |
| `scripts/run_real_eval.py` → `experiments/REAL_LLM_EVAL/run.py` | Generic real-LLM entry | **Legacy / generic** — defaults now aligned to `target_2` + `judge_fallback`, but **not** the L1 pack lock; do not treat as L1 AUDIT runner without `--stage-a` / `--stage-b` on the P1 runner |

Stage A/B live spend still requires human authorization (`LIVE_EVALUATION_GATE.md`). Default CLI path is `--preflight-only` / Stage 0.

---

## Config key retention

All keys in `configs/models.yaml` retain **code or test dependencies**. None were deleted in the hygiene pass. Mis-matched **descriptions** were corrected; roles are labeled in-file (canonical L1 / exploratory / provider-specific / local-dev).

---

## Explicit non-claims

- No live LLM/API execution from this document.  
- P1 frozen bytes unchanged by hygiene.  
- Track A / B AUDIT folders unchanged.
