# Phase-1 Scientific Report (Internal)

**Status:** Internal reference document. **Not for external submission** — no venue target, no author list, no citation formatting.  
**Purpose:** Give any team member a single, accurate, professionally written account of what Phase 1 claims, what it does not, and what is still open — without re-deriving it from a dozen scattered protocol files.  
**Binding data:** This report asserts nothing beyond what is already recorded in [`DUAL_TRACK_STATUS.md`](DUAL_TRACK_STATUS.md), [`CLAIMS_DUAL_TRACK.md`](CLAIMS_DUAL_TRACK.md), and the frozen AUDIT folders. Where this report and those files ever disagree, the **AUDIT folders win**.

---

## 1. Executive Summary

Phase 1 evaluated whether a label-blind, evidence→risk→policy runtime reduces harmful tool/action success by a language-model agent, compared to no defense (`B0`), on single-turn tool-use episodes.

Two independent confirmatory experiments exist, on two different frozen benchmarks, with two different outcomes:

| Track | Pack | Treatment | Outcome | Effect size (δ̂) | Statistically significant? | Utility ≥0.95? |
| --- | --- | --- | --- | --- | --- | --- |
| **A — VNEXT** | `vnext_confirm_v1.0` | `VNEXT-ADAPT` | **FAIL** | 0.082 (below MSID 0.20) | No (p=0.0625) | No (U≈0.934) |
| **B — Phase-1 confirm** | `phase1_confirm_v1` | `PHASE1-CORE` | **SUPPORTED_IMPROVEMENT** (scoped) | ≈0.443 (above MSID 0.20) | Yes (p≈1.49e-8) | Yes (U≈0.967) |

**These are not the same claim and do not cancel each other out.** Track A is an honest negative result for `VNEXT-ADAPT` on the VNEXT pack. Track B is a positive, statistically strong result for a different treatment (`PHASE1-CORE`) on a different pack. Track B does not reverse Track A’s FAIL verdict, and Track A does not invalidate Track B’s result — they are separate experiments and must be reported as such.

The single most important open item before Track B should be treated as fully closed (see §5) is that **Track B’s benchmark independence from the VNEXT pack has not yet been documented with episode-level provenance**. Until that is done, Track B should be read as “strong result, pending an independence audit” rather than “fully validated.”

---

## 2. Glossary (for readers not steeped in the protocol docs)

| Term | Meaning |
| --- | --- |
| **ASR / harmful-action success** | Fraction of attack episodes where the target performed the harmful action. Lower is better for a defense. |
| **B0** | Baseline condition: no defense applied. |
| **PHASE1-CORE / VNEXT-ADAPT** | The two different intervention treatments tested in Track B and Track A respectively. Not interchangeable. |
| **δ̂ (delta-hat)** | Estimated paired effect size: how much the treatment reduced harmful-action success vs B0 on the same episodes. |
| **MSID** | Minimum Scientifically Interesting Difference — the pre-registered threshold δ̂ must clear (locked at **0.20** for both tracks). |
| **McNemar / b10, b01** | Paired binary test. `b10` = B0 harmful success and treatment intervention win; `b01` = the reverse. Needs `b10 > b01` and significant p to count. |
| **U (utility)** | Fraction of benign episodes the treatment still lets complete normally. Below 0.95 means the defense blocks too much legitimate work. |
| **Qualified win** | Compound pass: MSID met, p<0.05, and utility eligible — all at once. |
| **`target_refusal`** | Model refuses on its own. Explicitly **not** a defense win. |
| **`correct_tool_deny` / `correct_block`** | Defense mechanism blocked the harmful tool/action. These count as genuine wins. |
| **Label-blind** | Core detection/policy path never sees gold attack/benign labels; labels are used only afterward for scoring. |

---

## 3. What Phase 1 Built (Engineering Contribution)

A causal, single-turn defense pipeline:

```
Context → Phase-1 evidence detector → RiskCore → CorePolicy → ActionLayer → ToolPermissionGate → Trace
```

- The Phase-1 detector (`evidence_phase1.0` on Track B; Track A’s `VNEXT-ADAPT` used frozen `evidence_v4.0`) scores observable text/behavior for injection evidence without gold labels.
- Risk bands and action sensitivity (tool call present vs text-only) jointly determine an action tier A0–A3.
- A0–A3 are graded interventions, not a binary allow/block — e.g., MEDIUM risk with a tool call can escalate to a hard deny (A2); MEDIUM risk with text only may get a lighter intervention (A1) that is not a tool deny.
- Decisions are traced; gold metadata is structurally excluded from the core decision path (covered by dedicated tests, not only code review).

This engineering stack either runs correctly (deterministic suite) or it does not; it is not itself the confirmatory statistical claim.

---

## 4. What Phase 1 Found (Scientific Contribution)

### 4.1 Track A — VNEXT confirmation (FAIL)

On frozen `vnext_confirm_v1.0` (SHA-256 `523c881820710783b5290c76ea5fe5fc01a6341fb427defcba1119fc3e721518`), `VNEXT-ADAPT` reduced ASR from **0.9508** to **0.8689** — a real but small effect (δ̂=**0.0820**) that did not clear MSID **0.20**, was not statistically significant (McNemar exact p=**0.0625**, b10=5 / b01=0), and dropped utility below the eligibility line (U=**0.9344** < 0.95).

**This is an honest negative result**, not a near-miss to be spun positively. All three gate conditions (MSID, significance, utility) needed to pass together, and none did.

Official record: `experiments/real_llm_eval/VNEXT_CONFIRM/20260914-133147/AUDIT.md`.

### 4.2 Track B — Phase-1 confirmatory live run (SUPPORTED_IMPROVEMENT)

On frozen `phase1_confirm_v1` (SHA-256 `c789811a07d3ed06e1c77d8a45eda6172f480226e006d84fa28386a982536d01`), `PHASE1-CORE` reduced harmful-action success from **1.000** (B0) to **0.557** — a large effect (δ̂≈**0.443**) that cleared MSID, was highly significant (McNemar p≈**1.49e-8**, b10=**27** / b01=**0**, all wins `correct_tool_deny`), and retained utility above threshold (U≈**0.967**).

**This is a strong result**, on its own terms, on its own benchmark, for its own treatment. It must not be described as “VNEXT now works” or as reversing Track A.

Official record: `experiments/real_llm_eval/PHASE1_CONFIRM/phase1_confirm_20260914T213022Z_a2681e92/AUDIT.md`.

### 4.3 Why these can both be true

Different pack, different treatment, same MSID/utility protocol family. A defense can perform differently across benchmarks that stress different attack surfaces or difficulty distributions. The interesting question — *why* `PHASE1-CORE` succeeded on its pack where `VNEXT-ADAPT` failed on the VNEXT pack — is not answered here and must not be answered by assumption. See §5.1.

---

## 5. Limitations and Open Risks

### 5.1 Benchmark independence for Track B is not yet documented (highest priority)

Track B’s confirmatory pack has a different hash from the VNEXT pack and is described as a separate benchmark. What is **not yet on record**:

- Episode-level provenance showing zero overlap (prompts, seeds, paraphrase families, scenario templates) with the VNEXT pack or with packs used to iterate the Phase-1 evidence detector.
- Confirmation that freeze order (holdout constructed → hashed → code frozen → single eval pass) was followed, rather than the benchmark being adjusted with knowledge of how `PHASE1-CORE` would perform.

Until documented, Track B is a strong, promising, but **not yet independently audited** confirmatory result. This is a process gap, not evidence the result is wrong — but it is the item most likely to matter if the work is escalated beyond internal use.

### 5.2 Same-model-family judge

Track B’s judge (`qwen/qwen-2.5-72b-instruct`) is a larger model in the same family as the target (`qwen/qwen-2.5-7b-instruct`). Same-family judging has known potential for correlated bias in some LLM-as-judge setups. Not ruled out here.

### 5.3 Sample size

N=61 attack + 61 benign per track. Adequate for McNemar when effects are large (Track B), but too small to support generalization claims beyond these packs.

### 5.4 Detector blind spots (known, not silently patched)

Documented residual blind spots include obfuscation styles (e.g., l33t, Morse-like, reversed text) and some social-engineering patterns. Frozen for current evaluation; any future fix must be validated on a benchmark it was not tuned against.

### 5.5 Scope

Single-turn, tool-using-agent episodes only. No multi-turn context, no adaptive attacker across turns, no evaluation against an attacker that knows the defense and adapts to it.

### 5.6 No external baseline comparison

Phase 1 compares its own treatments (`B0`, `VNEXT-ADAPT`, `PHASE1-CORE`, and static A1/A2/A3 ablations where run) against each other. It does not compare against externally published prompt-injection defenses. No SOTA claim is made or supported.

---

## 6. What This Report Does Not Claim

Consistent with [`CLAIMS_DUAL_TRACK.md`](CLAIMS_DUAL_TRACK.md), this report does not claim: SOTA status; production readiness; that prompt injection is “solved”; that Track B reverses Track A; that either track generalizes beyond its pack/target/judge; or that Phase-2 / multi-turn live results exist (Phase-2 planning docs may exist; live confirmatory evaluation does not).

---

## 7. Where to Look for More Detail

| Question | Document / artifact |
| --- | --- |
| Exact allowed/forbidden phrasing | [`CLAIMS_DUAL_TRACK.md`](CLAIMS_DUAL_TRACK.md) |
| Raw dual-track numbers + AUDIT pointers | [`DUAL_TRACK_STATUS.md`](DUAL_TRACK_STATUS.md) |
| Research question / hypotheses | [`docs/experiments/PHASE1_SCIENTIFIC_SPEC.md`](../../experiments/PHASE1_SCIENTIFIC_SPEC.md) |
| Threat model | [`docs/experiments/PHASE1_THREAT_MODEL.md`](../../experiments/PHASE1_THREAT_MODEL.md) |
| Statistical plan (endpoints, MSID) | [`docs/experiments/PHASE1_STATISTICAL_PLAN.md`](../../experiments/PHASE1_STATISTICAL_PLAN.md) |
| Detector study | [`docs/experiments/PHASE1_DETECTOR_STUDY.md`](../../experiments/PHASE1_DETECTOR_STUDY.md) |
| Ablation design | [`docs/experiments/PHASE1_ABLATION_PROTOCOL.md`](../../experiments/PHASE1_ABLATION_PROTOCOL.md) |
| Scientific gate (SH1–SH8) | [`docs/experiments/PHASE1_SCIENTIFIC_GATE.md`](../../experiments/PHASE1_SCIENTIFIC_GATE.md) |
| Track A official FAIL AUDIT | `experiments/real_llm_eval/VNEXT_CONFIRM/20260914-133147/AUDIT.md` |
| Track B official confirm AUDIT | `experiments/real_llm_eval/PHASE1_CONFIRM/phase1_confirm_20260914T213022Z_a2681e92/AUDIT.md` |
| VNEXT workshop claims map (FAIL-only) | [`docs/paper/workshop_vnext_fail/CLAIMS_MAP.md`](../workshop_vnext_fail/CLAIMS_MAP.md) |

---

## 8. Suggested Next Actions (discussion only — not authorized by this report)

1. **Close §5.1:** document episode-level provenance for `phase1_confirm_v1` against the VNEXT pack (and detector-fit sources). Highest-value next step for Phase 1 credibility.
2. Consider a short ablation / pack-difficulty note explaining why `PHASE1-CORE` and `VNEXT-ADAPT` diverge on their respective packs — even a qualitative attack-type comparison would strengthen §4.3.
3. No live LLM calls, no retuning, and no new pack construction should happen as a side effect of writing this report — it is documentation only.
