#!/usr/bin/env python3
"""Switch the active Codex Lite Skin.

Registry: <skill-root>/skins/<id>/skin.json
  skin.json = {
    "id": "...", "label": "...", "light": "light.jpg", "dark": "dark.jpg",
    "palette": {"light": {...}, "dark": {...}}
  }

Switching renders scripts/style.css from scripts/style.template.css using the
skin's palette, copies light.jpg/dark.jpg over scripts/art.jpg/art-dark.jpg,
and records the current skin in the runtime state. Restart the injector
(scripts/start.ps1) afterwards to apply.

Usage:
  python switch_skin.py --list
  python switch_skin.py --skin <id>
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKINS = ROOT / "skins"
SCRIPTS = ROOT / "scripts"
TEMPLATE = SCRIPTS / "style.template.css"
STYLE = SCRIPTS / "style.css"
STATE_PATH = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "CodexLiteSkin" / "state.json"

# token suffix -> palette key (same keys exist in light and dark palettes)
TOKEN_MAP = {
    "BODY_BG": "bodyBg",
    "BODY_GLOW_A": "bodyGlowA",
    "BODY_GLOW_B": "bodyGlowB",
    "ASIDE_A": "asideA",
    "ASIDE_B": "asideB",
    "BORDER": "border",
    "TOP_A": "topA",
    "TOP_B": "topB",
    "MAIN_A": "mainA",
    "MAIN_B": "mainB",
    "MAIN_C": "mainC",
    "MAIN_D": "mainD",
    "HEADER_BG": "headerBg",
    "ACTIVE_BG": "activeBg",
    "CARD_BG": "cardBg",
    "CARD_BG2": "cardBg2",
    "INPUT_BG": "inputBg",
    "TOP_FADE": "topFade",
    "COMPOSER_FADE": "composerFade",
    "MENU_BG": "menuBg",
    "MODULE_BG": "moduleBg",
    "BUTTON_BG": "buttonBg",
    "TERMINAL_BG": "terminalBg",
    "TERMINAL_INK": "terminalInk",
}


def list_skins() -> list[dict]:
    result = []
    if not SKINS.is_dir():
        return result
    for folder in sorted(SKINS.iterdir()):
        manifest = folder / "skin.json"
        if not manifest.is_file():
            continue
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if "id" in data and "label" in data:
            result.append(data)
    return result


def render_style(palette: dict) -> str:
    css = TEMPLATE.read_text(encoding="utf-8")
    missing = []
    for variant in ("light", "dark"):
        p = palette.get(variant)
        if not p:
            missing.append(variant)
            continue
        for token, key in TOKEN_MAP.items():
            placeholder = "@@" + variant.upper() + "_" + token + "@@"
            if placeholder in css:
                if key not in p:
                    missing.append(variant + "." + key)
                    continue
                css = css.replace(placeholder, str(p[key]))
    if "@@LIGHT_" in css or "@@DARK_" in css:
        sys.exit("style template has unreplaced tokens; palette keys missing: " + ", ".join(missing))
    return css


def switch(skin: dict) -> None:
    folder = SKINS / skin["id"]
    light_src = folder / skin.get("light", "light.jpg")
    dark_src = folder / skin.get("dark", "dark.jpg")
    if not light_src.is_file():
        sys.exit("light artwork missing: " + str(light_src))
    shutil.copy2(light_src, SCRIPTS / "art.jpg")
    if dark_src.is_file():
        shutil.copy2(dark_src, SCRIPTS / "art-dark.jpg")
    else:
        (SCRIPTS / "art-dark.jpg").unlink(missing_ok=True)
    STYLE.write_text(render_style(skin["palette"]), encoding="utf-8")

    state = {}
    if STATE_PATH.is_file():
        try:
            state = json.loads(STATE_PATH.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            state = {}
    state["currentSkin"] = skin["id"]
    state["currentSkinLabel"] = skin["label"]
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Switched to skin: " + skin["label"] + " (" + skin["id"] + ")")
    print("  light art -> " + str(SCRIPTS / "art.jpg"))
    print("  dark  art -> " + str(SCRIPTS / "art-dark.jpg"))
    print("  palette  -> " + str(STYLE))


def delete_skin(skin_id: str) -> None:
    skins = list_skins()
    target = next((s for s in skins if s["id"] == skin_id), None)
    if not target:
        sys.exit("Unknown skin '" + skin_id + "'.")
    if len(skins) <= 1:
        sys.exit("Refusing to delete the last registered skin.")
    state = {}
    if STATE_PATH.is_file():
        try:
            state = json.loads(STATE_PATH.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            state = {}
    if state.get("currentSkin") == skin_id:
        fallback = next(
            (s for s in sorted(skins, key=lambda x: x["id"]) if s["id"] != skin_id),
            None,
        )
        print("'" + skin_id + "' is active; switching to '" + fallback["id"] + "' first.")
        switch(fallback)
    folder = SKINS / skin_id
    if folder.is_dir():
        shutil.rmtree(folder)
    print("Deleted skin: " + target["label"] + " (" + skin_id + ")")


def main() -> None:
    ap = argparse.ArgumentParser(description="Switch the active Codex Lite Skin")
    ap.add_argument("--list", action="store_true", help="List registered skins")
    ap.add_argument("--skin", default=None, help="Skin id to activate")
    ap.add_argument("--delete", default=None, help="Delete a registered skin")
    args = ap.parse_args()

    if args.delete:
        delete_skin(args.delete)
        return
    skins = list_skins()
    if args.list:
        if not skins:
            print("No skins registered under " + str(SKINS))
            return
        for s in skins:
            print(s["id"] + "\t" + s["label"])
        return
    if not args.skin:
        sys.exit("Missing --skin <id> (or use --list to see available skins)")
    skin = next((s for s in skins if s["id"] == args.skin), None)
    if not skin:
        known = ", ".join(s["id"] for s in skins) or "(none)"
        sys.exit("Unknown skin '" + args.skin + "'. Registered: " + known)
    switch(skin)


if __name__ == "__main__":
    main()
