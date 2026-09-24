# Literature Gap Audit — Multi-turn + Adaptive + Agentic

**ID:** `LIT-GAP-MT-AA-AG-1.0`  
**Status:** **IN PROGRESS** — structure locked; per-paper cells **UNVERIFIED** until primary source read  
**When:** Before Phase 3 live campaign; informs Q1 Related Work planning and extension RQs  
**Does not:** remove Layer 0 base papers; does not invent metrics or SOTA claims; does not claim multi-turn / AgentDojo / adaptive-attacker **live-evaluated**

**Companions:** [`LITERATURE_BASE.md`](LITERATURE_BASE.md) · [`UNIFIED_RESEARCH_FRAMEWORK.md`](UNIFIED_RESEARCH_FRAMEWORK.md) · [`../paper/q1_findings/Q1_JOURNAL_EMPIRICAL_EXTENSION_FRAME.md`](../paper/q1_findings/Q1_JOURNAL_EMPIRICAL_EXTENSION_FRAME.md) · [`../paper/q1_findings/CLAIMS_MAP.md`](../paper/q1_findings/CLAIMS_MAP.md)

---

## Purpose

For each **verified** paper in [`LITERATURE_BASE.md`](LITERATURE_BASE.md) Layer 1, extract nine dimensions and map **gap** to AdaptiGuard contributions:

- Controlled detector–policy decomposition  
- Tool-HASR vs Judge-ASR  
- Progressive realism (single-turn → multi-turn → adaptive → agentic) — **design roadmap**, not current live evidence  
- Reproducible protocol + evidence schema  

---

## Audit matrix (template)

Copy one block per paper after verification. Leave `source_verified: false` until PDF/official page checked.

### Paper: `<BibTeX key>` — `<Slot ID>`

| # | Dimension | Extracted from literature (quote or paraphrase + page/§) | AdaptiGuard gap / alignment |
| --- | --- | --- | --- |
| 1 | Definition (MT / adaptive / agentic) | *UNVERIFIED* | |
| 2 | Threat model | *UNVERIFIED* | |
| 3 | Attack mechanism | *UNVERIFIED* | |
| 4 | Dataset / benchmark | *UNVERIFIED* | |
| 5 | Models | *UNVERIFIED* | |
| 6 | Metrics | *UNVERIFIED* | |
| 7 | Defense | *UNVERIFIED* | |
| 8 | Limitations | *UNVERIFIED* | |
| 9 | Research gap | *UNVERIFIED* | |

```yaml
source_verified: false
primary_url: null
extraction_date_utc: null
extractor: null
```

---

## Cross-cutting gaps (hypothesis — refine after audit)

These are **design hypotheses**, not literature findings:

| Gap | Hypothesis | Confirmed after audit? |
| --- | --- | --- |
| G1 | Few works isolate **detector vs policy** under multi-turn agent episodes | **PENDING** |
| G2 | Textual ASR often reported without **tool outcome** verification | **PENDING** |
| G3 | Adaptive **attacker** vs adaptive **defense** conflated in related work | **PENDING** |
| G4 | Multi-turn benchmarks rarely share **frozen protocol** with single-turn confirm packs | **PENDING** |
| G5 | External baselines not comparable without harness lock | **PENDING** |

---

## Minimum paper count (Q1 bar)

| Extension pillar | Min. distinct verified papers (suggested) | Current verified |
| --- | ---: | ---: |
| Multi-turn injection | ≥3 | 0 |
| Adaptive (feedback) | ≥2 | 0 |
| Agentic / tool-use | ≥3 | 0 |
| Overlap allowed | same paper may cover 2 branches | — |

**Do not** cite in manuscript until `source_verified: true` row exists.

---

## Output artifacts (when audit completes)

1. Updated [`LITERATURE_BASE.md`](LITERATURE_BASE.md) slot table (PENDING → verified keys)  
2. Related Work subsection map in manuscript blueprint  
3. [`../paper/q1_findings/CLAIMS_MAP.md`](../paper/q1_findings/CLAIMS_MAP.md) — literature-backed claims only after verification  
4. No change to frozen experiments or Track A/B wording (Track A **FAIL** + Track B scoped **SUPPORTED_IMPROVEMENT** immutable)

---

## Workflow

```text
Select slot → Read primary source → Fill 9 rows → Mark source_verified
     → Synthesize gap paragraph (per extension, not per paper spam)
     → Human sign-off on bibliography before venue submit
```

**API=0** until Matin authorizes spend. Gap audit completion ≠ live eval authorization.
