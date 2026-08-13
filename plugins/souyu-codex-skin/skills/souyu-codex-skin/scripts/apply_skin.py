#!/usr/bin/env python3
"""Apply a registered skin from its color table + images.

A skin is defined by:
  skins/<id>/colors.json   editable color table (native + 24-key panel, light/dark)
  skins/<id>/light.jpg     light wallpaper
  skins/<id>/dark.jpg      dark wallpaper

After editing colors.json or swapping the images, run this script to push the
whole skin live:

  python apply_skin.py --id <id>            # apply
  python apply_skin.py --id <id> --dry-run  # preview only

It syncs colors.json -> skin.json palette, re-renders style.css, copies the
wallpapers to the injector assets, updates the runtime state, regenerates the
native theme packs (Settings > Appearance > Import strings) and refreshes the
human-readable colors.md view.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
SKINS = ROOT / "skins"
sys.path.insert(0, str(SCRIPTS))

import create_skin  # noqa: E402
import switch_skin  # noqa: E402

FONT_UI = "Inter, system-ui, sans-serif"
FONT_CODE = "JetBrains Mono, SF Mono, Menlo, monospace"


def load_colors(skin_dir: Path) -> dict:
    colors_file = skin_dir / "colors.json"
    if not colors_file.is_file():
        sys.exit(f"color table missing: {colors_file} (run create_skin.py first)")
    return json.loads(colors_file.read_text(encoding="utf-8"))


def synced_manifest(skin_dir: Path, colors: dict) -> dict:
    manifest_path = skin_dir / "skin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for variant in ("light", "dark"):
        panel = colors.get("variants", {}).get(variant, {}).get("panel")
        if panel:
            manifest["palette"][variant] = panel
    if colors.get("label"):
        manifest["label"] = colors["label"]
    if colors.get("id"):
        manifest["id"] = colors["id"]
    return manifest


def derived_from_colors(colors: dict, manifest: dict) -> dict:
    """Rebuild the derived-theme view used to refresh colors.md."""
    derived = {}
    for variant in ("light", "dark"):
        c = colors.get("variants", {}).get(variant, {})
        panel = c.get("panel", manifest["palette"][variant])
        derived[variant] = {
            "accent": create_skin.build_theme.parse_hex(c.get("accent", panel.get("accent", "#888888"))),
            "surface": create_skin.build_theme.parse_hex(c.get("surface", panel.get("bodyBg", "#111111"))),
            "ink": create_skin.build_theme.parse_hex(c.get("ink", panel.get("terminalInk", "#222222"))),
            "contrast": c.get("contrast", 60),
            "semantic": c.get(
                "semanticColors",
                {"diffAdded": "#3fb950", "diffRemoved": "#f85149", "skill": "#d29922"},
            ),
        }
    return derived


def native_theme(skin_id: str, variant: str, c: dict) -> dict:
    panel = c.get("panel", {})
    return {
        "codeThemeId": create_skin.build_theme.slugify(skin_id),
        "theme": {
            "accent": c.get("accent", panel.get("accent", "#888888")),
            "contrast": c.get("contrast", 60),
            "fonts": {"ui": FONT_UI, "code": FONT_CODE},
            "ink": c.get("ink", panel.get("terminalInk", "#222222")),
            "opaqueWindows": True,
            "semanticColors": c.get(
                "semanticColors",
                {"diffAdded": "#3fb950", "diffRemoved": "#f85149", "skill": "#d29922"},
            ),
            "surface": c.get("surface", panel.get("bodyBg", "#111111")),
        },
        "variant": variant,
    }


def regen_native_packs(skin_dir: Path, colors: dict, skin_id: str) -> list[Path]:
    out = ROOT / "outputs" / skin_id
    written = []
    for variant in ("light", "dark"):
        c = colors.get("variants", {}).get(variant)
        if not c:
            continue
        pack = out / variant
        pack.mkdir(parents=True, exist_ok=True)
        art = skin_dir / f"{variant}.jpg"
        if art.is_file():
            shutil.copy2(art, pack / "background.png")
        theme = native_theme(skin_id, variant, c)
        (pack / "theme.json").write_text(
            json.dumps(theme, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        import_str = "codex-theme-v1:" + json.dumps(theme, separators=(",", ":"), ensure_ascii=False)
        (pack / "codex-theme-v1.txt").write_text(import_str, encoding="utf-8")
        written.append(pack / "codex-theme-v1.txt")
    return written


def main() -> None:
    ap = argparse.ArgumentParser(description="Apply a skin from its color table + images")
    ap.add_argument("--id", required=True, help="Registered skin id")
    ap.add_argument("--dry-run", action="store_true", help="Preview what would be applied")
    args = ap.parse_args()

    skin_dir = SKINS / args.id
    if not (skin_dir / "skin.json").is_file():
        sys.exit(f"skin not registered: {skin_dir}")

    colors = load_colors(skin_dir)
    manifest = synced_manifest(skin_dir, colors)
    p = manifest["palette"]
    if args.dry_run:
        print(f"[dry-run] would apply {args.id} ({manifest['label']}):")
        print(
            f"  light: accent={p['light']['accent']} bodyBg={p['light']['bodyBg']} "
            f"terminalInk={p['light']['terminalInk']}"
        )
        print(
            f"  dark:  accent={p['dark']['accent']} bodyBg={p['dark']['bodyBg']} "
            f"terminalInk={p['dark']['terminalInk']}"
        )
        print(f"  wallpapers: skins/{args.id}/light.jpg + dark.jpg")
        return

    (skin_dir / "skin.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    switch_skin.switch(manifest)
    packs = regen_native_packs(skin_dir, colors, args.id)
    create_skin.write_color_tables(skin_dir, manifest, derived_from_colors(colors, manifest))

    print(f"\nApplied: {manifest['label']} ({args.id})")
    print("  style.css re-rendered, wallpapers copied, state updated")
    print("  native import strings: " + ", ".join(str(x) for x in packs))
    print("  colors.md refreshed from colors.json")
    print("Verify: node scripts/check.mjs --port 9335")


if __name__ == "__main__":
    main()
