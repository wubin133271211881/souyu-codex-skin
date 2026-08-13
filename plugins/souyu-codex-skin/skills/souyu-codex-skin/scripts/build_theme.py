#!/usr/bin/env python3
"""Build a Codex app skin pack from an image.

Outputs (all written to --out):
  theme.json          native theme JSON (codeThemeId + theme + variant)
  codex-theme-v1.txt  paste-ready import string for Settings > Appearance > Import
  background.png      copy of the source artwork
  palette.png         color swatch preview for visual QA
  README.md           usage and restore guidance (unless --no-readme)

Usage:
  python build_theme.py --image <path> [--variant auto|light|dark]
                        [--name <skin-name>] [--accent #hex] [--surface #hex]
                        [--ink #hex] [--font-ui <names>] [--font-code <names>]
                        [--out <dir>] [--no-readme]
"""

from __future__ import annotations

import argparse
import colorsys
import json
import re
import shutil
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is required: pip install Pillow")


HEX_RE = re.compile(r"^#?([0-9a-fA-F]{6})$")


def parse_hex(value: str) -> tuple[int, int, int]:
    m = HEX_RE.match(value.strip())
    if not m:
        raise SystemExit(f"Invalid hex color: {value}")
    h = m.group(1)
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def _linearize(c: int) -> float:
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = (_linearize(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: tuple[int, int, int], bg: tuple[int, int, int]) -> float:
    l1, l2 = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def blend(rgb: tuple[int, int, int], target: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(round(c + (t - c) * amount) for c, t in zip(rgb, target))  # type: ignore[return-value]


def saturation(rgb: tuple[int, int, int]) -> float:
    r, g, b = (c / 255.0 for c in rgb)
    _, _, s = colorsys.rgb_to_hls(r, g, b)
    return s


def lightness(rgb: tuple[int, int, int]) -> float:
    r, g, b = (c / 255.0 for c in rgb)
    _, l, _ = colorsys.rgb_to_hls(r, g, b)
    return l


def hue_of(rgb: tuple[int, int, int]) -> float:
    r, g, b = (c / 255.0 for c in rgb)
    h, _, _ = colorsys.rgb_to_hls(r, g, b)
    return h


def saturate_to(rgb: tuple[int, int, int], level: float, lightness: float) -> tuple[int, int, int]:
    r, g, b = (c / 255.0 for c in rgb)
    h, _, _ = colorsys.rgb_to_hls(r, g, b)
    return tuple(round(c * 255) for c in colorsys.hls_to_rgb(h, lightness, level))  # type: ignore[return-value]


def dominant_colors(img: Image.Image, n: int = 6) -> list[tuple[int, int, int]]:
    small = img.copy()
    small.thumbnail((160, 160))
    if small.mode != "RGB":
        small = small.convert("RGB")
    q = small.quantize(colors=8, method=Image.MEDIANCUT)
    palette = q.getpalette() or []
    counts = sorted(q.getcolors(), reverse=True)
    return [tuple(palette[idx * 3 : idx * 3 + 3]) for _, idx in counts[:n]]


def ensure_contrast(
    ink: tuple[int, int, int],
    surface: tuple[int, int, int],
    target: float,
    toward: tuple[int, int, int],
) -> tuple[int, int, int]:
    for _ in range(24):
        if contrast_ratio(ink, surface) >= target:
            break
        ink = blend(ink, toward, 0.12)
    return ink


def pick_semantic(colors: list[tuple[int, int, int]], variant: str) -> dict[str, str]:
    defaults = {
        "light": {"diffAdded": "#1f8a4c", "diffRemoved": "#d13438", "skill": "#b7791f"},
        "dark": {"diffAdded": "#3fb950", "diffRemoved": "#f85149", "skill": "#d29922"},
    }[variant]
    lo_l, hi_l = (0.0, 0.62) if variant == "light" else (0.38, 1.0)
    for rgb in colors:
        h = hue_of(rgb)
        s = saturation(rgb)
        l = lightness(rgb)
        if s < 0.4 or not (lo_l <= l <= hi_l):
            continue
        if 80 <= h * 360 <= 170 and "diffAdded" in defaults:
            defaults["diffAdded"] = to_hex(rgb)
        elif (340 <= h * 360 <= 360 or h * 360 <= 20) and "diffRemoved" in defaults:
            defaults["diffRemoved"] = to_hex(rgb)
        elif 30 <= h * 360 <= 70 and "skill" in defaults:
            defaults["skill"] = to_hex(rgb)
    return defaults


def derive_theme(img: Image.Image, variant: str = "auto") -> dict:
    """Derive the native theme core (accent/surface/ink + semantic) from artwork.

    Shared by build_theme.py itself and by create_skin.py so the full-board
    panel palette and the native theme always come from the same colors.
    Returns a dict with variant, colors, accent, surface, ink, contrast,
    semantic.
    """
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    colors = dominant_colors(img)
    if variant == "auto":
        variant = "dark" if sum(luminance(c) for c in colors) / len(colors) < 0.25 else "light"

    if variant == "light":
        surface = max(colors, key=luminance)
        while luminance(surface) < 0.75:
            surface = blend(surface, (255, 255, 255), 0.25)
        ink = min(colors, key=luminance)
        while luminance(ink) > 0.10:
            ink = blend(ink, (0, 0, 0), 0.2)
        accent = max(colors, key=saturation)
        if saturation(accent) < 0.3:
            accent = parse_hex("#c85a3f")  # muted image: warm fallback
        else:
            accent = saturate_to(accent, 0.7, 0.5)
        accent = ensure_contrast(accent, surface, 3.0, (0, 0, 0))
        if lightness(accent) < 0.35:
            accent = saturate_to(accent, 0.7, 0.5)
        ink = ensure_contrast(ink, surface, 7.0, (0, 0, 0))
    else:
        surface = min(colors, key=luminance)
        while luminance(surface) > 0.05:
            surface = blend(surface, (0, 0, 0), 0.2)
        ink = max(colors, key=luminance)
        while luminance(ink) < 0.85:
            ink = blend(ink, (255, 255, 255), 0.2)
        accent = max(colors, key=saturation)
        if saturation(accent) < 0.3:
            accent = parse_hex("#e58e4c")  # muted image: warm fallback
        else:
            accent = saturate_to(accent, 0.7, 0.6)
        accent = ensure_contrast(accent, surface, 3.0, (255, 255, 255))
        if lightness(accent) > 0.75:
            accent = saturate_to(accent, 0.7, 0.6)
        ink = ensure_contrast(ink, surface, 7.0, (255, 255, 255))

    ratio = contrast_ratio(ink, surface)
    contrast = max(0, min(100, round((ratio - 1.0) / 20.0 * 100)))
    semantic = pick_semantic(colors, variant)
    return {
        "variant": variant,
        "colors": colors,
        "accent": accent,
        "surface": surface,
        "ink": ink,
        "contrast": contrast,
        "semantic": semantic,
    }


def slugify(name: str) -> str:
    s = re.sub(r"[^0-9a-zA-Z-]+", "-", name.strip().lower()).strip("-")
    return s or "codex-skin"


def draw_palette(colors: list[tuple[int, int, int]], out: Path) -> None:
    swatch_w, swatch_h, label_h = 240, 140, 40
    w, h = swatch_w * len(colors), swatch_h + label_h
    img = Image.new("RGB", (w, h), "#ffffff")
    draw = ImageDraw.Draw(img)
    font = None
    for candidate in (
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            font = ImageFont.truetype(candidate, 18)
            break
        except OSError:
            continue
    for i, rgb in enumerate(colors):
        x = i * swatch_w
        draw.rectangle((x, 0, x + swatch_w, swatch_h), fill=rgb)
        label = to_hex(rgb)
        text_color = "#111111" if luminance(rgb) > 0.5 else "#ffffff"
        draw.text((x + 12, swatch_h + 10), label, fill=text_color, font=font)
    img.save(out)


def write_readme(out: Path, name: str, variant: str, theme_json: dict) -> None:
    lines = [
        f"# {name} — Codex skin",
        "",
        "Pack contents:",
        "- `background.png` — skin artwork",
        "- `theme.json` — native theme JSON",
        "- `codex-theme-v1.txt` — paste-ready import string",
        "- `palette.png` — extracted color palette preview",
        "",
        f"## Apply (colors & fonts, native)",
        f"1. Open Codex App **Settings → Appearance**.",
        f"2. In the **{variant.title()} theme** section, click **Import** and paste the contents of `codex-theme-v1.txt`.",
        "",
        "## Apply (full wallpaper skin, optional)",
        "Native import only changes colors and fonts. To show `background.png` behind the whole window,",
        "use a community skin engine such as Codex Dream Skin or Codex AutoSkin and point it at this pack.",
        "",
        "## Restore",
        "Switch back to any built-in base theme in Settings → Appearance. Keeping this folder lets you re-import anytime.",
        "",
    ]
    out.joinpath("README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Build a Codex app skin pack from an image.")
    ap.add_argument("--image", required=True, help="Source artwork (landscape preferred, no text/watermark)")
    ap.add_argument("--variant", default="auto", choices=["auto", "light", "dark"])
    ap.add_argument("--name", default="codex-skin", help="Skin name (also used as codeThemeId)")
    ap.add_argument("--accent", default=None, help="Override accent hex, e.g. #d96b42")
    ap.add_argument("--surface", default=None, help="Override surface (background) hex")
    ap.add_argument("--ink", default=None, help="Override ink (foreground) hex")
    ap.add_argument("--font-ui", default="Inter, system-ui, sans-serif", help="UI font stack")
    ap.add_argument("--font-code", default="JetBrains Mono, SF Mono, Menlo, monospace", help="Code font stack")
    ap.add_argument("--out", default=None, help="Output directory (default: outputs/<name>)")
    ap.add_argument("--no-readme", action="store_true", help="Skip README.md generation")
    args = ap.parse_args()

    src = Path(args.image)
    if not src.is_file():
        sys.exit(f"Image not found: {src}")

    img = Image.open(src)
    img.load()
    if img.width < img.height:
        print("Warning: portrait image; landscape backgrounds are recommended.")

    derived = derive_theme(img, args.variant)
    variant = derived["variant"]
    colors = derived["colors"]
    accent, surface, ink = derived["accent"], derived["surface"], derived["ink"]
    if args.accent:
        accent = parse_hex(args.accent)
    if args.surface:
        surface = parse_hex(args.surface)
    if args.ink:
        ink = parse_hex(args.ink)

    semantic = pick_semantic(colors, variant)
    ratio = contrast_ratio(ink, surface)
    contrast = max(0, min(100, round((ratio - 1.0) / 20.0 * 100)))

    theme = {
        "codeThemeId": slugify(args.name),
        "theme": {
            "accent": to_hex(accent),
            "contrast": contrast,
            "fonts": {"ui": args.font_ui, "code": args.font_code},
            "ink": to_hex(ink),
            "opaqueWindows": True,
            "semanticColors": semantic,
            "surface": to_hex(surface),
        },
        "variant": variant,
    }

    out = Path(args.out) if args.out else Path("outputs") / slugify(args.name)
    out.mkdir(parents=True, exist_ok=True)

    shutil.copy2(src, out / "background.png")
    out.joinpath("theme.json").write_text(json.dumps(theme, indent=2, ensure_ascii=False), encoding="utf-8")
    import_str = "codex-theme-v1:" + json.dumps(theme, separators=(",", ":"), ensure_ascii=False)
    out.joinpath("codex-theme-v1.txt").write_text(import_str, encoding="utf-8")
    draw_palette(colors, out / "palette.png")
    if not args.no_readme:
        write_readme(out, args.name, variant, theme)

    print(f"Variant: {variant}")
    print(f"Palette: {', '.join(to_hex(c) for c in colors)}")
    print(f"accent={to_hex(accent)} surface={to_hex(surface)} ink={to_hex(ink)} contrast={contrast} (ratio {ratio:.1f}:1)")
    print(f"Semantic: {semantic}")
    print(f"Pack written to: {out}")
    print(f"Import string: {out / 'codex-theme-v1.txt'}")


if __name__ == "__main__":
    main()
