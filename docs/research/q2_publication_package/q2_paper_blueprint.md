# Q2 Paper Blueprint

RQ: Does the detector-related security effect under locked Stage-B target remain directionally consistent on independently selected secondary targets?

## Sections

| # | Section | Claim | Evidence | Figure/Table | Reviewer question |
| --- | --- | --- | --- | --- | --- |
| 1 | Introduction | Central contribution sentence | Framing | Fig1 teaser | Why not just another guardrail? |
| 2 | Related Work | Position vs injection/guardrails/agent eval | Repo + verified cites | — | What is new? |
| 3 | Threat Model | Tool-harm; C4 out of scope | P2 TM | T7 | Adaptive attackers? |
| 4 | ADAPTI-GUARD | Detector→risk→policy→tool gate | Architecture | Fig1–2 | How is policy held fixed? |
| 5 | Benchmark & Protocol | P1/P2 SHAs; Tool-HASR def; locks | Freeze + protocol | T1–T2 | Power? |
| 6 | Detector-Policy Isolation | Only detector varies | P3 design | Fig2 | Confounders? |
| 7 | Results | Δ vs D0 on T0; no ranking | Stage-B | T3 | Small n? |
| 8 | Cross-Target Analysis | 9/9 sign agreement | Q2 | Fig3, T4 | All LLMs? (no: selected set only) |
| 9 | Forensic Analysis | M3/M4; INVALID S0/S2 | Q2+SB traces | Fig4, T5–T6 | INVALID bias? |
| 10 | Cost and Utility | Normalized weights; action dists | Traces | Fig5 | Real money? |
| 11 | Limitations | Full list | This package | T7 | Hidden weaknesses? |
| 12 | Discussion | Attribution enabled/not | Ledger | — | Overclaim? |
| 13 | Conclusion | Restate bounded contribution | — | — | Future work = new study |

## TABLE SPECIFICATIONS (no invented values)

**TABLE 1 — Benchmark composition:** P1 44/44/8; P2 16/16/4; turns; SHAs.  
**TABLE 2 — Experimental configuration:** T0–T3 IDs; judge; seed 42; T=0; cache off; PHASE1-CORE; D0/D1/D2/D4; run IDs.  
**TABLE 3 — Stage-B detector-policy:** PHASE1-CORE Tool-HASR/Δ/CI per detector (from Stage-B).  
**TABLE 4 — Q2 cross-target Δ:** full Δ + Δ_change + sign_agreement (from `q2_final_statistics.json`).  
**TABLE 5 — Tool-HASR vs Judge-ASR / M3 / M4:** per target + aggregate.  
**TABLE 6 — INVALID sensitivity:** counts + S0 vs S2 signs.  
**TABLE 7 — Limitations and scope:** enumerated limits.

## FIGURE SPECIFICATIONS

**FIG 1 — Architecture:** boxes Detector / Risk / Policy / Tool Gate / Tools; no metrics. Source: system design docs.  
**FIG 2 — Pipeline:** annotate *varied*=detector, *locked*=policy/tools/thresholds.  
**FIG 3 — Δ across targets:** grouped bars D1/D2/D4 × T0–T3; data=`delta_table`; annotate 9/9; optional Wilson on underlying rates not on Δ.  
**FIG 4 — Disagreement:** M3/M4 counts + Tool-HASR vs Judge-ASR rates by target; data=stats JSON.  
**FIG 5 — Intervention/cost:** action distribution + mean normalized cost by target; label weights as normalized.

Plotting rules: exact numerators/denominators; no detector ranking colors/crowns; no cherry-picking.
