# P2 Agentic Candidate — Freeze Record `v0.1.0`

**Status:** `FROZEN`  
**Date (UTC):** 2026-09-16  
**Datetime (UTC):** 2026-09-16T14:16:45Z  
**Pack path:** `datasets/frozen/p2_agentic_v0.1.0/`  
**dataset SHA-256:** `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd`

---

## Decision chain

```text
P2.2 OFFLINE HARNESS COMPLETE
 ↓
P2.3 CANDIDATE COMPLETE (16/16/4)
 ↓
FREEZE AUDIT v1 = NOT-FREEZE-READY
 ↓
REMEDIATION (taxonomy / chaining / persistence)
 ↓
FREEZE AUDIT v2 = NOT-FREEZE-READY (persistence causality)
 ↓
PERSISTENCE REMEDIATION v2
 ↓
FREEZE AUDIT v3 = FREEZE-READY (blocking issues: NONE)
 ↓
P2 p2_agentic_v0.1.0 FROZEN
 ↓
HUMAN BUDGET / LIVE-EVALUATION GATE
 ↓
Stage A / Stage B (not started by this freeze)
```

Audit v3:

- `/opt/cursor/artifacts/p2_freeze_audit_v3_report.md`
- `/opt/cursor/artifacts/p2_freeze_audit_v3_report.json`

Verdict: **`FREEZE-READY`**

---

## Inventory (verified at freeze)

| Item | Count |
| --- | ---: |
| Attacks | 16 |
| Benign twins | 16 |
| Hard negatives | 4 |
| Total trajectories | 36 |

---

## Provenance / lineage

| Field | Value |
| --- | --- |
| Version | `p2_agentic_v0.1.0` |
| Status | `FROZEN` |
| live_evaluated | `false` |
| Source candidate | `datasets/candidates/p2_agentic_v0/` |
| Source SHA-256 | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` |
| Frozen SHA-256 | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` |
| Freeze base commit | `1f572ce5145d968736e88cae2c45e58595bc619e` |
| Freeze commit | *(stamped after freeze commit)* |
| Candidate retained | yes (byte-identical `dataset.jsonl`) |

`dataset.jsonl` bytes were **copied without modification**. Manifest/card/README for the frozen path are freeze metadata only.

---

## Explicit status

```text
status = FROZEN
live_evaluated = false
NO LIVE LLM EVALUATION PERFORMED
```

---

## Known limitations (immutable documentation)

- pilot-scale n=16 attacks; not statistically powered
- not publication-ready
- mock tools only
- scripted adaptive attacker only (no LLM attacker)
- `C3-miss` and `B4-error` remain VARIANT `mechanism_id` labels
- provenance is metadata-level (`metadata.persistence_provenance`); `TurnSpec` unchanged
- `p2a_atk_002` / `p2a_atk_015` lack `persistence_provenance` objects despite observable turn-level causal chains
- benign twins may rename memory keys for benignity while preserving structure

Freeze means **immutable artifact**, not **perfect benchmark**.

---

## Scientific integrity at freeze

```text
P1 frozen pack unchanged
L1 evidence tree unchanged
P2.2 harness unchanged
detector unchanged
defense policy unchanged
thresholds unchanged
candidate pack contents unchanged (byte-identical copy only)
```

Verified at freeze:

- P1 SHA-256 `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235`
- L1 tree `l1_p1m_full_20260915T160302Z_ef2e98c3` → `3e4df48d06a0abeaa5408fb7c242fb79ae8de8525dec8bbd848c8635420eac03`

---

## Next gate

```text
HUMAN BUDGET / LIVE-EVALUATION GATE
```

Do not start Stage A, Stage B, or live evaluation automatically from this freeze.
