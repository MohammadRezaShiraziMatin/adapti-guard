# P3 Research Specification — Detector Comparison

**Status:** Design + offline validation only (`P3_DESIGN_VALID` target)  
**Live execution:** Forbidden until separate human gate (`P3-C` not started)

---

## 1. Research questions

**Primary:** How much of observed agent-security behavior is attributable to the **detector** versus the **downstream intervention policy**?

**Secondary:** Can detector alternatives improve detection coverage while controlling false positives and preserving legitimate utility?

This is **not** a search for a universally “best” detector. No overall detector score. No ranking.

---

## 2. Evidence boundary

| Track | Artifact | SHA-256 |
| --- | --- | --- |
| P1 | `datasets/frozen/p1_mechanism_v1.0.0/` | `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` |
| P2 | `datasets/frozen/p2_agentic_v0.1.0/` | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` |
| P2 confirmation | `p2_agentic_p25_confirm_20260916T174248Z_f68783f1` | pilot/confirmation only |

Do **not** pool P2 with L1/VNEXT. Do not modify P1/P2 frozen packs or PHASE1-CORE thresholds.

---

## 3. Causal comparison structure

Hold constant: benchmark, trajectory, target model, tool schemas, permissions, risk thresholds, action costs, downstream policy, judge, temperature, cache.

**Only the detector varies.**

```text
same episode
     │
     ├── D0 ──┐
     ├── D1 ──┤
     ├── D2 ──┤
     └── D4 ──┘   (D3 deferred — no offline embedding stack)
                  ↓
            same policy
                  ↓
            same tool layer
                  ↓
          same outcome metrics
```

Fundamental observation IDs:

- Detector layer: `trajectory_id × detector_id × turn`
- End-to-end: `trajectory_id × detector_id × policy_id` (unique)

---

## 4. Detector candidates

| ID | Name | Status |
| --- | --- | --- |
| D0 | No detection (`detector_hit=false`) | Offline operational |
| D1 | Current PHASE1 detector (as-is, not retuned) | Offline operational |
| D2 | Pattern/heuristic taxonomy rules | Offline operational |
| D3 | Semantic/embedding | **DEFERRED** (no locked offline embedding; live API forbidden) |
| D4 | Structured/context provenance cues | Offline operational |

See `P3_DETECTOR_TAXONOMY.md`.

---

## 5. Common contract

```text
detect(EpisodeDetectionContext) -> DetectorResult
```

Required fields: `detector_id`, `detector_hit`, `risk_signal`, `evidence`, `confidence` (optional), `latency`, `reason_code`, `input_scope`, `version`.

Detectors must **not**: execute tools, mutate policy state, change action costs, or read judge/final-outcome/gold labels.

---

## 6. Leakage controls

Forbidden inputs include: judge fields, Tool-HASR/final outcomes, future turns/tool results, gold `label`/`is_attack`, final policy decisions.

Multi-turn: later turns must not influence earlier detector decisions. Offline tests enforce this.

---

## 7. Evaluation layers

| Layer | Measures |
| --- | --- |
| A Detection | attack detection rate, benign FPR, HN FPR, latency, mechanism coverage |
| B Intervention | intervention rate, A0–A3, mean cost (same policy) |
| C Outcome | Tool-HASR, Judge-ASR, M3/M4, utility, FPR |

Never attribute Layer C solely to the detector without policy interaction.

---

## 8. Metrics & statistics

**Primary detector-level:** attack detection rate, benign FPR, HN FPR  
**Primary end-to-end:** Tool-HASR, benign utility  
**Secondary:** Judge-ASR, M3/M4, intervention/cost, latency, coverage, disagreement  

Report numerator, denominator, point estimate, Wilson 95% CI, paired discordant counts.  
If McNemar used without freeze preregistration: `pre_registered = false`.

Action costs fixed: A0=0, A1=0.10, A2=0.25, A3=0.50.

Preserve P2.4 execution states and event-based invalid-args accounting (no snapshot-note inflation).

---

## 9. Phased plan

| Phase | Mode | Purpose |
| --- | --- | --- |
| P3-A | Offline on frozen P1 | Mechanism-level detector coverage |
| P3-B | Offline on frozen P2 | Agentic-context coverage |
| P3-C | Live | Only after offline gates + **separate human approval** |

**This work stops after design + offline validation. No P3-C.**

---

## 10. Quality gates

1. `P3_DESIGN_VALID`  
2. `P3_OFFLINE_VALID`  
3. `P3_HUMAN_GATE_READY` → then live may be considered (not automatic)

---

## 11. Implementation map

```text
docs/research/P3_RESEARCH_SPEC.md
docs/research/P3_DETECTOR_TAXONOMY.md
docs/research/P3_EVALUATION_PROTOCOL.md
src/adapti_guard/detectors/
tests/test_p3_detectors.py
tests/test_p3_protocol.py
```
