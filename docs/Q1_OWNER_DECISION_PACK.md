# Q1 Owner Decision Pack (protocol closure)

**HEAD at pack creation:** `dfa1ec7` · **Intake @ HEAD:** `a10fb0e` (no owner sign-off received) · **Execution:** forbidden until all D01–D19 `OWNER_DECIDED`  
**Integrity:** `models.yaml` `37174858…` · dataset `523c8818…` · panel `50e2e2e5…`

## Owner decision intake (explicit status — not locks)

| ID | Status |
|----|--------|
| D01–D10 | NEEDS_OWNER_DECISION |
| D11 J1/J2 IDs | UNVERIFIED |
| D12 model IDs (Gemma 3 27B, GPT-5.4, Claude Sonnet 5) | UNVERIFIED |
| D13–D19 | NEEDS_OWNER_DECISION |

Partial repo evidence only (not owner decisions): 3/4 primary OpenRouter ids in `models_q1_eval_panel.yaml` (qwen, mistral, llama).

## Dependency graph

```text
RQ/H (D01)
 ↓ Primary Endpoint + Unit (D02)
 ↓ Primary Comparisons + Holm family (D03)
 ↓ B1 static mapping (D04) + B2 condition + attacker mode (D05)
 ↓ Benign / utility (D06) + threshold sensitivity (D08)
 ↓ Ablations optional (D07)
 ↓ SAP (D09) + claims scope (D10)
 ↓ Judges (D11) + model IDs (D12) + subsets SHA (D13)
 ↓ Leakage (D14) + stochasticity (D15) + order (D16) + cost/latency (D17)
 ↓ External validation role (D18) + failure analysis (D19)
 ↓ Runner mapping → preflight → live authorization → execution
```

---

## Decision matrix

### D01 — Research Questions / Hypotheses

| Field | Content |
|-------|---------|
| DECISION_ID | D01 |
| QUESTION | What are Q1-specific RQ/H (distinct from VNEXT Track A `VNEXT_PROTOCOL.md`)? |
| CURRENT_REPO_STATE | `scientific_design.research_questions: NEEDS_DECISION`; VNEXT RQ is B0 vs adaptive on same pack, not B0/B1/B2 matrix. |
| EVIDENCE | `configs/q1_evaluation_contract.yaml`; `docs/experiments/protocols/VNEXT_PROTOCOL.md` §2 |
| OPTIONS | (A) Three pairwise security RQs: B1 vs B0, B2 vs B0, B2 vs B1 on 61 attacks × 4 targets. (B) Single primary RQ (e.g. B2 vs B0 only) + secondary RQs. (C) Defer Q1 RQs; keep VNEXT-only claims. |
| SCIENTIFIC_IMPACT | Defines estimands and claim boundaries. |
| REPRODUCIBILITY_IMPACT | Without locked RQ/H, post-hoc reframing risk. |
| COST_IMPACT | More primary RQs → more multiplicity / reporting burden; not necessarily more API if same matrix. |
| DEPENDENCIES | None (root). |
| RISK_IF_WRONG | Mixed VNEXT vs Q1 narratives in manuscript. |
| OWNER_DECISION_REQUIRED | Yes |
| RECOMMENDED_DEFAULT | None locked — evaluate candidate structure in OPTIONS only. |
| STATUS | OPEN |

**Candidate RQ skeleton (not adopted):** For each chosen primary comparison in D03, specify endpoint=ASR, unit=episode (D02), H0: paired attack success equal, H1: direction pre-specified.

---

### D02 — Primary Endpoint / Estimand / Unit

| Field | Content |
|-------|---------|
| DECISION_ID | D02 |
| QUESTION | Lock ASR definition, denominator, blocked/missing handling, and unit for B0/B1/B2. |
| CURRENT_REPO_STATE | `endpoints.primary_security: attack_success_rate`; B2 `EPISODE_SUCCESS_RULE` in `b2_adaptive_contract.py`; pipeline `compute_real_metrics`. |
| EVIDENCE | `q1_evaluation_contract.yaml` endpoints; `b2_adaptive_contract.py` L81-83; `VNEXT_PROTOCOL.md` §3 |
| OPTIONS | (A) Episode-level paired McNemar on `attack_succeeded` for gold attacks; blocked → not success (VNEXT-style). (B) Exclude blocked from denominator (different estimand). (C) Turn-level primary (not repo default for B2). |
| SCIENTIFIC_IMPACT | Changes interpretability of ASR and blocks. |
| REPRODUCIBILITY_IMPACT | Must match runner + judge fields in raw jsonl. |
| COST_IMPACT | Neutral if same calls. |
| DEPENDENCIES | D01 |
| RISK_IF_WRONG | Incomparable to VNEXT / DIAG ASR. |
| OWNER_DECISION_REQUIRED | Yes (utility gate tier overlaps D06) |
| RECOMMENDED_DEFAULT | Episode-level attack paired outcomes aligns with existing `mcnemar_test` + B2 final-turn rule (evidence-backed, not owner lock). |
| STATUS | OPEN |

---

### D03 — Primary Comparison Family

| Field | Content |
|-------|---------|
| DECISION_ID | D03 |
| QUESTION | Which arm pairs are **primary** and Holm family definition? |
| CURRENT_REPO_STATE | `primary_comparisons: NEEDS_DECISION`; `statistics.multiple_comparison: NEEDS_DECISION`. |
| EVIDENCE | `statistics.holm_correction`; MT1 audit: Holm not run on r1. |
| OPTIONS | (A) Co-primary: B0 vs B1, B0 vs B2 (2 tests, Holm). (B) Single primary B0 vs B2; B1 descriptive. (C) All three pairs with Holm over 3. |
| SCIENTIFIC_IMPACT | Controls multiplicity. |
| REPRODUCIBILITY_IMPACT | Family must be fixed before first live call. |
| COST_IMPACT | Same matrix; reporting only. |
| DEPENDENCIES | D01, D02 |
| RISK_IF_WRONG | Comparison explosion / cherry-picking. |
| OWNER_DECISION_REQUIRED | Yes |
| RECOMMENDED_DEFAULT | None — family size is a scientific choice. |
| STATUS | OPEN |

---

### D04 — B1 Static Defense

| Field | Content |
|-------|---------|
| DECISION_ID | D04 |
| QUESTION | Map Q1 arm **B1** to which resolver key? |
| CURRENT_REPO_STATE | `arms.B1: NEEDS_DECISION`. Factories: `B1`→`make_b1_rule_based(threshold)` detector block if prob≥τ; `STATIC-A3` unconditional block all; `STATIC-A1` unconditional sanitize (`defense_baselines.py`). |
| EVIDENCE | DIAG B0/B1 used `B1` rule-based on layer_a_v2; MT1 STATIC-A3 FPR=1 by design. |
| OPTIONS | `B1` (detector threshold 0.25 default in `b2_matrix_contract.B1_RULE_THRESHOLD`) \| `STATIC-A3` \| `STATIC-A1` |
| SCIENTIFIC_IMPACT | B1≈selective block; A3≈oracle ceiling; A1≈sanitize not block. |
| REPRODUCIBILITY_IMPACT | Historical DIAG B1 comparable only if `B1` chosen. |
| COST_IMPACT | Similar per episode. |
| DEPENDENCIES | D03 |
| RISK_IF_WRONG | “Static defense” claim mislabeled. |
| OWNER_DECISION_REQUIRED | Yes |
| RECOMMENDED_DEFAULT | None — semantics differ materially. |
| STATUS | OPEN |

---

### D05 — B2 Adaptive Contract

| Field | Content |
|-------|---------|
| DECISION_ID | D05 |
| QUESTION | Q1 `B2` condition_id + defense mode (A0/B1) + attacker mode (fixed vs adaptive)? |
| CURRENT_REPO_STATE | `arms.B2: NEEDS_DECISION`; `max_turns: 3` = `LIVE_WIRING_MAX_TURNS`. IDs: `B2-ADAPTIVE-A0|B1`, `B2-FIXED-A0|B1`, `B2-FIXED`, `B2-ADAPTIVE`, `LIVE-PRO-PI-B2-ADAPTIVE` (`b2_adaptive_contract.py`, `b2_matrix_contract.py`). |
| EVIDENCE | `b2_attack_mode_contract`: adaptive = `AdaptiveAttacker`; fixed = `FixedSequenceAttacker`. Matrix 2×2 separates attack×defense. |
| OPTIONS | (A) Single arm: `B2-ADAPTIVE-B1` + adaptive attacker. (B) `B2-FIXED-B1` + fixed sequence (defense multi-turn only). (C) Full 2×2 (cost ↑, not 732-only). |
| SCIENTIFIC_IMPACT | Confounds defense vs attacker adaptation if wrong ID. |
| REPRODUCIBILITY_IMPACT | Must match `live_extension_wiring` / batch runner condition. |
| COST_IMPACT | Multi-turn × turns × judge; 2×2 multiplies episodes. |
| DEPENDENCIES | D03, D04 |
| RISK_IF_WRONG | “Adaptive defense” claim with adaptive attacker only or vice versa. |
| OWNER_DECISION_REQUIRED | Yes |
| RECOMMENDED_DEFAULT | If Q1 label is “adaptive multi-turn **defense**”, repo evidence requires picking defense stack (`make_b3_adaptive` is single-turn B3, **not** B2 wiring) — B2 path is `b2_*` contracts, not B3. |
| STATUS | OPEN |

---

### D06 — Benign / Utility Protocol

| Field | Content |
|-------|---------|
| DECISION_ID | D06 |
| QUESTION | Benign matrix N and utility tier (primary vs gate)? |
| CURRENT_REPO_STATE | 61 benign in pack; `benign_episodes: NEEDS_DECISION`; attack budget 732 only. |
| EVIDENCE | Full benign matrix = 732 episodes + judge calls; $3 cap likely infeasible without preflight proof. |
| OPTIONS | (A) 61×4×3=732 benign symmetric. (B) Benign on subset with frozen SHA. (C) Primary security only; utility secondary on fixed benign slice. |
| SCIENTIFIC_IMPACT | Utility/FPR claims require benign N plan. |
| REPRODUCIBILITY_IMPACT | Must pre-register N formula. |
| COST_IMPACT | High for (A). |
| DEPENDENCIES | D02 |
| RISK_IF_WRONG | Over budget or unreported FPR. |
| OWNER_DECISION_REQUIRED | Yes |
| RECOMMENDED_DEFAULT | None — cost constraint is binding ($3). |
| STATUS | OPEN |

---

### D07 — Ablation Plan

| Field | Content |
|-------|---------|
| DECISION_ID | D07 |
| QUESTION | Which 2–3 ablations support core AdaptiGuard claims? |
| CURRENT_REPO_STATE | `ablations: MISSING`; no Q1 ablation arms. |
| EVIDENCE | Architecture: `PolicyUpdateEngine`, `RiskEngine`, `AdaptiveDefenseState` (`defense_baselines.py`); not wired to Q1 contract. |
| OPTIONS | (1) Fixed defense level vs adaptive escalation. (2) Risk/policy off vs on. (3) Intervention off (A0) vs on. Each adds arms/N/cost. |
| SCIENTIFIC_IMPACT | Needed for mechanism claims beyond B0/B1/B2. |
| REPRODUCIBILITY_IMPACT | Separate experiment ID if added. |
| COST_IMPACT | +arms × episodes. |
| DEPENDENCIES | D05 |
| RISK_IF_WRONG | Overclaiming adaptive mechanism. |
| OWNER_DECISION_REQUIRED | Yes (include/exclude ablations from Q1 confirmatory) |
| RECOMMENDED_DEFAULT | Defer ablations to Phase-2 experiment ID unless owner expands budget/matrix. |
| STATUS | OPEN |

---

### D08 — Threshold Sensitivity

| Field | Content |
|-------|---------|
| DECISION_ID | D08 |
| QUESTION | Primary B1 threshold and pre-registered sensitivity grid? |
| CURRENT_REPO_STATE | `threshold_sensitivity: MISSING`; code default τ=0.25 (`b2_matrix_contract`, `make_b1_rule_based`). |
| EVIDENCE | Only if D04=`B1`. |
| OPTIONS | (A) Lock τ=0.25 only. (B) Pre-register grid e.g. {0.15,0.25,0.35} secondary/descriptive. |
| SCIENTIFIC_IMPACT | Post-hoc τ invalidates confirmatory B1. |
| REPRODUCIBILITY_IMPACT | Grid must be in contract before live. |
| COST_IMPACT | Grid multiplies B1 runs. |
| DEPENDENCIES | D04 |
| RISK_IF_WRONG | Tuned threshold. |
| OWNER_DECISION_REQUIRED | Yes if B1=rule-based |
| RECOMMENDED_DEFAULT | If B1=rule-based, lock τ=0.25 as primary **only if** owner accepts DIAG alignment (not automatic). |
| STATUS | OPEN |

---

### D09 — Statistical Analysis Plan

| Field | Content |
|-------|---------|
| DECISION_ID | D09 |
| QUESTION | Lock α, Holm, δ̂, CI, exclusions? |
| CURRENT_REPO_STATE | `mcnemar: SUPPORTED`; α/CI/Holm `NEEDS_DECISION`. Helpers: `mcnemar_test`, `holm_correction`, `delta_hat_from_mcnemar_contingency`, Wilson/bootstrap in `statistics.py`. VNEXT: α=0.05, MSID δ=0.20 (VNEXT treatment, not automatically Q1). |
| EVIDENCE | `VNEXT_PROTOCOL.md` §9-10; `q1_evaluation_contract.yaml` statistics |
| OPTIONS | Align with VNEXT α=0.05 vs Q1-only α; MSID apply or not; CI Wilson vs bootstrap; judge-fail exclusion per VNEXT §12 pattern. |
| SCIENTIFIC_IMPACT | Confirmatory vs diagnostic labeling. |
| REPRODUCIBILITY_IMPACT | SAP must be frozen in contract. |
| COST_IMPACT | Neutral. |
| DEPENDENCIES | D02, D03 |
| RISK_IF_WRONG | p-hacking / mixed VNEXT MSID with B1/B2. |
| OWNER_DECISION_REQUIRED | Yes |
| RECOMMENDED_DEFAULT | McNemar exact for paired attacks (already contract); α=0.05 matches VNEXT **if** owner declares Q1 confirmatory tier same as VNEXT (not auto). |
| STATUS | OPEN |

---

### D10 — Claims / Generalization

| Field | Content |
|-------|---------|
| DECISION_ID | D10 |
| QUESTION | Allowed claim scope? |
| CURRENT_REPO_STATE | `claims_generalization: NEEDS_DECISION` |
| EVIDENCE | 61 attacks, 6 families in dataset card; 4 open-weight targets + 2 supplementary; hosted nondeterminism. |
| OPTIONS | Internal pack-only vs multi-target hosted; supplementary non-pooled; no SOTA/general agent claims. |
| SCIENTIFIC_IMPACT | Publication boundary. |
| REPRODUCIBILITY_IMPACT | Tied to D12/D13. |
| COST_IMPACT | Neutral. |
| DEPENDENCIES | D06, D12, D18 |
| RISK_IF_WRONG | Overgeneralization. |
| OWNER_DECISION_REQUIRED | Yes |
| RECOMMENDED_DEFAULT | Benchmark-specific + model-list explicit (minimal safe wording pattern). |
| STATUS | OPEN |

---

### D11 — Judges (J1/J2)

| Field | Content |
|-------|---------|
| DECISION_ID | D11 |
| QUESTION | Lock J1 DeepSeek V4 Flash + J2 Grok 4.7 OpenRouter IDs and protocol? |
| CURRENT_REPO_STATE | Panel `NEEDS_DECISION`; `model_c` is `deepseek/deepseek-chat-v3-0324` (different name). No Grok in repo. |
| EVIDENCE | `models_q1_eval_panel.yaml`; `docs/archive/q1/JUDGE_PROTOCOL.md` |
| OPTIONS | Owner verifies IDs offline; define blindness, disagreement, κ on J2 subset. |
| SCIENTIFIC_IMPACT | Judge drives ASR. |
| REPRODUCIBILITY_IMPACT | IDs + snapshot required. |
| COST_IMPACT | J2 doubles judge calls on subset. |
| DEPENDENCIES | D13 |
| RISK_IF_WRONG | UNVERIFIED judge invalidates run. |
| OWNER_DECISION_REQUIRED | Yes |
| RECOMMENDED_DEFAULT | None for IDs. |
| STATUS | OPEN — **UNVERIFIED** IDs |

---

### D12 — Supplementary / Primary Model IDs

| Field | Content |
|-------|---------|
| DECISION_ID | D12 |
| QUESTION | Lock Gemma 3 27B, GPT-5.4, Claude Sonnet 5 OR IDs? |
| CURRENT_REPO_STATE | 3 primary slots verified in panel: qwen, mistral, llama; gemma slot UNVERIFIED; supplementary UNVERIFIED. |
| EVIDENCE | `models_q1_eval_panel.yaml`; `models.yaml` model_a is gemma-4-31b-it (**not** Gemma 3 27B). |
| OPTIONS | Owner supplies verified OR ids; do not substitute gemma-4-31b-it. |
| SCIENTIFIC_IMPACT | Wrong model voids target panel. |
| REPRODUCIBILITY_IMPACT | Registry SHA lock after edit. |
| COST_IMPACT | Supplementary optional under budget. |
| DEPENDENCIES | D13 |
| RISK_IF_WRONG | UNVERIFIED execution. |
| OWNER_DECISION_REQUIRED | Yes |
| RECOMMENDED_DEFAULT | None. |
| STATUS | OPEN — **UNVERIFIED** (4th primary + 2 supplementary) |

---

### D13 — Supplementary / J2 Subsets

| Field | Content |
|-------|---------|
| DECISION_ID | D13 |
| QUESTION | Frozen subset manifest + SHA for supplementary and J2? |
| CURRENT_REPO_STATE | `subset.path/sha256: NEEDS_DECISION`; J2 `frozen_subset_only`. |
| EVIDENCE | Full pack SHA locked; no Q1 subset file in `datasets/frozen/`. |
| OPTIONS | Full 61 vs stratified vs fixed id list JSON + sha256. |
| SCIENTIFIC_IMPACT | Prevents post-hoc selection. |
| REPRODUCIBILITY_IMPACT | `subset_sha256` in repro chain. |
| COST_IMPACT | Smaller subset reduces cost. |
| DEPENDENCIES | D06, D11 |
| RISK_IF_WRONG | Invalid confirmatory subset. |
| OWNER_DECISION_REQUIRED | Yes |
| RECOMMENDED_DEFAULT | None. |
| STATUS | OPEN |

---

### D14 — Leakage / Contamination

| Field | Content |
|-------|---------|
| DECISION_ID | D14 |
| QUESTION | Q1 leakage policy beyond label-blind defense? |
| CURRENT_REPO_STATE | `label_blind_defense: SUPPORTED`; judge leakage `NEEDS_DECISION`. |
| EVIDENCE | `real_llm_pipeline.py` non-oracle path; VNEXT leakage rules in protocol. |
| OPTIONS | Adopt VNEXT judge-blind fields; document no gold label in judge prompt; no train on pack. |
| SCIENTIFIC_IMPACT | Invalid inference if judge sees arm labels. |
| REPRODUCIBILITY_IMPACT | Manifest in run_context. |
| COST_IMPACT | Neutral. |
| DEPENDENCIES | D11 |
| RISK_IF_WRONG | Contaminated ASR. |
| OWNER_DECISION_REQUIRED | Yes |
| RECOMMENDED_DEFAULT | Reuse VNEXT judge-blind wording by reference (owner sign-off). |
| STATUS | OPEN |

---

### D15 — Stochasticity / Runtime

| Field | Content |
|-------|---------|
| DECISION_ID | D15 |
| QUESTION | Lock temp/top_p/seed/retry/timeout per target? |
| CURRENT_REPO_STATE | Panel temp 0.0 where set; `top_p_seed_retry_timeout: NEEDS_DECISION`. |
| EVIDENCE | `models_q1_eval_panel.yaml`; MT1 `max_retries=0` pattern in runners. |
| OPTIONS | temp=0, max_retries=0, cache=false (VNEXT/MT1 pattern) + document nondeterminism disclaimer. |
| SCIENTIFIC_IMPACT | Repeatability. |
| REPRODUCIBILITY_IMPACT | Execution manifest. |
| COST_IMPACT | Retries increase spend. |
| DEPENDENCIES | D12 |
| RISK_IF_WRONG | Hidden retries post-hoc. |
| OWNER_DECISION_REQUIRED | Yes |
| RECOMMENDED_DEFAULT | temp=0 + max_retries=0 aligns with existing diagnostic runs (not auto-lock). |
| STATUS | OPEN |

---

### D16 — Order / Randomization

| Field | Content |
|-------|---------|
| DECISION_ID | D16 |
| QUESTION | Episode/target/arm ordering? |
| CURRENT_REPO_STATE | `order_randomization: NEEDS_DECISION`; vnext pack file order seed 61. |
| EVIDENCE | DIAG order B0 then B1; MT1 seed 42 episode ids. |
| OPTIONS | Fixed nested loop (target×arm×episode) vs randomized with locked seed. |
| SCIENTIFIC_IMPACT | Ordering bias for adaptive state. |
| REPRODUCIBILITY_IMPACT | Must log order in manifest. |
| COST_IMPACT | Neutral. |
| DEPENDENCIES | D05 |
| RISK_IF_WRONG | B2 state carryover ambiguity. |
| OWNER_DECISION_REQUIRED | Yes |
| RECOMMENDED_DEFAULT | None. |
| STATUS | OPEN |

---

### D17 — Cost / Latency Reporting

| Field | Content |
|-------|---------|
| DECISION_ID | D17 |
| QUESTION | Which cost/latency metrics are co-primary for Cost-Aware claim? |
| CURRENT_REPO_STATE | `budget_cap SUPPORTED`; reporting `NEEDS_DECISION`. |
| EVIDENCE | `BudgetLedger`, prediction row latency/token fields in pipeline. |
| OPTIONS | Minimal: spent_usd, requests_used, per-episode latency_ms; optional token sums from API metadata. |
| SCIENTIFIC_IMPACT | Cost-aware contribution needs reported tradeoff. |
| REPRODUCIBILITY_IMPACT | Ledger in SUMMARY.json pattern (MT1). |
| COST_IMPACT | Neutral. |
| DEPENDENCIES | D06 |
| RISK_IF_WRONG | Cap-only without tradeoff evidence. |
| OWNER_DECISION_REQUIRED | Yes |
| RECOMMENDED_DEFAULT | Ledger fields already implemented (reporting choice only). |
| STATUS | OPEN |

---

### D18 — External Validation

| Field | Content |
|-------|---------|
| DECISION_ID | D18 |
| QUESTION | Role of agent-injection-bench? |
| CURRENT_REPO_STATE | `agent_injection_bench: MISSING` in repo. |
| EVIDENCE | No repo reference found. |
| OPTIONS | Future work only vs secondary external (separate ID/budget). |
| SCIENTIFIC_IMPACT | Generalization beyond vnext_confirm. |
| REPRODUCIBILITY_IMPACT | Separate artifact chain. |
| COST_IMPACT | Not in $3 Q1 scope. |
| DEPENDENCIES | D10 |
| RISK_IF_WRONG | Scope creep. |
| OWNER_DECISION_REQUIRED | Yes |
| RECOMMENDED_DEFAULT | Future work / separate protocol (not Q1 confirmatory). |
| STATUS | OPEN |

---

### D19 — Failure Analysis

| Field | Content |
|-------|---------|
| DECISION_ID | D19 |
| QUESTION | Pre-specified failure breakdown tables? |
| CURRENT_REPO_STATE | `taxonomy_ref SUPPORTED`; `q1_failure_report_spec MISSING`. |
| EVIDENCE | VNEXT taxonomy; MT1 episode `taxonomy_class`. |
| OPTIONS | Mandatory tables: FN/FP by family, judge_fail, B2 turn-outcome, J1/J2 disagreement. |
| SCIENTIFIC_IMPACT | Explains negative/null results. |
| REPRODUCIBILITY_IMPACT | Derived from raw jsonl only. |
| COST_IMPACT | Neutral (offline). |
| DEPENDENCIES | D09, D11 |
| RISK_IF_WRONG | Cherry-picked failure stories. |
| OWNER_DECISION_REQUIRED | Yes |
| RECOMMENDED_DEFAULT | Reuse VNEXT taxonomy columns in derived metrics (owner sign-off). |
| STATUS | OPEN |

---

## Contract change plan (post sign-off only)

| File | Section | Current | Required after owner | Reason |
|------|---------|---------|----------------------|--------|
| `configs/q1_evaluation_contract.yaml` | `arms.B1/B2` | NEEDS_DECISION | Locked keys/IDs | D04,D05 |
| same | `statistics.*` | NEEDS_DECISION | Locked SAP | D09 |
| same | `primary_episode_budget.benign_episodes` | NEEDS_DECISION | Formula + N | D06 |
| same | `supplementary.subset` | NEEDS_DECISION | path + sha256 | D13 |
| same | `judges.*` | NEEDS_DECISION | verified model ids | D11,D12 |
| `configs/models_q1_eval_panel.yaml` | UNVERIFIED rows | NEEDS_DECISION | provider+model | D12 |
| same | — | — | **Do not edit until D12/D11 locked** | integrity |
| `configs/models.yaml` | — | frozen | **no change** | VNEXT binding |

No runner wiring until execution gate satisfied.

## Execution gate checklist

All must be **LOCKED** (not NEEDS_DECISION): D01–D19 fields + runner mapping + preflight + Phase7 authorization.

**Current:** **BLOCKED** — owner sign-off required.

---

## Signable Owner Decision Record (HEAD `3669509`)

**Owner sign-off field:** _empty until human fills `OWNER_DECISION` column and commits / signs._

| ID | Current Status | Owner Decision | Evidence (repo) | Dependency | Lockable? |
|----|----------------|----------------|-----------------|------------|-----------|
| D01 | NEEDS_OWNER_DECISION | — | Q1 contract has no RQ/H; VNEXT RQ separate (`VNEXT_PROTOCOL.md` §2) | — | No |
| D02 | NEEDS_OWNER_DECISION | — | `endpoints.primary_security`; B2 `EPISODE_SUCCESS_RULE` (`b2_adaptive_contract.py`); `compute_real_metrics` | D01 | No |
| D03 | NEEDS_OWNER_DECISION | — | `holm_correction` (`statistics.py`); comparisons not preregistered | D01,D02 | No |
| D04 | NEEDS_OWNER_DECISION | — | `B1`/`STATIC-A3`/`STATIC-A1` (`defense_baselines.py`); DIAG used `B1` | D03 | No |
| D05 | NEEDS_OWNER_DECISION | — | `LIVE_WIRING_MAX_TURNS=3`; condition IDs in `b2_adaptive_contract` / `b2_matrix_contract`; `AdaptiveAttacker` vs `FixedSequenceAttacker` | D03,D04 | No |
| D06 | NEEDS_OWNER_DECISION | — | 61 benign in pack; attack budget 732 only; options A/B/C not chosen | D02 | No |
| D07 | NEEDS_OWNER_DECISION | — | No Q1 ablation arms; escalation/RiskCore in code only | D05 | No |
| D08 | NEEDS_OWNER_DECISION | — | τ=0.25 in `make_b1_rule_based` / `B1_RULE_THRESHOLD` (if D04=`B1`) | D04 | No |
| D09 | NEEDS_OWNER_DECISION | — | `mcnemar_test`, `holm_correction`, `delta_hat_*`, Wilson/bootstrap helpers | D02,D03 | No |
| D10 | NEEDS_OWNER_DECISION | — | 61+61 pack; 4 primary slots; hosted nondeterminism | D06,D12,D18 | No |
| D11 | UNVERIFIED | — | J1/J2 slots `NEEDS_DECISION` in panel; no Grok; DeepSeek v3-0324 only (different product name) | D13 | No |
| D12 | UNVERIFIED | — | 3 repo IDs: qwen/mistral/llama in panel; Gemma 3 27B / GPT-5.4 / Claude Sonnet 5 not verified; **not** `gemma-4-31b-it` | D13 | No |
| D13 | NEEDS_OWNER_DECISION | — | No supplementary/J2 subset manifest in `datasets/frozen/` | D06,D11 | No |
| D14 | NEEDS_OWNER_DECISION | — | Label-blind defense (`real_llm_pipeline`); VNEXT leakage patterns | D11 | No |
| D15 | NEEDS_OWNER_DECISION | — | Panel temp=0.0 where set; MT1 `max_retries=0` pattern | D12 | No |
| D16 | NEEDS_OWNER_DECISION | — | Pack order seed 61; runner order not Q1-locked | D05 | No |
| D17 | NEEDS_OWNER_DECISION | — | `BudgetLedger`; hard_cap $3 in contract; reporting fields not locked | D06 | No |
| D18 | NEEDS_OWNER_DECISION | — | `agent-injection-bench` absent from repo | D10 | No |
| D19 | NEEDS_OWNER_DECISION | — | VNEXT taxonomy ref; no Q1 failure table spec | D09,D11 | No |

**Freeze rule:** all rows `Lockable?` → Yes only after `Owner Decision` filled and propagated to `q1_evaluation_contract.yaml` / verified panel rows.

---

## Minimum Q1 Scientific Protocol (freeze scope)

Standardization serves three questions only: (1) what is claimed, (2) is comparison fair/reproducible, (3) can a reviewer rebuild without the authors. Anything else is out of scope for **Protocol Freeze**.

| Tier | D IDs | Freeze before confirmatory live? | Rationale |
|------|-------|----------------------------------|-----------|
| **P0 — required** | D01, D02, D03, D04, D05, D09, D10, D11, D12, D14, D15 (+ missing/retry in D09/D15) | **Yes** | RQ, endpoint/unit, comparisons, B1/B2 arms, SAP+Holm, models, judges, leakage, runtime |
| **P1 — important** | D06, D16, D17, D19, D08 | **Yes if claiming utility / cost-aware / B1 rule-based** | Benign matrix, order, cost reporting, failure tables, τ sensitivity |
| **P2 — deferrable** | D07 (ablations), D18 (external bench) | **No for initial Q1 freeze** | Architecture ablations = separate experiment ID; `agent-injection-bench` = secondary/future unless owner elevates |

**Stop rule:** Do not block Q1 on D18 or full ablation matrix (D07). Protocol Freeze minimum = **all P0** + owner-selected P1 items tied to stated claims (e.g. utility claim → D06; Cost-Aware title → D17).

**Not infinite:** After P0 (+ required P1) `OWNER_DECIDED`, freeze contract and proceed to runner mapping / preflight / auth as separate gates.
