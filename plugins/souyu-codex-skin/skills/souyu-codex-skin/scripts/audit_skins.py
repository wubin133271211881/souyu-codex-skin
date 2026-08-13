#!/usr/bin/env python3
"""Audit all registered skins for palette completeness and balance."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKINS = ROOT / "skins"
REQUIRED = {
    "bodyBg", "bodyGlowA", "bodyGlowB", "asideA", "asideB", "border",
    "topA", "topB", "mainA", "mainB", "mainC", "mainD", "headerBg",
    "activeBg", "cardBg", "cardBg2", "inputBg", "topFade", "composerFade",
    "menuBg", "moduleBg", "buttonBg", "terminalBg", "terminalInk",
}


def lum(hex_or_rgba: str) -> float:
    s = hex_or_rgba.strip()
    if s.startswith("#"):
        h = s.lstrip("#")
        rgb = tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    else:
        nums = [float(x) for x in s[s.index("(") + 1 : s.index(")")].split(",")[:3]]
        rgb = tuple(n / 255 for n in nums)
    r, g, b = rgb
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def main() -> None:
    problems = []
    for folder in sorted(SKINS.iterdir()):
        mf = folder / "skin.json"
        if not mf.is_file():
            continue
        m = json.loads(mf.read_text(encoding="utf-8"))
        for variant in ("dark", "light"):
            p = m["palette"].get(variant)
            if not p:
                problems.append(f"{folder.name}/{variant}: palette missing")
                continue
            missing = REQUIRED - set(p)
            if missing:
                problems.append(f"{folder.name}/{variant}: missing {sorted(missing)}")
                continue
            tb = p["terminalBg"]
            ti = p["terminalInk"]
            tl, tl_ink = lum(tb), lum(ti)
            if variant == "light" and tl < 0.5:
                problems.append(f"{folder.name}/light: terminalBg too dark ({tb})")
            if variant == "dark" and tl > 0.25:
                problems.append(f"{folder.name}/dark: terminalBg too light ({tb})")
            if abs(tl - tl_ink) < 0.25:
                problems.append(f"{folder.name}/{variant}: terminal contrast low ({tb} vs {ti})")
            print(
                f"{folder.name:<24} {variant:<6} surf={p['bodyBg']:<8} "
                f"menu={p['menuBg'][:28]:<30} termBgLum={tl:.2f} inkLum={tl_ink:.2f}"
            )
    print()
    if problems:
        print("ISSUES:")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    print("All skins OK")


if __name__ == "__main__":
    main()
