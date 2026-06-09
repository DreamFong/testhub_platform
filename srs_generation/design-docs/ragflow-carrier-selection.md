# RAGFlow 载体选择策略

## Context

Skill B 的真实 online 验证表明，不同输入载体在当前 RAGFlow 环境中的解析稳定性差异明显。早期尝试中：Markdown 直传不可解析，PDF + DeepDOC 可能出现相邻章节标题串接或正文丢失，而从 `srs-kb-friendly.md` 生成 TXT 后再以 `book` 模式解析，效果最好。

## Decision

当前主 SRS KB 采用以下策略：

- 主载体：从 `srs-kb-friendly.md` 临时生成的 TXT carrier
- 主解析方式：`book`
- `source-evidence-map.md`：作为必填分析输入，但默认不上传主 SRS KB
- `srs-kb-friendly.pdf`：保留为阅读版和 parser 对比实验输入，不作为默认主 KB 输入

## Consequences

- 当前 online 验证路径更稳定，可获得更可靠的 chunk 与 retrieval 结果。
- 主 SRS KB 侧重业务需求检索，不直接承担源码级证据追溯。
- 若后续需要源码级检索，应单独设计 evidence KB，而不是强行把所有材料塞入主 KB。

## Alternatives Considered

### 方案：Markdown 直传

未采用。原因是当前环境不支持 `.md` 解析。

### 方案：PDF 作为主上传材料

未采用。原因是解析质量不稳定，曾出现标题串接和正文丢失问题。
