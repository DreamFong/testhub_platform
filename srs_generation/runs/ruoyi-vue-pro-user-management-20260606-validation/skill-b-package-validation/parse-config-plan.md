# Parse Config Plan

## 1. 基本信息

```text
project: ruoyi-pro
target_module: user management
run_id: ruoyi-vue-pro-user-management-20260606-validation
execution_mode: offline_only
```

## 2. 推荐载体

```text
recommended_upload_carrier: TXT generated from srs-kb-friendly.md
fallback_carrier: srs-kb-friendly.pdf only for parser comparison, not primary handoff
not_recommended_carrier: direct Markdown upload in current tested RAGFlow environment
```

## 3. 解析策略摘要

| 载体 | 推荐动作 | 解析方式 | 风险 |
|---|---|---|---|
| Markdown | 不直接上传 | 当前环境历史验证不支持 `.md` | parse failed / no chunks |
| PDF | 不作为主结果 | PDF + DeepDOC + book | 可能标题串接、正文丢失、短 chunk |
| TXT | 推荐 | book | 顶层标题可能重复进入 chunk，但整体可控 |

## 4. TXT 载体生成原则

- 从 `srs-kb-friendly.md` 转换，不改变业务语义。
- 保留当前章节标题与 FR 标题，帮助检索定位。
- 可去掉无助于检索的过度重复总标题。
- 不把 `source-evidence-map.md` 合并进主 TXT。

## 5. chunk 质量检查点

真实 online 阶段应检查：

- 是否生成 chunks。
- 是否存在只有标题、没有正文的短块。
- 是否存在相邻 FR 标题串接但正文丢失。
- 字段规则、异常处理、验收标准是否可定位。
- 核心业务规则是否出现在同一或相邻合理 chunks 中。

## 6. 结论

```text
recommended_parse_config_ready: true
needs_online_verification: true
recommended_online_test_scope: P0/P1 retrieval questions from retrieval-question-set.md
notes: 本次只完成离线解析计划，不产生真实 parser / chunk 结果。
```
