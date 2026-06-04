# 当前 SRS Skill 化工作总结

更新日期：2026-06-04  
当前分支：`srs-generation-skill-a-prep`

## 1. 当前总目标

本阶段目标是把已经跑通的“源码逆向生成 SRS → PDF → RAGFlow 验证 → TestHub 闭环”案例，沉淀为可复用的 Skill 能力链。

整体能力链拆分为：

```text
Skill A：源码逆向生成 SRS
Skill B：知识库构建与检索验证
Skill C：执行约束增强
总编排：ragflow-testhub-agent-workflow
```

本轮重点是完成 **进入 Skill B / Skill C 之前的 Skill A 最小可行版本**。

## 2. 当前阶段结论

当前已经完成到：

```text
Skill A spec
→ Skill A templates
→ Skill A prompts
→ PDF 生成与文本层检查脚本
→ 用户管理样本回归
→ 角色管理第二样本验证
→ Skill A handoff 包
→ 停在 Skill B/C 前
```

结论：

- Skill A 已经不只是讨论稿，已经形成可执行的规范、模板、prompt、脚本和两个验证样本。
- 用户管理样本和角色管理样本均已通过 Skill A gate。
- 两个样本 PDF 文本层检查均通过。
- 当前尚未进入 Skill B / Skill C。
- 当前没有创建 RAGFlow 知识库，没有上传文档，没有执行 retrieval gate，没有提炼执行约束。

## 3. 已完成的核心工作

### 3.1 任务体系拆解

已创建细粒度任务清单目录：

- `srs_generation/tasks/`

重点入口：

- `srs_generation/tasks/README.md`
- `srs_generation/tasks/00-implementation-roadmap.md`
- `srs_generation/tasks/19-task-index-by-priority.md`
- `srs_generation/tasks/26-minimum-viable-skill-a.md`
- `srs_generation/tasks/31-final-checklist-before-implementation.md`

### 3.2 Skill A 正式规范

已创建 Skill A 规范文件：

- `srs_generation/specs/skill-a-source-to-srs.md`
- `srs_generation/specs/skill-a-scope-confirmation.md`
- `srs_generation/specs/skill-a-source-evidence-map.md`
- `srs_generation/specs/skill-a-scorecard.md`
- `srs_generation/specs/skill-a-review-and-gate.md`
- `srs_generation/specs/skill-a-pdf-generation-and-text-check.md`

核心规则已定：

- Skill A 默认输出 `kb-friendly` SRS。
- `module_scope` 不再是必填输入，改为选填 `scope_hint`。
- Skill A 先自动推断 scope，再确认。
- 长程自主执行模式下，高置信 scope 可自动 confirmed；低置信项进入 risk_items；严重不清才 blocked。
- `source_evidence_map` 是强制产物。
- Skill A 只评估 SRS 文档质量，不评估 RAGFlow 检索效果。
- PDF 文本层不可提取是硬性 fail。
- 关键结论无法提供源码依据是硬性 fail 或人工复核触发项。

### 3.3 Skill A 模板

已创建模板：

- `srs_generation/templates/scope-confirmation.md`
- `srs_generation/templates/source-evidence-map.md`
- `srs_generation/templates/skill-a-scorecard.md`
- `srs_generation/templates/skill-a-review-gate.md`
- `srs_generation/templates/pdf-text-check-report.md`

### 3.4 Skill A Prompts

已创建 Skill A prompt 文件：

- `srs_generation/prompts/skill-a/skill-a-controller.md`
- `srs_generation/prompts/skill-a/scope-inference.md`
- `srs_generation/prompts/skill-a/source-fact-extraction.md`
- `srs_generation/prompts/skill-a/source-evidence-map.md`
- `srs_generation/prompts/skill-a/srs-draft-generation.md`
- `srs_generation/prompts/skill-a/srs-kb-friendly-rewrite.md`
- `srs_generation/prompts/skill-a/srs-aligned-rewrite.md`
- `srs_generation/prompts/skill-a/self-review.md`
- `srs_generation/prompts/skill-a/independent-review.md`

同时创建了 B/C/总编排 prompt 占位目录，但未进入 B/C 实施：

- `srs_generation/prompts/skill-b/.gitkeep`
- `srs_generation/prompts/skill-c/.gitkeep`
- `srs_generation/prompts/orchestration/.gitkeep`

### 3.5 PDF 生成与文本层检查脚本

已创建脚本：

- `srs_generation/scripts/generate_srs_pdf.py`
- `srs_generation/scripts/check_pdf_text_layer.py`
- `srs_generation/scripts/README.md`

脚本特点：

- `generate_srs_pdf.py` 优先使用 `reportlab`；若当前 Python 环境缺少 `reportlab`，会使用内置 PDF writer 生成带文本层的 PDF。
- `check_pdf_text_layer.py` 优先使用 `pypdf` / `PyPDF2`；若当前 Python 环境缺少依赖，会使用内置提取逻辑检查文本层。
- 已通过最小中文 smoke test。
- 已通过用户管理和角色管理两个样本的 PDF 文本层检查。

## 4. 验证样本

### 4.1 样本一：RuoYi-Vue-Pro 用户管理

源码路径：

```text
g:/work/genlot/projects/ruoyi-vue-pro
```

目标模块：

```text
system user management
```

运行目录：

- `srs_generation/runs/ruoyi-vue-pro-user-management-20260604/skill-a/`

结果：

```text
scope_confirm_status: confirmed
pdf_text_check: pass
gate: pass
```

主要产物：

- `srs_generation/runs/ruoyi-vue-pro-user-management-20260604/skill-a/srs-kb-friendly.md`
- `srs_generation/runs/ruoyi-vue-pro-user-management-20260604/skill-a/srs-kb-friendly.pdf`
- `srs_generation/runs/ruoyi-vue-pro-user-management-20260604/skill-a/source-evidence-map.md`
- `srs_generation/runs/ruoyi-vue-pro-user-management-20260604/skill-a/pdf-text-check-report.md`
- `srs_generation/runs/ruoyi-vue-pro-user-management-20260604/skill-a/independent-review-report.md`
- `srs_generation/runs/ruoyi-vue-pro-user-management-20260604/skill-a/gate-result.md`

报告：

- `srs_generation/reports/skill-a-user-management-regression.md`

### 4.2 样本二：RuoYi-Vue-Pro 角色管理

选择原因：

- 与用户管理同属 RuoYi-Vue-Pro，降低跨项目变量。
- 业务结构不同，覆盖角色唯一性、超级管理员标识保护、系统内置角色保护、删除后权限关联清理等规则。
- 验证 Skill A 不只适配用户管理案例。

目标模块：

```text
system role management
```

运行目录：

- `srs_generation/runs/ruoyi-vue-pro-role-management-20260604/skill-a/`

结果：

```text
scope_confirm_status: confirmed
pdf_text_check: pass
gate: pass
```

主要产物：

- `srs_generation/runs/ruoyi-vue-pro-role-management-20260604/skill-a/srs-kb-friendly.md`
- `srs_generation/runs/ruoyi-vue-pro-role-management-20260604/skill-a/srs-kb-friendly.pdf`
- `srs_generation/runs/ruoyi-vue-pro-role-management-20260604/skill-a/source-evidence-map.md`
- `srs_generation/runs/ruoyi-vue-pro-role-management-20260604/skill-a/pdf-text-check-report.md`
- `srs_generation/runs/ruoyi-vue-pro-role-management-20260604/skill-a/independent-review-report.md`
- `srs_generation/runs/ruoyi-vue-pro-role-management-20260604/skill-a/gate-result.md`

报告：

- `srs_generation/reports/skill-a-second-sample-validation.md`

## 5. Skill A Handoff 包

已打包进入 Skill B/C 前的 handoff：

- `srs_generation/handoff/skill-a-before-skill-bc-20260604/`

入口文件：

- `srs_generation/handoff/skill-a-before-skill-bc-20260604/handoff-summary.md`

handoff 包包含：

### 用户管理

- `user-management-srs-kb-friendly.md`
- `user-management-srs-kb-friendly.pdf`
- `user-management-source-evidence-map.md`
- `user-management-pdf-text-check-report.md`
- `user-management-independent-review-report.md`
- `user-management-gate-result.md`

### 角色管理

- `role-management-srs-kb-friendly.md`
- `role-management-srs-kb-friendly.pdf`
- `role-management-source-evidence-map.md`
- `role-management-pdf-text-check-report.md`
- `role-management-independent-review-report.md`
- `role-management-gate-result.md`

最终报告：

- `srs_generation/reports/skill-a-before-skill-bc-final-report.md`

## 6. 进入 Skill B 前的状态

进入 Skill B 的前置条件已满足：

- Skill A prompt 已可执行。
- 至少两个样本验证通过。
- 两个样本均生成 `kb-friendly` SRS。
- 两个样本均生成 PDF。
- 两个样本 PDF 文本层检查均为 pass。
- 两个样本均有 `source_evidence_map`。
- 两个样本均有 `independent_review_report`。
- 两个样本 gate 均为 pass。

但当前仍按授权停在 Skill B/C 之前。

## 7. 尚未执行的事项

未执行：

- 未创建 RAGFlow 知识库。
- 未上传 SRS PDF 到外部系统。
- 未执行 RAGFlow chunk 质量评估。
- 未执行 retrieval sanity check。
- 未执行 retrieval gate。
- 未提炼 Skill C 执行约束。
- 未操作 TestHub 自动化闭环。

## 8. 新会话恢复建议

新会话建议先读取：

1. `srs_generation/current-work-summary.md`
2. `srs_generation/handoff/skill-a-before-skill-bc-20260604/handoff-summary.md`
3. `srs_generation/reports/skill-a-before-skill-bc-final-report.md`
4. `srs_generation/specs/skill-a-source-to-srs.md`
5. `srs_generation/tasks/19-task-index-by-priority.md`

如果继续推进，应从 Skill B 开始，而不是重新做 Skill A：

```text
Skill B spec
→ RAGFlow 建库计划
→ 外部系统操作前用户确认
→ chunk 质量检查
→ retrieval sanity check
→ retrieval gate
→ 通过后再进入 Skill C
```

Skill C 建议在 Skill B 通过后启动，避免把执行约束混入纯 SRS 知识库。

## 9. 当前一句话总结

当前已完成：**Skill A 从规范、模板、prompt、PDF 脚本到两个样本验证和 handoff 包的完整落地，两个样本均 gate=pass，并已按要求停在 Skill B/C 之前。**
