# FINAL Baseline Assessment

**Date:** 2026-09-17. **API_CALLS=0.**

## BASELINE_STATUS = NO_MATCHED_EXTERNAL_BASELINE_IDENTIFIED

B0 (no detection) is the internal reference arm, NOT an external baseline.

## Fairness criteria (all 10 must hold)

Same benchmark, target, judge, tool schema, permissions, trajectory, protocol, comparable action semantics, documented implementation, reproducible config.

## Assessment

No candidate (CaMeL, AgentDojo, ASB, Llama Guard, PromptShield, IsolateGPT, NeMo, StruQ, Spotlighting, Instruction Hierarchy, Meta SecAlign) satisfies all 10 criteria without introducing a new uncontrolled variable.

## Decision: DO NOT RUN

External baseline comparison was not performed because no matched, reproducible baseline satisfying the locked experimental protocol was identified.

Detailed: `docs/BASELINE_GAP_ASSESSMENT.md`.
