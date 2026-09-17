# Novelty audit

**API calls:** 0. **Live experiments:** false. **NETWORK_CALLS=0.**  
**Source:** `RELATED_WORK_MATRIX.json` (21 records; identity VERIFIED from existing package Hub metadata).  
**NOVELTY_CLASS = PARTIAL_GAP** (unchanged).  
**Rule:** do not claim novelty merely because a method looks different. Missing implementation in this repo ≠ new science. Do not write “first,” “unique,” “no prior work,” or “novel for the first time.”

## Positioning: controlled attribution, not a new defense

The contribution under test is **controlled attribution**, not invention of a new defense algorithm.

A controlled evaluation protocol that:

1. holds the downstream intervention policy fixed (PHASE1-CORE);
2. varies detector identity, including a no-detection arm (D0);
3. measures Tool-HASR (harmful tool execution);
4. tests whether detector-related Δ relative to D0 preserves sign across independently selected target models.

This is **one** methodological contribution with supporting measurements. It is not a claim of a defense covering all threat models.

## What existing literature already provides

The verified literature establishes extensive work on:

| Already provided | Examples in the surveyed set (arXiv) |
| --- | --- |
| Prompt-injection attacks | Perez & Ribeiro `2211.09527`; Liu et al. `2306.05499`, `2310.12815`; Tensor Trust `2311.01011` |
| Indirect prompt injection | Greshake et al. `2302.12173`; BIPIA `2312.14197`; InjecAgent `2403.02691` |
| Agent security benchmarks | AgentDojo `2406.13352`; ASB `2410.02644`; AgentHarm `2410.09024`; ToolEmu `2309.15817` |
| Dynamic evaluation | AgentDojo (identity VERIFIED; NeurIPS 2024 operator-supplied) |
| Defense architectures | CaMeL `2503.18813`; IsolateGPT `2403.04960`; StruQ `2402.06363`; Spotlighting `2403.14720` |
| Architectural isolation | CaMeL (published design, not an unverified idea); IsolateGPT |
| Adaptive attacks / adaptive evaluation | AgentDojo evolving attacks; MELON `2502.05174` (masked re-execution). Q2 C4 open attacker remains out of scope |
| Memory/tool security | ASB tool/memory stages; InjecAgent tool-integrated IPI |
| Runtime security mechanisms | NeMo Guardrails `2310.10501`; Llama Guard `2312.06674`; PromptShield `2501.15145`; Instruction Hierarchy `2404.13208` |

The paper does **not** claim invention of those components. AgentDojo and ASB are **verified papers**, not uncertain citations. CaMeL is a **published architectural defense**, not a rumor.

## Residual gap (narrow)

**NOVELTY_CLASS = PARTIAL_GAP**

> The verified literature establishes extensive work on attacks, benchmarks, defenses, and adaptive evaluation, but does not establish the exact locked-policy detector-attribution factorial used here as the central measurement protocol.

That sentence is the maximum claim. It is **not** a global uniqueness proof. Exact literature gap cannot be claimed globally (`LIMITATIONS.md` item 19).

## Explicit tests against prior work

| Question | Already studied in surveyed set? | Evidence | Implication for Q2 |
| --- | --- | --- | --- |
| Detector-only effects | Yes | PromptShield `2501.15145`; Llama Guard `2312.06674` | Not a new detector family. |
| Policy-only / intervention effects | Yes | NeMo `2310.10501`; IsolateGPT; CaMeL | Not a new runtime policy. |
| Architectural isolation | Yes | CaMeL control/data; IsolateGPT execution | Related class; different mechanism than detector identity under a locked policy. |
| Agent attack/defense benchmarks | Yes | AgentDojo, ASB, InjecAgent, AgentHarm | Established. Paper identities VERIFIED. Not numerical Q2 baselines. |
| Locked-policy detector-attribution factorial as the *central* protocol | Not established in the surveyed set as that central protocol | Matrix + this audit | PARTIAL_GAP. Not “first.” Not “no prior work.” |
| Tool-harm execution as an endpoint | Partial | InjecAgent, AgentDojo, AgentHarm, ASB, ToolEmu score actions/tools | Tool-HASR is related. Dual Tool-HASR vs Judge-ASR + M3/M4 is a measurement layer, not a new harm theory. |
| Cross-model directional Δ vs D0 under one locked policy | Not established as the surveyed papers’ central protocol | — | Distinctive protocol. Not uniqueness. |

## What is *not* novel

- Prompt-injection threat models.
- Guardrail detectors and programmable rails.
- Model-level instruction hierarchy / SecAlign-class training.
- Channel separation and spotlighting.
- Cost-sensitive actions as a general ML idea.
- Adaptive attacker evaluation (out of Q2 claim scope).
- D1/D2/D4 as new detector families (they are instantiations under a shared `P3Detector` contract).

## Residual uncertainty (do not paper over)

1. Full texts of AgentDojo and ASB were not read end-to-end in this audit. Their paper identities are verified; whether a close cousin of the factorial appears inside those full texts is **not** upgraded to a global “no overlap” claim.
2. Venue versions may differ from arXiv abstracts. Most venue/DOI fields remain UNVERIFIED; AgentDojo/BIPIA venue/DOI are operator-supplied and not re-fetched this turn.
3. Industry products were not experimentally compared.
4. A CLEAR GAP would require exhaustive search plus full-text confirmation. This audit does not have that. **Do not upgrade to CLEAR GAP.**

## Safe novelty sentence for the manuscript

Prior work already provides prompt-injection attacks, agent security benchmarks, dynamic evaluation, defense architectures, architectural isolation, adaptive evaluation, memory/tool security, and runtime security mechanisms. This study does not claim invention of those components. What it adds is a **controlled attribution protocol**: hold downstream intervention policy, thresholds, pack, and judge fixed; vary detector identity including D0; measure Tool-HASR; and test whether detector-related Δ relative to D0 preserves sign across independently selected target models. Novelty class: **PARTIAL_GAP**.
