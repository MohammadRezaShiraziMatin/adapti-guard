# Claim–evidence matrix (`MANUSCRIPT_FINAL.md`)

**API=0.** Every substantive claim in `MANUSCRIPT_FINAL.md` is classified.

Legend: **OBSERVED** · **DERIVED** · **INTERPRETATION** · **LITERATURE CLAIM** · **LIMITATION** · **UNVERIFIED**

| ID | CLAIM | SOURCE | EVIDENCE TYPE | VERIFIED? | SCOPE | LIMITATION |
| --- | --- | --- | --- | --- | --- | --- |
| C00 | Detector-related Tool-HASR Δ vs D0 remained directionally consistent across T0–T3 (9/9) | Tables 3–4 | INTERPRETATION of OBSERVED | Yes if scoped | Four models; PHASE1-CORE; n=16; `scientific_evidence=false` | Not causal proof; not confirmatory |
| C01 | Detector, policy, Tool-HASR, Judge-ASR, M3, M4, INVALID are distinct layers | §3 | INTERPRETATION | Yes as formulation | This protocol | Not an empirical ranking |
| C02 | Contribution is controlled attribution, not novel detector families | §4, §12 | INTERPRETATION | Yes | Surveyed set | PARTIAL_GAP |
| C03 | Policy locked; detectors D0/D1/D2/D4 varied | manifest / lock | OBSERVED | Yes | Q2 + T0 reuse | T0 not re-run |
| C04 | Tool-HASR primary; Judge-ASR secondary and non-identical | protocol | OBSERVED | Yes | This study | Other papers use other endpoints |
| C05 | 432/432 completed | manifest | OBSERVED | Yes | Q2 live T1–T3 | T0 not in 432 |
| C06 | Historical spend $0.152885 | spend.json | OBSERVED | Yes | Q2 live | Not A0–A3 USD |
| C07 | Cell Tool-HASR n/N and Wilson CIs as tabulated | statistics JSON | DERIVED | Yes | n=16/cell | Wide CIs; no Δ CI |
| C08 | Authoritative Δ: T0 −0.6875/−0.2500/−0.5625; T1 −0.7500/−0.3125/−0.6250; T2 −0.6875/−0.2500/−0.5625; T3 −0.5625/−0.1875/−0.5000; all NEG | statistics JSON | DERIVED | Yes | 12 cells | Not a ranking |
| C09 | 9/9 sign agreement | statistics / live report | DERIVED | Yes | 3×3 contrasts | No Q2 p-value |
| C10 | Pilot-scale directional consistency | C08+C09+C17 | INTERPRETATION | Yes if scoped | Tested protocol | Not general robustness |
| C11 | T1–T3 Tool-HASR 81/192 = 0.421875; Judge-ASR 186/192 = 0.96875 | statistics | DERIVED | Yes | T1–T3 attack arms | Pooled; not a ranking |
| C12 | M3=108, M4=3 on T1–T3 | statistics | DERIVED | Yes | T1–T3 | Diagnostic |
| C13 | Related but non-identical endpoints; neither declared invalid | C11–C12 | INTERPRETATION | Yes | This study | No single-cause inference |
| C14 | INVALID 192 events / 136 arms | metrics + recompute | OBSERVED | Yes | Q2 live 432 | T0 INVALID not recomputed here |
| C15 | INVALID is a potential confounder; not discarded; not equivalent to attack success; not claimed negligible | protocol + C14 | INTERPRETATION | Yes | S0 official | Co-occurs with some Tool-HASR true |
| C16 | S2 9/9; 0 S0→S2 flips | invalid_sensitivity | DERIVED | Yes | Pre-specified S2 | Magnitudes ≠ S0 |
| C17 | `scientific_evidence=false` | manifest | OBSERVED | Yes | Q2 | Must appear in abstract |
| C18 | D3 deferred | lock | LIMITATION | Yes | Q2 | No D3 scores |
| C19 | C4 open attacker out of scope | D3_AND_C4 | LIMITATION | Yes | Claims | Not interactive adversary |
| C20 | Attribution study, not a defense leaderboard | absence | LIMITATION | Yes | Q2 | No external numbers |
| C21 | P1/P2/Q2 SHAs as listed; rechecked this pass | file hashes | OBSERVED | Yes | Frozen files | Stage-B bytes absent |
| C22 | Integrity/forensic PASS on Q2 run | audit JSON | OBSERVED | Yes | Q2 | ≠ scientific_evidence true |
| C23 | 21 arXiv identities | package Hub records | LITERATURE CLAIM | Yes for identity | 21 papers | Venues PARTIAL |
| C24 | PARTIAL_GAP residual sentence | novelty audit | INTERPRETATION | Qualified | Surveyed set | Not global uniqueness |
| C25 | SOTA / best / superior / guaranteed / production-ready / solves injection / causal effect | — | — | **Must not appear as assertion** | — | Forbidden |
| C26 | Q2 confirmatory | — | — | **Must not appear** | — | Protocol false |
| C27 | Track mixing / VNEXT reversal | dual-track | — | **Must not appear** | Different packs | Claims error |
| C28 | Stage-B traces present | glob | LIMITATION | Absence verified | Packaging | MISSING_LOCALLY |
| C29 | Figures 3–5 present | PNG files | DERIVED | Yes | Packaging | No significance encoding |
| C30 | T2 Δ equals T0 Δ | Table 4 | OBSERVED | Yes in sample | n=16 | Coincidence |
| C31 | Detector-related association, not unqualified causality | protocol | INTERPRETATION | Yes if scoped | This study | Limitation 19 |
| C32 | Task Shield is a verified bibliographic record | matrix | — | **No; not in matrix; not cited as reference** | — | UNVERIFIED_NOT_IN_MATRIX |
| C33 | 124/192 is locally verified T0 | STAGE_B | — | **Must not appear as local verification** | — | NOT_FOUND_ON_THIS_CHECKOUT |

**C00 allowed:** “the observed Δ direction remained consistent across T0–T3”; “9/9 preserved the negative direction”; “pilot-scale evidence of directional consistency under the tested protocol.”

**C00 forbidden:** universal/general robustness; SOTA; best detector/defense; production-ready; guaranteed security; causal proof; comprehensive generalization; superiority over external defenses.
