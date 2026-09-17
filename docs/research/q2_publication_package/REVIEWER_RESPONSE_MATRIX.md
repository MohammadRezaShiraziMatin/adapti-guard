# Reviewer response matrix (document-only)

**Not an official review. No scores. No new experiments.**  
Manuscript under review: `MANUSCRIPT_FINAL.md`.  
Separate **required for submission** from **future-study recommendations**.

## Reviewer 1 — methodology / experimental design

**Likely criticism.** n=16/cell and four models cannot support a general claim; T0 reuse plus missing Stage-B traces weakens the reference arm; factorial is still one policy.

**Does the manuscript answer it?** Yes, as scope. Research Question and Experimental Protocol state `scientific_evidence=false`, n=16, PHASE1-CORE-only Q2 live. Limitations Table 7 items 1–3, 9, 15. Reproducibility states PARTIAL.

**Exact sections.** §2 Research Question; §6 Experimental Protocol (Tables 1–2); §10 Limitations; §11 Reproducibility.

**Remaining unresolved.** Stage-B raw traces MISSING_LOCALLY. Independent T0 INVALID recompute is impossible on this checkout.

**Required for submission.** Keep pilot framing; document Stage-B hole in the PDF (already in §6 and §10).  
**Future study.** Larger n; re-run or package T0 traces; optional policy factor — new experiment.

## Reviewer 2 — security / agent robustness

**Likely criticism.** No CaMeL / AgentDojo / ASB / Llama Guard / PromptShield / IsolateGPT / Task Shield numbers; INVALID may drive Tool-HASR; Qwen-heavy set; open adaptive attacker missing.

**Does the manuscript answer it?** Yes, as an attribution study not a leaderboard (§4, §9). INVALID treated as a confounder, not discarded, not claimed negligible (§3, §8.2, Table 6). C4 out of scope (§10). Task Shield is explicitly not a verified citation and not compared.

**Exact sections.** §4 Related Work; §8 Diagnostic Analysis; §9 Discussion; §10 Limitations items 7–12.

**Remaining unresolved.** No matched external baseline exists. That is a documented scope boundary, not a hidden weakness.

**Required for submission.** Keep the scope sentence in abstract and discussion.  
**Future study.** Matched live baseline experiment if a comparative-defense claim is later desired.

## Reviewer 3 — ML / statistics

**Likely criticism.** 9/9 without a p-value; Wilson CIs wide; T2 exact Δ match to T0 looks over-interpreted; dual endpoints without a reconciliation test.

**Does the manuscript answer it?** Yes. §2 states p-values were not preregistered and are not reported. McNemar is not reported. Wilson CIs are on rates only. T2=T0 Δ is labeled n=16 coincidence. Tool-HASR vs Judge-ASR is diagnostic, not a significance contest. Paired discordants are descriptive.

**Exact sections.** §2; §6 statistics paragraph; §7 Table 3–4 and Figure 3 caption; §8.1; `STATISTICAL_REPORTING.md`.

**Remaining unresolved.** No preregistered inferential test for Q2 exists. Manufacturing one would be a claims error.

**Required for submission.** Do not add post-hoc p-values.  
**Future study.** Pre-register a powered confirmatory analysis on a new freeze.

## Reviewer 4 — novelty / related work

**Likely criticism.** AgentDojo, ASB, CaMeL, IsolateGPT, instruction hierarchy, and InjecAgent already exist; factorial may overlap; bibliography venues incomplete.

**Does the manuscript answer it?** Partially. §4 distinguishes those verified papers, keeps PARTIAL_GAP, does not claim novel detector families, does not claim full-text exclusion, does not add Task Shield as a fabricated record. Bibliography status is PARTIAL and disclosed.

**Exact sections.** §4 Related Work; §12 Conclusion; `NOVELTY_AUDIT.md`; `BIBLIOGRAPHY_VERIFICATION.md`.

**Remaining unresolved.** Camera-ready venue/DOI for 19/21 records; operator-supplied AgentDojo/BIPIA not publisher-rechecked; full texts not end-to-end audited.

**Required for submission.** Human venue/DOI verification from official pages.  
**Future study.** Full-text overlap audit if authors later want to shrink PARTIAL_GAP — still not a “first” claim.

## Cross-review

| Theme | Required for submission? | Future study? |
| --- | --- | --- |
| n=16 / scientific_evidence=false | Keep honest framing | Larger n |
| No external baseline | Keep attribution scope | Matched live comparison |
| Stage-B traces missing | Disclose; do not fabricate | Package original bytes |
| No Q2 p-values | Do not manufacture | New preregistered confirmatory study |
| PARTIAL bibliography | Verify venues before camera-ready | — |
| INVALID / metric disagreement | Already in diagnostics | — |
