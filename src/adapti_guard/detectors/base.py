"""P3 detector comparison — common contract and offline protocol helpers.

Design-only / offline. Detectors never execute tools, mutate policy state,
or change action costs. No live LLM/API.
"""

from __future__ import annotations

import hashlib
import json
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

# Locked frozen pack SHAs (must match P1/P2 freeze constants).
P1_SHA256 = "1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235"
P2_SHA256 = "32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd"

# Canonical tool execution states preserved from P2.4.
EXECUTION_STATES = frozenset(
    {
        "EXECUTED",
        "POLICY_DENIED",
        "INVALID_TOOL_ARGS",
        "UNSUPPORTED_TOOL",
        "RUNTIME_ERROR",
        "NO_TOOL_REQUESTED",
    }
)

# Fields that must NEVER appear in detector inputs (leakage).
FORBIDDEN_INPUT_KEYS = frozenset(
    {
        "judge",
        "judge_asr_success",
        "judge_outcome",
        "tool_hasr_success",
        "security_outcome",
        "final_outcome",
        "attack_success",
        "harmful_action_final",
        "future_turns",
        "future_tool_results",
        "policy_decision_final",
        "label",  # gold label — detectors must be label-blind at inference
        "is_attack",
    }
)


@dataclass(frozen=True)
class DetectorResult:
    """Common P3 detector output contract."""

    detector_id: str
    detector_hit: bool
    risk_signal: float
    evidence: tuple[str, ...] = ()
    confidence: float | None = None
    latency_ms: float = 0.0
    reason_code: str = ""
    input_scope: str = "current_turn"
    version: str = "unknown"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["evidence"] = list(self.evidence)
        d["metadata"] = dict(self.metadata)
        return d


@dataclass(frozen=True)
class EpisodeDetectionContext:
    """Information available at detection time only (no future / judge / gold)."""

    trajectory_id: str
    turn_id: int
    current_input: str
    tool_name: str | None = None
    tool_arguments: Mapping[str, Any] | None = None
    tool_output: str | None = None  # only if already observed this turn/before
    context: str | None = None  # prior messages/memory already visible
    state: Mapping[str, Any] | None = None  # prior detector/policy-visible state
    source_channel: str | None = None  # e.g. user | tool_output | memory
    input_scope: str = "current_turn"

    def to_dict(self) -> dict[str, Any]:
        return {
            "trajectory_id": self.trajectory_id,
            "turn_id": self.turn_id,
            "current_input": self.current_input,
            "tool_name": self.tool_name,
            "tool_arguments": dict(self.tool_arguments or {}),
            "tool_output": self.tool_output,
            "context": self.context,
            "state": dict(self.state or {}),
            "source_channel": self.source_channel,
            "input_scope": self.input_scope,
        }


class P3Detector(ABC):
    """P3 detector interface. Must not execute tools or mutate policy."""

    detector_id: str = "abstract"
    version: str = "0.0.0"

    @abstractmethod
    def detect(self, ctx: EpisodeDetectionContext) -> DetectorResult:
        raise NotImplementedError

    def config_dict(self) -> dict[str, Any]:
        return {"detector_id": self.detector_id, "version": self.version}

    def config_hash(self) -> str:
        blob = json.dumps(self.config_dict(), sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def assert_no_forbidden_keys(payload: Mapping[str, Any], *, _path: str = "") -> None:
    """Reject leakage keys at any nesting depth (state, nested maps)."""
    bad = sorted(set(payload.keys()) & FORBIDDEN_INPUT_KEYS)
    if bad:
        where = f" at {_path}" if _path else ""
        raise ValueError(f"detector input leakage keys forbidden{where}: {bad}")
    for key, value in payload.items():
        if isinstance(value, Mapping):
            child = f"{_path}.{key}" if _path else str(key)
            assert_no_forbidden_keys(value, _path=child)


def make_detector_observation_id(
    trajectory_id: str, detector_id: str, turn_id: int
) -> str:
    return f"{trajectory_id}::{detector_id}::t{int(turn_id)}"


def make_end_to_end_arm_id(
    trajectory_id: str, detector_id: str, policy_id: str
) -> str:
    return f"{trajectory_id}::{detector_id}::{policy_id}"


def assert_unique_ids(ids: Sequence[str], *, what: str) -> None:
    if len(ids) != len(set(ids)):
        raise ValueError(f"duplicate {what}: {len(ids) - len(set(ids))} extras")


def assert_pack_sha(path: Path, expected: str, *, label: str) -> str:
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if digest != expected:
        raise ValueError(f"{label} SHA mismatch: got {digest} expected {expected}")
    return digest


def assert_unique_output_dir(path: Path, *, force: bool = False) -> None:
    path = Path(path)
    if path.exists() and any(path.iterdir()) and not force:
        raise FileExistsError(
            f"P3 overwrite protection: non-empty output dir {path} (pass force=True to override)"
        )


def timed_detect(detector: P3Detector, ctx: EpisodeDetectionContext) -> DetectorResult:
    """Run detect with wall-clock latency filled if detector returns 0."""
    t0 = time.perf_counter()
    result = detector.detect(ctx)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    if result.latency_ms <= 0.0:
        return DetectorResult(
            detector_id=result.detector_id,
            detector_hit=result.detector_hit,
            risk_signal=result.risk_signal,
            evidence=result.evidence,
            confidence=result.confidence,
            latency_ms=elapsed_ms,
            reason_code=result.reason_code,
            input_scope=result.input_scope,
            version=result.version,
            metadata=result.metadata,
        )
    return result


# ---------------------------------------------------------------------------
# Metric helpers (offline reporting only — no ranking / composite scores)
# ---------------------------------------------------------------------------


def rate_with_counts(successes: int, n: int) -> dict[str, Any]:
    """Numerator/denominator/point estimate + Wilson 95% CI (no ranking)."""
    from adapti_guard.evaluation.statistics import proportion_ci_wilson

    out: dict[str, Any] = {
        "numerator": int(successes),
        "denominator": int(n),
        "point_estimate": (successes / n) if n else None,
        "ci_95_wilson": None,
    }
    if n > 0:
        _p, lo, hi = proportion_ci_wilson(int(successes), int(n), ci=0.95)
        out["ci_95_wilson"] = {"low": lo, "high": hi}
    return out
