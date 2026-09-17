# Venue decision matrix (no selection)

**As of:** 2026-09-18  
**VENUE_STATUS = CATEGORY_ONLY**  
**NETWORK_CALLS=0 this turn.** Deadlines, page limits, and “currently open” flags are **UNVERIFIED** unless an official source was already in the package (none were). **Do not invent deadlines. Do not claim a venue is open.**

This file compares **realistic venue categories**. It does not convert the manuscript to a venue template. No venue is selected. No acceptance probability is stated.

Manuscript genre: **controlled attribution protocol + pilot-scale directional evidence**.  
Not: SOTA defense; not a systems bake-off; not a large-n confirmatory multi-model study.  
Pilot-scale risk applies to **every** row: n=16/cell, `scientific_evidence=false`, four Qwen-heavy targets, missing Stage-B raw traces, PARTIAL bibliography.

## Category A — AI Security workshop

| Field | Record |
| --- | --- |
| Scope fit | High if framed as evaluation/attribution of agent prompt-injection outcomes |
| Paper maturity required | Workshop: methods + bounded evidence often acceptable if limitations are blunt |
| Page limit | **UNVERIFIED** (often shorter than conference; do not guess) |
| Archival status | **UNVERIFIED** per workshop (some PMLR/CEUR; some non-archival) |
| Deadline | **UNVERIFIED** |
| Current status as of 2026-09-18 | **UNVERIFIED** |
| Submission still open | **UNVERIFIED** — not claimed |
| Risk from pilot-scale evidence | Reviewers may still demand bake-offs; `BASELINE_GAP.md` must be in the paper. Page limits may cut INVALID/M3 diagnostics that are scientifically required |

## Category B — Trustworthy / Safe AI workshop

| Field | Record |
| --- | --- |
| Scope fit | High for factorial isolation, dual endpoints, and honest `scientific_evidence=false` |
| Paper maturity required | Methods/evaluation workshops can accept pilots if the claim is directional, not confirmatory |
| Page limit | **UNVERIFIED** |
| Archival status | **UNVERIFIED** |
| Deadline | **UNVERIFIED** |
| Current status as of 2026-09-18 | **UNVERIFIED** |
| Submission still open | **UNVERIFIED** — not claimed |
| Risk from pilot-scale evidence | Pressure to generalize beyond four models; Qwen-heavy set is a predictable objection |

## Category C — Agent security workshop

| Field | Record |
| --- | --- |
| Scope fit | Highest thematically (Tool-HASR, agents, IPI) |
| Paper maturity required | Workshop findings paper; still needs reproducible artifacts |
| Page limit | **UNVERIFIED** (often short) |
| Archival status | **UNVERIFIED** |
| Deadline | **UNVERIFIED** |
| Current status as of 2026-09-18 | **UNVERIFIED** |
| Submission still open | **UNVERIFIED** — not claimed |
| Risk from pilot-scale evidence | Highest chance of “why no AgentDojo/ASB/CaMeL numbers?” The answer is scope: attribution, not leaderboard. Page cuts on diagnostics are dangerous |

## Category D — Security / AI systems short paper

| Field | Record |
| --- | --- |
| Scope fit | Medium-high if sold as a measurement protocol for runtime intervention, not as a product defense |
| Paper maturity required | Short papers still face security-venue demand for attacks, baselines, or larger n |
| Page limit | **UNVERIFIED** |
| Archival status | Typically archival for conference short papers — **UNVERIFIED per venue** |
| Deadline | **UNVERIFIED** |
| Current status as of 2026-09-18 | **UNVERIFIED** |
| Submission still open | **UNVERIFIED** — not claimed |
| Risk from pilot-scale evidence | High. Missing Stage-B traces and no matched baseline are default reject reasons if the title sounds like a defense system |

## Category E — Journal

| Field | Record |
| --- | --- |
| Scope fit | Medium if framed as evaluation infrastructure for agent tool governance |
| Paper maturity required | Highest: related-work venues verified, traces packaged, often larger n or a matched baseline |
| Page limit | **UNVERIFIED** (usually flexible) |
| Archival status | Archival (journal) |
| Deadline | Rolling or **UNVERIFIED** per journal; none claimed |
| Current status as of 2026-09-18 | **UNVERIFIED** |
| Submission still open | **UNVERIFIED** — not claimed |
| Risk from pilot-scale evidence | Highest maturity bar. PARTIAL bibliography and MISSING Stage-B traces currently block a responsible journal submit |

## Cross-category recommendation (not a venue pick)

Human chooses later. This package remains **READY_WITH_MAJOR_REVISIONS**. Do not submit until Stage-B traces are packaged or explicitly accepted as a documented hole, and until venue/DOI cleanup matches the target author kit.

Related category notes (not a decision): `VENUE_REQUIREMENTS.md`.
