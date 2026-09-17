# Reviewer response matrix (document-only)

**Not an official review. No scores. No new experiments.**  
Manuscript under review: `MANUSCRIPT_FINAL.md`.  
Response class is **DOCUMENTATION_FIX** or **FUTURE_STUDY**. A new experiment is not automatically justified.

## Reviewer A — Security

**Likely criticism.** No CaMeL / AgentDojo / ASB / Llama Guard / PromptShield numbers; INVALID may drive Tool-HASR; Qwen-heavy set; open adaptive attacker missing; paper sounds like a defense system.

**Evidence-based answer.** The research question is controlled detector-related attribution, not comparative ranking of defenses. External baselines are outside the current primary claim (methodological scope). INVALID_TOOL_ARGS is a canonical execution-state category (192 events / 136 arms), retained in S0, not treated as attack success/failure/harmlessness/detector failure, and not claimed to explain all metric disagreement. Target set is four models, three Qwen-family; model-family diversity is limited. C4 / open-ended adaptive attackers are out of scope.

**Manuscript section.** Abstract; §6 Related Work; §10 Diagnostic Analysis; §11 Discussion; §12 Limitations (Table 6 items 4–8, 10–11).

**Unresolved limitation.** No matched external baseline exists. INVALID remains a confounder. Adaptive-attacker robustness is not established.

**New experiment necessary?** No, not to finish this package. **DOCUMENTATION_FIX** for scope sentences. **FUTURE_STUDY** for matched live baselines or C4.

## Reviewer B — ML / Statistics

**Likely criticism.** n=16/cell cannot support a general claim; 9/9 without a p-value; Wilson CIs wide; T2 exact Δ match to T0 looks over-interpreted; dual endpoints without a reconciliation test.

**Evidence-based answer.** n=16 per cell is stated as pilot-scale with limited precision and limited power. Directional consistency is an observed property of this evaluation; it does not establish population-level generalization. Inferential p-values were not preregistered and are not reported. Wilson 95% CIs are on rates, derived from locked counts, not on Δ. T2=T0 Δ is labeled n=16 coincidence. Tool-HASR vs Judge-ASR is diagnostic, not a significance contest. Paired discordants are descriptive.

**Manuscript section.** Abstract; §4 Research Question; §8 statistics paragraph; §9 Table 3 and Figure 3 caption; §10.1; `STATISTICAL_REPORTING.md`.

**Unresolved limitation.** No preregistered inferential test for Q2 exists. Manufacturing one would be a claims error. Power remains limited.

**New experiment necessary?** No, not to report this pilot honestly. **DOCUMENTATION_FIX** for n=16 / derived-CI labeling. **FUTURE_STUDY** for a preregistered powered confirmatory analysis on a new freeze.

## Reviewer C — Agent Evaluation

**Likely criticism.** T0 reuse plus missing Stage-B traces weakens the reference arm; Tool-HASR vs Judge-ASR (81/192 vs 186/192) looks like a broken metric; INVALID 192/136 looks like a failed harness; mock tools / short horizon; judge also Qwen.

**Evidence-based answer.** Official Stage-B reported T0 PHASE1-CORE is reused from the Q2 live report. Local Stage-B `predictions.jsonl` is `MISSING_LOCALLY`. The manuscript distinguishes official reported result from locally reproducible raw-trace availability and does not present T0 as independently recomputed. Tool-HASR and Judge-ASR are distinct measurements; M3=108, M4=3; possible disagreement sources are listed conservatively. INVALID is retained, not discarded. Pack/horizon/judge constraints are limitations.

**Manuscript section.** §8 Stage-B paragraph; §10; Table 5; Table 6 items 8–9, 12–15; `STAGE_B_EVIDENCE_STATUS.md`.

**Unresolved limitation.** Stage-B raw traces remain missing locally. Independent T0 INVALID recompute is impossible on this checkout. Metric disagreement is observed, not causally explained.

**New experiment necessary?** No, not if the hole is disclosed. **DOCUMENTATION_FIX** for official vs local distinction. **FUTURE_STUDY** to package original Stage-B bytes (read-only) or re-run T0 under rule 6.

## Reviewer D — Novelty / Related Work

**Likely criticism.** AgentDojo, ASB, CaMeL, IsolateGPT, instruction hierarchy, and InjecAgent already exist; factorial may overlap; bibliography venues incomplete; “first protocol” claim.

**Evidence-based answer.** Novelty class remains **PARTIAL_GAP**. The paper is not a new detector family and not a defense covering all threat models. Existing literature is separated from this paper’s controlled attribution protocol. Full-text novelty exclusion is not claimed. 21/21 identities are verified; most venue/DOI remain UNVERIFIED; AgentDojo/BIPIA venue/DOI are operator-supplied and not re-fetched. Names not in the matrix are not invented as citations.

**Manuscript section.** §6 Related Work; §14 Conclusion; `NOVELTY_AUDIT.md`; `BIBLIOGRAPHY_VERIFICATION.md`.

**Unresolved limitation.** Camera-ready venue/DOI for 19/21 records; operator-supplied AgentDojo/BIPIA not publisher-rechecked; full texts not end-to-end audited.

**New experiment necessary?** No. **DOCUMENTATION_FIX** for PARTIAL_GAP and bibliography honesty. **FUTURE_STUDY** for human venue/DOI verification from official pages (network allowed only under a later authorized bibliography pass) and optional full-text overlap audit.

## Cross-review

| Theme | Class | New experiment required to finish this package? |
| --- | --- | --- |
| n=16 / pilot-scale / not confirmatory | DOCUMENTATION_FIX | No |
| No external baseline | DOCUMENTATION_FIX (scope) | No; FUTURE_STUDY only if a ranking claim is later desired |
| Stage-B traces missing | DOCUMENTATION_FIX (disclose) | No; FUTURE_STUDY to package bytes |
| No Q2 p-values | DOCUMENTATION_FIX (do not manufacture) | No |
| PARTIAL bibliography | DOCUMENTATION_FIX | No for this package; required before camera-ready |
| INVALID / metric disagreement | DOCUMENTATION_FIX | No |
| D3 / C4 / more families | FUTURE_STUDY | Yes only if those claims are later desired |
| PARTIAL_GAP | DOCUMENTATION_FIX | No |
