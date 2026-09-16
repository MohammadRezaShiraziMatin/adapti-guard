"""P3-C Stage-A live smoke helpers (detector × policy Cartesian product).

Scientific status: Stage A infrastructure validation only.
  scientific_evidence = false
  stage = A

Locked contract mirrors P2 live:
  Pack SHA, models, temperature=0.0, cache off, P2.4 tool states.
Detectors: D0/D1/D2/D4 (D3 deferred). Policies: B0, STATIC-A1, PHASE1-CORE.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from adapti_guard.detectors import DEFERRED_DETECTORS, default_p3_detectors, list_detector_catalog
from adapti_guard.detectors.base import P1_SHA256, P2_SHA256, assert_pack_sha, assert_unique_ids
from adapti_guard.detectors.core_adapter import P3CoreDetectorAdapter
from adapti_guard.detectors.harness import make_evaluation_id
from adapti_guard.detectors.protocol import ACTION_COSTS, config_bundle_hash
from adapti_guard.evaluation.experiment_logging import git_commit
from adapti_guard.evaluation.prediction_provenance import PROVENANCE_SCHEMA_VERSION
from adapti_guard.experiments.defense_baselines import (
    get_defense_fn,
    make_b0_no_defense,
    make_core_defense,
    make_l1_fixed_sanitize,
)
from adapti_guard.experiments.p2_agentic_live import (
    ARTIFACT_ROOT as _P2_ARTIFACT_ROOT,  # noqa: F401 — imported for reference only
    CONFIG_VERSION,
    LOCKED_BACKEND,
    LOCKED_JUDGE,
    LOCKED_JUDGE_KEY,
    LOCKED_SEED,
    LOCKED_TARGET,
    LOCKED_TARGET_KEY,
    LOCKED_TEMPERATURE,
    LiveRunStats,
    P2LiveGateError,
    PACK_PATH,
    PACK_SHA256,
    P1_PATH,
    build_run_manifest as _p2_build_run_manifest,
    evaluate_trajectory_live,
    load_p2_pack,
    preflight as p2_preflight,
    score_stage_a_results,
    write_json,
)
from adapti_guard.metrics.tool_hasr import COSTS, compute_p2_security_bundle, disagreement_rows

ROOT = Path(__file__).resolve().parents[3]

ARTIFACT_ROOT = ROOT / "experiments" / "real_llm_eval" / "P3_DETECTOR_COMPARISON"
LIVE_HARNESS_VERSION = "p3.0.0-live-stage-a"

PRIMARY_POLICIES = ("B0", "STATIC-A1", "PHASE1-CORE")
OPERATIONAL_DETECTORS = ("D0", "D1", "D2", "D4")

# Deterministic Stage-A smoke: 2 attack + 2 benign twins + 1 hard-negative.
P3_SMOKE_TRAJECTORY_IDS = (
    "p2a_atk_001",
    "p2a_atk_011",
    "p2a_ben_001",
    "p2a_ben_011",
    "p2a_hn_001",
)
P3_SMOKE_ATTACK_IDS = ("p2a_atk_001", "p2a_atk_011")
P3_SMOKE_BENIGN_TWIN_IDS = ("p2a_ben_001", "p2a_ben_011")
P3_SMOKE_HARD_NEGATIVE_IDS = ("p2a_hn_001",)

EXPECTED_N_ARMS = (
    len(P3_SMOKE_TRAJECTORY_IDS)
    * len(OPERATIONAL_DETECTORS)
    * len(PRIMARY_POLICIES)
)  # 60


class P3LiveGateError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        super().__init__(f"{code}: {detail}" if detail else code)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def tool_schema_hash() -> str:
    path = ROOT / "src" / "adapti_guard" / "defense" / "tool_schema.py"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prompt_template_hash() -> str:
    from adapti_guard.experiments.p2_agentic_live import TOOL_REQUEST_SYSTEM_HINT

    blob = TOOL_REQUEST_SYSTEM_HINT.encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def verify_frozen_integrity() -> dict[str, str]:
    return {
        "p1_sha256": assert_pack_sha(P1_PATH, P1_SHA256, label="P1"),
        "p2_sha256": assert_pack_sha(PACK_PATH, P2_SHA256, label="P2"),
    }


def p3_smoke_subset(pack_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_id = {str(r["id"]): dict(r) for r in pack_rows}
    missing = [tid for tid in P3_SMOKE_TRAJECTORY_IDS if tid not in by_id]
    if missing:
        raise P3LiveGateError("STOP_SMOKE_IDS_MISSING", f"missing: {missing}")
    attacks = [by_id[i] for i in P3_SMOKE_ATTACK_IDS]
    twins = [by_id[i] for i in P3_SMOKE_BENIGN_TWIN_IDS]
    hards = [by_id[i] for i in P3_SMOKE_HARD_NEGATIVE_IDS]
    if any(r.get("label") != "attack" for r in attacks):
        raise P3LiveGateError("STOP_SMOKE_COMPOSITION", "attack ids invalid")
    if any(r.get("label") != "benign" for r in twins + hards):
        raise P3LiveGateError("STOP_SMOKE_COMPOSITION", "benign/hn ids invalid")
    if any(not bool(r.get("hard_negative")) for r in hards):
        raise P3LiveGateError("STOP_SMOKE_COMPOSITION", "hard-negative unmarked")
    if any(bool(r.get("hard_negative")) for r in twins):
        raise P3LiveGateError("STOP_SMOKE_COMPOSITION", "twin marked hard_negative")
    return [by_id[tid] for tid in P3_SMOKE_TRAJECTORY_IDS]


def stage_a_cartesian_schedule() -> list[tuple[str, str, str]]:
    """Full trajectory × detector × policy product (max 60)."""
    arms: list[tuple[str, str, str]] = []
    for tid in P3_SMOKE_TRAJECTORY_IDS:
        for did in OPERATIONAL_DETECTORS:
            for pid in PRIMARY_POLICIES:
                arms.append((tid, did, pid))
    if len(arms) != EXPECTED_N_ARMS:
        raise P3LiveGateError(
            "STOP_ARM_COUNT", f"expected {EXPECTED_N_ARMS} got {len(arms)}"
        )
    return arms


def get_p3_defense_fn(policy_key: str, detector_id: str):
    """Build defense fn. Detector injects only into PHASE1-CORE."""
    if detector_id not in OPERATIONAL_DETECTORS:
        raise P3LiveGateError("STOP_DETECTOR", f"detector not operational: {detector_id}")
    if detector_id == "D3" or detector_id in DEFERRED_DETECTORS:
        raise P3LiveGateError("STOP_D3_DEFERRED", "D3 must remain deferred")

    dets = default_p3_detectors()
    p3_det = dets[detector_id]

    if policy_key == "B0":
        fn = make_b0_no_defense()
        adapter = P3CoreDetectorAdapter(p3_det)

        def wrapped(prompt: str, context: str | None = None, **kwargs):
            blob = kwargs.get("tool_call") if isinstance(kwargs.get("tool_call"), Mapping) else {}
            tool_name = kwargs.get("tool_name") or (blob.get("name") if blob else None)
            tool_output = kwargs.get("tool_output")
            probe = adapter.detect_episode(
                prompt or "",
                context,
                tool_name=str(tool_name) if tool_name else None,
                tool_output=str(tool_output) if tool_output else None,
            )
            out = fn(prompt, context)
            wrapped.last_detector_hit = bool(probe.is_injection)
            return out

        wrapped.last_detector_hit = False
        return wrapped, None

    if policy_key == "STATIC-A1":
        fn = make_l1_fixed_sanitize()
        adapter = P3CoreDetectorAdapter(p3_det)

        def wrapped(prompt: str, context: str | None = None, **kwargs):
            blob = kwargs.get("tool_call") if isinstance(kwargs.get("tool_call"), Mapping) else {}
            tool_name = kwargs.get("tool_name") or (blob.get("name") if blob else None)
            tool_output = kwargs.get("tool_output")
            probe = adapter.detect_episode(
                prompt or "",
                context,
                tool_name=str(tool_name) if tool_name else None,
                tool_output=str(tool_output) if tool_output else None,
            )
            out = fn(prompt, context)
            wrapped.last_detector_hit = bool(probe.is_injection)
            return out

        wrapped.last_detector_hit = False
        return wrapped, None

    if policy_key in ("PHASE1-CORE", "CORE"):
        adapter = P3CoreDetectorAdapter(p3_det)
        return make_core_defense(detector=adapter)

    raise P3LiveGateError("STOP_POLICY", f"unknown policy: {policy_key}")


def preflight_p3(*, require_key: bool = False) -> dict[str, Any]:
    info = p2_preflight(require_key=require_key)
    integrity = verify_frozen_integrity()
    if integrity["p2_sha256"] != PACK_SHA256 or integrity["p1_sha256"] != P1_SHA256:
        raise P3LiveGateError("STOP_SHA_MISMATCH", str(integrity))
    if "D3" in default_p3_detectors():
        raise P3LiveGateError("STOP_D3_PRESENT", "D3 must not be operational")
    info = dict(info)
    info["p3_harness_version"] = LIVE_HARNESS_VERSION
    info["p3_detectors"] = list_detector_catalog()
    info["p3_smoke_ids"] = list(P3_SMOKE_TRAJECTORY_IDS)
    info["expected_n_arms"] = EXPECTED_N_ARMS
    info["tool_schema_sha256"] = tool_schema_hash()
    info["prompt_template_sha256"] = prompt_template_hash()
    info["action_costs"] = dict(ACTION_COSTS)
    info["scientific_evidence"] = False
    info["stage"] = "A"
    return info


def build_p3_manifest(
    *,
    run_id: str,
    git_commit_value: str | None = None,
) -> dict[str, Any]:
    dets = default_p3_detectors()
    return {
        "run_id": run_id,
        "stage": "A",
        "scientific_evidence": False,
        "live_execution_authorized": True,
        "live_harness_version": LIVE_HARNESS_VERSION,
        "config_version": CONFIG_VERSION or PROVENANCE_SCHEMA_VERSION,
        "git_commit": git_commit_value or git_commit(),
        "p1_sha256": P1_SHA256,
        "p2_sha256": P2_SHA256,
        "benchmark_sha256": P2_SHA256,
        "pack_id": "p2_agentic_v0.1.0",
        "detectors": list_detector_catalog(),
        "detector_ids": list(OPERATIONAL_DETECTORS),
        "detector_config_bundle_hash": config_bundle_hash(dets),
        "detector_versions": {k: v.version for k, v in dets.items()},
        "detector_config_hashes": {k: v.config_hash() for k, v in dets.items()},
        "d3_status": DEFERRED_DETECTORS["D3"]["status"],
        "policy_ids": list(PRIMARY_POLICIES),
        "policy_version": "p2_primary_arms_v1",
        "policy_config_hash": hashlib.sha256(
            json.dumps(
                {"policies": list(PRIMARY_POLICIES), "costs": ACTION_COSTS},
                sort_keys=True,
            ).encode()
        ).hexdigest(),
        "action_costs": dict(ACTION_COSTS),
        "target_model": LOCKED_TARGET,
        "target_config_key": LOCKED_TARGET_KEY,
        "judge_model": LOCKED_JUDGE,
        "judge_config_key": LOCKED_JUDGE_KEY,
        "backend": LOCKED_BACKEND,
        "temperature": LOCKED_TEMPERATURE,
        "cache_enabled": False,
        "seed": LOCKED_SEED,
        "prompt_template_sha256": prompt_template_hash(),
        "tool_schema_sha256": tool_schema_hash(),
        "smoke_trajectory_ids": list(P3_SMOKE_TRAJECTORY_IDS),
        "expected_n_arms": EXPECTED_N_ARMS,
        "artifact_root": str(ARTIFACT_ROOT),
        "note": "Stage A is infrastructure smoke only — not scientific detector evidence.",
    }


def evaluate_p3_arm(
    record: Mapping[str, Any],
    *,
    detector_id: str,
    policy_key: str,
    run_id: str,
    target,
    judge,
    stats: LiveRunStats,
) -> dict[str, Any]:
    defense_fn, defense_state = get_p3_defense_fn(policy_key, detector_id)
    row = evaluate_trajectory_live(
        record,
        policy_key,
        target=target,
        judge=judge,
        tool_mode="scripted_preferred",
        call_judge=True,
        stats=stats,
        defense_fn=defense_fn,
        defense_state=defense_state,
    )
    row = dict(row)
    tid = str(row.get("trajectory_id") or row.get("id"))
    eid = make_evaluation_id(run_id, tid, detector_id, policy_id=policy_key)
    row["evaluation_id"] = eid
    row["detector_id"] = detector_id
    row["policy_id"] = policy_key
    row["policy_key"] = policy_key
    row["run_id"] = run_id
    row["stage"] = "A"
    row["scientific_evidence"] = False
    row["p3_harness_version"] = LIVE_HARNESS_VERSION
    return row


def score_p3_stage_a(results: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    rows = [dict(r) for r in results]
    assert_unique_ids([str(r["evaluation_id"]) for r in rows], what="evaluation_id")

    # Event tallies (canonical states only)
    state_counts: dict[str, int] = {
        "EXECUTED": 0,
        "POLICY_DENIED": 0,
        "INVALID_TOOL_ARGS": 0,
        "UNSUPPORTED_TOOL": 0,
        "RUNTIME_ERROR": 0,
        "TARGET_ERROR": 0,
        "JUDGE_ERROR": 0,
    }
    invalid_n = 0
    unsupported_n = 0
    runtime_n = 0
    for r in rows:
        if r.get("target_errors"):
            state_counts["TARGET_ERROR"] += 1
        for e in r.get("security_events") or []:
            st = str(e.get("primary_execution_state") or "")
            if st in state_counts:
                state_counts[st] += 1
            if st == "INVALID_TOOL_ARGS" or str(e.get("reason") or "") == "invalid_tool_arguments":
                invalid_n += 1
            if st == "UNSUPPORTED_TOOL":
                unsupported_n += 1
            if st == "RUNTIME_ERROR":
                runtime_n += 1

    overall = score_stage_a_results(rows)
    by_detector: dict[str, Any] = {}
    for did in OPERATIONAL_DETECTORS:
        subset = [r for r in rows if r.get("detector_id") == did]
        by_detector[did] = compute_p2_security_bundle(subset) if subset else {}

    by_policy: dict[str, Any] = {}
    for pid in PRIMARY_POLICIES:
        subset = [r for r in rows if r.get("policy_key") == pid]
        by_policy[pid] = compute_p2_security_bundle(subset) if subset else {}

    disagrees = disagreement_rows(rows)
    m3 = sum(1 for d in disagrees if str(d.get("pattern") or "").startswith("M3"))
    m4 = sum(1 for d in disagrees if str(d.get("pattern") or "").startswith("M4"))

    bundle = overall["bundle"]
    return {
        "stage": "A",
        "scientific_evidence": False,
        "n_results": len(rows),
        "n_expected_arms": EXPECTED_N_ARMS,
        "Tool-HASR": bundle.get("Tool-HASR"),
        "Judge-ASR": bundle.get("Judge-ASR"),
        "M3": m3,
        "M4": m4,
        "benign_utility": bundle.get("utility_benign_twin"),
        "hard_negative_utility": bundle.get("utility_hard_negative"),
        "benign_twin_FPR": bundle.get("benign_twin_FPR"),
        "hard_negative_FPR": bundle.get("hard_negative_FPR"),
        "intervention_rate": bundle.get("intervention_rate"),
        "mean_intervention_cost": bundle.get("mean_intervention_cost"),
        "action_distribution": bundle.get("action_distribution"),
        "invalid_tool_args_count": invalid_n,
        "unsupported_tool_count": unsupported_n,
        "runtime_error_count": runtime_n,
        "execution_state_counts": state_counts,
        "by_detector": by_detector,
        "by_policy": by_policy,
        "disagreements": disagrees,
        "costs": dict(COSTS),
        "note": "Stage A smoke — do not rank detectors or claim superiority.",
    }
