# Q1 Contribution Framework

**Rule:** One primary contribution; secondaries support it. Do not present every module as an independent breakthrough.

## PRIMARY CONTRIBUTION

**Detector-related security effects in agentic runtime defense can be isolated and evaluated separately from downstream intervention policy under a controlled protocol.**

Operationalization:

- Hold fixed: pack, trajectories, tools, permissions, thresholds, action costs, policy stratum, judge, temperature, cache.
- Vary only: `detector_id ∈ {D0, D1, D2, D4}` (D3 deferred).
- Primary estimand: `Δ(d,t) = Tool-HASR(d,t) − Tool-HASR(D0,t)` on attack arms (PHASE1-CORE for Q2; multi-policy reported for Stage-B descriptively).
- No ranking / no winner.

Evidence anchors: P3 Stage-B `p3_stage_b_20260916T235438Z_7e401714`; Q2 `p3_stage_c_q2_20260917T123855Z_b075df0f`.

## SECONDARY CONTRIBUTIONS (support only)

| # | Contribution | Role in paper |
| --- | --- | --- |
| S1 | Tool-HASR as execution-grounded security endpoint | Metric justification (§Endpoints) |
| S2 | Explicit detector → policy → tool execution separation | Architecture (§System) |
| S3 | Forensic Tool-HASR vs Judge-ASR (M3/M4) | Forensic analysis section |
| S4 | Cross-target directional consistency (Q2) | Bounded generalization section |
| S5 | Cost-aware intervention *accounting* (normalized weights) | Cost appendix; not economic validation |

## What is NOT a major contribution

- Inventing prompt-injection detection as a field
- Claiming a new adaptive-attacker defense
- Declaring a best detector
- Claiming validated USD cost optimization
- Claiming broad LLM generalization

## Paper narrative spine

1. Problem: agent tool harms ≠ textual jailbreak success.
2. Gap: detector and policy are usually entangled → attribution unclear.
3. Method: isolate detector under fixed policy; measure Tool-HASR.
4. Results: Δ vs D0 on T0; directional consistency on T1–T3.
5. Forensics: Judge disagreement + INVALID sensitivity.
6. Limits: pilot n, baselines, C4, costs as weights.

## Claim discipline

Every abstract/intro sentence must map to the primary contribution or a labeled secondary. If it does not, delete or move to Limitations.
