"""MT2 confirmatory target/judge panel — offline config validation only."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from adapti_guard.evaluation.live_model_resolver import TargetJudgeGuardError, model_id_for_config_key
from adapti_guard.evaluation.target_model import load_model_config

DEFAULT_MODELS_PATH = Path("configs/models.yaml")
DEFAULT_PANEL_PATH = Path("configs/mt2_panel.yaml")

MT2_TARGET_KEY_PREFIX = "mt2_target_"


class MT2PanelConfigError(Exception):
    """Invalid MT2 panel contract."""


def load_mt2_panel_contract(path: str | Path = DEFAULT_PANEL_PATH) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _vendor_family_for_key(config_key: str, models: dict[str, Any]) -> str:
    spec = models.get(config_key) or {}
    family = spec.get("vendor_family")
    if family:
        return str(family)
    model_id = str(spec.get("model", ""))
    if model_id.startswith("qwen/"):
        return "qwen"
    if model_id.startswith("google/"):
        return "google"
    if model_id.startswith("mistralai/"):
        return "mistral"
    if model_id.startswith("meta-llama/"):
        return "meta-llama"
    if model_id.startswith("openai/"):
        return "openai"
    if model_id.startswith("anthropic/"):
        return "anthropic"
    if model_id.startswith("deepseek/"):
        return "deepseek"
    if model_id.startswith("amazon/"):
        return "amazon"
    raise MT2PanelConfigError(f"cannot infer vendor_family for {config_key}")


def resolve_mt2_judges_for_target(
    target_config_key: str,
    *,
    models_path: str | Path = DEFAULT_MODELS_PATH,
    panel_path: str | Path = DEFAULT_PANEL_PATH,
) -> dict[str, str]:
    """Per-episode judge keys: primary/secondary config keys for a target."""
    contract = load_mt2_panel_contract(panel_path)
    target_keys = list(contract.get("target_panel", {}).get("keys", []))
    if target_config_key not in target_keys:
        raise MT2PanelConfigError(f"{target_config_key} not in MT2 target panel")

    override = contract.get("judge_panel", {}).get("when_target_vendor_conflicts_with_primary", {})
    if target_config_key in list(override.get("applies_to_target_config_keys", [])):
        return {
            "primary_config_key": str(override["primary_config_key"]),
            "secondary_config_key": str(override["secondary_config_key"]),
            "rule": "openai_target_vendor_substitute",
        }

    default = contract.get("judge_panel", {}).get("default", {})
    return {
        "primary_config_key": str(default["primary_config_key"]),
        "secondary_config_key": str(default["secondary_config_key"]),
        "rule": "default",
    }


def validate_mt2_panel(
    *,
    models_path: str | Path = DEFAULT_MODELS_PATH,
    panel_path: str | Path = DEFAULT_PANEL_PATH,
) -> dict[str, Any]:
    """Validate MT2 panel: six targets, OpenRouter ids, judge independence."""
    cfg = load_model_config(models_path)
    models = cfg.get("models", {})
    contract = load_mt2_panel_contract(panel_path)
    target_keys = list(contract.get("target_panel", {}).get("keys", []))
    if len(target_keys) != 6:
        raise MT2PanelConfigError(f"expected 6 MT2 targets, got {len(target_keys)}")

    verification = contract.get("openrouter_verification", {}).get("models", {})
    target_families: set[str] = set()
    target_report: list[dict[str, Any]] = []

    for key in target_keys:
        if key not in models:
            raise MT2PanelConfigError(f"missing models.yaml entry: {key}")
        model_id = model_id_for_config_key(key, models_path)
        if model_id not in verification or not verification[model_id].get("listed"):
            raise MT2PanelConfigError(f"target {key} model {model_id} not listed in panel verification")
        family = _vendor_family_for_key(key, models)
        target_families.add(family)
        target_report.append({"config_key": key, "model_id": model_id, "vendor_family": family})

    if len(target_families) != 6:
        raise MT2PanelConfigError("MT2 targets must span six distinct vendor families")

    judge_checks: list[dict[str, Any]] = []
    for target_key in target_keys:
        judges = resolve_mt2_judges_for_target(target_key, models_path=models_path, panel_path=panel_path)
        t_family = _vendor_family_for_key(target_key, models)
        t_id = model_id_for_config_key(target_key, models_path)
        for role in ("primary_config_key", "secondary_config_key"):
            j_key = judges[role]
            if j_key not in models:
                raise MT2PanelConfigError(f"missing judge key {j_key}")
            j_id = model_id_for_config_key(j_key, models_path)
            if j_id not in verification or not verification[j_id].get("listed"):
                raise MT2PanelConfigError(f"judge {j_key} model {j_id} not in OpenRouter verification block")
            j_family = _vendor_family_for_key(j_key, models)
            if j_family == t_family:
                raise MT2PanelConfigError(
                    f"target {target_key} ({t_family}) shares vendor with judge {j_key} ({j_family})"
                )
            if j_id == t_id:
                raise TargetJudgeGuardError("configuration_failure: target_model_id == judge_model_id")
        p_id = model_id_for_config_key(judges["primary_config_key"], models_path)
        s_id = model_id_for_config_key(judges["secondary_config_key"], models_path)
        if p_id == s_id:
            raise MT2PanelConfigError(f"primary and secondary judge identical for target {target_key}")
        p_fam = _vendor_family_for_key(judges["primary_config_key"], models)
        s_fam = _vendor_family_for_key(judges["secondary_config_key"], models)
        if p_fam == s_fam:
            raise MT2PanelConfigError(f"primary/secondary judges share vendor for target {target_key}")
        judge_checks.append({**judges, "target_config_key": target_key})

    mt2_section = cfg.get("mt2_panel") or {}
    if list(mt2_section.get("target_keys", [])) != target_keys:
        raise MT2PanelConfigError("models.yaml mt2_panel.target_keys out of sync with mt2_panel.yaml")

    return {
        "status": "valid",
        "n_targets": 6,
        "targets": target_report,
        "judge_resolution": judge_checks,
    }
