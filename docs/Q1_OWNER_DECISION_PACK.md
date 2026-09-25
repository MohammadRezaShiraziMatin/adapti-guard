# Q1 Owner Decision Pack — final fill-in sheet

**HEAD:** `779660f` (update on commit) · **execution_gate:** `BLOCKED` · **p0_freeze_ready:** `false`  
**Agent rule:** Evidence and supported choices only. Do not treat repository values as owner lock. Owner fills blank fields below.

**Immutable (not modified in this workflow):** `configs/models.yaml` · `datasets/frozen/vnext_confirm_v1/dataset.jsonl` · frozen/VNEXT/historical results

---

# P0 — Owner decisions (12 blocking items)

## D01 — Research Questions

**Repository evidence:** No Q1 RQ/H text in contract (`scientific_design.research_questions: NEEDS_DECISION`). Arms B0/B1/B2 in `configs/q1_evaluation_contract.yaml`. VNEXT RQs are separate (`docs/experiments/protocols/VNEXT_PROTOCOL.md`).

**Owner Decision required:**
- RQ1:
- H0:
- H1:

---

## D02 — Endpoint / Estimand / Unit

**Repository evidence:** Contract `endpoints.primary_security: attack_success_rate`; `attack_benign_split: separate_endpoints`. B2 `episode_judgment: final_turn_only` (`b2_adaptive_contract.EPISODE_SUCCESS_RULE`). Unit hints: B0/B1 single-turn episode; B2 final executed turn (`scientific_design.unit_of_analysis` in contract).

**Owner Decision required:**
- Primary endpoint:
- Estimand:
- Unit of analysis:

---

## D03 — Primary Comparisons / α / Holm

**Repository evidence:** Three arms → candidate pairs: B0–B1, B0–B2, B1–B2. Test helper: `mcnemar_exact` (`statistics.paired_attack_test` in contract). Multiplicity helper: `holm_correction` in `src/adapti_guard/evaluation/statistics.py`. Family not preregistered in Q1 contract.

**Supported choices (repo only):** Comparisons — any subset of `{B0 vs B1, B0 vs B2, B1 vs B2}` (owner lists which are primary). Test — `mcnemar_exact`. Correction — `Holm-Bonferroni` via `holm_correction` (family definition is owner choice).

**Owner Decision required:**
- Primary comparison #1:
- Primary comparison #2:
- Primary comparison #3: *(leave blank if fewer than three)*
- α:
- Multiple-comparison family:
- Correction:

---

## D04 — B1

**Repository evidence:** `BASELINE_FACTORIES` in `src/adapti_guard/experiments/defense_baselines.py`; contract `arms.B1` `NEEDS_DECISION`.

**Supported choices (repo only):** exactly one of:
- `B1` → `make_b1_rule_based` (τ=0.25 in `b2_matrix_contract.B1_RULE_THRESHOLD` when used from matrix)
- `STATIC-A3` → `make_l3_fixed_block`
- `STATIC-A1` → `make_l1_fixed_sanitize`

**Owner Decision required:** *(one of: `B1` / `STATIC-A3` / `STATIC-A1`)*

---

## D05 — B2

**Repository evidence:** `B2_LIVE_CONDITION_IDS` in `b2_adaptive_contract.py`; `attack_mode_for_condition_id` in `b2_attack_mode_contract.py`; contract `max_turns: 3`, `episode_judgment: final_turn_only`.

**Supported choices (repo only):**

| condition_id (pick one) | attacker mode (repo mapping) |
|---|---|
| `B2-FIXED-A0`, `B2-FIXED-B1`, `B2-FIXED` | `FixedSequenceAttacker` (`fixed_sequence`) |
| `B2-ADAPTIVE-A0`, `B2-ADAPTIVE-B1`, `B2-ADAPTIVE`, `LIVE-PRO-PI-B2-ADAPTIVE`, `COND-E2-ADAPTIVE-OFFLINE` | `AdaptiveAttacker` (`adaptive_defense_feedback`) |

**Evaluation design (owner picks one scope):**
- `defense-only` — single `condition_id` for Q1 arm B2
- `matrix` — full 2×2 attack-mode matrix as separate registered design (repo supports matrix cells; not default in Q1 contract)

**Owner Decision required:**
- condition_id:
- attacker mode: `FixedSequenceAttacker` / `AdaptiveAttacker`
- evaluation design: `defense-only` / `matrix`

---

## D09 — Statistical Analysis Plan

**Repository evidence:** Contract `statistics.paired_attack_test: mcnemar_exact`; `alpha`, `holm_family`, `effect_size`, `ci_method`, `ties_missing_judge_fail`: `NEEDS_DECISION`. Code: `mcnemar_test`, `holm_correction`, `delta_hat_from_mcnemar_contingency`, Wilson/bootstrap CI in `statistics.py`. VNEXT locked α=0.05 is reference only — not Q1 owner decision.

**Owner Decision required:**
- statistical test:
- α:
- CI:
- effect size / estimand:
- missing outcome:
- judge failure:
- retry:
- exclusion:
- ties:
- multiplicity:

---

## D10 — Claims

**Repository evidence:** Pack 61 attack + 61 benign; primary attack budget 732 (61×4×3); supplementary `merge_with_primary_comparisons: false`; `claims_generalization: NEEDS_DECISION`.

**Owner Decision required:**
- primary claim:
- target/model scope:
- attack scope:
- defense scope:
- generalization boundary:
- explicit limitations:

---

## D11 — Target Model Panel

**Repository evidence:** `configs/models_q1_eval_panel.yaml`, contract `primary_targets.config_keys`.

| Slot | Repository ID | Status | Owner Decision |
|---|---|---|---|
| Qwen | `qwen/qwen3-30b-a3b` | REPO-VERIFIED | LOCK / REJECT |
| Mistral | `mistralai/mistral-small-3.2-24b-instruct` | REPO-VERIFIED | LOCK / REJECT |
| Llama | `meta-llama/llama-3.3-70b-instruct` | REPO-VERIFIED | LOCK / REJECT |
| Gemma 3 27B | *(none in repo)* | UNVERIFIED | LOCK / REJECT — if LOCK, owner supplies exact OpenRouter ID on next line |

**Owner Decision required (Gemma exact ID, only if LOCK):**
- Gemma 3 27B OpenRouter model id:

*(Do not substitute `google/gemma-4-31b-it` without explicit owner ID.)*

---

## D12 — Judges

**Repository evidence:** Panel + contract `judges.*.openrouter_model_id: NEEDS_DECISION`. Archive blindness template: `docs/archive/q1/JUDGE_PROTOCOL.md` (legacy judge models — not Q1 IDs).

| Judge | Exact ID | Verification | Owner Decision |
|---|---|---|---|
| J1 DeepSeek V4 Flash | *(none in repo)* | UNVERIFIED | LOCK / REJECT |
| J2 Grok 4.7 | *(none in repo)* | UNVERIFIED | LOCK / REJECT |

**Owner Decision required (exact OpenRouter id, only if LOCK):**
- J1 model id:
- J2 model id:
- blindness:
- independence:
- disagreement:
- adjudication:

---

## D13 — Subsets

**Repository evidence:** Contract `supplementary_targets.subset` path/sha `NEEDS_DECISION`; J2 `frozen_subset_only`; no Q1 subset manifest verified in repo. Full pack: `datasets/frozen/vnext_confirm_v1/dataset.jsonl` SHA `523c881820710783b5290c76ea5fe5fc01a6341fb427defcba1119fc3e721518`.

**Owner Decision required:**
- supplementary subset: `path + SHA` / `none`
- J2 validation subset: `path + SHA` / `none`

---

## D14 — Leakage / Contamination

**Repository evidence:** Non-oracle arms label-blind in `real_llm_pipeline.py`; contract `label_blind_defense: SUPPORTED`; archive judge input restrictions in `docs/archive/q1/JUDGE_PROTOCOL.md`.

**Supported controls (repo):** Defense path without gold label (non-oracle); judge must not receive baseline ID, defense action, blocked flag, detector scores (archive template).

**Owner Decision required:**
- defense blindness:
- target blindness:
- judge input restrictions:
- dataset leakage policy:
- contamination exclusion policy:

---

## D15 — Runtime

**Repository evidence:** Panel verified targets `temperature: 0.0`, `max_tokens: 512`; contract `budget.hard_cap_usd: 3.0`; live paths set `max_retries=0` in `live_extension_wiring.py` / `live_b0_report.py`; `OpenRouterTargetModel` default `max_retries: 3` in `target_model.py` if not overridden.

**Owner Decision required:**
- temperature:
- top_p:
- seed:
- max_tokens:
- retry:
- timeout:
- malformed output:
- missing output:
- ordering:
- randomization:

---

# P1 — Claim-gated (not part of P0 freeze blockers)

| ID | Status |
|---|---|
| D06 Utility / benign | CLAIM-GATED / OWNER DECISION REQUIRED |
| D08 B1 threshold sensitivity | CLAIM-GATED / OWNER DECISION REQUIRED |
| D16 Order / randomization | CLAIM-GATED / OWNER DECISION REQUIRED |
| D17 Cost reporting | CLAIM-GATED / OWNER DECISION REQUIRED |
| D19 Failure analysis | CLAIM-GATED / OWNER DECISION REQUIRED |

# P2 — Deferred

| ID | Status |
|---|---|
| D07 Ablation | DEFERRED |
| D18 External benchmark | DEFERRED |

---

## After owner fill

When all P0 fields above contain non-placeholder values, commit this file → separate step: validate → propagate to `configs/q1_evaluation_contract.yaml` and `configs/models_q1_eval_panel.yaml` only. No freeze in this document alone.
