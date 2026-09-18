"""Offline validation for P3 Stage-C Q1 protocol (no API/network/LLM)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from adapti_guard.experiments.p3_stage_c_q1 import (
    EXPECTED_N_ARMS_STAGE_B,
    PRIMARY_POLICY_STRATUM,
    QUESTION_ID,
    STAGE_B_DIR,
    assert_locks_match_stage_b_manifest,
    build_q1_protocol,
    delta_vs_d0,
    pairing_key,
    run_offline_validation,
    sign_agreement,
    sign_delta,
    write_q1_artifacts,
)
from adapti_guard.experiments.security_event_id import (
    EVENT_ID_SCHEMA_SCOPED_REP,
    event_id_schema_for,
    make_security_event_id,
)

ROOT = Path(__file__).resolve().parents[1]
P1 = ROOT / "datasets" / "frozen" / "p1_mechanism_v1.0.0" / "dataset.jsonl"
P2 = ROOT / "datasets" / "frozen" / "p2_agentic_v0.1.0" / "dataset.jsonl"


def test_protocol_schema_complete():
    p = build_q1_protocol()
    assert p["question_id"] == QUESTION_ID
    assert p["factor"] == "repetition_id"
    assert p["changed_factor"] == {"repetition_id": ["R1", "R2"]}
    assert p["live_execution_allowed"] is False
    assert p["arms"]["r2_n"] == EXPECTED_N_ARMS_STAGE_B == 432
    assert p["primary_endpoint"]["primary_policy_stratum"] == PRIMARY_POLICY_STRATUM
    assert p["primary_endpoint"]["not_raw_hasr_alone"] is True


@pytest.mark.stage_b
@pytest.mark.skipif(not STAGE_B_DIR.is_dir(), reason="Stage-B raw traces not present locally (MISSING_LOCALLY)")
def test_locks_match_stage_b():
    assert_locks_match_stage_b_manifest()


def test_sign_zero_treatment():
    assert sign_delta(0.0) == "ZERO"
    assert sign_delta(0.1) == "POS"
    assert sign_delta(-0.05) == "NEG"
    assert sign_agreement(0.0, 0.0) is True
    assert sign_agreement(0.1, 0.2) is True
    assert sign_agreement(-0.1, -0.01) is True
    assert sign_agreement(0.1, -0.1) is False
    assert sign_agreement(0.0, 0.1) is False


def test_event_id_v3_includes_repetition():
    eid = make_security_event_id(
        "p2a_atk_001",
        3,
        "create_record",
        "invalid_tool_arguments",
        detector_id="D2",
        policy_id="PHASE1-CORE",
        repetition_id="R2",
    )
    assert "R2" in eid
    assert event_id_schema_for(
        detector_id="D2", policy_id="PHASE1-CORE", repetition_id="R2"
    ) == EVENT_ID_SCHEMA_SCOPED_REP
    other = make_security_event_id(
        "p2a_atk_001",
        3,
        "create_record",
        "invalid_tool_arguments",
        detector_id="D2",
        policy_id="PHASE1-CORE",
        repetition_id="R1",
    )
    assert eid != other


def test_pairing_key_excludes_run():
    assert pairing_key("t", "D0", "B0") == "t::D0::B0"


@pytest.mark.skipif(not STAGE_B_DIR.is_dir(), reason="Stage-B absent")
def test_delta_on_r1_attack_denom_16():
    rows = [
        json.loads(line)
        for line in (STAGE_B_DIR / "predictions.jsonl").read_text().splitlines()
        if line.strip()
    ]
    cell = delta_vs_d0(rows, detector_id="D1", policy_id="PHASE1-CORE")
    assert cell["tool_hasr_d"]["n_attack"] == 16
    assert cell["delta"] is not None


@pytest.mark.skipif(not STAGE_B_DIR.is_dir(), reason="Stage-B absent")
def test_stage_b_metrics_and_frozen_sha_untouched():
    m = json.loads((STAGE_B_DIR / "metrics.json").read_text())
    assert m["Tool-HASR"]["n_success"] == 124
    assert m["Judge-ASR"]["n_success"] == 163
    assert m["M3"] == 61
    assert m["M4"] == 22
    assert m["invalid_tool_args_count"] == 231
    assert hashlib.sha256(P1.read_bytes()).hexdigest().startswith("1a0b0053")
    assert hashlib.sha256(P2.read_bytes()).hexdigest().startswith("32b40e3b")


def test_invalid_args_not_hasr_failure_in_policy():
    p = build_q1_protocol()
    assert p["invalid_tool_args_policy"]["counts_as_tool_hasr_failure"] is False
    assert len(p["invalid_tool_args_policy"]["sensitivity_analyses_preregistered"]) >= 3


@pytest.mark.stage_b
@pytest.mark.skipif(not STAGE_B_DIR.is_dir(), reason="Stage-B raw traces not present locally (MISSING_LOCALLY)")
def test_full_offline_validation_gate_ready():
    report = run_offline_validation()
    assert report["gate_status"] == "P3_STAGE_C_Q1_GATE_READY"
    assert report["api_calls"] == 0
    assert report["live_execution_allowed"] is False
    assert report["blockers"] == []


@pytest.mark.stage_b
@pytest.mark.skipif(not STAGE_B_DIR.is_dir(), reason="Stage-B raw traces not present locally (MISSING_LOCALLY)")
def test_write_artifacts(tmp_path, monkeypatch):
    # write_q1_artifacts uses fixed /opt/cursor/artifacts — call real path once in gate run
    paths = write_q1_artifacts()
    for p in paths.values():
        assert Path(p).is_file()
