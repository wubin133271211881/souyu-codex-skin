# How Codex Lite Skin works

## Mechanism

The Codex desktop app is an Electron app. When launched with
`--remote-debugging-port=9335`, it exposes Chrome DevTools Protocol (CDP) on
loopback only. `inject.mjs` connects to the main renderer (`app://-/index.html`)
and injects a single `<style id="codex-lite-skin-style">` plus an
`html.lite-skin` class. The style:

- paints the artwork (embedded as JPEG data URIs) on
  `main[class*="MainContentSurface"]` with a left-heavy white gradient for
  readability;
- tints `aside.app-shell-left-panel` and
  `div[class*="ApplicationMenuTopBar"]` pink;
- adds a soft pink glow on `body`.

No DOM restructuring, no injected decorations, no file changes to the app
bundle or `config.toml`.

## Light / dark adaptivity

The app toggles `electron-light` / `electron-dark` on the `<html>` element when
the user switches Appearance mode. The style ships two variants:

- `html.lite-skin.electron-light` — pink-white pastel backgrounds with the
  light artwork (`art.jpg`, placeholder `__ART__`);
- `html.lite-skin.electron-dark` — deep pink-plum tinted backgrounds with the
  dark artwork (`art-dark.jpg`, placeholder `__ART_DARK__`; falls back to
  `art.jpg` when missing).

Font colors and control colors are never overridden, so they keep the app's own
light/dark palette and stay readable on both variants.

## Selectors (current app 26.803)

| Area | Selector |
| --- | --- |
| Main surface | `main[class*="MainContentSurface"]` |
| Left sidebar | `aside.app-shell-left-panel` |
| Top menu bar | `div[class*="ApplicationMenuTopBar"]` |
| Inner header | `main[class*="MainContentSurface"] > header` |

Class names are hashed by CSS modules but keep a readable fragment
(`MainContentSurface`, `ApplicationMenuTopBar`); the `[class*="..."]` match
survives hash changes.

## Persistence

`start.ps1` restarts Codex with the debugging port once, then starts:

- `inject.mjs --watch` — keeps the style applied and re-injects on page reloads;
- `watch.ps1` — a hidden keeper: if Codex is later launched normally (no debug
  port), it restarts Codex through the launcher so the skin returns.

Runtime state lives in `%LOCALAPPDATA%\CodexLiteSkin\state.json` and
`injector.log` / `injector-error.log`.

## Troubleshooting

- **Background not visible**: verify `html` has `lite-skin` class and the
  `#codex-lite-skin-style` tag exists; check `injector-error.log`.
- **App updated and skin stopped matching**: update `scripts/style.css`
  selectors for the new DOM; re-run `start.ps1`.
- **Port 9335 busy**: pass a different `-Port` to all scripts (start, watch,
  check, restore).
- **Settings pages stay clean**: the style intentionally does not paint the
  Settings page; the background shows on Home and conversation views.
