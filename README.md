# PopViva agent-doctor

PopViva 独立维护的声明式仓库一致性检查器。它检查协作规则、文档引用、生成索引和能力声明，不定义业务格式。

- 协作与开发规则：[AGENTS.md](AGENTS.md)
- 原项目来源与复用流程：[BRAND_TRANSITION.md](BRAND_TRANSITION.md)
- 公开边界：[SECURITY.md](SECURITY.md)

```bash
go build ./...
go test ./...
go run ./cmd/agent-doctor check -C /path/to/repo
```

发布产出 Linux/macOS 的 amd64/arm64 四平台二进制，命令保持 `agent-doctor`。
