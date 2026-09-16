"""P3 offline artifact verifier — fail closed."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from adapti_guard.detectors.base import (
    FORBIDDEN_INPUT_KEYS,
    P1_SHA256,
    P2_SHA256,
    assert_unique_ids,
)
from adapti_guard.detectors.protocol import ACTION_COSTS, CANONICAL_EXECUTION_STATES

REQUIRED_ARTIFACT_FILES = (
    "manifest.json",
    "turn_observations.jsonl",
    "policy_schedule.jsonl",
    "metrics.json",
    "reproducibility.json",
)

REQUIRED_MANIFEST_KEYS = {
    "run_id",
    "pack",
    "benchmark_sha256",
    "detectors",
    "policy_ids",
    "action_costs",
    "live_execution_authorized",
}

REQUIRED_TURN_KEYS = {
    "evaluation_id",
    "trajectory_id",
    "detector_id",
    "turn_id",
    "result",
    "evaluation_hash",
}

REQUIRED_RESULT_KEYS = {
    "detector_id",
    "detector_hit",
    "risk_signal",
    "evidence",
    "reason_code",
    "input_scope",
    "version",
}

OPERATIONAL_DETECTOR_IDS = frozenset({"D0", "D1", "D2", "D4"})


class P3ArtifactVerificationError(ValueError):
    """Fail-closed verification failure."""


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def _require_keys(obj: Mapping[str, Any], keys: set[str], *, where: str) -> None:
    missing = sorted(keys - set(obj.keys()))
    if missing:
        raise P3ArtifactVerificationError(f"{where} missing keys: {missing}")


def _scan_forbidden(obj: Any, *, path: str = "") -> None:
    if isinstance(obj, Mapping):
        bad = sorted(set(obj.keys()) & FORBIDDEN_INPUT_KEYS)
        if bad:
            raise P3ArtifactVerificationError(
                f"future/leakage keys present at {path or '/'}: {bad}"
            )
        for k, v in obj.items():
            _scan_forbidden(v, path=f"{path}.{k}" if path else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _scan_forbidden(v, path=f"{path}[{i}]")


def verify_p3_artifact_dir(path: Path | str) -> dict[str, Any]:
    """Verify a P3 offline artifact directory. Raises on any failure."""
    root = Path(path)
    if not root.is_dir():
        raise P3ArtifactVerificationError(f"artifact dir missing: {root}")

    missing_files = [f for f in REQUIRED_ARTIFACT_FILES if not (root / f).is_file()]
    if missing_files:
        raise P3ArtifactVerificationError(f"required files missing: {missing_files}")

    manifest = _load_json(root / "manifest.json")
    if not isinstance(manifest, Mapping):
        raise P3ArtifactVerificationError("manifest.json must be an object")
    _require_keys(manifest, REQUIRED_MANIFEST_KEYS, where="manifest")

    if manifest.get("live_execution_authorized") is not False:
        raise P3ArtifactVerificationError("live_execution_authorized must be false for offline")

    costs = manifest.get("action_costs")
    if dict(costs) != dict(ACTION_COSTS):
        raise P3ArtifactVerificationError(
            f"action_costs mutated: {costs} != {ACTION_COSTS}"
        )

    pack = str(manifest.get("pack") or "").upper()
    sha = str(manifest.get("benchmark_sha256") or "")
    if pack == "P1" and sha != P1_SHA256:
        raise P3ArtifactVerificationError(f"P1 SHA mismatch in manifest: {sha}")
    if pack == "P2" and sha != P2_SHA256:
        raise P3ArtifactVerificationError(f"P2 SHA mismatch in manifest: {sha}")
    if pack not in {"P1", "P2"}:
        raise P3ArtifactVerificationError(f"unknown pack: {pack}")

    turns = _load_jsonl(root / "turn_observations.jsonl")
    policies = _load_jsonl(root / "policy_schedule.jsonl")
    metrics = _load_json(root / "metrics.json")
    repro = _load_json(root / "reproducibility.json")

    if not isinstance(metrics, Mapping):
        raise P3ArtifactVerificationError("metrics.json must be an object")
    if not isinstance(repro, Mapping) or "reproducibility_hash" not in repro:
        raise P3ArtifactVerificationError("reproducibility.json missing reproducibility_hash")

    turn_eval_ids: list[str] = []
    episode_det: list[str] = []
    for i, row in enumerate(turns):
        _require_keys(row, REQUIRED_TURN_KEYS, where=f"turn_observations[{i}]")
        _require_keys(row["result"], REQUIRED_RESULT_KEYS, where=f"turn_observations[{i}].result")
        did = str(row["detector_id"])
        if did not in OPERATIONAL_DETECTOR_IDS:
            raise P3ArtifactVerificationError(f"unknown/deferred detector in turns: {did}")
        if did != str(row["result"].get("detector_id")):
            raise P3ArtifactVerificationError("result.detector_id mismatch")
        turn_eval_ids.append(str(row["evaluation_id"]))
        episode_det.append(f"{row['trajectory_id']}::{row['detector_id']}::t{row['turn_id']}")
        _scan_forbidden(row.get("result") or {}, path=f"turn[{i}].result")
        # Ensure no future-turn references smuggled into result metadata
        meta = (row.get("result") or {}).get("metadata") or {}
        _scan_forbidden(meta, path=f"turn[{i}].metadata")

    try:
        assert_unique_ids(turn_eval_ids, what="turn evaluation_id")
        assert_unique_ids(episode_det, what="trajectory×detector×turn")
    except ValueError as e:
        raise P3ArtifactVerificationError(str(e)) from e

    policy_eval_ids: list[str] = []
    ep_det_pol: list[str] = []
    for i, row in enumerate(policies):
        for k in ("evaluation_id", "trajectory_id", "detector_id", "policy_id"):
            if k not in row:
                raise P3ArtifactVerificationError(f"policy_schedule[{i}] missing {k}")
        did = str(row["detector_id"])
        if did not in OPERATIONAL_DETECTOR_IDS:
            raise P3ArtifactVerificationError(f"unknown detector in policy schedule: {did}")
        if str(row.get("policy_id") or "") not in set(manifest.get("policy_ids") or []):
            raise P3ArtifactVerificationError(
                f"policy_id {row.get('policy_id')} not in manifest.policy_ids"
            )
        policy_eval_ids.append(str(row["evaluation_id"]))
        ep_det_pol.append(
            f"{row['trajectory_id']}::{row['detector_id']}::{row['policy_id']}"
        )

    try:
        assert_unique_ids(policy_eval_ids, what="policy evaluation_id")
        assert_unique_ids(ep_det_pol, what="trajectory×detector×policy")
    except ValueError as e:
        raise P3ArtifactVerificationError(str(e)) from e

    # Metric denominators non-negative / coherent when present
    det_metrics = metrics.get("detector_level_metrics") or {}
    if not isinstance(det_metrics, Mapping):
        raise P3ArtifactVerificationError("detector_level_metrics must be an object")
    for did, block in det_metrics.items():
        if did not in OPERATIONAL_DETECTOR_IDS:
            raise P3ArtifactVerificationError(f"metrics for unknown detector {did}")
        for key in ("attack_detection_rate", "benign_FPR", "hard_negative_FPR"):
            rate = (block or {}).get(key) or {}
            num = int(rate.get("numerator") or 0)
            den = int(rate.get("denominator") or 0)
            if num < 0 or den < 0 or num > den:
                raise P3ArtifactVerificationError(
                    f"invalid metric denominator for {did}.{key}: {num}/{den}"
                )

    # Optional event-state validation if present in metrics / extras
    for state in (metrics.get("observed_execution_states") or []):
        if str(state) not in CANONICAL_EXECUTION_STATES and str(state) != "NO_TOOL_REQUESTED":
            raise P3ArtifactVerificationError(f"invalid execution state: {state}")

    return {
        "ok": True,
        "path": str(root),
        "run_id": manifest.get("run_id"),
        "pack": pack,
        "benchmark_sha256": sha,
        "n_turn_observations": len(turns),
        "n_policy_arms": len(policies),
        "reproducibility_hash": repro.get("reproducibility_hash"),
        "detector_ids": sorted(OPERATIONAL_DETECTOR_IDS),
    }


def verify_no_overwrite(path: Path | str) -> None:
    """Fail if target output dir already has artifacts (caller should use empty dir)."""
    root = Path(path)
    if root.exists() and any(root.iterdir()):
        raise P3ArtifactVerificationError(
            f"overwrite protection: non-empty output dir {root}"
        )
