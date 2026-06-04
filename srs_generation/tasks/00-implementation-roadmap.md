# SRS Skill 化总实施路线图任务清单

## 目标

将已经跑通的“源码逆向生成 SRS → PDF → RAGFlow 验证 → TestHub 闭环”案例，沉淀为可复用、可评审、可编排的 Skill 能力链。

整体拆分为：

```text
Skill A：源码逆向生成 SRS
Skill B：知识库构建与检索验证
Skill C：执行约束增强
总编排：ragflow-testhub-agent-workflow
```

## 阶段 1：Skill A 规范固化

- [ ] 完成 Skill A spec v0.2 正式文档
- [ ] 明确 Skill A 职责边界
- [ ] 明确必填输入：source_project、target_module
- [ ] 明确选填输入：entry_files、scope_hint、reference_srs、output_mode、domain_hints
- [ ] 固化 scope 自动推断与用户确认机制
- [ ] 固化 source_evidence_map 为强制产物
- [ ] 固化 kb-friendly 为默认输出模式
- [ ] 固化 Skill A 评分模型与硬性不合格项
- [ ] 固化 Skill A 与 Skill B 的 handoff 格式

完成标准：Skill A 的输入、输出、流程、评分和 gate 规则已经可被独立实现者复现。

## 阶段 2：Skill A 可执行化

- [ ] 设计 Skill A 总控 prompt
- [ ] 设计 scope 推断 prompt
- [ ] 设计源码事实抽取 prompt
- [ ] 设计 SRS 草稿生成 prompt
- [ ] 设计 kb-friendly 改写 prompt
- [ ] 设计 PDF 生成与文本层检查流程
- [ ] 设计生成 Agent 自评 prompt
- [ ] 设计独立评审 Agent prompt
- [ ] 设计输出目录与文件命名规则

完成标准：可以对一个目标模块稳定执行 `scope confirm → SRS Markdown → PDF → review gate`。

## 阶段 3：Skill A 多样本验证

- [ ] 使用 RuoYi-Vue-Pro 用户管理作为样本 1 回归验证
- [ ] 选择第二个不同业务模块作为样本 2
- [ ] 对样本 2 执行 scope 自动推断
- [ ] 对样本 2 生成 kb-friendly SRS
- [ ] 对样本 2 生成 PDF 并检查文本层
- [ ] 对样本 2 执行独立评审
- [ ] 汇总样本间差异与模板调整点

完成标准：Skill A 不再明显依赖用户管理单一案例，能迁移到至少一个新模块。

## 阶段 4：Skill B 规范与流程沉淀

- [ ] 明确 Skill B 输入输出契约
- [ ] 明确 RAGFlow 知识库创建或复用规则
- [ ] 明确 chunk 质量检查规则
- [ ] 明确 retrieval sanity check 规则
- [ ] 明确 retrieval gate 判定标准
- [ ] 明确 Skill B handoff 输出格式

完成标准：Skill B 可以接收 Skill A 的 SRS PDF，并输出知识库质量判定。

## 阶段 5：Skill C 规范与流程沉淀

- [ ] 明确 Skill C 的输入输出契约
- [ ] 提炼 token 提取规则
- [ ] 提炼 userId / entityId 提取规则
- [ ] 提炼最小请求 body 规则
- [ ] 提炼必带 headers 规则
- [ ] 提炼错误字段与路径黑名单
- [ ] 形成执行约束增强文档模板

完成标准：Skill C 可以基于真实跑通案例生成对 TestHub 执行有帮助的约束增强层。

## 阶段 6：总编排 Skill

- [ ] 设计 `ragflow-testhub-agent-workflow` 总入口
- [ ] 串联 Skill A → Skill B → Skill C
- [ ] 定义每阶段 gate 与失败回退策略
- [ ] 定义最终交付目录结构
- [ ] 定义最小闭环验收标准
- [ ] 使用完整样本执行端到端验证

完成标准：用户提供源码项目与目标模块后，可以按阶段生成 SRS、建库验证、提炼执行约束，并形成可交付结果。
