# Q1 Owner Decision Pack — Decision-Ready Matrix

**HEAD:** `91c07b4` · **execution_gate:** `BLOCKED` · **p0_freeze_ready:** `false`  
**Owner Decision:** all P0 fields **EMPTY** · Proposal ≠ Owner Decision · Agent must not lock decisions.

## Freeze readiness (gate)

| Gate | Value | Reason |
|---|---|---|
| `p0_freeze_ready` | `false` | P0 Owner Decisions empty |
| `execution_gate` | `BLOCKED` | Intake incomplete |
| Proposal-only approval | — | Does not open gate |

## Canonical topics (no duplicate decisions)

| Topic | Canonical | Notes |
|---|---|---|
| α, Holm family | **D03** | D09 references only |
| Retry | **D15** | D09 references only |
| Order / randomization | **D15** | D16 references only |
| Causal B2 pair | **D03 + D05** | W1: `B2-ADAPTIVE-A0` vs `B2-ADAPTIVE-B1` |
| `attack_episodes`, `hard_cap_usd` | Owner + contract | Derived formula only; not locked |

## W1–W8 readiness (scientific — not owner-locked)

| ID | Check | Result | Evidence |
|---|---|---|---|
| W1 | Causal B2 A0 vs B1 in repo | **PASS** | `b2_matrix_contract`: `B2-ADAPTIVE-A0` / `B2-ADAPTIVE-B1`, `build_pre_target_defense`, `AdaptiveAttacker`, `max_turns=3`; `B0 vs B2` = contextual only in proposals |
| W2 | Episode unit; no pooled McNemar without estimand | **PASS** (proposal) | Unit = episode per attack×target×arm; 6-test Holm example = 2 comparisons × 3 targets — **OWNER** must lock family |
| W3 | H1 vs test sidedness | **UNRESOLVED** | `mcnemar_test` two-sided; directional H1 in proposal — **OWNER** picks Option A or B (below) |
| W4 | J2 subset + κ | **P0 BLOCKER** (conditional) | Contract `kappa_subset: NEEDS_DECISION`; no J2 manifest; archive κ≥0.6 **not** in Q1 contract — if owner adopts κ GO, subset cannot be `none` |
| W5 | Blocked vs judge-fail | **PASS** (semantics) | B2 all-blocked → scorable fail (`b2_adaptive_contract`); `episode_judge_failed` excludes judge fails — sensitivity rule **OWNER** |
| W6 | B0 repeat in Q1 contract | **PASS** (absent) | No replicate arm registered — optional trade-off only |
| W7 | B1 result neutrality | **PASS** | No pre-coded null/significance in contract |
| W8 | Episode vs API calls | **PASS** (derived) | See workload table; **BUDGET FEASIBILITY = UNRESOLVED** |

### W3 options (OWNER must choose one — not agent)

| Option | H1 | Test |
|---|---|---|
| **A** | Defense reduces ASR (directional) | One-sided McNemar (**not implemented** in `statistics.py` today) |
| **B** | Defense changes ASR | Two-sided McNemar (current code) |

### Workload (derived; **Candidate** `T=6` primary — not owner-locked)

| Quantity | Formula | Candidate (T=6) |
|---|---|---|
| Attacks | `n_attack` | 61 |
| Primary **episodes** | `61 × T × 3 arms` | **1098** |
| Per-arm episodes | `61 × T` | 366 |
| B0/B1 **target+judge** calls/ep (worst) | 2 | 732 calls/arm → **1464** total |
| B2 **target+judge** calls/ep (worst) | `max_turns+1` (=4) | **1464** total |
| **Worst-case API calls** (primary matrix) | `2×(B0+B1)+4×B2` per target slice | **2928** |
| Historical reference `qwen-2.5-7b` | Not in episode formula unless Owner adds | **0** (default) |
| J2 validation calls | D13 subset only | **UNRESOLVED** |

**Budget:** phase rule ≤ **$2** (MT1 reference). `hard_cap_usd` / `attack_episodes`: **EMPTY**. OpenRouter list prices (metadata, 2026-09-25): verified IDs below. **BUDGET FEASIBILITY = BLOCKED** for full 6×61×3 matrix at worst-case calls with closed models (GPT-5.4 / Claude 4.6 pricing >> open models); feasible only with Owner-chosen caps/subset — not agent-selected.

---

## Q1 Candidate Panel (NOT Owner-Locked)

Source: owner candidate list + `configs/models_q1_eval_panel.yaml` → `candidate_panel_reconciliation`. **Contract `primary_targets` still legacy 4-key panel until Owner propagation.**

| Model | Exact ID | Role | Family | Evidence | Pricing (OR metadata) | Cost control | Owner Decision | Status |
|---|---|---|---|---|---|---|---|---|
| Qwen3 30B A3B | `qwen/qwen3-30b-a3b` | primary candidate | qwen | panel + MT2 snapshot + OR API | p `1.2e-7` / c `5e-7` per token | BudgetLedger / caps | **EMPTY** | VERIFIED |
| Gemma 4 31B IT | `google/gemma-4-31b-it` | primary candidate | google | `models.yaml` model_a, MT1/MT2 — **not Gemma 3 27B** | p `9e-8` / c `3.4e-7` | same matrix | **EMPTY** | VERIFIED |
| Llama 3.3 70B | `meta-llama/llama-3.3-70b-instruct` | primary candidate | meta | panel + snapshot + OR | p `1e-7` / c `3.2e-7` | same matrix | **EMPTY** | VERIFIED |
| DeepSeek V3.2 | `deepseek/deepseek-v3.2` | primary candidate (replaces Mistral in candidate list) | deepseek | OR API (not in MT2 snapshot) | p `2.69e-7` / c `4e-7` | same matrix | **EMPTY** | VERIFIED |
| GPT-5.4 | `openai/gpt-5.4` | primary candidate (closed) | openai | OR API | p `2.5e-6` / c `1.5e-5` | call/token/budget gate only | **EMPTY** | VERIFIED |
| Claude Sonnet 4.6 | `anthropic/claude-sonnet-4.6` | primary candidate (closed) | anthropic | OR API | p `3e-6` / c `1.5e-5` | call/token/budget gate only | **EMPTY** | VERIFIED |
| Qwen 2.5 7B Instruct | `qwen/qwen-2.5-7b-instruct` | **historical / AUDIT reference** | qwen | `models.yaml` target_2, MT1 r1 | p `1e-7` / c `2e-7` | not in primary matrix unless Owner adds | **EMPTY** | VERIFIED |
| J1 | `deepseek/deepseek-v4-flash` | judge candidate | deepseek | OR API | p `4.87e-8` / c `9.74e-8` | J2 subset + ledger | **EMPTY** | VERIFIED · **independence note:** same vendor as DeepSeek target |
| J2 | `x-ai/grok-4.7` | judge candidate | xai | OR API | p `1.6e-6` / c `4.8e-6` | validation subset (D13) | **EMPTY** | VERIFIED |

**Removed from candidate primary (vs legacy contract panel):** `mistralai/mistral-small-3.2-24b-instruct` — legacy row remains in `models:` until Owner propagation.

**Scientific independence (D12):** J1 DeepSeek + primary `deepseek/deepseek-v3.2` → vendor overlap — **P0 scientific review required** (not auto-blocked). J2 on deterministic subset only if κ GO (W4).

**Closed-model integrity:** same attack protocol / endpoint / scoring; only `resource guard` (episode/call/turn caps, ledger) — no model-specific payload or temperature changes without preregistration (D15).

---

# Decision-Ready Matrix — P0 (D01–D15)

### D01 — Research Questions / Hypotheses

| Field | Content |
|---|---|
| **Evidence** | README prompt-injection testbed; contract arms B0/B1/B2; 61 attacks; no Q1 RQ text |
| **Supported Choices** | Owner-written RQ/H testable via judge ASR + D03 comparisons |
| **Scientific Implication** | Bounds D03, D10, W1 causal vs contextual claims |
| **Owner Decision** | **EMPTY** (RQ1, H0, H1) |
| **Status** | `NEEDS_OWNER_DECISION` |

### D02 — Endpoint / Estimand / Unit

| Field | Content |
|---|---|
| **Evidence** | `attack_success_rate`; B2 `final_turn_only`; `delta_hat_from_mcnemar_contingency` |
| **Supported Choices** | Episode-level judge ASR; pair on attack_id×target |
| **Scientific Implication** | Defines McNemar rows (W2) |
| **Owner Decision** | **EMPTY** |
| **Status** | `NEEDS_OWNER_DECISION` |

### D03 — Comparisons / α / Holm *(canonical)*

| Field | Content |
|---|---|
| **Evidence** | `mcnemar_exact`, `holm_correction`; matrix conditions A0/B1 |
| **Supported Choices** | Per-target pairs; proposal: B0–B1, **B2-ADAPTIVE-A0 vs B2-ADAPTIVE-B1** (causal), B0–B2 contextual; Holm on declared family (e.g. 6 tests) |
| **Scientific Implication** | W1/W2; no pooled targets without estimand |
| **Owner Decision** | **EMPTY** |
| **Status** | `NEEDS_OWNER_DECISION` · W3 **UNRESOLVED** until sidedness chosen |

### D04 — B1 static arm

| Field | Content |
|---|---|
| **Evidence** | `B1`, `STATIC-A3`, `STATIC-A1` in `defense_baselines.py` |
| **Supported Choices** | One resolver key only |
| **Scientific Implication** | Ties to B2-ADAPTIVE-B1 defense mode if rule-based B1 |
| **Owner Decision** | **EMPTY** |
| **Status** | `NEEDS_OWNER_DECISION` |

### D05 — B2 condition / attacker

| Field | Content |
|---|---|
| **Evidence** | `B2-ADAPTIVE-A0`, `B2-ADAPTIVE-B1`; `AdaptiveAttacker`; `AdaptiveEpisodeRunner` via `live_extension_wiring` |
| **Supported Choices** | Matrix cells; same attacker/protocol/turns; defense A0 vs B1 |
| **Scientific Implication** | W1 causal comparator implementation **supported** (no new runner required) |
| **Owner Decision** | **EMPTY** |
| **Status** | `NEEDS_OWNER_DECISION` |

### D06 — Utility / benign (P1)

| Field | Content |
|---|---|
| **Evidence** | 61 benign; `benign_episodes: NEEDS_DECISION` |
| **Supported Choices** | Defer vs symmetric matrix |
| **Scientific Implication** | Not required for security-only P0 |
| **Owner Decision** | **EMPTY** |
| **Status** | `CLAIM-GATED` |

### D07 — Ablations (P2)

| Field | Content |
|---|---|
| **Evidence** | No Q1 ablation arms in contract |
| **Supported Choices** | None in confirmatory matrix or separate experiment ID |
| **Scientific Implication** | Out of minimum P0 scope unless owner expands |
| **Owner Decision** | **EMPTY** |
| **Status** | `NEEDS_OWNER_DECISION` |

### D08 — B1 threshold (P1)

| Field | Content |
|---|---|
| **Evidence** | `B1_RULE_THRESHOLD=0.25` in matrix contract only |
| **Supported Choices** | Single τ vs grid if D04=B1 |
| **Scientific Implication** | Claim-dependent |
| **Owner Decision** | **EMPTY** |
| **Status** | `CLAIM-GATED` |

### D09 — SAP

| Field | Content |
|---|---|
| **Evidence** | `mcnemar_test`, bootstrap CI, `episode_judge_failed` |
| **Supported Choices** | W5 blocked=scorable fail; judge-fail exclude + owner sensitivity; α/Holm → **D03**; retry → **D15** |
| **Scientific Implication** | Must align W3 sidedness |
| **Owner Decision** | **EMPTY** |
| **Status** | `NEEDS_OWNER_DECISION` |

### D10 — Claims

| Field | Content |
|---|---|
| **Evidence** | Frozen pack; no SOTA in README |
| **Supported Choices** | Causal B2 A0–B1; B0–B1 static; W7 null-neutral wording |
| **Scientific Implication** | No B0–B2 causal defense claim |
| **Owner Decision** | **EMPTY** |
| **Status** | `NEEDS_OWNER_DECISION` |

### D11 — Target panel

| Field | Content |
|---|---|
| **Evidence** | Candidate table above; legacy contract keys (4) incl. Mistral + Gemma 3 27B placeholder |
| **Supported Choices** | Six **verified** primary candidates + `qwen-2.5-7b` reference only; `google/gemma-4-31b-it` per MT1/MT2 (not Gemma 3 27B) |
| **Scientific Implication** | `T=6` → 1098 episodes derived; budget **BLOCKED** at $2/phase unless Owner caps |
| **Owner Decision** | **EMPTY** |
| **Status** | `NEEDS_OWNER_DECISION` · candidate IDs **VERIFIED** (OR metadata) |

### D12 — Judges

| Field | Content |
|---|---|
| **Evidence** | Candidate J1/J2 verified on OpenRouter; MT2 judges remain **separate protocol** |
| **Supported Choices (Q1)** | `deepseek/deepseek-v4-flash`, `x-ai/grok-4.7` (candidate — not locked) |
| **Scientific Implication** | W4 κ + subset; DeepSeek J1 vs DeepSeek target vendor overlap |
| **Owner Decision** | **EMPTY** |
| **Status** | `NEEDS_OWNER_DECISION` · κ/subset **UNRESOLVED** |

### D13 — Subsets

| Field | Content |
|---|---|
| **Evidence** | No Q1 subset manifest in repo |
| **Supported Choices** | `none` or frozen path+SHA |
| **Scientific Implication** | J2 scope; ≥20% units if κ validation required |
| **Owner Decision** | **EMPTY** |
| **Status** | `NEEDS_OWNER_DECISION` · **P0 BLOCKER** if κ GO without manifest |

### D14 — Leakage / contamination

| Field | Content |
|---|---|
| **Evidence** | Label-blind non-oracle pipeline; archive judge blindness |
| **Supported Choices** | Documented controls only |
| **Scientific Implication** | Ties to D12 judge input |
| **Owner Decision** | **EMPTY** |
| **Status** | `NEEDS_OWNER_DECISION` |

### D15 — Runtime *(canonical retry/order)*

| Field | Content |
|---|---|
| **Evidence** | Panel temp 0.0, max_tokens 512; live max_retries=0; B2 max_turns=3 |
| **Supported Choices** | Owner sets timeout/top_p/seed/order |
| **Scientific Implication** | D09 retry reference |
| **Owner Decision** | **EMPTY** |
| **Status** | `NEEDS_OWNER_DECISION` |

---

# Critical contradiction scan

| # | Check | Status |
|---|---|---|
| 1 | Directional H1 + two-sided test | **BLOCKED** until W3 Option A/B (UNRESOLVED) |
| 2 | κ GO + no J2 subset | **BLOCKED** if κ adopted (W4) |
| 3 | Causal B2 + B0/B2-only primary | **PASS** (proposal separates causal vs contextual) |
| 4 | Pooled targets + no estimand | **PASS** (proposal forbids) |
| 5 | Judge failure silent exclusion | **UNRESOLVED** (sensitivity OWNER) |
| 6 | Blocked = unscorable | **PASS** (W5 evidence) |
| 7 | Budget cap + unresolved workload | **UNRESOLVED** (`BUDGET FEASIBILITY`) |
| 8 | Gemma slot + no exact ID | **BLOCKED** |
| 9 | J1/J2 + unverified IDs | **BLOCKED** |
| 10 | Owner EMPTY + freeze true | **PASS** (`p0_freeze_ready=false`) |

---

# Reproducibility chain (repository SHA — read-only)

| Link | SHA / status |
|---|---|
| Contract | `c48697979654265cc25304b8afd102c2aa2f88e76b3a14bcf3281b5b67e29cc1` |
| Dataset | `523c881820710783b5290c76ea5fe5fc01a6341fb427defcba1119fc3e721518` |
| `models.yaml` (VNEXT binding) | `37174858710a087b3fe58c40e65c796418d1791ff4280bca08d96486b35d7ec3` |
| Panel | `50e2e2e5c56358db02d19e1691b9994426b9334539e7f98a05ff32803ec7badf` |
| Subset | `NEEDS_DECISION` |
| Code commit | owner records at run time |
| Raw → stats → manuscript | not produced (no live run) |

---

# P1 / P2

| ID | Status |
|---|---|
| D06, D08, D16, D17, D19 | `CLAIM-GATED` / OWNER DECISION REQUIRED |
| D07, D18 | `NEEDS_OWNER_DECISION` |

---

**Next step:** Owner fills matrix → validate → propagate to contract/panel only. No freeze while **EMPTY** or **P0 BLOCKER** rows remain.
