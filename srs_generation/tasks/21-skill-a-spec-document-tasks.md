# Skill A 正式 Spec 文档编写任务清单

> 当前状态：本文件已归并到 `../exec-plans/completed/plan-0001-skill-a-foundation-and-validation.md`，作为历史拆分清单保留。

## 目标

把 Skill A spec v0.2 从讨论稿整理成正式文档，建议路径为 `srs_generation/specs/skill-a-source-to-srs.md`。

## 1. 文档元信息

- [x] 写明文档标题
- [x] 写明版本号
- [x] 写明适用范围
- [x] 写明非适用范围
- [x] 写明与当前 RuoYi 用户管理案例的关系

完成标准：读者能知道文档用于规范 Skill A，而不是记录单次实验。

## 2. 背景与目标

- [x] 简述源码逆向生成 SRS 的目标
- [x] 简述为何默认输出 kb-friendly
- [x] 简述为何需要 scope confirm
- [x] 简述为何需要 source_evidence_map
- [x] 简述为何 Skill A 不直接做 RAGFlow 评估

完成标准：规范背后的动机清晰。

## 3. 输入契约章节

- [x] 写明必填输入
- [x] 写明选填输入
- [x] 写明参数解释
- [x] 写明默认值
- [x] 写明参数不得覆盖源码事实的规则
- [x] 写明输入示例

完成标准：可以据此实现表单、CLI 或 prompt 输入。

## 4. Scope 机制章节

- [x] 写明自动推断规则
- [x] 写明候选范围输出格式
- [x] 写明待确认相邻能力输出格式
- [x] 写明用户确认机制
- [x] 写明 scope confirm gate
- [x] 写明 blocked 处理方式

完成标准：scope 不再依赖用户手工完整填写。

## 5. 流程章节

- [x] 写明 Step 0 输入标准化
- [x] 写明 Step 1 候选范围推断
- [x] 写明 Step 2 用户确认范围
- [x] 写明 Step 3 源码事实抽取
- [x] 写明 Step 4 事实草稿生成
- [x] 写明 Step 5 正式 SRS 改写
- [x] 写明 Step 6 PDF 生成与检查
- [x] 写明 Step 7 质量评审与 gate

完成标准：执行步骤线性清晰。

## 6. 输出契约章节

- [x] 写明主产物
- [x] 写明支撑产物
- [x] 写明 source_evidence_map 要求
- [x] 写明 review report 要求
- [x] 写明风险项要求
- [x] 写明文件命名建议

完成标准：每次执行产物完整可审计。

## 7. 文档模板章节

- [x] 写明默认 SRS 章节
- [x] 写明 FR 编号规则
- [x] 写明 kb-friendly 版表达规则
- [x] 写明 aligned 版表达规则
- [x] 写明表格使用限制

完成标准：SRS 输出结构稳定。

## 8. 评分与 Gate 章节

- [x] 写明五维评分模型
- [x] 写明硬性不合格项
- [x] 写明自评机制
- [x] 写明独立评审机制
- [x] 写明人工复核机制
- [x] 写明 gate 结果定义
- [x] 写明进入 Skill B 的条件

完成标准：质量判断可执行。

## 9. Handoff 章节

- [x] 写明 Skill A → Skill B handoff 文件集合
- [x] 写明默认交接 kb-friendly
- [x] 写明 conditional pass 的交接条件
- [x] 写明 fail 时不得交接

完成标准：Skill B 可以无歧义消费 Skill A 结果。

## 10. 附录

- [x] 添加输入示例
- [x] 添加 scope 输出示例
- [x] 添加 source_evidence_map 示例
- [x] 添加评分表示例
- [x] 添加 gate 输出示例

完成标准：正式 spec 既有规则，也有示例。
