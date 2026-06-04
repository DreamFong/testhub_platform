# 术语表

## Skill A

源码逆向生成 SRS 的能力层。负责从源码抽取需求事实，生成 SRS Markdown / PDF，并完成文档质量评审。

## Skill B

知识库构建与检索验证能力层。负责将 SRS 等文档导入 RAGFlow，检查 chunk 质量并执行 retrieval gate。

## Skill C

执行约束增强能力层。负责从真实跑通案例中提炼 token、ID、body、headers、错误字段黑名单等自动化执行约束。

## ragflow-testhub-agent-workflow

最终总编排 Skill。负责串联 Skill A、Skill B、Skill C，并输出 TestHub 可消费的 handoff。

## kb-friendly

知识库友好版 SRS。默认输出模式，强调连续段落、标题稳定、低表格依赖、适合文本提取和检索。

## aligned

对齐历史 SRS 风格版。可选输出模式，强调章节风格和表达方式与历史文档接近，但不得覆盖源码事实。

## scope_hint

用户提供的范围提示。它是选填输入，用于辅助 Skill A 推断范围，不是事实来源。

## scope confirm

Skill A 正式生成前的范围确认机制。Skill A 先自动推断候选范围，再交由用户确认。

## source_evidence_map

源码依据清单。用于记录 SRS 中功能、字段、规则、权限、异常和验收标准对应的源码依据。

## self_review_report

生成 Agent 对自己产物的自评分报告。只作为参考，不能作为最终通过依据。

## independent_review_report

独立评审 Agent 的正式评审报告。作为默认机器主评分来源。

## conditional pass

有条件通过。表示没有致命问题，但存在必须修改项，修正后可进入下一阶段。

## retrieval gate

检索质量门禁。用于判断知识库是否能够稳定回答功能、字段、权限、异常和验收标准相关问题。

## execution constraints

执行约束。指自动化执行所需但纯需求文档通常不包含的规则，如 token 提取、ID 提取、最小 body、headers、错误字段黑名单。

## handoff

阶段交接物。用于把一个 Skill 的结果稳定传递给下一个 Skill 或 TestHub。
