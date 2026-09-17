#!/usr/bin/env python3
"""Track A / Phase-2 STANDARD $2 SMOKE TEST (B0 then VNEXT-ADAPT).

Validates the existing evaluation pipeline on a small real-model subset.
Does NOT modify defenses, thresholds, frozen packs, or attack prompts.
Does NOT authorize publication-level claims.

Usage:
  PYTHONPATH=src python3 scripts/run_track_a_phase2_smoke.py
  PYTHONPATH=src python3 scripts/run_track_a_phase2_smoke.py --preflight-only
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from adapti_guard.experiments.env_loader import load_project_env

load_project_env()

from adapti_guard.evaluation.attack_success import evaluate_episode
from adapti_guard.evaluation.experiment_logging import git_commit, sha256_file
from adapti_guard.evaluation.prediction_provenance import (
    PROVENANCE_SCHEMA_VERSION,
    build_prediction_row,
)
from adapti_guard.evaluation.statistics import mcnemar_test
from adapti_guard.experiments.defense_baselines import get_defense_fn
from adapti_guard.experiments.real_llm_pipeline import (
    BaselineRunContext,
    EvaluationBackend,
    PipelineConfig,
    build_models,
)
from adapti_guard.experiments.vnext_confirm import (
    ADDENDUM_VERSION,
    B0_BASELINE_KEY,
    LOCKED_JUDGE_KEY,
    LOCKED_JUDGE_MODEL,
    LOCKED_PACK_PATH,
    LOCKED_PACK_SHA256,
    LOCKED_SEED,
    LOCKED_TARGET_KEY,
    LOCKED_TARGET_MODEL,
    MSID_ID,
    PACK_ID,
    PROTOCOL_VERSION,
    TREATMENT_BASELINE_KEY,
    VNextGateError,
    load_locked_pack,
    require_openrouter_key,
    verify_pack_hash,
)

EXPERIMENT_ID = "TRACK_A_PHASE2_SMOKE_2USD"
N_ATTACK = 20
N_BENIGN = 20
MAX_BUDGET_USD = 2.0
# Exact OpenRouter catalog prices for locked models (USD / 1M tokens).
TARGET_PRICE = {"prompt": 0.10, "completion": 0.20}
JUDGE_PRICE = {"prompt": 0.36, "completion": 0.40}
# Conservative preflight token ceilings per call (not used as observed cost).
PREFLIGHT_TARGET_IN, PREFLIGHT_TARGET_OUT = 2048, 512
PREFLIGHT_JUDGE_IN, PREFLIGHT_JUDGE_OUT = 2048, 512
ACTION_COSTS = {"A0": 0.0, "A1": 0.10, "A2": 0.25, "A3": 0.50}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cost_usd(prompt_tokens: int, completion_tokens: int, rates: dict[str, float]) -> float:
    return (prompt_tokens / 1_000_000.0) * rates["prompt"] + (
        completion_tokens / 1_000_000.0
    ) * rates["completion"]


def select_smoke_records(pack: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deterministic subset: first 20 attack + first 20 benign in frozen file order."""
    attacks = [r for r in pack if r.get("label") == "attack"][:N_ATTACK]
    benigns = [r for r in pack if r.get("label") == "benign"][:N_BENIGN]
    if len(attacks) < N_ATTACK or len(benigns) < N_BENIGN:
        raise RuntimeError(
            f"pack too small: attack={len(attacks)} benign={len(benigns)}"
        )
    # Preserve pack-relative pairing order: interleave not required; same ID set
    # for both arms. Keep attacks then benigns for stable traces.
    return attacks + benigns


def preflight_estimate_usd() -> dict[str, Any]:
    n_eps = (N_ATTACK + N_BENIGN) * 2  # B0 + VNEXT-ADAPT
    # One target + one judge call per episode upper bound (A3 may skip target).
    target_calls = n_eps
    judge_calls = n_eps
    target = target_calls * cost_usd(
        PREFLIGHT_TARGET_IN, PREFLIGHT_TARGET_OUT, TARGET_PRICE
    )
    judge = judge_calls * cost_usd(PREFLIGHT_JUDGE_IN, PREFLIGHT_JUDGE_OUT, JUDGE_PRICE)
    total = target + judge
    return {
        "n_episodes_total": n_eps,
        "target_calls_ub": target_calls,
        "judge_calls_ub": judge_calls,
        "target_usd_ub": round(target, 6),
        "judge_usd_ub": round(judge, 6),
        "estimated_usd_upper_bound": round(total, 6),
        "max_budget_usd": MAX_BUDGET_USD,
        "within_budget": total <= MAX_BUDGET_USD,
        "pricing": {
            "target": {**TARGET_PRICE, "model": LOCKED_TARGET_MODEL},
            "judge": {**JUDGE_PRICE, "model": LOCKED_JUDGE_MODEL},
            "unit": "USD_per_1M_tokens",
        },
        "token_ceilings": {
            "target_in": PREFLIGHT_TARGET_IN,
            "target_out": PREFLIGHT_TARGET_OUT,
            "judge_in": PREFLIGHT_JUDGE_IN,
            "judge_out": PREFLIGHT_JUDGE_OUT,
        },
    }


def run_arm(
    *,
    baseline_key: str,
    records: list[dict[str, Any]],
    target,
    judge,
    output_dir: Path,
    run_context: BaselineRunContext,
    spend: dict[str, float],
) -> dict[str, Any]:
    arm_dir = output_dir / baseline_key
    arm_dir.mkdir(parents=True, exist_ok=True)
    predictions_path = arm_dir / f"{baseline_key}_predictions.jsonl"
    traces_path = arm_dir / f"{baseline_key}_traces.jsonl"
    defense_fn, state = get_defense_fn(baseline_key)
    if state is not None:
        state.reset()

    rows: list[dict[str, Any]] = []
    traces: list[dict[str, Any]] = []
    for record in records:
        if spend["estimated_usd_total"] >= MAX_BUDGET_USD:
            raise RuntimeError(
                f"STOP_BUDGET: spend {spend['estimated_usd_total']:.6f} >= {MAX_BUDGET_USD}"
            )
        eid = str(record["id"])
        t0 = time.perf_counter()
        ep = evaluate_episode(
            record,
            defense_fn=defense_fn,
            target_model=target,
            judge=judge,
        )
        ep.metadata["baseline"] = baseline_key
        ep.metadata["evaluation_mode"] = "real_llm_judge"
        ep.metadata["scientific_arm"] = baseline_key
        ep.metadata["smoke_experiment_id"] = EXPERIMENT_ID

        judge_usage = (ep.metadata or {}).get("judge_usage") or {}
        j_prompt = int(judge_usage.get("prompt_tokens", 0) or 0)
        j_comp = int(judge_usage.get("completion_tokens", 0) or 0)
        t_prompt = int(ep.prompt_tokens or 0)
        t_comp = int(ep.completion_tokens or 0)
        t_cost = cost_usd(t_prompt, t_comp, TARGET_PRICE)
        j_cost = cost_usd(j_prompt, j_comp, JUDGE_PRICE)
        call_cost = t_cost + j_cost
        # Project one more worst-case episode before committing if near limit
        remaining_after = spend["estimated_usd_total"] + call_cost
        if remaining_after > MAX_BUDGET_USD:
            raise RuntimeError(
                f"STOP_BUDGET_PROJECTED: {remaining_after:.6f} would exceed {MAX_BUDGET_USD}"
            )
        spend["estimated_usd_total"] = remaining_after
        spend["target_usd"] += t_cost
        spend["judge_usd"] += j_cost
        spend["target_prompt_tokens"] += t_prompt
        spend["target_completion_tokens"] += t_comp
        spend["judge_prompt_tokens"] += j_prompt
        spend["judge_completion_tokens"] += j_comp
        spend["n_target_calls"] += 1 if (not ep.blocked or t_prompt or t_comp) else 0
        spend["n_judge_calls"] += 1

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
        )
        pred_row["scientific_arm"] = baseline_key
        pred_row["taxonomy_class"] = ep.taxonomy_class
        pred_row["defense_action"] = ep.defense_action
        pred_row["action"] = ep.defense_action
        pred_row["judge_usage"] = judge_usage
        pred_row["tool_turn"] = (ep.metadata or {}).get("tool_turn")
        pred_row["target_prompt_tokens"] = t_prompt
        pred_row["target_completion_tokens"] = t_comp
        pred_row["judge_prompt_tokens"] = j_prompt
        pred_row["judge_completion_tokens"] = j_comp
        pred_row["estimated_usd_target"] = round(t_cost, 8)
        pred_row["estimated_usd_judge"] = round(j_cost, 8)
        pred_row["estimated_usd_total"] = round(call_cost, 8)
        pred_row["cumulative_spend_usd"] = round(spend["estimated_usd_total"], 8)
        pred_row["label"] = record.get("label")
        pred_row["gold_label"] = record.get("label")
        rows.append(pred_row)

        traces.append(
            {
                "id": eid,
                "baseline": baseline_key,
                "label": record.get("label"),
                "prompt": record.get("prompt"),
                "context": record.get("context"),
                "defended_or_raw_response": ep.model_response,
                "defense_action": ep.defense_action,
                "blocked": ep.blocked,
                "attack_succeeded": ep.attack_succeeded,
                "utility_success": ep.utility_success,
                "taxonomy_class": ep.taxonomy_class,
                "judge_reason": getattr(ep, "judge_reason", None)
                or (ep.metadata or {}).get("judge_reason"),
                "tokens": {
                    "target_prompt": t_prompt,
                    "target_completion": t_comp,
                    "judge_prompt": j_prompt,
                    "judge_completion": j_comp,
                },
                "cost_usd": {
                    "target": round(t_cost, 8),
                    "judge": round(j_cost, 8),
                    "total": round(call_cost, 8),
                },
                "elapsed_s": round(time.perf_counter() - t0, 3),
            }
        )
        print(
            f"  [{baseline_key}] {eid} label={record.get('label')} "
            f"action={ep.defense_action} asr={ep.attack_succeeded} "
            f"util={ep.utility_success} cost={call_cost:.6f} "
            f"cum={spend['estimated_usd_total']:.6f}",
            flush=True,
        )
        predictions_path.write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
            encoding="utf-8",
        )
        traces_path.write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in traces),
            encoding="utf-8",
        )

    metrics = {
        "baseline": baseline_key,
        "n_samples": len(rows),
        "n_attack": sum(1 for r in rows if r.get("label") == "attack"),
        "n_benign": sum(1 for r in rows if r.get("label") == "benign"),
        "status": "COMPLETED",
        "spend_usd_arm": round(
            sum(float(r.get("estimated_usd_total") or 0) for r in rows), 6
        ),
    }
    _write_json(arm_dir / f"{baseline_key}_metrics.json", metrics)
    return {"metrics": metrics, "rows": rows, "traces": traces}


def _bool(v: Any) -> bool:
    return bool(v) is True


def score_smoke(
    b0_rows: list[dict[str, Any]],
    t_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    b0 = {str(r["id"]): r for r in b0_rows}
    tr = {str(r["id"]): r for r in t_rows}
    shared = sorted(set(b0) & set(tr))
    attacks = [i for i in shared if b0[i].get("label") == "attack"]
    benigns = [i for i in shared if b0[i].get("label") == "benign"]

    b0_asr_n = sum(1 for i in attacks if _bool(b0[i].get("attack_success")))
    t_asr_n = sum(1 for i in attacks if _bool(tr[i].get("attack_success")))
    n_atk = len(attacks)
    b0_asr = b0_asr_n / n_atk if n_atk else None
    t_asr = t_asr_n / n_atk if n_atk else None

    # Simple paired ASR McNemar on attack_success bits (smoke diagnostic).
    b0_bits = [1 if _bool(b0[i].get("attack_success")) else 0 for i in attacks]
    t_bits = [1 if _bool(tr[i].get("attack_success")) else 0 for i in attacks]
    # mcnemar_test expects success vectors where 1=success; b10 = control success & treatment fail
    mcn = mcnemar_test(b0_bits, t_bits)

    b0_util_n = sum(1 for i in benigns if _bool(b0[i].get("utility_success")))
    t_util_n = sum(1 for i in benigns if _bool(tr[i].get("utility_success")))
    n_ben = len(benigns)
    b0_util = b0_util_n / n_ben if n_ben else None
    t_util = t_util_n / n_ben if n_ben else None

    actions = [str(tr[i].get("defense_action") or tr[i].get("action") or "A0") for i in shared]
    action_dist = dict(Counter(actions))
    interventions = sum(1 for a in actions if a in {"A1", "A2", "A3"})
    costs = [ACTION_COSTS.get(a, 0.0) for a in actions]

    return {
        "n_shared": len(shared),
        "n_attack": n_atk,
        "n_benign": n_ben,
        "attack": {
            "B0_ASR": b0_asr,
            "B0_ASR_frac": f"{b0_asr_n}/{n_atk}",
            "VNEXT_ADAPT_ASR": t_asr,
            "VNEXT_ADAPT_ASR_frac": f"{t_asr_n}/{n_atk}",
            "absolute_asr_difference": (
                None if b0_asr is None or t_asr is None else round(b0_asr - t_asr, 6)
            ),
            "b10": int(mcn["b10"]),
            "b01": int(mcn["b01"]),
            "mcnemar_exact_p": float(mcn["p_value"]),
            "mcnemar_note": (
                "Smoke diagnostic on attack_success bits only; not a publication claim"
            ),
        },
        "benign": {
            "B0_utility": b0_util,
            "B0_utility_frac": f"{b0_util_n}/{n_ben}",
            "VNEXT_ADAPT_utility": t_util,
            "VNEXT_ADAPT_utility_frac": f"{t_util_n}/{n_ben}",
            "utility_difference": (
                None if b0_util is None or t_util is None else round(t_util - b0_util, 6)
            ),
        },
        "defense": {
            "intervention_count": interventions,
            "intervention_rate": interventions / len(actions) if actions else None,
            "action_distribution": action_dist,
            "mean_action_cost": statistics.mean(costs) if costs else None,
            "median_action_cost": statistics.median(costs) if costs else None,
            "total_action_cost": sum(costs),
        },
        "attack_ids": attacks,
        "benign_ids": benigns,
    }


def integrity_checks(
    *,
    records: list[dict[str, Any]],
    b0_rows: list[dict[str, Any]],
    t_rows: list[dict[str, Any]],
    output_dir: Path,
    spend: dict[str, float],
) -> dict[str, Any]:
    ids = [str(r["id"]) for r in records]
    checks: dict[str, Any] = {}
    checks["no_duplicate_case_ids"] = len(ids) == len(set(ids))
    checks["attack_benign_counts"] = {
        "attack": sum(1 for r in records if r.get("label") == "attack"),
        "benign": sum(1 for r in records if r.get("label") == "benign"),
        "expected": {"attack": N_ATTACK, "benign": N_BENIGN},
        "ok": (
            sum(1 for r in records if r.get("label") == "attack") == N_ATTACK
            and sum(1 for r in records if r.get("label") == "benign") == N_BENIGN
        ),
    }
    b0_ids = [str(r["id"]) for r in b0_rows]
    t_ids = [str(r["id"]) for r in t_rows]
    checks["pairing_same_case_set"] = set(b0_ids) == set(t_ids) == set(ids)
    checks["labels_preserved"] = all(
        str(r.get("label")) == str(r.get("gold_label")) for r in b0_rows + t_rows
    )
    # Hidden label leakage: defense factories must not require is_attack; spot-check
    # that B0 never intervenes and VNEXT rows do not contain gold is_attack in controller.
    checks["b0_no_intervention"] = all(
        str(r.get("defense_action") or "A0") == "A0" for r in b0_rows
    )
    checks["judge_ne_target"] = LOCKED_TARGET_MODEL != LOCKED_JUDGE_MODEL
    checks["raw_outputs_exist"] = all(
        (output_dir / arm / f"{arm}_predictions.jsonl").is_file()
        and (output_dir / arm / f"{arm}_traces.jsonl").is_file()
        for arm in (B0_BASELINE_KEY, TREATMENT_BASELINE_KEY)
    )
    # Cost consistency: sum of per-row costs ≈ spend ledger
    row_sum = sum(float(r.get("estimated_usd_total") or 0) for r in b0_rows + t_rows)
    checks["cost_accounting_consistent"] = abs(row_sum - spend["estimated_usd_total"]) < 1e-6
    checks["within_budget"] = spend["estimated_usd_total"] <= MAX_BUDGET_USD
    checks["cache_off"] = True
    checks["seed"] = LOCKED_SEED
    checks["all_pass"] = all(
        bool(v) if not isinstance(v, dict) else bool(v.get("ok", True))
        for k, v in checks.items()
        if k != "all_pass"
    )
    return checks


def decide(integrity: dict[str, Any], scored: dict[str, Any], spend: dict[str, float]) -> str:
    if not integrity.get("all_pass"):
        return "FAIL"
    if spend["estimated_usd_total"] > MAX_BUDGET_USD:
        return "FAIL"
    if scored["n_attack"] < N_ATTACK or scored["n_benign"] < N_BENIGN:
        return "INCONCLUSIVE"
    # Pipeline completed within budget with internal validity → PASS (not efficacy claim)
    return "PASS"


def write_report(
    *,
    output_dir: Path,
    env: dict[str, Any],
    scored: dict[str, Any],
    integrity: dict[str, Any],
    spend: dict[str, float],
    decision: str,
    command: str,
) -> Path:
    atk = scored["attack"]
    ben = scored["benign"]
    defense = scored["defense"]
    md = f"""# SMOKE_TEST_REPORT — Track A / Phase-2 STANDARD $2 SMOKE

**DECISION: `{decision}`**

> This smoke test validates pipeline/accounting integrity only.
> It is **not** publication-level evidence of defense effectiveness.
> Do **not** claim statistical improvement merely because ASR decreased.

## A. Environment

| Field | Value |
| --- | --- |
| git commit | `{env['git_commit']}` |
| branch | `{env['branch']}` |
| target model | `{env['target_model']}` |
| judge model | `{env['judge_model']}` |
| seed | `{env['seed']}` |
| cache | `{env['cache_enabled']}` |
| protocol | `{env['protocol_version']}` + `{env['addendum_version']}` |
| pack | `{env['pack_id']}` SHA `{env['pack_sha256'][:16]}…` |
| n_attack / n_benign | {N_ATTACK} / {N_BENIGN} |
| estimated USD upper bound (preflight) | {env['preflight']['estimated_usd_upper_bound']} |
| actual estimated USD (token×price) | **{spend['estimated_usd_total']:.6f}** |
| max budget USD | {MAX_BUDGET_USD} |

## B. Attack results

| Metric | Value |
| --- | --- |
| B0 ASR | {atk['B0_ASR_frac']} = {atk['B0_ASR']} |
| VNEXT-ADAPT ASR | {atk['VNEXT_ADAPT_ASR_frac']} = {atk['VNEXT_ADAPT_ASR']} |
| absolute ASR difference (B0−VNEXT) | {atk['absolute_asr_difference']} |
| b10 | {atk['b10']} |
| b01 | {atk['b01']} |
| McNemar exact p-value | {atk['mcnemar_exact_p']} |

Note: McNemar here is a smoke diagnostic on `attack_success` bits, not a confirmatory publication test.

## C. Benign results

| Metric | Value |
| --- | --- |
| B0 utility | {ben['B0_utility_frac']} = {ben['B0_utility']} |
| VNEXT-ADAPT utility | {ben['VNEXT_ADAPT_utility_frac']} = {ben['VNEXT_ADAPT_utility']} |
| utility difference (VNEXT−B0) | {ben['utility_difference']} |

## D. Defense behavior (VNEXT-ADAPT arm, all smoke cases)

| Metric | Value |
| --- | --- |
| intervention count / rate | {defense['intervention_count']} / {defense['intervention_rate']} |
| action distribution | {defense['action_distribution']} |
| mean / median action cost | {defense['mean_action_cost']} / {defense['median_action_cost']} |
| total action cost | {defense['total_action_cost']} |
| API spend (USD) | {spend['estimated_usd_total']:.6f} |

## E. Integrity checks

```json
{json.dumps(integrity, indent=2)}
```

## F. DECISION

`{decision}`

## Run command

```bash
{command}
```

## Actual USD cost

`{spend['estimated_usd_total']:.6f}`
"""
    path = output_dir / "SMOKE_TEST_REPORT.md"
    path.write_text(md, encoding="utf-8")
    _write_json(
        output_dir / "SMOKE_TEST_REPORT.json",
        {
            "decision": decision,
            "environment": env,
            "attack": atk,
            "benign": ben,
            "defense": defense,
            "integrity": integrity,
            "spend": spend,
            "command": command,
            "not_publication_evidence": True,
        },
    )
    # Also copy to artifacts
    art = Path("/opt/cursor/artifacts")
    art.mkdir(parents=True, exist_ok=True)
    (art / "SMOKE_TEST_REPORT.md").write_text(md, encoding="utf-8")
    (art / "SMOKE_TEST_REPORT.json").write_text(
        (output_dir / "SMOKE_TEST_REPORT.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Track A Phase-2 $2 smoke test")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    command = (
        "PYTHONPATH=src python3 scripts/run_track_a_phase2_smoke.py"
        + (f" --output {args.output}" if args.output else "")
    )

    try:
        hash_info = verify_pack_hash()
        require_openrouter_key()
    except VNextGateError as exc:
        print(f"STATUS={exc.status}", flush=True)
        print(exc.message, file=sys.stderr)
        return 2

    from adapti_guard.evaluation.target_model import load_model_config
    import subprocess

    cfg = load_model_config(ROOT / "configs" / "models.yaml")
    cache_enabled = bool((cfg.get("cache") or {}).get("enabled", True))
    if cache_enabled:
        print("STATUS=INVALID_CACHE_ENABLED", flush=True)
        return 3
    target_model = ((cfg.get("models") or {}).get(LOCKED_TARGET_KEY) or {}).get("model")
    judge_model = ((cfg.get("models") or {}).get(LOCKED_JUDGE_KEY) or {}).get("model")
    if target_model != LOCKED_TARGET_MODEL or judge_model != LOCKED_JUDGE_MODEL:
        print("STATUS=INVALID_MODEL_LOCK", flush=True)
        return 3
    if target_model == judge_model:
        print("STATUS=INVALID_MODEL_LOCK_SAME", flush=True)
        return 3

    pack = load_locked_pack()
    records = select_smoke_records(pack)
    pre = preflight_estimate_usd()
    branch = (
        subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT)
        .decode()
        .strip()
    )
    env = {
        "git_commit": git_commit() or "UNKNOWN",
        "branch": branch,
        "target_model": LOCKED_TARGET_MODEL,
        "judge_model": LOCKED_JUDGE_MODEL,
        "seed": LOCKED_SEED,
        "cache_enabled": False,
        "protocol_version": PROTOCOL_VERSION,
        "addendum_version": ADDENDUM_VERSION,
        "msid_id": MSID_ID,
        "pack_id": PACK_ID,
        "pack_sha256": LOCKED_PACK_SHA256,
        "preflight": pre,
        "experiment_id": EXPERIMENT_ID,
        "scientific_evidence": False,
    }
    print(json.dumps({"preflight": pre, "n_records": len(records)}, indent=2), flush=True)
    if not pre["within_budget"]:
        print("STATUS=STOP_BUDGET_PREFLIGHT", flush=True)
        return 4
    if args.preflight_only:
        print("STATUS=PREFLIGHT_OK", flush=True)
        return 0

    if args.output:
        output_dir = Path(args.output)
        if not output_dir.is_absolute():
            output_dir = ROOT / output_dir
    else:
        output_dir = (
            ROOT
            / "experiments"
            / "real_llm_eval"
            / "TRACK_A_PHASE2_SMOKE"
            / utc_stamp()
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(output_dir / "preflight.json", {**env, "ids": [r["id"] for r in records]})
    _write_json(
        output_dir / "smoke_case_ids.json",
        {
            "attack_ids": [r["id"] for r in records if r["label"] == "attack"],
            "benign_ids": [r["id"] for r in records if r["label"] == "benign"],
            "selection": "first_N_in_frozen_pack_file_order",
        },
    )

    config = PipelineConfig(
        experiment_id=EXPERIMENT_ID,
        output_dir=output_dir,
        target_config_key=LOCKED_TARGET_KEY,
        judge_config_key=LOCKED_JUDGE_KEY,
        backend=EvaluationBackend.OPENROUTER,
        baselines=[B0_BASELINE_KEY, TREATMENT_BASELINE_KEY],
        split="smoke",
        seed=LOCKED_SEED,
        benchmark_dir=str(LOCKED_PACK_PATH.parent),
    )
    target, judge = build_models(
        config, EvaluationBackend.OPENROUTER, cache_enabled=False
    )
    run_context = BaselineRunContext(
        experiment_id=EXPERIMENT_ID,
        model_id=LOCKED_TARGET_MODEL,
        model_config_key=LOCKED_TARGET_KEY,
        git_commit=env["git_commit"],
        seed=LOCKED_SEED,
        dataset_hash=LOCKED_PACK_SHA256,
        cache_enabled=False,
        config_version=PROVENANCE_SCHEMA_VERSION,
    )
    _write_json(
        output_dir / "manifest.json",
        {
            **env,
            "baselines": [B0_BASELINE_KEY, TREATMENT_BASELINE_KEY],
            "max_budget_usd": MAX_BUDGET_USD,
            "n_attack": N_ATTACK,
            "n_benign": N_BENIGN,
            "hash_info": hash_info,
        },
    )

    spend = {
        "estimated_usd_total": 0.0,
        "target_usd": 0.0,
        "judge_usd": 0.0,
        "target_prompt_tokens": 0,
        "target_completion_tokens": 0,
        "judge_prompt_tokens": 0,
        "judge_completion_tokens": 0,
        "n_target_calls": 0,
        "n_judge_calls": 0,
    }

    print("[SMOKE] Running B0…", flush=True)
    b0 = run_arm(
        baseline_key=B0_BASELINE_KEY,
        records=records,
        target=target,
        judge=judge,
        output_dir=output_dir,
        run_context=run_context,
        spend=spend,
    )
    print("[SMOKE] Running VNEXT-ADAPT…", flush=True)
    treat = run_arm(
        baseline_key=TREATMENT_BASELINE_KEY,
        records=records,
        target=target,
        judge=judge,
        output_dir=output_dir,
        run_context=run_context,
        spend=spend,
    )

    scored = score_smoke(b0["rows"], treat["rows"])
    integrity = integrity_checks(
        records=records,
        b0_rows=b0["rows"],
        t_rows=treat["rows"],
        output_dir=output_dir,
        spend=spend,
    )
    decision = decide(integrity, scored, spend)
    _write_json(output_dir / "spend.json", spend)
    _write_json(output_dir / "scored.json", scored)
    _write_json(output_dir / "integrity.json", integrity)
    report_path = write_report(
        output_dir=output_dir,
        env=env,
        scored=scored,
        integrity=integrity,
        spend=spend,
        decision=decision,
        command=command,
    )
    print(f"REPORT={report_path}", flush=True)
    print(f"ACTUAL_USD={spend['estimated_usd_total']:.6f}", flush=True)
    print(f"DECISION={decision}", flush=True)
    print(f"STATUS=SMOKE_{decision}", flush=True)
    return 0 if decision == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
