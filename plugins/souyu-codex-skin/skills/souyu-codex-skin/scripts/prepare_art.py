#!/usr/bin/env python3
"""Compress background image(s) for the Codex Lite Skin.

Usage:
  python prepare_art.py <image> [--dark <dark-image>] [--out <path>]

Default outputs next to this script:
  art.jpg        light-mode artwork (required; inject.mjs embeds it)
  art-dark.jpg   dark-mode artwork (optional; if omitted, dark mode reuses art.jpg)
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required: pip install Pillow")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("image", help="Source image (landscape preferred, subject right, no text/watermark)")
    ap.add_argument("--dark", default=None, help="Dark-mode variant image (night palette)")
    ap.add_argument("--out", default=None, help="Output jpg path (default: art.jpg next to this script)")
    ap.add_argument("--max-width", type=int, default=2560)
    args = ap.parse_args()

    src = Path(args.image)
    if not src.is_file():
        sys.exit(f"Image not found: {src}")
    out = Path(args.out) if args.out else Path(__file__).resolve().parent / "art.jpg"

    def compress(image_path: Path, target: Path) -> None:
        img = Image.open(image_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        if img.width > args.max_width:
            img = img.resize((args.max_width, round(img.height * args.max_width / img.width)), Image.LANCZOS)
        img.save(target, "JPEG", quality=82, optimize=True)
        print(f"art saved: {target} ({target.stat().st_size} bytes, {img.width}x{img.height})")

    compress(src, out)
    if args.dark:
        dark_src = Path(args.dark)
        if not dark_src.is_file():
            sys.exit(f"Dark image not found: {dark_src}")
        compress(dark_src, out.with_name("art-dark.jpg"))


if __name__ == "__main__":
    main()
