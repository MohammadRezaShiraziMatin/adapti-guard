# Novelty audit

**API calls:** 0. **Live experiments:** false.  
**Source:** `RELATED_WORK_MATRIX.json` (21 Hub-verified arXiv records) plus Q2 locked protocol.  
**Rule:** do not claim novelty merely because a method looks different. Missing implementation in this repo ≠ new science.

## Central contribution under test

A **controlled framework for isolating detector-related effects from downstream intervention policy** in LLM-agent security, with Tool-HASR as the primary operational endpoint and a bounded cross-target Δ sign check (Q2 / RQ-C2).

This is **one** contribution with supporting measurements. It is not five unrelated algorithmic inventions.

## Explicit tests against prior work

| Question | Already studied in surveyed set? | Evidence | Implication for Q2 |
| --- | --- | --- | --- |
| Detector-only effects | **Yes** | PromptShield (`2501.15145`); Llama Guard (`2312.06674`) | Not novel as “we built a detector.” |
| Policy-only / intervention effects | **Yes** | NeMo Guardrails (`2310.10501`); IsolateGPT (`2403.04960`); CaMeL (`2503.18813`) | Not novel as “we added a runtime policy.” |
| Detector–policy decomposition | **Partial** | CaMeL isolates *control vs data*; IsolateGPT isolates *execution*; AgentDojo/ASB evaluate many defenses | Architectural isolation ≠ experimental factorial with policy locked and detector identity varied. |
| Fixed-policy detector comparison | **Uncertain** | AgentDojo and ASB swap defenses; Hub metadata does not verify a locked intervention policy × detector identity design | Cannot claim “first.” Possible overlap remains. |
| Tool-harm execution as primary endpoint | **Partial** | InjecAgent, AgentDojo, AgentHarm, ASB, ToolEmu all score actions/tools | Tool-HASR is related. Dual Tool-HASR vs Judge-ASR + M3/M4 is a measurement contribution, not a new harm theory. |
| Target-model sensitivity of detector effects | **Uncertain** | ASB ~13 backbones; BIPIA and Liu et al. evaluate many LLMs | Multi-model evals exist. Detector-related Δ vs D0 under locked intervention is not verified in those papers from Hub metadata. |
| Agentic trajectory-level security | **Yes** | AgentDojo, MELON, ToolEmu, AgentHarm | Established. |
| Cross-model consistency under locked intervention policy | **Not found in surveyed set** | No verified paper pre-registers Δ(d,t) sign agreement of detector-vs-D0 Tool-HASR across independently selected secondary targets with one locked policy | Distinctive *protocol*. Not a proof of uniqueness. |

## What is *not* novel

- Prompt-injection threat models (Perez & Ribeiro; Greshake; Liu et al.).
- Guardrail detectors and programmable rails (Llama Guard; NeMo).
- Model-level instruction hierarchy / SecAlign-class training (Wallace et al.; Chen et al. Meta SecAlign).
- Channel separation (StruQ) and spotlighting of untrusted data (Hines et al.).
- Cost-sensitive actions as a general ML idea (A0–A3 here are experimental weights).
- Adaptive *attacker* evaluation (out of Q2 claim scope; C4 open attacker not run).

D1/D2/D4 are **interpretable instantiations** under a shared `P3Detector` contract. They are not claimed as new detector families.

## Residual uncertainty (do not paper over)

1. Full texts of AgentDojo and ASB were **not** read end-to-end in this audit. They may contain defense tables that hold some policy constant.
2. Venue versions may differ from arXiv abstracts.
3. Industry products (Prompt Shields, vendor firewalls) are not academic papers and were not experimentally compared.
4. A “CLEAR GAP” would require exhaustive search plus full-text confirmation. This audit does not have that.

## Classification

**PARTIAL GAP**

- **Supported distinctiveness:** experimental isolation of detector identity under a *locked* agent intervention policy, with Tool-HASR Δ vs a no-detection arm (D0), plus a pre-registered cross-target sign-agreement check on independently selected models.
- **Not a clear gap:** detection, rails, architectural isolation, agent benchmarks, and multi-model evals already exist.
- **Uncertain remainder:** whether AgentDojo/ASB already implemented a close cousin of the factorial.

Do **not** write “first,” “only,” or “CLEAR GAP.”  
Do **not** upgrade this to CLEAR GAP without full-text confirmation of AgentDojo/ASB defense protocols.

## Safe novelty sentence for the manuscript

Prior work studies prompt injection, agent benchmarks, detectors, and architectural isolation. What this study adds is a **controlled attribution protocol**: hold downstream intervention policy, thresholds, pack, and judge fixed; vary detector identity including a no-detection arm; measure operational harmful tool execution (Tool-HASR); and test whether the detector-related Δ sign remains consistent on independently selected target models. That protocol is **partially distinct** from surveyed work; it is **not** a claim of a new universal defense.
