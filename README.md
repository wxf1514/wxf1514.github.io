# 王霄飞 · 学术个人主页

## 修改内容

在 GitHub 打开 `index.html`，点击铅笔 Edit this file，修改后点击 Commit changes，提交到 main。GitHub Pages 会自动重新部署。

|内容|搜索关键词|文件|
|---|---|---|
|个人简介与职称|`id="about"`|index.html|
|研究方向|`id="research"`|index.html|
|教育、工作经历|`id="experience"`|index.html|
|论文|`id="publications"`|index.html|
|主持项目|`id="projects"`|index.html|
|奖励与学术服务|`id="awards"`|index.html|
|专利|`id="patents"`|index.html|
|颜色、字体、布局|对应 CSS 选择器|styles.css|

只改文字时，请保留 `<h3>`、`<p>` 等 HTML 标签。
新增论文：复制一个完整的 `<article class="publication" ...>...</article>`，修改年份、标题、作者和期刊信息。期刊保留 `data-type="journal"`，会议使用 `data-type="conference"`。筛选统计自动计算。
新增专利：在 `<ol class="patents">` 中复制一个 `<li>...</li>`，修改名称及申请号。只有核实授权后才标注已授权。

## 预览与发布

下载本仓库后，直接双击 index.html 即可预览，不需要安装开发工具。修改后上传对应文件，或直接在 GitHub 编辑。
部署记录在仓库 Actions 页面查看。部署成功后刷新网页；如仍显示旧内容，可使用 Ctrl+F5。
网站采用本地字体和资源，无需第三方服务。
