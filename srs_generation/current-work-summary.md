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
→ PDF 生成、文本层检查与可读性 gate 脚本
→ 用户管理样本回归
→ 角色管理第二样本验证
→ Skill A handoff 包
→ 停在 Skill B/C 前
```

结论：

- Skill A 已经不只是讨论稿，已经形成可执行的规范、模板、prompt、脚本和两个验证样本。
- 用户管理样本和角色管理样本均已通过 Skill A gate。
- 两个样本 PDF 文本层 gate 和可读性 gate 均通过。
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
- PDF 可读性 gate fail 是硬性 fail；Skill A PDF 产物必须同时满足知识库友好和人类可读。
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

### 3.5 PDF 生成、文本层检查与可读性 gate 脚本

已创建脚本：

- `srs_generation/scripts/generate_srs_pdf.py`
- `srs_generation/scripts/check_pdf_text_layer.py`
- `srs_generation/scripts/README.md`

脚本特点：

- `generate_srs_pdf.py` 优先使用 `reportlab` 和适合中英文混排的 CJK 字体，修复标题重复、英文异常拆字和标题层级弱化问题；若当前 Python 环境缺少 `reportlab`，会使用内置 PDF writer 生成带文本层的兜底 PDF。
- `generate_srs_pdf.py` 已按代码审查修复字体候选策略和内置 writer 英文 token 硬切问题。
- `check_pdf_text_layer.py` 优先使用 `pypdf` / `PyPDF2`；若当前 Python 环境缺少依赖，会使用内置提取逻辑检查文本层。
- `check_pdf_text_layer.py` 已升级为同时输出 `pdf_text_layer_gate` 和 `pdf_readability_gate`，并按代码审查修复标题识别、标题重复检测和英文异常拆字误报问题。
- 已通过最小中文 smoke test。
- 已通过用户管理和角色管理两个样本的 PDF 文本层 gate 与可读性 gate。

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
pdf_text_layer_gate: pass
pdf_readability_gate: pass
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
pdf_text_layer_gate: pass
pdf_readability_gate: pass
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

## 6. Source-to-SRS Claude Skill 包装状态

已将 Skill A 包装为完整可移植 Claude skill：

```text
skill name: source-to-srs
skill path: /root/.claude/skills/source-to-srs/
```

该 skill 包包含：

- `SKILL.md`
- `references/`：Skill A 规范文件
- `templates/`：输出模板
- `prompts/`：执行 prompts
- `scripts/`：PDF 生成与 PDF 质量检查脚本

已完成检查：

- Claude Code 已识别 `source-to-srs` 为可用 skill。
- skill 包内 Python 脚本已通过 `py_compile` 语法检查。
- 当前版本采用完整可移植方案，不依赖当前项目目录下的脚本才能使用。

## 7. 进入 Skill B 前的状态

进入 Skill B 的前置条件已满足：

- Skill A prompt 已可执行。
- 至少两个样本验证通过。
- 两个样本均生成 `kb-friendly` SRS。
- 两个样本均生成 PDF。
- 两个样本 PDF 文本层 gate 均为 pass。
- 两个样本 PDF 可读性 gate 均为 pass。
- 两个样本均有 `source_evidence_map`。
- 两个样本均有 `independent_review_report`。
- 两个样本 gate 均为 pass。

但当前仍按授权停在 Skill B/C 之前。

## 8. 尚未执行的事项

未执行：

- 未创建 RAGFlow 知识库。
- 未上传 SRS PDF 到外部系统。
- 未执行 RAGFlow chunk 质量评估。
- 未执行 retrieval sanity check。
- 未执行 retrieval gate。
- 未提炼 Skill C 执行约束。
- 未操作 TestHub 自动化闭环。

## 9. 新会话恢复建议

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

## 10. 当前一句话总结

当前已完成：**Skill A 从规范、模板、prompt、PDF 脚本到两个样本验证和 handoff 包的完整落地，已修复 PDF 标题重复、英文异常拆字和标题层级弱化问题；两个样本均通过 PDF 文本层 gate、PDF 可读性 gate 和 Skill A gate；并已包装为可移植 Claude skill `source-to-srs`，按要求停在 Skill B/C 之前。**

## 11. 2026-06-04 当日补充（新设备恢复用）

### 11.1 已推到远程的最新状态

- 当前分支：`srs-generation-skill-a-prep`
- 远程分支：`origin/srs-generation-skill-a-prep`
- 最新提交：`5736093`
- commit message：`docs: 完善 Skill A PDF 可读性 gate`

### 11.2 本次提交覆盖内容

- 已完成 Skill A PDF 生成、文本层检查与可读性 gate 升级。
- `generate_srs_pdf.py` 已修复标题重复、英文异常拆字、标题层级弱化，并补强字体候选策略和内置 writer 的英文 token 处理。
- `check_pdf_text_layer.py` 已升级为同时输出 `pdf_text_layer_gate` 与 `pdf_readability_gate`，并修复标题识别、标题重复检测和英文异常拆字误报问题。
- 用户管理、角色管理两个样本的 PDF、检查报告、gate-result、handoff 包与总结报告均已完成回归更新。
- 当前仍停在 Skill B / Skill C 之前，未执行任何外部系统操作。

### 11.3 当前未提交 / 未处理项

- 工作区仍有未跟踪文件 `ragflow-testhub-autotest-roadmap.md`，未纳入上述 commit，也未推送到远程。
- `source-to-srs` 关于“非研发可读性不足、正文混入过多实现细节”的修复清单已讨论完成，但尚未正式落盘实施。

### 11.4 新设备恢复最短路径

在新设备上建议先执行：

```bash
git fetch origin
git checkout srs-generation-skill-a-prep
git pull
```

然后按顺序优先读取：

1. `srs_generation/current-work-summary.md`
2. `srs_generation/handoff/skill-a-before-skill-bc-20260604/handoff-summary.md`
3. `srs_generation/reports/skill-a-before-skill-bc-final-report.md`
4. `srs_generation/tasks/36-skill-a-pdf-readability-fix.md`
5. `srs_generation/specs/skill-a-pdf-generation-and-text-check.md`

如果下一步继续的是“Skill 本身修复”，而不是进入 Skill B，则额外读取：

- `srs_generation/prompts/skill-a/srs-kb-friendly-rewrite.md`
- `srs_generation/prompts/skill-a/independent-review.md`
- `srs_generation/specs/skill-a-review-and-gate.md`
- `docs/ruoyi-user-management-srs-v2.pdf`

其中 `docs/ruoyi-user-management-srs-v2.pdf` 只参考格式和描述方式，不要求参照其具体内容。

### 11.5 当前下一步建议

当前下一步更像是修 Skill A 的“产物把控”，而不是继续修 PDF 脚本。

建议优先处理：

1. 强化 `srs-kb-friendly` 改写约束，明确主文档默认面向业务、产品、测试和知识库使用者。
2. 明确 `@PreAuthorize`、接口路径、类名、方法名、权限码等实现细节默认不进入正文，而下沉到 `source-evidence-map` 或追溯说明。
3. 在独立评审与 gate 中新增“非研发可读性”检查，避免正文虽然事实正确，但仍像技术实现说明。

这一轮修复尚未开始实施；如继续推进，建议先做 prompt / review / gate 三处约束收紧，再决定是否需要补充产物结构调整。

## 12. 2026-06-07 补充：source-to-srs 非研发可读性优化

### 12.1 当前本地最新提交

- 当前分支：`srs-generation-skill-a-prep`
- 最新本地提交：`619a188`
- commit message：`docs: 优化 source-to-srs 非研发可读性约束`
- 该提交尚未在本节记录时确认推送远程。

### 12.2 本次优化目标

本轮优化针对可移植 Claude skill `source-to-srs`，重点解决：

- 主 SRS 正文混入过多实现细节，导致非研发读者阅读困难。
- 权限码、接口路径、注解名、类名/方法名等技术细节进入正文主体。
- 独立评审和 gate 过去更偏向判断“事实是否正确”，对“需求表达是否业务可读”的约束不足。

优化目标不是删除技术追溯，而是分层：

```text
主文档正文：业务语义、系统行为、需求规则
source-evidence-map.md：接口路径、权限码、注解、类名/方法名等源码依据
```

### 12.3 已完成的 repo 内改动

已收紧以下 Skill A 规范和 prompt：

- `srs_generation/prompts/skill-a/srs-kb-friendly-rewrite.md`
  - 明确主文档默认面向业务、产品、测试设计人员和知识库使用者。
  - 要求正文优先使用业务语义和系统行为描述。
  - 将“源码依据说明”改为“需求追溯说明”。
  - 要求技术细节下沉到 `source-evidence-map.md`。
  - 禁止在主文档正文中直接堆砌 `@PreAuthorize`、接口路径、控制器方法名、DTO/VO/Entity 类名和权限码。

- `srs_generation/prompts/skill-a/independent-review.md`
  - 新增非研发可读性检查。
  - 要求识别正文技术细节污染。
  - 明确正文混入较多实现细节时至少应记为 required fix。
  - 补齐 `PDF 可读性 gate fail` 为硬性不合格项。

- `srs_generation/specs/skill-a-review-and-gate.md`
  - `pass` 条件新增：正文以业务语义为主、非研发可读、技术追溯不侵入主体。
  - `conditional pass` 触发条件新增：正文混入较多实现细节或技术追溯未充分下沉。
  - “不得进入 Skill B”条件补齐 `PDF 可读性 gate fail`。

- `srs_generation/specs/skill-a-scorecard.md`
  - “需求表达质量”评分纳入非研发可读性和技术细节污染。

- `srs_generation/prompts/skill-a/skill-a-controller.md`
- `srs_generation/specs/skill-a-source-evidence-map.md`
- `srs_generation/specs/skill-a-source-to-srs.md`
  - 统一 `source_evidence_map` / `source-evidence-map.md` 口径。
  - 具体文件统一写为 `source-evidence-map.md`，概念表述为“源码依据映射文件”。

### 12.4 已同步 portable skill

同类改动已同步到实际可调用的 portable skill：

```text
/root/.claude/skills/source-to-srs/
```

涉及：

- `prompts/srs-kb-friendly-rewrite.md`
- `prompts/independent-review.md`
- `prompts/skill-a-controller.md`
- `references/skill-a-review-and-gate.md`
- `references/skill-a-scorecard.md`
- `references/skill-a-source-evidence-map.md`
- `references/skill-a-source-to-srs.md`

### 12.5 已完成的验证 run

为验证本轮优化效果，新增三组 Skill A 验证产物：

#### 用户管理回归验证

目录：

- `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-a/`

结果：

```text
gate: pass
pdf_text_layer_gate: pass
pdf_readability_gate: pass
```

结论：主文档更偏业务表达，技术细节主要下沉到 `source-evidence-map.md`。

#### ERP 仓库管理验证

目录：

- `srs_generation/runs/ruoyi-vue-pro-erp-warehouse-validation-20260607/skill-a/`

结果：

```text
gate: pass
pdf_text_layer_gate: pass
pdf_readability_gate: pass
independent_review: pass, 24/25
```

结论：正文未明显泄漏 `@PreAuthorize`、接口路径、类名/方法名、原始权限码；技术依据主要进入 `source-evidence-map.md`。

#### MES 盘点任务验证

目录：

- `srs_generation/runs/ruoyi-vue-pro-mes-stocktaking-task-validation-20260607/skill-a/`

结果：

```text
gate: pass
pdf_text_layer_gate: pass
pdf_readability_gate: pass
risk-items.md: generated
```

结论：复杂业务规则模块下，可读性优化仍生效；盘点差异 `count` 正负业务口径风险被显式记录，没有被强行写死为确定需求。

### 12.6 当前工作区注意事项

- 用户已自行删除已跟踪文件 `ragflow-testhub-minimal-flow-handoff.md`；该删除不属于 `619a188` 提交内容。
- 该删除是否最终提交，需由用户单独决定。
- 当前 `source-to-srs` 优化已完成本地提交，但本节记录时尚未确认是否推送远程。

### 12.7 下一步建议

建议下一步先处理工作区状态：

1. 确认是否提交或保留 `ragflow-testhub-minimal-flow-handoff.md` 的删除。
2. 将本总结文件更新单独提交。
3. 如需远程同步，再推送当前分支。
4. 之后再决定是否进入 Skill B，或继续追加更多 `source-to-srs` 验证样本。

## 13. 2026-06-08 补充：Skill B Offline 设计骨架

### 13.1 当前本地最新提交

- 当前分支：`srs-generation-skill-a-prep`
- 最新本地提交：`b29b579`
- commit message：`docs: 初始化 Skill B offline 设计骨架`
- 本节记录时尚未确认是否推送远程。

### 13.2 当前背景约束

- 当前没有可用 RAGFlow 供访问。
- Skill B 当前不做真实建库、真实 parser、真实 chunk 检查、真实 retrieval sanity check。
- 当前阶段先推进 **Skill B Offline MVP**，把输入契约、输出契约、问题集与 blocked 语义落盘。

### 13.3 已确认的 Skill B 能力边界

Skill B 当前边界已确认：

- 负责：知识库创建/复用计划、解析配置计划、retrieval 问题集生成、离线可检索性预检、offline_readiness_gate、online_retrieval_gate blocked 语义、handoff 打包。
- 不负责：生成或修改 SRS、生成 TestHub scenario JSON、执行 TestHub、失败诊断、替业务裁决不确定规则、伪造真实 RAGFlow 结果。

### 13.4 已确认的输入与上传策略

当前口径：

```text
主分析输入 / 主上传候选：srs-kb-friendly.md
必填分析输入 / 默认不上传：source-evidence-map.md
参考输入 / 默认不上传：srs-kb-friendly.pdf
```

补充说明：

- `source-evidence-map.md` 是 Skill B 的必填分析输入，用于辅助追溯、风险判断和问题集补强，但不默认上传到主 RAGFlow SRS 知识库。
- `srs-kb-friendly.pdf` 用于正式交付阅读、PDF gate 证明和未来 parser / retrieval 对比实验，不是当前 Offline MVP 的主分析输入。
- 若后续要比较 Markdown / PDF 的建库效果，应通过独立实验执行，而不是先把二者上传到同一个主知识库。

### 13.5 已落盘的 Skill B Offline 文件

#### spec

- `srs_generation/specs/skill-b-knowledge-base-and-retrieval.md`

#### templates

- `srs_generation/templates/skill-b-input-snapshot.md`
- `srs_generation/templates/kb-plan.md`
- `srs_generation/templates/parse-config-plan.md`
- `srs_generation/templates/retrieval-question-set.md`
- `srs_generation/templates/offline-retrieval-readiness-report.md`
- `srs_generation/templates/retrieval-gate-result.md`
- `srs_generation/templates/skill-b-handoff.md`

#### prompts

- `srs_generation/prompts/skill-b/skill-b-controller.md`
- `srs_generation/prompts/skill-b/retrieval-question-generation.md`
- `srs_generation/prompts/skill-b/offline-readiness-review.md`
- `srs_generation/prompts/skill-b/retrieval-gate.md`

### 13.6 Gate 语义

当前已明确：

```text
offline_readiness_gate: pass | conditional pass | fail
online_retrieval_gate: blocked | pass | conditional pass | fail
```

当真实 RAGFlow 不可用时，必须输出：

```text
online_retrieval_gate: blocked
blocked_reason: RAGFlow unavailable
```

不得伪造：

- `dataset_id`
- `chunk_count`
- 真实 retrieval 命中结果
- `online_retrieval_gate = pass`

### 13.7 首个离线样例选择

已确认首个 Skill B Offline 样例使用：

- `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-a/`

建议输出目录：

- `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-b-offline/`

选择原因：

- 用户管理样本最成熟，历史上下文最完整。
- 已通过 Skill A 非研发可读性优化验证。
- 适合作为 Skill B Offline 首个结构样例。

### 13.8 当前停留点

当前已经完成：

- Skill B Offline spec
- Skill B Offline templates
- Skill B Offline prompts

当前尚未执行：

- 尚未运行首个 `skill-b-offline` 样例
- 尚未生成 `ruoyi-vue-pro-user-management-20260606-validation/skill-b-offline/` 产物
- 尚未决定是否将 `b29b579` 推送远程

### 13.9 下一步建议

建议下一步按以下顺序推进：

1. 将本总结补充单独提交。
2. 如需远程同步，推送当前分支。
3. 基于用户管理样例运行首个 `skill-b-offline` 样例。
4. 检查问题集、offline-readiness-report、retrieval-gate-result 和 handoff 是否满足预期。
5. 样例通过后，再决定是否扩展到 ERP 仓库管理和 MES 盘点任务的 `skill-b-offline` 样例。

## 14. 2026-06-08 补充：Skill B Hybrid MVP 与首个 online 验证

### 14.1 当前方向变化

由于当前已恢复对 RAGFlow 的访问，Skill B 目标已从原先的 **Offline MVP** 调整为 **Hybrid MVP**：

```text
先完成离线准备度验证
再在 RAGFlow 可访问且用户确认后执行最小真实 online 验证
```

已完成的 repo 内语义收敛包括：

- `srs_generation/specs/skill-b-knowledge-base-and-retrieval.md`
- `srs_generation/prompts/skill-b/skill-b-controller.md`
- `srs_generation/prompts/skill-b/offline-readiness-review.md`
- `srs_generation/prompts/skill-b/retrieval-gate.md`
- `srs_generation/templates/retrieval-gate-result.md`
- `srs_generation/templates/skill-b-handoff.md`

收敛内容包括：

- `online_retrieval_gate` 不再默认写死为 `blocked`。
- 新增 `blocked_reason = RAGFlow unavailable | external action not approved | online step not executed yet` 语义。
- `allowed_next_stage` 从“等 RAGFlow”扩展为可进入 `request_online_execution | skill_c | orchestration | manual_fix`。
- `skill_c` 与 `orchestration` 的职责边界已在 gate 模板中补充说明。

### 14.2 用户管理样例的三次 online 尝试

首个 online 样例仍使用：

- `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-a/`

#### 尝试一：Markdown 直传

上传材料：

- `srs-kb-friendly.md`

结果：

```text
online_retrieval_gate: blocked
```

原因：

- 当前 RAGFlow 环境不支持 `.md` 作为可解析文档类型。
- 上传成功，但解析失败，无法生成 chunks。

#### 尝试二：PDF 上传

上传材料：

- `srs-kb-friendly.pdf`

结果：

```text
解析成功，但不接受为主 handoff 结果
```

原因：

- 虽完成 OCR、布局分析、切块与嵌入，但人工抽检发现存在“相邻章节标题串接、正文内容丢失”的结构性问题。
- 示例现象：两个 FR 标题被串成一个 chunk，而中间正文未被稳定挂接。
- 因此 PDF 方案不能视为当前可接受的主知识库载体。

#### 尝试三：TXT 临时载体上传

上传材料：

- `/tmp/ruoyi-pro-user-management-srs-20260608.txt`
- 该文件由 `srs-kb-friendly.md` 临时转出，仅用于 RAGFlow online 验证，不写回仓库。

结果：

```text
online_retrieval_gate: conditional pass
skill_b_status: online_verified_with_risks
```

实际结果：

- dataset 名称：`ruoyi-pro-user-management-srs-txt-20260608`
- `SRS_KB_ID = 00c0dbdc632111f18243434b552cc465`
- `document_id = 00c783a6632111f18243434b552cc465`
- parse status：`DONE`
- `chunk_method = book`
- `chunk_count = 37`

### 14.3 TXT 方案相对 PDF 的结论

TXT 方案明显优于 PDF 方案：

- 未再出现“只有标题、没有正文”的孤立短块。
- 未再出现明显“相邻 FR 标题串接、正文丢失”的结构问题。
- 多数 chunk 形态为“章节标题 + 完整规则/需求句”。

仍存在的轻度噪声：

- 顶层文档标题会重复进入多个 chunk。
- 该问题不阻断当前业务型检索使用，但建议下游 retrieval 至少查看 top 3，而不是只依赖 top 1。

### 14.4 Retrieval sanity check 结果

TXT 方案下，6 道检索题结果为：

```text
5 命中
1 弱命中
0 未命中
```

命中类型覆盖：

- 功能需求问题
- 规则类问题
- 异常/边界问题

弱命中问题为：

- 源码证据追溯题

原因：

- 当前主知识库只上传了 SRS TXT 载体，未上传 `source-evidence-map.md`。
- 因此当前知识库只能稳定回答“证据已下沉到 source-evidence-map.md”这一说明层，不能直接返回更细的 controller / service / permission 明细。

### 14.5 当前 handoff 结论

当前建议以 TXT 方案作为用户管理样例的主 Skill B handoff：

- `PROJECT_NAME = ruoyi-pro`
- `BUSINESS_DOMAIN = user management`
- `TEST_SCOPE = 用户新增、编辑、启停用、唯一性校验、权限约束、异常提示`
- `MIN_BUSINESS_FLOW = 查询用户列表 → 新增用户 → 编辑用户 → 禁用用户`
- `SRS_KB_ID = 00c0dbdc632111f18243434b552cc465`
- `API_DOCS_KB_ID =`
- `KNOWN_CAVEATS = 证据追溯仅弱命中到 SRS 说明层，未覆盖 evidence map 细粒度源码证据`

对应样例级产物已补充到：

- `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-b/retrieval-gate-result.md`
- `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-b/skill-b-handoff.md`

### 14.6 当前一句话判断

当前用户管理样例已经完成 Skill B Hybrid MVP 的首个真实 online 验证；其中 Markdown 在当前环境不可解析，PDF 可解析但结构不可靠，TXT 临时载体在 `book` 模式下得到稳定得多的 chunk 与检索结果，因此当前主 handoff 应采用 TXT 方案生成的 `SRS_KB_ID`，并在后续进入 Skill C 时明确：业务检索可依赖当前 SRS_KB，源码级证据追溯仍需借助 `source-evidence-map.md` 或未来独立 evidence KB。
