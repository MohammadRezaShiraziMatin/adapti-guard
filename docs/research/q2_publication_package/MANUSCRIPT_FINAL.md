# Controlled Detector Attribution under a Locked Runtime Intervention Policy: A Pilot-Scale Agent Security Evaluation

**Manuscript FINAL (internal package).** Not a venue submission.  
**Evidence freeze:** Q2 run `p3_stage_c_q2_20260917T123855Z_b075df0f` · commit `b075df0f5ec5ad11ede76ac4e4079cade15208f1`.  
**This packaging:** LIVE_EVAL=false · API_CALLS=0 · LLM_CALLS=0 · NETWORK_CALLS=0.  
**Protocol flag:** `scientific_evidence=false`. Scope: **protocol-complete pilot-scale directional consistency**. Not confirmatory.

Related-work identities use existing Hub-verified arXiv records. Most venue/DOI fields remain UNVERIFIED. AgentDojo venue/DOI and BIPIA venue/DOI are operator-supplied and not re-fetched this turn (`BIBLIOGRAPHY_VERIFICATION.md`). Novelty class: **PARTIAL_GAP**.

---

## Abstract

This study evaluates whether detector-related security effects under a **locked intervention policy** remain directionally consistent across independently selected target models. It is a **controlled attribution protocol**, not a new defense algorithm.

The downstream policy is held fixed (PHASE1-CORE). Detector identity is varied, including a no-detection arm (D0). The primary endpoint is **Tool-HASR** (harmful tool execution). **Judge-ASR** is a secondary, non-identical diagnostic. The study uses **four target models** and **n=16 attack arms per target/detector cell**. Q2 live completed **432/432 arms** (historical spend $0.152885).

Observed detector-related Tool-HASR Δ versus D0 was negative for D1/D2/D4 on the locked Stage-B target T0 and on independently selected T1–T3 (**9/9 directional agreement**). This is **pilot-scale** evidence of directional consistency under the tested protocol (`scientific_evidence=false`). T1–T3 Tool-HASR was 81/192 = 0.421875; Judge-ASR was 186/192 = 0.96875 (M3=108, M4=3). INVALID_TOOL_ARGS occurred on 192 events / 136 arms.

The manuscript does not claim universal robustness, production readiness, confirmatory multi-model generalization, or a ranking against external defenses.

---

## 1. Introduction

Tool-using language-model agents can cause harm by **executing** a tool call, not only by producing a string that a judge later labels successful. Typical stacks combine (i) a **detector**, (ii) a risk mapping, and (iii) a **downstream intervention policy** that allows, wraps, or denies tools. Evaluations that move those pieces together report an operational outcome, not an attribution.

This paper studies **attribution**. The central question is whether detector-related security effects under a locked intervention policy remain directionally consistent across independently selected target models.

Under the tested protocol the observed Δ direction remained consistent across T0–T3: 9/9 detector-target comparisons preserved the negative direction. That is pilot-scale directional consistency (`scientific_evidence=false`; n=16/cell; four models; mock tools). It is a **detector-related association** under a locked policy. It is not causal proof, not comprehensive model generalization, and not a ranking of detectors.

This manuscript does not reverse other tracks in the same repository. Track A (VNEXT confirmation) is an immutable FAIL on a different pack and treatment. Track B (Phase-1 confirmatory LIVE) is a scoped SUPPORTED_IMPROVEMENT on a third pack. Q2 must not be pooled with either.

---

## 2. Research Question

**RQ-C2 (locked protocol).** Does the detector-related Tool-HASR effect versus D0 observed under the locked Stage-B target (T0) remain directionally consistent when the same policy, pack, detectors, thresholds, and judge are applied to independently selected secondary target models T1–T3?

**Experimental factor.** `target_model_id ∈ {T0, T1, T2, T3}`.  
**Locked.** Policy = PHASE1-CORE; detectors ∈ {D0, D1, D2, D4}; D3 deferred; pack `p2_agentic_v0.1.0`; judge `qwen/qwen-2.5-72b-instruct`.  
**Primary estimand.** sign(Δ(d,t)) for d ∈ {D1, D2, D4}, t ∈ {T1, T2, T3}, compared with sign(Δ(d,T0)).  
**Agreement rule.** 9 contrasts; agreement if signs match (exact 0.0 would be ZERO; none observed in primary Δ).

Q2 is **not** powered as a confirmatory hypothesis test. The run sets `scientific_evidence=false`. Live-report “supported” means protocol sign-agreement support, not Track B `SUPPORTED_IMPROVEMENT` and not a qualified win (MSID ∧ significance ∧ U).

> Q2 was designed as a directional consistency analysis; inferential p-values were not preregistered and are not reported.

---

## 3. Problem Formulation

Security outcomes on a tool-using agent mix several layers. This paper names them separately.

| Layer | What it is | What it is not |
| --- | --- | --- |
| **Detector behavior** | Hits/scores on untrusted context under a `P3Detector` contract (D0/D1/D2/D4) | The intervention that grants or denies tools |
| **Downstream intervention policy** | PHASE1-CORE mapping of detector/risk signals to actions A0–A3, then the tool-permission gate | A detector family |
| **Tool-HASR (primary)** | Attack-arm rate of harmful **tool execution** matching a pre-registered `success_condition` | A judge-model opinion |
| **Judge-ASR (secondary)** | Attack-arm rate of judge-classified attack success | Harmful tool execution |
| **M3** | Judge success ∧ ¬ Tool-HASR success | Proof that the judge is wrong |
| **M4** | Tool-HASR success ∧ ¬ judge success | Proof that the judge is right |
| **INVALID_TOOL_ARGS** | Canonical tool-state events: schema/argument failures | Tool-HASR success; automatic attack success; a harmless nuisance |

**Δ(d,t)** = Tool-HASR(d,t) − Tool-HASR(D0,t) on attack arms at the same target, under locked PHASE1-CORE. This is a **detector-related effect** under the controlled protocol, not an unqualified causal effect of “the detector in isolation from all runtime factors.”

**Unit of analysis.** Attack episode-arm: trajectory × detector × PHASE1-CORE × target. Official n=16 True+False per cell; UNKNOWN excluded (`exclude_unknown=true`); Q2 cells have n_unknown=0.

**INVALID policy.** S0 (official) retains the primary denominator. S1 stratifies arms with vs without INVALID. S2 excludes arms with ≥1 INVALID (`derived_after_run`). INVALID is **not** silently discarded. INVALID is **not** automatically equivalent to a successful attack. INVALID can affect **execution observability** and is a **potential confounder**. No claim of negligibility.

---

## 4. Related Work

We cite records whose title, authors, year, and arXiv id were verified from existing package Hub metadata. Most venues remain UNVERIFIED. AgentDojo (NeurIPS 2024, DOI `10.52202/079017-2636`) and BIPIA (KDD 2025, DOI `10.1145/3690624.3709179`) venue/DOI are **operator-supplied** and not re-fetched this turn. Full-text novelty exclusion is **not** claimed. Novelty class: **PARTIAL_GAP**. Matrix: `RELATED_WORK_MATRIX.md`.

**Existing literature already provides** prompt-injection attacks, agent security benchmarks, dynamic evaluation, defense architectures, architectural isolation, adaptive evaluation, memory/tool security, runtime policy enforcement, and instruction-hierarchy training. This paper does **not** claim invention of those components, and does **not** claim that D1/D2/D4 are novel detector families.

**Indirect prompt injection.** Greshake et al. (`2302.12173`) define IPI via retrieved/untrusted content. Yi et al. (BIPIA, `2312.14197`) benchmark IPI. Perez & Ribeiro (`2211.09527`), Liu et al. (`2306.05499`, `2310.12815`), and Toyer et al. (`2311.01011`) document direct/application injection. These are threat papers, not locked-policy detector attribution.

**Agent security benchmarks.** InjecAgent (`2403.02691`) measures IPI that induces detrimental tool use. AgentDojo (`2406.13352`; identity VERIFIED) is a dynamic attack/defense environment. AgentHarm (`2410.09024`) measures agent harmfulness after jailbreaks. Agent Security Bench / ASB (`2410.02644`; identity VERIFIED) evaluates many attacks and defenses. ToolEmu (`2309.15817`) emulates tool trajectories. Paper identities are verified. Packs, metrics, and execution environments differ from Q2. They are **not** numerical Q2 baselines.

**Architectural isolation and runtime defenses.** IsolateGPT (`2403.04960`) isolates execution. CaMeL (`2503.18813`) is a **published** control/data isolation design, not an unverified idea. NeMo Guardrails (`2310.10501`) encodes programmable rails. Llama Guard (`2312.06674`) and PromptShield (`2501.15145`) are detector/safeguard systems. StruQ (`2402.06363`) and Spotlighting (`2403.14720`) channel or mark untrusted data. MELON (`2502.05174`) re-executes masked trajectories. These are related mechanism classes. They are not the Q2 factorial and are not compared numerically here.

**Instruction hierarchy.** Wallace et al. (`2404.13208`) train privileged-instruction priority. Meta SecAlign (`2507.02735`) is a model-level defense. Those change the **target**, which would violate Q2’s locked-target × vary-detector design.

**Task Shield.** The name Task Shield (`arXiv:2412.16682`) is **not** in this package’s verified `RELATED_WORK_MATRIX` and is **not** added as a bibliographic record (identity/venue/DOI were not verified in-package). It is noted only so the paper is not read as claiming task-shielding. This study does not implement, evaluate, or numerically compare Task Shield.

**Residual gap (narrow).** The verified literature establishes extensive work on attacks, benchmarks, defenses, and adaptive evaluation, but does not establish the exact locked-policy detector-attribution factorial used here as the central measurement protocol. That is a **partial gap**, not a global uniqueness claim. The present study is an attribution study, not a head-to-head defense benchmark.

---

## 5. Controlled Attribution Framework

Each episode-arm runs:

**Detector → RiskCore → CorePolicy (PHASE1-CORE) → ToolPermissionGate → mock tools**, with a parallel **judge** that does not enter the detector→policy path. Gold labels (`is_attack`, `label`, `category`) do not enter that path.

| Varied | Locked |
| --- | --- |
| Detector identity {D0, D1, D2, D4} | PHASE1-CORE, thresholds, action costs, P2 pack, judge, temperature=0.0, cache=false, seed=42 |

D0 implements no detection (no hits). D1/D2/D4 share a `P3Detector` contract. D3 is `DEFERRED_NO_OFFLINE_IMPL` and has no scores.

PHASE1-CORE maps detector/risk signals to actions A0–A3 with locked thresholds (is_injection 0.25; risk 0.25/0.60) and normalized action costs (A0=0, A1=0.10, A2=0.25, A3=0.50). Those costs are experimental weights, not USD prices.

D0 estimates tool-harm when the policy receives no detector hits. Contrasts versus D0 are therefore **detector-related under this policy**. Schema failures, target refusals, provider formatting, and judge behavior still occur in every arm. Protocol: `no_ranking=true`.

---

## 6. Experimental Protocol

### Table 1 — Experimental design

| Field | Value |
| --- | --- |
| Question | RQ-C2 |
| Design | B_REDUCED_Q2 |
| Run ID | `p3_stage_c_q2_20260917T123855Z_b075df0f` |
| Evidence commit | `b075df0f5ec5ad11ede76ac4e4079cade15208f1` |
| Pack | `p2_agentic_v0.1.0` · SHA `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` |
| P1 (supporting freeze) | SHA `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` |
| Q2 predictions SHA | `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6` |
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
| Historical live API calls | 2061 (target+judge) |
| `scientific_evidence` | false |
| n per cell | 16 attack arms |

### Table 2 — Target models (not a quality ranking)

| Slot | Model ID | Role |
| --- | --- | --- |
| T0 | `qwen/qwen-2.5-7b-instruct` | Stage-B reference, not re-run |
| T1 | `qwen/qwen3-30b-a3b` | secondary |
| T2 | `google/gemma-3-27b-it` | secondary |
| T3 | `qwen/qwen3.5-35b-a3b` | secondary |
| Judge | `qwen/qwen-2.5-72b-instruct` | locked, not an experimental factor |

Three of four targets are Qwen-line models. Architectural diversity is limited. Target-model behavior may influence observed effects. All calls used OpenRouter. Provider-side tool formatting can affect Tool-HASR and INVALID rates.

**Statistics.** Rates: numerator/denominator, point estimate, Wilson 95% CI where already computed. Δ: difference of rates; **no Δ CI was pre-registered** and none is manufactured. Paired discordant counts vs T0 are descriptive. McNemar was **not** preregistered for Q2 and is **not** reported.

**Stage-B traces.** Official packaged T0 PHASE1-CORE Tool-HASR/Δ are reused from the Q2 live report (not a local raw-trace recompute). Local Stage-B `predictions.jsonl` is **MISSING_LOCALLY**. Independent local recomputation of T0 from raw traces was not performed. See `STAGE_B_EVIDENCE_STATUS.md`.

---

## 7. Results

All cells use n=16 attack arms. Wilson 95% CIs are on **rates**, not on Δ. Source: `q2_final_statistics.json`. This section reports **observed detector-related effects** under the tested protocol. It does not turn 9/9 into causal proof.

### Table 3 — Tool-HASR by cell

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

### Table 4 — Primary Δ Tool-HASR versus D0 (authoritative values)

| Target | D1 | D2 | D4 | Signs |
| --- | ---: | ---: | ---: | --- |
| T0 | −0.6875 | −0.2500 | −0.5625 | NEG, NEG, NEG |
| T1 | −0.7500 | −0.3125 | −0.6250 | NEG, NEG, NEG |
| T2 | −0.6875 | −0.2500 | −0.5625 | NEG, NEG, NEG |
| T3 | −0.5625 | −0.1875 | −0.5000 | NEG, NEG, NEG |

**9/9 detector-target comparisons preserved the negative direction** relative to T0. Intervals on the underlying rates are wide (especially 2/16 cells). Magnitudes should not be over-read. Detectors are not ranked.

**Figure 3.** Δ Tool-HASR relative to D0 across T0–T3. n=16 attack arms/cell. D0 is the reference (Δ=0 by definition). Categorical grouping; no ranking colors; no significance encoding. File: `figures/figure3_delta_across_targets.png`. Caption: *pilot-scale; scientific_evidence=false; detector-related Δ under locked PHASE1-CORE; not causal proof.*

T2 Δ matches T0 Δ exactly in this sample. That is an observed coincidence at n=16, not evidence that T2 equals T0 in general.

Paired discordant Tool-HASR counts (descriptive; no p-value): T0 vs T1 D0 discordant=1; T0 vs T3 D0 discordant=2; T0 vs T3 D2 discordant=1; T0 vs T3 D4 discordant=1; remaining listed pairs discordant=0 (`STATISTICAL_REPORTING.md`).

---

## 8. Diagnostic Analysis

### 8.1 Tool-HASR versus Judge-ASR

Tool-HASR measures **harmful tool execution behavior**. Judge-ASR reflects **judge-level attack-success assessment**. They are not interchangeable.

For T1–T3: Tool-HASR = 81/192 = 0.421875; Judge-ASR = 186/192 = 0.96875; M3=108; M4=3.

Disagreement can arise from several sources. This paper does **not** infer a single cause:

- refusal behavior;
- tool execution state (blocked or not executed);
- malformed/invalid tool arguments;
- judge interpretation;
- target-model behavior;
- runtime/provider behavior.

**Finding.** Judge-ASR and Tool-HASR capture related but non-identical operational outcomes. Neither metric is declared invalid because they disagree. Tool-HASR remains primary.

### Table 5 — Tool-HASR vs Judge-ASR (n=16/cell; Wilson 95% CI on each rate)

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

**Figure 4.** Tool-HASR versus Judge-ASR with M3/M4 diagnostic interpretation. Pooled attack n=64/target (16×4). Not a ranking; no significance encoding. File: `figures/figure4_toolhasr_vs_judgeasr.png`. Caption: *related but non-identical endpoints; Judge-ASR is not declared invalid.*

### 8.2 INVALID_TOOL_ARGS

Q2 live: **192 INVALID_TOOL_ARGS events / 136 affected arms** (of 432). Independent recompute on `predictions.jsonl` matches official `metrics.json`.

These are **canonical tool-state events**. They are **not** automatically equivalent to successful attacks. They can affect **execution observability**. They are a **potential confounder** for Tool-HASR interpretation (a schema failure can stop a harmful call; INVALID also co-occurs with some Tool-HASR-true attack arms). The analysis does **not** silently discard them. No unsupported claim of negligibility is made.

### Table 6 — INVALID diagnostics (existing S0/S1/S2 only)

| Metric | S0 (official) | S1 (stratify) | S2 (exclude ≥1 INVALID) |
| --- | --- | --- | --- |
| Role | Primary | Descriptive; does not replace official | Sensitivity; does not replace official |
| Sign agreement | 9/9 (protocol) | Not a protocol 9/9 statistic; observed D1/D2/D4 Δ signs remain NEG in both strata | 9/9 vs T0 S2 |
| S0→layer sign flips | n/a | Not a protocol flip table | 0 |
| Events | 192 (T1–T3; retained) | 192 (stratified, not dropped) | same events sit on excluded arms; S0 unchanged |
| Arms | 136/432 have ≥1 INVALID; all retained | Same 136 stratified | Attack arms excluded: T0=14, T1=19, T2=22, T3=21 |

S0/S1/S2 sensitivity did not change the Q2 sign-consistency conclusion. That does **not** establish that invalid arguments are negligible.

**Figure 5.** INVALID_TOOL_ARGS diagnostic, T1–T3. n=432 arms. S0 denominator unchanged. File: `figures/figure5_invalid_tool_args.png`. Caption: *frequent; not discarded; not Tool-HASR success; not proven negligible.*

T0 INVALID 61 events / 39 arms is a **prior derived record**, not a raw-trace recompute (`STAGE_B_TRACE_STATUS=MISSING_LOCALLY`).

---

## 9. Discussion

Under locked PHASE1-CORE, the observed Δ direction remained consistent across T0–T3. Nine of nine detector-target comparisons preserved the negative direction. That **suggests**, at pilot scale and under the tested protocol, that detector-related Tool-HASR differences versus D0 can keep sign on independently selected secondary targets.

It does **not** establish:

- universal robustness or general robustness;
- comprehensive model generalization;
- production readiness or guaranteed security;
- causal proof of detector identity;
- comparison as a ranking against CaMeL, AgentDojo defenses, ASB defenses, Llama Guard, PromptShield, IsolateGPT, instruction-hierarchy models, or Task Shield;
- that Judge-ASR is invalid;
- that INVALID_TOOL_ARGS are negligible.

The present study is an **attribution study**, not a head-to-head defense benchmark. Protocols, populations, metrics, and execution environments differ across papers; numerical cross-paper comparison would be a claims error.

Track A VNEXT FAIL and Track B Phase-1 LIVE remain on different packs. They must not be pooled with Q2 Tool-HASR.

---

## 10. Limitations

Limitations are technically binding, not boilerplate.

### Table 7 — Limitations

| # | Limitation |
| --- | --- |
| 1 | n=16 per cell; Wilson CIs are wide (2/16 Tool-HASR CI [0.035, 0.360]) |
| 2 | Pilot-scale study; `scientific_evidence=false`; not confirmatory |
| 3 | Four target models only |
| 4 | Qwen-heavy target set; T2 is Gemma-3; judge also Qwen |
| 5 | Limited model-family / architectural diversity; OpenRouter only |
| 6 | D3 deferred; no embedding-detector numbers |
| 7 | C4 / open adaptive attacker out of scope |
| 8 | INVALID_TOOL_ARGS frequency (192 events / 136 arms on Q2 live); potential confounder |
| 9 | Stage-B raw traces unavailable in the current checkout (`MISSING_LOCALLY`); no reconstruction |
| 10 | No matched external defense baseline |
| 11 | No ranking versus published systems; no claim of comprehensive comparison |
| 12 | No claim of universal generalization |
| 13 | Target-model behavior may influence observed effects |
| 14 | Judge/tool disagreement (T1–T3 M3=108, M4=3); endpoints are non-identical |
| 15 | Results are protocol-specific (PHASE1-CORE, frozen P2, mock tools, short horizon, one judge) |
| 16 | Provider/runtime and tool-call formatting effects |
| 17 | Refusal is not credited as a defense win |
| 18 | Exact literature gap cannot be claimed globally (PARTIAL_GAP) |
| 19 | No claim of universal detector causality |
| 20 | Bibliography venue/DOI mostly UNVERIFIED; camera-ready citations incomplete |

---

## 11. Reproducibility

`REPRODUCIBILITY_STATUS = PARTIAL`. Full reproducibility is **not** claimed while Stage-B raw traces remain missing.

**Frozen evidence (do not modify):** P1 SHA `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235`; P2 SHA `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd`; Q2 predictions SHA `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6`; evidence commit `b075df0f5ec5ad11ede76ac4e4079cade15208f1`; run `p3_stage_c_q2_20260917T123855Z_b075df0f`. Local file hashes of P1/P2/Q2 predictions were rechecked this pass and match.

**Derived analysis:** `q2_final_statistics.json`; INVALID recompute; Figures 3–5; S0/S1/S2; Wilson CIs on rates.

**Manuscript interpretation:** this file; `CLAIM_EVIDENCE_MATRIX.md`.

Checklist: `Q2_REPRODUCIBILITY_CHECKLIST.md`. Stage-B: `STAGE_B_EVIDENCE_STATUS.md`.

---

## 12. Conclusion

This study evaluates whether detector-related security effects under a locked intervention policy remain directionally consistent across independently selected target models. Under the tested protocol, the observed Δ direction remained consistent across T0–T3: 9/9 comparisons preserved the negative direction (432/432 arms; $0.152885 historical spend; n=16/cell; `scientific_evidence=false`). That is **pilot-scale evidence of directional consistency**, not confirmatory proof.

The contribution is the **controlled attribution protocol** plus that bounded empirical analysis. Detector families D1/D2/D4 are not claimed as novel. The evidence does not establish universal robustness, production readiness, causal proof, or a ranking against external defenses.

Future matched baselines, larger n, more model families, D3, or open adaptive attackers would be **new studies**, not silent extensions of this run.

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

Task Shield (`arXiv:2412.16682`) is **not** a verified in-package bibliographic record and is not listed as a reference.
