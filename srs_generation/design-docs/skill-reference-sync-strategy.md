# Skill References 同步策略

## Context

Skill A 与 Skill B 已被打包为可移植 Claude skill，导致 repo 内 `srs_generation/specs/` 与 `.claude/skills/*/references/` 同时存在相似内容。如果没有明确同步策略，容易出现双向漂移。

## Decision

采用单向同步策略：

- `srs_generation/specs/` 是规范事实源。
- `.claude/skills/*/references/` 是 Skill 可移植参考副本。
- 规范变更必须先修改 repo specs，再同步到对应 Skill 参考副本。
- 不允许只在 Skill 参考副本中独立演化规范语义。

允许 Skill 参考副本做不改变规则含义的可移植改写：

- 将项目内路径改为 Skill 包相对路径，例如 `<skill_dir>/scripts/...`。
- 将真实 run 样例路径改为占位路径，例如 `<run_dir>/skill-a/`。
- 将具体样例名称改为通用样例名称。
- 将项目专属参考文档名称改为通用参考文档名称。

不允许 Skill 参考副本改写：

- 输入输出契约。
- gate 判定规则。
- handoff 字段。
- `blocked`、`fail`、`pass` 等状态语义。
- Skill A / Skill B / Skill C 的职责边界。

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
