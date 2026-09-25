# Q1 Evaluation Protocol (canonical contract)

**Binding file:** `configs/q1_evaluation_contract.yaml`  
**Model panel (additive):** `configs/models_q1_eval_panel.yaml`  
**Offline check:** `validate_q1_evaluation_contract()` · `tests/test_q1_evaluation_contract.py`

Does **not** replace VNEXT `target_2`/`judge_fallback` binding in `configs/models.yaml` (SHA `37174858…`).  
Dataset: `vnext_confirm_v1` (61+61, SHA `523c8818…`). Primary attack matrix: **732** episodes (61×4×3). Budget hard cap **$3.00** via `BudgetLedger`.

Items marked `NEEDS_DECISION` in YAML require owner lock before live authorization.

Scientific design audit: `docs/Q1_SCIENTIFIC_COMPLETENESS_AUDIT.md`. Owner decisions: `docs/Q1_OWNER_DECISION_PACK.md`.
