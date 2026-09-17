# Q1 Novelty / Contribution Audit

**Generated:** 2026-09-17 (from frozen evidence only)  
**External literature verification:** REQUIRED before submission — no citations invented here.  
**Machine-readable:** `/opt/cursor/artifacts/q1_novelty_audit.json`

## Method

Position ADAPTI-GUARD against nine research areas without fabricating citations. Items requiring library verification are marked `UNVERIFIED_EXTERNAL`.

## Novelty boundary by area

| Area | Status | Boundary |
| --- | --- | --- |
| Prompt-injection defenses | ESTABLISHED | Heuristics / filters / detectors are known; not the paper’s breakthrough |
| Runtime guardrails | ESTABLISHED | Runtime allow/deny/sanitize is known; integration into tool-loops is systems work |
| Adaptive defenses | PARTIAL | PHASE1-CORE risk→action adaptation exists; adaptive *attacker* closure (C4) is out of scope |
| Agent security | EVAL + SYSTEMS | Contribution is measurement/protocol + pipeline, not a new agent architecture |
| Tool-use security | PRIMARY MEASUREMENT | Tool-HASR grounds outcomes in harmful tool execution |
| Policy-based intervention | ESTABLISHED | Held fixed in P3 detector isolation |
| Cost-aware defense | SECONDARY / ASSUMPTION | Normalized A0–A3 weights; not validated monetary costs |
| Detector–policy separation | PRIMARY METHOD | Controlled isolation: only detector varies |
| Agentic security evaluation | PRIMARY PROTOCOL | P2 pack + Tool-HASR + M3/M4 + INVALID forensics |

## Established components (do not overclaim as novel)

- Prompt-injection / jailbreak pattern detection
- Runtime LLM guardrails and safety filters
- Policy actions (allow / sanitize / deny / block)
- Cost-sensitive decision framing (generic)
- Interpretable heuristic and provenance detectors (D2/D4 as instantiations)

## Novel integration / mechanism (defensible)

1. **Primary:** Controlled isolation of *detector-related* security effects from downstream intervention policy inside an agentic tool-execution loop (P3: same pack/policy/tools/thresholds; Δ vs D0).
2. **Secondary:** Tool-HASR as an execution-grounded primary endpoint, with Judge-ASR secondary and M3/M4 disagreement forensics.
3. **Secondary:** Explicit detector → risk → policy → tool-gate → execution contract with locked costs and execution states (incl. INVALID_TOOL_ARGS).
4. **Secondary (bounded):** Cross-target *directional consistency* of Δ(d,t) on T0–T3 under PHASE1-CORE (Q2: 9/9 sign agreements).

## Strongest defensible contribution (one sentence)

A controlled protocol that isolates detector-related effects on agentic tool-security outcomes (Tool-HASR) from downstream intervention policy, with execution-grounded metrics, forensic disagreement analysis, and bounded cross-target directional consistency.

## Claims that must be weakened

- “Breakthrough / SOTA defense”
- “Universally robust / model-independent”
- “Best detector” or any ranking among D1/D2/D4
- “Solves prompt injection”
- “Production-ready agent security”
- “Statistically powered confirmatory efficacy”
- Generalization beyond frozen packs / evaluated models

## Claims that should NOT appear

- Winner / ranking language
- Outperforms all prior published defenses (without fair baselines)
- Closes adaptive attack threat (C4)
- Semantic detector superiority (D3 deferred)
- Monetary optimality of A0–A3
- Pooling Track-A smoke / L1 / P2 / P3 into one estimand

## External verification checklist (authors)

- [ ] Survey agent tool-security benchmarks and map Tool-HASR analogues
- [ ] Survey runtime guardrail / agent firewall systems for fair conceptual baselines
- [ ] Survey prompt-injection detectors used as agent middleware
- [ ] Cite only verified papers; remove any unverified comparative language
