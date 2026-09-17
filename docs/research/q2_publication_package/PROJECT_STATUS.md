# Q2 publication package — project status (final packaging)

**Date:** 2026-09-17  
**Packaging branch:** `cursor/q2-final-publication-packaging-f6f3`  
**LIVE_EVAL=false. API_CALLS=0. LLM_CALLS=0. NETWORK_CALLS=0.** Frozen evidence not modified.

| Class | Meaning |
| --- | --- |
| **VERIFIED** | Hashed or copied from locked Q2 reports |
| **DERIVED** | Computed from VERIFIED traces/JSON after the run |
| **UNAVAILABLE / MISSING locally** | Required for independent recompute but not on this checkout |
| **NOT CLAIMABLE** | Would need new experiments or forbidden wording |

## VERIFIED (this checkout)

P1 SHA `1a0b0053…dd235`; P2 SHA `32b40e3b…8d64dd`; Q2 predictions SHA `2a2c2f31…886cc6`; Q2 432/432; spend $0.152885; 9/9 sign agreement; D1/D2/D4 Δ NEG on T0–T3; Tool-HASR 81/192; Judge-ASR 186/192; M3=108; M4=3; INVALID 192/136; S2 9/9; `scientific_evidence=false`; evidence commit `b075df0f5ec5ad11ede76ac4e4079cade15208f1`.

## Official vs local (Stage-B)

| | |
| --- | --- |
| Official T0 Tool-HASR/Δ | In Q2 live report / `q2_final_statistics.json` (Stage-B reuse) |
| Local `predictions.jsonl` | **MISSING_LOCALLY** — not fabricated |

## Figures 3–5

**COMPLETE** as stdlib PNG from verified JSON. matplotlib **MISSING** (blocked network install; alternative renderer used).

## Bibliography

**PARTIAL:** arXiv title/authors/year/id from existing package records; venue/DOI **UNVERIFIED**. Novelty remains **PARTIAL GAP**.

## Readiness

**FINAL_PACKAGING_STATUS = READY_WITH_MAJOR_REVISIONS**

Not PUBLICATION_READY: Stage-B traces missing locally; venues/DOI unverified; camera-ready LaTeX/venue template not applied.
