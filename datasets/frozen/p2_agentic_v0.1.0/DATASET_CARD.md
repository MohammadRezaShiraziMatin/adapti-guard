# DATASET CARD — `p2_agentic_v0.1.0`

**Status:** `FROZEN`  
**live_evaluated:** `false`  
**Freeze date (UTC):** 2026-09-16

| Field | Value |
| --- | --- |
| Path | `datasets/frozen/p2_agentic_v0.1.0/dataset.jsonl` |
| Created from | `datasets/candidates/p2_agentic_v0/` (byte-identical `dataset.jsonl`) |
| SHA-256 | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` |
| Rows | 36 (16 attack / 16 benign twins / 4 hard negatives) |
| Harness | `p2.2.0-offline` |
| Freeze base commit | `1f572ce5145d968736e88cae2c45e58595bc619e` |
| Freeze decision | `FREEZE-READY` — Freeze Audit v3 |

## Freeze decision

Independent Audit v3 verdict **FREEZE-READY** with **no material blockers**. This freeze is **benchmark versioning + integrity**, not a live evaluation and not a claim of improved security.

Audit artifacts:

- `/opt/cursor/artifacts/p2_freeze_audit_v3_report.md`
- `/opt/cursor/artifacts/p2_freeze_audit_v3_report.json`

## Known limitations (retained at freeze)

- pilot-scale n=16 attacks; not statistically powered
- not publication-ready
- mock tools only
- scripted adaptive attacker only (no LLM attacker)
- `C3-miss` and `B4-error` remain VARIANT `mechanism_id` labels
- provenance is metadata-level; `TurnSpec` unchanged
- `p2a_atk_002` / `p2a_atk_015` lack `persistence_provenance` objects despite observable turn-level causal chains
- benign twins may rename memory keys for benignity while preserving structure

## Live evaluation

```text
NO LIVE LLM EVALUATION PERFORMED
live_evaluated = false
```

Next gate: **HUMAN BUDGET / LIVE-EVALUATION GATE** (not automatic).

## Provenance

Candidate copy retained at `datasets/candidates/p2_agentic_v0/` for provenance. Do not edit either `dataset.jsonl` after freeze.
