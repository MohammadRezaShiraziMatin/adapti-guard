# FINAL Security Metric Analysis

**Date:** 2026-09-17. **API_CALLS=0.**

## METRIC_INTERPRETATION_STATUS = DISTINCT_DIAGNOSTIC_RETAINED

## Tool-HASR (primary)

Actual harmful tool execution: attack arms with tool execution matching a pre-registered success_condition. Measures what the agent *did*.

## Judge-ASR (secondary)

Judge-assessed harmfulness: a judge model classifies whether the trajectory constitutes a successful attack. Related but non-identical to Tool-HASR.

## Q2 observed values (T1-T3)

- Tool-HASR: 81/192 = 0.421875
- Judge-ASR: 186/192 = 0.96875
- M3 (judge success, no tool success): 108
- M4 (tool success, no judge success): 3

## Why they diverge (trace-supported, no speculation)

- Model refusal: target may refuse (Tool-HASR false) but judge may label text a successful attack (M3).
- Tool execution state: blocked or not executed.
- INVALID_TOOL_ARGS: can prevent harmful execution.
- Judge interpretation: trajectory-level semantics, not execution state.
- Target-model behavior; runtime/provider formatting.

## Key distinction

Judged harmfulness and actual harmful tool execution are different operational outcomes. Neither metric is declared invalid. Tool-HASR remains primary. The discrepancy is a methodological diagnostic.

Detailed: `docs/SECURITY_METRIC_INTERPRETATION.md`.
