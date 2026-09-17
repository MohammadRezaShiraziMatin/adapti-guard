# Q2 limitations (reviewer-facing)

**API calls:** 0. Observed evidence vs interpretation is separated.  
This is a **protocol-complete pilot-scale directional consistency study**. `scientific_evidence=false`.

1. **n=16 per cell.** Wilson CIs are wide (2/16 Tool-HASR CI [0.035, 0.360]). Pilot-scale, not powered for small Δ.
2. **Four target models only.** Directional consistency is within this selected set.
3. **Qwen-heavy target set.** T0/T1/T3 Qwen-line; T2 Gemma-3; judge also Qwen.
4. **Limited architectural diversity.** Four OpenRouter-served models. No GPT/Claude/Gemini-native API family.
5. **Pilot-scale evidence.** Not a large-n confirmatory multi-model study.
6. **`scientific_evidence=false`.** Protocol-complete directional consistency, not confirmation.
7. **No matched external defense baseline.** The present study is an attribution study, not a head-to-head defense benchmark (`BASELINE_GAP.md`).
8. **No ranking comparison against published systems.** Other papers’ numeric ASRs are incommensurable without matched conditions.
9. **No production robustness claim.**
10. **D3 deferred.** `DEFERRED_NO_OFFLINE_IMPL`. No D3 numbers (`D3_AND_C4.md`).
11. **C4 / open adaptive attacker out of scope.** P2 C4-mini is scripted. PHASE1-CORE action adaptation ≠ closed-loop adaptive adversary.
12. **Frozen benchmark effects.** P2 is mock-tool, short-horizon, small. SHA `32b40e3b…`.
13. **Provider/runtime effects.** OpenRouter tool schemas, temp=0 residual nondeterminism.
14. **Tool-call formatting.** Parser/schema failures can stop execution (INVALID) independently of detector hits.
15. **Model refusal behavior.** Refusal is not credited as a defense win. Non-execution is simply not Tool-HASR success.
16. **INVALID_TOOL_ARGS are frequent and scientifically relevant.** Q2 live: 192 unique events / 136 arms. Not Tool-HASR success; not negligible; S0 primary unchanged; S2 signs 9/9. Does not prove INVALID is negligible.
17. **Judge/Tool metric disagreement.** T1–T3 M3=108, M4=3. Judge-ASR and Tool-HASR capture related but non-identical operational outcomes. Judge-ASR is not declared invalid.
18. **Stage-B raw trace unavailable locally.** Official packaged T0 PHASE1-CORE is reused from `p3_stage_b_20260916T235438Z_7e401714`. `STAGE_B_TRACE_STATUS = MISSING_LOCALLY`. Operator-stated 124/192 aggregate was not found as a local file and was not reconstructed. Independent T0 recompute was not performed (`STAGE_B_EVIDENCE_STATUS.md`).
19. **Exact literature gap cannot be claimed globally.** Novelty remains PARTIAL_GAP. AgentDojo/ASB identities are VERIFIED; that does not prove uniqueness of the factorial.
20. **Observed Δ vs D0 is a detector-related association under the controlled protocol.** It does not establish a causal effect of detector identity in isolation from all runtime factors.

## Threats (short)

| Threat | Direction of concern |
| --- | --- |
| Small n | Over-reading Δ magnitude / CI overlap |
| INVALID | Tool-HASR may miss attempted harm that failed schema |
| Judge M3 | Text success without tool harm inflates Judge-ASR |
| OpenRouter runtime | Provider-specific tool formatting |
| T0 not re-run; traces missing locally | Independent T0 INVALID recompute blocked here; official T0 rates remain in Q2 report JSON |
| Model selection | Pre-registered but Qwen-heavy |
| Attribution vs association | Detector-related association under locked policy; does not establish detector identity as the sole associated factor |
