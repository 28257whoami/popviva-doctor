# PopViva 项目分叉说明

本仓于 2026-09-12 从公开仓 `28257whoami/demisugar-doctor` 独立分叉。
基线提交：`8962af55d52f03972e500c84de36a8d446a62811`。
原项目继续独立开发；本仓服务于 PopViva，通用命令仍名为 `agent-doctor`。

## 仓库与历史

- `origin`：`git@github.com:28257whoami/popviva-doctor.git`，日常拉取与推送。
- `old-origin`：`git@github.com:28257whoami/demisugar-doctor.git`，查阅与选择性复用原项目修复。
- 保留完整祖先历史和原始提交，不改写旧作者、日期或提交说明。
- 历史文档中的 demisugar 描述当时的背景；新增当前文档使用 PopViva，机器标识使用 `popviva`。
- 发布二进制来自本仓的新 Release，消费方通过固定版本与 SHA256 升级。

复用修复先执行 `git fetch old-origin`，审阅 `git log HEAD..old-origin/main`，
再对所需提交执行 `git cherry-pick <commit>`，适配后运行 `./tools/ci-quality`。
原仓的整条主线不会自动合入本仓。

全工作区的分叉清单与文档规则维护在私有 `popviva-workspace` 的
`BRAND_TRANSITION.md`；产品内容不复制进本公开工具仓。
