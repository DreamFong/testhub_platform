# Skill A：Review 与 Gate 机制

版本：v0.1  
适用范围：Skill A 自评、独立评审、人工复核与质量门禁

## 1. 目标

Review 与 Gate 机制用于判断 Skill A 生成的 SRS 是否具备进入 Skill B 的条件。它关注 SRS 文档本身的质量，不直接评估 RAGFlow 分块和检索效果。

## 2. 评审角色

### 2.1 生成 Agent 自评

生成 Agent 自评用于：

- 暴露生成过程中的风险。
- 标记不确定项。
- 主动发现缺失或误读。

自评不能作为最终通过依据。

### 2.2 独立评审 Agent

独立评审 Agent 是默认机器正式评分来源。它应使用独立上下文和独立提示词，对 SRS、source_evidence_map、PDF 检查结果进行核验。

### 2.3 人工复核

人工复核拥有最高裁决优先级，用于处理评分分歧、硬性不合格项争议和复杂模块边界问题。

## 3. 自评流程

### 3.1 自评输入

- scope-confirmation.md
- source-facts.md
- srs-kb-friendly.md
- source-evidence-map.md
- pdf-text-check-report.md

### 3.2 自评输出

- 五维评分。
- 硬性不合格项自查。
- 风险项。
- 不确定项。
- 必须修改项。
- 建议修改项。

### 3.3 自评限制

```text
自评不得作为最终通过依据。
自评为 pass 时，仍必须经过独立评审。
```

## 4. 独立评审流程

### 4.1 独立评审输入

- input-snapshot.md
- scope-inference.md
- scope-confirmation.md
- source-facts.md
- srs-kb-friendly.md
- source-evidence-map.md
- pdf-text-check-report.md
- self-review-report.md

### 4.2 独立评审输出

- 五维正式评分。
- 硬性不合格项检查。
- source evidence findings。
- required fixes。
- recommended improvements。
- final gate。

### 4.3 源码依据核验要求

独立评审必须检查：

- 每个主要 FR 是否有 evidence 支撑。
- 字段规则是否有 DTO / VO / Entity / Service 依据。
- 业务规则是否有 Service 或数据约束依据。
- 权限规则是否有权限注解、权限码或初始化配置依据。
- 异常规则是否有错误码和抛出逻辑依据。
- 验收标准是否能从功能规则合理推导。

## 5. 分差处理

### 5.1 分差计算

```text
score_gap_total = abs(self_review_total_score - independent_review_total_score)
score_gap_by_dimension = abs(self_dimension_score - independent_dimension_score)
```

### 5.2 触发人工复核条件

- 总分差 ≥ 3。
- 任一单项分差 ≥ 2。
- 自评为 pass 但独立评审为 fail。
- 是否命中硬性不合格项存在争议。
- 独立评审为 conditional pass。

## 6. Gate 判定

### 6.1 pass

条件：

- scope confirm 已完成。
- 无硬性不合格项。
- SRS 覆盖最终纳入范围。
- source_evidence_map 可支撑关键结论。
- PDF 文本层可提取。
- 无阻断级必须修改项。

### 6.2 conditional pass

条件：

- 无硬性不合格项。
- SRS 主体可用。
- 存在少量必须修改项。
- 修复后可进入 Skill B。

限制：

```text
conditional pass 不自动进入 Skill B。
```

### 6.3 fail

任一命中即 fail：

- scope confirm 未完成。
- 编造源码中不存在的需求、字段、权限或流程。
- 核心功能缺失。
- 关键规则写反。
- 文档结构不可用。
- PDF 文本层不可提取。
- 关键结论无法提供源码依据。

## 7. 必须修改项与 Gate 的关系

- 阻断级必须修改项存在时，gate 不能为 pass。
- 硬性不合格项存在时，gate 必须为 fail。
- 非阻断建议项不影响 pass。
- conditional pass 的必须修改项完成后，需要重新评审或人工确认。

## 8. 进入 Skill B 的最低条件

允许进入 Skill B：

- gate 为 pass。
- 或 conditional pass 的必须修改项已完成，并由人工明确允许进入 Skill B。

不得进入 Skill B：

- gate 为 fail。
- scope confirm 未完成。
- PDF 文本层不可提取。
- 关键 evidence 缺失且未完成人工复核。

## 9. 人工复核输出

人工复核应输出：

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

## 10. Review 报告结构

Review 报告必须包含：

1. Summary
2. Scorecard
3. Hard-fail Checklist
4. Source Evidence Findings
5. Required Fixes
6. Recommended Improvements
7. Final Gate
