# Final peer-review response matrix (document-only)

**Not an official review. No numeric scores. No new experiments.**  
Document-only simulated review of `MANUSCRIPT_V1.md` after the hardening pass.

## Reviewer concern → response

### Sample too small

**Concern:** n is too small for a security paper.

**Response:** Pilot-scale directional study; n=16/cell; `scientific_evidence=false`. Wilson 95% CIs are reported on rates. Magnitudes are not over-read. Inferential p-values were not preregistered and are not reported. The claim is protocol-complete directional consistency (9/9 sign agreement), not confirmatory power.

### No external baseline

**Concern:** No comparison to CaMeL, AgentDojo defenses, ASB defenses, Llama Guard, PromptShield.

**Response:** This is an attribution protocol, not a defense leaderboard. Protocols, populations, metrics, and execution environments differ. Numerical cross-paper comparison is a claims error (`BASELINE_GAP.md`). Closing that gap would be a new matched live study, not a silent extension of Q2.

### Missing Stage-B raw traces

**Concern:** T0 is reused but `predictions.jsonl` is absent.

**Response:** Official packaged T0 PHASE1-CORE results are retained from the Q2 live report (Tool-HASR 28/64; Judge-ASR 55/64; M3=33; M4=6). Raw traces are unavailable in the current checkout (`STAGE_B_TRACE_STATUS=MISSING_LOCALLY`). No reconstruction was attempted. Operator-stated 124/192 was not found as a local file and is not used as independently recomputed T0. Reproducibility status is PARTIAL.

### Novelty overlap

**Concern:** AgentDojo, ASB, CaMeL, IsolateGPT already exist.

**Response:** Expanded related work; paper identities of AgentDojo and ASB are VERIFIED (not UNCERTAIN); CaMeL is a published architectural defense, not an unverified idea. Contribution is narrowed to controlled attribution. `NOVELTY_CLASS=PARTIAL_GAP`. Residual sentence: the verified literature does not establish the exact locked-policy detector-attribution factorial used here as the central measurement protocol. No “first” / “unique” / “no prior work” claim.

### INVALID_TOOL_ARGS

**Concern:** Schema failures may drive Tool-HASR.

**Response:** Explicit diagnostic and sensitivity treatment. INVALID is frequent (192 events / 136 arms on Q2 live), not silently discarded, not treated as harmless, and can affect Tool-HASR interpretation. S0 remains official. S2 sign agreement remains 9/9. This does not prove invalid arguments are negligible (`INVALID_TOOL_ARGS_ANALYSIS.md`).

### Judge-ASR dependence

**Concern:** Results depend on a judge model.

**Response:** Tool-HASR is primary; Judge-ASR is secondary and non-identical. T1–T3 Tool-HASR 81/192 vs Judge-ASR 186/192 (M3=108, M4=3). They can disagree because of refusal, blocked execution, invalid arguments, judge interpretation, or runtime/provider behavior. The paper does not conclude that Judge-ASR is invalid.

### Model diversity

**Concern:** Four Qwen-heavy targets.

**Response:** Four Qwen-heavy targets; transfer beyond this set is not claimed. T2 is Gemma-3; T0/T1/T3 and the judge are Qwen-line. Limited architectural diversity is a listed limitation.

### Additional anticipated concerns

| Concern | Response |
| --- | --- |
| Causal proof of detectors | Detector-related effect under a locked policy; not universal detector causality |
| Ranking D1/D2/D4 | `no_ranking=true`; figures do not encode winners or significance |
| Q2 “supported” vs Track B | Protocol sign-agreement only; not `SUPPORTED_IMPROVEMENT`; not a qualified win |
| Dual-track contamination | Track A FAIL immutable; Track B scoped; Q2 must not be pooled |
| Venue template / deadlines | `VENUE_DECISION_MATRIX.md`; deadlines UNVERIFIED; no venue selected |
| Bibliography camera-ready | PARTIAL; most venue/DOI UNVERIFIED |

## Consensus (document-only)

**Major revisions** remain appropriate. Genuine blockers: Stage-B raw traces missing; bibliography not fully verified. No new live Q2 rerun is required to answer these reviews.
