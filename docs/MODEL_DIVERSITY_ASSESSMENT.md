# ADAPTI-GUARD Model Diversity Assessment

**Date:** 2026-09-17. **API_CALLS=0.**

## Targets

| Slot | Model | Family | Architecture | Provider |
| --- | --- | --- | --- | --- |
| T0 | qwen/qwen-2.5-7b-instruct | Qwen-2.5 | dense | OpenRouter |
| T1 | qwen/qwen3-30b-a3b | Qwen3 | MoE | OpenRouter |
| T2 | google/gemma-3-27b-it | Gemma-3 | dense | OpenRouter |
| T3 | qwen/qwen3.5-35b-a3b | Qwen3.5 | MoE | OpenRouter |
| Judge | qwen/qwen-2.5-72b-instruct | Qwen-2.5 | dense | OpenRouter |

## Diversity analysis

- 4 targets; 3 of 4 are Qwen-family.
- 1 non-Qwen (Gemma-3).
- Architectural diversity: 2 dense + 2 MoE.
- Provider: all OpenRouter (single provider).
- Judge also Qwen-family.

## MODEL_DIVERSITY_STATUS = MODERATE_QWEN_HEAVY

Model-family diversity is limited. Results should not be generalized to arbitrary model families. Target-model behavior can influence observed tool execution and judge outcomes. Provider-side tool formatting can affect Tool-HASR and INVALID rates.

## Decision: no additional model required

No additional live model is scientifically necessary for the current pilot-scale directional-consistency claim. Adding a model would be a new study, not a silent extension.
