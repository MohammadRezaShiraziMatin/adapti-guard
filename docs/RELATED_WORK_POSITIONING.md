# ADAPTI-GUARD Related Work Positioning

**Date:** 2026-09-17. **NOVELTY_STATUS = DEFENSIBLE_POSITIONING.**

## Contribution (narrow)

Controlled detector-policy attribution for agent security: hold the downstream intervention policy fixed (PHASE1-CORE), vary detector identity including a no-detection reference (D0), measure Tool-HASR as primary operational security outcome, and test whether detector-related Δ versus D0 preserves sign across independently selected target models.

This is NOT a new detector family, NOT a new benchmark, NOT a SOTA defense, NOT a universal security solution.

## Matrix: prior work vs ADAPTI-GUARD

| Work | Year | Problem | Agentic | Detector | Policy | Tool exec | Eval design | Attribution | Relation to ADAPTI-GUARD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Greshake et al. | 2023 | IPI | partial | — | — | — | attack | — | Threat model; not attribution factorial |
| BIPIA (Yi et al.) | 2023 | IPI defense | yes | — | — | — | benchmark | — | Benchmark; not locked-policy factorial |
| InjecAgent (Zhan et al.) | 2024 | IPI tool harm | yes | — | — | yes | benchmark | — | Benchmark; not attribution factorial |
| AgentDojo (Debenedetti et al.) | 2024 | Agent attack/defense | yes | yes | entangled | yes | dynamic | partial | Dynamic env; detector+policy entangled |
| ASB (Zhang et al.) | 2024 | Agent attacks+defenses | yes | yes | entangled | yes | benchmark | — | Benchmark; not locked-policy factorial |
| AgentHarm (Andriushchenko et al.) | 2024 | Agent harmfulness | yes | — | — | yes | benchmark | — | Harmfulness; not detector attribution |
| IsolateGPT (Wu et al.) | 2024 | Execution isolation | yes | — | architectural | yes | defense | — | Architectural; not detector factorial |
| CaMeL (Debenedetti et al.) | 2025 | Control/data isolation | yes | — | architectural | yes | defense | — | Architectural; not detector factorial |
| Llama Guard (Inan et al.) | 2023 | I/O safeguard | no | yes | — | — | detector | — | Detector; not locked-policy attribution |
| PromptShield (Jacob et al.) | 2025 | PI detection | partial | yes | — | — | detector | — | Detector; not locked-policy attribution |
| NeMo Guardrails (Rebedea et al.) | 2023 | Programmable rails | partial | yes | entangled | — | defense | — | Rails entangle detection+policy |
| StruQ (Chen et al.) | 2024 | Structured queries | partial | yes | — | — | defense | — | Defense; not attribution factorial |
| Spotlighting (Hines et al.) | 2024 | Data channeling | partial | yes | — | — | defense | — | Defense; not attribution factorial |
| Instruction Hierarchy (Wallace et al.) | 2024 | Privileged instructions | no | — | model-level | — | training | — | Changes target; violates Q2 design |
| MELON (Zhu et al.) | 2025 | Masked re-execution | yes | yes | — | yes | defense | — | Defense; not locked-policy attribution |
| Meta SecAlign (Chen et al.) | 2025 | Model-level defense | no | — | model-level | — | training | — | Changes target; violates Q2 design |
| **ADAPTI-GUARD Q2** | **2026** | **Detector-policy attribution** | **yes** | **D0/D1/D2/D4** | **PHASE1-CORE locked** | **Tool-HASR** | **controlled factorial** | **yes** | **This study** |

## Closest methodological neighbors

AgentDojo (dynamic env, detector+policy entangled), ASB (benchmark, detector+policy entangled), NeMo Guardrails (rails entangle detection+policy). None locks the downstream intervention policy as the controlled factor while varying detector identity with a D0 reference and measuring Tool-HASR Δ directional consistency across targets.

## Safe novelty sentence

To the best of our literature search, we did not identify prior work that evaluates this exact controlled detector-policy attribution design with cross-target directional consistency using Tool-HASR as the primary outcome.

Full matrix: `docs/research/q2_publication_package/RELATED_WORK_MATRIX.md`.
