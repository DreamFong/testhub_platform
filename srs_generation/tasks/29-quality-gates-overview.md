# Quality Gates 总览

## 目标

统一定义 SRS Skill 化链路中的所有质量门禁，确保每个阶段都有明确的继续 / 停止条件。

## Gate 1：Scope Confirm Gate

所属阶段：Skill A

通过条件：

- [ ] 候选范围已输出
- [ ] 相邻待确认能力已输出
- [ ] 用户已确认范围
- [ ] 排除项已记录

阻断条件：

- [ ] 用户未确认范围
- [ ] 范围存在重大歧义
- [ ] 关键入口文件无法定位且用户无法补充

输出：

- `confirmed`
- `confirmed_with_changes`
- `blocked`

## Gate 2：SRS Document Quality Gate

所属阶段：Skill A

通过条件：

- [ ] 无硬性不合格项
- [ ] 五维评分达到约定阈值
- [ ] source_evidence_map 可支撑关键结论
- [ ] PDF 文本层可提取

阻断条件：

- [ ] 编造源码事实
- [ ] 核心功能缺失
- [ ] 关键规则写反
- [ ] 文档结构不可用
- [ ] PDF 文本层不可提取
- [ ] 关键结论无源码依据

输出：

- `pass`
- `conditional pass`
- `fail`

## Gate 3：Knowledge Base Parsing Gate

所属阶段：Skill B

通过条件：

- [ ] 文档成功进入知识库
- [ ] chunk 数量合理
- [ ] 短 chunk 比例可接受
- [ ] 关键章节可在 chunk 中定位
- [ ] 字段规则、异常处理、验收标准有稳定 chunk

阻断条件：

- [ ] 文档解析失败
- [ ] 关键章节丢失
- [ ] chunk 极度碎片化或异常
- [ ] 关键规则无法在 chunk 中定位

输出：

- `pass`
- `conditional pass`
- `fail`

## Gate 4：Retrieval Gate

所属阶段：Skill B

通过条件：

- [ ] 功能需求问题可检索
- [ ] 字段规则问题可检索
- [ ] 权限规则问题可检索
- [ ] 异常处理问题可检索
- [ ] 验收标准问题可检索

阻断条件：

- [ ] 核心功能问题无法命中
- [ ] 关键字段规则无法命中
- [ ] 关键异常处理无法命中
- [ ] 检索结果明显误导

输出：

- `pass`
- `conditional pass`
- `fail`

## Gate 5：Execution Constraint Gate

所属阶段：Skill C

通过条件：

- [ ] 认证规则明确
- [ ] token 提取路径明确
- [ ] 实体 ID 提取路径明确
- [ ] 最小请求 body 明确
- [ ] 必带 headers 明确
- [ ] 错误字段黑名单明确

阻断条件：

- [ ] 缺少认证规则且目标接口需要认证
- [ ] 缺少 ID 提取规则导致流程无法串联
- [ ] 最小 body 仍依赖猜测
- [ ] 约束来自未经验证的假设

输出：

- `ready`
- `partial`
- `blocked`

## Gate 6：TestHub Handoff Gate

所属阶段：总编排

通过条件：

- [ ] Skill A gate 可接受
- [ ] Skill B retrieval gate 可接受
- [ ] Skill C 约束足够支撑最小闭环
- [ ] 知识库 ID 已记录
- [ ] 最终 handoff 文档完整

阻断条件：

- [ ] SRS 文档质量 fail
- [ ] retrieval gate fail
- [ ] 执行约束不足以运行最小闭环
- [ ] 外部知识库状态不可确认

输出：

- `ready_for_testhub`
- `needs_manual_fix`
- `blocked`
