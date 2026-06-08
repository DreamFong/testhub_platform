# Skill B Handoff

## 1. 当前状态

```text
status: final
execution_mode: hybrid_mvp
offline_readiness_gate: pass
online_retrieval_gate: conditional pass
skill_b_status: online_verified_with_risks
stop_point: skill_b_complete_ready_for_skill_c
```

## 2. 输入来源

- Skill A run: `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-a/`
- SRS Markdown（主分析输入 / 默认主上传候选）: `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-a/srs-kb-friendly.md`
- SRS PDF（参考输入 / 默认不上传主知识库）: `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-a/srs-kb-friendly.pdf`
- source-evidence-map.md（必填分析输入 / 默认不上传主知识库）: `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-a/source-evidence-map.md`
- gate-result.md: `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-a/gate-result.md`
- pdf-text-check-report.md: `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-a/pdf-text-check-report.md`
- risk-items.md: 未生成

## 3. 知识库计划摘要

```text
recommended_kb_action: create_new
recommended_kb_name: ruoyi-pro-user-management-srs-txt-20260608
recommended_document_set: /tmp/ruoyi-pro-user-management-srs-20260608.txt
requires_user_confirmation: false
online_execution_requested: true
online_execution_completed: true
```

## 4. 解析配置计划摘要

```text
parse_strategy_summary: 使用 TXT 载体替代 Markdown/PDF，避免 PDF OCR 与布局重建引入的正文丢失和标题串接问题。
chunk_strategy_summary: 使用 built-in = book；chunk 形态以“章节标题 + 完整规则/需求句”为主。
real_parser_executed: true
real_chunk_result_available: true
retrieval_sanity_check_executed: true
```

## 5. 检索问题集摘要

```text
question_total: 6
critical_question_total: 5
risk_question_total: 1
```

### 5.1 关键问题列表

- 查询用户列表支持哪些筛选条件。
- 新增用户成功后默认状态是什么，还会建立什么关联。
- 新增或修改用户前需要满足哪些唯一性规则。
- 禁用用户后系统还必须执行什么安全动作。
- 当导入数据为空、初始化密码未配置或租户账号配额不足时，系统如何处理。
- 这些需求的实现依据下沉到了哪里，包含哪些类型的源码证据。

## 6. 风险项摘要

| 风险 | 来源 | 当前处理 | 后续动作 |
|---|---|---|---|
| Markdown 在当前环境不可解析 | RAGFlow 文档类型限制 | 改用 TXT 临时载体完成 online 验证 | 若后续固定走 RAGFlow，应优先沉淀可上传 TXT 载体策略 |
| PDF 解析存在标题串接与正文丢失 | PDF + DeepDOC 实测结果 | 不采用 PDF 结果作为本次主 handoff | 若需保留 PDF 交付，应将 PDF 仅作为阅读版，而非主建库载体 |
| 源码级证据追溯仅弱命中 | 当前未上传 `source-evidence-map.md` | 保持主 SRS KB 专注业务检索 | 后续如需源码级追溯，可单独构建 evidence KB |
| 顶层文档标题重复进入 chunk | TXT + book 切块噪声 | 记录为轻度噪声，不阻断使用 | 下游 retrieval 建议至少查看 top 3 |

## 7. Gate 与限制

```text
offline_readiness_gate: pass
online_retrieval_gate: conditional pass
blocked_reason: 
```

## 8. RAGFlow online 验证结果

```text
PROJECT_NAME=ruoyi-pro
BUSINESS_DOMAIN=user management
TEST_SCOPE=用户新增、编辑、启停用、唯一性校验、权限约束、异常提示
MIN_BUSINESS_FLOW=查询用户列表 → 新增用户 → 编辑用户 → 禁用用户
SRS_KB_ID=00c0dbdc632111f18243434b552cc465
API_DOCS_KB_ID=
```

### 8.1 实际运行记录

- Markdown 尝试：上传成功，但解析失败；当前环境不支持 `.md` 作为可解析文档类型。
- PDF 尝试：解析成功，但人工抽检发现相邻章节标题串接、正文内容丢失，故不采纳为主结果。
- TXT 尝试：
  - dataset: `ruoyi-pro-user-management-srs-txt-20260608`
  - dataset_id / SRS_KB_ID: `00c0dbdc632111f18243434b552cc465`
  - document_id: `00c783a6632111f18243434b552cc465`
  - parse status: `DONE`
  - chunk_count: `37`
  - retrieval sanity checks: 5 命中，1 弱命中，0 未命中

### 8.2 推荐 retrieval 参数

```text
similarity_threshold: 0.25 ~ 0.30
keywords_similarity_weight: 0.60
vector_weight: 0.40
top_n: 5 ~ 8
top_k: 1024
use_kg: false
```

## 9. 后续动作建议

### 9.1 建议进入 Skill C

- 当前 TXT SRS KB 已能支持业务需求、字段规则、异常处理和最小业务流的稳定检索。
- 下一阶段应提炼“哪些规则可直接进入执行、哪些规则需保持风险提示、哪些追溯信息不应混入主 SRS KB”。

### 9.2 当前不得做的声明

- 不得把当前 SRS_KB 解释为“已覆盖源码级证据追溯”。
- 不得把 PDF 方案的解析成功误判为结构质量已通过。
- 不得省略 TXT 作为当前主 handoff 载体这一前提。

## 10. 一句话交接结论

- 当前 Skill B 已完成真实 online 验证，主 handoff 结果应采用 TXT 载体生成的 SRS_KB；该知识库适合进入 Skill C，但源码级追溯仍需通过 `source-evidence-map.md` 或后续独立 evidence KB 补充。
