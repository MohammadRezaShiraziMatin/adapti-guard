#!/usr/bin/env python3
"""Live eval preflight — NO generation API calls."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adapti_guard.evaluation.experiment_logging import git_commit
from adapti_guard.evaluation.live_extension_wiring import (
    DEFAULT_LIVE_RUN_ROOT,
    authorization_allows_live_spend,
    load_authorization_yaml,
    load_wiring,
)
from adapti_guard.evaluation.live_model_resolver import validate_target_judge_keys
from adapti_guard.experiments.env_loader import load_project_env, validate_openrouter_key


def main() -> int:
    load_project_env()
    checks: dict[str, str] = {}
    ok_or, msg = validate_openrouter_key()
    checks["openrouter_key_format"] = "PASS" if ok_or else f"FAIL:{msg}"
    checks["api_key_present"] = "true" if ok_or else "false"

    auth_ok, auth_reason = authorization_allows_live_spend()
    checks["authorization_complete"] = "true" if auth_ok else "false"
    checks["authorization_detail"] = auth_reason if not auth_ok else "ok"

    auth_yaml = load_authorization_yaml(ROOT / "docs/research/live_budget_authorization.yaml")
    checks["api_spend_permitted_yaml"] = str(bool(auth_yaml.get("api_spend_permitted")))

    try:
        validate_target_judge_keys("model_b", "judge_primary")
        checks["target_ne_judge_sample"] = "PASS"
    except Exception as exc:
        checks["target_ne_judge_sample"] = f"FAIL:{exc}"

    p7 = ROOT / "docs/research/PHASE7_LIVE_AUTHORIZATION.json"
    if p7.is_file():
        j = json.loads(p7.read_text())
        checks["authorization_gate"] = j.get("live_execution_gate", "UNKNOWN")
        checks["api_spend_permitted"] = str(j.get("api_spend_permitted", False))
    else:
        checks["authorization_gate"] = "MISSING_PHASE7_JSON"

    schema = (ROOT / "docs/research/EVIDENCE_SCHEMA.yaml").is_file()
    checks["evidence_schema"] = "PASS" if schema else "FAIL"

    try:
        wiring = load_wiring(ROOT / "docs/research/PHASE7_LIVE_EXTENSION_WIRING.yaml")
        checks["condition_ids"] = "PASS"
        checks["canonical_runner"] = str(
            (wiring.get("canonical_executors") or {}).get("live_extension", "MISSING")
        )
    except Exception as exc:
        checks["condition_ids"] = f"FAIL:{exc}"
        checks["canonical_runner"] = "FAIL"

    max_req = auth_yaml.get("max_requests")
    if isinstance(max_req, int):
        checks["budget_contract"] = "PASS"
    elif isinstance(max_req, str) and max_req.startswith("PENDING"):
        checks["budget_contract"] = "PENDING"
    else:
        checks["budget_contract"] = "PENDING"

    checks["output_path_root"] = "PASS" if DEFAULT_LIVE_RUN_ROOT.parent.is_dir() else "FAIL"
    checks["code_commit"] = git_commit() or "UNKNOWN"

    blocked = checks.get("authorization_gate") != "LIVE_AUTHORIZED" or not auth_ok
    out = {"status": "BLOCKED" if blocked else "READY", "checks": checks, "api_generation": "NOT_RUN"}
    print(json.dumps(out, indent=2))
    return 0 if not blocked else 1


if __name__ == "__main__":
    sys.exit(main())
