# P3 Offline Implementation

**Status target:** `P3_OFFLINE_VALID`  
**Live P3-C:** not started  
**D3:** deferred (`DEFERRED_NO_OFFLINE_IMPL`)

This document describes the offline detector-comparison infrastructure. It does **not** claim scientific detector superiority or confirmatory live results.

---

## Implemented detectors

| ID | Class | Notes |
| --- | --- | --- |
| D0 | `NoDetectionDetector` | Always `detector_hit=false` |
| D1 | `CurrentPhase1Detector` | Wrapper around PHASE1; **not retuned** |
| D2 | `HeuristicTaxonomyDetector` | Transparent regex/taxonomy rules + documented blind spots |
| D4 | `StructuredContextDetector` | Provenance / channel / tool-transition cues (current-turn only) |
| D3 | — | **Deferred** — no locked offline embedding; no fake implementation |

---

## Common interface

```text
detect(EpisodeDetectionContext) -> DetectorResult
```

Expanded adapter: `P3Detector.detect_parts(episode_context, current_input, tool_context, state, ...)`.

Required result fields: `detector_id`, `detector_hit`, `risk_signal`, `evidence`, `confidence` (optional), `latency_ms`, `reason_code`, `input_scope`, `version`.

Side-effect free: no tool execution, no judge calls, no future turns, no policy/benchmark mutation. Isolation helpers hash policy/tool/trajectory state before/after detect.

---

## Leakage controls

`FORBIDDEN_INPUT_KEYS` scanned recursively (including nested `state`): judge fields, Tool-HASR/final outcomes, future turns/tool results, gold labels, final policy decisions.

Multi-turn: detector decision at turn N must be identical whether or not turn N+1 exists.

---

## Counterfactual harness

Module: `adapti_guard.detectors.harness.OfflineDetectorHarness`

- Turn matrix: `trajectory × detector × turn` with unique `evaluation_id = run_id::trajectory::detector::tN`
- Policy schedule: `trajectory × detector × policy` with unique `evaluation_id = run_id::trajectory::detector::policy`
- Episode remains the statistical unit for end-to-end security metrics (turns are not episodes)
- Fail-closed SHA check before loading frozen P1/P2
- Downstream policy constants preserved: action costs A0–A3 unchanged; no PHASE1-CORE retune

---

## Metrics

Module: `adapti_guard.detectors.metrics`

**Detector-level:** attack detection rate, benign FPR, hard-negative FPR, mechanism coverage (descriptive), detection latency.

**End-to-end:** Tool-HASR, Judge-ASR, M3, M4, benign utility, hard-negative utility, intervention rate, mean intervention cost.

Rates report numerator, denominator, point estimate, Wilson 95% CI. Paired discordant counts use `pre_registered=false` unless a future human-approved protocol changes that.

No automatic winner selection, ranking, or overall detector score.

P2.4 event states: `EXECUTED | POLICY_DENIED | INVALID_TOOL_ARGS | UNSUPPORTED_TOOL | RUNTIME_ERROR` (event provenance; never snapshot-note inflation).

---

## Replay cases

Module: `adapti_guard.detectors.replay_cases` — 10 synthetic offline cases for **semantics validation only**. Not scientific performance evidence.

---

## Artifact verifier

Module: `adapti_guard.detectors.verifier.verify_p3_artifact_dir`

Fail-closed checks: required files, schema, unique evaluation IDs, detector IDs, benchmark SHA, policy IDs, no duplicate episode-detector / episode-detector-policy records, no leakage keys, valid metric denominators, reproducibility hash, overwrite protection.

---

## Benchmark compatibility

| Pack | Path | SHA-256 |
| --- | --- | --- |
| P1 | `datasets/frozen/p1_mechanism_v1.0.0/dataset.jsonl` | `1a0b0053…dd235` |
| P2 | `datasets/frozen/p2_agentic_v0.1.0/dataset.jsonl` | `32b40e3b…d64dd` |

Do not pool P2 with L1/VNEXT. Do not modify frozen bytes.

---

## Known limitations

1. D3 deferred.
2. Offline Layer-A matrices on frozen packs are descriptive infrastructure validation — not live confirmatory science.
3. End-to-end Layer B/C with live policy interaction requires a separate human gate (P3-C) — out of scope here.
4. P1/P2 are small/pilot-scale; Wilson CIs do not manufacture significance.
5. Synthetic replay cases must not be cited as benchmark results.

---

## Quality gates

1. `P3_DESIGN_VALID` — complete  
2. `P3_OFFLINE_VALID` — this implementation + offline tests  
3. `P3_HUMAN_GATE_READY` — future; not claimed here  
4. P3-C live — **false**
