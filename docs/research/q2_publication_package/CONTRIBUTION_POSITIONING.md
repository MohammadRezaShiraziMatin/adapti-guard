# Q2 contribution positioning

**API calls:** 0. Not five unrelated novel algorithms.

## One central contribution

A **controlled framework for isolating detector-related effects from downstream intervention policy** in LLM-agent security, measured primarily by **Tool-HASR**, with a bounded check that the detector-related Δ sign observed on the locked Stage-B target remains **directionally consistent** on independently selected secondary targets (Q2 / RQ-C2).

## Problem

Tool-using agents can cause harm by **executing** a tool, not only by emitting a successful-looking string. Detector hit rate, text refusal, and Judge-ASR are easy to mix with the intervention policy that actually grants or denies tools. When those pieces move together, a lower attack-success number cannot be attributed to “the detector.”

## Gap

Published agent-security evaluations often report a stacked defense (filter + policy + tool layer) or a text-level ASR. This repository’s Q2 protocol holds **policy, thresholds, action costs, pack, and judge** fixed and varies **only detector identity** (D0/D1/D2/D4) under PHASE1-CORE, then asks whether Δ vs D0 keeps sign across targets.

This gap statement is methodological. It is **not** a verified literature claim that no prior paper ever isolated these factors. Related-work names need human citation verification (`BASELINE_GAP.md`).

## Methodological contribution

1. **Detector–policy decomposition:** D0 (no detection) vs operational detectors under one policy stratum.
2. **Tool-HASR primary operational endpoint:** harmful tool execution matching a pre-registered `success_condition`.
3. **Judge-ASR secondary diagnostic:** same arms; M3/M4 disagreement counts required.
4. **Cross-target directional consistency (Q2):** Δ(d,t) sign vs Δ(d,T0) on T1–T3; 9/9 observed.
5. **Forensic layer:** M3/M4 plus pre-specified INVALID_TOOL_ARGS S0/S1/S2.

Supporting findings, not independent inventions of new detector families. D1/D2/D4 are interpretable instantiations under a shared contract (`docs/research/P3_DETECTOR_TAXONOMY.md`). Runtime guardrails and cost-sensitive actions are established ideas; this work does not claim to invent them.

## Empirical finding (scoped)

Under locked PHASE1-CORE on frozen `p2_agentic_v0.1.0`, attack-cell n=16:

- T0 (Stage-B reuse): Δ(D1/D2/D4) = −0.6875 / −0.25 / −0.5625 (all NEG).
- T1–T3 (Q2 live, 432/432 arms, $0.152885 historical spend): all nine Δ signs NEG; sign agreement 9/9.
- Q2 live T1–T3: Tool-HASR 81/192; Judge-ASR 186/192; M3=108; M4=3.
- INVALID 192 events / 136 arms on T1–T3; S2 signs remain 9/9; S0 stays official.

`scientific_evidence=false` on the run. Frame as **protocol-complete pilot-scale directional consistency**, not confirmation for all LLMs.

## Scope

- Pack: `p2_agentic_v0.1.0` (SHA `32b40e3b…`).
- Policy: PHASE1-CORE only in Q2 live.
- Targets: four OpenRouter IDs (T0–T3) + locked judge.
- Detectors: D0/D1/D2/D4; D3 deferred.
- Mock tools; short multi-turn trajectories.

## Limitations

See `LIMITATIONS.md`. Headline limits: n=16, four targets, INVALID frequency, M3 mass, no fair external baseline, D3 deferred, C4 open adaptive attacker out of claim scope, Stage-B raw traces not in this checkout.

## What is NOT claimed

- SOTA / best / superior detector or defense.
- Production-ready or universally effective protection.
- Confirmation for all LLMs.
- Causal identification in deployment.
- Monetary cost-optimality (A0–A3 are normalized weights; token-USD is separate).
- That Judge-ASR is invalid.
- That Track B reverses Track A, or that Q2 reverses VNEXT FAIL.
- Adaptive-attacker (open C4) robustness.
- Five novel algorithms.
