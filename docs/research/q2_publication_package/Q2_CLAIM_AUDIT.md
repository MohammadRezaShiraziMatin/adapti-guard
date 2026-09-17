# Q2 Claim Audit

**API_CALLS=0. NETWORK_CALLS=0. LIVE_EVAL=false.**
Manuscript audited: `MANUSCRIPT_FINAL.md`. Central claim status: **PARTIALLY_SUPPORTED / PILOT-SCALE**.

## 1. Forbidden-word scan of the live manuscript

Terms scanned: `best`, `better`, `superior`, `SOTA`, `state-of-the-art`, `guarantee`, `guaranteed`, `universal`, `universally`, `production-ready`, `solves`, `definitive`, `proves`, `causal`, `generalizable`, `comprehensive`.

Result: **0 unsupported assertions** in `MANUSCRIPT_FINAL.md`. Remaining occurrences of scoped terms appear only in negations ("does not establish ...", "not confirmatory") and in the claim matrix's forbidden-wording column, never as positive claims.

## 2. Claim status summary

| ID | Claim | Status | Allowed wording | Forbidden wording |
| --- | --- | --- | --- | --- |
| C00 | Detector-related Tool-HASR Δ vs D0 directionally consistent across T0–T3 (9/9) | **PARTIALLY_SUPPORTED / PILOT-SCALE** | observed Δ direction remained consistent; 9/9 directional agreements; pilot-scale directional consistency under the tested protocol | confirmatory; definitive; generalizable; universal; proves; causal; SOTA; best; robust (unqualified) |
| C01 | Detector, policy, Tool-HASR, Judge-ASR, M3, M4, INVALID are distinct layers | SUPPORTED (formulation) | distinct measurements / layers | ranking of layers; Judge-ASR invalid |
| C02 | Contribution is controlled attribution, not a new detector family | PARTIALLY_SUPPORTED (PARTIAL_GAP) | controlled attribution protocol; PARTIAL_GAP | first; novel detector; novel defense; unique; no prior work |
| C03 | Policy locked; detectors D0/D1/D2/D4 varied | SUPPORTED | held PHASE1-CORE fixed; varied detector identity including D0 | T0 independently recomputed from local Stage-B traces |
| C04 | Tool-HASR primary; Judge-ASR secondary and non-identical | SUPPORTED | distinct measurements; related but non-identical | either metric invalid; forced into one metric |
| C05 | 432/432 arms completed | SUPPORTED | 432/432 Q2 live arms | T0 included in 432 |
| C06 | Historical spend $0.152885 | SUPPORTED | historical execution cost $0.152885 | A0–A3 as USD |
| C07 | Cell Tool-HASR n/N and Wilson CIs as tabulated | SUPPORTED (rates); CIs DERIVED from locked counts | numerator/denominator; Wilson 95% CI derived from locked counts | preregistered Δ CI; significance |
| C08 | Authoritative Δ values (all NEG) | SUPPORTED | observed Δ versus D0; all NEG | ranking of detectors; Δ CI |
| C09 | 9/9 sign agreement; 0 S0→S2 flips | SUPPORTED | 9/9 directional agreements; S2 9/9 | confirmatory hypothesis test; p-value |
| C10 | Pilot-scale directional consistency | **PARTIALLY_SUPPORTED / PILOT-SCALE** | pilot-scale directional consistency; observed property of this evaluation | confirmatory; definitive; generalizable; population-level |
| C11 | T1–T3 Tool-HASR 81/192; Judge-ASR 186/192 | SUPPORTED | Tool-HASR 81/192; Judge-ASR 186/192 | interchangeable endpoints |
| C12 | M3=108, M4=3 on T1–T3 | SUPPORTED | M3=108; M4=3 | proof judge wrong/right |
| C13 | Related but non-identical endpoints; neither declared invalid | PARTIALLY_SUPPORTED (interpretation) | suggests disagreement sources conservatively | single-cause inference; causal explanation of M3 |
| C14 | INVALID 192 events / 136 arms | SUPPORTED | 192 INVALID events / 136 affected arms | T0 INVALID independently recomputed this checkout |
| C15 | INVALID is canonical execution-state; not discarded; not automatic success/failure/harmlessness/detector failure | SUPPORTED (formulation) | canonical execution-state diagnostic; potential confounder | negligible; explains all metric disagreement |
| C16 | S2 9/9; 0 S0→S2 flips | SUPPORTED (derived) | S2 9/9; 0 S0→S2 sign flips | INVALID negligible |
| C17 | Internal protocol flag `scientific_evidence=false` | SUPPORTED | protocol-complete pilot; not confirmatory | confirmatory scientific_evidence=true |
| C18 | D3 deferred; no D3 results | NOT_ESTABLISHED (D3 effect) | deferred because embedding dependency was not in locked offline protocol; future work | invented D3 scores |
| C19 | Robustness against open-ended adaptive attackers / C4 / attacker adaptation | NOT_ESTABLISHED | out of scope; future work | robust to adaptive attackers; handles C4 |
| C20 | Attribution study, not a defense leaderboard | SUPPORTED (scope) | external baselines outside primary claim; methodological scope | accidental omission; numerical bake-off |
| C21 | P1/P2/Q2 SHAs as listed; rechecked this pass | SUPPORTED | locked SHA identifiers | Stage-B bytes hashed this checkout |
| C22 | Integrity/forensic PASS on Q2 run | SUPPORTED | Q2 integrity PASS | publication acceptance; scientific_evidence true |
| C23 | 21 arXiv identities | PARTIALLY_SUPPORTED (identity only) | IDENTITY_VERIFIED; most VENUE_UNVERIFIED | 21/21 fully publication-verified |
| C24 | Residual factorial gap | PARTIALLY_SUPPORTED (PARTIAL_GAP) | partial gap; not global uniqueness | first; unique; CLEAR GAP |
| C25 | SOTA / best / superior / guaranteed / production-ready / solves injection / causal effect / generalizable | NOT_ESTABLISHED | observed; under the tested protocol; associated with; does not establish | those words as assertions |
| C26 | Q2 confirmatory | NOT_ESTABLISHED | directional consistency analysis | confirmatory; definitive |
| C27 | Track mixing / VNEXT reversal | NOT_ESTABLISHED (forbidden) | tracks remain separate | VNEXT reversed; unlabeled win |
| C28 | Stage-B traces present and independently recomputed | NOT_ESTABLISHED | STAGE_B_TRACE_STATUS=MISSING_LOCALLY; official T0 reuse ≠ local recompute | independently recomputed from local traces |
| C29 | Figures 3–5 present | SUPPORTED | figures present; no ranking/significance encoding | significance implied |
| C30 | T2 Δ equals T0 Δ | SUPPORTED (this sample) | observed coincidence at n=16 | T2 equals T0 in general |
| C31 | Detector-related association under locked policy | PARTIALLY_SUPPORTED | associated with detector identity under locked PHASE1-CORE | causal proof; detector in isolation |
| C32 | Task Shield / AutoDojo / SCOUT / etc. as verified citations | NOT_ESTABLISHED | NOT_IN_PACKAGE; not cited | invented venue/DOI |
| C33 | Operator-stated Stage-B aggregate 124/192 as locally verified | NOT_ESTABLISHED | not found on this checkout; not used as locally verified manuscript rates | locally verified 124/192 |

## 3. Central claim (C00)

**Allowed:** "the observed Δ direction remained consistent across T0–T3"; "9/9 directional agreements"; "pilot-scale directional consistency under the tested protocol."

**Forbidden:** confirmatory; definitive; generalizable; universal; SOTA; best detector/defense; production-ready; guaranteed security; causal; ranking against external defenses.

Full row-level matrix: `CLAIM_EVIDENCE_MATRIX.md`.
