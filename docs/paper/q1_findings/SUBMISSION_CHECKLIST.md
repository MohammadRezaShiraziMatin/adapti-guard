# Q1 findings — submission checklist (human only)

**Venue:** **TBD** (not selected in this repository)  
**Upload status:** **NOT DONE** — no agent or automation may mark submission complete.  
**Author:** Seyed Mohammadreza Shirazi Matin · `mrshirazimatin@gmail.com`

Agents: **do not** merge PRs, upload to OpenReview/EasyChair/arXiv, or run live LLM eval.

---

## Pre-submit (documentation)

| Step | Owner | Status |
| --- | --- | --- |
| Read [`CLAIMS_MAP.md`](CLAIMS_MAP.md) + [`docs/paper/CLAIMS_CHECKLIST.md`](../CLAIMS_CHECKLIST.md) | Human | Required |
| Verify dual-track sections labeled (Track A / Track B / Layer A) | Human | Required |
| Confirm no invented Track A δ̂ CI (BLOCKING GAP in AUDIT) | Human | Required |
| Confirm V2 / AgentDojo / SOTA baselines cited as **Future Work** only (Q1-P2) | Human | Required |
| Offline smoke: `python3 docs/paper/workshop_vnext_fail/verify_manuscript_facts.py` | Human | Recommended |
| Hash appendix: [`workshop_vnext_fail/APPENDIX_HASHES.md`](../workshop_vnext_fail/APPENDIX_HASHES.md) | Human | Required |
| Optional P3 supplements | Human | **N/A until budget** — Phase 3 not done |

---

## Camera-ready (venue TBD)

| Step | Owner | Notes |
| --- | --- | --- |
| Pick venue / CFP | **HUMAN_ONLY** | Not decided in-repo |
| Convert [`MANUSCRIPT.md`](MANUSCRIPT.md) to venue template (LaTeX/Word) | **HUMAN_ONLY** | Markdown is source draft |
| Anonymization policy per venue | **HUMAN_ONLY** | Author name fixed in repo draft |
| Figure/table policy | **HUMAN_ONLY** | Separate Track A and Track B tables |
| Ethics / data availability statements | **HUMAN_ONLY** | Synthetic packs; no PII |

---

## Submit (explicitly not executed by agents)

| Step | Owner | Status |
| --- | --- | --- |
| Portal upload | **HUMAN_ONLY** | **NOT DONE** |
| Mark “submitted” in git | **HUMAN_ONLY** | Do not commit DONE without Matin |

---

## Related checklists

- Workshop packet (shorter Track A): [`workshop_vnext_fail/SUBMISSION_CHECKLIST.md`](../workshop_vnext_fail/SUBMISSION_CHECKLIST.md)
- Q1 roadmap Phase 4: [`docs/experiments/Q1_ROADMAP_4PHASE.md`](../../experiments/Q1_ROADMAP_4PHASE.md) (P3 live evidence still **pending budget**)
