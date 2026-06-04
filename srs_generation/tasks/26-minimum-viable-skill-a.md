# 最小可行 Skill A 任务清单

## 目标

定义一个最小但完整的 Skill A 版本，避免一开始就把 A/B/C 全链路做得过大。

## 最小可行范围

最小可行 Skill A 只需要完成：

```text
source_project + target_module
→ scope 自动推断
→ 用户确认
→ SRS Markdown
→ PDF
→ source_evidence_map
→ 独立评审 gate
```

不包含：

- RAGFlow 建库
- chunk 质量检查
- retrieval gate
- 执行约束增强
- TestHub 自动化执行

## 必须完成任务

### 1. 输入

- [x] 支持 `source_project`
- [x] 支持 `target_module`
- [x] 支持可选 `entry_files`
- [x] 支持可选 `scope_hint`
- [x] 支持默认 `output_mode = kb-friendly`

### 2. Scope

- [x] 自动发现候选入口文件
- [x] 自动推断候选功能范围
- [x] 输出待确认相邻能力
- [x] 请求用户确认
- [x] 保存确认结果

### 3. SRS

- [x] 抽取功能点
- [x] 抽取字段规则
- [x] 抽取业务规则
- [x] 抽取权限规则
- [x] 抽取异常处理
- [x] 抽取验收标准
- [x] 生成 kb-friendly SRS Markdown

### 4. Evidence

- [x] 为每个 FR 记录源码依据
- [x] 为关键字段规则记录源码依据
- [x] 为关键业务规则记录源码依据
- [x] 为关键权限规则记录源码依据
- [x] 为关键异常规则记录源码依据

### 5. PDF

- [x] 生成 PDF
- [x] 检查文本层可提取
- [x] 检查 FR 编号可检索
- [x] 检查关键规则可检索

### 6. Review

- [x] 执行生成 Agent 自评
- [x] 执行独立评审 Agent 正式评分
- [x] 检查硬性不合格项
- [x] 输出 gate 结果

## 最小完成标准

- [x] 用户管理样本可完整跑通
- [x] 第二样本可完整跑通
- [x] 两个样本均有 SRS Markdown
- [x] 两个样本均有 PDF
- [x] 两个样本均有 source_evidence_map
- [x] 两个样本均有 independent_review_report
- [x] 两个样本均有明确 gate 结果

## 暂不做事项

- [x] 不自动创建 RAGFlow 知识库
- [x] 不做 RAGAS
- [x] 不自动生成 TestHub 执行用例
- [x] 不把执行约束混入 SRS

## 推荐下一步

先围绕这个最小可行 Skill A 完成 spec 和 prompt，再决定是否推进 Skill B。
