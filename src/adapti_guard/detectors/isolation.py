"""P3 state hashing / isolation helpers (offline)."""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Mapping


def canonical_json(obj: Any) -> str:
    """Deterministic JSON serialization for hashes."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str, separators=(",", ":"))


def state_hash(obj: Any) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def deep_freeze_copy(obj: Any) -> Any:
    return copy.deepcopy(obj)


def assert_state_unchanged(before: Any, after: Any, *, what: str) -> None:
    hb = state_hash(before)
    ha = state_hash(after)
    if hb != ha:
        raise AssertionError(f"{what} mutated during detector execution: {hb} != {ha}")
