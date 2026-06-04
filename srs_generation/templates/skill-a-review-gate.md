# Skill A Review 与 Gate 模板

## 1. 基本信息

```text
project: 
target_module: 
run_id: 
review_stage: self_review | independent_review | manual_review
reviewer: 
reviewed_at: 
```

## 2. 评审输入

### 2.1 必须读取的产物

- [ ] input-snapshot.md
- [ ] scope-inference.md
- [ ] scope-confirmation.md
- [ ] source-facts.md
- [ ] srs-factual-draft.md
- [ ] srs-kb-friendly.md
- [ ] srs-kb-friendly.pdf
- [ ] source-evidence-map.md
- [ ] pdf-text-check-report.md

### 2.2 可选读取的产物

- [ ] srs-aligned.md
- [ ] srs-aligned.pdf
- [ ] reference_srs
- [ ] previous review report

## 3. 自评流程

生成 Agent 自评应输出：

- 五维评分。
- 硬性不合格项自查。
- 风险项。
- 不确定项。
- 必须修改项。
- 建议修改项。

规则：

```text
自评只作为参考，不能作为最终通过依据。
```

## 4. 独立评审流程

独立评审 Agent 必须检查：

- SRS 是否覆盖 scope confirmation 中的最终纳入范围。
- SRS 是否错误纳入明确排除范围。
- 每个主要 FR 是否有 source_evidence_map 支撑。
- 字段规则、业务规则、权限规则、异常规则是否与源码依据一致。
- PDF 文本层检查是否通过。
- 是否命中硬性不合格项。

独立评审输出作为默认机器正式评分。

## 5. 分差处理

### 5.1 分差计算

```text
score_gap_total = abs(self_review_total_score - independent_review_total_score)
score_gap_by_dimension = abs(self_dimension_score - independent_dimension_score)
```

### 5.2 触发人工复核

以下情况触发人工复核：

- 总分差 ≥ 3。
- 任一单项分差 ≥ 2。
- 是否命中硬性不合格项存在争议。
- 独立评审结果为 `conditional pass`。
- 独立评审结果为 `fail` 但生成 Agent 自评为 `pass`。

### 5.3 分差记录

| 维度 | 自评分 | 独立评分 | 分差 | 是否触发复核 |
|---|---:|---:|---:|---|
| 功能覆盖度 |  |  |  |  |
| 源码准确度 |  |  |  |  |
| 规则完整度 |  |  |  |  |
| 需求表达质量 |  |  |  |  |
| 知识库友好度 |  |  |  |  |
| 总分 |  |  |  |  |

## 6. Gate 判定规则

### 6.1 pass

满足全部条件：

- 无硬性不合格项。
- scope confirm 已完成。
- SRS 可覆盖最终纳入范围。
- source_evidence_map 能支撑关键结论。
- PDF 文本层可提取。
- 没有必须修改项，或仅有不阻断的小问题。

### 6.2 conditional pass

满足：

- 无硬性不合格项。
- SRS 主体可用。
- 存在必须修改项，但修改范围有限。
- 修复后可进入 Skill B。

`conditional pass` 不自动进入 Skill B，除非人工明确允许带条件交接。

### 6.3 fail

任一情况触发：

- 编造源码中不存在的需求、字段、权限或流程。
- 核心功能缺失。
- 关键规则写反。
- 文档结构不可用。
- PDF 文本层不可提取。
- 关键结论无法提供源码依据。
- scope confirm 未完成。

## 7. 必须修改项与 Gate 的关系

| 情况 | Gate |
|---|---|
| 无硬性不合格项，无必须修改项 | pass |
| 无硬性不合格项，有少量必须修改项 | conditional pass |
| 命中硬性不合格项 | fail |
| 关键结论无 evidence 且无法复核 | fail |
| PDF 文本层不可提取 | fail |
| scope 未确认 | fail |

## 8. 进入 Skill B 的最低条件

允许进入 Skill B：

- gate 为 `pass`。
- 或 gate 为 `conditional pass`，且必须修改项已完成并经人工允许。

不得进入 Skill B：

- gate 为 `fail`。
- scope confirm 未完成。
- PDF 文本层不可提取。
- 关键 evidence 缺失且未复核。

## 9. 人工复核

### 9.1 触发条件

- 分差达到触发阈值。
- gate 存在争议。
- 硬性不合格项存在争议。
- 模块边界复杂。
- 用户明确要求人工裁决。

### 9.2 人工复核输入资料

- scope-confirmation.md
- srs-kb-friendly.md
- source-evidence-map.md
- pdf-text-check-report.md
- self-review-report.md
- independent-review-report.md
- risk-items.md

### 9.3 人工复核输出格式

```text
manual_decision: pass | conditional pass | fail
reason: 
overrides_machine_review: true | false
required_fixes:
  - 
allowed_to_enter_skill_b: true | false
reviewer: 
reviewed_at: 
```

### 9.4 记录文件名

```text
manual-review-report.md
```

## 10. Review 报告结构

### 10.1 Summary

```text
summary: 
overall_score: 
gate: 
main_risks: 
```

### 10.2 Scorecard

引用或内嵌 Skill A 评分表。

### 10.3 Hard-fail Checklist

列出硬性不合格项检查结果。

### 10.4 Source Evidence Findings

记录 source_evidence_map 中发现的问题：

- 缺失 evidence。
- evidence 与 SRS 不一致。
- 低置信度 evidence。

### 10.5 Required Fixes

| 编号 | 问题 | 修改要求 | 阻断原因 |
|---|---|---|---|
|  |  |  |  |

### 10.6 Recommended Improvements

| 编号 | 建议 | 价值 |
|---|---|---|
|  |  |  |

### 10.7 Final Gate

```text
gate: pass | conditional pass | fail
allowed_next_stage: Skill B | none
reason: 
```
