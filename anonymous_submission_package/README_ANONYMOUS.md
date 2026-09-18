# Controlled Detector Attribution under a Locked Runtime Intervention Policy: A Pilot-Scale Agent Security Evaluation

## Abstract

Observed security behavior in tool-using language-model agents can mix detector behavior with the downstream intervention policy that allows, wraps, or denies tools. Without holding that policy fixed, detector-related effects are difficult to attribute.

This paper reports a controlled attribution protocol, not a new detector family and not a defense covering all threat models. The intervention policy is held fixed (PHASE1-CORE). Detector identity is varied, including a no-detection reference (D0). The primary outcome is Tool-HASR (harmful tool execution). Judge-ASR is a secondary, non-identical diagnostic of judge-level attack-success assessment. The evaluation uses frozen pack `p2_agentic_v0.1.0` (16 attack / 16 twin / 4 hard-negative trajectories), four target models, and n=16 attack arms per target×detector cell. Q2 live completed 432/432 arms (historical spend $0.152885).

Under the tested protocol, detector-related Tool-HASR Δ versus D0 was negative for D1, D2, and D4 on the locked Stage-B target T0 and on independently selected T1–T3 (9/9 directional agreements). This is pilot-scale directional consistency. It does not establish population-level generalization. T1–T3 Tool-HASR was 81/192 = 0.421875; Judge-ASR was 186/192 = 0.96875 (M3=108, M4=3). INVALID_TOOL_ARGS occurred on 192 events / 136 arms and is treated as a canonical execution-state diagnostic, not as automatic attack success or failure.

The manuscript does not claim robustness beyond the tested protocol, production readiness, confirmatory multi-model generalization, or a ranking against external defenses.

## Reproducibility

**Author information, repository URL, and identifying metadata have been removed for double-blind review.**

REPRODUCIBILITY_STATUS = PARTIAL

Stage-B raw traces (`predictions.jsonl`, `metrics.json`, `manifest.json` for run `p3_stage_b_20260916T235438Z_7e401714`) are MISSING_LOCALLY. Only the SHA pointer and packaged metrics are available. Full Stage-B replication requires access to the original run directory, which is not present in the current checkout.

## Artifact contents

- `manuscript.md` — anonymized manuscript
- `figures/` — Figures 3–5 (PNG, unmodified)
- `README_ANONYMOUS.md` — this file

## Key results

- 432/432 arms completed
- 9/9 directional sign agreements (all Δ negative)
- T1–T3 Tool-HASR: 81/192 = 0.421875
- T1–T3 Judge-ASR: 186/192 = 0.96875
- M3=108, M4=3
- INVALID_TOOL_ARGS: 192 events / 136 arms
- Historical cost: $0.152885
- n=16 per cell
- scientific_evidence = false (pilot-scale)
