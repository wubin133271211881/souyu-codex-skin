# Codex Native Theme Format

A Codex app theme is a JSON object imported through **Settings → Appearance → Import**.

## Import string

The paste-ready form is the compact JSON prefixed with `codex-theme-v1:`:

```text
codex-theme-v1:{"codeThemeId":"...","theme":{...},"variant":"light"}
```

Paste it into the **Light theme** or **Dark theme** Import box depending on `variant`.

## Schema

| Field | Type | Meaning |
| --- | --- | --- |
| `codeThemeId` | string | Theme identifier |
| `variant` | `"light"` \| `"dark"` | Base theme |
| `theme.accent` | hex | Accent / highlight color |
| `theme.surface` | hex | Background color |
| `theme.ink` | hex | Foreground text color |
| `theme.contrast` | 0–100 | Ink/surface contrast strength |
| `theme.opaqueWindows` | bool | Solid vs translucent surfaces |
| `theme.fonts.ui` | string | UI font stack |
| `theme.fonts.code` | string | Code font stack |
| `theme.semanticColors.diffAdded` | hex | Added lines in diffs |
| `theme.semanticColors.diffRemoved` | hex | Removed lines in diffs |
| `theme.semanticColors.skill` | hex | Skill-related accents |

## Design guidance

- **Light themes**: surface luminance ≥ 0.75, ink luminance ≤ 0.10 (WCAG relative luminance).
- **Dark themes**: surface luminance ≤ 0.05, ink luminance ≥ 0.85 (WCAG relative luminance).
- **Accent**: take the most saturated color from the image; boost saturation toward 0.6–0.8 if the image is muted. Keep contrast against surface ≥ 3:1.
- **Contrast value**: `≈ (contrast_ratio − 1) / 20 × 100`, clamped 0–100. Ratio 21:1 → 100.
- **Semantic defaults**: light → diffAdded `#1f8a4c`, diffRemoved `#d13438`, skill `#b7791f`; dark → `#3fb950`, `#f85149`, `#d29922`. Shift hue toward the image palette but keep the green/red/amber roles and ensure readability on the surface.
- **opaqueWindows**: `true` for solid, readable surfaces; `false` enables translucency.
- **Fonts**: unknown font names fall back gracefully; prefer common stacks such as `Inter, system-ui, sans-serif` and `JetBrains Mono, SF Mono, Menlo, monospace`.

## Manual tuning

`build_theme.py` accepts `--accent`, `--surface`, `--ink`, `--font-ui`, `--font-code` overrides.
For finer control, edit `theme.json` directly and re-import; regenerate the import string by running:

```bash
python -c "import json,pathlib; t=json.loads(pathlib.Path('theme.json').read_text()); open('codex-theme-v1.txt','w').write('codex-theme-v1:'+json.dumps(t,separators=(',',':')))"
```

## Extending to full wallpaper skins

Native import only changes colors and fonts. Showing `background.png` behind the whole window
requires a community skin engine (e.g., Codex Dream Skin, Codex AutoSkin) that injects the artwork
at runtime. The pack from `build_theme.py` is compatible with those engines: `background.png` + `theme.json`.
