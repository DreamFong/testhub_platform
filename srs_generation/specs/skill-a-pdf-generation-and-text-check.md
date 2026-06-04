# Skill A：PDF 生成与文本层检查规范

版本：v0.1  
适用范围：Skill A Markdown → PDF 生成与基础可用性检查

## 1. 目标

Skill A 必须将最终 SRS Markdown 转换为带文本层的 PDF，并在进入 Skill B 之前完成基础可用性检查。

该检查只判断 PDF 是否具备知识库输入的基本条件，不评估 RAGFlow chunk 或 retrieval 质量。

## 2. Markdown 输入规范

Markdown 文档应满足：

- 使用稳定标题层级。
- 功能需求使用 `FR-{MODULE}-{NNN}` 编号。
- 列表使用标准 Markdown 语法。
- 避免复杂表格承载唯一关键规则。
- 中文正文应保留为真实文本，而不是图片。
- 代码块仅用于少量路径、参数或示例，不承载主要需求内容。

## 3. PDF 生成脚本

默认脚本：

```text
srs_generation/scripts/generate_srs_pdf.py
```

参数：

```text
--input   输入 Markdown 路径
--output  输出 PDF 路径
--title   PDF 标题，可选
--author  PDF 作者元数据，可选
--subject PDF 主题元数据，可选
--font    中文 CID 字体，可选，默认 STSong-Light
```

示例：

```bash
python srs_generation/scripts/generate_srs_pdf.py \
  --input srs-kb-friendly.md \
  --output srs-kb-friendly.pdf \
  --title "用户管理 SRS"
```

## 4. 文本层检查脚本

默认脚本：

```text
srs_generation/scripts/check_pdf_text_layer.py
```

参数：

```text
--pdf             输入 PDF 路径
--report          输出检查报告路径
--required-title  必须检出的标题，可重复
--fr-regex        FR 编号正则，默认 FR-[A-Za-z0-9]+-\d{3}
--key-term        必须检出的关键术语，可重复
--min-text-length 最小文本长度，默认 100
--strict          conditional pass 时也返回非零退出码
```

示例：

```bash
python srs_generation/scripts/check_pdf_text_layer.py \
  --pdf srs-kb-friendly.pdf \
  --report pdf-text-check-report.md \
  --key-term 字段规则 \
  --key-term 异常处理 \
  --key-term 验收标准
```

## 5. 检查内容

文本层检查至少覆盖：

- PDF 是否存在。
- 文本是否可提取。
- 中文文本是否可识别。
- 标题是否可检出。
- FR 编号是否可检出。
- 关键字段规则是否可检出。
- 关键异常规则是否可检出。
- 验收标准关键词是否可检出。

## 6. Gate 影响

### pass

满足：

- 文本层可提取。
- 中文文本可识别。
- 标题、FR 编号和关键术语均可检出。

### conditional pass

满足：

- 文本层可提取。
- 但部分标题、FR 编号或关键术语未检出。

### fail

任一命中：

- PDF 不存在。
- 文本提取失败。
- 文本长度过短。
- 中文文本无法识别。

PDF 文本层不可提取是 Skill A 硬性不合格项，不得进入 Skill B。
