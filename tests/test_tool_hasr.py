"""Offline tests for P2 Tool-HASR / Judge-ASR metrics. No API."""

from __future__ import annotations

from adapti_guard.metrics.tool_hasr import (
    compute_judge_asr,
    compute_p2_security_bundle,
    compute_tool_hasr,
    disagreement_rows,
)


def test_tool_hasr_basic():
    rows = [
        {"id": "a1", "label": "attack", "tool_hasr_success": True},
        {"id": "a2", "label": "attack", "tool_hasr_success": False},
        {"id": "b1", "label": "benign", "tool_hasr_success": False},
    ]
    m = compute_tool_hasr(rows)
    assert m["n_attack"] == 2
    assert m["n_success"] == 1
    assert m["rate"] == 0.5


def test_tool_hasr_unknown_excluded_by_default():
    rows = [
        {"id": "a1", "label": "attack", "tool_hasr_success": True},
        {"id": "a2", "label": "attack", "tool_hasr_success": None},
        {"id": "a3", "label": "attack", "tool_hasr_success": False},
    ]
    m = compute_tool_hasr(rows, exclude_unknown=True)
    assert m["n_unknown"] == 1
    assert m["denominator"] == 2
    assert m["rate"] == 0.5
    m2 = compute_tool_hasr(rows, exclude_unknown=False)
    assert m2["denominator"] == 3
    assert abs(m2["rate"] - (1 / 3)) < 1e-9


def test_judge_asr_and_disagreement():
    rows = [
        {
            "id": "m3",
            "label": "attack",
            "tool_hasr_success": False,
            "judge_asr_success": True,
        },
        {
            "id": "m4",
            "label": "attack",
            "tool_hasr_success": True,
            "judge_asr_success": False,
        },
        {
            "id": "ok",
            "label": "attack",
            "tool_hasr_success": True,
            "judge_asr_success": True,
        },
    ]
    j = compute_judge_asr(rows)
    assert j["n_success"] == 2
    assert abs(j["rate"] - (2 / 3)) < 1e-9
    d = disagreement_rows(rows)
    assert len(d) == 2
    patterns = {x["pattern"] for x in d}
    assert "M3_judge_success_tool_not_executed" in patterns
    assert "M4_tool_executed_judge_not_success" in patterns


def test_security_bundle_keeps_axes_separate():
    rows = [
        {
            "id": "a1",
            "label": "attack",
            "family": "A1",
            "tool_hasr_success": True,
            "judge_asr_success": True,
            "final_action": "A0",
            "detector_hit": False,
        },
        {
            "id": "t1",
            "label": "benign",
            "hard_negative": False,
            "utility_success": True,
            "final_action": "A0",
        },
        {
            "id": "h1",
            "label": "benign",
            "hard_negative": True,
            "utility_success": False,
            "final_action": "A3",
            "fpr_event": True,
        },
    ]
    b = compute_p2_security_bundle(rows)
    assert "Tool-HASR" in b and "Judge-ASR" in b
    assert b["utility_hard_negative"] == 0.0
    assert b["hard_negative_FPR"] == 1.0
    assert b["benign_twin_FPR"] == 0.0
    assert b["delta_ToolHASR_minus_JudgeASR"] == 0.0
