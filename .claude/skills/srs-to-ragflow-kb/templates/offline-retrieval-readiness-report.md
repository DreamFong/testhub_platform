# Skill B 离线可检索性预检报告模板

## 1. 基本信息

```text
project: 
target_module: 
run_id: 
review_stage: offline_readiness
reviewer: 
reviewed_at: 
```

## 2. 已复用的 Skill A 结论

| 项目 | 结果 | 证据 | 是否重复检查 |
|---|---|---|---|
| Skill A gate |  |  | 否 |
| PDF 文本层 gate |  |  | 否 |
| PDF 可读性 gate |  |  | 否 |
| 主文档 kb-friendly 一阶要求 |  |  | 部分复用 |

## 3. Skill B Offline 新增检查项

| 检查项 | 结果 | 证据 | 是否阻断 |
|---|---|---|---|
| 可生成功能需求问题 | pass / conditional pass / fail |  | 是 / 否 |
| 可生成字段规则问题 | pass / conditional pass / fail |  | 是 / 否 |
| 可生成权限规则问题 | pass / conditional pass / fail |  | 是 / 否 |
| 可生成异常处理问题 | pass / conditional pass / fail |  | 是 / 否 |
| 可生成验收标准问题 | pass / conditional pass / fail |  | 是 / 否 |
| 可生成排除项问题 | pass / conditional pass / fail |  | 是 / 否 |
| 风险项已纳入问题集或 handoff | pass / conditional pass / fail |  | 是 / 否 |
| 文档结构适合进入真实建库计划 | pass / conditional pass / fail |  | 是 / 否 |

## 4. 主要发现

### 4.1 正向结论

- 

### 4.2 风险与限制

- 

### 4.3 需要回退 Skill A 的问题

- 

## 5. Gate 建议

```text
offline_readiness_gate: pass | conditional pass | fail
reason: 
requires_manual_review: true | false
can_prepare_online_stage: true | false
```

## 6. 说明

```text
本报告不代表真实 RAGFlow 检索已经通过。
若 RAGFlow 当前不可用，online_retrieval_gate 应在后续结果中标记为 blocked。
```
