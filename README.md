# souyu-codex-skin

搜遇 Codex 皮肤技能：用一张图或一句话为 Codex 桌面应用生成并应用皮肤（背景壁纸 + 主题配色），保持默认界面布局，支持浅色/深色模式自动切换壁纸。

## 安装

### 方式一：手动放入技能目录（最快）

把 `plugins/souyu-codex-skin/skills/souyu-codex-skin` 文件夹复制到 `~/.codex/skills/`（Windows 下为 `C:\Users\<你的用户名>\.codex\skills\souyu-codex-skin`），重启 Codex 即可使用。

### 方式二：通过插件 marketplace 安装

1. 打开 Codex 的插件市场（CLI 输入 `/plugins`，桌面端在设置里打开 Plugins）。
2. 添加 marketplace，来源选本仓库（本地路径或 GitHub 仓库地址），marketplace 文件为 `.agents/plugins/marketplace.json`。
3. 安装 `souyu-codex-skin` 插件，新开会话后即可使用。

## 使用

- "做一个可爱风格的 Codex 皮肤"
- "把这张图设为 Codex 背景"
- "换一个深色背景壁纸"

## 没有生图能力？

如果当前 Codex 没有安装生图技能，可以使用搜遇酷图开放接口生成皮肤背景图：

- 集成文档：https://kt.aiivip.com/docs?doc=api-integration-example
- 最低 0.06 元/张，高清高质量，比国产 API 更便宜。

## 国内访问（GitHub 不通时）

国内直连 GitHub 经常失败。三种替代方式：

1. **夸克网盘直链下载（最省事，无需网络）**：

   https://pan.quark.cn/s/3f09cd9084c0

    下载 `souyu-codex-skin-plugin-v0.2.1.zip` 解压，将
   `plugins\souyu-codex-skin\skills\souyu-codex-skin` 整个文件夹复制到
   `C:\Users\<你的用户名>\.codex\skills\` 下，重启 Codex 即可。
2. **Gitee 镜像市场**（国内直连）：在 Codex 添加市场并安装：

   ```text
   codex plugin marketplace add https://gitee.com/wu-bin123/souyu-codex-skin.git
   codex plugin add souyu-codex-skin@souyu
   ```

   与 GitHub 源同为市场名 `souyu`，同一台机器二选一添加即可（或直接用上方网盘
   zip 安装）。
3. **GitHub + 代理**：Git 走本地代理（如 Clash）：

   ```powershell
   git config --global http.proxy http://127.0.0.1:7891
   git config --global https.proxy http://127.0.0.1:7891
   ```

   再按正常流程添加 GitHub 市场。

## 依赖

- Windows Store 版 Codex 桌面应用
- Node.js ≥ 20、Python（含 Pillow）——缺少时会由 Codex 自动安装

## 说明

- 技能只注入背景/色调，不修改 `config.toml`，不改变默认界面布局。
- 生图依赖（`souyu-image-2`）不在本包内；如有需要请单独安装或接入搜遇酷图 API。
