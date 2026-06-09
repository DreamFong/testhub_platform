# Specs Index

`specs/` 是 SRS Skill 化的规范事实源。

## 目的

本目录用于定义稳定、可复用、可评审的规范，包括：

- Skill A / B / C 的职责边界
- 输入输出契约
- gate 与判定标准
- artifact 与 handoff 规则
- 与 portable skill references 的同步规则

## 哪些内容属于 specs

适合放入 `specs/` 的内容：

- 文档目的
- 适用范围与非适用范围
- 输入契约
- 输出契约
- 工作流
- gate 标准
- failure / blocked 语义
- artifact 命名与结构标准
- handoff block 规范

## 哪些内容不属于 specs

以下内容不应写入 `specs/`：

- 单次 run 的结果与日志
- 某次会话的推进记录
- 临时 next steps
- 本地工作区状态
- 历史 commit / push 提醒
- 外部系统一次性操作记录

## 当前规范索引

- `skill-a-source-to-srs.md`
- `skill-a-scope-confirmation.md`
- `skill-a-source-evidence-map.md`
- `skill-a-scorecard.md`
- `skill-a-review-and-gate.md`
- `skill-a-pdf-generation-and-text-check.md`
- `skill-b-knowledge-base-and-retrieval.md`
- `artifact-run-standard.md`
- `handoff-sync-policy.md`

## 与 portable skill references 的关系

- `srs_generation/specs/` 是 canonical source of truth。
- `.claude/skills/*/references/` 是可移植执行副本。
- 若二者不一致，以 `srs_generation/specs/` 为准。
- references 的同步属于受控复制，不应在 references 中独立演化规范。

## 变更规则

- 规范发生实质变化时，应先更新 `specs/`，再同步到 skill references。
- 规范变更不应只落在 `current-work-summary.md`、`tasks/` 或会话讨论中。
