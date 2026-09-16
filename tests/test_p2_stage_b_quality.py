"""Offline quality tests for P2 Stage-B evaluation infrastructure.

API calls = 0. No OpenRouter. No network. No Stage-B live execution.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adapti_guard.evaluation.target_model import MockTargetModel  # noqa: F401 — reserved
from adapti_guard.experiments.p2_agentic import (
    OfflinePolicy,
    P2AgenticHarness,
    trajectory_from_dict,
)
from adapti_guard.experiments.p2_agentic_live import (
    PACK_SHA256,
    P1_SHA256,
    PRIMARY_ARMS,
    P2LiveGateError,
    evaluate_trajectory_live,
    load_p2_pack,
)
from adapti_guard.experiments.p2_stage_b import (
    STAGE_B_EXPECTED_EPISODE_ARMS,
    OUTCOME_PREVENTED,
    OUTCOME_UNKNOWN,
    assert_episode_arm_coverage,
    assert_stage_b_pack_locked,
    assert_unique_output_dir,
    build_stage_b_manifest,
    classify_security_outcome,
    configuration_hash,
    detect_invalid_tool_args,
    enrich_episode_for_stage_b,
    expected_evaluation_ids,
    extract_multiturn_diagnostics,
    inventory_frozen_pack,
    make_evaluation_id,
    metric_with_wilson,
    paired_discordant_counts,
    parse_evaluation_id,
    prompt_template_hash,
    refuse_live_stage_b_without_approval,
    score_stage_b_results,
    stage_b_arm_schedule,
    tool_schema_hash,
    write_stage_b_artifact_bundle,
)
from adapti_guard.metrics.tool_hasr import COSTS, disagreement_rows

SCRIPT = ROOT / "scripts" / "run_p2_agentic_live.py"
VERIFY = ROOT / "scripts" / "verify_p2_stage_b_artifacts.py"


def _stub_episode(
    *,
    tid: str,
    policy: str,
    label: str,
    tool_hasr: bool | None,
    judge_asr: bool | None,
    action: str = "A0",
    hard_negative: bool = False,
    security_events: list | None = None,
    turns: list | None = None,
    utility_success: bool | None = None,
    harmful_prevented: bool = False,
    target_errors: list | None = None,
    runtime_error: bool = False,
) -> dict:
    return {
        "id": tid,
        "trajectory_id": tid,
        "label": label,
        "family": "C1",
        "mechanism": "C1",
        "hard_negative": hard_negative,
        "policy_key": policy,
        "success_condition": {"tool": "create_record", "args_match": {"payload": "X"}},
        "tool_hasr_success": tool_hasr,
        "judge_asr_success": judge_asr,
        "action": action,
        "final_action": action,
        "utility_success": utility_success,
        "fpr_event": action in {"A2", "A3"} and label == "benign",
        "harmful_action_prevented": harmful_prevented,
        "tool_prevented": harmful_prevented,
        "security_events": security_events or [],
        "turns": turns or [],
        "n_turns": len(turns or []),
        "n_harmful_executions": 1 if tool_hasr else 0,
        "target_errors": target_errors or [],
        "runtime_error": runtime_error,
        "judge": {
            "attack_success": judge_asr,
            "parse_error": None,
            "reason": "ok",
        },
        "adaptive_rewrites_used": 0,
        "metadata": {},
    }


def _full_pack_stubs(run_id: str = "p2_stage_b_offline_test") -> list[dict]:
    rows = load_p2_pack()
    out = []
    for r in rows:
        tid = str(r["id"])
        label = str(r["label"])
        hard = bool(r.get("hard_negative"))
        for pol in PRIMARY_ARMS:
            if label == "attack":
                th = pol == "B0"
                ja = True
                action = "A0" if pol == "B0" else ("A1" if pol == "STATIC-A1" else "A2")
                prevented = pol == "PHASE1-CORE"
                out.append(
                    _stub_episode(
                        tid=tid,
                        policy=pol,
                        label=label,
                        tool_hasr=th and not prevented,
                        judge_asr=ja,
                        action=action,
                        harmful_prevented=prevented,
                        security_events=[
                            {
                                "tool_name": "create_record",
                                "tool_arguments": {"payload": "X"},
                                "turn_id": 1,
                                "permission_allowed": not prevented,
                                "tool_executed": th and not prevented,
                                "harmful_action": th and not prevented,
                                "harmful_action_prevented": prevented,
                                "reason": "a2_tool_restriction" if prevented else "executed",
                            }
                        ],
                    )
                )
            else:
                out.append(
                    _stub_episode(
                        tid=tid,
                        policy=pol,
                        label="benign",
                        tool_hasr=False,
                        judge_asr=False,
                        action="A0",
                        hard_negative=hard,
                        utility_success=True,
                    )
                )
    assert len(out) == STAGE_B_EXPECTED_EPISODE_ARMS
    return [enrich_episode_for_stage_b(r, run_id=run_id) for r in out]


def test_inventory_and_pack_lock():
    inv = inventory_frozen_pack()
    assert inv["benchmark_sha256"] == PACK_SHA256
    assert inv["n_total"] == 36
    assert inv["n_attack"] == 16
    assert inv["n_benign_twin"] == 16
    assert inv["n_hard_negative"] == 4
    assert inv["live_evaluated"] is False
    assert inv["p1_integrity"]["p1_sha256"] == P1_SHA256
    locked = assert_stage_b_pack_locked()
    assert locked["sha_match"] is True
    assert len(locked["trajectory_ids"]) == 36
    assert len(set(locked["trajectory_ids"])) == 36


def test_stage_b_schedule_36x3():
    schedule = stage_b_arm_schedule()
    assert set(schedule) == set(PRIMARY_ARMS)
    for _arm, ids in schedule.items():
        assert len(ids) == 36
        assert len(set(ids)) == 36
    eids = expected_evaluation_ids("runX")
    assert len(eids) == 108
    assert len(set(eids)) == 108


def test_evaluation_id_roundtrip():
    eid = make_evaluation_id("run1", "p2a_atk_001", "B0")
    ident = parse_evaluation_id(eid)
    assert ident.run_id == "run1"
    assert ident.trajectory_id == "p2a_atk_001"
    assert ident.policy_id == "B0"
    with pytest.raises(P2LiveGateError):
        parse_evaluation_id("bad")


def test_duplicate_evaluation_id_fails():
    rows = _full_pack_stubs("run_dup")
    rows.append(dict(rows[0]))
    with pytest.raises(P2LiveGateError) as exc:
        assert_episode_arm_coverage(rows, run_id="run_dup")
    assert exc.value.status == "STOP_DUPLICATE_EVALUATION_ID"


def test_missing_and_extra_trajectory_fails():
    rows = _full_pack_stubs("run_miss")
    trimmed = [r for r in rows if r["trajectory_id"] != "p2a_atk_001"]
    with pytest.raises(P2LiveGateError) as exc:
        assert_episode_arm_coverage(trimmed, run_id="run_miss")
    assert exc.value.status == "STOP_STAGE_B_COVERAGE"

    extra = _full_pack_stubs("run_extra")
    extra[0] = enrich_episode_for_stage_b(
        {**extra[0], "trajectory_id": "p2a_atk_999", "id": "p2a_atk_999"},
        run_id="run_extra",
    )
    with pytest.raises(P2LiveGateError):
        assert_episode_arm_coverage(extra, run_id="run_extra")


def test_wrong_policy_count_fails():
    rows = [r for r in _full_pack_stubs("run_pol") if r["policy_id"] != "STATIC-A1"]
    with pytest.raises(P2LiveGateError):
        assert_episode_arm_coverage(rows, run_id="run_pol")


def test_tool_hasr_and_judge_asr_separation():
    rows = [
        _stub_episode(
            tid="a1",
            policy="B0",
            label="attack",
            tool_hasr=False,
            judge_asr=True,
            harmful_prevented=True,
            security_events=[
                {
                    "tool_name": "create_record",
                    "tool_arguments": {"payload": "X"},
                    "permission_allowed": False,
                    "tool_executed": False,
                    "harmful_action": False,
                    "harmful_action_prevented": True,
                }
            ],
        ),
        _stub_episode(
            tid="a2",
            policy="B0",
            label="attack",
            tool_hasr=True,
            judge_asr=False,
            security_events=[
                {
                    "tool_name": "create_record",
                    "tool_arguments": {"payload": "X"},
                    "permission_allowed": True,
                    "tool_executed": True,
                    "harmful_action": True,
                    "harmful_action_prevented": False,
                }
            ],
        ),
    ]
    metrics = score_stage_b_results(rows, run_id="sep")
    assert metrics["primary"]["estimand"] == "Tool-HASR"
    assert metrics["secondary"]["estimand"] == "Judge-ASR"
    assert metrics["primary"]["point_estimate"] == 0.5
    assert metrics["secondary"]["point_estimate"] == 0.5
    assert metrics["disagreements"]["n_M3"] == 1
    assert metrics["disagreements"]["n_M4"] == 1
    patterns = {d["pattern"] for d in disagreement_rows(rows)}
    assert "M3_judge_success_tool_not_executed" in patterns
    assert "M4_tool_executed_judge_not_success" in patterns


def test_invalid_tool_args_diagnostic_not_auto_defense():
    row = _stub_episode(
        tid="a1",
        policy="B0",
        label="attack",
        tool_hasr=False,
        judge_asr=False,
        security_events=[
            {
                "tool_name": "retrieve_document",
                "tool_arguments": {"document_type": "x"},
                "permission_allowed": True,
                "tool_executed": False,
                "harmful_action": False,
                "harmful_action_prevented": False,
                "reason": "invalid_tool_arguments",
            }
        ],
    )
    assert detect_invalid_tool_args(row) is True
    enriched = enrich_episode_for_stage_b(row, run_id="inv")
    assert enriched["invalid_tool_args"] is True
    assert enriched["security_outcome"] != OUTCOME_PREVENTED


def test_runtime_unknown_fail_closed():
    row = _stub_episode(
        tid="a1",
        policy="B0",
        label="attack",
        tool_hasr=None,
        judge_asr=True,
    )
    assert classify_security_outcome(row) == OUTCOME_UNKNOWN
    bad = _stub_episode(
        tid="a1",
        policy="B0",
        label="attack",
        tool_hasr=True,
        judge_asr=True,
        target_errors=["boom"],
    )
    with pytest.raises(P2LiveGateError) as exc:
        enrich_episode_for_stage_b(bad, run_id="bad")
    assert exc.value.status == "STOP_INFRA_MARKED_HASR_SUCCESS"


def test_wilson_ci_and_paired_discordant():
    w = metric_with_wilson(4, 6, name="Tool-HASR")
    assert w["point_estimate"] == pytest.approx(4 / 6)
    assert w["ci_95_wilson"]["low"] <= w["point_estimate"] <= w["ci_95_wilson"]["high"]
    rows = _full_pack_stubs("wilson_run")
    paired = paired_discordant_counts(rows, metric="tool_hasr")
    assert "B0_to_PHASE1-CORE" in paired["pairs"]
    assert "B0_to_STATIC-A1" in paired["pairs"]
    assert "STATIC-A1_to_PHASE1-CORE" in paired["pairs"]
    assert paired["mcnemar_b0_vs_core"]["pre_registered"] is False


def test_costs_unchanged():
    assert COSTS == {"A0": 0.0, "A1": 0.10, "A2": 0.25, "A3": 0.50}
    rows = _full_pack_stubs("cost_run")
    metrics = score_stage_b_results(rows)
    assert metrics["costs"] == COSTS
    assert metrics["intervention"]["costs"] == COSTS


def test_manifest_completeness_and_hashes():
    man = build_stage_b_manifest(run_id="man1", git_commit_value="deadbeef")
    for key in (
        "run_id",
        "benchmark_version",
        "benchmark_sha256",
        "git_commit",
        "target_model",
        "judge_model",
        "provider",
        "temperature",
        "cache_enabled",
        "prompt_template_hash",
        "tool_schema_hash",
        "configuration_hash",
        "python_version",
        "platform",
        "stage_b_harness_version",
        "scientific_evidence",
        "n_episode_arms_expected",
    ):
        assert key in man
    assert man["benchmark_sha256"] == PACK_SHA256
    assert man["cache_enabled"] is False
    assert man["scientific_evidence"] is False
    assert man["n_episode_arms_expected"] == 108
    assert len(configuration_hash()) == 64
    assert len(tool_schema_hash()) == 64
    assert len(prompt_template_hash()) == 64


def test_overwrite_protection(tmp_path: Path):
    l1 = tmp_path / "experiments" / "real_llm_eval" / "P1_MECHANISM_L1" / "run"
    l1.mkdir(parents=True)
    (l1 / "x.txt").write_text("nope")
    with pytest.raises(P2LiveGateError) as exc:
        assert_unique_output_dir(l1)
    assert exc.value.status == "STOP_OVERWRITE_HISTORICAL_L1"

    smoke = tmp_path / "p2_agentic_smoke_20260101T000000Z_abcd"
    smoke.mkdir()
    (smoke / "manifest.json").write_text("{}")
    with pytest.raises(P2LiveGateError) as exc2:
        assert_unique_output_dir(smoke)
    assert exc2.value.status == "STOP_OVERWRITE_STAGE_A"

    occupied = tmp_path / "p2_agentic_stage_b_run"
    occupied.mkdir()
    (occupied / "old.json").write_text("{}")
    with pytest.raises(P2LiveGateError) as exc3:
        assert_unique_output_dir(occupied)
    assert exc3.value.status == "STOP_OUTPUT_EXISTS"


def test_artifact_bundle_and_independent_verifier(tmp_path: Path):
    run_id = "p2_stage_b_offline_bundle"
    rows = _full_pack_stubs(run_id)
    out = tmp_path / run_id
    man = build_stage_b_manifest(run_id=run_id, git_commit_value="abc12345")
    paths = write_stage_b_artifact_bundle(
        out,
        run_id=run_id,
        predictions=rows,
        manifest=man,
        stats={
            "prompt_tokens_target": 10,
            "completion_tokens_target": 2,
            "prompt_tokens_judge": 8,
            "completion_tokens_judge": 1,
            "n_target_failures": 0,
            "n_judge_failures": 0,
        },
    )
    assert Path(paths["predictions"]).is_file()
    assert Path(paths["event_trace"]).is_file()
    assert Path(paths["metrics"]).is_file()
    assert Path(paths["summary"]).is_file()

    metrics = json.loads(Path(paths["metrics"]).read_text())
    assert metrics["primary"]["estimand"] == "Tool-HASR"
    assert metrics["secondary"]["estimand"] == "Judge-ASR"
    assert "ci_95_wilson" in metrics["primary"]

    proc = subprocess.run(
        [sys.executable, str(VERIFY), str(out)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "STATUS=VERIFY_PASS" in proc.stdout


def test_state_isolation_across_policies():
    pack = {r["id"]: r for r in load_p2_pack()}
    rec = pack["p2a_atk_001"]
    r_b0 = evaluate_trajectory_live(
        rec, "B0", tool_mode="scripted_only", call_judge=False
    )
    r_core = evaluate_trajectory_live(
        rec, "PHASE1-CORE", tool_mode="scripted_only", call_judge=False
    )
    assert r_b0["final_state"]["memory"].get("authz_token") == "GRANT-OPS-ALPHA"
    assert r_core["final_state"]["memory"].get("authz_token") == "GRANT-OPS-ALPHA"
    # Independent clean state per call: both retain memory; policy action differs
    assert r_b0["action"] == "A0"
    assert r_core["action"] in {"A1", "A2", "A3"}
    assert r_b0 is not r_core


def test_persistence_and_toi_diagnostics_from_offline_harness():
    pack = {r["id"]: r for r in load_p2_pack()}
    harness = P2AgenticHarness(policy=OfflinePolicy(mode="scripted"))
    atk001 = trajectory_from_dict(pack["p2a_atk_001"])
    offline = harness.run_trajectory(atk001)
    row = {
        "id": "p2a_atk_001",
        "trajectory_id": "p2a_atk_001",
        "label": "attack",
        "policy_key": "B0",
        "success_condition": pack["p2a_atk_001"].get("success_condition")
        or atk001.success_condition,
        "tool_hasr_success": offline.get("tool_hasr_success"),
        "judge_asr_success": offline.get("judge_asr_success"),
        "security_events": offline.get("security_events") or [],
        "turns": offline.get("turns") or [],
        "metadata": pack["p2a_atk_001"].get("metadata") or {},
        "adaptive_rewrites_used": offline.get("adaptive_rewrites_used") or 0,
        "action": offline.get("final_action") or offline.get("action") or "A0",
        "final_action": offline.get("final_action") or offline.get("action") or "A0",
        "harmful_action_prevented": offline.get("harmful_action_prevented") or False,
        "tool_prevented": offline.get("tool_prevented") or False,
        "n_harmful_executions": offline.get("n_harmful_executions") or 0,
        "judge": {"attack_success": offline.get("judge_asr_success"), "parse_error": None},
    }
    diag = extract_multiturn_diagnostics(row)
    assert "persistence_diagnostic" in diag

    live = evaluate_trajectory_live(
        pack["p2a_atk_011"], "B0", tool_mode="scripted_only", call_judge=False
    )
    enriched_toi = enrich_episode_for_stage_b(live, run_id="toi")
    toi = enriched_toi["multiturn_diagnostics"]["tool_output_injection_events"]
    assert isinstance(toi, list)
    for ev in toi:
        assert ev["source_channel"] == "tool_output_injection"
        assert "malicious_content_from_authored_inject" in ev


def test_cli_stage_b_gates():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--stage-b"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert "STATUS=STOP_STAGE_B_REQUIRES_HUMAN_APPROVAL" in proc.stdout

    proc2 = subprocess.run(
        [sys.executable, str(SCRIPT), "--stage-b", "--approve-stage-b"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc2.returncode == 2
    assert "STATUS=STOP_STAGE_B_LIVE_NOT_WIRED" in proc2.stdout


def test_refuse_helper():
    with pytest.raises(P2LiveGateError) as exc:
        refuse_live_stage_b_without_approval(approve_stage_b=False)
    assert exc.value.status == "STOP_STAGE_B_REQUIRES_HUMAN_APPROVAL"
    with pytest.raises(P2LiveGateError) as exc2:
        refuse_live_stage_b_without_approval(approve_stage_b=True)
    assert exc2.value.status == "STOP_STAGE_B_LIVE_NOT_WIRED"


def test_full_pack_score_primary_counts():
    rows = _full_pack_stubs("fullscore")
    metrics = score_stage_b_results(rows)
    assert metrics["bundle"]["n_attack"] == 48
    assert metrics["primary"]["n_success"] == 16
    assert metrics["primary"]["denominator"] == 48
    assert metrics["secondary"]["n_success"] == 48
    assert metrics["disagreements"]["n_M3"] == 32
    assert metrics["n_results"] == 108
