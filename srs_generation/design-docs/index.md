# Design Docs Index

`design-docs/` 用于记录 SRS Skill 化过程中的设计解释与关键取舍。

## 目的

本目录回答的问题不是“现在做到哪了”，而是：

- 为什么这样分层
- 为什么采用这个 carrier / handoff / sync 策略
- 为什么某些内容属于 Skill A、Skill B 或 Skill C
- 为什么当前不采用其他方案

## 适合写入的主题

- Skill A / B / C 职责边界演进
- TXT / PDF / Markdown 载体选择
- Skill references 与 repo specs 的同步策略
- Skill B offline → hybrid 的设计变化
- handoff、gate、canonical result 的定义方式

## 建议模板

```md
# <design title>

## Context

## Decision

## Consequences

## Alternatives Considered
```

## 当前设计文档索引

- `doc-boundary-model.md`：定义 `specs / design-docs / exec-plans / runs / summary / handoff / tasks` 的职责边界。
- `lifecycle-governance.md`：定义文档新增、执行、归档与状态收敛的生命周期。
- `skill-reference-sync-strategy.md`：定义仓库正式规范与 Skill 可移植参考副本的同步策略。
- `ragflow-carrier-selection.md`：记录主 SRS KB 的载体选择与非默认方案取舍。

## 当前说明

本目录是新增骨架。已有分散在 `current-work-summary.md`、`tasks/` 和会话讨论中的设计解释，后续可按主题逐步迁入本目录。
