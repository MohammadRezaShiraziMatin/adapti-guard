# P3 Detector Taxonomy

Interpretable detector set for causal attribution. No composite ranking score.

---

## D0 — No detection

| Field | Value |
| --- | --- |
| Class | `NoDetectionDetector` |
| Behavior | Always `detector_hit=false`, `risk_signal=0` |
| Purpose | Bound intervention attributable to downstream risk/policy without detector hits |
| Blind spots | Detects nothing by design |

---

## D1 — Current PHASE1 detector

| Field | Value |
| --- | --- |
| Class | `CurrentPhase1Detector` |
| Inner | `PromptInjectionDetectorPhase1` (`evidence_phase1.0`) |
| Retune | **Forbidden** — wrap as-is |
| Purpose | Current production/scientific baseline used by PHASE1-CORE stack |
| Notes | Policy still consumes risk engine separately; P3 isolates detector output via common contract |

---

## D2 — Pattern / heuristic detector

| Field | Value |
| --- | --- |
| Class | `HeuristicTaxonomyDetector` |
| Normalization | None beyond case-insensitive regex |
| Matching | OR over rules on `current_input + context` |
| Rules | `R_OVERRIDE`, `R_PRIVILEGE`, `R_EXFIL`, `R_TOOL_INJECT`, `R_MEMORY_PLANT`, `R_DELAYED_FIRE` |
| Purpose | Transparent mechanism-oriented coverage baseline |
| Blind spots | Documented per rule in `HEURISTIC_RULES` (paraphrase without keywords, novel tokens, silent injection) |

Risk signal = transparent function of number of fired rules (not calibrated probability).

---

## D3 — Semantic detector (**DEFERRED**)

| Field | Value |
| --- | --- |
| Status | `DEFERRED_NO_OFFLINE_IMPL` |
| Reason | No locked offline embedding dependency in-repo; live external model/API forbidden in design phase |
| Policy | Do **not** ship a placeholder that appears scientifically operational |

---

## D4 — Structured / context detector

| Field | Value |
| --- | --- |
| Class | `StructuredContextDetector` |
| Signals | untrusted source channel, tool_output present, MEMORY provenance marker, privileged tool name, tool-chain transition, privilege-escalation cues in visible text |
| Deterministic | Yes |
| Purpose | Agentic provenance coverage complementary to lexical rules |

---

## Contract reminder

All operational detectors implement `P3Detector.detect(EpisodeDetectionContext) -> DetectorResult` and refuse forbidden leakage keys.
