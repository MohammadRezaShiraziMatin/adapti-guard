"""P3 offline counterfactual detector-comparison harness.

Evaluates trajectory × detector × turn and trajectory × detector × policy
schedules. No live LLM/API. Fail-closed on frozen pack SHA mismatch.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from adapti_guard.detectors import default_p3_detectors, list_detector_catalog
from adapti_guard.detectors.base import (
    P1_SHA256,
    P2_SHA256,
    DetectorResult,
    EpisodeDetectionContext,
    P3Detector,
    assert_no_forbidden_keys,
    assert_pack_sha,
    assert_unique_ids,
    assert_unique_output_dir,
    make_detector_observation_id,
    make_end_to_end_arm_id,
)
from adapti_guard.detectors.isolation import state_hash
from adapti_guard.detectors.metrics import aggregate_episode_hits, detector_level_metrics
from adapti_guard.detectors.protocol import ACTION_COSTS, P1_PATH, P2_PATH, config_bundle_hash


# Downstream policy IDs used for scheduling only — thresholds/costs unchanged.
DEFAULT_POLICY_IDS = ("STATIC", "CORE")


def make_evaluation_id(
    run_id: str,
    trajectory_id: str,
    detector_id: str,
    *,
    policy_id: str | None = None,
    turn_id: int | None = None,
) -> str:
    """Unique evaluation record id.

    Turn-level: run_id::trajectory::detector::tN
    Episode×policy: run_id::trajectory::detector::policy
    """
    if policy_id is not None and turn_id is not None:
        raise ValueError("evaluation_id must not mix policy and turn in one key")
    if policy_id is not None:
        return f"{run_id}::{trajectory_id}::{detector_id}::{policy_id}"
    if turn_id is not None:
        return f"{run_id}::{trajectory_id}::{detector_id}::t{int(turn_id)}"
    raise ValueError("evaluation_id requires policy_id or turn_id")


def result_core_dict(result: DetectorResult | Mapping[str, Any]) -> dict[str, Any]:
    """Deterministic core fields (excludes nondeterministic latency)."""
    if isinstance(result, DetectorResult):
        d = result.to_dict()
    else:
        d = dict(result)
    return {
        "detector_id": d["detector_id"],
        "detector_hit": bool(d["detector_hit"]),
        "risk_signal": float(d["risk_signal"]),
        "evidence": list(d.get("evidence") or []),
        "confidence": d.get("confidence"),
        "reason_code": d.get("reason_code"),
        "input_scope": d.get("input_scope"),
        "version": d.get("version"),
    }


def evaluation_hash(
    ctx: EpisodeDetectionContext | Mapping[str, Any],
    result: DetectorResult | Mapping[str, Any],
) -> str:
    payload = {
        "context": ctx.to_dict() if isinstance(ctx, EpisodeDetectionContext) else dict(ctx),
        "result_core": result_core_dict(result),
    }
    return state_hash(payload)


def detect_side_effect_free(
    detector: P3Detector,
    ctx: EpisodeDetectionContext,
    *,
    policy_state: Mapping[str, Any] | None = None,
    tool_state: Mapping[str, Any] | None = None,
    trajectory_state: Mapping[str, Any] | None = None,
) -> DetectorResult:
    """Run detect while asserting external states are unchanged."""
    from adapti_guard.detectors.isolation import assert_state_unchanged, deep_freeze_copy

    assert_no_forbidden_keys(ctx.to_dict())
    ps = deep_freeze_copy(dict(policy_state or {}))
    ts = deep_freeze_copy(dict(tool_state or {}))
    tr = deep_freeze_copy(dict(trajectory_state or {}))
    # Also protect mutable copies that callers may share
    ps_live = dict(policy_state) if policy_state is not None else {}
    ts_live = dict(tool_state) if tool_state is not None else {}
    tr_live = dict(trajectory_state) if trajectory_state is not None else {}
    before = {
        "policy": state_hash(ps_live),
        "tool": state_hash(ts_live),
        "trajectory": state_hash(tr_live),
        "ctx_state": state_hash(dict(ctx.state or {})),
    }
    result = detector.detect(ctx)
    after = {
        "policy": state_hash(ps_live),
        "tool": state_hash(ts_live),
        "trajectory": state_hash(tr_live),
        "ctx_state": state_hash(dict(ctx.state or {})),
    }
    if before != after:
        raise AssertionError(f"detector side effects detected: before={before} after={after}")
    assert_state_unchanged(ps, ps_live, what="policy_state")
    assert_state_unchanged(ts, ts_live, what="tool_state")
    assert_state_unchanged(tr, tr_live, what="trajectory_state")
    return result


def load_frozen_jsonl(path: Path, *, expected_sha: str, label: str) -> list[dict[str, Any]]:
    """Load frozen pack after fail-closed SHA verification."""
    assert_pack_sha(path, expected_sha, label=label)
    rows: list[dict[str, Any]] = []
    with Path(path).open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_p1_frozen() -> list[dict[str, Any]]:
    return load_frozen_jsonl(P1_PATH, expected_sha=P1_SHA256, label="P1")


def load_p2_frozen() -> list[dict[str, Any]]:
    return load_frozen_jsonl(P2_PATH, expected_sha=P2_SHA256, label="P2")


def p1_row_to_context(row: Mapping[str, Any]) -> EpisodeDetectionContext:
    """Map a frozen P1 row to a detection-time context (no gold labels in state)."""
    meta = row.get("metadata") if isinstance(row.get("metadata"), Mapping) else {}
    tool_call = meta.get("tool_call") if isinstance(meta, Mapping) else None
    if not isinstance(tool_call, Mapping):
        tool_call = row.get("tool_call") if isinstance(row.get("tool_call"), Mapping) else {}
    return EpisodeDetectionContext(
        trajectory_id=str(row.get("id")),
        turn_id=0,
        current_input=str(row.get("prompt") or ""),
        context=str(row.get("context") or "") or None,
        tool_name=(str(tool_call.get("name")) if tool_call and tool_call.get("name") else None),
        tool_arguments=(
            dict(tool_call.get("arguments") or {})
            if tool_call and isinstance(tool_call.get("arguments"), Mapping)
            else None
        ),
        source_channel=str(meta.get("context_source") or "user") if isinstance(meta, Mapping) else "user",
        input_scope="current_turn",
    )


def p2_row_to_contexts(row: Mapping[str, Any]) -> list[EpisodeDetectionContext]:
    """Map frozen P2 trajectory to per-turn contexts available at each turn.

    Uses only turns up to and including the current index (no future leakage).
    """
    tid = str(row.get("id"))
    turns_raw = row.get("turns") or row.get("dialogue") or row.get("messages") or []
    contexts: list[EpisodeDetectionContext] = []
    if isinstance(turns_raw, list) and turns_raw:
        prior_bits: list[str] = []
        last_tool = None
        for i, turn in enumerate(turns_raw):
            if not isinstance(turn, Mapping):
                continue
            text = str(
                turn.get("user_content")
                or turn.get("content")
                or turn.get("user")
                or turn.get("text")
                or turn.get("input")
                or ""
            )
            agent_tc = turn.get("agent_tool_call") or turn.get("tool_call") or {}
            if not isinstance(agent_tc, Mapping):
                agent_tc = {}
            tool_name = agent_tc.get("name") or turn.get("tool_name")
            tool_args = (
                dict(agent_tc.get("arguments") or {})
                if isinstance(agent_tc.get("arguments"), Mapping)
                else None
            )
            inj = turn.get("inject_tool_observation")
            tool_output = str(inj) if inj is not None else None
            if tool_output is None and turn.get("tool_output") is not None:
                tool_output = str(turn.get("tool_output"))

            # Provenance channel: prefer explicit source; tool_output if injection present
            channel = str(turn.get("source") or turn.get("source_channel") or "user")
            if tool_output and channel == "user":
                channel = "tool_output"

            # Memory already visible before/at this turn from prior writes + current write text
            mem_ctx = list(prior_bits)
            mw = turn.get("memory_write")
            if isinstance(mw, Mapping) and mw:
                mem_ctx.append("MEMORY: " + " ".join(f"{k}={v}" for k, v in mw.items()))

            turn_id = int(turn.get("turn_id")) if turn.get("turn_id") is not None else i
            ctx = EpisodeDetectionContext(
                trajectory_id=tid,
                turn_id=turn_id,
                current_input=text,
                context="\n".join(mem_ctx) if mem_ctx else None,
                tool_name=str(tool_name) if tool_name else None,
                tool_arguments=tool_args,
                tool_output=tool_output,
                source_channel=channel,
                state={"last_tool_name": last_tool} if last_tool else None,
                input_scope="current_turn",
            )
            contexts.append(ctx)
            if text:
                prior_bits.append(text)
            if isinstance(mw, Mapping) and mw:
                prior_bits.append("MEMORY: " + " ".join(f"{k}={v}" for k, v in mw.items()))
            if tool_output:
                prior_bits.append(f"TOOL_OUTPUT:{tool_output}")
            if tool_name:
                last_tool = str(tool_name)
        if contexts:
            return contexts

    # Fallback: single-turn from top-level prompt-like fields
    text = str(row.get("prompt") or row.get("user_input") or row.get("seed_prompt") or "")
    if not text:
        meta = row.get("metadata") if isinstance(row.get("metadata"), Mapping) else {}
        text = str(meta.get("seed_prompt") or meta.get("prompt") or json.dumps({"id": tid})[:500])
    return [
        EpisodeDetectionContext(
            trajectory_id=tid,
            turn_id=0,
            current_input=text,
            source_channel=str(row.get("attack_channel") or "user"),
            input_scope="current_turn",
        )
    ]


def label_sets_from_rows(rows: Sequence[Mapping[str, Any]]) -> dict[str, set[str]]:
    attack, benign, hn = set(), set(), set()
    for r in rows:
        tid = str(r.get("id"))
        label = str(r.get("label") or "").lower()
        hard = bool(r.get("hard_negative") or (r.get("metadata") or {}).get("hard_negative"))
        if label == "attack":
            attack.add(tid)
        elif label == "benign" and hard:
            hn.add(tid)
        elif label == "benign":
            benign.add(tid)
        elif label in {"hard_negative", "hard-negative"}:
            hn.add(tid)
        else:
            benign.add(tid)
    return {"attack_ids": attack, "benign_ids": benign, "hard_negative_ids": hn}


def mechanism_map_from_rows(rows: Sequence[Mapping[str, Any]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for r in rows:
        tid = str(r.get("id"))
        meta = r.get("metadata") if isinstance(r.get("metadata"), Mapping) else {}
        mech = (
            r.get("mechanism_id")
            or r.get("family")
            or meta.get("family")
            or meta.get("mechanism")
            or "unknown"
        )
        out[tid] = str(mech)
    return out


class OfflineDetectorHarness:
    """Counterfactual offline harness for P3-A/B style matrices."""

    def __init__(
        self,
        *,
        run_id: str,
        detectors: Mapping[str, P3Detector] | None = None,
        policy_ids: Sequence[str] = DEFAULT_POLICY_IDS,
    ) -> None:
        self.run_id = run_id
        self.detectors = dict(detectors or default_p3_detectors())
        self.policy_ids = list(policy_ids)
        # Preserve downstream constants (must not change)
        self.action_costs = dict(ACTION_COSTS)

    def evaluate_turn_matrix(
        self,
        contexts: Sequence[EpisodeDetectionContext],
    ) -> list[dict[str, Any]]:
        """Produce unique trajectory × detector × turn records."""
        rows: list[dict[str, Any]] = []
        eval_ids: list[str] = []
        for ctx in contexts:
            assert_no_forbidden_keys(ctx.to_dict())
            for det_id, det in self.detectors.items():
                result = detect_side_effect_free(det, ctx)
                eid = make_evaluation_id(
                    self.run_id, ctx.trajectory_id, det_id, turn_id=ctx.turn_id
                )
                eval_ids.append(eid)
                core = result_core_dict(result)
                rows.append(
                    {
                        "evaluation_id": eid,
                        "observation_id": make_detector_observation_id(
                            ctx.trajectory_id, det_id, ctx.turn_id
                        ),
                        "run_id": self.run_id,
                        "trajectory_id": ctx.trajectory_id,
                        "detector_id": det_id,
                        "turn_id": ctx.turn_id,
                        "result": result.to_dict(),
                        "result_core": core,
                        "evaluation_hash": evaluation_hash(ctx, result),
                        "statistical_unit_note": "turn_observation_not_episode",
                    }
                )
        assert_unique_ids(eval_ids, what="evaluation_id trajectory×detector×turn")
        return rows

    def build_policy_schedule(
        self, trajectory_ids: Sequence[str]
    ) -> list[dict[str, Any]]:
        """Schedule unique trajectory × detector × policy arms (no execution)."""
        arms: list[dict[str, Any]] = []
        eval_ids: list[str] = []
        for tid in trajectory_ids:
            for det_id in self.detectors:
                for pid in self.policy_ids:
                    eid = make_evaluation_id(
                        self.run_id, tid, det_id, policy_id=pid
                    )
                    eval_ids.append(eid)
                    arms.append(
                        {
                            "evaluation_id": eid,
                            "arm_id": make_end_to_end_arm_id(tid, det_id, pid),
                            "run_id": self.run_id,
                            "trajectory_id": tid,
                            "detector_id": det_id,
                            "policy_id": pid,
                            "action_costs": dict(self.action_costs),
                            "statistical_unit": "episode",
                        }
                    )
        assert_unique_ids(eval_ids, what="evaluation_id trajectory×detector×policy")
        return arms

    def run_pack(
        self,
        *,
        pack: str,
        output_dir: Path | None = None,
        max_trajectories: int | None = None,
    ) -> dict[str, Any]:
        """Offline matrix on frozen P1 or P2. Writes artifacts if output_dir set."""
        pack = pack.upper()
        if pack == "P1":
            rows = load_p1_frozen()
            sha = P1_SHA256
            contexts: list[EpisodeDetectionContext] = []
            for r in rows[: max_trajectories or len(rows)]:
                contexts.append(p1_row_to_context(r))
        elif pack == "P2":
            rows = load_p2_frozen()
            sha = P2_SHA256
            contexts = []
            for r in rows[: max_trajectories or len(rows)]:
                contexts.extend(p2_row_to_contexts(r))
        else:
            raise ValueError(f"unknown pack {pack}")

        labels = label_sets_from_rows(rows[: max_trajectories or len(rows)])
        mechs = mechanism_map_from_rows(rows[: max_trajectories or len(rows)])
        turn_rows = self.evaluate_turn_matrix(contexts)
        traj_ids = sorted({c.trajectory_id for c in contexts})
        policy_arms = self.build_policy_schedule(traj_ids)
        det_metrics = detector_level_metrics(
            turn_rows,
            attack_ids=labels["attack_ids"],
            benign_ids=labels["benign_ids"],
            hard_negative_ids=labels["hard_negative_ids"],
            mechanism_by_id=mechs,
        )
        episode_hits = {
            f"{tid}::{did}": hit
            for (tid, did), hit in aggregate_episode_hits(turn_rows).items()
        }

        manifest = {
            "stage": "P3_OFFLINE",
            "run_id": self.run_id,
            "pack": pack,
            "benchmark_sha256": sha,
            "p1_sha256": P1_SHA256,
            "p2_sha256": P2_SHA256,
            "detectors": list_detector_catalog(),
            "detector_config_bundle_hash": config_bundle_hash(self.detectors),
            "policy_ids": list(self.policy_ids),
            "action_costs": dict(self.action_costs),
            "live_execution_authorized": False,
            "n_trajectories": len(traj_ids),
            "n_turn_observations": len(turn_rows),
            "n_policy_arms": len(policy_arms),
            "primary_security_endpoint": "Tool-HASR",
            "secondary_security_endpoint": "Judge-ASR",
            "d3_status": "DEFERRED_NO_OFFLINE_IMPL",
            "scientific_performance_claim": False,
        }

        artifact = {
            "manifest": manifest,
            "turn_observations": turn_rows,
            "policy_schedule": policy_arms,
            "detector_level_metrics": det_metrics,
            "episode_hits": episode_hits,
            "label_sets": {k: sorted(v) for k, v in labels.items()},
            "reproducibility_hash": state_hash(
                {
                    "manifest_core": {
                        k: manifest[k]
                        for k in (
                            "run_id",
                            "pack",
                            "benchmark_sha256",
                            "detector_config_bundle_hash",
                            "policy_ids",
                            "action_costs",
                        )
                    },
                    "n_turn_observations": len(turn_rows),
                    "eval_ids": [r["evaluation_id"] for r in turn_rows],
                    "eval_hashes": [r["evaluation_hash"] for r in turn_rows],
                }
            ),
        }

        if output_dir is not None:
            out = Path(output_dir)
            assert_unique_output_dir(out)
            out.mkdir(parents=True, exist_ok=True)
            (out / "manifest.json").write_text(
                json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            (out / "turn_observations.jsonl").write_text(
                "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in turn_rows),
                encoding="utf-8",
            )
            (out / "policy_schedule.jsonl").write_text(
                "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in policy_arms),
                encoding="utf-8",
            )
            (out / "metrics.json").write_text(
                json.dumps(
                    {
                        "detector_level_metrics": det_metrics,
                        "episode_hits": episode_hits,
                        "label_sets": artifact["label_sets"],
                    },
                    indent=2,
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            (out / "reproducibility.json").write_text(
                json.dumps(
                    {"reproducibility_hash": artifact["reproducibility_hash"]},
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            artifact["output_dir"] = str(out)

        return artifact


def verify_benchmark_bytes_unchanged(path: Path, *, expected_sha: str) -> str:
    """Fail closed if frozen file bytes diverge."""
    return assert_pack_sha(path, expected_sha, label=str(path))
