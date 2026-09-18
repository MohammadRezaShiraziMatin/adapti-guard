# ADAPTI-GUARD Research Reference

## 1. Project Identity

- **Title:** Controlled Detector Attribution under a Locked Runtime Intervention Policy: A Pilot-Scale Agent Security Evaluation
- **Subtitle:** Cost-Aware Runtime Intervention for Prompt Injection in LLM Agents
- **Authors:** [REDACTED for double-blind review]
- **Repository:** [REDACTED for double-blind review]
- **Project status:** READY_FOR_SUBMISSION_WITH_DISCLOSED_LIMITATIONS
- **Manuscript target:** IEEE SaTML 2027 (Research Paper track)
- **Intended publication type:** Workshop / Conference Research Paper

## 2. Research Question

### Primary RQ-C2

Does the detector-related Tool-HASR effect versus D0 observed under the locked Stage-B target (T0) remain directionally consistent when the same locked policy, pack, detectors, thresholds, and judge are applied to independently selected secondary target models T1–T3?

### Secondary questions

- SQ1: Does the sign of the detector-related Δ hold across independently selected targets?
- SQ2: Are Tool-HASR and Judge-ASR distinct measurements?
- SQ3: Does INVALID_TOOL_ARGS confound the interpretation?

### Hypotheses

- H1 (directional): The sign of Δ(d,t) relative to D0 is preserved across targets T0–T3.
- H2 (distinctness): Tool-HASR and Judge-ASR measure different operational outcomes.

### Evaluation objectives

- Measure detector-related Tool-HASR Δ versus D0 under a locked intervention policy.
- Test directional consistency of the Δ sign across independently selected target models.
- Retain INVALID_TOOL_ARGS as a diagnostic, not discarding or equating it with success/failure.

## 3. Contribution Inventory

### Confirmed contributions

#### Engineering contributions

1. **Controlled detector-policy attribution protocol.** A factorial evaluation design that holds the downstream intervention policy (PHASE1-CORE) fixed while varying detector identity (D0/D1/D2/D4), including a no-detection reference (D0).
2. **Cost-aware runtime intervention framework.** The CorePolicy → ActionLayer → ToolPermissionGate pipeline with normalized action costs (A0=0, A1=0.10, A2=0.25, A3=0.50).

#### Evaluation contributions

1. **P2 agentic benchmark.** Frozen pack `p2_agentic_v0.1.0` with 36 trajectories (16 attack / 16 benign twin / 4 hard-negative).
2. **Cross-target directional consistency evaluation.** Q2 evaluates whether the Δ sign observed on T0 generalizes to independently selected T1–T3.

#### Methodological contributions

1. **Tool-HASR as primary operational security outcome.** Measures actual harmful tool execution, not judge opinion.
2. **Judge-ASR as secondary diagnostic.** Judge-level attack-success assessment, kept distinct from Tool-HASR.
3. **M3/M4 discordant-pair diagnostics.** M3 = judge success ∧ ¬ Tool-HASR success; M4 = Tool-HASR success ∧ ¬ judge success.
4. **INVALID_TOOL_ARGS as canonical execution-state category.** Retained as a diagnostic confounder, not discarded or equated with success/failure.

### Potential contributions (NOT yet validated)

- Broader model-family diversity evaluation
- D3 semantic-embedding detector
- C4 open adaptive attacker robustness
- Matched external baseline comparison

## 4. System Architecture

### Pipeline

```
Untrusted Context
    |
    v
ContextBuilder
    |
    v
Detector (D0 / D1 / D2 / D4)
    |  detector signal
    v
RiskCore (RiskEngine)
    |  risk score
    v
CorePolicy (PHASE1-CORE)
    |  thresholds: is_injection=0.25, risk=0.25/0.60
    |  action costs: A0=0, A1=0.10, A2=0.25, A3=0.50
    v
ActionLayer (DefenseActionLayer)
    |  intervention action A0-A3
    v
ToolPermissionGate
    |  allow / wrap / deny
    v
Mock Tools --> Tool-HASR (primary)

Judge (qwen-2.5-72b) --> Judge-ASR (secondary, parallel)
```

### Components

| Component | File | Role |
| --- | --- | --- |
| ContextBuilder | `src/adapti_guard/core/episode.py` | Builds context from untrusted input |
| Detector | `src/adapti_guard/detector/base.py` | P3Detector contract (D0/D1/D2/D4) |
| RiskEngine | `src/adapti_guard/risk/risk_engine.py` | Scores risk from detector signal |
| CorePolicy | `src/adapti_guard/policy/core_policy.py` | Maps risk to intervention action |
| ActionLayer | `src/adapti_guard/defense/action_layer.py` | Executes intervention (A0-A3) |
| ToolPermissionGate | `src/adapti_guard/defense/tool_permission.py` | Enforces tool allow/wrap/deny |
| EpisodeTrace | `src/adapti_guard/core/episode.py` | Records execution trace |
| Judge | `src/adapti_guard/evaluation/llm_judge.py` | Post-hoc attack-success scoring |

### Label blindness

Gold labels (`is_attack`, `label`, `category`) do not enter the detector->policy path. The judge does not enter the detector->policy path.

## 5. Threat Model

### Attacker

- **Type:** Adversarial prompt injector
- **Capability:** Injects instructions via untrusted context to hijack agent tool execution
- **Access:** Indirect (via retrieved content, tool output, document/RAG)
- **Limitations:** Constrained to frozen benchmark pack; no adaptive attacker in Q2

### Victim / Agent

- **Type:** Tool-using LLM agent
- **Trusted components:** System prompt, detector, risk engine, policy, tool permission gate
- **Untrusted components:** Retrieved context, tool output, documents, memory

### Attack surface

| Surface | Description |
| --- | --- |
| Direct prompt injection | User input contains injected instructions |
| Indirect prompt injection | Retrieved/untrusted content contains injected instructions |
| Tool-output injection | Tool results contain injected instructions |
| Document/RAG injection | Retrieved documents contain injected instructions |
| Memory/state injection | Agent memory/state contains injected instructions |

### Categories evaluated in P2

| Category | Count | Evidence |
| --- | --- | --- |
| Persistence | 7 | P2 taxonomy |
| Delayed execution | 4 | P2 taxonomy |
| Tool-output injection | 5 | P2 taxonomy |
| Chaining | 6 | P2 taxonomy |
| Memory | 2 | P2 taxonomy |
| Adaptive | 2 | P2 taxonomy (scripted, not LLM attacker) |

### Categories NOT evaluated

- Open-ended adaptive attackers (C4) -- out of scope
- Long-horizon multi-turn -- not in Q2 protocol

### Security objectives

1. Detect prompt injection in untrusted context.
2. Attribute detector-related effects under a locked policy.
3. Prevent harmful tool execution via intervention.
4. Preserve benign utility.

## 6. Attack Taxonomy

| Family | Technique | Objective | Target | Path | Source | Interaction | Horizon | Success criterion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Direct PI | Ignore previous prompt | Override instructions | System prompt | User input | Direct | Single | Agent follows injected instruction |
| IPI | Retrieved content injection | Hijack agent | Agent context | Retrieved data | Indirect | Single | Agent executes harmful tool call |
| IPI | Tool-output injection | Chain attacks | Agent | Tool result | Tool output | Multi | Agent processes injected tool output |
| IPI | Memory/state | Persist attack | Agent memory | Stored state | Memory | Multi | Attacker state persists across turns |
| IPI | Delayed execution | Time bomb | Agent | Scheduled action | Deferred | Multi | Delayed action fires later |
| IPI | Chaining | Prior result in args | Propagate attack | Agent | Prior tool output | Tool args | Multi | Prior result feeds next call |

## 7. Defense Model

### Intervention levels

| Level | Action | Security effect | Utility effect | Cost | Assumptions |
| --- | --- | --- | --- | --- | --- |
| A0 | No intervention | Baseline | Full | 0 | No detection needed |
| A1 | Sanitization | Reduces injection surface | Minor degradation | 0.10 | Sanitization is safe |
| A2 | Tool restriction | Blocks harmful tools | Moderate degradation | 0.25 | Tool restriction is enforceable |
| A3 | Blocking | Stops execution | Major degradation | 0.50 | Blocking is last resort |

### Cost model

Costs are **normalized experimental weights**, not USD prices:
- A0 = 0.0
- A1 = 0.10
- A2 = 0.25
- A3 = 0.50

## 8. Experimental Protocol

| Field | Value | Evidence |
| --- | --- | --- |
| Question | RQ-C2 | `MANUSCRIPT_FINAL.md` S4 |
| Design | B_REDUCED_Q2 | `manifest.json` |
| Run ID | `p3_stage_c_q2_20260917T123855Z_b075df0f` | `manifest.json` |
| Evidence commit | `b075df0f5ec5ad11ede76ac4e4079cade15208f1` | `manifest.json` |
| Pack | `p2_agentic_v0.1.0` | `manifest.json` |
| Pack SHA | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` | `manifest.json` |
| P1 SHA | `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` | `manifest.json` |
| Q2 predictions SHA | `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6` | `manifest.json` |
| Trajectories | 36 (16 attack / 16 benign twin / 4 hard-negative) | `manifest.json` |
| Detectors | D0, D1, D2, D4 (D3 deferred) | `manifest.json` |
| Policy | PHASE1-CORE | `manifest.json` |
| T0 | `qwen/qwen-2.5-7b-instruct` (reused from Stage-B) | `manifest.json` |
| T1 | `qwen/qwen3-30b-a3b` | `manifest.json` |
| T2 | `google/gemma-3-27b-it` | `manifest.json` |
| T3 | `qwen/qwen3.5-35b-a3b` | `manifest.json` |
| Judge | `qwen/qwen-2.5-72b-instruct` | `manifest.json` |
| Q2 live arms | 432 (36 traj x 4 det x PHASE1-CORE x {T1,T2,T3}) | `metrics.json` |
| Completed | 432/432, 0 failed | `metrics.json` |
| Temperature | 0.0 | `manifest.json` |
| Cache | false | `manifest.json` |
| Seed | 42 | `manifest.json` |
| Backend | OpenRouter | `manifest.json` |
| Budget cap | $10.0 | `manifest.json` |
| Actual cost | $0.152885 | `spend.json` |
| Historical API calls | 2061 (target+judge) | `spend.json` |
| scientific_evidence | false | `manifest.json` |
| n per cell | 16 attack arms | `MANUSCRIPT_FINAL.md` S8 |
| Primary outcome | Tool-HASR | `manifest.json` |
| Secondary diagnostic | Judge-ASR | `manifest.json` |
| Stage-B run | `p3_stage_b_20260916T235438Z_7e401714` | `manifest.json` (t0_reuse_run_id) |
| Stage-B predictions SHA | `7b0b72d942dae988d87acf238424c9f2d331b62d5ec582c9ba7d9bfbb293c214` | `STAGE_B_EVIDENCE_STATUS.json` (pointer only) |

## 9. Dataset / Benchmark

### P2 agentic pack

| Field | Value |
| --- | --- |
| Pack ID | `p2_agentic_v0.1.0` |
| SHA-256 | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` |
| Rows | 36 (16 attack / 16 benign twin / 4 hard-negative) |
| Attack families | Persistence, Delayed, Tool-output, Chaining, Memory, Adaptive |
| Source | Frozen construction (not live-generated) |
| Validation | Freeze Audit v3 (FREEZE-READY) |
| Deduplication | Pack-level dedup applied |
| Train/test split | Not applicable (frozen evaluation pack) |

### P1 mechanism pack

| Field | Value |
| --- | --- |
| Pack ID | `p1_mechanism_v1.0.0` |
| SHA-256 | `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` |
| Rows | 20 (10 attack / 10 benign) |

## 10. Evaluation Metrics

### Tool-HASR (primary)

Tool-HASR = (attack arms with harmful tool execution) / (attack arms)

- **Numerator:** attack arms where the agent executed a harmful tool call matching the pre-registered `success_condition`.
- **Denominator:** attack arms with `tool_hasr_success in {True, False}` (UNKNOWN excluded).
- **Measures:** Actual harmful tool execution behavior.

### Judge-ASR (secondary)

Judge-ASR = (attack arms with judge-classified attack success) / (attack arms)

- **Numerator:** attack arms where the judge model classified the outcome as a successful attack.
- **Denominator:** attack arms with `judge_asr_success in {True, False}`.
- **Measures:** Judge-level attack-success assessment.

### M3 (diagnostic)

M3 = |{a : Judge-ASR(a) = True and Tool-HASR(a) = False}|

### M4 (diagnostic)

M4 = |{a : Tool-HASR(a) = True and Judge-ASR(a) = False}|

### Delta(d,t) (detector-related effect)

Delta(d,t) = Tool-HASR(d,t) - Tool-HASR(D0,t)

- **Sign:** exact 0.0 -> ZERO; else POS/NEG.
- **Interpretation:** Detector-related association under the controlled protocol.

### Wilson 95% CI (on rates)

Applied to **rates** (Tool-HASR, Judge-ASR), not to Delta. Derived from locked counts.

## 11. Statistical Analysis

### Tests used

| Test | Status | Evidence |
| --- | --- | --- |
| Sign agreement (9 contrasts) | VERIFIED | `q2_final_statistics.json` |
| Wilson 95% CI | VERIFIED (on rates) | `q2_final_statistics.json` |
| McNemar | NOT USED | `MANUSCRIPT_FINAL.md` ("not preregistered") |
| p-values | NOT USED | `MANUSCRIPT_FINAL.md` (none reported) |

### Q2 results

| ID | Experiment | Metric | Value | N | Evidence | Status |
| --- | --- | --- | --- | - | --- | --- |
| Q2-001 | Q2 live | Tool-HASR (T1-T3) | 81/192 = 0.421875 | 192 | `metrics.json` | CONFIRMED |
| Q2-002 | Q2 live | Judge-ASR (T1-T3) | 186/192 = 0.96875 | 192 | `metrics.json` | CONFIRMED |
| Q2-003 | Q2 live | M3 (T1-T3) | 108 | 192 | `metrics.json` | CONFIRMED |
| Q2-004 | Q2 live | M4 (T1-T3) | 3 | 192 | `metrics.json` | CONFIRMED |
| Q2-005 | Q2 live | INVALID_TOOL_ARGS | 192 events / 136 arms | 432 | `metrics.json` | CONFIRMED |
| Q2-006 | Q2 live | Sign agreement | 9/9 | 9 | `q2_final_statistics.json` | CONFIRMED |

### Delta values (all NEG)

| Target | D1 | D2 | D4 | Signs |
| --- | ---: | ---: | ---: | --- |
| T0 | -0.6875 | -0.2500 | -0.5625 | NEG, NEG, NEG |
| T1 | -0.7500 | -0.3125 | -0.6250 | NEG, NEG, NEG |
| T2 | -0.6875 | -0.2500 | -0.5625 | NEG, NEG, NEG |
| T3 | -0.5625 | -0.1875 | -0.5000 | NEG, NEG, NEG |

## 12. Results Ledger

| ID | Experiment | Metric | Value | N | Evidence | Status |
| --- | ---------- | ------ | ----- | - | -------- | ------ |
| R-001 | Q2 live | 432/432 arms | 432 | 432 | `metrics.json` | CONFIRMED |
| R-002 | Q2 live | API calls | 2061 | - | `spend.json` | CONFIRMED |
| R-003 | Q2 live | Actual cost | $0.152885 | - | `spend.json` | CONFIRMED |
| R-004 | Q2 live | Tool-HASR (T1-T3) | 81/192 | 192 | `metrics.json` | CONFIRMED |
| R-005 | Q2 live | Judge-ASR (T1-T3) | 186/192 | 192 | `metrics.json` | CONFIRMED |
| R-006 | Q2 live | M3 | 108 | 192 | `metrics.json` | CONFIRMED |
| R-007 | Q2 live | M4 | 3 | 192 | `metrics.json` | CONFIRMED |
| R-008 | Q2 live | INVALID_TOOL_ARGS | 192 events / 136 arms | 432 | `metrics.json` | CONFIRMED |
| R-009 | Q2 live | Sign agreement | 9/9 | 9 | `q2_final_statistics.json` | CONFIRMED |

## 13. Evidence Hierarchy

1. **Frozen official evaluation artifact** -- `metrics.json`, `predictions.jsonl` (Q2)
2. **Reproducible experiment output** -- `q2_final_statistics.json` (derived from Q2 traces)
3. **Versioned result file** -- `spend.json` (Q2 cost)
4. **Diagnostic experiment** -- `p3_q2_forensic_audit.json` (integrity check)
5. **Historical experiment** -- Stage-B AUDIT (Track A), Phase-1 AUDIT (Track B)
6. **Manual observation** -- manuscript observations
7. **Hypothesis/illustration** -- pilot-scale framing

## 14. Track Separation

| Track | Pack | Treatment | Result | Status |
| --- | --- | --- | --- | --- |
| A | `vnext_confirm_v1.0` | B0 vs VNEXT-ADAPT | delta_hat=0.0820 (MSID not met) | FAIL (immutable) |
| B | `phase1_confirm_v1` | B0 vs PHASE1-CORE | delta_hat=0.4426 (MSID met) | SUPPORTED_IMPROVEMENT (scoped) |
| Q2 | `p2_agentic_v0.1.0` | D0/D1/D2/D4 under PHASE1-CORE | 9/9 sign agreement | CONFIRMED (pilot-scale) |

**Track A does NOT reverse Track B. Track B does NOT reverse Track A. Q2 must not be pooled with either track.

## 15. Reproducibility

### Frozen evidence

| Artifact | SHA-256 | Status |
| --- | --- | --- |
| P1 pack | `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` | VERIFIED |
| P2 pack | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` | VERIFIED |
| Q2 predictions | `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6` | VERIFIED |

### Run configuration

| Field | Value | Evidence |
| --- | --- | --- |
| Run ID | `p3_stage_c_q2_20260917T123855Z_b075df0f` | `manifest.json` |
| Evidence commit | `b075df0f5ec5ad11ede76ac4e4079cade15208f1` | `manifest.json` |
| Backend | OpenRouter | `manifest.json` |
| Temperature | 0.0 | `manifest.json` |
| Cache | false | `manifest.json` |
| Seed | 42 | `manifest.json` |
| Judge | `qwen/qwen-2.5-72b-instruct` | `manifest.json` |
| Targets | T0-T3 (see §16) | `manifest.json` |
| Budget cap | $10.0 | `manifest.json` |
| Actual cost | $0.152885 | `spend.json` |
| API calls | 2061 | `spend.json` |
| scientific_evidence | false | `manifest.json` |

### Stage-B provenance

| Field | Status | Evidence |
| --- | --- | --- |
| Stage-B run ID | `p3_stage_b_20260916T235438Z_7e401714` | `manifest.json` (t0_reuse_run_id) |
| Stage-B predictions SHA | `7b0b72d942dae988d87acf238424c9f2d331b62d5ec582c9ba7d9bfbb293c214` | `STAGE_B_EVIDENCE_STATUS.json` (pointer only) |
| Stage-B raw traces | **MISSING_LOCALLY** | `STAGE_B_EVIDENCE_STATUS.md` |
| Q2 rerun | false | `manifest.json` (t0_rerun=false) |

`REPRODUCIBILITY_STATUS = PARTIAL`. Full reproducibility is not claimed while Stage-B raw traces remain missing.

## 16. Limitations

1. n=16 per cell; Wilson CIs are wide (2/16 Tool-HASR CI [0.035, 0.360]); limited precision; limited power for broad generalization
2. Pilot-scale study; internal flag `scientific_evidence=false`; not confirmatory; directional consistency is an observed property of this evaluation
3. Four target models only; does not establish population-level generalization
4. Qwen-heavy target set: T0=`qwen/qwen-2.5-7b-instruct`, T1=`qwen/qwen3-30b-a3b`, T2=`google/gemma-3-27b-it`, T3=`qwen/qwen3.5-35b-a3b`; judge=`qwen/qwen-2.5-72b-instruct`
5. Three of four targets are Qwen-family; model-family diversity is limited; results should not be generalized to arbitrary model families
6. D3 deferred because the planned semantic-embedding dependency was not part of the locked offline protocol; no D3 scores
7. The present study does not establish robustness against open-ended adaptive attackers, C4 interaction horizon, or attacker adaptation against the detector-policy system
8. INVALID_TOOL_ARGS frequency (192 events / 136 arms on Q2 live); canonical execution state; potential confounder for Tool-HASR observability and Tool-HASR/Judge-ASR disagreement; not discarded; not claimed to explain all metric disagreement
9. Stage-B raw traces unavailable in the current checkout (`MISSING_LOCALLY`); official Stage-B reported T0 reuse is distinct from independent raw-trace recomputation; no reconstruction
10. No matched external defense baseline; attribution scope, not comparative ranking of defenses
11. No ranking versus published systems
12. Target-model behavior can influence observed tool execution and judge outcomes
13. Judge/tool disagreement (T1-T3 M3=108, M4=3); endpoints are non-identical
14. Results are protocol-specific (PHASE1-CORE, frozen P2, mock tools, short horizon, one judge)
15. Provider/runtime and tool-call formatting effects
16. Refusal is not credited as a defense win
17. Exact literature gap cannot be claimed globally (PARTIAL_GAP)
18. Observed Delta vs D0 is a detector-related association under the controlled protocol; it does not establish detector causality in isolation
19. Bibliography venue/DOI mostly UNVERIFIED; camera-ready citations incomplete

## 17. Claims Checklist

| Claim | Status | Evidence | Safe wording | Unsafe wording |
| --- | --- | --- | --- | --- |
| C00: Detector-related Tool-HASR Delta vs D0 directionally consistent across T0-T3 (9/9) | PARTIALLY_SUPPORTED / PILOT-SCALE | `q2_final_statistics.json` | "observed Delta direction remained consistent"; "9/9 directional agreements" | "confirmatory"; "definitive"; "generalizable"; "universal"; "proves"; "causal"; "SOTA"; "best" |
| C10: Pilot-scale directional consistency | PARTIALLY_SUPPORTED / PILOT-SCALE | Observed property of this evaluation | "pilot-scale directional consistency" | "confirmatory"; "population-level generalization" |
| C25: SOTA/best/superior/guaranteed/production-ready | NOT_ESTABLISHED | Forbidden in manuscript | -- | "SOTA"; "best"; "superior"; "guaranteed"; "production-ready" |
| C26: Q2 confirmatory | NOT_ESTABLISHED | `scientific_evidence=false` | "directional consistency analysis" | "confirmatory"; "definitive" |
| C19: C4/adaptive attacker robustness | NOT_ESTABLISHED | Out of scope | "out of scope" | "robust to adaptive attackers" |
| C20: No matched external baseline | SUPPORTED (scope) | `BASELINE_GAP.md` | "external baselines outside primary claim" | "fair comparison to external defenses" |
| C28: Stage-B traces locally available | NOT_ESTABLISHED | `STAGE_B_EVIDENCE_STATUS.md` | "MISSING_LOCALLY" | "fully reproducible"; "all raw traces available" |

## 18. Citation Registry

| # | BibTeX key | Title | Authors | Year | Venue | DOI/arXiv | Used in | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | perez_ribeiro_2022 | Ignore Previous Prompt | Perez, Ribeiro | 2022 | NeurIPS 2022 ML Safety Workshop | arXiv:2211.09527 | S6.1 | VERIFIED |
| 2 | greshake_ipi_2023 | Not what you've signed up for | Greshake et al. | 2023 | ACM AISec 2023 | 10.1145/3605764.3623985 | S6.1 | VERIFIED |
| 3 | liu_houyi_2023 | Prompt Injection attack against LLM-integrated Applications | Liu, Deng et al. | 2023 | Preprint | arXiv:2306.05499 | S6.1 | VERIFIED (preprint) |
| 4 | ruan_toolemu_2023 | Identifying the Risks of LM Agents with an LM-Emulated Sandbox | Ruan et al. | 2023 | ICLR 2024 spotlight | arXiv:2309.15817 | S6.1 | VERIFIED |
| 5 | rebedea_nemo_2023 | NeMo Guardrails | Rebedea et al. | 2023 | EMNLP 2023 Demo | arXiv:2310.10501 | S6.1 | VERIFIED |
| 6 | liu_formalize_2023 | Formalizing and Benchmarking Prompt Injection Attacks and Defenses | Liu, Jia et al. | 2023 | USENIX Security 2024 | arXiv:2310.12815 | S6.1 | VERIFIED |
| 7 | toyer_tensortrust_2023 | Tensor Trust | Toyer et al. | 2023 | ICLR 2024 spotlight | arXiv:2311.01011 | S6.1 | VERIFIED |
| 8 | inan_llamaguard_2023 | Llama Guard | Inan et al. | 2023 | Preprint | arXiv:2312.06674 | S6.1 | VERIFIED (preprint) |
| 9 | yi_bipia_2023 | Benchmarking and Defending Against Indirect Prompt Injection Attacks | Yi et al. | 2023 | KDD 2025 | 10.1145/3690624.3709179 | S6.1 | VERIFIED |
| 10 | chen_struq_2024 | StruQ | Chen, Piet, Sitawarin, Wagner | 2024 | USENIX Security 2025 | arXiv:2402.06363 | S6.1 | VERIFIED |
| 11 | zhan_injecagent_2024 | InjecAgent | Zhan et al. | 2024 | ACL 2024 Findings | 10.18653/v1/2024.findings-acl.624 | S6.1 | VERIFIED |
| 12 | wu_isolategpt_2024 | IsolateGPT | Wu et al. | 2024 | NDSS 2025 | arXiv:2403.04960 | S6.1 | VERIFIED |
| 13 | hines_spotlighting_2024 | Defending Against IPI Attacks With Spotlighting | Hines et al. | 2024 | CAMLIS 2024 | arXiv:2403.14720 | S6.1 | VERIFIED |
| 14 | wallace_instruction_hierarchy_2024 | The Instruction Hierarchy | Wallace et al. | 2024 | ICLR 2025 | arXiv:2404.13208 | S6.1 | VERIFIED |
| 15 | debenedetti_agentdojo_2024 | AgentDojo | Debenedetti et al. | 2024 | NeurIPS 2024 | 10.52202/079017-2636 | S6.1 | VERIFIED |
| 16 | zhang_asb_2024 | Agent Security Bench | Zhang et al. | 2024 | ICLR 2025 | arXiv:2410.02644 | S6.1 | VERIFIED |
| 17 | andriushchenko_agentharm_2024 | AgentHarm | Andriushchenko et al. | 2024 | ICLR 2025 | arXiv:2410.09024 | S6.1 | VERIFIED |
| 18 | jacob_promptshield_2025 | PromptShield | Jacob et al. | 2025 | ACM CODASPY 2025 | arXiv:2501.15145 | S6.1 | VERIFIED |
| 19 | zhu_melon_2025 | MELON | Zhu et al. | 2025 | ICML 2025 | arXiv:2502.05174 | S6.1 | VERIFIED |
| 20 | debenedetti_camel_2025 | Defeating Prompt Injections by Design | Debenedetti et al. | 2025 | IEEE SaTML 2026 | arXiv:2503.18813 | S6.1 | VERIFIED |
| 21 | chen_meta_secalign_2025 | Meta SecAlign | Chen, Zharmagambetov, Wagner, Guo | 2025 | Preprint | arXiv:2507.02735 | S6.1 | VERIFIED (preprint) |

## 19. Figure Registry

| Figure | Title | Purpose | Source | Status |
| --- | --- | --- | --- | --- |
| FIG-1 | System architecture | Show pipeline: ContextBuilder -> Detector -> RiskCore -> CorePolicy -> ActionLayer -> ToolPermissionGate -> Tools -> Tool-HASR; Judge -> Judge-ASR | To be generated from REFERENCE | PLANNED |
| FIG-2 | Threat/attack taxonomy | Show attack families and paths | To be generated from REFERENCE | PLANNED |
| FIG-3 | Delta across targets | Show D1/D2/D4 Delta for T0-T3 | `figures/figure3_delta_across_targets.png` | EXISTS (VERIFIED) |
| FIG-4 | Tool-HASR vs Judge-ASR | Show dual metrics with M3/M4 | `figures/figure4_toolhasr_vs_judgeasr.png` | EXISTS (VERIFIED) |
| FIG-5 | INVALID_TOOL_ARGS diagnostic | Show 192/136 frequency | `figures/figure5_invalid_tool_args.png` | EXISTS (VERIFIED) |

## 20. Table Registry

| Table | Purpose | Source | Status |
| --- | --- | --- | --- |
| TAB-1 | Study design | `MANUSCRIPT_FINAL.md` S8 | EXISTS (VERIFIED) |
| TAB-2 | Target and judge models | `MANUSCRIPT_FINAL.md` S8 | EXISTS (VERIFIED) |
| TAB-3 | Primary Delta results | `MANUSCRIPT_FINAL.md` S9 | EXISTS (VERIFIED) |
| TAB-4 | Tool-HASR vs Judge-ASR | `MANUSCRIPT_FINAL.md` S10.1 | EXISTS (VERIFIED) |
| TAB-5 | INVALID_TOOL_ARGS diagnostics | `MANUSCRIPT_FINAL.md` S10.2 | EXISTS (VERIFIED) |
| TAB-6 | Threats and limitations | `MANUSCRIPT_FINAL.md` S12 | EXISTS (VERIFIED) |
