# Publication preparation — final report to operator

**LIVE_EVAL=false. API_CALLS=0. Frozen evidence not modified. Q2 not re-run.**

Final status: **READY_WITH_MAJOR_REVISIONS**

## 1. What is the actual scientific contribution?

A **controlled attribution protocol** for LLM-agent security: hold downstream intervention policy (PHASE1-CORE), thresholds, action costs, frozen pack, and judge fixed; vary detector identity including a no-detection arm; take **Tool-HASR** as the primary operational endpoint; and test whether detector-related Δ vs D0 keeps **sign** on independently selected secondary targets.

Supporting layers (not separate inventions): Judge-ASR as secondary diagnostic; M3/M4; INVALID_TOOL_ARGS S0/S1/S2.

## 2. What is genuinely novel versus prior work?

**PARTIAL GAP.** Detection, rails, architectural isolation (CaMeL, IsolateGPT), and agent benchmarks (AgentDojo, InjecAgent, ASB, AgentHarm) already exist. What is not verified in the surveyed Hub-metadata set is this **factorial**: locked intervention policy × detector identity × Tool-HASR Δ sign across independently selected targets.

Not novel: D1/D2/D4 as detector families; runtime guardrails; cost weights; trajectory eval as an idea.

Uncertain remainder: AgentDojo/ASB full texts were not audited; they may contain a close cousin. Do not claim “first” or CLEAR GAP.

## 3. What does Q2 prove/establish under its protocol?

It does not “prove” a general law. Under locked PHASE1-CORE on frozen `p2_agentic_v0.1.0`:

- 432/432 Q2 live arms; historical spend $0.152885
- D1/D2/D4 Tool-HASR Δ vs D0 is NEG on T0, T1, T2, T3
- Sign agreement **9/9**
- Dual endpoints: T1–T3 Tool-HASR 81/192 vs Judge-ASR 186/192; M3=108; M4=3
- INVALID 192/136 on Q2 live; S2 signs still 9/9; S0 remains official
- `scientific_evidence=false`: protocol-complete **pilot-scale directional consistency**

## 4. What does Q2 NOT establish?

Universal defense; SOTA/best detector; production robustness; confirmatory multi-model study; that detectors are the sole cause of outcomes; causal ID in deployment; fair comparison to CaMeL/IsolateGPT/Llama Guard/PromptShield/AgentDojo defenses; D3 performance; open adaptive-attacker robustness; Track A reversal; Judge-ASR invalidity; INVALID negligibility.

## 5. What are the three biggest publication weaknesses?

1. **Pilot evidence vs paper ambition:** n=16, four Qwen-heavy models, `scientific_evidence=false`.
2. **Reproducibility hole + bibliography:** Stage-B traces missing here; venues/DOIs UNVERIFIED; figures not rasterized.
3. **Baseline gap:** isolation vs D0 is not a comparative defense result; reviewers will ask anyway.

## 6. What evidence is still missing?

- Stage-B `predictions.jsonl` on this checkout
- Venue/DOI for 21 related-work records
- Raster figures
- Matched external baselines (only if a comparative claim is desired later)
- D3 implementation; open C4 eval
- Δ CIs / Q2 p-values (not pre-registered; must not be manufactured)
- Human red-team log
- Exhaustive full-text novelty proof

## 7. What manuscript work is complete?

- `MANUSCRIPT_V1.md` with the required sections, bounded abstract, limitations, dual endpoints, tables sourced from locked JSON
- Related-work matrix (21 Hub-verified arXiv records) + novelty audit (PARTIAL GAP)
- Claim–evidence matrix; claims language audit
- Reproducibility checklist with MISSING labels
- Simulated four-reviewer audit
- Venue *categories* without selection
- Table/figure specifications and mermaid architecture diagrams

## 8. What remains before submission?

Human: verify venues/DOIs; attach Stage-B traces read-only; pick a venue category and apply its template; render figures; decide whether to stay methods+pilot or commission a **new** baseline study; keep claims frozen. No agent merge or venue submit.

## 9. Are new live experiments actually required?

**No** for completing this methods+pilot package and for Q2 as locked.  
**Yes** only if authors later claim superiority to external defenses, add D3, enlarge n, add model families, or evaluate open adaptive attackers. Those are new studies (rule 6), not Q2 reruns.

## 10. What should be done next?

1. Do not re-run Q2.
2. Package Stage-B traces without modification.
3. Verify bibliography venues from official pages.
4. Render Figure 3–5 offline.
5. Keep status **READY_WITH_MAJOR_REVISIONS** until those packaging items land.
6. Do not mark PUBLICATION_READY while Stage-B traces, venues, and figures remain open.

Hashes checked this packaging (file SHA on checkout): P1 `1a0b0053…dd235`; P2 `32b40e3b…8d64dd`; Q2 predictions `2a2c2f31…886cc6`. Evidence commit `b075df0f5ec5ad11ede76ac4e4079cade15208f1`. API this task: **0**.
