"""P3 offline artifact verifier tests — fail closed."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from adapti_guard.detectors.base import P1_SHA256
from adapti_guard.detectors.harness import OfflineDetectorHarness
from adapti_guard.detectors.protocol import ACTION_COSTS
from adapti_guard.detectors.verifier import (
    P3ArtifactVerificationError,
    verify_no_overwrite,
    verify_p3_artifact_dir,
)


@pytest.fixture
def valid_artifact(tmp_path: Path) -> Path:
    out = tmp_path / "valid_p3"
    OfflineDetectorHarness(run_id="verify_ok").run_pack(
        pack="P1", output_dir=out, max_trajectories=3
    )
    return out


def test_verifier_accepts_valid_artifact(valid_artifact: Path):
    result = verify_p3_artifact_dir(valid_artifact)
    assert result["ok"] is True
    assert result["benchmark_sha256"] == P1_SHA256


def test_verifier_rejects_missing_file(valid_artifact: Path):
    (valid_artifact / "metrics.json").unlink()
    with pytest.raises(P3ArtifactVerificationError, match="required files missing"):
        verify_p3_artifact_dir(valid_artifact)


def test_verifier_rejects_duplicate_evaluation_ids(valid_artifact: Path):
    path = valid_artifact / "turn_observations.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(lines[0] + "\n" + lines[0] + "\n", encoding="utf-8")
    with pytest.raises(P3ArtifactVerificationError, match="duplicate"):
        verify_p3_artifact_dir(valid_artifact)


def test_verifier_rejects_sha_mismatch(valid_artifact: Path):
    man = json.loads((valid_artifact / "manifest.json").read_text(encoding="utf-8"))
    man["benchmark_sha256"] = "0" * 64
    (valid_artifact / "manifest.json").write_text(json.dumps(man), encoding="utf-8")
    with pytest.raises(P3ArtifactVerificationError, match="SHA mismatch"):
        verify_p3_artifact_dir(valid_artifact)


def test_verifier_rejects_cost_mutation(valid_artifact: Path):
    man = json.loads((valid_artifact / "manifest.json").read_text(encoding="utf-8"))
    man["action_costs"] = {**ACTION_COSTS, "A3": 0.99}
    (valid_artifact / "manifest.json").write_text(json.dumps(man), encoding="utf-8")
    with pytest.raises(P3ArtifactVerificationError, match="action_costs"):
        verify_p3_artifact_dir(valid_artifact)


def test_verifier_rejects_live_flag(valid_artifact: Path):
    man = json.loads((valid_artifact / "manifest.json").read_text(encoding="utf-8"))
    man["live_execution_authorized"] = True
    (valid_artifact / "manifest.json").write_text(json.dumps(man), encoding="utf-8")
    with pytest.raises(P3ArtifactVerificationError, match="live_execution_authorized"):
        verify_p3_artifact_dir(valid_artifact)


def test_verifier_rejects_unknown_detector(valid_artifact: Path):
    path = valid_artifact / "turn_observations.jsonl"
    row = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    row["detector_id"] = "D3"
    row["result"]["detector_id"] = "D3"
    row["evaluation_id"] = (
        row["evaluation_id"]
        .replace("::D0::", "::D3::")
        .replace("::D1::", "::D3::")
        .replace("::D2::", "::D3::")
        .replace("::D4::", "::D3::")
    )
    # force
    parts = row["evaluation_id"].split("::")
    if len(parts) >= 3:
        parts[2] = "D3"
        row["evaluation_id"] = "::".join(parts)
    path.write_text(json.dumps(row) + "\n", encoding="utf-8")
    with pytest.raises(P3ArtifactVerificationError, match="unknown|deferred"):
        verify_p3_artifact_dir(valid_artifact)


def test_overwrite_protection(tmp_path: Path):
    d = tmp_path / "occ"
    d.mkdir()
    (d / "x").write_text("1", encoding="utf-8")
    with pytest.raises(P3ArtifactVerificationError, match="overwrite"):
        verify_no_overwrite(d)
    empty = tmp_path / "empty"
    empty.mkdir()
    verify_no_overwrite(empty)
