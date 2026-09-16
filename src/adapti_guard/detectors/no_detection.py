"""D0 — No detection baseline for P3."""

from __future__ import annotations

from adapti_guard.detectors.base import (
    DetectorResult,
    EpisodeDetectionContext,
    P3Detector,
    assert_no_forbidden_keys,
)


class NoDetectionDetector(P3Detector):
    """Always returns detector_hit=false. Isolates downstream policy effects."""

    detector_id = "D0"
    version = "p3.d0.1"

    def detect(self, ctx: EpisodeDetectionContext) -> DetectorResult:
        assert_no_forbidden_keys(ctx.to_dict())
        return DetectorResult(
            detector_id=self.detector_id,
            detector_hit=False,
            risk_signal=0.0,
            evidence=(),
            confidence=1.0,
            latency_ms=0.0,
            reason_code="no_detection",
            input_scope=ctx.input_scope,
            version=self.version,
        )
