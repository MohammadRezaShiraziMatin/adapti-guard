# Simulated peer review (Q2 manuscript V1)

**Not an official review. No numeric scores.**  
Evidence vs writing is labeled. Reviewers did not receive fabricated extra results.

## Reviewer A — research methodology

**Strongest point.** The factorial is explicit: policy, pack, judge, thresholds, and costs locked; detector identity varied, including a no-detection arm; primary estimand Δ vs D0; Q2 asks for sign consistency rather than a new defense.

**Major concern.** n=16/cell and `scientific_evidence=false` make magnitude language unsafe. T2’s exact Δ match to T0 is under-powered coincidence unless labeled as such. T0 reuse plus missing Stage-B traces on the checkout is a reproducibility hole for the reference arm. **Evidence-related.**

**Minor concern.** Dual-track honesty is necessary but can confuse readers who did not ask for VNEXT. **Writing-related.**

**Required revision.** Keep abstract/conclusion on signs + isolation; move magnitudes to tables with CIs; package Stage-B traces or label T0 INVALID as unrecomputed; do not add post-hoc p-values.

## Reviewer B — LLM / agent security

**Strongest point.** Tool-HASR as operational execution, with Judge-ASR retained as diagnostic, matches how agent harm actually happens. Related work covers injection, IPI, AgentDojo/InjecAgent/ASB, rails, and architectural isolation without copying other papers’ ASRs.

**Major concern.** No matched baseline against Llama Guard, PromptShield, CaMeL, IsolateGPT, or AgentDojo defenses. Isolation vs D0 is not a substitute for “does this beat known defenses?” Novelty is only a partial gap. **Evidence-related** (baseline) and **writing-related** (do not oversell gap).

**Minor concern.** D1/D2/D4 hit rates on benign/hard-negative rows will be read as a ranking unless captions repeat `no_ranking`. **Writing-related.**

**Required revision.** Keep `BASELINE_GAP.md` in the paper body in compressed form. State PARTIAL GAP. Never rank detectors.

## Reviewer C — trustworthy AI / empirical evaluation

**Strongest point.** Label-blind path stated; gold labels forbidden in detector→policy; INVALID not silently dropped; M3/M4 reported; limitations are specific rather than boilerplate.

**Major concern.** Qwen-heavy OpenRouter set plus mock tools plus one judge (also Qwen) is a narrow trustworthiness claim. INVALID frequency (136/432 arms) can make Tool-HASR look like a parser artifact rather than a security effect, even though S2 signs hold. **Evidence-related.**

**Minor concern.** Related-work venues UNVERIFIED will fail camera-ready checks. **Writing-related.**

**Required revision.** Title/abstract must say pilot / four models / mock tools. Verify venues before submission. Do not imply judge independence from the Qwen family.

## Reviewer D — reproducibility / statistics

**Strongest point.** SHAs, run ID, spend, 432/432, Wilson CIs on rates, no manufactured Δ CIs or p-values, S0 vs S2 documented, generation script is deterministic.

**Major concern.** Stage-B `predictions.jsonl` **MISSING**; matplotlib figures **MISSING**; seed 42 does not imply provider determinism; Q2 “supported” verdict is easy to misread as Track B SUPPORTED_IMPROVEMENT. **Evidence-related** (traces/figures) and **writing-related** (verdict vocabulary).

**Minor concern.** Paired discordant counts are present in JSON but under-explained in the manuscript. **Writing-related.**

**Required revision.** Checklist already labels MISSING — do not fill. Add one sentence that Q2 “supported” ≠ Track B. Render figures offline when the dependency exists.

## Cross-review synthesis

| Theme | Evidence or writing? | Blocks PUBLICATION_READY? |
| --- | --- | --- |
| n=16 / scientific_evidence=false | Evidence (immutable) | Yes, unless framed as a methods+pilot paper and accepted as such |
| No external baseline | Evidence (documented gap) | Yes for a comparative-defense paper; not fatal for an isolation-protocol paper if honest |
| Stage-B traces missing | Evidence packaging | Yes for full reproducibility of T0 |
| Venues UNVERIFIED | Writing/bibliography | Yes for camera-ready |
| Figures not rendered | Packaging | Yes for most venues |
| Claims language | Writing | Currently scoped; must not regress |

No reviewer assigned a score. Consensus recommendation: **major revisions** before any venue submit. No new live Q2 rerun is required to answer these reviews, except a future baseline study if the authors later want a comparative claim.
