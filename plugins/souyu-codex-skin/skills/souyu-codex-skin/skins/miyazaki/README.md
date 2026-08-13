# 宫崎骏治愈 (miyazaki)

内置预设皮肤：可爱的宫崎骏/吉卜力水彩风格 Codex 壁纸，带一个圆润六边形雪花小精灵吉祥物。

- `light.jpg` — 明亮版：夏日田园（蓝天白云、山丘、木屋、溪流），适合浅色模式
- `dark.jpg` — 夜间版：星空银河、弯月、萤火虫、村庄灯火，适合深色模式
- `skin.json` — 明暗两套完整配色（含 `accent`），注入后布局与字体颜色保持原生

本皮肤同时是 skill 的默认壁纸素材（`scripts/art.jpg` / `scripts/art-dark.jpg`）。

激活方式：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\switch_skin.ps1 -Name miyazaki -Port 9335
```

或在 Codex 左下角「皮肤」按钮中选择「宫崎骏治愈」。
