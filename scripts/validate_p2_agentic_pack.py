#!/usr/bin/env python3
"""Offline validator for datasets/candidates/p2_agentic_v0 (no LLM/API)."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "datasets" / "candidates" / "p2_agentic_v0"
FROZEN_P1 = ROOT / "datasets" / "frozen" / "p1_mechanism_v1.0.0" / "dataset.jsonl"
EXPECTED_P1_SHA = "1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235"

sys.path.insert(0, str(ROOT / "scripts"))
from build_p2_agentic_v0_pack import (  # noqa: E402
    REQUIRED_DYNAMICS_MIN,
    VALID_CHANNELS,
    VALID_DYNAMICS,
    VALID_MECHANISM_IDS,
    stable_dumps,
)

REQUIRED_TOP = (
    "id",
    "label",
    "family",
    "mechanism_id",
    "component",
    "turns",
    "n_turns",
    "hard_negative",
    "dynamics",
    "pack_id",
    "version",
)


def load_rows() -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in (PACK / "dataset.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _tool_names(turns: list[dict]) -> list[str | None]:
    out = []
    for t in turns:
        call = t.get("agent_tool_call")
        out.append((call or {}).get("name") if call else None)
    return out


def validate(rows: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []

    if len(rows) != 36:
        errors.append(f"expected 36 trajectories, got {len(rows)}")

    attacks = [r for r in rows if r.get("label") == "attack"]
    benigns = [r for r in rows if r.get("label") == "benign" and not r.get("hard_negative")]
    hard = [r for r in rows if r.get("hard_negative")]

    if len(attacks) != 16:
        errors.append(f"expected 16 attacks, got {len(attacks)}")
    if len(benigns) != 16:
        errors.append(f"expected 16 benign twins, got {len(benigns)}")
    if len(hard) != 4:
        errors.append(f"expected 4 hard negatives, got {len(hard)}")

    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate trajectory ids")

    by_id = {r["id"]: r for r in rows}

    # Content uniqueness (stable serialization of turns+success+harmful)
    seen_content: set[str] = set()
    for r in rows:
        key = stable_dumps(
            {
                "turns": r.get("turns"),
                "success_condition": r.get("success_condition"),
                "harmful_action": r.get("harmful_action"),
                "utility_condition": r.get("utility_condition"),
            }
        )
        if key in seen_content:
            errors.append(f"duplicate trajectory content: {r['id']}")
        seen_content.add(key)

    dyn_counts: Counter[str] = Counter()
    for atk in attacks:
        for key in REQUIRED_TOP:
            if key not in atk:
                errors.append(f"{atk.get('id')} missing {key}")

        mid = atk.get("mechanism_id")
        if mid not in VALID_MECHANISM_IDS:
            errors.append(f"{atk['id']} invalid mechanism_id={mid}")

        twin = atk.get("benign_twin")
        if not twin or twin not in by_id:
            errors.append(f"{atk['id']} missing benign twin")
        else:
            ben = by_id[twin]
            if ben.get("label") != "benign" or ben.get("hard_negative"):
                errors.append(f"{twin} is not a benign twin")
            if ben.get("attack_twin") != atk["id"]:
                errors.append(f"{twin} attack_twin mismatch")
            if ben.get("n_turns") != atk.get("n_turns"):
                errors.append(f"{atk['id']}/{twin} turn-count mismatch")
            # structural tool-sequence alignment (names per turn)
            if _tool_names(atk["turns"]) != _tool_names(ben["turns"]):
                errors.append(f"{atk['id']}/{twin} tool-sequence mismatch")
            if ben.get("harmful_action") is not None:
                errors.append(f"{twin} must not declare harmful_action")
            if ben.get("success_condition"):
                # benign may have empty success_condition only
                if ben["success_condition"] not in ({}, None):
                    errors.append(f"{twin} must not have harmful success_condition")

        act = atk.get("activation_turn")
        if act is None:
            errors.append(f"{atk['id']} missing activation_turn")
        else:
            turn_ids = {int(t["turn_id"]) for t in atk.get("turns") or []}
            if int(act) not in turn_ids:
                errors.append(f"{atk['id']} activation_turn {act} not in trajectory")

        ha = atk.get("harmful_action")
        if not isinstance(ha, dict) or not ha.get("tool"):
            errors.append(f"{atk['id']} harmful_action must be explicit")
        sc = atk.get("success_condition") or {}
        if sc.get("tool") != (ha or {}).get("tool"):
            errors.append(f"{atk['id']} success_condition tool mismatch vs harmful_action")

        for d in atk.get("dynamics") or []:
            if d not in VALID_DYNAMICS:
                errors.append(f"{atk['id']} invalid dynamics tag {d}")
            else:
                dyn_counts[d] += 1

        for t in atk.get("turns") or []:
            for ch in t.get("channels") or []:
                if ch not in VALID_CHANNELS:
                    errors.append(f"{atk['id']} turn {t.get('turn_id')} invalid channel {ch}")
            # tool event structural validity
            call = t.get("agent_tool_call")
            if call is not None:
                if not isinstance(call, dict) or "name" not in call:
                    errors.append(f"{atk['id']} invalid agent_tool_call")
                if "arguments" not in call:
                    errors.append(f"{atk['id']} tool call missing arguments")
            inj = t.get("inject_tool_observation")
            if inj is not None:
                if not isinstance(inj, dict) or "observation" not in inj:
                    errors.append(f"{atk['id']} invalid inject_tool_observation")

        if atk.get("taxonomy_status") == "P2_NEW" and not atk.get("taxonomy_note"):
            errors.append(f"{atk['id']} P2_NEW missing taxonomy_note")

    for k, need in REQUIRED_DYNAMICS_MIN.items():
        if dyn_counts.get(k, 0) < need:
            errors.append(f"dynamics {k} count {dyn_counts.get(k, 0)} < required {need}")

    for hn in hard:
        if hn.get("label") != "benign":
            errors.append(f"{hn['id']} hard negative must be label=benign")
        if hn.get("harmful_action") is not None:
            errors.append(f"{hn['id']} hard negative must not have harmful_action")
        if hn.get("success_condition"):
            errors.append(f"{hn['id']} hard negative must not have success_condition")

    # Deterministic serialization / hashes
    listed = (PACK / "hashes.sha256").read_text(encoding="utf-8").strip().split()
    file_digest = hashlib.sha256((PACK / "dataset.jsonl").read_bytes()).hexdigest()
    if not listed or listed[0] != file_digest:
        errors.append("hashes.sha256 mismatch vs dataset.jsonl")
    man = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
    if man.get("dataset_sha256") != file_digest:
        errors.append("manifest dataset_sha256 mismatch")
    if man.get("live_evaluated") is not False:
        errors.append("manifest.live_evaluated must be false")
    if man.get("status") != "CANDIDATE":
        errors.append("manifest.status must be CANDIDATE")
    if man.get("frozen") is True:
        errors.append("manifest.frozen must not be true")
    if man.get("scientific_evidence") is True:
        errors.append("manifest.scientific_evidence must be false")

    # Required artifacts
    for name in ("dataset.jsonl", "manifest.json", "schema.json", "coverage.json", "README.md", "hashes.sha256"):
        if not (PACK / name).is_file():
            errors.append(f"missing artifact {name}")

    # No P1 mutation
    if FROZEN_P1.is_file():
        p1 = hashlib.sha256(FROZEN_P1.read_bytes()).hexdigest()
        if p1 != EXPECTED_P1_SHA:
            errors.append(f"P1 dataset SHA changed: {p1}")

    # Must not live under frozen/
    if "datasets/frozen/" in str(PACK):
        errors.append("candidate pack must not be under datasets/frozen/")

    return errors


def main() -> int:
    rows = load_rows()
    errors = validate(rows)
    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("OK", len(rows), "trajectories")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
