# Skill References 同步策略

## Context

Skill A 与 Skill B 已被打包为可移植 Claude skill，导致 repo 内 `srs_generation/specs/` 与 `.claude/skills/*/references/` 同时存在相似内容。如果没有明确同步策略，容易出现双向漂移。

## Decision

采用单向同步策略：

- `srs_generation/specs/` 是 canonical source of truth。
- `.claude/skills/*/references/` 是可移植执行副本。
- 规范变更必须先修改 repo specs，再同步到对应 skill references。
- 不允许只在 skill references 中独立演化规范语义。

当前涉及：

- `.claude/skills/source-to-srs/`
- `.claude/skills/srs-to-ragflow-kb/`

## Consequences

- 规范事实源唯一，降低双写冲突。
- skill references 更适合作为可移植副本和执行随行文档。
- repo 内需要承担更多规范索引与同步说明职责。

## Alternatives Considered

### 方案：让 skill references 成为事实源

未采用。原因是 skill 目录更适合执行分发，不适合承担项目内长期规范治理与全局目录索引职责。
