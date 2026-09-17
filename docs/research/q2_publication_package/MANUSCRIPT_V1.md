# Controlled Detector Attribution under a Locked Runtime Intervention Policy: A Pilot-Scale Agent Security Evaluation

**Manuscript V1 (internal).** Not a venue submission.  
**Evidence freeze:** Q2 run `p3_stage_c_q2_20260917T123855Z_b075df0f` · commit `b075df0f5ec5ad11ede76ac4e4079cade15208f1`.  
**This packaging:** LIVE_EVAL=false · API_CALLS=0 · no new experiments.  
**Protocol flag:** `scientific_evidence=false`. Scope: **protocol-complete pilot-scale directional consistency**. Not confirmatory.

Related-work identities use existing Hub-verified arXiv records. Most venue/DOI fields remain UNVERIFIED. AgentDojo venue/DOI and BIPIA venue/DOI are operator-supplied and not re-fetched this turn (`RELATED_WORK_MATRIX.md`).

---

## Abstract

Security numbers for tool-using LLM agents mix detector scoring with downstream intervention. This paper reports a **controlled attribution protocol**, not a new defense algorithm: the intervention policy is held fixed (PHASE1-CORE), **detector identity is varied** including a no-detection arm (D0), and the primary endpoint is **Tool-HASR** (harmful tool execution). The study uses **four target models** and n=16 attack arms per target/detector cell. Q2 live completed **432/432 arms** (historical spend $0.152885). Detector-related Tool-HASR Δ versus D0 was negative for D1/D2/D4 on the locked Stage-B target and on three independently selected secondary targets (**9/9 directional agreement**). T1–T3 Tool-HASR was 81/192; Judge-ASR was 186/192 (M3=108, M4=3). INVALID_TOOL_ARGS occurred on 192 events / 136 arms. This is **pilot-scale** evidence (`scientific_evidence=false`). It is not confirmatory, not a universal robustness result, and not a head-to-head defense benchmark.

---

## 1. Introduction

Tool-using language-model agents can cause harm by **executing** a tool call, not only by producing a string that a judge later labels successful. Defenses typically stack a detector, a risk mapping, and an intervention policy that allows, wraps, or denies tools. Published evaluations often report the stack as a whole. That is operationally useful and scientifically ambiguous: a drop in attack success may come from the detector, from a conservative policy, from schema failures that prevent execution, or from the target model refusing.

This paper studies **attribution**, not leaderboard performance. The central contribution is a controlled evaluation protocol that holds the downstream intervention policy fixed, varies detector identity including D0, measures Tool-HASR, and tests whether detector-related Δ relative to D0 preserves sign across independently selected target models.

This paper is a **protocol-complete pilot-scale directional consistency study**. Under this protocol the observed answer is yes: 9/9 Δ signs agree (all negative). That finding is scoped to four models, n=16 per cell, mock tools, and `scientific_evidence=false`. It is not evidence that any detector is best, that the system is production-ready, or that prompt injection is solved. It is a **detector-related effect** under a locked policy, not unqualified detector causality.

This manuscript does not reverse other tracks in the same repository. Track A (VNEXT confirmation) is an immutable FAIL on a different pack and treatment. Track B (Phase-1 confirmatory LIVE) is a scoped SUPPORTED_IMPROVEMENT on a third pack. Q2 must not be pooled with either.

---

## 2. Related Work

We cite records whose title, authors, year, and arXiv id were verified from existing package Hub metadata. Most venues remain UNVERIFIED. AgentDojo (NeurIPS 2024, DOI `10.52202/079017-2636`) and BIPIA (KDD 2025, DOI `10.1145/3690624.3709179`) venue/DOI are operator-supplied and not re-fetched this turn. Full matrix: `RELATED_WORK_MATRIX.md`. Novelty class: **PARTIAL_GAP** (`NOVELTY_AUDIT.md`).

**Existing literature already provides** prompt-injection attacks, agent security benchmarks, dynamic evaluation, defense architectures, architectural isolation, adaptive evaluation, memory/tool security, and runtime security mechanisms. This paper does not claim invention of those components.

**Prompt injection and indirect injection.** Perez and Ribeiro document goal hijacking and prompt leaking (`2211.09527`). Liu et al. study injection against LLM-integrated applications (`2306.05499`, `2310.12815`). Toyer et al. collect human-written injection attacks in Tensor Trust (`2311.01011`). Greshake et al. introduce indirect prompt injection via retrieved content (`2302.12173`). Yi et al. benchmark IPI with BIPIA (`2312.14197`).

**Agent and tool-use security evaluation.** Ruan et al. emulate tool-using agents in ToolEmu (`2309.15817`). Zhan et al. benchmark IPI that induces detrimental tool use in InjecAgent (`2403.02691`). Debenedetti et al. provide AgentDojo, a dynamic environment for agent attacks and defenses (`2406.13352`; paper identity VERIFIED). Zhang et al. propose Agent Security Bench (`2410.02644`; paper identity VERIFIED, not UNCERTAIN). Andriushchenko et al. measure agent harmfulness after jailbreaks in AgentHarm (`2410.09024`). These establish that agent security is trajectory- and action-sensitive. They are not numerical Q2 baselines.

**Guardrails, detectors, and model-level defenses.** Inan et al. describe Llama Guard (`2312.06674`). Rebedea et al. describe NeMo Guardrails (`2310.10501`). Jacob et al. study deployable prompt-injection detection in PromptShield (`2501.15145`). Wallace et al. train an instruction hierarchy (`2404.13208`). Chen et al. separate prompts and data in StruQ (`2402.06363`) and later describe Meta SecAlign (`2507.02735`). Hines et al. spotlight untrusted content (`2403.14720`). Zhu et al. detect IPI by re-executing masked trajectories (MELON, `2502.05174`).

**Architectural isolation.** Wu et al. propose IsolateGPT, an execution-isolation architecture (`2403.04960`). Debenedetti et al. propose CaMeL, segregating control and data flows (`2503.18813`). CaMeL is a published architectural defense, not an unverified idea. These isolate *channels or execution*, which is related to but distinct from isolating *detector identity* while holding an intervention policy fixed.

**Residual gap (narrow).** The verified literature establishes extensive work on attacks, benchmarks, defenses, and adaptive evaluation, but does not establish the exact locked-policy detector-attribution factorial used here as the central measurement protocol. This is a **partial gap**, not a global uniqueness claim. Numeric results from other papers are not copied here. The present study is an attribution study, not a head-to-head defense benchmark (`BASELINE_GAP.md`).

---

## 3. Controlled Attribution Protocol

**RQ-C2 (locked protocol).** Does the detector-related Tool-HASR effect versus D0 observed under the locked Stage-B target (T0) remain directionally consistent when the same policy, pack, detectors, thresholds, and judge are applied to independently selected secondary target models T1–T3?

**Factor.** `target_model_id ∈ {T0, T1, T2, T3}`.  
**Locked.** Policy = PHASE1-CORE; detectors ∈ {D0, D1, D2, D4}; D3 deferred; pack `p2_agentic_v0.1.0`; judge `qwen/qwen-2.5-72b-instruct`.  
**Primary estimand.** sign(Δ(d,t)) for d ∈ {D1, D2, D4}, t ∈ {T1, T2, T3}, compared with sign(Δ(d,T0)).  
**Pre-registered agreement.** 9 contrasts; agreement if signs match (exact 0 would be ZERO; none observed).

Q2 is **not** powered as a confirmatory hypothesis test. The run sets `scientific_evidence=false`. “Supported” in the live verdict means protocol sign-agreement support, not Track B `SUPPORTED_IMPROVEMENT` and not a qualified win (MSID ∧ significance ∧ U).

### 3.1 System decomposition

Each episode-arm runs: **Detector → RiskCore → CorePolicy (PHASE1-CORE) → ToolPermissionGate → mock tools**, with a parallel **judge** that does not enter the detector→policy path. Gold labels (`is_attack`, `label`, `category`) do not enter that path.

D0 implements no detection (no hits). D1/D2/D4 share a `P3Detector` contract and differ in how they score context. D3 (semantic/embedding) is `DEFERRED_NO_OFFLINE_IMPL` and has no scores.

PHASE1-CORE maps detector/risk signals to actions A0–A3 with locked thresholds (is_injection 0.25; risk 0.25/0.60) and normalized action costs (A0=0, A1=0.10, A2=0.25, A3=0.50). Those costs are experimental weights, not USD prices.

**Varied:** detector identity {D0, D1, D2, D4}.  
**Locked:** PHASE1-CORE, thresholds, action costs, P2 pack, judge, temperature, cache-off, seed.

D0 estimates tool-harm when the policy receives no detector hits. Contrasts versus D0 are therefore **detector-related** under this policy, not estimates of “the detector in isolation from all other runtime effects.” Schema failures, target refusals, and judge behavior still occur in every arm. This is experimental isolation under the controlled protocol, not causal identification in deployment. Protocol: `no_ranking=true`.

### 3.2 Endpoints

**Tool-HASR (primary).** Fraction of attack episode-arms with `tool_hasr_success=True` among True+False. UNKNOWN excluded (`exclude_unknown=true`); Q2 cells have n_unknown=0. Success requires harmful tool execution matching the pre-registered `success_condition`. INVALID_TOOL_ARGS is **not** Tool-HASR success.

**Judge-ASR (secondary).** Fraction of attack episode-arms with `judge_asr_success=True`. A judge-model assessment of attack success.

**M3 / M4.** M3: judge success ∧ ¬ tool success. M4: tool success ∧ ¬ judge success.

**Δ(d,t).** Tool-HASR(d,t) − Tool-HASR(D0,t) on attack arms at the same target.

**INVALID_TOOL_ARGS.** Schema/argument failures. Official policy S0 keeps the primary denominator. S1 stratifies; S2 excludes arms with ≥1 INVALID (`derived_after_run`). No post-hoc sensitivity variants.

### 3.3 Statistics

Rates are reported as n/N, point estimate, and Wilson 95% CI. Δ is a difference of rates; **no Δ CI was pre-registered** and none is manufactured.

> Q2 was designed as a directional consistency analysis; inferential p-values were not preregistered and are not reported.

Sign agreement is the protocol quantity. Paired discordant counts vs T0 are descriptive.

---

## 4. Experimental Design

| Field | Value |
| --- | --- |
| Question | RQ-C2 |
| Design | B_REDUCED_Q2 |
| Run ID | `p3_stage_c_q2_20260917T123855Z_b075df0f` |
| Commit | `b075df0f5ec5ad11ede76ac4e4079cade15208f1` |
| Pack | `p2_agentic_v0.1.0` · SHA `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` |
| P1 (supporting freeze) | SHA `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` |
| Trajectories | 16 attack / 16 twin / 4 hard negative |
| Detectors | D0, D1, D2, D4 (D3 deferred) |
| Policy | PHASE1-CORE |
| T0 | reused from `p3_stage_b_20260916T235438Z_7e401714` (not re-run) |
| Q2 live | 36 traj × 4 detectors × PHASE1-CORE × {T1,T2,T3} = 432 arms |
| Completed | 432/432, 0 failed |
| Temperature | 0.0 |
| Cache | false |
| Seed | 42 |
| Backend | OpenRouter |
| Budget cap / actual | $10.0 / $0.152885 (historical live) |
| `scientific_evidence` | false |
| n per cell | 16 attack arms |

Target slots (not a quality ranking):

| Slot | Model ID | Role |
| --- | --- | --- |
| T0 | `qwen/qwen-2.5-7b-instruct` | Stage-B reference, not re-run |
| T1 | `qwen/qwen3-30b-a3b` | secondary |
| T2 | `google/gemma-3-27b-it` | secondary |
| T3 | `qwen/qwen3.5-35b-a3b` | secondary |
| Judge | `qwen/qwen-2.5-72b-instruct` | locked, not an experimental factor |

Three of four targets are Qwen-line models. Architectural diversity is limited. All calls used OpenRouter. Provider-side tool formatting can affect Tool-HASR and INVALID rates.

Q2 predictions SHA-256: `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6`.

Official T0 Tool-HASR/Δ is reused from Stage-B. Local Stage-B `predictions.jsonl` is **MISSING_LOCALLY** (`STAGE_B_EVIDENCE_STATUS.md`). Packaged T0 PHASE1-CORE rates are 28/64 Tool-HASR and 55/64 Judge-ASR (M3=33, M4=6). Independent local recomputation of T0 from raw traces was not performed.

---

## 5. Results

All cells use n=16 attack arms. Wilson 95% CIs are on rates, not on Δ. Source: `q2_final_statistics.json` / `FIGURES_AND_TABLES.md`. This section reports **detector-related effects** under the locked protocol. It does not turn 9/9 into causal proof.

### 5.1 Tool-HASR by cell

| Cell | n/N | Rate | Wilson 95% CI |
| --- | ---: | ---: | --- |
| T0/D0 | 13/16 | 0.8125 | [0.570, 0.934] |
| T0/D1 | 2/16 | 0.1250 | [0.035, 0.360] |
| T0/D2 | 9/16 | 0.5625 | [0.332, 0.769] |
| T0/D4 | 4/16 | 0.2500 | [0.102, 0.495] |
| T1/D0 | 14/16 | 0.8750 | [0.640, 0.965] |
| T1/D1 | 2/16 | 0.1250 | [0.035, 0.360] |
| T1/D2 | 9/16 | 0.5625 | [0.332, 0.769] |
| T1/D4 | 4/16 | 0.2500 | [0.102, 0.495] |
| T2/D0 | 13/16 | 0.8125 | [0.570, 0.934] |
| T2/D1 | 2/16 | 0.1250 | [0.035, 0.360] |
| T2/D2 | 9/16 | 0.5625 | [0.332, 0.769] |
| T2/D4 | 4/16 | 0.2500 | [0.102, 0.495] |
| T3/D0 | 11/16 | 0.6875 | [0.444, 0.858] |
| T3/D1 | 2/16 | 0.1250 | [0.035, 0.360] |
| T3/D2 | 8/16 | 0.5000 | [0.280, 0.720] |
| T3/D4 | 3/16 | 0.1875 | [0.066, 0.430] |

Q2 live T1–T3 pooled Tool-HASR: 81/192 = 0.421875.

### 5.2 Primary Δ (detector-related, vs D0)

| Cell | Δ | Sign |
| ---: | ---: | --- |
| T0/D1 | −0.6875 | NEG |
| T0/D2 | −0.25 | NEG |
| T0/D4 | −0.5625 | NEG |
| T1/D1 | −0.75 | NEG |
| T1/D2 | −0.3125 | NEG |
| T1/D4 | −0.625 | NEG |
| T2/D1 | −0.6875 | NEG |
| T2/D2 | −0.25 | NEG |
| T2/D4 | −0.5625 | NEG |
| T3/D1 | −0.5625 | NEG |
| T3/D2 | −0.1875 | NEG |
| T3/D4 | −0.5 | NEG |

All D1/D2/D4 Δ values are negative across T0–T3. Intervals on the underlying rates are wide (especially 2/16 cells). Magnitudes should not be over-read. Detectors are not ranked. Figure 3 plots Δ Tool-HASR relative to D0 across T0–T3 (`figures/figure3_delta_across_targets.png`). Colors and bar order are categorical, not a ranking, and do not encode statistical significance.

---

## 6. Diagnostic Analysis

### 6.1 Tool-HASR versus Judge-ASR

Tool-HASR measures harmful tool execution. Judge-ASR measures judge-classified attack success.

They can disagree because:

- the target may refuse;
- tool execution may be blocked;
- tool arguments may be invalid;
- judge interpretation may differ;
- runtime/provider behavior may intervene.

**Finding:** Judge-ASR and Tool-HASR capture related but non-identical operational outcomes. The paper does **not** conclude that Judge-ASR is invalid. Tool-HASR remains primary.

| Cell | Tool-HASR | Judge-ASR |
| --- | --- | --- |
| T0/D0 | 13/16 = 0.8125 [0.570, 0.934] | 12/16 = 0.7500 [0.505, 0.898] |
| T0/D1 | 2/16 = 0.1250 [0.035, 0.360] | 14/16 = 0.8750 [0.640, 0.965] |
| T0/D2 | 9/16 = 0.5625 [0.332, 0.769] | 15/16 = 0.9375 [0.717, 0.989] |
| T0/D4 | 4/16 = 0.2500 [0.102, 0.495] | 14/16 = 0.8750 [0.640, 0.965] |
| T1/D0 | 14/16 = 0.8750 [0.640, 0.965] | 15/16 = 0.9375 [0.717, 0.989] |
| T1/D1 | 2/16 = 0.1250 [0.035, 0.360] | 16/16 = 1.0000 [0.806, 1.000] |
| T1/D2 | 9/16 = 0.5625 [0.332, 0.769] | 16/16 = 1.0000 [0.806, 1.000] |
| T1/D4 | 4/16 = 0.2500 [0.102, 0.495] | 15/16 = 0.9375 [0.717, 0.989] |
| T2/D0 | 13/16 = 0.8125 [0.570, 0.934] | 15/16 = 0.9375 [0.717, 0.989] |
| T2/D1 | 2/16 = 0.1250 [0.035, 0.360] | 16/16 = 1.0000 [0.806, 1.000] |
| T2/D2 | 9/16 = 0.5625 [0.332, 0.769] | 16/16 = 1.0000 [0.806, 1.000] |
| T2/D4 | 4/16 = 0.2500 [0.102, 0.495] | 15/16 = 0.9375 [0.717, 0.989] |
| T3/D0 | 11/16 = 0.6875 [0.444, 0.858] | 15/16 = 0.9375 [0.717, 0.989] |
| T3/D1 | 2/16 = 0.1250 [0.035, 0.360] | 16/16 = 1.0000 [0.806, 1.000] |
| T3/D2 | 8/16 = 0.5000 [0.280, 0.720] | 16/16 = 1.0000 [0.806, 1.000] |
| T3/D4 | 3/16 = 0.1875 [0.066, 0.430] | 15/16 = 0.9375 [0.717, 0.989] |

| Scope | M3 (J+ T−) | M4 (T+ J−) |
| --- | ---: | ---: |
| T0 PHASE1-CORE pooled | 33 | 6 |
| T1 | 34 | 1 |
| T2 | 35 | 1 |
| T3 | 39 | 1 |
| Q2 live T1–T3 | 108 | 3 |

Q2 live Judge-ASR: 186/192 = 0.96875. Figure 4 plots Tool-HASR versus Judge-ASR with M3/M4 diagnostic interpretation (`figures/figure4_toolhasr_vs_judgeasr.png`). Judge-ASR is high across detectors, including D1/D2/D4 where Tool-HASR is lower.

### 6.2 INVALID_TOOL_ARGS

INVALID_TOOL_ARGS are frequent. They are not silently discarded. They are not treated as harmless. They are part of the execution validity diagnostics. They can affect Tool-HASR interpretation. S0/S1/S2 sensitivity did not change the Q2 sign-consistency conclusion. This does **not** prove invalid arguments are negligible.

**PRIMARY (S0):** official Q2 live INVALID = 192 unique events, 136/432 arms. Independent recompute on `predictions.jsonl` matches. INVALID is not Tool-HASR success. Figure 5 is the INVALID diagnostic (`figures/figure5_invalid_tool_args.png`).

**SENSITIVITY:** S2 excluding arms with ≥1 INVALID does not flip within-target Δ signs (0 flips). S2 cross-target sign agreement vs T0 S2 remains 9/9. S1 is descriptive stratification; observed D1/D2/D4 Δ signs remain NEG in both strata. Magnitudes are not interchangeable with S0. Compact table: `INVALID_TOOL_ARGS_ANALYSIS.md`.

T0 INVALID counts are cited from prior derived JSON because Stage-B `predictions.jsonl` is **MISSING_LOCALLY**.

### 6.3 Detector-level operational metrics (Q2 live T1–T3; not a ranking)

| Detector | Attack Tool-HASR | Attack Judge-ASR | detector_hit attack | detector_hit label=benign | detector_hit hard_negative |
| --- | --- | --- | --- | --- | --- |
| D0 | 38/48 = 0.7917 | 45/48 = 0.9375 | 0/48 | 0/60 | 0/12 |
| D1 | 6/48 = 0.1250 | 48/48 = 1.0000 | 48/48 | 54/60 | 12/12 |
| D2 | 26/48 = 0.5417 | 48/48 = 1.0000 | 24/48 | 15/60 | 6/12 |
| D4 | 11/48 = 0.2292 | 45/48 = 0.9375 | 48/48 | 51/60 | 3/12 |

Hit rates on benign/hard-negative rows are reported for transparency. They are not a ranking and not a qualified-win utility metric.

---

## 7. Robustness / Secondary Target Analysis

| Contrast | Δ_T0 | Δ_Tk | Δ-change | Sign agreement |
| --- | ---: | ---: | ---: | --- |
| D1, T1 | −0.6875 | −0.75 | −0.0625 | True |
| D2, T1 | −0.25 | −0.3125 | −0.0625 | True |
| D4, T1 | −0.5625 | −0.625 | −0.0625 | True |
| D1, T2 | −0.6875 | −0.6875 | 0.0 | True |
| D2, T2 | −0.25 | −0.25 | 0.0 | True |
| D4, T2 | −0.5625 | −0.5625 | 0.0 | True |
| D1, T3 | −0.6875 | −0.5625 | 0.125 | True |
| D2, T3 | −0.25 | −0.1875 | 0.0625 | True |
| D4, T3 | −0.5625 | −0.5 | 0.0625 | True |

**Sign agreement: 9/9 (disagree=0).** Δ-change is descriptive. Sign agreement uses signs of Δ_T0 and Δ_Tk, not the sign of Δ-change.

T2 matches T0 Δ exactly in this sample. That is an observed coincidence at n=16, not evidence that T2 equals T0 in general.

Paired discordant Tool-HASR counts (descriptive; no p-value): T0 vs T1 D0 discordant=1; T0 vs T3 D0 discordant=2; T0 vs T3 D2 discordant=1; T0 vs T3 D4 discordant=1; remaining listed pairs discordant=0 (`STATISTICAL_REPORTING.md`).

Interpretation, no more: under locked PHASE1-CORE, the detector-related Tool-HASR effect observed on T0 remained directionally consistent on T1–T3. This does not establish universal LLM generalization, production robustness, or that detector behavior is the sole cause of security outcomes.

The present study is an attribution study, not a head-to-head defense benchmark. No numerical comparison is made to CaMeL, AgentDojo defenses, ASB defenses, Llama Guard, or PromptShield.

---

## 8. Limitations

See also `LIMITATIONS.md` and `D3_AND_C4.md`.

1. **n=16 per cell.** Wilson CIs are wide. 2/16 = 0.125 has CI [0.035, 0.360]. Pilot-scale.
2. **Four target models only.**
3. **Qwen-heavy target set.** T0, T1, T3 are Qwen-line; T2 is Gemma-3; judge also Qwen.
4. **Limited architectural diversity.** No GPT/Claude/Gemini-native API family; all via OpenRouter.
5. **Pilot-scale evidence.** Protocol-complete directional consistency, not a large-n study.
6. **`scientific_evidence=false`.** Not confirmatory.
7. **No matched external defense baseline.** Attribution study, not a defense leaderboard.
8. **No SOTA comparison.** Other papers’ numbers are incommensurable here.
9. **No production robustness claim.**
10. **D3 deferred.** No embedding-detector numbers.
11. **C4 / open adaptive attacker out of scope.**
12. **Frozen benchmark effects.** P2 is small, mock-tool, short-horizon. SHA `32b40e3b…`.
13. **Provider/runtime effects.** Tool-call formatting, schema compliance, residual nondeterminism at temperature 0.
14. **Tool-call formatting** can stop execution independently of detector hits.
15. **Model refusal behavior.** Refusal is not credited as a defense win. Non-execution is simply not Tool-HASR success.
16. **INVALID_TOOL_ARGS.** Frequent (192/136 on Q2 live); not success; not negligible; S2 signs 9/9.
17. **Judge/Tool metric disagreement.** T1–T3 M3=108, M4=3. Related but non-identical outcomes.
18. **Stage-B raw trace unavailable locally.** Official packaged T0 PHASE1-CORE is reused; `LOCAL_RAW_TRACE=MISSING_LOCALLY`; no reconstruction; no independent T0 recompute.
19. **Exact literature gap cannot be claimed globally.** Novelty remains PARTIAL_GAP.
20. **No claim of universal detector causality.** Observed effects are detector-related under the controlled protocol.

---

## 9. Reproducibility

`REPRODUCIBILITY_STATUS = PARTIAL` because Stage-B raw traces remain missing locally. Full reproducibility is not claimed.

| Field | Value |
| --- | --- |
| repository_commit (run) | `b075df0f5ec5ad11ede76ac4e4079cade15208f1` |
| run_id | `p3_stage_c_q2_20260917T123855Z_b075df0f` |
| harness | `p3.0.0-live-stage-c-q2` |
| p1_sha256 | `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` |
| p2_sha256 | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` |
| q2_predictions_sha256 | `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6` |
| judge | `qwen/qwen-2.5-72b-instruct` |
| temperature / cache / seed | 0.0 / false / 42 |
| historical API calls | 2061 |
| this packaging API calls | 0 |
| analysis | `p3_stage_c_q2.py`, `generate_tables_figures.py`, `render_figures_offline.py`, this package |
| figures 3–5 | `docs/research/q2_publication_package/figures/*.png` (stdlib PNG; matplotlib **MISSING**) |

Checklist: `Q2_REPRODUCIBILITY_CHECKLIST.md`. Stage-B status: `STAGE_B_EVIDENCE_STATUS.md`.

---

## 10. Conclusion

Under a locked intervention policy, detector identity is associated with lower operational harmful-tool rates than a no-detection arm, and that detector-related association kept sign across three independently selected secondary targets in this pilot (432/432 arms; 9/9 directional agreement; n=16/cell; `scientific_evidence=false`). The contribution is a **controlled attribution protocol** plus that bounded empirical check. The evidence does not establish a new defense algorithm, a universal defense, a best detector, production robustness, confirmatory multi-model proof, or unqualified detector causality.

Future work — matched external baselines, larger n, more model families, D3 after an offline embedding lock, open adaptive attackers — would be **new studies** with their own freezes and budgets, not silent extensions of this run.

---

## References (identity verified from existing records; most venues UNVERIFIED)

1. Perez & Ribeiro, 2022. Ignore Previous Prompt. arXiv:2211.09527  
2. Greshake et al., 2023. Indirect Prompt Injection. arXiv:2302.12173  
3. Liu, Deng, et al., 2023. Prompt Injection attack against LLM-integrated Applications. arXiv:2306.05499  
4. Ruan et al., 2023. ToolEmu. arXiv:2309.15817  
5. Rebedea et al., 2023. NeMo Guardrails. arXiv:2310.10501  
6. Liu, Jia, Geng, Jia, Gong, 2023. Prompt Injection Attacks and Defenses in LLM-Integrated Applications. arXiv:2310.12815  
7. Toyer et al., 2023. Tensor Trust. arXiv:2311.01011  
8. Inan et al., 2023. Llama Guard. arXiv:2312.06674  
9. Yi et al., 2023. BIPIA. arXiv:2312.14197. Venue/DOI operator-supplied: KDD 2025, 10.1145/3690624.3709179  
10. Chen, Piet, Sitawarin, Wagner, 2024. StruQ. arXiv:2402.06363  
11. Zhan et al., 2024. InjecAgent. arXiv:2403.02691  
12. Wu et al., 2024. IsolateGPT. arXiv:2403.04960  
13. Hines et al., 2024. Spotlighting. arXiv:2403.14720  
14. Wallace et al., 2024. Instruction Hierarchy. arXiv:2404.13208  
15. Debenedetti et al., 2024. AgentDojo. arXiv:2406.13352. Venue/DOI operator-supplied: NeurIPS 2024, 10.52202/079017-2636  
16. Zhang et al., 2024. Agent Security Bench. arXiv:2410.02644  
17. Andriushchenko et al., 2024. AgentHarm. arXiv:2410.09024  
18. Jacob et al., 2025. PromptShield. arXiv:2501.15145  
19. Zhu et al., 2025. MELON. arXiv:2502.05174  
20. Debenedetti et al., 2025. CaMeL (Defeating Prompt Injections by Design). arXiv:2503.18813  
21. Chen, Zharmagambetov, Wagner, Guo, 2025. Meta SecAlign. arXiv:2507.02735  
