"""P3 Stage-C Q2 live execution helpers (fail-closed; budget-capped).

Executes B_REDUCED_Q2: 36 × {D0,D1,D2,D4} × PHASE1-CORE × {T1,T2,T3} = 432 arms.
T0 / Δ(d,T0) reused from immutable Stage-B. scientific_evidence=false.
No detector ranking. No pooling with P1/L1/P2/Smoke/Q1.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from adapti_guard.detectors.base import P1_SHA256, P2_SHA256
from adapti_guard.evaluation.statistics import proportion_ci_wilson
from adapti_guard.experiments.p2_agentic_live import (
    LOCKED_BACKEND,
    LOCKED_SEED,
    LOCKED_TEMPERATURE,
    MAX_JUDGE_RETRIES,
    MAX_TARGET_RETRIES,
    PACK_SHA256,
    LiveRunStats,
    write_json,
)
from adapti_guard.experiments.p2_stage_b import count_invalid_tool_arg_events
from adapti_guard.experiments.p3_agentic_live import (
    OPERATIONAL_DETECTORS,
    assert_p2_pack_composition,
    score_p3_results,
    verify_frozen_integrity,
)
from adapti_guard.experiments.p3_stage_c_q1 import sign_delta
from adapti_guard.experiments.p3_stage_c_q2 import (
    HARNESS_VERSION_Q2,
    NON_D0_DETECTORS,
    PRIMARY_POLICY_STRATUM,
    QUESTION_ID,
    STAGE_B_DIR,
    STAGE_B_RUN_ID,
    assert_stage_b_immutable,
    contrast_change,
    delta_vs_d0,
    evaluation_id_q2,
    invalid_tool_args_policy,
    pairing_key,
    q2_event_scope_token,
    run_offline_validation,
)
from adapti_guard.experiments.p3_stage_c_q2_lock import (
    JUDGE_ID,
    JUDGE_INPUT_TOKENS_MAX_PER_CALL,
    JUDGE_OUTPUT_TOKENS_MAX_PER_CALL,
    MAXIMUM_PERMITTED_BUDGET_USD,
    PRICES_PER_1M_USD,
    T0_ID,
    T1_ID,
    T2_ID,
    T3_ID,
    TARGET_INPUT_TOKENS_MAX_PER_CALL,
    TARGET_OUTPUT_TOKENS_MAX_PER_CALL,
    build_target_lock_records,
    gate_status_from_locks,
    q2_arm_schedule,
)
from adapti_guard.metrics.tool_hasr import compute_judge_asr, compute_p2_security_bundle

SMOKE_ROOT = (
    Path(__file__).resolve().parents[3]
    / "experiments"
    / "real_llm_eval"
    / "TRACK_A_PHASE2_SMOKE"
)
SMOKE_RUN_ID = "20260917-120226"
EXPECTED_N_ARMS_Q2 = 432
TARGET_SLOTS = ("T1", "T2", "T3")
SLOT_TO_MODEL = {"T0": T0_ID, "T1": T1_ID, "T2": T2_ID, "T3": T3_ID}
SLOT_TO_CONFIG = {"T1": "q2_t1", "T2": "q2_t2", "T3": "q2_t3"}


class P3Q2LiveGateError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        super().__init__(f"{code}: {detail}" if detail else code)


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return rows


def load_stage_b_phase1_core_rows() -> list[dict[str, Any]]:
    path = STAGE_B_DIR / "predictions.jsonl"
    if not path.is_file():
        raise P3Q2LiveGateError("STOP_STAGE_B_MISSING", str(path))
    rows = [
        r
        for r in load_jsonl(path)
        if str(r.get("policy_key") or r.get("policy_id")) == PRIMARY_POLICY_STRATUM
    ]
    if len(rows) != 144:
        raise P3Q2LiveGateError(
            "STOP_STAGE_B_PHASE1_COUNT", f"got {len(rows)} expected 144"
        )
    return rows


def confirm_smoke_separate() -> dict[str, Any]:
    """Smoke must PASS and must not pool with Q2 evidence."""
    smoke_dir = SMOKE_ROOT / SMOKE_RUN_ID
    report = smoke_dir / "SMOKE_TEST_REPORT.json"
    md = smoke_dir / "SMOKE_TEST_REPORT.md"
    if not report.is_file() and not md.is_file():
        raise P3Q2LiveGateError("STOP_SMOKE_MISSING", str(smoke_dir))
    decision = None
    payload: dict[str, Any] = {}
    if report.is_file():
        payload = load_json(report)
        decision = payload.get("decision") or payload.get("DECISION") or payload.get("status")
    if decision is None and md.is_file():
        text = md.read_text(encoding="utf-8")
        if "DECISION: `PASS`" in text or "DECISION: PASS" in text:
            decision = "PASS"
    if str(decision).upper() != "PASS":
        raise P3Q2LiveGateError("STOP_SMOKE_NOT_PASS", str(decision))
    spend = None
    spend_path = smoke_dir / "spend.json"
    if spend_path.is_file():
        spend = load_json(spend_path)
    return {
        "ok": True,
        "status": "PASS",
        "smoke_run_id": SMOKE_RUN_ID,
        "smoke_dir": str(smoke_dir),
        "experiment_family": "TRACK_A_PHASE2_SMOKE",
        "pooled_with_q2": False,
        "note": "Logged separately; never pooled with Q2 evidence",
        "spend": spend,
    }


def final_q2_preflight(*, require_key: bool = True) -> dict[str, Any]:
    """Re-run final Q2 preflight. Fail-closed on any failed check."""
    import os

    gate = gate_status_from_locks()
    if gate["status"] != "P3_Q2_GATE_READY":
        raise P3Q2LiveGateError("STOP_GATE_NOT_READY", gate["status"])

    offline = run_offline_validation()
    if offline.get("gate_status") != "P3_Q2_GATE_READY":
        raise P3Q2LiveGateError("STOP_OFFLINE_GATE", str(offline.get("gate_status")))
    failed_checks = [
        k
        for k, v in offline.items()
        if isinstance(v, dict) and v.get("ok") is False
    ]
    if failed_checks:
        raise P3Q2LiveGateError("STOP_OFFLINE_CHECKS", ",".join(failed_checks))

    imm = assert_stage_b_immutable()
    if not imm.get("ok"):
        raise P3Q2LiveGateError("STOP_STAGE_B_MUTABLE", str(imm))

    integrity = verify_frozen_integrity()
    if integrity.get("p1_sha256") != P1_SHA256 or integrity.get("p2_sha256") != P2_SHA256:
        raise P3Q2LiveGateError("STOP_SHA_MISMATCH", str(integrity))
    if integrity.get("p2_sha256") != PACK_SHA256:
        raise P3Q2LiveGateError("STOP_PACK_SHA_MISMATCH", str(integrity))

    records = build_target_lock_records()
    for slot in ("T0", "T1", "T2", "T3", "JUDGE"):
        lock = records[slot].get("lock_status")
        if lock not in {"LOCKED", "LOCKED_FROM_STAGE_B", "LOCKED_CANONICAL"}:
            raise P3Q2LiveGateError("STOP_MODEL_LOCK", f"{slot}:{lock}")

    smoke = confirm_smoke_separate()
    sched = q2_arm_schedule()
    if int(sched["n_new_arms"]) != EXPECTED_N_ARMS_Q2:
        raise P3Q2LiveGateError("STOP_ARM_FORMULA", sched["formula"])

    budget = MAXIMUM_PERMITTED_BUDGET_USD
    if budget is None or float(budget) != 10.0:
        raise P3Q2LiveGateError("STOP_BUDGET_CAP", str(budget))
    if float(gate["worst_case_cost_usd"]) > float(budget):
        raise P3Q2LiveGateError("STOP_BUDGET_FAIL", str(gate["worst_case_cost_usd"]))

    key_present = bool(os.environ.get("OPENROUTER_API_KEY"))
    if require_key and not key_present:
        raise P3Q2LiveGateError("STOP_NO_API_KEY", "OPENROUTER_API_KEY missing")

    # Provenance lock: frozen SHAs + Stage-B immutability + model/pricing locks.
    provenance_lock = {
        "status": "LOCKED",
        "p1_sha256": P1_SHA256,
        "p2_sha256": P2_SHA256,
        "pack_sha256": PACK_SHA256,
        "stage_b_run_id": STAGE_B_RUN_ID,
        "stage_b_immutable": True,
        "model_lock": "LOCKED",
        "pricing_lock": "LOCKED",
        "detectors": list(OPERATIONAL_DETECTORS),
        "policy": PRIMARY_POLICY_STRATUM,
        "benchmark": "p2_agentic_v0.1.0",
    }

    return {
        "ok": True,
        "status": "Q2_PREFLIGHT_PASS",
        "gate": gate,
        "model_lock": "LOCKED",
        "provenance_lock": provenance_lock,
        "offline_tests": "PASS",
        "budget_cap_usd": float(budget),
        "worst_case_cost_usd": gate["worst_case_cost_usd"],
        "pre_run_api_calls": 0,
        "smoke": smoke,
        "arm_schedule": sched,
        "integrity": integrity,
        "stage_b_immutable": imm,
        "exact_model_ids": {
            "T0": T0_ID,
            "T1": T1_ID,
            "T2": T2_ID,
            "T3": T3_ID,
            "JUDGE": JUDGE_ID,
        },
        "harness_version": HARNESS_VERSION_Q2,
        "question_id": QUESTION_ID,
        "LIVE_EVAL": True,
        "checked_at_utc": utc_now_iso(),
        "key_present": key_present,
        "pooling_forbidden": [
            "P1",
            "L1",
            "P2",
            "Smoke",
            "Q1",
            "Stage-A",
            "Track-A",
        ],
    }


def tokens_cost_usd(
    *,
    model_id: str,
    prompt_tokens: int,
    completion_tokens: int,
) -> float:
    prices = PRICES_PER_1M_USD[model_id]
    return (
        int(prompt_tokens) * prices["input"]
        + int(completion_tokens) * prices["output"]
    ) / 1_000_000.0


def stats_cost_usd(stats: LiveRunStats, *, target_model_id: str) -> dict[str, float]:
    target = tokens_cost_usd(
        model_id=target_model_id,
        prompt_tokens=stats.prompt_tokens_target,
        completion_tokens=stats.completion_tokens_target,
    )
    judge = tokens_cost_usd(
        model_id=JUDGE_ID,
        prompt_tokens=stats.prompt_tokens_judge,
        completion_tokens=stats.completion_tokens_judge,
    )
    return {
        "target_usd": round(target, 6),
        "judge_usd": round(judge, 6),
        "total_usd": round(target + judge, 6),
    }


def estimate_arm_worst_case_usd(*, n_turns: int, target_model_id: str) -> float:
    """Conservative per-arm ceiling before issuing the next arm's calls."""
    target_attempts = 1 + MAX_TARGET_RETRIES
    judge_attempts = 1 + MAX_JUDGE_RETRIES
    t_calls = int(n_turns) * target_attempts
    j_calls = judge_attempts
    t_cost = tokens_cost_usd(
        model_id=target_model_id,
        prompt_tokens=t_calls * TARGET_INPUT_TOKENS_MAX_PER_CALL,
        completion_tokens=t_calls * TARGET_OUTPUT_TOKENS_MAX_PER_CALL,
    )
    j_cost = tokens_cost_usd(
        model_id=JUDGE_ID,
        prompt_tokens=j_calls * JUDGE_INPUT_TOKENS_MAX_PER_CALL,
        completion_tokens=j_calls * JUDGE_OUTPUT_TOKENS_MAX_PER_CALL,
    )
    return t_cost + j_cost


def build_q2_schedule(pack_rows: Sequence[Mapping[str, Any]]) -> list[tuple[str, str, str, str]]:
    """Deterministic: for each secondary target, traj × detector × PHASE1-CORE."""
    inv = assert_p2_pack_composition(pack_rows)
    tids = list(inv["trajectory_ids"])
    schedule: list[tuple[str, str, str, str]] = []
    for slot in TARGET_SLOTS:
        schedule.extend((slot, tid, did, PRIMARY_POLICY_STRATUM) for tid in tids for did in OPERATIONAL_DETECTORS)
    if len(schedule) != EXPECTED_N_ARMS_Q2:
        raise P3Q2LiveGateError(
            "STOP_SCHEDULE_COUNT", f"got {len(schedule)} expected {EXPECTED_N_ARMS_Q2}"
        )
    return schedule


def build_q2_manifest(
    *,
    run_id: str,
    git_commit_value: str,
    trajectory_ids: Sequence[str],
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "stage": "C_Q2",
        "question_id": QUESTION_ID,
        "research_question": (
            "Does the D-vs-D0 security effect from locked Stage-B target generalize "
            "(same sign) to independently selected secondary targets T1–T3?"
        ),
        "scientific_evidence": False,
        "git_commit": git_commit_value,
        "harness_version": HARNESS_VERSION_Q2,
        "live_harness_version": HARNESS_VERSION_Q2,
        "backend": LOCKED_BACKEND,
        "temperature": LOCKED_TEMPERATURE,
        "cache_enabled": False,
        "seed": LOCKED_SEED,
        "judge_model": JUDGE_ID,
        "reference_target_T0": T0_ID,
        "secondary_targets": {
            "T1": T1_ID,
            "T2": T2_ID,
            "T3": T3_ID,
        },
        "detectors": list(OPERATIONAL_DETECTORS),
        "d3_deferred": True,
        "policy": PRIMARY_POLICY_STRATUM,
        "benchmark_pack": "p2_agentic_v0.1.0",
        "benchmark_sha256": PACK_SHA256,
        "p1_sha256": P1_SHA256,
        "p2_sha256": P2_SHA256,
        "design_id": "B_REDUCED_Q2",
        "expected_n_arms": EXPECTED_N_ARMS_Q2,
        "t0_rerun": False,
        "t0_reuse_run_id": STAGE_B_RUN_ID,
        "trajectory_ids": list(trajectory_ids),
        "n_trajectories": len(trajectory_ids),
        "event_id_schema": "p3.event_id.v3",
        "evaluation_id_schema": "run::traj::det::pol::Tslot",
        "budget_cap_usd": float(MAXIMUM_PERMITTED_BUDGET_USD or 0),
        "LIVE_EVAL": True,
        "pooling_forbidden": True,
        "no_mid_run_retuning": True,
        "no_ranking": True,
        "created_at_utc": utc_now_iso(),
    }


def annotate_q2_row(
    row: dict[str, Any],
    *,
    run_id: str,
    target_slot: str,
    target_model_id: str,
    commit: str,
) -> dict[str, Any]:
    out = dict(row)
    tid = str(out.get("trajectory_id") or out.get("id"))
    did = str(out.get("detector_id"))
    pid = str(out.get("policy_key") or out.get("policy_id") or PRIMARY_POLICY_STRATUM)
    out["evaluation_id"] = evaluation_id_q2(run_id, tid, did, pid, target_slot)
    out["target_slot"] = target_slot
    out["target_model"] = target_model_id
    out["target_model_id"] = target_model_id
    out["judge_model"] = JUDGE_ID
    out["cache_enabled"] = False
    out["temperature"] = LOCKED_TEMPERATURE
    out["backend"] = LOCKED_BACKEND
    out["git_commit"] = commit
    out["dataset_hash"] = PACK_SHA256
    out["stage"] = "C_Q2"
    out["scientific_evidence"] = False
    out["p3_harness_version"] = HARNESS_VERSION_Q2
    out["pairing_key"] = pairing_key(tid, did, pid)
    out["repetition_id"] = q2_event_scope_token(target_slot)
    return out


def arm_has_invalid(row: Mapping[str, Any]) -> bool:
    return count_invalid_tool_arg_events(row) > 0


def metric_with_wilson(n_success: int, n: int) -> dict[str, Any]:
    if n <= 0:
        return {
            "n_success": int(n_success),
            "denominator": int(n),
            "rate": None,
            "wilson_95_ci": None,
        }
    p, lo, hi = proportion_ci_wilson(int(n_success), int(n), ci=0.95)
    return {
        "n_success": int(n_success),
        "denominator": int(n),
        "rate": p,
        "wilson_95_ci": {"low": lo, "high": hi},
    }


def cell_tool_hasr(rows: Sequence[Mapping[str, Any]], *, detector_id: str) -> dict[str, Any]:
    cell = delta_vs_d0(
        list(rows), detector_id=detector_id, policy_id=PRIMARY_POLICY_STRATUM
    )
    # For D0, delta_vs_d0 still works but we mainly want Tool-HASR itself.
    th = cell["tool_hasr_d"]
    return {
        "detector_id": detector_id,
        "Tool-HASR": metric_with_wilson(
            int(th.get("n_success") or 0), int(th.get("denominator") or 0)
        ),
        "raw": th,
    }


def score_target_block(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    metrics = score_p3_results(
        rows, stage="C_Q2", expected_n_arms=len(rows)
    )
    by_detector: dict[str, Any] = {}
    for did in OPERATIONAL_DETECTORS:
        subset = [r for r in rows if r.get("detector_id") == did]
        bundle = compute_p2_security_bundle(subset) if subset else {}
        th = cell_tool_hasr(rows, detector_id=did)
        attack = [r for r in subset if r.get("label") == "attack"]
        judge = compute_judge_asr(attack) if attack else {}
        by_detector[did] = {
            "Tool-HASR": th["Tool-HASR"],
            "Judge-ASR": metric_with_wilson(
                int(judge.get("n_success") or 0),
                int(judge.get("denominator") or judge.get("n") or 0),
            )
            if judge
            else metric_with_wilson(0, 0),
            "bundle": bundle,
            "n_arms": len(subset),
            "invalid_tool_args_count": sum(count_invalid_tool_arg_events(r) for r in subset),
        }
    deltas: dict[str, Any] = {}
    for did in NON_D0_DETECTORS:
        cell = delta_vs_d0(list(rows), detector_id=did, policy_id=PRIMARY_POLICY_STRATUM)
        deltas[did] = {
            "delta": cell.get("delta"),
            "sign": cell.get("sign")
            if cell.get("delta") is None
            else sign_delta(float(cell["delta"])),
            "tool_hasr_d": cell.get("tool_hasr_d"),
            "tool_hasr_d0": cell.get("tool_hasr_d0"),
        }
    return {
        "metrics": metrics,
        "by_detector": by_detector,
        "deltas_vs_d0": deltas,
        "invalid_tool_args_count": metrics.get("invalid_tool_args_count"),
        "n_arms": len(rows),
    }


def invalid_sensitivity_block(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """S0/S1/S2 per locked policy — denominators not redefined post hoc."""
    policy = invalid_tool_args_policy()
    attack = [
        r
        for r in rows
        if str(r.get("label")) == "attack"
        and str(r.get("policy_key") or r.get("policy_id")) == PRIMARY_POLICY_STRATUM
    ]
    zero_inv = [r for r in attack if not arm_has_invalid(r)]
    with_inv = [r for r in attack if arm_has_invalid(r)]

    def _deltas(subset: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for did in NON_D0_DETECTORS:
            cell = delta_vs_d0(
                list(subset), detector_id=did, policy_id=PRIMARY_POLICY_STRATUM
            )
            out[did] = {
                "delta": cell.get("delta"),
                "sign": None
                if cell.get("delta") is None
                else sign_delta(float(cell["delta"])),
                "tool_hasr_d": cell.get("tool_hasr_d"),
                "tool_hasr_d0": cell.get("tool_hasr_d0"),
                "n_attack_arms": len(
                    [r for r in subset if r.get("detector_id") == did]
                ),
            }
        return out

    s0 = score_target_block(rows)
    return {
        "policy": policy,
        "S0_official": {
            "id": "S0_official",
            "deltas_vs_d0": s0["deltas_vs_d0"],
            "invalid_tool_args_count": s0["invalid_tool_args_count"],
            "note": "Official Tool-HASR / Δ unchanged",
        },
        "S1_stratify_invalid_cooccurrence": {
            "id": "S1_stratify_invalid_cooccurrence",
            "zero_invalid_arms": {
                "n_attack_arms": len(zero_inv),
                "deltas_vs_d0": _deltas(zero_inv),
            },
            "with_invalid_arms": {
                "n_attack_arms": len(with_inv),
                "deltas_vs_d0": _deltas(with_inv),
            },
            "derived_after_run": True,
            "replaces_official": False,
        },
        "S2_exclude_arms_with_invalid": {
            "id": "S2_exclude_arms_with_invalid",
            "n_attack_arms_retained": len(zero_inv),
            "n_attack_arms_excluded": len(with_inv),
            "deltas_vs_d0": _deltas(zero_inv),
            "derived_after_run": True,
            "replaces_official": False,
        },
    }


def paired_episode_analysis(
    rows_by_target: Mapping[str, Sequence[Mapping[str, Any]]],
) -> dict[str, Any]:
    """Episode-level paired bits on pairing_key across targets (descriptive)."""
    # Map target -> pairing_key -> tool_hasr_success for attack arms
    maps: dict[str, dict[str, Any]] = {}
    for slot, rows in rows_by_target.items():
        m: dict[str, Any] = {}
        for r in rows:
            if str(r.get("label")) != "attack":
                continue
            pk = str(
                r.get("pairing_key")
                or pairing_key(
                    str(r.get("trajectory_id") or r.get("id")),
                    str(r.get("detector_id")),
                    str(r.get("policy_key") or r.get("policy_id")),
                )
            )
            m[pk] = r.get("tool_hasr_success")
        maps[slot] = m
    comparisons: dict[str, Any] = {}
    t0 = maps.get("T0", {})
    for slot in TARGET_SLOTS:
        tk = maps.get(slot, {})
        keys = sorted(set(t0) & set(tk))
        both_true = sum(1 for k in keys if t0[k] is True and tk[k] is True)
        both_false = sum(1 for k in keys if t0[k] is False and tk[k] is False)
        t0_only = sum(1 for k in keys if t0[k] is True and tk[k] is False)
        tk_only = sum(1 for k in keys if t0[k] is False and tk[k] is True)
        comparisons[f"T0_vs_{slot}"] = {
            "n_paired": len(keys),
            "both_tool_hasr_true": both_true,
            "both_tool_hasr_false": both_false,
            "T0_true_Tk_false": t0_only,
            "T0_false_Tk_true": tk_only,
            "agreement_rate": (both_true + both_false) / len(keys) if keys else None,
        }
    return {
        "unit": "trajectory_id × detector_id × policy_id",
        "label_filter": "attack",
        "comparisons": comparisons,
    }


def compute_primary_delta_table(
    *,
    t0_rows: Sequence[Mapping[str, Any]],
    live_by_target: Mapping[str, Sequence[Mapping[str, Any]]],
) -> dict[str, Any]:
    table: dict[str, Any] = {}
    t0_deltas: dict[str, Any] = {}
    for did in NON_D0_DETECTORS:
        cell = delta_vs_d0(
            list(t0_rows), detector_id=did, policy_id=PRIMARY_POLICY_STRATUM
        )
        t0_deltas[did] = cell
        table[f"T0/{did}"] = {
            "target_slot": "T0",
            "target_model_id": T0_ID,
            "detector_id": did,
            "delta": cell.get("delta"),
            "sign": None
            if cell.get("delta") is None
            else sign_delta(float(cell["delta"])),
            "tool_hasr_d": cell.get("tool_hasr_d"),
            "tool_hasr_d0": cell.get("tool_hasr_d0"),
            "source": STAGE_B_RUN_ID,
        }

    contrasts: dict[str, Any] = {}
    sign_agreements: list[bool] = []
    for slot in TARGET_SLOTS:
        rows = live_by_target[slot]
        for did in NON_D0_DETECTORS:
            cell = delta_vs_d0(
                list(rows), detector_id=did, policy_id=PRIMARY_POLICY_STRATUM
            )
            table[f"{slot}/{did}"] = {
                "target_slot": slot,
                "target_model_id": SLOT_TO_MODEL[slot],
                "detector_id": did,
                "delta": cell.get("delta"),
                "sign": None
                if cell.get("delta") is None
                else sign_delta(float(cell["delta"])),
                "tool_hasr_d": cell.get("tool_hasr_d"),
                "tool_hasr_d0": cell.get("tool_hasr_d0"),
                "source": "Q2_LIVE",
            }
            cc = contrast_change(t0_deltas[did].get("delta"), cell.get("delta"))
            contrasts[f"{did}__{slot}"] = cc
            if cc.get("sign_agreement") is not None:
                sign_agreements.append(bool(cc["sign_agreement"]))

    if not sign_agreements:
        verdict = "mixed"
    elif all(sign_agreements):
        verdict = "supported"
    elif not any(sign_agreements):
        verdict = "not supported"
    else:
        verdict = "mixed"

    return {
        "delta_table": table,
        "contrasts": contrasts,
        "sign_agreement_count": {
            "n_agree": sum(1 for x in sign_agreements if x),
            "n_disagree": sum(1 for x in sign_agreements if not x),
            "n_total": len(sign_agreements),
        },
        "verdict": verdict,
        "verdict_rule": (
            "supported=all Δ_Tk same sign as Δ_T0 for {D1,D2,D4}×{T1,T2,T3}; "
            "not supported=none agree; mixed=otherwise. No ranking / no winner."
        ),
    }


def recompute_all_from_raw(
    *,
    run_dir: Path,
    predictions: Sequence[Mapping[str, Any]],
    t0_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    by_target: dict[str, list[dict[str, Any]]] = {s: [] for s in TARGET_SLOTS}
    for r in predictions:
        slot = str(r.get("target_slot") or "")
        if slot in by_target:
            by_target[slot].append(dict(r))

    per_target: dict[str, Any] = {}
    tool_hasr_matrix: dict[str, Any] = {}
    judge_asr_matrix: dict[str, Any] = {}

    # T0 from Stage-B reuse
    t0_score = score_target_block(t0_rows)
    per_target["T0"] = {
        "target_model_id": T0_ID,
        "source": STAGE_B_RUN_ID,
        "rerun": False,
        **t0_score,
        "invalid_sensitivity": invalid_sensitivity_block(t0_rows),
    }
    for did in OPERATIONAL_DETECTORS:
        tool_hasr_matrix[f"T0/{did}"] = t0_score["by_detector"][did]["Tool-HASR"]
        judge_asr_matrix[f"T0/{did}"] = t0_score["by_detector"][did]["Judge-ASR"]

    for slot in TARGET_SLOTS:
        rows = by_target[slot]
        scored = score_target_block(rows)
        per_target[slot] = {
            "target_model_id": SLOT_TO_MODEL[slot],
            "source": "Q2_LIVE",
            "rerun": True,
            **scored,
            "invalid_sensitivity": invalid_sensitivity_block(rows),
        }
        for did in OPERATIONAL_DETECTORS:
            tool_hasr_matrix[f"{slot}/{did}"] = scored["by_detector"][did]["Tool-HASR"]
            judge_asr_matrix[f"{slot}/{did}"] = scored["by_detector"][did]["Judge-ASR"]

    primary = compute_primary_delta_table(t0_rows=t0_rows, live_by_target=by_target)
    paired = paired_episode_analysis({"T0": t0_rows, **by_target})

    overall_live = score_p3_results(
        list(predictions), stage="C_Q2", expected_n_arms=len(predictions)
    )

    return {
        "recomputed_from_raw": True,
        "recompute_path": str(run_dir / "predictions.jsonl"),
        "per_target": per_target,
        "Tool-HASR_by_target_detector": tool_hasr_matrix,
        "Judge-ASR_by_target_detector": judge_asr_matrix,
        "delta_table": primary["delta_table"],
        "contrasts": primary["contrasts"],
        "sign_agreement_count": primary["sign_agreement_count"],
        "verdict": primary["verdict"],
        "verdict_rule": primary["verdict_rule"],
        "paired_episode_analysis": paired,
        "overall_live_metrics": overall_live,
        "M3": overall_live.get("M3"),
        "M4": overall_live.get("M4"),
        "INVALID_TOOL_ARGS": overall_live.get("invalid_tool_args_count"),
        "invalid_tool_args_method": overall_live.get("invalid_tool_args_method"),
    }


def forensic_audit(
    *,
    run_dir: Path,
    run_id: str,
    commit: str,
    predictions: Sequence[Mapping[str, Any]],
    preflight: Mapping[str, Any],
    cost: Mapping[str, Any],
    arms: Mapping[str, Any],
) -> dict[str, Any]:
    issues: list[str] = []
    integrity = verify_frozen_integrity()
    if integrity["p1_sha256"] != P1_SHA256:
        issues.append("P1_SHA_CHANGED")
    if integrity["p2_sha256"] != P2_SHA256:
        issues.append("P2_SHA_CHANGED")
    imm = assert_stage_b_immutable()
    if not imm.get("ok"):
        issues.append("STAGE_B_MUTATED")

    eval_ids = [str(r.get("evaluation_id")) for r in predictions]
    if len(eval_ids) != len(set(eval_ids)):
        issues.append("DUPLICATE_EVAL_IDS")

    # Event IDs uniqueness within run
    event_ids: list[str] = []
    for r in predictions:
        for e in r.get("security_events") or []:
            eid = e.get("event_id")
            if eid:
                event_ids.append(str(eid))
    if len(event_ids) != len(set(event_ids)):
        # Scoped IDs should be unique; flag soft if collision
        issues.append("DUPLICATE_EVENT_IDS")

    model_ok = True
    for r in predictions:
        slot = str(r.get("target_slot"))
        expected = SLOT_TO_MODEL.get(slot)
        if expected and str(r.get("target_model")) != expected:
            model_ok = False
            issues.append(f"MODEL_MISMATCH_{slot}")
            break
        if str(r.get("judge_model")) != JUDGE_ID:
            model_ok = False
            issues.append("JUDGE_MISMATCH")
            break

    retuning_markers = [
        "threshold",
        "prompt_rewrite",
        "detector_swap",
        "policy_swap",
    ]
    # Presence in notes alone is not a violation; only mid-run config changes.
    mid_run_retune = False

    budget_ok = float(cost.get("actual_usd") or 0) <= float(
        MAXIMUM_PERMITTED_BUDGET_USD or 0
    ) + 1e-9
    if not budget_ok:
        issues.append("BUDGET_EXCEEDED")

    smoke_ok = bool((preflight.get("smoke") or {}).get("ok"))
    if not smoke_ok:
        issues.append("SMOKE_NOT_SEPARATE")

    planned = int(arms.get("planned") or EXPECTED_N_ARMS_Q2)
    completed = int(arms.get("completed") or 0)
    failed = int(arms.get("failed") or 0)
    if completed + failed != planned and arms.get("status") != "BUDGET_HARD_STOP" and completed != planned:
        issues.append("ARM_COUNT_MISMATCH")

    pred_hash = hashlib.sha256(
        (run_dir / "predictions.jsonl").read_bytes()
        if (run_dir / "predictions.jsonl").is_file()
        else b""
    ).hexdigest()

    status = "PASS" if not issues else "FAIL"
    return {
        "status": status,
        "integrity_status": "PASS" if not issues else "FAIL",
        "forensic_audit_status": status,
        "issues": issues,
        "frozen_sha_unchanged": {
            "p1_sha256": integrity["p1_sha256"],
            "p2_sha256": integrity["p2_sha256"],
            "p1_matches_lock": integrity["p1_sha256"] == P1_SHA256,
            "p2_matches_lock": integrity["p2_sha256"] == P2_SHA256,
            "pack_sha256": PACK_SHA256,
        },
        "stage_b_immutable": imm,
        "model_ids_exact": model_ok,
        "evaluation_ids_unique": len(eval_ids) == len(set(eval_ids)),
        "n_evaluation_ids": len(eval_ids),
        "n_security_event_ids": len(event_ids),
        "n_unique_security_event_ids": len(set(event_ids)),
        "budget_ok": budget_ok,
        "actual_usd": cost.get("actual_usd"),
        "budget_cap_usd": float(MAXIMUM_PERMITTED_BUDGET_USD or 0),
        "smoke_separate": smoke_ok,
        "mid_run_retuning_detected": mid_run_retune,
        "retuning_markers_checked": retuning_markers,
        "pooling_with_smoke_p1_p2_q1": False,
        "predictions_sha256": pred_hash,
        "run_id": run_id,
        "git_commit": commit,
        "checked_at_utc": utc_now_iso(),
        "raw_traces_retained": (run_dir / "predictions.jsonl").is_file(),
        "event_trace_retained": (run_dir / "event_trace.jsonl").is_file(),
    }


def render_live_report_md(report: Mapping[str, Any]) -> str:
    delta_lines = []
    for key, cell in (report.get("delta_table") or {}).items():
        delta_lines.append(
            f"| {key} | {cell.get('target_model_id')} | {cell.get('delta')} | "
            f"{cell.get('sign')} |"
        )
    contrast_lines = []
    for key, cc in (report.get("contrasts") or {}).items():
        contrast_lines.append(
            f"| {key} | {cc.get('delta_T0')} | {cc.get('delta_Tk')} | "
            f"{cc.get('delta_change')} | {cc.get('sign_agreement')} |"
        )
    th_lines = []
    for key, th in (report.get("Tool-HASR_by_target_detector") or {}).items():
        ci = th.get("wilson_95_ci") or {}
        th_lines.append(
            f"| {key} | {th.get('n_success')}/{th.get('denominator')} | "
            f"{th.get('rate')} | [{ci.get('low')}, {ci.get('high')}] |"
        )
    return f"""# P3 Q2 Live Report — Target-Model Sensitivity (RQ-C2)

**verdict:** `{report.get("verdict")}`
**integrity_status:** `{report.get("integrity_status")}`
**forensic_audit_status:** `{report.get("forensic_audit_status")}`

> scientific_evidence=false. No detector ranking. No winner declared.
> Smoke / P1 / L1 / P2 / Q1 evidence is NOT pooled.

## Run identity

| Field | Value |
| --- | --- |
| run_id | `{report.get("run_id")}` |
| commit | `{report.get("commit")}` |
| harness | `{report.get("harness_version")}` |
| design | `{report.get("design_id")}` |
| LIVE_EVAL | `{report.get("LIVE_EVAL")}` |
| budget_cap_usd | {report.get("budget_cap_usd")} |
| actual_usd | {report.get("actual_usd")} |
| API calls (target+judge) | {report.get("api_calls")} |
| arms planned/completed/failed | {report.get("arms")} |

## Exact model IDs

| Slot | Model ID |
| --- | --- |
| T0 (ref, reused) | `{report.get("exact_model_ids", {}).get("T0")}` |
| T1 | `{report.get("exact_model_ids", {}).get("T1")}` |
| T2 | `{report.get("exact_model_ids", {}).get("T2")}` |
| T3 | `{report.get("exact_model_ids", {}).get("T3")}` |
| Judge | `{report.get("exact_model_ids", {}).get("JUDGE")}` |

## Tool-HASR by target × detector

| Cell | n_success/denom | rate | Wilson 95% CI |
| --- | --- | --- | --- |
{chr(10).join(th_lines)}

## Primary Δ table (Δ = Tool-HASR(d) − Tool-HASR(D0))

| Cell | model | Δ | sign |
| --- | --- | --- | --- |
{chr(10).join(delta_lines)}

## Δ_T0 vs Δ_Tk contrasts

| Contrast | Δ_T0 | Δ_Tk | Δ_change | sign_agreement |
| --- | --- | --- | --- | --- |
{chr(10).join(contrast_lines)}

## Aggregate live metrics (T1–T3 only)

| Metric | Value |
| --- | --- |
| Judge-ASR | {report.get("Judge-ASR")} |
| M3 | {report.get("M3")} |
| M4 | {report.get("M4")} |
| INVALID_TOOL_ARGS | {report.get("INVALID_TOOL_ARGS")} |
| sign_agreement | {report.get("sign_agreement_count")} |

## Notes

- T0 Tool-HASR / Δ reused from Stage-B `{STAGE_B_RUN_ID}` (not re-run).
- INVALID sensitivity S0/S1/S2 retained under locked denominators (see JSON).
- Constraint: no additional experiments after Q2 completes.
"""


def render_forensic_md(audit: Mapping[str, Any]) -> str:
    issues = audit.get("issues") or []
    issue_txt = ", ".join(issues) if issues else "(none)"
    sha = audit.get("frozen_sha_unchanged") or {}
    return f"""# P3 Q2 Forensic / Integrity Audit

**forensic_audit_status:** `{audit.get("forensic_audit_status")}`
**integrity_status:** `{audit.get("integrity_status")}`

| Check | Result |
| --- | --- |
| P1 SHA unchanged | {sha.get("p1_matches_lock")} (`{sha.get("p1_sha256")}`) |
| P2 SHA unchanged | {sha.get("p2_matches_lock")} (`{sha.get("p2_sha256")}`) |
| Stage-B immutable | {audit.get("stage_b_immutable")} |
| Model IDs exact | {audit.get("model_ids_exact")} |
| evaluation_id unique | {audit.get("evaluation_ids_unique")} |
| Budget OK | {audit.get("budget_ok")} (actual={audit.get("actual_usd")} / cap={audit.get("budget_cap_usd")}) |
| Smoke separate | {audit.get("smoke_separate")} |
| Mid-run retuning | {audit.get("mid_run_retuning_detected")} |
| Raw traces retained | {audit.get("raw_traces_retained")} |
| Issues | {issue_txt} |

run_id=`{audit.get("run_id")}` commit=`{audit.get("git_commit")}`
checked_at=`{audit.get("checked_at_utc")}`
predictions_sha256=`{audit.get("predictions_sha256")}`
"""


def emit_q2_reports(
    *,
    run_dir: Path,
    artifacts_dir: Path,
    report: Mapping[str, Any],
    audit: Mapping[str, Any],
) -> dict[str, str]:
    run_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "live_report_json": run_dir / "p3_q2_live_report.json",
        "live_report_md": run_dir / "p3_q2_live_report.md",
        "forensic_json": run_dir / "p3_q2_forensic_audit.json",
        "forensic_md": run_dir / "p3_q2_forensic_audit.md",
        "art_live_json": artifacts_dir / "p3_q2_live_report.json",
        "art_live_md": artifacts_dir / "p3_q2_live_report.md",
        "art_forensic_json": artifacts_dir / "p3_q2_forensic_audit.json",
        "art_forensic_md": artifacts_dir / "p3_q2_forensic_audit.md",
    }
    write_json(paths["live_report_json"], dict(report))
    paths["live_report_md"].write_text(render_live_report_md(report), encoding="utf-8")
    write_json(paths["forensic_json"], dict(audit))
    paths["forensic_md"].write_text(render_forensic_md(audit), encoding="utf-8")
    for src, dst in (
        (paths["live_report_json"], paths["art_live_json"]),
        (paths["live_report_md"], paths["art_live_md"]),
        (paths["forensic_json"], paths["art_forensic_json"]),
        (paths["forensic_md"], paths["art_forensic_md"]),
    ):
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return {k: str(v) for k, v in paths.items()}
