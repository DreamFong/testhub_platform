# Skill B 输入快照模板

## 1. 基本信息

```text
project: 
skill_a_run_dir: 
target_module: 
run_id: 
execution_mode: offline_only | online_enabled
status: draft
```

## 2. 输入产物摘要

### 2.1 必填输入

```text
srs_markdown: 
source_evidence_map: 
skill_a_gate_result: 
pdf_text_check_report: 
```

### 2.2 选填输入

```text
srs_pdf: 
risk_items: 
knowledge_base_name_hint: 
manual_retrieval_questions: 
api_docs_path: 
```

## 3. Skill A 前置条件检查

| 检查项 | 结果 | 证据 | 备注 |
|---|---|---|---|
| Skill A gate 满足进入 Skill B 条件 | pass / conditional pass / fail |  |  |
| `pdf_text_layer_gate = pass` | 是 / 否 |  |  |
| `pdf_readability_gate = pass` | 是 / 否 |  |  |
| `source-evidence-map.md` 存在 | 是 / 否 |  |  |
| 关键风险项已读取 | 是 / 否 |  |  |

## 4. 运行环境约束

```text
ragflow_available: true | false
blocked_reason: 
external_operations_allowed: true | false
```

## 5. 首次判断

```text
offline_mvp_applicable: true | false
can_enter_kb_plan_stage: true | false
notes: 
```
