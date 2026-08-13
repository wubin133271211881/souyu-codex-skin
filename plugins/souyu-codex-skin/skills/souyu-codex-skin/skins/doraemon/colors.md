# 颜色表 · doraemon（哆啦A梦 · 童趣蓝）

> 一套皮肤 = 颜色表（本文件是可视化视图，机器读取 `colors.json`）+ 图片（`light.jpg` / `dark.jpg`）。
> 改色或换图后运行：`python scripts\apply_skin.py --id doraemon`（`--dry-run` 先预览）

## 原生主题（Settings → Appearance → Import）

| 角色 | light | dark |
| --- | --- | --- |
| accent（主角色） | #218cbf | #5273e0 |
| surface（窗口底色） | #f4f3ed | #000926 |
| ink（文字色） | #36525e | #edf1f9 |
| contrast | 32 | 82 |
| semantic.diffAdded（新增行） | #1f8a4c | #3fb950 |
| semantic.diffRemoved（删除行） | #d13438 | #f85149 |
| semantic.skill（技能） | #b7791f | #d29922 |

## 面板调色板（24 键 × light/dark，注入 CSS 用）

| 键 | 用途 | light | dark |
| --- | --- | --- | --- |
| accent | 主角色：欢迎页建议卡图标 | #218cbf | #5273e0 |
| bodyBg | 窗口底色 | #f4f3ed | #000926 |
| bodyGlowA | 背景右上光晕 | rgba(33, 140, 191, 0.18) | rgba(82, 115, 224, 0.24) |
| bodyGlowB | 背景左上光晕 | rgba(181, 212, 223, 0.22) | rgba(82, 115, 224, 0.16) |
| asideA | 左侧栏渐变起点 | rgba(244, 243, 237, 0.96) | rgba(0, 9, 38, 0.97) |
| asideB | 左侧栏渐变终点 | rgba(202, 222, 228, 0.90) | rgba(25, 41, 94, 0.93) |
| border | 边框/分隔线 | rgba(181, 212, 223, 0.30) | rgba(82, 115, 224, 0.30) |
| topA | 顶部菜单栏渐变起点 | rgba(244, 243, 237, 0.97) | rgba(0, 9, 38, 0.97) |
| topB | 顶部菜单栏渐变终点 | rgba(202, 222, 228, 0.92) | rgba(25, 41, 94, 0.92) |
| mainA | 主内容区渐变 A | rgba(244, 243, 237, 0.97) | rgba(0, 9, 38, 0.97) |
| mainB | 主内容区渐变 B | rgba(202, 222, 228, 0.90) | rgba(16, 30, 75, 0.90) |
| mainC | 主内容区渐变 C | rgba(181, 212, 223, 0.55) | rgba(33, 51, 112, 0.70) |
| mainD | 主内容区渐变 D（叠加壁纸） | rgba(138, 192, 214, 0.30) | rgba(82, 115, 224, 0.45) |
| headerBg | 会话头部背景 | rgba(244, 243, 237, 0.85) | rgba(16, 30, 75, 0.88) |
| activeBg | 侧栏选中项/悬停 | rgba(181, 212, 223, 0.38) | rgba(82, 115, 224, 0.26) |
| cardBg | 设置/会话主表面 | rgba(244, 243, 237, 0.94) | rgba(0, 9, 38, 0.94) |
| cardBg2 | 次级表面 | rgba(202, 222, 228, 0.90) | rgba(25, 41, 94, 0.90) |
| utilityBg | 欢迎页 composer 工具条（任务 chip/完全访问/自定义高） | rgba(202, 222, 228, 0.90) | rgba(25, 41, 94, 0.90) |
| inputBg | 输入框/胶块 | rgba(202, 222, 228, 0.78) | rgba(41, 62, 131, 0.72) |
| topFade | 顶部淡出 | linear-gradient(to top, rgba(244, 243, 237, 0.95) 0%, rgba(244, 243, 237, 0.00) 100%) | linear-gradient(to top, rgba(0, 9, 38, 0.95) 0%, rgba(0, 9, 38, 0.00) 100%) |
| composerFade | 输入区底部淡出 | linear-gradient(to top, rgba(244, 243, 237, 0.95) 0%, rgba(181, 212, 223, 0.55) 50%, rgba(244, 243, 237, 0.00) 100%) | linear-gradient(to top, rgba(0, 9, 38, 0.95) 0%, rgba(25, 41, 94, 0.55) 50%, rgba(0, 9, 38, 0.00) 100%) |
| menuBg | 菜单栏菜单 + 下拉 | rgba(244, 243, 237, 0.98) | rgba(33, 51, 112, 0.97) |
| moduleBg | 设置模块卡 | rgba(202, 222, 228, 0.92) | rgba(25, 41, 94, 0.90) |
| buttonBg | 设置页按钮 | rgba(160, 202, 219, 0.20) | rgba(82, 115, 224, 0.22) |
| terminalBg | 终端框架/视口 | rgba(244, 243, 237, 0.96) | rgba(16, 30, 75, 0.97) |
| terminalInk | 终端文字 | #36525e | #edf1f9 |
