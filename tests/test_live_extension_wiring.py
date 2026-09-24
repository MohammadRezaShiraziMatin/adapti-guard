"""Phase 7 pre-flight wiring (no live API)."""
import json
from pathlib import Path

import pytest

from adapti_guard.evaluation.live_extension_wiring import (
    LiveExtensionBlockedError,
    authorization_allows_live_spend,
    plan_live_execution,
    resolve_offline_path,
    run_live_condition,
)


def test_offline_path_for_e1():
    assert resolve_offline_path("COND-E1-STATEFUL-OFFLINE") == "offline"


def test_live_plan_blocked_without_auth():
    with pytest.raises(LiveExtensionBlockedError):
        plan_live_execution("COND-E1-STATEFUL-OFFLINE")


def test_wiring_covers_extension_conditions():
    for cid in (
        "COND-E1-STATEFUL-OFFLINE",
        "COND-E2-ADAPTIVE-OFFLINE",
        "COND-E3-AGENT-OFFLINE",
        "COND-EXT6-BASELINE",
        "COND-PHASE7-CAMPAIGN",
    ):
        with pytest.raises(LiveExtensionBlockedError):
            plan_live_execution(cid)


def test_authorization_blocks_live_spend():
    ok, _ = authorization_allows_live_spend()
    assert not ok


def test_live_mode_blocked_without_authorization(tmp_path: Path):
    with pytest.raises(LiveExtensionBlockedError):
        run_live_condition(
            "COND-E1-STATEFUL-OFFLINE",
            run_id="blocked-run",
            run_dir=tmp_path,
            execution_mode="LIVE",
        )


def test_offline_mock_stateful_canonical_runner(tmp_path: Path):
    result = run_live_condition(
        "COND-E1-STATEFUL-OFFLINE",
        run_id="mock-run",
        run_dir=tmp_path,
        execution_mode="OFFLINE_MOCK",
        turn_messages=["hello", "follow-up"],
    )
    assert result.status == "ok"
    raw = json.loads((tmp_path / "raw" / "episode_raw.json").read_text())
    assert raw["turn_count"] == 2
    assert Path(result.trace_path).is_file()
    assert Path(result.derived_metrics_path).is_file()
    assert (tmp_path / "raw" / "episode_raw.json").exists()


def test_offline_mock_adaptive_feedback(tmp_path: Path):
    result = run_live_condition(
        "COND-E2-ADAPTIVE-OFFLINE",
        run_id="adapt-mock",
        run_dir=tmp_path,
        execution_mode="OFFLINE_MOCK",
    )
    assert result.execution_mode == "OFFLINE_MOCK"
    raw = json.loads((tmp_path / "raw" / "episode_raw.json").read_text())
    assert raw["episode_type"] == "adaptive"
