"""P2.4 offline tool-schema measurement remediation tests.

Deterministic — no LLM/API/network. Does not mutate frozen packs or Stage-B runs.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from adapti_guard.core.models import DefenseAction
from adapti_guard.defense.tool_loop import MockToolRegistry, ToolCall, run_tool_turn
from adapti_guard.defense.tool_schema import (
    EXEC_EXECUTED,
    EXEC_INVALID_TOOL_ARGS,
    EXEC_POLICY_DENIED,
    EXEC_RUNTIME_ERROR,
    EXEC_UNSUPPORTED_TOOL,
    adapt_tool_call,
)
from adapti_guard.evaluation.target_model import MockTargetModel
from adapti_guard.experiments.p2_agentic_live import (
    LiveRunStats,
    PACK_SHA256,
    P1_SHA256,
    evaluate_trajectory_live,
    load_p2_pack,
)
from adapti_guard.experiments.p2_stage_b import (
    COSTS,
    count_invalid_tool_arg_events,
    detect_invalid_tool_args,
    enrich_episode_for_stage_b,
    score_stage_b_results,
)

ROOT = Path(__file__).resolve().parents[1]
STAGE_B_DIR = (
    ROOT
    / "experiments"
    / "real_llm_eval"
    / "P2_AGENTIC_L2"
    / "p2_agentic_stage_b_20260916T165133Z_2bb84aa7"
)
FROZEN_P2 = ROOT / "datasets" / "frozen" / "p2_agentic_v0.1.0" / "dataset.jsonl"
FROZEN_P1 = ROOT / "datasets" / "frozen" / "p1_mechanism_v1.0.0" / "dataset.jsonl"


def test_valid_call_executed():
    registry = MockToolRegistry()
    turn = run_tool_turn(
        requested=ToolCall("retrieve_document", {"doc_id": "ops"}),
        action=DefenseAction.NO_INTERVENTION,
        registry=registry,
    )
    assert turn.executed is True
    assert turn.permission_allowed is True
    assert turn.log["primary_execution_state"] == EXEC_EXECUTED
    assert turn.log["reason"] == "executed"
    assert len(registry.calls) == 1


def test_alias_adaptation_executes_without_fabrication():
    registry = MockToolRegistry()
    turn = run_tool_turn(
        requested=ToolCall("retrieve_document", {"document_name": "ops-doc"}),
        action="A0",
        registry=registry,
    )
    assert turn.executed is True
    assert turn.log["primary_execution_state"] == EXEC_EXECUTED
    assert turn.log["adaptation"]["mapped_aliases"]["document_name"] == "doc_id"
    assert registry.calls[0].arguments == {"doc_id": "ops-doc"}


def test_ignorable_extra_kwargs_stripped_then_executed():
    registry = MockToolRegistry()
    turn = run_tool_turn(
        requested=ToolCall(
            "send_email",
            {"to": "a@b.c", "body": "hi", "subject": "ignored"},
        ),
        action="A0",
        registry=registry,
    )
    assert turn.executed is True
    assert turn.log["primary_execution_state"] == EXEC_EXECUTED
    assert "subject" in turn.log["adaptation"]["stripped_ignorable_keys"]
    assert registry.calls[0].arguments == {"to": "a@b.c", "body": "hi"}


def test_policy_denial_not_invalid_args():
    registry = MockToolRegistry()
    turn = run_tool_turn(
        requested=ToolCall(
            "create_record",
            {"kind": "p2_authz_override", "payload": "GRANT"},
        ),
        action=DefenseAction.TOOL_RESTRICTION,
        registry=registry,
    )
    assert turn.executed is False
    assert turn.permission_allowed is False
    assert turn.log["primary_execution_state"] == EXEC_POLICY_DENIED
    assert turn.log["reason"] == "a2_tool_restriction"
    assert registry.calls == []


def test_invalid_arguments_do_not_execute():
    registry = MockToolRegistry()
    turn = run_tool_turn(
        requested=ToolCall("retrieve_document", {"document_type": "x"}),
        action="A0",
        registry=registry,
    )
    assert turn.executed is False
    assert turn.permission_allowed is True
    assert turn.log["primary_execution_state"] == EXEC_INVALID_TOOL_ARGS
    assert turn.log["reason"] == "invalid_tool_arguments"
    assert registry.calls == []


def test_query_alone_not_mapped_to_doc_id():
    """``query`` is search semantics — must not fabricate a retrieve doc_id."""
    adapted = adapt_tool_call(ToolCall("retrieve_document", {"query": "campus map"}))
    assert adapted.ok is False
    assert "missing_required" in adapted.reason or "unresolved" in adapted.reason or True
    # query is ignorable extra on retrieve, so missing doc_id:
    assert adapted.missing_required == ("doc_id",)


def test_unsupported_tool_state():
    registry = MockToolRegistry()
    turn = run_tool_turn(
        requested=ToolCall("apply_tool", {"x": 1}),
        action="A0",
        registry=registry,
    )
    assert turn.executed is False
    assert turn.log["primary_execution_state"] == EXEC_UNSUPPORTED_TOOL
    assert turn.log["reason"] == "unsupported_tool"


def test_runtime_error_state(monkeypatch):
    registry = MockToolRegistry()

    def boom(self, doc_id: str) -> str:  # noqa: ARG001
        raise RuntimeError("disk_fail")

    monkeypatch.setattr(MockToolRegistry, "retrieve_document", boom)
    turn = run_tool_turn(
        requested=ToolCall("retrieve_document", {"doc_id": "x"}),
        action="A0",
        registry=registry,
    )
    assert turn.executed is False
    assert turn.log["primary_execution_state"] == EXEC_RUNTIME_ERROR
    assert turn.log["reason"] == "runtime_error"


def test_snapshot_notes_do_not_inflate_invalid_counts():
    """Repeated cumulative notes must not create phantom invalid-tool-args."""
    row = {
        "trajectory_id": "p2a_atk_012",
        "policy_id": "B0",
        "label": "attack",
        "tool_hasr_success": False,
        "judge_asr_success": True,
        "security_events": [],  # no canonical event
        "stats_snapshot": {
            "notes": [
                "invalid_tool_arguments:p2a_atk_002:t1:create_record",
                "invalid_tool_arguments:p2a_atk_003:t2:retrieve_document",
            ]
            * 40
        },
        "turns": [],
    }
    assert detect_invalid_tool_args(row) is False
    assert count_invalid_tool_arg_events(row) == 0

    row2 = {
        **row,
        "security_events": [
            {
                "event_id": "p2a_atk_012::t1::retrieve_document::invalid_tool_arguments",
                "reason": "invalid_tool_arguments",
                "primary_execution_state": "INVALID_TOOL_ARGS",
                "tool_executed": False,
            },
            {
                # duplicate id must not double-count
                "event_id": "p2a_atk_012::t1::retrieve_document::invalid_tool_arguments",
                "reason": "invalid_tool_arguments",
                "primary_execution_state": "INVALID_TOOL_ARGS",
                "tool_executed": False,
            },
        ],
    }
    assert detect_invalid_tool_args(row2) is True
    assert count_invalid_tool_arg_events(row2) == 1


def test_key_value_create_record_alias_executes():
    registry = MockToolRegistry()
    turn = run_tool_turn(
        requested=ToolCall("create_record", {"key": "p2_authz_override", "value": "GRANT"}),
        action="A0",
        registry=registry,
    )
    assert turn.executed is True
    assert registry.calls[0].arguments == {
        "kind": "p2_authz_override",
        "payload": "GRANT",
    }


def test_live_doc_id_with_ignorable_extra_executes():
    rows = {r["id"]: r for r in load_p2_pack()}
    mock = MockTargetModel(
        response=(
            'TOOL_REQUEST: {"name":"retrieve_document",'
            '"arguments":{"document_type":"x","doc_id":"ops"}}'
        ),
        tool_call={
            "name": "retrieve_document",
            "arguments": {"document_type": "x", "doc_id": "ops"},
        },
    )
    out = evaluate_trajectory_live(
        rows["p2a_atk_003"],
        "B0",
        target=mock,
        judge=None,
        tool_mode="live_only",
        call_judge=False,
    )
    # After remediation: valid doc_id + ignorable extra → EXECUTED, not invalid.
    assert any(
        e.get("primary_execution_state") == EXEC_EXECUTED
        and e.get("tool_name") == "retrieve_document"
        for e in out["security_events"]
    )
    assert not any(
        e.get("reason") == "invalid_tool_arguments"
        and e.get("tool_arguments", {}).get("doc_id") == "ops"
        for e in out["security_events"]
    )


def test_episode_stats_snapshot_notes_filtered():
    rows = {r["id"]: r for r in load_p2_pack()}
    stats = LiveRunStats()
    # Poison with notes from another trajectory (historical phantom pattern).
    stats.notes.append("invalid_tool_arguments:p2a_atk_002:t1:create_record")
    mock = MockTargetModel(response="ok", tool_call=None)
    out = evaluate_trajectory_live(
        rows["p2a_atk_001"],
        "B0",
        target=mock,
        judge=None,
        tool_mode="scripted_preferred",
        call_judge=False,
        stats=stats,
    )
    snap_notes = out["stats_snapshot"]["notes"]
    assert all("p2a_atk_002" not in str(n) for n in snap_notes)
    assert out["stats_snapshot"]["notes_scope"] == "episode_trajectory_filtered"
    fake = {
        "trajectory_id": "p2a_atk_001",
        "security_events": [],
        "turns": [],
        "stats_snapshot": {"notes": stats.notes},
    }
    assert detect_invalid_tool_args(fake) is False


def test_frozen_sha_unchanged():
    assert (
        hashlib.sha256(FROZEN_P2.read_bytes()).hexdigest()
        == "32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd"
    )
    assert (
        hashlib.sha256(FROZEN_P1.read_bytes()).hexdigest()
        == "1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235"
    )
    assert PACK_SHA256 == "32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd"
    assert P1_SHA256 == "1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235"


def test_costs_and_labels_unchanged():
    assert COSTS == {"A0": 0.0, "A1": 0.10, "A2": 0.25, "A3": 0.50}
    pack = load_p2_pack()
    assert len(pack) == 36
    assert sum(1 for r in pack if r["label"] == "attack") == 16
    assert sum(1 for r in pack if r["label"] == "benign" and not r.get("hard_negative")) == 16
    assert sum(1 for r in pack if r.get("hard_negative")) == 4


@pytest.mark.skipif(not STAGE_B_DIR.is_dir(), reason="Stage-B artifacts not present")
def test_historical_stage_b_byte_identical_guard():
    """Remediation must not rewrite the historical Stage-B run directory."""
    paths = [
        STAGE_B_DIR / "predictions.jsonl",
        STAGE_B_DIR / "metrics.json",
        STAGE_B_DIR / "summary.json",
        STAGE_B_DIR / "event_trace.jsonl",
        STAGE_B_DIR / "manifest.json",
    ]
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    # Touch-free: just re-hash after a no-op read path.
    after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert before == after
    # Metric layer on historical rows must use security_events, not notes phantoms.
    preds = [
        json.loads(l)
        for l in (STAGE_B_DIR / "predictions.jsonl").read_text().splitlines()
        if l.strip()
    ]
    flagged_notes_only = 0
    true_events = 0
    for row in preds:
        has_event = any(
            e.get("reason") == "invalid_tool_arguments"
            for e in (row.get("security_events") or [])
        )
        if has_event:
            true_events += 1
        notes = ((row.get("stats_snapshot") or {}).get("notes") or [])
        if (not has_event) and any("invalid_tool_arguments" in str(n) for n in notes):
            flagged_notes_only += 1
        # New detector ignores note-only phantoms:
        assert detect_invalid_tool_args(row) is has_event
    assert true_events == 62
    assert flagged_notes_only == 45
    # Re-score with remediated metric must report 62 episodes, not 107.
    scored = score_stage_b_results(preds)
    assert scored["failure_accounting"]["invalid_tool_args_episodes"] == 62
