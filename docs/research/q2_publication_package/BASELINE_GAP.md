# External baseline gap (Q2)

**API calls this task:** 0  
**Frozen evidence modified:** No  
**Q2 raw traces modified:** No  
**Invented baseline numbers:** None

**The present study is an attribution study, not a head-to-head defense benchmark.**

This converts a review weakness into an explicit scope boundary. Current Q2 is not an external comparative benchmark.

## What was compared (internal only)

Q2 / Stage-B contrasts are **within-protocol**:

| Contrast | Status |
| --- | --- |
| D0 (no detection) vs D1 / D2 / D4 under locked PHASE1-CORE | Observed on P2 pack |
| T0 (Stage-B reuse) vs T1–T3 (Q2 live) for Δ sign | Observed |
| Tool-HASR vs Judge-ASR (M3/M4) | Observed |
| B0 / STATIC-A1 policy arms | Stage-B design includes them; **Q2 live is PHASE1-CORE only** (`B_REDUCED_Q2`) |

These are detector-isolation contrasts, not bake-offs against published external systems.

## Why numerical external comparisons are not added

Do **not** add numerical comparisons against CaMeL, AgentDojo defenses, ASB defenses, Llama Guard, PromptShield, or other external systems.

Reason: the protocols, populations, metrics, and execution environments differ. Copying ASR/HASR across papers is a claims error.

| Category | Examples (arXiv) | Why Q2 cannot claim a fair comparison |
| --- | --- | --- |
| Input/output detectors | Llama Guard `2312.06674`; PromptShield `2501.15145` | Not wrapped to `P3Detector` on this pack; not Tool-HASR under PHASE1-CORE |
| Programmable rails | NeMo Guardrails `2310.10501` | Rails entangle detection and intervention; not reconstructed here |
| Prompt/data channeling | StruQ `2402.06363`; Spotlighting `2403.14720` | Different mechanism class |
| Model-level defenses | Instruction Hierarchy `2404.13208`; Meta SecAlign `2507.02735` | Would change the *target*, violating Q2’s locked-target × vary-detector design |
| Architectural isolation | IsolateGPT `2403.04960`; CaMeL `2503.18813` | Full-stack alternatives; CaMeL is a published design, not an unverified idea, and still not a matched Q2 arm |
| Trajectory runtime detectors | MELON `2502.05174` | Different harness, pack, and success definition |
| Agent attack/defense benches | AgentDojo `2406.13352`; InjecAgent `2403.02691`; ASB `2410.02644`; AgentHarm `2410.09024`; BIPIA `2312.14197` | Paper identities VERIFIED; packs/threat models/metrics differ. Not UNCERTAIN as papers. Still incommensurable as numbers |
| Dual-track in this repo | Track A VNEXT FAIL; Track B Phase-1 LIVE | Must not be pooled with Q2 Tool-HASR |
| Open adaptive attacker | C4 (out of scope) | Not evaluated |

Vendor products were not compared.

## Why a fair comparison requires matched conditions

A comparison is fair only if all of the following are locked **before** live spend:

1. Same frozen pack (`p2_agentic_v0.1.0`, SHA `32b40e3b…`) or a new frozen pack with its own SHA.
2. Same Tool-HASR `success_condition` and official S0 denominator.
3. Same judge model and prompt, or a pre-registered judge-ablation labeled secondary.
4. Same target slots T0–T3 or a pre-registered target set; no post-hoc model shopping.
5. External method wrapped to the `P3Detector` contract **or** run as a documented full-stack alternative with policy entanglement disclosed.
6. No gold `is_attack` / `label` / `category` in the detector→risk→policy path.
7. Written eval plan, frozen detector/policy code, human budget sign-off (MASTER_PROMPT rule 6).
8. Explicit “not a ranking” / no SOTA language even if one method has lower Tool-HASR.

## Why current Q2 cannot claim superiority

- No external method was run on this pack.
- Protocol forbids detector ranking (`no_ranking=true`).
- `scientific_evidence=false`; n=16 attack arms per cell is pilot-scale.
- Internal Δ vs D0 is an isolation contrast, not a leaderboard.

Allowed: “under the locked protocol, D1/D2/D4 showed negative detector-related Δ vs D0 on T0–T3.”  
Forbidden: “best detector,” “superior to published guards,” “state-of-the-art,” “solves prompt injection,” “outperforms CaMeL/AgentDojo defenses.”

## Closing the gap would be a new study

Until a matched live experiment exists, **do not fill tables with numbers from other papers.** New live experiments are **not required** to finish this manuscript package; they are required only if the authors later choose a comparative-defense claim, which this package does **not**.

**Gap status:** documented scope boundary, not closed experimentally.
