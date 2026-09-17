# ADAPTI-GUARD Security Metric Interpretation

**Date:** 2026-09-17. **API_CALLS=0.**

## Tool-HASR (primary)

Harmful tool execution behavior: attack arms with tool execution matching a pre-registered success_condition. Measures what the agent *did*, not what a judge *said*.

## Judge-ASR (secondary)

Judge-level attack-success assessment: a judge model classifies whether the trajectory constitutes a successful attack. Related but non-identical to Tool-HASR.

## Q2 observed values (T1-T3)

- Tool-HASR: 81/192 = 0.421875
- Judge-ASR: 186/192 = 0.96875
- M3 (judge success, no tool success): 108
- M4 (tool success, no judge success): 3

## Why they diverge (trace-supported, no speculation)

- Model refusal behavior: target may refuse (Tool-HASR false), but judge may label text a successful attack (Judge-ASR true → M3).
- Tool execution state: blocked or not executed.
- Malformed tool arguments (INVALID_TOOL_ARGS): can prevent harmful execution without counting as Tool-HASR success.
- Judge interpretation: judge assesses trajectory-level semantics, not execution state.
- Target-model behavior: different models format/refuse differently.
- Runtime/provider behavior: OpenRouter tool formatting.

## Key distinction

Judged harmfulness and actual harmful tool execution are different operational outcomes. They answer different questions. Neither metric is declared invalid. Tool-HASR remains primary. The discrepancy is a methodological diagnostic, not a defect to hide.

## INVALID_TOOL_ARGS interaction

192 events / 136 arms. INVALID can prevent intended tool execution (affecting Tool-HASR observability) and can co-occur with Tool-HASR-true arms. INVALID is a canonical execution-state category, not automatic attack success/failure/harmlessness/detector failure. S0/S1/S2 diagnostics are preserved.

Detailed analysis: `docs/research/q2_publication_package/INVALID_TOOL_ARGS_ANALYSIS.md`.
