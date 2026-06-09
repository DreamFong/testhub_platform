# KB Plan

## 1. 基本信息

```text
project: ruoyi-pro
target_module: user management
run_id: ruoyi-vue-pro-user-management-20260606-validation
plan_mode: offline_package_validation
```

## 2. 知识库目标

```text
knowledge_base_purpose: 为后续 TestHub 场景生成准备可检索的 SRS 知识库
expected_downstream_use: RAGFlow Agent retrieval / Skill C execution constraint extraction
business_domain: 用户管理
```

## 3. 推荐知识库动作

```text
recommended_kb_action: create_new
recommended_kb_name: ruoyi-pro-user-management-srs-txt-validation
recommended_document_set: TXT carrier generated from srs-kb-friendly.md
requires_user_confirmation: true
```

## 4. 文档上传策略

| 文档 | 默认动作 | 原因 |
|---|---|---|
| `srs-kb-friendly.md` | 不直接上传，优先转为 TXT 载体 | 当前 RAGFlow 环境历史验证不支持 `.md` 解析 |
| `srs-kb-friendly.pdf` | 不作为主上传材料 | PDF 曾出现标题串接和正文丢失，解析成功不等于 chunk 质量可用 |
| `source-evidence-map.md` | 不上传主 SRS KB | 作为必填分析输入和追溯依据，避免源码细节污染主业务 KB |
| TXT carrier | 推荐作为主上传材料 | 最接近 SRS 原文结构，历史验证 chunk 更稳定 |

## 5. 外部操作确认项

真实 online 阶段开始前，必须由用户确认：

- 是否允许访问 RAGFlow。
- 是否新建 dataset。
- 是否仅上传 TXT carrier。
- 是否继续不上传 `source-evidence-map.md`。
- 是否记录 `SRS_KB_ID` 用于 Skill C。

## 6. 阻塞信息

```text
ragflow_available: not_checked
blocked_reason: online step not executed yet
can_execute_now: false
```

## 7. 结论

```text
recommended_next_action: request_online_execution
reason: 离线输入完整，主文档适合转 TXT 载体进入 RAGFlow；但本次验证未获授权执行真实 online 操作，因此不能宣称知识库已通过检索验证。
```
