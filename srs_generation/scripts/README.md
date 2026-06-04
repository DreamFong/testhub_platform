# SRS Generation Scripts

## generate_srs_pdf.py

将 Markdown SRS 转换为带文本层的 PDF。

示例：

```bash
python srs_generation/scripts/generate_srs_pdf.py \
  --input path/to/srs-kb-friendly.md \
  --output path/to/srs-kb-friendly.pdf \
  --title "模块 SRS"
```

## check_pdf_text_layer.py

检查 PDF 文本层、标题、FR 编号和关键术语。

示例：

```bash
python srs_generation/scripts/check_pdf_text_layer.py \
  --pdf path/to/srs-kb-friendly.pdf \
  --report path/to/pdf-text-check-report.md \
  --key-term 字段规则 \
  --key-term 异常处理 \
  --key-term 验收标准
```
