# Codex 皮肤 · 颜色使用全盘点

> 日期：2026-08-13 · 适用版本：Codex 桌面应用 26.803，souyu-codex-skin 技能
> 结论先行：所有颜色都来自一张图。整条链路由 **图片 → 原生主题三色（accent/surface/ink）→ 24 键面板调色板 → CSS 注入** 逐层展开，最后统一落到各个 UI 表面。现在由 `scripts/create_skin.py` 一条命令完成全盘配色，不再需要逐个字段手填。

## 颜色分层总览

| 层 | 文件 | 内容 | 作用 |
| --- | --- | --- | --- |
| 0. 图片（源头） | `skins/<id>/light.jpg`、`dark.jpg`（压缩壁纸）；`outputs/<id>/raw/{light,dark}/`（原图） | 壁纸画面 | 窗口背景最上层；全部颜色的推导来源 |
| 1. 原生主题 | `outputs/<id>/pack/{light,dark}/theme.json` + `codex-theme-v1.txt` | accent / surface / ink / contrast / semanticColors / fonts | Settings → Appearance → Import 导入，控制文字可读性与全局强调色 |
| 2. 面板调色板 | `skins/<id>/skin.json` → `palette.light/dark` | 24 个键 | 注入 CSS 的全部颜色来源（背景/边框/渐变/终端） |
| 3. CSS 注入 | `scripts/style.template.css` → `style.css` → `inject.mjs` | `@@LIGHT_*@@`/`@@DARK_*@@` 占位符 | 按选择器覆盖各 UI 表面的背景/边框 |
| 4. 工具兜底 | `scripts/build_theme.py` 内的默认值 | 语义色、低饱和回退色 | 图片色彩不足时保持可读性与语义（绿=新增/红=删除/琥珀=技能） |

## 第 1 层：原生主题字段

| 字段 | 含义 | 生成来源 |
| --- | --- | --- |
| `theme.accent` | 全 App 强调色 | 图片中最饱和色，提饱和到 0.7 |
| `theme.surface` | 窗口底色（light 提亮 ≥0.75 亮度，dark 压暗 ≤0.05） | 图片最亮/最暗主色 |
| `theme.ink` | 文字色（light 压暗 ≤0.10，dark 提亮 ≥0.85，对比度 ≥7:1） | 图片最深/最浅主色 |
| `theme.contrast` | 对比度 0–100 | ink/surface 对比度换算 |
| `theme.semanticColors.diffAdded` | diff 新增行 | 图片绿色系，默认 light `#1f8a4c` / dark `#3fb950` |
| `theme.semanticColors.diffRemoved` | diff 删除行 | 图片红色系，默认 light `#d13438` / dark `#f85149` |
| `theme.semanticColors.skill` | 技能相关强调 | 图片琥珀色系，默认 light `#b7791f` / dark `#d29922` |
| `theme.fonts.ui/code` | UI / 代码字体 | 固定栈（Inter / JetBrains Mono） |

## 第 2 层：24 键面板调色板 → UI 位置映射

生成公式（`import_skin.py derive_palette`）：以 surface(S)、ink(I)、accent(A) 为基色，按固定比例混合出中间色并配固定透明度。
SA2/SA3/SA4/SA5 = S 与 A 按 0.2/0.3/0.4/0.5 混合。

| 键 | 作用位置（CSS 选择器 / 表面） | dark 透明度 | light 透明度 |
| --- | --- | --- | --- |
| `accent` | 新对话欢迎页 4 个建议卡图标（`section[class*="home-suggestions"] svg[class*="text-token-charts-"]`） | A 全量 | A 全量 |
| `bodyBg` | 窗口底色（`html.lite-skin body`） | S 全量 | S 全量 |
| `bodyGlowA` | 背景右上光晕（radial 82% 4%） | A @.24 | A @.18 |
| `bodyGlowB` | 背景左上光晕（radial 18% 0%） | A @.16 | SA3 @.22 |
| `asideA` | 左侧栏渐变起点（`aside.app-shell-left-panel`） | S @.97 | S @.96 |
| `asideB` | 左侧栏渐变终点 | SA3 @.93 | SA2 @.90 |
| `border` | 全部分隔线/边框（`border-token-border`、`after:bg-token-border::after`） | A @.30 | SA3 @.30 |
| `topA` | 顶部菜单栏渐变起点（`ApplicationMenuTopBar`） | S @.97 | S @.97 |
| `topB` | 顶部菜单栏渐变终点 | SA3 @.92 | SA2 @.92 |
| `mainA`–`mainD` | 主内容区四段渐变（`MainContentSurface`，叠加壁纸） | S/SA2/SA4/A | S/SA2/SA3/SA5 |
| `headerBg` | 会话头部（`MainContentSurface > header`） | SA2 @.88 | S @.85 |
| `activeBg` | 侧栏选中项（`aside [data-state="active"]`、建议卡 hover） | A @.26 | SA3 @.38 |
| `cardBg` | 设置/会话主表面（`bg-token-main-surface-primary`） | S @.94 | S @.94 |
| `cardBg2` | 次级表面（`bg-token-main-surface-secondary`） | SA3 @.90 | SA2 @.90 |
| `utilityBg` | 欢迎页 composer 工具条（任务 chip/完全访问/自定义高） | SA3 @.90 | SA2 @.90 |
| `inputBg` | 输入框/胶块（`bg-token-input-background`、`_ComposerLayoutRoot_`、`_ComposerLayoutBody_`） | SA5 @.72 | SA2 @.78 |
| `topFade` | 顶部淡出（`_MainContentTopFade_`） | S .95→0 渐变 | S .95→0 渐变 |
| `composerFade` | 输入区底部淡出（`bg-gradient-to-t from-token-main-surface-primary`） | S .95→SA3 .55→0 | S .95→SA3 .55→0 |
| `menuBg` | 菜单栏菜单 + Radix 下拉（`bg-token-application-menu-background`、`bg-token-dropdown-background`） | SA4 @.97 | S @.98 |
| `moduleBg` | 设置模块卡（`rounded-2xl overflow-hidden border-token-border`） | SA3 @.90 | SA2 @.92 |
| `buttonBg` | 设置页按钮（`bg-token-bg-fog`、`bg-token-foreground/5`） | A @.22 | SA4 @.20 |
| `terminalBg` | 终端框架/视口（`[class*="app-theme"]`、`.xterm-viewport`、`.xterm-screen`） | SA2 @.97 | S @.96 |
| `terminalInk` | 终端文字（`.xterm`、`.xterm-rows span`） | I（浅色） | I（深色） |

## 第 3 层：CSS 注入

- `scripts/style.template.css`：light/dark 两套规则，`@@LIGHT_ACCENT@@` 等占位符由 `switch_skin.py` 的 `TOKEN_MAP`（24 个 token → 调色板键）渲染成 `scripts/style.css`，再由 `inject.mjs` 注入运行中的应用。
- 模板内仅有的硬编码颜色（不跟图换色，属中性阴影）：
  - `.codex-skin-btn` → `box-shadow: 0 1px 3px rgba(0,0,0,.10)`
  - `.codex-skin-menu` → `box-shadow: 0 10px 30px rgba(0,0,0,.28)`

## 第 4 层：工具兜底色

`scripts/build_theme.py`：
- 低饱和图片回退强调色：light `#c85a3f` / dark `#e58e4c`（仅当图片主色饱和度 < 0.3 时启用）。
- `palette.png` 色板标签：深色底用白字 `#ffffff`、浅色底用黑字 `#111111`。

## 一键全盘配色

```powershell
python scripts\create_skin.py --light <light图> --dark <dark图> --id <id> --label "<中文名>"
```

一条命令完成：derive_theme ×2（原生主题）→ 原生包 ×2 → derive_palette ×2（24 键）→ 压缩壁纸 → 注册 `skins/<id>/` → 渲染 `style.css` → 切换生效 → 记录 `state.json`。

不带 `--dark` 时暗色复用亮色图；`--no-switch` 只注册不激活。验证：

```powershell
node scripts\check.mjs --port 9335
```

### 主角色覆盖

自动推导会选图片里最饱和的颜色作为 accent。人物/主题皮肤想让某一种颜色当主角（例如 sakura-cute 暗色要樱粉而非暗图里的蓝），可用 `--light-accent` / `--dark-accent`（或同时生效的 `--accent`）固定 accent，其余 22 键仍全部自动推导：

```powershell
python scripts\create_skin.py --light <light图> --dark <dark图> --id sakura-cute --label "春野樱 · 可爱粉" --dark-accent #f28fc6
```

## 皮肤 = 颜色表 + 图片

每套皮肤注册后自带一份颜色表，皮肤定义就两样东西：

| 文件 | 内容 | 谁读 |
| --- | --- | --- |
| `skins/<id>/colors.json` | 可编辑颜色表：原生三色/语义色 + 24 键面板（light/dark） | 机器（apply_skin.py） |
| `skins/<id>/colors.md` | 颜色表可视化视图（含每键用途说明） | 人（改色前先看它） |
| `skins/<id>/light.jpg`、`dark.jpg` | 亮/暗壁纸 | 注入器 |

改色：编辑 `colors.json`（或重新跑 `create_skin.py`）；换图：覆盖 `light.jpg` / `dark.jpg`。之后一条命令全部生效：

```powershell
python scripts\apply_skin.py --id <id>            # 应用
python scripts\apply_skin.py --id <id> --dry-run  # 先预览
```

`apply_skin.py` 会把 `colors.json` 同步进 `skin.json` 调色板、重渲染 `style.css`、复制壁纸到注入资产、更新 `state.json`、重生成原生导入串（`outputs/<id>/pack/*/codex-theme-v1.txt`），并刷新 `colors.md`。

老皮肤补全颜色表（新增键如 `utilityBg` 缺失时）：

```powershell
python scripts\sync_color_tables.py --all
```

已有颜色表的皮肤只合并缺失键并刷新 `colors.md`，不会覆盖手工改动。

## 审计结论（2026-08-13）

静态 + 动态（运行中 App 实测：主对话页 / 欢迎页 / avatar 浮层 / 皮肤切换菜单）扫描结果：所有 UI 背景/边框色均来自调色板，无遗漏的硬编码界面色。

有意不跟随皮肤的颜色（设计如此，勿当漏网）：

- 文字/正文颜色：走原生明暗调色板，保证可读性（技能规则：不覆盖字体色，终端文字除外）；
- "完全访问"权限徽标的橙红色：原生语义色；
- 消息/代码内容里的语法高亮色：属于内容本身；
- 切换器阴影 `rgba(0,0,0,.10)` / `rgba(0,0,0,.28)`：中性阴影；
- 工具兜底色：语义色默认值、低饱和回退强调色、`palette.png` 标签黑白字。
