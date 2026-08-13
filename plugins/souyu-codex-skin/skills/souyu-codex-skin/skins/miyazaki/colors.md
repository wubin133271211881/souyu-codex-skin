# 颜色表 · miyazaki（宫崎骏治愈）

> 一套皮肤 = 颜色表（本文件是可视化视图，机器读取 `colors.json`）+ 图片（`light.jpg` / `dark.jpg`）。
> 改色或换图后运行：`python scripts\apply_skin.py --id miyazaki`（`--dry-run` 先预览）

## 原生主题（Settings → Appearance → Import）

| 角色 | light | dark |
| --- | --- | --- |
| accent（主角色） | #2189bf | #527de0 |
| surface（窗口底色） | #e2f0d7 | #021128 |
| ink（文字色） | #2d4d39 | #f0f1f6 |
| contrast | 35 | 79 |
| semantic.diffAdded（新增行） | #1f8a4c | #3fb950 |
| semantic.diffRemoved（删除行） | #d13438 | #f85149 |
| semantic.skill（技能） | #b7791f | #d29922 |

## 面板调色板（24 键 × light/dark，注入 CSS 用）

| 键 | 用途 | light | dark |
| --- | --- | --- | --- |
| accent | 主角色：欢迎页建议卡图标 | #2189bf | #527de0 |
| bodyBg | 窗口底色 | #e2f0d7 | #021128 |
| bodyGlowA | 背景右上光晕 | rgba(33, 137, 191, 0.18) | rgba(82, 125, 224, 0.24) |
| bodyGlowB | 背景左上光晕 | rgba(168, 209, 208, 0.22) | rgba(82, 125, 224, 0.16) |
| asideA | 左侧栏渐变起点 | rgba(226, 240, 215, 0.96) | rgba(2, 17, 40, 0.97) |
| asideB | 左侧栏渐变终点 | rgba(187, 219, 210, 0.90) | rgba(26, 49, 95, 0.93) |
| border | 边框/分隔线 | rgba(168, 209, 208, 0.30) | rgba(82, 125, 224, 0.30) |
| topA | 顶部菜单栏渐变起点 | rgba(226, 240, 215, 0.97) | rgba(2, 17, 40, 0.97) |
| topB | 顶部菜单栏渐变终点 | rgba(187, 219, 210, 0.92) | rgba(26, 49, 95, 0.92) |
| mainA | 主内容区渐变 A | rgba(226, 240, 215, 0.97) | rgba(2, 17, 40, 0.97) |
| mainB | 主内容区渐变 B | rgba(187, 219, 210, 0.90) | rgba(18, 39, 77, 0.90) |
| mainC | 主内容区渐变 C | rgba(168, 209, 208, 0.55) | rgba(34, 60, 114, 0.70) |
| mainD | 主内容区渐变 D（叠加壁纸） | rgba(130, 188, 203, 0.30) | rgba(82, 125, 224, 0.45) |
| headerBg | 会话头部背景 | rgba(226, 240, 215, 0.85) | rgba(18, 39, 77, 0.88) |
| activeBg | 侧栏选中项/悬停 | rgba(168, 209, 208, 0.38) | rgba(82, 125, 224, 0.26) |
| cardBg | 设置/会话主表面 | rgba(226, 240, 215, 0.94) | rgba(2, 17, 40, 0.94) |
| cardBg2 | 次级表面 | rgba(187, 219, 210, 0.90) | rgba(26, 49, 95, 0.90) |
| utilityBg | 欢迎页 composer 工具条（任务 chip/完全访问/自定义高） | rgba(187, 219, 210, 0.90) | rgba(26, 49, 95, 0.90) |
| inputBg | 输入框/胶块 | rgba(187, 219, 210, 0.78) | rgba(42, 71, 132, 0.72) |
| topFade | 顶部淡出 | linear-gradient(to top, rgba(226, 240, 215, 0.95) 0%, rgba(226, 240, 215, 0.00) 100%) | linear-gradient(to top, rgba(2, 17, 40, 0.95) 0%, rgba(2, 17, 40, 0.00) 100%) |
| composerFade | 输入区底部淡出 | linear-gradient(to top, rgba(226, 240, 215, 0.95) 0%, rgba(168, 209, 208, 0.55) 50%, rgba(226, 240, 215, 0.00) 100%) | linear-gradient(to top, rgba(2, 17, 40, 0.95) 0%, rgba(26, 49, 95, 0.55) 50%, rgba(2, 17, 40, 0.00) 100%) |
| menuBg | 菜单栏菜单 + 下拉 | rgba(226, 240, 215, 0.98) | rgba(34, 60, 114, 0.97) |
| moduleBg | 设置模块卡 | rgba(187, 219, 210, 0.92) | rgba(26, 49, 95, 0.90) |
| buttonBg | 设置页按钮 | rgba(149, 199, 205, 0.20) | rgba(82, 125, 224, 0.22) |
| terminalBg | 终端框架/视口 | rgba(226, 240, 215, 0.96) | rgba(18, 39, 77, 0.97) |
| terminalInk | 终端文字 | #2d4d39 | #f0f1f6 |
