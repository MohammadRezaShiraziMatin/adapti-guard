"""Offline validation for P3 Stage-C Q2 model/pricing/budget lock (no live eval)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from adapti_guard.experiments.p2_agentic_live import (
    LOCKED_BACKEND,
    LOCKED_TARGET,
    MAX_JUDGE_RETRIES,
    MAX_TARGET_RETRIES,
)
from adapti_guard.experiments.p3_stage_c_q1 import (
    QUESTION_ID as Q1_QUESTION_ID,
)
from adapti_guard.experiments.p3_stage_c_q1 import (
    build_q1_protocol,
)
from adapti_guard.experiments.p3_stage_c_q2 import (
    PRIMARY_POLICY_STRATUM,
    QUESTION_ID,
    STAGE_B_DIR,
    assert_stage_b_immutable,
    build_q2_protocol,
    build_target_lock_manifest,
    design_schedules,
    run_offline_validation,
    write_q2_artifacts,
)
from adapti_guard.experiments.p3_stage_c_q2_lock import (
    JUDGE_ID,
    T0_ID,
    T1_ID,
    T2_ID,
    T3_ID,
    gate_status_from_locks,
    pricing_lock,
    q2_arm_schedule,
    q2_call_bounds,
    worst_case_cost_usd,
)

ROOT = Path(__file__).resolve().parents[1]
P1 = ROOT / "datasets" / "frozen" / "p1_mechanism_v1.0.0" / "dataset.jsonl"
P2 = ROOT / "datasets" / "frozen" / "p2_agentic_v0.1.0" / "dataset.jsonl"


def test_exact_model_ids_locked():
    m = build_target_lock_manifest()
    assert m["exact_ids"]["T0"] == T0_ID == LOCKED_TARGET
    assert m["exact_ids"]["T1"] == T1_ID == "qwen/qwen3-30b-a3b"
    assert m["exact_ids"]["T2"] == T2_ID == "google/gemma-3-27b-it"
    assert m["exact_ids"]["T3"] == T3_ID == "qwen/qwen3.5-35b-a3b"
    assert m["exact_ids"]["JUDGE"] == JUDGE_ID
    assert m["unique_ids"] is True
    assert m["lock_complete"] is True
    assert m["provider"] == LOCKED_BACKEND == "openrouter"
    assert m["targets"]["T0"]["lock_status"] == "LOCKED_FROM_STAGE_B"


def test_provider_and_pricing_complete():
    pl = pricing_lock()
    assert pl["all_secondary_pricing_verified"] is True
    for s in ("T1", "T2", "T3", "JUDGE"):
        b = pl["models"][s]
        assert b["verified"] is True
        assert b["pricing_unit"] == "USD_per_1M_tokens"
        assert isinstance(b["input_price"], (float, int))
        assert isinstance(b["output_price"], (float, int))


def test_arm_and_call_counts_deterministic():
    sched = q2_arm_schedule()
    bounds = q2_call_bounds()
    assert sched["n_new_arms"] == 432
    assert sched["pack_turns"]["n_turns_total"] == 140
    assert bounds["scheduled_target_calls_if_unblocked"] == 1680
    assert bounds["scheduled_judge_calls"] == 432
    assert bounds["target_calls_max"] == 1680 * (1 + MAX_TARGET_RETRIES) == 5040
    assert bounds["judge_calls_max"] == 432 * (1 + MAX_JUDGE_RETRIES) == 1296
    assert bounds["explicitly_not_stage_b_empirical_1663"] is True
    d = design_schedules()
    assert d["selected_design_id"] == "B_REDUCED_Q2"
    assert d["B_reduced"]["n_new_arms"] == 432


def test_worst_case_cost_and_human_budget_pass():
    cost = worst_case_cost_usd()
    assert cost["worst_case_cost_usd"] == pytest.approx(4.403528, abs=1e-6)
    assert cost["maximum_permitted_budget_usd"] == 10.0
    assert cost["budget_check"] == "PASS"
    assert cost["budget_status"] == "BUDGET_PASS"
    # Explicit override still respected
    cost2 = worst_case_cost_usd(maximum_permitted_budget_usd=100.0)
    assert cost2["budget_check"] == "PASS"
    cost3 = worst_case_cost_usd(maximum_permitted_budget_usd=0.01)
    assert cost3["budget_check"] == "FAIL"


def test_gate_status_ready_with_budget():
    g = gate_status_from_locks()
    assert g["status"] == "P3_Q2_GATE_READY"
    assert g["blockers"] == []
    assert g["budget_check"] == "PASS"
    assert g["maximum_permitted_budget_usd"] == 10.0
    assert g["model_lock_complete"] is True
    assert g["pricing_complete"] is True
    assert g["live_execution_allowed"] is False
    assert g["api_calls"] == g["llm_calls"] == g["network_live_eval_calls"] == 0


def test_q1_separation_and_factor():
    q1 = build_q1_protocol()
    q2 = build_q2_protocol()
    assert q1["question_id"] == Q1_QUESTION_ID
    assert q1["factor"] == "repetition_id"
    assert q2["question_id"] == QUESTION_ID
    assert q2["factor"] == "target_model_id"
    assert q2["primary_endpoint"]["primary_policy_stratum"] == PRIMARY_POLICY_STRATUM


@pytest.mark.stage_b
@pytest.mark.skipif(not STAGE_B_DIR.is_dir(), reason="Stage-B raw traces not present locally (MISSING_LOCALLY)")
def test_t0_and_stage_b_immutable():
    assert_stage_b_immutable()
    assert hashlib.sha256(P1.read_bytes()).hexdigest() == (
        "1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235"
    )
    assert hashlib.sha256(P2.read_bytes()).hexdigest() == (
        "32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd"
    )
    if STAGE_B_DIR.is_dir():
        m = json.loads((STAGE_B_DIR / "metrics.json").read_text())
        assert m["Tool-HASR"]["n_success"] == 124


@pytest.mark.stage_b
@pytest.mark.skipif(not STAGE_B_DIR.is_dir(), reason="Stage-B raw traces not present locally (MISSING_LOCALLY)")
def test_full_offline_validation_gate_ready():
    report = run_offline_validation()
    assert report["gate_status"] == "P3_Q2_GATE_READY"
    assert report["offline_structural_tests"] == "PASS"
    assert report["blockers"] == []
    assert report["api_calls"] == 0
    assert report["llm_calls"] == 0
    assert report["network_live_eval_calls"] == 0
    assert report["exact_arm_count"]["n_new_arms"] == 432
    assert report["pricing_completeness"]["ok"] is True
    assert report["budget_preflight"]["budget_check"] == "PASS"
    assert report["budget_preflight"]["maximum_permitted_budget_usd"] == 10.0


@pytest.mark.stage_b
@pytest.mark.skipif(not STAGE_B_DIR.is_dir(), reason="Stage-B raw traces not present locally (MISSING_LOCALLY)")
def test_write_artifacts_include_pricing_budget():
    paths = write_q2_artifacts()
    for key in (
        "model_verification_json",
        "pricing_lock_json",
        "budget_preflight_json",
        "target_lock_manifest_json",
        "validation_json",
    ):
        assert Path(paths[key]).is_file()
    bp = json.loads(Path(paths["budget_preflight_json"]).read_text())
    assert bp["worst_case_cost_usd"] == pytest.approx(4.403528, abs=1e-6)
    assert bp["maximum_permitted_budget_usd"] == 10.0
    assert "[MY_BUDGET]" not in Path(paths["budget_preflight_json"]).read_text()
    assert "null" not in json.dumps({"maximum_permitted_budget_usd": bp["maximum_permitted_budget_usd"]})
    man = json.loads(Path(paths["target_lock_manifest_json"]).read_text())
    assert man["exact_ids"]["T2"] == "google/gemma-3-27b-it"
