# Q1 Baseline Gap Analysis

**Constraint:** No new live baselines. No fabricated reconstructions.

## What current detectors provide

| ID | Role | Provides | Does not provide |
| --- | --- | --- | --- |
| D0 | No-detection anchor | Counterfactual: policy+tools without detector hits | Not a published external defense |
| D1 | PHASE1 evidence detector (frozen) | Current production-path detector as-is | Not retuned; not an external SOTA detector |
| D2 | Heuristic taxonomy regex OR-rules | Interpretable pattern baseline | Not equivalent to published learned detectors |
| D4 | Structured/context provenance cues | Channel/tool/memory provenance signals | Not a full information-flow monitor from literature |
| D3 | Semantic/embedding | — | **Deferred** — unavailable |

Policies B0 / STATIC-A1 / PHASE1-CORE are **intervention baselines**, not detector baselines.

## Conceptual comparators (literature class — UNVERIFIED_EXTERNAL until cited)

| Class | Why relevant | Fair reconstruction from *existing* ADAPTI-GUARD evidence? |
| --- | --- | --- |
| Prompt-injection classifiers / scanners | Closest to D1/D2 | **No** — different I/O contracts; not run on P2 pack |
| LLM self-reminder / system-prompt hardening | Common simple baseline | **No** — not executed in P3 matrix |
| Output filters / regex deny lists | Partial overlap with heuristics | **Partial conceptual only** — not matched configs |
| Agent firewall / tool permission systems | Overlap with tool gate | **Partial** — our tool permissions are pack-fixed, not a published firewall product |
| Learned embedding detectors | D3 class | **Unavailable** (D3 deferred) |
| Human-oracle / perfect detector | Upper bound | **Not run** |

## Gap priority

| Missing comparison | Priority | Reason |
| --- | --- | --- |
| At least one external published detector or agent-guardrail on same P2 pack | **A. Critical** for systems/defense papers | Reviewers will ask; currently only internal D0–D4 |
| Prompt-only hardening baseline (fixed system prompt) | **B. Useful** | Cheap conceptually; still needs a run — **not available now** |
| Embedding/semantic detector (D3) | **B. Useful** | Taxonomy incomplete |
| Commercial API moderators | **C. Unnecessary** for RQ (detector vs policy isolation) if RQ stays methodological | Different threat/API assumptions |
| Full SOTA bake-off / ranking | **C. Unnecessary / forbidden** | Protocol forbids ranking |

## Honest statement for the paper

> Fair reconstructions of external published defenses on the frozen P2 pack are **unavailable** in the current evidence set. D0 provides an internal no-detection anchor; D1/D2/D4 are internal interpretable alternatives under a shared contract. Claims are limited to **within-protocol detector contrasts vs D0**, not superiority over the external literature.

## If a future experiment is ever approved (out of scope now)

Match pack SHA, Tool-HASR definition, policy lock, and report as a new study — do not rewrite Q2/Stage-B.
