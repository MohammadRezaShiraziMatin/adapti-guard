# arXiv readiness audit

## Repository audit

Audited against the Q2 publication-packaging branch and current default-branch state.

### Current default branch

`main` currently points to `6f3b1ccaf58a0b9cf44461f14a1b411d93999a78`.

The default branch contains the older dual-track/workshop-facing manuscript surface. The newer Q2 publication manuscript is on the publication-packaging lineage, not the default branch.

### Current manuscript surfaces

Historical/current surfaces found:

- `docs/paper/workshop_vnext_fail/MANUSCRIPT.md`: negative-result workshop/preprint text; explicitly not an arXiv deposit.
- `docs/paper/dual_track/DUAL_TRACK_STATUS.md`: Track A FAIL + Track B scoped result.
- `docs/research/q2_publication_package/MANUSCRIPT_V1.md`: current Q2 manuscript candidate.
- `docs/research/q2_publication_package/FINAL_PACKAGING_AUDIT.md`: prior packaging audit.

For the arXiv package, **MANUSCRIPT_V1.md is the selected scientific source** because it matches the current detector-attribution contribution and Q2 evidence.

## Scientific integrity

PASS:

- P1 frozen SHA preserved.
- P2 frozen SHA preserved.
- Q2 prediction SHA preserved.
- Q2 run ID preserved.
- Q2 live run was not rerun during packaging.
- `scientific_evidence=false` is retained.
- Tool-HASR is primary; Judge-ASR remains secondary.
- D3 remains deferred.
- No detector ranking is claimed.
- Track A / Track B / Q2 are kept separate.

Important disclosure:

- Stage-B `predictions.jsonl` is missing from the current checkout.
- Recorded Stage-B SHA is retained only as historical provenance.
- No Stage-B bytes are fabricated or reconstructed.
- T0 Q2 values are explicitly described as reused official results.

## Claims audit

Allowed:

> We introduce a controlled evaluation framework for isolating detector-related effects from downstream intervention policy in LLM-agent security, with a bounded pilot-scale cross-target directional-consistency analysis.

Allowed:

> Under locked PHASE1-CORE, the detector-related Tool-HASR effect observed on T0 retained its direction on T1–T3 in this pilot.

Forbidden:

- SOTA
- best detector
- first/unique/global novelty claim
- universal/model-independent protection
- production-ready
- solves prompt injection
- confirmatory multi-model claim
- Q1/Q2 journal-quartile claim

## Bibliography

The Q2 package contains 21 arXiv identifiers with title/author/year metadata verified in the existing package records. Venue/DOI metadata were deliberately not guessed. arXiv identifiers are sufficient for this preprint reference layer.

## arXiv-specific assessment

The previous Q2 packaging blockers about a journal template and venue/DOI are **not arXiv blockers**.

The actual arXiv blockers are:

1. Produce and inspect a final PDF.
2. Produce a clean TeX/source archive.
3. Ensure all referenced figures are included.
4. Remove internal repository-only paths from the final paper.
5. Verify final author metadata.
6. Perform a final PDF/source hygiene check.

arXiv's current TeX guidance says submissions are automatically processed, figures must be supplied, and extraneous/intermediate files should be excluded. It also recommends explicit arXiv identifiers in references. urlarXiv TeX submission guidancehttps://info.arxiv.org/help/submit_tex.html

## Final status

**Scientific package:** READY_WITH_DISCLOSURES

**Submission package:** READY after local PDF build + manual inspection.

**Not yet submitted to arXiv.**
