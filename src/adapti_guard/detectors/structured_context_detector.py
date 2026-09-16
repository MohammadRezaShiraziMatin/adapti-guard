"""D4 — Structured/context detector (deterministic agentic provenance cues).

Uses only channels/state available at detection time:
untrusted source, tool-output origin, memory provenance markers,
privilege tool names, and simple tool-chain transitions.
No live model / embedding dependency.
"""

from __future__ import annotations

from adapti_guard.detectors.base import (
    DetectorResult,
    EpisodeDetectionContext,
    P3Detector,
    assert_no_forbidden_keys,
)

PRIVILEGED_TOOLS = frozenset({"send_email", "create_record", "retrieve_document"})
UNTRUSTED_CHANNELS = frozenset({"tool_output", "untrusted", "injected", "external"})


class StructuredContextDetector(P3Detector):
    """Deterministic structured cues for agentic context."""

    detector_id = "D4"
    version = "p3.d4.structured.1"

    def config_dict(self) -> dict:
        return {
            "detector_id": self.detector_id,
            "version": self.version,
            "privileged_tools": sorted(PRIVILEGED_TOOLS),
            "untrusted_channels": sorted(UNTRUSTED_CHANNELS),
            "signals": [
                "untrusted_source",
                "tool_output_present",
                "memory_provenance_marker",
                "privileged_tool",
                "tool_chain_transition",
            ],
        }

    def detect(self, ctx: EpisodeDetectionContext) -> DetectorResult:
        assert_no_forbidden_keys(ctx.to_dict())
        evidence: list[str] = []
        state = dict(ctx.state or {})

        channel = (ctx.source_channel or "").lower().strip()
        if channel in UNTRUSTED_CHANNELS:
            evidence.append("untrusted_source")

        if ctx.tool_output:
            evidence.append("tool_output_present")

        context = ctx.context or ""
        if "MEMORY:" in context or "memory_write" in context.lower():
            # Provenance: memory content already visible in context string.
            evidence.append("memory_provenance_marker")

        if ctx.tool_name and ctx.tool_name in PRIVILEGED_TOOLS:
            evidence.append("privileged_tool")

        prior_tool = state.get("last_tool_name")
        if (
            prior_tool
            and ctx.tool_name
            and str(prior_tool) != str(ctx.tool_name)
            and str(ctx.tool_name) in PRIVILEGED_TOOLS
        ):
            evidence.append("tool_chain_transition")

        # Escalation cue in visible text (not future labels).
        text = f"{context}\n{ctx.current_input or ''}".lower()
        if "grant-" in text or "authz_token" in text or "privilege" in text:
            evidence.append("privilege_escalation_cue")

        hit = bool(evidence)
        risk = min(1.0, 0.2 * len(set(evidence)))
        return DetectorResult(
            detector_id=self.detector_id,
            detector_hit=hit,
            risk_signal=float(risk),
            evidence=tuple(sorted(set(evidence))),
            confidence=float(risk) if hit else 0.0,
            latency_ms=0.0,
            reason_code="structured_hit" if hit else "structured_clear",
            input_scope=ctx.input_scope,
            version=self.version,
        )
