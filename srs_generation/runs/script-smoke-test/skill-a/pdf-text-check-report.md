# PDF 文本层检查报告

## 1. 基本信息

```text
pdf_file: srs_generation\runs\script-smoke-test\skill-a\srs-kb-friendly.pdf
report_file: srs_generation\runs\script-smoke-test\skill-a\pdf-text-check-report.md
page_count: 1
extraction_engine: builtin
```

## 2. 检查摘要

```text
pdf_generated: true
text_extractable: true
extracted_text_length: 237
has_chinese_text: true
has_title_structure: true
has_fr_numbers: true
recommended_gate_impact: pass
```

## 3. 标题检查

| 标题 | 是否检出 |
|---|---|
| 文档概述 | 是 |
| 模块范围 | 是 |
| 功能需求 | 是 |
| 字段与输入规则 | 是 |
| 业务规则 | 是 |
| 异常处理规则 | 是 |
| 验收标准 | 是 |

## 4. FR 编号检查

正则：`FR-[A-Za-z0-9]+-\d{3}`

检出结果：

- FR-USER-001

## 5. 关键术语检查

| 术语 | 是否检出 |
|---|---|
| 字段规则 | 是 |
| 异常处理 | 是 |
| 验收标准 | 是 |

## 6. 问题记录

| 问题 | 影响 | 处理建议 |
|---|---|---|
| 无 | low | 无需处理 |

## 7. 结论

```text
result: pass
reason: PDF 文本层可提取，标题、FR 编号和关键术语检查通过。
```
