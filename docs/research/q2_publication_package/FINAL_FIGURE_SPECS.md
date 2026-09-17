# FINAL Figure Specs

## Figure 3 — Δ Tool-HASR relative to D0 across T0-T3

- File: `figures/figure3_delta_across_targets.png`
- SHA-256: `cc8ee54afa73af8d0d6ca6025fe9e403d13e335cd2dd9478f2fb00dbbd124a0a`
- Type: grouped bars D1/D2/D4 × T0-T3
- D0 is reference (Δ=0 by definition; not a bar)
- Caption: Δ is relative to D0; pilot-scale directional consistency; n=16/cell; not a ranking; no significance encoding
- Values: D1 T0/T1/T2/T3 = −0.6875/−0.7500/−0.6875/−0.5625; D2 = −0.2500/−0.3125/−0.2500/−0.1875; D4 = −0.5625/−0.6250/−0.5625/−0.5000

## Figure 4 — Tool-HASR vs Judge-ASR

- File: `figures/figure4_toolhasr_vs_judgeasr.png`
- SHA-256: `747f1b807fd18d2cf9c44a717363ff44b4e9c6ab36eb31b1d0dac0ffa1445304`
- Caption: related but non-identical; neither metric declared invalid; n=16/cell; not a ranking
- Pooled attack n=64/target. T0: Tool 28/64, Judge 55/64; T1: 29/64, 62/64; T2: 28/64, 62/64; T3: 24/64, 62/64. M3/M4 as Table 4.

## Figure 5 — INVALID_TOOL_ARGS diagnostic

- File: `figures/figure5_invalid_tool_args.png`
- SHA-256: `f737805f97fab25bbb302bbeccdf37f731e753c7cba554232c7da104bfb1f21a`
- Caption: diagnostic execution-state category; frequent (192/136); not discarded; not Tool-HASR success; not proven negligible; not a ranking
- T1: 62 events/41 arms; T2: 62/46; T3: 68/49

Renderer: stdlib zlib PNG (matplotlib unavailable; no network install).
