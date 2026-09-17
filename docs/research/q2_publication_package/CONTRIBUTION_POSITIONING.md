# Contribution positioning

**API calls:** 0. One central contribution. Not five unrelated algorithms.  
**Literature basis:** `RELATED_WORK_MATRIX.md`. Paper identities VERIFIED; venues mostly UNVERIFIED.  
**NOVELTY_CLASS = PARTIAL_GAP.**

## Candidate wording (evaluated)

> A controlled evaluation protocol that holds the downstream intervention policy fixed, varies detector identity including D0, measures Tool-HASR, and tests whether detector-related Δ relative to D0 preserves sign across independently selected target models.

**Verdict:** supported as a **methodological / attribution** claim, with scope limits.  
Not supported as a **new defense** claim.

## Central problem

Tool-using agents can cause harm by **executing** a tool, not only by emitting a successful-looking string. Observed security numbers mix (i) detector behavior and (ii) the intervention policy that grants or denies tools. When those pieces move together, a lower attack-success number cannot be attributed to “the detector.”

## Literature (established vs residual)

**Existing literature already provides:** prompt-injection attacks; agent security benchmarks; dynamic evaluation; defense architectures; architectural isolation; adaptive attacks/evaluation; memory/tool security; runtime security mechanisms.

The paper does **not** claim invention of those components.

**Residual gap (narrow):**

> The verified literature establishes extensive work on attacks, benchmarks, defenses, and adaptive evaluation, but does not establish the exact locked-policy detector-attribution factorial used here as the central measurement protocol.

AgentDojo and ASB are verified papers, not uncertain citations. CaMeL is a published architectural design, not an unverified idea. None of those facts licenses a “first” / “unique” / “no prior work” sentence.

## Methodological contribution (central)

Hold policy, thresholds, action costs, frozen pack, and judge **fixed**. Vary detector identity {D0, D1, D2, D4}. Define

Δ(d,t) = Tool-HASR(d,t) − Tool-HASR(D0,t)

and test directional consistency of sign(Δ) on independently selected secondary targets.

Language: **detector-related effect** under the controlled protocol. Not “detector causality,” unless explicitly qualified as attribution under that protocol.

## Empirical contribution (supporting, not a second paper)

Under locked PHASE1-CORE on frozen `p2_agentic_v0.1.0`, n=16 attack arms/cell, `scientific_evidence=false`:

- Protocol-complete **pilot-scale directional consistency** (not confirmation).
- T0 (Stage-B reuse, PHASE1-CORE): Δ(D1/D2/D4) = −0.6875 / −0.25 / −0.5625 (all NEG). Packaged T0 Tool-HASR 28/64; Judge-ASR 55/64; M3=33; M4=6. Raw Stage-B traces MISSING_LOCALLY (`STAGE_B_EVIDENCE_STATUS.md`).
- T1–T3 (Q2 live, 432/432 arms, historical $0.152885): all nine Δ signs NEG; sign agreement 9/9.
- Q2 live T1–T3: Tool-HASR 81/192; Judge-ASR 186/192; M3=108; M4=3.
- INVALID 192 events / 136 arms on T1–T3; S2 signs remain 9/9; S0 stays official.

## Diagnostic contribution (supporting)

1. Tool-HASR as operational harmful-tool endpoint (primary).
2. Judge-ASR as secondary diagnostic (not “invalid”).
3. M3/M4 disagreement accounting: Judge-ASR and Tool-HASR capture related but non-identical operational outcomes.
4. INVALID_TOOL_ARGS S0/S1/S2 (S0 official; S2 sensitivity). Frequent; not silently discarded; not treated as harmless.

## Scope

- Pack: `p2_agentic_v0.1.0` (SHA `32b40e3b…8d64dd`).
- Policy: PHASE1-CORE only in Q2 live.
- Targets: four OpenRouter IDs (T0–T3), Qwen-heavy; locked judge.
- Detectors: D0/D1/D2/D4; D3 deferred.
- Mock tools; short multi-turn trajectories.
- Attribution study, **not** a head-to-head defense benchmark.

## Non-claims

- New defense algorithm; SOTA / best / superior detector or defense.
- Production-ready or universally effective protection.
- Confirmation for all LLMs.
- Causal identification in deployment (“detector causality” as an unqualified claim).
- Monetary cost-optimality.
- That Judge-ASR is invalid.
- That Track B reverses Track A, or that Q2 reverses VNEXT FAIL.
- Adaptive-attacker robustness.
- CLEAR GAP / “first” / “no prior work.”
- Numerical comparison to CaMeL, AgentDojo defenses, ASB defenses, Llama Guard, or PromptShield.
