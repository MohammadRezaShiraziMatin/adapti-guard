# Final weakness closure (Q2 publication hardening)

**Date:** 2026-09-17  
**Branch:** `cursor/q2-publication-hardening-f6f3`  
**FINAL_STATUS:** `READY_WITH_MAJOR_REVISIONS`  
**PUBLICATION_READY:** false (Stage-B raw evidence missing; bibliography PARTIAL)

Do not make the paper look stronger than the evidence. Remaining blockers are genuine.

## RESOLVED

- Stage-B local search completed; missing traces labeled; no reconstruction
- Official vs local T0 distinction documented (`STAGE_B_EVIDENCE_STATUS.md`)
- Operator-stated 124/192 recorded as NOT_FOUND_ON_THIS_CHECKOUT; manuscript uses packaged T0 PHASE1-CORE 28/64 from the Q2 live report
- Related-work identities classified; AgentDojo/ASB no longer UNCERTAIN as papers
- CaMeL positioned as a published architectural defense, not an unverified idea
- AgentDojo/BIPIA venue/DOI applied as operator-supplied, not invented
- Task Shield not added (was not in the matrix)
- Novelty rewritten as **controlled attribution**, not a new defense; `NOVELTY_CLASS=PARTIAL_GAP` unchanged
- Residual gap sentence narrowed and scoped; no “first” / “unique” / “no prior work”
- External comparisons framed as a scope boundary: attribution study, not a defense leaderboard
- INVALID_TOOL_ARGS compact S0/S1/S2 table from existing evidence; frequent / not discarded / not harmless / not proven negligible
- Tool-HASR vs Judge-ASR treated as a scientific finding (related but non-identical)
- Paired discordant counts added from existing JSON; no manufactured p-values or Δ CIs
- Explicit statement: Q2 was designed as a directional consistency analysis; inferential p-values were not preregistered and are not reported
- Detector-related effect language; no unqualified detector causality
- Manuscript restructured to 10 required sections; title does not imply a new defense
- Abstract includes protocol, detector variation, fixed policy, Tool-HASR, four targets, 432/432, 9/9, n=16/cell, pilot-scale; not confirmatory
- Twenty limitations listed
- Figures 3–5 retained; captions state D0 reference, no ranking, no significance encoding
- Reproducibility checklist split A/B/C/D; `REPRODUCIBILITY_STATUS=PARTIAL`
- Venue decision matrix without invented deadlines or “currently open” claims
- Document-only peer-review response matrix
- Forbidden-word scan of the manuscript: remaining hits are negations/limitations
- Required numbers consistent: 432/432, $0.152885, 9/9, 81/192, 186/192, M3=108, M4=3, 192/136, n=16/cell, scientific_evidence=false

## PARTIALLY_RESOLVED

- Bibliography: 21/21 identities VERIFIED; 19/21 venue/DOI still UNVERIFIED; AgentDojo/BIPIA operator-supplied and not re-fetched from publisher pages (NETWORK_CALLS=0)
- Novelty residual: full texts of AgentDojo/ASB not end-to-end audited; PARTIAL_GAP retained rather than CLEAR GAP or uniqueness
- Figure rasterization: stdlib PNG present; matplotlib still MISSING
- S1: stratum Δ signs observed NEG, but S1 is not a protocol 9/9 statistic
- T0 INVALID: prior derived record only (61/39), not raw-trace recompute
- Venue strategy: categories compared; no venue selected; page limits/deadlines UNVERIFIED

## GENUINELY_BLOCKED

- Stage-B raw `predictions.jsonl` / run-dir `metrics.json` / `manifest.json` **MISSING_LOCALLY** — independent T0 recompute impossible without the original bytes
- Camera-ready bibliography — most venue/DOI UNVERIFIED; operator-supplied DOIs not independently re-checked this turn
- Matched external defense baseline — requires a new live experiment if a comparative claim is desired (out of scope; not required for this attribution paper)
- Pilot-scale evidence itself — n=16/cell, four Qwen-heavy targets, `scientific_evidence=false` cannot be repaired from documentation
- D3 deferred; C4 open adaptive attacker out of scope — new science, not this task
- Exact global literature-gap proof — not available from a 21-paper offline matrix

## Flags

| Flag | Value |
| --- | --- |
| NO_NEW_EXPERIMENT_REQUIRED | true |
| API_CALLS | 0 |
| LLM_CALLS | 0 |
| NETWORK_CALLS | 0 |
| LIVE_EVAL | false |
| Q2_RERUN | false |
| P1_MODIFIED | false |
| P2_MODIFIED | false |
| Q2_TRACE_MODIFIED | false |
| novelty_class | PARTIAL_GAP |
| reproducibility_status | PARTIAL |
| bibliography_status | PARTIAL |
| final_status | READY_WITH_MAJOR_REVISIONS |

Manuscript SHA-256 (this pass): `e163f709ed4d5b24973ec2958b75466b68e2875526361d0911e72251d6bfaf79`

Machine-readable: `FINAL_WEAKNESS_CLOSURE.json`.
