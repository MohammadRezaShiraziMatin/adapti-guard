# FINAL Reproducibility

## REPRODUCIBILITY_STATUS = PARTIAL_WITH_EXPLICIT_PROVENANCE_LIMITATION

Full reproducibility is not claimed while Stage-B raw traces remain MISSING_LOCALLY.

## FROZEN (immutable, rechecked this pass)

- P1 SHA `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235` — match True
- P2 SHA `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd` — match True
- Q2 predictions SHA `2a2c2f314a9c397d570b743336bd3d835306620867c1d73936952bfb01886cc6` — match True
- Q2 evidence commit `b075df0f5ec5ad11ede76ac4e4079cade15208f1`
- Q2 run `p3_stage_c_q2_20260917T123855Z_b075df0f`
- Stage-B run pointer `p3_stage_b_20260916T235438Z_7e401714`
- Targets: T0/T1/T2/T3 locked; judge locked; detectors D0/D1/D2/D4 locked; policy PHASE1-CORE locked
- Temperature 0.0; cache false; seed 42; cost $0.152885; 432/432 arms

## DERIVED

- `q2_final_statistics.json`; Figures 3-5; Wilson 95% CIs on rates (derived from locked counts); INVALID recompute 192/136; S2 9/9.

## INTERPRETIVE

- Manuscript; claim matrix; novelty PARTIAL_GAP; attribution vs ranking scope.

## MISSING

- Stage-B `predictions.jsonl` — MISSING_LOCALLY (0 git object hits; not reconstructed)
- matplotlib — MISSING (stdlib PNG used)
- Q2 p-values — MISSING (not preregistered; not manufactured)

Detailed: `Q2_REPRODUCIBILITY_CHECKLIST.md`, `Q2_REPRODUCIBILITY_AUDIT.md`.
