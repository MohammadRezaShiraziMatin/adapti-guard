# Q2 Reviewer Attack (simulated)

**Not an official review. No scores. No acceptance prediction. No new experiments.**
Manuscript under review: `MANUSCRIPT_FINAL.md`.
For every criticism: `severity | evidence | fix possible now? | action`.

## Reviewer A — Security / ML

| # | Criticism | Severity | Evidence | Fix possible now? | Action |
| --- | --- | --- | --- | --- | --- |
| A1 | Novelty is thin; AgentDojo/ASB/CaMeL already cover agent security | MAJOR | `Q2_NOVELTY_AUDIT.md` PARTIAL_GAP; full-text overlap not audited | Yes (documentation) | Keep PARTIAL_GAP; do not claim "first"; separate existing literature from this protocol |
| A2 | Detector attribution may be entangled with provider/runtime tool formatting | MAJOR | OpenRouter-only; INVALID 192/136 | No (new run) | Document as limitation (Table 6 items 5, 15); FUTURE_STUDY for provider factor |
| A3 | Benchmark validity: mock tools, short horizon, one pack | MAJOR | `p2_agentic_v0.1.0` SHA `32b40e3b…` | No (new pack) | Document as protocol-specific limitation; FUTURE_STUDY |
| A4 | D3 missing weakens detector coverage | MINOR | `DEFERRED_NO_OFFLINE_IMPL` | No (new offline lock) | State D3 deferred; FUTURE_STUDY |
| A5 | No external baseline numbers | MAJOR | `BASELINE_GAP.md` | No (matched live run) | Scope sentence; FUTURE_STUDY only if ranking claim desired |

## Reviewer B — Reproducibility

| # | Criticism | Severity | Evidence | Fix possible now? | Action |
| --- | --- | --- | --- | --- | --- |
| B1 | Stage-B raw traces unavailable; T0 not independently recomputed | MAJOR | `STAGE_B_EVIDENCE_STATUS.md` MISSING_LOCALLY; git object hits 0 | No (need original bytes) | Disclose official vs local distinction; FUTURE_STUDY to package bytes read-only |
| B2 | Bibliography venues/DOI mostly UNVERIFIED | MAJOR | `BIBLIOGRAPHY_VERIFICATION.md` PARTIAL | No (NETWORK=0) | Document PARTIAL; FUTURE_STUDY human publisher-page verification |
| B3 | Wilson CIs are wide; no inferential test | MINOR | n=16; `STATISTICAL_REPORTING.md` | No (post-hoc) | Do not manufacture p-values; label CIs derived from locked counts; FUTURE_STUDY preregistered test |
| B4 | matplotlib unavailable | INFORMATIONAL | `figure_metadata.json` renderer stdlib_zlib | Yes (already handled) | Figures rendered offline; no network install |
| B5 | INVALID deduplication and denominator treatment | MINOR | `INVALID_TOOL_ARGS_ANALYSIS.md` 192/136; S0/S1/S2 | Yes (already documented) | Retain S0; S1/S2 sensitivity; do not silently drop |

## Reviewer C — LLM / Agent Evaluation

| # | Criticism | Severity | Evidence | Fix possible now? | Action |
| --- | --- | --- | --- | --- | --- |
| C1 | Tool-HASR (81/192) vs Judge-ASR (186/192) looks like a broken metric | MAJOR | M3=108, M4=3 | Yes (documentation) | Keep distinct; list disagreement sources conservatively; do not declare either invalid |
| C2 | Qwen-heavy target set; judge also Qwen | MAJOR | Table 2: T0/T1/T3 Qwen; judge Qwen | No (new targets) | Document limited family diversity; FUTURE_STUDY |
| C3 | No open adaptive attacker (C4) | MAJOR | `D3_AND_C4.md` | No (new run) | Out of scope; FUTURE_STUDY |
| C4 | Generalization to arbitrary model families not shown | MAJOR | n=16; four models | No (new run) | State does not establish population-level generalization; FUTURE_STUDY |
| C5 | INVALID may drive Tool-HASR | MINOR | 192/136; co-occurrence with Tool-HASR true | Yes (documentation) | Treat as confounder; not negligible; not all disagreement |

## Cross-review action map

| Theme | Class | New experiment required to finish this package? |
| --- | --- | --- |
| n=16 / pilot-scale / not confirmatory | DOCUMENTATION_FIX | No |
| No external baseline | DOCUMENTATION_FIX (scope) | No; FUTURE_STUDY only if ranking claim later desired |
| Stage-B traces missing | DOCUMENTATION_FIX (disclose) | No; FUTURE_STUDY to package bytes |
| No Q2 p-values | DOCUMENTATION_FIX (do not manufacture) | No |
| PARTIAL bibliography | DOCUMENTATION_FIX | No for this package; required before camera-ready |
| INVALID / metric disagreement | DOCUMENTATION_FIX | No |
| D3 / C4 / more families | FUTURE_STUDY | Yes only if those claims are later desired |
| PARTIAL_GAP | DOCUMENTATION_FIX | No |

## Summary

No simulated criticism requires a new experiment to finish **this** package. All MAJOR/MINOR items are either already documented as limitations or are documentation/provenance fixes. The two genuine provenance/metadata blockers (Stage-B traces, bibliography) keep the package at READY_WITH_MAJOR_REVISIONS but do not contradict any reported Q2 number.
