# Q1 Owner Decision Pack (direct owner fill-in)

**HEAD:** `a7e284c` · **execution_gate:** `BLOCKED` · **p0_freeze_ready:** `false`  
**Integrity (unchanged):** `models.yaml` `37174858…` · dataset `523c8818…` · panel `50e2e2e5…`  
**Agent rule:** fill only `Owner Decision` fields below. Do not treat repo evidence as owner lock.

## Status snapshot

| Tier | IDs | Agent status |
|------|-----|----------------|
| P0 | D01–D05, D09–D15 | NEEDS_OWNER_DECISION / UNVERIFIED (D11–D12) |
| P1 | D06, D08, D16, D17, D19 | NEEDS_OWNER_DECISION (claim-gated) |
| P2 | D07, D18 | DEFERRED |

Repo-verified only (not owner lock): `qwen/qwen3-30b-a3b`, `mistralai/mistral-small-3.2-24b-instruct`, `meta-llama/llama-3.3-70b-instruct` in `configs/models_q1_eval_panel.yaml`.

## Dependency graph

```text
D01 → D02 → D03 → D04,D05 → D09,D10 → D11,D12 → D13 → D14,D15 → (P1) → runner/preflight/auth
```

## Minimum Q1 freeze scope

**P0** must be `OWNER_DECIDED` before protocol freeze. **P2** D07/D18 do not block freeze.

---

# P0 — Owner decisions (blocking)

## D01 — Research Questions

**Decision:** Q1-specific RQ(s) and H0/H1 per RQ (distinct from VNEXT Track A `VNEXT_PROTOCOL.md` §2).

**Allowed choices:** Owner must specify explicitly (e.g. pairwise B0 vs B1 / B0 vs B2 / B1 vs B2 on 61 attacks × 4 targets — structure only, not pre-selected).

**Current repository evidence:** `configs/q1_evaluation_contract.yaml` `arms` B0/B1/B2; no Q1 RQ text; VNEXT RQ is separate adaptive-vs-B0 track.

**Dependency:** D02, D03, D10.

**Blocking:** P0 — BLOCKING

**Owner Decision:** _______________________________________________

---

## D02 — Primary Endpoint / Estimand / Unit

**Decision:** ASR numerator/denominator; blocked-before-target; missing/timeout/malformed; judge failure; B2 episode success rule; unit (attack-level paired vs episode).

**Allowed choices:** Owner must specify explicitly. Repo supports episode-level `attack_succeeded` (`real_llm_pipeline` / `compute_real_metrics`); B2 final-turn rule in `b2_adaptive_contract.py` (`EPISODE_SUCCESS_RULE`).

**Current repository evidence:** `endpoints.primary_security` in contract; B2 `max_turns: 3`, `episode_judgment: final_turn_only`.

**Dependency:** D01, D03, D09.

**Blocking:** P0 — BLOCKING

**Owner Decision:** _______________________________________________

---

## D03 — Primary Comparisons

**Decision:** Which pairs are primary (B0 vs B1, B0 vs B2, B1 vs B2); pre-registered comparison family for multiplicity.

**Allowed choices:** Owner must specify explicitly (subset of the three pairwise comparisons).

**Current repository evidence:** `statistics.holm_correction` in `src/adapti_guard/evaluation/statistics.py`; no preregistered family in contract.

**Dependency:** D01, D02, D09.

**Blocking:** P0 — BLOCKING

**Owner Decision:** _______________________________________________

---

## D04 — B1 Definition

**Decision:** Map Q1 arm B1 to exactly one defense resolver key / factory.

**Allowed choices (repo-supported only):**
- `B1` → `make_b1_rule_based` (detector threshold; default τ=0.25 in `b2_matrix_contract.B1_RULE_THRESHOLD`)
- `STATIC-A3` → `make_l3_fixed_block` (unconditional block)
- `STATIC-A1` → `make_l1_fixed_sanitize` (unconditional sanitize)

**Current repository evidence:** `defense_baselines.py`; DIAG-B0-B1 used `B1` on layer_a_v2 (historical, not auto-selected).

**Dependency:** D03, D08 (if rule-based).

**Blocking:** P0 — BLOCKING

**Owner Decision:** _______________________________________________

---

## D05 — B2 Definition / Attack Mode

**Decision:** (1) Defense-only adaptive multi-turn vs also adaptive attacker. (2) Exact B2 `condition_id` and defense mode (A0/B1). (3) Attacker mode if applicable.

**Allowed choices (condition IDs in repo only — do not invent):**
- `B2-ADAPTIVE-A0`, `B2-ADAPTIVE-B1`, `B2-FIXED-A0`, `B2-FIXED-B1`, `B2-FIXED`, `B2-ADAPTIVE`, `LIVE-PRO-PI-B2-ADAPTIVE` (`b2_adaptive_contract.py`, `b2_matrix_contract.py`)
- Attacker: `adaptive_defense_feedback` (`AdaptiveAttacker`) vs `fixed_sequence` (`FixedSequenceAttacker`) — `b2_attack_mode_contract.py`
- `LIVE_WIRING_MAX_TURNS=3` (contract already references)

**Current repository evidence:** B2 is separate protocol from single-turn B1 (`B2_B1_RELATIONSHIP`); matrix 2×2 is optional design, not Q1 default.

**Dependency:** D03, D04.

**Blocking:** P0 — BLOCKING

**Owner Decision:** _______________________________________________

---

## D09 — Statistical Analysis Plan

**Decision:** α; primary test (paired attacks); Holm family tied to D03; effect-size estimand; CI method/level; ties; missing pairs; judge failure; exclusions; retries (must be pre-registered, not post-hoc).

**Allowed choices:** Owner must specify explicitly. Repo helpers: `mcnemar_test`, `holm_correction`, `delta_hat_from_mcnemar_contingency`, Wilson/bootstrap in `statistics.py`. VNEXT uses α=0.05, McNemar exact (reference only — not auto-applied to Q1).

**Current repository evidence:** `statistics` block in contract all `NEEDS_DECISION` except `mcnemar` helper name.

**Dependency:** D02, D03.

**Blocking:** P0 — BLOCKING

**Owner Decision:** _______________________________________________

---

## D10 — Claims / Generalization

**Decision:** Allowed claim scope (models, n=61, internal pack only, supplementary non-pooled, nondeterminism disclaimer, forbidden wording).

**Allowed choices:** Owner must specify explicitly.

**Current repository evidence:** `vnext_confirm_v1` 61+61; 4 primary target keys; supplementary `merge_with_primary_comparisons: false`.

**Dependency:** D01, D12, D13.

**Blocking:** P0 — BLOCKING

**Owner Decision:** _______________________________________________

---

## D11 — Primary Model Panel

**Decision:** Lock each primary target: config key, provider, exact OpenRouter model id, role=target, version/snapshot if used.

| Slot | Config key | Repo status | Provider | Model ID | Owner Decision |
|------|------------|-------------|----------|----------|----------------|
| Qwen3-30B-A3B | `q1_primary_qwen3_30b_a3b` | Repo-verified / Owner-unlocked | openrouter | `qwen/qwen3-30b-a3b` | ______ |
| Mistral Small 3.2 24B | `q1_primary_mistral_small_3_2_24b` | Repo-verified / Owner-unlocked | openrouter | `mistralai/mistral-small-3.2-24b-instruct` | ______ |
| Llama 3.3 70B | `q1_primary_llama_3_3_70b` | Repo-verified / Owner-unlocked | openrouter | `meta-llama/llama-3.3-70b-instruct` | ______ |
| Gemma 3 27B | `q1_primary_gemma_3_27b` | UNVERIFIED | — | — | ______ |

**Allowed choices:** Owner must specify explicitly for Gemma 3 27B. **Do not** substitute `google/gemma-4-31b-it` (`model_a`).

**Current repository evidence:** `configs/models_q1_eval_panel.yaml`.

**Dependency:** D13 (supplementary), D15.

**Blocking:** P0 — BLOCKING

---

## D12 — Judge Protocol / IDs

**Decision:** J1 primary judge + J2 agreement judge: config keys, provider, exact model ids, blindness/independence/disagreement/adjudication rules.

| Role | Config key | Repo status | Provider | Model ID | Owner Decision |
|------|------------|-------------|----------|----------|----------------|
| J1 (DeepSeek V4 Flash) | `q1_judge_deepseek_v4_flash` | UNVERIFIED | — | — | ______ |
| J2 (Grok 4.7) | `q1_judge_grok_4_7` | UNVERIFIED | — | — | ______ |

**Allowed choices:** Owner must specify explicitly after independent ID verification. `model_c` in `models.yaml` is `deepseek/deepseek-chat-v3-0324` (different product name — not auto-J1).

**Current repository evidence:** `judges` in contract; `docs/archive/q1/JUDGE_PROTOCOL.md` (via stub).

**Dependency:** D13 (J2 subset), D14.

**Blocking:** P0 — BLOCKING

---

## D13 — Supplementary / Validation Subsets

**Decision:** Supplementary target execution subset (path + SHA); J2 validation subset (membership, manifest, SHA); rule: predefined before results.

**Allowed choices:** Owner must specify explicitly (full 61 vs frozen id-list manifest under `datasets/frozen/`).

**Current repository evidence:** `supplementary.subset` path/sha `NEEDS_DECISION`; no subset file in repo.

**Dependency:** D11 (supplementary models), D12.

**Blocking:** P0 — BLOCKING

**Owner Decision:** _______________________________________________

---

## D14 — Leakage / Contamination

**Decision:** Policies for dataset leakage, judge/defense label leakage, evaluator prompts, exclusions when contamination suspected.

**Allowed choices:** Owner must specify explicitly. Repo: non-oracle arms label-blind (`real_llm_pipeline.py`).

**Current repository evidence:** `scientific_design.leakage_contamination.label_blind_defense: SUPPORTED`.

**Dependency:** D11, D12.

**Blocking:** P0 — BLOCKING

**Owner Decision:** _______________________________________________

---

## D15 — Runtime / Stochasticity / Reproducibility

**Decision:** temperature, top_p, seed, max_tokens, timeout, retry count/policy, malformed output handling, provider snapshot; alignment with budget hard cap $3.

**Allowed choices:** Owner must specify explicitly. Repo partial: panel `temperature: 0.0` on verified rows; MT1 pattern `max_retries=0`, `cache.enabled: false`.

**Current repository evidence:** `configs/models_q1_eval_panel.yaml`; `budget.hard_cap_usd: 3.0` in contract.

**Dependency:** D11, D12.

**Blocking:** P0 — BLOCKING

**Owner Decision:** _______________________________________________

---

# P1 — Claim-dependent (do not block minimum freeze unless claim requires)

| ID | Topic | Required for claim? YES / NO | Owner Decision |
|----|-------|------------------------------|----------------|
| D06 | Utility / benign matrix & tier | ______ | ______ |
| D08 | B1 threshold τ & sensitivity grid | ______ | ______ |
| D16 | Order / randomization | ______ | ______ |
| D17 | Cost-aware reporting (calls/tokens/latency) | ______ | ______ |
| D19 | Failure analysis tables | ______ | ______ |

---

# P2 — Non-blocking (no action)

- **D07** Ablation plan — `DEFERRED` (separate experiment ID)
- **D18** `agent-injection-bench` — `DEFERRED` (future/secondary; not in repo)

---

## Signable summary (after fill)

| ID | Blocking | Owner Decision recorded? |
|----|----------|---------------------------|
| D01–D05, D09–D10, D13–D15 | P0 | Owner fills sections above |
| D11–D12 | P0 | Per-row in tables |
| D06,D08,D16,D17,D19 | P1 | Claim gate |
| D07,D18 | P2 | DEFERRED |

After all **P0** fields are filled, owner commits/signs this file → agent may propagate to `configs/q1_evaluation_contract.yaml` / panel **only** for stated values (separate step; not this task).
