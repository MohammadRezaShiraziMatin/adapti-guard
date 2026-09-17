# Q2 limitations (reviewer-facing)

**API calls:** 0. Observed evidence vs interpretation is separated.

## Model diversity (required)

Only **four target models** were evaluated:

| Slot | ID | Family (lock file) |
| --- | --- | --- |
| T0 | `qwen/qwen-2.5-7b-instruct` | qwen2.5-dense (reference; not re-run) |
| T1 | `qwen/qwen3-30b-a3b` | qwen3-moe |
| T2 | `google/gemma-3-27b-it` | gemma3 |
| T3 | `qwen/qwen3.5-35b-a3b` | qwen3.5-moe |

Judge: `qwen/qwen-2.5-72b-instruct` (not the experimental factor).

Family/architecture diversity is **limited**: three Qwen-line models + one Gemma; all reached via OpenRouter. No closed commercial API family (for example GPT/Claude/Gemini-API-native) is in this set. Provider/runtime behavior (tool-request parsing, schema compliance, temp=0 residual nondeterminism) can affect Tool-HASR and INVALID rates.

**Supports:** directional consistency of Δ sign **within this selected set**.  
**Does not establish:** universal LLM generalization.

## Benchmark size / n=16 per cell

P2: 16 attacks / 16 twins / 4 hard negatives. Wilson CIs on 2/16 cells are wide. P1 (supporting) uses 2 examples per mechanism leaf and is a different pack. Pilot-scale, not powered for small Δ.

## `scientific_evidence=false`

The locked Q2 run is a protocol-complete **pilot** directional-consistency study. It is not a confirmatory multi-model study and not a qualified-win track (MSID ∧ significance ∧ U).

## INVALID_TOOL_ARGS

Frequent on Q2 live (192 deduped events, 136/432 arms). S0 primary denom unchanged; S2 signs stable (9/9). Still a diagnostic limitation (schema/compliance noise). Details: `INVALID_TOOL_ARGS_ANALYSIS.md`. Do not silently drop INVALID events.

## Tool-HASR vs Judge-ASR

Large M3 (108 on T1–T3). Dual-metric reporting is required. Judge-ASR is not invalid; it is a different endpoint. Tool-HASR is operational harmful tool execution. Judge-ASR is a judge-model assessment of attack success.

## D3 deferred

Semantic/embedding detector class: `DEFERRED_NO_OFFLINE_IMPL`. No D3 numbers exist. See `D3_AND_C4.md`.

## C4 scope

Open-ended adaptive attackers are **out of current claim scope**. P1 has C4=0. P2 contains **C4-mini** scripted templates, not an LLM attacker or human red team. PHASE1-CORE adapts actions; that is not a closed-loop adaptive attacker. Do not claim adaptive-attacker robustness. See `D3_AND_C4.md`.

## External baselines

None fairly reconstructed on this pack. Current Q2 is not an external comparative benchmark. See `BASELINE_GAP.md`. Not SOTA.

## Cost

A0–A3 are experimental weights. Token-USD ($0.152885) is Q2 live spend, not validated intervention prices.

## T0 reuse / missing Stage-B traces on this checkout

T0 Tool-HASR/Δ are reused from Stage-B `p3_stage_b_20260916T235438Z_7e401714` (not re-run). This branch does **not** contain Stage-B `predictions.jsonl`. T0 INVALID counts are cited from prior derived JSON. Independent T0 recompute is blocked until those traces are packaged without rewriting them.

## Provider / runtime / tool-call formatting

OpenRouter-mediated tool schemas and parser behavior can induce INVALID_TOOL_ARGS and can change whether a harmful call executes. Results may not transfer to native provider tool APIs.

## Refusal behavior

A target may refuse in text without executing a harmful tool. Refusal is not credited as a defense win. Non-execution is simply not Tool-HASR success. Judge-ASR may still label the transcript as attack success (M3).

## Benchmark construction effects

Frozen P2 is mock-tool, short-horizon, and small. Attack templates and `success_condition` definitions can dominate observed Tool-HASR. Construction is frozen (SHA `32b40e3b…`); it is not a sample from all agent tasks.

## Limited generalization

One pack, one policy (Q2 live), one judge, four targets, mock tools. No human red team in this package.

## Dual-track contamination

Track A VNEXT FAIL and Track B Phase-1 LIVE use different packs and treatments. They must not be pooled with Q2 Tool-HASR.

## Related-work venues

arXiv metadata verified; conference/journal venue UNVERIFIED. Not a camera-ready bibliography.

## Figures

matplotlib was unavailable; figures are specified, not rasterized.

## Threats to validity (short)

| Threat | Direction of concern |
| --- | --- |
| Small n | Over-reading Δ magnitude / CI overlap |
| INVALID | Tool-HASR may miss some attempted harm that failed schema |
| Judge M3 | Text success without tool harm inflates Judge-ASR |
| OpenRouter runtime | Provider-specific tool formatting |
| T0 not re-run | Harness-version drift vs Q2 live (forensic audit reported Stage-B immutable + PASS; traces not in this tree) |
| Model selection | Pre-registered but Qwen-heavy |
