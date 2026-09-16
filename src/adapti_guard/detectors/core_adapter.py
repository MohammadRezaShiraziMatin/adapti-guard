"""Adapt a P3Detector to the CORE ``detect_episode`` duck type.

Does not retune PHASE1-CORE risk/policy thresholds. Non-calibrated detectors that
return ``detector_hit=True`` with ``risk_signal < 0.25`` are floored to 0.25 so the
frozen CORE ``DetectionResult.is_injection`` threshold can consume binary hits.
"""

from __future__ import annotations

from adapti_guard.core.models import DetectionResult
from adapti_guard.detectors.base import EpisodeDetectionContext, P3Detector


class P3CoreDetectorAdapter:
    """Duck-typed wrapper: ``detect_episode(...) -> DetectionResult``."""

    def __init__(self, inner: P3Detector) -> None:
        self.inner = inner
        self.version = f"p3_adapter({inner.detector_id}:{inner.version})"

    def detect_episode(
        self,
        prompt: str,
        context: str | None = None,
        *,
        tool_name: str | None = None,
        tool_output: str | None = None,
    ) -> DetectionResult:
        ctx = EpisodeDetectionContext(
            trajectory_id="_live_",
            turn_id=0,
            current_input=prompt or "",
            context=context,
            tool_name=tool_name,
            tool_output=tool_output,
            source_channel="tool_output" if tool_output else "user",
            input_scope="current_turn",
        )
        result = self.inner.detect(ctx)
        prob = float(result.risk_signal)
        if result.detector_hit and prob < 0.25:
            # Binary / non-calibrated hit → actionable under frozen CORE threshold.
            prob = 0.25
        if not result.detector_hit:
            prob = min(prob, 0.249)
        indicators = list(result.evidence) or (
            [result.reason_code] if result.reason_code else []
        )
        return DetectionResult(
            injection_probability=prob,
            indicators=[str(x) for x in indicators],
        )
