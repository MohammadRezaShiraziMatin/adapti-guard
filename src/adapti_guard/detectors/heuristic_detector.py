"""D2 — Transparent pattern/heuristic detector (mechanism-taxonomy oriented).

Deterministic, offline, no ML/API. Documented rules — not a retune of PHASE1.
Known blind spots are intentional for scientific interpretability.
"""

from __future__ import annotations

import re
from typing import Any

from adapti_guard.detectors.base import (
    DetectorResult,
    EpisodeDetectionContext,
    P3Detector,
    assert_no_forbidden_keys,
)

# Explicit rule table (rule_id → compiled pattern, mechanism hint).
# Matching is case-insensitive substring/regex over current_input + context only.
HEURISTIC_RULES: tuple[dict[str, Any], ...] = (
    {
        "rule_id": "R_OVERRIDE",
        "mechanism_hint": "B4/C1",
        "pattern": re.compile(
            r"(ignore|disregard|override).{0,40}(instruction|system|policy|prior)",
            re.I,
        ),
        "blind_spot": "Paraphrases without keyword stems; quoted benign instructional text",
    },
    {
        "rule_id": "R_PRIVILEGE",
        "mechanism_hint": "C2/D1",
        "pattern": re.compile(
            r"\b(sudo(?:\s+mode)?|root\s+operator|temporary\s+admin|sudo_grant|"
            r"authz[_-]?token|privilege\s+escalat)\b",
            re.I,
        ),
        "blind_spot": "Novel privilege tokens not in this lexicon",
    },
    {
        "rule_id": "R_EXFIL",
        "mechanism_hint": "C3/C4",
        "pattern": re.compile(
            r"(exfil|send[_-]?email|leak|dump).{0,60}(secret|token|credential|password|outside)",
            re.I,
        ),
        "blind_spot": "Indirect exfil without email/secret keywords",
    },
    {
        "rule_id": "R_TOOL_INJECT",
        "mechanism_hint": "E3/tool_output",
        "pattern": re.compile(
            r"(tool[_-]?output|injected?\s+observation|untrusted\s+source|"
            r"from\s+the\s+tool\s+result)",
            re.I,
        ),
        "blind_spot": "Silent tool-output injection without lexical markers",
    },
    {
        "rule_id": "R_MEMORY_PLANT",
        "mechanism_hint": "persistence/durable_memory",
        "pattern": re.compile(
            r"(store|write|plant|persist).{0,40}(memory|authz|grant-|token\s*=)",
            re.I,
        ),
        "blind_spot": "Memory writes described without store/write verbs",
    },
    {
        "rule_id": "R_DELAYED_FIRE",
        "mechanism_hint": "delayed_activation",
        "pattern": re.compile(
            r"(later|next\s+turn|when\s+ready|delayed|after\s+confirm).{0,40}"
            r"(send|execute|trigger|fire)",
            re.I,
        ),
        "blind_spot": "Delayed activation without temporal cue words",
    },
)


class HeuristicTaxonomyDetector(P3Detector):
    """Rule-based detector with explicit taxonomy-oriented patterns."""

    detector_id = "D2"
    version = "p3.d2.heuristic.1"

    def __init__(self, rules: tuple[dict[str, Any], ...] | None = None) -> None:
        self.rules = rules or HEURISTIC_RULES

    def config_dict(self) -> dict:
        return {
            "detector_id": self.detector_id,
            "version": self.version,
            "n_rules": len(self.rules),
            "rule_ids": [r["rule_id"] for r in self.rules],
            "normalization": "none (raw text; case-insensitive regex)",
            "matching_semantics": "any-rule OR over current_input + context",
        }

    def detect(self, ctx: EpisodeDetectionContext) -> DetectorResult:
        assert_no_forbidden_keys(ctx.to_dict())
        text = f"{ctx.context or ''}\n{ctx.current_input or ''}"
        hits: list[str] = []
        mechanisms: list[str] = []
        for rule in self.rules:
            if rule["pattern"].search(text):
                hits.append(str(rule["rule_id"]))
                mechanisms.append(str(rule["mechanism_hint"]))
        hit = bool(hits)
        # Transparent risk: fraction of rules fired (not calibrated).
        risk = min(1.0, len(hits) / max(1, len(self.rules)) * 2.0) if hit else 0.0
        return DetectorResult(
            detector_id=self.detector_id,
            detector_hit=hit,
            risk_signal=float(risk),
            evidence=tuple(hits),
            confidence=float(risk) if hit else 0.0,
            latency_ms=0.0,
            reason_code="heuristic_match" if hit else "heuristic_clear",
            input_scope=ctx.input_scope,
            version=self.version,
            metadata={"mechanism_hints": mechanisms},
        )

    @staticmethod
    def documented_blind_spots() -> list[dict[str, str]]:
        return [
            {"rule_id": r["rule_id"], "blind_spot": r["blind_spot"]} for r in HEURISTIC_RULES
        ]
