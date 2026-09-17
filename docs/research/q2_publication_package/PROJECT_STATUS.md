# Q2 publication package — project status (hardening)

**Date:** 2026-09-17  
**Packaging branch:** `cursor/q2-publication-hardening-f6f3`  
**LIVE_EVAL=false. API_CALLS=0. LLM_CALLS=0. NETWORK_CALLS=0.** Frozen evidence not modified.

| Class | Meaning |
| --- | --- |
| **VERIFIED** | Hashed or copied from locked Q2 reports |
| **DERIVED** | Computed from VERIFIED traces/JSON after the run |
| **UNAVAILABLE / MISSING locally** | Required for independent recompute but not on this checkout |
| **NOT CLAIMABLE** | Would need new experiments or forbidden wording |

## VERIFIED (this checkout)

P1 SHA `1a0b0053…dd235`; P2 SHA `32b40e3b…8d64dd`; Q2 predictions SHA `2a2c2f31…886cc6`; Q2 432/432; spend $0.152885; 9/9 sign agreement; D1/D2/D4 Δ NEG on T0–T3; Tool-HASR 81/192; Judge-ASR 186/192; M3=108; M4=3; INVALID 192/136; S2 9/9; `scientific_evidence=false`; n=16/cell; evidence commit `b075df0f5ec5ad11ede76ac4e4079cade15208f1`.

## Official vs local (Stage-B)

| | |
| --- | --- |
| Official packaged T0 PHASE1-CORE | Tool-HASR 28/64; Judge-ASR 55/64; M3=33; M4=6 in Q2 live report |
| Operator-stated Stage-B aggregate 124/192 | NOT_FOUND_ON_THIS_CHECKOUT; not reconstructed; not used as locally verified manuscript rates |
| Local `predictions.jsonl` | **MISSING_LOCALLY** |

## Figures 3–5

**COMPLETE** as stdlib PNG from verified JSON. Not a ranking. No significance encoding. matplotlib **MISSING**.

## Bibliography

**PARTIAL:** 21/21 identities VERIFIED; most venue/DOI UNVERIFIED; AgentDojo/BIPIA venue/DOI operator-supplied, not re-fetched. Novelty remains **PARTIAL_GAP**. AgentDojo/ASB identities are not UNCERTAIN. CaMeL is not an unverified idea.

## Readiness

**STATUS = READY_WITH_MAJOR_REVISIONS** (`FINAL_SUBMISSION_READINESS.md`)

Not SUBMISSION_READY: Stage-B traces missing locally; bibliography not fully verified. CI 2/2 PASS is not publication acceptance.
