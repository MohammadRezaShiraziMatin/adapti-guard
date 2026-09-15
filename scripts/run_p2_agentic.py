#!/usr/bin/env python3
"""Offline P2.2 agentic harness runner (NO LLM/API).

Default mode runs the tiny deterministic smoke suite and writes artifacts.
Live evaluation flags are rejected in this phase.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from adapti_guard.experiments.p2_agentic import (  # noqa: E402
    OfflinePolicy,
    example_smoke_trajectories,
    run_offline_suite,
    write_run_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="P2.2 offline agentic harness (no API)")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output",
        default="experiments/real_llm_eval/P2_AGENTIC_OFFLINE/smoke",
        help="Output directory for offline smoke artifacts",
    )
    parser.add_argument(
        "--policy",
        default="scripted",
        help="scripted (default) or a baseline key for offline policy mode",
    )
    parser.add_argument("--stage-a", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--stage-b", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--live", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.stage_a or args.stage_b or args.live:
        print("STATUS=STOP_LIVE_NOT_AUTHORIZED_IN_P2_2", flush=True)
        print(
            "P2.2 is offline-only. Do not pass --stage-a/--stage-b/--live.",
            file=sys.stderr,
        )
        return 2

    if args.policy == "scripted":
        policy = OfflinePolicy(mode="scripted")
    else:
        policy = OfflinePolicy(mode="policy", policy_key=args.policy)

    payload = run_offline_suite(
        example_smoke_trajectories(),
        seed=args.seed,
        policy=policy,
    )
    out = Path(args.output)
    if not out.is_absolute():
        out = ROOT / out
    paths = write_run_artifacts(payload, out)
    print(json.dumps({"status": "P2_2_OFFLINE_SMOKE_OK", "paths": paths, "metrics": payload["metrics"]}, indent=2))
    print("STATUS=P2_2_OFFLINE_SMOKE_OK", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
