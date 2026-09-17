#!/usr/bin/env python3
"""Render Q2 Figures 3–5 offline without matplotlib (stdlib zlib PNG + numpy).

Read-only on frozen evidence / derived JSON. API/LLM/network = 0.
Does not write into datasets/frozen or experiments/real_llm_eval.
"""

from __future__ import annotations

import json
import math
import struct
import zlib
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PKG = Path(__file__).resolve().parent
STATS = PKG / "q2_final_statistics.json"
INVALID = PKG / "q2_invalid_args_analysis.json"
FIGDIR = PKG / "figures"
ART = Path("/opt/cursor/artifacts")

# 5x7 glyphs, bit rows (MSB left). Covers labels used on these figures.
_GLYPHS: dict[str, tuple[str, ...]] = {
    " ": ("00000",) * 7,
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "/": ("00001", "00010", "00100", "01000", "10000", "00000", "00000"),
    "(": ("00100", "01000", "10000", "10000", "10000", "01000", "00100"),
    ")": ("00100", "00010", "00001", "00001", "00001", "00010", "00100"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "%": ("11001", "11010", "00100", "01000", "10000", "01011", "10011"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11100", "10010", "10001", "10001", "10001", "10010", "11100"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01110"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    ">": ("00001", "00010", "00100", "01000", "00100", "00010", "00001"),
    "<": ("10000", "01000", "00100", "00010", "00100", "01000", "10000"),
    "*": ("00000", "00100", "10101", "01110", "10101", "00100", "00000"),
}


def _png(rgb: np.ndarray) -> bytes:
    h, w = rgb.shape[:2]
    raw = b"".join(b"\x00" + rgb[y].tobytes() for y in range(h))
    compressed = zlib.compress(raw, 9)

    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", compressed) + chunk(b"IEND", b"")


def _put(img: np.ndarray, x: int, y: int, w: int, h: int, color: tuple[int, int, int]) -> None:
    H, W = img.shape[:2]
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    if x1 > x0 and y1 > y0:
        img[y0:y1, x0:x1] = color


def _text(img: np.ndarray, s: str, x: int, y: int, scale: int, color: tuple[int, int, int]) -> None:
    cx = x
    for ch in s:
        glyph = _GLYPHS.get(ch, _GLYPHS.get(ch.upper(), _GLYPHS[" "]))
        for r, row in enumerate(glyph):
            for c, bit in enumerate(row):
                if bit == "1":
                    _put(img, cx + c * scale, y + r * scale, scale, scale, color)
        cx += 6 * scale


def _text_w(s: str, scale: int) -> int:
    return len(s) * 6 * scale


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Same binomial Wilson interval already used in q2_final_statistics.json. Not a new test."""
    if n <= 0:
        return (float("nan"), float("nan"))
    p = k / n
    z2 = z * z
    den = 1.0 + z2 / n
    centre = p + z2 / (2.0 * n)
    adj = z * math.sqrt(p * (1.0 - p) / n + z2 / (4.0 * n * n))
    return (centre - adj) / den, (centre + adj) / den


def fig3(stats: dict) -> np.ndarray:
    """Δ(d,t) Tool-HASR vs D0. No Δ CI (not pre-registered). Not a ranking."""
    W, H = 1600, 980
    img = np.full((H, W, 3), 255, dtype=np.uint8)
    ink = (25, 25, 25)
    _text(img, "Figure 3. Detector-related Tool-HASR Delta vs D0", 40, 28, 3, ink)
    _text(img, "Locked PHASE1-CORE. Pilot-scale. n=16/cell. scientific_evidence=false. Not a ranking.", 40, 62, 2, (70, 70, 70))
    _text(img, "Delta = Tool-HASR(d,t) - Tool-HASR(D0,t). Sign agreement 9/9. No Delta CI manufactured.", 40, 88, 2, (70, 70, 70))

    targets = ["T0", "T1", "T2", "T3"]
    dets = ["D1", "D2", "D4"]
    colors = {"D1": (0, 90, 140), "D2": (180, 110, 20), "D4": (35, 35, 35)}
    values = {}
    for t in targets:
        for d in dets:
            cell = f"{t}/{d}"
            d0 = stats["Tool-HASR_by_target_detector"][f"{t}/D0"]["rate"]
            dv = stats["Tool-HASR_by_target_detector"][cell]["rate"]
            values[(d, t)] = dv - d0

    left, right, top, bottom = 140, 1540, 150, 780
    ymin, ymax = -0.90, 0.10
    # axes
    _put(img, left, top, 2, bottom - top, ink)
    _put(img, left, bottom, right - left, 2, ink)
    y0 = int(bottom - (0 - ymin) / (ymax - ymin) * (bottom - top))
    _put(img, left, y0, right - left, 1, (160, 160, 160))
    for tick in (-0.75, -0.50, -0.25, 0.00):
        yy = int(bottom - (tick - ymin) / (ymax - ymin) * (bottom - top))
        _put(img, left - 8, yy, 8, 2, ink)
        lab = f"{tick:.2f}"
        _text(img, lab, left - 90, yy - 8, 2, ink)
    _text(img, "Delta", 24, 430, 2, ink)

    group_w = (right - left) / len(targets)
    bar_w = 70
    gap = 12
    for i, t in enumerate(targets):
        gx = left + int(i * group_w)
        cx = gx + int(group_w / 2)
        _text(img, t, cx - 18, bottom + 16, 3, ink)
        for j, d in enumerate(dets):
            v = values[(d, t)]
            bx = cx - (3 * bar_w + 2 * gap) // 2 + j * (bar_w + gap)
            yv = int(bottom - (v - ymin) / (ymax - ymin) * (bottom - top))
            if v <= 0:
                _put(img, bx, yv, bar_w, y0 - yv, colors[d])
                _put(img, bx, yv, bar_w, 2, (0, 0, 0))
            else:
                _put(img, bx, y0, bar_w, yv - y0, colors[d])
                _put(img, bx, yv, bar_w, 2, (0, 0, 0))
            lab = f"{v:.4f}"
            _text(img, lab, bx - 4, yv - 22 if v < 0 else yv + 6, 2, colors[d])

    # legend (identity coding, not rank)
    lx = 140
    ly = 840
    for d in dets:
        _put(img, lx, ly, 28, 18, colors[d])
        _text(img, d, lx + 36, ly, 2, ink)
        lx += 120
    _text(img, "Source: q2_final_statistics.json Tool-HASR cells. T0 reused from Stage-B report (traces MISSING locally).", 40, 890, 2, (80, 80, 80))
    _text(img, "Caption: controlled isolation contrast vs D0; not a detector leaderboard.", 40, 916, 2, (80, 80, 80))
    return img


def fig4(stats: dict) -> np.ndarray:
    """Tool-HASR vs Judge-ASR by target (pooled detectors, 64 attack arms). Wilson on rates only."""
    W, H = 1600, 1040
    img = np.full((H, W, 3), 255, dtype=np.uint8)
    ink = (25, 25, 25)
    _text(img, "Figure 4. Tool-HASR (primary) vs Judge-ASR (secondary)", 40, 28, 3, ink)
    _text(img, "Pooled across D0/D1/D2/D4 at each target. n=64 attack arms/target. scientific_evidence=false.", 40, 62, 2, (70, 70, 70))
    _text(img, "Wilson 95% CI on rates (same method as tables). Judge-ASR is diagnostic, not invalid. Not a ranking.", 40, 88, 2, (70, 70, 70))

    # cell sums from official per-cell n_success
    th = stats["Tool-HASR_by_target_detector"]
    ja = stats["Judge-ASR_by_target_detector"]
    m3m4 = {
        t: (stats["M3_M4_by_target"][t]["M3"], stats["M3_M4_by_target"][t]["M4"])
        for t in ("T0", "T1", "T2", "T3")
    }
    targets = ["T0", "T1", "T2", "T3"]
    dets = ["D0", "D1", "D2", "D4"]
    tool_col = (0, 90, 140)
    judge_col = (140, 70, 70)

    left, right, top, bottom = 140, 1100, 150, 780
    ymin, ymax = 0.0, 1.05
    _put(img, left, top, 2, bottom - top, ink)
    _put(img, left, bottom, right - left, 2, ink)
    for tick in (0.0, 0.25, 0.50, 0.75, 1.00):
        yy = int(bottom - (tick - ymin) / (ymax - ymin) * (bottom - top))
        _put(img, left - 8, yy, 8, 2, ink)
        _text(img, f"{tick:.2f}", left - 90, yy - 8, 2, ink)
    _text(img, "Rate", 24, 430, 2, ink)

    group_w = (right - left) / len(targets)
    bar_w = 70
    pooled = {}
    for i, t in enumerate(targets):
        k_t = sum(th[f"{t}/{d}"]["n_success"] for d in dets)
        k_j = sum(ja[f"{t}/{d}"]["n_success"] for d in dets)
        n = 64
        pooled[t] = (k_t, k_j, n)
        lo_t, hi_t = wilson(k_t, n)
        lo_j, hi_j = wilson(k_j, n)
        gx = left + int(i * group_w)
        cx = gx + int(group_w / 2)
        _text(img, t, cx - 18, bottom + 16, 3, ink)
        for j, (k, lo, hi, col) in enumerate(
            ((k_t, lo_t, hi_t, tool_col), (k_j, lo_j, hi_j, judge_col))
        ):
            rate = k / n
            bx = cx - bar_w - 8 + j * (bar_w + 16)
            yv = int(bottom - (rate - ymin) / (ymax - ymin) * (bottom - top))
            _put(img, bx, yv, bar_w, bottom - yv, col)
            ylo = int(bottom - (lo - ymin) / (ymax - ymin) * (bottom - top))
            yhi = int(bottom - (hi - ymin) / (ymax - ymin) * (bottom - top))
            mx = bx + bar_w // 2
            _put(img, mx, yhi, 2, ylo - yhi, ink)
            _put(img, mx - 8, yhi, 16, 2, ink)
            _put(img, mx - 8, ylo, 16, 2, ink)
            _text(img, f"{k}/{n}", bx - 8, yv - 22, 2, col)

    _put(img, 140, 840, 28, 18, tool_col)
    _text(img, "Tool-HASR primary", 176, 840, 2, ink)
    _put(img, 460, 840, 28, 18, judge_col)
    _text(img, "Judge-ASR secondary", 496, 840, 2, ink)
    _text(img, "Whiskers: Wilson 95% CI on the plotted rate. No p-values.", 140, 872, 2, (80, 80, 80))

    # M3/M4 panel
    _text(img, "M3 (J+ T-) and M4 (T+ J-)", 1160, 150, 2, ink)
    px0, py0 = 1160, 200
    pw, ph = 380, 560
    _put(img, px0, py0, 2, ph, ink)
    _put(img, px0, py0 + ph, pw, 2, ink)
    mmax = 45
    for i, t in enumerate(targets):
        m3, m4 = m3m4[t]
        cx = px0 + 50 + i * 90
        h3 = int(m3 / mmax * (ph - 40))
        h4 = int(m4 / mmax * (ph - 40))
        _put(img, cx, py0 + ph - h3, 28, h3, (90, 90, 90))
        _put(img, cx + 32, py0 + ph - max(h4, 2), 28, max(h4, 2), (180, 110, 20))
        _text(img, t, cx + 10, py0 + ph + 12, 2, ink)
        _text(img, str(m3), cx, py0 + ph - h3 - 18, 2, (90, 90, 90))
        _text(img, str(m4), cx + 32, py0 + ph - h4 - 18, 2, (180, 110, 20))
    _text(img, "M3 gray  M4 ochre", 1160, 800, 2, (80, 80, 80))
    _text(img, "T1-T3 M3=108 M4=3 (metrics.json)", 1160, 828, 2, (80, 80, 80))
    _text(img, "Source: q2_final_statistics.json cell n_success; M3/M4 from Table 4 / metrics.json.", 40, 920, 2, (80, 80, 80))
    _text(img, "Q2 live T1-T3 Tool-HASR 81/192; Judge-ASR 186/192.", 40, 946, 2, (80, 80, 80))
    _text(img, "Disagreement is diagnostic information. Endpoints are not interchangeable.", 40, 972, 2, (80, 80, 80))
    return img, pooled


def fig5(inv: dict) -> np.ndarray:
    W, H = 1500, 920
    img = np.full((H, W, 3), 255, dtype=np.uint8)
    ink = (25, 25, 25)
    _text(img, "Figure 5. INVALID_TOOL_ARGS diagnostic (S0 primary unchanged)", 40, 28, 3, ink)
    _text(img, "INVALID is not Tool-HASR success and is not negligible. S2 is sensitivity only.", 40, 62, 2, (70, 70, 70))
    _text(img, "Q2 live T1-T3: 192 unique events / 136 arms. T0 cited prior derived; traces MISSING locally.", 40, 88, 2, (70, 70, 70))

    rows = []
    for slot in ("T0", "T1", "T2", "T3"):
        b = inv["by_target"][slot]
        rows.append(
            (
                slot,
                b["invalid_event_count_dedup_per_arm"],
                b["n_arms_with_invalid"],
                slot == "T0",
            )
        )

    left, right, top, bottom = 160, 1420, 160, 720
    _put(img, left, top, 2, bottom - top, ink)
    _put(img, left, bottom, right - left, 2, ink)
    ymax = 220
    for tick in (0, 50, 100, 150, 200):
        yy = int(bottom - tick / ymax * (bottom - top))
        _put(img, left - 8, yy, 8, 2, ink)
        _text(img, str(tick), left - 70, yy - 8, 2, ink)

    group_w = (right - left) / 4
    bar_w = 70
    ev_col = (90, 90, 90)
    arm_col = (140, 90, 40)
    for i, (slot, ev, arms, t0) in enumerate(rows):
        cx = left + int(i * group_w + group_w / 2)
        he = int(ev / ymax * (bottom - top))
        ha = int(arms / ymax * (bottom - top))
        _put(img, cx - bar_w - 8, bottom - he, bar_w, he, ev_col)
        _put(img, cx + 8, bottom - ha, bar_w, ha, arm_col)
        _text(img, str(ev), cx - bar_w - 4, bottom - he - 22, 2, ev_col)
        _text(img, str(arms), cx + 8, bottom - ha - 22, 2, arm_col)
        lab = slot + ("*" if t0 else "")
        _text(img, lab, cx - 18, bottom + 18, 3, ink)

    _put(img, 160, 780, 28, 18, ev_col)
    _text(img, "Deduped INVALID events", 196, 780, 2, ink)
    _put(img, 560, 780, 28, 18, arm_col)
    _text(img, "Arms with 1+ INVALID", 596, 780, 2, ink)
    _text(img, "* T0 counts are official-prior-derived; Stage-B predictions.jsonl MISSING locally (not recomputed).", 40, 820, 2, (80, 80, 80))
    _text(img, "T1-T3 recomputed on Q2 predictions.jsonl: 192/136 match metrics.json. S2 sign agreement 9/9.", 40, 846, 2, (80, 80, 80))
    _text(img, "Do not drop INVALID from the S0 primary denominator. Source: q2_invalid_args_analysis.json.", 40, 872, 2, (80, 80, 80))
    return img


def main() -> int:
    stats = json.loads(STATS.read_text(encoding="utf-8"))
    inv = json.loads(INVALID.read_text(encoding="utf-8"))
    FIGDIR.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)

    p3 = _png(fig3(stats))
    p4_img, pooled = fig4(stats)
    p4 = _png(p4_img)
    p5 = _png(fig5(inv))

    files = {
        "figure3_delta_across_targets.png": p3,
        "figure4_toolhasr_vs_judgeasr.png": p4,
        "figure5_invalid_tool_args.png": p5,
    }
    meta = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "api_calls": 0,
        "llm_calls": 0,
        "network_calls": 0,
        "live_eval": False,
        "renderer": "stdlib_zlib_png_numpy",
        "matplotlib": False,
        "delta_ci_manufactured": False,
        "p_values_manufactured": False,
        "ranking": False,
        "source_stats": str(STATS.relative_to(ROOT)),
        "source_invalid": str(INVALID.relative_to(ROOT)),
        "caption_scope": "pilot-scale; n=16/cell; scientific_evidence=false; not a ranking",
        "figure3_values": {
            t: {
                d: stats["Tool-HASR_by_target_detector"][f"{t}/{d}"]["rate"]
                - stats["Tool-HASR_by_target_detector"][f"{t}/D0"]["rate"]
                for d in ("D1", "D2", "D4")
            }
            for t in ("T0", "T1", "T2", "T3")
        },
        "figure4_pooled_attack_n64": {
            t: {"tool_n": a, "judge_n": b, "N": n, "tool_wilson": wilson(a, n), "judge_wilson": wilson(b, n)}
            for t, (a, b, n) in pooled.items()
        },
        "figure5": {
            "T1T3_official": {"events": 192, "arms": 136},
            "T0_status": "prior_derived_StageB_traces_MISSING_locally",
        },
        "files": {},
    }
    for name, blob in files.items():
        dest = FIGDIR / name
        dest.write_bytes(blob)
        art = ART / f"q2_{name}"
        art.write_bytes(blob)
        meta["files"][name] = {"bytes": len(blob), "path": str(dest), "artifact": str(art)}
        print("wrote", dest, len(blob))

    (FIGDIR / "figure_metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    (ART / "q2_figure_metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
