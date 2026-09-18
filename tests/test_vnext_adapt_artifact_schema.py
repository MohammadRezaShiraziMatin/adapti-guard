"""Offline schema and consistency guards for the VNEXT-ADAPT prediction artifact.

No OpenRouter/LLM/API. These tests pin the artifact schema (label/attack_label,
no `is_attack` field) and the historical metric consistency, and assert that
malformed packs (wrong attack/benign counts) fail closed at load time.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pytest

from adapti_guard.experiments.vnext_confirm import (
    LOCKED_N_ATTACK,
    LOCKED_N_BENIGN,
    LOCKED_PACK_SHA256,
    VNextGateError,
    load_locked_pack,
    score_run,
    verify_pack_hash,
)

ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "experiments" / "real_llm_eval" / "VNEXT_CONFIRM" / "20260914-133147"
VNEXT_ADAPT_PREDICTIONS = RUN_DIR / "VNEXT-ADAPT" / "VNEXT-ADAPT_predictions.jsonl"
B0_PREDICTIONS = RUN_DIR / "B0" / "B0_predictions.jsonl"


def _load_jsonl(path: Path) -> list[dict]:
    assert path.is_file(), f"missing artifact: {path}"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _skip_if_artifact_absent() -> None:
    if not VNEXT_ADAPT_PREDICTIONS.is_file() or not B0_PREDICTIONS.is_file():
        pytest.skip("VNEXT-ADAPT/B0 prediction artifacts not present locally (MISSING_LOCALLY)")


# --- 1. Existing artifact: row counts and label distribution ---


def test_vnext_adapt_artifact_has_122_rows():
    _skip_if_artifact_absent()
    rows = _load_jsonl(VNEXT_ADAPT_PREDICTIONS)
    assert len(rows) == 122


def test_vnext_adapt_artifact_label_counts_are_61_attack_61_benign():
    _skip_if_artifact_absent()
    rows = _load_jsonl(VNEXT_ADAPT_PREDICTIONS)
    counts = Counter(r.get("label") for r in rows)
    assert counts["attack"] == 61
    assert counts["benign"] == 61


def test_vnext_adapt_artifact_attack_label_matches_label():
    _skip_if_artifact_absent()
    rows = _load_jsonl(VNEXT_ADAPT_PREDICTIONS)
    label_counts = Counter(r.get("label") for r in rows)
    attack_label_counts = Counter(r.get("attack_label") for r in rows)
    assert attack_label_counts == label_counts
    assert attack_label_counts["attack"] == 61
    assert attack_label_counts["benign"] == 61


# --- 2. Schema: no is_attack field ---


def test_vnext_adapt_artifact_has_no_is_attack_field():
    _skip_if_artifact_absent()
    rows = _load_jsonl(VNEXT_ADAPT_PREDICTIONS)
    for row in rows:
        assert "is_attack" not in row, (
            f"is_attack must not be part of the artifact schema; found in id={row.get('id')}"
        )


def test_vnext_adapt_artifact_required_provenance_fields():
    _skip_if_artifact_absent()
    rows = _load_jsonl(VNEXT_ADAPT_PREDICTIONS)
    for row in rows:
        assert row.get("scientific_arm") == "VNEXT-ADAPT"
        assert row.get("baseline") == "VNEXT-ADAPT"
        assert "label" in row
        assert "attack_succeeded" in row
        assert "api_status" in row


# --- 3. Historical metric consistency: score the existing run ---


def test_score_run_on_existing_artifact_yields_historical_fail():
    _skip_if_artifact_absent()
    scored = score_run(RUN_DIR)
    vnext = scored["comparison"]["VNEXT-ADAPT"]
    assert vnext["n_attack"] == 61
    assert vnext["n_attack_success"] == 53
    assert vnext["asr"] == pytest.approx(0.8688524590163934)
    assert scored["verdict"]["status"] == "FAIL"
    assert scored["verdict"]["qualified_win"] is False


def test_score_run_historical_fail_reasons_unchanged():
    _skip_if_artifact_absent()
    scored = score_run(RUN_DIR)
    reasons = scored["verdict"]["fail_reasons"]
    assert "s5_mcnemar_not_significant" in reasons
    assert "msid_not_met" in reasons
    assert "s4_utility_ineligible" in reasons
    assert scored["verdict"]["p_value"] == pytest.approx(0.0625)
    assert scored["verdict"]["delta_hat"] == pytest.approx(0.08196721311475409)
    assert scored["verdict"]["utility"] == pytest.approx(0.9344262295081968)


def test_score_run_no_exclusions_on_existing_artifact():
    _skip_if_artifact_absent()
    scored = score_run(RUN_DIR)
    assert scored["comparison"]["excluded"] == {}
    assert len(scored["comparison"]["scorable_attack_ids"]) == 61
    assert len(scored["comparison"]["scorable_benign_ids"]) == 61


# --- 4 & 5. Fail-closed malformed packs ---


def _write_malformed_pack(tmp_path: Path, n_attack: int, n_benign: int) -> Path:
    """Write a pack with the given attack/benign counts (total != 61+61)."""
    rows = [{"id": f"atk_{i:03d}", "label": "attack", "prompt": "x"} for i in range(n_attack)]
    rows.extend({"id": f"ben_{i:03d}", "label": "benign", "prompt": "x"} for i in range(n_benign))
    pack = tmp_path / "malformed_dataset.jsonl"
    pack.write_text(
        "".join(json.dumps(r) + "\n" for r in rows),
        encoding="utf-8",
    )
    return pack


def test_malformed_pack_zero_attack_122_benign_fails_closed(tmp_path: Path):
    pack = _write_malformed_pack(tmp_path, n_attack=0, n_benign=122)
    with pytest.raises(VNextGateError) as exc:
        load_locked_pack(pack)
    assert exc.value.status == "INVALID_PACK_COUNTS"


def test_malformed_pack_60_attack_62_benign_fails_closed(tmp_path: Path):
    pack = _write_malformed_pack(tmp_path, n_attack=60, n_benign=62)
    with pytest.raises(VNextGateError) as exc:
        load_locked_pack(pack)
    assert exc.value.status == "INVALID_PACK_COUNTS"


def test_frozen_pack_hash_unchanged():
    info = verify_pack_hash()
    assert info["sha256"] == LOCKED_PACK_SHA256
    assert info["match"] is True


def test_frozen_pack_counts_locked():
    rows = load_locked_pack()
    assert len(rows) == LOCKED_N_ATTACK + LOCKED_N_BENIGN
    assert sum(1 for r in rows if r.get("label") == "attack") == LOCKED_N_ATTACK
    assert sum(1 for r in rows if r.get("label") == "benign") == LOCKED_N_BENIGN
