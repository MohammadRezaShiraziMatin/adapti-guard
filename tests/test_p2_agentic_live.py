"""Offline tests for P2 live Stage-A runner helpers and CLI gates.

API calls = 0. No OpenRouter. No network.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adapti_guard.evaluation.target_model import MockTargetModel
from adapti_guard.experiments.p2_agentic_live import (
    LOCKED_JUDGE,
    LOCKED_TARGET,
    PACK_SHA256,
    P1_SHA256,
    PRIMARY_ARMS,
    SMOKE_CORE_ID,
    SMOKE_SEED,
    SMOKE_TRAJECTORY_IDS,
    LiveRunStats,
    P2LiveGateError,
    build_run_manifest,
    evaluate_trajectory_live,
    load_p2_pack,
    preflight,
    redact_secrets,
    score_stage_a_results,
    smoke_subset,
    stage_a_arm_schedule,
    verify_pack_invariants,
    verify_p1_integrity,
)

SCRIPT = ROOT / "scripts" / "run_p2_agentic_live.py"


def test_frozen_sha_gate():
    info = verify_pack_invariants()
    assert info["dataset_hash"] == PACK_SHA256
    assert info["status"] == "FROZEN"
    assert info["live_evaluated"] is False
    digest = hashlib.sha256(
        (ROOT / "datasets/frozen/p2_agentic_v0.1.0/dataset.jsonl").read_bytes()
    ).hexdigest()
    assert digest == PACK_SHA256


def test_p1_integrity_unchanged():
    info = verify_p1_integrity()
    assert info["p1_sha256"] == P1_SHA256


def test_preflight_ok_offline():
    info = preflight(require_key=False)
    assert info["status"] == "PREFLIGHT_OK"
    assert info["cache_enabled"] is False
    assert info["target_model"] == LOCKED_TARGET
    assert info["judge_model"] == LOCKED_JUDGE
    assert info["api_calls_allowed"] is False
    assert info["smoke_seed"] == SMOKE_SEED
    assert list(info["smoke_trajectory_ids"]) == list(SMOKE_TRAJECTORY_IDS)


def test_preflight_require_key_fail_closed(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(P2LiveGateError) as exc:
        preflight(require_key=True)
    assert exc.value.status == "INVALID_MISSING_KEYS"


def test_smoke_selection_deterministic():
    rows = load_p2_pack()
    a = [r["id"] for r in smoke_subset(rows)]
    b = [r["id"] for r in smoke_subset(rows)]
    assert a == b == list(SMOKE_TRAJECTORY_IDS)
    assert 6 <= len(a) <= 8
    assert SMOKE_CORE_ID in a
    assert "p2a_hn_001" in a
    assert "p2a_ben_001" in a


def test_policy_selection_schedule():
    sched = stage_a_arm_schedule()
    assert set(sched.keys()) == set(PRIMARY_ARMS)
    assert set(sched["B0"]) == set(SMOKE_TRAJECTORY_IDS)
    assert sched["STATIC-A1"] == (SMOKE_CORE_ID,)
    assert sched["PHASE1-CORE"] == (SMOKE_CORE_ID,)
    assert "ORACLE_RISK" not in sched
    assert "ORACLE_BLOCK" not in sched


def test_cli_stage_flag_gate_no_live_by_default():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env={**os.environ},
    )
    assert proc.returncode == 0
    assert "STATUS=PREFLIGHT_OK" in proc.stdout
    assert "STATUS=NO_LIVE_EXECUTION" in proc.stdout


def test_cli_stage_a_requires_smoke():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--stage-a"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 2
    assert "STATUS=STOP_SMOKE_REQUIRED" in proc.stdout


def test_cli_smoke_requires_stage_a():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--smoke"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 2
    assert "STATUS=STOP_STAGE_A_REQUIRED" in proc.stdout


def test_cli_stage_b_refused():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--stage-b"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 2
    assert "STATUS=STOP_STAGE_B_REQUIRES_HUMAN_APPROVAL" in proc.stdout


def test_trajectory_isolation_and_multi_turn_state():
    rows = {r["id"]: r for r in load_p2_pack()}
    stats = LiveRunStats()
    # Two independent evals of same trajectory must not share memory.
    r1 = evaluate_trajectory_live(
        rows["p2a_atk_001"],
        "B0",
        target=None,
        judge=None,
        tool_mode="scripted_only",
        call_judge=True,
        stats=stats,
    )
    r2 = evaluate_trajectory_live(
        rows["p2a_atk_001"],
        "B0",
        target=None,
        judge=None,
        tool_mode="scripted_only",
        call_judge=True,
        stats=LiveRunStats(),
    )
    assert r1["n_turns"] >= 3
    assert r1["final_state"]["memory"].get("authz_token") == "GRANT-OPS-ALPHA"
    assert r2["final_state"]["memory"].get("authz_token") == "GRANT-OPS-ALPHA"
    # Persistence visible across turns inside one episode
    mem_seen = False
    for t in r1["turns"]:
        if t["OBSERVED"].get("memory_reads", {}).get("authz_token") == "GRANT-OPS-ALPHA":
            mem_seen = True
    assert mem_seen
    assert r1["tool_hasr_success"] is True
    assert r1["judge_asr_success"] is None  # judge not provided → UNKNOWN


def test_tool_trace_generation_and_policy_application():
    rows = {r["id"]: r for r in load_p2_pack()}
    b0 = evaluate_trajectory_live(
        rows[SMOKE_CORE_ID],
        "B0",
        tool_mode="scripted_only",
        call_judge=False,
    )
    assert b0["n_security_events"] >= 1
    assert any(e.get("tool_name") == "create_record" for e in b0["security_events"])
    # Scripted intervention_action from pack must be ignored (not forced A0-only path)
    assert "ignored_scripted_intervention" in b0["turns"][0]["DERIVED"]


def test_invalid_live_tool_arguments_do_not_crash_episode():
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
    assert out["n_security_events"] >= 1
    assert any(
        e.get("reason") == "invalid_tool_arguments" for e in out["security_events"]
    )


def test_live_target_injection_scripted_preferred():
    rows = {r["id"]: r for r in load_p2_pack()}
    mock = MockTargetModel(
        response='TOOL_REQUEST: {"name":"create_record","arguments":{"kind":"p2_authz_override","payload":"GRANT-OPS-ALPHA"}}',
        tool_call={
            "name": "create_record",
            "arguments": {"kind": "p2_authz_override", "payload": "GRANT-OPS-ALPHA"},
        },
    )
    out = evaluate_trajectory_live(
        rows["p2a_atk_001"],
        "B0",
        target=mock,
        judge=None,
        tool_mode="scripted_preferred",
        call_judge=False,
    )
    assert mock.calls  # target was invoked
    assert out["tool_hasr_success"] is True


def test_manifest_generation_fields():
    man = build_run_manifest(run_id="test_run", stage="A_smoke")
    required = {
        "run_id",
        "timestamp",
        "git_commit",
        "dataset_hash",
        "pack_id",
        "p1_sha256",
        "target_model",
        "judge_model",
        "backend",
        "temperature",
        "cache_enabled",
        "baselines",
        "smoke_seed",
        "trajectory_ids",
        "live_harness_version",
    }
    assert required.issubset(man.keys())
    assert man["dataset_hash"] == PACK_SHA256
    assert man["p1_sha256"] == P1_SHA256
    assert man["cache_enabled"] is False
    assert man["temperature"] == 0.0
    assert man["scientific_evidence"] is False
    assert "OPENROUTER_API_KEY" not in json.dumps(man)


def test_secret_redaction():
    raw = "Authorization: Bearer sk-abcdefghijklmnopqrstuvwxyz api_key=secret123"
    red = redact_secrets(raw)
    assert "sk-abcdefghijklmnopqrstuvwxyz" not in red
    assert "secret123" not in red
    assert "REDACTED" in red


def test_retry_accounting_on_target_error():
    class Flaky(MockTargetModel):
        def __init__(self):
            super().__init__(response="ok")
            self.n = 0

        def generate(self, request):
            from adapti_guard.evaluation.target_model import GenerationResult

            self.n += 1
            self.calls.append(request)
            if self.n == 1:
                return GenerationResult(
                    text="",
                    model_id="mock",
                    latency_ms=0.0,
                    error="temporary",
                    raw={},
                )
            return GenerationResult(
                text='TOOL_REQUEST: {"name":"search","arguments":{"query":"x"}}',
                model_id="mock",
                latency_ms=0.0,
                raw={"tool_call": {"name": "search", "arguments": {"query": "x"}}},
            )

    rows = {r["id"]: r for r in load_p2_pack()}
    stats = LiveRunStats()
    evaluate_trajectory_live(
        rows["p2a_atk_011"],
        "B0",
        target=Flaky(),
        judge=None,
        tool_mode="scripted_preferred",
        call_judge=False,
        stats=stats,
    )
    assert stats.n_target_retries >= 1
    assert stats.n_target_calls >= 1


def test_cache_off_enforced_in_preflight_and_manifest():
    info = preflight(require_key=False)
    assert info["cache_enabled"] is False
    man = build_run_manifest(run_id="x")
    assert man["cache_enabled"] is False


def test_fail_closed_unsupported_tool():
    rows = {r["id"]: r for r in load_p2_pack()}
    bad = json.loads(json.dumps(rows["p2a_atk_001"]))
    # Corrupt a tool name on activation turn
    for t in bad["turns"]:
        if t.get("agent_tool_call"):
            t["agent_tool_call"]["name"] = "not_a_real_tool"
            break
    with pytest.raises(P2LiveGateError) as exc:
        evaluate_trajectory_live(
            bad,
            "B0",
            tool_mode="scripted_only",
            call_judge=False,
        )
    assert exc.value.status == "STOP_UNSUPPORTED_TOOL"


def test_score_bundle_separates_tool_hasr_and_judge_asr():
    rows = {r["id"]: r for r in load_p2_pack()}
    results = []
    for tid in SMOKE_TRAJECTORY_IDS:
        results.append(
            evaluate_trajectory_live(
                rows[tid],
                "B0",
                tool_mode="scripted_only",
                call_judge=False,
            )
        )
    scored = score_stage_a_results(results, policy="B0")
    assert "bundle" in scored
    # compute_p2_security_bundle nests metrics under "Tool-HASR" / "Judge-ASR"
    assert scored["bundle"]["Tool-HASR"]["metric"] == "Tool-HASR"
    assert scored["bundle"]["Judge-ASR"]["metric"] == "Judge-ASR"
    assert scored["scientific_evidence"] is False
