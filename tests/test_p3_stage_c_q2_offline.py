"""Offline validation for P3 Stage-C Q2 protocol (no API/network/LLM)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from adapti_guard.experiments.p3_stage_c_q1 import (
    QUESTION_ID as Q1_QUESTION_ID,
    build_q1_protocol,
)
from adapti_guard.experiments.p3_stage_c_q2 import (
    PRIMARY_POLICY_STRATUM,
    QUESTION_ID,
    STAGE_B_DIR,
    STAGE_B_RUN_ID,
    assert_stage_b_immutable,
    build_q2_protocol,
    build_target_lock_manifest,
    contrast_change,
    design_schedules,
    evaluation_id_q2,
    pairing_key,
    q2_event_scope_token,
    run_offline_validation,
    sign_agreement,
    sign_delta,
    write_q2_artifacts,
)
from adapti_guard.experiments.security_event_id import make_security_event_id

ROOT = Path(__file__).resolve().parents[1]
P1 = ROOT / "datasets" / "frozen" / "p1_mechanism_v1.0.0" / "dataset.jsonl"
P2 = ROOT / "datasets" / "frozen" / "p2_agentic_v0.1.0" / "dataset.jsonl"


def test_protocol_schema_and_factor():
    p = build_q2_protocol()
    assert p["question_id"] == QUESTION_ID == "RQ-C2"
    assert p["factor"] == "target_model_id"
    assert p["changed_factor"] == {"target_model_id": ["T0", "T1", "T2", "T3"]}
    assert p["live_execution_allowed"] is False
    assert p["live_execution"] == "BLOCKED_UNTIL_EXPLICIT_HUMAN_APPROVAL"
    assert p["primary_endpoint"]["primary_policy_stratum"] == PRIMARY_POLICY_STRATUM
    assert p["primary_endpoint"]["not_raw_detector_performance"] is True
    assert p["primary_endpoint"]["not_detector_ranking"] is True
    assert p["q1_separation"]["separate_studies"] is True
    assert p["q1_separation"]["no_pooling"] is True


def test_q1_untouched_and_separated():
    q1 = build_q1_protocol()
    q2 = build_q2_protocol()
    assert q1["question_id"] == Q1_QUESTION_ID == "RQ-C1"
    assert q1["factor"] == "repetition_id"
    assert q2["factor"] == "target_model_id"
    assert q1["question_id"] != q2["question_id"]
    assert q1["changed_factor"] != q2["changed_factor"]


def test_stage_b_immutable():
    assert_stage_b_immutable()


def test_sign_zero_treatment_and_contrast_change():
    assert sign_delta(0.0) == "ZERO"
    assert sign_agreement(0.1, 0.2) is True
    assert sign_agreement(0.1, -0.1) is False
    cc = contrast_change(0.1, -0.05)
    assert cc["delta_change"] == pytest.approx(-0.15)
    assert cc["sign_agreement"] is False
    cc0 = contrast_change(0.0, 0.0)
    assert cc0["sign_agreement"] is True


def test_design_reduced_selected_not_full():
    d = design_schedules()
    assert d["selected_design_id"] == "B_REDUCED_Q2"
    assert d["B_reduced"]["n_new_arms"] == 432
    assert d["A_full"]["n_new_arms"] == 1296
    assert d["selection_not_solely_on_cost"] is True
    assert d["B2_attack_only_rejected"]["selected"] is False
    p = build_q2_protocol()
    assert p["arms"]["new_n"] == 432


def test_model_lock_incomplete_without_network():
    m = build_target_lock_manifest()
    assert m["lock_complete"] is False
    assert m["stop_model_lock"] is True
    assert m["targets"]["T0"]["lock_status"] == "LOCKED"
    assert m["targets"]["T1"]["lock_status"] == "PROPOSED_UNVERIFIED"
    assert m["targets"]["T2"]["exact_provider_model_id"] is None
    assert m["targets"]["T3"]["exact_provider_model_id"] is None
    assert m["selected_from_results"] is False


def test_event_and_eval_ids_unique_across_targets():
    eids = [
        evaluation_id_q2("run", "p2a_atk_001", "D1", "PHASE1-CORE", s)
        for s in ("T0", "T1", "T2", "T3")
    ]
    assert len(set(eids)) == 4
    slots = [
        make_security_event_id(
            "p2a_atk_001",
            1,
            "search",
            "invalid_tool_arguments",
            detector_id="D0",
            policy_id="PHASE1-CORE",
            repetition_id=q2_event_scope_token(s),
        )
        for s in ("T1", "T2", "T3")
    ]
    assert len(set(slots)) == 3
    r2 = make_security_event_id(
        "p2a_atk_001",
        1,
        "search",
        "invalid_tool_arguments",
        detector_id="D0",
        policy_id="PHASE1-CORE",
        repetition_id="R2",
    )
    assert r2 not in slots
    assert pairing_key("t", "D0", "B0") == "t::D0::B0"


@pytest.mark.skipif(not STAGE_B_DIR.is_dir(), reason="Stage-B absent")
def test_stage_b_metrics_and_frozen_sha_untouched():
    m = json.loads((STAGE_B_DIR / "metrics.json").read_text())
    assert m["Tool-HASR"]["n_success"] == 124
    assert m["Judge-ASR"]["n_success"] == 163
    assert m["M3"] == 61
    assert m["M4"] == 22
    assert m["invalid_tool_args_count"] == 231
    assert STAGE_B_RUN_ID.startswith("p3_stage_b_")
    assert hashlib.sha256(P1.read_bytes()).hexdigest().startswith("1a0b0053")
    assert hashlib.sha256(P2.read_bytes()).hexdigest().startswith("32b40e3b")


def test_invalid_args_policy_reuses_s0_s1_s2():
    p = build_q2_protocol()
    inv = p["invalid_tool_args_policy"]
    assert inv["counts_as_tool_hasr_failure"] is False
    ids = [s["id"] for s in inv["sensitivity_analyses_preregistered"]]
    assert ids == [
        "S0_official",
        "S1_stratify_invalid_cooccurrence",
        "S2_exclude_arms_with_invalid",
    ]
    assert inv["no_post_hoc_sensitivity_variants"] is True


def test_claim_boundary_forbids_universal_claims():
    p = build_q2_protocol()
    forbidden = p["claim_boundary"]["forbidden_claims"]
    assert "universal_model_generalization" in forbidden
    assert "detector_superiority" in forbidden
    assert "causal_effect_of_model_size" in forbidden


def test_full_offline_validation_incomplete_gate():
    report = run_offline_validation()
    assert report["gate_status"] == "P3_Q2_PROTOCOL_INCOMPLETE"
    assert report["offline_structural_tests"] == "PASS"
    assert report["api_calls"] == 0
    assert report["llm_calls"] == 0
    assert report["network_calls"] == 0
    assert report["live_execution_allowed"] is False
    assert "MODEL_LOCK_INCOMPLETE" in report["blockers"]
    assert "PRICING_UNKNOWN" in report["blockers"]
    assert "BUDGET_BOUND_UNSET" in report["blockers"]


def test_write_artifacts():
    paths = write_q2_artifacts()
    for p in paths.values():
        assert Path(p).is_file()
    # Must not overwrite Q1 artifacts as part of Q2 writer outputs
    assert "q1" not in "".join(paths.keys()).lower()
    proto = json.loads(Path(paths["protocol_json"]).read_text())
    assert proto["question_id"] == "RQ-C2"
    assert proto["live_execution_allowed"] is False
    man = json.loads(Path(paths["target_lock_manifest_json"]).read_text())
    assert man["stop_model_lock"] is True
