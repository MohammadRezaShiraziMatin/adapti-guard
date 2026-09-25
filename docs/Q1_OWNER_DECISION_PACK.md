# Q1 Owner Decision Pack

**HEAD:** `b871733` · **execution_gate:** `BLOCKED` · **p0_freeze_ready:** `false`  
Proposals below are `PROPOSED — REQUIRES OWNER APPROVAL` unless marked otherwise. **Proposal ≠ Owner Decision.**

## Canonical decision map (single source per topic)

| Topic | Canonical ID | Other sections |
|---|---|---|
| α, Holm family, multiplicity correction | **D03** | D09 references D03 only |
| Retry policy | **D15** | D09 references D15 only |
| Episode order / randomization | **D15** | D16 references D15 only |
| Primary target models (OpenRouter IDs) | **D11** | — |
| Q1 judges J1/J2 + protocol | **D12** | MT2 judges listed as separate protocol evidence only |
| Primary attack episode count N | **Owner + contract** `primary_episode_budget.attack_episodes` | Derived: `n_attack × n_primary_targets × n_arms` |
| Live budget cap | **Owner + contract** `budget.hard_cap_usd` | No agent default |

**D11 semantics:** primary **target** panel slots only.  
**D12 semantics:** Q1 **judge** panel (J1 primary, J2 agreement) + optional cross-reference to MT2 judge registry (different protocol).

---

# P0 — Owner decisions (12 items)

## D01 — Research Questions

**Owner Decision required:**
- RQ1:
- H0:
- H1:

```text
Evidence: No Q1 RQ in contract. Arms B0/B1/B2; judge-labeled attack_success_rate path.
Proposal: (PROPOSED — REQUIRES OWNER APPROVAL) RQ on B0 vs B1/B2 attack success on vnext_confirm_v1 attacks.
Owner Approval Required: APPROVE / REJECT / replace in fields above.
```

---

## D02 — Endpoint / Estimand / Unit

**Owner Decision required:**
- Primary endpoint:
- Estimand:
- Unit of analysis:

```text
Evidence: attack_success_rate; B2 final_turn_only; McNemar δ̂ helper in statistics.py.
Proposal: (PROPOSED — REQUIRES OWNER APPROVAL) judge ASR; δ̂=(b10−b01)/n_attack; episode per (attack_id, target, arm).
Owner Approval Required: APPROVE / REJECT.
```

---

## D03 — Primary Comparisons / α / Holm *(canonical for α & multiplicity)*

**Owner Decision required:**
- Primary comparison #1:
- Primary comparison #2:
- Primary comparison #3:
- α:
- Multiple-comparison family:
- Correction:

```text
Evidence: Pairwise B0–B1, B0–B2, B1–B2 possible; mcnemar_exact + holm_correction in repo.
Proposal: (PROPOSED — REQUIRES OWNER APPROVAL) B0–B1 and B0–B2 only; α=0.05 two-sided; Holm over those two tests.
Owner Approval Required: APPROVE / REJECT.
```

---

## D04 — B1

**Owner Decision required:** `B1` / `STATIC-A3` / `STATIC-A1`

```text
Evidence: make_b1_rule_based vs STATIC-A3/A1 in defense_baselines.py.
Proposal: (PROPOSED — REQUIRES OWNER APPROVAL) B1 rule-based.
Owner Approval Required: APPROVE / select alternate supported key.
```

---

## D05 — B2

**Owner Decision required:**
- condition_id:
- attacker mode: `FixedSequenceAttacker` / `AdaptiveAttacker`
- evaluation design: `defense-only` / `matrix`

```text
Evidence: B2_LIVE_CONDITION_IDS; attack_mode_for_condition_id (fixed vs adaptive).
Proposal: (PROPOSED — REQUIRES OWNER APPROVAL) B2-ADAPTIVE-B1, AdaptiveAttacker, defense-only.
Owner Approval Required: APPROVE / REJECT.
```

---

## D09 — Statistical Analysis Plan

**Owner Decision required:**
- statistical test:
- effect size / estimand:
- CI:
- missing outcome:
- judge failure:
- exclusion:
- ties:
- α / multiplicity / correction: *(see **D03** — do not duplicate)*

- retry: *(see **D15** — do not duplicate)*

```text
Evidence: mcnemar_test, bootstrap CI, Wilson in statistics.py.
Proposal: (PROPOSED — REQUIRES OWNER APPROVAL) mcnemar_exact; δ̂ and bootstrap CI; unscorable exclusions; ties discordant-only; α/Holm per D03; retry per D15.
Owner Approval Required: APPROVE / REJECT.
```

---

## D10 — Claims

**Owner Decision required:**
- primary claim:
- target/model scope:
- attack scope:
- defense scope:
- generalization boundary:
- explicit limitations:

```text
Evidence: 61 attacks frozen pack; 4 primary keys; supplementary not pooled.
Proposal: (PROPOSED — REQUIRES OWNER APPROVAL) scoped McNemar/ASR claims only; no SOTA/production claim.
Owner Approval Required: APPROVE / REJECT.
```

---

## D11 — Target Model Panel *(targets only)*

**Supported repository choices** (OpenRouter IDs verified in `configs/mt2_openrouter_catalog_snapshot.json` and/or `models_q1_eval_panel.yaml`):

| Slot | Exact ID | Source | Owner Decision |
|---|---|---|---|
| Qwen 3 30B A3B | `qwen/qwen3-30b-a3b` | panel + catalog snapshot | LOCK / REJECT |
| Mistral Small 3.2 24B Instruct | `mistralai/mistral-small-3.2-24b-instruct` | panel + catalog snapshot | LOCK / REJECT |
| Llama 3.3 70B Instruct | `meta-llama/llama-3.3-70b-instruct` | panel + catalog snapshot | LOCK / REJECT |

**Not in supported choices** (no exact Gemma 3 27B ID in repo or catalog snapshot): Gemma 3 27B slot — owner may REJECT slot or supply a verified ID outside this list after independent check.

**Owner Decision required:**
- Qwen: LOCK / REJECT
- Mistral: LOCK / REJECT
- Llama: LOCK / REJECT
- Gemma 3 27B: LOCK / REJECT — if LOCK, exact OpenRouter id:

---

## D12 — Judges *(Q1 J1/J2; MT2 separate protocol)*

### Q1 judge slots (this protocol)

**Supported repository choices:** none for product labels “DeepSeek V4 Flash” / “Grok 4.7” — no matching exact IDs in Q1 panel or MT2 catalog snapshot.

**Owner Decision required:**
- J1: LOCK / REJECT — if LOCK, exact OpenRouter id:
- J2: LOCK / REJECT — if LOCK, exact OpenRouter id:
- blindness:
- independence:
- disagreement:
- adjudication:

### MT2 confirmatory protocol (`docs/PROTOCOL_MT2.md`, `configs/models_mt2.yaml`) — **not** Q1 J1/J2

Supported repository choices (catalog snapshot + MT2 registry; do not auto-lock for Q1):

| Role | Exact ID | Config key |
|---|---|---|
| MT2 primary judge | `openai/gpt-oss-120b` | `mt2_judge_primary` |
| MT2 secondary judge | `deepseek/deepseek-chat-v3-0324` | `mt2_judge_secondary` |

```text
Evidence: MT2 uses separate panel contract; forbidden_shared_vendor_between_target_and_judge in mt2_panel.yaml.
Proposal: (PROPOSED — REQUIRES OWNER APPROVAL) Q1 blindness per docs/archive/q1/JUDGE_PROTOCOL.md when J1/J2 IDs are owner-supplied.
Owner Approval Required: APPROVE / REJECT.
```

---

## D13 — Subsets

**Owner Decision required:**
- supplementary subset: `path + SHA` / `none`
- J2 validation subset: `path + SHA` / `none`

```text
Proposal: (PROPOSED — REQUIRES OWNER APPROVAL) none / none until frozen manifests exist.
Owner Approval Required: APPROVE / REJECT.
```

---

## D14 — Leakage / Contamination

**Owner Decision required:**
- defense blindness:
- target blindness:
- judge input restrictions:
- dataset leakage policy:
- contamination exclusion policy:

```text
Evidence: label-blind non-oracle arms in real_llm_pipeline.py; archive judge blindness.
Proposal: (PROPOSED — REQUIRES OWNER APPROVAL) minimal policies aligned with repo controls.
Owner Approval Required: APPROVE / REJECT.
```

---

## D15 — Runtime *(canonical retry + ordering)*

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

```text
Evidence: panel temp 0.0, max_tokens 512; live max_retries=0; budget.hard_cap_usd NEEDS_DECISION in contract.
Proposal: (PROPOSED — REQUIRES OWNER APPROVAL) lock temp 0.0, max_tokens 512, retry 0 live; ordering fixed manifest; randomization none unless D16 claim.
Owner Approval Required: APPROVE / REJECT.
```

### Episode budget & cap *(contract fields)*

**Owner Decision required:**
- `primary_episode_budget.attack_episodes`: *(numeric or confirm derived)*
- `budget.hard_cap_usd`:

```text
Evidence: formula n_attack * n_primary_targets * n_arms; derived currently 732 if 61×4×3 unchanged. No sufficiency claim for budget.
Owner Approval Required: owner sets both values in contract at propagation step.
```

---

# P1 — Claim-gated

| ID | Status |
|---|---|
| D06 | CLAIM-GATED / OWNER DECISION REQUIRED |
| D08 | CLAIM-GATED / OWNER DECISION REQUIRED |
| D16 | CLAIM-GATED — references **D15** ordering/randomization |
| D17 | CLAIM-GATED / OWNER DECISION REQUIRED |
| D19 | CLAIM-GATED / OWNER DECISION REQUIRED |

# P2 — Owner decision required (not agent-deferred)

| ID | Status |
|---|---|
| D07 Ablation | NEEDS_OWNER_DECISION |
| D18 External benchmark | NEEDS_OWNER_DECISION |

---

After owner fill → validate → propagate to `configs/q1_evaluation_contract.yaml` and `configs/models_q1_eval_panel.yaml` only.
