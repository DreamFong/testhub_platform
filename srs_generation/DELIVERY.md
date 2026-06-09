# Delivery Workflow

本文档定义 SRS Skill 化相关文档与规范治理的交付流程。

## 适用范围

适用于以下工作：

- Skill A / B / C 规范调整
- 目录结构治理
- handoff / gate / artifact 标准调整
- prompt、template、script 相关的非平凡变更

当前主治理计划：`exec-plans/active/plan-0004-sdd-doc-structure-governance.md`

## 标准工作流

1. 明确目标与边界
2. 如有必要，先写或更新 exec-plan
3. 需要长期生效的规则，更新到 `specs/`
4. 需要设计解释的内容，更新到 `design-docs/`
5. 真实样例与验证结果写入 `runs/`
6. 完成后更新 `current-work-summary.md` 或 `session-handoff.md`

## 讨论 / 实施 / 外部操作边界

- 讨论阶段只输出方案、模板、迁移建议，不默认改文件。
- 实施阶段才落文件或修改文档。
- 涉及 RAGFlow、TestHub 或其他外部系统的操作，必须在执行前明确获得确认。

## 验证与 gate

- `specs/` 负责定义 gate 规则。
- `runs/` 负责记录某次实际 gate 结果。
- `current-work-summary.md` 只保留最近有效结论，不重复复制完整验证内容。

## 完成标准

一项文档治理工作可视为完成，至少满足：

- 目标容器已明确
- source-of-truth 已明确
- 新增职责不再落入旧混合目录
- 关键入口文件已更新
- 当前状态与下一步建议可被新会话快速恢复

### 勾选与关闭规则

- 只有实际完成的工作才能标记为完成。
- 讨论确认但未落文件的事项，不计为完成。
- 文件已创建但内容尚未评审或尚未落到正确容器的事项，不计为完成。
- 被后续决策替代或废弃的事项，应明确标注 `superseded`、`cancelled` 或原因说明。

### 阶段收口动作

当某个阶段或治理变更完成后，应至少同步以下信息：

- 对应 `exec-plan` 的状态与 `Learnings`
- 受影响的 `specs/` 文档
- 如有真实验证，更新对应 `runs/` 产物或 handoff
- 如当前 stop point 改变，更新 `current-work-summary.md` 或 `session-handoff.md`

## 文档维护规则

- 一个文件只承担一种主要职责。
- 索引文件只做导航，不堆积细节。
- summary 文件只保留状态，不保留完整历史。
- 长期规则进入 `specs/`，不要只写在任务清单或会话总结里。
- 历史目录可暂时保留，但不再接收新的默认内容。
- 决策类内容优先进入 `design-docs/`，不要继续堆在任务索引中。
- 风险类内容应进入当前 `exec-plan` 的 `Risks`，或沉淀为长期设计/治理风险文档。
- 概览类文件只做入口和导航，不重复维护第二套完整清单。

## 旧 tasks/ 目录规则

- 旧 `tasks/` 进入冻结迁移期。
- 已有文件暂不删除。
- 新增推进内容优先写入 `exec-plans/`。
- 后续按主题逐步把旧内容迁出或吸收。
