"""P3 Stage-C Q2 model/provider/pricing/budget lock (offline; no live eval).

Verification may cite OpenRouter public model-catalog metadata.
This module NEVER issues inference / chat-completion requests.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from adapti_guard.detectors.base import P2_SHA256
from adapti_guard.experiments.p2_agentic_live import (
    LOCKED_BACKEND,
    LOCKED_JUDGE,
    LOCKED_JUDGE_KEY,
    LOCKED_SEED,
    LOCKED_TARGET,
    LOCKED_TARGET_KEY,
    LOCKED_TEMPERATURE,
    MAX_JUDGE_RETRIES,
    MAX_TARGET_RETRIES,
    P1_SHA256,
    PACK_SHA256,
)
from adapti_guard.experiments.p3_agentic_live import (
    N_P2_ATTACK,
    N_P2_BENIGN_TWIN,
    N_P2_HARD_NEGATIVE,
    N_P2_TOTAL,
    OPERATIONAL_DETECTORS,
)

ROOT = Path(__file__).resolve().parents[3]
PACK_PATH = ROOT / "datasets" / "frozen" / "p2_agentic_v0.1.0" / "dataset.jsonl"

QUESTION_ID = "RQ-C2"
FACTOR = "target_model_id"
PRIMARY_POLICY = "PHASE1-CORE"
PLANNING_ID_PREFIX = "p3_q2_plan"

# OpenRouter public catalog snapshot captured during verification (no inference).
VERIFICATION_DATE_UTC = "2026-09-17"
PRICING_VERIFIED_AT_UTC = "2026-09-17T02:21:34Z"
CATALOG_SOURCE_URL = "https://openrouter.ai/api/v1/models"
PAGE_SOURCES = {
    "T1": "https://openrouter.ai/qwen/qwen3-30b-a3b/pricing",
    "T2": "https://openrouter.ai/google/gemma-3-27b-it/pricing",
    "T3": "https://openrouter.ai/qwen/qwen3.5-35b-a3b/pricing",
    "JUDGE": "https://openrouter.ai/qwen/qwen-2.5-72b-instruct/pricing",
    "T0": "https://openrouter.ai/qwen/qwen-2.5-7b-instruct/pricing",
}

# Locked OpenRouter IDs (exact; not invented).
T0_ID = LOCKED_TARGET  # qwen/qwen-2.5-7b-instruct
T1_ID = "qwen/qwen3-30b-a3b"
T2_ID = "google/gemma-3-27b-it"
T3_ID = "qwen/qwen3.5-35b-a3b"
JUDGE_ID = LOCKED_JUDGE

# Pricing from OpenRouter catalog API field `pricing` (USD per token → per 1M).
# Units: USD per 1M tokens.
PRICES_PER_1M_USD: dict[str, dict[str, float]] = {
    T0_ID: {"input": 0.10, "output": 0.20},
    T1_ID: {"input": 0.12, "output": 0.50},
    T2_ID: {"input": 0.08, "output": 0.45},
    T3_ID: {"input": 0.1625, "output": 1.30},
    JUDGE_ID: {"input": 0.36, "output": 0.40},
}

# Human-approved Q2 budget bound (numeric USD). Live eval still blocked until
# explicit separate approval; this constant only clears the offline budget gate.
MAXIMUM_PERMITTED_BUDGET_USD: float | None = 10.0
BUDGET_APPROVED_BY = "human"
BUDGET_APPROVED_VALUE_USD = 10.0
BUDGET_APPROVED_AT_UTC = "2026-09-17T11:31:00Z"

# Conservative token ceilings (offline, from pack content + locked max_tokens=512).
TARGET_INPUT_TOKENS_MAX_PER_CALL = 2048
TARGET_OUTPUT_TOKENS_MAX_PER_CALL = 512
JUDGE_INPUT_TOKENS_MAX_PER_CALL = 2048
JUDGE_OUTPUT_TOKENS_MAX_PER_CALL = 512


def count_pack_turns(pack_path: Path | None = None) -> dict[str, Any]:
    path = pack_path or PACK_PATH
    n_traj = 0
    n_turns = 0
    by_len: dict[int, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        n_traj += 1
        nt = len(row.get("turns") or [])
        n_turns += nt
        by_len[nt] = by_len.get(nt, 0) + 1
    if n_traj != N_P2_TOTAL:
        raise RuntimeError(f"pack traj count {n_traj} != {N_P2_TOTAL}")
    return {
        "n_trajectories": n_traj,
        "n_turns_total": n_turns,
        "turns_per_trajectory_histogram": {str(k): v for k, v in sorted(by_len.items())},
        "formula_note": "sum(len(turns)) over frozen p2_agentic_v0.1.0 dataset.jsonl",
    }


def q2_arm_schedule() -> dict[str, Any]:
    """Exact reduced Q2 schedule (deterministic)."""
    n_traj = N_P2_TOTAL
    n_det = len(OPERATIONAL_DETECTORS)
    n_pol = 1  # PHASE1-CORE only
    n_secondary = 3
    n_arms = n_traj * n_det * n_pol * n_secondary
    turns = count_pack_turns()
    n_turn_slots = turns["n_turns_total"] * n_det * n_pol * n_secondary
    return {
        "design_id": "B_REDUCED_Q2",
        "trajectories": n_traj,
        "detectors": list(OPERATIONAL_DETECTORS),
        "n_detectors": n_det,
        "policies": [PRIMARY_POLICY],
        "n_policies": n_pol,
        "secondary_targets": ["T1", "T2", "T3"],
        "n_secondary_targets": n_secondary,
        "t0_rerun": False,
        "formula": f"{n_traj} × {n_det} × {PRIMARY_POLICY} × {{T1,T2,T3}} = {n_arms}",
        "n_new_arms": n_arms,
        "pack_turns": turns,
        "n_target_turn_slots_if_unblocked": n_turn_slots,
        "composition": {
            "attack": N_P2_ATTACK,
            "benign_twin": N_P2_BENIGN_TWIN,
            "hard_negative": N_P2_HARD_NEGATIVE,
        },
        "verified_against_implementation": True,
        "not_stage_b_empirical_copy": True,
    }


def q2_call_bounds() -> dict[str, Any]:
    """Deterministic call bounds from schedule + locked retry policy.

    Harness calls the target once per unblocked turn and the judge once per arm.
    Worst-case assumes every turn is unblocked (no defense short-circuit), which
    maximizes target calls. Retries: attempts = 1 + MAX_*_RETRIES per call site.
    """
    sched = q2_arm_schedule()
    target_attempts = 1 + MAX_TARGET_RETRIES
    judge_attempts = 1 + MAX_JUDGE_RETRIES
    scheduled_target = int(sched["n_target_turn_slots_if_unblocked"])
    scheduled_judge = int(sched["n_new_arms"])
    return {
        "scheduled_arms": sched["n_new_arms"],
        "scheduled_target_calls_if_unblocked": scheduled_target,
        "scheduled_judge_calls": scheduled_judge,
        "max_target_retries_per_call_site": MAX_TARGET_RETRIES,
        "max_judge_retries_per_call_site": MAX_JUDGE_RETRIES,
        "target_attempts_per_call_site": target_attempts,
        "judge_attempts_per_call_site": judge_attempts,
        "target_calls_max": scheduled_target * target_attempts,
        "judge_calls_max": scheduled_judge * judge_attempts,
        "total_calls_max": scheduled_target * target_attempts
        + scheduled_judge * judge_attempts,
        "retries_allowed": True,
        "defense_blocks_reduce_target_calls": True,
        "worst_case_assumes_zero_blocks": True,
        "derivation": (
            f"pack_turns={sched['pack_turns']['n_turns_total']} × "
            f"detectors={sched['n_detectors']} × policies={sched['n_policies']} × "
            f"targets={sched['n_secondary_targets']} = {scheduled_target} turn slots; "
            f"×{target_attempts} attempts; "
            f"judge={scheduled_judge} arms ×{judge_attempts} attempts"
        ),
        "explicitly_not_stage_b_empirical_1663": True,
    }


def _price_block(model_id: str) -> dict[str, Any]:
    p = PRICES_PER_1M_USD[model_id]
    return {
        "provider": LOCKED_BACKEND,
        "model_id": model_id,
        "input_price": p["input"],
        "output_price": p["output"],
        "pricing_unit": "USD_per_1M_tokens",
        "pricing_source": CATALOG_SOURCE_URL,
        "pricing_page": PAGE_SOURCES.get(
            next(
                (
                    k
                    for k, mid in {
                        "T0": T0_ID,
                        "T1": T1_ID,
                        "T2": T2_ID,
                        "T3": T3_ID,
                        "JUDGE": JUDGE_ID,
                    }.items()
                    if mid == model_id
                ),
                "T0",
            )
        ),
        "pricing_verified_at": PRICING_VERIFIED_AT_UTC,
        "pricing_notes": (
            "OpenRouter public /api/v1/models catalog `pricing.prompt` / "
            "`pricing.completion` fields converted ×1e6 to USD/1M. "
            "No inference request issued. Catalog prices may differ from "
            "individual upstream host list rates on OpenRouter UI tables."
        ),
        "verified": True,
    }


def build_target_lock_records() -> dict[str, Any]:
    """Explicit provider/model lock records for T0–T3 + judge."""
    common_compat_note = (
        "P3 live path uses OpenRouter OpenAI-compatible chat completions with "
        "text TOOL_REQUEST parsing (not requiring native tool-call API success). "
        "Catalog lists tools/structured_outputs support. Runtime compatibility "
        "for secondary targets is not yet demonstrated by live Q2 evidence."
    )
    records = {
        "T0": {
            "target_model_id": "T0",
            "provider": LOCKED_BACKEND,
            "provider_model_id": T0_ID,
            "display_name": "Qwen2.5 7B Instruct",
            "model_family": "qwen2.5-dense",
            "config_key": LOCKED_TARGET_KEY,
            "verification_source": [
                "Stage-B manifest",
                "configs/models.yaml#target_2",
                CATALOG_SOURCE_URL,
                PAGE_SOURCES["T0"],
            ],
            "verification_date": VERIFICATION_DATE_UTC,
            "availability_status": "AVAILABLE_ON_OPENROUTER_CATALOG",
            "tool_call_support": True,
            "structured_output_support": True,
            "context_window": 32768,
            "input_price": PRICES_PER_1M_USD[T0_ID]["input"],
            "output_price": PRICES_PER_1M_USD[T0_ID]["output"],
            "pricing_unit": "USD_per_1M_tokens",
            "compatibility_status": "COMPATIBLE_BY_CONFIGURATION",
            "compatibility_evidence": "Stage-B live execution on P2 pack",
            "selection_rationale": (
                "Immutable Stage-B reference target for Δ(d,T0); not re-selected."
            ),
            "lock_status": "LOCKED_FROM_STAGE_B",
            "selected_from_observed_q2_results": False,
            "called_best": False,
            "rerun_in_q2": False,
        },
        "T1": {
            "target_model_id": "T1",
            "provider": LOCKED_BACKEND,
            "provider_model_id": T1_ID,
            "display_name": "Qwen3 30B A3B",
            "model_family": "qwen3-moe",
            "config_key": "q2_t1",
            "parameter_notes": "30.5B params / 3.3B activated (MoE A3B); catalog+page",
            "verification_source": [CATALOG_SOURCE_URL, PAGE_SOURCES["T1"]],
            "verification_date": VERIFICATION_DATE_UTC,
            "availability_status": "AVAILABLE_ON_OPENROUTER_CATALOG",
            "tool_call_support": True,
            "structured_output_support": True,
            "context_window": 131072,
            "input_price": PRICES_PER_1M_USD[T1_ID]["input"],
            "output_price": PRICES_PER_1M_USD[T1_ID]["output"],
            "pricing_unit": "USD_per_1M_tokens",
            "compatibility_status": "COMPATIBLE_BY_CONFIGURATION",
            "compatibility_notes": common_compat_note,
            "selection_rationale": (
                "Within-family architectural evolution (dense T0 → MoE) for "
                "target-model sensitivity; tool-capable on OpenRouter; "
                "pre-result criteria only."
            ),
            "lock_status": "LOCKED",
            "verification_status": "VERIFIED",
            "selected_from_observed_q2_results": False,
            "called_best": False,
        },
        "T2": {
            "target_model_id": "T2",
            "provider": LOCKED_BACKEND,
            "provider_model_id": T2_ID,
            "display_name": "Google Gemma 3 27B (IT)",
            "model_family": "gemma3",
            "config_key": "q2_t2",
            "parameter_notes": "Gemma 3 27B instruct; OpenRouter id google/gemma-3-27b-it",
            "verification_source": [CATALOG_SOURCE_URL, PAGE_SOURCES["T2"]],
            "verification_date": VERIFICATION_DATE_UTC,
            "availability_status": "AVAILABLE_ON_OPENROUTER_CATALOG",
            "tool_call_support": True,
            "structured_output_support": True,
            "context_window": 131072,
            "input_price": PRICES_PER_1M_USD[T2_ID]["input"],
            "output_price": PRICES_PER_1M_USD[T2_ID]["output"],
            "pricing_unit": "USD_per_1M_tokens",
            "compatibility_status": "COMPATIBLE_BY_CONFIGURATION",
            "compatibility_notes": common_compat_note
            + " Catalog modality text+image→text; P3 prompts are text-only.",
            "selection_rationale": (
                "Cross-family diversity (Google Gemma vs Qwen) under identical "
                "detectors/policies/benchmark; pre-result criteria only."
            ),
            "lock_status": "LOCKED",
            "verification_status": "VERIFIED",
            "selected_from_observed_q2_results": False,
            "called_best": False,
            "pricing_note_ui_vs_catalog": (
                "OpenRouter UI may show upstream host rates (e.g. DeepInfra "
                "$0.08/$0.16). Locked price uses catalog API completion=$0.45/1M."
            ),
        },
        "T3": {
            "target_model_id": "T3",
            "provider": LOCKED_BACKEND,
            "provider_model_id": T3_ID,
            "display_name": "Qwen3.5 35B A3B",
            "model_family": "qwen3.5-moe",
            "config_key": "q2_t3",
            "parameter_notes": "Qwen3.5-35B-A3B MoE; OpenRouter id qwen/qwen3.5-35b-a3b",
            "verification_source": [CATALOG_SOURCE_URL, PAGE_SOURCES["T3"]],
            "verification_date": VERIFICATION_DATE_UTC,
            "availability_status": "AVAILABLE_ON_OPENROUTER_CATALOG",
            "tool_call_support": True,
            "structured_output_support": True,
            "context_window": 262144,
            "input_price": PRICES_PER_1M_USD[T3_ID]["input"],
            "output_price": PRICES_PER_1M_USD[T3_ID]["output"],
            "pricing_unit": "USD_per_1M_tokens",
            "compatibility_status": "COMPATIBLE_BY_CONFIGURATION",
            "compatibility_notes": common_compat_note,
            "selection_rationale": (
                "Adjacent next-generation Qwen MoE band for sensitivity coverage; "
                "not a causal size claim; pre-result criteria only."
            ),
            "lock_status": "LOCKED",
            "verification_status": "VERIFIED",
            "selected_from_observed_q2_results": False,
            "called_best": False,
        },
        "JUDGE": {
            "target_model_id": "JUDGE",
            "provider": LOCKED_BACKEND,
            "provider_model_id": JUDGE_ID,
            "display_name": "Qwen2.5 72B Instruct",
            "model_family": "qwen2.5-dense",
            "config_key": LOCKED_JUDGE_KEY,
            "verification_source": [
                "Stage-B/Q1 canonical judge lock",
                CATALOG_SOURCE_URL,
                PAGE_SOURCES["JUDGE"],
            ],
            "verification_date": VERIFICATION_DATE_UTC,
            "availability_status": "AVAILABLE_ON_OPENROUTER_CATALOG",
            "tool_call_support": True,
            "structured_output_support": True,
            "context_window": 32768,
            "input_price": PRICES_PER_1M_USD[JUDGE_ID]["input"],
            "output_price": PRICES_PER_1M_USD[JUDGE_ID]["output"],
            "pricing_unit": "USD_per_1M_tokens",
            "compatibility_status": "COMPATIBLE_BY_CONFIGURATION",
            "compatibility_evidence": "Stage-B live judge path",
            "selection_rationale": (
                "Canonical locked judge retained; judge is not the Q2 factor."
            ),
            "lock_status": "LOCKED_CANONICAL",
            "verification_status": "VERIFIED",
        },
    }
    return records


def pricing_lock() -> dict[str, Any]:
    return {
        "provider": LOCKED_BACKEND,
        "pricing_verified_at": PRICING_VERIFIED_AT_UTC,
        "pricing_source": CATALOG_SOURCE_URL,
        "pricing_unit": "USD_per_1M_tokens",
        "models": {
            "T0": _price_block(T0_ID),
            "T1": _price_block(T1_ID),
            "T2": _price_block(T2_ID),
            "T3": _price_block(T3_ID),
            "JUDGE": _price_block(JUDGE_ID),
        },
        "all_secondary_pricing_verified": True,
        "inference_requests": 0,
    }


def worst_case_cost_usd(
    *,
    maximum_permitted_budget_usd: float | None = None,
) -> dict[str, Any]:
    """Reproducible worst-case cost from locked prices + deterministic call bounds."""
    bounds = q2_call_bounds()
    sched = q2_arm_schedule()
    # Equal turn slots per secondary target
    slots_per_target = (
        sched["pack_turns"]["n_turns_total"]
        * sched["n_detectors"]
        * sched["n_policies"]
    )
    attempts_t = bounds["target_attempts_per_call_site"]
    bounds["judge_attempts_per_call_site"]
    calls_per_target_max = slots_per_target * attempts_t
    judge_calls_max = bounds["judge_calls_max"]

    tin = TARGET_INPUT_TOKENS_MAX_PER_CALL
    tout = TARGET_OUTPUT_TOKENS_MAX_PER_CALL
    jin = JUDGE_INPUT_TOKENS_MAX_PER_CALL
    jout = JUDGE_OUTPUT_TOKENS_MAX_PER_CALL

    def _call_cost(n: int, pin: float, pout: float, i: int, o: int) -> float:
        return n * ((i * pin) + (o * pout)) / 1_000_000.0

    per_target = {}
    target_cost = 0.0
    for slot, mid in (("T1", T1_ID), ("T2", T2_ID), ("T3", T3_ID)):
        pin = PRICES_PER_1M_USD[mid]["input"]
        pout = PRICES_PER_1M_USD[mid]["output"]
        c = _call_cost(calls_per_target_max, pin, pout, tin, tout)
        per_target[slot] = {
            "model_id": mid,
            "target_calls_max": calls_per_target_max,
            "input_per_1m_usd": pin,
            "output_per_1m_usd": pout,
            "input_tokens_max_per_call": tin,
            "output_tokens_max_per_call": tout,
            "cost_usd": round(c, 6),
        }
        target_cost += c

    jpin = PRICES_PER_1M_USD[JUDGE_ID]["input"]
    jpout = PRICES_PER_1M_USD[JUDGE_ID]["output"]
    judge_cost = _call_cost(judge_calls_max, jpin, jpout, jin, jout)
    # Retry cost is already included in *_calls_max (attempts multiplier).
    worst = target_cost + judge_cost

    budget = (
        maximum_permitted_budget_usd
        if maximum_permitted_budget_usd is not None
        else MAXIMUM_PERMITTED_BUDGET_USD
    )
    if budget is None:
        budget_check = "BLOCKED"
        budget_status = "BUDGET_BOUND_UNSET"
    else:
        budget_check = "PASS" if worst <= float(budget) else "FAIL"
        budget_status = "BUDGET_PASS" if budget_check == "PASS" else "BUDGET_FAIL"

    return {
        "target_calls_max": bounds["target_calls_max"],
        "judge_calls_max": judge_calls_max,
        "total_calls_max": bounds["total_calls_max"],
        "target_input_tokens_max_per_call": tin,
        "target_output_tokens_max_per_call": tout,
        "judge_input_tokens_max_per_call": jin,
        "judge_output_tokens_max_per_call": jout,
        "target_input_tokens_max": bounds["target_calls_max"] * tin,
        "target_output_tokens_max": bounds["target_calls_max"] * tout,
        "judge_input_tokens_max": judge_calls_max * jin,
        "judge_output_tokens_max": judge_calls_max * jout,
        "per_target_cost_usd": per_target,
        "target_cost_usd": round(target_cost, 6),
        "judge_cost_usd": round(judge_cost, 6),
        "retry_cost_usd": "INCLUDED_IN_CALLS_MAX",
        "worst_case_cost_usd": round(worst, 6),
        "maximum_permitted_budget_usd": budget,
        "budget_check": budget_check,
        "budget_status": budget_status,
        "token_ceiling_basis": (
            "output=locked max_tokens 512; input=conservative 2048 from offline "
            "pack content char analysis (max traj content ≪ ceiling) + formatting "
            "overhead; NOT Stage-B empirical averages"
        ),
        "assumptions": [
            "every turn unblocked (maximizes target calls)",
            f"target attempts per turn site = 1+{MAX_TARGET_RETRIES}",
            f"judge attempts per arm = 1+{MAX_JUDGE_RETRIES}",
            "OpenRouter catalog prices locked at verification timestamp",
            "T0 not re-billed (Stage-B reuse)",
        ],
    }


def gate_status_from_locks(
    *,
    maximum_permitted_budget_usd: float | None = None,
) -> dict[str, Any]:
    records = build_target_lock_records()
    unverified = [
        s
        for s in ("T1", "T2", "T3")
        if records[s].get("verification_status") != "VERIFIED"
        or records[s].get("lock_status") not in {"LOCKED", "LOCKED_FROM_STAGE_B"}
    ]
    pricing = pricing_lock()
    cost = worst_case_cost_usd(
        maximum_permitted_budget_usd=maximum_permitted_budget_usd
    )
    blockers: list[str] = []
    if unverified:
        status = "P3_Q2_MODEL_LOCK_BLOCKED"
        blockers.extend(f"TARGET_{s}_UNVERIFIED" for s in unverified)
    elif not pricing["all_secondary_pricing_verified"]:
        status = "P3_Q2_PRICING_BLOCKED"
        blockers.append("PRICING_UNKNOWN")
    elif cost["maximum_permitted_budget_usd"] is None:
        status = "P3_Q2_BUDGET_BOUND_BLOCKED"
        blockers.append("BUDGET_BOUND_UNSET")
    elif cost["budget_status"] == "BUDGET_FAIL":
        status = "P3_Q2_BUDGET_FAIL"
        blockers.append("WORST_CASE_EXCEEDS_BUDGET")
    else:
        # Offline protocol + model/pricing/budget gates clear.
        # Live execution remains separately blocked (live_execution_allowed=False).
        status = "P3_Q2_GATE_READY"
    return {
        "status": status,
        "blockers": blockers,
        "model_lock_complete": not unverified,
        "pricing_complete": pricing["all_secondary_pricing_verified"],
        "budget_check": cost["budget_check"],
        "worst_case_cost_usd": cost["worst_case_cost_usd"],
        "maximum_permitted_budget_usd": cost["maximum_permitted_budget_usd"],
        "live_execution_allowed": False,
        "api_calls": 0,
        "llm_calls": 0,
        "network_live_eval_calls": 0,
    }


def planning_provenance(*, code_commit: str | None = None) -> dict[str, Any]:
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    blob = json.dumps(
        {
            "question_id": QUESTION_ID,
            "factor": FACTOR,
            "targets": {s: build_target_lock_records()[s]["provider_model_id"] for s in ("T0", "T1", "T2", "T3")},
            "judge": JUDGE_ID,
            "pricing_verified_at": PRICING_VERIFIED_AT_UTC,
            "schedule": q2_arm_schedule()["formula"],
        },
        sort_keys=True,
    ).encode()
    digest = hashlib.sha256(blob).hexdigest()[:12]
    planning_id = f"{PLANNING_ID_PREFIX}_{VERIFICATION_DATE_UTC.replace('-', '')}_{digest}"
    return {
        "planning_id": planning_id,
        "question_id": QUESTION_ID,
        "factor": FACTOR,
        "reference_target": T0_ID,
        "secondary_targets": [T1_ID, T2_ID, T3_ID],
        "judge_model_id": JUDGE_ID,
        "detectors": list(OPERATIONAL_DETECTORS),
        "policy": PRIMARY_POLICY,
        "temperature": LOCKED_TEMPERATURE,
        "cache": False,
        "seed": LOCKED_SEED,
        "benchmark_sha": PACK_SHA256,
        "p1_sha": P1_SHA256,
        "p2_sha": P2_SHA256,
        "code_commit": code_commit,
        "provider": LOCKED_BACKEND,
        "pricing_verified_at": PRICING_VERIFIED_AT_UTC,
        "verification_sources": [CATALOG_SOURCE_URL, *PAGE_SOURCES.values()],
        "generated_at_utc": now,
        "not_an_evaluation_result": True,
    }


def build_verification_bundle(
    *,
    maximum_permitted_budget_usd: float | None = None,
    code_commit: str | None = None,
) -> dict[str, Any]:
    gate = gate_status_from_locks(
        maximum_permitted_budget_usd=maximum_permitted_budget_usd
    )
    return {
        "model_verification": {
            "provider": LOCKED_BACKEND,
            "records": build_target_lock_records(),
            "model_lock_complete": gate["model_lock_complete"],
            "verification_date_utc": VERIFICATION_DATE_UTC,
            "catalog_source": CATALOG_SOURCE_URL,
            "inference_requests": 0,
        },
        "pricing_lock": pricing_lock(),
        "arm_schedule": q2_arm_schedule(),
        "call_bounds": q2_call_bounds(),
        "budget_preflight": worst_case_cost_usd(
            maximum_permitted_budget_usd=maximum_permitted_budget_usd
        ),
        "provenance": planning_provenance(code_commit=code_commit),
        "gate": gate,
    }
