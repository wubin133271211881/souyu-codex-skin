# 颜色表 · hinata-adult（日向雏田 · 月夜紫）

> 一套皮肤 = 颜色表（本文件是可视化视图，机器读取 `colors.json`）+ 图片（`light.jpg` / `dark.jpg`）。
> 改色或换图后运行：`python scripts\apply_skin.py --id hinata-adult`（`--dry-run` 先预览）

## 原生主题（Settings → Appearance → Import）

| 角色 | light | dark |
| --- | --- | --- |
| accent（主角色） | #ba98cb | #6f58ab |
| surface（窗口底色） | #fbf3f9 | #141746 |
| ink（文字色） | #241f45 | #e6e2f5 |
| contrast | 66 | 62 |
| semantic.diffAdded（新增行） | #1f8a4c | #3fb950 |
| semantic.diffRemoved（删除行） | #d13438 | #f85149 |
| semantic.skill（技能） | #b7791f | #d29922 |

## 面板调色板（24 键 × light/dark，注入 CSS 用）

| 键 | 用途 | light | dark |
| --- | --- | --- | --- |
| accent | 主角色：欢迎页建议卡图标 | #ba98cb | #6f58ab |
| bodyBg | 窗口底色 | #fbf3f9 | #141746 |
| bodyGlowA | 背景右上光晕 | rgba(186, 152, 203, .28) | rgba(111, 88, 171, .24) |
| bodyGlowB | 背景左上光晕 | rgba(215, 209, 247, .32) | rgba(82, 101, 224, .16) |
| asideA | 左侧栏渐变起点 | rgba(251, 243, 249, .96) | rgba(20, 23, 70, .97) |
| asideB | 左侧栏渐变终点 | rgba(244, 231, 247, .90) | rgba(41, 36, 101, .93) |
| border | 边框/分隔线 | rgba(154, 134, 175, .28) | rgba(111, 88, 171, .30) |
| topA | 顶部菜单栏渐变起点 | rgba(251, 243, 249, .97) | rgba(20, 23, 70, .97) |
| topB | 顶部菜单栏渐变终点 | rgba(244, 231, 247, .92) | rgba(49, 51, 128, .92) |
| mainA | 主内容区渐变 A | rgba(251, 243, 249, .97) | rgba(16, 18, 48, .97) |
| mainB | 主内容区渐变 B | rgba(248, 240, 249, .90) | rgba(31, 29, 82, .90) |
| mainC | 主内容区渐变 C | rgba(238, 224, 242, .55) | rgba(61, 48, 122, .70) |
| mainD | 主内容区渐变 D（叠加壁纸） | rgba(222, 187, 224, .30) | rgba(82, 101, 224, .45) |
| headerBg | 会话头部背景 | rgba(251, 243, 249, .85) | rgba(24, 26, 74, .88) |
| activeBg | 侧栏选中项/悬停 | rgba(186, 152, 203, .38) | rgba(82, 101, 224, .26) |
| cardBg | 设置/会话主表面 | rgba(251, 243, 249, .94) | rgba(23, 26, 78, .94) |
| cardBg2 | 次级表面 | rgba(244, 231, 247, .90) | rgba(31, 29, 82, .90) |
| utilityBg | 欢迎页 composer 工具条（任务 chip/完全访问/自定义高） | rgba(244, 231, 247, .90) | rgba(31, 29, 82, .90) |
| inputBg | 输入框/胶块 | rgba(244, 231, 247, .78) | rgba(41, 36, 101, .72) |
| topFade | 顶部淡出 | linear-gradient(rgba(251, 243, 249, .95), rgba(251, 243, 249, 0)) | linear-gradient(rgba(20, 23, 70, .95), rgba(20, 23, 70, 0)) |
| composerFade | 输入区底部淡出 | linear-gradient(to top, rgba(251, 243, 249, .95) 0%, rgba(251, 243, 249, .55) 50%, rgba(251, 243, 249, 0) 100%) | linear-gradient(to top, rgba(16, 18, 48, .95) 0%, rgba(31, 29, 82, .55) 50%, rgba(16, 18, 48, 0) 100%) |
| menuBg | 菜单栏菜单 + 下拉 | rgba(251, 243, 249, .98) | rgba(31, 29, 82, .97) |
| moduleBg | 设置模块卡 | rgba(244, 231, 247, .92) | rgba(31, 29, 82, .90) |
| buttonBg | 设置页按钮 | rgba(186, 152, 203, .18) | rgba(111, 88, 171, .22) |
| terminalBg | 终端框架/视口 | rgba(251, 243, 249, .96) | rgba(10, 12, 40, .97) |
| terminalInk | 终端文字 | #241f45 | #e6e2f5 |
