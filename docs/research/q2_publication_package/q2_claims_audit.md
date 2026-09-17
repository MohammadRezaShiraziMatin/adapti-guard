# Q2 Claims Audit

GREEN=supported · YELLOW=qualify · RED=remove/rewrite

| ID | Claim | Status | Safe | Unsafe |
| --- | --- | --- | --- | --- |
| A1 | Detector-related Tool-HASR effect vs D0 is NEG under PHASE1-CORE on T0 | **GREEN** | On locked T0/PHASE1-CORE, Δ(D1/D2/D4) are negative (pilot n=16). | Detectors guarantee security. |
| A2 | Δ sign remains consistent on T1–T3 (9/9) | **GREEN** | Directional consistency across evaluated targets T0–T3. | Generalizes to all LLMs / universally robust. |
| A3 | Protocol isolates detector from policy | **GREEN** | Experimental isolation under fixed policy stratum. | Full causal identification in production. |
| A4 | Tool-HASR and Judge-ASR measure different endpoints | **GREEN** | Large M3 mass shows divergence; Tool-HASR is execution-grounded primary. | Judge-ASR is invalid. |
| A5 | INVALID does not overturn primary Δ signs | **GREEN** | Under locked S0/S2, signs stable; INVALID must still be reported. | INVALID is negligible. |
| A6 | ADAPTI-GUARD is production-ready / SOTA | **RED** | (remove) | production-ready / SOTA / best detector |
| A7 | Results prove robust generalization | **RED** | Bounded directional consistency on 4 models / P2 pack. | proves robust / significantly generalizes |
| A8 | Cost-aware defense with real USD intervention costs | **RED** | Normalized experimental action weights; token-USD separate. | cost-optimal / scalable economic defense |
| A9 | D1 superior to D2/D4 | **RED** | Report Δ vs D0 without ranking. | best / superior detector |
| A10 | Adaptive attacker (C4) handled | **RED** | Out of scope / not established. | robust to adaptive attacks |
| A11 | Q2 scientific_evidence confirmatory | **YELLOW** | Protocol-complete pilot consistency study; scientific_evidence=false retained. | confirmatory multi-model proof |
| A12 | Novelty of detector-policy isolation + Tool-HASR protocol | **YELLOW** | Defensible integration/protocol contribution pending verified related work. | first/only breakthrough |

## Banned stems unless carefully redefined
`proves`, `guarantees`, `robust`, `generalizes` (unbounded), `best`, `superior`, `state-of-the-art`, `significantly`, `causal` (unqualified), `scalable`, `production-ready`.
