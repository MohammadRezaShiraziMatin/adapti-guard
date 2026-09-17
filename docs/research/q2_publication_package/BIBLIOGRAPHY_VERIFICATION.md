# Bibliography verification (offline)

**API_CALLS=0. LLM_CALLS=0. NETWORK_CALLS=0.**  
Mode: compare `MANUSCRIPT_V1.md` references to existing `RELATED_WORK_MATRIX.json` records only. No Hub/web lookup in this packaging pass.

**Overall:** `BIBLIOGRAPHY_STATUS = PARTIAL`

| Field | Status |
| --- | --- |
| title / authors / year / arXiv id | **VERIFIED_FROM_EXISTING_PACKAGE_RECORD** (21/21) |
| venue | **UNVERIFIED** |
| DOI | **UNVERIFIED** |
| manuscript arXiv set vs matrix | **MATCH** (21 ids) |

No metadata was invented. Venues were not guessed.

## Novelty positioning preserved

**PARTIAL GAP.** The exact detector×locked-policy×Tool-HASR Δ sign factorial is **not** claimed to be globally unique. AgentDojo (`2406.13352`) and ASB (`2410.02644`) full texts were **not** completely audited.

| Paper | arXiv | Positioning vs Q2 |
| --- | --- | --- |
| Prompt injection / IPI | `2211.09527`, `2302.12173`, `2306.05499`, `2310.12815` | Threat literature; not the factorial |
| Guardrails / detectors | `2312.06674`, `2310.10501`, `2501.15145` | Detector- or rail-class; not locked-policy Tool-HASR Δ |
| Architectural isolation | CaMeL `2503.18813`; IsolateGPT `2403.04960` | Isolates channels/execution, **not** detector identity under fixed intervention |
| AgentDojo | `2406.13352` | Closest harness; full-text overlap **UNCERTAIN** |
| InjecAgent | `2403.02691` | Tool-integrated IPI benchmark |
| ASB | `2410.02644` | Large agent security bench; full-text overlap **UNCERTAIN** |
| AgentHarm | `2410.09024` | Harmfulness/jailbreak; not detector isolation |

Machine-readable: `BIBLIOGRAPHY_VERIFICATION.json`.
