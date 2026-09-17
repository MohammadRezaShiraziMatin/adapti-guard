# Q1 Claims Ledger

**JSON:** `/opt/cursor/artifacts/q1_claims_ledger.json`

Status ∈ {SUPPORTED, PARTIALLY_SUPPORTED, NOT_SUPPORTED, OUT_OF_SCOPE}

| ID | Claim | Evidence | Status | Safe wording | Unsafe wording | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | Detector choice affects Tool-HASR vs D0 under PHASE1-CORE | Stage-B Δ D1/D2/D4 = −0.6875/−0.25/−0.5625 (n=16) | SUPPORTED | Pilot-scale D-vs-D0 Tool-HASR reductions under locked protocol | “Robust security” / “D1 is best” | Small n; no ranking; P3 `scientific_evidence=false` |
| C2 | Detector effects isolable from policy by holding policy fixed | P3 design: only detector varies | SUPPORTED | Protocol isolates detector-related contrasts under fixed policy | Full real-world causal proof | INVALID and model behavior remain confounders |
| C3 | Tool-HASR ≠ Judge-ASR; execution-grounded primary | M3/M4 large (Stage-B 61/22; Q2 108/3) | SUPPORTED | Dual-metric forensics; Tool-HASR primary for tool harm | “Judges useless” | Context-dependent metric choice |
| C4 | Δ sign consistency on T1–T3 | Q2 9/9 agreements | SUPPORTED | Directional consistency across evaluated targets | “All LLMs” / “universal” | 4 models; reduced design |
| C5 | PHASE1-CORE improves P1 L1 security vs B0 | L1 HASR 41/44→22/44 | PARTIALLY_SUPPORTED | Pilot L1 judge-aliased HASR reduction | Production safety proof | Metric ≠ Tool-HASR; residual misses |
| C6 | Validated monetary cost-aware defense | A0–A3 weights only | NOT_SUPPORTED | Normalized experimental cost weights | USD optimality | Assumptions |
| C7 | Breakthrough end-to-end novel defense | Novelty audit | PARTIALLY_SUPPORTED | Novel integration: isolation protocol + Tool-HASR eval | “First/only/breakthrough” | Needs verified related work |
| C8 | Generalizes beyond P1/P2 packs | Pack sizes / coverage gaps | NOT_SUPPORTED | Scoped to frozen packs | Broad generalization | Pilot coverage |
| C9 | INVALID overturns primary Δ | S0/S1/S2 stable signs | NOT_SUPPORTED | Report INVALID; signs stable | Ignore INVALID | Still a confound |
| C10 | Detector ranking / winner | Protocol forbids | OUT_OF_SCOPE | Report Δ vs D0 only | “Winner” | Non-goal |

## Enforcement rule

Manuscript text must only use **safe wording** for SUPPORTED/PARTIALLY_SUPPORTED claims. NOT_SUPPORTED and OUT_OF_SCOPE claims appear only as limitations or explicit non-goals.
