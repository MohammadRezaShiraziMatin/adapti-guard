# Q1 Owner Decision Pack — P0 proposals (documentation only)

**HEAD:** `2bd53a0` · **execution_gate:** `BLOCKED` · **p0_freeze_ready:** `false`  
**Status:** `PROPOSAL DOCUMENTATION` — **Proposal ≠ Owner Decision.** All **Owner Decision** fields remain **EMPTY**.

## Canonical decision map

| Topic | Canonical ID | References |
|---|---|---|
| α, Holm family, multiplicity | **D03** | D09 |
| Retry | **D15** | D09 |
| Order / randomization | **D15** | D16 |
| Target models | **D11** | — |
| Q1 judges J1/J2 | **D12** | MT2 block = separate protocol |
| `attack_episodes` | contract + **Owner** | derived = `n_attack × n_primary_targets × n_arms` |
| `hard_cap_usd` | contract + **Owner** | no agent default |

---

# P0 proposals (D01–D15)

## D01 — Research Questions / Hypotheses

| | |
|---|---|
| **Question** | What are Q1 RQ and H0/H1 for runtime intervention vs prompt injection across B0/B1/B2? |
| **Repository Evidence** | README: hash-locked testbed for prompt-injection; fixed/adaptive intervention policies L0–L3; Q1 contract arms B0/B1/B2 on `vnext_confirm_v1` (61 attacks). No Q1 RQ text (`scientific_design.research_questions: NEEDS_DECISION`). VNEXT Track A is separate confirmatory track. |
| **Supported Choices** | Owner-authored RQ/H only (no repo-locked RQ). Must be testable with judge-labeled ASR + paired comparisons on frozen pack. |
| **Implication** | RQ bounds which comparisons (D03) and claims (D10) are in scope; utility/cost only if D06/D17 claimed. |
| **Proposal** | **PROPOSED — REQUIRES OWNER APPROVAL:** RQ1: On `vnext_confirm_v1` gold attacks, do static (B1) or adaptive multi-turn (B2) runtime interventions reduce judge-labeled attack success vs B0 on the locked primary target panel? H0: For each prespecified B0-reference pair (D03), paired discordant attack outcomes are exchangeable (McNemar null). H1: For at least one prespecified pair, attack success rate differs from B0 in the direction of lower success under defense. B2 claim scope: multi-turn **defense protocol** (contract `adaptive_multi_turn_defense`), not conflation with “adaptive attacker” unless D05 binds it. Cost/utility: not co-primary unless owner adds via D06/D10. |
| **Confidence** | Medium — aligned with README + contract arms; RQ wording needs owner sign-off. |
| **Owner must approve** | Exact RQ1, H0, H1 text; whether utility/cost is in RQ scope. |

**Owner Decision:** EMPTY  
- RQ1:  
- H0:  
- H1:  

---

## D02 — Primary Endpoint / Estimand / Unit

| | |
|---|---|
| **Question** | Primary endpoint, estimand, and unit of analysis for B0/B1/B2? |
| **Repository Evidence** | `endpoints.primary_security: attack_success_rate`; `compute_real_metrics` / `evaluate_episode` (B0/B1 single-turn); B2 `episode_judgment: final_turn_only`, `EPISODE_SUCCESS_RULE` = judge `attack_success` on final executed turn (`b2_adaptive_contract`); `attack_benign_split: separate_endpoints`. |
| **Supported Choices** | Judge-labeled attack success on gold attacks; episode-level unit; paired attack IDs across arms; B2 success = final turn only (not turn-level primary in contract: `turn_level_primary: MISSING`). |
| **Implication** | McNemar (D09) requires consistent pairing key = attack_id × target_model across arms. |
| **Proposal** | **PROPOSED — REQUIRES OWNER APPROVAL:** Primary endpoint = attack_success_rate (proportion of gold attack episodes with judge `attack_success=true`). Estimand = paired difference in attack success via McNemar discordant cells; δ̂ = (b10−b01)/n_attack (`delta_hat_from_mcnemar_contingency`). Unit = one episode per (attack_id, primary target, arm); B2 episode may include ≤3 turns but success is final-turn judge verdict only. |
| **Confidence** | High — matches implemented metrics path. |
| **Owner must approve** | Whether utility co-endpoint is co-primary (else benign stays separate per D06). |

**Owner Decision:** EMPTY  
- Primary endpoint:  
- Estimand:  
- Unit of analysis:  

---

## D03 — Primary Comparisons / α / Multiplicity *(canonical)*

| | |
|---|---|
| **Question** | Which arm pairs are primary; α; Holm family; correction method? |
| **Repository Evidence** | Arms {B0,B1,B2}; `statistics.paired_attack_test: mcnemar_exact`; `holm_correction` in `statistics.py`; `multiple_comparison: NEEDS_DECISION`. |
| **Supported Choices** | Subset of {B0 vs B1, B0 vs B2, B1 vs B2}; Holm via `holm_correction`; McNemar exact only wired as primary test in contract. |
| **Implication** | Family size drives power and claim count; B1 vs B2 optional third pair increases multiplicity. |
| **Proposal** | **PROPOSED — REQUIRES OWNER APPROVAL:** Primary comparisons: (1) B0 vs B1, (2) B0 vs B2 only (omit B1 vs B2 from confirmatory family). α = 0.05 two-sided (proposal only; VNEXT memo uses 0.05 as reference, not Q1 lock). Family = two B0-reference tests at study level (pool targets per comparison or stratify — owner must pick pooling rule). Correction = Holm-Bonferroni on family p-values. |
| **Confidence** | Medium — minimal family; pooling rule unresolved. |
| **Owner must approve** | Exact comparison list, α, family definition (per-target vs pooled). |

**Owner Decision:** EMPTY  
- Primary comparison #1:  
- Primary comparison #2:  
- Primary comparison #3:  
- α:  
- Multiple-comparison family:  
- Correction:  

---

## D04 — Static defense arm (B1)

| | |
|---|---|
| **Question** | Which static defense maps to Q1 arm B1? |
| **Repository Evidence** | `BASELINE_FACTORIES`: `B1`→`make_b1_rule_based` (detector threshold, default τ=0.25 in matrix); `STATIC-A3`→unconditional block; `STATIC-A1`→unconditional sanitize (`defense_baselines.py`). `live_b0_report` uses `make_b1_rule_based` for B1 path. |
| **Supported Choices** | Exactly one of: `B1`, `STATIC-A3`, `STATIC-A1`. |
| **Implication** | D08 threshold sweep only applies if D04=`B1` rule-based. |
| **Proposal** | **PROPOSED — REQUIRES OWNER APPROVAL:** `B1` / `make_b1_rule_based` as Q1 static arm (matches existing live B1 wiring and B2-ADAPTIVE-B1 defense mode in matrix). |
| **Confidence** | Medium-high for operational alignment; owner may prefer unconditional STATIC-A3/A1 for interpretability. |
| **Owner must approve** | Single resolver key choice. |

**Owner Decision:** EMPTY  

---

## D05 — B2 condition / attacker contract

| | |
|---|---|
| **Question** | B2 `condition_id`, attacker mode, evaluation design scope? |
| **Repository Evidence** | `B2_LIVE_CONDITION_IDS`; `attack_mode_for_condition_id`: `B2-FIXED*`→`FixedSequenceAttacker`; `B2-ADAPTIVE*`→`AdaptiveAttacker` (`b2_attack_mode_contract`); `B2_B1_RELATIONSHIP` separates multi-turn B2 from single-turn B1; contract `max_turns: 3`. |
| **Supported Choices** | condition_id from repo set; modes FixedSequence vs Adaptive per mapping; design `defense-only` (single cell) vs `matrix` (2×2 attack-mode study). |
| **Implication** | Adaptive **attacker** rotates families on defense feedback; adaptive **defense** is B2 arm role — primary claim should state which is held fixed in D05. |
| **Proposal** | **PROPOSED — REQUIRES OWNER APPROVAL:** `condition_id=B2-ADAPTIVE-B1`, attacker mode=`AdaptiveAttacker`, design=`defense-only` (one Q1 B2 arm; defense mode B1 under multi-turn protocol). Primary comparison B0 vs B2 then measures this bundle, not a full attack-mode matrix. |
| **Confidence** | Medium — consistent with contract B2 role; owner may choose `B2-FIXED-B1` for fixed-sequence attacker. |
| **Owner must approve** | condition_id, attacker class, defense-only vs matrix. |

**Owner Decision:** EMPTY  
- condition_id:  
- attacker mode:  
- evaluation design:  

---

## D06 — Utility / benign (P1)

| | |
|---|---|
| **Question** | Benign matrix and utility tier for claims? |
| **Repository Evidence** | `n_benign: 61`; `primary_utility: benign_utility_success`; `benign_episodes: NEEDS_DECISION`; VNEXT utility gate pattern in memos (not Q1-locked). |
| **Supported Choices** | 0 benign episodes; full symmetric matrix; utility as gate vs secondary. |
| **Implication** | Not required for minimum security-only P0 closure unless D10 claims utility. |
| **Proposal** | **PROPOSED — REQUIRES OWNER APPROVAL:** DEFER benign matrix for minimum Q1 security claim; if owner claims FPR/utility, set benign_episodes = owner N and tier in D10. |
| **Confidence** | Medium. |
| **Owner must approve** | IN SCOPE vs defer; benign N if in scope. |

**Owner Decision:** EMPTY (P1 claim-gated)

---

## D07 — Ablations (P2)

| | |
|---|---|
| **Question** | Ablation arms for Q1? |
| **Repository Evidence** | Contract `ablations: MISSING`; `_ABLATION_KEYS` in `defense_baselines.py` (diagnostic, not Q1-registered). Contract intake: `NEEDS_OWNER_DECISION`. |
| **Supported Choices** | Owner defines separate experiment ID or none. |
| **Proposal** | **PROPOSED — REQUIRES OWNER APPROVAL:** No ablation arms in Q1 confirmatory 732-class matrix unless owner adds new experiment — keep Q1 to B0/B1/B2 only. |
| **Confidence** | High for minimum scope. |
| **Owner must approve** | Whether any ablation is in Q1 scope. |

**Owner Decision:** EMPTY · **Status:** `NEEDS_OWNER_DECISION` (not DEFERRED)

---

## D08 — B1 threshold τ (P1)

| | |
|---|---|
| **Question** | Preregistered τ / sensitivity for rule-based B1? |
| **Repository Evidence** | `B1_RULE_THRESHOLD=0.25` in `b2_matrix_contract` only; Q1 `threshold_sensitivity: MISSING`. |
| **Supported Choices** | Single τ; grid (owner-listed). |
| **Implication** | Only if D04=`B1` and claim mentions robustness. |
| **Proposal** | **PROPOSED — REQUIRES OWNER APPROVAL:** Single τ=0.25 if D04=B1; no sweep unless claim requires (then owner lists grid). |
| **Confidence** | Medium. |
| **Owner must approve** | Defer vs preregister sweep. |

**Owner Decision:** EMPTY (P1 claim-gated)

---

## D09 — Statistical Analysis Plan

| | |
|---|---|
| **Question** | Complete SAP excluding canonical D03 (α/multiplicity) and D15 (retry). |
| **Repository Evidence** | `mcnemar_test`, `holm_correction`, `delta_hat_*`, Wilson/bootstrap in `statistics.py`. |
| **Supported Choices** | McNemar exact; bootstrap/Wilson CIs; exclude unscorable episodes. |
| **Implication** | Must reference D03 for α/Holm; D15 for retry; D12 for judge failure/disagreement. |
| **Proposal** | **PROPOSED — REQUIRES OWNER APPROVAL:** Test: `mcnemar_exact` per D03 comparisons (paired on attack_id×target). Effect size: δ̂ per D02. CI: 95% bootstrap (`n_bootstrap=5000`). Ties: use discordant cells only. Missing/malformed/timeout target: episode unscorable, exclude from pair. Judge failure (J1): unscorable, exclude. Disagreement (J1 vs J2): report rate on J2 subset if D13 defines one; primary analysis J1 only. Exclusion: pre-registered unscorable only. Multiplicity/α: **see D03**. Retry: **see D15**. |
| **Confidence** | Medium-high on test/estimand; disagreement policy needs owner. |
| **Owner must approve** | J2 role; exclusion strictness. |

**Owner Decision:** EMPTY  
- statistical test:  
- effect size / estimand:  
- CI:  
- missing outcome:  
- judge failure:  
- exclusion:  
- ties:  

---

## D10 — Claim scope

| | |
|---|---|
| **Question** | Allowed wording and boundaries? |
| **Repository Evidence** | 61 attacks; 4 primary keys (one may be REJECTED); 3 arms; supplementary not pooled; README warns against SOTA/production claims. |
| **Supported Choices** | Internal pack + locked panel + prespecified arms only. |
| **Implication** | Must match D03 comparisons and D11 locks. |
| **Proposal** | **PROPOSED — REQUIRES OWNER APPROVAL:** Claim paired McNemar/ASR results for B0–B1 and B0–B2 on frozen 61 attacks and owner-locked primary targets; multi-turn B2 as specified in D05; no external benchmark superiority (D18 not in Q1); no SOTA; cost/latency only if D17 in scope; stochastic LLM disclaimer. |
| **Confidence** | High if D11/D05 approved as proposed. |
| **Owner must approve** | Final claim text. |

**Owner Decision:** EMPTY  
- primary claim:  
- target/model scope:  
- attack scope:  
- defense scope:  
- generalization boundary:  
- explicit limitations:  

---

## D11 — Target model panel

| | |
|---|---|
| **Question** | LOCK/REJECT per primary target; exact IDs. |
| **Repository Evidence** | `models_q1_eval_panel.yaml`; catalog `configs/mt2_openrouter_catalog_snapshot.json`. |
| **Supported Choices** | Verified IDs only (below). Gemma 3 27B: **NOT SUPPORTED / OWNER ACTION REQUIRED** (no exact ID in repo or snapshot). |
| **Implication** | Derived episodes use `n_primary_targets` = count of locked primaries (contract currently lists 4 keys until propagation). |
| **Proposal** | **PROPOSED — REQUIRES OWNER APPROVAL:** LOCK Qwen `qwen/qwen3-30b-a3b`, Mistral `mistralai/mistral-small-3.2-24b-instruct`, Llama `meta-llama/llama-3.3-70b-instruct`. REJECT or replace Gemma 3 27B slot until owner supplies verified OpenRouter ID (do not use `google/gemma-4-31b-it` without explicit owner ID). |
| **Confidence** | High for three models; Gemma unresolved. |
| **Owner must approve** | Per-slot LOCK/REJECT; Gemma ID or panel size change at propagation. |

**Owner Decision:** EMPTY  

| Slot | Exact ID | Verification | Owner Decision |
|---|---|---|---|
| Qwen 3 30B A3B | `qwen/qwen3-30b-a3b` | catalog + panel | |
| Mistral Small 3.2 24B | `mistralai/mistral-small-3.2-24b-instruct` | catalog + panel | |
| Llama 3.3 70B | `meta-llama/llama-3.3-70b-instruct` | catalog + panel | |
| Gemma 3 27B | — | NOT SUPPORTED | |

---

## D12 — Judge panel

| | |
|---|---|
| **Question** | Q1 J1/J2 IDs and protocol; MT2 reference only. |
| **Repository Evidence** | Q1 panel judges `NEEDS_DECISION`; archive `JUDGE_PROTOCOL.md` blindness rules. MT2: `openai/gpt-oss-120b`, `deepseek/deepseek-chat-v3-0324` in `models_mt2.yaml` + catalog. |
| **Supported Choices (Q1)** | **None** for labeled “DeepSeek V4 Flash” / “Grok 4.7” — **NOT SUPPORTED** until owner supplies exact OpenRouter IDs. |
| **Supported Choices (MT2 only)** | `openai/gpt-oss-120b`, `deepseek/deepseek-chat-v3-0324` — do not import into Q1 without owner. |
| **Implication** | J2 subset ties to D13; disagreement handling in D09. |
| **Proposal** | **PROPOSED — REQUIRES OWNER APPROVAL:** Owner supplies J1/J2 exact IDs. Blindness/independence: archive template (no baseline/defense/blocked/detector in judge input). Disagreement: report J1≠J2 rate; primary analysis J1; adjudication = owner rule (no third-judge code). Validation subset: **see D13**. |
| **Confidence** | Low for IDs; medium for protocol template. |
| **Owner must approve** | Exact J1/J2 IDs; adjudication rule. |

**Owner Decision:** EMPTY  

### MT2 evidence (separate protocol — not Q1 J1/J2)

| Role | Exact ID |
|---|---|
| MT2 primary judge | `openai/gpt-oss-120b` |
| MT2 secondary judge | `deepseek/deepseek-chat-v3-0324` |

---

## D13 — Supplementary / validation subsets

| | |
|---|---|
| **Question** | Subset path+SHA for supplementary runs and J2 validation? |
| **Repository Evidence** | `supplementary_targets.subset` NEEDS_DECISION; no Q1 subset manifest in repo. Full pack SHA `523c8818…`. |
| **Supported Choices** | `none`; or frozen manifest under `datasets/frozen/` with SHA (owner-provided). |
| **Implication** | J2 `frozen_subset_only` in contract requires matching SHA if subset used. |
| **Proposal** | **PROPOSED — REQUIRES OWNER APPROVAL:** supplementary subset = `none`; J2 validation subset = `none` for minimum Q1. |
| **Confidence** | High absent owner manifests. |
| **Owner must approve** | Paths/SHA or confirm none. |

**Owner Decision:** EMPTY  
- supplementary subset:  
- J2 validation subset:  

---

## D14 — Leakage / contamination

| | |
|---|---|
| **Question** | Label/judge leakage and exclusion policies? |
| **Repository Evidence** | `real_llm_pipeline.py` label-blind non-oracle arms; `ORACLE_*` diagnostic only; archive judge blindness. |
| **Supported Choices** | Documented blindness only (no new controls claimed as implemented). |
| **Implication** | D12 judge input must match stated restrictions. |
| **Proposal** | **PROPOSED — REQUIRES OWNER APPROVAL:** Defense/target paths without gold attack label; judge sees only archive-permitted fields; frozen pack only; exclude episodes if contamination suspected (pre-registered rule). |
| **Confidence** | Medium-high for defense blindness; judge policy depends on D12 IDs. |
| **Owner must approve** | Contamination exclusion trigger. |

**Owner Decision:** EMPTY  

---

## D15 — Runtime / randomization / reproducibility *(canonical retry + order)*

| | |
|---|---|
| **Question** | Runtime parameters and execution order? |
| **Repository Evidence** | Panel `temperature: 0.0`, `max_tokens: 512`; live `max_retries=0`; B2 `max_turns=3`; `hard_cap_usd: NEEDS_DECISION`. |
| **Supported Choices** | Values evidenced in panel/live wiring; owner must set timeout/top_p/seed if needed. |
| **Implication** | D09 references retry here; D16 references order here. |
| **Proposal** | **PROPOSED — REQUIRES OWNER APPROVAL:** temperature=0.0, max_tokens=512, live retry=0; top_p/seed/timeout=owner-specified or provider default (document in manifest); malformed/missing→unscorable; ordering=fixed attack_id order; randomization=none unless D16 claim. |
| **Confidence** | Medium. |
| **Owner must approve** | timeout/top_p/seed; order manifest. |

**Owner Decision:** EMPTY  

---

# Derived workload & budget (no owner lock)

| Quantity | Formula / evidence | Current derived (if defaults unchanged) |
|---|---|---|
| Primary attack episodes | `n_attack × n_primary_targets × n_arms` | 61 × 4 × 3 = **732** (contract `attack_episodes: NEEDS_DECISION`) |
| B2 target calls (upper bound) | attack episodes for B2 arm × `max_turns` (3) | ≤ 732 × 3 target calls (not additive to episode count) |
| Primary judge calls (J1) | ~1 per scorable attack episode per arm | ≤ ~732 per full matrix (excl. unscorable) |
| J2 calls | subset only if D13 defines | **unresolved** if subset none |
| Supplementary | separate if D13 + panel | **unresolved** (2 supplementary keys in contract) |
| `hard_cap_usd` | Owner Decision | **NEEDS_DECISION** — no sufficiency claim |

---

# Scientific consistency matrix (proposal-level)

| Link | Proposal alignment | Unresolved |
|---|---|---|
| RQ → Endpoint | RQ asks attack-success reduction; endpoint ASR | Utility only if D06/D10 expanded |
| Endpoint → Unit | ASR on episodes; McNemar paired attacks | Pooling across 4 targets in D03 |
| Unit → Comparison | Paired per attack×target | B2 final-turn vs B0/B1 single-turn semantics documented in D02 |
| Comparison → SAP | B0–B1, B0–B2 McNemar + Holm | B1 vs B2 omitted — OK if not claimed |
| Panel → Claim | Up to 3 LOCK + Gemma gap | Gemma slot vs “4 models” wording |
| SAP → Claim | McNemar + δ̂ only | Judge IDs not supported until owner adds |
| D05 → D10 | B2 bundle named in claim | Attacker adaptive in proposal — must match D05 approval |

**Contradictions to resolve at approval:** Gemma 3 27B in contract keys vs NOT SUPPORTED; Q1 judge labels vs no supported IDs.

---

# P1 / P2 status (unchanged)

| ID | Status |
|---|---|
| D06, D08, D16, D17, D19 | CLAIM-GATED / OWNER DECISION REQUIRED |
| D07, D18 | **NEEDS_OWNER_DECISION** |

---

After owner fills **Owner Decision** fields → validate → propagate (separate step). **execution_gate** remains `BLOCKED` until then.
