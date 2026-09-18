# Isolating Detector-Related Effects from Intervention Policy in LLM-Agent Security: A Controlled Multi-Target Study

**Manuscript V1 (internal).** Not a venue submission.  
**Evidence freeze:** Q2 run `p3_stage_c_q2_20260917T123855Z_b075df0f` · commit `b075df0f5ec5ad11ede76ac4e4079cade15208f1`.  
**This packaging:** LIVE_EVAL=false · API_CALLS=0 · no new experiments.  
**Protocol flag:** `scientific_evidence=false`. This is a **protocol-complete pilot-scale directional consistency study**, not a confirmatory multi-model study.

Related-work citations use Hub-verified arXiv identifiers. **Venue and DOI are UNVERIFIED** (`RELATED_WORK_MATRIX.md`).

---

## Abstract

**Problem.** Security outcomes for tool-using LLM agents mix two mechanisms: how a detector scores untrusted context, and how a downstream intervention policy grants, rewrites, or denies tool execution. When those mechanisms move together, a lower attack-success number cannot be attributed to the detector.

**Methodological gap.** Prior work documents prompt injection, agent benchmarks, guardrail detectors, programmable rails, and architectural isolation. It remains difficult to attribute operational tool-harm change to detector behavior independently of intervention policy.

**Controlled approach.** We hold downstream policy, thresholds, action costs, frozen benchmark pack, and judge fixed, and vary detector identity, including a no-detection arm (D0). The primary endpoint is Tool-HASR: whether a harmful tool execution matching a pre-registered success condition occurred. Judge-ASR is a secondary diagnostic. The estimand is Δ(d,t) = Tool-HASR(d,t) − Tool-HASR(D0,t).

**Scope.** Frozen pack `p2_agentic_v0.1.0` (16 attack / 16 twin / 4 hard-negative trajectories). Q2 design `B_REDUCED_Q2`: 432/432 completed arms under PHASE1-CORE on three secondary targets; T0 reused from a locked Stage-B run. n=16 attack arms per cell. Historical Q2 live spend $0.152885.

**Main observed finding.** Under locked PHASE1-CORE, D1/D2/D4 all had negative Tool-HASR Δ versus D0 on the Stage-B target T0, and the same sign on independently selected T1–T3 (9/9 sign agreements). This is a controlled isolation finding on four OpenRouter-served models.

**Limitations.** Pilot scale (`scientific_evidence=false`); wide Wilson intervals; Qwen-heavy target set; frequent INVALID_TOOL_ARGS (192 events / 136 arms on Q2 live); large Judge-ASR vs Tool-HASR disagreement (M3=108, M4=3 on T1–T3); no matched external baseline; D3 deferred; open adaptive attackers out of scope. **Official T0 Tool-HASR/Δ** is reused from Stage-B run `p3_stage_b_20260916T235438Z_7e401714`. **Local artifact availability:** Stage-B `predictions.jsonl` is `MISSING_LOCALLY` on this checkout (not fabricated).

**Contribution.** A controlled framework for isolating detector-related effects from downstream intervention policy in LLM-agent security, with a bounded cross-target directional-consistency check. The study does not claim a universal defense, a best detector, or production robustness.

---

## 1. Introduction

Tool-using language-model agents can cause harm by **executing** a tool call, not only by producing a string that a judge later labels successful. Defenses for this setting typically stack a detector, a risk mapping, and an intervention policy that allows, wraps, or denies tools. Published evaluations often report the stack as a whole. That is operationally useful and scientifically ambiguous: a drop in attack success may come from the detector, from a conservative policy, from schema failures that prevent execution, or from the target model refusing.

This paper studies **attribution**, not leaderboard performance. The central contribution is a controlled framework for isolating detector-related effects from downstream intervention policy. Concretely, we lock PHASE1-CORE (thresholds, action costs, frozen pack, judge) and vary detector identity {D0, D1, D2, D4}, where D0 is a no-detection arm. Primary security is Tool-HASR. Secondary is Judge-ASR. The Q2 question (RQ-C2) asks whether the detector-related Tool-HASR Δ observed on a locked primary target remains **directionally consistent** on three independently selected secondary targets.

This paper is a **protocol-complete pilot-scale directional consistency study**. The answer, under this protocol, is yes: 9/9 Δ signs agree (all negative). That finding is scoped to four models, n=16 per cell, mock tools, and `scientific_evidence=false`. It is not evidence that any detector is best, that the system is production-ready, or that prompt injection is solved.

This manuscript does not reverse other tracks in the same repository. Track A (VNEXT confirmation) is an immutable FAIL on a different pack and treatment. Track B (Phase-1 confirmatory LIVE) is a scoped SUPPORTED_IMPROVEMENT on a third pack. Q2 must not be pooled with either.

---

## 2. Related Work

We cite only records whose title, authors, year, and arXiv id were verified from Hugging Face Hub paper metadata. Venues remain UNVERIFIED. Full matrix: `RELATED_WORK_MATRIX.md`. Novelty test: `NOVELTY_AUDIT.md`.

**Prompt injection and indirect injection.** Perez and Ribeiro document goal hijacking and prompt leaking against instruction-following models (`2211.09527`). Liu et al. study practical injection against LLM-integrated applications (`2306.05499`) and propose a systematic attack/defense framework (`2310.12815`). Toyer et al. collect large-scale human-written injection attacks in Tensor Trust (`2311.01011`). Greshake et al. introduce indirect prompt injection via retrieved content (`2302.12173`). Yi et al. benchmark IPI with BIPIA (`2312.14197`).

**Agent and tool-use security evaluation.** Ruan et al. emulate tool-using agents in ToolEmu (`2309.15817`). Zhan et al. benchmark IPI that induces detrimental tool use in InjecAgent (`2403.02691`). Debenedetti et al. provide AgentDojo, a dynamic environment for agent attacks and defenses (`2406.13352`). Zhang et al. propose Agent Security Bench with many attack/defense methods and LLM backbones (`2410.02644`). Andriushchenko et al. measure agent harmfulness and multi-step capability after jailbreaks in AgentHarm (`2410.09024`). These establish that agent security is trajectory- and action-sensitive. They do not, from Hub metadata, verify Q2’s locked-policy detector factorial.

**Guardrails, detectors, and model-level defenses.** Inan et al. describe Llama Guard as an input/output safeguard (`2312.06674`). Rebedea et al. describe NeMo Guardrails as programmable rails (`2310.10501`). Jacob et al. study deployable prompt-injection detection in PromptShield (`2501.15145`). Wallace et al. train an instruction hierarchy (`2404.13208`). Chen et al. separate prompts and data in StruQ (`2402.06363`) and later describe Meta SecAlign as a model-level defense (`2507.02735`). Hines et al. spotlight untrusted content (`2403.14720`). Zhu et al. detect IPI by re-executing masked trajectories (MELON, `2502.05174`).

**Isolation by architecture, not by factorial.** Wu et al. propose IsolateGPT, an execution-isolation architecture for LLM apps (`2403.04960`). Debenedetti et al. propose CaMeL, segregating control and data flows (`2503.18813`). These isolate *channels or execution*, which is related to but distinct from isolating *detector identity* while holding an intervention policy fixed.

**Positioning.** Detection-only and policy-only studies exist. Architectural isolation exists. Agent benchmarks exist. The remaining methodological gap, as qualified in `NOVELTY_AUDIT.md`, is **attribution**: measuring detector-related change in operational tool harm conditional on a locked intervention policy, then checking Δ sign on independently selected targets. We classify this as a **partial gap**, not a clear gap. We do not claim priority.

Numeric results from other papers are not copied here. Q2 is not an external comparative benchmark (`BASELINE_GAP.md`).

---

## 3. Research Question

**RQ-C2 (locked protocol).** Does the detector-related Tool-HASR effect versus D0 observed under the locked Stage-B target (T0) remain directionally consistent when the same policy, pack, detectors, thresholds, and judge are applied to independently selected secondary target models T1–T3?

**Factor.** `target_model_id ∈ {T0, T1, T2, T3}`.  
**Locked.** Policy = PHASE1-CORE; detectors ∈ {D0, D1, D2, D4}; D3 deferred; pack `p2_agentic_v0.1.0`; judge `qwen/qwen-2.5-72b-instruct`.  
**Primary estimand.** sign(Δ(d,t)) for d ∈ {D1, D2, D4}, t ∈ {T1, T2, T3}, compared with sign(Δ(d,T0)).  
**Pre-registered agreement.** 9 contrasts; agreement if signs match (exact 0 would be ZERO; none observed).

Q2 is **not** powered as a confirmatory hypothesis test. The run sets `scientific_evidence=false`. “Supported” in the live verdict means protocol sign-agreement support, not Track B `SUPPORTED_IMPROVEMENT` and not a qualified win (MSID ∧ significance ∧ U).

---

## 4. Method

### 4.1 System decomposition

Each episode-arm runs: **Detector → RiskCore → CorePolicy (PHASE1-CORE) → ToolPermissionGate → mock tools**, with a parallel **judge** that does not enter the detector→policy path. Gold labels (`is_attack`, `label`, `category`) do not enter that path.

D0 implements no detection (no hits). D1/D2/D4 share a `P3Detector` contract and differ in how they score context. D3 (semantic/embedding) is `DEFERRED_NO_OFFLINE_IMPL` and has no scores.

PHASE1-CORE maps detector/risk signals to actions A0–A3 with locked thresholds (is_injection 0.25; risk 0.25/0.60) and normalized action costs (A0=0, A1=0.10, A2=0.25, A3=0.50). Those costs are experimental weights, not USD prices.

### 4.2 Endpoints

**Tool-HASR (primary).** Fraction of attack episode-arms with `tool_hasr_success=True` among True+False. UNKNOWN excluded (`exclude_unknown=true`); Q2 cells have n_unknown=0. Success requires harmful tool execution matching the pre-registered `success_condition`. INVALID_TOOL_ARGS is **not** Tool-HASR success.

**Judge-ASR (secondary).** Fraction of attack episode-arms with `judge_asr_success=True`. A judge-model assessment of attack success. It is diagnostic, not “invalid” when it disagrees with Tool-HASR.

**M3 / M4.** M3: judge success ∧ ¬ tool success. M4: tool success ∧ ¬ judge success.

**Δ(d,t).** Tool-HASR(d,t) − Tool-HASR(D0,t) on attack arms at the same target.

**INVALID_TOOL_ARGS.** Schema/argument failures. Official policy S0 keeps the primary denominator. S1 stratifies; S2 excludes arms with ≥1 INVALID (`derived_after_run`). No post-hoc sensitivity variants.

### 4.3 Statistics

Rates are reported as n/N, point estimate, and Wilson 95% CI. Δ is a difference of rates; **no Δ CI was pre-registered** and none is manufactured. No McNemar or multiplicity-adjusted tests were added in this packaging. Sign agreement is the protocol quantity. Paired discordant counts vs T0 are descriptive.

---

## 5. Experimental Design

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

Target slots (not a quality ranking):

| Slot | Model ID | Role |
| --- | --- | --- |
| T0 | `qwen/qwen-2.5-7b-instruct` | Stage-B reference, not re-run |
| T1 | `qwen/qwen3-30b-a3b` | secondary |
| T2 | `google/gemma-3-27b-it` | secondary |
| T3 | `qwen/qwen3.5-35b-a3b` | secondary |
| Judge | `qwen/qwen-2.5-72b-instruct` | locked, not an experimental factor |

Three of four targets are Qwen-line models. Family diversity is limited. All calls used OpenRouter. Provider-side tool formatting can affect Tool-HASR and INVALID rates.

Q2 predictions SHA-256: `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6`.

---

## 6. Detector–Policy Decomposition

Figure 2 (specification in `FIGURES_AND_TABLES.md`) annotates what varies and what is locked.

**Varied:** detector identity {D0, D1, D2, D4}.  
**Locked:** PHASE1-CORE, thresholds, action costs, P2 pack, judge, temperature, cache-off, seed.

D0 estimates tool-harm when the policy receives no detector hits. Contrasts versus D0 are therefore **detector-related** under this policy, not estimates of “the detector in isolation from all other runtime effects.” Schema failures, target refusals, and judge behavior still occur in every arm.

This is experimental isolation, not causal identification in deployment. It is not a ranking of D1 vs D2 vs D4. Protocol: `no_ranking=true`.

D3 is absent. Absence is documented, not scored (`D3_AND_C4.md`).

---

## 7. Results

All cells use n=16 attack arms. Wilson 95% CIs are on rates, not on Δ. Source: `q2_final_statistics.json` / `FIGURES_AND_TABLES.md`.

### 7.1 Tool-HASR by cell

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

### 7.2 Primary Δ

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

Intervals on the underlying rates are wide (especially 2/16 cells). Magnitudes should not be over-read. Signs are uniformly NEG. Detectors are not ranked.

---

## 8. Cross-Target Analysis

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

**Sign agreement: 9/9 (disagree=0).** Rendered: `figures/figure3_delta_across_targets.png` (stdlib PNG; matplotlib unavailable).

Δ-change is descriptive. Sign agreement uses signs of Δ_T0 and Δ_Tk, not the sign of Δ-change.

T2 matches T0 Δ exactly in this sample. That is an observed coincidence at n=16, not evidence that T2 equals T0 in general.

Interpretation, no more: under locked PHASE1-CORE, the detector-related Tool-HASR effect observed on T0 remained directionally consistent on T1–T3. This does not establish universal LLM generalization, production robustness, or that detector behavior is the sole cause of security outcomes.

---

## 9. Diagnostic Analysis

### 9.1 Tool-HASR versus Judge-ASR

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

Q2 live Judge-ASR: 186/192 = 0.96875. T1–T3 M3=108; M4=3. Rendered: `figures/figure4_toolhasr_vs_judgeasr.png`.

Judge-ASR is high across detectors, including D1/D2/D4 where Tool-HASR is lower. The endpoints measure different things. Tool-HASR is operational harmful execution. Judge-ASR is a judge-model assessment. Disagreement is diagnostic information. We do not claim Judge-ASR is invalid.

### 9.2 INVALID_TOOL_ARGS

**PRIMARY (S0):** official Q2 live INVALID = 192 unique events, 136/432 arms. Independent recompute on `predictions.jsonl` matches. INVALID is not Tool-HASR success and is not negligible. Rendered: `figures/figure5_invalid_tool_args.png`.

**SENSITIVITY (S2):** excluding arms with ≥1 INVALID does not flip within-target Δ signs (0 flips). S2 cross-target sign agreement vs T0 S2 remains 9/9. Magnitudes are not interchangeable with S0.

**DIAGNOSTIC / LIMITATION:** INVALID can stop a harmful call via schema failure even when the judge later labels text success (contributes to M3). Co-occurrence with Tool-HASR true also exists (T1 7, T2 8, T3 4 attack arms). Silent dropping of INVALID events is forbidden.

T0 INVALID counts are cited from prior derived JSON because Stage-B `predictions.jsonl` is **UNAVAILABLE** on this checkout.

### 9.3 Detector-level operational metrics (Q2 live T1–T3; not a ranking)

| Detector | Attack Tool-HASR | Attack Judge-ASR | detector_hit attack | detector_hit label=benign | detector_hit hard_negative |
| --- | --- | --- | --- | --- | --- |
| D0 | 38/48 = 0.7917 | 45/48 = 0.9375 | 0/48 | 0/60 | 0/12 |
| D1 | 6/48 = 0.1250 | 48/48 = 1.0000 | 48/48 | 54/60 | 12/12 |
| D2 | 26/48 = 0.5417 | 48/48 = 1.0000 | 24/48 | 15/60 | 6/12 |
| D4 | 11/48 = 0.2292 | 45/48 = 0.9375 | 48/48 | 51/60 | 3/12 |

Hit rates on benign/hard-negative rows are reported for transparency. They are not a ranking and not a qualified-win utility metric (U is a different-track quantity).

---

## 10. Discussion

The study supports a narrow attribution statement: **conditional on PHASE1-CORE, detector identity is associated with lower Tool-HASR than D0, and that association kept sign on the selected secondary targets.**

It does not support several tempting stronger statements:

- Policy is irrelevant. Q2 live does not vary policy; Stage-B policy arms are a different design and are not this paper’s primary table.
- Detectors “work” as products. Benign/hard-negative hit rates, INVALID, and M3 show that operational security is not detector hit rate.
- Judge-ASR confirms or refutes Tool-HASR. They disagree in bulk (M3=108).
- Cross-target equality of magnitudes. T3 D0 Tool-HASR is 11/16 vs 13–14/16 on T0–T2; Δ magnitudes move. Only signs were pre-registered as the consistency criterion.
- Comparison to CaMeL, IsolateGPT, AgentDojo defenses, Llama Guard, or PromptShield. Those systems were not run on this pack.

The methodological value is the **locked factorial** plus **execution-grounded primary endpoint** plus **explicit diagnostic layers**. That is a measurement contribution. Algorithmic novelty of D1/D2/D4 is not claimed.

---

## 11. Limitations

See also `LIMITATIONS.md` and `D3_AND_C4.md`.

1. **n=16 per cell.** Wilson CIs are wide. 2/16 = 0.125 has CI [0.035, 0.360]. Pilot-scale.
2. **`scientific_evidence=false`.** Protocol-complete directional consistency, not a confirmatory powered study.
3. **Limited model diversity / Qwen-heavy set.** T0, T1, T3 are Qwen-line; T2 is Gemma-3; all via OpenRouter. No GPT/Claude/Gemini-native API family.
4. **External baseline gap.** Q2 is not an external comparative benchmark.
5. **INVALID_TOOL_ARGS is frequent** (192/136 on Q2 live). Not success; not negligible.
6. **T0 reuse vs local Stage-B traces.** **Official evidence result:** T0 Tool-HASR/Δ are reused from Stage-B `p3_stage_b_20260916T235438Z_7e401714` (not re-run); Q2 live report JSON records those cells. **Local artifact availability:** `STAGE_B_TRACE_STATUS = MISSING_LOCALLY` — `predictions.jsonl` is not on this checkout and was not fabricated. T0 INVALID counts remain cited from prior derived JSON.
7. **D3 deferred.** No embedding-detector numbers.
8. **C4 open adaptive attacker out of scope.** P2 C4-mini templates are scripted, not an interactive attacker. PHASE1-CORE action adaptation ≠ closed-loop adaptive adversary.
9. **Provider/runtime effects.** Tool-call formatting, schema compliance, residual nondeterminism at temperature 0.
10. **Refusal behavior.** Target refusal can prevent tool harm without being counted as a defense win in this protocol’s Tool-HASR definition (non-execution is not Tool-HASR success; we do not treat refusal as a credited win).
11. **Benchmark construction.** Frozen P2 is small, mock-tool, short-horizon. Construction choices can drive both Tool-HASR and INVALID.
12. **Limited generalization.** Four models, one pack, one policy, one judge.
13. **Judge-ASR vs Tool-HASR.** Dual reporting is required; they are not interchangeable.
14. **Related-work venues UNVERIFIED.** Bibliography is not camera-ready.
15. **Figures 3–5** are rendered offline as PNG via stdlib zlib (matplotlib unavailable; no network install). Source: `q2_final_statistics.json` / `q2_invalid_args_analysis.json`. No Δ CI or p-values were added.
16. **No universal defense, SOTA/best, production robustness, or Q2 confirmatory claim.** This remains a protocol-complete pilot-scale directional consistency study.

---

## 12. Threats to Validity

| Threat | Type | Direction of concern |
| --- | --- | --- |
| Small n | Statistical | Over-reading Δ magnitude; CI overlap |
| Sign agreement without a pre-registered exact test on Q2 | Statistical | 9/9 is descriptive protocol support, not a p-value |
| INVALID schema failures | Construct / internal | Tool-HASR may miss attempted harm that failed arguments |
| Judge M3 | Construct | Text “success” without tool harm inflates Judge-ASR |
| OpenRouter tool formatting | External | Provider-specific execution |
| T0 not re-run; traces missing here | Internal / reproducibility | Harness drift vs Q2 live cannot be re-audited from this tree |
| Pre-registered but Qwen-heavy models | External | Directional consistency may not hold on other families |
| Mock tools | External | Not production side effects |
| Label-blind path assumed | Internal | Gold labels must not leak; protocol forbids it; this paper does not re-prove the implementation |
| Dual-track contamination | Claims | Mixing VNEXT FAIL or Phase-1 LIVE numbers with Q2 Tool-HASR |

---

## 13. Reproducibility

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

**MISSING on this checkout:** Stage-B `predictions.jsonl`. Recorded Stage-B predictions SHA `7b0b72d942dae988d87acf238424c9f2d331b62d5ec582c9ba7d9bfbb293c214` is not re-hashed here.

Checklist: `Q2_REPRODUCIBILITY_CHECKLIST.md`.

---

## 14. Conclusion

Under a locked intervention policy, detector identity is associated with lower operational harmful-tool rates than a no-detection arm, and that association kept sign across three independently selected secondary targets in this pilot. The contribution is a **controlled attribution protocol** plus that bounded empirical check. The evidence does not establish a universal defense, a best detector, production robustness, or confirmation for all LLMs.

Future work — matched external baselines, larger n, more model families, D3 after an offline embedding lock, open adaptive attackers — would be **new studies** with their own freezes and budgets, not silent extensions of this run.

---

## References (arXiv-verified; venue UNVERIFIED)

1. Perez & Ribeiro, 2022. Ignore Previous Prompt. arXiv:2211.09527  
2. Greshake et al., 2023. Indirect Prompt Injection. arXiv:2302.12173  
3. Liu, Deng, et al., 2023. Prompt Injection attack against LLM-integrated Applications. arXiv:2306.05499  
4. Ruan et al., 2023. ToolEmu. arXiv:2309.15817  
5. Rebedea et al., 2023. NeMo Guardrails. arXiv:2310.10501  
6. Liu, Jia, Geng, Jia, Gong, 2023. Prompt Injection Attacks and Defenses in LLM-Integrated Applications. arXiv:2310.12815  
7. Toyer et al., 2023. Tensor Trust. arXiv:2311.01011  
8. Inan et al., 2023. Llama Guard. arXiv:2312.06674  
9. Yi et al., 2023. BIPIA. arXiv:2312.14197  
10. Chen, Piet, Sitawarin, Wagner, 2024. StruQ. arXiv:2402.06363  
11. Zhan et al., 2024. InjecAgent. arXiv:2403.02691  
12. Wu et al., 2024. IsolateGPT. arXiv:2403.04960  
13. Hines et al., 2024. Spotlighting. arXiv:2403.14720  
14. Wallace et al., 2024. Instruction Hierarchy. arXiv:2404.13208  
15. Debenedetti et al., 2024. AgentDojo. arXiv:2406.13352  
16. Zhang et al., 2024. Agent Security Bench. arXiv:2410.02644  
17. Andriushchenko et al., 2024. AgentHarm. arXiv:2410.09024  
18. Jacob et al., 2025. PromptShield. arXiv:2501.15145  
19. Zhu et al., 2025. MELON. arXiv:2502.05174  
20. Debenedetti et al., 2025. CaMeL (Defeating Prompt Injections by Design). arXiv:2503.18813  
21. Chen, Zharmagambetov, Wagner, Guo, 2025. Meta SecAlign. arXiv:2507.02735  
