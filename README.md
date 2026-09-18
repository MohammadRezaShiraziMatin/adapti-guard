# ADAPTI-GUARD

**Controlled runtime intervention and detector attribution for prompt injection in LLM agents.**

ADAPTI-GUARD is a research testbed for studying how **detector behavior and downstream runtime intervention policy** jointly affect the security, utility, and cost of LLM agents. The project uses hash-locked evaluation packs, controlled detector variants, discrete intervention policies, and explicit security/utility/cost metrics.

> **Research status:** pilot-scale empirical evaluation. The repository documents both positive and negative findings, including cases where a defense effect is not supported. Results are reported with their scope and limitations; no claim of SOTA, universal protection, or production readiness is made.

[![Tests](https://github.com/Mohammadreza583/adapti-guard/actions/workflows/tests.yml/badge.svg)](https://github.com/Mohammadreza583/adapti-guard/actions/workflows/tests.yml)

## Research question

**How much of observed LLM-agent security behavior is attributable to the detector itself, versus the downstream intervention policy?**

The controlled evaluation keeps the trajectory, target/judge setup, tool environment, policy configuration, and evaluation protocol fixed while varying the detector. This makes detector-related effects easier to separate from effects introduced by the intervention policy.

## What the project evaluates

At runtime, the pipeline follows the general sequence:

`Agent input → Detector → Risk signal → Intervention policy → Tool/action`

| Action | Meaning |
| --- | --- |
| **A0** | Allow / no intervention |
| **A1** | Sanitize input |
| **A2** | Restrict tool access |
| **A3** | Block the action |

The project is therefore not only a detector benchmark and not only a defense benchmark. It is a **controlled framework for attribution** between detection and downstream intervention.

## Evaluation design

### P1 — Mechanism benchmark

A frozen mechanism-level benchmark provides controlled examples for prompt-injection and related LLM-agent attack mechanisms.

- Version: `p1_mechanism_v1.0.0`
- 44 attacks
- 44 benign twins
- 8 hard negatives
- 22 mechanisms × 2 examples
- Frozen SHA-256: `1a0b0053c392e7b3e0727b92b4f088790abda001fd852ec1703c5ee0a67dd235`

P1 is a **frozen pilot benchmark**, not a claim of comprehensive attack coverage.

### P2 — Agentic benchmark

P2 extends evaluation to agent trajectories rather than isolated prompts.

It covers six documented behavior families:

- persistence
- delayed execution
- tool-output injection
- chaining
- memory
- adaptive behavior

Frozen benchmark:

- Version: `p2_agentic_v0.1.0`
- 16 attack trajectories
- 16 benign twins
- 4 hard negatives
- Frozen SHA-256: `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd`

This should be read as **agentic attack coverage for the evaluated families**, not as a comprehensive multi-turn benchmark.

### P3 — Detector attribution

P3 is the main controlled attribution experiment.

Detector variants are evaluated under a common downstream pipeline:

- **D0:** no detection
- **D1:** current PHASE1 detector wrapper
- **D2:** transparent heuristic detector
- **D4:** structured/context detector
- **D3:** semantic embedding detector — deferred

The detector interface is intentionally separated from intervention policy. A detector does not execute tools, call the judge/LLM, access future turns, mutate policy, or modify the benchmark.

## Security metrics

Two security measures are kept distinct:

- **Tool-HASR:** whether the harmful tool action actually occurred.
- **Judge-ASR:** whether the independent judge classified the trajectory as a successful attack.

They can disagree. The repository preserves **M3/M4 disagreement diagnostics** rather than silently treating one metric as a substitute for the other.

Other reported quantities include:

- attack detection rate
- benign false-positive rate
- hard-negative false-positive rate
- intervention rate
- benign utility
- mean intervention cost
- invalid tool-argument diagnostics

## Main empirical package

### Stage-B: locked-target detector attribution

The full Stage-B design evaluated 432 detector × policy × trajectory arms.

Recorded aggregate results:

- Tool-HASR: **124/192 = 0.6458**
- Judge-ASR: **163/192 = 0.8490**
- M3: **61**
- M4: **22**
- invalid tool-argument events: **231** after event-ID deduplication
- Run ID: `p3_stage_b_20260916T235438Z_7e401714`

**Evidence status:** the original Stage-B raw evidence is currently **not recoverable from the accessible repository/storage**. The recorded result is therefore preserved as a provenance pointer and is not presented as independently reproducible raw evidence. The project does not fabricate or silently rerun the historical run to replace missing evidence.

### Q2: secondary-target consistency

Q2 tested whether the direction of detector-related effects observed under the locked target remained consistent across independently selected secondary targets.

- 432/432 arms completed
- Targets: `qwen/qwen3-30b-a3b`, `google/gemma-3-27b-it`, `qwen/qwen3.5-35b-a3b`
- Judge: `qwen/qwen-2.5-72b-instruct`
- API calls: 2,061
- Recorded cost: **$0.152885**
- Judge-ASR across secondary targets: **186/192 = 0.96875**
- M3: **108**
- M4: **3**
- invalid-argument count: **192**

Across the evaluated detector/target combinations, the observed Tool-HASR effect had the same direction as the locked-target result in all 9 comparisons.

This is a **pilot-scale directional-consistency finding**, not a claim of model independence or universal generalization.

## Historical confirmatory tracks

The repository also contains an earlier dual-track evaluation package. It remains important for scientific provenance but should not be confused with the current detector-attribution question.

| Track | Result | Interpretation |
| --- | --- | --- |
| **Track A — VNEXT** | δ̂ = **0.0820**, p = **0.0625**, U = **0.9344**, b10/b01 = **5/0** | **FAIL** under the registered criterion |
| **Track B — Phase-1 CORE** | δ̂ = **0.4426**, 95% CI **[0.2757, 0.6096]**, p = **1.49012e-08**, U = **0.9672**, b10/b01 = **27/0** | **SUPPORTED_IMPROVEMENT** on a different pack |

Track B does **not** reverse Track A. The two tracks use different evaluation packs and are not to be pooled into a single unlabeled effect estimate.

Historical sources:

- [Track A audit](experiments/real_llm_eval/VNEXT_CONFIRM/20260914-133147/AUDIT.md)
- [Track B audit](experiments/real_llm_eval/PHASE1_CONFIRM/phase1_confirm_20260914T213022Z_a2681e92/AUDIT.md)

## Reproducibility

### Offline

```bash
git clone https://github.com/Mohammadreza583/adapti-guard.git
cd adapti-guard
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
pytest -q
```

The offline test suite is the default entry point and does not require live LLM access.

Scientific audit scripts:

```bash
python scripts/audit_phase1_confirm_independence.py
python scripts/audit_phase1_holdout_overlap_origin.py
python scripts/classify_phase1_holdout_pairs_full59.py
```

Manuscript fact checking:

```bash
python docs/paper/workshop_vnext_fail/verify_manuscript_facts.py
```

### Live evaluation

Live LLM evaluation is intentionally gated. Frozen datasets and historical AUDIT evidence are treated as read-only.

**Do not run confirmation evaluations or consume API budget unless a human explicitly approves the live run.**

Never commit `.env`, provider credentials, or API keys.

## Limitations

1. **Pilot scale:** the agentic benchmark uses 16 attack trajectories and 16 benign twins.
2. **Invalid tool arguments:** invalid-argument events are frequent enough to require explicit diagnostic reporting.
3. **Model diversity:** the evaluated target set is still limited and includes multiple Qwen-family targets.
4. **Deferred detector:** D3 was not executed in the reported P3 package.
5. **Agentic scope:** C4-style long-horizon memory behavior remains out of scope.
6. **Evidence provenance:** the original Stage-B raw traces are missing from currently accessible storage.
7. **External baselines:** the package is not a head-to-head comparison against a broad set of external defenses.
8. **Generalization:** Q2 provides pilot-scale directional consistency, not model-independent or universal guarantees.

These limitations are part of the result package, not omitted from it.

## What this project is not

ADAPTI-GUARD does **not** claim to:

- solve prompt injection in general;
- provide universal or model-independent protection;
- be SOTA or the best available defense;
- be production-ready;
- provide comprehensive coverage of all agentic attacks;
- establish that one detector is universally superior to another.

The purpose is narrower: **controlled empirical attribution of detector-related effects within a runtime intervention framework.**

## Repository structure

| Path | Role |
| --- | --- |
| `src/adapti_guard/` | Installable package |
| `configs/` | YAML/JSON configuration |
| `scripts/` | CLI and audit entrypoints |
| `tests/` | Pytest suite |
| `datasets/frozen/` | Frozen evaluation packs — **do not edit** |
| `experiments/real_llm_eval/` | Live evaluation AUDIT/evidence |
| `docs/paper/` | Scientific reports, claims, and manuscript material |
| `docs/archive/` | Superseded and historical material |
| `CITATION.cff` | Citation metadata |

## Citation

See [`CITATION.cff`](CITATION.cff).

```bibtex
@software{adapti_guard,
  author = {Shirazi Matin, Seyed Mohammadreza},
  title  = {AdaptiGuard: A Hash-Locked Evaluation Testbed for Runtime LLM-Agent Intervention Policies},
  year   = {2026},
  url    = {https://github.com/Mohammadreza583/adapti-guard},
  note   = {Controlled detector-attribution evaluation; pilot-scale empirical results with documented limitations}
}
```

## License

Released under the MIT License. See [`LICENSE`](LICENSE).