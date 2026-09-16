"""D1 — Current PHASE1 detector wrapper (frozen as-is; not retuned)."""

from __future__ import annotations

from adapti_guard.detector.prompt_injection_detector_phase1 import (
    PromptInjectionDetectorPhase1,
)
from adapti_guard.detectors.base import (
    DetectorResult,
    EpisodeDetectionContext,
    P3Detector,
    assert_no_forbidden_keys,
)


class CurrentPhase1Detector(P3Detector):
    """Wraps ``PromptInjectionDetectorPhase1`` without threshold/retune changes."""

    detector_id = "D1"
    version = "p3.d1.evidence_phase1.0"

    def __init__(self, inner: PromptInjectionDetectorPhase1 | None = None) -> None:
        self._inner = inner or PromptInjectionDetectorPhase1()

    def config_dict(self) -> dict:
        return {
            "detector_id": self.detector_id,
            "version": self.version,
            "inner_version": getattr(self._inner, "version", "evidence_phase1.0"),
            "retuned": False,
        }

    def detect(self, ctx: EpisodeDetectionContext) -> DetectorResult:
        assert_no_forbidden_keys(ctx.to_dict())
        raw = self._inner.detect_episode(
            ctx.current_input,
            ctx.context,
            tool_name=ctx.tool_name,
            tool_output=ctx.tool_output,
        )
        hit = bool(raw.is_injection)
        indicators = tuple(str(x) for x in (raw.indicators or []))
        return DetectorResult(
            detector_id=self.detector_id,
            detector_hit=hit,
            risk_signal=float(raw.injection_probability),
            evidence=indicators,
            confidence=float(raw.injection_probability),
            latency_ms=0.0,
            reason_code="phase1_hit" if hit else "phase1_miss",
            input_scope=ctx.input_scope,
            version=self.version,
            metadata={"inner_version": getattr(self._inner, "version", "")},
        )
