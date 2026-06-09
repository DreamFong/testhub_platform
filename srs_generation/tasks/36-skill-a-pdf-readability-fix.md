# Skill A PDF 可读性修复任务拆解

> 当前状态：本文件已归并到 `../exec-plans/completed/plan-0001-skill-a-foundation-and-validation.md`，作为历史修复清单保留。

## 1. 背景

当前 Skill A 已经完成规范、模板、prompt、PDF 脚本、两个样本验证和 handoff 包。已有样本的 PDF 文本层检查为 `pass`，但用户在查看用户管理样本 PDF 时发现明显阅读体验问题：

```text
RuoYi-Vue-Pro 被显示成 R u o Y i - V u e - P r o
Controller / Service 等英文术语被拆成大间距字母
标题重复出现
标题层级不明显
整体排版过于简陋
```

该问题说明现有 PDF gate 只覆盖“文本层可提取”，没有覆盖“人类可读性”。

## 2. 修复目标

Skill A 默认仍输出 **知识库友好版 SRS**，但 PDF 产物必须同时满足：

```text
内容结构知识库友好
PDF 样式人类可读
文本层可提取可搜索
排版风格参考已确认的原始 SRS v2
```

参考基准：

- `docs/ruoyi-user-management-srs-v2.pdf`

目标不是像素级复刻原始 PDF，而是保持其简洁、正式、清晰、可读的文档风格。

## 3. 当前问题定性

当前问题属于 **Skill A PDF 产物质量缺口**，不是 SRS 内容生成失败。

需要修复的是：

- PDF 生成脚本
- PDF 文本层与可读性检查脚本
- PDF gate 标准
- PDF 检查报告模板
- 两个样本 PDF 与 gate 结果
- handoff 包中的 PDF 与报告

## 4. 非目标

本任务不进入 Skill B / Skill C，不做以下事项：

- 不创建 RAGFlow 知识库
- 不上传 PDF 到 RAGFlow
- 不执行 chunk 质量评估
- 不执行 retrieval sanity check
- 不执行 retrieval gate
- 不提炼执行约束
- 不操作 TestHub 自动化闭环

## 5. 任务拆解

### 5.1 更新 Skill A PDF 质量标准

涉及文件：

- `srs_generation/specs/skill-a-pdf-generation-and-text-check.md`
- `srs_generation/specs/skill-a-review-and-gate.md`
- `srs_generation/specs/skill-a-scorecard.md`

需要补充：

```text
pdf_text_layer_gate
pdf_readability_gate
```

要求 Skill A 的 PDF 产物从“文本层可提取”升级为：

```text
文本层可提取 + 人类可读 + 样式参考原始 SRS v2
```

### 5.2 更新 PDF 检查报告模板

涉及文件：

- `srs_generation/templates/pdf-text-check-report.md`

需要补充检查项：

- 标题不重复
- 中英文混排正常
- 英文术语没有异常拆字
- 标题层级清晰
- 正文段落连续可读
- 页边距、行距、段落间距正常
- 页面无明显截断、溢出、乱码
- PDF 文本层可提取
- 提取文本中关键术语正常
- FR 编号、字段规则、异常处理、验收标准可搜索

### 5.3 修复 PDF 生成脚本

涉及文件：

- `srs_generation/scripts/generate_srs_pdf.py`

重点修复：

1. 标题重复问题。
2. 英文字母异常间距问题。
3. Markdown 标题层级丢失问题。
4. 正文排版过于简陋问题。
5. 字体不可用时静默生成低质量 PDF 的问题。

建议实现方向：

```text
优先使用 ReportLab 高质量排版
使用适合中英文混排的字体
直接解析 Markdown 标题层级
保留正文连续段落结构
内置 PDF writer 只作为兜底方案
```

标题策略建议：

```text
Markdown 控制正文标题
--title 优先作为 PDF metadata
不要重复渲染正文标题
```

字体策略建议：

```text
优先使用 Noto Sans CJK / 思源黑体 / 思源宋体 / 文泉驿等适合中英文混排的字体
若无法找到合适字体，可以生成兜底 PDF，但 pdf_readability_gate 不得直接判 pass
```

### 5.4 增强 PDF 检查脚本

涉及文件：

- `srs_generation/scripts/check_pdf_text_layer.py`

新增自动检查：

- 是否能提取文本
- 提取文本字符数是否合理
- 是否包含文档标题
- 是否包含 FR 编号
- 是否包含字段规则、异常处理、验收标准
- 是否存在标题重复
- 是否存在英文异常拆字模式，例如：

```text
R u o Y i
C o n t r o l l e r
S e r v i c e
F R - U S E R
```

自动检查不能完全替代人工检查。页边距、视觉层级、整体风格仍需要人工确认。

### 5.5 回归用户管理样本

涉及目录：

- `srs_generation/runs/ruoyi-vue-pro-user-management-20260604/skill-a/`

需要更新：

- `srs-kb-friendly.pdf`
- `pdf-text-check-report.md`
- `gate-result.md`

验收要求：

```text
标题不重复
RuoYi-Vue-Pro 正常显示
Controller / Service / VO / DO / Mapper 正常显示
FR-USER-001 正常显示
system:user:create 正常显示
GET /system/user/page 正常显示
标题层级清晰
正文段落自然换行
PDF 文本层仍可提取
整体阅读效果接近原始 SRS v2 的简洁风格
```

### 5.6 回归角色管理样本

涉及目录：

- `srs_generation/runs/ruoyi-vue-pro-role-management-20260604/skill-a/`

需要更新：

- `srs-kb-friendly.pdf`
- `pdf-text-check-report.md`
- `gate-result.md`

目标是确认修复不是只针对用户管理样本生效。

### 5.7 更新 handoff 包

涉及目录：

- `srs_generation/handoff/skill-a-before-skill-bc-20260604/`

需要更新：

- 用户管理 PDF
- 用户管理 PDF 检查报告
- 用户管理 gate 结果
- 角色管理 PDF
- 角色管理 PDF 检查报告
- 角色管理 gate 结果
- `handoff-summary.md`

确保交给 Skill B 的 PDF 是修复后的可读版本。

### 5.8 更新报告与总结

涉及文件：

- `srs_generation/current-work-summary.md`
- `srs_generation/reports/skill-a-before-skill-bc-final-report.md`
- `srs_generation/reports/skill-a-user-management-regression.md`
- `srs_generation/reports/skill-a-second-sample-validation.md`

需要把结论修正为：

```text
两个样本已通过内容 gate 和 PDF 文本层 gate；
补充 PDF 人类可读性 gate 后重新回归；
修复后的两个样本需要同时通过 pdf_text_layer_gate 和 pdf_readability_gate。
```

## 6. 推荐执行顺序

```text
1. 更新 PDF 质量标准
2. 更新 PDF 检查报告模板
3. 修复 generate_srs_pdf.py
4. 增强 check_pdf_text_layer.py
5. 重新生成用户管理 PDF
6. 对照原始 SRS v2 做人工可读性确认
7. 重新生成角色管理 PDF
8. 更新 handoff 包
9. 更新总结和最终报告
```

## 7. 最小修复闭环

如果先做最小闭环，建议只做：

```text
1. 更新 PDF 质量标准
2. 修复 PDF 生成脚本
3. 增强 PDF 检查脚本
4. 重新生成用户管理 PDF
5. 人工确认用户管理 PDF 可读性
```

用户管理样本确认通过后，再扩展到角色管理和 handoff 包。

## 8. Gate 标准

修复后 Skill A 的 PDF gate 应拆成两层：

```text
pdf_text_layer_gate = pass / fail
pdf_readability_gate = pass / fail
```

只有两者都为 `pass`，Skill A 才能认为 PDF 产物合格。

### 8.1 文本层 gate

检查项：

- [ ] PDF 可提取文本
- [ ] 提取文本字符数合理
- [ ] 包含标题
- [ ] 包含 FR 编号
- [ ] 包含字段规则、异常处理、验收标准
- [ ] 关键术语可搜索

### 8.2 可读性 gate

检查项：

- [ ] 标题不重复
- [ ] 中英文混排正常
- [ ] 英文术语没有异常拆字
- [ ] 标题层级清晰
- [ ] 正文段落连续可读
- [ ] 页边距、行距、段落间距正常
- [ ] 页面无明显截断、溢出、乱码
- [ ] 整体风格简洁正式，接近原始 SRS v2

## 9. 完成标准

本任务完成的标准是：

- [ ] Skill A PDF 质量标准已更新
- [ ] PDF 检查报告模板已更新
- [ ] PDF 生成脚本已修复标题、字体和层级问题
- [ ] PDF 检查脚本已能识别文本层和部分可读性问题
- [ ] 用户管理样本 PDF 重新生成并通过文本层 gate 与可读性 gate
- [ ] 角色管理样本 PDF 重新生成并通过文本层 gate 与可读性 gate
- [ ] handoff 包已替换为修复后的 PDF 和报告
- [ ] 当前总结与最终报告已更新

## 10. 当前状态

当前修复已完成：

- Skill A PDF 质量标准已更新。
- PDF 检查报告模板已更新。
- PDF 生成脚本已修复标题重复、英文异常拆字和标题层级弱化问题。
- PDF 生成脚本已按代码审查修复字体候选策略和内置 writer 英文 token 硬切问题。
- PDF 检查脚本已升级为同时输出文本层 gate 与可读性 gate。
- PDF 检查脚本已按代码审查修复标题识别、标题重复检测和英文异常拆字误报问题。
- 用户管理样本 PDF 已重新生成，并通过文本层 gate 与可读性 gate。
- 角色管理样本 PDF 已重新生成，并通过文本层 gate 与可读性 gate。
- handoff 包已替换为修复后的 PDF、检查报告和 gate 结果。
- 当前总结与最终报告已更新。

本任务完成后仍未进入 Skill B / Skill C，未创建 RAGFlow 知识库，未上传文档到外部系统。
