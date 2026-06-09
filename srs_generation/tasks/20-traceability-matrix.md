# 任务追踪矩阵

> 当前状态：本文件保留为历史 traceability 快照。当前 live 规范与计划的对应关系优先通过 `../specs/`、`../exec-plans/` 与 `../current-work-summary.md` 的链接关系维护。

## 目标

把实施任务与上游结论建立映射，确保每个已确认结论都有对应落地任务。

## 结论到任务映射

### 结论 1：Skill A 默认输出 kb-friendly

对应任务：

- [01-skill-a-spec-tasks.md](01-skill-a-spec-tasks.md)
- [02-skill-a-execution-prompts-tasks.md](02-skill-a-execution-prompts-tasks.md)

落地检查：

- [ ] spec 中明确默认 output_mode
- [ ] prompt 中明确默认生成 kb-friendly
- [ ] aligned 仅作为显式请求输出

### 结论 2：module_scope 改为 scope_hint，且非必填

对应任务：

- [01-skill-a-spec-tasks.md](01-skill-a-spec-tasks.md)
- [11-scope-confirmation-tasks.md](11-scope-confirmation-tasks.md)

落地检查：

- [ ] 输入契约不再要求 module_scope
- [ ] scope_hint 被定义为选填提示
- [ ] 未提供 scope_hint 时自动推断

### 结论 3：必须先自动推断 scope，再由用户确认

对应任务：

- [11-scope-confirmation-tasks.md](11-scope-confirmation-tasks.md)
- [02-skill-a-execution-prompts-tasks.md](02-skill-a-execution-prompts-tasks.md)

落地检查：

- [ ] 有 scope 推断 prompt
- [ ] 有确认问题模板
- [ ] 有确认状态记录

### 结论 4：未完成 scope confirm，不进入正式 SRS 生成

对应任务：

- [01-skill-a-spec-tasks.md](01-skill-a-spec-tasks.md)
- [11-scope-confirmation-tasks.md](11-scope-confirmation-tasks.md)

落地检查：

- [ ] spec 中定义 gate
- [ ] blocked 状态阻止后续生成

### 结论 5：source_evidence_map 是强制产物

对应任务：

- [12-source-evidence-map-tasks.md](12-source-evidence-map-tasks.md)
- [15-review-and-gate-tasks.md](15-review-and-gate-tasks.md)

落地检查：

- [ ] 输出契约中包含 source_evidence_map
- [ ] 评审必须检查 source_evidence_map
- [ ] 关键结论无依据触发 fail 或人工复核

### 结论 6：Skill A 只评估 SRS 文档质量

对应任务：

- [01-skill-a-spec-tasks.md](01-skill-a-spec-tasks.md)
- [10-skill-a-scorecard-tasks.md](10-skill-a-scorecard-tasks.md)

落地检查：

- [ ] Skill A 评分不包含 RAGFlow 检索准确率
- [ ] Skill B 独立负责 retrieval gate

### 结论 7：Skill A 采用三阶段评分机制

对应任务：

- [10-skill-a-scorecard-tasks.md](10-skill-a-scorecard-tasks.md)
- [15-review-and-gate-tasks.md](15-review-and-gate-tasks.md)

落地检查：

- [ ] 有自评
- [ ] 有独立评审
- [ ] 有人工复核触发条件

### 结论 8：Skill B 负责知识库构建与检索质量

对应任务：

- [04-skill-b-tasks.md](04-skill-b-tasks.md)

落地检查：

- [ ] Skill B 输入接收 Skill A 产物
- [ ] Skill B 输出 chunk 报告与 retrieval gate

### 结论 9：Skill C 负责执行约束增强

对应任务：

- [05-skill-c-tasks.md](05-skill-c-tasks.md)
- [16-testhub-handoff-tasks.md](16-testhub-handoff-tasks.md)

落地检查：

- [ ] Skill C 不污染纯 SRS
- [ ] 执行约束作为独立 handoff 输出

### 结论 10：最终需要总编排 Skill

对应任务：

- [06-orchestration-skill-tasks.md](06-orchestration-skill-tasks.md)
- [16-testhub-handoff-tasks.md](16-testhub-handoff-tasks.md)

落地检查：

- [ ] A/B/C 串联
- [ ] 每阶段 gate 明确
- [ ] 最终 handoff 可被 TestHub 消费
