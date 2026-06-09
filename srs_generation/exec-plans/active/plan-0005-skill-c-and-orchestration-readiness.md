# Skill C 与总编排就绪化

Status: active

## Objective

当当前焦点从骨架治理切换后，使用统一计划收敛 Skill C、总编排、最终 handoff 与产物结构，而不是继续依赖分散在旧 `tasks/` 中的细粒度清单。

## Scope

- 收敛 Skill C 执行约束增强的职责边界与输入输出。
- 收敛总编排 `ragflow-testhub-agent-workflow` 的阶段串联、gate 与失败回退。
- 收敛最终 TestHub handoff 所需信息与文档结构。
- 收敛剩余跨阶段 artifact / handoff 约定。

## Out of scope

- 当前不进入 Skill C 实施。
- 当前不访问 RAGFlow。
- 当前不修改 `runs/` 事实产物。
- 当前不做真实 TestHub 自动化闭环执行。

## Approach

1. 以旧 `tasks/05`、`06`、`07`、`16`、`24` 作为历史材料。
2. 当工作焦点切换时，先补齐或收紧 Skill C / orchestration 所需 specs。
3. 明确 Skill C 与纯 SRS KB 的边界，避免执行约束污染需求文档层。
4. 基于已存在的 Skill A / Skill B handoff，设计最终 TestHub handoff 结构。

## Acceptance criteria

- Skill C 与 orchestration 的 live 推进不再依赖旧 `tasks/`。
- 存在可执行的 Skill C / orchestration 主计划。
- 当授权切换焦点后，可直接按本计划推进而不必重新整理历史任务清单。

## Risks

- 若在未明确切换目标时过早推进，容易把当前骨架治理和未来执行增强层混在一起。
- Skill C 的有效约束需要真实跑通案例支撑，不能从纯规范推断代替。

## Learnings

- 待未来切换到 Skill C / orchestration 焦点后补充。
