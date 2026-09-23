# Q1 blocker matrix

**Author / owner:** Seyed Mohammadreza Shirazi Matin  
**Tip baseline:** `main` @ `e4870b9cc03a344835f341bfd61aa83d2bdf2bff`  
**Companion:** [`Q1_ROADMAP_4PHASE.md`](Q1_ROADMAP_4PHASE.md)  
**Authority for numbers:** Frozen `AUDIT.md` / `verdict.json` — this table does **not** override them.

Severity: **BLOCKING** = cannot claim Q1-ready confirmatory story without fix or explicit Future Work boundary; **MAJOR** = weakens external credibility; **MINOR** = polish / process.

| Blocker | Severity | Evidence today | Fix in which Q1 phase | Honest alternative if unfixed |
| --- | --- | --- | --- | --- |
| Track A VNEXT **FAIL** (immutable) | BLOCKING (for “win” claims) | FAIL; H1 qualified win = NO; AUDIT `VNEXT_CONFIRM/20260914-133147/` | — (not fixable by narrative) | Frame as **confirmed negative** under locked protocol; do not claim adaptive VNEXT success |
| Track A small **n = 61** attack (+61 benign) | MAJOR | Frozen pack manifest; same n in AUDIT | P2 (design: V2 sizing / power discussion); optional P3 if new pack approved | Report power limits; avoid generalization; V2 as Future Work if not run |
| McNemar **p = 0.0625** (b10=5, b01=0) — not significant at α=0.05 | MAJOR | `DUAL_TRACK_STATUS.md`; VNEXT AUDIT | P2 (methods text); not “fixed” by rewording | State non-significance explicitly; forbid “marginally confirmed” |
| **MSID not met** (δ̂ = 0.0820 &lt; 0.20) | BLOCKING (for Track A win) | VNEXT AUDIT; fail reason `msid_not_met` | — for Track A historical run | Negative result + estimand discussion; Track B MSID only on Track B pack |
| Track A **δ̂ 95% CI missing** in AUDIT | **BLOCKING GAP** | AUDIT reports δ̂ point estimate only; no CI field in official artifact | P2 (gap doc + approved offline recompute PR if Matin approves); never invent in prose | Cite point δ̂ only; label CI as **not reported in AUDIT**; or Future Work |
| **Heuristic detector** / no AgentDojo-class tool loops | MAJOR | Phase-1 / VNEXT harness; no AgentDojo integration in repo | P2 (must-have vs Future Work); P3 only if budget + protocol lock | Scope claims to frozen single-turn confirmatory setting; multi-step tool loops = Future Work |
| **No external SOTA baselines** run | MAJOR | No third-party defense arm in live AUDIT folders | P2 (baseline spec); P3 (optional run) | Compare to B0 and locked treatments only; no SOTA table |
| **Simulation ≠ real-LLM confirmatory** | BLOCKING (if mis-cited) | Historical sim in `04_results.md`; confirmatory = live AUDIT only | P1–P2 (claims discipline) | Never cite simulation ASR as live judge success ([`CLAIMS_CHECKLIST.md`](../paper/CLAIMS_CHECKLIST.md) F6) |
| **Dual-track mixup** risk (A vs B packs/treatments) | BLOCKING | Separate packs, SHAs, AUDIT paths documented | P1–P2; P4 manuscript review | Always label track; forbid one unlabeled ASR table |
| Confirmatory **V2**: D-22 **names locked**; allocation / episodes / SAP **not locked** | MAJOR | [`DECISION_LOCK_D22_CONFIRMATORY_V2_TAXONOMY.md`](DECISION_LOCK_D22_CONFIRMATORY_V2_TAXONOMY.md) | P2 (allocation + SAP); P3 (pack + eval) | Use Track A n=61 evidence only; V2 as planned work with 151÷6 remainder deferred |
| **`p1_mechanism_v1.0.0` frozen** but **`live_evaluated=false`** | MAJOR | Freeze on tip; gate docs; no mechanism-pack live AUDIT | P2 (gate checklist); P3 after budget | Cite benchmark spec + freeze SHA only; no live mechanism claims |
| **Venue TBD** / camera-ready | MINOR | Workshop checklist done; no venue marked submitted | P4 (human) | Internal manuscript + preprint decision deferred to Matin |
| **Overclaim risk** (ASR=0, L3 oracle, refusal-as-win) | BLOCKING (if violated) | [`CLAIMS_CHECKLIST.md`](../paper/CLAIMS_CHECKLIST.md) F5–F7 | P1–P4 claims review | Diagnostic layers and refusals labeled; harmful-action judge outcome only for confirmatory arms |
| Track A **utility ineligible** (U &lt; 0.95) | MAJOR | VNEXT AUDIT fail reason `s4_utility_ineligible` | P2 (discussion) | Report utility gate failure; no “deployable” wording |
| **Target ≠ Judge** discipline | MINOR (if maintained) / BLOCKING (if blurred) | qwen-7B target vs qwen-72B judge on confirmatory runs | P2–P4 | Keep models explicit in every table caption |
| Optional historical **PR stack #23–#44** not merged | MINOR | [`PR_STACK.md`](../paper/workshop_vnext_fail/PR_STACK.md) | Human (outside Q1 phases) | Tip `main` + merged #73 quality path sufficient for current docs truth |

---

## Process

- **API=0** for maintaining this matrix unless Matin approves live work (Phase 3).
- Update this table when a blocker moves to **fixed** — with pointer to decision doc or AUDIT path, not ad hoc numbers.
- **No Q1 acceptance guarantee:** clearing a row does not imply venue acceptance.

**Navigation:** [`Q1_ROADMAP_4PHASE.md`](Q1_ROADMAP_4PHASE.md) · [`STATUS.md`](STATUS.md)
