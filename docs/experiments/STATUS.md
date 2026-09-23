# Experiments — tip status (docs)

**Updated:** 2026-09-23 (process unlock on tip `main`, SHA `30ddc75`)  
**Mode:** Documentation and decision locks only. **API=0.** Agents do not merge.

---

## Tip intent

Raise **publisher readiness** and remove **process/admin bottlenecks** via honest docs — not by changing frozen science or rerunning live eval.

Active quality work follows [`QUALITY_ROADMAP_5PHASE.md`](QUALITY_ROADMAP_5PHASE.md). **This PR completes P1 + P2 (docs).**

---

## Science locks (unchanged)

| Track | Outcome | Pack / pointer |
| --- | --- | --- |
| **A — VNEXT** | **FAIL** (immutable) | `vnext_confirm_v1.0`, SHA `523c881820710783b5290c76ea5fe5fc01a6341fb427defcba1119fc3e721518`; AUDIT `experiments/real_llm_eval/VNEXT_CONFIRM/20260914-133147/` |
| **B — Phase-1 LIVE** | **SUPPORTED_IMPROVEMENT** (scoped) | `phase1_confirm_v1`, SHA `c789811a07d3ed06e1c77d8a45eda6172f480226e006d84fa28386a982536d01`; AUDIT `experiments/real_llm_eval/PHASE1_CONFIRM/phase1_confirm_20260914T213022Z_a2681e92/` |

Track B **does not** reverse Track A. Wording: [`docs/paper/dual_track/CLAIMS_DUAL_TRACK.md`](../paper/dual_track/CLAIMS_DUAL_TRACK.md).

Do not edit `datasets/frozen/**` or `experiments/real_llm_eval/**` AUDIT/verdict/numbers.

---

## D-22 — Confirmatory V2 taxonomy (names locked)

**Decision:** Option A — six `family_id` strings from frozen `datasets/frozen/vnext_confirm_v1` (`manifest.json` → `family_counts`).

**Record:** [`DECISION_LOCK_D22_CONFIRMATORY_V2_TAXONOMY.md`](DECISION_LOCK_D22_CONFIRMATORY_V2_TAXONOMY.md)

**Not decided here:** 151-episode allocation, episode bodies, SAP, new pack bytes. Remainder `151 mod 6 = 1` → separate Researcher rule later.

No prior `DECISION_REQUEST` file was found under `docs/` at lock time; any informal request is **closed** by the D-22 lock doc above.

---

## Open PRs and merge

Official index: [`docs/paper/workshop_vnext_fail/PR_STACK.md`](../paper/workshop_vnext_fail/PR_STACK.md) (PRs #23–#44 stack). **Human merge only.** Agents never merge and never close PRs via API.

This quality PR is a **single docs-only branch off tip `main`**, separate from the historical stack unless Matin chooses to integrate it.

---

## Next after this PR

**Phase 3** (roadmap): manuscript claims polish under `docs/paper/` — still no live eval, no frozen edits, no FAIL reversal.

Human-only gates unchanged: venue submit, live LLM budget, merge to `main`.
