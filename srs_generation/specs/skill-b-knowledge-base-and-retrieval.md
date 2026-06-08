# Skill B：知识库构建与检索验证规范（Offline MVP）

版本：v0.1  
状态：draft  
适用阶段：Skill B 规范固化与离线 MVP 设计

## 1. 文档目的

本文档用于规范 Skill B 的职责、输入、输出、执行流程、门禁语义与交接方式。Skill B 的目标是把 Skill A 产出的 SRS 文档转化为适合进入 RAGFlow 知识库链路的标准输入，并在真实 RAGFlow 不可用时先完成离线准备度验证。

Skill B 不是单次实验记录。当前 ERP 仓库管理与 MES 盘点任务样本只作为 Skill B Offline MVP 的候选验证样本，用于校验规范是否可复现、可迁移、可交接。

## 2. 适用范围与非适用范围

### 2.1 适用范围

Skill B 适用于以下场景：

- 已有 Skill A 产出的 `kb-friendly` SRS 文档。
- 希望把 SRS 文档纳入 RAGFlow 知识库链路。
- 希望在真实建库前先评估文档是否具备检索准备条件。
- 希望生成固定的 retrieval sanity check 问题集。
- 希望明确哪些风险项可继续等待 RAGFlow，哪些问题必须回退 Skill A。

Skill B 的标准链路为：

```text
Skill A handoff
→ 知识库创建/复用计划
→ 解析配置计划
→ retrieval 问题集生成
→ 离线可检索性预检
→ offline_readiness_gate
→ online_retrieval_gate（真实 RAGFlow 可用时）
→ Skill C / 总编排 handoff
```

### 2.2 非适用范围

Skill B 不负责以下工作：

- 不负责生成 SRS。
- 不负责修改 Skill A 产物。
- 不负责生成 TestHub scenario JSON。
- 不负责执行 TestHub。
- 不负责失败诊断与自动修正。
- 不负责提炼执行约束增强层。
- 不负责替业务裁决不确定规则。
- 不负责伪造真实 RAGFlow 检索结果。

对应边界为：

```text
Skill A：评估 SRS 文档质量
Skill B：评估知识库准备度与检索可用性
Skill C：提炼执行约束增强层
总编排：串联知识库、场景生成、归一化、导入与执行
```

## 3. 背景与目标

### 3.1 Skill B 的核心目标

Skill B 的核心目标不是“上传文件”，而是判断：

- 当前 SRS 是否值得进入知识库构建链路？
- 哪些知识点应该能被后续检索问题稳定召回？
- 哪些文档结构问题会阻断真实建库？
- 在 RAGFlow 不可用时，如何输出可交接但不误导的 blocked 结果？

Skill B 最终应能回答：

- 该 SRS 适合如何建库？
- 该 SRS 的关键功能、字段、权限、异常和验收标准是否可被设计成固定检索问题？
- 当前阶段是否允许进入真实 RAGFlow online 验证？
- 当前阶段是否允许交给后续 Skill C / 总编排等待继续？

### 3.2 Offline MVP 的原因

当前阶段没有可用 RAGFlow 供访问，因此 Skill B 不能立即执行真实建库、真实 chunk 检查和真实 retrieval sanity check。

因此 Skill B 需要拆分为两层：

```text
offline_readiness_gate：不依赖 RAGFlow，判断文档是否具备建库准备条件
online_retrieval_gate：依赖 RAGFlow，判断真实知识库是否检索可用
```

Offline MVP 先解决：

- 输入契约。
- 输出契约。
- 建库计划模板。
- 解析配置计划模板。
- retrieval 问题集模板。
- 离线可检索性预检规则。
- blocked 语义。

### 3.3 设计原则

Skill B 必须遵守以下原则：

1. **先计划，后外部操作**  
   涉及真实 RAGFlow 建库、上传和检索的动作必须先输出计划，再由用户确认。

2. **不伪造 online 结果**  
   RAGFlow 不可用时，`online_retrieval_gate` 只能是 `blocked`，不能伪造 `dataset_id`、`chunk_count` 或 `pass` 结果。

3. **离线预检不替代真实检索**  
   离线阶段只能判断“是否值得建库”，不能宣布“知识库已经可检索”。

4. **风险显式暴露**  
   Skill A 已识别的风险项必须进入 Skill B 的问题集、预检报告或 handoff，不得在中间阶段消失。

## 4. 输入契约

### 4.1 必填输入

#### skill_a_run_dir

Skill A 运行产物根目录。

示例：

```text
srs_generation/runs/ruoyi-vue-pro-erp-warehouse-validation-20260607/skill-a/
```

#### srs-kb-friendly.md

Skill A 生成的最终 Markdown 主文档。

#### source-evidence-map.md

Skill A 生成的源码依据映射文件。它是 Skill B 的必填分析输入，用于辅助追溯、风险判断和问题集补强，但不默认作为主 RAGFlow SRS 知识库上传材料。

#### gate-result.md

Skill A 最终 gate 结果文件。

#### pdf-text-check-report.md

Skill A PDF 文本层与可读性检查报告。

### 4.2 选填输入

#### srs-kb-friendly.pdf

Skill A 生成的最终 PDF 文档。它作为正式交付阅读版、PDF gate 证明材料和未来 parser 对比实验候选物保留；Offline MVP 中默认作为参考输入，不作为主分析输入，也不默认作为主知识库上传材料。

#### risk-items.md

若 Skill A 已生成风险项文件，Skill B 必须读取并把风险纳入问题集或 handoff。

#### knowledge_base_name_hint

用户或上层编排提供的知识库命名提示。

#### retrieval_question_set

若用户已手工提供检索问题集，Skill B 应与自动生成问题集合并，而不是盲目覆盖。

#### api_docs_path

未来扩展到 API docs KB 时可选。Offline MVP 默认不启用。

### 4.3 输入前置条件

Skill B Offline MVP 的前置条件为：

```text
Skill A gate = pass
或
Skill A gate = conditional pass，且人工明确允许继续
```

同时必须满足：

- `pdf_text_layer_gate = pass`
- `pdf_readability_gate = pass`
- `source-evidence-map.md` 存在

说明：

- `srs-kb-friendly.md` 是 Skill B Offline MVP 的主分析输入，也是主 RAGFlow SRS 知识库的默认上传候选。
- `srs-kb-friendly.pdf` 是参考输入，不是当前 MVP 的主分析输入。
- `source-evidence-map.md` 是必填分析输入，但不默认上传到主 RAGFlow SRS 知识库。

以下情况不进入 Skill B：

- Skill A gate = fail
- PDF 文本层不可提取
- PDF 可读性 gate fail
- 关键源码依据缺失

## 5. 输出契约

### 5.1 Offline MVP 固定输出

Skill B Offline MVP 至少输出：

1. `input-snapshot.md`
2. `kb-plan.md`
3. `parse-config-plan.md`
4. `retrieval-question-set.md`
5. `offline-retrieval-readiness-report.md`
6. `retrieval-gate-result.md`
7. `skill-b-handoff.md`

### 5.2 暂不输出的 online 产物

真实 RAGFlow 不可用时，以下文件不应伪造：

- `dataset-record.md`
- `upload-record.md`
- `chunk-quality-report.md`
- `online-retrieval-check-report.md`

这些文件应在真实 online 阶段补充。

## 6. 知识库创建 / 复用规则（计划层）

### 6.1 Offline MVP 允许输出的内容

Offline MVP 允许输出：

- 是否建议创建新知识库。
- 是否建议复用已有知识库。
- 建议知识库名称。
- 建议上传的文档列表。
- 建议解析配置。
- 后续真实操作所需用户确认项。

Offline MVP 默认上传策略为：

```text
默认上传：srs-kb-friendly.md
默认不上传：srs-kb-friendly.pdf、source-evidence-map.md
```

若需要比较 Markdown / PDF 的 parser 或 retrieval 效果，应通过独立对比实验执行，而不是先把 Markdown 与 PDF 一起上传到同一个主知识库。

### 6.2 Offline MVP 禁止输出的内容

Offline MVP 禁止输出：

- 伪造 `dataset_id`。
- 伪造文档上传成功状态。
- 伪造真实 chunk 数量。
- 伪造真实 retrieval 命中结果。

### 6.3 建议命名规则

若创建新知识库，建议名称至少包含：

```text
项目名
模块名
文档类型（SRS）
版本或日期
```

示例：

```text
ruoyi-vue-pro-erp-warehouse-srs-20260607
```

## 7. retrieval 问题集设计

### 7.1 最低覆盖类型

Skill B 自动生成的问题集至少覆盖：

- 功能需求问题
- 字段规则问题
- 权限规则问题
- 异常处理问题
- 验收标准问题
- 明确排除项问题
- 风险项问题（若存在）

### 7.2 问题集目标

问题集的目的不是“模拟最终用户随便提问”，而是构造一组固定问题，用于判断知识库是否能稳定召回关键知识点。

### 7.3 风险项处理

若 Skill A 提供 `risk-items.md`，Skill B 必须：

- 把风险项转为检索问题；
- 或在 handoff 中记录“该风险需人工复核”；
- 不得在中间阶段把风险项静默忽略。

## 8. 离线可检索性预检

### 8.1 检查目标

离线可检索性预检用于判断当前文档是否具备进入真实 RAGFlow 检索验证的准备条件。

### 8.2 最低检查项

至少检查：

- 标题层级是否稳定。
- FR 编号是否存在且可定位。
- 功能需求是否能映射为固定问题。
- 字段规则是否可定位。
- 业务规则是否可定位。
- 权限规则是否可定位。
- 异常处理是否可定位。
- 验收标准是否可定位。
- 风险项是否明确。
- 关键规则是否没有被复杂表格或碎片化结构掩埋。

### 8.3 离线预检限制

离线预检不能替代：

- 真实 parser 行为
- 真实 chunk 切分效果
- 真实 retrieval 命中/误命中结果

因此离线预检只能用于 `offline_readiness_gate`，不能直接宣布 `online_retrieval_gate = pass`。

## 9. Gate 机制

### 9.1 offline_readiness_gate

#### pass

满足：

- Skill A 输入完整且前置条件满足。
- SRS 结构稳定。
- 关键功能、字段、权限、异常和验收标准都能生成检索问题。
- 风险项已显式暴露。
- 文档具备进入真实建库的准备条件。

#### conditional pass

满足：

- 文档主体可建库。
- 少量检索问题或风险项需要人工确认。
- 修复或确认后可进入真实 online 阶段。

#### fail

任一命中：

- Skill A 输入不完整。
- Skill A 前置 gate 不满足。
- 关键规则无法定位。
- 无法生成稳定 retrieval 问题集。
- 风险项被隐藏或消失。
- 文档结构明显不适合建库。

### 9.2 online_retrieval_gate

#### blocked

当真实 RAGFlow 不可用时，固定输出：

```text
online_retrieval_gate: blocked
blocked_reason: RAGFlow unavailable
```

#### pass / conditional pass / fail

仅在真实 RAGFlow 可用且已执行建库、解析、chunk 检查与 retrieval sanity check 后允许使用。

### 9.3 总体状态字段

建议输出：

```text
skill_b_status: offline_ready | blocked_waiting_ragflow | fail
```

语义：

- `offline_ready`：离线预检通过，且 online 阶段也已通过。
- `blocked_waiting_ragflow`：离线预检已完成，但 online 阶段因 RAGFlow 不可用而 blocked。
- `fail`：离线或在线阶段存在阻断问题。

## 10. 交接规则

### 10.1 交给 Skill C / 总编排的最小内容

Skill B Offline MVP 至少交付：

- 当前输入快照
- 知识库计划
- 解析配置计划
- retrieval 问题集
- offline_readiness_gate 结果
- online_retrieval_gate blocked 原因
- 风险项摘要

### 10.2 不允许的误导性结论

真实 RAGFlow 不可用时，不得写出：

```text
knowledge_base_ready_for_execution = true
online_retrieval_gate = pass
dataset_id = fake_xxx
chunk_count = 123
```

只能明确写为：

```text
online_retrieval_gate = blocked
blocked_reason = RAGFlow unavailable
```

## 11. Offline MVP 推荐样本

### 11.1 首个样本

建议优先使用：

```text
srs_generation/runs/ruoyi-vue-pro-erp-warehouse-validation-20260607/skill-a/
```

原因：

- 刚完成非研发可读性优化验证。
- 技术细节已下沉到 `source-evidence-map.md`。
- 适合作为 Skill B Offline MVP 的首个样例。

### 11.2 第二个样本

建议使用：

```text
srs_generation/runs/ruoyi-vue-pro-mes-stocktaking-task-validation-20260607/skill-a/
```

原因：

- 包含 `risk-items.md`。
- 适合验证风险项如何进入 retrieval 问题集与 handoff。

## 12. 一句话结论

Skill B Offline MVP 的职责是：**在真实 RAGFlow 不可用时，先把 Skill A 产出的 SRS 文档转化为可建库、可提问、可交接的标准输入，并明确给出 offline_readiness_gate 与 online_retrieval_gate blocked 语义，而不是伪造真实知识库结果。**
