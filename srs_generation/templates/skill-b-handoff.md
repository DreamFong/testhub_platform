# Skill B Handoff 模板

## 1. 当前状态

```text
status: 
execution_mode: offline_only | hybrid_mvp
offline_readiness_gate: 
online_retrieval_gate: 
skill_b_status: 
stop_point: 
```

## 2. 输入来源

- Skill A run: 
- SRS Markdown（主分析输入 / 默认主上传候选）: 
- SRS PDF（参考输入 / 默认不上传主知识库）: 
- source-evidence-map.md（必填分析输入 / 默认不上传主知识库）: 
- gate-result.md: 
- pdf-text-check-report.md: 
- risk-items.md: 

## 3. 知识库计划摘要

```text
recommended_kb_action: create_new | reuse_existing | blocked
recommended_kb_name: 
recommended_document_set: 
requires_user_confirmation: true | false
online_execution_requested: true | false
online_execution_completed: true | false
```

## 4. 解析配置计划摘要

```text
parse_strategy_summary: 
chunk_strategy_summary: 
real_parser_executed: true | false
real_chunk_result_available: true | false
retrieval_sanity_check_executed: true | false
```

## 5. 检索问题集摘要

```text
question_total: 
critical_question_total: 
risk_question_total: 
```

### 5.1 关键问题列表

- 

## 6. 风险项摘要

| 风险 | 来源 | 当前处理 | 后续动作 |
|---|---|---|---|
|  |  |  |  |

## 7. Gate 与限制

```text
offline_readiness_gate: 
online_retrieval_gate: 
blocked_reason: 
```

## 8. 后续动作建议

### 8.1 若尚未完成 online 验证，应执行

- 创建或复用知识库。
- 上传计划文档集。
- 按解析配置执行真实 parser。
- 检查 chunk 质量。
- 执行 retrieval sanity check。
- 更新 online_retrieval_gate。

### 8.2 当前不得做的声明

- 不得宣称知识库已真实通过检索验证。
- 不得伪造 dataset_id、chunk_count 或 retrieval 命中结果。
- 不得绕过 blocked 状态直接进入执行链路。
- 不得把 offline_readiness_gate = pass 直接解释为可进入 TestHub 执行链路。

## 9. 一句话交接结论

- 
