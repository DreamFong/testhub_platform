# Quality Score

本文档用于收敛 SRS Skill 化的跨阶段质量原则与 gate 关注点。

## Golden Principles

1. `specs/` 是规范事实源，不能让任务清单或 summary 重新定义规范。
2. `runs/` 是执行事实源，不能让 summary 冒充运行事实。
3. `current-work-summary.md` 只保留当前状态快照。
4. `session-handoff.md` 只保留新会话恢复入口。
5. `.claude/skills/*/references/` 是可移植副本，不是 canonical source。
6. 外部系统真实结果不得伪造。
7. 每个 Skill 的边界必须清晰，不把下游职责混入上游产物。

## 当前重点规范

- `specs/artifact-run-standard.md`
- `specs/handoff-sync-policy.md`
- `exec-plans/active/plan-0004-sdd-doc-structure-governance.md`

## Gate 一览

- Skill A：SRS 文档质量 gate
- Skill B：知识库准备度与检索可用性 gate
- Skill C：执行约束增强质量 gate
- 文档治理：目录职责清晰、source-of-truth 明确、恢复入口稳定

## 文档质量关注点

治理相关文档至少应满足：

- 读者能快速知道该读哪个文件
- 文件职责单一
- 不重复定义同一规则
- 不把临时状态写成长期规范
- 新会话可在短时间内恢复上下文

## Freshness / Integrity

以下内容应保持同步：

- `specs/` 与 portable skill references
- `current-work-summary.md` 与最新 canonical handoff
- `session-handoff.md` 与当前 stop point
- `exec-plans/active/` 与当前真实推进状态

## 校准机制

当发现以下问题时，应回到骨架治理：

- 同一规则在多个地方定义且不一致
- 新会话恢复需要阅读过多历史文件
- summary 再次变成长日志
- `tasks/` 再次承担规范或设计职责
- `runs/` 中已有事实，但状态文档仍未收敛
