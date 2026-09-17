# Publication preparation — hardening report

**LIVE_EVAL=false. API_CALLS=0. LLM_CALLS=0. NETWORK_CALLS=0.** Frozen evidence not modified. Q2 not re-run.

Final status: **READY_WITH_MAJOR_REVISIONS**

## 1. Actual scientific contribution

A **controlled attribution protocol**: hold downstream intervention policy fixed, vary detector identity including D0, measure Tool-HASR, and test whether detector-related Δ vs D0 preserves sign across independently selected target models.

Not a new defense algorithm.

## 2. Novelty

**PARTIAL_GAP.** Existing literature already provides attacks, benchmarks, dynamic evaluation, defense architectures, architectural isolation, adaptive evaluation, memory/tool security, and runtime mechanisms. Residual: the verified literature does not establish the exact locked-policy detector-attribution factorial used here as the central measurement protocol.

## 3. What Q2 establishes under its protocol

Protocol-complete **pilot-scale directional consistency** (`scientific_evidence=false`, n=16/cell): 432/432; $0.152885; 9/9; all D1/D2/D4 Δ NEG on T0–T3; T1–T3 Tool-HASR 81/192; Judge-ASR 186/192; M3=108; M4=3; INVALID 192/136; S2 9/9.

## 4. What Q2 does not establish

Universal defense; SOTA/best; production robustness; confirmatory multi-model study; unqualified detector causality; fair numerical comparison to external defenses; D3; open adaptive attacker; Track A reversal; Judge-ASR invalidity; INVALID negligibility; global uniqueness of the factorial.

## 5. Biggest remaining weaknesses (genuine)

1. Stage-B raw traces MISSING_LOCALLY.
2. Bibliography PARTIAL (most venue/DOI UNVERIFIED; operator-supplied AgentDojo/BIPIA not re-fetched).
3. Pilot n=16 / four Qwen-heavy targets / no matched external baseline (documented scope, not closable without new science).

## 6. Missing evidence

- Stage-B `predictions.jsonl`
- Camera-ready venue/DOI for 19/21 records
- Matched external baselines (only if a comparative claim is desired later)
- D3; open C4
- Δ CIs / Q2 p-values (not pre-registered; not manufactured)

## 7. Hardening completed this pass

- Stage-B official vs local distinction
- Related-work identity classification; AgentDojo/ASB not UNCERTAIN; CaMeL not an unverified idea
- Novelty rewritten as controlled attribution
- Manuscript 10-section structure + hardened abstract
- INVALID compact S0/S1/S2 table
- Tool-HASR vs Judge-ASR as a finding
- Venue decision matrix without invented deadlines
- Peer-review response matrix
- `FINAL_WEAKNESS_CLOSURE.md`

## 8. Before submission

Human: package Stage-B traces read-only; verify remaining venues from official pages; pick a venue after `VENUE_DECISION_MATRIX.md`; keep claims frozen. No agent merge or venue submit.

## 9. New live experiments required?

**No** for this methods+pilot package. **Yes** only for comparative-defense, D3, larger n, more families, or open adaptive attackers.

## 10. Next

Keep status **READY_WITH_MAJOR_REVISIONS**. Do not mark PUBLICATION_READY.
