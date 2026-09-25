# Q1 Owner Decision Pack (evidence-backed owner selection)

**HEAD:** `215e83f` · **execution_gate:** `BLOCKED` · **p0_freeze_ready:** `false`  
**Integrity (do not change in this step):** `models.yaml` `37174858…` · dataset `523c8818…` · panel `50e2e2e5…`  
**Agent rule:** Repository evidence ≠ Owner Decision. Fill only `Owner Decision` lines below; do not treat repo values as owner lock. Agent must not mark a choice as selected.

## Status snapshot

| Tier | IDs | Status |
|------|-----|--------|
| P0 | D01–D05, D09–D15 | NEEDS_OWNER_DECISION / UNVERIFIED (D11 Gemma, D12 J1/J2) |
| P1 | D06, D08, D16, D17, D19 | Claim-gated — owner picks `IN SCOPE` or `DEFERRED` per row |
| P2 | D07, D18 | `DEFERRED` (no action) |

## How to fill

1. Read **Repository Evidence** and **Supported Choices** (repo-provable only).
2. Write your choice on the **Owner Decision** line using bracket notation.
3. If no repo-backed options exist, use `[REQUIRED — NO REPOSITORY DECISION]` and supply explicit text on the next line if needed.
4. After all **P0** fields are filled and committed, a separate agent step may propagate to `configs/q1_evaluation_contract.yaml` / panel (not before sign-off).

## Dependency graph

```text
D01 → D02 → D03 → D04,D05 → D09,D10 → D11,D12 → D13 → D14,D15 → (P1) → runner/preflight/auth
```

## Minimum Q1 freeze scope

**P0** must be `OWNER_DECIDED` before protocol freeze. **P2** D07/D18 do not block minimum freeze.

---

# P0 — Evidence-backed decisions (blocking)

## D01 — Research Questions

| Field | Value |
|---|---|
| Decision ID | D01 |
| Question | Q1-specific research question(s) and H0/H1 per RQ (distinct from VNEXT Track A in `VNEXT_PROTOCOL.md` §2) |
| Repository Evidence | Contract: `scientific_design.research_questions: NEEDS_DECISION`, `hypotheses: NEEDS_DECISION`. Arms B0/B1/B2 defined in `configs/q1_evaluation_contract.yaml`; no Q1 RQ/H text in repo. VNEXT RQ/H are separate (adaptive vs B0 track). |
| Supported Choices | **NO REPOSITORY DECISION — OWNER MUST WRITE RQ** (structure example only in prior checklist: pairwise comparisons on 61 attacks × 4 targets — not pre-selected) |
| Evidence Location | `configs/q1_evaluation_contract.yaml` (`scientific_design.research_questions`, `arms`); `docs/experiments/protocols/VNEXT_PROTOCOL.md` (VNEXT only) |
| Dependency | D02, D03, D10 |
| Blocking | P0 |

**Owner Decision:** `[REQUIRED — NO REPOSITORY DECISION]`

---

## D02 — Primary Endpoint / Estimand / Unit

| Field | Value |
|---|---|
| Decision ID | D02 |
| Question | Primary security endpoint definition: ASR numerator/denominator; blocked-before-target; missing/timeout/malformed; judge failure; B2 episode success; unit of analysis (attack-level paired vs episode) |
| Repository Evidence | Contract `endpoints.primary_security: attack_success_rate` (gold attack, judge `attack_success`). `attack_benign_split: separate_endpoints`. B2: `max_turns: 3`, `episode_judgment: final_turn_only`. Contract `unit_of_analysis`: B0/B1 `SUPPORTED` (single-turn episode via `evaluate_episode`); B2 `SUPPORTED` (final executed turn); `turn_level_primary: MISSING`. `EPISODE_SUCCESS_RULE` in code: judge on final executed turn. Utility co-primary pattern exists in VNEXT memo (`U>=0.95`) but Q1 `utility_gate: NEEDS_DECISION`. |
| Supported Choices | **Security endpoint label (repo):** `attack_success_rate` on gold attacks. **B2 success rule (repo):** `final_turn_only` / `final_state_success`. **Unit (repo, multiple — owner must unify for Q1):** (A) single-turn episode per attack for B0/B1; (B) multi-turn episode, success = final turn for B2; (C) attack-level paired discordant cells for McNemar (implies pairing key across arms — not fully specified in Q1 contract). **Utility:** `[co-primary utility gate / secondary only / not in Q1 scope]` — not locked in Q1 contract |
| Evidence Location | `configs/q1_evaluation_contract.yaml` (`endpoints`, `unit_of_analysis`, `arms.B2`); `src/adapti_guard/evaluation/b2_adaptive_contract.py` (`EPISODE_SUCCESS_RULE`); `src/adapti_guard/evaluation/attack_success.py` (`compute_real_metrics`, `evaluate_episode`); `docs/experiments/protocols/VNEXT_POWER_MEMO.md` (VNEXT utility reference only) |
| Dependency | D01, D03, D09 |
| Blocking | P0 |

**Owner Decision:** `[REQUIRED — NO REPOSITORY DECISION]`

---

## D03 — Primary Comparisons

| Field | Value |
|---|---|
| Decision ID | D03 |
| Question | Which arm pairs are primary; α; pre-registered Holm comparison family |
| Repository Evidence | Contract `primary_comparisons: NEEDS_DECISION`. Three arms B0, B1, B2 → candidate pairs: B0–B1, B0–B2, B1–B2. `statistics.paired_attack_test: mcnemar_exact`; `multiple_comparison: NEEDS_DECISION`. Helpers: `holm_correction`, `mcnemar_test` in `statistics.py`. VNEXT confirmatory family is VNEXT-ADAPT vs B0 only (reference — not auto-applied to Q1). |
| Supported Choices | **Pair subset:** `[B0 vs B1 only / B0 vs B2 only / B1 vs B2 only / any two of three / all three pairs]` (owner must list exact set). **Multiplicity:** `[Holm-Bonferroni across listed pairs / Holm across pairs×targets / other family — owner must specify]` + **α:** `[REQUIRED — NO REPOSITORY DECISION]` (VNEXT reference α=0.05 two-sided in `VNEXT_POWER_MEMO.md` — not Q1 lock) |
| Evidence Location | `configs/q1_evaluation_contract.yaml` (`statistics`, `primary_comparisons`); `src/adapti_guard/evaluation/statistics.py` (`holm_correction`, `mcnemar_test`) |
| Dependency | D01, D02, D09 |
| Blocking | P0 |

**Owner Decision:** `[REQUIRED — NO REPOSITORY DECISION]`

---

## D04 — B1 Definition

| Field | Value |
|---|---|
| Decision ID | D04 |
| Question | Map Q1 arm B1 to exactly one `defense_resolver_key` + factory |
| Repository Evidence | Contract B1: `defense_resolver_key: NEEDS_DECISION`, `factory: NEEDS_DECISION`. `BASELINE_FACTORIES` in `defense_baselines.py`. Default τ=0.25 for rule-based B1 in `b2_matrix_contract.B1_RULE_THRESHOLD`. Historical DIAG used `B1` on layer_a_v2 (not auto-selected for Q1). |
| Supported Choices | `[B1 → make_b1_rule_based (τ=0.25 default in matrix) / STATIC-A3 → make_l3_fixed_block / STATIC-A1 → make_l1_fixed_sanitize]` |
| Evidence Location | `src/adapti_guard/experiments/defense_baselines.py` (`BASELINE_FACTORIES`); `src/adapti_guard/evaluation/b2_matrix_contract.py` (`B1_RULE_THRESHOLD`); `configs/q1_evaluation_contract.yaml` (`arms.B1`) |
| Dependency | D03, D08 (if rule-based B1) |
| Blocking | P0 |

**Owner Decision:** `[B1 / STATIC-A3 / STATIC-A1]`

---

## D05 — B2 Definition / Attack Mode

| Field | Value |
|---|---|
| Decision ID | D05 |
| Question | B2 `condition_id`; defense mode (A0 vs B1 under matrix IDs); attacker mode (`FixedSequenceAttacker` vs `AdaptiveAttacker`); whether Q1 binds defense-only vs full 2×2 attack-mode matrix |
| Repository Evidence | Contract B2: `NEEDS_DECISION` keys; `max_turns: 3` (`LIVE_WIRING_MAX_TURNS`); `episode_judgment: final_turn_only`. `B2_LIVE_CONDITION_IDS` includes: `B2-FIXED`, `B2-ADAPTIVE`, `B2-FIXED-A0`, `B2-FIXED-B1`, `B2-ADAPTIVE-A0`, `B2-ADAPTIVE-B1`, `LIVE-PRO-PI-B2-ADAPTIVE`, `COND-E2-ADAPTIVE-OFFLINE`. `attack_mode_for_condition_id`: `B2-FIXED*` → `fixed_sequence` (`FixedSequenceAttacker`); `B2-ADAPTIVE*` / `LIVE-PRO-PI-B2-ADAPTIVE` → `adaptive_defense_feedback` (`AdaptiveAttacker`). `B2_B1_RELATIONSHIP`: B2 is separate multi-turn protocol from single-turn B1. Contract flags: `Q1_B2_binds_attack_mode: NEEDS_DECISION`, `Q1_B2_binds_defense_only: NEEDS_DECISION`. |
| Supported Choices | **condition_id (repo IDs only):** `[B2-ADAPTIVE-A0 / B2-ADAPTIVE-B1 / B2-FIXED-A0 / B2-FIXED-B1 / B2-FIXED / B2-ADAPTIVE / LIVE-PRO-PI-B2-ADAPTIVE / COND-E2-ADAPTIVE-OFFLINE]`. **Attacker class (derived from ID unless owner overrides wiring):** `[FixedSequenceAttacker / AdaptiveAttacker]`. **Design scope:** `[single condition_id only / full 2×2 matrix as separate experiment — owner must state]` |
| Evidence Location | `src/adapti_guard/evaluation/b2_adaptive_contract.py` (`B2_LIVE_CONDITION_IDS`, `LIVE_WIRING_MAX_TURNS`, `B2_B1_RELATIONSHIP`); `src/adapti_guard/evaluation/b2_attack_mode_contract.py` (`attack_mode_for_condition_id`, `B2_ATTACK_MODE_FIXED`, `B2_ATTACK_MODE_ADAPTIVE`); `src/adapti_guard/evaluation/b2_matrix_contract.py` |
| Dependency | D03, D04 |
| Blocking | P0 |

**Owner Decision:** `[condition_id: ___ ]` · `[FixedSequenceAttacker / AdaptiveAttacker]` · `[defense-only vs attack-mode matrix: ___]`

---

## D09 — Statistical Analysis Plan

| Field | Value |
|---|---|
| Decision ID | D09 |
| Question | α; Holm family (tie to D03); effect-size estimand; CI method/level; ties; missing pairs; judge failure; exclusions; retries (pre-registered) |
| Repository Evidence | Contract: `mcnemar_exact` **SUPPORTED**; `alpha: NEEDS_DECISION`; `holm_family: NEEDS_DECISION`; `effect_size_estimand: NEEDS_DECISION`; `ci_method: NEEDS_DECISION`; `ties_missing_judge_fail: NEEDS_DECISION`. Code: `delta_hat_from_mcnemar_contingency` → \((b_{10}-b_{01})/n_{attack}\); `delta_hat_ci_bootstrap_from_mcnemar_contingency` (bootstrap n=5000 default); Wilson score in `statistics.py`. VNEXT locked α=0.05, McNemar exact (reference only). |
| Supported Choices | **Test (repo):** `mcnemar_exact` only wired as primary in contract. **α:** `[REQUIRED — NO REPOSITORY DECISION]`. **Holm family:** must match D03 list — `[REQUIRED — NO REPOSITORY DECISION]`. **Effect size:** `[delta_hat_from_mcnemar_contingency / other — owner specify]`. **CI:** `[bootstrap_percentile (code default n_bootstrap=5000) / Wilson on proportion / other]`. **Ties / missing / judge fail / exclusion / retry:** `[REQUIRED — NO REPOSITORY DECISION]` (VNEXT §9–§12 patterns exist — not copied into Q1 contract) |
| Evidence Location | `configs/q1_evaluation_contract.yaml` (`statistics`, `scientific_design.statistical_analysis_plan`); `src/adapti_guard/evaluation/statistics.py`; `docs/experiments/protocols/VNEXT_POWER_MEMO.md` (reference) |
| Dependency | D02, D03 |
| Blocking | P0 |

**Owner Decision:** `[REQUIRED — NO REPOSITORY DECISION]`

---

## D10 — Claims / Generalization

| Field | Value |
|---|---|
| Decision ID | D10 |
| Question | Allowed claim scope: models, n=61, dataset pack, supplementary non-pooled, stochasticity, forbidden wording |
| Repository Evidence | Frozen pack `vnext_confirm_v1` 61 attack + 61 benign; primary attack budget 732 (61×4×3). Four primary target **keys** in contract; supplementary `merge_with_primary_comparisons: false`. No formal Q1 claims text in contract (`claims_generalization: NEEDS_DECISION`). Archive judge doc describes blindness rules (legacy judge models — not Q1 J1/J2). |
| Supported Choices | **OWNER MUST SPECIFY** claim boundaries. Repo bounds (factual, not claims): internal pack only unless owner adds external bench; supplementary not pooled into primary Holm family per contract flag; nondeterminism possible unless D15 locks seeds. |
| Evidence Location | `configs/q1_evaluation_contract.yaml` (`dataset`, `primary_episode_budget`, `supplementary_targets`, `scientific_design.claims_generalization`); `docs/archive/q1/JUDGE_PROTOCOL.md` (blindness template) |
| Dependency | D01, D12, D13 |
| Blocking | P0 |

**Owner Decision:** `[REQUIRED — NO REPOSITORY DECISION]`

---

## D11 — Primary Model Panel

| Field | Value |
|---|---|
| Decision ID | D11 |
| Question | Lock each primary target: config key, provider, exact OpenRouter model id, role=target, optional version/snapshot |
| Repository Evidence | Panel file `configs/models_q1_eval_panel.yaml`; contract `primary_targets.config_keys` (4 slots). |
| Supported Choices | Per-row below (owner confirms or supplies ID) |
| Evidence Location | `configs/models_q1_eval_panel.yaml`; `configs/q1_evaluation_contract.yaml` (`primary_targets`) |
| Dependency | D13, D15 |
| Blocking | P0 |

| Slot | Config key | Status | Provider | Model ID (repo) | Source | Owner Decision |
|------|------------|--------|----------|-----------------|--------|----------------|
| Qwen3-30B-A3B | `q1_primary_qwen3_30b_a3b` | REPO-VERIFIED / OWNER-UNLOCKED | openrouter | `qwen/qwen3-30b-a3b` | `models_q1_eval_panel.yaml`; aligned `models.yaml` `model_b` | `[LOCK as listed / REJECT slot]` |
| Mistral Small 3.2 24B | `q1_primary_mistral_small_3_2_24b` | REPO-VERIFIED / OWNER-UNLOCKED | openrouter | `mistralai/mistral-small-3.2-24b-instruct` | panel; `models_mt2` / MT2 evidence | `[LOCK as listed / REJECT slot]` |
| Llama 3.3 70B | `q1_primary_llama_3_3_70b` | REPO-VERIFIED / OWNER-UNLOCKED | openrouter | `meta-llama/llama-3.3-70b-instruct` | panel; MT2 target evidence | `[LOCK as listed / REJECT slot]` |
| Gemma 3 27B | `q1_primary_gemma_3_27b` | **UNVERIFIED** | — | — | No exact Gemma **3 27B** ID in repo; `models.yaml` `model_a` is `google/gemma-4-31b-it` (different product) | `[REQUIRED — supply exact OpenRouter ID after verification / REMOVE from primary panel]` |

**Critical:** Do not substitute `google/gemma-4-31b-it` for Gemma 3 27B without explicit owner ID.

---

## D12 — Judge Protocol / IDs

| Field | Value |
|---|---|
| Decision ID | D12 |
| Question | J1 primary + J2 agreement: exact model IDs; provider; blindness; independence; disagreement / adjudication; J2 subset link (D13) |
| Repository Evidence | Contract `judges.*.openrouter_model_id: NEEDS_DECISION`; J2 `scope: frozen_subset_only`. Panel rows `NEEDS_DECISION`. Archive `JUDGE_PROTOCOL.md`: blindness fields (baseline ID, defense action, blocked flag, detector scores forbidden); legacy judges Claude Sonnet 4 / GPT-4o — **not** Q1 J1/J2 IDs. `models.yaml` `model_c`: `deepseek/deepseek-chat-v3-0324` (different from “DeepSeek V4 Flash” label). |
| Supported Choices | **J1/J2 IDs:** `[REQUIRED — NO REPOSITORY DECISION]` per slot after independent catalog verification. **Blindness (repo template):** adopt archive judge input schema vs owner-defined Q1 schema. **Disagreement:** `[REQUIRED — NO REPOSITORY DECISION]` |
| Evidence Location | `configs/models_q1_eval_panel.yaml` (`q1_judge_*`); `configs/q1_evaluation_contract.yaml` (`judges`); `docs/archive/q1/JUDGE_PROTOCOL.md`; `configs/models.yaml` (`model_c` — not auto-J1) |
| Dependency | D13, D14 |
| Blocking | P0 |

| Role | Config key | Status | Provider | Model ID (repo) | Owner Decision |
|------|------------|--------|----------|-----------------|----------------|
| J1 (DeepSeek V4 Flash) | `q1_judge_deepseek_v4_flash` | **UNVERIFIED** | — | — | `[REQUIRED — exact OpenRouter ID]` |
| J2 (Grok 4.7) | `q1_judge_grok_4_7` | **UNVERIFIED** | — | — | `[REQUIRED — exact OpenRouter ID]` |

---

## D13 — Supplementary / Validation Subsets

| Field | Value |
|---|---|
| Decision ID | D13 |
| Question | Supplementary target execution subset (path + SHA); J2 validation subset; predefined-before-results rule |
| Repository Evidence | `supplementary_targets.subset.path/sha256: NEEDS_DECISION`; `selection_rule: predefined_before_results`. J2 linked to same subset SHA per contract. **No subset manifest file verified in repo** for Q1 supplementary/J2. Full attack pack: 61 rows in `datasets/frozen/vnext_confirm_v1/dataset.jsonl` (SHA `523c8818…`). |
| Supported Choices | **Supplementary execution:** `[full 61 attacks / frozen id-list manifest under datasets/frozen/ — owner must add path+SHA / none — no supplementary live]`. **J2 validation subset:** `[same as supplementary subset / separate manifest — path+SHA / none]`. **Verified subsets in repo for Q1 gate:** `NONE VERIFIED` |
| Evidence Location | `configs/q1_evaluation_contract.yaml` (`supplementary_targets.subset`, `judges.J2_agreement`); `datasets/frozen/vnext_confirm_v1/dataset.jsonl` |
| Dependency | D11, D12 |
| Blocking | P0 |

**Owner Decision:** `[REQUIRED — NO REPOSITORY DECISION]`

---

## D14 — Leakage / Contamination

| Field | Value |
|---|---|
| Decision ID | D14 |
| Question | Dataset leakage; judge/defense label leakage; evaluator prompts; exclusions when contamination suspected |
| Repository Evidence | Contract `label_blind_defense: SUPPORTED` (non-oracle arms). `real_llm_pipeline.py`: adaptive/fixed arms label-blind `(prompt, context)` only; oracle diagnostics bind `label` separately (`ORACLE_*` keys in `BASELINE_FACTORIES` — not Q1 arms). Archive judge protocol: judge must not receive baseline ID, defense action, blocked flag, detector scores. Q1-specific judge input contract not duplicated in Q1 YAML (`gold_label_judge_leakage_rule: NEEDS_DECISION`). |
| Supported Choices | **Defense label access (repo):** non-oracle arms do not receive gold label in defense path. **Judge leakage rule for Q1:** `[adopt archive blindness + owner additions / owner-written Q1 judge contract]`. **Exclusion on suspected contamination:** `[REQUIRED — NO REPOSITORY DECISION]` |
| Evidence Location | `src/adapti_guard/experiments/real_llm_pipeline.py` (label-blind comment ~L375); `docs/archive/q1/JUDGE_PROTOCOL.md`; `configs/q1_evaluation_contract.yaml` (`scientific_design.leakage_contamination`) |
| Dependency | D11, D12 |
| Blocking | P0 |

**Owner Decision:** `[REQUIRED — NO REPOSITORY DECISION]`

---

## D15 — Runtime / Stochasticity / Reproducibility

| Field | Value |
|---|---|
| Decision ID | D15 |
| Question | temperature, top_p, seed, max_tokens, timeout, retry, malformed/missing output; provider snapshot; alignment with $3 hard cap |
| Repository Evidence | Panel verified targets: `temperature: 0.0`, `max_tokens: 512`. Contract `budget.hard_cap_usd: 3.0`, `cache.enabled: false` in panel. Live wiring sets `inner_judge.max_retries = 0`, `inner_target.max_retries = 0` in `live_extension_wiring.py` / `live_b0_report.py`. `OpenRouterTargetModel` default `max_retries: 3` in `target_model.py` if not overridden. **UNSPECIFIED in Q1 contract:** top_p, seed, timeout, malformed handling, episode order/randomization (see D16). |
| Supported Choices | **Repo-partial locks:** `[temperature 0.0 / other]`, `[max_tokens 512 / other]`, `[max_retries 0 for live paths / default 3 / other]`. **Owner must specify:** top_p, seed, timeout, malformed/missing policy, provider snapshot pinning — or mark `UNSPECIFIED` items in execution manifest |
| Evidence Location | `configs/models_q1_eval_panel.yaml`; `configs/q1_evaluation_contract.yaml` (`budget`); `src/adapti_guard/evaluation/live_extension_wiring.py`; `src/adapti_guard/evaluation/target_model.py` |
| Dependency | D11, D12 |
| Blocking | P0 |

**Owner Decision:** `[REQUIRED — NO REPOSITORY DECISION]`

---

# P1 — Claim-dependent (evidence + owner gate)

Owner sets **Claim required?** to `YES` or `NO`, then **Scope** to `IN SCOPE` or `DEFERRED`. If `YES` and scope `IN SCOPE`, decision fields must be filled; if `NO`, may `DEFERRED`.

## D06 — Utility / benign matrix

| Field | Value |
|---|---|
| Repository Evidence | Pack `n_benign: 61`; contract `primary_utility: benign_utility_success`; `benign_episodes: NEEDS_DECISION` (symmetric 732 noted as comment); `benign_matrix_n`, `utility_tier: NEEDS_DECISION`; FPR via blocked on benign in metrics path |
| Supported Choices | **Matrix size:** `[0 benign episodes / 61×4×3 symmetric / other — owner specify]`. **Tier:** `[co-primary gate / secondary / descriptive only]` |
| Evidence Location | `configs/q1_evaluation_contract.yaml`; `src/adapti_guard/evaluation/attack_success.py` |

| Claim required? | Scope | Owner Decision |
|-----------------|-------|----------------|
| `[YES / NO]` | `[IN SCOPE / DEFERRED]` | `[REQUIRED if YES+IN SCOPE]` |

## D08 — B1 threshold τ & sensitivity

| Field | Value |
|---|---|
| Repository Evidence | `B1_RULE_THRESHOLD = 0.25` in `b2_matrix_contract.py` only; Q1 `threshold_sensitivity: MISSING` in contract |
| Supported Choices | If rule-based B1 (D04): `[single τ=0.25 / preregistered grid — owner list / DEFERRED]` |
| Evidence Location | `src/adapti_guard/evaluation/b2_matrix_contract.py`; `configs/q1_evaluation_contract.yaml` |

| Claim required? | Scope | Owner Decision |
|-----------------|-------|----------------|
| `[YES / NO]` | `[IN SCOPE / DEFERRED]` | `[REQUIRED if YES+IN SCOPE]` |

## D16 — Order / randomization

| Field | Value |
|---|---|
| Repository Evidence | Contract `order_randomization: NEEDS_DECISION`; no Q1 shuffle manifest |
| Supported Choices | `[fixed episode order / seeded shuffle — owner specify seed+manifest / DEFERRED]` |
| Evidence Location | `configs/q1_evaluation_contract.yaml` (`scientific_design.order_randomization`) |

| Claim required? | Scope | Owner Decision |
|-----------------|-------|----------------|
| `[YES / NO]` | `[IN SCOPE / DEFERRED]` | `[REQUIRED if YES+IN SCOPE]` |

## D17 — Cost-aware reporting

| Field | Value |
|---|---|
| Repository Evidence | `BudgetLedger`, `estimate_api_cost_usd` in attack_success path; contract `report_token_calls_latency_tradeoff: NEEDS_DECISION`; hard cap $3 |
| Supported Choices | `[report ledger totals only / per-episode cost table / latency — owner specify fields / DEFERRED]` |
| Evidence Location | `src/adapti_guard/evaluation/live_budget_gate.py`; `configs/q1_evaluation_contract.yaml` |

| Claim required? | Scope | Owner Decision |
|-----------------|-------|----------------|
| `[YES / NO]` | `[IN SCOPE / DEFERRED]` | `[REQUIRED if YES+IN SCOPE]` |

## D19 — Failure analysis

| Field | Value |
|---|---|
| Repository Evidence | `taxonomy_ref: SUPPORTED` via VNEXT outcome taxonomy link; `q1_failure_report_spec: MISSING` |
| Supported Choices | `[VNEXT taxonomy tables only / owner-defined Q1 failure table spec / DEFERRED]` |
| Evidence Location | `configs/q1_evaluation_contract.yaml` (`endpoints.success_definition_ref`); `docs/experiments/protocols/VNEXT_PROTOCOL.md` |

| Claim required? | Scope | Owner Decision |
|-----------------|-------|----------------|
| `[YES / NO]` | `[IN SCOPE / DEFERRED]` | `[REQUIRED if YES+IN SCOPE]` |

---

# P2 — Non-blocking (no action)

| Decision ID | Status | Note |
|---|---|---|
| D07 | `DEFERRED` | Ablation plan — separate experiment ID; not in minimum Q1 freeze |
| D18 | `DEFERRED` | `agent-injection-bench` — not referenced in repo |

---

## Signable summary (after fill)

| ID | Blocking | Owner Decision recorded? |
|----|----------|---------------------------|
| D01–D05, D09–D10, D13–D15 | P0 | Owner fills bracket lines above |
| D11–D12 | P0 | Per-row in tables |
| D06,D08,D16,D17,D19 | P1 | Claim gate + scope |
| D07,D18 | P2 | DEFERRED |

After all **P0** fields are filled with non-placeholder values, owner commits/signs this file → separate step: propagate to `configs/q1_evaluation_contract.yaml` / panel **only** for stated values. **No freeze in this step.**
