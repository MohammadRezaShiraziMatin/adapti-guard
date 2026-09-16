"""Immutability checks for frozen P2 agentic pack v0.1.0.

Does not modify packs. No LLM/API.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "datasets" / "frozen" / "p2_agentic_v0.1.0"
CANDIDATE = ROOT / "datasets" / "candidates" / "p2_agentic_v0"
P1_FROZEN = ROOT / "datasets" / "frozen" / "p1_mechanism_v1.0.0"

EXPECTED_SHA = "32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd"
P1_EXPECTED_SHA = "1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_frozen_pack_files_exist():
    for name in ("dataset.jsonl", "manifest.json", "hashes.sha256", "DATASET_CARD.md", "README.md"):
        assert (FROZEN / name).is_file(), name


def test_frozen_dataset_sha_matches_expected():
    assert _sha(FROZEN / "dataset.jsonl") == EXPECTED_SHA


def test_candidate_and_frozen_dataset_bytes_identical():
    assert (CANDIDATE / "dataset.jsonl").read_bytes() == (FROZEN / "dataset.jsonl").read_bytes()


def test_frozen_manifest_status():
    man = json.loads((FROZEN / "manifest.json").read_text(encoding="utf-8"))
    assert man["status"] == "FROZEN"
    assert man["live_evaluated"] is False
    assert man["version"] == "p2_agentic_v0.1.0"
    assert man["dataset_sha256"] == EXPECTED_SHA
    assert man["source_sha256"] == EXPECTED_SHA
    assert man["source_candidate"] == "datasets/candidates/p2_agentic_v0/"
    assert man["attack_count"] == 16
    assert man["benign_twin_count"] == 16
    assert man["hard_negative_count"] == 4
    assert man["n_rows"] == 36
    assert man["audit_v3_verdict"] == "FREEZE-READY"
    assert len(man["known_limitations"]) >= 5


def test_hashes_sidecar_lists_dataset_digest():
    listed = (FROZEN / "hashes.sha256").read_text(encoding="utf-8").split()[0]
    assert listed == EXPECTED_SHA


def test_p1_frozen_unchanged():
    assert _sha(P1_FROZEN / "dataset.jsonl") == P1_EXPECTED_SHA


def test_candidate_manifest_remains_candidate_provenance():
    man = json.loads((CANDIDATE / "manifest.json").read_text(encoding="utf-8"))
    assert man["status"] == "CANDIDATE"
    assert man["live_evaluated"] is False
    assert man.get("frozen") is False
