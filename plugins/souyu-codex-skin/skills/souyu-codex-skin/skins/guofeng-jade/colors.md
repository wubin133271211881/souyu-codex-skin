# 颜色表 · guofeng-jade（国风 · 青绿山水）

> 一套皮肤 = 颜色表（本文件是可视化视图，机器读取 `colors.json`）+ 图片（`light.jpg` / `dark.jpg`）。
> 改色或换图后运行：`python scripts\apply_skin.py --id guofeng-jade`（`--dry-run` 先预览）

## 原生主题（Settings → Appearance → Import）

| 角色 | light | dark |
| --- | --- | --- |
| accent（主角色） | #d9b426 | #5289e0 |
| surface（窗口底色） | #f8f2da | #081427 |
| ink（文字色） | #454d40 | #edf1f4 |
| contrast | 34 | 76 |
| semantic.diffAdded（新增行） | #1f8a4c | #3fb950 |
| semantic.diffRemoved（删除行） | #d13438 | #f85149 |
| semantic.skill（技能） | #b7791f | #d29922 |

## 面板调色板（24 键 × light/dark，注入 CSS 用）

| 键 | 用途 | light | dark |
| --- | --- | --- | --- |
| accent | 主角色：欢迎页建议卡图标 | #d9b426 | #5289e0 |
| bodyBg | 窗口底色 | #f8f2da | #081427 |
| bodyGlowA | 背景右上光晕 | rgba(217, 180, 38, 0.18) | rgba(82, 137, 224, 0.24) |
| bodyGlowB | 背景左上光晕 | rgba(239, 223, 164, 0.22) | rgba(82, 137, 224, 0.16) |
| asideA | 左侧栏渐变起点 | rgba(248, 242, 218, 0.96) | rgba(8, 20, 39, 0.97) |
| asideB | 左侧栏渐变终点 | rgba(242, 230, 182, 0.90) | rgba(30, 55, 94, 0.93) |
| border | 边框/分隔线 | rgba(239, 223, 164, 0.30) | rgba(82, 137, 224, 0.30) |
| topA | 顶部菜单栏渐变起点 | rgba(248, 242, 218, 0.97) | rgba(8, 20, 39, 0.97) |
| topB | 顶部菜单栏渐变终点 | rgba(242, 230, 182, 0.92) | rgba(30, 55, 94, 0.92) |
| mainA | 主内容区渐变 A | rgba(248, 242, 218, 0.97) | rgba(8, 20, 39, 0.97) |
| mainB | 主内容区渐变 B | rgba(242, 230, 182, 0.90) | rgba(23, 43, 76, 0.90) |
| mainC | 主内容区渐变 C | rgba(239, 223, 164, 0.55) | rgba(38, 67, 113, 0.70) |
| mainD | 主内容区渐变 D（叠加壁纸） | rgba(232, 211, 128, 0.30) | rgba(82, 137, 224, 0.45) |
| headerBg | 会话头部背景 | rgba(248, 242, 218, 0.85) | rgba(23, 43, 76, 0.88) |
| activeBg | 侧栏选中项/悬停 | rgba(239, 223, 164, 0.38) | rgba(82, 137, 224, 0.26) |
| cardBg | 设置/会话主表面 | rgba(248, 242, 218, 0.94) | rgba(8, 20, 39, 0.94) |
| cardBg2 | 次级表面 | rgba(242, 230, 182, 0.90) | rgba(30, 55, 94, 0.90) |
| utilityBg | 欢迎页 composer 工具条（任务 chip/完全访问/自定义高） | rgba(242, 230, 182, 0.90) | rgba(30, 55, 94, 0.90) |
| inputBg | 输入框/胶块 | rgba(242, 230, 182, 0.78) | rgba(45, 78, 132, 0.72) |
| topFade | 顶部淡出 | linear-gradient(to top, rgba(248, 242, 218, 0.95) 0%, rgba(248, 242, 218, 0.00) 100%) | linear-gradient(to top, rgba(8, 20, 39, 0.95) 0%, rgba(8, 20, 39, 0.00) 100%) |
| composerFade | 输入区底部淡出 | linear-gradient(to top, rgba(248, 242, 218, 0.95) 0%, rgba(239, 223, 164, 0.55) 50%, rgba(248, 242, 218, 0.00) 100%) | linear-gradient(to top, rgba(8, 20, 39, 0.95) 0%, rgba(30, 55, 94, 0.55) 50%, rgba(8, 20, 39, 0.00) 100%) |
| menuBg | 菜单栏菜单 + 下拉 | rgba(248, 242, 218, 0.98) | rgba(38, 67, 113, 0.97) |
| moduleBg | 设置模块卡 | rgba(242, 230, 182, 0.92) | rgba(30, 55, 94, 0.90) |
| buttonBg | 设置页按钮 | rgba(236, 217, 146, 0.20) | rgba(82, 137, 224, 0.22) |
| terminalBg | 终端框架/视口 | rgba(248, 242, 218, 0.96) | rgba(23, 43, 76, 0.97) |
| terminalInk | 终端文字 | #454d40 | #edf1f4 |
