# Q2 INVALID_TOOL_ARGS analysis

**Official primary result unchanged (S0).** Denominator not redefined.  
**API calls this task:** 0. **Q2 raw traces:** read-only.

Recompute used `count_invalid_tool_arg_events` on `predictions.jsonl` (432 Q2 live arms) and compared `event_trace.jsonl` security_events. T0 Stage-B `predictions.jsonl` is **not present** on this checkout; T0 counts are cited from the prior derived package (`q2_invalid_args_analysis.json`), not re-derived here.

## Separation of layers

| Layer | What it is | What it is not |
| --- | --- | --- |
| **PRIMARY RESULT** | S0 Tool-HASR / Δ(d,t) on all attack arms (n=16 per cell) | Sensitivity after dropping INVALID arms |
| **SENSITIVITY ANALYSIS** | Pre-specified S1 (stratify) and S2 (exclude arms with ≥1 INVALID); `derived_after_run`; does not replace official | A new primary endpoint |
| **DIAGNOSTIC LIMITATION** | INVALID is frequent; schema/compliance noise can prevent harmful execution without counting as Tool-HASR success | Proof that Tool-HASR is biased, or license to drop events silently |

Protocol lock: `invalid_tool_args_policy()` in `src/adapti_guard/experiments/p3_stage_c_q2.py` (reuse of Q1/P3 S0/S1/S2). INVALID **does not** count as Tool-HASR failure or success; it is a separate execution state.

## PRIMARY RESULT (S0) — official INVALID incidence

Official Q2 live (`metrics.json`): `invalid_tool_args_count=192`, method `per_arm_event_id_dedup_security_events`.

Independent recompute on Q2 `predictions.jsonl` (this task):

| Target | Raw events (no event_id dedup) | Deduped events | Arms with ≥1 | Attack arms with ≥1 | Trajectories | Attack ∩ Tool-HASR true / false |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| T1 | 62 | 62 | 41 | 19 | 16 | 7 / 12 |
| T2 | 62 | 62 | 46 | 22 | 16 | 8 / 14 |
| T3 | 68 | 68 | 49 | 21 | 17 | 4 / 17 |
| T1–T3 | 192 | 192 | 136 | 62 | — | — |

`event_trace.jsonl` security_events: raw 192, unique `event_id` 192, arms 136. Matches official 192/136.

Raw = deduped on Q2 live: no within-arm duplicate INVALID `event_id`s in this run. `live_stats.json` `notes` still **inflate** (repeated strings) and must not be used as the official count.

### Affected detector / policy arms (Q2 live; policy = PHASE1-CORE only)

Arms with ≥1 INVALID (not event counts):

| Target | D0 | D1 | D2 | D4 |
| --- | ---: | ---: | ---: | ---: |
| T1 | 13 | 5 | 9 | 14 |
| T2 | 15 | 8 | 13 | 10 |
| T3 | 16 | 8 | 14 | 11 |

Event-level `event_trace` INVALID by detector (T1–T3): D0=63, D1=30, D2=53, D4=46 (sum 192). Do not interpret as a detector ranking.

### T0 (Stage-B; not recomputed this checkout)

Cited prior derived (PHASE1-CORE): 61 deduped events, 39 arms, 14 attack arms, 15 trajectories, attack Tool-HASR true/false = 5/9. **Reproducibility caveat:** Stage-B `predictions.jsonl` is missing from this branch.

## Can INVALID alter Tool-HASR interpretation?

**PRIMARY:** No. Tool-HASR success requires harmful tool execution matching `success_condition`. INVALID is not success. Official attack denominators stay 16/cell.

**DIAGNOSTIC:** Yes, as a limitation. INVALID can stop a harmful call from executing (schema fail) even when the judge later labels text success (M3). Co-occurrence with Tool-HASR true also exists (T1 7, T2 8, T3 4 attack arms): INVALID somewhere on the trajectory does not imply Tool-HASR false.

Do not claim INVALID is negligible. Do not silently drop INVALID events from S0.

## SENSITIVITY (pre-specified S1 / S2)

From locked live report / `q2_final_statistics.json` `invalid_sensitivity` (not a new test):

- **S1:** Δ among attack arms with zero INVALID vs ≥1 INVALID — descriptive strata; unequal n; not official.
- **S2:** recompute Δ after excluding arms with ≥1 INVALID; `derived_after_run`.
- Within-target S0→S2 **sign flips: 0**.
- S2 cross-target sign agreement vs T0 S2: **9/9**.

S2 Δ magnitudes differ from S0 (denominators shrink, e.g. T0 D1 S2 uses 13 vs 10 attack arms). Magnitudes are **not** interchangeable with official Δ. Only sign stability is used as a diagnostic.

**Conclusion:** The primary NEG Δ / 9/9 sign-agreement claim is **stable** under locked S2. INVALID remains a reported limitation.

## What was not done

- No new sensitivity variants (protocol: `no_post_hoc_sensitivity_variants`).
- No change to official primary denominator.
- No live API calls.
