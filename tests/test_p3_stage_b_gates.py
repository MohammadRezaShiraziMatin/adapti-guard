"""Offline gates for P3 Stage-B live harness (no API)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from adapti_guard.experiments.p2_agentic_live import load_p2_pack
from adapti_guard.experiments.p3_agentic_live import (
    EXPECTED_N_ARMS_STAGE_B,
    OPERATIONAL_DETECTORS,
    PRIMARY_POLICIES,
    P3LiveGateError,
    arm_level_disagreements,
    assert_p2_pack_composition,
    refuse_live_stage_b_without_approval,
    stage_b_cartesian_schedule,
    write_p3_stage_b_artifact_bundle,
)

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_p3_live_stage_a.py"


def test_stage_b_pack_composition():
    rows = load_p2_pack()
    inv = assert_p2_pack_composition(rows)
    assert inv["n_total"] == 36
    assert inv["n_attack"] == 16
    assert inv["n_benign_twin"] == 16
    assert inv["n_hard_negative"] == 4


def test_stage_b_cartesian_432():
    rows = load_p2_pack()
    arms = stage_b_cartesian_schedule(rows)
    assert len(arms) == EXPECTED_N_ARMS_STAGE_B == 432
    assert len(set(arms)) == 432
    assert {a[1] for a in arms} == set(OPERATIONAL_DETECTORS)
    assert {a[2] for a in arms} == set(PRIMARY_POLICIES)
    assert "D3" not in {a[1] for a in arms}


def test_refuse_stage_b_without_approval():
    with pytest.raises(P3LiveGateError) as exc:
        refuse_live_stage_b_without_approval(approve_stage_b=False)
    assert exc.value.code == "STOP_STAGE_B_REQUIRES_HUMAN_APPROVAL"
    refuse_live_stage_b_without_approval(approve_stage_b=True)


def test_cli_stage_b_requires_approval():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--stage-b"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 2
    assert "STOP_STAGE_B_REQUIRES_HUMAN_APPROVAL" in proc.stdout


def test_cli_mutual_exclusion():
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--stage-a",
            "--smoke",
            "--approve-stage-a",
            "--stage-b",
            "--approve-stage-b",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 2
    assert "STOP_MUTUAL_EXCLUSION" in proc.stdout


def test_arm_level_m3_m4_not_collapsed():
    rows = [
        {
            "evaluation_id": "r::atk::D0::B0",
            "id": "atk",
            "trajectory_id": "atk",
            "label": "attack",
            "detector_id": "D0",
            "policy_key": "B0",
            "tool_hasr_success": False,
            "judge_asr_success": True,
        },
        {
            "evaluation_id": "r::atk::D1::B0",
            "id": "atk",
            "trajectory_id": "atk",
            "label": "attack",
            "detector_id": "D1",
            "policy_key": "B0",
            "tool_hasr_success": False,
            "judge_asr_success": True,
        },
    ]
    d = arm_level_disagreements(rows)
    assert len(d) == 2
    assert all(x["pattern"].startswith("M3") for x in d)


def test_score_rejects_wrong_arm_count(tmp_path: Path):
    stub = {
        "evaluation_id": "only-one",
        "id": "x",
        "trajectory_id": "x",
        "label": "benign",
        "hard_negative": False,
        "detector_id": "D0",
        "policy_key": "B0",
        "tool_hasr_success": None,
        "judge_asr_success": None,
        "security_events": [],
        "final_action": "A0",
    }
    with pytest.raises(P3LiveGateError) as exc:
        write_p3_stage_b_artifact_bundle(
            tmp_path / "bundle",
            run_id="t",
            predictions=[stub],
            manifest={"git_commit": "deadbeef", "scientific_evidence": False},
        )
    assert exc.value.code == "STOP_STAGE_B_ARM_COUNT"


def test_invalid_args_method_canonical():
    """Scoring must expose per-arm event_id dedup method (not notes)."""
    # Minimal valid-shaped attack/benign stubs — score_p3_stage_b needs 432
    # so only check helper path via score_p3_results expected method constant.
    from adapti_guard.experiments.p3_agentic_live import _count_invalid_tool_args_canonical

    row = {
        "security_events": [
            {
                "event_id": "atk::t3::create_record::invalid",
                "primary_execution_state": "INVALID_TOOL_ARGS",
                "reason": "invalid_tool_arguments",
            },
            {
                "event_id": "atk::t3::create_record::invalid",
                "primary_execution_state": "INVALID_TOOL_ARGS",
                "reason": "invalid_tool_arguments",
            },
        ]
    }
    assert _count_invalid_tool_args_canonical([row]) == 1
