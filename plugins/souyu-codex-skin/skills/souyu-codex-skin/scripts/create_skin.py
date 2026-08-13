#!/usr/bin/env python3
"""One-shot full-board skin generator: artwork -> every color the skin uses.

Turns light/dark artwork into the complete color system in one command:

  1. Native theme packs (outputs/<id>/pack/{light,dark}/theme.json +
     codex-theme-v1.txt) for Settings > Appearance > Import.
  2. Full 24-key panel palettes (skins/<id>/skin.json -> palette.light/dark)
     rendered by style.template.css into the injected style.css.
  3. Compressed wallpapers skins/<id>/light.jpg + dark.jpg.
  4. Palette preview image (outputs/<id>/palette-preview.png).
  5. Unless --no-switch: renders style.css, copies the active art, records the
     runtime state (same effect as switch_skin.ps1 -Name <id>).

No field-by-field color work is needed: every value is derived from the
artwork by the same formulas build_theme.py (native theme) and import_skin.py
(panel palette) already use.

Usage:
  python create_skin.py --light <light-img> --dark <dark-img> --id <id> --label "<name>"
  python create_skin.py --light <light-img> --id <id> --label "<name>" --no-switch
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
SKINS = ROOT / "skins"
sys.path.insert(0, str(SCRIPTS))

import build_theme  # noqa: E402
import import_skin  # noqa: E402
import switch_skin  # noqa: E402

RGBA_RE = re.compile(r"rgba\((\d+),\s*(\d+),\s*(\d+)")


def native_theme(skin_id: str, variant: str, derived: dict) -> dict:
    return {
        "codeThemeId": build_theme.slugify(skin_id),
        "theme": {
            "accent": build_theme.to_hex(derived["accent"]),
            "contrast": derived["contrast"],
            "fonts": {
                "ui": "Inter, system-ui, sans-serif",
                "code": "JetBrains Mono, SF Mono, Menlo, monospace",
            },
            "ink": build_theme.to_hex(derived["ink"]),
            "opaqueWindows": True,
            "semanticColors": derived["semantic"],
            "surface": build_theme.to_hex(derived["surface"]),
        },
        "variant": variant,
    }


def write_native_pack(out: Path, skin_id: str, variant: str, derived: dict, art: Path) -> None:
    pack = out / variant
    pack.mkdir(parents=True, exist_ok=True)
    theme = native_theme(skin_id, variant, derived)
    shutil.copy2(art, pack / "background.png")
    (pack / "theme.json").write_text(
        json.dumps(theme, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    import_str = "codex-theme-v1:" + json.dumps(theme, separators=(",", ":"), ensure_ascii=False)
    (pack / "codex-theme-v1.txt").write_text(import_str, encoding="utf-8")
    build_theme.draw_palette(derived["colors"], pack / "palette.png")


def _font(size: int):
    for candidate in (
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            return build_theme.ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return None


def swatch_color(value: str) -> tuple[int, int, int]:
    m = RGBA_RE.search(value)
    if m:
        return tuple(int(m.group(i)) for i in (1, 2, 3))
    return build_theme.parse_hex(value)


def write_preview(out: Path, palette: dict) -> None:
    """Two rows of the full palette (dark / light) for visual QA."""
    keys = list(palette["dark"].keys())
    cell_w, cell_h, label_h, title_h = 118, 56, 20, 26
    w = cell_w * len(keys)
    h = title_h + (cell_h + label_h) * 2 + 10
    img = build_theme.Image.new("RGB", (w, h), "#ffffff")
    draw = build_theme.ImageDraw.Draw(img)
    font = _font(12)
    title_font = _font(16)
    for row, variant in enumerate(("dark", "light")):
        y = title_h + row * (cell_h + label_h)
        draw.text((6, 4 + row * (cell_h + label_h)), variant.upper(), fill="#111111", font=title_font)
        for i, key in enumerate(keys):
            x = i * cell_w
            color = swatch_color(palette[variant][key])
            draw.rectangle((x, y, x + cell_w - 2, y + cell_h), fill=color)
            label_color = "#111111" if build_theme.luminance(color) > 0.5 else "#ffffff"
            if font:
                draw.text((x + 2, y + cell_h + 2), key, fill=label_color, font=font)
    img.save(out / "palette-preview.png")


PANEL_ROLES = {
    "accent": "主角色：欢迎页建议卡图标",
    "bodyBg": "窗口底色",
    "bodyGlowA": "背景右上光晕",
    "bodyGlowB": "背景左上光晕",
    "asideA": "左侧栏渐变起点",
    "asideB": "左侧栏渐变终点",
    "border": "边框/分隔线",
    "topA": "顶部菜单栏渐变起点",
    "topB": "顶部菜单栏渐变终点",
    "mainA": "主内容区渐变 A",
    "mainB": "主内容区渐变 B",
    "mainC": "主内容区渐变 C",
    "mainD": "主内容区渐变 D（叠加壁纸）",
    "headerBg": "会话头部背景",
    "activeBg": "侧栏选中项/悬停",
    "cardBg": "设置/会话主表面",
    "cardBg2": "次级表面",
    "utilityBg": "欢迎页 composer 工具条（任务 chip/完全访问/自定义高）",
    "inputBg": "输入框/胶块",
    "topFade": "顶部淡出",
    "composerFade": "输入区底部淡出",
    "menuBg": "菜单栏菜单 + 下拉",
    "moduleBg": "设置模块卡",
    "buttonBg": "设置页按钮",
    "terminalBg": "终端框架/视口",
    "terminalInk": "终端文字",
}


def render_colors_md(colors: dict) -> str:
    """Human-readable color table view (the machine source is colors.json)."""
    v = colors["variants"]
    lines = [
        f"# 颜色表 · {colors['id']}（{colors['label']}）",
        "",
        "> 一套皮肤 = 颜色表（本文件是可视化视图，机器读取 `colors.json`）+ 图片（`light.jpg` / `dark.jpg`）。",
        f"> 改色或换图后运行：`python scripts\\apply_skin.py --id {colors['id']}`（`--dry-run` 先预览）",
        "",
        "## 原生主题（Settings → Appearance → Import）",
        "",
        "| 角色 | light | dark |",
        "| --- | --- | --- |",
    ]
    for key, label in (
        ("accent", "accent（主角色）"),
        ("surface", "surface（窗口底色）"),
        ("ink", "ink（文字色）"),
        ("contrast", "contrast"),
    ):
        lines.append(f"| {label} | {v['light'].get(key, '')} | {v['dark'].get(key, '')} |")
    for skey, label in (
        ("diffAdded", "semantic.diffAdded（新增行）"),
        ("diffRemoved", "semantic.diffRemoved（删除行）"),
        ("skill", "semantic.skill（技能）"),
    ):
        lines.append(
            f"| {label} | {v['light'].get('semanticColors', {}).get(skey, '')} | "
            f"{v['dark'].get('semanticColors', {}).get(skey, '')} |"
        )
    lines += [
        "",
        "## 面板调色板（24 键 × light/dark，注入 CSS 用）",
        "",
        "| 键 | 用途 | light | dark |",
        "| --- | --- | --- | --- |",
    ]
    for key, role in PANEL_ROLES.items():
        lines.append(f"| {key} | {role} | {v['light']['panel'].get(key, '')} | {v['dark']['panel'].get(key, '')} |")
    return "\n".join(lines) + "\n"


def write_color_tables(skin_dir: Path, manifest: dict, derived_by_variant: dict) -> None:
    """Write the editable color table (colors.json) and its markdown view."""
    colors = {"id": manifest["id"], "label": manifest["label"], "variants": {}}
    for variant in ("light", "dark"):
        d = derived_by_variant[variant]
        colors["variants"][variant] = {
            "accent": build_theme.to_hex(d["accent"]),
            "surface": build_theme.to_hex(d["surface"]),
            "ink": build_theme.to_hex(d["ink"]),
            "contrast": d["contrast"],
            "semanticColors": d["semantic"],
            "panel": manifest["palette"][variant],
        }
    (skin_dir / "colors.json").write_text(
        json.dumps(colors, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (skin_dir / "colors.md").write_text(render_colors_md(colors), encoding="utf-8")
    print(f"  color table     -> {skin_dir / 'colors.json'} (+ colors.md)")


def main() -> None:
    ap = argparse.ArgumentParser(description="One-shot full-board skin generator from artwork")
    ap.add_argument("--light", required=True, help="Light-mode artwork (bright/pastel, landscape)")
    ap.add_argument("--dark", default=None, help="Dark-mode artwork (dark night); falls back to --light")
    ap.add_argument("--id", required=True, help="Skin id (folder name, lowercase/ascii)")
    ap.add_argument("--label", default=None, help="Display label, e.g. 春野樱 · 可爱粉")
    ap.add_argument("--out", default=None, help="Native pack output dir (default: outputs/<id>)")
    ap.add_argument("--no-switch", action="store_true", help="Register the skin without activating it")
    ap.add_argument("--accent", default=None, help="Override accent for BOTH variants, e.g. #f28fc6")
    ap.add_argument("--light-accent", default=None, help="Override the light accent only")
    ap.add_argument("--dark-accent", default=None, help="Override the dark accent only")
    args = ap.parse_args()

    light_art = Path(args.light)
    dark_art = Path(args.dark) if args.dark else light_art
    for p in (light_art, dark_art):
        if not p.is_file():
            sys.exit(f"Image not found: {p}")

    label = args.label or args.id
    out = Path(args.out) if args.out else ROOT / "outputs" / args.id

    accent_overrides = {
        "light": args.light_accent or args.accent,
        "dark": args.dark_accent or args.accent,
    }
    palette = {}
    derived_by_variant = {}
    for variant, art in (("light", light_art), ("dark", dark_art)):
        img = build_theme.Image.open(art)
        img.load()
        derived = build_theme.derive_theme(img, variant)
        surface = build_theme.to_hex(derived["surface"])
        ink = build_theme.to_hex(derived["ink"])
        accent = build_theme.to_hex(derived["accent"])
        override = accent_overrides[variant]
        if override:
            accent = build_theme.to_hex(build_theme.parse_hex(override))
            derived["accent"] = build_theme.parse_hex(override)
        derived_by_variant[variant] = derived
        palette[variant] = import_skin.derive_palette(variant, surface, ink, accent)
        write_native_pack(out, args.id, variant, derived, art)
        print(
            f"[{variant}] accent={accent} surface={surface} ink={ink} "
            f"contrast={derived['contrast']} semantic={derived['semantic']}"
        )

    skin_dir = SKINS / args.id
    skin_dir.mkdir(parents=True, exist_ok=True)
    import_skin.compress(light_art, skin_dir / "light.jpg")
    import_skin.compress(dark_art, skin_dir / "dark.jpg")
    manifest = {
        "id": args.id,
        "label": label,
        "light": "light.jpg",
        "dark": "dark.jpg",
        "palette": palette,
    }
    (skin_dir / "skin.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_preview(out, palette)
    write_color_tables(skin_dir, manifest, derived_by_variant)

    print(f"\nRegistered: {label} ({args.id})")
    print(f"  skin.json       -> {skin_dir / 'skin.json'}")
    print(f"  color table     -> {skin_dir / 'colors.json'}")
    print(f"  wallpapers      -> {skin_dir / 'light.jpg'} + dark.jpg")
    print(f"  native packs    -> {out / 'light'} + {out / 'dark'}")
    print(f"  palette preview -> {out / 'palette-preview.png'}")

    if args.no_switch:
        print("Activate later with: switch_skin.ps1 -Name " + args.id)
        return
    switch_skin.switch(manifest)
    print("Activated. Verify: node scripts/check.mjs --port 9335")


if __name__ == "__main__":
    main()
