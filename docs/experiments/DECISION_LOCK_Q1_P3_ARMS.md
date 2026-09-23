# Decision lock Q1-P3 — Optional live arms (pre-registration scaffold)

**Decision ID:** Q1-P3  
**Status:** **LOCKED** (design / gates only — **no runs authorized**)  
**Date (UTC):** 2026-09-23  
**Author:** Seyed Mohammadreza Shirazi Matin  
**Mode:** Documentation only. **API=0** until explicit human budget. **No** merge, venue upload, or AUDIT edits from agents.

**Companion:** [`Q1_ROADMAP_4PHASE.md`](Q1_ROADMAP_4PHASE.md) · [`DECISION_LOCK_Q1_P2_EVIDENCE_DESIGN.md`](DECISION_LOCK_Q1_P2_EVIDENCE_DESIGN.md) · [`LIVE_EVALUATION_GATE.md`](../research/LIVE_EVALUATION_GATE.md)

---

## Immutable (all arms)

| Lock | Rule |
| --- | --- |
| Track A VNEXT FAIL | **Immutable** — no re-run to amend `VNEXT_CONFIRM/20260914-133147/` numbers or verdict |
| Retune-to-win | **Forbidden** — no threshold/detector/policy changes after seeing confirmatory outcomes |
| Target / Judge | **`qwen/qwen-2.5-7b-instruct`** target · **`qwen/qwen-2.5-72b-instruct`** judge unless a **new** human lock doc names a multi-model sweep |
| Claim mixing | Track labels mandatory; Track B **does not reverse** Track A |
| API spend | **HUMAN** budget placeholder — record approved USD cap and stop before run if exceeded |

**Phase 3 is not done** until Matin signs budget **and** a run completes with a **new** immutable AUDIT folder.

---

## Arm 1 — External baseline (optional)

**May run only after:** Human budget + written arm spec (baseline method id, config SHA, treatment name) + gate checklist.

| Item | Lock |
| --- | --- |
| Purpose | Commensurate third-party defense under **same** protocol as an existing frozen pack (Track A or B pack id declared before run) |
| Success (design) | Pre-specified: report ASR/U/McNemar vs B0 on **same episode IDs**; no pooled headline with other tracks |
| Failure / stop | Judge API failure → same-ID repair rule as VNEXT; hash mismatch → abort; do not impute ASR=0 |
| **Not allowed** | Claim SOTA; change Track A FAIL; fabricate expected ASR in this doc |

---

## Arm 2 — `p1_mechanism_v1.0.0` live eval (optional)

**May run only after:** [`LIVE_EVALUATION_GATE.md`](../research/LIVE_EVALUATION_GATE.md) + budget + pack SHA verified on execution branch.

| Item | Lock |
| --- | --- |
| Pack | `datasets/frozen/p1_mechanism_v1.0.0/` (SHA per freeze record) |
| Status today | **`live_evaluated=false`** |
| Success (design) | New AUDIT folder with hash-locked config; claims limited to mechanism benchmark scope |
| **Not allowed** | AgentDojo-class claim; replace Track A/B confirmatory evidence |

---

## Arm 3 — Confirmatory V2 pack + live (optional; **not executable in this lock**)

**May run only after:** Separate **pack freeze PR**, allocation/SAP human locks beyond Q1-P2 naming, budget, and new decision record superseding Q1-P2 “Future Work” for V2 **only when authorized**.

| Item | Lock |
| --- | --- |
| Taxonomy names | D-22 six `family_id` strings ([`DECISION_LOCK_D22_CONFIRMATORY_V2_TAXONOMY.md`](DECISION_LOCK_D22_CONFIRMATORY_V2_TAXONOMY.md)) |
| Allocation when built | Q1-P2 +1 → `PRIVILEGE_EXFIL` rule (design only until freeze) |
| This Q1-P3 doc | **Does not** authorize dataset bytes, episode bodies, or live eval for V2 |

---

## Stop rules (any live arm)

1. Hash mismatch on frozen pack → **stop** (no ad hoc pack).
2. Budget cap reached → **stop** (partial runs not merged into confirmatory claims).
3. Any attempt to re-test Track A VNEXT on `vnext_confirm_v1.0` for a “win” → **forbidden** (new experiment id ≠ amending FAIL AUDIT).
4. Outcomes feed **new** AUDIT paths only; update claims via [`CLAIMS_CHECKLIST.md`](../paper/CLAIMS_CHECKLIST.md).

---

## Success criteria (process — no fabricated ASR)

| Criterion | Meaning |
| --- | --- |
| Immutable AUDIT | New folder under `experiments/real_llm_eval/` written once; not edited in place |
| Pre-registration | Arm id, pack SHA, treatments, and stop rules cited in run request **before** API calls |
| Honest reporting | Results labeled by arm; FAIL/SUPPORTED_IMPROVEMENT outcomes on **historical** tracks unchanged |
| Optional Q1 manuscript supplement | Only after Matin adds AUDIT citation to findings draft — not assumed in this lock |

---

## API budget (human placeholder)

| Field | Value |
| --- | --- |
| Approved USD cap | **TBD — Matin** |
| Default until signed | **API=0** |
| Agents | Never approve spend or call OpenRouter |

**Navigation:** [`STATUS.md`](STATUS.md) · [`Q1_BLOCKER_MATRIX.md`](Q1_BLOCKER_MATRIX.md)
