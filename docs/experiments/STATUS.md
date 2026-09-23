# Experiments — tip status (docs)

**Updated:** 2026-09-23 (tip `main`, SHA `e4870b9` until PR #74 merge; Q1 P1–P2 on branch)  
**Mode:** Documentation and decision locks only. **API=0.** Agents do not merge.

---

## Tip intent

Raise **publisher readiness** and remove **process/admin bottlenecks** via honest docs — not by changing frozen science or rerunning live eval.

**Workshop quality path (done):** [`QUALITY_ROADMAP_5PHASE.md`](QUALITY_ROADMAP_5PHASE.md) **P1–P5 complete** on tip `e4870b9` (PR #73 merged to `main`).

**Q1 findings ladder (active, PR #74):** **P1–P2 complete**; **P4 packet ready for human review** ([`docs/paper/q1_findings/`](../paper/q1_findings/README.md) — manuscript, cover packet, bib, figures, [`VENUE_SHORTLIST.md`](../paper/q1_findings/VENUE_SHORTLIST.md)); **P3 not done** (budget). Roadmap · matrix · Q1-P2: [`Q1_ROADMAP_4PHASE.md`](Q1_ROADMAP_4PHASE.md) · [`Q1_BLOCKER_MATRIX.md`](Q1_BLOCKER_MATRIX.md) · [`DECISION_LOCK_Q1_P2_EVIDENCE_DESIGN.md`](DECISION_LOCK_Q1_P2_EVIDENCE_DESIGN.md). Not a redo of the workshop five-phase path.

---

## Science locks (unchanged)

| Track | Outcome | Pack / pointer |
| --- | --- | --- |
| **A — VNEXT** | **FAIL** (immutable) | `vnext_confirm_v1.0`, SHA `523c881820710783b5290c76ea5fe5fc01a6341fb427defcba1119fc3e721518`; AUDIT `experiments/real_llm_eval/VNEXT_CONFIRM/20260914-133147/` |
| **B — Phase-1 LIVE** | **SUPPORTED_IMPROVEMENT** (scoped) | `phase1_confirm_v1`, SHA `c789811a07d3ed06e1c77d8a45eda6172f480226e006d84fa28386a982536d01`; AUDIT `experiments/real_llm_eval/PHASE1_CONFIRM/phase1_confirm_20260914T213022Z_a2681e92/` |

Track B **does not** reverse Track A. Wording: [`docs/paper/dual_track/CLAIMS_DUAL_TRACK.md`](../paper/dual_track/CLAIMS_DUAL_TRACK.md) · one-liners [`docs/paper/CLAIMS_CHECKLIST.md`](../paper/CLAIMS_CHECKLIST.md).

Do not edit `datasets/frozen/**` or `experiments/real_llm_eval/**` AUDIT/verdict/numbers.

---

## D-22 — Confirmatory V2 taxonomy (names locked)

**Decision:** Option A — six `family_id` strings from frozen `datasets/frozen/vnext_confirm_v1` (`manifest.json` → `family_counts`).

**Record:** [`DECISION_LOCK_D22_CONFIRMATORY_V2_TAXONOMY.md`](DECISION_LOCK_D22_CONFIRMATORY_V2_TAXONOMY.md)

**Q1 cycle (Q1-P2):** V2 episodes, 151 allocation table, SAP, and new pack bytes = **Future Work**; paper uses Track A/B n=61 only. **When V2 is later authorized:** +1 remainder → **`PRIVILEGE_EXFIL`** (25 per other family) — [`DECISION_LOCK_Q1_P2_EVIDENCE_DESIGN.md`](DECISION_LOCK_Q1_P2_EVIDENCE_DESIGN.md) §B.

No prior `DECISION_REQUEST` file was found under `docs/` at lock time; any informal request is **closed** by the D-22 lock doc above.

---

## Open PRs and merge

Official index: [`docs/paper/workshop_vnext_fail/PR_STACK.md`](../paper/workshop_vnext_fail/PR_STACK.md) (PRs #23–#44 stack). **Human merge only.** Agents never merge and never close PRs via API.

This quality PR is a **single docs-only branch off tip `main`**, separate from the historical stack unless Matin chooses to integrate it.

---

## Manuscript / claims (P3 done)

Workshop FAIL text: [`docs/paper/workshop_vnext_fail/MANUSCRIPT.md`](../paper/workshop_vnext_fail/MANUSCRIPT.md). Human cover: [`SUBMISSION_PACKET.md`](../paper/workshop_vnext_fail/SUBMISSION_PACKET.md). Author: **Seyed Mohammadreza Shirazi Matin**.

## Reproducibility (P4 done)

Hub: [`REPRODUCIBILITY_PACKAGE.md`](REPRODUCIBILITY_PACKAGE.md) · hashes [`APPENDIX_HASHES.md`](../paper/workshop_vnext_fail/APPENDIX_HASHES.md) · offline: `verify_manuscript_facts.py` + pytest (no OpenRouter).

## Workshop submit (P5 done)

Checklist: [`docs/paper/workshop_vnext_fail/SUBMISSION_CHECKLIST.md`](../paper/workshop_vnext_fail/SUBMISSION_CHECKLIST.md) · packet [`SUBMISSION_PACKET.md`](../paper/workshop_vnext_fail/SUBMISSION_PACKET.md).

## Next (human only)

1. Review **Q1 P1–P2 + P4 draft** on PR #74 (`q1_findings/` manuscript).  
2. **Choose venue** (TBD) for workshop packet and/or Q1 manuscript — **submit** camera-ready; agents do not upload.  
3. Optional: historical PR stack merge per [`PR_STACK.md`](../paper/workshop_vnext_fail/PR_STACK.md).  
4. **Budget sign-off** before any Q1 Phase 3 live eval (`API=0` until then).
