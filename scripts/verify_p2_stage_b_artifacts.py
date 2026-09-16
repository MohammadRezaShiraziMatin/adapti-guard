#!/usr/bin/env python3
"""Independently recompute Stage-B metrics from raw predictions/event_trace.

Does NOT trust summary.json blindly. Offline only — no API/LLM/network.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adapti_guard.experiments.p2_agentic_live import PACK_SHA256, P2LiveGateError
from adapti_guard.experiments.p2_stage_b import (
    STAGE_B_EXPECTED_EPISODE_ARMS,
    assert_episode_arm_coverage,
    assert_stage_b_pack_locked,
    detect_invalid_tool_args,
    score_stage_b_results,
)
from adapti_guard.metrics.tool_hasr import (
    compute_judge_asr,
    compute_tool_hasr,
    disagreement_rows,
)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def verify_stage_b_dir(run_dir: Path) -> dict[str, Any]:
    run_dir = Path(run_dir)
    preds_path = run_dir / "predictions.jsonl"
    metrics_path = run_dir / "metrics.json"
    summary_path = run_dir / "summary.json"
    manifest_path = run_dir / "manifest.json"
    events_path = run_dir / "event_trace.jsonl"

    errors: list[str] = []
    for required in (preds_path, metrics_path, summary_path, manifest_path):
        if not required.is_file():
            errors.append(f"missing {required.name}")
    if errors:
        return {"status": "VERIFY_FAIL", "errors": errors}

    pack = assert_stage_b_pack_locked()
    predictions = _load_jsonl(preds_path)
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    run_id = str(manifest.get("run_id") or summary.get("run_id") or "")
    if not run_id:
        errors.append("missing run_id")

    if manifest.get("benchmark_sha256") != PACK_SHA256:
        errors.append(
            f"manifest SHA {manifest.get('benchmark_sha256')} != locked {PACK_SHA256}"
        )

    try:
        coverage = assert_episode_arm_coverage(predictions, run_id=run_id)
    except P2LiveGateError as exc:
        errors.append(f"coverage: {exc.status}: {exc.message}")
        coverage = None

    recomputed = score_stage_b_results(predictions)
    tool = compute_tool_hasr(predictions)
    judge = compute_judge_asr(predictions)
    disagrees = disagreement_rows(predictions)
    m3 = [d for d in disagrees if d["pattern"] == "M3_judge_success_tool_not_executed"]
    m4 = [d for d in disagrees if d["pattern"] == "M4_tool_executed_judge_not_success"]

    # Compare primary rates to metrics.json (not summary)
    reported_tool = (metrics.get("primary") or {}).get("point_estimate")
    reported_judge = (metrics.get("secondary") or {}).get("point_estimate")
    if reported_tool is not None and tool["rate"] is not None:
        if abs(float(reported_tool) - float(tool["rate"])) > 1e-12:
            errors.append(
                f"Tool-HASR mismatch reported={reported_tool} recomputed={tool['rate']}"
            )
    if reported_judge is not None and judge["rate"] is not None:
        if abs(float(reported_judge) - float(judge["rate"])) > 1e-12:
            errors.append(
                f"Judge-ASR mismatch reported={reported_judge} recomputed={judge['rate']}"
            )

    if int(metrics.get("disagreements", {}).get("n_M3", -1)) != len(m3):
        errors.append("M3 count mismatch vs recomputed")
    if int(metrics.get("disagreements", {}).get("n_M4", -1)) != len(m4):
        errors.append("M4 count mismatch vs recomputed")

    # summary.json must not be the sole source of truth — cross-check against predictions
    if int(summary.get("n_results") or -1) != len(predictions):
        errors.append("summary n_results != predictions length")
    if len(predictions) != STAGE_B_EXPECTED_EPISODE_ARMS and coverage is not None:
        errors.append(
            f"n_predictions={len(predictions)} expected={STAGE_B_EXPECTED_EPISODE_ARMS}"
        )

    invalid_n = sum(1 for r in predictions if detect_invalid_tool_args(r))
    events_n = len(_load_jsonl(events_path)) if events_path.is_file() else 0

    status = "VERIFY_PASS" if not errors else "VERIFY_FAIL"
    return {
        "status": status,
        "errors": errors,
        "run_id": run_id,
        "pack_sha256": pack["benchmark_sha256"],
        "n_predictions": len(predictions),
        "coverage": coverage,
        "recomputed": {
            "Tool-HASR": tool,
            "Judge-ASR": judge,
            "n_M3": len(m3),
            "n_M4": len(m4),
            "mean_intervention_cost": recomputed["intervention"]["mean_intervention_cost"],
            "action_distribution": recomputed["intervention"]["action_distribution"],
            "utility_benign_twin": recomputed["benign_utility"]["utility_benign_twin"],
            "benign_twin_FPR": recomputed["benign_utility"]["benign_twin_FPR"],
            "invalid_tool_args_episodes": invalid_n,
        },
        "event_trace_rows": events_n,
        "trusted_summary_blindly": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path, help="Stage-B artifact directory")
    args = parser.parse_args()
    try:
        report = verify_stage_b_dir(args.run_dir)
    except P2LiveGateError as exc:
        print(json.dumps({"status": "VERIFY_FAIL", "errors": [f"{exc.status}: {exc.message}"]}))
        print(f"STATUS={exc.status}", flush=True)
        return 2
    print(json.dumps(report, indent=2, default=str))
    print(f"STATUS={report['status']}", flush=True)
    return 0 if report["status"] == "VERIFY_PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
