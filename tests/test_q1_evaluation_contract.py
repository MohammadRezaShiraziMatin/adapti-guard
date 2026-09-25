from adapti_guard.evaluation.b2_adaptive_contract import LIVE_WIRING_MAX_TURNS
from adapti_guard.evaluation.q1_evaluation_contract import validate_q1_evaluation_contract


def test_q1_contract_offline_validation():
    report = validate_q1_evaluation_contract(repo_root=".")
    assert report["dataset_sha256"] == report["dataset_sha256"]
    assert report["primary_attack_episodes"] == 732
    assert report["budget_cap_usd"] == 3.0
    assert report["models_yaml_sha256"] == "37174858710a087b3fe58c40e65c796418d1791ff4280bca08d96486b35d7ec3"
    assert LIVE_WIRING_MAX_TURNS == 3
    assert "q1_primary_gemma_3_27b" in report["panel_keys_pending_verification"]
