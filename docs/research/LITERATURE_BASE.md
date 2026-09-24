# Literature Base — Layered (Q1)

**Author context:** Seyed Mohammadreza Shirazi Matin  
**Status:** Layer 1 **scaffold** — candidate slots **PENDING**; not a manuscript bibliography.  
**Rule:** Base Papers (prompt injection core, runtime defense, Track A/B context) are **retained**. This document adds a **second layer** for confirmatory extensions.

**Rule:** No citation text or metric copied here without primary-source verification (`source_verified` in the gap audit). Slots below name **categories** and **candidate works** to audit — not empirical claims.

**Q1 frame:** Literature prep supports gated Future Work only — **not** done evidence. See [`../paper/q1_findings/Q1_JOURNAL_EMPIRICAL_EXTENSION_FRAME.md`](../paper/q1_findings/Q1_JOURNAL_EMPIRICAL_EXTENSION_FRAME.md). **API=0.**

---

## Layer 0 — Base Papers (unchanged)

Existing related-work spine for:

- Direct / indirect prompt injection
- Runtime intervention & guardrails
- Evaluation methodology (ASR vs operational harm)
- Project frozen evidence (VNEXT FAIL, Phase-1 confirm — **not** relabeled)

Pointers: [`../paper/dual_track/`](../paper/dual_track/) · workshop [`../paper/workshop_vnext_fail/`](../paper/workshop_vnext_fail/) · findings [`../paper/q1_findings/references.bib`](../paper/q1_findings/references.bib) · [`MANUSCRIPT.md`](../paper/q1_findings/MANUSCRIPT.md) §2.

---

## Layer 1 — Extension Literature Base (add; do not replace Layer 0)

```text
Literature Base (extensions)
│
├── Prompt Injection (mechanism refinement)
│   ├── Direct
│   ├── Indirect
│   └── RAG-oriented
│
├── Adaptive Attacks
│   └── Iterative / feedback-guided
│
├── Agentic Security
│   ├── Tool-use
│   └── Stateful environment
│
└── Multi-turn Injection
    ├── Multi-turn attacks
    ├── Persistent / delayed injection
    └── Adaptive multi-turn interaction
```

---

## Candidate paper slots (verify before citing in manuscript)

Assign each verified paper to one or more branches. **Do not** treat this table as bibliography until audited.

| Slot ID | Branch | Candidate work (title short) | Verification |
| --- | --- | --- | --- |
| MT-1 | Multi-turn | AgentDojo (dynamic agent eval) | **PENDING** |
| MT-2 | Multi-turn | InjecAgent (indirect tool-agent PI) | **PENDING** |
| MT-3 | Multi-turn | IterInject (iterative indirect PI) | **PENDING** |
| MT-4 | Persistent / delayed | Task Shield / delayed activation lines | **PENDING** |
| AD-1 | Adaptive | Adaptive attacks break defenses (agent PI) | **PENDING** |
| AD-2 | Adaptive | AutoDojo / adaptive black-box eval | **PENDING** |
| AG-1 | Tool-use | Design patterns for securing LLM agents | **PENDING** |
| AG-2 | Tool-use | VIGIL / tool-stream defense | **PENDING** |
| PI-RAG | RAG | BIPIA / retrieved-document injection | **PENDING** |

Replace **PENDING** with BibTeX key + URL only after human/agent reads primary PDF and records `source_verified: true` in [`LITERATURE_GAP_AUDIT_MT_AA_AGENTIC.md`](LITERATURE_GAP_AUDIT_MT_AA_AGENTIC.md).

---

## Extraction schema (per paper)

Use [`LITERATURE_GAP_AUDIT_MT_AA_AGENTIC.md`](LITERATURE_GAP_AUDIT_MT_AA_AGENTIC.md) — nine fields:

1. Multi-turn / extension **definition**
2. **Threat model**
3. **Attack mechanism**
4. **Dataset / benchmark**
5. **Models**
6. **Metrics**
7. **Defense**
8. **Limitations**
9. **Research gap** (vs AdaptiGuard unified framework)

---

## Link to research program

| Extension | Literature branches |
| --- | --- |
| E1 Stateful multi-turn | Multi-turn + Agentic (state) |
| E2 Adaptive attacker | Adaptive + Multi-turn (adaptive interaction) |
| E3 Agent / tool-use | Agentic + Indirect/RAG where tool I/O |

Gap audit gates **Phase 3 live campaign** planning; it does **not** authorize live spend and does **not** claim multi-turn / AgentDojo / adaptive-attacker live evaluation. Track A **FAIL** and Track B scoped **SUPPORTED_IMPROVEMENT** remain immutable.

**Navigation:** [`UNIFIED_RESEARCH_FRAMEWORK.md`](UNIFIED_RESEARCH_FRAMEWORK.md) · [`LITERATURE_GAP_AUDIT_MT_AA_AGENTIC.md`](LITERATURE_GAP_AUDIT_MT_AA_AGENTIC.md) · [`../paper/q1_findings/Q1_JOURNAL_EMPIRICAL_EXTENSION_FRAME.md`](../paper/q1_findings/Q1_JOURNAL_EMPIRICAL_EXTENSION_FRAME.md)
