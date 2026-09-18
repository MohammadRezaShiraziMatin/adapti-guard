# ADAPTI-GUARD · Evaluation Integrity Rules

## ROLE

You are working on the ADAPTI-GUARD research repository.
Your priority is:
1. scientific integrity
2. evidence provenance
3. reproducibility
4. deterministic validation
5. minimal code changes

Do not optimize results for a desired outcome.
Do not silently change historical results.
Do not mix historical and new evidence.

---

# 1. HISTORICAL TRACK-A STATUS

The following historical result is frozen:

**Source protocol/pack:** `vnext_confirm_v1.0`

**Composition:** 61 attack + 61 benign

**Historical B0:** `58/61 = 0.9508`

**Historical VNEXT-ADAPT:** `53/61 = 0.8689`

**Historical Track-A:** `FAIL`

Historical evidence must remain unchanged.

**IMPORTANT:**
Do NOT infer or assign a SHA to the frozen pack unless it is verified from the actual artifact.
Do NOT copy the SHA of a prediction artifact and label it as the pack SHA.
Every SHA must be calculated from the exact file it describes.

---

# 2. HISTORICAL STAGE-B

**Run ID:** `p3_stage_b_20260916T235438Z_7e401714`

**Status:** `EVIDENCE_NOT_RECOVERABLE`

**Recorded historical predictions SHA:** `7b0b72d942dae988d87acf238424c9f2d331b62d5ec582c9ba7d9bfbb293c214`

The original Stage-B bytes are unavailable.

**Rules:**
- Do NOT rerun Stage-B.
- Do NOT recreate Stage-B.
- Do NOT fabricate missing artifacts.
- Do NOT assign new artifacts to the historical Stage-B run ID.
- Do NOT modify the historical scientific record.

---

# 3. TRACK-A ARTIFACT FINDING

The VNEXT-ADAPT prediction artifact (`VNEXT-ADAPT_predictions.jsonl`, SHA256 `50ca9c0345e0b477999fc73b9c3759ae6d0b9a97ebabfc6f66f28d45bbc7a318`) is the complete attack+benign evaluation artifact:

- **total rows:** 122
- **attack rows:** 61
- **benign rows:** 61
- **classification fields:** `label` and `attack_label` (both report 61 attack / 61 benign)
- **`is_attack` is not part of the artifact schema**; no row carries an `is_attack` field. Counting attacks via a non-existent `is_attack` field yields 0 attack / 122 benign and is an inspection error, not a property of the evidence.

The historical `53/61` VNEXT-ADAPT ASR is computed by `arm_metrics()` from the **61 attack rows in this artifact**. The historical `58/61` B0 ASR is computed from the B0 artifact's 61 attack rows.

**Classification:** `CONSISTENT` (no mismatch). The prior `ARTIFACT_MISMATCH` / "benign-only artifact" statement was a field-name inspection error and is withdrawn.

Do not change the historical result. The historical Track-A verdict remains **FAIL**.

---

# 4. FROZEN EVIDENCE RULES

Never modify:
- frozen datasets
- frozen evaluation packs
- historical metrics
- historical reports
- historical manifests
- P1/P2/Q2 frozen evidence
- historical Track-A results

Never:
- overwrite historical artifacts
- silently replace historical metrics
- recalculate historical metrics from a different artifact
- merge historical and new predictions
- reuse historical run IDs for new evaluations

If a historical artifact is incomplete or missing, preserve that fact.

---

# 5. NEW RUNS MUST BE SEPARATE

Any new evaluation must receive a NEW run ID.

Example: `vnext_adapt_repro_<timestamp>_<short_hash>`

A new run must never overwrite:
- `vnext_confirm_v1.0`
- historical Track-A evidence
- Stage-B evidence
- historical run directories

---

# 6. PRE-EVALUATION CONTRACT

Before a new evaluation starts, validate:
- dataset identity
- dataset SHA256
- protocol identity
- protocol SHA256
- expected attack count
- expected benign count
- expected total
- unique sample IDs
- unique episode IDs
- model identity
- target/judge configuration
- seed
- code commit

For the standard VNEXT pack:
- expected attack: 61
- expected benign: 61
- expected total: 122

These values must preferably be read from the verified protocol/manifest rather than hard-coded.

If:
- attack != expected_attack
- OR
- benign != expected_benign
- OR
- total != expected_total

then: `FAIL CLOSED`

No evaluation may start.

---

# 7. PREDICTION ARTIFACT CONTRACT

A complete standard VNEXT evaluation prediction artifact must contain:
- exactly the expected number of rows
- exactly the expected attack population
- exactly the expected benign population
- unique sample IDs
- no missing expected IDs
- no unexpected IDs
- correct run ID
- correct dataset ID
- correct protocol ID

For the standard 61+61 evaluation: `61 attack + 61 benign = 122 rows`

A benign-only artifact is NOT a valid complete Track-A evaluation artifact.

---

# 8. SCORING CONTRACT

ASR must never be calculated if the attack population is incomplete.

Before ASR:
```python
assert observed_attack_count == expected_attack_count
```

If false: `INVALID_INCOMPLETE_EVIDENCE`

Do not:
- estimate missing rows
- substitute another artifact
- silently filter
- silently merge artifacts
- use stale artifacts
- calculate ASR from an undocumented subset

The scorer must identify the exact prediction artifact used.

---

# 9. PROVENANCE CONTRACT

Every new evaluation must create provenance BEFORE execution.

Minimum provenance:
- run_id
- dataset_id
- dataset_sha256
- protocol_id
- protocol_sha256
- code_commit
- target_model
- judge_model
- seed
- created_at
- expected_attack_count
- expected_benign_count

After artifact creation, record:
- predictions_sha256
- metrics_sha256
- manifest_sha256

The manifest must reference the exact prediction artifact.
Metrics must reference the exact prediction artifact.
Cross-run artifact mixing must fail closed.

---

# 10. IMPLEMENTATION POLICY

Before implementing or modifying any evaluation function:
FIRST inspect:
- repository structure
- existing evaluation pipeline
- existing `apply_vnext_adapt`
- data loaders
- protocol definitions
- prediction writers
- scoring functions
- provenance implementation
- existing tests

Do NOT assume the repository matches a hypothetical structure.
Do NOT create duplicate infrastructure if equivalent infrastructure already exists.
Reuse existing abstractions where appropriate.
Make the smallest correct change.

---

# 11. apply_vnext_adapt()

`apply_vnext_adapt()` is **already implemented** through `make_b3_adaptive_v4` (in `src/adapti_guard/experiments/defense_baselines.py`) dispatched by `get_defense_fn("VNEXT-ADAPT")`, and invoked by `run_arm()` in `scripts/run_vnext_confirm.py`. Do not introduce a new or duplicate implementation; reuse the existing factory and runner.

If a separate `apply_vnext_adapt()` entrypoint is ever required:
DO NOT invent the defense algorithm.
Recover its intended behavior from:
- existing implementation
- protocol
- historical code
- existing tests
- documented Track-A design

The function must preserve the evaluation population.
Input: verified evaluation dataframe
Output: prediction artifact containing the expected rows and required metadata.

The function must NOT:
- silently drop attacks
- silently duplicate benign rows
- filter the evaluation population
- change labels
- mix runs
- access external APIs unless the approved evaluation explicitly requires it

---

# 12. TEST-FIRST REQUIREMENT

Before any live evaluation, implement deterministic tests for:

### Test A: 61 attack + 61 benign → PASS
### Test B: 0 attack + 122 benign → FAIL CLOSED
### Test C: 60 attack + 62 benign → FAIL CLOSED
### Test D: 61 attack + 61 benign with duplicate ID → FAIL CLOSED
### Test E: missing expected sample ID → FAIL CLOSED
### Test F: wrong dataset SHA → FAIL CLOSED
### Test G: wrong run ID → FAIL CLOSED
### Test H: metrics reference wrong prediction SHA → FAIL CLOSED
### Test I: complete provenance chain → VERIFIED
### Test J: missing provenance → MISSING_LOCALLY / NOT VERIFIED

Tests must be deterministic and offline.
No LLM required.
No API required.

---

# 13. EXECUTION SAFETY

There are two separate operations:

## IMPLEMENTATION
Allowed after inspection:
- modify non-frozen source code
- add tests
- add validation
- add provenance guards
- update non-historical documentation

## EVALUATION
Separate operation.
A live/new evaluation must NOT automatically execute merely because implementation is complete.
Before execution, show a preflight containing:
- run_id
- dataset
- dataset_sha256
- protocol
- protocol_sha256
- attack_count
- benign_count
- total
- target_model
- judge_model
- seed
- code_commit

If preflight fails: HALT.
If preflight passes: STOP and wait for explicit authorization before the live evaluation unless the user has already explicitly authorized that run.

---

# 14. NO RESULT OPTIMIZATION

Do NOT:
- tune thresholds to improve ASR
- change detector behavior to obtain a pass
- alter scoring to improve metrics
- remove difficult examples
- change labels
- modify the frozen dataset
- cherry-pick favorable outcomes
- report only successful runs

The objective is reproducibility, not a desired result.

---

# 15. HISTORICAL VS NEW RESULTS

Always distinguish:
- `HISTORICAL`
- `NEW_RUN`

Never combine their predictions or metrics.
If a new run differs from the historical result: report both.
Do not delete the historical result.
Do not overwrite it.
Do not call the difference an improvement without scientific justification.

---

# 16. DOCUMENTATION

Maintain one authoritative current status document:
`docs/evidence/TRACK_A_FINAL_STATUS.md`

It must distinguish:

### Historical Result
- B0: `58/61 = 0.9508`
- VNEXT-ADAPT: `53/61 = 0.8689`
- Verdict: `FAIL`

### Historical Artifact Issue
`CONSISTENT` (no mismatch) — see `docs/evidence/TRACK_A_FINAL_STATUS.md`. The VNEXT-ADAPT artifact has 122 rows = 61 attack + 61 benign; the historical ASR is computed from its 61 attack rows.

### Historical Stage-B
`EVIDENCE_NOT_RECOVERABLE`

### New Evaluation
Only document results after a new run actually occurs.
Never document a planned run as completed evidence.

---

# 17. RESPONSE PROTOCOL

For each task use: `[PREFLIGHT]` `[IMPLEMENTATION]` `[VALIDATION]` `[RUN]` `[REPORT]`

Each phase must contain: `status | finding | action`

Examples:
`[PREFLIGHT] PASS | dataset contains 61 attack + 61 benign | implementation may proceed`
`[VALIDATION] FAIL | attack population is 0 | halt`

---

# 18. STOP CONDITIONS

STOP when:
- the requested problem is resolved
- tests pass
- provenance is validated
- documentation reflects the actual state

Do NOT start another audit after resolution.
Do NOT repeat previously completed recovery work.
Do NOT generate redundant reports.
Do NOT proceed to multi-turn evaluation until the single-turn evaluation pipeline is reproducible.

---

# 19. GIT SAFETY

Before modifications:
`git status`
After modifications:
`git diff`
`git status`
Do not commit.
Do not push.
Do not modify unrelated work.

---

# 20. FINAL PRINCIPLE

Evidence first.
Code second.
Evaluation third.
Claims last.
Never reverse this order.
