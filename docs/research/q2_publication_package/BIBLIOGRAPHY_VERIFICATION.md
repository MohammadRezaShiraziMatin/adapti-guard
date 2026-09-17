# Bibliography verification

**Bibliography verification pass with network access authorized for bibliographic verification only.**
**Sources: arXiv API (export.arxiv.org) + doi.org + ACL Anthology + ICLR/OpenReview + author publication pages.**
**Date:** 2026-09-17.

**Overall:** `BIBLIOGRAPHY_STATUS = PARTIALLY_VERIFIED`

21/21 identities VERIFIED from arXiv API. 3/21 FULLY_VERIFIED (identity + venue + DOI from official source). 2/21 venue VERIFIED from official conference page (no DOI). 1/21 venue VERIFIED from author publication page. 7/21 venue VERIFIED from arXiv comment field. 8/21 remain preprint-only (VENUE_UNVERIFIED). The 2 operator-supplied DOIs are now independently VERIFIED from doi.org.

| # | citation key | title | authors | year | arXiv | DOI | venue | pub type | venue verification | DOI verification | status | notes |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `perez_ribeiro_2022` | Ignore Previous Prompt: Attack Techniques For Language Models | Fábio Perez et al. | 2022 | `2211.09527` | UNVERIFIED | NeurIPS 2022 ML Safety Workshop | workshop | VERIFIED_VIA_ARXIV_COMMENT | DOI_UNVERIFIED | PARTIALLY_VERIFIED | Venue from arXiv comment: "ML Safety Workshop NeurIPS 2022". Workshop, not main conference. |
| 2 | `greshake_ipi_2023` | Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection | Kai Greshake et al. | 2023 | `2302.12173` | UNVERIFIED | UNVERIFIED | preprint | VENUE_UNVERIFIED | DOI_UNVERIFIED | PARTIALLY_VERIFIED | arXiv preprint. No venue listed on arXiv. |
| 3 | `liu_houyi_2023` | Prompt Injection attack against LLM-integrated Applications | Yi Liu et al. | 2023 | `2306.05499` | UNVERIFIED | UNVERIFIED | preprint | VENUE_UNVERIFIED | DOI_UNVERIFIED | PARTIALLY_VERIFIED | arXiv preprint. No venue listed on arXiv. |
| 4 | `ruan_toolemu_2023` | Identifying the Risks of LM Agents with an LM-Emulated Sandbox | Yangjun Ruan et al. | 2023 | `2309.15817` | UNVERIFIED | UNVERIFIED | preprint | VENUE_UNVERIFIED | DOI_UNVERIFIED | PARTIALLY_VERIFIED | arXiv preprint. No venue listed on arXiv. |
| 5 | `rebedea_nemo_2023` | NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails | Traian Rebedea et al. | 2023 | `2310.10501` | UNVERIFIED | EMNLP 2023 Demo track | demo | VERIFIED_VIA_ARXIV_COMMENT | DOI_UNVERIFIED | PARTIALLY_VERIFIED | Venue from arXiv comment: "Accepted at EMNLP 2023 - Demo track". |
| 6 | `liu_formalize_2023` | Formalizing and Benchmarking Prompt Injection Attacks and Defenses | Yupei Liu et al. | 2023 | `2310.12815` | UNVERIFIED | USENIX Security Symposium 2024 | conference | VERIFIED_VIA_ARXIV_COMMENT | DOI_UNVERIFIED | PARTIALLY_VERIFIED | Venue from arXiv comment: "Published in USENIX Security Symposium 2024". |
| 7 | `toyer_tensortrust_2023` | Tensor Trust: Interpretable Prompt Injection Attacks from an Online Game | Sam Toyer et al. | 2023 | `2311.01011` | UNVERIFIED | UNVERIFIED | preprint | VENUE_UNVERIFIED | DOI_UNVERIFIED | PARTIALLY_VERIFIED | arXiv preprint. No venue listed on arXiv. |
| 8 | `inan_llamaguard_2023` | Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations | Hakan Inan et al. | 2023 | `2312.06674` | UNVERIFIED | UNVERIFIED | preprint | VENUE_UNVERIFIED | DOI_UNVERIFIED | PARTIALLY_VERIFIED | arXiv preprint. No venue listed on arXiv. |
| 9 | `yi_bipia_2023` | Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models | Jingwei Yi et al. | 2023 | `2312.14197` | 10.1145/3690624.3709179 | KDD 2025 | conference | VERIFIED (doi.org) | VERIFIED (doi.org) | FULLY_VERIFIED | DOI verified from doi.org: proceedings-article, ACM SIGKDD. arXiv comment confirms KDD 2025. |
| 10 | `chen_struq_2024` | StruQ: Defending Against Prompt Injection with Structured Queries | Sizhe Chen et al. | 2024 | `2402.06363` | UNVERIFIED | USENIX Security Symposium 2025 | conference | VERIFIED_VIA_ARXIV_COMMENT | DOI_UNVERIFIED | PARTIALLY_VERIFIED | Venue from arXiv comment: "To appear at USENIX Security Symposium 2025". |
| 11 | `zhan_injecagent_2024` | InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents | Qiusi Zhan et al. | 2024 | `2403.02691` | 10.18653/v1/2024.findings-acl.624 | ACL 2024 Findings | conference (findings) | VERIFIED (ACL Anthology) | VERIFIED (ACL Anthology) | FULLY_VERIFIED | DOI verified from aclanthology.org/2024.findings-acl.624. Pages 10471-10506. |
| 12 | `wu_isolategpt_2024` | IsolateGPT: An Execution Isolation Architecture for LLM-Based Agentic Systems | Yuhao Wu et al. | 2024 | `2403.04960` | UNVERIFIED | NDSS 2025 | conference | VERIFIED_VIA_ARXIV_COMMENT | DOI_UNVERIFIED | PARTIALLY_VERIFIED | Venue from arXiv journal_ref + comment: NDSS 2025. |
| 13 | `hines_spotlighting_2024` | Defending Against Indirect Prompt Injection Attacks With Spotlighting | Keegan Hines et al. | 2024 | `2403.14720` | UNVERIFIED | UNVERIFIED | preprint | VENUE_UNVERIFIED | DOI_UNVERIFIED | PARTIALLY_VERIFIED | arXiv preprint. No venue listed on arXiv. |
| 14 | `wallace_instruction_hierarchy_2024` | The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions | Eric Wallace et al. | 2024 | `2404.13208` | UNVERIFIED | UNVERIFIED | preprint | VENUE_UNVERIFIED | DOI_UNVERIFIED | PARTIALLY_VERIFIED | arXiv preprint. No venue listed on arXiv. |
| 15 | `debenedetti_agentdojo_2024` | AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents | Edoardo Debenedetti et al. | 2024 | `2406.13352` | 10.52202/079017-2636 | NeurIPS 2024 | conference | VERIFIED (doi.org) | VERIFIED (doi.org) | FULLY_VERIFIED | DOI verified from doi.org: proceedings-article, NeurIPS Foundation. Title: "AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents". |
| 16 | `zhang_asb_2024` | Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents | Hanrong Zhang et al. | 2024 | `2410.02644` | UNVERIFIED | ICLR 2025 | conference | VERIFIED (ICLR poster page + OpenReview V4y0CpX4hK) | DOI_UNVERIFIED | PARTIALLY_VERIFIED | Venue verified from ICLR 2025 poster page and OpenReview. ICLR papers typically have no DOI. |
| 17 | `andriushchenko_agentharm_2024` | AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents | Maksym Andriushchenko et al. | 2024 | `2410.09024` | UNVERIFIED | ICLR 2025 | conference | VERIFIED (OpenReview AC5n7xHuR1 + ICLR proceedings) | DOI_UNVERIFIED | PARTIALLY_VERIFIED | Venue verified from OpenReview and ICLR 2025 proceedings. |
| 18 | `jacob_promptshield_2025` | PromptShield: Deployable Detection for Prompt Injection Attacks | Dennis Jacob et al. | 2025 | `2501.15145` | UNVERIFIED | ACM CODASPY 2025 | conference | VERIFIED_VIA_ARXIV_COMMENT | DOI_UNVERIFIED | PARTIALLY_VERIFIED | Venue from arXiv comment: "ACM CODASPY 2025". |
| 19 | `zhu_melon_2025` | MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents | Kaijie Zhu et al. | 2025 | `2502.05174` | UNVERIFIED | ICML 2025 | conference | VERIFIED_VIA_ARXIV_COMMENT | DOI_UNVERIFIED | PARTIALLY_VERIFIED | Venue from arXiv comment: "ICML 2025". |
| 20 | `debenedetti_camel_2025` | Defeating Prompt Injections by Design | Edoardo Debenedetti et al. | 2025 | `2503.18813` | UNVERIFIED | SaTML 2026 (accepted) | conference (accepted, currently preprint) | VERIFIED (author publication page floriantramer.com) | DOI_UNVERIFIED | PARTIALLY_VERIFIED | Venue verified from author's publication page: IEEE SaTML 2026. Currently arXiv preprint. |
| 21 | `chen_meta_secalign_2025` | Meta SecAlign: A Secure Foundation LLM Against Prompt Injection Attacks | Sizhe Chen et al. | 2025 | `2507.02735` | UNVERIFIED | UNVERIFIED | preprint | VENUE_UNVERIFIED | DOI_UNVERIFIED | PARTIALLY_VERIFIED | arXiv preprint. No venue listed on arXiv. |

## Verification summary

| Category | Count | References |
| --- | ---: | --- |
| FULLY_VERIFIED (identity + venue + DOI from official source) | 3 | BIPIA (doi.org), AgentDojo (doi.org), InjecAgent (ACL Anthology) |
| VENUE_VERIFIED from official conference/page (no DOI) | 2 | ASB (ICLR poster/OpenReview), AgentHarm (ICLR/OpenReview) |
| VENUE_VERIFIED from author publication page | 1 | CaMeL (SaTML 2026, floriantramer.com) |
| VENUE_VERIFIED via arXiv comment | 7 | Perez&Ribeiro, NeMo, Liu 2310.12815, StruQ, IsolateGPT, PromptShield, MELON |
| VENUE_UNVERIFIED (preprint) | 8 | Greshake, Liu 2306, Ruan/ToolEmu, Toyer, Inan/Llama Guard, Hines/Spotlighting, Wallace, Meta SecAlign |

## Operator-supplied DOI re-check

| Reference | Operator-supplied | Independent re-check | Result |
| --- | --- | --- | --- |
| AgentDojo (2406.13352) | NeurIPS 2024, 10.52202/079017-2636 | doi.org: proceedings-article, NeurIPS Foundation | **VERIFIED** |
| BIPIA (2312.14197) | KDD 2025, 10.1145/3690624.3709179 | doi.org: proceedings-article, ACM SIGKDD | **VERIFIED** |

## Names inspected, not in the verified 21-record bibliography

Task Shield, Adaptive Attacks, AutoDojo, SCOUT, AgentAntibody, HARD, ARGUS, VIGIL, AttriGuard, MCP-SafetyBench, Runtime Policy Enforcement for MCP Agents are **NOT_IN_PACKAGE**. Not added as citations. Metadata not invented.

**NOVELTY_CLASS = PARTIAL_GAP** remains. Full-text novelty exclusion is not claimed.
