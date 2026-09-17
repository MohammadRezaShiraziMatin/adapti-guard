# FINAL INVALID_TOOL_ARGS Analysis

**Date:** 2026-09-17. **API_CALLS=0.**

## INVALID_TOOL_ARGS_STATUS = DOCUMENTED_CONFOUNDER_RETAINED

## Counts (Q2 live T1-T3)

- Raw events: 192; deduplicated (event_id): 192; affected arms: 136/432.
- T1: 62 events/41 arms; T2: 62/46; T3: 68/49.
- T0 (Stage-B traces MISSING_LOCALLY): 61 events/39 arms (prior derived record, not recompute).

## Classification

INVALID_TOOL_ARGS is a canonical execution-state category. It is NOT automatically: attack success; attack failure; harmlessness; detector failure.

## Effect on metrics

- Tool-HASR: INVALID can prevent intended tool execution (schema failure stops a harmful call). Co-occurrence with Tool-HASR-true also exists (T1=7, T2=8, T3=4 attack arms).
- Judge-ASR: INVALID can inflate Judge-ASR if judge labels text success despite no tool execution (M3=108).
- Detector/policy asymmetry: event-level INVALID by detector D0=63, D1=30, D2=53, D4=46. Not interpreted as a detector ranking.

## Sensitivity (S0/S1/S2)

- S0 (official): 192 retained; 9/9 sign agreement.
- S1 (stratify): D1/D2/D4 Δ signs remain NEG in both strata.
- S2 (exclude ≥1 INVALID): 9/9 vs T0 S2; 0 S0→S2 flips.
- S2 does not prove INVALID is negligible.

## Decision

Retain all events. Do not delete or silently exclude. Document as confounder. No new experiment required.

Detailed: `docs/research/q2_publication_package/INVALID_TOOL_ARGS_ANALYSIS.md`.
