# 王霄飞 · 学术个人主页

浅色学术主页，保留原站点全部研究、经历、项目、奖励与专利信息。按年份展示论文，支持搜索、类型筛选和配色保存。参考 lue.fan 的学术布局，未使用其个人照片或论文图片。

## 内容维护
- `index.html`：简介、动态、研究方向、经历、项目和专利；包含不依赖 JavaScript 的论文后备列表。
- `data/publications.json`：论文数据。`updated_at: null` 表示尚未成功同步，当前数据来自原主页。
- `data/scholar.json`：Google Scholar ID，已配置 `Gq2ORzoAAAAJ`。
- `styles.css`：排版与响应式样式。

## Google Scholar 自动同步
`.github/workflows/scholar.yml` 每天北京时间约 06:23 执行，也可在 Actions 中手动运行。GitHub 的排队可能造成延迟；这不是即时推送。任务成功后提交 JSON，并显式执行 Pages 部署（机器人提交本身不保证触发 Pages 构建）。仓库需启用 Actions 和 Pages，并允许工作流写入 contents、部署 Pages。

抓取公开资料的标题、年份、作者、发表信息、引用数和 Scholar 论文链接；保留已人工整理的作者列表和类型。新增论文类型不能可靠识别时标记为“论文”。同步采用分页和原子写入。限流、验证码、解析错误、数量减少均使任务失败，原有数据不变；不会绕过验证码。公开仓库的定时任务可能因长期无活动被 GitHub 停用，届时需重新启用。

2026-10-28 本地首次请求返回 HTTP 429；尚未验证真实 Scholar 同步成功。页面保持原有 8 篇论文，不展示虚构的同步日期。持续限流时应改用获授权的数据服务或手动维护 JSON。

## 本地预览与验证
```sh
python -m http.server 8765 --bind 127.0.0.1
python -m pip install requests==2.32.3 beautifulsoup4==4.12.3
python -m unittest discover -s scripts -p 'test_*.py'
node --check script.js
```
打开 http://127.0.0.1:8765 。部署时保留 `.github` 目录及 `data` 目录；Pages 发布根目录应包含 index.html。初次改版仍可沿用现有 main 分支 Pages 发布方式。

## 发布工作流
`pages.yml` 在主页文件推送到 main 后自动部署，独立于 Scholar 同步，避免抓取限流阻塞页面发布。`scholar.yml` 首次加入仓库时也会尝试同步；之后每日定时执行或手动触发。两个部署任务使用同一并发组，避免同时发布。
