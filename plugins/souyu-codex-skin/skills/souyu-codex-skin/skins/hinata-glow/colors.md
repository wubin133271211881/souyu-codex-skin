# 颜色表 · hinata-glow（日向雏田 · 紫焰高光）

> 一套皮肤 = 颜色表（本文件是可视化视图，机器读取 `colors.json`）+ 图片（`light.jpg` / `dark.jpg`）。
> 改色或换图后运行：`python scripts\apply_skin.py --id hinata-glow`（`--dry-run` 先预览）

## 原生主题（Settings → Appearance → Import）

| 角色 | light | dark |
| --- | --- | --- |
| accent（主角色） | #e896dc | #8b5cf6 |
| surface（窗口底色） | #fdf2ff | #0e1035 |
| ink（文字色） | #241f45 | #eae6fb |
| contrast | 66 | 70 |
| semantic.diffAdded（新增行） | #1f8a4c | #3fb950 |
| semantic.diffRemoved（删除行） | #d13438 | #f85149 |
| semantic.skill（技能） | #b7791f | #d29922 |

## 面板调色板（24 键 × light/dark，注入 CSS 用）

| 键 | 用途 | light | dark |
| --- | --- | --- | --- |
| accent | 主角色：欢迎页建议卡图标 | #e896dc | #8b5cf6 |
| bodyBg | 窗口底色 | #fdf2ff | #0e1035 |
| bodyGlowA | 背景右上光晕 | rgba(232, 150, 220, .30) | rgba(139, 92, 246, .30) |
| bodyGlowB | 背景左上光晕 | rgba(196, 181, 253, .34) | rgba(99, 102, 241, .22) |
| asideA | 左侧栏渐变起点 | rgba(253, 242, 255, .96) | rgba(14, 16, 53, .97) |
| asideB | 左侧栏渐变终点 | rgba(250, 232, 252, .90) | rgba(49, 46, 129, .93) |
| border | 边框/分隔线 | rgba(214, 148, 205, .30) | rgba(139, 92, 246, .34) |
| topA | 顶部菜单栏渐变起点 | rgba(253, 242, 255, .97) | rgba(14, 16, 53, .97) |
| topB | 顶部菜单栏渐变终点 | rgba(250, 232, 252, .92) | rgba(67, 56, 202, .90) |
| mainA | 主内容区渐变 A | rgba(253, 242, 255, .97) | rgba(10, 12, 40, .97) |
| mainB | 主内容区渐变 B | rgba(250, 240, 254, .90) | rgba(30, 27, 105, .90) |
| mainC | 主内容区渐变 C | rgba(243, 220, 248, .55) | rgba(76, 60, 183, .72) |
| mainD | 主内容区渐变 D（叠加壁纸） | rgba(232, 179, 228, .32) | rgba(129, 84, 244, .48) |
| headerBg | 会话头部背景 | rgba(253, 242, 255, .85) | rgba(16, 18, 62, .88) |
| activeBg | 侧栏选中项/悬停 | rgba(232, 150, 220, .40) | rgba(139, 92, 246, .30) |
| cardBg | 设置/会话主表面 | rgba(253, 242, 255, .94) | rgba(16, 18, 62, .94) |
| cardBg2 | 次级表面 | rgba(250, 232, 252, .90) | rgba(30, 27, 105, .90) |
| utilityBg | 欢迎页 composer 工具条（任务 chip/完全访问/自定义高） | rgba(250, 232, 252, .90) | rgba(30, 27, 105, .90) |
| inputBg | 输入框/胶块 | rgba(250, 232, 252, .78) | rgba(49, 46, 129, .72) |
| topFade | 顶部淡出 | linear-gradient(rgba(253, 242, 255, .95), rgba(253, 242, 255, 0)) | linear-gradient(rgba(14, 16, 53, .95), rgba(14, 16, 53, 0)) |
| composerFade | 输入区底部淡出 | linear-gradient(to top, rgba(253, 242, 255, .95) 0%, rgba(253, 242, 255, .55) 50%, rgba(253, 242, 255, 0) 100%) | linear-gradient(to top, rgba(10, 12, 40, .95) 0%, rgba(30, 27, 105, .55) 50%, rgba(10, 12, 40, 0) 100%) |
| menuBg | 菜单栏菜单 + 下拉 | rgba(253, 242, 255, .98) | rgba(30, 27, 105, .97) |
| moduleBg | 设置模块卡 | rgba(250, 232, 252, .92) | rgba(30, 27, 105, .90) |
| buttonBg | 设置页按钮 | rgba(232, 150, 220, .20) | rgba(139, 92, 246, .24) |
| terminalBg | 终端框架/视口 | rgba(253, 242, 255, .96) | rgba(10, 12, 40, .97) |
| terminalInk | 终端文字 | #241f45 | #eae6fb |
