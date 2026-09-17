# Weakness closure audit (final scientific publication supervisor)

**Date:** 2026-09-17  
**Branch:** `cursor/q2-publication-hardening-f6f3`  
**API_CALLS=0. LLM_CALLS=0. NETWORK_CALLS=0. LIVE_EVAL=false.**  
**Q2_RERUN=false. P1_MODIFIED=false. P2_MODIFIED=false. Q2_TRACE_MODIFIED=false.**

**STATUS = READY_WITH_MAJOR_REVISIONS**  
Not SUBMISSION_READY: bibliography is not fully publication-verified, and Stage-B raw traces remain MISSING_LOCALLY. Not BLOCKED: official Q2 numbers are internally consistent and no unsupported major claim remains in `MANUSCRIPT_FINAL.md`.

CI 2/2 PASS is **not** publication acceptance.

## Closed by documentation (no new experiment)

| Weakness | Closure | Residual |
| --- | --- | --- |
| Attribution vs new defense | Explicit PARTIAL_GAP; not a new detector family | Residual literature overlap untested at full-text |
| Abstract overclaim | Problem, method, 432/432, n=16, 9/9, Tool-HASR vs Judge-ASR, pilot-scale; no `scientific_evidence=false` string in abstract | Venue template still unapplied |
| n=16 hidden | Stated in Abstract, Results, Discussion, Conclusion, Table 6 | Fundamental: limited precision/power |
| Model diversity overstated | Table 2 families; three of four Qwen; judge Qwen | Fundamental: Qwen-heavy |
| INVALID treated as nuisance | Canonical execution-state; 192/136; S0/S1/S2 preserved | Confounder remains |
| Tool-HASR vs Judge-ASR collapsed | Distinct measurements; 81/192 vs 186/192; M3=108; M4=3 | Disagreement not causally explained |
| D3 implied | Deferred; embedding dependency not in locked offline protocol; future work | No D3 scores (by design) |
| C4 implied | Explicitly not established; future work | Adaptive robustness untested |
| External numerical baselines | Scope: attribution, not ranking | No matched comparison |
| Invented p-values | None; Wilson CIs labeled derived from locked counts | No confirmatory test |
| Table numbering | Tables 1–6 as specified | — |
| Introduction five-beat | Problem / Gap / Approach / Result / Qualification | — |
| Forbidden wording | Scanned; unsupported assertions removed | Negation phrasing uses “does not establish” |
| Stage-B presented as local recompute | Official vs local distinction; MISSING_LOCALLY retained | Traces still absent |
| Extra named papers invented | NOT_IN_PACKAGE; not cited | Not in bibliography |

## Not closed (and not closable without new evidence or network)

| Item | Class | Action |
| --- | --- | --- |
| Stage-B `predictions.jsonl` | Evidence/provenance | Disclose; do not fabricate; optional future packaging of original bytes |
| Bibliography venues/DOI | Documentation/metadata | Human publisher-page verification (later authorized network pass) |
| n=16 | Fundamental study limitation | Do not hide; larger n is FUTURE_STUDY |
| Qwen-heavy targets | Fundamental study limitation | Do not call the set diverse without qualification |
| D3 / C4 / matched baselines / more families | Future-study | New experiment only if those claims are later desired |

## Integrity flags (this pass)

| Flag | Value |
| --- | --- |
| P1_MODIFIED | false (SHA match) |
| P2_MODIFIED | false (SHA match) |
| Q2_TRACE_MODIFIED | false (SHA match) |
| Q2_RERUN | false |
| LIVE_EVAL | false |
| official results altered | false |
| missing evidence fabricated | false |
| derived statistics traceable to locked counts | true |
