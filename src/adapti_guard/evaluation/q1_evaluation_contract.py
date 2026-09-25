"""Q1 evaluation protocol — offline contract validation (no API)."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import yaml

from adapti_guard.evaluation.b2_adaptive_contract import LIVE_WIRING_MAX_TURNS

DEFAULT_CONTRACT_PATH = Path("configs/q1_evaluation_contract.yaml")
DEFAULT_PANEL_PATH = Path("configs/models_q1_eval_panel.yaml")
VNEXT_DATASET_SHA = "523c881820710783b5290c76ea5fe5fc01a6341fb427defcba1119fc3e721518"
VNEXT_MODELS_YAML_SHA = "37174858710a087b3fe58c40e65c796418d1791ff4280bca08d96486b35d7ec3"
EPISODE_BUDGET_FORMULA = "n_attack * n_primary_targets * n_arms"


class Q1ContractError(Exception):
    pass


def load_q1_contract(path: str | Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def contract_sha256(path: str | Path = DEFAULT_CONTRACT_PATH) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def derived_primary_attack_episodes(contract: dict[str, Any]) -> int:
    ds = contract.get("dataset") or {}
    n_attack = int(ds.get("n_attack", 0))
    prim = contract.get("primary_targets") or {}
    n_targets = len(list(prim.get("config_keys", [])))
    n_arms = len(contract.get("arms") or {})
    return n_attack * n_targets * n_arms


def validate_q1_evaluation_contract(
    *,
    contract_path: str | Path = DEFAULT_CONTRACT_PATH,
    panel_path: str | Path = DEFAULT_PANEL_PATH,
    repo_root: str | Path = ".",
) -> dict[str, Any]:
    root = Path(repo_root)
    contract = load_q1_contract(contract_path)
    panel = yaml.safe_load(panel_path.read_text(encoding="utf-8"))
    models = panel.get("models") or {}

    ds = contract.get("dataset") or {}
    ds_path = root / str(ds.get("path", ""))
    if not ds_path.is_file():
        raise Q1ContractError(f"missing dataset: {ds_path}")
    actual_ds_sha = hashlib.sha256(ds_path.read_bytes()).hexdigest()
    expected_ds_sha = str(ds.get("sha256", ""))
    if actual_ds_sha != expected_ds_sha:
        raise Q1ContractError(f"dataset SHA mismatch: {actual_ds_sha} != {expected_ds_sha}")

    if int(ds.get("n_attack", 0)) != 61 or int(ds.get("n_benign", 0)) != 61:
        raise Q1ContractError("dataset N must be 61 attack + 61 benign")

    prim = contract.get("primary_targets") or {}
    if len(list(prim.get("config_keys", []))) != 4:
        raise Q1ContractError("primary_targets must list exactly 4 config keys")
    supp = contract.get("supplementary_targets") or {}
    if len(list(supp.get("config_keys", []))) != 2:
        raise Q1ContractError("supplementary_targets must list exactly 2 config keys")
    if supp.get("merge_with_primary_comparisons") is not False:
        raise Q1ContractError("supplementary must not merge with primary comparisons")

    arms = contract.get("arms") or {}
    if set(arms) != {"B0", "B1", "B2"}:
        raise Q1ContractError("arms must be exactly B0, B1, B2")
    b2 = arms.get("B2") or {}
    if int(b2.get("max_turns", 0)) != LIVE_WIRING_MAX_TURNS:
        raise Q1ContractError(f"B2 max_turns must match LIVE_WIRING_MAX_TURNS={LIVE_WIRING_MAX_TURNS}")

    peb = contract.get("primary_episode_budget") or {}
    if str(peb.get("formula")) != EPISODE_BUDGET_FORMULA:
        raise Q1ContractError(f"primary_episode_budget.formula must be {EPISODE_BUDGET_FORMULA!r}")
    derived_attack = derived_primary_attack_episodes(contract)
    declared_attack = peb.get("attack_episodes")
    if str(declared_attack) != "NEEDS_DECISION":
        if int(declared_attack) != derived_attack:
            raise Q1ContractError(
                f"attack_episodes {declared_attack} != derived {derived_attack} from formula"
            )

    budget = contract.get("budget") or {}
    cap = budget.get("hard_cap_usd")
    if str(cap) != "NEEDS_DECISION":
        try:
            cap_f = float(cap)
        except (TypeError, ValueError):
            raise Q1ContractError("hard_cap_usd must be NEEDS_DECISION or a positive number")
        if cap_f <= 0:
            raise Q1ContractError("hard_cap_usd must be positive when set")
    if budget.get("hard_stop") is not True:
        raise Q1ContractError("budget hard_stop must be true")

    binding = contract.get("legacy_binding_untouched") or {}
    models_yaml = root / "configs/models.yaml"
    if hashlib.sha256(models_yaml.read_bytes()).hexdigest() != VNEXT_MODELS_YAML_SHA:
        raise Q1ContractError("configs/models.yaml VNEXT binding SHA changed")

    for key in list(prim.get("config_keys", [])) + list(supp.get("config_keys", [])):
        if key not in models:
            raise Q1ContractError(f"panel missing key: {key}")

    judges = contract.get("judges") or {}
    if "J1_primary" not in judges or "J2_agreement" not in judges:
        raise Q1ContractError("judges J1 and J2 required")

    blocked = [
        k
        for k, spec in models.items()
        if str(spec.get("model", "")).startswith("NEEDS_DECISION")
        or str(spec.get("verification", "")) == "NEEDS_DECISION"
    ]

    needs = []
    if str(arms["B1"].get("defense_resolver_key")) == "NEEDS_DECISION":
        needs.append("arms.B1.static_defense_mapping")
    if str(arms["B2"].get("defense_resolver_key")) == "NEEDS_DECISION":
        needs.append("arms.B2.live_condition_id")
    if str(supp.get("subset", {}).get("path")) == "NEEDS_DECISION":
        needs.append("supplementary.frozen_subset")
    if str(peb.get("attack_episodes")) == "NEEDS_DECISION":
        needs.append("primary_episode_budget.attack_episodes")
    if str(cap) == "NEEDS_DECISION":
        needs.append("budget.hard_cap_usd")
    stats = contract.get("statistics") or {}
    if str(stats.get("multiple_comparison")) == "NEEDS_DECISION":
        needs.append("statistics.multiple_comparison")

    sheet = contract.get("q1_decision_sheet_v2") or {}
    d13 = sheet.get("j2_subset_d13") or {}
    manifest_rel = d13.get("manifest_path")
    if manifest_rel and str(manifest_rel) != "NEEDS_DECISION":
        manifest_path = root / str(manifest_rel)
        if not manifest_path.is_file():
            raise Q1ContractError(f"missing J2 subset manifest: {manifest_path}")
        expected_manifest_sha = str(d13.get("manifest_sha256", ""))
        actual_manifest_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        if expected_manifest_sha and actual_manifest_sha != expected_manifest_sha:
            raise Q1ContractError(
                f"J2 subset manifest SHA mismatch: {actual_manifest_sha} != {expected_manifest_sha}"
            )
        if int(d13.get("subset_pairs", 0)) != 49 or int(d13.get("j2_episodes", 0)) != 98:
            raise Q1ContractError("D13 J2 subset must be 49 pairs / 98 episodes")
    needs.extend(blocked)

    sci = contract.get("scientific_design") or {}
    execution_gate = str(sci.get("execution_gate", "BLOCKED"))

    return {
        "status": "valid_offline" if not needs else "valid_offline_with_blockers",
        "execution_gate": execution_gate,
        "contract_sha256": contract_sha256(contract_path),
        "dataset_sha256": actual_ds_sha,
        "models_yaml_sha256": VNEXT_MODELS_YAML_SHA,
        "panel_keys_pending_verification": blocked,
        "needs_decision": sorted(set(needs)),
        "derived_attack_episodes": derived_attack,
        "attack_episodes_declared": declared_attack,
        "episode_budget_formula": EPISODE_BUDGET_FORMULA,
        "budget_cap_usd": cap,
    }
