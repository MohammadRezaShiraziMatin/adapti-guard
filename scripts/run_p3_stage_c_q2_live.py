#!/usr/bin/env python3
"""P3 Stage-C Q2 live runner — B_REDUCED_Q2 under $10 hard budget.

Authorization:
  default / --preflight-only     → NO_LIVE_EXECUTION
  --approve-q2                   → LIVE_EVAL (432 arms; T1–T3 × PHASE1-CORE)

scientific_evidence=false. No detector ranking. No pooling with Smoke/P1/P2/Q1.
Hard stop before any call that would exceed budget_cap_usd=10.00.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from adapti_guard.experiments.env_loader import load_project_env

load_project_env()

from adapti_guard.detectors.base import assert_unique_output_dir
from adapti_guard.evaluation.experiment_logging import git_commit
from adapti_guard.experiments.p2_agentic_live import (
    LOCKED_JUDGE_KEY,
    LOCKED_SEED,
    LiveRunStats,
    P2LiveGateError,
    load_p2_pack,
    write_json,
)
from adapti_guard.experiments.p3_agentic_live import (
    ARTIFACT_ROOT,
    P3LiveGateError,
    assert_p2_pack_composition,
    build_p3_event_trace,
    evaluate_p3_arm,
)
from adapti_guard.experiments.p3_stage_c_q2 import (
    HARNESS_VERSION_Q2,
    PRIMARY_POLICY_STRATUM,
    q2_event_scope_token,
)
from adapti_guard.experiments.p3_stage_c_q2_lock import (
    JUDGE_ID,
    MAXIMUM_PERMITTED_BUDGET_USD,
    T1_ID,
    T2_ID,
    T3_ID,
)
from adapti_guard.experiments.p3_stage_c_q2_live import (
    EXPECTED_N_ARMS_Q2,
    SLOT_TO_CONFIG,
    SLOT_TO_MODEL,
    TARGET_SLOTS,
    P3Q2LiveGateError,
    annotate_q2_row,
    build_q2_manifest,
    build_q2_schedule,
    emit_q2_reports,
    estimate_arm_worst_case_usd,
    final_q2_preflight,
    forensic_audit,
    load_stage_b_phase1_core_rows,
    recompute_all_from_raw,
    stats_cost_usd,
)
from adapti_guard.experiments.real_llm_pipeline import (
    EvaluationBackend,
    PipelineConfig,
    build_models,
)

ARTIFACTS_DIR = Path("/opt/cursor/artifacts")


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def make_run_id(commit: str) -> str:
    return f"p3_stage_c_q2_{utc_stamp()}_{commit[:8]}"


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(r, ensure_ascii=False, default=str) + "\n" for r in rows),
        encoding="utf-8",
    )


def _failed_arm_row(
    *,
    tid: str,
    did: str,
    pid: str,
    slot: str,
    record: dict[str, Any],
    run_id: str,
    target_model_id: str,
    commit: str,
    exc: BaseException,
) -> dict[str, Any]:
    row = {
        "id": tid,
        "trajectory_id": tid,
        "label": record.get("label"),
        "hard_negative": bool(record.get("hard_negative")),
        "detector_id": did,
        "policy_key": pid,
        "policy_id": pid,
        "run_id": run_id,
        "stage": "C_Q2",
        "scientific_evidence": False,
        "failure_state": getattr(exc, "code", None)
        or getattr(exc, "status", None)
        or "RUNTIME_ERROR",
        "error": str(exc),
        "tool_hasr_success": None,
        "judge_asr_success": None,
        "final_action": "A0",
        "target_errors": [str(exc)],
        "security_events": [],
        "target_slot": slot,
        "target_model": target_model_id,
        "judge_model": JUDGE_ID,
    }
    return annotate_q2_row(
        row,
        run_id=run_id,
        target_slot=slot,
        target_model_id=target_model_id,
        commit=commit,
    )


def cumulative_usd(
    *,
    per_target_stats: dict[str, LiveRunStats],
) -> dict[str, Any]:
    total = 0.0
    breakdown: dict[str, Any] = {}
    api_calls = 0
    for slot, stats in per_target_stats.items():
        mid = SLOT_TO_MODEL[slot]
        c = stats_cost_usd(stats, target_model_id=mid)
        breakdown[slot] = {
            **c,
            "n_target_calls": stats.n_target_calls,
            "n_judge_calls": stats.n_judge_calls,
            "prompt_tokens_target": stats.prompt_tokens_target,
            "completion_tokens_target": stats.completion_tokens_target,
            "prompt_tokens_judge": stats.prompt_tokens_judge,
            "completion_tokens_judge": stats.completion_tokens_judge,
        }
        total += c["total_usd"]
        api_calls += int(stats.n_target_calls) + int(stats.n_judge_calls)
    return {
        "actual_usd": round(total, 6),
        "budget_cap_usd": float(MAXIMUM_PERMITTED_BUDGET_USD or 0),
        "per_target": breakdown,
        "api_calls": api_calls,
    }


def run_q2_live(*, run_dir: Path, run_id: str, commit: str) -> dict[str, Any]:
    preflight = final_q2_preflight(require_key=True)
    write_json(run_dir / "preflight.json", preflight)
    print("STATUS=Q2_PREFLIGHT_PASS", flush=True)
    print(
        json.dumps(
            {
                "model_lock": preflight["model_lock"],
                "provenance_lock": preflight["provenance_lock"]["status"],
                "offline_tests": preflight["offline_tests"],
                "budget_cap_usd": preflight["budget_cap_usd"],
                "worst_case_cost_usd": preflight["worst_case_cost_usd"],
                "pre_run_api_calls": preflight["pre_run_api_calls"],
                "smoke": {
                    "status": preflight["smoke"]["status"],
                    "pooled_with_q2": False,
                },
            },
            indent=2,
        ),
        flush=True,
    )

    pack_rows = load_p2_pack()
    inv = assert_p2_pack_composition(pack_rows)
    by_id = {str(r["id"]): r for r in pack_rows}
    schedule = build_q2_schedule(pack_rows)
    t0_rows = load_stage_b_phase1_core_rows()

    write_json(
        run_dir / "integrity.json",
        {
            "status": "INTEGRITY_OK",
            "pack_composition": {
                k: inv[k]
                for k in ("n_total", "n_attack", "n_benign_twin", "n_hard_negative")
            },
            "n_schedule_arms": len(schedule),
            "expected_n_arms": EXPECTED_N_ARMS_Q2,
            "t0_reuse_n_arms": len(t0_rows),
            "detectors": list(preflight["exact_model_ids"]),
            "policy": PRIMARY_POLICY_STRATUM,
        },
    )
    print("STATUS=INTEGRITY_OK", flush=True)

    manifest = build_q2_manifest(
        run_id=run_id,
        git_commit_value=commit,
        trajectory_ids=inv["trajectory_ids"],
    )
    write_json(run_dir / "manifest.json", manifest)

    budget_cap = float(MAXIMUM_PERMITTED_BUDGET_USD or 0)
    per_target_stats: dict[str, LiveRunStats] = {s: LiveRunStats() for s in TARGET_SLOTS}
    results: list[dict[str, Any]] = []
    failed_arms: list[dict[str, Any]] = []
    hard_stop_reason: str | None = None
    t_start = time.perf_counter()
    pred_dir = run_dir / "predictions"
    pred_dir.mkdir(parents=True, exist_ok=True)

    # Build judge once; rebuild target per slot.
    models_by_slot: dict[str, Any] = {}
    for slot in TARGET_SLOTS:
        cfg = PipelineConfig(
            experiment_id=f"{run_id}_{slot}",
            output_dir=run_dir / slot,
            target_config_key=SLOT_TO_CONFIG[slot],
            judge_config_key=LOCKED_JUDGE_KEY,
            backend=EvaluationBackend.OPENROUTER,
            baselines=[PRIMARY_POLICY_STRATUM],
            split="p3_stage_c_q2",
            seed=LOCKED_SEED,
        )
        (run_dir / slot).mkdir(parents=True, exist_ok=True)
        target, judge = build_models(
            cfg, EvaluationBackend.OPENROUTER, cache_enabled=False
        )
        judge.use_fallback = False
        if target.model_id != SLOT_TO_MODEL[slot]:
            raise P3Q2LiveGateError(
                "STOP_TARGET_MODEL_MISMATCH",
                f"{slot}: got {target.model_id} expected {SLOT_TO_MODEL[slot]}",
            )
        j_model = getattr(judge, "model", None)
        jid = getattr(judge, "model_id", None)
        if jid is None and j_model is not None:
            jid = getattr(j_model, "model_id", None)
        if jid is not None and str(jid) != JUDGE_ID:
            raise P3Q2LiveGateError(
                "STOP_JUDGE_MODEL_MISMATCH", f"got {jid} expected {JUDGE_ID}"
            )
        models_by_slot[slot] = (target, judge)
        print(
            f"MODEL_LOCK_OK slot={slot} target={target.model_id} judge={JUDGE_ID}",
            flush=True,
        )

    print(
        f"P3 Q2 live: n_arms={len(schedule)} harness={HARNESS_VERSION_Q2} "
        f"budget_cap_usd={budget_cap} targets={list(TARGET_SLOTS)} "
        f"policy={PRIMARY_POLICY_STRATUM}",
        flush=True,
    )
    print("STATUS=LIVE_Q2_START", flush=True)

    current_slot = None
    target = judge = None
    for i, (slot, tid, did, pid) in enumerate(schedule, start=1):
        if slot != current_slot:
            current_slot = slot
            target, judge = models_by_slot[slot]
            print(f"=== TARGET SLOT {slot} ({SLOT_TO_MODEL[slot]}) ===", flush=True)

        cost_now = cumulative_usd(per_target_stats=per_target_stats)
        record = by_id[tid]
        n_turns = len(record.get("turns") or [])
        arm_ceil = estimate_arm_worst_case_usd(
            n_turns=n_turns, target_model_id=SLOT_TO_MODEL[slot]
        )
        if cost_now["actual_usd"] + arm_ceil > budget_cap:
            hard_stop_reason = (
                f"BUDGET_HARD_STOP before arm {i}/{len(schedule)} "
                f"{slot}×{tid}×{did}: actual={cost_now['actual_usd']} "
                f"arm_ceil={arm_ceil:.6f} cap={budget_cap}"
            )
            print(f"STATUS={hard_stop_reason}", flush=True)
            break

        print(
            f"[{i}/{len(schedule)}] {slot} × {tid} × {did} × {pid} "
            f"usd={cost_now['actual_usd']:.6f}",
            flush=True,
        )
        try:
            row = evaluate_p3_arm(
                record,
                detector_id=did,
                policy_key=pid,
                run_id=run_id,
                target=target,
                judge=judge,
                stats=per_target_stats[slot],
                stage="C_Q2",
                repetition_id=q2_event_scope_token(slot),
            )
            row = annotate_q2_row(
                row,
                run_id=run_id,
                target_slot=slot,
                target_model_id=SLOT_TO_MODEL[slot],
                commit=commit,
            )
        except (P2LiveGateError, P3LiveGateError, P3Q2LiveGateError) as exc:
            row = _failed_arm_row(
                tid=tid,
                did=did,
                pid=pid,
                slot=slot,
                record=record,
                run_id=run_id,
                target_model_id=SLOT_TO_MODEL[slot],
                commit=commit,
                exc=exc,
            )
            failed_arms.append(
                {"i": i, "slot": slot, "tid": tid, "did": did, "error": str(exc)}
            )
            print(f"  FAIL {exc}", flush=True)

        results.append(row)
        write_jsonl(pred_dir / f"{slot}__{did}__{pid}__{tid}.jsonl", [row])
        if i % 12 == 0 or i == len(schedule):
            write_jsonl(run_dir / "predictions.partial.jsonl", results)
            write_json(
                run_dir / "spend.partial.json",
                cumulative_usd(per_target_stats=per_target_stats),
            )

        # Post-arm hard stop if somehow over (should not happen with pre-check)
        cost_after = cumulative_usd(per_target_stats=per_target_stats)
        if cost_after["actual_usd"] > budget_cap + 1e-9:
            hard_stop_reason = (
                f"BUDGET_EXCEEDED_AFTER_ARM {i}: actual={cost_after['actual_usd']}"
            )
            print(f"STATUS={hard_stop_reason}", flush=True)
            break

    elapsed = time.perf_counter() - t_start
    cost = cumulative_usd(per_target_stats=per_target_stats)
    write_json(run_dir / "spend.json", cost)
    write_jsonl(run_dir / "predictions.jsonl", results)

    events = build_p3_event_trace(results)
    (run_dir / "event_trace.jsonl").write_text(
        "".join(json.dumps(e, ensure_ascii=False, default=str) + "\n" for e in events),
        encoding="utf-8",
    )

    live_stats = {s: per_target_stats[s].to_dict() for s in TARGET_SLOTS}
    write_json(run_dir / "live_stats.json", live_stats)
    write_json(run_dir / "elapsed.json", {"elapsed_sec": elapsed})

    arms = {
        "planned": EXPECTED_N_ARMS_Q2,
        "completed": len(results),
        "failed": len(failed_arms),
        "remaining_not_started": EXPECTED_N_ARMS_Q2 - len(results),
        "status": (
            "BUDGET_HARD_STOP"
            if hard_stop_reason
            else (
                "COMPLETE"
                if len(results) == EXPECTED_N_ARMS_Q2
                else "PARTIAL"
            )
        ),
        "hard_stop_reason": hard_stop_reason,
        "failed_detail": failed_arms,
    }
    write_json(run_dir / "arms.json", arms)

    # Unique eval IDs (completed set)
    eval_ids = [str(r["evaluation_id"]) for r in results]
    if len(eval_ids) != len(set(eval_ids)):
        raise P3Q2LiveGateError("STOP_DUPLICATE_EVAL_IDS", "duplicate evaluation_id")

    print("STATUS=RECOMPUTE_FROM_RAW", flush=True)
    recomputed = recompute_all_from_raw(
        run_dir=run_dir, predictions=results, t0_rows=t0_rows
    )
    write_json(run_dir / "recompute.json", recomputed)
    write_json(run_dir / "metrics.json", recomputed.get("overall_live_metrics") or {})

    # Disagreement ledger from overall metrics
    disagrees = list(
        (recomputed.get("overall_live_metrics") or {}).get("disagreements") or []
    )
    (run_dir / "disagreement_ledger.jsonl").write_text(
        "".join(
            json.dumps(d, ensure_ascii=False, default=str) + "\n" for d in disagrees
        ),
        encoding="utf-8",
    )

    print("STATUS=FORENSIC_AUDIT", flush=True)
    audit = forensic_audit(
        run_dir=run_dir,
        run_id=run_id,
        commit=commit,
        predictions=results,
        preflight=preflight,
        cost=cost,
        arms=arms,
    )
    # If incomplete due to budget, integrity may still PASS with issue note
    if hard_stop_reason and "ARM_COUNT_MISMATCH" in (audit.get("issues") or []):
        audit = dict(audit)
        audit["issues"] = [
            x for x in audit["issues"] if x != "ARM_COUNT_MISMATCH"
        ] + ["BUDGET_HARD_STOP_INCOMPLETE"]
        audit["status"] = "PASS_WITH_BUDGET_STOP"
        audit["forensic_audit_status"] = audit["status"]
        audit["integrity_status"] = "PASS"

    report = {
        "run_id": run_id,
        "commit": commit,
        "harness_version": HARNESS_VERSION_Q2,
        "design_id": "B_REDUCED_Q2",
        "LIVE_EVAL": True,
        "exact_model_ids": {
            "T0": preflight["exact_model_ids"]["T0"],
            "T1": T1_ID,
            "T2": T2_ID,
            "T3": T3_ID,
            "JUDGE": JUDGE_ID,
        },
        "arms": arms,
        "api_calls": cost["api_calls"],
        "actual_usd": cost["actual_usd"],
        "budget_cap_usd": cost["budget_cap_usd"],
        "spend": cost,
        "elapsed_sec": elapsed,
        "Tool-HASR_by_target_detector": recomputed["Tool-HASR_by_target_detector"],
        "Judge-ASR_by_target_detector": recomputed["Judge-ASR_by_target_detector"],
        "Judge-ASR": (recomputed.get("overall_live_metrics") or {}).get("Judge-ASR"),
        "delta_table": recomputed["delta_table"],
        "contrasts": recomputed["contrasts"],
        "sign_agreement_count": recomputed["sign_agreement_count"],
        "M3": recomputed.get("M3"),
        "M4": recomputed.get("M4"),
        "INVALID_TOOL_ARGS": recomputed.get("INVALID_TOOL_ARGS"),
        "invalid_tool_args_method": recomputed.get("invalid_tool_args_method"),
        "per_target": recomputed.get("per_target"),
        "paired_episode_analysis": recomputed.get("paired_episode_analysis"),
        "integrity_status": audit.get("integrity_status"),
        "forensic_audit_status": audit.get("forensic_audit_status"),
        "verdict": recomputed.get("verdict"),
        "verdict_rule": recomputed.get("verdict_rule"),
        "scientific_evidence": False,
        "no_ranking": True,
        "no_winner_declared": True,
        "no_additional_experiments_after_q2": True,
        "smoke_separation": preflight.get("smoke"),
        "preflight": {
            "model_lock": preflight["model_lock"],
            "provenance_lock": preflight["provenance_lock"]["status"],
            "offline_tests": preflight["offline_tests"],
            "budget_cap_usd": preflight["budget_cap_usd"],
            "pre_run_api_calls": 0,
        },
        "run_dir": str(run_dir),
    }

    paths = emit_q2_reports(
        run_dir=run_dir,
        artifacts_dir=ARTIFACTS_DIR,
        report=report,
        audit=audit,
    )
    write_json(run_dir / "summary.json", report)
    write_json(run_dir / "run_summary.json", report)
    write_json(run_dir / "output_paths.json", paths)

    print(f"STATUS=Q2_LIVE_COMPLETE verdict={report.get('verdict')}", flush=True)
    print(f"actual_usd={cost['actual_usd']} api_calls={cost['api_calls']}", flush=True)
    print(f"arms={arms}", flush=True)
    print(f"reports={paths}", flush=True)
    return {
        "run_dir": str(run_dir),
        "report": report,
        "audit": audit,
        "paths": paths,
        "preflight": preflight,
        "cost": cost,
        "arms": arms,
        "results": results,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="P3 Stage-C Q2 live runner")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument(
        "--approve-q2",
        action="store_true",
        help="Explicit authorization for Q2 live spend (budget_cap=$10)",
    )
    parser.add_argument("--output-dir", type=str, default="")
    args = parser.parse_args(argv)

    commit = git_commit()
    print(f"git_commit={commit}", flush=True)

    try:
        if args.preflight_only or not args.approve_q2:
            info = final_q2_preflight(require_key=False)
            write_json(ARTIFACTS_DIR / "p3_q2_final_preflight.json", info)
            print(json.dumps({
                "status": info["status"],
                "model_lock": info["model_lock"],
                "provenance_lock": info["provenance_lock"]["status"],
                "offline_tests": info["offline_tests"],
                "budget_cap_usd": info["budget_cap_usd"],
                "worst_case_cost_usd": info["worst_case_cost_usd"],
                "pre_run_api_calls": info["pre_run_api_calls"],
                "smoke_status": info["smoke"]["status"],
                "n_arms": info["arm_schedule"]["n_new_arms"],
            }, indent=2), flush=True)
            if not args.approve_q2:
                print("STATUS=NO_LIVE_EXECUTION", flush=True)
            return 0

        run_id = make_run_id(commit)
        run_dir = Path(args.output_dir) if args.output_dir else ARTIFACT_ROOT / run_id
        assert_unique_output_dir(run_dir)
        run_dir.mkdir(parents=True, exist_ok=True)
        out = run_q2_live(run_dir=run_dir, run_id=run_id, commit=commit)
        print(f"run_id={run_id}", flush=True)
        print(f"verdict={out['report'].get('verdict')}", flush=True)
        print(
            "SCIENTIFIC BOUNDARY: scientific_evidence=false; "
            "no detector ranking; no additional experiments after Q2.",
            flush=True,
        )
        return 0
    except (P3Q2LiveGateError, P3LiveGateError, P2LiveGateError, FileExistsError) as exc:
        code = getattr(exc, "code", None) or "Q2_LIVE_BLOCKED"
        print(f"STATUS={code} error={exc}", flush=True)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
