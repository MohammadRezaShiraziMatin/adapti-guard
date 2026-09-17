# Q2 limitations (reviewer-facing)

**API calls:** 0. Observed evidence vs interpretation is separated.  
This is a **protocol-complete pilot-scale directional consistency study**. `scientific_evidence=false`.

1. **n=16 per cell.** Wilson CIs are wide (2/16 Tool-HASR CI [0.035, 0.360]). Pilot-scale, not powered for small Δ.
2. **Four targets are Qwen-heavy.** T0/T1/T3 Qwen-line; T2 Gemma-3; judge also Qwen. Limited model diversity. No GPT/Claude/Gemini-native API family.
3. **Limited model diversity.** Four OpenRouter-served models only. Directional consistency is within this selected set.
4. **No matched external defense baseline.** Current Q2 is not an external comparative benchmark (`BASELINE_GAP.md`).
5. **D3 deferred.** `DEFERRED_NO_OFFLINE_IMPL`. No D3 numbers (`D3_AND_C4.md`).
6. **C4 / open adaptive attacker out of scope.** P2 C4-mini is scripted. PHASE1-CORE action adaptation ≠ closed-loop adaptive adversary.
7. **INVALID_TOOL_ARGS are frequent and scientifically relevant.** Q2 live: 192 unique events / 136 arms. Not Tool-HASR success; not negligible; S0 primary unchanged; S2 signs 9/9.
8. **Provider/runtime/model formatting effects.** OpenRouter tool schemas, temp=0 residual nondeterminism.
9. **Refusal behavior.** Refusal is not credited as a defense win. Non-execution is simply not Tool-HASR success.
10. **Tool-call formatting.** Parser/schema failures can stop execution (INVALID) independently of detector hits.
11. **Benchmark-specific effects.** Frozen P2 is mock-tool, short-horizon, small. SHA `32b40e3b…`.
12. **Judge-ASR vs Tool-HASR disagreement.** T1–T3 M3=108, M4=3. Judge-ASR is secondary diagnostic, not invalid, not interchangeable with Tool-HASR.
13. **Stage-B trace availability.** **Official evidence result:** T0 Tool-HASR/Δ reused from `p3_stage_b_20260916T235438Z_7e401714` (Q2 live report). **Local artifact availability:** `STAGE_B_TRACE_STATUS = MISSING_LOCALLY`. Not fabricated.
14. **No claim of universal defense.**
15. **No SOTA / best / ranking claim.** `no_ranking=true`.
16. **No production robustness claim.**
17. **No Q2 confirmatory claim.** `scientific_evidence=false`.

## Threats (short)

| Threat | Direction of concern |
| --- | --- |
| Small n | Over-reading Δ magnitude / CI overlap |
| INVALID | Tool-HASR may miss attempted harm that failed schema |
| Judge M3 | Text success without tool harm inflates Judge-ASR |
| OpenRouter runtime | Provider-specific tool formatting |
| T0 not re-run; traces missing locally | Independent T0 INVALID recompute blocked here; official T0 rates remain in Q2 report JSON |
| Model selection | Pre-registered but Qwen-heavy |
