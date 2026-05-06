# RAGFlow 到 TestHub 链路阶段性交接摘要

## 1. 背景和目标

本阶段围绕 RAGFlow 与 TestHub 的 API 测试链路集成展开，目标是将需求文档和接口文档转化为可在 TestHub 中导入并执行的接口自动化测试场景。

当前已经形成的稳定链路是：

```text
业务需求文档 + API 文档
→ RAGFlow 两个知识库
→ RAGFlow Agent 工作流
→ 候选测试场景 JSON
→ TestHub 契约归一化
→ JSON Schema 校验
→ TestHub 场景导入
→ TestHub 测试套件执行
→ 目标系统接口结果
```

核心定位：

- RAGFlow 负责知识检索和候选场景生成。
- TestHub 负责契约收敛、强校验、导入和执行。
- RAGFlow Agent 输出不直接视为最终导入 payload，必须先经过 TestHub 侧归一化和 Schema 校验。

## 2. 已完成工作

### 2.1 RAGFlow 知识库建设

已完成两个知识库的建设和验证：

1. 业务需求知识库
   - 用途：存放 SRS/PRD/业务规则。
   - 当前样例：若依用户管理需求文档。

2. API 文档知识库
   - 用途：存放接口 Method、Path、请求字段、响应结构、认证和 Header 要求。
   - 当前样例：若依用户管理相关 OpenAPI/Swagger 接口。

已验证 API 文档知识库能检索到关键接口：

- 登录接口
- 创建用户接口
- 查询用户详情接口
- 删除用户接口

### 2.2 RAGFlow Agent 工作流

已创建并验证 Agent 组件版工作流：

```text
Begin
→ Agent:QueryRewrite
→ Retrieval:Knowledge
→ Agent:ScenarioGen
→ Message:Output
```

当前结论：

- 工作流拓扑可用。
- Knowledge 节点已正确绑定两个知识库。
- 检索链路可命中目标业务流程所需接口。
- 生成结果作为候选 JSON 使用，后续必须交给 TestHub 侧做契约归一化和校验。

### 2.3 TestHub 场景契约

当前使用的契约文件：

```text
contracts/ragflow-testhub-scenario-schema.json
```

契约版本：

```text
schema_version=1.0.0
```

进入 TestHub 导入流程前，最终 JSON 必须通过该 Schema 校验。

### 2.4 TestHub 侧归一化和执行能力

已在 TestHub 项目中落地后端能力：

- `apps/api_testing/services/ragflow_scenario_runner.py`
- `apps/api_testing/management/commands/run_ragflow_testhub_scenario.py`
- `apps/api_testing/tests/test_ragflow_scenario_runner.py`

当前支持能力：

1. 从 RAGFlow completion 输出中提取候选 JSON。
2. 将候选 JSON 归一化为 TestHub 契约结构。
3. 使用 JSON Schema 强校验。
4. 校验通过后调用现有 `import_scenario()` 导入。
5. 可选调用 `execute_test_suite()` 执行导入后的第一个测试套件。
6. 输出导入和执行摘要。

当前支持的归一化规则：

- 顶层 `requests` 移入 `collections[0].requests`
- `variable_name` 转为 `variable`
- `params` 数组转为对象
- `environment.scope` 转为 `GLOBAL` / `LOCAL`
- `environment.variables` 补全
- `metadata` 非契约字段剔除
- `suite.steps[].enabled` 补齐

归一化原则：

- 只处理结构性契约偏差。
- 不编造 API Path。
- 不编造请求字段。
- 不编造响应结构。
- 不猜测业务 ID。

### 2.5 Management Command

新增命令：

```bash
python manage.py run_ragflow_testhub_scenario
```

支持两种输入模式：

1. 本地候选 JSON 模式

```bash
python manage.py run_ragflow_testhub_scenario \
  --candidate-json /path/to/candidate.json \
  --username admin \
  --env-var baseUrl=http://target.example.com \
  --env-var tenantId=1 \
  --env-var adminUsername=admin \
  --env-var adminPassword='******'
```

2. 在线调用 RAGFlow Agent 模式

```bash
export RAGFLOW_KEY='******'

python manage.py run_ragflow_testhub_scenario \
  --agent-id <RAGFLOW_AGENT_ID> \
  --ragflow-api <RAGFLOW_API> \
  --username admin \
  --question '生成用户管理最小主流程接口自动化场景' \
  --env-var baseUrl=http://target.example.com \
  --env-var tenantId=1 \
  --env-var adminUsername=admin \
  --env-var adminPassword='******'
```

可选参数：

```bash
--normalized-output /tmp/normalized-scenario.json
--report-output /tmp/ragflow-testhub-report.json
--no-execute
```

### 2.6 文档建设

已新增或更新以下文档：

- `docs/ragflow-testhub-workflow-guide.md`
  - 面向当前可用链路的使用说明。

- `docs/ragflow-testhub-API测试链路使用文档.md`
  - 面向零上下文用户的接入准备清单。
  - 已补充 Mermaid 流程图。

- `docs/ragflow-testhub-handoff-summary.md`
  - 当前交接摘要，即本文档。

## 3. 验证结果

### 3.1 单元测试

已执行并通过：

```bash
./.venv/bin/python manage.py test apps.api_testing.tests.test_ragflow_scenario_runner
```

结果：

```text
OK，6 tests
```

已执行并通过既有场景导入测试：

```bash
./.venv/bin/python manage.py test apps.api_testing.tests.test_scenario_import
```

结果：

```text
OK，17 tests
```

### 3.2 完整链路验证

已使用 RAGFlow 生成的候选 JSON，通过新增 management command 跑通完整链路。

验证结果摘要：

```text
TestHub 导入成功
TestHub 执行成功
总请求数：4
通过请求数：4
失败请求数：0
```

当前样例业务闭环：

```text
管理员登录
→ 创建用户
→ 查询用户详情
→ 删除用户
```

## 4. 当前可用能力边界

当前链路已经可以支持：

- 基于两个 RAGFlow 知识库生成候选测试场景。
- 将候选 JSON 归一化为 TestHub 场景契约。
- 对最终 JSON 做强 Schema 校验。
- 自动导入 TestHub。
- 自动执行导入后的测试套件。
- 返回导入和执行摘要。

当前不建议：

- 直接把 RAGFlow 原始输出当作最终导入 JSON。
- 在归一化逻辑中猜测业务字段、接口路径或响应结构。
- 一次性生成和导入“所有可能场景”。
- 将真实密钥、密码、Token 写入文档、候选 JSON 或提交文件。

## 5. 关于两个 Skill 的后续优化方向

当前讨论结论：两个 skill 应保持通用能力，不应强依赖本地 TestHub 项目代码。

### 5.1 `ragflow-knowledge-base-builder`

建议优化方向：

1. 增加面向下游工作流的标准交接字段：

```text
PROJECT_NAME=
BUSINESS_DOMAIN=
TEST_SCOPE=
MIN_BUSINESS_FLOW=
SRS_KB_ID=
API_DOCS_KB_ID=
RETRIEVAL_PARAMS=
KNOWN_CAVEATS=
```

2. 增加门禁规则：

```text
如果关键接口、字段、响应结构检索不到，不应继续创建 Agent 工作流。
应先修正文档、重新切分或重新上传知识库。
```

3. 引导用户准备接入清单中的必要信息。

### 5.2 `ragflow-testhub-agent-workflow`

建议优化方向：

1. 明确 RAGFlow Agent 输出是 candidate JSON，不是最终导入 payload。
2. 强调必须经过验证/导入 runner：

```text
candidate JSON
→ parse
→ normalize known structural deviations
→ schema validate
→ import
→ execute
→ report
```

3. 不把本地 management command 写成唯一实现。
4. 将具体实现方式放到 reference 中，例如：

```text
references/validation-flow.md
references/testhub-management-command.md
references/normalization-rules.md
references/api-import-execution.md
```

5. 在主 skill 中保留通用流程，在 reference 中说明不同环境下的执行方式。

## 6. 验证失败时的处理策略

推荐决策树：

```text
生成 candidate JSON
  ↓
是否可解析 JSON？
  否 → 重新生成，最多重试 1-2 次
  是
  ↓
执行归一化
  ↓
Schema 是否通过？
  是 → 导入 TestHub
  否
    ↓
    是否属于已知可归一化结构问题？
      是 → 增加或调整归一化规则后重新校验
      否 → 回到 RAGFlow Prompt / 知识库 / 输入信息补充
```

失败类型建议分为三类：

### 6.1 可确定归一化的问题

例如：

- 顶层 `requests`
- `variable_name` 应为 `variable`
- `params` 数组应为对象
- `scope` 大小写不符合契约
- `metadata` 多余字段

处理方式：

```text
程序归一化 → 重新 Schema 校验
```

### 6.2 信息缺失或模型编造的问题

例如：

- 接口路径不在检索内容中。
- 请求字段无法从 API 文档确认。
- 响应结构无法确认。
- 变量提取路径没有依据。
- Suite 引用了不存在的 Request。

处理方式：

```text
不要强行修。
回到 RAGFlow 重新生成，或回到知识库检查文档质量。
```

### 6.3 Schema 通过但执行失败

例如：

- 登录失败。
- 租户 Header 缺失。
- 创建数据不满足目标系统约束。
- 变量提取为空。
- 删除清理失败。

处理方式：

```text
归类为运行时问题。
检查目标系统环境变量、测试账号、业务数据约束和 API 文档准确性。
```

## 7. 下一步产品化方向

### 7.1 第一阶段：后端服务化当前 Command

目标：将当前 command 能力封装为 TestHub 后端 API。

建议新增接口：

```text
POST /api/api-testing/ragflow/scenarios/generate/
```

请求体示例：

```json
{
  "agent_id": "<RAGFLOW_AGENT_ID>",
  "question": "生成用户管理最小主流程接口自动化场景",
  "environment_variables": {
    "baseUrl": "http://target.example.com",
    "tenantId": "1",
    "adminUsername": "admin",
    "adminPassword": "******"
  },
  "execute": true
}
```

后端流程：

```text
调用 RAGFlow Agent
→ 解析候选 JSON
→ 归一化
→ Schema 校验
→ 导入 TestHub
→ 可选执行
→ 返回结果
```

### 7.2 第二阶段：TestHub 前端入口

建议在 API 测试模块增加入口：

```text
API 测试 → AI 生成场景
```

页面字段建议：

- RAGFlow Agent 选择
- 业务需求 Query
- 目标环境选择
- 是否导入后执行
- 是否保存归一化 JSON / 报告
- 生成按钮

结果展示建议：

- 归一化变更
- Schema 校验结果
- 创建的项目 / 集合 / 套件
- 执行结果
- 失败原因

### 7.3 第三阶段：配置管理和任务记录

建议新增配置和任务记录能力：

- RAGFlow API 地址
- RAGFlow Key
- Agent ID
- SRS_KB_ID
- API_DOCS_KB_ID
- 默认模型
- 默认检索参数
- 每次生成任务
- 候选 JSON
- 归一化 JSON
- Schema errors
- 导入 / 执行结果

可考虑的数据模型：

```text
RagflowConfig
RagflowKnowledgeBase
RagflowAgentWorkflow
RagflowScenarioGenerationTask
```

### 7.4 第四阶段：异步任务化

RAGFlow 生成和 TestHub 执行可能耗时较长，建议后续使用异步任务。

任务状态建议：

```text
PENDING
GENERATING
NORMALIZING
VALIDATING
IMPORTING
EXECUTING
COMPLETED
FAILED
```

推荐流程：

```text
前端提交任务
→ 后端创建 generation task
→ 异步任务调用 RAGFlow
→ 写入候选 JSON / 归一化 JSON / 执行结果
→ 前端轮询任务状态
```

### 7.5 第五阶段：场景清单发现和批量生成

不建议一开始直接生成“所有可能场景”。

推荐方式：

```text
RAGFlow 先生成候选场景清单
→ 用户勾选需要的场景
→ TestHub 逐个生成、校验、导入、执行
```

候选场景清单示例：

```json
[
  {
    "name": "用户管理最小主流程",
    "type": "positive",
    "priority": "high"
  },
  {
    "name": "用户名重复创建失败",
    "type": "negative",
    "priority": "medium"
  },
  {
    "name": "未登录查询用户失败",
    "type": "auth",
    "priority": "high"
  }
]
```

## 8. 建议的下一步执行顺序

推荐按以下顺序继续推进：

1. 优化两个 RAGFlow/TestHub 相关 skill，使其成为跨项目可用的通用流程。
2. 将具体 TestHub management command 使用方式抽到 skill reference 中。
3. 将当前 command 能力服务化为 TestHub 后端 API。
4. 在 TestHub 前端增加“AI 生成场景”入口。
5. 增加 RAGFlow 配置管理和任务记录。
6. 支持异步任务执行。
7. 支持候选场景清单发现和批量生成。

## 9. 安全注意事项

- 不在文档中记录真实 RAGFlow API Key。
- 不在文档中记录目标系统真实密码。
- 不提交包含真实密码的候选 JSON、归一化 JSON 或报告文件。
- 报告和日志中应输出摘要，避免输出 Header、Token、密码等敏感信息。
- RAGFlow Key、目标系统密码等应通过环境变量、密钥管理或受保护配置传入。
- 如果接入前端页面，后端必须控制密钥读取和权限校验，前端不应直接持有 RAGFlow Key。
