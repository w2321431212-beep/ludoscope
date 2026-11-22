# LudoScope NOVA 4.5 — GitHub Pages 部署版

本文件夹只包含网站上线需要的静态文件（不包含原始爬虫、清洗脚本、研究原始数据）。请**把本文件夹里面的所有文件与子文件夹**放在 GitHub 仓库的根目录。不要只上传 `index.html`，也不要将 ZIP 当作网页文件上传。

## 操作步骤
1. 登录 GitHub，新建一个 **Public** 仓库，建议名称 `ludoscope`。
2. 在仓库首页选择 **Add file → Upload files**，将本文件夹内的所有文件和文件夹拖入上传区（应保留 `data/` 和 `assets/` 目录层级），然后点击 **Commit changes**。如果一次上传失败，建议改用 GitHub Desktop 上传整个项目。
3. 检查仓库顶层有 `index.html`、`styles.css`、`app.js`、`data/`、`assets/`。
4. 打开仓库 **Settings → Pages**，选择 **Build and deployment → Source: Deploy from a branch**，分支 **main**，目录 **/(root)**，点击 **Save**。
5. 等待部署完成，访问：`https://<你的用户名>.github.io/ludoscope/`。Pages 配置页可看到实际链接。

## 常见问题
- 出现 404：确认 `index.html` 位于仓库根目录；Pages 选择了 `main / (root)`；部署完成后再刷新。
- 页面只剩原始按钮/背景变白：CSS 或 JS 没找到，核对文件夹层级和路径，不能只上传 `index.html`。
- 一直显示“加载数据”：检查 `data/catalog.js` 是否上传成功（约 22.4MB）。
- 手机无法打开：请分享 GitHub Pages 网站地址，不是 GitHub 源码仓库链接。
- 游戏封面：优先从 Steam 的远程图片服务器加载；网络不可访问时显示内置备用图。

## 安全及法律提醒
这个版本内含约 31,953 款游戏的目录数据。公开部署后访客可以读取前端数据及脚本，请先确认所用 Steam/第三方数据和图像的公开再分发权限，移除内部机密及不应公开的字段。项目鉴定报告等信息储存在每个访客各自浏览器的 localStorage，并不会跨设备自动同步，也没有后端用户账户与真实服务端隐私保护。

## 更新
修改仓库内对应文件并提交到 main 分支，GitHub Pages 会重新发布。原有链接保持不变。
