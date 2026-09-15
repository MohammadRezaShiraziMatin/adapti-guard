# P2 Agentic Candidate Pack v0

**Status:** CANDIDATE · NOT FROZEN · NOT scientific evidence  
**Pack ID:** `p2_agentic_v0-candidate`  
**SHA-256 (dataset.jsonl):** `32b40e3bd3ffe6ce4f82b8b3cb863fe2df26f74a7bb8a49f2b00e2f9738d64dd`  
**Size:** 16 attack + 16 benign twins + 4 hard negatives = 36 trajectories  

## Purpose

Pilot / failure-localization trajectory pack for offline P2.2 harness validation.
Trajectory-level multi-turn attacks (not longer single prompts).

## Files

- `dataset.jsonl` — trajectories
- `manifest.json` — pack metadata
- `schema.json` — trajectory JSON schema
- `coverage.json` — dynamics/mechanism coverage matrix
- `hashes.sha256` — content lock for candidate (not a freeze)

## Safety

- Authored offline; no LLM/API generation
- Does not modify `datasets/frozen/p1_mechanism_v1.0.0/`
- Does not modify historical L1 artifacts
- `live_evaluated=false`, `scientific_evidence=false`

## Rebuild

```bash
python3 scripts/build_p2_agentic_v0_pack.py
python3 scripts/validate_p2_agentic_pack.py
```
