# Bibliography verification (hardening pass)

**API_CALLS=0. LLM_CALLS=0. NETWORK_CALLS=0.**  
This turn did **not** re-fetch publisher or arXiv pages. Classification uses existing package Hub records plus operator-supplied venue/DOI named in the hardening brief.

**Overall:** `BIBLIOGRAPHY_STATUS = PARTIAL`

| Field | Status |
| --- | --- |
| title / authors / year / arXiv id | **VERIFIED** (21/21, existing package Hub records) |
| venue / DOI (most records) | **UNVERIFIED** |
| AgentDojo venue/DOI | NeurIPS 2024 / `10.52202/079017-2636` — **OPERATOR_SUPPLIED_NOT_RECHECKED_THIS_TURN** |
| BIPIA venue/DOI | KDD 2025 / `10.1145/3690624.3709179` — **OPERATOR_SUPPLIED_NOT_RECHECKED_THIS_TURN** |
| manuscript arXiv set vs matrix | **MATCH** (21 ids) |
| Task Shield `2412.16682` | **Not in verified matrix; not added as a reference.** Noted in `MANUSCRIPT_FINAL.md` §4 only as a named class this study does not implement or compare. Identity/venue/DOI **UNVERIFIED** in-package. |
| AgentDojo / ASB identity | **VERIFIED** (not UNCERTAIN) |
| CaMeL | **VERIFIED paper identity**; published architectural isolation; not an unverified idea |

No metadata was invented. Venues were not guessed beyond the two operator-supplied records.

## Per-record overall class

All 21 records: identity **VERIFIED**, overall **PARTIALLY_VERIFIED** (venue/DOI incomplete or operator-supplied without publisher re-fetch). None **UNVERIFIED** as papers. None upgraded to camera-ready **VERIFIED** bibliography.

## Novelty positioning preserved

**PARTIAL_GAP.** Residual sentence:

> The verified literature establishes extensive work on attacks, benchmarks, defenses, and adaptive evaluation, but does not establish the exact locked-policy detector-attribution factorial used here as the central measurement protocol.

| Paper | arXiv | Positioning vs Q2 |
| --- | --- | --- |
| Greshake et al. | `2302.12173` | IPI threat literature; identity VERIFIED |
| AgentDojo | `2406.13352` | Dynamic agent eval; identity VERIFIED; venue operator-supplied; not Q2 factorial; not a numerical baseline |
| ASB | `2410.02644` | Agent security bench; identity VERIFIED; not UNCERTAIN; not Q2 factorial; not a numerical baseline |
| CaMeL | `2503.18813` | Published control/data isolation; not an unverified idea; not Q2 factorial |
| InjecAgent | `2403.02691` | Tool-integrated IPI benchmark |
| AgentHarm | `2410.09024` | Harmfulness/jailbreak; not detector isolation |
| IsolateGPT | `2403.04960` | Execution isolation architecture |
| BIPIA | `2312.14197` | IPI benchmark/defense; KDD 2025 operator-supplied |
| Instruction Hierarchy | `2404.13208` | Privileged-instruction training; changes the target |

Machine-readable: `BIBLIOGRAPHY_VERIFICATION.json`.
