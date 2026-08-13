#!/usr/bin/env python3
"""Import previously generated skin packs into the switcher registry.

Historical packs produced by build_theme.py look like:
  <pack>/
    theme.json            {codeThemeId, variant, theme:{accent,surface,ink,...}}
    background.png        2048x1152 artwork (or dark/light subfolders, *-dark.png...)
    dark/theme.json + dark/background.png + light/...   (optional split layout)

The importer:
  1. finds dark + light theme colors (derives missing ones from artwork via
     build_theme.py);
  2. compresses the dark/light artwork into skins/<id>/dark.jpg + light.jpg;
  3. renders the full 22-key skin.json palette from (surface, ink, accent);
  4. registers the skin so switch_skin.ps1 can activate it.

Usage:
  python import_skin.py --source <pack-dir> [--id ID] [--label LABEL]
  python import_skin.py --scan [--base C:\\Users\\wubin\\Documents\\Codex]
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required: pip install Pillow")

ROOT = Path(__file__).resolve().parent.parent
SKINS = ROOT / "skins"
SCRIPTS = ROOT / "scripts"
MAX_W = 2560

KNOWN_LABELS = {
    "gongsunli-codex-skin": "公孙离 · 卡通粉",
    "silver-moon": "凡人修仙 · 银月",
    "wei-long": "wei-long · 暖金",
    "honor-of-kings-daji": "妲己 · 王者粉",
    "mai-shiranui-skin": "不知火舞 · 绯红",
    "cute-girl": "可爱女孩 · 蜜桃粉",
}


def read_theme(path: Path) -> dict | None:
    try:
        t = json.loads(path.read_text(encoding="utf-8"))
        if "theme" not in t:
            return None
        return t
    except (OSError, ValueError):
        return None


def derive_theme_from_art(art: Path, variant: str, tmp_id: str) -> dict:
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)
        subprocess.run(
            [sys.executable, str(SCRIPTS / "build_theme.py"), "--image", str(art),
             "--variant", variant, "--name", tmp_id, "--out", str(out), "--no-readme"],
            check=True, capture_output=True,
        )
        theme = read_theme(out / "theme.json")
        if not theme:
            sys.exit(f"derive_theme failed for {art}")
        return theme


def find_art(roots: list[Path], id_hint: str) -> dict[str, Path]:
    """Return {'dark': path, 'light': path} across multiple source dirs."""
    dark = light = None
    patterns = [
        (f"{id_hint}-dark.png", "dark"), ("dark.png", "dark"),
        ("wallpaper-dark.png", "dark"), (f"{id_hint}-light.png", "light"),
        ("light.png", "light"), ("wallpaper-light.png", "light"),
    ]
    for root in roots:
        for name, mode in patterns:
            p = root / name
            if p.is_file():
                if mode == "dark":
                    dark = dark or p
                else:
                    light = light or p
        for sub, mode in (("dark", "dark"), ("light", "light")):
            p = root / sub / "background.png"
            if p.is_file():
                if mode == "dark":
                    dark = dark or p
                else:
                    light = light or p
    # Fallback: assign one background.png per variant in root order, so split
    # packs (dark/ + light/ siblings) get distinct images when possible.
    fallbacks = [root / "background.png" for root in roots if (root / "background.png").is_file()]
    if not dark and fallbacks:
        dark = fallbacks[0]
    if not light and fallbacks:
        light = fallbacks[1] if len(fallbacks) > 1 else fallbacks[0]
    return {"dark": dark, "light": light}


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.strip().lstrip("#")
    if len(h) != 6:
        sys.exit(f"bad hex: {h}")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def blend(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))  # type: ignore[return-value]


def rgba(c: tuple[int, int, int], a: float) -> str:
    return f"rgba({c[0]}, {c[1]}, {c[2]}, {a:.2f})"


def linear_gradient(stops: list[tuple[tuple[int, int, int], float, float]]) -> str:
    parts = []
    for c, a, pos in stops:
        parts.append(f"rgba({c[0]}, {c[1]}, {c[2]}, {a:.2f}) {pos}%")
    return "linear-gradient(to top, " + ", ".join(parts) + ")"


def derive_palette(variant: str, surface: str, ink: str, accent: str) -> dict:
    S = hex_to_rgb(surface)
    I = hex_to_rgb(ink)
    A = hex_to_rgb(accent)
    SA2 = blend(S, A, 0.20)
    SA3 = blend(S, A, 0.30)
    SA4 = blend(S, A, 0.40)
    SA5 = blend(S, A, 0.50)
    if variant == "dark":
        return {
            "accent": accent,
            "bodyBg": surface,
            "bodyGlowA": rgba(A, 0.24),
            "bodyGlowB": rgba(A, 0.16),
            "asideA": rgba(S, 0.97),
            "asideB": rgba(SA3, 0.93),
            "border": rgba(A, 0.30),
            "topA": rgba(S, 0.97),
            "topB": rgba(SA3, 0.92),
            "mainA": rgba(S, 0.97),
            "mainB": rgba(SA2, 0.90),
            "mainC": rgba(SA4, 0.70),
            "mainD": rgba(A, 0.45),
            "headerBg": rgba(SA2, 0.88),
            "activeBg": rgba(A, 0.26),
            "cardBg": rgba(S, 0.94),
            "cardBg2": rgba(SA3, 0.90),
            "utilityBg": rgba(SA3, 0.90),
            "inputBg": rgba(SA5, 0.72),
            "topFade": linear_gradient([(S, 0.95, 0), (S, 0.0, 100)]),
            "composerFade": linear_gradient([(S, 0.95, 0), (SA3, 0.55, 50), (S, 0.0, 100)]),
            "menuBg": rgba(SA4, 0.97),
            "moduleBg": rgba(SA3, 0.90),
            "buttonBg": rgba(A, 0.22),
            "terminalBg": rgba(SA2, 0.97),
            "terminalInk": ink,
        }
    return {
        "accent": accent,
        "bodyBg": surface,
        "bodyGlowA": rgba(A, 0.18),
        "bodyGlowB": rgba(SA3, 0.22),
        "asideA": rgba(S, 0.96),
        "asideB": rgba(SA2, 0.90),
        "border": rgba(SA3, 0.30),
        "topA": rgba(S, 0.97),
        "topB": rgba(SA2, 0.92),
        "mainA": rgba(S, 0.97),
        "mainB": rgba(SA2, 0.90),
        "mainC": rgba(SA3, 0.55),
        "mainD": rgba(SA5, 0.30),
        "headerBg": rgba(S, 0.85),
        "activeBg": rgba(SA3, 0.38),
        "cardBg": rgba(S, 0.94),
        "cardBg2": rgba(SA2, 0.90),
        "utilityBg": rgba(SA2, 0.90),
        "inputBg": rgba(SA2, 0.78),
        "topFade": linear_gradient([(S, 0.95, 0), (S, 0.0, 100)]),
        "composerFade": linear_gradient([(S, 0.95, 0), (SA3, 0.55, 50), (S, 0.0, 100)]),
        "menuBg": rgba(S, 0.98),
        "moduleBg": rgba(SA2, 0.92),
        "buttonBg": rgba(SA4, 0.20),
        "terminalBg": rgba(S, 0.96),
        "terminalInk": ink,
    }


def compress(src: Path, dst: Path) -> None:
    img = Image.open(src)
    if img.mode != "RGB":
        img = img.convert("RGB")
    if img.width > MAX_W:
        img = img.resize((MAX_W, round(img.height * MAX_W / img.width)), Image.LANCZOS)
    img.save(dst, "JPEG", quality=82, optimize=True)


def import_pack(sources: list[Path], skin_id: str, label: str) -> None:
    themes = {}
    for source in sources:
        for tj in source.rglob("theme.json"):
            t = read_theme(tj)
            if t and t.get("variant") in ("dark", "light"):
                themes.setdefault(t["variant"], t)
    arts = find_art(sources, skin_id)

    def colors_for(variant: str, art: Path) -> dict:
        t = themes.get(variant)
        if t and t.get("theme"):
            return t["theme"]
        if not art:
            sys.exit(f"{variant} colors and artwork missing for {sources}")
        return derive_theme_from_art(art, variant, skin_id + "-" + variant)["theme"]

    out = SKINS / skin_id
    out.mkdir(parents=True, exist_ok=True)
    palette = {}
    light_art = arts["light"] or arts["dark"]
    dark_art = arts["dark"] or arts["light"]
    if not light_art:
        sys.exit(f"no artwork found for {sources}")
    for variant, art in (("dark", dark_art), ("light", light_art)):
        th = colors_for(variant, art)
        palette[variant] = derive_palette(
            variant, th["surface"], th["ink"], th["accent"]
        )
        compress(art, out / f"{variant}.jpg")
    manifest = {"id": skin_id, "label": label, "light": "light.jpg", "dark": "dark.jpg", "palette": palette}
    (out / "skin.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Registered: {label} ({skin_id})")
    print(f"  dark  -> {out / 'dark.jpg'}")
    print(f"  light -> {out / 'light.jpg'}")
    print(f"Switch with: switch_skin.ps1 -Name {skin_id}")


def scan_packs(base: Path) -> list[tuple[list[Path], str]]:
    """Find pack dirs directly containing theme.json; merge dark/light siblings."""
    units = []
    for tj in base.rglob("theme.json"):
        units.append(tj.parent)
    grouped: dict[str, list[Path]] = {}
    for d in units:
        t = read_theme(d / "theme.json")
        if not t:
            continue
        cid = t.get("codeThemeId") or d.name
        merged = re.sub(r"-(dark|light)$", "", cid)
        grouped.setdefault(merged, []).append(d)
    packs = []
    for cid, dirs in grouped.items():
        packs.append((dirs, cid))
    return packs


def main() -> None:
    ap = argparse.ArgumentParser(description="Import historical skin packs into the switcher")
    ap.add_argument("--source", default=None, help="Pack directory to import")
    ap.add_argument("--id", default=None, help="Skin id (default: codeThemeId)")
    ap.add_argument("--label", default=None, help="Display label (default: known/pretty name)")
    ap.add_argument("--scan", action="store_true", help="Scan base for all packs")
    ap.add_argument("--base", default=str(Path.home() / "Documents" / "Codex"), help="Base dir for --scan")
    args = ap.parse_args()

    if args.scan:
        base = Path(args.base)
        if not base.is_dir():
            sys.exit(f"base not found: {base}")
        for dirs, cid in scan_packs(base):
            if (SKINS / cid / "skin.json").exists():
                print(f"skip {cid} (already registered)")
                continue
            label = KNOWN_LABELS.get(cid, cid)
            try:
                import_pack(dirs, cid, label)
            except SystemExit as e:
                print(f"skip {cid}: {e}")
        return

    if not args.source:
        sys.exit("--source required (or use --scan)")
    source = Path(args.source)
    if not source.is_dir():
        sys.exit(f"source not found: {source}")
    t = read_theme(source / "theme.json") or next(
        (read_theme(p) for p in source.rglob("theme.json")), None
    )
    cid = args.id or (t.get("codeThemeId") if t else source.name)
    cid = re.sub(r"-(dark|light)$", "", cid)
    label = args.label or KNOWN_LABELS.get(cid, cid)
    import_pack([source], cid, label)


if __name__ == "__main__":
    main()
