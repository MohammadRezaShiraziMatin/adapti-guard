# Quality roadmap — five phases (docs / process)

**Tip baseline:** `main` @ `30ddc75` (2026-09-23 process unlock)  
**Scope:** Documentation and admin/process clarity only. **API=0.** No merge from agents.

This roadmap separates **process unlocks** (what contributors may do on tip without changing science) from **science locks** (immutable evidence and honest dual-track outcomes).

---

## Science locks (kept in every phase)

| Lock | Rule |
| --- | --- |
| Frozen packs | Do not edit `datasets/frozen/**` bytes or quoted SHA-256 in AUDIT/verdict. |
| Live eval artifacts | Do not edit `experiments/real_llm_eval/**` AUDIT, verdict, or reported numbers. |
| Track A | VNEXT confirmation **FAIL** remains FAIL (`vnext_confirm_v1.0`, SHA `523c8818…`). |
| Track B | Phase-1 LIVE **SUPPORTED_IMPROVEMENT** on `phase1_confirm_v1` — scoped; **does not reverse Track A**. |
| Live LLM | No OpenRouter / API calls unless explicit human budget sign-off (default **API=0**). |
| Metrics | No invented statistics; cite frozen AUDIT or mark **BLOCKING GAP**. |
| Merge / venue | **Human-only:** no agent merge, no venue upload, no PR close via API. |

---

## P1 — Hygiene and truth docs (this PR)

**Unlocks:** Refresh navigation (`START_HERE`, experiment status), publish this roadmap, resolve doc conflict markers if present (tip truth: dual-track FAIL + Track B scoped improvement).

**Does not unlock:** New frozen bytes, live eval, claim reversal, or Phase-2 harness implementation.

**Deliverables:** `QUALITY_ROADMAP_5PHASE.md`, `STATUS.md`, minimal `START_HERE` pointer, D-22 name lock (P2 doc).

---

## P2 — D-22 taxonomy decision lock (names only; with P1 in same PR)

**Unlocks:** Lock **six** Confirmatory V2 `family_id` strings aligned to Track A frozen pack `datasets/frozen/vnext_confirm_v1` (see `DECISION_LOCK_D22_CONFIRMATORY_V2_TAXONOMY.md`).

**Still not locked:** Episode text, 151 attack allocation table, SAP, new dataset files, live eval.

**Does not unlock:** Building Confirmatory V2 episodes or changing historical n_attack=61 evidence.

---

## P3 — Manuscript claims polish

**Unlocks:** Wording pass on workshop/dual-track manuscript docs under `docs/paper/` — allowed/forbidden claims, cross-links, publisher-facing consistency with `CLAIMS_DUAL_TRACK.md`.

**Locks kept:** All AUDIT numbers and FAIL/SUPPORTED_IMPROVEMENT outcomes unchanged.

---

## P4 — Artifact and reproducibility

**Unlocks:** Repro checklists, hash citation tables, offline verification steps (no LLM), alignment of `REPRODUCIBILITY_PACKAGE.md` with tip tree.

**Locks kept:** No regeneration of eval outputs; simulation ≠ confirmatory live claims.

---

## P5 — Workshop submit checklist (no external upload)

**Unlocks:** Human checklist: merge order (`PR_STACK.md`), packet completeness, citation/hashes, **explicit** “human submits venue” steps — documentation only.

**Locks kept:** Agents do not submit to arXiv/workshop; Track A FAIL narrative unchanged.

---

## Read order after P1

1. [`docs/START_HERE.md`](../START_HERE.md)  
2. [`STATUS.md`](STATUS.md) (this folder)  
3. [`DECISION_LOCK_D22_CONFIRMATORY_V2_TAXONOMY.md`](DECISION_LOCK_D22_CONFIRMATORY_V2_TAXONOMY.md)  
4. [`docs/paper/dual_track/DUAL_TRACK_STATUS.md`](../paper/dual_track/DUAL_TRACK_STATUS.md)
