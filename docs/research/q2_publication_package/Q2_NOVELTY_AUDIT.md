# Q2 Novelty Audit

**API_CALLS=0. NETWORK_CALLS=0. LIVE_EVAL=false.**
Source: `RELATED_WORK_MATRIX.json` (21 records; identity VERIFIED from existing package Hub metadata).
**NOVELTY_STATUS = PARTIAL_GAP** (unchanged).

## A. What is already established (surveyed set)

| Area | Examples (arXiv) | Established? |
| --- | --- | --- |
| Prompt injection | Perez & Ribeiro `2211.09527`; Liu et al. `2306.05499`, `2310.12815`; Tensor Trust `2311.01011` | Yes |
| Indirect prompt injection | Greshake et al. `2302.12173`; BIPIA `2312.14197`; InjecAgent `2403.02691` | Yes |
| Agent security benchmarks | AgentDojo `2406.13352`; ASB `2410.02644`; AgentHarm `2410.09024`; ToolEmu `2309.15817` | Yes |
| Agentic attacks | InjecAgent; AgentHarm; BIPIA | Yes |
| Runtime guardrails | NeMo Guardrails `2310.10501`; Llama Guard `2312.06674`; PromptShield `2501.15145` | Yes |
| Detector-based defenses | Llama Guard; PromptShield | Yes |
| Architectural isolation | IsolateGPT `2403.04960`; CaMeL `2503.18813` (published design) | Yes |
| Tool security | InjecAgent; ASB tool stages; ToolEmu | Yes |
| Adaptive attacks / adaptive evaluation | AgentDojo evolving attacks; MELON `2502.05174` | Yes (Q2 C4 open attacker remains out of scope) |

## B. What ADAPTI-GUARD Q2 actually contributes

A **controlled detector-policy attribution protocol**:
1. hold the downstream intervention policy fixed (PHASE1-CORE);
2. vary detector identity, including a no-detection reference (D0);
3. measure Tool-HASR (harmful tool execution) as primary;
4. test whether detector-related Δ relative to D0 preserves sign across independently selected target models;
5. retain Judge-ASR, M3/M4, and INVALID_TOOL_ARGS as diagnostics.

This is **one** methodological contribution with supporting measurements. It is not a new detector family, not a new benchmark, not a SOTA defense, and not a universal security solution. D1/D2/D4 are instantiations under a shared `P3Detector` contract, not novel detector families.

## C. Specific novelty claim tested

> Existing work does not clearly establish the exact controlled factorial attribution of detector identity versus a locked downstream intervention policy using Tool-HASR, with D0 as reference and directional consistency tested across independently selected target models.

**Verdict:** the surveyed set does not establish that exact factorial as a central measurement protocol. The claim is **supported as a partial gap**, not a global uniqueness proof.

**Residual uncertainty (do not paper over):**
1. Full texts of AgentDojo and ASB were not read end-to-end; whether a close cousin appears inside those full texts is not upgraded to a global "no overlap" claim.
2. Venue versions may differ from arXiv abstracts; most venue/DOI fields remain UNVERIFIED.
3. Industry products were not experimentally compared.
4. A CLEAR GAP would require exhaustive search plus full-text confirmation; this audit does not have that. **Do not upgrade to CLEAR GAP.**

## D. External baselines

No fair external baseline exists. No numerical comparison against CaMeL, AgentDojo, ASB, Llama Guard, PromptShield, IsolateGPT, instruction-hierarchy models, or Task Shield is performed. Protocols, populations, metrics, and execution environments differ; cross-paper ASR/HASR copying would be a claims error. Comparative evaluation is **future work**, not a current claim.

## E. Safe novelty sentence for the manuscript

Prior work already provides prompt-injection attacks, agent security benchmarks, dynamic evaluation, defense architectures, architectural isolation, adaptive evaluation, memory/tool security, and runtime security mechanisms. This study does not claim invention of those components. What it adds is a controlled attribution protocol: hold downstream intervention policy, thresholds, pack, and judge fixed; vary detector identity including D0; measure Tool-HASR; and test whether detector-related Δ relative to D0 preserves sign across independently selected target models. Novelty class: **PARTIAL_GAP**.

## F. Names inspected, not in the verified 21-record matrix

Task Shield, Adaptive Attacks, AutoDojo, SCOUT, AgentAntibody, HARD, ARGUS, VIGIL, AttriGuard, MCP-SafetyBench, Runtime Policy Enforcement for MCP Agents are **NOT_IN_PACKAGE**. They are not added as citations; metadata is not invented.
