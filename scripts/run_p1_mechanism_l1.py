#!/usr/bin/env python3
"""Canonical Track L1 Real-LLM runner for frozen P1 mechanism pack.

Scientific contract (locked):
  Dataset: datasets/frozen/p1_mechanism_v1.0.0/  (SHA 1a0b0053…dd235)
  Target:  target_2 = qwen/qwen-2.5-7b-instruct
  Judge:   judge_fallback = qwen/qwen-2.5-72b-instruct
  Policies (primary): B0 / STATIC-A1 / PHASE1-CORE
  Backend: OpenRouter ; temperature 0.0 ; cache disabled

Stages:
  Stage 0  --preflight-only   static validation, no API
  Stage A  --stage-a          smoke (NOT paper evidence); requires live keys
  Stage B  --stage-b --approve-full-l1   full 96×3; human gate required

Default (no stage flag): Stage 0 preflight only — never spends API budget.
ORACLE_* arms are never run in the primary comparison.
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
# Match pytest.ini pythonpath: repo root + src/ package-dir.
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from adapti_guard.experiments.env_loader import load_project_env

load_project_env()

from adapti_guard.evaluation.attack_success import evaluate_episode
from adapti_guard.evaluation.experiment_logging import git_commit
from adapti_guard.evaluation.prediction_provenance import (
    PROVENANCE_SCHEMA_VERSION,
    build_prediction_row,
)
from adapti_guard.experiments.defense_baselines import get_defense_fn
from adapti_guard.experiments.p1_mechanism_l1 import (
    ARTIFACT_ROOT,
    COSTS,
    CONFIG_VERSION,
    LOCKED_BACKEND,
    LOCKED_JUDGE,
    LOCKED_JUDGE_KEY,
    LOCKED_SEED,
    LOCKED_TARGET,
    LOCKED_TARGET_KEY,
    LOCKED_TEMPERATURE,
    PACK_ID,
    PACK_PATH,
    PACK_SHA256,
    PRIMARY_ARMS,
    SMOKE_CORE_EPISODE_ID,
    SMOKE_EPISODE_IDS,
    L1GateError,
    load_p1_pack,
    preflight,
    reproducibility_fields,
    score_run,
    smoke_subset,
    write_json,
)
from adapti_guard.experiments.real_llm_pipeline import (
    BaselineRunContext,
    EvaluationBackend,
    PipelineConfig,
    build_models,
)
from adapti_guard.experiments.vnext_confirm import load_predictions, row_excluded


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def make_run_id(commit: str, *, stage: str) -> str:
    return f"l1_p1m_{stage}_{utc_stamp()}_{commit[:8]}"


def prediction_ok(row: dict[str, Any] | None) -> bool:
    if not row:
        return False
    return not row_excluded(row)


def enrich_row(
    ep: Any,
    pred_row: dict[str, Any],
    *,
    run_id: str,
    policy: str,
    dataset_hash: str,
    timestamp: str,
) -> dict[str, Any]:
    pred_row = dict(pred_row)
    pred_row["id"] = ep.id
    pred_row["scientific_arm"] = policy
    pred_row["policy"] = policy
    pred_row["taxonomy_class"] = ep.taxonomy_class
    pred_row["defense_action"] = ep.defense_action
    pred_row["action"] = ep.defense_action
    pred_row["model_refusal"] = bool(ep.model_refusal)
    pred_row["detector_hit"] = bool(ep.detector_hit)
    pred_row["tool_blocked"] = bool(ep.tool_blocked)
    pred_row["intervention_cost"] = float(COSTS.get(str(ep.defense_action), 0.0))
    pred_row["judge_usage"] = (ep.metadata or {}).get("judge_usage")
    pred_row["tool_turn"] = (ep.metadata or {}).get("tool_turn")
    pred_row["judge_config_key"] = LOCKED_JUDGE_KEY
    pred_row["judge_model_id"] = LOCKED_JUDGE
    pred_row["temperature"] = LOCKED_TEMPERATURE
    pred_row["backend"] = LOCKED_BACKEND
    pred_row["pack_id"] = PACK_ID
    # Merge canonical reproducibility block (does not invent values).
    pred_row.update(
        reproducibility_fields(
            run_id=run_id,
            timestamp=timestamp,
            policy=policy,
            dataset_hash=dataset_hash,
            git_commit_value=str(pred_row.get("git_commit") or git_commit()),
        )
    )
    return pred_row


def ensure_output_dir(path: Path, *, force: bool) -> None:
    if path.exists() and any(path.iterdir()) and not force:
        raise L1GateError(
            "STOP_OUTPUT_EXISTS",
            f"output dir exists and is non-empty: {path} (pass --force to overwrite)",
        )
    path.mkdir(parents=True, exist_ok=True)


def run_arm(
    *,
    baseline_key: str,
    records: list[dict[str, Any]],
    target: Any,
    judge: Any,
    output_dir: Path,
    run_context: BaselineRunContext,
    run_id: str,
) -> dict[str, Any]:
    if baseline_key not in PRIMARY_ARMS:
        raise L1GateError("FORBIDDEN_ARM", f"non-primary arm forbidden in L1: {baseline_key}")

    arm_dir = output_dir / baseline_key
    arm_dir.mkdir(parents=True, exist_ok=True)
    predictions_path = arm_dir / f"{baseline_key}_predictions.jsonl"
    failures_path = arm_dir / f"{baseline_key}_api_failures.jsonl"
    log_path = output_dir / "logs" / f"{baseline_key}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    existing = load_predictions(predictions_path)
    defense_fn, state = get_defense_fn(baseline_key)
    if state is not None and hasattr(state, "reset"):
        state.reset()

    n_ok = sum(1 for r in records if prediction_ok(existing.get(str(r["id"]))))
    msg = f"[{baseline_key}] keep_ok={n_ok} retry_or_missing={len(records) - n_ok}"
    print(msg, flush=True)
    log_path.write_text(msg + "\n", encoding="utf-8")

    ordered_rows: list[dict[str, Any]] = []
    n_api_calls = 0
    failure_rows: list[dict[str, Any]] = []
    target_tokens = 0
    judge_tokens = 0

    for record in records:
        eid = str(record["id"])
        prev = existing.get(eid)
        if prediction_ok(prev):
            # Advance defense state consistently without re-calling the API.
            try:
                defense_fn(
                    record.get("prompt", ""),
                    record.get("context") or None,
                    tool_call=record.get("tool_call"),
                )
            except TypeError:
                defense_fn(record.get("prompt", ""), record.get("context") or None)
            ordered_rows.append(prev)
            continue

        t0 = time.perf_counter()
        timestamp = datetime.now(timezone.utc).isoformat()
        ep = evaluate_episode(
            record,
            defense_fn=defense_fn,
            target_model=target,
            judge=judge,
        )
        ep.metadata["baseline"] = baseline_key
        ep.metadata["evaluation_mode"] = "real_llm_judge"
        ep.metadata["scientific_arm"] = baseline_key
        ep.metadata["policy"] = baseline_key
        pred_row = build_prediction_row(
            ep,
            baseline=baseline_key,
            model_id=run_context.model_id,
            model_config_key=run_context.model_config_key,
            experiment_id=run_context.experiment_id,
            git_commit=run_context.git_commit,
            seed=run_context.seed,
            dataset_hash=run_context.dataset_hash,
            cache_enabled=run_context.cache_enabled,
            config_version=run_context.config_version,
            timestamp=timestamp,
        )
        pred_row = enrich_row(
            ep,
            pred_row,
            run_id=run_id,
            policy=baseline_key,
            dataset_hash=run_context.dataset_hash,
            timestamp=timestamp,
        )
        ordered_rows.append(pred_row)
        n_api_calls += 1
        elapsed = time.perf_counter() - t0

        pt = int(pred_row.get("prompt_tokens") or 0)
        ct = int(pred_row.get("completion_tokens") or 0)
        target_tokens += pt + ct
        ju = pred_row.get("judge_usage") or {}
        judge_tokens += int(ju.get("prompt_tokens") or 0) + int(ju.get("completion_tokens") or 0)

        if not prediction_ok(pred_row):
            failure_rows.append(
                {
                    "episode_id": eid,
                    "arm": baseline_key,
                    "api_status": pred_row.get("api_status"),
                    "judge_reason": pred_row.get("judge_reason"),
                    "error": (ep.metadata or {}).get("target_error")
                    or (ep.metadata or {}).get("judge_parse_error"),
                    "elapsed_s": round(elapsed, 3),
                    # Explicit failure ledger — do not invent replacement values.
                    "observation_status": "FAILED",
                }
            )

        line = (
            f"  [{baseline_key}] {eid} blocked={ep.blocked} action={ep.defense_action} "
            f"tax={ep.taxonomy_class} asr={ep.attack_succeeded} "
            f"api={pred_row.get('api_status')} {elapsed:.1f}s"
        )
        print(line, flush=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")

        predictions_path.write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in ordered_rows),
            encoding="utf-8",
        )
        write_json(
            output_dir / "progress.json",
            {
                "arm": baseline_key,
                "last_id": eid,
                "completed": len(ordered_rows),
                "total": len(records),
                "elapsed_s": round(elapsed, 3),
            },
        )

    predictions_path.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in ordered_rows),
        encoding="utf-8",
    )
    failures_path.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in failure_rows),
        encoding="utf-8",
    )
    errors_path = output_dir / "errors" / f"{baseline_key}_errors.jsonl"
    errors_path.parent.mkdir(parents=True, exist_ok=True)
    errors_path.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in failure_rows),
        encoding="utf-8",
    )

    preds = load_predictions(predictions_path)
    n_ok_final = sum(1 for r in records if prediction_ok(preds.get(str(r["id"]))))
    metrics = {
        "baseline": baseline_key,
        "scientific_arm": baseline_key,
        "n_samples": len(preds),
        "n_api_calls_this_pass": n_api_calls,
        "n_api_failures_logged": len(failure_rows),
        "n_scorable": n_ok_final,
        "target_tokens": target_tokens,
        "judge_tokens": judge_tokens,
        "evaluation_mode": "real_llm_judge",
        "dataset_hash": run_context.dataset_hash,
        "cache_enabled": run_context.cache_enabled,
        "seed": run_context.seed,
        "git_commit": run_context.git_commit,
        "status": "COMPLETED" if n_ok_final >= len(records) else "PARTIAL",
    }
    write_json(arm_dir / f"{baseline_key}_metrics.json", metrics)
    return metrics


def build_manifest(
    *,
    run_id: str,
    stage: str,
    commit: str,
    n_episodes: int,
    arms: list[str],
    episode_ids: list[str] | None,
) -> dict[str, Any]:
    ts = datetime.now(timezone.utc).isoformat()
    return {
        **reproducibility_fields(
            run_id=run_id,
            timestamp=ts,
            policy=",".join(arms),
            dataset_hash=PACK_SHA256,
            git_commit_value=commit,
        ),
        "experiment_id": "P1-MECHANISM-L1",
        "stage": stage,
        "pack_id": PACK_ID,
        "pack_path": str(PACK_PATH),
        "dataset_hash": PACK_SHA256,
        "target_config_key": LOCKED_TARGET_KEY,
        "target_model": LOCKED_TARGET,
        "model_id": LOCKED_TARGET,
        "model_config_key": LOCKED_TARGET_KEY,
        "judge_config_key": LOCKED_JUDGE_KEY,
        "judge_model": LOCKED_JUDGE,
        "temperature": LOCKED_TEMPERATURE,
        "seed": LOCKED_SEED,
        "cache_enabled": False,
        "config_version": CONFIG_VERSION,
        "backend": LOCKED_BACKEND,
        "baselines": arms,
        "policies_primary": list(PRIMARY_ARMS),
        "oracle_excluded_from_primary": True,
        "n_episodes": n_episodes,
        "episode_ids": episode_ids,
        "costs": COSTS,
        "evaluation_mode": "real_llm_judge",
        "scientific_evidence": stage == "B_full",
        "note": (
            "Stage A is instrumentation smoke only — not paper evidence."
            if stage.startswith("A")
            else "Primary comparison: B0 vs STATIC-A1 vs PHASE1-CORE."
        ),
    }


def run_live(
    *,
    stage: str,
    records: list[dict[str, Any]],
    arms: list[str],
    run_dir: Path,
    run_id: str,
    commit: str,
    episode_ids: list[str] | None,
) -> dict[str, Any]:
    write_json(
        run_dir / "manifest.json",
        build_manifest(
            run_id=run_id,
            stage=stage,
            commit=commit,
            n_episodes=len(records),
            arms=arms,
            episode_ids=episode_ids,
        ),
    )

    config = PipelineConfig(
        experiment_id=run_id,
        output_dir=run_dir,
        target_config_key=LOCKED_TARGET_KEY,
        judge_config_key=LOCKED_JUDGE_KEY,
        backend=EvaluationBackend.OPENROUTER,
        baselines=list(arms),
        split="l1_p1_mechanism",
        seed=LOCKED_SEED,
        benchmark_dir=str(PACK_PATH.parent),
    )
    # Hard lock: never AUTO / groq / gemini for canonical L1.
    target, judge = build_models(
        config, EvaluationBackend.OPENROUTER, cache_enabled=False
    )
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

    t_start = time.perf_counter()
    arm_stats: list[dict[str, Any]] = []
    for arm in arms:
        # Stage A: B0 on all smoke episodes; PHASE1-CORE on one episode only.
        arm_records = records
        if stage.startswith("A") and arm == "PHASE1-CORE":
            arm_records = [r for r in records if str(r["id"]) == SMOKE_CORE_EPISODE_ID]
        print(f"Running {arm} n={len(arm_records)} cache=off", flush=True)
        arm_stats.append(
            run_arm(
                baseline_key=arm,
                records=arm_records,
                target=target,
                judge=judge,
                output_dir=run_dir,
                run_context=run_context,
                run_id=run_id,
            )
        )
    elapsed = round(time.perf_counter() - t_start, 2)
    write_json(run_dir / "elapsed.json", {"elapsed_seconds": elapsed})

    pack_rows = load_p1_pack()
    metrics = score_run(run_dir, pack_rows, arms=arms)
    api_calls = sum(int(a.get("n_api_calls_this_pass") or 0) for a in arm_stats)
    api_failures = sum(int(a.get("n_api_failures_logged") or 0) for a in arm_stats)
    target_tokens = sum(int(a.get("target_tokens") or 0) for a in arm_stats)
    judge_tokens = sum(int(a.get("judge_tokens") or 0) for a in arm_stats)

    summary = {
        "run_id": run_id,
        "stage": stage,
        "dir": str(run_dir),
        "episodes_completed": sum(int(a.get("n_scorable") or 0) for a in arm_stats),
        "api_calls": api_calls,
        "api_failures": api_failures,
        "parse_errors": api_failures,  # failures ledger includes judge parse errors
        "runtime_errors": api_failures,
        "target_tokens": target_tokens,
        "judge_tokens": judge_tokens,
        "elapsed_seconds": elapsed,
        "arm_stats": arm_stats,
        "output_paths": {
            "manifest": str(run_dir / "manifest.json"),
            "metrics": str(run_dir / "metrics.json"),
            "logs": str(run_dir / "logs"),
            "errors": str(run_dir / "errors"),
            "predictions": {
                arm: str(run_dir / arm / f"{arm}_predictions.jsonl") for arm in arms
            },
        },
    }
    write_json(run_dir / "metrics.json", metrics)
    write_json(run_dir / "run_summary.json", summary)
    write_json(
        run_dir / "run_meta.json",
        {
            **reproducibility_fields(
                run_id=run_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                policy=",".join(arms),
                dataset_hash=PACK_SHA256,
                git_commit_value=commit,
            ),
            "stage": stage,
            "api_calls": api_calls,
            "api_failures": api_failures,
            "target_tokens": target_tokens,
            "judge_tokens": judge_tokens,
            "elapsed_seconds": elapsed,
            "scientific_evidence": stage == "B_full",
        },
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Canonical L1 Real-LLM runner (frozen P1 mechanism pack)"
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Stage 0 static validation only (default if no stage flag)",
    )
    parser.add_argument(
        "--stage-a",
        action="store_true",
        help="Stage A smoke (NOT scientific evidence); spends API budget",
    )
    parser.add_argument(
        "--stage-b",
        action="store_true",
        help="Stage B full L1 (96×3); requires --approve-full-l1",
    )
    parser.add_argument(
        "--approve-full-l1",
        action="store_true",
        help="Explicit human approval for Stage B budget spend",
    )
    parser.add_argument("--score-only", action="store_true")
    parser.add_argument("--require-key", action="store_true")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow writing into an existing non-empty output directory",
    )
    parser.add_argument("--output", default="", help="Existing or new run dir")
    args = parser.parse_args()

    if args.stage_a and args.stage_b:
        print("STATUS=STOP_AMBIGUOUS_STAGE", flush=True)
        print("Pass only one of --stage-a / --stage-b", file=sys.stderr)
        return 2

    # Safe default: Stage 0 only — never auto-spend.
    stage0_only = (
        args.preflight_only
        or (not args.stage_a and not args.stage_b and not args.score_only)
    )

    try:
        live = bool(args.stage_a or args.stage_b) and not args.score_only
        info = preflight(require_key=live or args.require_key)
    except L1GateError as exc:
        print(f"STATUS={exc.status}", flush=True)
        print(exc.message, file=sys.stderr, flush=True)
        return 2

    print(json.dumps(info, indent=2))
    print("STATUS=PREFLIGHT_OK", flush=True)
    if stage0_only and not args.score_only:
        return 0

    if args.stage_b and not args.approve_full_l1:
        print("STATUS=STOP_STAGE_B_NEEDS_APPROVAL", flush=True)
        print(
            "Stage B requires explicit --approve-full-l1 after human gate.",
            file=sys.stderr,
        )
        return 2

    commit = git_commit() or "unknown"
    if args.output:
        run_dir = Path(args.output)
        if not run_dir.is_absolute():
            run_dir = ROOT / run_dir
        run_id = run_dir.name
    else:
        stage_tag = "smoke" if args.stage_a else ("full" if args.stage_b else "score")
        run_id = make_run_id(commit, stage=stage_tag)
        run_dir = ARTIFACT_ROOT / run_id

    try:
        if not args.score_only:
            ensure_output_dir(run_dir, force=args.force)
        else:
            run_dir.mkdir(parents=True, exist_ok=True)
    except L1GateError as exc:
        print(f"STATUS={exc.status}", flush=True)
        print(exc.message, file=sys.stderr, flush=True)
        return 2

    write_json(run_dir / "preflight.json", info)

    if args.score_only:
        pack_rows = load_p1_pack()
        metrics = score_run(run_dir, pack_rows)
        write_json(run_dir / "metrics.json", metrics)
        print(json.dumps({"run_id": run_id, "dir": str(run_dir), "scored": True}, indent=2))
        return 0

    pack_rows = load_p1_pack()
    try:
        if args.stage_a:
            records = smoke_subset(pack_rows)
            arms = ["B0", "PHASE1-CORE"]
            summary = run_live(
                stage="A_smoke",
                records=records,
                arms=arms,
                run_dir=run_dir,
                run_id=run_id,
                commit=commit,
                episode_ids=list(SMOKE_EPISODE_IDS),
            )
            print("STATUS=STAGE_A_COMPLETE", flush=True)
            print(
                "HUMAN GATE: do not start Stage B without explicit approval.",
                flush=True,
            )
        else:
            records = pack_rows
            arms = list(PRIMARY_ARMS)
            summary = run_live(
                stage="B_full",
                records=records,
                arms=arms,
                run_dir=run_dir,
                run_id=run_id,
                commit=commit,
                episode_ids=[str(r["id"]) for r in records],
            )
            print("STATUS=STAGE_B_COMPLETE", flush=True)
    except L1GateError as exc:
        print(f"STATUS={exc.status}", flush=True)
        print(exc.message, file=sys.stderr, flush=True)
        return 2

    print(json.dumps(summary, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
