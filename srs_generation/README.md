# SRS Generation Docs Map

本目录用于沉淀 TestHub SRS Skill 化相关的规范、执行计划、运行事实与会话恢复入口。

## Read First

新会话默认按以下顺序恢复：

1. `README.md`
2. `session-handoff.md`
3. `current-work-summary.md`
4. `exec-plans/active/plan-0004-sdd-doc-structure-governance.md`
5. 最新 canonical handoff
6. 必要时再读相关 `specs/` 或 `design-docs/`

## 目录职责总览

- `specs/`：规范事实源。定义 Skill A / B / C 的输入输出契约、边界、gate、artifact 标准与 handoff 规则。
- `exec-plans/`：执行计划与推进追踪。记录当前或已完成变更的 objective、scope、approach、acceptance criteria 与 learnings。
- `design-docs/`：设计决策与架构解释。记录为什么这样设计、为什么不用其他方案。
- `runs/`：单次执行事实。保存样例运行目录、gate 结果、handoff、验证报告与真实产物。
- `templates/`：固定输出模板。
- `prompts/`：Skill 执行 prompts。
- `scripts/`：文档生成、检查与辅助脚本。
- `current-work-summary.md`：当前状态快照。
- `session-handoff.md`：新会话恢复入口。

## Source Priority

当多个来源不一致时，优先级如下：

1. `specs/`
2. `runs/` 中最新 canonical handoff / gate 结果
3. `current-work-summary.md`
4. `session-handoff.md`
5. `.claude/skills/*/references/`
6. 旧 `tasks/` 与历史讨论

## 当前治理入口

- 当前主治理计划：`exec-plans/active/plan-0004-sdd-doc-structure-governance.md`
- 当前交付规则：`DELIVERY.md`
- 当前质量原则：`QUALITY_SCORE.md`

## 当前治理约定

- `specs/` 是规范事实源。
- `runs/` 是执行事实源。
- `current-work-summary.md` 只保留当前状态快照，不再承载完整历史。
- `session-handoff.md` 只保留新会话恢复入口。
- 旧 `tasks/` 进入冻结迁移期：历史内容保留，但新增内容不再默认写入该目录。

## 维护约定

- 新增长期规则时，优先考虑写入 `specs/`。
- 新增阶段性推进内容时，优先写入 `exec-plans/`。
- 新增设计取舍说明时，优先写入 `design-docs/`。
- 新增样例事实、验证结果与 handoff 时，写入 `runs/`。
