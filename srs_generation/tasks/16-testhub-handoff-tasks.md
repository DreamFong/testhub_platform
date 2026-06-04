# TestHub Handoff 任务清单

## 目标

定义 SRS Skill 化链路最终如何把需求知识、知识库结果和执行约束交给 TestHub，支撑后续自动化测试生成与执行。

## 1. Handoff 输入来源

- [ ] 接收 Skill A 最终 SRS Markdown
- [ ] 接收 Skill A 最终 SRS PDF
- [ ] 接收 Skill A source_evidence_map
- [ ] 接收 Skill A review gate
- [ ] 接收 Skill B dataset_id / SRS_KB_ID
- [ ] 接收 Skill B retrieval gate
- [ ] 接收 Skill C 执行约束增强文档

完成标准：最终 handoff 汇总所有关键上游产物。

## 2. TestHub 所需信息

- [ ] 定义需求知识库 ID
- [ ] 定义模块名称
- [ ] 定义功能范围
- [ ] 定义测试生成目标
- [ ] 定义认证方式
- [ ] 定义环境配置
- [ ] 定义执行约束
- [ ] 定义禁止使用的字段和路径

完成标准：TestHub 不需要重新猜测上下文。

## 3. Handoff 文档结构

- [ ] 定义项目与模块摘要
- [ ] 定义 Skill A 产物摘要
- [ ] 定义 Skill B 知识库摘要
- [ ] 定义 Skill C 执行约束摘要
- [ ] 定义可执行前置条件
- [ ] 定义风险和限制
- [ ] 定义下一步建议

完成标准：人类和自动化流程都能读懂 handoff。

## 4. 验收标准

- [ ] 检查 SRS gate 是否 pass 或允许的 conditional pass
- [ ] 检查 retrieval gate 是否 pass
- [ ] 检查执行约束是否足够生成最小闭环
- [ ] 检查知识库 ID 是否可用
- [ ] 检查认证规则是否明确
- [ ] 检查 ID 提取规则是否明确

完成标准：handoff 不把不完整链路伪装成可执行状态。

## 5. 输出文件

- [ ] 定义 `testhub-handoff.md`
- [ ] 定义 `testhub-handoff.json` 是否需要
- [ ] 定义人工摘要字段
- [ ] 定义机器可读字段
- [ ] 定义版本和时间戳字段

完成标准：最终交接既可阅读，也可被后续自动化消费。
