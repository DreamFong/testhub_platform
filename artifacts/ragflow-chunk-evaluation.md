# RAGFlow 分块验证报告：RuoYi 用户管理再生成 SRS

## 1. 验证目标

本次验证目标是确认从 RuoYi-Vue-Pro 用户管理源码逆向生成的 SRS PDF，是否能够作为 RAGFlow 需求知识库输入，并稳定支持后续 RAGFlow → TestHub 自动化测试场景生成链路。

---

## 2. 验证对象

### 2.1 表格对齐版

- Markdown：`artifacts/ruoyi-user-management-srs-v2-regenerated-aligned.md`
- PDF：`artifacts/ruoyi-user-management-srs-v2-regenerated-aligned.pdf`
- RAGFlow 知识库：`ruoyi-user-srs-regenerated-aligned-20260603`
- SRS_KB_ID：`6aa9ae305f1011f18243434b552cc465`
- Document ID：`7417107a5f1011f18243434b552cc465`
- 分块方式：`book + DeepDOC`

### 2.2 RAGFlow 友好连续段落版

- Markdown：`artifacts/ruoyi-user-management-srs-v2-regenerated-ragflow-friendly.md`
- PDF：`artifacts/ruoyi-user-management-srs-v2-regenerated-ragflow-friendly.pdf`
- RAGFlow 知识库：`ruoyi-user-srs-regenerated-ragflow-friendly-20260603`
- SRS_KB_ID：`804270d25f1111f18243434b552cc465`
- Document ID：`805121cc5f1111f18243434b552cc465`
- 分块方式：`book + DeepDOC`

---

## 3. 分块结果对比

| 版本 | chunks | 短 chunk 数 | 短 chunk 比例 | 结论 |
|------|--------|-------------|---------------|------|
| 表格对齐版 | 34 | 1 | 2.94% | 总体可用，但部分表格明细没有稳定进入 chunk |
| RAGFlow 友好连续段落版 | 67 | 1 | 1.49% | 推荐使用，字段规则、错误处理和验收标准拆分更稳定 |

---

## 4. 表格对齐版问题

表格对齐版在 PDF 文本层上看起来与既有 SRS v2 更接近，但上传 RAGFlow 后，`book + DeepDOC` 对部分表格区域的抽取不稳定。

观察到的问题：

- `Error Handling and Messages` 标题可见，但错误处理明细表没有稳定进入相邻 chunk；
- `Acceptance Criteria` 泛化检索命中存在噪声；
- 表格区域存在被解析器跳过或切碎的风险。

因此，该版本可以作为样式对齐参考，但不适合作为最终推荐的 RAGFlow 输入。

---

## 5. RAGFlow 友好连续段落版结果

连续段落版将字段规则、权限规则、错误处理和验收标准从表格改写为自然段。解析后表现更稳定。

已确认稳定进入 chunk 的内容包括：

- 用户账号必填、唯一、格式和长度规则；
- 用户昵称必填和长度规则；
- 密码新增/重置必填和长度规则；
- 手机号和邮箱格式及唯一性规则；
- 用户账号重复、手机号重复、邮箱重复；
- 用户不存在；
- 部门或岗位不可用；
- 密码格式不符合规则；
- 导入文件为空；
- 导入初始密码为空；
- 导入部分失败；
- 超过租户账号配额；
- 用户列表、新增用户、删除用户、导入导出等验收标准。

---

## 6. 检索验证结果

### 6.1 新增用户的必填字段是什么？

结果：通过。  
Top hit 命中 `FR-USER-004`，明确返回新增用户必填字段包括用户账号、用户昵称和密码。

### 6.2 账号重复时系统如何处理？

结果：通过。  
Top hit 命中 `Error Handling and Messages`，明确返回系统阻止创建或保存，并提示账号已存在。

### 6.3 删除用户的业务规则是什么？

结果：通过。  
命中删除用户验收标准、`FR-USER-007` 和 Business Rules，能检索到删除确认、列表移除、清理角色关联和岗位关联等规则。

### 6.4 导入失败有哪些错误提示？

结果：通过。  
可检索到导入失败反馈、导入数据为空、初始密码为空、失败明细等内容。

### 6.5 手机号和邮箱有什么唯一性规则？

结果：通过。  
命中 Business Rules 和新增用户校验规则，明确手机号和邮箱填写后必须唯一。

### 6.6 导入初始密码为空时系统如何处理？

结果：通过。  
Top hit 命中 `Error Handling and Messages`，明确返回系统阻止导入，并提示初始密码不能为空。

### 6.7 验收标准检索

结果：通过，但建议使用具体问法。  
泛化问题“用户管理模块有哪些验收标准？”会命中文档元信息，效果不稳定；使用具体问法效果稳定，例如：

- 新增用户验收标准是什么？
- 删除用户验收标准是什么？
- 导入导出验收标准是什么？
- Acceptance Criteria 新增用户 删除用户 导入导出 验收标准

---

## 7. Retrieval Gate

`retrieval_gate = pass`

通过理由：

- 文档已成功解析和 embedding；
- 核心功能 FR-USER-001 到 FR-USER-012 可检索；
- 字段规则、业务规则、错误处理和验收标准可检索；
- 对后续 RAGFlow → TestHub 场景生成所需的业务约束支持充分。

---

## 8. 推荐后续 handoff 参数

```text
PROJECT_NAME=RuoYi-Vue-Pro 用户管理模块
BUSINESS_DOMAIN=System Management / User Management
TEST_SCOPE=后台用户管理：查询、新增、编辑、删除、重置密码、状态修改、导入、导出
MIN_BUSINESS_FLOW=管理员登录 → 创建用户 → 查询用户 → 修改用户 → 删除用户
SRS_KB_ID=804270d25f1111f18243434b552cc465
RETRIEVAL_PARAMS=similarity_threshold=0.30, keywords_similarity_weight=0.60, top_n=8, top_k=1024, use_kg=false
KNOWN_CAVEATS=验收标准检索建议使用具体问法；RAGFlow 输入文档优先使用连续段落而非表格。
```

---

## 9. 结论

从源码逆向生成的 SRS 已完成 RAGFlow 分块验证。推荐使用 `RAGFlow 友好连续段落版` 作为后续需求知识库输入。

该结果证明当前复现链路已经跑通到：

```text
源码阅读
→ SRS 逆向生成
→ PDF 生成
→ RAGFlow 知识库解析
→ chunk 质量检查
→ 检索 sanity check
→ retrieval gate pass
```
