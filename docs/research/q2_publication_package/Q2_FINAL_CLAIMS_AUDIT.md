# Q2 final claims language audit

**Scope:** `docs/research/q2_publication_package/` after manuscript V1.  
**API=0.** Frozen Q2 evidence not edited.

Meta documentation that **lists** forbidden terms as forbidden does **not** count as an unsupported claim.

## Search terms

`best` · `better` · `superior` · `SOTA` · `state-of-the-art` · `guarantee` · `guaranteed` · `universal` · `universally` · `production-ready` · `optimal` · `solves` · `proves`

(Also scanned: `confirmatory` as a Q2-status word.)

## Substantive vs meta

| File | Hits | Classification |
| --- | --- | --- |
| `MANUSCRIPT_V1.md` | “does not claim … production”; “not … confirmatory”; related-work notes that Hub abstracts of MELON/Meta SecAlign *use* SOTA language **which Q2 must not import** | Allowed negation / literature-hygiene. No asserted SOTA. |
| `CONTRIBUTION_POSITIONING.md` | Non-claims list | Meta |
| `BASELINE_GAP.md` | Forbidden examples; “cannot claim superiority” | Meta |
| `NOVELTY_AUDIT.md` | “not novel”; “do not write first” | Meta |
| `PROJECT_STATUS.md` | NOT CLAIMABLE list | Meta |
| `CLAIM_EVIDENCE_MATRIX.md` | Forbidden row C25–C27 | Meta |
| `PEER_REVIEW_SIMULATION.md` | Reviewer language | Meta |
| `VENUE_REQUIREMENTS.md` | Venue category names | Meta (not performance claims) |
| `q2_claims_audit*.md`, `STATISTICAL_REPORTING.md`, `LIMITATIONS.md` | Banned-term tables | Meta |
| Frozen `manifest.json` research_question | “generalize (same sign)” | Frozen; publication prose uses **directionally consistent** instead. **Do not edit the frozen file.** |

## Flagged residual risks (writing, not new evidence)

1. Manuscript related-work mentions that MELON/Meta SecAlign Hub abstracts contain SOTA wording — must stay clearly attributed to those abstracts, never adopted.
2. “Better” must not appear as “D1 is better than D2.” Grep after this audit should show no such ranking sentence in `MANUSCRIPT_V1.md`.
3. “Universal” appears in BIPIA Hub summary (“universally vulnerable”) — if quoted, attribute; do not say Q2 is universally effective.

## MANUSCRIPT_V1 hits (all negations / non-claims)

| Line | Term context | Flag? |
| --- | --- | --- |
| Abstract contribution | “does not claim a universal defense, a best detector, or production robustness” | No — forbidden terms listed as non-claims |
| Introduction | “not evidence that any detector is best, that the system is production-ready, or that prompt injection is solved” | No |
| Cross-target | “does not establish universal LLM generalization, production robustness” | No |
| Conclusion | “does not establish a universal defense, a best detector, production robustness” | No |

No ranking sentence (“D1 is better than D2”). Contrast vs D0 uses “lower Tool-HASR than a no-detection arm,” which is the locked estimand, not a detector ranking.

`generate_tables_figures.py` package-wide scan reported 154 hits; inspection shows meta/forbidden-example lists plus the four manuscript negations.

## Result

**CLAIMS_STATUS = scoped_GREEN_no_asserted_SOTA**

No asserted best/superior/SOTA/production-ready/universal-robustness/solves-injection/proves-all-LLMs claim in manuscript results. Q2 is not called confirmatory.
