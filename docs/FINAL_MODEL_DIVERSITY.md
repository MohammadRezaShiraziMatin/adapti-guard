# FINAL Model Diversity

**Date:** 2026-09-17. **API_CALLS=0.**

## MODEL_DIVERSITY_STATUS = MODERATE_QWEN_HEAVY

## Targets

| Slot | Model | Family | Architecture | Provider |
| --- | --- | --- | --- | --- |
| T0 | qwen/qwen-2.5-7b-instruct | Qwen-2.5 | dense | OpenRouter |
| T1 | qwen/qwen3-30b-a3b | Qwen3 | MoE | OpenRouter |
| T2 | google/gemma-3-27b-it | Gemma-3 | dense | OpenRouter |
| T3 | qwen/qwen3.5-35b-a3b | Qwen3.5 | MoE | OpenRouter |
| Judge | qwen/qwen-2.5-72b-instruct | Qwen-2.5 | dense | OpenRouter |

## Analysis

- 4 targets; 3 of 4 Qwen-family; 1 non-Qwen (Gemma-3).
- Architectural: 2 dense + 2 MoE.
- Provider: all OpenRouter (single provider).
- Judge also Qwen-family.

## Decision: no additional model required

Model-family diversity is limited. Results should not be generalized to arbitrary model families. No additional live model is scientifically necessary for the current pilot-scale claim.
