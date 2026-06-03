# `ruoyi-user-management-srs-v2.pdf` 逆向生成过程汇报

## 1. 结论摘要

`ruoyi-user-management-srs-v2.pdf` 围绕 RuoYi-Vue-Pro 用户管理模块源码与接口实现逆向整理、迭代优化而来。演进链路如下：

```text
开源项目源码
→ 逆向整理 PRD 文本
→ 生成 PRD PDF
→ 在 RAGFlow 中验证 PDF 分块质量
→ 发现 PDF 文本层/段落结构问题
→ 重构为更接近真实 SRS 风格的 v2 文档
→ 用于 RAGFlow 知识库与 TestHub 自动化链路验证
```

---

## 2. 已确认事实清单

### 2.1 基于开源项目源码逆向整理出 PRD 文本

以 RuoYi-Vue-Pro 用户管理模块为试点，基于源码生成了纯产品需求文档 `docs/ruoyi-user-management-prd.txt`，并已与项目实现进行过复核对齐。对齐依据包括 `UserController`、`AdminUserServiceImpl`、`UserSaveReqVO`、SQL 权限数据。

### 2.2 将 PRD 文本生成 PDF，用于 RAGFlow 知识库测试

生成了 `docs/ruoyi-user-management-prd.pdf`（WeasyPrint 生成），并上传 RAGFlow 进行知识库创建和分块质量测试：

```text
需求文档 PDF
→ 上传 RAGFlow
→ 构建知识库
→ 评估 chunk 质量
→ 验证是否适合下游 Agent 检索与测试场景生成
```

### 2.3 围绕 PDF 分块质量进行了两轮共 8 组测试

覆盖了 `book + DeepDOC`、`book + Plain Text`、`book + Vision`、`naive + DeepDOC`、`naive + Plain Text`、overlap 等组合，目标是最适合 RAGFlow 检索的 PDF 结构和解析方案。

### 2.4 确认根因在 PDF 文本层结构

对比真实 SRS（Word 导出）与自生成 PRD PDF（WeasyPrint 生成）后发现：

- WeasyPrint 生成的 PDF 为逐行 bullet，标题与正文、字段规则、异常说明之间不够连续；
- 这导致 `book` 分块的标题层级合并效果差，`naive` 也只能机械合并，无法稳定保住语义边界。

### 2.5 SRS v2 已生成，chunk 质量优于前序版本

v2 使用 `book + DeepDOC`，结果 35 chunks，<50 字碎片率约 5.71%，已标记为推荐使用。

相比前一版增强内容：

- 明确必填字段：用户账号、用户昵称、密码
- 明确可选字段：部门、岗位、手机号、邮箱、性别、备注、头像
- 补充唯一性异常：账号/手机号/邮箱重复提示
- 补充导入异常：初始密码为空、导入文件为空
- 新增 Error Handling and Messages 章节

v2 由 ReportLab PDF Library 生成，创建于 2026-04-26。

### 2.6 SRS v2 已投入 RAGFlow → TestHub 自动化链路

`ruoyi-user-management-srs-v2.pdf` 作为 `requirement_doc`，与 API 文档知识库（`ruoyi-api-docs`）一起供 RAGFlow Agent 使用，生成符合 TestHub 契约的测试场景 JSON：

```text
SRS v2
→ RAGFlow 知识库
→ Agent 检索与生成
→ TestHub 场景导入
→ 测试执行验证
```

---

## 3. 演进阶段总览

| 阶段 | 动作 |
|------|------|
| 阶段 1 | 从 RuoYi-Vue-Pro 源码逆向整理出 PRD 文本 |
| 阶段 2 | 将 PRD 文本生成 PDF（WeasyPrint），上传 RAGFlow 做知识库 |
| 阶段 3 | 多轮 PDF 分块测试，确认根因在文本层结构 |
| 阶段 4 | 重构为 SRS 风格 v2 文档（ReportLab 生成） |
| 阶段 5 | v2 投入 RAGFlow → TestHub 自动化链路验证 |

---

## 4. 结论

- `ruoyi-user-management-srs-v2.pdf` 是一次围绕源码逆向、知识库优化和测试自动化落地的迭代产物。
- 验证了：开源项目代码可逆向整理为需求型文档 → 优化为适合 RAG 检索的知识库输入 → 进入 TestHub 自动化执行链路，支撑测试场景生成与执行闭环。
