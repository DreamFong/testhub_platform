# PDF 质量检查报告模板

## 1. 基本信息

```text
project: 
target_module: 
pdf_file: 
source_markdown: 
reference_pdf: 
checked_at: 
status: draft
```

## 2. 检查摘要

```text
pdf_generated: true | false
page_count: 
extraction_engine: 
text_extractable: true | false
extracted_text_length: 
has_chinese_text: true | false
has_title_structure: true | false
has_fr_numbers: true | false
has_key_field_rules: true | false
has_key_exception_rules: true | false
has_acceptance_criteria: true | false
has_duplicate_title: true | false
has_abnormal_english_spacing: true | false
pdf_text_layer_gate: pass | conditional pass | fail
pdf_readability_gate: pass | conditional pass | fail
recommended_gate_impact: pass | conditional pass | fail
```

## 3. 文本层 gate

| 检查项 | 结果 | 备注 |
|---|---|---|
| PDF 文件存在 |  |  |
| PDF 文本可提取 |  |  |
| 提取文本长度合理 |  |  |
| 中文文本可识别 |  |  |
| 标题可检出 |  |  |
| FR 编号可检出 |  |  |
| 字段规则可检出 |  |  |
| 异常处理可检出 |  |  |
| 验收标准可检出 |  |  |
| 关键英文术语提取正常 |  |  |

## 4. 标题检查

| 标题 | 是否检出 | 是否重复 | 备注 |
|---|---|---|---|
| 文档概述 |  |  |  |
| 模块范围 |  |  |  |
| 功能需求 |  |  |  |
| 字段与输入规则 |  |  |  |
| 业务规则 |  |  |  |
| 异常处理规则 |  |  |  |
| 验收标准 |  |  |  |

## 5. FR 编号检查

| FR 编号 | 是否检出 | 备注 |
|---|---|---|
|  |  |  |

## 6. 关键术语检查

| 术语 | 是否检出 | 类型 | 备注 |
|---|---|---|---|
|  |  | 字段规则 / 异常处理 / 验收标准 / 权限 / 接口 |  |

## 7. 可读性 gate

| 检查项 | 结果 | 检查方式 | 备注 |
|---|---|---|---|
| 标题不重复 |  | 自动 + 人工 |  |
| 中英文混排正常 |  | 自动 + 人工 |  |
| 英文术语没有异常拆字 |  | 自动 |  |
| 标题层级清晰 |  | 人工 |  |
| 正文段落连续可读 |  | 人工 |  |
| 页边距、行距、段落间距正常 |  | 人工 |  |
| 页面无明显截断、溢出、乱码 |  | 人工 |  |
| 整体风格简洁正式，接近参考 SRS / PDF |  | 人工 |  |

## 8. 自动发现的问题

| 问题 | 影响 | 处理建议 |
|---|---|---|
|  | high / medium / low |  |

## 9. 人工可读性确认

```text
manual_readability_checked: true | false
manual_readability_result: pass | conditional pass | fail
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
pdf_text_layer_gate: pass | conditional pass | fail
pdf_readability_gate: pass | conditional pass | fail
result: pass | conditional pass | fail
reason: 
allowed_to_enter_skill_b: true | false
```
