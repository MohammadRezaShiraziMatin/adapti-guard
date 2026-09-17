# External baseline gap (Q2)

**API calls this task:** 0  
**Frozen evidence modified:** No  
**Q2 raw traces modified:** No  
**Invented baseline numbers:** None

This note records what is **missing**. It is not an experimental result.

## What was compared (internal only)

Q2 / Stage-B contrasts are **within-protocol**:

| Contrast | Status |
| --- | --- |
| D0 (no detection) vs D1 / D2 / D4 under locked PHASE1-CORE | Observed on P2 pack |
| T0 (Stage-B reuse) vs T1–T3 (Q2 live) for Δ sign | Observed |
| Tool-HASR vs Judge-ASR (M3/M4) | Observed |
| B0 / STATIC-A1 policy arms | Stage-B design includes them; **Q2 live is PHASE1-CORE only** (`B_REDUCED_Q2`) |

These are detector-isolation contrasts, not bake-offs against published external systems.

## Relevant baseline categories (not experimentally compared here)

| Category | Why relevant | Why it cannot currently be claimed as compared |
| --- | --- | --- |
| Commercial / published input filters (e.g. prompt-injection classifiers, Llama-Guard-class, PromptGuard-class, vendor firewalls) | Reviewers will ask “vs standard guards” | No locked reconstruction on frozen `p2_agentic_v0.1.0` under this harness, judge, Tool-HASR definition, or budget |
| Agent-tool permission / firewall stacks that entangle detection and policy | Closest product category | Q2 holds policy fixed (PHASE1-CORE) and varies detector; external stacks were not reimplemented |
| Prompt-injection benchmarks’ reported numbers (AgentDojo, InjecAgent, BIPIA, etc.) | Apparent external score tables | Different packs, threat models, success definitions, models, and often text-ASR not Tool-HASR. Cross-paper numeric comparison is a claims error |
| Track A VNEXT FAIL / Track B Phase-1 LIVE | Historical dual-track evidence in this repo | **Different packs and treatments.** Must not be pooled with Q2 Tool-HASR (MASTER_PROMPT rule 7) |
| Human red-team / open adaptive attacker | Threat-model completeness | C4 open adaptive attacker is out of current claim scope (see `LIMITATIONS.md` / `D3_AND_C4.md`) |

Exact product names, papers, and scores above are **category labels only**. They are **not** verified citations and **not** results. Literature verification is still required before a related-work section names any system.

## What a future fair baseline experiment would require

A comparison is fair only if all of the following are locked **before** live spend:

1. Same frozen pack (`p2_agentic_v0.1.0`, SHA `32b40e3b…`) or a new frozen pack with its own SHA.
2. Same Tool-HASR success_condition and official S0 denominator.
3. Same judge model and prompt, or a pre-registered judge-ablation labeled secondary.
4. Same target slots T0–T3 or a pre-registered target set; no post-hoc model shopping.
5. External method wrapped to the `P3Detector` contract **or** run as a documented full-stack alternative with policy entanglement disclosed.
6. No gold `is_attack` / `label` / `category` in the detector→risk→policy path.
7. Written eval plan, frozen detector/policy code, human budget sign-off (MASTER_PROMPT rule 6).
8. Explicit “not a ranking” / no SOTA language even if one method has lower Tool-HASR.

Until that experiment exists, **do not fill tables with numbers from other papers.**

## Why Q2 must not be described as SOTA / best / superior

- No external method was run on this pack.
- Protocol forbids detector ranking (`no_ranking=true`).
- `scientific_evidence=false` on the Q2 run; n=16 attack arms per cell is pilot-scale.
- Internal Δ vs D0 is an isolation contrast, not a leaderboard.

Allowed: “under the locked protocol, D1/D2/D4 showed negative Δ vs D0 on T0–T3.”  
Forbidden: “best detector,” “superior to published guards,” “state-of-the-art,” “solves prompt injection.”

## Baseline claims that require literature verification

These phrases must not appear in the manuscript until a human verifies the cited papers/systems and the comparison conditions:

- Any named external guardrail as “comparable” or “outperformed.”
- Any numeric ASR/HASR copied from another benchmark.
- “First” / “only” isolation of detector vs policy in agent security.
- Equivalence or superiority to Llama-Guard, PromptGuard, NeMo Guardrails, Microsoft Prompt Shields, or similar (names listed as **unverified category examples**, not citations).

**Gap status:** documented, not closed. Closing it requires a new live experiment (not this task).
