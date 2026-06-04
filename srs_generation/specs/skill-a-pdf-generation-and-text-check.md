# Skill A：PDF 生成与文本层检查规范

版本：v0.2  
适用范围：Skill A Markdown → PDF 生成、文本层检查与人类可读性检查

## 1. 目标

Skill A 必须将最终 SRS Markdown 转换为带文本层且人类可读的 PDF，并在进入 Skill B 之前完成 PDF 质量检查。

该检查只判断 PDF 是否具备知识库输入和人工阅读的基本条件，不评估 RAGFlow chunk 或 retrieval 质量。

Skill A 默认输出知识库友好版 SRS，但 PDF 产物必须同时满足：

```text
内容结构知识库友好
PDF 样式人类可读
文本层可提取可搜索
排版风格参考已确认的原始 SRS v2
```

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
--font    字体名称或字体文件路径，可选；默认自动选择适合中英文混排的字体
```

PDF 生成要求：

- Markdown 控制正文标题，`--title` 优先作为 PDF metadata，不得导致正文标题重复。
- PDF 默认应使用适合中英文混排的字体，例如 Noto Sans CJK、思源黑体、思源宋体或文泉驿字体。
- 标题必须按 Markdown 层级渲染，不能把所有标题拍平成普通正文。
- 正文应保持自然段落和稳定行距，不能出现英文异常拆字、大量乱码、页面截断或溢出。
- 内置 PDF writer 只能作为兜底方案；如果兜底输出无法满足可读性 gate，不得判定为 PDF 完全合格。

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

PDF 检查分为两层：

```text
pdf_text_layer_gate
pdf_readability_gate
```

### 5.1 文本层 gate

文本层检查至少覆盖：

- PDF 是否存在。
- 文本是否可提取。
- 中文文本是否可识别。
- 标题是否可检出。
- FR 编号是否可检出。
- 关键字段规则是否可检出。
- 关键异常规则是否可检出。
- 验收标准关键词是否可检出。
- 提取文本中的英文术语是否保持正常形式。

### 5.2 可读性 gate

可读性检查至少覆盖：

- 标题不重复。
- 中英文混排正常。
- 英文项目名、类名、接口路径、权限码和 FR 编号没有异常拆字。
- 标题层级清晰。
- 正文段落连续可读。
- 页边距、行距、段落间距正常。
- 页面无明显截断、溢出、乱码。
- 整体风格简洁正式，接近已确认的原始 SRS v2。

可读性 gate 可由脚本自动检查部分项目，但视觉层级、页边距和整体风格仍需要人工确认。

## 6. Gate 影响

### pass

满足：

- `pdf_text_layer_gate = pass`。
- `pdf_readability_gate = pass`。
- 标题、FR 编号和关键术语均可检出。
- 未发现阻断级 PDF 排版或文本层问题。

### conditional pass

满足：

- 文本层可提取。
- 但部分标题、FR 编号、关键术语或可读性检查项需要人工确认或局部修复。

限制：

```text
conditional pass 不自动进入 Skill B。
```

### fail

任一命中：

- PDF 不存在。
- 文本提取失败。
- 文本长度过短。
- 中文文本无法识别。
- 标题重复且未修复。
- 英文术语出现异常拆字。
- 页面存在明显截断、溢出或乱码。
- PDF 阅读效果明显不满足人类可读性要求。

PDF 文本层不可提取或 PDF 可读性 gate fail 都是 Skill A 硬性不合格项，不得进入 Skill B。
