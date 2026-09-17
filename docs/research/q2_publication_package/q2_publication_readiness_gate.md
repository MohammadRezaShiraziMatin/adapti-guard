# Q2 Publication Readiness Gate

| Dimension | Assessment |
| --- | --- |
| A Scientific validity | Protocol-valid pilot consistency; Δ signs stable; dual-metric forensics present |
| B Experimental integrity | Q2 432/432, 0 failed, integrity PASS, forensic PASS; T0 reuse documented |
| C Statistical completeness | Wilson CIs, Δ, Δ-change, sign agreement, paired bits, S0/S1/S2 packaged |
| D Novelty clarity | Central contribution framed; needs verified external related work |
| E Baseline positioning | External baselines unavailable — documented gap (not fabricated) |
| F Reproducibility | SHAs, run IDs, locks, raw traces retained |
| G Limitations | Reviewer-facing list written |
| H Writing readiness | Blueprint + claims audit ready; full manuscript not yet drafted |
| I Figure/table readiness | Specs complete; plots not yet rendered |
| J Journal-fit readiness | Fit as protocol/attribution + bounded multi-target consistency paper |

## Verdict

**Q2_PUBLICATION_READINESS = READY_WITH_REQUIRED_REVISIONS**

### Required revisions (no new experiments)
1. Draft manuscript enforcing one central contribution + claims audit
2. Verified related-work citations (no invented refs)
3. Render figures/tables from `q2_final_statistics.json` only
4. Explicit `scientific_evidence=false` / pilot framing in abstract
5. Baseline gap paragraph (unavailable fair reconstructions)
6. Full limitations section from `q2_limitations.md`
7. Purge RED claims / banned stems

### Not blockers requiring new live spend
- External baselines (acknowledge)
- D3 deferred (acknowledge)
- Larger n / more models (future work)
