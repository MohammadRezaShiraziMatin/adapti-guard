# ADAPTI-GUARD Baseline Gap Assessment

**Date:** 2026-09-17. **API_CALLS=0.**

## BASELINE_STATUS = NO_MATCHED_EXTERNAL_BASELINE_IDENTIFIED

## B0 is an internal control, NOT an external baseline

B0 (no detection) is the internal reference arm within the Q2 factorial. It is not a published external defense. Do not misrepresent B0 as an external baseline.

## Candidate external baselines assessed

| Candidate | Applicable? | Fair? | Why not run |
| --- | --- | --- | --- |
| CaMeL | Architectural isolation; different mechanism class | No | Not wrappable to P3Detector without uncontrolled variables |
| AgentDojo defenses | Entangled detector+policy | No | Policy not locked; different protocol |
| ASB defenses | Entangled detector+policy | No | Policy not locked; different protocol |
| Llama Guard | I/O detector; different scope | No | Not wrapped to P3Detector; different success_condition |
| PromptShield | PI detector; different scope | No | Not wrapped to P3Detector |
| IsolateGPT | Architectural isolation | No | Full-stack alternative; not a detector arm |
| NeMo Guardrails | Rails entangle detection+policy | No | Cannot isolate detector from policy |
| StruQ/Spotlighting | Data channeling | No | Different mechanism class |
| Instruction Hierarchy/Meta SecAlign | Model-level | No | Changes target; violates locked-target design |

## Fairness criteria (all 10 must hold)

1. Same benchmark. 2. Same target. 3. Same judge. 4. Same tool schema. 5. Same permissions. 6. Same trajectory. 7. Same protocol. 8. Comparable action semantics. 9. Documented implementation. 10. Reproducible config.

No candidate satisfies all 10 criteria without introducing a new uncontrolled variable.

## Decision: DO NOT RUN

External baseline comparison was not performed because no matched, reproducible baseline satisfying the locked experimental protocol was identified. A matched live baseline would be a new study requiring human approval.

Detailed audit: `docs/research/q2_publication_package/BASELINE_GAP.md`.
