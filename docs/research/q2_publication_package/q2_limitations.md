# Limitations (reviewer-facing)

1. **Benchmark size:** P2 has 16 attacks (Wilson CIs wide; e.g. 2/16 cells). P1 uses 2 examples per mechanism leaf.
2. **P2 composition:** 16 twins / 4 hard negatives; short multi-turn (≈2–6 turns), not long-horizon agents.
3. **Model/provider coverage:** Four OpenRouter targets (mostly Qwen + one Gemma) + one judge; not commercial closed-model diversity.
4. **D3 deferred:** Semantic/embedding detector class unevaluated.
5. **INVALID_TOOL_ARGS:** Frequent (192 events on T1–T3); reported via S0/S1/S2; primary denom unchanged but schema noise is real.
6. **Judge/tool disagreement:** Large M3; dual-metric reporting required.
7. **Normalized action costs:** A0–A3 are experimental weights, not validated monetary intervention costs (token-USD reported separately for Q2).
8. **Benchmark-level evidence:** Mock tools; not production deployments.
9. **Generalization:** Directional consistency ≠ universal LLM generalization.
10. **No human red-team evaluation** in this package.
11. **Model-specific tool-calling:** Formatting/compliance differences may interact with INVALID and Tool-HASR.
12. **scientific_evidence=false** on P3/Q2: frame as protocol-complete pilot consistency, not confirmatory SOTA.
13. **External published baselines** not fairly reconstructed on the same pack (gap documented).
14. **Adaptive attacks (C4)** out of scope / absent from P1.
