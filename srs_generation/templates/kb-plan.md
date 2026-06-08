# Skill B 知识库计划模板

## 1. 基本信息

```text
project: 
target_module: 
run_id: 
plan_stage: kb_plan
status: draft
```

## 2. 目标

```text
本计划用于说明：
- 是否建议创建新知识库
- 是否建议复用已有知识库
- 建议上传哪些文档
- 在真实 RAGFlow 可用后需要执行哪些外部操作
```

## 3. 知识库创建 / 复用建议

```text
action: create_new | reuse_existing | blocked
recommended_kb_name: 
recommended_kb_type: srs_only | srs_plus_api_docs
reuse_candidate: 
reason: 
```

## 4. 建议上传文档

| 文档 | 是否建议上传 | 用途 | 原因 | 备注 |
|---|---|---|---|---|
| `srs-kb-friendly.md` | 是 / 否 | 主 SRS 知识源 | 默认主上传候选 |  |
| `srs-kb-friendly.pdf` | 是 / 否 | 对比实验 / 交付参考 | 默认不上传到主知识库 |  |
| `source-evidence-map.md` | 是 / 否 | 辅助追溯材料 | 默认不上传到主知识库 |  |
| 其他文档 | 是 / 否 |  |  |  |

## 5. 外部操作前置确认项

| 项目 | 是否需要用户确认 | 说明 |
|---|---|---|
| 创建新知识库 | 是 / 否 |  |
| 复用已有知识库 | 是 / 否 |  |
| 上传 PDF | 是 / 否 |  |
| 上传 Markdown | 是 / 否 |  |
| 上传 evidence map | 是 / 否 |  |

## 6. 当前阻塞信息

```text
ragflow_available: true | false
blocked_reason: 
can_execute_now: true | false
```

## 7. 结论

```text
recommended_next_action: wait_for_ragflow | ask_user_confirmation | return_to_skill_a | blocked
reason: 
```
