# PDF 质量检查报告

## 1. 基本信息

```text
pdf_file: /root/work/genlot/projects/testhub_platform/srs_generation/runs/ruoyi-vue-pro-erp-warehouse-validation-20260607/skill-a/srs-kb-friendly.pdf
report_file: /root/work/genlot/projects/testhub_platform/srs_generation/runs/ruoyi-vue-pro-erp-warehouse-validation-20260607/skill-a/pdf-text-check-report.md
page_count: 3
extraction_engine: pypdf
reference_pdf: docs/ruoyi-user-management-srs-v2.pdf
```

## 2. 检查摘要

```text
pdf_generated: true
text_extractable: true
extracted_text_length: 2262
has_chinese_text: true
has_title_structure: true
has_fr_numbers: true
has_key_field_rules: true
has_key_exception_rules: true
has_acceptance_criteria: true
has_duplicate_title: false
has_abnormal_english_spacing: false
pdf_text_layer_gate: pass
pdf_readability_gate: pass
recommended_gate_impact: pass
```

## 3. 文本层 gate

| 检查项 | 结果 | 备注 |
|---|---|---|
| PDF 文件存在 | 是 |  |
| PDF 文本可提取 | 是 | 文本长度：2262 |
| 中文文本可识别 | 是 |  |
| 标题可检出 | 是 | 缺失：无 |
| FR 编号可检出 | 是 | 数量：8 |
| 字段规则可检出 | 是 |  |
| 异常处理可检出 | 是 |  |
| 验收标准可检出 | 是 |  |
| 关键英文术语提取正常 | 是 | 无异常拆字 |

## 4. 标题检查

| 标题 | 是否检出 | 是否重复 | 备注 |
|---|---|---|---|
| 文档概述 | 是 | 否 | 出现 1 次 |
| 模块范围 | 是 | 否 | 出现 1 次 |
| 功能需求 | 是 | 否 | 出现 1 次 |
| 字段与输入规则 | 是 | 否 | 出现 1 次 |
| 业务规则 | 是 | 否 | 出现 1 次 |
| 异常处理规则 | 是 | 否 | 出现 1 次 |
| 验收标准 | 是 | 否 | 出现 1 次 |

## 5. FR 编号检查

正则：`FR-[A-Za-z0-9]+-\d{3}`

检出结果：

- FR-WH-001
- FR-WH-002
- FR-WH-003
- FR-WH-004
- FR-WH-005
- FR-WH-006
- FR-WH-007
- FR-WH-008

## 6. 关键术语检查

| 术语 | 是否检出 |
|---|---|
| 仓库 | 是 |
| 默认 | 是 |
| 异常 | 是 |
| 验收标准 | 是 |

## 7. 可读性 gate

| 检查项 | 结果 | 检查方式 | 备注 |
|---|---|---|---|
| 标题不重复 | 是 | 自动 | 无重复标题 |
| 中英文混排正常 | 是 | 自动 + 人工 | 未发现异常拆字 |
| 英文术语没有异常拆字 | 是 | 自动 |  |
| 标题层级清晰 | 待人工确认 | 人工 | 自动脚本不判断视觉层级 |
| 正文段落连续可读 | 待人工确认 | 人工 | 自动脚本不判断段落视觉效果 |
| 页边距、行距、段落间距正常 | 待人工确认 | 人工 | 自动脚本不判断版式舒适度 |
| 页面无明显截断、溢出、乱码 | 待人工确认 | 人工 | 自动脚本不判断页面截图 |
| 整体风格简洁正式，接近原始 SRS v2 | 待人工确认 | 人工 | 需人工对照 reference_pdf |

## 8. 自动发现的问题

| 问题 | 影响 | 处理建议 |
|---|---|---|
| 无自动发现问题 | low | 人工确认可读性后可进入下一步 |

## 9. 人工可读性确认

```text
manual_readability_checked: true
manual_readability_result: pass
manual_reviewer: 
manual_checked_at: 
manual_notes: 
```

建议人工至少检查：

- 首页标题和文档概述页
- 一个功能需求页
- 字段规则相关页面
- 异常处理或验收标准相关页面

## 10. 结论

```text
pdf_text_layer_gate: pass
pdf_text_layer_reason: PDF 文本层可提取，标题、FR 编号、关键术语和英文术语检查通过。
pdf_readability_gate: pass
pdf_readability_reason: 自动检查通过，人工可读性检查通过。
result: pass
allowed_to_enter_skill_b: true
```
