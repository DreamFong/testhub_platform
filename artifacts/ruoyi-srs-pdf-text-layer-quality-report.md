# RuoYi 用户管理再生成 SRS PDF 文本层质量检查报告

## 1. 检查对象

| 项目 | 文件 |
|------|------|
| 验收基准 PDF | `docs/ruoyi-user-management-srs-v2.pdf` |
| 再生成对齐稿 Markdown | `artifacts/ruoyi-user-management-srs-v2-regenerated-aligned.md` |
| 再生成 PDF | `artifacts/ruoyi-user-management-srs-v2-regenerated-aligned.pdf` |
| PDF 生成脚本 | `artifacts/generate_ruoyi_srs_pdf.py` |

---

## 2. PDF 生成结果

再生成 PDF 已使用 ReportLab 成功生成。

| 指标 | 结果 |
|------|------|
| Producer | ReportLab PDF Library |
| 页面大小 | A4 |
| 页数 | 6 |
| 文件大小 | 约 18.9 KB |
| 是否可提取文本层 | 是 |

---

## 3. 文本层指标对比

| 指标 | 既有 SRS v2 | 再生成 PDF |
|------|-------------|------------|
| 字符数 | 8701 | 7624 |
| 非空行数 | 192 | 192 |
| 短行数（<50 字符） | 140 | 155 |
| 短行比例 | 0.729 | 0.807 |
| FR-USER 行数 | 12 | 12 |
| form-feed 页标记口径页数 | 9 | 7 |

---

## 4. 关键需求项覆盖检查

以下关键项在既有 SRS v2 和再生成 PDF 文本层中均可检索到：

- FR-USER-001 到 FR-USER-012
- 用户账号
- 用户昵称
- 密码
- 手机号码
- 邮箱
- 部门
- 岗位
- 账号状态
- 初始密码不能为空
- 导入数据不能为空
- 角色关联
- 岗位关联
- Error Handling and Messages
- Acceptance Criteria
- Boundaries and Exclusions

---

## 5. 质量判断

再生成 PDF 的文本层已经满足以下要求：

- 标题结构可提取；
- 核心章节可检索；
- FR-USER 功能编号完整；
- 字段规则、异常处理、权限规则和验收标准均保留；
- 内容不是逐行孤立 bullet，而是以段落和表格为主；
- 可作为 RAGFlow 分块验证的输入。

需要注意的是，再生成 PDF 的短行比例略高于既有 SRS v2，主要原因是表格行、目录行和标题行较多。该现象与既有 SRS v2 的文本层表现接近，不影响当前作为复现样本进入下一步 RAGFlow 验证。

---

## 6. 当前结论

再生成 PDF 已达到“可进入 RAGFlow 分块验证”的状态。

下一步应执行：

```text
上传 regenerated aligned PDF
→ 使用 book + DeepDOC 解析
→ 查看 chunk 数量和碎片率
→ 用关键问题做检索验证
→ 判断是否达到既有 SRS v2 的检索质量
```
