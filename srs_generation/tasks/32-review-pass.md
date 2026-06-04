# 任务清单自检

## 检查目标

确认本目录下的任务清单已经覆盖从当前案例沉淀为 Skill 化能力链所需的主要工作。

## 覆盖检查

- [x] 覆盖总实施路线图
- [x] 覆盖 Skill A spec 固化
- [x] 覆盖 Skill A prompt 可执行化
- [x] 覆盖 Skill A 多样本验证
- [x] 覆盖 Skill B 知识库构建与检索验证
- [x] 覆盖 Skill C 执行约束增强
- [x] 覆盖总编排 Skill
- [x] 覆盖产物目录与命名
- [x] 覆盖待确认决策
- [x] 覆盖风险登记
- [x] 覆盖质量门禁
- [x] 覆盖 TestHub handoff

## 与当前已确认结论的一致性

- [x] `module_scope` 不再作为必填输入
- [x] 使用 `scope_hint` 作为选填输入
- [x] Skill A 先自动推断 scope，再由用户确认
- [x] 未完成 scope confirm 不进入正式 SRS 生成
- [x] 默认输出 kb-friendly SRS
- [x] source_evidence_map 作为强制产物
- [x] Skill A 评分不包含 RAGFlow 检索质量
- [x] Skill B 独立承担 retrieval gate
- [x] Skill C 独立承担执行约束增强

## 建议执行入口

优先阅读：

1. [README.md](README.md)
2. [19-task-index-by-priority.md](19-task-index-by-priority.md)
3. [26-minimum-viable-skill-a.md](26-minimum-viable-skill-a.md)
4. [31-final-checklist-before-implementation.md](31-final-checklist-before-implementation.md)

## 下一步

建议从 Skill A 正式 spec 开始落地，而不是马上推进全链路自动化。
