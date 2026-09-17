"""Offline tests for P2.3 agentic candidate trajectory pack.

No LLM/API. Does not modify frozen P1 or historical L1 artifacts.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from adapti_guard.experiments.p2_agentic import (
    OfflinePolicy,
    P2AgenticHarness,
    trajectory_from_dict,
)

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "datasets" / "candidates" / "p2_agentic_v0"
BUILDER = ROOT / "scripts" / "build_p2_agentic_v0_pack.py"
VALIDATOR = ROOT / "scripts" / "validate_p2_agentic_pack.py"
FROZEN_P1 = ROOT / "datasets" / "frozen" / "p1_mechanism_v1.0.0" / "dataset.jsonl"
EXPECTED_P1_SHA = "1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235"


def _load_builder():
    spec = importlib.util.spec_from_file_location("build_p2_agentic_v0_pack", BUILDER)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _rows() -> list[dict]:
    return [
        json.loads(line)
        for line in (PACK / "dataset.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_pack_artifacts_exist():
    for name in (
        "dataset.jsonl",
        "manifest.json",
        "schema.json",
        "coverage.json",
        "hashes.sha256",
        "README.md",
        "DATASET_CARD.md",
    ):
        assert (PACK / name).is_file(), name


def test_cardinality_and_pairing():
    rows = _rows()
    assert len(rows) == 36
    attacks = [r for r in rows if r["label"] == "attack"]
    twins = [r for r in rows if r["label"] == "benign" and not r["hard_negative"]]
    hard = [r for r in rows if r["hard_negative"]]
    assert len(attacks) == 16
    assert len(twins) == 16
    assert len(hard) == 4
    by_id = {r["id"]: r for r in rows}
    for a in attacks:
        b = by_id[a["benign_twin"]]
        assert b["attack_twin"] == a["id"]
        assert b["n_turns"] == a["n_turns"]


def test_unique_ids_and_mechanisms():
    rows = _rows()
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids))
    builder = _load_builder()
    attacks = [r for r in rows if r["label"] == "attack"]
    for a in attacks:
        assert a["mechanism_id"] in builder.VALID_MECHANISM_IDS
        assert a["activation_turn"] in {t["turn_id"] for t in a["turns"]}
        assert isinstance(a["harmful_action"], dict)
        assert a["harmful_action"].get("tool")


def test_coverage_matrix():
    cov = json.loads((PACK / "coverage.json").read_text(encoding="utf-8"))
    assert cov["dynamics_ok"] is True
    builder = _load_builder()
    for k, need in builder.REQUIRED_DYNAMICS_MIN.items():
        assert cov["dynamics_counts"][k] >= need


def test_channel_provenance():
    builder = _load_builder()
    for r in _rows():
        for t in r["turns"]:
            for ch in t.get("channels") or []:
                assert ch in builder.VALID_CHANNELS
        # tool-output injection attacks must include a tool_output channel somewhere
        if "tool_output_injection" in (r.get("dynamics") or []) and r["label"] == "attack":
            assert any("tool_output" in (t.get("channels") or []) for t in r["turns"])


def test_harmful_action_semantics():
    for r in _rows():
        if r["label"] == "attack":
            assert r["harmful_action"] is not None
            assert r["success_condition"].get("tool") == r["harmful_action"]["tool"]
        else:
            assert r.get("harmful_action") is None
            assert not r.get("success_condition")


def test_schema_required_fields():
    schema = json.loads((PACK / "schema.json").read_text(encoding="utf-8"))
    required = set(schema["required"])
    for r in _rows():
        assert required.issubset(r.keys())


def test_deterministic_hash_rebuild(tmp_path: Path):
    builder = _load_builder()
    # Rebuild into a temp dir by monkeypatching OUT
    original_out = builder.OUT
    try:
        builder.OUT = tmp_path / "p2_agentic_v0"
        result = builder.write_pack()
        assert result["ok"] is True
        digest_a = result["sha256"]
        result2 = builder.write_pack()
        assert result2["sha256"] == digest_a
        # Match committed pack hash
        committed = (PACK / "hashes.sha256").read_text(encoding="utf-8").split()[0]
        assert digest_a == committed
    finally:
        builder.OUT = original_out


def test_validator_script_ok():
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OK 36" in proc.stdout


def test_no_p1_mutation():
    digest = hashlib.sha256(FROZEN_P1.read_bytes()).hexdigest()
    assert digest == EXPECTED_P1_SHA
    assert "datasets/candidates/" in str(PACK)
    assert "datasets/frozen/" not in str(PACK.resolve())


def test_harness_loads_attack_offline():
    """Candidate rows load into P2.2 harness without network."""
    attack = next(r for r in _rows() if r["id"] == "p2a_atk_001")
    spec = trajectory_from_dict(attack)
    out = P2AgenticHarness(seed=42, policy=OfflinePolicy(mode="scripted")).run_trajectory(spec)
    assert out["n_turns"] == attack["n_turns"]
    assert out["final_state"]["memory"].get("authz_token") == "GRANT-OPS-ALPHA"


def test_manifest_not_frozen_not_live():
    man = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
    assert man["status"] == "CANDIDATE"
    assert man["live_evaluated"] is False
    assert man["scientific_evidence"] is False
    assert man.get("frozen") is False
    assert man["n_attack"] == 16
    assert man["n_benign_twin"] == 16
    assert man["n_hard_negative"] == 4


def test_p2_new_documented():
    attacks = [r for r in _rows() if r["label"] == "attack"]
    news = [r for r in attacks if r.get("taxonomy_status") == "P2_NEW"]
    assert news, "expected some P2_NEW mechanisms"
    for r in news:
        assert r.get("taxonomy_note")
