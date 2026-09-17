# FINAL Limitations

## Pilot scale

- n=16 per cell; limited precision; limited power for broad generalization.
- Pilot-scale study; not confirmatory; directional consistency is an observed property of this evaluation.

## Model diversity

- Four targets only; three of four Qwen-family; judge also Qwen.
- Model-family diversity is limited; results should not be generalized to arbitrary model families.

## Provenance

- Stage-B raw traces MISSING_LOCALLY; official T0 reuse is not independent local recomputation.
- Bibliography: 8/21 remain preprint-only (VENUE_UNVERIFIED).

## External baseline

- No matched external baseline identified; attribution scope, not comparative ranking.

## D3 / C4 / adaptive attackers

- D3 deferred (embedding dependency not in locked offline protocol).
- C4 / open-ended adaptive attacker out of scope; not established.

## INVALID_TOOL_ARGS

- 192 events / 136 arms; canonical execution-state; potential confounder; not discarded; not proven negligible.

## Tool-HASR / Judge-ASR

- T1-T3 M3=108, M4=3; endpoints non-identical; disagreement not causally explained.

## Protocol-specific

- PHASE1-CORE, frozen P2, mock tools, short horizon, one judge, OpenRouter-only.

## Bibliography

- 8/21 preprint-only; camera-ready citations incomplete.

Detailed: `LIMITATIONS.md`, `docs/research/q2_publication_package/MANUSCRIPT_FINAL.md` Table 6.
