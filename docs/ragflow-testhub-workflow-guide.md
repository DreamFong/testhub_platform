# RAGFlow 到 TestHub 自动化场景生成链路使用文档

## 1. 文档目的

本文档说明如何基于需求文档和接口文档，在 RAGFlow 中生成接口测试场景，并导入 TestHub 执行。

当前链路定位：

- RAGFlow 负责知识检索和候选场景生成。
- TestHub 负责契约归一化、JSON Schema 校验、场景导入和测试执行。

## 2. 当前可用链路总览

输入：

- SRS/PRD 文档
- API 文档
- 目标系统环境信息
- TestHub 场景契约

输出：

- TestHub 场景 JSON
- TestHub API 项目、环境、集合、测试套件
- 测试执行结果

整体流程：

```text
SRS/PRD + API Docs
→ RAGFlow Knowledge Base
→ RAGFlow Agent Workflow
→ Candidate Scenario JSON
→ TestHub Normalizer
→ Schema Validation
→ Scenario Import
→ Suite Execution
```

## 3. 前置条件

### 3.1 RAGFlow

- RAGFlow 服务可访问。
- 已创建 RAGFlow API Key。
- 已配置可用模型。
- 已配置知识库，或准备好待导入的需求文档和接口文档。

### 3.2 TestHub

- TestHub 后端服务可运行。
- 本地存在用于导入和执行场景的用户。
- 已存在场景导入契约：
  - [ragflow-testhub-scenario-schema.json](../contracts/ragflow-testhub-scenario-schema.json)

### 3.3 目标系统

- 目标系统 API 可访问。
- 已准备测试账号。
- 明确租户、Header 等运行时要求。
- 明确一个最小业务闭环流程。

## 4. 需要提供的信息清单

### 4.1 RAGFlow 信息

- RAGFlow API Base URL
- RAGFlow API Key
- RAGFlow Agent ID
- SRS/PRD 知识库 ID
- API 文档知识库 ID

### 4.2 TestHub 信息

- TestHub 本地用户名
- 是否导入后自动执行
- 是否需要保存归一化 JSON
- 是否需要保存执行报告

### 4.3 目标系统信息

- `baseUrl`
- 登录账号
- 登录密码
- `tenant-id` 或其他租户 Header
- 其他必要 Header
- 最小业务流程说明

### 4.4 文档信息

- SRS/PRD 文件路径
- API 文档地址或文件路径
- 业务测试范围

## 5. RAGFlow 知识库准备

### 5.1 创建 SRS/PRD 知识库

1. 上传需求文档。
2. 等待解析完成。
3. 确认 chunk 数量合理。
4. 抽查关键业务规则是否能被检索到。

### 5.2 创建 API 文档知识库

推荐从 OpenAPI/Swagger 转换为面向 Endpoint 的文本。

每个接口尽量形成一个独立 chunk，内容应包含：

- HTTP Method
- API Path
- Summary
- Request Params
- Request Body
- Response Structure
- Auth/Header Requirements

推荐格式示例：

```text
## POST /admin-api/system/auth/login - 使用账号密码登录
模块:管理后台 - 认证 | 请求体: username, password | Header: tenant-id | 响应: code, msg, data.accessToken
```

### 5.3 检索验证

创建知识库后，应使用关键业务流程进行检索验证。

验证重点：

- 能命中核心接口。
- 能看到请求字段。
- 能看到响应结构。
- 能看到鉴权和 Header 要求。
- 能看到变量提取所需字段。

例如用户管理流程应至少命中：

- 登录接口
- 创建用户接口
- 查询用户详情接口
- 删除用户接口

## 6. RAGFlow Agent 工作流配置

### 6.1 推荐工作流拓扑

```text
Begin
→ Agent:QueryRewrite
→ Retrieval:Knowledge
→ Agent:ScenarioGen
→ Message:Output
```

### 6.2 QueryRewrite 节点

作用：把用户需求改写为适合检索的查询文本。

输出要求：

- 只输出纯文本查询。
- 不输出 Markdown。
- 尽量覆盖接口路径、字段、鉴权、变量传递等关键词。

建议覆盖内容：

- 业务模块
- 正向业务流程
- 接口 Method/Path
- 登录鉴权
- 租户 Header
- 变量传递
- 创建后查询和删除清理

### 6.3 Knowledge 节点

作用：从 SRS/PRD 知识库和 API 文档知识库中检索上下文。

配置要点：

- 绑定 SRS/PRD 知识库。
- 绑定 API 文档知识库。
- 使用 QueryRewrite 的输出作为 Query。
- 将检索结果的 `formalized_content` 提供给 ScenarioGen。

### 6.4 ScenarioGen 节点

作用：基于用户需求和检索内容生成候选 TestHub 场景 JSON。

要求：

- 只输出 JSON。
- 不输出解释、摘要或 Markdown。
- 不编造接口路径。
- 不编造字段名。
- 不编造响应结构。
- 优先生成最小可执行业务闭环。

注意：RAGFlow 输出是候选结果，最终进入 TestHub 前必须经过 TestHub 侧归一化和 Schema 校验。

### 6.5 Message 节点

作用：输出 ScenarioGen 的 `content`。

## 7. TestHub 场景契约要求

TestHub 场景导入契约以 [ragflow-testhub-scenario-schema.json](../contracts/ragflow-testhub-scenario-schema.json) 为准。

### 7.1 顶层结构

顶层对象包含：

- `schema_version`
- `project`
- `environment`
- `collections`
- `suites`
- `metadata`

其中 `metadata` 为可选字段。

### 7.2 environment

`environment` 用于定义运行时静态变量。

必要字段：

- `name`
- `variables`

常用字段：

- `scope`

示例：

```json
{
  "name": "ruoyi-dev",
  "scope": "GLOBAL",
  "variables": {
    "baseUrl": "http://target.example.com",
    "tenantId": "1",
    "adminUsername": "admin",
    "adminPassword": "******"
  }
}
```

### 7.3 collections[].requests

请求必须放在 `collections[].requests` 中。

常用字段：

- `name`
- `method`
- `url`
- `headers`
- `params`
- `body`
- `assertions`
- `variable_extractions`

### 7.4 suites[].steps

测试套件通过 `steps` 定义执行顺序。

常用字段：

- `request_name`
- `enabled`
- `assertions`

`request_name` 必须引用已存在的请求名称。

### 7.5 变量传递规则

典型变量链：

1. 登录接口提取 `token`。
2. 创建资源接口提取资源 ID。
3. 后续查询、更新、删除步骤引用提取出的资源 ID。

示例：

```json
{
  "variable_extractions": [
    {
      "variable": "token",
      "source": "body",
      "json_path": "$.data.accessToken"
    }
  ]
}
```

## 8. TestHub 侧归一化与校验

### 8.1 归一化目标

RAGFlow 生成的 JSON 可能是候选结果。TestHub 侧归一化的目标是将候选结果收敛到 TestHub 场景契约，保证进入导入流程的 JSON 严格符合 Schema。

### 8.2 当前支持的归一化

当前支持以下归一化处理：

- 顶层 `requests` 移入 `collections[0].requests`
- `variable_name` 转为 `variable`
- `params` 数组转为对象
- `environment.scope` 转为 `GLOBAL` / `LOCAL`
- `environment.variables` 补全
- `metadata` 非契约字段剔除
- `suite.steps[].enabled` 补齐

### 8.3 校验策略

- 归一化后执行 JSON Schema 校验。
- `schema_errors > 0` 时不导入、不执行。
- 导入前必须保证 `suite.steps[].request_name` 引用的请求存在。

## 9. Management Command 使用方式

命令入口：

```bash
python manage.py run_ragflow_testhub_scenario
```

### 9.1 使用本地候选 JSON

```bash
python manage.py run_ragflow_testhub_scenario \
  --candidate-json /path/to/candidate.json \
  --username admin \
  --env-var baseUrl=http://target.example.com \
  --env-var tenantId=1 \
  --env-var adminUsername=admin \
  --env-var adminPassword='******'
```

### 9.2 在线调用 RAGFlow Agent

```bash
export RAGFLOW_KEY='******'

python manage.py run_ragflow_testhub_scenario \
  --agent-id <RAGFLOW_AGENT_ID> \
  --ragflow-api http://ragflow.example.com/api/v1 \
  --username admin \
  --question '生成用户管理最小主流程接口自动化场景' \
  --env-var baseUrl=http://target.example.com \
  --env-var tenantId=1 \
  --env-var adminUsername=admin \
  --env-var adminPassword='******'
```

### 9.3 保存归一化结果和报告

```bash
python manage.py run_ragflow_testhub_scenario \
  --candidate-json /path/to/candidate.json \
  --username admin \
  --env-var baseUrl=http://target.example.com \
  --normalized-output /tmp/normalized-scenario.json \
  --report-output /tmp/ragflow-testhub-report.json
```

### 9.4 只导入不执行

```bash
python manage.py run_ragflow_testhub_scenario \
  --candidate-json /path/to/candidate.json \
  --username admin \
  --no-execute
```

## 10. 执行结果说明

### 10.1 成功结果

命令成功时会输出摘要信息：

- `project_id`
- `environment_id`
- `collection_ids`
- `suite_ids`
- `execution_id`
- `passed_count`
- `failed_count`
- `total_count`

### 10.2 失败结果

失败时应优先查看：

- Schema 错误
- 导入错误
- 执行错误

如果使用了 `--report-output`，可以查看报告中的 `schema_errors`、`changes` 和执行摘要。

## 11. 用户管理样例流程

### 11.1 输入信息

用户管理样例通常需要：

- 目标系统 `baseUrl`
- `tenant-id`
- 管理员账号
- 管理员密码

### 11.2 推荐业务闭环

1. 管理员登录。
2. 创建用户。
3. 查询用户详情。
4. 删除用户。

### 11.3 变量链

- 登录响应提取 `token`。
- 创建用户响应提取 `newUserId`。
- 查询用户详情使用 `newUserId`。
- 删除用户使用 `newUserId`。

### 11.4 验收标准

- 4 个请求全部执行。
- 4 个请求全部通过。
- 临时测试数据被删除。

## 12. 常见问题

### 12.1 RAGFlow 输出不是标准契约 JSON

处理方式：

- 使用 TestHub 归一化层处理。
- 查看报告中的 `changes`。
- 如果归一化后仍不符合 Schema，查看 `schema_errors`。

### 12.2 Schema 校验失败

排查方向：

- 是否缺少 `collections`。
- 是否缺少 `suites`。
- 是否缺少 `environment`。
- `suite.steps[].request_name` 是否引用不存在的请求。
- `variable_extractions` 是否使用了正确字段名。
- `params` 是否为对象。

### 12.3 执行失败

排查方向：

- 目标系统账号密码是否正确。
- 租户 Header 是否正确。
- 变量提取路径是否正确。
- 请求体字段是否符合接口文档。
- 目标系统是否有必填字段或数据约束。

### 12.4 创建资源失败

排查方向：

- 唯一字段是否使用动态变量。
- 接口必填字段是否完整。
- 是否传入目标系统不存在的 ID。
- 是否缺少业务必需字段。

## 13. 安全注意事项

- 不要在文档中写真实 API Key。
- 不要提交包含真实密码的候选 JSON 或归一化 JSON。
- RAGFlow Key 使用环境变量传入。
- 报告文件只用于本地排查，提交前检查敏感信息。
- 命令行历史中避免保留明文密码。
- 临时文件应保存在本地安全目录，不应提交到代码仓库。

## 14. 后续扩展方向

- 支持更多业务模块。
- 将命令能力接入 TestHub 页面。
- 支持批量业务流程生成。
- 归一化报告可视化。
- 增加更多契约校验规则。
- 支持更细粒度的执行结果分析。
