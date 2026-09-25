from adapti_guard.evaluation.b2_adaptive_contract import LIVE_WIRING_MAX_TURNS
from adapti_guard.evaluation.q1_evaluation_contract import (
    VNEXT_DATASET_SHA,
    VNEXT_MODELS_YAML_SHA,
    validate_q1_evaluation_contract,
)


def test_q1_contract_offline_validation():
    report = validate_q1_evaluation_contract(repo_root=".")
    assert report["execution_gate"] == "BLOCKED"
    assert report["dataset_sha256"] == VNEXT_DATASET_SHA
    assert report["models_yaml_sha256"] == VNEXT_MODELS_YAML_SHA
    assert report["derived_attack_episodes"] == 61 * 4 * 3
    assert report["attack_episodes_declared"] == "NEEDS_DECISION"
    assert report["budget_cap_usd"] == "NEEDS_DECISION"
    assert "primary_episode_budget.attack_episodes" in report["needs_decision"]
    assert "budget.hard_cap_usd" in report["needs_decision"]
    assert LIVE_WIRING_MAX_TURNS == 3
    assert "q1_primary_gemma_3_27b" in report["panel_keys_pending_verification"]
