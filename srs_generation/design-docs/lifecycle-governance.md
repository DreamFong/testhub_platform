# 文档生命周期治理

## Context

`srs_generation/` 需要一种稳定的治理节奏，确保新增内容先落在正确容器，而不是再次回流到 `tasks/` 或超长 summary 中。

## Decision

采用以下文档生命周期：

```text
README / session-handoff
→ active exec-plan
→ specs / design-docs
→ runs（如有真实执行）
→ current-work-summary
→ completed exec-plan
```

具体规则：

1. 新增治理或阶段性工作时，先写或更新 `exec-plans/active/*.md`。
2. 长期有效的规则落入 `specs/`。
3. 设计解释与取舍落入 `design-docs/`。
4. 真实验证结果只写入 `runs/`。
5. `current-work-summary.md` 只保留当前状态与关键路径。
6. 工作完成后补齐 `Learnings`，再移入 `exec-plans/completed/`。

## Consequences

- 新内容有稳定落点。
- 新会话不需要遍历全部历史文件即可恢复。
- 当前状态与历史事实的边界更清晰。

## Alternatives Considered

### 方案：直接在 summary 中持续追加阶段日志

未采用。原因是 summary 会快速膨胀为历史日志仓库，破坏其作为状态快照与恢复入口的价值。
