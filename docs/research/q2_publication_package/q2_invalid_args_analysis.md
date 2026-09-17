# Q2 INVALID_TOOL_ARGS Analysis

**Official primary result unchanged (S0).** Denominator not redefined. API calls this task: 0.

## Separation of layers
1. **Official primary:** S0 Tool-HASR / Δ  
2. **Sensitivity:** S1 stratify / S2 exclude (descriptive; `derived_after_run`)  
3. **Diagnostic:** counts, affected trajs, co-occurrence with Tool-HASR

## Counts by target (PHASE1-CORE)

| Target | INVALID events (per-arm event_id dedup) | Arms w/ INVALID | Attack arms w/ INVALID | Affected trajs |
| --- | ---: | ---: | ---: | ---: |
| T0 | 61 | 39 | 14 | 15 |
| T1 | 62 | 41 | 19 | 16 |
| T2 | 62 | 46 | 22 | 16 |
| T3 | 68 | 49 | 21 | 17 |
| T1–T3 live | 192 | 136 | — | — |

## Materiality to Tool-HASR
INVALID is **not** Tool-HASR success. Official attack denominators unchanged. Co-occurrence is diagnostic (schema/compliance noise may reduce executed harmful tools without counting as HASR success).

## S0 / S1 / S2
- Within-target S0→S2 sign flips: **0** (none)
- S2 cross-target sign agreement vs T0 S2: **{'n_agree': 9, 'n_total': 9}**

**Conclusion:** Primary NEG Δ / 9/9 sign-agreement claim is **stable** under locked sensitivity. INVALID remains frequent and must be reported — do not silently drop events.
