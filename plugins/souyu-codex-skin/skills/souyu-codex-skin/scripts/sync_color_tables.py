#!/usr/bin/env python3
"""Sync the editable color table (colors.json/colors.md) for every skin.

Every registered skin should ship a color table so the full 24-key palette is
visible and editable per skin. Skins imported before the color-table feature
get colors.json built from their skin.json palette (native core derived from
accent/bodyBg/terminalInk; semantic colors use the variant defaults). Skins
that already have colors.json only get missing panel keys merged in and their
colors.md refreshed, so manual edits are never clobbered.

Usage:
  python sync_color_tables.py --all
  python sync_color_tables.py --id <skin-id>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
SKINS = ROOT / "skins"
sys.path.insert(0, str(SCRIPTS))

import build_theme  # noqa: E402
import create_skin  # noqa: E402

SEMANTIC_DEFAULTS = {
    "light": {"diffAdded": "#1f8a4c", "diffRemoved": "#d13438", "skill": "#b7791f"},
    "dark": {"diffAdded": "#3fb950", "diffRemoved": "#f85149", "skill": "#d29922"},
}


def build_colors(skin_dir: Path, manifest: dict) -> dict:
    colors = {"id": manifest["id"], "label": manifest["label"], "variants": {}}
    for variant in ("light", "dark"):
        p = manifest["palette"][variant]
        surface = build_theme.parse_hex(p.get("bodyBg", "#111111"))
        ink = build_theme.parse_hex(p.get("terminalInk", "#222222"))
        ratio = build_theme.contrast_ratio(ink, surface)
        contrast = max(0, min(100, round((ratio - 1.0) / 20.0 * 100)))
        colors["variants"][variant] = {
            "accent": p.get("accent", p.get("terminalInk")),
            "surface": p.get("bodyBg"),
            "ink": p.get("terminalInk"),
            "contrast": contrast,
            "semanticColors": dict(SEMANTIC_DEFAULTS[variant]),
            "panel": dict(p),
        }
    return colors


def sync(skin_dir: Path) -> str:
    manifest_path = skin_dir / "skin.json"
    if not manifest_path.is_file():
        return f"skip {skin_dir.name}: no skin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    colors_file = skin_dir / "colors.json"
    if colors_file.is_file():
        colors = json.loads(colors_file.read_text(encoding="utf-8"))
        changed = False
        for variant in ("light", "dark"):
            panel = colors.setdefault("variants", {}).setdefault(variant, {}).setdefault("panel", {})
            for key, value in manifest["palette"][variant].items():
                if key not in panel:
                    panel[key] = value
                    changed = True
        if changed:
            colors_file.write_text(json.dumps(colors, ensure_ascii=False, indent=2), encoding="utf-8")
        (skin_dir / "colors.md").write_text(create_skin.render_colors_md(colors), encoding="utf-8")
        return f"refreshed {skin_dir.name} (panel keys merged: {changed})"
    colors = build_colors(skin_dir, manifest)
    colors_file.write_text(json.dumps(colors, ensure_ascii=False, indent=2), encoding="utf-8")
    (skin_dir / "colors.md").write_text(create_skin.render_colors_md(colors), encoding="utf-8")
    return f"created {skin_dir.name}"


def main() -> None:
    ap = argparse.ArgumentParser(description="Sync color tables for registered skins")
    ap.add_argument("--all", action="store_true", help="Sync every registered skin")
    ap.add_argument("--id", default=None, help="Sync one skin by id")
    args = ap.parse_args()
    if args.id:
        results = [sync(SKINS / args.id)]
    elif args.all:
        results = [sync(d) for d in sorted(SKINS.iterdir()) if d.is_dir()]
    else:
        sys.exit("pass --all or --id <skin-id>")
    print("\n".join(results))


if __name__ == "__main__":
    main()
