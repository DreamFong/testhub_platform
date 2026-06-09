# SRS 文档骨架治理（Phase 1）

Status: completed

## Objective

完成 `srs_generation/` 的第一阶段骨架治理，使规范、设计解释、执行计划、事实产物、状态快照和会话恢复入口各自落入稳定容器，并将旧 `tasks/` 降级为只读历史层。

## Scope

- 建立 `README.md`、`DELIVERY.md`、`QUALITY_SCORE.md`、`specs/README.md`、`exec-plans/README.md`、`design-docs/index.md` 等基础入口。
- 建立最小必要的补充规范与设计文档。
- 建立 `exec-plans/active/` 与 `exec-plans/completed/`。
- 压缩 `current-work-summary.md` 与 `session-handoff.md` 的职责。
- 为旧 `tasks/` 全量补充当前状态与归属去向提示。

## Out of scope

- 不批量移动或删除历史 `tasks/` 文件。
- 不改写 `runs/` 内事实产物。
- 不进入 Skill C 实施。
- 不执行新的 RAGFlow 或 TestHub 外部操作。

## Approach

1. 先建立骨架入口与目录。
2. 再明确 source-of-truth、同步规则与生命周期。
3. 冻结旧 `tasks/` 入口并补状态提示。
4. 收敛 current summary / session handoff。
5. 把已完成主线归并为 completed exec-plans，把未来主线收敛到少量 active plans。

## Acceptance criteria

- `specs/`、`design-docs/`、`exec-plans/`、`runs/`、`current-work-summary.md`、`session-handoff.md` 的职责边界清晰。
- 新会话恢复顺序稳定。
- 旧 `tasks/` 全量标注当前状态并可视为只读历史层。
- Skill A / Skill B 已完成主线有对应 completed plans。
- Skill C / orchestration 已有统一延后计划承接。

## Risks

- 历史 `tasks/` 仍然保留，目录体量较大，读者仍可能被旧文件数量干扰。
- 后续若继续新增规则但未同步到 `specs/`，仍可能出现 source-of-truth 漂移。

## Learnings

- 先建立骨架入口，再冻结旧入口、最后压缩 summary / handoff，比直接迁移历史文件更稳。
- `runs/` 只读化是治理成功的关键约束之一。
- 旧目录不必立刻删除，只要完成“live 职责迁出 + 历史语义显式化”，就能显著降低新会话恢复成本。
- 把已完成能力主线收敛为少量 completed plans，比维护大量碎片化任务文件更利于长期记忆管理。
