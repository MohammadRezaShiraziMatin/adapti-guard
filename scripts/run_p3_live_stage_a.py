#!/usr/bin/env python3
"""P3-C Stage-A live smoke runner (fail-closed).

Authorization:
  default / --preflight-only     → NO_LIVE_EXECUTION
  --stage-a --smoke --approve-stage-a → Stage-A live smoke (60 arms)

Never starts Stage-B. scientific_evidence=false.
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

from adapti_guard.evaluation.experiment_logging import git_commit
from adapti_guard.evaluation.prediction_provenance import PROVENANCE_SCHEMA_VERSION
from adapti_guard.experiments.p2_agentic_live import (
    LOCKED_JUDGE,
    LOCKED_JUDGE_KEY,
    LOCKED_SEED,
    LOCKED_TARGET,
    LOCKED_TARGET_KEY,
    LOCKED_TEMPERATURE,
    LOCKED_BACKEND,
    LiveRunStats,
    P2LiveGateError,
    PACK_SHA256,
    write_json,
)
from adapti_guard.experiments.p3_agentic_live import (
    ARTIFACT_ROOT,
    EXPECTED_N_ARMS,
    LIVE_HARNESS_VERSION,
    OPERATIONAL_DETECTORS,
    P3LiveGateError,
    P3_SMOKE_TRAJECTORY_IDS,
    PRIMARY_POLICIES,
    build_p3_manifest,
    evaluate_p3_arm,
    preflight_p3,
    p3_smoke_subset,
    score_p3_stage_a,
    stage_a_cartesian_schedule,
    verify_frozen_integrity,
)
from adapti_guard.experiments.p2_agentic_live import load_p2_pack
from adapti_guard.experiments.real_llm_pipeline import (
    EvaluationBackend,
    PipelineConfig,
    build_models,
)
from adapti_guard.detectors.base import assert_unique_output_dir, P1_SHA256, P2_SHA256
from adapti_guard.detectors.verifier import P3ArtifactVerificationError


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def make_run_id(commit: str) -> str:
    return f"p3_stage_a_smoke_{utc_stamp()}_{commit[:8]}"


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
        encoding="utf-8",
    )


def run_stage_a_smoke(*, run_dir: Path, run_id: str, commit: str) -> dict[str, Any]:
    info = preflight_p3(require_key=True)
    write_json(run_dir / "preflight.json", info)

    manifest = build_p3_manifest(run_id=run_id, git_commit_value=commit)
    write_json(run_dir / "manifest.json", manifest)

    config = PipelineConfig(
        experiment_id=run_id,
        output_dir=run_dir,
        target_config_key=LOCKED_TARGET_KEY,
        judge_config_key=LOCKED_JUDGE_KEY,
        backend=EvaluationBackend.OPENROUTER,
        baselines=list(PRIMARY_POLICIES),
        split="p3_stage_a_smoke",
        seed=LOCKED_SEED,
    )
    target, judge = build_models(
        config, EvaluationBackend.OPENROUTER, cache_enabled=False
    )
    judge.use_fallback = False

    pack_rows = load_p2_pack()
    smoke = p3_smoke_subset(pack_rows)
    by_id = {str(r["id"]): r for r in smoke}
    schedule = stage_a_cartesian_schedule()

    stats = LiveRunStats()
    results: list[dict[str, Any]] = []
    t_start = time.perf_counter()
    pred_dir = run_dir / "predictions"
    pred_dir.mkdir(parents=True, exist_ok=True)

    print(
        f"P3 Stage-A smoke: n_arms={len(schedule)} "
        f"detectors={list(OPERATIONAL_DETECTORS)} policies={list(PRIMARY_POLICIES)}",
        flush=True,
    )

    for i, (tid, did, pid) in enumerate(schedule, start=1):
        record = by_id[tid]
        print(f"[{i}/{len(schedule)}] {tid} × {did} × {pid}", flush=True)
        try:
            row = evaluate_p3_arm(
                record,
                detector_id=did,
                policy_key=pid,
                run_id=run_id,
                target=target,
                judge=judge,
                stats=stats,
            )
        except P2LiveGateError as exc:
            # Preserve failed arm explicitly — do not drop.
            row = {
                "id": tid,
                "trajectory_id": tid,
                "label": record.get("label"),
                "hard_negative": bool(record.get("hard_negative")),
                "detector_id": did,
                "policy_key": pid,
                "policy_id": pid,
                "evaluation_id": f"{run_id}::{tid}::{did}::{pid}",
                "run_id": run_id,
                "stage": "A",
                "scientific_evidence": False,
                "failure_state": getattr(exc, "code", "RUNTIME_ERROR"),
                "error": str(exc),
                "tool_hasr_success": None,
                "judge_asr_success": None,
                "final_action": "A0",
                "target_errors": [str(exc)],
            }
            print(f"  FAIL {exc}", flush=True)
        row["cache_enabled"] = False
        row["temperature"] = LOCKED_TEMPERATURE
        row["backend"] = LOCKED_BACKEND
        row["target_model"] = LOCKED_TARGET
        row["judge_model"] = LOCKED_JUDGE
        row["git_commit"] = commit
        row["dataset_hash"] = PACK_SHA256
        results.append(row)
        write_jsonl(pred_dir / f"{did}__{pid}__{tid}.jsonl", [row])

    elapsed = time.perf_counter() - t_start
    metrics = score_p3_stage_a(results)
    write_json(run_dir / "metrics.json", metrics)
    write_jsonl(run_dir / "predictions.jsonl", results)

    live_stats = stats.to_dict() if hasattr(stats, "to_dict") else dict(stats.__dict__)
    summary = {
        "run_id": run_id,
        "stage": "A",
        "scientific_evidence": False,
        "git_commit": commit,
        "n_arms": len(results),
        "expected_n_arms": EXPECTED_N_ARMS,
        "elapsed_sec": elapsed,
        "live_stats": live_stats,
        "metrics_keys": sorted(metrics.keys()),
        "Tool-HASR": metrics.get("Tool-HASR"),
        "Judge-ASR": metrics.get("Judge-ASR"),
        "M3": metrics.get("M3"),
        "M4": metrics.get("M4"),
        "status": "P3_STAGE_A_COMPLETE"
        if len(results) == EXPECTED_N_ARMS
        else "P3_STAGE_A_PARTIAL",
    }
    write_json(run_dir / "summary.json", summary)
    write_json(run_dir / "live_stats.json", live_stats)
    write_json(run_dir / "elapsed.json", {"elapsed_sec": elapsed})

    # Lightweight artifact checks (live-authorized manifest)
    eval_ids = [str(r["evaluation_id"]) for r in results]
    if len(eval_ids) != len(set(eval_ids)):
        raise P3LiveGateError("STOP_DUPLICATE_EVAL_IDS", "duplicate evaluation_id")
    if len(results) != EXPECTED_N_ARMS:
        raise P3LiveGateError(
            "STOP_ARM_COUNT", f"got {len(results)} expected {EXPECTED_N_ARMS}"
        )

    return {
        "run_dir": str(run_dir),
        "summary": summary,
        "metrics": metrics,
        "manifest": manifest,
        "live_stats": live_stats,
        "results": results,
        "preflight": info,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="P3-C Stage-A live smoke (fail-closed)")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--stage-a", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument(
        "--approve-stage-a",
        action="store_true",
        help="Explicit human/authorization flag required for live spend",
    )
    parser.add_argument("--output-dir", type=str, default="")
    args = parser.parse_args(argv)

    commit = git_commit()
    print(f"git_commit={commit}", flush=True)

    try:
        integrity = verify_frozen_integrity()
        print(f"integrity={integrity}", flush=True)

        if args.preflight_only or not (args.stage_a or args.smoke or args.approve_stage_a):
            info = preflight_p3(require_key=False)
            print(json.dumps({k: info.get(k) for k in (
                "ok", "p3_harness_version", "expected_n_arms", "p3_smoke_ids"
            ) if k in info or True}, indent=2, default=str)[:2000], flush=True)
            print("STATUS=NO_LIVE_EXECUTION", flush=True)
            return 0

        if args.stage_a and not args.smoke:
            print("STOP_SMOKE_REQUIRED", flush=True)
            return 2
        if args.smoke and not args.stage_a:
            print("STOP_STAGE_A_REQUIRED", flush=True)
            return 2
        if not args.approve_stage_a:
            print("STOP_STAGE_A_REQUIRES_APPROVAL", flush=True)
            return 2
        if args.stage_a and args.smoke and args.approve_stage_a:
            run_id = make_run_id(commit)
            run_dir = (
                Path(args.output_dir)
                if args.output_dir
                else ARTIFACT_ROOT / run_id
            )
            assert_unique_output_dir(run_dir)
            run_dir.mkdir(parents=True, exist_ok=True)
            print(f"STATUS=LIVE_STAGE_A_START run_dir={run_dir}", flush=True)
            out = run_stage_a_smoke(run_dir=run_dir, run_id=run_id, commit=commit)
            print(f"STATUS={out['summary']['status']}", flush=True)
            print(f"run_id={run_id}", flush=True)
            print(f"n_arms={out['summary']['n_arms']}", flush=True)
            return 0

        print("STOP_UNRECOGNIZED_FLAGS", flush=True)
        return 2
    except (P3LiveGateError, P2LiveGateError, FileExistsError, P3ArtifactVerificationError) as exc:
        print(f"STATUS=P3_STAGE_A_BLOCKED error={exc}", flush=True)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
