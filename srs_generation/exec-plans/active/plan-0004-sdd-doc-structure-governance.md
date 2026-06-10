# SRS 文档骨架治理

Status: active

> 当前状态：Phase 1 骨架治理已完成，收官记录见 `../completed/plan-0003-sdd-doc-structure-governance-phase-1.md`。本计划继续保留在 `active/`，仅作为后续小修、补链路或维护性治理入口。

## Objective

为 `srs_generation/` 建立清晰、可持续维护的分层文档骨架，使规范、执行计划、设计解释、运行事实和会话恢复入口各自落在单一职责容器中，降低新会话恢复成本与重复定义风险。

## Scope

- 建立 `README.md`、`specs/README.md`、`exec-plans/README.md`、`design-docs/index.md`、`DELIVERY.md`、`QUALITY_SCORE.md` 等骨架入口。
- 明确 `specs/`、`runs/`、`current-work-summary.md`、`session-handoff.md`、`exec-plans/`、`design-docs/` 的职责边界。
- 将旧 `tasks/` 标记为冻结迁移期，并把 live 规则逐步收口到新骨架。
- 为后续逐文件迁移提供统一落点。

## Out of scope

- 本轮不批量移动历史 `tasks/` 文件。
- 本轮不进入 Skill C，不新增 RAGFlow 操作。
- 本轮不修改既有 `runs/` 事实产物。
- 本轮不删除历史文档，只做入口收敛、规则收口与最小必要的新文档补齐。

## Approach

1. 先创建最小骨架入口文件与目录。
2. 在新骨架中定义 source-of-truth 与目录职责。
3. 给旧 `tasks/` 关键入口和索引文件加冻结迁移提示。
4. 把完成标准、维护规则和优先级维护方式收口到 `DELIVERY.md` 与 `exec-plans/README.md`。
5. 后续再按主题把旧 `tasks/` 内容归并为少量 active/completed exec-plans，并逐步压缩 summary。

## Acceptance criteria

- `srs_generation/README.md`、`specs/README.md`、`exec-plans/README.md`、`design-docs/index.md`、`DELIVERY.md`、`QUALITY_SCORE.md` 已创建。
- `specs/artifact-run-standard.md` 与 `specs/handoff-sync-policy.md` 已创建。
- `design-docs/doc-boundary-model.md`、`lifecycle-governance.md`、`skill-reference-sync-strategy.md`、`ragflow-carrier-selection.md` 已创建。
- `exec-plans/active/` 与 `exec-plans/completed/` 已建立。
- 旧 `tasks/README.md`、`19-task-index-by-priority.md`、`25-work-breakdown-summary.md`、`18-done-criteria.md`、`35-task-maintenance-rules.md` 已标注冻结迁移期或历史快照语义。
- `current-work-summary.md` 已收敛为状态快照，`session-handoff.md` 已收敛为恢复入口。
- 新增推进内容已有明确默认落点：`exec-plans/`。
- 当前治理工作的目标、范围与后续迁移方向已可被新会话快速理解。

## Risks

- 历史 `tasks/` 内容仍大量存在，短期内仍会形成“旧索引 + 新骨架”并存状态。
- 在未完成第二波迁移前，部分 live 规则仍可能被读者误从旧文件中获取。
- 后续若继续新增计划但未遵守统一的 `plan-xxxx-...` 四位编号命名与 source-of-truth 规则，仍可能重新引入目录混乱。

## Learnings

- 先建立骨架入口，再冻结旧入口、最后压缩 summary / handoff，比直接批量迁移历史文件更稳。
- `runs/` 作为事实产物区保持只读，可以显著降低治理时误改历史结果的风险。
- `current-work-summary.md` 与 `session-handoff.md` 必须分层：前者记录当前状态，后者记录恢复动作，否则新会话恢复会再次膨胀。
- 为旧 `tasks/` 全量补充“当前状态 / 归属去向”提示后，新会话可以安全地把该目录视为只读历史层，而不必再手工判断哪些文件仍然 live。
- Skill 参考副本与正式规范同步时，不应追求逐字一致；路径、样例名和参考文档名可以做可移植改写，但输入输出契约、gate 判定、handoff 字段、状态语义和 Skill 边界必须与正式规范一致。
