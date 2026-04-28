# RAGFlow PDF 分块优化工作交接摘要

- 日期: 2026-04-24
- 项目: testhub_platform
- 目标: 走通 RAGFlow 知识库 → Agent 生成测试场景 → TestHub 导入执行的端到端流程
- 当前阶段: RAGFlow 知识库构建与 PDF 分块质量优化

---

## 1. 背景与目标

以 RuoYi-Vue-Pro 用户管理模块为试点，验证 RAGFlow 知识库的文档切片质量。要求使用 PDF 格式（硬性要求，需推广到所有项目），找到最佳的分块策略 + 解析器组合。

## 2. 已完成工作

### 2.1 PRD 文档生成

- 基于 RuoYi-Vue-Pro 源码（`~/projects/github/ruoyi-vue-pro`）生成了纯产品需求文档
- 文件: `docs/ruoyi-user-management-prd.txt`（454 行，v1.1 已复核对齐）
- PDF: `docs/ruoyi-user-management-prd.pdf`（353KB，13 页，WeasyPrint 生成）
- 已与项目实际实现（UserController、AdminUserServiceImpl、UserSaveReqVO、SQL 权限数据）完全对齐

### 2.2 RAGFlow 知识库创建

- 知识库名: `ruoyi-prd`
- 知识库 ID: `4377d38e3fba11f1bb078f6f74f53e6e`
- 文档 ID: `643a835a3fba11f1bb078f6f74f53e6e`
- RAGFlow 地址: `http://81.70.235.9:9380`
- Embedding 模型: `bge-m3___OpenAI-API@OpenAI-API-Compatible`

### 2.3 PDF 分块测试（两轮共 8 组）

#### 第一轮：book 分块策略 × 不同解析器

| # | 分块策略 | 解析器 | 状态 | Chunks | 碎片率(<50字) | 核心问题 |
|---|---------|--------|------|--------|-------------|---------|
| 1 | book | DeepDOC | DONE | 65 | 34% | 同一小节拆成多块 |
| 2 | book | Plain Text | DONE | 284 | 96.5% | 逐行切分，极端碎片 |
| 3 | book | Docling | FAIL | - | - | 服务器未安装 |
| 4 | book | TCADP | FAIL | - | - | 服务未授权 |
| 5 | book | gemma-4 Vision | DONE | 7 | 0% | 30% 内容重复 |

#### 第二轮：切换分块策略

| # | 分块策略 | 解析器 | 状态 | Chunks | 碎片率 | 核心问题 |
|---|---------|--------|------|--------|--------|---------|
| 6 | naive | DeepDOC | DONE | 12 | 0% | 功能点边界被切断 |
| 7 | naive | Plain Text | DONE | 12 | 0% | 章节顺序被打乱 |
| 8 | book | DeepDOC(512t) | DONE | 65 | 34% | chunk_token_num 未生效 |

### 2.4 overlap 测试

- 在 `ruoyi-prd-test-naive-deepdoc` 上设置 `overlapped_percent: 0.2`（通过 UI）
- 重新解析后验证：**overlap 未生效**，12 个 chunk 之间无重叠内容
- 原因：虽然配置写入了数据库，但 naive + DeepDOC 的代码路径未实际使用该参数

### 2.5 真实 SRS PDF 对比

- 从 RAGFlow `requirements_srs` 知识库下载了真实需求书 `FINAL SIGNED GENLOT Central System General SRS v1.pdf`（21 页，605KB）
- 对比发现根因：**WeasyPrint 生成的 PDF 文本层是逐行 bullet 格式，而真实 SRS（Word 导出）是连续段落格式**

| 维度 | 真实 SRS PDF（Word 导出） | 我们的 PRD PDF（WeasyPrint） |
|------|-------------------------|---------------------------|
| 文本密度 | 每页 1,000~5,000 字符 | 每页 400~1,500 字符 |
| 段落结构 | 连续自然语言段落 | 每行一个 `•` 列表项 |
| 标题+内容 | 标题后紧跟正文段落 | 标题独立成行，列表项各自独立成行 |

---

## 3. 关键结论

### 3.1 当前最优方案

**`naive` 分块策略 + `DeepDOC` 解析器**（测试 #6）:
- 12 chunks，0% 碎片，大小均匀（165~665 字符）
- 章节顺序正确
- 缺点：功能点边界被机械切断（如"导入应失败"被拆成"导入应失"+"败。"）

### 3.2 根因分析

问题不在 RAGFlow 解析器或分块策略，而在 **PDF 文本层格式**：
- WeasyPrint（HTML → PDF）生成的是逐行 bullet 格式
- `book` 的 TitleChunker 期望标题后跟连续段落，bullet 格式导致 hierarchical_merge 失效
- `naive` 的 naive_merge 按 token 数合并能缓解碎片化，但无法保证语义边界

### 3.3 不可用的方案

- **Docling**: 服务器未安装，需要 `pip install docling`
- **TCADP Parser**: 需要配置腾讯文档解析服务 API key
- **Plain Text 解析器**: PDF 文本层提取会导致章节乱序
- **gemma Vision**: 内容重复严重（30%），解析耗时 173 秒
- **overlapped_percent**: API 不支持设置，UI 设置后也未实际生效

---

## 4. 待解决问题

### 4.1 优化方向（按优先级）

1. **改 PDF 生成方式（推荐）**
   - 不用 WeasyPrint，改用 `python-docx` 生成 `.docx` 再转 PDF
   - 或用 `fpdf2` 生成段落式 PDF，让文本层保持连续性
   - 目标：文本层格式接近真实 SRS PDF（标题后跟连续段落）
   - 改进后重新测试 naive + DeepDOC 或 book + DeepDOC

2. **在 RAGFlow UI 上调试 overlap**
   - 当前 naive + DeepDOC 的 overlap 未生效，可能是 RAGFlow 版本 bug
   - 可以在 RAGFlow GitHub 提 issue 或查看最新版本是否修复

3. **安装 Docling**
   - `pip install docling` 后重新测试 book + Docling 组合
   - Docling 是结构化文档解析器，理论上对标题清晰文档效果最好

4. **配置 TCADP Parser**
   - 需要腾讯文档解析服务的 API key
   - 中文文档优化，可能对中文 PRD 效果更好

### 4.2 下一步工作

- 确定 PDF 生成优化方案并重新生成 PDF
- 用优化后的 PDF 重新测试分块质量
- 验证检索效果（用实际 Agent 查询测试）
- 清理测试知识库（保留最优方案，删除其他测试库）
- 将 ruoyi-api-docs 和优化后的 ruoyi-prd 关联到 RAGFlow Agent
- 验证完整流程: PRD + API 文档 → Agent 生成测试场景 → TestHub 导入

---

## 5. RAGFlow 测试知识库清单

以下测试知识库可清理：

| 知识库名 | dataset_id | 状态 | 建议 |
|----------|-----------|------|------|
| ruoyi-prd-test-naive | 8128ac0c3fca11f1bb078f6f74f53e6e | book+PlainText 284碎片 | 删除 |
| ruoyi-prd-test-docling | 8058477e3fca11f1bb078f6f74f53e6e | FAIL 未安装 | 删除 |
| ruoyi-prd-test-tcadp | 87fee7763fca11f1bb078f6f74f53e6e | FAIL 未授权 | 删除 |
| ruoyi-prd-test-gemma | 8194ccf23fca11f1bb078f6f74f53e6e | 7chunks/30%重复 | 删除 |
| ruoyi-prd-test-naive-deepdoc | b791f8783fd611f1bb078f6f74f53e6e | 12chunks/0%碎片(当前最优) | 暂留 |
| ruoyi-prd-test-naive-plaintext | ba2c4d403fd611f1bb078f6f74f53e6e | 章节乱序 | 删除 |
| ruoyi-prd-test-book-deepdoc-512 | b7db65c63fd611f1bb078f6f74f53e6e | 同原始65chunks | 删除 |
| ruoyi-prd-test-naive-overlap | 6fac1b863fd811f1bb078f6f74f53e6e | 未完成测试 | 删除 |

保留的知识库：

| 知识库名 | dataset_id | 用途 |
|----------|-----------|------|
| ruoyi-prd | 4377d38e3fba11f1bb078f6f74f53e6e | 原始 PRD（book+DeepDOC） |
| ruoyi-api-docs | 02b7eebc3f1311f1bb078f6f74f53e6e | API 接口文档 |

---

## 6. RAGFlow book 分块技术细节

### 6.1 处理流水线

```
PDF 文件 → Parser（文本提取） → TitleChunker（标题识别+层级合并） → Tokenizer（向量化+索引）
```

### 6.2 PDF 解析器选项

| 解析器 | 处理方式 | 可用性 |
|--------|---------|--------|
| DeepDOC（默认） | PDF 渲染为图片 → OCR → 布局分析 | 可用 |
| Plain Text (Naive) | 直接提取 PDF 内嵌文本，按 `\n` 分行 | 可用（但乱序） |
| Docling | IBM 结构化文档解析 | 未安装 |
| TCADP Parser | 腾讯文档解析 | 未授权 |
| MinerU | MinerU 解析器 | 未安装（UI 不显示） |
| PaddleOCR | PaddleOCR 引擎 | 未安装 |
| Vision 模型 | 多模态 LLM"看"PDF 页面 | 可用（gemma-4-31b-it） |

### 6.3 TitleChunker 标题匹配规则

book 分块的 TitleChunker 内置 5 套标题匹配规则（`levels` 参数），支持：
1. Markdown 格式: `#`, `##`, `###`, `####`
2. 中文编号: 第X编、第X章、第X节、第X条
3. 阿拉伯数字: `1.`, `1.1`, `1.1.1`
4. 中文数字混合
5. 英文: PART ONE, Chapter I, Section X

`hierarchy: 5` 表示最多识别 5 级深度。前端 UI 不暴露粒度选择器。

### 6.4 API 参考

```bash
# 创建知识库
curl -X POST ${RAGFLOW_API}/datasets \
  -H "Authorization: Bearer ${RAGFLOW_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"name": "xxx", "chunk_method": "naive", "embedding_model": "bge-m3___OpenAI-API@OpenAI-API-Compatible"}'

# 上传文档
curl -X POST ${RAGFLOW_API}/datasets/${DS_ID}/documents \
  -H "Authorization: Bearer ${RAGFLOW_KEY}" \
  -F "file=@/path/to/file.pdf"

# 触发解析
curl -X POST ${RAGFLOW_API}/datasets/${DS_ID}/chunks \
  -H "Authorization: Bearer ${RAGFLOW_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"document_ids": ["${DOC_ID}"]}'

# 查看解析状态
curl "${RAGFLOW_API}/datasets/${DS_ID}/documents?page=1&page_size=10" \
  -H "Authorization: Bearer ${RAGFLOW_KEY}"

# 查看 chunk 内容
curl "${RAGFLOW_API}/datasets/${DS_ID}/documents/${DOC_ID}/chunks?page=1&page_size=100" \
  -H "Authorization: Bearer ${RAGFLOW_KEY}"

# 检索测试
curl -X POST ${RAGFLOW_API}/retrieval \
  -H "Authorization: Bearer ${RAGFLOW_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"question": "新增用户的必填字段", "dataset_ids": ["${DS_ID}"], "page": 1, "page_size": 3, "similarity_threshold": 0.1}'
```

注意：`overlapped_percent` 和 `parser_config.layout_recognize` 等参数只能通过 UI 设置，API 创建/更新接口不接受这些字段。

---

## 7. 相关文件

| 文件 | 说明 |
|------|------|
| `docs/ruoyi-user-management-prd.txt` | 用户管理模块 PRD 纯文本版 |
| `docs/ruoyi-user-management-prd.pdf` | PRD PDF 版（WeasyPrint 生成） |
| `docs/ragflow-kb-creation-guide.md` | RAGFlow 知识库创建指南 |
| `/tmp/genlot-srs2.pdf` | 真实 SRS PDF（用于对比分析） |
