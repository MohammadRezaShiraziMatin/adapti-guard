# AdaptiGuard — Unified Research Framework (Q1 Journal)

**Status:** Architecture + scope lock (**documentation scaffold**).  
**Date context:** 2026-09-24  
**Author:** Seyed Mohammadreza Shirazi Matin  
**Rule:** Core evidence and dual-track verdicts are immutable unless independently authorized.  
**Rule:** Extensions are part of the **research design** (gated Future Work); claim / evidence tier is separate — see §3 and [`../paper/q1_findings/Q1_JOURNAL_EMPIRICAL_EXTENSION_FRAME.md`](../paper/q1_findings/Q1_JOURNAL_EMPIRICAL_EXTENSION_FRAME.md).  
**Rule:** This file does **not** import local experimental harnesses or claim multi-turn / AgentDojo / adaptive-attacker **live-evaluated**. **API=0.**

---

## 1. Conceptual stack

```text
Core Evaluation
│
├── Direct Prompt Injection
├── Indirect / RAG-oriented Injection (authored-channel in frozen packs)
├── Runtime Intervention (detector → risk → policy → action)
├── Deterministic Verification (success_condition / tool outcome)
├── LLM Judge (Target ≠ Judge)
└── Security–Utility–Cost
        │
        ▼
Official Research Extensions (design / Future Work — not this-cycle live evidence)
│
├── E1 Stateful Multi-turn
├── E2 Adaptive-to-Defense Attacks
└── E3 Agentic / Tool-use + State Transitions
        │
        ▼
Additional Robustness Dimensions (gated; not done this cycle)
│
├── R1 Multi-model (locked IDs + traces)
├── R2 Repeated seeds / trials
├── R3 Multilingual (if pre-registered)
└── R4 External baselines (fair harness match)
```

---

## 2. Single pipeline (no parallel frameworks)

```text
Attack / Episode spec
  ↓
Target LLM
  ↓
Runtime Defense
  ↓
Tool / Environment
  ↓
Verifier (deterministic + optional Judge)
  ↓
Metrics
  ↓
Statistical Analysis
```

**Extension overlays** (same pipeline; additional state machines — **designed** unless a future AUDIT says otherwise):

| Extension | Overlay | This-cycle status |
| --- | --- | --- |
| E1 Multi-turn | Turn → State → Turn → … → Outcome | Protocol lock only ([`PHASE2_PROTOCOL.md`](../experiments/protocols/PHASE2_PROTOCOL.md)); **not** live-evaluated |
| E2 Adaptive | Attack → Response → Defense observation → Attacker update → Next attack | Sim/template strata only; **not** live defense-aware red team |
| E3 Agentic | Prompt → Agent → Tool selection/args → Execution → State transition → Outcome verification | Mock tools / declared success conditions; **not** AgentDojo live |

Claim / gate status for extensions: [`../paper/q1_findings/Q1_JOURNAL_EMPIRICAL_EXTENSION_FRAME.md`](../paper/q1_findings/Q1_JOURNAL_EMPIRICAL_EXTENSION_FRAME.md) §3–4 (no separate `EXTENSION_STATUS_AUDIT.md` on this tip).

---

## 3. Evidence tiers (claim discipline)

| Tier | Meaning |
| --- | --- |
| **designed** | Protocol / taxonomy / architecture documented |
| **implemented** | Code path exists in this repo (may be mock/offline) — do not invent paths |
| **validated** | Deterministic tests or audits pass on harness |
| **live-evaluated** | Human-gated live LLM/API run with frozen lock + AUDIT |

Do not conflate tiers. Config names, literature **PENDING** slots, and manuscript prose are not evidence. Confirmatory live this cycle = Track A **FAIL** + Track B scoped **SUPPORTED_IMPROVEMENT** only.

---

## 4. Immutable historical layer

| Artifact | Binding |
| --- | --- |
| Track A VNEXT | **FAIL** (immutable) — [`../paper/dual_track/DUAL_TRACK_STATUS.md`](../paper/dual_track/DUAL_TRACK_STATUS.md) · AUDIT `VNEXT_CONFIRM/20260914-133147/` |
| Track B Phase-1 confirm | **SUPPORTED_IMPROVEMENT** (scoped) — same dual-track status |
| Frozen packs under `datasets/frozen/**` | Do not edit |
| Historical AUDIT / verdict JSON | Do not rewrite |

New Q1 work **extends**; it does not relabel Track A/B.

---

## 5. Live gate

No live evaluation without: frozen holdout/hash, detector/policy lock, written plan, explicit human budget sign-off ([`../experiments/MASTER_PROMPT.md`](../experiments/MASTER_PROMPT.md); [`LIVE_EVALUATION_GATE.md`](LIVE_EVALUATION_GATE.md)). Literature scaffold completion does **not** authorize spend.

---

## 6. Document map (paths on this tip)

| Topic | Canonical doc (this repository) |
| --- | --- |
| Extension gates / Scope honesty | [`../paper/q1_findings/Q1_JOURNAL_EMPIRICAL_EXTENSION_FRAME.md`](../paper/q1_findings/Q1_JOURNAL_EMPIRICAL_EXTENSION_FRAME.md) |
| Q1 claims map | [`../paper/q1_findings/CLAIMS_MAP.md`](../paper/q1_findings/CLAIMS_MAP.md) |
| Q1 reproducibility | [`../paper/q1_findings/REPRODUCIBILITY.md`](../paper/q1_findings/REPRODUCIBILITY.md) |
| Literature base (layered) | [`LITERATURE_BASE.md`](LITERATURE_BASE.md) |
| MT / Adaptive / Agentic gap audit | [`LITERATURE_GAP_AUDIT_MT_AA_AGENTIC.md`](LITERATURE_GAP_AUDIT_MT_AA_AGENTIC.md) |
| Core L1 live design | [`LIVE_EVALUATION_PROTOCOL.md`](LIVE_EVALUATION_PROTOCOL.md) |
| Phase-2 multi-turn protocol (design lock) | [`../experiments/protocols/PHASE2_PROTOCOL.md`](../experiments/protocols/PHASE2_PROTOCOL.md) |
| P1 mechanism pack | [`P1_MECHANISM_V1_0_0_FREEZE.md`](P1_MECHANISM_V1_0_0_FREEZE.md) |
| Dual-track claims | [`../paper/dual_track/CLAIMS_DUAL_TRACK.md`](../paper/dual_track/CLAIMS_DUAL_TRACK.md) |
| Research questions (stub → archive) | [`RESEARCH_QUESTIONS.md`](RESEARCH_QUESTIONS.md) |
| Metrics / estimands (stub → archive; confirmatory estimands in manuscript §5.4) | [`METRICS_AND_STATISTICS.md`](METRICS_AND_STATISTICS.md) · [`../../src/adapti_guard/evaluation/attack_success.py`](../../src/adapti_guard/evaluation/attack_success.py) |

**Not on this tip (do not invent):** `EXTENSION_STATUS_AUDIT.md`, `EXPERIMENT_PROTOCOL.md`, `EVIDENCE_SCHEMA.md`, `EXPERIMENT_MATRIX.yaml` — use the Q1 frame + dual-track / Phase-2 locks above instead of fabricating local WSL package paths.
