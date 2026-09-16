"""Offline gates for P3 Stage-A live harness (no API)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from adapti_guard.detectors.core_adapter import P3CoreDetectorAdapter
from adapti_guard.detectors import default_p3_detectors
from adapti_guard.experiments.p3_agentic_live import (
    EXPECTED_N_ARMS,
    OPERATIONAL_DETECTORS,
    P3_SMOKE_TRAJECTORY_IDS,
    get_p3_defense_fn,
    preflight_p3,
    stage_a_cartesian_schedule,
    verify_frozen_integrity,
)

ROOT = Path(__file__).resolve().parents[1]


def test_frozen_integrity():
    info = verify_frozen_integrity()
    assert info["p1_sha256"].startswith("1a0b0053")
    assert info["p2_sha256"].startswith("32b40e3b")


def test_cartesian_60_arms():
    arms = stage_a_cartesian_schedule()
    assert len(arms) == EXPECTED_N_ARMS == 60
    assert len({a for a in arms}) == 60


def test_d3_not_operational():
    assert "D3" not in default_p3_detectors()
    assert set(OPERATIONAL_DETECTORS) == {"D0", "D1", "D2", "D4"}


def test_core_adapter_floors_binary_hit():
    from adapti_guard.detectors.base import DetectorResult, EpisodeDetectionContext
    from adapti_guard.detectors.no_detection import NoDetectionDetector

    class HitLow(NoDetectionDetector):
        detector_id = "DX"

        def detect(self, ctx: EpisodeDetectionContext) -> DetectorResult:
            return DetectorResult(
                detector_id="DX",
                detector_hit=True,
                risk_signal=0.1,
                evidence=("x",),
                reason_code="hit",
                version="t",
            )

    ad = P3CoreDetectorAdapter(HitLow())
    r = ad.detect_episode("hi")
    assert r.is_injection is True
    assert r.injection_probability >= 0.25


def test_defense_fn_builds_for_all_policies():
    for did in OPERATIONAL_DETECTORS:
        for pid in ("B0", "STATIC-A1", "PHASE1-CORE"):
            fn, _st = get_p3_defense_fn(pid, did)
            action, blocked, text = fn("hello", None)
            assert action in {"A0", "A1", "A2", "A3"}


def test_cli_default_no_live():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "run_p3_live_stage_a.py")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0
    assert "STATUS=NO_LIVE_EXECUTION" in proc.stdout


def test_cli_stage_a_requires_approval():
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "run_p3_live_stage_a.py"),
            "--stage-a",
            "--smoke",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 2
    assert "STOP_STAGE_A_REQUIRES_APPROVAL" in proc.stdout


def test_smoke_ids_count():
    assert len(P3_SMOKE_TRAJECTORY_IDS) == 5
