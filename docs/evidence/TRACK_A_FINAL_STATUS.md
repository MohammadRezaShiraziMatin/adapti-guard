# ADAPTI-GUARD Track-A Final Status

**Date:** 2026-09-18
**Branch:** `cursor/q2-publication-hardening-f6f3`
**HEAD:** `58ef5bb`

## Historical Result (FROZEN)

| Metric | Value |
| --- | --- |
| B0 ASR | 58/61 = 0.9508 |
| VNEXT-ADAPT ASR | 53/61 = 0.8689 |
| Δ (δ̂) | 0.082 |
| p-value (McNemar) | 0.0625 |
| Utility (U) | 0.9344 |
| Verdict | **FAIL** |

**Fail reasons:**
1. `s5_mcnemar_not_significant` — p=0.0625 > α=0.05
2. `msid_not_met` — δ=0.082 < MSID=0.20
3. `s4_utility_ineligible` — U=0.9344 < required U≥0.95

## Historical Artifact Status

**Classification:** `CONSISTENT` (no mismatch)

The VNEXT-ADAPT predictions file (`VNEXT-ADAPT_predictions.jsonl`) contains **122 rows = 61 attack + 61 benign**. Verified facts:

- Row count: 122 (matches the frozen pack `vnext_confirm_v1.0`, 61 attack + 61 benign).
- Attack/benign classification uses the `label` and `attack_label` fields (both report 61 attack / 61 benign).
- `is_attack` is **not** part of the artifact schema; no row carries an `is_attack` field. Counting attacks via a non-existent `is_attack` field yields 0 attack / 122 benign and is an inspection error, not a property of the evidence.
- Historical VNEXT-ADAPT ASR = **53/61 = 0.8689**, computed by `arm_metrics()` from the **61 attack rows in this artifact**.
- Historical B0 ASR = **58/61 = 0.9508**, computed from the B0 artifact's 61 attack rows.
- `comparison.json` for the run reports `VNEXT-ADAPT.n_attack = 61`, `n_attack_success = 53`, `asr = 0.8689`, `excluded = {}`.

The historical Track-A verdict remains **FAIL** and is unchanged. The prior `ARTIFACT_MISMATCH` / "benign-only artifact" statement was a field-name inspection error and is withdrawn.

## Historical Stage-B

**Run ID:** `p3_stage_b_20260916T235438Z_7e401714`
**Status:** `EVIDENCE_NOT_RECOVERABLE`
**Recorded predictions SHA:** `7b0b72d942dae988d87acf238424c9f2d331b62d5ec582c9ba7d9bfbb293c214`

The original Stage-B bytes are unavailable. Do not rerun, recreate, or fabricate.

## New Evaluation

No new evaluation has been executed. No new runs are documented.

## Frozen Evidence

| Artifact | SHA-256 | Status |
| --- | --- | --- |
| P1 pack | `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` | VERIFIED (unchanged) |
| P2 pack | `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` | VERIFIED (unchanged) |
| Q2 predictions | `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6` | VERIFIED (unchanged) |
| VNEXT pack | `523c881820710783b5290c76ea5fe5fc01a6341fb427defcba1119fc3e721518` | VERIFIED (unchanged) |

## Tests

- **35 passed** (Track-A test suite)
- **0 failed**

## Integrity

- Code modified: NO
- Frozen evidence modified: NO
- API calls: 0
- LLM calls: 0
- Live experiments: 0
- Commits: 0
- Pushes: 0
