# Frozen Evaluation Datasets

**Status:** `FREEZE` for `eval_v1`; `layer_a_v2` is historical; `layer_a_v3` is the closed Layer A mixed PI pack; `vnext_confirm_v1` is the VNEXT confirmation pack; `p1_mechanism_v1.0.0` is the P1 mechanism pilot; `p2_agentic_v0.1.0` is the P2 agentic trajectory pilot.

- `eval_v1/` — original 770-row attack-only set (unchanged)
- `layer_a_v2/` — historical 40 PI + 40 benign Layer A pack (do not modify)
- `layer_a_v3/` — 80 PI + 80 benign with train/dev/test (`DATASET_CARD.md`; do not modify)
- `vnext_confirm_v1/` — VNEXT confirmation 61 attack + 61 benign (`DATASET_CARD.md`; SHA-256 in `docs/experiments/VNEXT_PROTOCOL_ADDENDUM.md` §4)
- `p1_mechanism_v1.0.0/` — P1 mechanism pack (FROZEN; `live_evaluated=false`)
- `p2_agentic_v0.1.0/` — P2 agentic pack (FROZEN; SHA-256 `32b40e3b…8d64dd`; `live_evaluated=false`; freeze note `docs/research/P2_AGENTIC_V0_1_0_FREEZE.md`)
