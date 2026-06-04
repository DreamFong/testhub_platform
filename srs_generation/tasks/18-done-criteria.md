# 完成标准总表

## Skill A 完成标准

- [ ] 有正式 Skill A spec
- [ ] 有可执行总控 prompt
- [ ] 有 scope 自动推断 prompt
- [ ] 有 scope confirm gate
- [ ] 有 SRS 文档模板
- [ ] 有 source_evidence_map 模板
- [ ] 有 PDF 生成与文本层检查流程
- [ ] 有自评 prompt
- [ ] 有独立评审 prompt
- [ ] 有评分表
- [ ] 有 gate 判定规则
- [ ] 通过用户管理样本回归
- [ ] 通过第二样本验证

## Skill B 完成标准

- [ ] 有正式 Skill B spec
- [ ] 能接收 Skill A handoff
- [ ] 能创建或复用 RAGFlow 知识库
- [ ] 能记录 dataset_id / SRS_KB_ID
- [ ] 能输出 chunk 质量报告
- [ ] 能执行检索 sanity check
- [ ] 能输出 retrieval gate
- [ ] 能交接给 Skill C 或总编排

## Skill C 完成标准

- [ ] 有正式 Skill C spec
- [ ] 能提炼认证规则
- [ ] 能提炼 token 提取规则
- [ ] 能提炼实体 ID 提取规则
- [ ] 能提炼最小请求 body
- [ ] 能提炼 headers 模板
- [ ] 能提炼错误字段黑名单
- [ ] 能输出执行约束增强文档
- [ ] 能交接给 TestHub handoff

## 总编排完成标准

- [ ] 有 `ragflow-testhub-agent-workflow` 总入口设计
- [ ] 能串联 Skill A / B / C
- [ ] 有阶段 gate 与失败回退策略
- [ ] 有统一输出目录结构
- [ ] 有最终 handoff 文档
- [ ] 完成用户管理端到端回归
- [ ] 完成第二样本端到端验证

## 最小可交付版本标准

最小可交付版本不要求 A/B/C 全自动化，但必须满足：

- [ ] Skill A spec 定稿
- [ ] Skill A prompt 能手动执行
- [ ] Skill A 至少两个样本验证通过
- [ ] Skill B 有手动建库与检索验证流程
- [ ] Skill C 有执行约束模板
- [ ] 总 handoff 格式明确

## 完整可推广版本标准

完整可推广版本应满足：

- [ ] A/B/C 均有正式 spec
- [ ] A/B/C 均有可执行 prompt 或 workflow
- [ ] 每阶段均有 gate
- [ ] 每阶段产物均可追踪
- [ ] 至少两个样本端到端验证通过
- [ ] 能说明适用范围与不适用范围
