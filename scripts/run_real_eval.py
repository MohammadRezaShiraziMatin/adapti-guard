#!/usr/bin/env python3
"""Legacy/generic convenience entry for real LLM evaluation.

Delegates to experiments/REAL_LLM_EVAL/run.py.

Not the locked Track A/B confirm runner and not a dedicated P1 L1 AUDIT runner.
Canonical L1 keys (when a gated L1 runner exists): target_2 + judge_fallback
+ OpenRouter + policies B0/STATIC-A1/PHASE1-CORE on frozen p1_mechanism_v1.0.0.
See docs/research/L1_CANONICAL_CONFIG.md.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if __name__ == "__main__":
    runpy.run_path(str(ROOT / "experiments" / "REAL_LLM_EVAL" / "run.py"), run_name="__main__")
