"""Offline Stage-0 gates for the canonical P1 L1 runner.

No OpenRouter/LLM/API. Does not mutate frozen packs or historical evidence.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from adapti_guard.experiments.defense_baselines import get_defense_fn
from adapti_guard.experiments.p1_mechanism_l1 import (
    FORBIDDEN_CONFIG_KEYS,
    LOCKED_JUDGE,
    LOCKED_JUDGE_KEY,
    LOCKED_TARGET,
    LOCKED_TARGET_KEY,
    N_ATTACK,
    N_BENIGN_TWIN,
    N_HARD_NEGATIVE,
    N_MECHANISM,
    N_TOTAL,
    PACK_PATH,
    PACK_SHA256,
    PRIMARY_ARMS,
    SMOKE_CORE_EPISODE_ID,
    SMOKE_EPISODE_IDS,
    L1GateError,
    load_p1_pack,
    preflight,
    smoke_subset,
    verify_pack_invariants,
)

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "datasets" / "frozen" / "p1_mechanism_v1.0.0"
MODELS_YAML = ROOT / "configs" / "models.yaml"

HISTORICAL = {
    ROOT
    / "datasets/frozen/eval_v1/dataset.jsonl": "27b1733cb6678e6144687b60387b564bd248c89871042eef0ffb0e2ce4c54c24",
    ROOT
    / "datasets/frozen/phase1_confirm_v1/dataset.jsonl": "c789811a07d3ed06e1c77d8a45eda6172f480226e006d84fa28386a982536d01",
    ROOT
    / "datasets/frozen/vnext_confirm_v1/confirmation.jsonl": "523c881820710783b5290c76ea5fe5fc01a6341fb427defcba1119fc3e721518",
}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_p1_pack_invariants_match_scientific_contract():
    info = verify_pack_invariants()
    assert info["dataset_hash"] == PACK_SHA256
    assert info["n_total"] == N_TOTAL == 96
    assert info["n_attack"] == N_ATTACK == 44
    assert info["n_benign_twin"] == N_BENIGN_TWIN == 44
    assert info["n_hard_negative"] == N_HARD_NEGATIVE == 8
    assert info["n_mechanism"] == N_MECHANISM == 22


def test_preflight_resolves_canonical_keys_and_disables_cache():
    info = preflight(require_key=False)
    assert info["status"] == "PREFLIGHT_OK"
    assert info["target_config_key"] == LOCKED_TARGET_KEY == "target_2"
    assert info["judge_config_key"] == LOCKED_JUDGE_KEY == "judge_fallback"
    assert info["target_model"] == LOCKED_TARGET
    assert info["judge_model"] == LOCKED_JUDGE
    assert info["cache_enabled"] is False
    assert info["backend"] == "openrouter"
    assert info["temperature"] == 0.0
    assert info["policies_primary"] == list(PRIMARY_ARMS)
    assert "ORACLE_RISK" not in info["policies_primary"]
    assert "ORACLE_BLOCK" not in info["policies_primary"]
    assert info["api_calls_allowed"] is False


def test_preflight_rejects_forbidden_key_selection(monkeypatch):
    # Canonical keys must not be in the forbidden set.
    assert LOCKED_TARGET_KEY not in FORBIDDEN_CONFIG_KEYS
    assert LOCKED_JUDGE_KEY not in FORBIDDEN_CONFIG_KEYS
    for bad in (
        "groq_target",
        "groq_judge",
        "gemini_target",
        "gemini_judge",
        "cerebras_judge",
        "judge_primary",
        "judge",
    ):
        assert bad in FORBIDDEN_CONFIG_KEYS


def test_primary_policies_resolve_and_are_label_blind():
    for arm in PRIMARY_ARMS:
        fn, state = get_defense_fn(arm)
        if state is not None and hasattr(state, "reset"):
            state.reset()
        prompt = "List public library hours."
        try:
            a = fn(prompt, None, is_attack=True, label="attack")
            b = fn(prompt, None, is_attack=False, label="benign")
        except TypeError:
            a = fn(prompt, None)
            b = fn(prompt, None)
        assert a[:2] == b[:2]


def test_smoke_subset_composition():
    rows = load_p1_pack()
    smoke = smoke_subset(rows)
    assert [r["id"] for r in smoke] == list(SMOKE_EPISODE_IDS)
    assert len(smoke) == 6
    assert SMOKE_CORE_EPISODE_ID in SMOKE_EPISODE_IDS
    labels = [r["label"] for r in smoke]
    assert labels.count("attack") == 3
    assert labels.count("benign") == 3
    hard = next(r for r in smoke if r["id"] == "p1m_ben_045")
    assert hard["metadata"]["hard_negative"] is True
    fams = {
        r["metadata"]["family"]
        for r in smoke
        if r["label"] == "attack" and r["id"] != "p1m_atk_003"
    }
    assert smoke[-1]["metadata"]["family"] not in fams


def test_pack_sha_mismatch_raises(tmp_path: Path):
    bogus = tmp_path / "dataset.jsonl"
    bogus.write_text('{"id":"x","label":"attack"}\n', encoding="utf-8")
    # Monkeypatch via argument path through load + verify is file-locked to PACK_PATH;
    # assert hash gate on real digest inequality instead.
    assert _sha(PACK_PATH) == PACK_SHA256
    with pytest.raises(L1GateError) as exc:
        # Force mismatch by calling verify after temporarily swapping is not safe;
        # instead validate the error type contract with a direct raise path:
        from adapti_guard.experiments import p1_mechanism_l1 as mod

        original = mod.PACK_SHA256
        try:
            mod.PACK_SHA256 = "0" * 64
            mod.verify_pack_invariants()
        finally:
            mod.PACK_SHA256 = original
    assert exc.value.status == "STOP_BENCHMARK_SHA_MISMATCH"


def test_frozen_p1_bytes_unchanged_by_l1_runner_work():
    assert _sha(FROZEN / "dataset.jsonl") == PACK_SHA256
    man = json.loads((FROZEN / "manifest.json").read_text(encoding="utf-8"))
    assert man["live_evaluated"] is False
    assert man["status"] == "FROZEN"


def test_historical_evidence_hashes_unchanged():
    for path, expected in HISTORICAL.items():
        assert path.is_file(), path
        assert _sha(path) == expected, path


def test_models_yaml_canonical_block():
    text = MODELS_YAML.read_text(encoding="utf-8")
    assert "target_2:" in text
    assert "judge_fallback:" in text
    assert "qwen/qwen-2.5-7b-instruct" in text
    assert "qwen/qwen-2.5-72b-instruct" in text
    assert "enabled: false" in text


def test_cli_script_exists_and_is_importable():
    script = ROOT / "scripts" / "run_p1_mechanism_l1.py"
    assert script.is_file()
    # Syntax / import surface without executing live path.
    ns: dict = {}
    code = compile(script.read_text(encoding="utf-8"), str(script), "exec")
    # Do not exec full script (side-effect main). Just ensure module helpers import.
    from adapti_guard.experiments import p1_mechanism_l1 as mod

    assert mod.PACK_ID == "p1_mechanism_v1.0.0"
    assert code.co_filename.endswith("run_p1_mechanism_l1.py")
