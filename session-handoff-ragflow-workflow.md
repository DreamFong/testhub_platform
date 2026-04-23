# 会话交接摘要 - RAGFlow 工作流搭建前期调研

**日期**: 2026-04-23
**分支**: main
**状态**: 知识库已创建，待搭建 Agent 工作流

---

## 一、会话背景

上一轮会话完成了 TestHub 侧的场景导入功能（`POST /api/api-testing/import/scenario/`，17 个测试全部通过），并定义了 RAGFlow → TestHub 的 JSON Schema 契约（`contracts/ragflow-testhub-scenario-schema.json`）。本轮会话聚焦于 **RAGFlow 侧工作流搭建的可行性调研**。

---

## 二、关键调研结论

### 1. RAGFlow DSL 能否程序化构造？

**结论：完全可以。**

- API：`POST /api/v1/agents` 接受完整 `dsl` 对象参数
- DSL 双结构：`components`（逻辑层，定义参数和上下游）+ `graph`（可视化层，ReactFlow 节点/边）
- 官方 API 文档有多个真实 DSL 示例（空 Agent、Begin+Message、带 Generate 的 Agent）

### 2. RAGFlow Canvas 组件类型（38+）

**工作流组件（agent/component/，20 个）：**

| 组件 | 用途 |
|------|------|
| Begin | 流程入口，定义输入变量和开场白 |
| Generate (LLM) | LLM 调用，支持 prompt 模板和变量引用 |
| Message | 消息输出 |
| Categorize | 分类路由 |
| Switch | 条件分支 |
| Iteration | 迭代循环 |
| Loop / LoopItem / ExitLoop | 循环控制 |
| VariableAggregator | 变量聚合 |
| VariableAssigner | 变量赋值 |
| StringTransform | 字符串变换 |
| Invoke | HTTP 接口调用 |
| AgentWithTools | 带工具的智能体 |
| 其他 | Fillup, DataOperations, ListOperations, ExcelProcessor, DocsGenerator 等 |

**工具组件（agent/tools/，18+ 个）：**

| 组件 | 用途 |
|------|------|
| **Retrieval** | 知识库检索（核心 RAG 组件） |
| CodeExec | 代码执行 |
| Crawler | 网页爬取 |
| Google / Bing / DuckDuckGo / Tavily | 搜索引擎 |
| DeepL | 翻译 |
| ExeSQL | SQL 查询 |
| 其他 | Wikipedia, Arxiv, PubMed, GitHub, Email, AkShare, Tushare, YahooFinance 等 |

### 3. Query 改写是否可行？

**结论：完全可行。通过 Generate → Retrieval 链路实现。**

- RAGFlow 没有专用 Query Rewrite 组件，但 **Generate 组件可做 query 改写**
- 组件间通过 `{组件ID@输出变量}` 语法传递数据（变量引用系统）
- **Retrieval 的 query 参数支持变量引用**，不固定为用户原始 query
  - 源码验证：`agent/tools/retrieval.py` 中 `_retrieve_kb()` 方法会解析变量
  - 可设为 `{generate_rewrite@content}` 接收上游 Generate 的输出

**用户设想的 4 种改写策略（通过一个 prompt 交给大模型控制）：**

| 策略 | 实现方式 |
|------|---------|
| 子任务拆分检索 | Generate 拆分 → Iteration 逐个 Retrieval |
| HyDE（假设答案检索） | Generate 生成假设答案 → Retrieval |
| 回溯问题检索 | Generate 抽象化问题 → Retrieval |
| 直接检索 | `{sys.query}` 直接喂给 Retrieval |

**推荐方案：** 用一个 Generate 组件的 prompt 包含 4 种策略指令，让大模型自行判断和执行改写，不需要 4 条分支。

### 4. 目标工作流拓扑

```
Begin → Generate(query改写) → Retrieval → Generate(生成测试场景JSON) → Message
```

---

## 三、RuoYi-Vue-Pro 环境信息

### 远程服务器

| 项目 | 值 |
|------|------|
| SSH 别名 | `agent-for-ai-server` |
| IP | `81.70.235.9` |
| 用户 | `for_agent` |
| 认证 | `~/.ssh/for_agent_ed25519` |

### 运行中的服务

| 服务 | 端口 | 状态 |
|------|------|------|
| RuoYi-Vue-Pro 后端 | 48080 | healthy |
| RuoYi 前端 | 3000 | running |
| RAGFlow | 8080/9380-9382 | running |
| MySQL | 5455 | healthy |
| Redis (Valkey) | 6379 | healthy |
| MinIO | 9000-9001 | healthy |
| Elasticsearch | 1200 | healthy |
| Kibana | 5601 | running |
| LiteLLM Proxy | 8500 | running |
| vLLM (qwen3.6-35b) | - | running |
| vLLM (gemma4-31b) | - | running |
| vLLM (bge-m3 / bge-reranker) | - | running |

### RuoYi API 文档地址（已验证可访问）

| 文档类型 | 地址 |
|---------|------|
| Knife4j UI | `http://81.70.235.9:48080/doc.html` |
| Swagger UI | `http://81.70.235.9:48080/swagger-ui` |
| OpenAPI JSON | `http://81.70.235.9:48080/v3/api-docs` |

### 已导出文件

- **OpenAPI JSON**: `contracts/ruoyi-vue-pro-openapi.json`（355KB，407 个接口，50+ 模块标签）
  - API 前缀：`/admin-api/`
  - 认证方式：JWT（Authorization header）
  - 涵盖：用户、角色、部门、权限、字典、文件存储、OAuth2、定时任务等

---

## 四、RAGFlow 环境与知识库

### RAGFlow API 信息

| 项目 | 值 |
|------|------|
| 账号 | `junming.feng@genlot.com` |
| API 地址 | `http://81.70.235.9:9380/api/v1/` |
| API Key | `ragflow-08NOsrv8Ov-wF7AMgjap3awcowbE0-xcg95tgBEZ6K8` |
| RAGFlow 版本 | v0.24.0 |
| Embedding 模型 | `bge-m3___OpenAI-API@OpenAI-API-Compatible` |
| LLM 模型 | `qwen-distilled-v1___OpenAI-API@OpenAI-API-Compatible` |

### 知识库（ruoyi-api-docs）

| 项目 | 值 |
|------|------|
| 知识库 ID | `02b7eebc3f1311f1bb078f6f74f53e6e` |
| 文档 ID | `02bba8e03f1311f1bb078f6f74f53e6e` |
| 分块方法 | `book` |
| Chunks | **384**（383 接口 1:1 分块） |
| Tokens | 66,885 |
| 状态 | 已完成，检索验证通过 |

### 分块踩坑记录

RAGFlow `book` 分块按 Markdown 标题层级切分，**必须满足以下条件才能实现 1:1 分块**：

1. **无子标题**：每个接口只用一个 `##` 标题，不要用 `###` 等子标题
2. **无空行**：标题与内容之间不能有空行
3. **无分隔符**：接口之间不要用 `---` 等分隔符
4. **文件后缀用 `.txt`**：`book` 分块不支持 `.md` 后缀，只支持 doc/docx/pdf/txt
5. **内联格式**：请求参数、请求体、响应都用内联文本格式（分号分隔），不要用表格或代码块

正确格式示例：
```
## POST /admin-api/system/user/create - 新增用户
模块:管理后台 - 用户 | operationId:createUser | 请求体(application/json,必填): username(string, 必填); password(string, 必填) | 响应: 200 OK: code(integer); data(integer)
```

---

## 五、待办事项

搭建 RAGFlow Agent 工作流：

1. **LLM ID** — 需要确认 RAGFlow 中已配置的模型标识（已有 `qwen-distilled-v1` 和 `gemma-4-31b-it`）
2. **知识库 ID** — 已就绪：`02b7eebc3f1311f1bb078f6f74f53e6e`
3. **搭建工作流 DSL** — 按目标拓扑构造并创建 Agent

目标拓扑：`Begin → Generate(改写) → Retrieval → Generate(生成场景) → Message`

---

## 六、相关文件清单

| 文件 | 说明 |
|------|------|
| `contracts/ragflow-testhub-scenario-schema.json` | RAGFlow → TestHub 的 JSON Schema 契约 v1.0.0 |
| `contracts/examples/ruoyi-user-mgmt-scenario.json` | 契约示例（用户管理 CRUD 5 步场景） |
| `contracts/ruoyi-vue-pro-openapi.json` | RuoYi-Vue-Pro 完整 OpenAPI 文档（407 接口） |
| `apps/api_testing/services/scenario_import.py` | TestHub 场景导入服务（已完成） |
| `apps/api_testing/tests/test_scenario_import.py` | 导入服务测试（17 个，全部通过） |
| `apps/api_testing/views.py` | 导入接口视图（已完成） |
| `scripts/openapi2md.py` | OpenAPI JSON → Markdown 转换脚本 |

---

## 七、RAGFlow DSL 最小模板参考

```json
{
  "components": {
    "begin": {
      "downstream": ["Generate:QueryRewrite"],
      "obj": {
        "component_name": "Begin",
        "params": {
          "mode": "conversational",
          "prologue": "你好，我是测试场景生成助手。请描述你需要测试的功能模块。",
          "enablePrologue": true,
          "inputs": {},
          "outputs": {}
        }
      },
      "upstream": []
    },
    "Generate:QueryRewrite": {
      "downstream": ["Retrieval:ApiDocs"],
      "obj": {
        "component_name": "Generate",
        "params": {
          "llm_id": "<待填>",
          "prompt": "你是查询改写专家...4种策略...",
          "temperature": 0.1
        }
      },
      "upstream": ["begin"]
    },
    "Retrieval:ApiDocs": {
      "downstream": ["Generate:ScenarioGen"],
      "obj": {
        "component_name": "Retrieval",
        "params": {
          "query": "{Generate:QueryRewrite@content}",
          "kb_ids": ["<待填>"]
        }
      },
      "upstream": ["Generate:QueryRewrite"]
    },
    "Generate:ScenarioGen": {
      "downstream": ["Message:Output"],
      "obj": {
        "component_name": "Generate",
        "params": {
          "llm_id": "<待填>",
          "prompt": "根据检索到的API文档，生成符合契约的测试场景JSON..."
        }
      },
      "upstream": ["Retrieval:ApiDocs"]
    },
    "Message:Output": {
      "downstream": [],
      "obj": {
        "component_name": "Message",
        "params": {
          "content": ["{Generate:ScenarioGen@content}"]
        }
      },
      "upstream": ["Generate:ScenarioGen"]
    }
  },
  "graph": { "edges": [], "nodes": [] },
  "history": [], "messages": [], "path": [], "reference": []
}
```

注：`graph` 部分需要同步维护节点坐标和边，建议用 UI 搭好模板后导出，再程序化微调。
