# 文档职责边界模型

## Context

随着 Skill A、Skill B、handoff、tasks 和 summary 持续增长，`srs_generation/` 内开始出现职责重叠：规范、执行计划、历史事实和会话恢复信息混杂在同一批文件中，导致新会话恢复慢、source-of-truth 不清晰、同一规则可能在多个位置重复定义。

## Decision

采用分层骨架模型：

- `specs/`：规范事实源
- `design-docs/`：设计解释与决策记录
- `exec-plans/`：执行计划与推进状态
- `runs/`：单次执行事实产物
- `current-work-summary.md`：当前状态快照
- `session-handoff.md`：新会话恢复入口
- `tasks/`：冻结迁移期历史目录

其中：

- 规则与契约进入 `specs/`
- 为什么这样设计进入 `design-docs/`
- 当前准备怎么做进入 `exec-plans/`
- 真实发生了什么进入 `runs/`
- 现在做到哪一步进入 `current-work-summary.md`
- 新会话先读什么进入 `session-handoff.md`

## Consequences

- 新会话恢复路径更稳定。
- 同一规则不再需要在 tasks、summary 和会话中多次定义。
- 旧 `tasks/` 不再承担 live 职责，但历史材料仍可追溯。
- 目录治理需要额外维护入口文件之间的一致性。

## Alternatives Considered

### 方案：继续使用 `tasks/ + current-work-summary.md` 承载全部信息

未采用。原因是这种做法会让推进计划、规范、状态和历史继续混杂，导致后续维护成本持续上升。
