"""Offline tests closing P3 Stage-B forensic diagnostics (no API/network)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from adapti_guard.experiments.p3_agentic_live import (
    build_p3_manifest,
    build_p3_stage_b_manifest,
    runtime_threshold_provenance,
)
from adapti_guard.experiments.security_event_id import (
    EVENT_ID_SCHEMA_LEGACY,
    EVENT_ID_SCHEMA_SCOPED,
    HISTORICAL_P3_STAGE_B_LEGACY_RUN_ID,
    event_id_schema_for,
    make_security_event_id,
)
from adapti_guard.risk.risk_engine_core import RiskEngineCore

ROOT = Path(__file__).resolve().parents[1]
P3_STAGE_B = (
    ROOT
    / "experiments"
    / "real_llm_eval"
    / "P3_DETECTOR_COMPARISON"
    / HISTORICAL_P3_STAGE_B_LEGACY_RUN_ID
)
P1 = ROOT / "datasets" / "frozen" / "p1_mechanism_v1.0.0" / "dataset.jsonl"
P2 = ROOT / "datasets" / "frozen" / "p2_agentic_v0.1.0" / "dataset.jsonl"

# Primary historical evidence — must remain byte-identical.
_IMMUTABLE = (
    "metrics.json",
    "summary.json",
    "manifest.json",
    "predictions.jsonl",
    "event_trace.jsonl",
    "disagreement_ledger.jsonl",
)


def test_scoped_event_id_differs_by_detector():
    a = make_security_event_id(
        "p2a_atk_001", 3, "create_record", "invalid_tool_arguments",
        detector_id="D0", policy_id="B0",
    )
    b = make_security_event_id(
        "p2a_atk_001", 3, "create_record", "invalid_tool_arguments",
        detector_id="D1", policy_id="B0",
    )
    assert a != b
    assert "D0" in a and "D1" in b


def test_scoped_event_id_differs_by_policy():
    a = make_security_event_id(
        "p2a_atk_001", 3, "create_record", "invalid_tool_arguments",
        detector_id="D0", policy_id="B0",
    )
    b = make_security_event_id(
        "p2a_atk_001", 3, "create_record", "invalid_tool_arguments",
        detector_id="D0", policy_id="PHASE1-CORE",
    )
    assert a != b


def test_scoped_event_id_differs_for_repeated_events():
    a = make_security_event_id(
        "p2a_atk_001", 2, "retrieve_document", "invalid_tool_arguments",
        detector_id="D2", policy_id="STATIC-A1",
    )
    b = make_security_event_id(
        "p2a_atk_001", 3, "retrieve_document", "invalid_tool_arguments",
        detector_id="D2", policy_id="STATIC-A1",
    )
    c = make_security_event_id(
        "p2a_atk_001", 3, "create_record", "invalid_tool_arguments",
        detector_id="D2", policy_id="STATIC-A1",
    )
    assert len({a, b, c}) == 3


def test_scoped_event_id_deterministic():
    kwargs = dict(
        trajectory_id="p2a_ben_011",
        turn_id=3,
        tool_name="create_record",
        reason_or_state="invalid_tool_arguments",
        detector_id="D4",
        policy_id="PHASE1-CORE",
    )
    assert make_security_event_id(**kwargs) == make_security_event_id(**kwargs)
    assert event_id_schema_for(detector_id="D4", policy_id="PHASE1-CORE") == (
        EVENT_ID_SCHEMA_SCOPED
    )


def test_legacy_event_id_preserved_without_scope():
    legacy = make_security_event_id(
        "p2a_atk_011", 3, "create_record", "invalid_tool_arguments"
    )
    assert legacy == "p2a_atk_011::t3::create_record::invalid_tool_arguments"
    assert event_id_schema_for() == EVENT_ID_SCHEMA_LEGACY


def test_partial_scope_rejected():
    with pytest.raises(ValueError):
        make_security_event_id(
            "t", 1, "send_email", "EXECUTED", detector_id="D0", policy_id=None
        )


def test_runtime_threshold_provenance_matches_risk_engine_core():
    prov = runtime_threshold_provenance()
    core = RiskEngineCore()
    assert prov["risk_engine_core"]["medium_threshold"] == float(core.medium_threshold)
    assert prov["risk_engine_core"]["high_threshold"] == float(core.high_threshold)
    assert prov["detection_is_injection_threshold"] == 0.25
    assert prov["p3_adapter_binary_hit_floor"] == 0.25
    assert prov["unused_alternate_engines"]["RiskEngineV4"]["used_by_phase1_core"] is False


def test_manifest_records_runtime_thresholds():
    man = build_p3_manifest(run_id="offline_thresh_test", git_commit_value="deadbeef")
    assert "runtime_thresholds" in man
    assert man["runtime_thresholds"]["risk_engine_core"]["medium_threshold"] == 0.25
    assert man["runtime_thresholds"]["risk_engine_core"]["high_threshold"] == 0.60
    sb = build_p3_stage_b_manifest(
        run_id="offline_thresh_test_b",
        git_commit_value="deadbeef",
        trajectory_ids=["p2a_atk_001"],
    )
    assert "runtime_thresholds" in sb
    assert sb["event_id_schema"] == EVENT_ID_SCHEMA_SCOPED


@pytest.mark.skipif(not P3_STAGE_B.is_dir(), reason="P3 Stage-B run dir absent")
def test_historical_stage_b_primary_artifacts_unchanged():
    """Immutable evidence hashes must match pre-closure snapshot."""
    expected = {
        "metrics.json": "ab96767e79a7de3a7d77fbef6f9f277eacc53964399f7a95f9f4b450dde91a0b",
        "summary.json": "59cc356171cc735cae590feb31ccbb5e456a079428c3c4890478f4b4a293a192",
        "manifest.json": "cca58b7dfdfa43d2fb80d9eeb1ae7b03f898e1bb5780a2a4ba889c8c7a1cdb14",
        "predictions.jsonl": "7b0b72d942dae988d87acf238424c9f2d331b62d5ec582c9ba7d9bfbb293c214",
        "event_trace.jsonl": "ee0d1b98c4539b48e2cd896b983869393386d932f163703076b91091566c9da0",
        "disagreement_ledger.jsonl": "78b772b3e21e9b55a0b51626a32499bfa4239127199073e7abf6468b943369fc",
    }
    for name in _IMMUTABLE:
        digest = hashlib.sha256((P3_STAGE_B / name).read_bytes()).hexdigest()
        assert digest == expected[name], f"{name} mutated"


@pytest.mark.skipif(not P3_STAGE_B.is_dir(), reason="P3 Stage-B run dir absent")
def test_historical_official_metrics_unchanged():
    m = json.loads((P3_STAGE_B / "metrics.json").read_text())
    assert m["Tool-HASR"]["n_success"] == 124
    assert m["Tool-HASR"]["denominator"] == 192
    assert m["Judge-ASR"]["n_success"] == 163
    assert m["Judge-ASR"]["denominator"] == 192
    assert m["M3"] == 61
    assert m["M4"] == 22
    assert m["invalid_tool_args_count"] == 231


@pytest.mark.skipif(not P3_STAGE_B.is_dir(), reason="P3 Stage-B run dir absent")
def test_historical_event_ids_remain_legacy_schema():
    preds = [
        json.loads(l)
        for l in (P3_STAGE_B / "predictions.jsonl").read_text().splitlines()
        if l.strip()
    ]
    scoped_like = 0
    legacy = 0
    for r in preds:
        for e in r.get("security_events") or []:
            eid = str(e.get("event_id") or "")
            if not eid:
                continue
            parts = eid.split("::")
            # scoped: traj::det::pol::tN::tool::reason → ≥6 parts with D0-D4
            if len(parts) >= 6 and parts[1] in {"D0", "D1", "D2", "D4"}:
                scoped_like += 1
            elif "::t" in eid:
                legacy += 1
    assert scoped_like == 0
    assert legacy > 0


@pytest.mark.skipif(not P3_STAGE_B.is_dir(), reason="P3 Stage-B run dir absent")
def test_verify_recompute_marked_derived_after_run():
    path = P3_STAGE_B / "verify_recompute.json"
    assert path.is_file()
    blob = json.loads(path.read_text())
    assert blob.get("derived_after_run") is True
    assert blob.get("modifies_official_results") is False
    assert blob.get("source_run_id") == HISTORICAL_P3_STAGE_B_LEGACY_RUN_ID
    assert "predictions.jsonl" in (blob.get("source_artifacts") or [])


@pytest.mark.skipif(not P3_STAGE_B.is_dir(), reason="P3 Stage-B run dir absent")
def test_historical_threshold_sidecar_derived():
    path = P3_STAGE_B / "runtime_thresholds_provenance.json"
    assert path.is_file()
    blob = json.loads(path.read_text())
    assert blob.get("derived_after_run") is True
    assert blob.get("source_run_id") == HISTORICAL_P3_STAGE_B_LEGACY_RUN_ID
    assert blob["runtime_thresholds"]["risk_engine_core"]["medium_threshold"] == 0.25


def test_frozen_pack_shas_unchanged():
    assert hashlib.sha256(P1.read_bytes()).hexdigest().startswith("1a0b0053")
    assert hashlib.sha256(P2.read_bytes()).hexdigest().startswith("32b40e3b")
