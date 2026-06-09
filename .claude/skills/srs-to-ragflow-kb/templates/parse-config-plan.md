# Skill B 解析配置计划模板

## 1. 基本信息

```text
project: 
target_module: 
run_id: 
plan_stage: parse_config_plan
status: draft
```

## 2. 计划适用对象

```text
target_kb_name: 
document_set: 
execution_mode: offline_only | online_enabled
```

## 3. 文档解析策略建议

| 文档 | 建议 parser / 模式 | 建议原因 | 风险 | 备注 |
|---|---|---|---|---|
| `srs-kb-friendly.md` |  |  |  |  |
| `srs-kb-friendly.pdf` |  |  |  |  |
| `source-evidence-map.md` |  |  |  |  |

## 4. chunk 策略计划

```text
chunk_strategy: 
chunk_size_hint: 
overlap_hint: 
heading_preservation_required: true | false
complex_table_risk: low | medium | high
```

## 5. 关键预期

- 期望保留稳定标题层级。
- 期望 FR 编号可检索。
- 期望字段规则、异常处理、验收标准不要被切碎。
- 期望风险项在真实 online 阶段可被专门验证。

## 6. 当前限制

```text
real_parser_executed: true | false
real_chunk_result_available: true | false
blocked_reason: 
```

## 7. 结论

```text
recommended_parse_config_ready: true | false
needs_online_verification: true | false
notes: 
```
