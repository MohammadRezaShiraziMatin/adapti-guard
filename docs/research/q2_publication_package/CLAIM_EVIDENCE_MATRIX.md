# Claim–evidence matrix (`MANUSCRIPT_FINAL.md`)

**API=0. NETWORK=0. LIVE_EVAL=false.**  
**Central claim status: PARTIALLY_SUPPORTED / PILOT-SCALE**

Required statuses: **SUPPORTED** · **PARTIALLY_SUPPORTED** · **NOT_ESTABLISHED**.  
Wilson 95% CIs on rates are **derived from locked counts**, not a preregistered Δ analysis.

| ID | Claim | Evidence | Source | Numerator | Denominator | Status | Allowed wording | Forbidden wording |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C00 | Detector-related Tool-HASR Δ vs D0 remained directionally consistent across T0–T3 | All 9 D1/D2/D4 × T1–T3 signs match T0; all 12 Δ NEG | `q2_final_statistics.json`; Table 3 | 9 | 9 | **PARTIALLY_SUPPORTED / PILOT-SCALE** | observed Δ direction remained consistent; 9/9 directional agreements; pilot-scale directional consistency under the tested protocol | confirmatory; definitive; generalizable; universal; proves; causal; SOTA; best; robust (unqualified) |
| C01 | Detector, policy, Tool-HASR, Judge-ASR, M3, M4, INVALID are distinct layers | Protocol formulation | §5; lock | — | — | SUPPORTED (formulation) | distinct measurements / layers | ranking of layers; Judge-ASR invalid |
| C02 | Contribution is controlled attribution, not a new detector family | Novelty audit; surveyed 21 records | `NOVELTY_AUDIT.md`; §6 | — | 21 surveyed | PARTIALLY_SUPPORTED (PARTIAL_GAP) | controlled attribution protocol; PARTIAL_GAP | first; novel detector; novel defense; unique; no prior work |
| C03 | Policy locked; detectors D0/D1/D2/D4 varied | Manifest / lock | Q2 lock + T0 reuse | — | — | SUPPORTED | held PHASE1-CORE fixed; varied detector identity including D0 | T0 independently recomputed from local Stage-B traces |
| C04 | Tool-HASR primary; Judge-ASR secondary and non-identical | Protocol + T1–T3 disagreement | protocol; Table 4 | 81 vs 186 | 192 | SUPPORTED | distinct measurements; related but non-identical | either metric invalid; forced into one metric |
| C05 | 432/432 arms completed | Manifest | Q2 live | 432 | 432 | SUPPORTED | 432/432 Q2 live arms | T0 included in 432 |
| C06 | Historical spend $0.152885 | spend.json | Q2 live | — | — | SUPPORTED | historical execution cost $0.152885 | A0–A3 as USD |
| C07 | Cell Tool-HASR n/N and Wilson CIs as tabulated | statistics JSON | `q2_final_statistics.json` | cell n | 16 | SUPPORTED (rates); CIs DERIVED from locked counts | numerator/denominator; Wilson 95% CI derived from locked counts | preregistered Δ CI; significance |
| C08 | Authoritative Δ: T0 −0.6875/−0.2500/−0.5625; T1 −0.7500/−0.3125/−0.6250; T2 −0.6875/−0.2500/−0.5625; T3 −0.5625/−0.1875/−0.5000; all NEG | statistics JSON | Table 3 | — | n=16/cell | SUPPORTED | observed Δ versus D0; all NEG | ranking of detectors; Δ CI |
| C09 | 9/9 sign agreement; 0 S0→S2 sign flips | statistics / invalid_sensitivity | live report; S2 | 9 | 9 | SUPPORTED | 9/9 directional agreements; S2 9/9 | confirmatory hypothesis test; p-value |
| C10 | Pilot-scale directional consistency | C08+C09+n=16 | Abstract; §9; §14 | 9 | 9 | **PARTIALLY_SUPPORTED / PILOT-SCALE** | pilot-scale directional consistency; observed property of this evaluation | confirmatory; definitive; generalizable; population-level |
| C11 | T1–T3 Tool-HASR 81/192 = 0.421875; Judge-ASR 186/192 = 0.96875 | statistics | Table 4 | 81; 186 | 192 | SUPPORTED | Tool-HASR 81/192; Judge-ASR 186/192 | interchangeable endpoints |
| C12 | M3=108, M4=3 on T1–T3 | statistics | Table 4 | 108; 3 | 192 | SUPPORTED | M3=108; M4=3 | proof judge wrong/right |
| C13 | Related but non-identical endpoints; neither declared invalid | C11–C12 | §10.1 | — | — | PARTIALLY_SUPPORTED (interpretation) | suggests disagreement sources conservatively | single-cause inference; causal explanation of M3 |
| C14 | INVALID 192 events / 136 arms | metrics + recompute | Table 5 | 192; 136 | 432 arms | SUPPORTED | 192 INVALID events / 136 affected arms | T0 INVALID independently recomputed this checkout |
| C15 | INVALID is a canonical execution-state category; not discarded; not automatic success/failure/harmlessness/detector failure | protocol + C14 | §5; §10.2; Table 6 | — | — | SUPPORTED (formulation) | canonical execution-state diagnostic; potential confounder | negligible; explains all metric disagreement |
| C16 | S2 9/9; 0 S0→S2 flips | invalid_sensitivity | derived | 9 | 9 | SUPPORTED | S2 9/9; 0 S0→S2 sign flips | INVALID negligible |
| C17 | Internal protocol flag `scientific_evidence=false` | manifest | Q2 lock | — | — | SUPPORTED | protocol-complete pilot; not confirmatory | confirmatory scientific_evidence=true |
| C18 | D3 deferred; no D3 results | lock | `D3_AND_C4.md` | — | — | NOT_ESTABLISHED (D3 effect) | deferred because embedding dependency was not in the locked offline protocol; future work | invented D3 scores |
| C19 | Robustness against open-ended adaptive attackers / C4 horizon / attacker adaptation | absence | Limitations | — | — | NOT_ESTABLISHED | out of scope; future work | robust to adaptive attackers; handles C4 |
| C20 | Attribution study, not a defense leaderboard | absence of matched baselines | `BASELINE_GAP.md` | — | — | SUPPORTED (scope) | external baselines outside primary claim; methodological scope | accidental omission; numerical bake-off |
| C21 | P1/P2/Q2 SHAs as listed; rechecked this pass | file hashes | frozen files | — | — | SUPPORTED | locked SHA identifiers | Stage-B bytes hashed this checkout |
| C22 | Integrity/forensic PASS on Q2 run | audit JSON | Q2 run | — | — | SUPPORTED | Q2 integrity PASS | publication acceptance; scientific_evidence true |
| C23 | 21 arXiv identities | package Hub records | `BIBLIOGRAPHY_VERIFICATION.md` | 21 identities | 21 | PARTIALLY_SUPPORTED (identity only) | IDENTITY_VERIFIED; most VENUE_UNVERIFIED | 21/21 fully publication-verified |
| C24 | Residual factorial gap | novelty audit | §6 | — | surveyed set | PARTIALLY_SUPPORTED (PARTIAL_GAP) | partial gap; not global uniqueness | first; unique; CLEAR GAP |
| C25 | SOTA / best / superior / guaranteed / production-ready / solves injection / causal effect / generalizable | — | — | — | — | NOT_ESTABLISHED | observed; under the tested protocol; associated with; does not establish | those words as assertions |
| C26 | Q2 confirmatory | protocol false | manifest | — | — | NOT_ESTABLISHED | directional consistency analysis | confirmatory; definitive |
| C27 | Track mixing / VNEXT reversal | dual-track docs | `DUAL_TRACK_STATUS.md` | — | — | NOT_ESTABLISHED (forbidden) | tracks remain separate | VNEXT reversed; unlabeled win |
| C28 | Stage-B traces present and independently recomputed | glob + git objects | `STAGE_B_EVIDENCE_STATUS.md` | — | — | NOT_ESTABLISHED | STAGE_B_TRACE_STATUS=MISSING_LOCALLY; official T0 reuse ≠ local recompute | independently recomputed from local traces |
| C29 | Figures 3–5 present | PNG files | `figures/` | — | — | SUPPORTED | figures present; no ranking/significance encoding | significance implied |
| C30 | T2 Δ equals T0 Δ | Table 3 | sample | — | n=16 | SUPPORTED (this sample) | observed coincidence at n=16 | T2 equals T0 in general |
| C31 | Detector-related association under locked policy | protocol | §5; §11 | — | — | PARTIALLY_SUPPORTED | associated with detector identity under locked PHASE1-CORE | causal proof; detector in isolation |
| C32 | Task Shield / AutoDojo / SCOUT / AgentAntibody / HARD / ARGUS / VIGIL / AttriGuard / MCP-SafetyBench / Runtime Policy Enforcement / Adaptive Attacks as verified citations | matrix absence | bib verification | — | — | NOT_ESTABLISHED | NOT_IN_PACKAGE; not cited | invented venue/DOI |
| C33 | Operator-stated Stage-B aggregate 124/192 as locally verified | absence | STAGE_B | — | — | NOT_ESTABLISHED | not found on this checkout; not used as locally verified manuscript rates | locally verified 124/192 |

**C00 (central claim) allowed:** “the observed Δ direction remained consistent across T0–T3”; “9/9 directional agreements”; “pilot-scale directional consistency under the tested protocol.”

**C00 forbidden:** confirmatory; definitive; generalizable; universal; SOTA; best detector/defense; production-ready; guaranteed security; causal; ranking against external defenses.
