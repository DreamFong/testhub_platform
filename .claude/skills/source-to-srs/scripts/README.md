# SRS Generation Scripts

## generate_srs_pdf.py

将 Markdown SRS 转换为带文本层且人类可读的 PDF。

特点：

- 默认优先使用 ReportLab。
- 默认自动选择适合中英文混排的字体。
- Markdown 标题控制正文标题，`--title` 主要作为 PDF metadata，避免标题重复。
- 保留标题层级、连续段落和简洁正式的阅读风格。
- 当 ReportLab 不可用时，内置 PDF writer 仅作为兜底路径。

示例：

```bash
python <skill_dir>/scripts/generate_srs_pdf.py \
  --input path/to/srs-kb-friendly.md \
  --output path/to/srs-kb-friendly.pdf \
  --title "模块 SRS"
```

## check_pdf_text_layer.py

检查 PDF 文本层、标题、FR 编号、关键术语和部分可读性问题。

输出两个 gate：

```text
pdf_text_layer_gate
pdf_readability_gate
```

自动检查包括：

- PDF 文本是否可提取。
- 中文文本是否可识别。
- 标题、FR 编号和关键术语是否可检出。
- 标题是否重复。
- 英文术语是否存在异常拆字。

页边距、标题视觉层级、整体风格是否接近参考 SRS / PDF 仍需要人工确认；可通过 `--manual-readability pass` 记录人工确认结果。

示例：

```bash
python <skill_dir>/scripts/check_pdf_text_layer.py \
  --pdf path/to/srs-kb-friendly.pdf \
  --report path/to/pdf-text-check-report.md \
  --key-term 字段规则 \
  --key-term 异常处理 \
  --key-term 验收标准 \
  --manual-readability pass
```
