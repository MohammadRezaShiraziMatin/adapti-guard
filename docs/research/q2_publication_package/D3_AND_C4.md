# D3 deferred and C4 scope

**API calls:** 0. **No fabricated D3 or C4 experimental results.**

These items are **documentation of absence**, not placeholder scores.

## D3 — deferred (no result)

| Field | Value |
| --- | --- |
| Detector | D3 semantic / embedding class |
| Status | `DEFERRED_NO_OFFLINE_IMPL` |
| Operational in Q2? | **No.** Live gates raise `STOP_D3_DEFERRED` / `STOP_D3_PRESENT` |
| Why deferred | No locked offline embedding dependency in-repo; live external embedding/API calls are forbidden as a fake-operational detector (`src/adapti_guard/detectors/__init__.py`) |
| Q2 implication | Detector-related Δ is estimated only for D0/D1/D2/D4 |
| Future work | A new study may add D3 **after** an offline embedding stack is locked, hashed, and human-approved — that would be a new experiment, not a backfill of this run |

Do not add “D3 = N/A%” cells that look like measurements.

## C4 — out of current claim scope

Two different C4 meanings exist in this repo; mixing them is a claims error.

| Sense | Where | What it is | What Q2 may claim |
| --- | --- | --- | --- |
| **C4 family on P1** | Frozen P1 pack | **0 rows**; `out_of_scope_families: ["C4"]` | Nothing. P1 does not measure open adaptive attackers |
| **C4-mini on P2** | Frozen P2 pack / taxonomy | Scripted paraphrase / channel-shift / delay templates with a fixed rewrite budget (`P2_ATTACK_TAXONOMY.md` P2-D) | Trajectories may include those templates as **benchmark content**. That is not an interactive LLM attacker and not a human red team |
| **Open adaptive attacker** | Threat model / future | Attacker observes defense outputs and rewrites freely | **Out of scope. Not established.** |

PHASE1-CORE **adapts actions** (A0–A3) given detector/risk signals. Action adaptation ≠ closed-loop adaptive attacker.

**Interpretation:** Q2 directional consistency is not evidence of robustness to adaptive attacks. Do not write “handles C4” or “robust to adaptive attackers.”

**Future work:** a separately frozen pack + protocol for interactive adaptive attackers (new live spend, rule 6).
