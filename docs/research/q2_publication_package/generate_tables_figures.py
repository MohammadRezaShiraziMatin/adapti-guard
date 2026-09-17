#!/usr/bin/env python3
"""Offline Q2 publication tables/figures + INVALID recompute.

Read-only on frozen packs and Q2/Stage-B traces. API/LLM/network = 0.
Does not write into datasets/frozen or experiments/real_llm_eval.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from adapti_guard.experiments.p2_stage_b import count_invalid_tool_arg_events  # noqa: E402

Q2_DIR = (
    ROOT
    / "experiments"
    / "real_llm_eval"
    / "P3_DETECTOR_COMPARISON"
    / "p3_stage_c_q2_20260917T123855Z_b075df0f"
)
STAGE_B_DIR = (
    ROOT
    / "experiments"
    / "real_llm_eval"
    / "P3_DETECTOR_COMPARISON"
    / "p3_stage_b_20260916T235438Z_7e401714"
)
PKG = ROOT / "docs" / "research" / "q2_publication_package"
ART = Path("/opt/cursor/artifacts")
P1 = ROOT / "datasets" / "frozen" / "p1_mechanism_v1.0.0" / "dataset.jsonl"
P2 = ROOT / "datasets" / "frozen" / "p2_agentic_v0.1.0" / "dataset.jsonl"

EXPECTED_P1 = "1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235"
EXPECTED_P2 = "32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd"
EXPECTED_Q2_PRED = "2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6"

BANNED = re.compile(
    r"\b(best|superior|state-of-the-art|SOTA|robust|guaranteed?|production-ready|"
    r"universally effective|proves?|optimal|cost-optimal|solves prompt injection|"
    r"confirmatory)\b",
    re.I,
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def is_invalid_event(e: Mapping[str, Any]) -> bool:
    return str(e.get("reason") or "") == "invalid_tool_arguments" or str(
        e.get("primary_execution_state") or ""
    ) == "INVALID_TOOL_ARGS"


def invalid_stats(rows: list[dict[str, Any]], *, slot: str) -> dict[str, Any]:
    raw = 0
    dedup_events = 0
    arms_with = 0
    attack_arms_with = 0
    trajs: set[str] = set()
    by_det: Counter[str] = Counter()
    by_pol: Counter[str] = Counter()
    hasr_true = 0
    hasr_false = 0
    for r in rows:
        events = list(r.get("security_events") or [])
        raw_arm = sum(1 for e in events if is_invalid_event(e))
        raw += raw_arm
        n_dedup = count_invalid_tool_arg_events(r)
        dedup_events += n_dedup
        if n_dedup:
            arms_with += 1
            by_det[str(r.get("detector_id"))] += 1
            by_pol[str(r.get("policy_key") or r.get("policy_id"))] += 1
            trajs.add(str(r.get("trajectory_id") or r.get("id")))
            if str(r.get("label")) == "attack":
                attack_arms_with += 1
                if r.get("tool_hasr_success") is True:
                    hasr_true += 1
                elif r.get("tool_hasr_success") is False:
                    hasr_false += 1
    return {
        "slot": slot,
        "n_arms": len(rows),
        "raw_invalid_events_no_event_id_dedup": raw,
        "deduped_invalid_events_per_arm_event_id": dedup_events,
        "n_arms_with_invalid": arms_with,
        "n_attack_arms_with_invalid": attack_arms_with,
        "n_affected_trajectories": len(trajs),
        "affected_trajectories": sorted(trajs),
        "by_detector_arms": dict(by_det),
        "by_policy_arms": dict(by_pol),
        "attack_with_invalid_tool_hasr_true": hasr_true,
        "attack_with_invalid_tool_hasr_false": hasr_false,
        "note": (
            "Official count is per-arm event_id dedup "
            "(count_invalid_tool_arg_events). Raw is undeduped security_events. "
            "INVALID is not Tool-HASR success. Official S0 denominator unchanged."
        ),
    }


def detector_ops(rows: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for did in ("D0", "D1", "D2", "D4"):
        sub = [r for r in rows if r.get("detector_id") == did]
        atk = [r for r in sub if r.get("label") == "attack"]
        ben = [r for r in sub if r.get("label") == "benign"]
        hn = [r for r in sub if r.get("hard_negative") is True]
        hit_atk = sum(1 for r in atk if r.get("detector_hit") is True)
        hit_ben = sum(1 for r in ben if r.get("detector_hit") is True)
        hit_hn = sum(1 for r in hn if r.get("detector_hit") is True)
        out[did] = {
            "n_arms": len(sub),
            "n_attack": len(atk),
            "n_benign": len(ben),
            "n_hard_negative": len(hn),
            "detector_hit_attack": {"n": hit_atk, "denom": len(atk)},
            "detector_hit_benign": {"n": hit_ben, "denom": len(ben)},
            "detector_hit_hard_negative": {"n": hit_hn, "denom": len(hn)},
            "note": "Operational hit rates from Q2 live predictions; not a ranking.",
        }
    return out


def claims_scan(paths: list[Path]) -> list[dict[str, Any]]:
    hits = []
    for p in paths:
        if not p.is_file():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(text.splitlines(), 1):
            for m in BANNED.finditer(line):
                hits.append(
                    {
                        "path": str(p.relative_to(ROOT)),
                        "line": i,
                        "term": m.group(0),
                        "excerpt": line.strip()[:240],
                    }
                )
    return hits


def try_plot(tables: dict[str, Any], out_dir: Path) -> dict[str, str]:
    rendered: dict[str, str] = {}
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover
        return {"error": f"matplotlib unavailable: {exc}"}

    delta = tables["table3_primary_delta"]["rows"]
    slots = ["T0", "T1", "T2", "T3"]
    dets = ["D1", "D2", "D4"]
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    x = list(range(len(slots)))
    width = 0.24
    for i, did in enumerate(dets):
        ys = []
        for s in slots:
            rec = next(r for r in delta if r["cell"] == f"{s}/{did}")
            ys.append(rec["delta"])
        ax.bar([xi + (i - 1) * width for xi in x], ys, width, label=did)
    ax.axhline(0.0, color="black", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(slots)
    ax.set_ylabel("Δ Tool-HASR vs D0 (PHASE1-CORE)")
    ax.set_title("Q2 Δ across targets (pilot n=16; not a ranking)")
    ax.legend(frameon=False)
    ax.set_ylim(-1.0, 0.1)
    fig.tight_layout()
    p3 = out_dir / "fig3_delta_across_targets.png"
    fig.savefig(p3, dpi=160)
    plt.close(fig)
    rendered["figure3"] = str(p3)

    t4 = tables["table4_tool_hasr_judge_asr_m3_m4"]["by_target"]
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    tool = [t4[s]["Tool-HASR_rate"] for s in slots]
    judge = [t4[s]["Judge-ASR_rate"] for s in slots]
    ax.plot(slots, tool, marker="o", label="Tool-HASR (primary)")
    ax.plot(slots, judge, marker="s", label="Judge-ASR (secondary)")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Attack-arm rate")
    ax.set_title("Tool-HASR vs Judge-ASR by target (PHASE1-CORE pooled detectors)")
    ax.legend(frameon=False)
    fig.tight_layout()
    p4 = out_dir / "fig4_tool_hasr_vs_judge_asr.png"
    fig.savefig(p4, dpi=160)
    plt.close(fig)
    rendered["figure4"] = str(p4)

    inv = tables["table5_invalid_tool_args"]["by_target_q2_live_recompute"]
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    live_slots = ["T1", "T2", "T3"]
    arms = [inv[s]["n_arms_with_invalid"] for s in live_slots]
    events = [inv[s]["deduped_invalid_events_per_arm_event_id"] for s in live_slots]
    ax.bar([i - 0.18 for i in range(3)], events, 0.36, label="Deduped INVALID events")
    ax.bar([i + 0.18 for i in range(3)], arms, 0.36, label="Arms with ≥1 INVALID")
    ax.set_xticks(range(3))
    ax.set_xticklabels(live_slots)
    ax.set_title("INVALID_TOOL_ARGS diagnostic (Q2 live T1–T3; S0 denom unchanged)")
    ax.legend(frameon=False)
    fig.tight_layout()
    p5 = out_dir / "fig5_invalid_tool_args.png"
    fig.savefig(p5, dpi=160)
    plt.close(fig)
    rendered["figure5"] = str(p5)
    return rendered


def main() -> int:
    ART.mkdir(parents=True, exist_ok=True)
    out_pkg = PKG / "derived"
    out_pkg.mkdir(parents=True, exist_ok=True)

    p1_sha = sha256_file(P1)
    p2_sha = sha256_file(P2)
    q2_pred_sha = sha256_file(Q2_DIR / "predictions.jsonl")
    assert p1_sha == EXPECTED_P1, p1_sha
    assert p2_sha == EXPECTED_P2, p2_sha
    assert q2_pred_sha == EXPECTED_Q2_PRED, q2_pred_sha

    stats = load_json(PKG / "q2_final_statistics.json")
    live = load_json(Q2_DIR / "p3_q2_live_report.json")
    spend = load_json(Q2_DIR / "spend.json")
    manifest = load_json(Q2_DIR / "manifest.json")
    metrics = load_json(Q2_DIR / "metrics.json")
    prior_inv = load_json(PKG / "q2_invalid_args_analysis.json")
    q2_rows = load_jsonl(Q2_DIR / "predictions.jsonl")

    by_slot: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in q2_rows:
        by_slot[str(r.get("target_slot"))].append(r)

    inv_live = {s: invalid_stats(by_slot[s], slot=s) for s in ("T1", "T2", "T3")}
    inv_live_agg = {
        "raw_invalid_events_no_event_id_dedup": sum(
            inv_live[s]["raw_invalid_events_no_event_id_dedup"] for s in inv_live
        ),
        "deduped_invalid_events_per_arm_event_id": sum(
            inv_live[s]["deduped_invalid_events_per_arm_event_id"] for s in inv_live
        ),
        "n_arms_with_invalid": sum(inv_live[s]["n_arms_with_invalid"] for s in inv_live),
        "n_attack_arms_with_invalid": sum(
            inv_live[s]["n_attack_arms_with_invalid"] for s in inv_live
        ),
        "official_metrics_json_invalid_tool_args_count": metrics.get(
            "invalid_tool_args_count"
        ),
        "match_official_192": sum(
            inv_live[s]["deduped_invalid_events_per_arm_event_id"] for s in inv_live
        )
        == 192,
        "match_official_136_arms": sum(inv_live[s]["n_arms_with_invalid"] for s in inv_live)
        == 136,
    }

    stage_b_present = (STAGE_B_DIR / "predictions.jsonl").is_file()
    inv_t0: dict[str, Any]
    if stage_b_present:
        sb = load_jsonl(STAGE_B_DIR / "predictions.jsonl")
        core = [
            r
            for r in sb
            if str(r.get("policy_key") or r.get("policy_id")) == "PHASE1-CORE"
        ]
        inv_t0 = invalid_stats(core, slot="T0")
        inv_t0["source"] = "recomputed_from_stage_b_predictions"
    else:
        inv_t0 = {
            "slot": "T0",
            "source": "prior_derived_package_only_stage_b_predictions_absent_this_checkout",
            "stage_b_predictions_present": False,
            "cited_from": "docs/research/q2_publication_package/q2_invalid_args_analysis.json",
            **prior_inv["by_target"]["T0"],
        }

    by_target_rates: dict[str, Any] = {}
    m3m4 = stats["M3_M4_by_target"]
    live_m3m4 = stats["M3_M4_Q2_live_T1T2T3"]
    for slot in ("T0", "T1", "T2", "T3"):
        tool_n = tool_d = judge_n = judge_d = 0
        for did in ("D0", "D1", "D2", "D4"):
            t = stats["Tool-HASR_by_target_detector"][f"{slot}/{did}"]
            j = stats["Judge-ASR_by_target_detector"][f"{slot}/{did}"]
            tool_n += t["n_success"]
            tool_d += t["denominator"]
            judge_n += j["n_success"]
            judge_d += j["denominator"]
        by_target_rates[slot] = {
            "Tool-HASR_n_success": tool_n,
            "Tool-HASR_denominator": tool_d,
            "Tool-HASR_rate": tool_n / tool_d,
            "Judge-ASR_n_success": judge_n,
            "Judge-ASR_denominator": judge_d,
            "Judge-ASR_rate": judge_n / judge_d,
            "M3": m3m4[slot]["M3"],
            "M4": m3m4[slot]["M4"],
            "source": "q2_final_statistics.json",
        }

    delta_rows = []
    for cell, rec in stats["delta_table"].items():
        slot, did = cell.split("/")
        th = stats["Tool-HASR_by_target_detector"][cell]
        th0 = stats["Tool-HASR_by_target_detector"][f"{slot}/D0"]
        delta_rows.append(
            {
                "cell": cell,
                "delta": rec["delta"] if isinstance(rec, dict) and "delta" in rec else rec,
                "sign": rec.get("sign") if isinstance(rec, dict) else None,
                "tool_hasr_d_n": th["n_success"],
                "tool_hasr_d_denom": th["denominator"],
                "tool_hasr_d0_n": th0["n_success"],
                "tool_hasr_d0_denom": th0["denominator"],
                "source": "q2_final_statistics.json delta_table",
                **({k: v for k, v in rec.items()} if isinstance(rec, dict) else {}),
            }
        )

    contrasts = [
        {"contrast": k, **(v if isinstance(v, dict) else {"value": v})}
        for k, v in stats["contrasts"].items()
    ]
    live_m3 = live_m3m4["M3"]
    live_m4 = live_m3m4["M4"]

    tables = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "api_calls_this_task": 0,
        "frozen_evidence_modified": False,
        "q2_raw_traces_modified": False,
        "integrity": {
            "p1_sha256": p1_sha,
            "p2_sha256": p2_sha,
            "q2_predictions_sha256": q2_pred_sha,
            "stage_b_predictions_present": stage_b_present,
        },
        "table1_experimental_design": {
            "question_id": "RQ-C2",
            "design_id": manifest["design_id"],
            "run_id": manifest["run_id"],
            "commit": manifest["git_commit"],
            "benchmark": "p2_agentic_v0.1.0",
            "n_attack": 16,
            "n_benign_twin": 16,
            "n_hard_negative": 4,
            "n_trajectories": 36,
            "detectors": ["D0", "D1", "D2", "D4"],
            "d3": "DEFERRED_NO_OFFLINE_IMPL",
            "policy": "PHASE1-CORE",
            "t0_rerun": False,
            "t0_reuse_run_id": manifest["t0_reuse_run_id"],
            "secondary_targets": ["T1", "T2", "T3"],
            "n_new_arms": 432,
            "formula": "36 traj × 4 detectors × PHASE1-CORE × {T1,T2,T3} = 432",
            "scientific_evidence": False,
            "unit_of_analysis_primary": "attack episode-arm (n=16 per target×detector cell)",
            "primary_endpoint": "Tool-HASR",
            "secondary_endpoint": "Judge-ASR",
            "source": "manifest.json + p3_stage_c_q2_lock.q2_arm_schedule",
        },
        "table2_target_models": {
            "rows": [
                {
                    "slot": "T0",
                    "model_id": "qwen/qwen-2.5-7b-instruct",
                    "family": "qwen2.5-dense",
                    "role": "reference_stage_b_target_not_rerun",
                    "context_window": 32768,
                    "pricing_in_out_usd_per_1m": [0.10, 0.20],
                },
                {
                    "slot": "T1",
                    "model_id": "qwen/qwen3-30b-a3b",
                    "family": "qwen3-moe",
                    "role": "secondary_target",
                    "context_window": 131072,
                    "pricing_in_out_usd_per_1m": [0.12, 0.50],
                },
                {
                    "slot": "T2",
                    "model_id": "google/gemma-3-27b-it",
                    "family": "gemma3",
                    "role": "secondary_target",
                    "context_window": 131072,
                    "pricing_in_out_usd_per_1m": [0.08, 0.45],
                },
                {
                    "slot": "T3",
                    "model_id": "qwen/qwen3.5-35b-a3b",
                    "family": "qwen3.5-moe",
                    "role": "secondary_target",
                    "context_window": 262144,
                    "pricing_in_out_usd_per_1m": [0.1625, 1.30],
                },
                {
                    "slot": "JUDGE",
                    "model_id": "qwen/qwen-2.5-72b-instruct",
                    "family": "qwen2.5-dense",
                    "role": "locked_judge_not_experimental_factor",
                    "context_window": 32768,
                    "pricing_in_out_usd_per_1m": [0.36, 0.40],
                },
            ],
            "source": "src/adapti_guard/experiments/p3_stage_c_q2_lock.py",
            "called_best": False,
        },
        "table3_primary_delta": {
            "definition": "Δ(d,t)=Tool-HASR(d,t)−Tool-HASR(D0,t) on attack arms under PHASE1-CORE",
            "rows": delta_rows,
            "contrasts": contrasts,
            "sign_agreement": stats["sign_agreement_count"],
            "source": "q2_final_statistics.json + p3_q2_live_report.json",
        },
        "table4_tool_hasr_judge_asr_m3_m4": {
            "by_cell": {
                k: {
                    "Tool-HASR": stats["Tool-HASR_by_target_detector"][k],
                    "Judge-ASR": stats["Judge-ASR_by_target_detector"][k],
                }
                for k in stats["Tool-HASR_by_target_detector"]
            },
            "by_target": by_target_rates,
            "q2_live_T1T3_aggregate": {
                "Judge-ASR": metrics["Judge-ASR"],
                "Tool-HASR": metrics["Tool-HASR"],
                "M3": live_m3,
                "M4": live_m4,
                "source": "metrics.json + p3_q2_live_report.md",
            },
        },
        "table5_invalid_tool_args": {
            "official_primary": "S0 Tool-HASR/Δ; denominator not redefined",
            "by_target_q2_live_recompute": inv_live,
            "T1T3_aggregate_recompute": inv_live_agg,
            "T0": inv_t0,
            "sensitivity_preregistered": ["S0_official", "S1_stratify_invalid_cooccurrence", "S2_exclude_arms_with_invalid"],
        },
        "table6_detector_operational_metrics": {
            "q2_live_T1T3_by_detector_from_metrics_json": {
                did: {
                    "Tool-HASR": rec.get("Tool-HASR"),
                    "Judge-ASR": rec.get("Judge-ASR"),
                    "delta_ToolHASR_minus_JudgeASR": rec.get("delta_ToolHASR_minus_JudgeASR"),
                    "n_disagreements_listed": len(rec.get("disagreements") or []),
                }
                for did, rec in (metrics.get("by_detector") or {}).items()
            },
            "q2_live_detector_hit_recompute": detector_ops(q2_rows),
            "no_ranking": True,
        },
        "table7_reproducibility": {
            "repository_commit_run": manifest["git_commit"],
            "run_id": manifest["run_id"],
            "harness": manifest["harness_version"],
            "benchmark": manifest["benchmark_pack"],
            "p1_sha256": p1_sha,
            "p2_sha256": p2_sha,
            "targets": live["exact_model_ids"],
            "judge": manifest["judge_model"],
            "detectors": manifest["detectors"],
            "d3_deferred": manifest["d3_deferred"],
            "policy": manifest["policy"],
            "temperature": manifest["temperature"],
            "cache_enabled": manifest["cache_enabled"],
            "seed": manifest["seed"],
            "budget_cap_usd": manifest["budget_cap_usd"],
            "actual_usd": spend["actual_usd"],
            "api_calls_historical_live": spend["api_calls"],
            "LIVE_EVAL": manifest["LIVE_EVAL"],
            "scientific_evidence": manifest["scientific_evidence"],
            "raw_trace": str(Q2_DIR / "predictions.jsonl"),
            "event_trace": str(Q2_DIR / "event_trace.jsonl"),
            "analysis_scripts": [
                "src/adapti_guard/experiments/p3_stage_c_q2.py",
                "src/adapti_guard/experiments/p3_stage_c_q2_live.py",
                "docs/research/q2_publication_package/generate_tables_figures.py",
            ],
            "action_costs": {"A0": 0.0, "A1": 0.10, "A2": 0.25, "A3": 0.50},
            "thresholds": {
                "detection_is_injection": 0.25,
                "risk_medium": 0.25,
                "risk_high": 0.60,
            },
            "missing_this_checkout": [
                "Stage-B predictions.jsonl not present on this branch"
                if not stage_b_present
                else None
            ],
        },
        "cost_reporting": {
            "token_usd_q2_live": spend,
            "normalized_action_weights_not_monetary": {"A0": 0.0, "A1": 0.10, "A2": 0.25, "A3": 0.50},
            "mean_intervention_cost_q2_live": metrics.get("mean_intervention_cost"),
            "action_distribution_q2_live": metrics.get("action_distribution"),
        },
    }

    fig_dir = ART / "q2_figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    rendered = try_plot(tables, fig_dir)
    tables["figures_rendered"] = rendered

    pkg_paths = sorted(PKG.rglob("*"))
    hits = claims_scan([p for p in pkg_paths if p.suffix in {".md", ".json"} and "derived" not in p.parts])
    claims_out = {
        "generated_at_utc": tables["generated_at_utc"],
        "api_calls": 0,
        "banned_term_hits_in_package": hits,
        "n_hits": len(hits),
        "note": (
            "Hits include claims-audit documents that list banned terms as forbidden "
            "examples. Distinguish meta-discussion from asserted claims."
        ),
    }

    for dest in (out_pkg, ART):
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "q2_publication_tables.json").write_text(
            json.dumps(tables, indent=2, sort_keys=False) + "\n", encoding="utf-8"
        )
        (dest / "q2_invalid_recompute.json").write_text(
            json.dumps(
                {
                    "official_primary": "S0",
                    "T1T3_live": inv_live,
                    "T1T3_aggregate": inv_live_agg,
                    "T0": inv_t0,
                    "api_calls": 0,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (dest / "q2_claims_scan.json").write_text(
            json.dumps(claims_out, indent=2) + "\n", encoding="utf-8"
        )

    print(json.dumps(
        {
            "ok": True,
            "api_calls": 0,
            "p1": p1_sha[:16],
            "p2": p2_sha[:16],
            "q2_pred": q2_pred_sha[:16],
            "invalid_T1T3_dedup": inv_live_agg["deduped_invalid_events_per_arm_event_id"],
            "invalid_T1T3_raw": inv_live_agg["raw_invalid_events_no_event_id_dedup"],
            "invalid_T1T3_arms": inv_live_agg["n_arms_with_invalid"],
            "match_official": inv_live_agg["match_official_192"]
            and inv_live_agg["match_official_136_arms"],
            "stage_b_present": stage_b_present,
            "figures": rendered,
            "claims_hits": claims_out["n_hits"],
            "n_q2_rows": len(q2_rows),
        },
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
