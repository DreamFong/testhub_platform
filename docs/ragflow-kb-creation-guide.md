# RAGFlow 接口文档知识库创建指南

本文档描述从 Swagger/OpenAPI 接口文档到 RAGFlow 知识库的完整流程。

---

## 前提条件

- RAGFlow 服务已部署并可访问
- 拥有 RAGFlow API Key
- 目标项目提供了 OpenAPI/Swagger 接口文档端点

## 环境变量

以下信息以 RuoYi-Vue-Pro 项目为例：

```
RAGFLOW_API=http://81.70.235.9:9380/api/v1
RAGFLOW_KEY=ragflow-08NOsrv8Ov-wF7AMgjap3awcowbE0-xcg95tgBEZ6K8
SWAGGER_URL=http://81.70.235.9:48080/v3/api-docs
```

---

## 步骤一：导出 OpenAPI JSON

从运行中的服务导出 OpenAPI 规范文件：

```bash
# 通过 SSH 从远程服务器导出
ssh agent-for-ai-server "curl -s http://localhost:48080/v3/api-docs" > contracts/ruoyi-vue-pro-openapi.json

# 如果是本地运行的服务
curl -s http://localhost:8080/v3/api-docs > openapi.json
```

验证导出结果：

```bash
python3 -c "import json; d=json.load(open('openapi.json')); print(f'接口数: {sum(len(v) for v in d[\"paths\"].values())}')"
```

---

## 步骤二：转换为扁平格式 Markdown

**这是最关键的步骤。** 转换质量直接决定检索效果。

### 为什么需要转换？

RAGFlow 的 `book` 分块按 Markdown 标题切分。直接上传原始 JSON 会被按 token 数机械切割，一个接口的定义可能被拆碎。转换的目标是**每个接口生成一个独立的、完整的、无子标题的段落**。

### 使用转换脚本

```bash
python3 scripts/openapi2md.py contracts/ruoyi-vue-pro-openapi.json -o /tmp/api-docs.txt --by-tag
```

### 转换格式要求

生成的 Markdown **必须**满足以下条件：

1. **只用 `##` 标题**，不用 `#`（模块分组用）或 `###`（子标题）
2. **标题与内容之间无空行**
3. **接口之间无分隔符**（不用 `---`）
4. **请求参数、请求体、响应都用内联格式**，不用表格或代码块
5. **文件后缀用 `.txt`**（RAGFlow `book` 分块不支持 `.md`）

正确格式：

```
## POST /admin-api/system/user/create - 新增用户
模块:管理后台 - 用户 | operationId:createUser | 请求体(application/json,必填): username(string, 必填, 用户账号); password(string, 必填, 密码) | 响应: 200 OK: code(integer); data(integer)
```

错误格式（会被切碎）：

```markdown
## POST /admin-api/system/user/create - 新增用户

### 模块信息
管理后台 - 用户

### 请求体
```json
{"username": "string", "password": "string"}
```

### 响应
| 字段 | 类型 |
|------|------|
| code | integer |

---
```

---

## 步骤三：通过 API 创建知识库

```bash
# 创建知识库（chunk_method 用 book）
curl -s -X POST ${RAGFLOW_API}/datasets \
  -H "Authorization: Bearer ${RAGFLOW_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ruoyi-api-docs",
    "description": "RuoYi-Vue-Pro API接口文档",
    "chunk_method": "book"
  }'
# 返回中获取 dataset_id
```

---

## 步骤四：上传文档

```bash
# 上传 .txt 文件
curl -s -X POST ${RAGFLOW_API}/datasets/${DATASET_ID}/documents \
  -H "Authorization: Bearer ${RAGFLOW_KEY}" \
  -F "file=@/tmp/api-docs.txt"
# 返回中获取 document_id
```

**注意**：文件后缀必须是 `.txt`，不能用 `.md`。RAGFlow 的 `book` 分块不支持 `.md` 文件，会报错：
```
file type not supported yet(doc, docx, pdf, txt supported)
```

---

## 步骤五：触发文档解析

```bash
curl -s -X POST ${RAGFLOW_API}/datasets/${DATASET_ID}/chunks \
  -H "Authorization: Bearer ${RAGFLOW_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"document_ids\": [\"${DOCUMENT_ID}\"]}"
```

解析是异步的，需要等待。可以通过以下命令轮询状态：

```bash
curl -s "${RAGFLOW_API}/datasets/${DATASET_ID}/documents?page=1&page_size=10" \
  -H "Authorization: Bearer ${RAGFLOW_KEY}"
# 查看 run 字段：UNSTART -> RUNNING -> DONE / FAIL
```

---

## 步骤六：验证分块质量

### 检查分块数量

期望：**接口数量 ≈ chunk 数量**（接近 1:1）。

如果 chunk 数远大于接口数，说明分块碎片化，需要回到步骤二调整格式。

### 查看实际 chunk 内容

```bash
curl -s "${RAGFLOW_API}/datasets/${DATASET_ID}/documents/${DOCUMENT_ID}/chunks?page=1&page_size=5" \
  -H "Authorization: Bearer ${RAGFLOW_KEY}"
```

每个 chunk 应包含完整的接口信息（方法+路径+参数+响应），而不是只有标题或只有参数。

### 测试检索效果

```bash
curl -s -X POST ${RAGFLOW_API}/retrieval \
  -H "Authorization: Bearer ${RAGFLOW_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "创建用户的接口",
    "dataset_ids": ["'"${DATASET_ID}"'"],
    "page": 1,
    "page_size": 3,
    "similarity_threshold": 0.1
  }'
```

验证：
- 命中的 chunk 是否包含目标接口的完整信息
- similarity 是否合理（> 0.2 一般算相关）

---

## 一键脚本

以下脚本将步骤 3-5 合并为一次执行（假设环境变量已设置）：

```bash
#!/bin/bash
set -e

FILE=${1:?用法: $0 <api-docs.txt>}
API=${RAGFLOW_API:?请设置 RAGFLOW_API}
KEY=${RAGFLOW_KEY:?请设置 RAGFLOW_KEY}
NAME=${2:-"api-docs"}

# 创建知识库
DS=$(curl -s -X POST ${API}/datasets \
  -H "Authorization: Bearer ${KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"${NAME}\", \"chunk_method\": \"book\"}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['id'])")
echo "dataset_id=${DS}"

# 上传文档
DOC=$(curl -s -X POST ${API}/datasets/${DS}/documents \
  -H "Authorization: Bearer ${KEY}" \
  -F "file=@${FILE}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data'][0]['id'])")
echo "doc_id=${DOC}"

# 触发解析
curl -s -X POST ${API}/datasets/${DS}/chunks \
  -H "Authorization: Bearer ${KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"document_ids\": [\"${DOC}\"]}"
echo ""
echo "解析已触发，等待完成..."

# 等待解析完成
while true; do
  STATUS=$(curl -s "${API}/datasets/${DS}/documents?page=1&page_size=1" \
    -H "Authorization: Bearer ${KEY}" \
    | python3 -c "import json,sys; d=json.load(sys.stdin)['data']['docs'][0]; print(d['run'])")
  if [ "$STATUS" = "DONE" ] || [ "$STATUS" = "FAIL" ]; then
    break
  fi
  sleep 10
done

# 输出结果
curl -s "${API}/datasets/${DS}/documents?page=1&page_size=1" \
  -H "Authorization: Bearer ${KEY}" \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)['data']['docs'][0]
print(f'状态: {d[\"run\"]}, chunks: {d[\"chunk_count\"]}, tokens: {d[\"token_count\"]}')
if 'progress_msg' in d and 'ERROR' in d.get('progress_msg',''):
    print(d['progress_msg'][-300:])
"
echo "dataset_id=${DS}"
echo "doc_id=${DOC}"
```

---

## 更新知识库（接口变更时）

当接口发生变更时，重新执行完整流程：

```bash
# 1. 重新导出
ssh agent-for-ai-server "curl -s http://localhost:48080/v3/api-docs" > contracts/ruoyi-vue-pro-openapi.json

# 2. 重新转换
python3 scripts/openapi2md.py contracts/ruoyi-vue-pro-openapi.json -o /tmp/api-docs.txt --by-tag

# 3. 删除旧知识库
curl -s -X DELETE ${RAGFLOW_API}/datasets \
  -H "Authorization: Bearer ${RAGFLOW_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"ids": ["'"${DATASET_ID}"'"]}'

# 4. 重新创建（使用上面的一键脚本）
bash upload-to-ragflow.sh /tmp/api-docs.txt ruoyi-api-docs
```

---

## 分块策略对比

| 策略 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| `book`（推荐） | 结构化 Markdown | 按标题切分，每个接口独立 chunk | 对格式要求严格 |
| `naive` | 无结构的纯文本 | 简单 | 可能拆碎接口定义 |
| `manual` | 精确控制 | 可手动标注每个 chunk | 耗时，不适合大量接口 |
| `qa` | QA 格式文档 | 问答对天然分块 | 接口文档不是 QA 格式 |
