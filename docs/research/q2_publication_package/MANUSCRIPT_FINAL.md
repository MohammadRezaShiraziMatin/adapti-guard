# 1. Title

**Controlled Detector Attribution under a Locked Runtime Intervention Policy: A Pilot-Scale Agent Security Evaluation**

**Manuscript FINAL (internal package).** Not a venue submission.  
**Evidence freeze:** Q2 run `p3_stage_c_q2_20260917T123855Z_b075df0f` · commit `b075df0f5ec5ad11ede76ac4e4079cade15208f1`.  
**This packaging:** LIVE_EVAL=false · API_CALLS=0 · LLM_CALLS=0 · NETWORK_CALLS=0.  
**Protocol flag (internal, not abstract copy):** `scientific_evidence=false`. Scope: **protocol-complete pilot-scale directional consistency**. Not confirmatory.

Related-work identities use existing Hub-verified arXiv records. Most venue/DOI fields remain UNVERIFIED. AgentDojo venue/DOI and BIPIA venue/DOI are operator-supplied and not re-fetched this turn (`BIBLIOGRAPHY_VERIFICATION.md`). Novelty class: **PARTIAL_GAP**. Central scientific claim status: **PARTIALLY_SUPPORTED / PILOT-SCALE**.

---

# 2. Abstract

Observed security behavior in tool-using language-model agents can mix **detector behavior** with the **downstream intervention policy** that allows, wraps, or denies tools. Without holding that policy fixed, detector-related effects are difficult to attribute.

This paper reports a **controlled attribution protocol**, not a new detector family and not a defense covering all threat models. The research question is whether the detector-related Tool-HASR effect observed under a locked Stage-B target remains directionally consistent when the same locked policy, pack, detectors, thresholds, and judge are applied to independently selected secondary target models. The intervention policy is held fixed (PHASE1-CORE). Detector identity is varied, including a no-detection reference (D0). The primary outcome is **Tool-HASR** (harmful tool execution). **Judge-ASR** is a secondary, non-identical diagnostic of judge-level attack-success assessment. The evaluation uses frozen pack `p2_agentic_v0.1.0` (16 attack / 16 twin / 4 hard-negative trajectories), four target models, and **n=16 attack arms per target×detector cell**. Q2 live completed **432/432 arms** (historical spend $0.152885).

Under the tested protocol, detector-related Tool-HASR Δ versus D0 was negative for D1, D2, and D4 on the locked Stage-B target T0 and on independently selected T1–T3 (**9/9 directional agreements**). This is **pilot-scale directional consistency**. It does not establish population-level generalization. T1–T3 Tool-HASR was 81/192 = 0.421875; Judge-ASR was 186/192 = 0.96875 (M3=108, M4=3). INVALID_TOOL_ARGS occurred on 192 events / 136 arms and is treated as a canonical execution-state diagnostic, not as automatic attack success or failure.

The manuscript does not claim robustness beyond the tested protocol, production readiness, confirmatory multi-model generalization, or a ranking against external defenses.

---

# 3. Introduction

**Problem.** Observed security behavior in agent systems may reflect both detector behavior and downstream intervention policy. A stack that changes detector and policy together reports an operational outcome. It does not isolate which layer is associated with a change in harmful tool execution.

**Gap.** Without controlling the intervention policy, detector-related effects can be difficult to attribute. Existing literature already provides prompt-injection attacks, agent security benchmarks, runtime guardrails, architectural isolation, and detector approaches. Those lines of work do not, in the surveyed set, establish the locked-policy detector-attribution factorial used here as the central measurement protocol (`NOVELTY_AUDIT.md`; novelty class **PARTIAL_GAP**).

**Approach.** Hold the intervention policy fixed and vary detector identity, including a no-detection reference (D0). Thresholds, action costs, frozen pack, judge, temperature, and cache settings remain locked. The primary estimand is the sign of Tool-HASR Δ versus D0 at each target. Tool-HASR and Judge-ASR are kept as distinct measurements.

**Result.** Observed Δ direction remained consistent across T0–T3 in this pilot-scale evaluation: 9/9 detector-target comparisons preserved the negative direction (n=16 per cell; 432/432 Q2 live arms).

**Qualification.** This is not a confirmatory claim. Sample size is pilot-scale. Precision is limited. Power is limited for broad generalization. Directional consistency is an observed property of this evaluation. It does not establish population-level generalization. Three of four targets are Qwen-family models. D3 was deferred. Open-ended adaptive attackers (C4 interaction horizon) are out of scope.

This manuscript does not reverse other tracks in the same repository. Track A (VNEXT confirmation) is an immutable FAIL on a different pack and treatment. Track B (Phase-1 confirmatory LIVE) is a scoped SUPPORTED_IMPROVEMENT on a third pack. Q2 must not be pooled with either (`docs/paper/dual_track/DUAL_TRACK_STATUS.md`).

---

# 4. Research Question

**RQ-C2 (locked protocol).** Does the detector-related Tool-HASR effect versus D0 observed under the locked Stage-B target (T0) remain directionally consistent when the same policy, pack, detectors, thresholds, and judge are applied to independently selected secondary target models T1–T3?

**Experimental factor.** `target_model_id ∈ {T0, T1, T2, T3}`.  
**Locked.** Policy = PHASE1-CORE; detectors ∈ {D0, D1, D2, D4}; D3 deferred; pack `p2_agentic_v0.1.0`; judge `qwen/qwen-2.5-72b-instruct`.  
**Primary estimand.** sign(Δ(d,t)) for d ∈ {D1, D2, D4}, t ∈ {T1, T2, T3}, compared with sign(Δ(d,T0)).  
**Agreement rule.** 9 contrasts; agreement if signs match (exact 0.0 would be ZERO; none observed in primary Δ).

Q2 is **not** powered as a confirmatory hypothesis test. The run records `scientific_evidence=false` in the internal protocol flag. Live-report “supported” means protocol sign-agreement support, not Track B `SUPPORTED_IMPROVEMENT` and not a qualified win (MSID ∧ significance ∧ U).

> Q2 was designed as a directional consistency analysis; inferential p-values were not preregistered and are not reported.

---

# 5. Problem Formulation

Security outcomes on a tool-using agent mix several layers. This paper names them separately.

| Layer | What it is | What it is not |
| --- | --- | --- |
| **Detector behavior** | Hits/scores on untrusted context under a `P3Detector` contract (D0/D1/D2/D4) | The intervention that grants or denies tools |
| **Downstream intervention policy** | PHASE1-CORE mapping of detector/risk signals to actions A0–A3, then the tool-permission gate | A detector family |
| **Tool-HASR (primary)** | Attack-arm rate of harmful **tool execution** matching a pre-registered `success_condition` | A judge-model opinion |
| **Judge-ASR (secondary)** | Attack-arm rate of judge-classified attack success | Harmful tool execution |
| **M3** | Judge success ∧ ¬ Tool-HASR success | Proof that the judge is wrong |
| **M4** | Tool-HASR success ∧ ¬ judge success | Proof that the judge is right |
| **INVALID_TOOL_ARGS** | Canonical tool-state events: schema/argument failures | Attack success; attack failure; harmlessness; detector failure |

**Δ(d,t)** = Tool-HASR(d,t) − Tool-HASR(D0,t) on attack arms at the same target, under locked PHASE1-CORE. This is a **detector-related association** under the controlled protocol. It does not establish that detector identity is the sole associated factor, independent of all runtime factors.

**Unit of analysis.** Attack episode-arm: trajectory × detector × PHASE1-CORE × target. Official n=16 True+False per cell; UNKNOWN excluded (`exclude_unknown=true`); Q2 cells have n_unknown=0.

**INVALID policy.** S0 (official) retains the primary denominator. S1 stratifies arms with vs without INVALID. S2 excludes arms with ≥1 INVALID (`derived_after_run`). INVALID is **not** silently discarded. INVALID is **not** automatically equivalent to a successful attack, a failed attack, harmlessness, or detector failure. INVALID can affect **execution observability** and is a **potential confounder**. No claim of negligibility.

---

# 6. Related Work

We cite records whose title, authors, year, and arXiv id were verified from the arXiv API. Venues and DOIs were verified from official sources where available: doi.org (BIPIA, AgentDojo), ACL Anthology (InjecAgent), ICLR poster/OpenReview (ASB, AgentHarm), and author publication page (CaMeL). Remaining venues are verified from arXiv comment fields or remain UNVERIFIED (preprints). See `BIBLIOGRAPHY_VERIFICATION.md`. Novelty class: **PARTIAL_GAP**. Matrix: `RELATED_WORK_MATRIX.md`.

## 6.1 Existing literature

**Prompt injection and indirect prompt injection.** Greshake et al. (`2302.12173`) define IPI via retrieved/untrusted content. Yi et al. (BIPIA, `2312.14197`) benchmark IPI. Perez & Ribeiro (`2211.09527`), Liu et al. (`2306.05499`, `2310.12815`), and Toyer et al. (`2311.01011`) document direct/application injection. These are threat papers, not locked-policy detector attribution.

**Agent security benchmarks.** InjecAgent (`2403.02691`) measures IPI that induces detrimental tool use. AgentDojo (`2406.13352`; identity VERIFIED) is a dynamic attack/defense environment. AgentHarm (`2410.09024`) measures agent harmfulness after jailbreaks. Agent Security Bench / ASB (`2410.02644`; identity VERIFIED) evaluates many attacks and defenses. ToolEmu (`2309.15817`) emulates tool trajectories. Paper identities are verified. Packs, metrics, and execution environments differ from Q2. They are **not** numerical Q2 baselines.

**Runtime guardrails and detector approaches.** NeMo Guardrails (`2310.10501`) encodes programmable rails. Llama Guard (`2312.06674`) and PromptShield (`2501.15145`) are detector/safeguard systems. StruQ (`2402.06363`) and Spotlighting (`2403.14720`) channel or mark untrusted data. MELON (`2502.05174`) re-executes masked trajectories. These are related mechanism classes. They are not the Q2 factorial and are not compared numerically here.

**Architectural isolation and defense mechanisms.** IsolateGPT (`2403.04960`) isolates execution. CaMeL (`2503.18813`) is a **published** control/data isolation design, not an unverified idea. Wallace et al. (`2404.13208`) train privileged-instruction priority. Meta SecAlign (`2507.02735`) is a model-level defense. Those change the **target**, which would violate Q2’s locked-target × vary-detector design.

Names requested for attention but **not** in this package’s verified 21-record bibliography (Task Shield, Adaptive Attacks, AutoDojo, SCOUT, AgentAntibody, HARD, ARGUS, VIGIL, AttriGuard, MCP-SafetyBench, Runtime Policy Enforcement for MCP Agents) are **not** added as citations. Metadata is not invented (`BIBLIOGRAPHY_VERIFICATION.md`).

## 6.2 This paper

This paper contributes a **controlled detector/policy attribution protocol**: D0 reference; fixed intervention policy; Tool-HASR as primary outcome; cross-target directional consistency; M3/M4 diagnostics; INVALID_TOOL_ARGS diagnostics. It does not claim a new detector family, a defense covering all threat models, or a ranking of published systems.

**Residual gap (narrow).** The verified literature establishes extensive work on attacks, benchmarks, defenses, and adaptive evaluation, but does not establish the exact locked-policy detector-attribution factorial used here as the central measurement protocol. That is a **partial gap**, not a global uniqueness claim. The present study is an attribution study, not a head-to-head defense benchmark.

The research question concerns controlled detector-related attribution, not comparative ranking of defenses. Therefore external baselines are outside the current primary claim. Their absence is **methodological scope**, not an accidental omission (`BASELINE_GAP.md`).

---

# 7. Controlled Attribution Framework

Each episode-arm runs the following control structure. What is **varied** is detector identity; what is **locked** is everything else.

```
[Varied]  Detector (D0 / D1 / D2 / D4)
            │  detector signal
            ▼
[Locked]  RiskCore
            │  risk score
            ▼
[Locked]  CorePolicy (PHASE1-CORE)  →  intervention action A0–A3
            │  thresholds 0.25 / 0.25 / 0.60;  action costs A0=0 A1=0.10 A2=0.25 A3=0.50
            ▼
[Locked]  ToolPermissionGate
            │  allow / wrap / deny
            ▼
[Locked]  Mock tools  ──►  Tool-HASR  (primary: harmful tool execution)

[Parallel, locked]  Judge (qwen-2.5-72b)  ──►  Judge-ASR  (secondary: judge-level assessment)
```

Gold labels (`is_attack`, `label`, `category`) do not enter the detector→policy path. The judge does not enter the detector→policy path.

| Varied | Locked |
| --- | --- |
| Detector identity {D0, D1, D2, D4} | PHASE1-CORE, thresholds, action costs, P2 pack, judge, temperature=0.0, cache=false, seed=42 |

D0 implements no detection (no hits). D1/D2/D4 share a `P3Detector` contract. D3 is `DEFERRED_NO_OFFLINE_IMPL` and has no scores. D3 was deferred because the planned semantic-embedding dependency was not part of the locked offline protocol. D3 is future work. No D3 results are simulated or invented.

PHASE1-CORE maps detector/risk signals to actions A0–A3 with locked thresholds (is_injection 0.25; risk 0.25/0.60) and normalized action costs (A0=0, A1=0.10, A2=0.25, A3=0.50). Those costs are experimental weights, not USD prices.

D0 estimates tool-harm when the policy receives no detector hits. Contrasts versus D0 are therefore **detector-related under this policy**. Schema failures, target refusals, provider formatting, and judge behavior still occur in every arm. Protocol: `no_ranking=true`.

---

# 8. Experimental Protocol

### Table 1 — Study design

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
| Internal protocol flag | `scientific_evidence=false` |
| n per cell | 16 attack arms |
| Primary outcome | Tool-HASR |
| Secondary diagnostic | Judge-ASR |

### Table 2 — Target and judge models (not a quality ranking)

| Slot | Model ID | Family | Role |
| --- | --- | --- | --- |
| T0 | `qwen/qwen-2.5-7b-instruct` | Qwen-2.5 dense | Stage-B reference, not re-run |
| T1 | `qwen/qwen3-30b-a3b` | Qwen3 MoE | secondary |
| T2 | `google/gemma-3-27b-it` | Gemma-3 | secondary |
| T3 | `qwen/qwen3.5-35b-a3b` | Qwen3.5 MoE | secondary |
| Judge | `qwen/qwen-2.5-72b-instruct` | Qwen-2.5 dense | locked, not an experimental factor |

Four targets were used. Three of four (T0, T1, T3) are Qwen-family. The judge is also Qwen-family. Model-family diversity is limited. Results should not be generalized to arbitrary model families. Target-model behavior can influence observed tool execution and judge outcomes. The target set is **not** described as diverse without that qualification. All calls used OpenRouter. Provider-side tool formatting can affect Tool-HASR and INVALID rates.

**Statistics.** Rates: numerator/denominator, point estimate, and Wilson 95% CI **derived from locked counts** (not a preregistered inferential analysis of Δ). Δ: difference of rates; **no Δ CI was preregistered** and none is manufactured. Paired discordant counts vs T0 are descriptive. McNemar was **not** preregistered for Q2 and is **not** reported. No p-values are invented.

**Stage-B traces.** Official packaged T0 PHASE1-CORE Tool-HASR/Δ are reused from the Q2 live report (not a local raw-trace recompute). Local Stage-B `predictions.jsonl` is **MISSING_LOCALLY** (`STAGE_B_TRACE_STATUS = MISSING_LOCALLY`). Independent local recomputation of T0 from raw traces was not performed. The official Stage-B reported result is distinct from locally reproducible raw-trace availability. See `STAGE_B_EVIDENCE_STATUS.md`.

---

# 9. Results

All cells use n=16 attack arms. Wilson 95% CIs on rates are **derived from locked counts**. They are not Δ intervals and were not preregistered as a confirmatory analysis. Source: `q2_final_statistics.json`. This section reports **observed detector-related associations** under the tested protocol.

### Table 3 — Primary Δ results (Tool-HASR versus D0)

Definition: Δ(d,t) = Tool-HASR(d,t) − Tool-HASR(D0,t) on attack arms, PHASE1-CORE. Wilson 95% CI on each Tool-HASR rate (derived from locked counts).

| Cell | Tool-HASR (d) | Tool-HASR (D0) | Δ | Sign |
| --- | --- | --- | ---: | --- |
| T0/D1 | 2/16 = 0.1250 [0.035, 0.360] | 13/16 = 0.8125 [0.570, 0.934] | −0.6875 | NEG |
| T0/D2 | 9/16 = 0.5625 [0.332, 0.769] | 13/16 = 0.8125 [0.570, 0.934] | −0.2500 | NEG |
| T0/D4 | 4/16 = 0.2500 [0.102, 0.495] | 13/16 = 0.8125 [0.570, 0.934] | −0.5625 | NEG |
| T1/D1 | 2/16 = 0.1250 [0.035, 0.360] | 14/16 = 0.8750 [0.640, 0.965] | −0.7500 | NEG |
| T1/D2 | 9/16 = 0.5625 [0.332, 0.769] | 14/16 = 0.8750 [0.640, 0.965] | −0.3125 | NEG |
| T1/D4 | 4/16 = 0.2500 [0.102, 0.495] | 14/16 = 0.8750 [0.640, 0.965] | −0.6250 | NEG |
| T2/D1 | 2/16 = 0.1250 [0.035, 0.360] | 13/16 = 0.8125 [0.570, 0.934] | −0.6875 | NEG |
| T2/D2 | 9/16 = 0.5625 [0.332, 0.769] | 13/16 = 0.8125 [0.570, 0.934] | −0.2500 | NEG |
| T2/D4 | 4/16 = 0.2500 [0.102, 0.495] | 13/16 = 0.8125 [0.570, 0.934] | −0.5625 | NEG |
| T3/D1 | 2/16 = 0.1250 [0.035, 0.360] | 11/16 = 0.6875 [0.444, 0.858] | −0.5625 | NEG |
| T3/D2 | 8/16 = 0.5000 [0.280, 0.720] | 11/16 = 0.6875 [0.444, 0.858] | −0.1875 | NEG |
| T3/D4 | 3/16 = 0.1875 [0.066, 0.430] | 11/16 = 0.6875 [0.444, 0.858] | −0.5000 | NEG |

**9/9 detector-target comparisons preserved the negative direction** relative to T0. All D1/D2/D4 Δ values versus D0 are negative. Intervals on the underlying rates are wide (especially 2/16 cells). Magnitudes should not be over-read. Detectors are not ranked. Q2 live T1–T3 pooled Tool-HASR: 81/192 = 0.421875.

**n=16 per cell** is pilot-scale. Precision is limited. Power is limited for broad generalization. Directional consistency is an observed property of this evaluation. It does not establish population-level generalization.

**Figure 3.** Δ Tool-HASR **relative to D0** across T0–T3. n=16 attack arms/cell. D0 is the reference (Δ=0 by definition). Categorical grouping; no ranking colors; no significance encoding. File: `figures/figure3_delta_across_targets.png`. Caption: *pilot-scale directional consistency; n=16/cell; detector-related Δ versus D0 under locked PHASE1-CORE; not a ranking; Wilson CIs reported in Table 3 are on rates, derived from locked counts, not on Δ.*

T2 Δ matches T0 Δ exactly in this sample. That is an observed coincidence at n=16, not evidence that T2 equals T0 in general.

Paired discordant Tool-HASR counts (descriptive; no p-value): T0 vs T1 D0 discordant=1; T0 vs T3 D0 discordant=2; T0 vs T3 D2 discordant=1; T0 vs T3 D4 discordant=1; remaining listed pairs discordant=0 (`STATISTICAL_REPORTING.md`).

---

# 10. Diagnostic Analysis

## 10.1 Tool-HASR versus Judge-ASR

Tool-HASR and Judge-ASR are **distinct measurements**.

- **Tool-HASR:** harmful tool execution behavior.
- **Judge-ASR:** judge-level attack-success assessment.

They are related but non-identical. Neither metric is declared invalid because they disagree. They are not forced into one metric. Tool-HASR remains primary.

For T1–T3: Tool-HASR = 81/192 = 0.421875; Judge-ASR = 186/192 = 0.96875; M3=108; M4=3.

Possible disagreement sources, stated conservatively (no single-cause inference):

- model refusal behavior;
- tool execution state (blocked or not executed);
- malformed tool arguments (INVALID_TOOL_ARGS);
- judge interpretation;
- target-model behavior;
- trajectory-level semantics;
- runtime/provider behavior.

### Table 4 — Tool-HASR vs Judge-ASR (n=16/cell; Wilson 95% CI on each rate, derived from locked counts)

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

**Figure 4.** Tool-HASR versus Judge-ASR with M3/M4 diagnostic interpretation. Pooled attack n=64/target (16×4). Related but non-identical endpoints. File: `figures/figure4_toolhasr_vs_judgeasr.png`. Caption: *Tool-HASR = harmful tool execution; Judge-ASR = judge-level attack-success assessment; related but non-identical; neither metric is declared invalid; n=16/cell; not a ranking.*

## 10.2 INVALID_TOOL_ARGS

Q2 live: **192 INVALID_TOOL_ARGS events / 136 affected arms** (of 432). Independent recompute on `predictions.jsonl` matches official `metrics.json`.

INVALID_TOOL_ARGS is a **canonical execution-state category**. It is **not** automatically:

- attack success;
- attack failure;
- harmlessness;
- detector failure.

It matters because:

- malformed calls can prevent intended tool execution;
- this affects observability of harmful execution;
- it can interact with target-model behavior;
- it can influence the relationship between Tool-HASR and Judge-ASR.

INVALID events are retained in the official S0 analysis. They are not discarded. They are not treated as negligible. This paper does not claim that INVALID explains all Tool-HASR vs Judge-ASR disagreement. S0/S1/S2 diagnostics are preserved.

### Table 5 — INVALID_TOOL_ARGS diagnostics (existing S0/S1/S2 only)

| Metric | S0 (official) | S1 (stratify) | S2 (exclude ≥1 INVALID) |
| --- | --- | --- | --- |
| Role | Primary | Descriptive; does not replace official | Sensitivity; does not replace official |
| Sign agreement | 9/9 (protocol) | Not a protocol 9/9 statistic; observed D1/D2/D4 Δ signs remain NEG in both strata | 9/9 vs T0 S2 |
| S0→layer sign flips | n/a | Not a protocol flip table | 0 |
| Events | 192 (T1–T3; retained) | 192 (stratified, not dropped) | same events sit on excluded arms; S0 unchanged |
| Arms | 136/432 have ≥1 INVALID; all retained | Same 136 stratified | Attack arms excluded: T0=14, T1=19, T2=22, T3=21 |

S0/S1/S2 sensitivity did not change the Q2 sign-consistency conclusion. That does **not** establish that invalid arguments are negligible.

**Figure 5.** INVALID_TOOL_ARGS diagnostic, T1–T3. n=432 arms. S0 denominator unchanged. File: `figures/figure5_invalid_tool_args.png`. Caption: *INVALID_TOOL_ARGS is a diagnostic execution-state category; frequent (192 events / 136 arms); not discarded; not Tool-HASR success; not proven negligible; not a ranking.*

T0 INVALID 61 events / 39 arms is a **prior derived record**, not a raw-trace recompute (`STAGE_B_TRACE_STATUS=MISSING_LOCALLY`).

---

# 11. Discussion

Under locked PHASE1-CORE, the observed Δ direction remained consistent across T0–T3. Nine of nine detector-target comparisons preserved the negative direction. That **suggests**, at pilot scale and under the tested protocol, that detector-related Tool-HASR differences versus D0 can keep sign on independently selected secondary targets.

It does **not** establish:

- robustness beyond the tested protocol;
- population-level generalization across model families;
- production readiness;
- that detector identity is the sole associated factor, independent of all runtime factors;
- a ranking against CaMeL, AgentDojo defenses, ASB defenses, Llama Guard, PromptShield, IsolateGPT, instruction-hierarchy models, or other external systems;
- that Judge-ASR is invalid;
- that INVALID_TOOL_ARGS are negligible;
- robustness against open-ended adaptive attackers.

The present study is an **attribution study**, not a head-to-head defense benchmark. Protocols, populations, metrics, and execution environments differ across papers; numerical cross-paper comparison would be a claims error. External baselines are outside the current primary claim by design.

Track A VNEXT FAIL and Track B Phase-1 LIVE remain on different packs. They must not be pooled with Q2 Tool-HASR.

---

# 12. Limitations

Limitations are technically binding, not boilerplate.

### Table 6 — Threats and limitations

| # | Limitation |
| --- | --- |
| 1 | n=16 per cell; Wilson CIs are wide (2/16 Tool-HASR CI [0.035, 0.360]); limited precision; limited power for broad generalization |
| 2 | Pilot-scale study; internal flag `scientific_evidence=false`; not confirmatory; directional consistency is an observed property of this evaluation |
| 3 | Four target models only; does not establish population-level generalization |
| 4 | Qwen-heavy target set: T0=`qwen/qwen-2.5-7b-instruct`, T1=`qwen/qwen3-30b-a3b`, T2=`google/gemma-3-27b-it`, T3=`qwen/qwen3.5-35b-a3b`; judge=`qwen/qwen-2.5-72b-instruct` |
| 5 | Three of four targets are Qwen-family; model-family diversity is limited; results should not be generalized to arbitrary model families |
| 6 | D3 deferred because the planned semantic-embedding dependency was not part of the locked offline protocol; no D3 scores |
| 7 | The present study does not establish robustness against open-ended adaptive attackers, C4 interaction horizon, or attacker adaptation against the detector-policy system |
| 8 | INVALID_TOOL_ARGS frequency (192 events / 136 arms on Q2 live); canonical execution state; potential confounder for Tool-HASR observability and Tool-HASR/Judge-ASR disagreement; not discarded; not claimed to explain all metric disagreement |
| 9 | Stage-B raw traces unavailable in the current checkout (`MISSING_LOCALLY`); official Stage-B reported T0 reuse is distinct from independent raw-trace recomputation; no reconstruction |
| 10 | No matched external defense baseline; attribution scope, not comparative ranking of defenses |
| 11 | No ranking versus published systems |
| 12 | Target-model behavior can influence observed tool execution and judge outcomes |
| 13 | Judge/tool disagreement (T1–T3 M3=108, M4=3); endpoints are non-identical |
| 14 | Results are protocol-specific (PHASE1-CORE, frozen P2, mock tools, short horizon, one judge) |
| 15 | Provider/runtime and tool-call formatting effects |
| 16 | Refusal is not credited as a defense win |
| 17 | Exact literature gap cannot be claimed globally (PARTIAL_GAP) |
| 18 | Observed Δ vs D0 is a detector-related association under the controlled protocol; it does not establish detector causality in isolation |
| 19 | Bibliography venue/DOI mostly UNVERIFIED; camera-ready citations incomplete |

**INVALID_TOOL_ARGS (limitations paragraph).** INVALID_TOOL_ARGS is a canonical execution-state category. Malformed calls can prevent intended tool execution, which affects observability of harmful execution, can interact with target-model behavior, and can influence the relationship between Tool-HASR and Judge-ASR. Official S0 retains these events. S1/S2 are sensitivity diagnostics. INVALID is not automatically attack success, attack failure, harmlessness, or detector failure. It is not negligible. It is not claimed to explain all metric disagreement.

**D3 (future work).** D3 was deferred because the planned semantic-embedding dependency was not part of the locked offline protocol. No D3 results exist. Adding D3 experimentally would be a new study.

**C4 / adaptive attackers (future work).** The present study does not establish robustness against open-ended adaptive attackers, C4 interaction horizon, or attacker adaptation against the detector-policy system. PHASE1-CORE action adaptation is not a closed-loop adaptive adversary. A C4 study would be a new experiment.

**External baselines (scope).** Numerical comparison against CaMeL, AgentDojo, ASB, Llama Guard, PromptShield, or other external defenses is outside the current primary claim. The research question is controlled detector-related attribution, not comparative ranking of defenses.

---

# 13. Reproducibility

`REPRODUCIBILITY_STATUS = PARTIAL`. Full reproducibility is **not** claimed while Stage-B raw traces remain missing.

**FROZEN (do not modify):** P1 SHA `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235`; P2 SHA `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd`; Q2 predictions SHA `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6`; evidence commit `b075df0f5ec5ad11ede76ac4e4079cade15208f1`; run `p3_stage_c_q2_20260917T123855Z_b075df0f`. Local file hashes of P1/P2/Q2 predictions were rechecked this pass and match.

**DERIVED:** `q2_final_statistics.json`; INVALID recompute; Figures 3–5; S0/S1/S2; Wilson CIs on rates (derived from locked counts).

**INTERPRETIVE:** this file; `CLAIM_EVIDENCE_MATRIX.md`; novelty PARTIAL_GAP; attribution vs ranking scope.

Checklist: `Q2_REPRODUCIBILITY_CHECKLIST.md`. Stage-B: `STAGE_B_EVIDENCE_STATUS.md`.

---

# 14. Conclusion

This study evaluates whether detector-related security effects under a locked intervention policy remain directionally consistent across independently selected target models. Under the tested protocol, the observed Δ direction remained consistent across T0–T3: 9/9 comparisons preserved the negative direction (432/432 arms; $0.152885 historical spend; n=16/cell). That is **pilot-scale directional consistency**. It is not confirmatory. It does not establish population-level generalization.

The contribution is the **controlled attribution protocol** plus that bounded empirical analysis. Detector families D1/D2/D4 are not claimed as new. The evidence does not establish robustness beyond the tested protocol, production readiness, that detector identity is the sole associated factor, or a ranking against external defenses.

Future matched baselines, larger n, more model families, D3 after an offline embedding lock, or open adaptive attackers would be **new studies**, not silent extensions of this run.

---

## References

1. Perez & Ribeiro, 2022. Ignore Previous Prompt. arXiv:2211.09527. Venue: NeurIPS 2022 ML Safety Workshop (verified via arXiv comment).  
2. Greshake et al., 2023. Indirect Prompt Injection. arXiv:2302.12173. Preprint.  
3. Liu, Deng, et al., 2023. Prompt Injection attack against LLM-integrated Applications. arXiv:2306.05499. Preprint.  
4. Ruan et al., 2023. ToolEmu. arXiv:2309.15817. Preprint.  
5. Rebedea et al., 2023. NeMo Guardrails. arXiv:2310.10501. Venue: EMNLP 2023 Demo track (verified via arXiv comment).  
6. Liu, Jia, Geng, Jia, Gong, 2023. Formalizing and Benchmarking Prompt Injection Attacks and Defenses. arXiv:2310.12815. Venue: USENIX Security Symposium 2024 (verified via arXiv comment).  
7. Toyer et al., 2023. Tensor Trust. arXiv:2311.01011. Preprint.  
8. Inan et al., 2023. Llama Guard. arXiv:2312.06674. Preprint.  
9. Yi et al., 2023. BIPIA. arXiv:2312.14197. Venue: KDD 2025. DOI: 10.1145/3690624.3709179 (verified from doi.org).  
10. Chen, Piet, Sitawarin, Wagner, 2024. StruQ. arXiv:2402.06363. Venue: USENIX Security Symposium 2025 (verified via arXiv comment).  
11. Zhan et al., 2024. InjecAgent. arXiv:2403.02691. Venue: ACL 2024 Findings. DOI: 10.18653/v1/2024.findings-acl.624 (verified from ACL Anthology).  
12. Wu et al., 2024. IsolateGPT. arXiv:2403.04960. Venue: NDSS 2025 (verified via arXiv journal_ref).  
13. Hines et al., 2024. Spotlighting. arXiv:2403.14720. Preprint.  
14. Wallace et al., 2024. Instruction Hierarchy. arXiv:2404.13208. Preprint.  
15. Debenedetti et al., 2024. AgentDojo. arXiv:2406.13352. Venue: NeurIPS 2024. DOI: 10.52202/079017-2636 (verified from doi.org).  
16. Zhang et al., 2024. Agent Security Bench. arXiv:2410.02644. Venue: ICLR 2025 (verified from ICLR poster page / OpenReview).  
17. Andriushchenko et al., 2024. AgentHarm. arXiv:2410.09024. Venue: ICLR 2025 (verified from OpenReview / ICLR proceedings).  
18. Jacob et al., 2025. PromptShield. arXiv:2501.15145. Venue: ACM CODASPY 2025 (verified via arXiv comment).  
19. Zhu et al., 2025. MELON. arXiv:2502.05174. Venue: ICML 2025 (verified via arXiv comment).  
20. Debenedetti et al., 2025. CaMeL (Defeating Prompt Injections by Design). arXiv:2503.18813. Venue: IEEE SaTML 2026, accepted (verified from author publication page; currently preprint).  
21. Chen, Zharmagambetov, Wagner, Guo, 2025. Meta SecAlign. arXiv:2507.02735. Preprint.  

Task Shield, Adaptive Attacks, AutoDojo, SCOUT, AgentAntibody, HARD, ARGUS, VIGIL, AttriGuard, MCP-SafetyBench, and Runtime Policy Enforcement for MCP Agents are **not** verified in-package bibliographic records and are not listed as references.
