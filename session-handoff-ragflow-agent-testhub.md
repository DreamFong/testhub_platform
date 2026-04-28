# RAGFlow → TestHub Agent 构建交接摘要

- 日期：2026-04-27
- 项目：testhub_platform
- 分支：main
- 阶段：RAGFlow Agent 已可生成符合 TestHub 契约的最小测试场景 JSON，下一步待导入 TestHub 执行验证

---

## 1. 背景目标

目标是打通端到端流程：

```text
RAGFlow 知识库（SRS + API 文档）
→ RAGFlow Agent 生成 TestHub 场景 JSON
→ TestHub 导入接口消费 JSON
→ 创建 API 测试项目、环境、集合、请求、套件和步骤
→ 执行测试套件验证变量提取、步骤依赖和断言
```

本轮工作承接已有成果：

- TestHub 侧导入契约已定义：`contracts/ragflow-testhub-scenario-schema.json`
- TestHub 导入服务已实现：`apps/api_testing/services/scenario_import.py`
- RuoYi API 文档知识库已创建：`ruoyi-api-docs`
- RuoYi 用户管理 SRS v2 PDF 已生成并验证 chunk 质量更优

---

## 2. 已确认的 TestHub 导入契约

核心契约文件：


| 文件                                                 | 说明                                      |
| -------------------------------------------------- | --------------------------------------- |
| `contracts/ragflow-testhub-scenario-schema.json`   | RAGFlow → TestHub 场景 JSON Schema v1.0.0 |
| `contracts/examples/ruoyi-user-mgmt-scenario.json` | 示例场景                                    |
| `apps/api_testing/services/scenario_import.py`     | TestHub 场景导入服务                          |


Agent 最终必须输出纯 JSON，顶层结构：

```json
{
  "schema_version": "1.0.0",
  "project": {},
  "environment": {},
  "collections": [],
  "suites": [],
  "metadata": {}
}
```

关键约束：

- `schema_version` 固定为 `1.0.0`
- `project` 必须是对象，不能是字符串
- `environment` 必须包含 `name`、`scope`、`variables`
- `headers` 必须是数组，每项为 `{ "key": "...", "value": "...", "enabled": true }`
- `assertions` 必须使用 `type` 和 `expected`
- `status_code` 断言示例：

```json
{"type":"status_code","name":"状态码200","expected":200}
```

- `json_path` 断言示例：

```json
{"type":"json_path","name":"code为0","json_path":"$.code","expected":0}
```

- `variable_extractions` 中 `source=body` 时必须包含 `json_path`
- `collections[].requests[].name` 全局唯一
- `suites[].steps[].request_name` 必须引用已存在 request
- 同一 suite 内不能重复引用同一 request

---

## 3. 当前可用知识库

### 3.1 SRS v2 知识库


| 项目         | 值                                       |
| ---------- | --------------------------------------- |
| 知识库名       | `ruoyi-prd-srs-v2-book-deepdoc`         |
| dataset_id | `e2a33ef6416f11f1bb078f6f74f53e6e`      |
| 文档         | `docs/ruoyi-user-management-srs-v2.pdf` |
| 解析方式       | `book + DeepDOC`                        |
| chunks     | 35                                      |
| <50 字碎片率   | 约 5.71%                                 |
| 状态         | 推荐使用                                    |


SRS v2 相比 v1 增强点：

- 明确新增用户必填字段：用户账号、用户昵称、密码
- 明确可选字段：部门、岗位、手机号、邮箱、性别、备注、头像
- 补充唯一性异常：账号/手机号/邮箱重复提示
- 补充导入异常：初始密码为空、导入文件为空
- 新增 `3.6 Error Handling and Messages` 章节

### 3.2 API 文档知识库


| 项目         | 值                                     |
| ---------- | ------------------------------------- |
| 知识库名       | `ruoyi-api-docs`                      |
| dataset_id | `02b7eebc3f1311f1bb078f6f74f53e6e`    |
| 分块方式       | `book`                                |
| 用途         | 提供真实 API method/path/body/response 信息 |


---

## 4. overlap 与解析方式结论

曾测试 `naive + DeepDOC + overlapped_percent=0.2`，重新上传 PDF 并解析后，实际 chunk 相邻边界只有极少重复，不能视为稳定生效。

后续修正后的结论：

- 原生 RAGFlow 中 `overlapped_percent` 并非完全不存在
- 官方实现中主要由 `naive` 和 Flow `TokenChunker` 消费 overlap
- `book + DeepDOC` 不应期待 overlap 生效
- 当前主线不依赖 overlap，而是通过 SRS 风格 PDF 降低碎片率、提升语义边界质量

---

## 5. RAGFlow Agent 构建过程

### 5.1 Agent 调用接口

RAGFlow Agent 调用方式：

```text
POST /api/v1/agents/{agent_id}/sessions?user_id=...
POST /api/v1/agents/{agent_id}/completions
```

非流式 completion 最终文本字段：

```text
data.data.content
```

### 5.2 第一个 Agent：Agent-with-tools 方案


| 项目       | 值                                              |
| -------- | ---------------------------------------------- |
| 标题       | `TestHub 测试场景生成 Agent - RuoYi 用户管理`            |
| agent_id | `ddb2f69e417311f1bb078f6f74f53e6e`             |
| 拓扑       | `Begin → Agent(with Retrieval tool) → Message` |
| 结论       | 不推荐继续使用                                        |


问题：

- 即使 prompt 强制只输出 JSON，该 Agent 仍输出解释性摘要
- 输出形如 `The provided JSON represents...`
- 不适合作为 TestHub 导入 JSON 生成器

### 5.3 第二个 Agent：显式 LLM 工作流方案


| 项目       | 值                                           |
| -------- | ------------------------------------------- |
| 标题       | `TestHub 测试场景生成 Agent - RuoYi 用户管理 v2显式工作流` |
| agent_id | `728d08a8417511f1bb078f6f74f53e6e`          |
| 状态       | 当前推荐使用                                      |


有效拓扑：

```text
Begin
→ LLM:QueryRewrite
→ Retrieval:Knowledge
→ LLM:ScenarioGen
→ Message:Output
```

重要修正：

- RAGFlow v0.24.0 中显式生成组件应使用 `component_name: "LLM"`
- 不应使用旧摘要中的 `Generate`
- Message 引用：`{LLM:ScenarioGen@content}`
- Retrieval 引用 QueryRewrite 输出：`{LLM:QueryRewrite@content}`

Retrieval 参数：

```json
{
  "kb_ids": [
    "e2a33ef6416f11f1bb078f6f74f53e6e",
    "02b7eebc3f1311f1bb078f6f74f53e6e"
  ],
  "similarity_threshold": 0.3,
  "keywords_similarity_weight": 0.6,
  "top_k": 1024,
  "top_n": 8,
  "rerank_id": "bge-reranker-v2-m3___OpenAI-API@OpenAI-API-Compatible",
  "use_kg": false
}
```

---

## 6. Agent 输出验证结果

### 6.1 首次显式工作流测试

第一次显式工作流输出已经是 JSON，但被截断，导致无法解析。

处理方式：

- 放宽 `LLM:ScenarioGen` 的 `max_tokens`
- 将测试范围缩小为最小主流程

### 6.2 Schema 错误修正

第二次输出完整 JSON，但 schema 校验发现错误：

- `project` 被输出成字符串，而 schema 要求对象
- `environment` 缺少 `name`
- `headers` 被输出成对象映射，而 schema 要求数组
- `assertions` 使用了错误字段：`status_code`、`expected_value`
- 步骤级 assertions 结构不符合 schema

已通过强化 `LLM:ScenarioGen` prompt 修复，明确写入最小合法骨架和字段形状。

### 6.3 当前通过的最小场景

测试需求：

```text
管理员登录 → 正常新增用户 → 查询该用户详情 → 删除该用户
```

输出文件：

```text
/tmp/testhub-agent-explicit-min2-output.json
```

校验结果：

```text
JSON 可解析：通过
JSON Schema 校验：0 个错误
request_count: 4
unique request names: 4
step_count: 4
missing_refs: []
```

结论：

```text
v2 显式工作流 Agent 已能生成符合 TestHub 契约的最小 API 测试场景 JSON。
```

注意：`/tmp/testhub-agent-explicit-min2-output.json` 是临时文件，如需长期保留，应复制到项目目录或重新调用 Agent 生成。

---

## 7. 当前推荐状态

当前推荐使用：

```text
Agent: TestHub 测试场景生成 Agent - RuoYi 用户管理 v2显式工作流
agent_id: 728d08a8417511f1bb078f6f74f53e6e
```

推荐知识库组合：

```text
SRS v2:    e2a33ef6416f11f1bb078f6f74f53e6e
API Docs: 02b7eebc3f1311f1bb078f6f74f53e6e
```

推荐检索参数：

```text
similarity_threshold = 0.30
keywords_similarity_weight = 0.60
vector_similarity_weight 约等价为 0.40
page/top_n = 8
```

---

## 8. 下一步工作

### 8.1 导入 TestHub 验证

下一步应使用通过 schema 校验的 JSON 调用 TestHub 导入接口：

```text
POST /api/api-testing/import/scenario/
```

验证是否成功创建：

- ApiProject
- Environment
- ApiCollection
- ApiRequest
- TestSuite
- TestSuiteRequest

### 8.2 执行测试套件

导入成功后执行最小主流程：

```text
管理员登录 → 新增用户 → 查询详情 → 删除用户
```

重点检查：

- `token` 是否从登录响应正确提取
- 后续请求是否正确使用 `Authorization: Bearer {{token}}`
- 新增用户响应是否提取 `newUserId`
- 查询详情和删除步骤是否正确使用 `{{newUserId}}`
- request 级 assertions 与 step 级 assertions 是否都正常执行

### 8.3 扩展负向场景

最小主流程通过后，再让 Agent 生成扩展场景：

- 用户账号重复
- 手机号重复
- 邮箱重复
- 必填字段缺失
- 密码格式错误
- 部门/岗位不可用
- 初始密码为空导致导入失败

建议一次只扩展 1～2 类负向场景，避免输出过长导致 JSON 截断。

### 8.4 持久化验证输出

如需保存 Agent 输出样例，建议新建目录，例如：

```text
contracts/generated/
```

并将通过 schema 校验的 JSON 保存为：

```text
contracts/generated/ruoyi-user-create-minimal-agent-output.json
```

当前尚未执行这一步。

---

## 9. 相关文件清单


| 文件                                                 | 说明                     |
| -------------------------------------------------- | ---------------------- |
| `session-handoff-ragflow-workflow.md`              | RAGFlow 工作流前期调研摘要      |
| `session-handoff-ragflow-pdf-chunking.md`          | PDF 分块优化摘要             |
| `docs/ruoyi-user-management-srs-v2.pdf`            | 当前推荐的 SRS 风格 PDF       |
| `docs/ruoyi-user-management-srs.pdf`               | SRS v1 PDF             |
| `docs/ruoyi-user-management-prd.pdf`               | 原始 PRD PDF             |
| `docs/ruoyi-user-management-prd.txt`               | 原始 PRD 文本              |
| `docs/ragflow-kb-creation-guide.md`                | RAGFlow 知识库创建指南        |
| `contracts/ragflow-testhub-scenario-schema.json`   | TestHub 导入 JSON Schema |
| `contracts/examples/ruoyi-user-mgmt-scenario.json` | 契约示例                   |
| `apps/api_testing/services/scenario_import.py`     | TestHub 场景导入服务         |
| `apps/api_testing/tests/test_scenario_import.py`   | 导入服务测试                 |


---

## 10. 注意事项

1. 不要继续使用 `Agent-with-tools` 方案作为最终生成器，它倾向于输出解释性摘要。
2. 后续应使用显式 `LLM → Retrieval → LLM` 工作流。
3. 如果 JSON 再次截断，优先缩小场景范围，而不是一次生成整个用户管理模块。
4. 如果 schema 校验失败，优先检查：`project`、`environment`、`headers`、`assertions`、`suites.steps` 的字段形状。
5. 本交接摘要未写入 RAGFlow API Key；如需调用 API，可读取本地已有配置文件，但不要在日志或摘要中明文输出密钥。

