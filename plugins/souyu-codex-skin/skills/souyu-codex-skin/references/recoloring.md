# 整体改色方案（Recoloring scheme）

本技能对 Codex 桌面应用的完整改色方案。目标是：生成/注册一套皮肤后，
整个应用（侧边栏、顶栏、对话、输入框、设置页、菜单、终端）的颜色全部
跟随皮肤调色板，明暗模式各自成体系，且随时可切换。

## 原则

1. **只染背景/边框，不改文字色**（唯一例外：xterm 终端，见下文，因为它
   强制深色主题，必须同时给文字色才能保证浅色模式可读）。
2. **不重构布局**：只覆盖 `background` / `background-image` / `border-color`，
   不注入 UI、不移动元素。
3. **明暗分离**：每套皮肤同时提供 light/dark 两套调色板 + 两张壁纸；
   应用切换外观时壁纸与面板配色自动互换。
4. **不写 `config.toml`**：原生主题走官方导入串；壁纸走 CDP 注入。
5. **验证不调视觉模型**：只用 `check.mjs` 计算样式 + 截图给用户看。

## 架构（三层）

```text
图片 → build_theme.py → 原生主题包（surface/ink/accent，手动导入用）
   ↓ 同时
skins/<id>/skin.json（完整调色板）→ style.template.css → style.css
   ↓
inject.mjs 把 style.css + art.jpg/art-dark.jpg(base64) 注入运行中的应用
   ↓
check.mjs 核验计算样式；switch_skin.ps1 完成切换+重注入+核验
```

## 调色板字段（skin.json，light/dark 各一份）

| 字段 | 作用 | 示例（暗色） |
| --- | --- | --- |
| `accent` | 强调色（新对话欢迎页 4 个建议卡片的图标） | `#e58e4c` |
| `bodyBg` | 窗口底色 | `#141746` |
| `bodyGlowA` / `bodyGlowB` | 背景光晕（径向渐变） | `rgba(111,88,171,.24)` |
| `asideA` / `asideB` | 左侧栏渐变 | `rgba(20,23,70,.97)` |
| `topA` / `topB` | 顶栏渐变 | `rgba(20,23,70,.97)` |
| `border` | 边框/分割线 | `rgba(111,88,171,.30)` |
| `mainA`–`mainD` | 主区四段渐变（叠加壁纸） | `rgba(16,18,48,.97)`… |
| `headerBg` | 会话头部背景 | `rgba(24,26,74,.88)` |
| `activeBg` | 侧栏选中项 | `rgba(82,101,224,.26)` |
| `cardBg` | 设置页/大表面（`bg-token-main-surface-primary`） | `rgba(23,26,78,.94)` |
| `cardBg2` | 次级表面（`bg-token-main-surface-secondary`） | `rgba(31,29,82,.90)` |
| `utilityBg` | 欢迎页 composer 工具条（任务 chip / 完全访问 / 自定义 高） | `rgba(31,29,82,.90)` |
| `inputBg` | 输入框/输入胶囊（`bg-token-input-background`、`_ComposerLayoutRoot_`） | `rgba(41,36,101,.72)` |
| `topFade` | 顶部淡出渐变（`_MainContentTopFade_`） | `linear-gradient(...)` |
| `composerFade` | 输入区底部淡出（`bg-gradient-to-t from-token-main-surface-primary`） | `linear-gradient(to top, ...)` |
| `menuBg` | 菜单栏菜单 + Radix 下拉菜单 | `rgba(31,29,82,.97)` |
| `moduleBg` | 设置模块卡片（`rounded-2xl overflow-hidden border-token-border`） | `rgba(31,29,82,.90)` |
| `buttonBg` | 设置页按钮（`bg-token-bg-fog` / `bg-token-foreground/5`） | `rgba(111,88,171,.22)` |
| `terminalBg` | 终端框/视口（`[class*="app-theme"]`、`.xterm-viewport`、`.xterm-screen`） | `rgba(10,12,40,.97)` |
| `terminalInk` | 终端文字色（明暗各自保证可读） | `#e6e2f5` |

## 选择器映射（app 26.803）

`bg-token-*` 是编译后的静态类，**不是 CSS 变量**——覆盖必须用类名子串选择器，
不能用 `--token-*` 自定义属性：

| 表面 | 选择器 |
| --- | --- |
| 壁纸 + 主渐变 | `main[class*="MainContentSurface"]` |
| 左侧栏 | `aside.app-shell-left-panel` |
| 顶栏/标题栏 | `div[class*="ApplicationMenuTopBar"]`, `main[class*="MainContentSurface"] > header`（叠加 accent 光晕 + `moduleBg` 左侧染色，近黑皮肤下仍可见） |
| 输入框/输入胶囊 | `[class*="_ComposerLayoutRoot_"]`, `[class*="bg-token-input-background"]` |
| 欢迎页 composer 工具条（任务 chip / 完全访问 / 自定义 高） | `[class*="_ComposerHomeUtilityBar_"]`, `[class*="_ComposerFooter_"]`（原生 `rgb(246,246,246)`，需覆盖为 `utilityBg`） |
| 输入框内部 | `[class*="_ComposerLayoutBody_"]`（默认 oklab 背景，需染成 `inputBg`） |
| 新对话欢迎页表面 | `div[class*="home-main-content"]`（accent 光晕 + `moduleBg` 顶部染色） |
| 顶部淡出 | `[class*="_MainContentTopFade_"]` |
| 输入区底部淡出 | `[class*="bg-gradient-to-t"][class*="from-token-main-surface-primary"]` |
| 设置/会话表面 | `[class*="bg-token-main-surface-primary"]`, `[class*="bg-token-main-surface-secondary"]` |
| 菜单栏菜单（文件/帮助） | `[class*="bg-token-application-menu-background"]` |
| Radix 下拉（权限/推理/置顶/输出面板） | `[class*="bg-token-dropdown-background"]` |
| 设置模块卡片 | `[class*="rounded-2xl"][class*="overflow-hidden"][class*="border-token-border"]` |
| 设置按钮 | `[class*="bg-token-bg-fog"]`, `[class*="bg-token-foreground/5"]` |
| 模块分割线 | `[class*="after:bg-token-border"]::after` |
| 终端框/视口 | `[class*="app-theme"]`, `[class*="app-theme"] .xterm-viewport`, `[class*="app-theme"] .xterm-screen` |
| 新对话欢迎页建议卡片（4 个） | `section[class*="home-suggestions"] button`（背景/边框/hover）+ `section[class*="home-suggestions"] svg[class*="text-token-charts-"]`（图标 = `accent`） |
| 边框 | `[class*="border-token-border"]` |

## 特殊组件

- **xterm 终端**：容器 `app-theme electron-dark` 强制深色；`.xterm-viewport`
  硬编码 `rgb(0,0,0)`。处理：把视口背景换成 `terminalBg`，并把
  `.xterm`/`.xterm-rows span` 文字色设为 `terminalInk`。浅色模式下文字会被
  统一压成深靛紫（ANSI 彩色会扁平化，可读性优先）。
- **两类菜单表面**：菜单栏菜单用 `bg-token-application-menu-background`，
  Radix 下拉用 `bg-token-dropdown-background`，两条规则都要有。
- **底部淡出**：输入区下方两层淡出是编译黑色渐变，用
  `[class*="bg-gradient-to-t"][class*="from-token-main-surface-primary"]` 覆盖。

## 新增一套皮肤的步骤

1. 用 `souyu-image-2` 出图（**提示词一律用中文**；16:9、主体靠右、无文字水印；暗色月夜 + 浅色樱花各一张，示例见 `SKILL.md`）。
2. `python scripts/prepare_art.py <light> --dark <dark>` 压缩壁纸。
3. 复制 `skins/hinata-adult/` 为 `skins/<id>/`，替换 jpg，按上面字段表填
   `skin.json`（从图提取主色，参考 `build_theme.py` 的推导逻辑）。
4. 切换：
   `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\switch_skin.ps1 -Name <id> -Port 9335`
5. 核验：`node scripts\check.mjs --port 9335`，再人工看截图确认各区域。

## 导入历史皮肤（import_skin.py）

以前线程生成过的皮肤包（含 `theme.json` + `background.png`，或
`dark/`、`light/` 子目录，或 `*-dark.png`/`*-light.png` 命名）可以直接注册进
切换器：

```powershell
python scripts\import_skin.py --scan --base C:\Users\wubin\Documents\Codex
python scripts\import_skin.py --source <pack目录> [--id <id>] [--label <中文名>]
```

规则：
- `--scan` 递归找 `theme.json`，把 `-dark`/`-light` 后缀的同 id 兄弟目录合并成一套；
- 缺明暗某一侧配色时，用 `build_theme.py` 从对应壁纸推导 surface/ink/accent；
- 由 (surface, ink, accent) 按统一公式渲染 24 键调色板（alpha 混合参考本文表格）；
- 壁纸压缩为 `skins/<id>/light.jpg` / `dark.jpg`；
- 已注册的 id 自动跳过；注册后 `switch_skin.ps1 -Name <id>` 即可切换。

删除已注册皮肤（若删除的是当前皮肤，会自动先切到另一套）：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\switch_skin.ps1 -Remove <id>
```

最后一套皮肤不允许删除；删除后注入器自动重启，侧边栏列表同步刷新。

## 应用内切换（侧边栏皮肤按钮）

注入器会在左侧栏底部（个人资料行上方）放一个「皮肤」按钮，点击弹出所有已
注册皮肤，点选即切换；控件颜色跟随当前皮肤调色板，应用重启/页面刷新后自动
重新注入。

实现要点：
- 控件样式在 `style.template.css` 里（`.codex-skin-switcher` 等），复用
  `CARD_BG2` / `MENU_BG` / `ACTIVE_BG` / `BORDER` / `BODY_GLOW_A` 等字段；
- `inject.mjs` 在 `--watch` 模式下注入控件 DOM + 事件；
- **app:// 页面 CSP 禁止 fetch 到回环 HTTP**（实测 "Failed to fetch"），所以
  控件点击只写 `window.__codexSkinPending`，注入器轮询发现后执行
  `switch_skin.py` 并重新注入，绕开 CSP；
- 切换流程：点选 → 轮询(≤2s) → 渲染新 style.css/壁纸 → 重注入全部会话。

## 启动加载与自愈

- **两步启动（设计如此）**：Codex 先普通启动 → 守护进程检测无调试端口 →
  用 `--remote-debugging-port` 重启并注入，打开后约 30–60 秒皮肤出现、窗口
  会重启一次。不是 bug，不用处理。
- **开机自启**：`scripts/autostart.vbs` 是隐藏启动模板；`start.ps1` 会把它
  复制到 `启动\CodexLiteSkinWatcher.vbs`，`restore.ps1` 会删除它。
- **控件自愈**：切换明暗/React 重建侧栏可能移除「皮肤」按钮，注入器每 2 秒
  巡检，丢失即重新注入（实测 6 秒内恢复）。
- **导入兜底**：`import_skin.find_art` 对 split 包（dark/ + light/ 兄弟目录）
  按目录顺序分别取明暗图；若把第一张 background.png 同时赋给两个变体，会
  导致明暗壁纸相同（曾发生在妲己/公孙离/不知火舞，已修复并全量核验）。

## 验证清单

- `liteSkinClass: true`，`styleLen > 0`。
- 侧边栏/顶栏/主区/头部计算背景为皮肤渐变。
- 输入框、输入胶囊为 `inputBg`；顶部/底部淡出为皮肤渐变。
- 打开设置（Ctrl+,）：表面 `cardBg`、模块卡片 `moduleBg`、按钮 `buttonBg`。
- 打开菜单（权限/推理/置顶/文件/帮助）：均为 `menuBg`。
- 打开终端（有命令运行时）：框/视口 `terminalBg`，文字 `terminalInk`，明暗各验一次。

## 常见坑

- `Set-Content -Encoding utf8`（PS5.1）写 BOM → Python 读 state.json 用 `utf-8-sig`。
- PowerShell 读无 BOM UTF-8 必须 `-Encoding UTF8`，否则中文 JSON 按 GBK 解码会坏。
- Python 打印中文前设 `$env:PYTHONIOENCODING='utf-8'`。
- Radix 菜单不吃 `el.click()`，验证要发真实 CDP 鼠标事件
  （`Input.dispatchMouseEvent`）。左下角头像菜单合成事件也打不开，按共享类规则覆盖即可。
- 应用升级导致类名变化时，按本表重新扫 DOM 并更新 `style.template.css`。

## 一键全盘配色（create_skin.py）

新增皮肤不再需要手工填 24 键：直接给图，一条命令生成全部颜色并注册/切换。

```powershell
python scripts\create_skin.py --light <light图> --dark <dark图> --id <id> --label "<中文名>" [--dark-accent #hex]
```

做了什么：

1. `build_theme.derive_theme` 从每张图推导原生主题三色（accent/surface/ink + 语义色），写出 `outputs/<id>/pack/{light,dark}/` 原生包；
2. `import_skin.derive_palette` 从三色渲染完整 24 键 light/dark 调色板；
3. 压缩壁纸到 `skins/<id>/light.jpg|dark.jpg`，写 `skin.json`；
4. 输出 `outputs/<id>/palette-preview.png` 供目检；
5. 默认直接 `switch_skin.switch` 生效（`--no-switch` 只注册）。

自动 accent 取图片最饱和色；人物皮肤想固定主角色用 `--light-accent` / `--dark-accent`（或 `--accent` 双端），其余 23 键仍全自动。验证照旧：`node scripts\check.mjs --port 9335`。

## 皮肤 = 颜色表 + 图片（apply_skin.py）

每套皮肤注册后自带颜色表：

- `skins/<id>/colors.json` — 可编辑颜色表（机器读取：原生三色/语义色 + 24 键面板，light/dark）；
- `skins/<id>/colors.md` — 颜色表可视化视图（自动生成）；
- `skins/<id>/light.jpg|dark.jpg` — 图片。

改色/换图后一条命令生效：

```powershell
python scripts\apply_skin.py --id <id>            # 应用
python scripts\apply_skin.py --id <id> --dry-run  # 预览
```

它会把 `colors.json` 同步进 `skin.json`、重渲染 `style.css`、复制壁纸、更新 state、重生成原生导入串与 `colors.md`。

老皮肤补颜色表（`utilityBg` 等新键缺失时）：

```powershell
python scripts\sync_color_tables.py --all
```

已有颜色表的皮肤只合并缺失键并刷新 `colors.md`，不会覆盖手工改动。
