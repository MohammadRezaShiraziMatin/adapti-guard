#!/usr/bin/env python3
"""P2 live Stage-A / Stage-B runner CLI (frozen agentic pack).

Hard gates (fail closed — never auto-spend):
  --stage-b without --approve-stage-b → STOP_STAGE_B_REQUIRES_HUMAN_APPROVAL
  --stage-b --approve-stage-b         → full Stage-B live (108 arms)
  --stage-a without --smoke           → STOP_SMOKE_REQUIRED
  --smoke without --stage-a           → STOP_STAGE_A_REQUIRED
  default / --preflight-only          → Stage-0 preflight; NO_LIVE_EXECUTION

Scientific contract (locked):
  Pack:   datasets/frozen/p2_agentic_v0.1.0/  (SHA 32b40e3b…8d64dd)
  Target: target_2 / qwen/qwen-2.5-7b-instruct (OpenRouter)
  Judge:  judge_fallback / qwen/qwen-2.5-72b-instruct (OpenRouter)
  Arms:   B0, STATIC-A1, PHASE1-CORE
  Temp:   0.0 ; cache disabled
"""

from __future__ import annotations

import argparse
import json
import subprocess
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
    ARTIFACT_ROOT,
    LOCKED_BACKEND,
    LOCKED_JUDGE,
    LOCKED_JUDGE_KEY,
    LOCKED_SEED,
    LOCKED_TARGET,
    LOCKED_TARGET_KEY,
    LOCKED_TEMPERATURE,
    PACK_SHA256,
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
    score_stage_a_results,
    smoke_subset,
    stage_a_arm_schedule,
    utc_now_iso,
    write_json,
)
from adapti_guard.experiments.p2_stage_b import (
    STAGE_B_EXPECTED_EPISODE_ARMS,
    assert_episode_arm_coverage,
    assert_stage_b_pack_locked,
    assert_unique_output_dir,
    build_stage_b_manifest,
    enrich_episode_for_stage_b,
    expected_evaluation_ids,
    refuse_live_stage_b_without_approval,
    stage_b_arm_schedule,
    write_stage_b_artifact_bundle,
)
from adapti_guard.experiments.real_llm_pipeline import (
    BaselineRunContext,
    EvaluationBackend,
    PipelineConfig,
    build_models,
)


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def make_smoke_run_id(commit: str) -> str:
    return f"p2_agentic_smoke_{utc_stamp()}_{commit[:8]}"


def make_stage_b_run_id(commit: str) -> str:
    return f"p2_agentic_stage_b_{utc_stamp()}_{commit[:8]}"


def ensure_output_dir(path: Path, *, force: bool) -> None:
    if path.exists() and any(path.iterdir()) and not force:
        raise P2LiveGateError(
            "STOP_OUTPUT_EXISTS",
            f"output dir exists and is non-empty: {path} (pass --force to overwrite)",
        )
    path.mkdir(parents=True, exist_ok=True)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
        encoding="utf-8",
    )


def run_stage_a_smoke(*, run_dir: Path, run_id: str, commit: str) -> dict[str, Any]:
    """Execute locked Stage-A smoke under OpenRouter (cache off, no judge fallback)."""
    info = preflight(require_key=True)
    write_json(run_dir / "preflight.json", info)

    manifest = build_run_manifest(
        run_id=run_id,
        stage="A_smoke",
        arms=PRIMARY_ARMS,
        trajectory_ids=list(SMOKE_TRAJECTORY_IDS),
        git_commit_value=commit,
        scientific_evidence=False,
    )
    write_json(run_dir / "manifest.json", manifest)

    config = PipelineConfig(
        experiment_id=run_id,
        output_dir=run_dir,
        target_config_key=LOCKED_TARGET_KEY,
        judge_config_key=LOCKED_JUDGE_KEY,
        backend=EvaluationBackend.OPENROUTER,
        baselines=list(PRIMARY_ARMS),
        split="p2_agentic_stage_a",
        seed=LOCKED_SEED,
    )
    target, judge = build_models(
        config, EvaluationBackend.OPENROUTER, cache_enabled=False
    )
    judge.use_fallback = False

    run_context = BaselineRunContext(
        experiment_id=run_id,
        model_id=LOCKED_TARGET,
        model_config_key=LOCKED_TARGET_KEY,
        git_commit=commit,
        seed=LOCKED_SEED,
        dataset_hash=PACK_SHA256,
        cache_enabled=False,
        config_version=PROVENANCE_SCHEMA_VERSION,
    )

    pack_rows = load_p2_pack()
    smoke = smoke_subset(pack_rows)
    by_id = {str(r["id"]): r for r in smoke}
    schedule = stage_a_arm_schedule(smoke)

    stats = LiveRunStats()
    results: list[dict[str, Any]] = []
    t_start = time.perf_counter()

    for arm in PRIMARY_ARMS:
        traj_ids = schedule[arm]
        arm_dir = run_dir / arm
        arm_dir.mkdir(parents=True, exist_ok=True)
        arm_rows: list[dict[str, Any]] = []
        print(f"Running {arm} n={len(traj_ids)} cache=off", flush=True)
        for tid in traj_ids:
            record = by_id[tid]
            row = evaluate_trajectory_live(
                record,
                arm,
                target=target,
                judge=judge,
                tool_mode="scripted_preferred",
                call_judge=True,
                stats=stats,
            )
            row = dict(row)
            row["run_id"] = run_id
            row["dataset_hash"] = run_context.dataset_hash
            row["git_commit"] = run_context.git_commit
            row["cache_enabled"] = False
            row["temperature"] = LOCKED_TEMPERATURE
            row["backend"] = LOCKED_BACKEND
            row["judge_model"] = LOCKED_JUDGE
            row["judge_config_key"] = LOCKED_JUDGE_KEY
            row["smoke_seed"] = SMOKE_SEED
            row["smoke_core_id"] = SMOKE_CORE_ID
            arm_rows.append(row)
            results.append(row)
            line = (
                f"  [{arm}] {tid} action={row.get('final_action')} "
                f"tool_hasr={row.get('tool_hasr_success')} "
                f"judge_asr={row.get('judge_asr_success')}"
            )
            print(line, flush=True)

        write_jsonl(arm_dir / f"{arm}_predictions.jsonl", arm_rows)
        write_json(
            arm_dir / f"{arm}_metrics.json",
            score_stage_a_results(arm_rows, policy=arm),
        )

    elapsed = round(time.perf_counter() - t_start, 2)
    scored = score_stage_a_results(results)
    write_json(run_dir / "metrics.json", scored)
    write_jsonl(run_dir / "predictions.jsonl", results)
    write_jsonl(
        run_dir / "disagreement_ledger.jsonl",
        list(scored.get("disagreements") or []),
    )

    summary = {
        "run_id": run_id,
        "stage": "A_smoke",
        "dir": str(run_dir),
        "scientific_evidence": False,
        "n_results": len(results),
        "elapsed_seconds": elapsed,
        "stats": stats.to_dict(),
        "target_model": LOCKED_TARGET,
        "judge_model": LOCKED_JUDGE,
        "cache_enabled": False,
        "dataset_hash": PACK_SHA256,
        "git_commit": commit,
        "arms": list(PRIMARY_ARMS),
        "trajectory_ids": list(SMOKE_TRAJECTORY_IDS),
        "output_paths": {
            "manifest": str(run_dir / "manifest.json"),
            "preflight": str(run_dir / "preflight.json"),
            "metrics": str(run_dir / "metrics.json"),
            "predictions": str(run_dir / "predictions.jsonl"),
            "disagreement_ledger": str(run_dir / "disagreement_ledger.jsonl"),
        },
    }
    write_json(run_dir / "run_summary.json", summary)
    write_json(run_dir / "elapsed.json", {"elapsed_seconds": elapsed})
    return summary


def stage_b_integrity_gate() -> dict[str, Any]:
    """Fail-closed integrity checks BEFORE any API/LLM call."""
    inv = assert_stage_b_pack_locked()
    schedule = stage_b_arm_schedule()
    probe_ids = expected_evaluation_ids("__integrity_probe__")
    if len(probe_ids) != STAGE_B_EXPECTED_EPISODE_ARMS:
        raise P2LiveGateError(
            "STOP_STAGE_B_ARM_COUNT",
            f"expected {STAGE_B_EXPECTED_EPISODE_ARMS}; got {len(probe_ids)}",
        )
    if len(PRIMARY_ARMS) != 3:
        raise P2LiveGateError(
            "STOP_POLICY_COUNT",
            f"expected 3 policies; got {len(PRIMARY_ARMS)}",
        )
    for arm, tids in schedule.items():
        if len(tids) != 36 or len(set(tids)) != 36:
            raise P2LiveGateError(
                "STOP_STAGE_B_SCHEDULE",
                f"arm {arm} must have 36 unique trajectories; got {len(tids)}",
            )
    return {
        "status": "INTEGRITY_OK",
        "benchmark_sha256": inv["benchmark_sha256"],
        "p1_sha256": inv["p1_integrity"]["p1_sha256"],
        "n_total": inv["n_total"],
        "n_attack": inv["n_attack"],
        "n_benign_twin": inv["n_benign_twin"],
        "n_hard_negative": inv["n_hard_negative"],
        "n_episode_arms_expected": STAGE_B_EXPECTED_EPISODE_ARMS,
        "n_unique_evaluation_ids": len(set(probe_ids)),
        "policies": list(PRIMARY_ARMS),
        "live_evaluated": inv["live_evaluated"],
    }


def run_stage_b_full(*, run_dir: Path, run_id: str, commit: str) -> dict[str, Any]:
    """Execute frozen Stage-B: 36 trajectories × 3 policies = 108 arms."""
    integrity = stage_b_integrity_gate()
    write_json(run_dir / "integrity.json", integrity)
    print(json.dumps(integrity, indent=2), flush=True)
    print("STATUS=INTEGRITY_OK", flush=True)

    info = preflight(require_key=True)
    write_json(run_dir / "preflight.json", info)
    print("STATUS=PREFLIGHT_OK", flush=True)

    started_at = utc_now_iso()
    manifest = build_stage_b_manifest(
        run_id=run_id,
        git_commit_value=commit,
        started_at=started_at,
        scientific_evidence=True,
        extra={
            "note": (
                "P2 Stage-B pilot live evidence under frozen p2_agentic_v0.1.0. "
                "Not broad generalization / production security guarantee."
            ),
        },
    )
    write_json(run_dir / "manifest.json", manifest)

    config = PipelineConfig(
        experiment_id=run_id,
        output_dir=run_dir,
        target_config_key=LOCKED_TARGET_KEY,
        judge_config_key=LOCKED_JUDGE_KEY,
        backend=EvaluationBackend.OPENROUTER,
        baselines=list(PRIMARY_ARMS),
        split="p2_agentic_stage_b",
        seed=LOCKED_SEED,
    )
    target, judge = build_models(
        config, EvaluationBackend.OPENROUTER, cache_enabled=False
    )
    judge.use_fallback = False

    pack_rows = load_p2_pack()
    by_id = {str(r["id"]): r for r in pack_rows}
    schedule = stage_b_arm_schedule(pack_rows)

    stats = LiveRunStats()
    results: list[dict[str, Any]] = []
    t_start = time.perf_counter()

    for arm in PRIMARY_ARMS:
        traj_ids = schedule[arm]
        arm_dir = run_dir / arm
        arm_dir.mkdir(parents=True, exist_ok=True)
        arm_rows: list[dict[str, Any]] = []
        print(
            f"Running Stage-B {arm} n={len(traj_ids)} cache=off "
            f"target={LOCKED_TARGET}",
            flush=True,
        )
        for tid in traj_ids:
            record = by_id[tid]
            row = evaluate_trajectory_live(
                record,
                arm,
                target=target,
                judge=judge,
                tool_mode="scripted_preferred",
                call_judge=True,
                stats=stats,
            )
            row = dict(row)
            row["run_id"] = run_id
            row["dataset_hash"] = PACK_SHA256
            row["git_commit"] = commit
            row["cache_enabled"] = False
            row["temperature"] = LOCKED_TEMPERATURE
            row["backend"] = LOCKED_BACKEND
            row["judge_model"] = LOCKED_JUDGE
            row["judge_config_key"] = LOCKED_JUDGE_KEY
            row["stage"] = "B_full"
            row = enrich_episode_for_stage_b(row, run_id=run_id)
            arm_rows.append(row)
            results.append(row)
            print(
                f"  [{arm}] {tid} action={row.get('final_action')} "
                f"tool_hasr={row.get('tool_hasr_success')} "
                f"judge_asr={row.get('judge_asr_success')} "
                f"outcome={row.get('security_outcome')}",
                flush=True,
            )
            # Incremental crash-safety checkpoint
            write_jsonl(arm_dir / f"{arm}_predictions.jsonl", arm_rows)
            write_jsonl(run_dir / "predictions.partial.jsonl", results)

        write_jsonl(arm_dir / f"{arm}_predictions.jsonl", arm_rows)

    # Coverage gate before finalizing
    assert_episode_arm_coverage(results, run_id=run_id)

    ended_at = utc_now_iso()
    elapsed = round(time.perf_counter() - t_start, 2)
    manifest["ended_at_utc"] = ended_at
    manifest["elapsed_seconds"] = elapsed

    paths = write_stage_b_artifact_bundle(
        run_dir,
        run_id=run_id,
        predictions=results,
        manifest=manifest,
        stats=stats.to_dict(),
        force=True,  # dir already contains checkpoints / preflight
    )
    write_json(run_dir / "elapsed.json", {"elapsed_seconds": elapsed})
    write_json(run_dir / "live_stats.json", stats.to_dict())

    # Independent verifier (must pass)
    verify_script = ROOT / "scripts" / "verify_p2_stage_b_artifacts.py"
    proc = subprocess.run(
        [sys.executable, str(verify_script), str(run_dir)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    verify_out = (proc.stdout or "") + (proc.stderr or "")
    (run_dir / "verifier_stdout.txt").write_text(verify_out, encoding="utf-8")
    if proc.returncode != 0 or "STATUS=VERIFY_PASS" not in proc.stdout:
        raise P2LiveGateError(
            "STOP_VERIFIER_FAILED",
            f"verify_p2_stage_b_artifacts.py failed (rc={proc.returncode}): {verify_out[-2000:]}",
        )

    summary = json.loads(Path(paths["summary"]).read_text(encoding="utf-8"))
    summary.update(
        {
            "dir": str(run_dir),
            "elapsed_seconds": elapsed,
            "stats": stats.to_dict(),
            "git_commit": commit,
            "verifier_status": "VERIFY_PASS",
            "integrity": integrity,
            "output_paths": paths,
            "scientific_boundary": (
                "P2 Stage-B pilot evidence under frozen pack; "
                "not broad generalization or production security guarantee."
            ),
        }
    )
    write_json(run_dir / "summary.json", summary)
    write_json(run_dir / "run_summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="P2 live Stage-A/B runner (frozen agentic pack; fail-closed gates)"
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Stage 0 static validation only (default if no live flags)",
    )
    parser.add_argument(
        "--stage-a",
        action="store_true",
        help="Stage A smoke (NOT scientific evidence); requires --smoke",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Authorize Stage-A smoke subset; requires --stage-a",
    )
    parser.add_argument(
        "--stage-b",
        action="store_true",
        help="Stage B full live (requires --approve-stage-b)",
    )
    parser.add_argument(
        "--approve-stage-b",
        action="store_true",
        help="Human approval token for Stage B live execution",
    )
    parser.add_argument(
        "--require-key",
        action="store_true",
        help="Require OPENROUTER_API_KEY even for Stage-0 preflight",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow writing into an existing non-empty output directory",
    )
    parser.add_argument("--output", default="", help="Existing or new run dir")
    args = parser.parse_args()

    # --- Hard gates (before any live spend) ---
    if args.stage_b:
        try:
            refuse_live_stage_b_without_approval(
                approve_stage_b=bool(args.approve_stage_b)
            )
        except P2LiveGateError as exc:
            print(f"STATUS={exc.status}", flush=True)
            print(exc.message, file=sys.stderr)
            return 2

    if args.stage_a and not args.smoke:
        print("STATUS=STOP_SMOKE_REQUIRED", flush=True)
        print(
            "Stage A requires explicit --smoke (instrumentation smoke only).",
            file=sys.stderr,
        )
        return 2

    if args.smoke and not args.stage_a:
        print("STATUS=STOP_STAGE_A_REQUIRED", flush=True)
        print(
            "--smoke requires --stage-a. Pass both flags for Stage-A smoke.",
            file=sys.stderr,
        )
        return 2

    if args.stage_a and args.stage_b:
        print("STATUS=STOP_MUTUALLY_EXCLUSIVE_STAGES", flush=True)
        print("Pass either Stage A or Stage B, not both.", file=sys.stderr)
        return 2

    live_a = bool(args.stage_a and args.smoke)
    live_b = bool(args.stage_b and args.approve_stage_b)

    if live_b:
        # Integrity BEFORE any API/model construction
        try:
            integrity = stage_b_integrity_gate()
            print(json.dumps(integrity, indent=2), flush=True)
            print("STATUS=INTEGRITY_OK", flush=True)
        except P2LiveGateError as exc:
            print(f"STATUS={exc.status}", flush=True)
            print(exc.message, file=sys.stderr, flush=True)
            print("STOP — NO LIVE CALLS", flush=True)
            return 2

        commit = git_commit() or "unknown"
        if args.output:
            run_dir = Path(args.output)
            if not run_dir.is_absolute():
                run_dir = ROOT / run_dir
            run_id = run_dir.name
        else:
            run_id = make_stage_b_run_id(commit)
            run_dir = ARTIFACT_ROOT / run_id

        try:
            assert_unique_output_dir(run_dir, force=args.force)
            ensure_output_dir(run_dir, force=args.force)
            summary = run_stage_b_full(run_dir=run_dir, run_id=run_id, commit=commit)
        except P2LiveGateError as exc:
            print(f"STATUS={exc.status}", flush=True)
            print(exc.message, file=sys.stderr, flush=True)
            return 2

        print("STATUS=STAGE_B_COMPLETE", flush=True)
        print(
            "SCIENTIFIC BOUNDARY: P2 Stage-B pilot evidence with stated limitations.",
            flush=True,
        )
        print(json.dumps(summary, indent=2, default=str), flush=True)
        return 0

    try:
        info = preflight(require_key=live_a or args.require_key)
    except P2LiveGateError as exc:
        print(f"STATUS={exc.status}", flush=True)
        print(exc.message, file=sys.stderr, flush=True)
        return 2

    print(json.dumps(info, indent=2))
    print("STATUS=PREFLIGHT_OK", flush=True)

    if not live_a:
        print("STATUS=NO_LIVE_EXECUTION", flush=True)
        return 0

    commit = git_commit() or "unknown"
    if args.output:
        run_dir = Path(args.output)
        if not run_dir.is_absolute():
            run_dir = ROOT / run_dir
        run_id = run_dir.name
    else:
        run_id = make_smoke_run_id(commit)
        run_dir = ARTIFACT_ROOT / run_id

    try:
        ensure_output_dir(run_dir, force=args.force)
        summary = run_stage_a_smoke(run_dir=run_dir, run_id=run_id, commit=commit)
    except P2LiveGateError as exc:
        print(f"STATUS={exc.status}", flush=True)
        print(exc.message, file=sys.stderr, flush=True)
        return 2

    print("STATUS=STAGE_A_COMPLETE", flush=True)
    print(
        "HUMAN GATE: Stage A is smoke only — not paper evidence. Do not start Stage B.",
        flush=True,
    )
    print(json.dumps(summary, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
