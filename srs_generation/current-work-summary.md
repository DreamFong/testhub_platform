# 当前 SRS 逆向生成工作总结

## 1. 工作目标

本轮工作的目标是围绕 `RuoYi-Vue-Pro` 用户管理模块，完成一条可复现、可推广的源码逆向生成 SRS 主线，并验证其在 RAGFlow 中作为需求知识库输入的可用性。进一步目标是把这条主线沉淀为可推广到其他项目的 skill 能力层。

整体目标拆分为三部分：

```text
1. 复现既有 SRS v2 的生成主线
2. 验证再生成 SRS 在 RAGFlow 中的分块与检索质量
3. 抽象出 skill 拆分结构，为后续推广做准备
```

---

## 2. 已完成工作

### 2.1 明确复现基准

已明确当前复现的主基准为：

```text
知识库名称：ruoyi-user-srs
SRS_KB_ID / dataset_id：49c03fa043a311f18243434b552cc465
文档：ruoyi-user-management-srs-v2.pdf
```

该知识库是一个**纯基于原始 SRS v2 PDF 的需求知识库**，用于评估 SRS 文档生成与分块质量。

同时明确了：

- `e2e-srs-user-mgmt` 不是纯 SRS 知识库；
- 它是 `SRS + 执行约束补充文本` 的混合知识库；
- 更适合作为 RAGFlow → TestHub 最小闭环的参考，而不是纯 SRS 复现基准。

### 2.2 定位并确认源码项目

已确认源码项目路径为：

```text
~/projects/github/ruoyi-vue-pro
```

并完成了用户管理模块核心源码入口的定位，覆盖：

- `UserController.java`
- `AdminUserServiceImpl.java`
- `UserSaveReqVO.java`
- `UserPageReqVO.java`
- `UserRespVO.java`
- `UserImportExcelVO.java`
- `UserUpdatePasswordReqVO.java`
- `UserUpdateStatusReqVO.java`
- `AdminUserDO.java`
- `AdminUserMapper.java`
- `ErrorCodeConstants.java`
- `sql/mysql/ruoyi-vue-pro.sql`

这些文件已经足够支撑从源码逆向抽取：

- 功能点
- 字段规则
- 业务规则
- 异常处理
- 权限规则
- 验收标准

### 2.3 拆解既有 SRS v2 结构与验收标准

已完成对 `docs/ruoyi-user-management-srs-v2.pdf` 的结构化拆解，产出：

- `artifacts/ruoyi-srs-v2-baseline-analysis.md`

该文档整理了：

- 章节结构
- FR-USER-001 ~ FR-USER-012 功能范围
- 字段规则基准
- 业务规则基准
- 权限规则基准
- 异常处理基准
- 验收标准基准
- 边界和排除项
- 对应源码依据位置

### 2.4 基于源码逆向生成第一版 SRS 草稿

已完成从源码抽取需求语义，并生成第一版逆向 SRS 草稿：

- `artifacts/ruoyi-user-management-srs-regenerated-draft.md`

这版草稿已经覆盖了：

- 用户列表查询
- 精简用户列表
- 用户详情
- 新增、编辑、删除、批量删除
- 重置密码
- 状态修改
- 用户导入、导出
- 字段规则
- 业务规则
- 权限规则
- 错误处理
- 验收标准

### 2.5 对比基准并生成对齐版 SRS

已完成基准对比分析，产出：

- `artifacts/ruoyi-srs-regeneration-comparison.md`

对比结论包括：

- 第一版草稿在内容覆盖上已经基本完整；
- 但表达风格更偏“源码事实说明”；
- 需要向既有 SRS v2 的正式需求文档风格靠拢。

基于该结论，已进一步生成：

- `artifacts/ruoyi-user-management-srs-v2-regenerated-aligned.md`

该版本已经按既有 SRS v2 的章节结构和需求表达方式进行了对齐。

### 2.6 生成 PDF 并做文本层检查

已完成对齐版 SRS 的 PDF 生成与文本层检查，产出：

- `artifacts/generate_ruoyi_srs_pdf.py`
- `artifacts/ruoyi-user-management-srs-v2-regenerated-aligned.pdf`
- `artifacts/ruoyi-srs-pdf-text-layer-quality-report.md`

检查结果表明：

- PDF 文本层可提取；
- 标题结构、FR 功能编号、主要规则均可检索；
- 但表格型内容在 RAGFlow `book + DeepDOC` 下存在不稳定风险。

### 2.7 针对 RAGFlow 解析特点优化为连续段落版

为解决表格被 DeepDOC 抽取不稳定的问题，已进一步生成一版 RAGFlow 友好的连续段落版：

- `artifacts/ruoyi-user-management-srs-v2-regenerated-ragflow-friendly.md`
- `artifacts/generate_ruoyi_srs_ragflow_friendly_pdf.py`
- `artifacts/ruoyi-user-management-srs-v2-regenerated-ragflow-friendly.pdf`

这一版将以下内容从表格改成连续段落：

- 字段规则
- 权限规则
- 错误处理
- 验收标准

目标是提高 `book + DeepDOC` 下的 chunk 稳定性和检索可用性。

### 2.8 完成 RAGFlow 分块验证

已分别对两版再生成 PDF 做 RAGFlow 验证：

#### 表格对齐版知识库

```text
名称：ruoyi-user-srs-regenerated-aligned-20260603
SRS_KB_ID：6aa9ae305f1011f18243434b552cc465
chunks：34
短 chunk 数：1
短 chunk 比例：2.94%
```

特点：

- chunk 数与原始 `ruoyi-user-srs` 的 35 非常接近；
- 但表格明细在 RAGFlow 中抽取不稳定。

#### 连续段落版知识库

```text
名称：ruoyi-user-srs-regenerated-ragflow-friendly-20260603
SRS_KB_ID：804270d25f1111f18243434b552cc465
chunks：67
短 chunk 数：1
短 chunk 比例：1.49%
retrieval_gate = pass
```

特点：

- chunk 数明显高于原始 SRS 知识库；
- 但字段规则、错误处理、验收标准等检索更稳定；
- 更适合作为后续可推广 skill 的默认输出格式。

对应报告：

- `artifacts/ragflow-chunk-evaluation.md`

### 2.9 澄清知识库职责边界

当前已经明确区分了两类知识库：

#### 纯 SRS 需求知识库

代表：

- `ruoyi-user-srs`
- `ruoyi-user-srs-regenerated-aligned-20260603`
- `ruoyi-user-srs-regenerated-ragflow-friendly-20260603`

职责：

- 承载需求、字段、异常、验收等业务知识；
- 作为 SRS 文档质量和需求检索质量的基准。

#### SRS + 执行约束混合知识库

代表：

- `e2e-srs-user-mgmt`

特点：

- 除原始 SRS PDF 外，还包含：
  - `ragflow-stage0-user-mgmt-requirement.txt`
  - `ragflow-stage0-user-mgmt-requirement(1).txt`
- 额外携带：
  - token 提取规则
  - userId 提取规则
  - create / update 最小 body 规则
  - 禁止错误字段与路径

结论：

- `ruoyi-user-srs` 适合作为 **SRS 复现基准**；
- `e2e-srs-user-mgmt` 适合作为 **TestHub 执行增强参考**。

### 2.10 输出了通用链路图与 skill 拆分图

已生成两张本地 SVG：

- `artifacts/source-to-srs-ragflow-skill-workflow.svg`
- `artifacts/skill-split-architecture.svg`

其中：

#### 通用链路图

说明了：

```text
源码
→ 需求语义抽取
→ SRS 初稿
→ RAGFlow 友好化改写
→ PDF
→ 本地文本层检查
→ RAGFlow 知识库验证
→ 进入 TestHub 自动化闭环
```

#### skill 拆分图

将整体能力拆成三层：

- Skill A：源码逆向生成 SRS
- Skill B：知识库构建与分块验证
- Skill C：执行约束增强层

并明确：

- `ragflow-testhub-agent-workflow` 是最终编排型 skill；
- A / B / C 是它前面的前置能力层。

---

## 3. 当前阶段结论

当前主线已经完成到：

```text
源码阅读
→ SRS 逆向生成
→ PDF 生成
→ RAGFlow 分块验证
→ 检索 sanity check
→ retrieval gate pass
```

也就是说：

- 这条“源码逆向生成 SRS”的链路已经不是纸面方案，而是已跑通；
- 目前已经有一套可执行的中间产物链；
- 也已经明确了“最像原始分块”和“最适合推广”的两个不同方向：
  - 最像原始：表格对齐版
  - 最适合推广：连续段落版

---

## 4. 当前推荐结论

### 4.1 如果目标是复现原始 `ruoyi-user-srs`

优先参考：

- `ruoyi-user-srs`
- `artifacts/ruoyi-user-management-srs-v2-regenerated-aligned.md`
- `artifacts/ruoyi-user-management-srs-v2-regenerated-aligned.pdf`

因为：

- chunk 数最接近原始基准（34 vs 35）；
- 章节结构和文档风格最贴近原始 SRS v2。

### 4.2 如果目标是做成可推广 skill

优先参考：

- `artifacts/ruoyi-user-management-srs-v2-regenerated-ragflow-friendly.md`
- `artifacts/ruoyi-user-management-srs-v2-regenerated-ragflow-friendly.pdf`
- `ruoyi-user-srs-regenerated-ragflow-friendly-20260603`

因为：

- 连续段落版在 RAGFlow 中对字段规则、错误处理、验收标准的检索更稳定；
- 更适合用作 skill 的默认输出格式；
- retrieval gate 已通过。

---

## 5. 下一步建议

下一步应进入 **skill 沉淀** 阶段，建议按以下顺序推进：

### 5.1 先沉淀 Skill A

目标：

```text
源码 → PRD / SRS Markdown → PDF
```

输出：

- 输入参数定义
- 输出产物定义
- 通用章节模板
- 源码抽取规则
- RAGFlow 友好化改写规则

### 5.2 再沉淀 Skill B

目标：

```text
SRS / API docs → RAGFlow 知识库 → chunk 检查 → retrieval gate
```

输出：

- 知识库创建 / 复用规则
- chunk 质量门槛
- 检索 sanity check 规则
- handoff 输出格式

### 5.3 最后沉淀 Skill C

目标：

```text
真实跑通案例 → 执行约束规则
```

输出：

- token / userId 提取规则
- 最小字段模板
- 必带 headers
- 错误字段黑名单
- 最小闭环模板

---

## 6. 当前产物总览

### 文档与报告

- `ruoyi-user-management-srs-v2-reverse-generation-report.md`
- `ruoyi-srs-reproduction-checklist.md`
- `srs_generation/current-work-summary.md`

### 中间工件

- `artifacts/ruoyi-srs-v2-baseline-analysis.md`
- `artifacts/ruoyi-user-management-srs-regenerated-draft.md`
- `artifacts/ruoyi-srs-regeneration-comparison.md`
- `artifacts/ruoyi-user-management-srs-v2-regenerated-aligned.md`
- `artifacts/ruoyi-user-management-srs-v2-regenerated-ragflow-friendly.md`
- `artifacts/ragflow-chunk-evaluation.md`
- `artifacts/ruoyi-srs-pdf-text-layer-quality-report.md`

### PDF 与脚本

- `artifacts/ruoyi-user-management-srs-v2-regenerated-aligned.pdf`
- `artifacts/ruoyi-user-management-srs-v2-regenerated-ragflow-friendly.pdf`
- `artifacts/generate_ruoyi_srs_pdf.py`
- `artifacts/generate_ruoyi_srs_ragflow_friendly_pdf.py`

### 图示

- `artifacts/source-to-srs-ragflow-skill-workflow.svg`
- `artifacts/skill-split-architecture.svg`

---

## 7. Skill A 质量评判机制补充结论

### 7.1 默认输出方向

Skill A 默认输出 **知识库友好版** SRS，而不是优先输出对齐版。对齐版用于复现历史 SRS 风格和原始分块特征；知识库友好版用于后续 RAGFlow 知识库构建和 skill 推广。

### 7.2 Skill A 评分维度

Skill A 的评分只评估 SRS 文档本身，不直接评估 RAGFlow 检索效果。建议采用 5 个维度、每项 5 分、总分 25 分：

1. 功能覆盖度
2. 源码准确度
3. 规则完整度
4. 需求表达质量
5. 知识库友好度

### 7.3 硬性不合格项

如果出现以下情况，即使总分较高也不能进入 Skill B：

- 编造源码中不存在的需求、字段、权限或流程
- 核心功能缺失
- 关键规则写反
- 文档结构不可用
- PDF 文本层不可提取

### 7.4 三阶段打分机制

Skill A 采用三阶段打分：

1. 生成 Agent 自评分：作为参考分，用于自检和暴露风险点。
2. 独立评审 Agent 正式评分：作为机器评审主分数，用于判断是否允许进入 Skill B。
3. 人工复核评分或确认：作为最终裁决，可覆盖前两阶段结论。

生成 Agent 和评审 Agent 可以使用同一个模型，但必须是不同 Agent、不同上下文、不同提示词。生成 Agent 自评分不能作为最终通过依据；评审 Agent 评分是默认机器正式分；人工复核拥有最高优先级。

如果生成 Agent 自评分和独立评审 Agent 评分相差较大，例如总分相差 3 分及以上，应触发人工复核或二次评审。

### 7.5 与 Skill B 检索质量评估的关系

Skill A 不直接评估检索准确率、检索召回率、答案忠实度和答案相关性。这些指标属于 Skill B 的知识库检索质量评估，可后续结合 RAGAS 实现。

当前建议边界为：

```text
Skill A：评估 SRS 文档质量
Skill B：评估 RAGFlow 分块质量与检索质量
```

---

## 8. 当前一句话总结

当前已经完成：**从 `RuoYi-Vue-Pro` 用户管理源码逆向生成 SRS、生成 PDF、在 RAGFlow 中完成分块与检索验证，初步拆解出可推广的 skill 结构，并补充了 Skill A 的质量评判机制。**
