# Skill B 知识库构建与检索验证任务清单

## 目标

将 Skill A 产出的 SRS / API docs 转化为 RAGFlow 知识库，并评估 chunk 与检索质量，判断是否可进入后续 TestHub 自动化闭环。

## 1. 职责边界

- [ ] 定义 Skill B 负责知识库创建或复用
- [ ] 定义 Skill B 负责文档上传与解析配置
- [ ] 定义 Skill B 负责 chunk 质量检查
- [ ] 定义 Skill B 负责检索 sanity check
- [ ] 定义 Skill B 负责 retrieval gate 判定
- [ ] 明确 Skill B 不负责生成 SRS
- [ ] 明确 Skill B 不负责提炼执行约束

完成标准：Skill B 与 Skill A / C 的边界清晰。

## 2. 输入契约

- [ ] 定义输入 SRS Markdown
- [ ] 定义输入 SRS PDF
- [ ] 定义输入 source_evidence_map
- [ ] 定义输入 Skill A gate 结果
- [ ] 定义输入知识库名称建议
- [ ] 定义输入解析策略建议
- [ ] 定义输入检索问题集

完成标准：Skill B 可以直接消费 Skill A 的 handoff。

## 3. 知识库创建 / 复用规则

- [ ] 定义何时创建新知识库
- [ ] 定义何时复用已有知识库
- [ ] 定义知识库命名规则
- [ ] 定义 dataset_id / SRS_KB_ID 记录格式
- [ ] 定义上传文档记录格式
- [ ] 定义解析配置记录格式

完成标准：每次建库结果可追踪、可复现。

## 4. Chunk 质量检查

- [ ] 定义 chunk 总数记录
- [ ] 定义短 chunk 阈值
- [ ] 定义短 chunk 比例阈值
- [ ] 定义空 chunk 或异常 chunk 检查
- [ ] 定义标题 chunk 检查
- [ ] 定义字段规则 chunk 检查
- [ ] 定义异常处理 chunk 检查
- [ ] 定义验收标准 chunk 检查
- [ ] 定义 chunk 质量报告模板

完成标准：能判断文档在 RAGFlow 解析后是否结构稳定。

## 5. 检索 sanity check

- [ ] 设计功能需求检索问题
- [ ] 设计字段规则检索问题
- [ ] 设计权限规则检索问题
- [ ] 设计异常处理检索问题
- [ ] 设计验收标准检索问题
- [ ] 定义检索命中判断标准
- [ ] 定义检索缺失记录格式
- [ ] 定义检索误命中记录格式

完成标准：能用一组固定问题快速判断知识库是否可用。

## 6. Retrieval Gate

- [ ] 定义 `pass`
- [ ] 定义 `conditional pass`
- [ ] 定义 `fail`
- [ ] 定义必须通过的检索问题类型
- [ ] 定义允许失败的非关键问题类型
- [ ] 定义触发人工复核的条件
- [ ] 定义不允许进入 TestHub 闭环的条件

完成标准：Skill B 输出明确的知识库可用性结论。

## 7. 输出契约

- [ ] 输出知识库名称
- [ ] 输出 dataset_id / SRS_KB_ID
- [ ] 输出上传文档列表
- [ ] 输出解析配置
- [ ] 输出 chunk 质量报告
- [ ] 输出检索 sanity check 报告
- [ ] 输出 retrieval gate 结果
- [ ] 输出 Skill C / 总编排 handoff

完成标准：后续步骤可以直接引用 Skill B 结果。
