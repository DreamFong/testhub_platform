# RAGFlow → TestHub 最小闭环交接摘要

## 1. 目标与结论

本次工作的目标是验证一条完整可执行的最小链路：

```text
RAGFlow 知识库
→ RAGFlow Agent 工作流生成 candidate scenario JSON
→ 本地 runner 归一化
→ schema 校验
→ 导入 TestHub
→ 执行最小闭环
→ 验证目标系统 API 结果
```

最终结论：**已验证通过**。

本次成功跑通的最小闭环为：

```text
登录
→ 创建用户
→ 分页查询用户
→ 查询用户详情
→ 修改用户
→ 删除用户
```

最终成功执行结果：

- `execution_id = 44`
- `passed_count = 6`
- `failed_count = 0`
- `total_count = 6`

## 2. 本次实际使用的知识库

### 2.1 SRS / 需求知识库

- **名称**：`e2e-srs-user-mgmt`
- **ID**：`52f0e8e6493811f18243434b552cc465`
- **作用**：提供用户管理相关的业务背景与闭环语义

### 2.2 API 文档知识库

- **名称**：`ruoyi-user-api-docs-preserve-schema-20260508`
- **ID**：`fbda1c7a4a9611f18243434b552cc465`
- **作用**：提供接口路径、字段名、响应结构、变量提取路径、字段约束等事实依据

### 2.3 为什么最终使用 `ruoyi-user-api-docs-preserve-schema-20260508`

这份 API 知识库基于保留 schema 约束信息的新转换结果重建，使用的输入文件是：

- [ruoyi-vue-pro-endpoint-centric-preserve-schema.txt](contracts/examples/ruoyi-vue-pro-endpoint-centric-preserve-schema.txt)

相较于旧 API 知识库，它能保住更多关键约束字段，例如：

- `pattern`
- `minLength`
- `maxLength`
- `minimum`
- `maximum`
- `uniqueItems`
- `example`
- `default`

这次最小闭环所需的关键事实在新 KB 中可稳定检索到，例如：

- 登录 token 提取路径：`$.data.accessToken`
- 创建用户返回 ID 提取路径：`$.data`
- 用户名字段约束：`^[a-zA-Z0-9]{4,30}$`
- 分页参数：`pageNo minimum=1`、`pageSize maximum=200`

## 3. 本次实际使用的工作流

### 3.1 RAGFlow Agent 工作流

- **名称**：`ruoyi 用户管理最小闭环候选生成器 20260508`
- **ID**：`321aeee24ab811f18243434b552cc465`
- **结构**：

```text
Begin
→ Agent:QueryRewrite
→ Retrieval:Knowledge
→ Agent:ScenarioGen
→ Message:Output
```

### 3.2 工作流中实际使用的模型

- `QueryRewrite`：`qwen3.5-flash@Tongyi-Qianwen`
- `ScenarioGen`：`qwen-plus@Tongyi-Qianwen`

### 3.3 实际使用的检索参数

最终在工作流中使用的是：

```text
similarity_threshold = 0.30
keywords_similarity_weight = 0.60
top_n = 8
top_k = 1024
use_kg = false
```

## 4. 目标系统与 TestHub 运行参数

### 4.1 TestHub 本地导入 / 执行环境

- `TESTHUB_BASE_URL = http://localhost:3000`
- `TESTHUB_AUTH_PATH = /api/auth/login/`
- `TESTHUB_USERNAME = admin`

### 4.2 目标系统运行参数

- `TARGET_BASE_URL = http://43.162.112.20:48080`
- `TARGET_AUTH_USERNAME = admin`
- `TARGET_TENANT_ID = 1`
- `TARGET_EXTRA_HEADERS = tenant-id: 1`

## 5. 场景契约与参考文件

- 场景 Schema：
  - [ragflow-testhub-scenario-schema.json](contracts/ragflow-testhub-scenario-schema.json)
- 参考样例：
  - [ruoyi-user-mgmt-scenario.json](contracts/examples/ruoyi-user-mgmt-scenario.json)

## 6. 本次采用的 runner

本次未直接把 RAGFlow 输出导入，而是走了完整安全链路：

```text
RAGFlow candidate JSON
→ 提取 JSON
→ 结构归一化
→ schema 校验
→ 导入 TestHub
→ 执行 TestSuite
→ 汇总结果
```

本地 runner 入口：

- 管理命令：
  - [run_ragflow_testhub_scenario.py](apps/api_testing/management/commands/run_ragflow_testhub_scenario.py)
- 核心服务：
  - [ragflow_scenario_runner.py](apps/api_testing/services/ragflow_scenario_runner.py)

## 7. 中间验证过程与关键转折

### 7.1 第一阶段：API 知识库重建与检索验证

- 重新生成了 endpoint-centric TXT：
  - [ruoyi-vue-pro-endpoint-centric-preserve-schema.txt](contracts/examples/ruoyi-vue-pro-endpoint-centric-preserve-schema.txt)
- 本地产物校验通过：
  - `407 endpoints -> 814 lines`
  - `strict_two_line = true`
- 新 API KB 解析首次因 Docker DNS 到 `223.5.5.5` 短时超时而失败
- 重试后解析成功，最终：
  - `chunk_count = 407`
  - `retrieval_gate = pass`

### 7.2 第二阶段：工作流 candidate 生成调优

初始版本 candidate 存在以下问题：

1. 生成了不符合执行器或目标系统要求的动态值写法
2. 生成了额外字段，导致运行时失败
3. 更新接口没有稳定包含必填字段 `password`
4. 变量链在 `create_user` 失败后断裂，导致后续 `get/update/delete` 级联失败

经过多轮收紧规则后，最终稳定约束为：

- 只使用这 6 个接口：
  - `POST /admin-api/system/auth/login`
  - `POST /admin-api/system/user/create`
  - `GET /admin-api/system/user/page`
  - `GET /admin-api/system/user/get`
  - `PUT /admin-api/system/user/update`
  - `DELETE /admin-api/system/user/delete`
- 所有 `$.code` 断言统一为：
  - `{"type":"json_path","json_path":"$.code","expected":0}`
- 登录 token 提取路径固定：
  - `$.data.accessToken`
- 创建用户 ID 提取路径固定：
  - `$.data`
- 强制所有相关请求都包含：
  - `tenant-id: {{tenantId}}`
- 需要鉴权的请求都包含：
  - `Authorization: Bearer {{token}}`
- `create_user` 只保留最小字段集合：
  - `username`
  - `nickname`
  - `password`
- `update_user` 只保留最小字段集合：
  - `id`
  - `username`
  - `nickname`
  - `password`

### 7.3 第三阶段：动态值写法修正

关键发现：

- `${timestamp()}` 在当前执行器中**理论支持**，但本地实现有调用缺陷，执行时会报参数错误
- [variable_resolver.py](apps/core/variable_resolver.py) 中 `timestamp` / `timestamp_sec` 这类内置函数的注册与调用方式不一致

因此最终为了保证这次闭环通过，采用了**绕开该问题**的方式：

- `create_user.username = testuser${random_digits(6)}`
- `update_user.username = updated${random_digits(6)}`

这样既满足：

- 文档约束 `^[a-zA-Z0-9]{4,30}$`
- 又避免了 `${timestamp()}` 的执行器缺陷

## 8. 最终成功版本的关键结构

### 8.1 成功的请求链

最终成功执行的 6 个请求名为：

- `login_admin`
- `create_user`
- `get_user_page`
- `get_user_by_id`
- `update_user`
- `delete_user`

### 8.2 最终 suite 名称

- `User Management Full Lifecycle`

### 8.3 最终成功的导入结果

第三轮导入结果：

- `project_id = 40`
- `environment_id = 40`
- `collection_ids = [40]`
- `suite_ids = [40]`

### 8.4 最终成功的执行结果

- `execution_id = 44`
- `passed_count = 6`
- `failed_count = 0`
- `total_count = 6`

## 9. 本次生成 / 归一化 / 执行工件

### 9.1 最终成功版工件

- candidate：`/tmp/ruoyi-ragflow-candidate-v3.parsed.json`
- 归一化结果：`/tmp/ruoyi-ragflow-v3-normalized.json`
- 报告：`/tmp/ruoyi-ragflow-v3-report.json`

### 9.2 报告中确认的信息

最终报告显示：

- `schema_errors = []`
- `import_result.success = true`
- `execution_result.success = true`

## 10. 当前已知限制 / 注意事项

### 10.1 已知执行器问题

文件：

- [variable_resolver.py](apps/core/variable_resolver.py)

问题概述：

- `timestamp` / `timestamp_sec` 注册为无参方法
- 调用分发时按 `(func_name, args)` 统一传参
- 导致 `${timestamp()}` 在当前执行器里会报参数数量错误

这次通过 `random_digits` 绕过，因此**不影响当前闭环验证结论**，但建议后续单独修复。

### 10.2 当前成功经验不等于所有场景都可直接泛化

这次跑通依赖了较强的“最小字段集合”约束和精确接口集合。若后续扩展到更复杂的用户管理场景，仍需重新验证：

- 目标环境中的业务前置条件
- 更多可选字段的真实可执行性
- 动态函数在执行器中的稳定性
- 更复杂变量链是否稳定闭合

## 11. 后续建议

### 11.1 短期建议

优先做这两件事：

1. 修复 [variable_resolver.py](apps/core/variable_resolver.py) 中 `${timestamp()}` 的调用问题
2. 把本次成功的规则沉淀为可复用模板，尤其是：
   - 精确 method/path 驱动的提问方式
   - 最小字段集合策略
   - `tenant-id` / `Authorization` 的显式约束
   - `$.data.accessToken` / `$.data` 的变量提取规则

### 11.2 复用建议

后续若要继续复用本次成功链路，优先从以下资产开始：

- **知识库**：
  - `e2e-srs-user-mgmt`
  - `ruoyi-user-api-docs-preserve-schema-20260508`
- **工作流**：
  - `ruoyi 用户管理最小闭环候选生成器 20260508`
- **Runner**：
  - [run_ragflow_testhub_scenario.py](apps/api_testing/management/commands/run_ragflow_testhub_scenario.py)

## 12. 一句话交接结论

本次 `ruoyi` 用户管理最小闭环已经完成以下验证：

```text
新 API 知识库重建成功
→ RAGFlow Agent 工作流生成成功
→ candidate 归一化与 schema 校验成功
→ TestHub 导入成功
→ 目标系统 6 步最小闭环执行通过
```

可视为当前这条 **RAGFlow → TestHub 最小闭环链路已打通**。
