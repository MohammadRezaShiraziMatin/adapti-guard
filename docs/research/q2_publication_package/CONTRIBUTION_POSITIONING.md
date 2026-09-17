# Contribution positioning

**API calls:** 0. One central contribution. Not five unrelated algorithms.  
**Literature basis:** `RELATED_WORK_MATRIX.md` (Hub-verified arXiv records). Venues UNVERIFIED.

## Candidate wording (evaluated)

> A controlled framework for isolating detector-related effects from downstream intervention policy in LLM-agent security.

**Verdict:** **supported as a methodological claim**, with scope limits.  
The literature audit finds detectors, rails, architectural isolation (CaMeL, IsolateGPT), and agent benchmarks (AgentDojo, InjecAgent, ASB, AgentHarm). It does **not** verify a matching factorial that holds agent intervention policy fixed, varies detector identity including a no-detection arm, and reports Tool-HASR Δ sign across independently selected targets. Novelty class: **PARTIAL GAP** (`NOVELTY_AUDIT.md`). Do not say “first.”

## Central problem

Tool-using agents can cause harm by **executing** a tool, not only by emitting a successful-looking string. Observed security numbers mix (i) detector behavior and (ii) the intervention policy that grants or denies tools. When those pieces move together, a lower attack-success number cannot be attributed to “the detector.”

## Literature gap (qualified)

- **Established:** prompt injection and IPI; guardrail detectors; programmable rails; model-level instruction hierarchy; execution/control-data isolation; agent attack/defense benchmarks.
- **Under-specified in surveyed work:** attribution of operational tool-harm change to detector identity **conditional on a locked intervention policy**.
- **Uncertain:** whether AgentDojo/ASB defense tables already approximate that factorial (full texts not audited here).

## Methodological contribution (central)

Hold policy, thresholds, action costs, frozen pack, and judge **fixed**. Vary detector identity {D0, D1, D2, D4}. Define

Δ(d,t) = Tool-HASR(d,t) − Tool-HASR(D0,t)

and test directional consistency of sign(Δ) on independently selected secondary targets.

## Empirical contribution (supporting, not a second paper)

Under locked PHASE1-CORE on frozen `p2_agentic_v0.1.0`, n=16 attack arms/cell:

- T0 (Stage-B reuse): Δ(D1/D2/D4) = −0.6875 / −0.25 / −0.5625 (all NEG).
- T1–T3 (Q2 live, 432/432 arms, historical $0.152885): all nine Δ signs NEG; sign agreement 9/9.
- Q2 live T1–T3: Tool-HASR 81/192; Judge-ASR 186/192; M3=108; M4=3.
- INVALID 192 events / 136 arms on T1–T3; S2 signs remain 9/9; S0 stays official.
- `scientific_evidence=false`. Protocol-complete **pilot-scale directional consistency**, not confirmation for all LLMs.

## Diagnostic contribution (supporting)

1. Tool-HASR as operational harmful-tool endpoint (primary).
2. Judge-ASR as secondary diagnostic (not “invalid”).
3. M3/M4 disagreement accounting.
4. INVALID_TOOL_ARGS S0/S1/S2 (S0 official; S2 sensitivity).

These are forensic layers of the same study.

## Scope

- Pack: `p2_agentic_v0.1.0` (SHA `32b40e3b…8d64dd`).
- Policy: PHASE1-CORE only in Q2 live.
- Targets: four OpenRouter IDs (T0–T3) + locked judge.
- Detectors: D0/D1/D2/D4; D3 deferred.
- Mock tools; short multi-turn trajectories.

## Limitations

See `LIMITATIONS.md`. Headline: n=16; four Qwen-heavy targets; INVALID frequency; M3 mass; no fair external baseline; D3 deferred; C4 open attacker out of scope; Stage-B traces missing on this checkout; venues UNVERIFIED.

## Non-claims

- SOTA / best / superior detector or defense.
- Production-ready or universally effective protection.
- Confirmation for all LLMs; Q2 is not a confirmatory multi-model study.
- Causal identification in deployment.
- Monetary cost-optimality (A0–A3 are normalized weights).
- That Judge-ASR is invalid.
- That Track B reverses Track A, or that Q2 reverses VNEXT FAIL.
- Adaptive-attacker robustness.
- That this wording is a “CLEAR GAP” vs all prior work.
