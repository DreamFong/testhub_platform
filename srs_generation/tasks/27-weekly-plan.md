# 分阶段推进计划

> 当前状态：本文件保留为历史分阶段计划快照。当前 live 节奏与主次顺序请以 `../exec-plans/active/*.md` 和 `../current-work-summary.md` 为准。

## 说明

这是一个按执行节奏拆分的计划，不强绑定自然周。每个阶段完成后再进入下一阶段。

## 阶段 1：Skill A Spec 定稿

目标：把 Skill A 的规则写清楚。

任务：

- [ ] 完成 Skill A 正式 spec
- [ ] 完成 scope confirm 机制文档
- [ ] 完成 source_evidence_map 模板
- [ ] 完成 Skill A 评分表
- [ ] 完成 review 与 gate 规则

输出：

- `srs_generation/specs/skill-a-source-to-srs.md`
- `srs_generation/templates/source-evidence-map.md`
- `srs_generation/templates/skill-a-scorecard.md`

## 阶段 2：Skill A Prompt 可执行化

目标：把规则变成可执行 prompt。

任务：

- [ ] 完成 Skill A 总控 prompt
- [ ] 完成 scope 推断 prompt
- [ ] 完成源码事实抽取 prompt
- [ ] 完成 kb-friendly 改写 prompt
- [ ] 完成自评 prompt
- [ ] 完成独立评审 prompt

输出：

- `srs_generation/prompts/skill-a/*.md`

## 阶段 3：用户管理回归

目标：确认新流程不比当前已跑通案例倒退。

任务：

- [ ] 使用用户管理模块重新执行 scope 推断
- [ ] 对比已知范围
- [ ] 生成或校验 SRS
- [ ] 生成或校验 PDF
- [ ] 执行 review gate

输出：

- 用户管理回归报告

## 阶段 4：第二样本验证

目标：验证泛化能力。

任务：

- [ ] 选择第二样本
- [ ] 执行 scope 推断
- [ ] 用户确认 scope
- [ ] 生成 SRS
- [ ] 生成 PDF
- [ ] 执行 review gate
- [ ] 汇总问题并修订 prompt

输出：

- 第二样本验证报告
- Skill A 修订清单

## 阶段 5：Skill B 手动流程沉淀

目标：把知识库质量评估从案例经验变成流程。

任务：

- [ ] 写 Skill B spec
- [ ] 定义 RAGFlow 建库记录模板
- [ ] 定义 chunk 质量报告模板
- [ ] 定义 retrieval sanity check 模板
- [ ] 定义 retrieval gate

输出：

- Skill B spec
- Skill B 报告模板

## 阶段 6：Skill C 手动流程沉淀

目标：把执行约束增强层独立出来。

任务：

- [ ] 写 Skill C spec
- [ ] 定义认证规则模板
- [ ] 定义 ID 提取规则模板
- [ ] 定义最小 body 模板
- [ ] 定义 headers 模板
- [ ] 定义错误黑名单模板

输出：

- Skill C spec
- 执行约束模板

## 阶段 7：总编排设计

目标：设计 A/B/C 串联方式。

任务：

- [ ] 写总编排 spec
- [ ] 定义阶段 gate
- [ ] 定义失败回退
- [ ] 定义最终 handoff
- [ ] 用两个样本做端到端演练

输出：

- `ragflow-testhub-agent-workflow` 设计文档
- 端到端验证报告
