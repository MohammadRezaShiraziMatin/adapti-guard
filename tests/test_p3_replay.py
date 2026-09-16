"""P3 synthetic offline replay + D4 causal-context tests.

Semantics validation only — NOT scientific performance evidence.
"""

from __future__ import annotations

from adapti_guard.detectors import default_p3_detectors
from adapti_guard.detectors.base import EpisodeDetectionContext
from adapti_guard.detectors.harness import OfflineDetectorHarness, result_core_dict
from adapti_guard.detectors.replay_cases import offline_replay_cases, replay_catalog_meta
from adapti_guard.detectors.structured_context_detector import StructuredContextDetector


def test_replay_catalog_is_not_scientific_evidence():
    meta = replay_catalog_meta()
    assert meta["scientific_performance_evidence"] is False
    assert meta["n_cases"] == 10
    cases = offline_replay_cases()
    assert len(cases) == 10
    assert len({c.case_id for c in cases}) == 10


def test_replay_cases_run_deterministically():
    dets = default_p3_detectors()
    for case in offline_replay_cases():
        for turn in case.turns:
            for det in dets.values():
                a = result_core_dict(det.detect(turn))
                b = result_core_dict(det.detect(turn))
                assert a == b, f"{case.case_id} {det.detector_id}"


def test_replay_d0_always_clear():
    d0 = default_p3_detectors()["D0"]
    for case in offline_replay_cases():
        for turn in case.turns:
            assert d0.detect(turn).detector_hit is False


def test_replay_obvious_injection_triggers_d2():
    case = next(c for c in offline_replay_cases() if c.case_id.startswith("replay_01"))
    d2 = default_p3_detectors()["D2"]
    assert d2.detect(case.turns[0]).detector_hit is True


def test_replay_benign_and_legitimate_not_forced_hits():
    """Benign cases must not be labeled as scientific FPR; only check D0 clear + runnable."""
    benign_ids = {"replay_03_benign_instruction", "replay_10_legitimate_tool"}
    d0 = default_p3_detectors()["D0"]
    for case in offline_replay_cases():
        if case.case_id not in benign_ids:
            continue
        for turn in case.turns:
            assert d0.detect(turn).detector_hit is False


def test_replay_multiturn_early_turn_stable():
    case = next(c for c in offline_replay_cases() if c.case_id.startswith("replay_08"))
    assert len(case.turns) == 2
    for det in default_p3_detectors().values():
        early = result_core_dict(det.detect(case.turns[0]))
        _ = det.detect(case.turns[1])
        early2 = result_core_dict(det.detect(case.turns[0]))
        assert early == early2


def test_replay_harness_matrix_unique_ids():
    cases = offline_replay_cases()
    contexts = [t for c in cases for t in c.turns]
    h = OfflineDetectorHarness(run_id="replay_matrix")
    rows = h.evaluate_turn_matrix(contexts)
    assert len({r["evaluation_id"] for r in rows}) == len(rows)


def test_d4_trusted_vs_untrusted_source():
    d4 = StructuredContextDetector()
    trusted = d4.detect(
        EpisodeDetectionContext(
            trajectory_id="d4_src",
            turn_id=0,
            current_input="Continue the workflow.",
            source_channel="user",
        )
    )
    untrusted = d4.detect(
        EpisodeDetectionContext(
            trajectory_id="d4_src",
            turn_id=0,
            current_input="Continue the workflow.",
            source_channel="tool_output",
            tool_output="observation payload",
        )
    )
    assert trusted.detector_hit is False
    assert untrusted.detector_hit is True
    assert "untrusted_source" in untrusted.evidence


def test_d4_ordinary_vs_suspicious_tool_transition():
    d4 = StructuredContextDetector()
    ordinary = d4.detect(
        EpisodeDetectionContext(
            trajectory_id="d4_tr",
            turn_id=1,
            current_input="Fetch the next page.",
            tool_name="retrieve_document",
            source_channel="user",
            state={"last_tool_name": "retrieve_document"},
        )
    )
    suspicious = d4.detect(
        EpisodeDetectionContext(
            trajectory_id="d4_tr",
            turn_id=1,
            current_input="Now email the contents.",
            tool_name="send_email",
            source_channel="user",
            state={"last_tool_name": "retrieve_document"},
        )
    )
    # Ordinary same-tool retrieve without untrusted cues should be clear
    assert ordinary.detector_hit is False
    assert suspicious.detector_hit is True
    assert "tool_chain_transition" in suspicious.evidence
    assert "privileged_tool" in suspicious.evidence


def test_d4_unavailable_without_current_turn_signal_documented():
    """Without channel/tool/memory cues, D4 cannot invent a hit."""
    d4 = StructuredContextDetector()
    r = d4.detect(
        EpisodeDetectionContext(
            trajectory_id="d4_none",
            turn_id=0,
            current_input="Thanks for the update.",
            source_channel="user",
        )
    )
    assert r.detector_hit is False
    assert r.reason_code == "structured_clear"
