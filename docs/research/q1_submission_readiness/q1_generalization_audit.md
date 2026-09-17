# Q1 Generalization / Benchmark Limitations Audit

**Rule:** Quantify → impact → what remains valid → what cannot be generalized. Do not hide small *n*.

## Pack sizes (quantified)

| Pack | Attacks | Benign twins | Hard negatives | Total | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| P1 `p1_mechanism_v1.0.0` | 44 | 44 | 8 | 96 | 22 mechanisms × 2 attacks; **C4 = 0** |
| P2 `p2_agentic_v0.1.0` | 16 | 16 | 4 | 36 | Multi-turn; mean ~3.9 turns |

SHAs (integrity): P1 `1a0b0053…dd235`; P2 `32b40e3b…64dd`.

## Limitation matrix

| Limitation | Quantify | Scientific impact | Remains valid | Cannot generalize |
| --- | --- | --- | --- | --- |
| P1 size | 2 attacks/mechanism leaf | Underpowered per mechanism; leaf-level rates unstable | Aggregate L1 policy contrasts are descriptive pilot evidence | Per-mechanism efficacy claims |
| P2 trajectory count | 16 attacks | Wide Wilson CIs (e.g. 2/16 Tool-HASR CI spans large range) | Sign/direction of large contrasts under fixed protocol | Precise effect sizes / ranking |
| Mechanism coverage | P1 omits C4; P2 mixes subset of families | Adaptive / delayed-fire threats under-represented | Results for covered mechanisms in packs | Adaptive attacker (C4) robustness |
| Benign twins | 44 (P1) / 16 (P2) | Utility/FPR estimates noisy | Separate twin vs HN strata reporting | Population FPR claims |
| Hard negatives | 8 (P1) / 4 (P2) | Detector confusion cases sparse | Qualitative HN behavior | Calibrated HN FPR |
| Indirect injection | Limited authored scenarios | May miss realistic tool-output injection diversity | Covered authored-channel cases | Broad indirect-injection security |
| Multi-turn | P2 turns 2–6; not long-horizon | Long-context / late-trigger attacks limited | Short multi-turn tool loops in pack | Long-horizon agents |
| Memory/state | Present in some trajs; not exhaustive | Memory-plant threats partially covered (D4 cues) | Provenance-cue usefulness as hypothesis | Full memory integrity guarantees |
| Adaptive attack coverage | C4 out of scope / zero in P1 | Attacker adapting to defense untested | Static authored attacks | Adaptive robustness |
| C4 limitations | Explicitly 0 in P1; out of scope in TM | Threat model incomplete for sophisticated attackers | Honesty of threat model | “Robust to adaptive attacks” |
| Model diversity | T0–T3 + fixed judge (4 targets) | Family/skew limited (mostly Qwen + one Gemma) | Directional consistency on evaluated set | All LLMs / providers |
| Detector set | D3 deferred | Semantic detector class absent | Interpretable D0/D1/D2/D4 contrasts | Complete detector taxonomy |
| Policy set (Q2) | PHASE1-CORE only | Cross-policy generalization of Δ untested in Q2 | Within PHASE1-CORE Δ consistency | Δ under B0/STATIC-A1 for T1–T3 |
| scientific_evidence flags | P3/Q2 = false | Cannot claim confirmatory science without reframing | Protocol + pilot measurement study | Confirmatory SOTA paper framing |

## Bottom line

ADAPTI-GUARD evidence supports **protocol-valid, pilot-scale** conclusions on locked packs and models. It does **not** support broad security guarantees, adaptive-attacker claims, or population-level generalization.
