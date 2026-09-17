# Q2 Novelty / Related Work Audit

**Method:** Repository related-work / research docs only (no web search). External citation verification still required before submission.  
**API calls:** 0

## Defensible central novelty
Experimental **isolation of detector-related effects** from downstream intervention policy in an agentic tool-execution loop, measured by **Tool-HASR**, with **bounded cross-target directional consistency** (Q2).

## Claim table

| Claim | Existing evidence | Potential prior-art overlap | Safe wording | Risk |
| --- | --- | --- | --- | --- |
| Detector–policy isolation protocol | P3 design + Stage-B/Q2 | Agent firewalls / guardrail stacks often entangle both | Controlled isolation of detector contrasts under fixed policy | MEDIUM — need verified cites |
| Tool-HASR execution-grounded endpoint | P2/P3 metrics + M3/M4 | Agent benchmarks may use different success defs | Execution-grounded harmful-tool rate as primary endpoint | MEDIUM |
| Cross-target Δ sign consistency | Q2 9/9 | Multi-model safety evals exist | Directional consistency across evaluated targets | LOW if wording bounded |
| Runtime guardrails / policy actions | Architecture | ESTABLISHED field | Systems integration, not field invention | HIGH if overclaimed as novel |
| Prompt-injection detectors | D1/D2 | ESTABLISHED | Interpretable instantiations under shared contract | HIGH if claimed as novel detectors |
| Cost-aware defense | A0–A3 weights | Cost-sensitive ML established | Normalized experimental weights | HIGH if claimed monetary novelty |
| Adaptive defense vs adaptive attacker | PHASE1-CORE adapts actions | Adaptive attacks largely out of scope (C4) | Action adaptation ≠ attacker-closed | HIGH |
| Best/SOTA detector | Forbidden by protocol | Bake-offs common | Do not claim | CRITICAL if present |

## Do not claim novelty merely from absence in this repo
Missing implementation ≠ new science. Position as **protocol + attribution + measurement** contribution.
