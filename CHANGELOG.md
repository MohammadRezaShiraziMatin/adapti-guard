# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [0.1.0]

### Added

- Pilot-scale Q2 evaluation: 432/432 arms completed under locked PHASE1-CORE policy with 9/9 directional sign agreements across T0–T3. Historical cost $0.152885; n=16 attack arms per cell.
- Stage-B integration: T0 reused from `p3_stage_b_20260916T235438Z_7e401714` (not re-run). Stage-B forensic audit PASS.
- Manuscript finalization: 14-section Research Paper (`MANUSCRIPT_FINAL.md`) with Tables 1–6, Figures 3–5, 21 bibliography entries.
- Bibliography verification: 21/21 arXiv identities verified from arXiv API; 18/21 venues verified from official sources (doi.org, ACL Anthology, ICLR/OpenReview, CEUR-WS, author publication page); 3 confirmed preprints.
- CI workflows: GitHub Actions `tests.yml` with pytest and ruff lint jobs.
- Controlled attribution protocol: hold downstream intervention policy fixed (PHASE1-CORE), vary detector identity including D0 reference, measure Tool-HASR as primary outcome, test directional consistency across independently selected target models.

### Known limitations

- REPRODUCIBILITY_STATUS = PARTIAL. Stage-B raw traces (`predictions.jsonl`, `metrics.json`, `manifest.json` for `p3_stage_b_20260916T235438Z_7e401714`) are MISSING_LOCALLY. The SHA pointer and packaged metrics are available; raw bytes are not.
- n=16 per cell: pilot-scale, not confirmatory. `scientific_evidence=false`.
- Qwen-heavy target set: 3 of 4 targets are Qwen-family; judge also Qwen.
- No matched external baseline identified (attribution scope, not comparative ranking).
- D3 deferred: semantic-embedding dependency not part of locked offline protocol.
- C4 / open adaptive attacker out of scope.
