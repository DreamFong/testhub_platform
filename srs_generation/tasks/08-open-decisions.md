# 待确认决策清单

## 目标

集中记录 SRS Skill 化实施过程中尚未完全拍板的设计决策，避免在任务执行时反复分歧。

## 已确认决策

- [x] Skill A 默认输出 `kb-friendly` SRS
- [x] `module_scope` 不作为必填输入
- [x] 使用 `scope_hint` 作为选填范围提示
- [x] Skill A 必须先自动推断 scope，再交由用户确认
- [x] 未完成 scope confirm，不进入正式 SRS 生成
- [x] `source_evidence_map` 作为 Skill A 强制产物
- [x] Skill A 允许 `conditional pass`
- [x] Skill A 不直接评估 RAGFlow 检索质量
- [x] Skill B 负责 chunk 与 retrieval gate
- [x] Skill C 负责执行约束增强

## 待确认决策

### 1. Skill A spec 文件位置

- [ ] 是否放在 `srs_generation/specs/skill-a.md`
- [ ] 是否放在 `.claude/skills/` 相关目录
- [ ] 是否同时维护设计文档和可执行 skill 文件

建议：先放 `srs_generation/specs/skill-a.md`，稳定后再迁移为真正 skill。

### 2. Prompt 文件是否单独拆分

- [ ] 总控 prompt 是否单文件维护
- [ ] scope 推断 prompt 是否单文件维护
- [ ] 抽取 prompt 是否单文件维护
- [ ] 评审 prompt 是否单文件维护

建议：拆分维护，便于单独迭代。

### 3. PDF 生成工具标准化

- [ ] 是否继续使用现有 Python 脚本
- [ ] 是否统一为一个通用 Markdown→PDF 脚本
- [ ] 是否要求支持中文字体配置
- [ ] 是否要求输出文本层检查报告

建议：统一为通用脚本，保留模块参数化能力。

### 4. 第二个验证样本选择

- [ ] 是否继续使用 RuoYi-Vue-Pro 中另一个模块
- [ ] 是否使用 TestHub 当前项目自身模块
- [ ] 是否选择 API testing 模块
- [ ] 是否选择 UI automation 模块

建议：优先选 RuoYi-Vue-Pro 中另一个模块，降低跨项目变量。

### 5. Skill B 是否接入 RAGAS

- [ ] 当前阶段只做 sanity check
- [ ] 后续阶段接入 RAGAS
- [ ] 定义 RAGAS 的适用指标

建议：当前先不引入 RAGAS，先把人工可解释的 sanity check 跑稳。

### 6. Skill C 是否生成独立知识库文档

- [ ] 执行约束是否与 SRS 放入同一知识库
- [ ] 执行约束是否作为单独知识库
- [ ] 执行约束是否只作为 TestHub 编排上下文

建议：先单独维护，不直接混入纯 SRS 知识库。

### 7. 总编排是否一开始就自动建库

- [ ] 全自动建库
- [ ] 先生成建库计划，用户确认后建库
- [ ] 只在用户指定时建库

建议：涉及外部系统状态，默认先生成计划并请求确认。
