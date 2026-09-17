# Venue requirements (no final selection)

**Do not choose a journal by prestige. Do not claim acceptance probability.**  
This file maps **categories** and the information a later venue decision needs. Article-type length limits below are **UNVERIFIED** until the official author kit is checked at submission time.

## Fit of this manuscript (as written)

**Genre:** empirical methods + bounded pilot evidence.  
**Not:** SOTA defense paper; not a systems bake-off; not a large-n confirmatory multi-model study.

Best category fit is a venue that accepts **evaluation methodology**, **negative/partial results**, and **agent security measurement** without requiring a leaderboard.

## Categories

### 1. Trustworthy AI / empirical evaluation

- **Scope fit:** High if the paper is framed as attribution/evaluation, not as a product defense.
- **Methodological fit:** High (factorial isolation, dual endpoints, sensitivity).
- **Recent related (arXiv, venues UNVERIFIED):** Llama Guard `2312.06674`; Instruction Hierarchy `2404.13208`; PromptShield `2501.15145`.
- **Article type (typical):** conference paper or journal methods article. **Length: UNVERIFIED.**
- **Reproducibility expectations:** artifacts, hashes, seeds, model IDs — this package is close; Stage-B traces and rendered figures still missing.
- **Risk:** reviewers may demand larger n or more model families.

### 2. AI / LLM security

- **Scope fit:** High on prompt injection + agents.
- **Methodological fit:** Medium-high; security venues often want attack/defense bake-offs.
- **Recent related:** Greshake `2302.12173`; Liu `2310.12815`; AgentDojo `2406.13352`; ASB `2410.02644`; CaMeL `2503.18813`.
- **Article type:** conference. **Length: UNVERIFIED.**
- **Reproducibility:** often artifact appendices; some require official code.
- **Risk:** “why no CaMeL/AgentDojo comparison?” is the default review. `BASELINE_GAP.md` must be in the paper, not only the repo.

### 3. Agent security (workshop or special track)

- **Scope fit:** Highest thematically.
- **Methodological fit:** High if Tool-HASR is accepted as an operational endpoint.
- **Recent related:** InjecAgent `2403.02691`; AgentHarm `2410.09024`; IsolateGPT `2403.04960`; MELON `2502.05174`.
- **Article type:** workshop paper or findings paper. **Length: UNVERIFIED** (often shorter).
- **Risk:** workshop page limits may force cutting diagnostic INVALID/M3 material that is scientifically necessary.

### 4. AI safety

- **Scope fit:** Medium. Safety venues may want harm ontologies and policy implications this paper deliberately does not overclaim.
- **Methodological fit:** Medium. Pilot n may be acceptable if limitations are blunt.
- **Recent related:** AgentHarm `2410.09024`; ToolEmu `2309.15817`.
- **Article type:** conference/workshop. **Length: UNVERIFIED.**
- **Risk:** pressure to generalize beyond four models.

### 5. Information systems + AI

- **Scope fit:** Medium if framed as evaluation infrastructure for agent tool governance.
- **Methodological fit:** Journal-length would help (full limitations, related work, reproducibility).
- **Recent related:** NeMo Guardrails `2310.10501` (toolkit); application-injection papers `2306.05499`.
- **Article type:** journal. **Length: UNVERIFIED.**
- **Submission requirements:** typically blinded PDF, data availability statement. **UNVERIFIED per journal.**
- **Risk:** slower cycle; still need venue/DOI cleanup.

## Information still required per candidate venue (later)

For each concrete venue, fill **UNVERIFIED** fields from the official site only:

| Item | Status now |
| --- | --- |
| Scope fit | Category-level only |
| Methodological fit | Category-level only |
| Recent related papers | arXiv ids listed; venues UNVERIFIED |
| Article type | Typical guess; **UNVERIFIED** |
| Length / page limits | **UNVERIFIED** |
| Anonymity / dual submission | **UNVERIFIED** |
| Reproducibility / artifact badge | **UNVERIFIED** |
| Dual-track prior-publication overlap | Must be checked against Track A/B writeups before submit |

## Explicit non-decision

No venue is selected. No acceptance probability is stated. Human chooses after bibliography venues are verified and after deciding whether the paper remains methods+pilot or waits for a baseline experiment.
