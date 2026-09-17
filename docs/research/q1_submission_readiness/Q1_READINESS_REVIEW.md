# Q1 Readiness Review (Hostile but Fair)

**JSON:** `/opt/cursor/artifacts/Q1_READINESS_REVIEW.json`  
**Persona:** Senior journal reviewer, AI security / trustworthy ML.

## Scores (1–5)

| Criterion | Score | Note |
| --- | ---: | --- |
| Novelty | 3 | Integration/protocol novelty plausible; not a breakthrough defense without lit verify |
| Significance | 3 | Important problem; pilot n limits impact claim |
| Methodological rigor | 4 | Strong locks, isolation design, forensic discipline |
| Reproducibility | 4 | SHAs, run IDs, harness versions present |
| Statistical validity | 3 | Honest CIs; underpowered; no fishing — good — but precision limited |
| Benchmark quality | 3 | Thoughtful twins/HN; small; C4 gap |
| Baseline quality | 2 | Critical gap: no external published baselines on same pack |
| Generalization | 2 | Q2 helps directionally; still 4 models / 2 packs |
| Clarity | 3 | Achievable if contribution hierarchy enforced |
| Limitations honesty | 4 | Materials now support honest limits |
| Threat validity | 3 | Clear scoped TM; adaptive attacker out of scope |
| Claim/evidence alignment | 3 | Ledger ready; manuscript must comply |

**Overall:** CONDITIONAL — publishable as a **rigorous pilot / protocol & attribution** paper if claims stay bounded; **not** ready as confirmatory SOTA defense paper.

## Weaknesses

| ID | Area | Sev | Fix w/o new exp? | Exact fix | Impact |
| --- | --- | --- | --- | --- | --- |
| W1 | Benchmark size | HIGH | Yes | Quantify n; weaken generalization | Avoid overclaim reject |
| W2 | scientific_evidence=false | HIGH | Yes | Frame as protocol/pilot; don’t silently upgrade | Alignment |
| W3 | External baselines | HIGH | **No** | Document unavailable fair reconstructions | Expect reviewer pushback |
| W4 | Novelty positioning | MED | Yes | Verified related work rewrite | Acceptance |
| W5 | INVALID_TOOL_ARGS | MED | Yes | Include S0/S1/S2 (done analytically) | Credibility |
| W6 | P1 vs Tool-HASR metrics | MED | Yes | Dual-metric narrative | Clarity |
| W7 | Cost model | MED | Yes | Label normalized weights + sensitivity | Avoid econ overclaim |
| W8 | D3 deferred | LOW | Yes | State deferred | Completeness |
| W9 | Doc lag (“P3-C not started”) | LOW | Yes | Docs-only update | Reproducibility |
| W10 | Utility tradeoff | MED | Yes | Report twin/HN FPR/utility prominently | Balance |
| W11 | Adaptive attacks C4 | HIGH | **No** | Bound threat model explicitly | Threat validity |
| W12 | Model diversity | MED | Yes | “Directional consistency on evaluated targets” | Honesty |

## FIX BEFORE SUBMISSION

1. Rewrite abstract/intro around **primary** contribution; demote secondaries.
2. Complete related work with **verified** citations only.
3. Add full Limitations (n, C4, baselines, costs, INVALID, evidence flags).
4. Include INVALID S0/S1/S2 + M3/M4 endpoint justification.
5. Include Q2 directional-consistency table with safe wording.
6. Label ACTION_COSTS as normalized weights; add offline cost sensitivity.
7. State baseline gap: unavailable fair external reconstructions.
8. Enforce claims ledger; purge ranking/universal language.
9. Documentation-only: update P3 design docs that still say P3-C not started.
10. **Do not** run new live experiments solely to inflate claims before claim alignment is fixed.

## Q1_READINESS_STATUS

| Dimension | Status |
| --- | --- |
| Evidence integrity | PASS (frozen SHAs; Q2 forensic PASS; this task did not mutate evidence) |
| Scientific analysis | COMPLETE_FOR_EXISTING_EVIDENCE |
| Novelty positioning | DRAFTED_PENDING_EXTERNAL_LIT_VERIFY |
| Generalization | BOUNDED_PILOT |
| Baseline coverage | GAP_DOCUMENTED |
| Statistical package | COMPLETE_FROM_EXISTING |
| Claim alignment | LEDGER_READY |
| Paper readiness | CONDITIONAL_NOT_YET_SUBMISSION_READY |
| Remaining HIGH risks | benchmark_size; scientific_evidence_flags; external_baselines; adaptive_attacks_C4 |
| Remaining MEDIUM risks | novelty_positioning; INVALID; P1/Tool-HASR continuity; cost_model; utility_tradeoff; model_diversity |
| Remaining LOW risks | D3_deferred; doc_lag_P3C |
