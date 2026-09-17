# Q1 Cost Model Audit

## Locked weights

| Action | Weight |
| --- | ---: |
| A0 | 0.00 |
| A1 | 0.10 |
| A2 | 0.25 |
| A3 | 0.50 |

Defined identically as `ACTION_COSTS` / `COSTS` in `detectors/protocol.py` and `metrics/tool_hasr.py`, and stamped into run manifests.

## Classification

These are **normalized experimental intervention cost weights**, **not**:

- measured monetary USD invoice costs of interventions, nor
- provider token prices (token USD is tracked separately on Q2 via OpenRouter list prices).

They encode a **relative** preference ordering: allow < light sanitize < heavier intervene < block.

## Observed mean intervention cost (official weights)

| Scope | Mean cost |
| --- | ---: |
| P3 Stage-B all arms | 0.078125 |
| PHASE1-CORE T0 (144 arms) | 0.134375 |
| Q2 T1 / T2 / T3 | 0.134375 / 0.132639 / 0.134375 |

(Computed from final actions under official weights; offline.)

## Offline sensitivity (no live runs)

Alternative weightings recomputed on frozen predictions:

| Scheme | Stage-B all | PHASE1 T0 | Q2 T1 |
| --- | ---: | ---: | ---: |
| official | 0.078 | 0.134 | 0.134 |
| uniform_step (0/0.25/0.5/0.75) | 0.173 | 0.269 | 0.269 |
| block_heavy (0/0.05/0.2/1.0) | 0.052 | 0.107 | 0.107 |
| sanitize_heavy (0/0.4/0.15/0.5) | 0.161 | 0.083 | 0.083 |
| zero_all_but_block | 0.0 | 0.0 | 0.0 |

**Qualitative interpretation:** Absolute mean-cost numbers move with weights (as expected). Under PHASE1-CORE, actions are mostly A0/A2 (few A3), so schemes that zero non-block actions drive mean cost → 0 without changing security endpoints. **Security estimands (Tool-HASR / Δ) are independent of these weights**; cost is an accounting overlay.

## Paper rules

- Label costs as **normalized experimental weights**.
- Do not claim monetary optimality or USD savings from A0–A3.
- Report token-USD (Q2: $0.152885) separately from intervention-weight costs.
- Include a short sensitivity note that qualitative security conclusions do not depend on the weight scale.
