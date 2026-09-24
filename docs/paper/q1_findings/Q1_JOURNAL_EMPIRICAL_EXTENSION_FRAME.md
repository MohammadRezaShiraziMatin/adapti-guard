# Q1 Journal empirical extension frame

**Author:** Seyed Mohammadreza Shirazi Matin  
**Date (UTC):** 2026-09-24  
**Tip SHA (`main` lineage):** `79cafd2`  
**Mode:** Documentation only. **API=0.** No live OpenRouter, no eval spend, no `datasets/frozen/**` or AUDIT mutation.

**Purpose:** Keep AdaptiGuard as a coherent, reproducible, extensible **empirical study** whose *current* evidence base stays Findings/workshop-defensible, while naming **gated** confirmatory extensions that a later Journal/Q1 main path may require—**without** claiming those extensions are done and **without** artificially enlarging Scope.

**Companions:** [`MANUSCRIPT.md`](MANUSCRIPT.md) · [`CLAIMS_MAP.md`](CLAIMS_MAP.md) · [`CONTRIBUTION_CEILING.md`](CONTRIBUTION_CEILING.md) · [`QUALITY_GAPS.md`](QUALITY_GAPS.md) · [`DECISION_LOCK_FINDINGS_VENUE.md`](DECISION_LOCK_FINDINGS_VENUE.md) · [`DECISION_LOCK_Q1_P2_EVIDENCE_DESIGN.md`](../../experiments/DECISION_LOCK_Q1_P2_EVIDENCE_DESIGN.md)

---

## 1. What this study IS (preserve)

| Element | Lock |
| --- | --- |
| **Design** | Dual-track confirmatory eval: hash-locked packs, Target ≠ Judge, defense-attributed McNemar cells, utility co-primary, MSID |
| **Track A** | VNEXT-ADAPT vs B0 on `vnext_confirm_v1.0` → **FAIL** immutable (`VNEXT_CONFIRM/20260914-133147/`) |
| **Track B** | PHASE1-CORE vs B0 on `phase1_confirm_v1` → **SUPPORTED_IMPROVEMENT** scoped; **does not reverse** Track A |
| **Layer A** | CLOSED diagnostic (detector lift; adaptive ASR reduction not significant) — not confirmatory for A/B |
| **Offline supplements** | Track A δ̂ 95% CI + McNemar power/sensitivity from frozen integers; labeled offline, not in original AUDIT |
| **Venue honesty** | Findings / workshop-style fit today; Journal/Q1 **main** needs extensions below — not overclaim now |

**Core estimands (unchanged):** defense-attributed \(\hat\delta=(b_{10}-b_{01})/n_{\text{attack}}\); McNemar exact on \((b_{10},b_{01})\); utility \(U\) co-primary; Track A MSID \(\delta=0.20\).

---

## 2. What stays frozen

- Track A **FAIL** numbers and fail reasons — no FAIL→PASS.
- Track B scoped **SUPPORTED_IMPROVEMENT** wording — no upgrade to “AdaptiGuard works.”
- `datasets/frozen/**` pack bytes and historical AUDIT folders.
- Confirmatory Target/Judge pair: `qwen/qwen-2.5-7b-instruct` ≠ `qwen/qwen-2.5-72b-instruct`.
- Single-seed confirmatory live (**R=1**); no invented multi-seed results.
- Authored synthetic packs as the confirmatory corpora for this cycle.

---

## 3. Scope audit — honest status (do not expand claims)

Use as **truth for prose**. Status labels: DONE / PARTIAL / GAP. None of the PARTIAL/GAP rows become “done” by this note.

| Area | Status | Honest bound |
| --- | --- | --- |
| Deterministic verifier + LLM Judge | **DONE** | Confirmatory tracks use independent Judge |
| Target ≠ Judge | **DONE** | Locked model IDs above |
| Direct / indirect / RAG-shaped packs | **PARTIAL** | Authored pack surfaces; **≠** live retriever / production RAG |
| Adaptive attacker | **PARTIAL** | Simulation / template strata only — **not** live defense-aware adaptive red team |
| Mock tools | **PARTIAL** | Declared tool success conditions; **not** AgentDojo sandboxes |
| Statistics | **PARTIAL** | Single-seed (**R=1**); Track A δ̂ CI offline-only |
| Ablation | **PARTIAL** | Layer A diagnostic only; Phase-3 arms design-only |
| Taxonomy docs ≫ live | **PARTIAL** | Mechanism / V2 family names locked for **future** metadata |
| OWASP cite | **PARTIAL** | Citation allowed; **no** NIST live eval; **no** AgentDojo live |
| Stateful multi-turn live | **GAP** | Phase-2 protocol unevaluated — Future Work |
| Multilingual corpora | **GAP** | Confirmatory packs are **English-only** — Future Work |
| Four named frontier targets | **GAP** | Qwen3-30B-A3B-Instruct-2507, Gemma4 26B A4B, GPT-5, Claude Sonnet 4 are **not** confirmatory targets this cycle — config placeholders / Future Work only |

---

## 4. Gated Future Work (extension roadmap — not implemented)

Extensions may be added later as **new** immutable AUDIT folders under human budget + design locks. They **do not** amend Track A FAIL or inflate this cycle’s Scope checklist.

| Gate | Extension | May add (when authorized) | Must not claim now |
| --- | --- | --- | --- |
| **FW-MT** | Stateful multi-turn | Phase-2 episode harness live per [`PHASE2_PROTOCOL.md`](../../experiments/protocols/PHASE2_PROTOCOL.md) | Multi-turn defense evaluated / wins |
| **FW-AD** | AgentDojo-class | Tool-loop benchmark under locked protocol | AgentDojo leaderboard entry |
| **FW-BL** | External baselines | Commensurate arms on same episode IDs (P3-1) | SOTA / superiority |
| **FW-MM** | Multi-model | Pre-locked Target/Judge matrix (P3-3/4); optional frontier IDs only after human lock | Four named frontier models as confirmatory evidence |
| **FW-V2** | Confirmatory V2 | Larger n / D-22 families after freeze+SAP | Retcon VNEXT MSID on old pack |
| **FW-RAG** | Live retrieval | Real retriever + injected docs under new pack | Authored RAG-shaped text = live RAG |
| **FW-ATK** | Live adaptive offense | Defense-aware attacker in live eval | Sim adaptive = live adaptive |
| **FW-LANG** | Multilingual | Non-English frozen packs + SAP | English-only = multilingual coverage |
| **FW-SEED** | Multi-seed / R>1 | Pre-registered seeds on locked packs | R=1 as multi-seed robustness |
| **FW-MECH** | Mechanism pack live | `p1_mechanism_v1.0.0` with `live_evaluated=true` | Spec/freeze SHA as live result |

**Priority / budget:** optional Phase 3 order in [`Q1_P3_PRIORITY.md`](../../experiments/Q1_P3_PRIORITY.md). **API=0** until Matin signs a spend cap. No guarantee any extension moves Findings → Journal main accept.

---

## 5. Claim discipline (binding)

1. Report **Track A FAIL first**, then Track B scoped improvement.
2. Never pool Track A and Track B ASR in one unlabeled table.
3. Label offline CI/power as offline; never invent AUDIT numbers.
4. Future Work rows are **gates**, not DONE checkmarks.
5. Forbidden paraphrases: [`CLAIMS_MAP.md`](CLAIMS_MAP.md) **Forbidden** table (incl. frontier targets, NIST/AgentDojo live, live adaptive attacker, live retriever, multilingual, R>1).

**Navigation:** [`MANUSCRIPT.md`](MANUSCRIPT.md) §5.5 / §8 · [`QUALITY_GAPS.md`](QUALITY_GAPS.md) · [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md)
