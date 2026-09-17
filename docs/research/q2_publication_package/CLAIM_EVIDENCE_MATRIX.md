# Claim–evidence matrix (MANUSCRIPT_V1)

**API=0.** Every substantive claim in `MANUSCRIPT_V1.md` is classified. Unsupported claims must be flagged. Meta lists of forbidden words are not claims.

Legend: **OBSERVED** locked-run fact · **DERIVED** computed from observed · **INTERPRETATION** scoped reading · **LITERATURE CLAIM** Hub-verified metadata only · **LIMITATION** absence or bound · **UNVERIFIED** not established.

| ID | CLAIM | SOURCE | EVIDENCE TYPE | VERIFIED? | SCOPE | LIMITATION |
| --- | --- | --- | --- | --- | --- | --- |
| C01 | Agent security outcomes mix detection and intervention | Method / intro | INTERPRETATION | Yes as framing | Conceptual | Not an empirical Q2 result |
| C02 | Hard to attribute security numbers to detectors if policy also moves | Intro / related work | INTERPRETATION | Yes as gap statement | Methodological | Novelty is PARTIAL GAP, not CLEAR GAP |
| C03 | Q2 holds PHASE1-CORE, pack, judge, thresholds, costs fixed and varies D0/D1/D2/D4 | `manifest.json`, lock files | OBSERVED | Yes | Q2 live + T0 reuse | T0 not re-run |
| C04 | Tool-HASR is primary; Judge-ASR secondary | Protocol / `p3_stage_c_q2.py` | OBSERVED (protocol) | Yes | This study | Other papers use other endpoints |
| C05 | 432/432 arms completed, 0 failed | `manifest` / live report | OBSERVED | Yes | Q2 live T1–T3 | T0 arms are Stage-B, not in 432 |
| C06 | Historical spend $0.152885 / cap $10 | `spend.json` | OBSERVED | Yes | Q2 live | Not intervention USD |
| C07 | Cell Tool-HASR n/N and Wilson CIs as tabulated | `q2_final_statistics.json` | DERIVED | Yes (matches live report) | n=16/cell | Wide CIs |
| C08 | All twelve Δ(d,t) for D1/D2/D4 × T0–T3 are NEG | statistics JSON | DERIVED | Yes | These 12 cells | No Δ CI; not a ranking |
| C09 | Sign agreement 9/9 | statistics JSON / live report | DERIVED | Yes | 3 detectors × 3 secondary targets | Descriptive; no Q2 p-value |
| C10 | Directionally consistent on selected T0–T3 | C08+C09 | INTERPRETATION | Yes if scoped | Four OpenRouter models | Not all LLMs; not confirmatory |
| C11 | Q2 live Tool-HASR 81/192; Judge-ASR 186/192 | statistics / Table 4 | DERIVED | Yes | T1–T3 attack arms | Pooled across detectors; not a ranking |
| C12 | M3=108, M4=3 on T1–T3 | statistics | DERIVED | Yes | T1–T3 | Diagnostic, not a win/loss |
| C13 | Judge-ASR is a different endpoint, not invalid | C11–C12 | INTERPRETATION | Yes | This study | Does not validate the judge |
| C14 | INVALID 192 events / 136 arms | `metrics.json` + recompute | OBSERVED | Yes | Q2 live 432 arms | T0 INVALID not recomputed here |
| C15 | INVALID is not Tool-HASR success and not negligible | protocol + C14 | INTERPRETATION | Yes | S0 official | Co-occurs with some Tool-HASR true |
| C16 | S2 sign agreement remains 9/9; 0 S0→S2 sign flips | `invalid_sensitivity` | DERIVED | Yes | Pre-specified S2 | Magnitudes ≠ S0 |
| C17 | `scientific_evidence=false` | `manifest.json` | OBSERVED | Yes | Q2 run | Must appear in abstract |
| C18 | D3 has no scores | detectors init / lock | LIMITATION | Yes | Q2 | Do not fill N/A% as a measurement |
| C19 | Open C4 adaptive attacker out of scope | taxonomy / `D3_AND_C4.md` | LIMITATION | Yes | Claims | P2 C4-mini ≠ interactive attacker |
| C20 | No external baseline on this pack | absence | LIMITATION | Yes (absence) | Q2 | Not a comparative benchmark |
| C21 | P1 SHA `1a0b0053…dd235`; P2 SHA `32b40e3b…8d64dd`; Q2 pred SHA `2a2c2f31…886cc6` | file hashes | OBSERVED | Yes this checkout | Frozen files | Stage-B file hash not rechecked |
| C22 | Integrity PASS / forensic PASS | Q2 audit JSON | OBSERVED | Yes | Q2 run | Does not imply scientific_evidence true |
| C23 | Related-work titles/authors/years/arXiv | Hub metadata | LITERATURE CLAIM | Yes for those fields | 21 papers | Venue/DOI UNVERIFIED |
| C24 | Isolation protocol is a partial literature gap | novelty audit | INTERPRETATION | Qualified | Surveyed set | Uncertain overlap with AgentDojo/ASB |
| C25 | Production-ready / SOTA / best / universal / solves injection | — | — | **Must not appear as assertion** | — | Forbidden |
| C26 | Q2 is confirmatory | — | — | **Must not appear as assertion** | — | Protocol says false |
| C27 | Track B reverses Track A or Q2 reverses VNEXT FAIL | dual-track docs | — | **Must not appear** | Different packs | Mixing is a claims error |
| C28 | Stage-B predictions present on this checkout | glob | LIMITATION | Absence verified | Packaging | T0 INVALID cited prior derived |
| C29 | matplotlib figures rendered | import check | LIMITATION | Absence | Packaging | Specs/scripts only |
| C30 | Δ T2 equals Δ T0 exactly | Table 3 | OBSERVED | Yes in sample | n=16 | Coincidence; not general equality |

No unsupported positive empirical claims were left unflagged. C23 venues remain UNVERIFIED by design.
