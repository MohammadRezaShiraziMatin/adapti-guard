"""P3 detector registry and deferred candidates."""

from __future__ import annotations

from adapti_guard.detectors.base import P3Detector
from adapti_guard.detectors.current_detector import CurrentPhase1Detector
from adapti_guard.detectors.heuristic_detector import HeuristicTaxonomyDetector
from adapti_guard.detectors.no_detection import NoDetectionDetector
from adapti_guard.detectors.structured_context_detector import StructuredContextDetector

# D3 (semantic/embedding) is intentionally deferred: no offline local embedding
# stack is locked in this repo, and live external model/API calls are forbidden
# in the design phase.
DEFERRED_DETECTORS = {
    "D3": {
        "status": "DEFERRED_NO_OFFLINE_IMPL",
        "reason": (
            "Semantic/embedding detector requires a locked offline embedding "
            "dependency or would need live external model/API calls. Not "
            "implemented as a placeholder that appears scientifically operational."
        ),
    }
}


def default_p3_detectors() -> dict[str, P3Detector]:
    """Return the offline-operational P3 detector set (D0/D1/D2/D4)."""
    return {
        "D0": NoDetectionDetector(),
        "D1": CurrentPhase1Detector(),
        "D2": HeuristicTaxonomyDetector(),
        "D4": StructuredContextDetector(),
    }


def list_detector_catalog() -> list[dict]:
    cats = []
    for det in default_p3_detectors().values():
        cats.append(
            {
                "detector_id": det.detector_id,
                "version": det.version,
                "config_hash": det.config_hash(),
                "status": "OFFLINE_OPERATIONAL",
            }
        )
    for did, meta in DEFERRED_DETECTORS.items():
        cats.append({"detector_id": did, **meta})
    return cats
