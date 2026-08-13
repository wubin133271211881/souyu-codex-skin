# 颜色表 · gongsunli-codex-skin（公孙离 · 卡通粉）

> 一套皮肤 = 颜色表（本文件是可视化视图，机器读取 `colors.json`）+ 图片（`light.jpg` / `dark.jpg`）。
> 改色或换图后运行：`python scripts\apply_skin.py --id gongsunli-codex-skin`（`--dry-run` 先预览）

## 原生主题（Settings → Appearance → Import）

| 角色 | light | dark |
| --- | --- | --- |
| accent（主角色） | #d94a5f | #e05290 |
| surface（窗口底色） | #fefbf7 | #110c23 |
| ink（文字色） | #8a2a36 | #f5ecf0 |
| contrast | 36 | 77 |
| semantic.diffAdded（新增行） | #1f8a4c | #3fb950 |
| semantic.diffRemoved（删除行） | #d13438 | #f85149 |
| semantic.skill（技能） | #b7791f | #d29922 |

## 面板调色板（24 键 × light/dark，注入 CSS 用）

| 键 | 用途 | light | dark |
| --- | --- | --- | --- |
| accent | 主角色：欢迎页建议卡图标 | #d94a5f | #e05290 |
| bodyBg | 窗口底色 | #fefbf7 | #110c23 |
| bodyGlowA | 背景右上光晕 | rgba(217, 74, 95, 0.18) | rgba(224, 82, 144, 0.24) |
| bodyGlowB | 背景左上光晕 | rgba(243, 198, 201, 0.22) | rgba(224, 82, 144, 0.16) |
| asideA | 左侧栏渐变起点 | rgba(254, 251, 247, 0.96) | rgba(17, 12, 35, 0.97) |
| asideB | 左侧栏渐变终点 | rgba(247, 216, 217, 0.90) | rgba(79, 33, 68, 0.93) |
| border | 边框/分隔线 | rgba(243, 198, 201, 0.30) | rgba(224, 82, 144, 0.30) |
| topA | 顶部菜单栏渐变起点 | rgba(254, 251, 247, 0.97) | rgba(17, 12, 35, 0.97) |
| topB | 顶部菜单栏渐变终点 | rgba(247, 216, 217, 0.92) | rgba(79, 33, 68, 0.92) |
| mainA | 主内容区渐变 A | rgba(254, 251, 247, 0.97) | rgba(17, 12, 35, 0.97) |
| mainB | 主内容区渐变 B | rgba(247, 216, 217, 0.90) | rgba(58, 26, 57, 0.90) |
| mainC | 主内容区渐变 C | rgba(243, 198, 201, 0.55) | rgba(100, 40, 79, 0.70) |
| mainD | 主内容区渐变 D（叠加壁纸） | rgba(236, 162, 171, 0.30) | rgba(224, 82, 144, 0.45) |
| headerBg | 会话头部背景 | rgba(254, 251, 247, 0.85) | rgba(58, 26, 57, 0.88) |
| activeBg | 侧栏选中项/悬停 | rgba(243, 198, 201, 0.38) | rgba(224, 82, 144, 0.26) |
| cardBg | 设置/会话主表面 | rgba(254, 251, 247, 0.94) | rgba(17, 12, 35, 0.94) |
| cardBg2 | 次级表面 | rgba(247, 216, 217, 0.90) | rgba(79, 33, 68, 0.90) |
| utilityBg | 欢迎页 composer 工具条（任务 chip/完全访问/自定义高） | rgba(247, 216, 217, 0.90) | rgba(79, 33, 68, 0.90) |
| inputBg | 输入框/胶块 | rgba(247, 216, 217, 0.78) | rgba(120, 47, 90, 0.72) |
| topFade | 顶部淡出 | linear-gradient(to top, rgba(254, 251, 247, 0.95) 0%, rgba(254, 251, 247, 0.00) 100%) | linear-gradient(to top, rgba(17, 12, 35, 0.95) 0%, rgba(17, 12, 35, 0.00) 100%) |
| composerFade | 输入区底部淡出 | linear-gradient(to top, rgba(254, 251, 247, 0.95) 0%, rgba(243, 198, 201, 0.55) 50%, rgba(254, 251, 247, 0.00) 100%) | linear-gradient(to top, rgba(17, 12, 35, 0.95) 0%, rgba(79, 33, 68, 0.55) 50%, rgba(17, 12, 35, 0.00) 100%) |
| menuBg | 菜单栏菜单 + 下拉 | rgba(254, 251, 247, 0.98) | rgba(100, 40, 79, 0.97) |
| moduleBg | 设置模块卡 | rgba(247, 216, 217, 0.92) | rgba(79, 33, 68, 0.90) |
| buttonBg | 设置页按钮 | rgba(239, 180, 186, 0.20) | rgba(224, 82, 144, 0.22) |
| terminalBg | 终端框架/视口 | rgba(254, 251, 247, 0.96) | rgba(58, 26, 57, 0.97) |
| terminalInk | 终端文字 | #8a2a36 | #f5ecf0 |
