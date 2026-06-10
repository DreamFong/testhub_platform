---
name: source-to-srs
description: 从项目源码逆向生成知识库友好且人类可读的 SRS，并输出 Markdown、PDF、源码依据映射、PDF 文本层与可读性检查、三阶段评分和 gate 结果。Use this skill when the user wants to generate or regenerate SRS/PRD/requirements documents from source code, analyze a module's implemented behavior into requirements, create a RAGFlow-friendly SRS before knowledge base creation, or prepare a source-derived SRS handoff for RAGFlow/TestHub workflows.
---

# Source to SRS

Use this skill to turn a source-code module into a verified SRS package:

```text
project source code
→ scope inference and confirmation
→ source fact extraction
→ source evidence map
→ factual SRS draft
→ knowledge-base-friendly SRS
→ readable text-layer PDF
→ PDF text-layer and readability gate
→ self review
→ independent review
→ gate result
→ handoff package for downstream knowledge-base work
```

This skill is the portable version of Skill A: 源码逆向生成 SRS.

## When to use

Use this skill when the user wants to:

- 从源码逆向生成 SRS、PRD 或需求规格说明。
- 把已经实现的模块整理成可读、可审查、可进入知识库的需求文档。
- 为 RAGFlow 知识库准备业务需求输入文档。
- 生成知识库友好版 SRS PDF，并检查文本层和人类可读性。
- 建立从源码事实到 SRS 结论的 evidence map。
- 在进入 RAGFlow / TestHub 前，对源码生成的 SRS 做质量门禁。

## When not to use

Do not use this skill for:

- 创建 RAGFlow 知识库。
- 上传文档到 RAGFlow 或其他外部系统。
- 执行 chunk 质量评估、检索准确率、召回率或 retrieval gate。
- 生成 TestHub 场景 JSON。
- 执行 API 测试或 UI 自动化测试。
- 提炼 token、变量提取、最小 body、headers 或执行约束。

Those belong to downstream skills such as `ragflow-knowledge-base-builder`, execution-constraint work, or `ragflow-testhub-agent-workflow`.

## Required inputs

Ask for missing values before starting unless the user explicitly authorizes autonomous inference.

```text
source_project       — source repository path
project_name         — project display name
target_module        — required target business/module name
scope_hint           — optional module/function hint; if missing, infer scope from source
output_run_dir       — where to write the run artifacts
reference_srs        — optional existing SRS/PDF used as style or acceptance reference
output_mode          — default: kb-friendly; optional: aligned
language             — output language; default should follow user/project preference
```

`target_module` is the required scope anchor. `module_scope` is not a required input. Prefer `scope_hint` only as a hint, then infer and confirm the actual scope from source.

## Outputs

A complete run should produce:

```text
input-snapshot.md
scope-inference.md
scope-confirmation.md
source-facts.md
source-evidence-map.md
srs-factual-draft.md
srs-kb-friendly.md
srs-kb-friendly.pdf
pdf-text-check-report.md
self-review-report.md
independent-review-report.md
gate-result.md
```

Optional outputs:

```text
srs-aligned.md
srs-aligned.pdf
risk-items.md
handoff-summary.md
```

## Recommended output layout

Use a stable per-run directory:

```text
srs_generation/runs/<project>-<module>-<date>/skill-a/
```

For a handoff package:

```text
srs_generation/handoff/<handoff-id>/
```

## Workflow

### 1. Capture input snapshot

Record the user's inputs, source path, scope hint, date, assumptions, and any reference SRS.

Output:

```text
input-snapshot.md
```

### 2. Infer and confirm scope

Use `prompts/scope-inference.md` and `templates/scope-confirmation.md`.

The scope result should be one of:

```text
confirmed
risk_items
blocked
```

High-confidence scope can be auto-confirmed in autonomous mode. Serious ambiguity must block execution and ask the user.

### 3. Extract source facts

Use `prompts/source-fact-extraction.md`.

Read the relevant source code such as:

```text
Controller / routes
Service / business logic
VO / DTO / request / response types
Entity / DO / models
Mapper / repository / SQL
error codes
permission annotations or configuration
frontend pages and API calls when relevant
```

Output factual notes only; do not write polished SRS text yet.

### 4. Build source evidence map

Use `prompts/source-evidence-map.md` and `templates/source-evidence-map.md`.

This is mandatory. Key requirements, field rules, business rules, permission rules, error handling, and acceptance criteria must be traceable to source evidence.

If a key conclusion has no evidence, treat it as a hard fail or manual-review trigger.

### 5. Generate factual SRS draft

Use `prompts/srs-draft-generation.md`.

The factual draft should prioritize completeness and source accuracy over style.

### 6. Rewrite to knowledge-base-friendly SRS

Use `prompts/srs-kb-friendly-rewrite.md`.

Default output is `srs-kb-friendly.md`.

Requirements:

- Use stable headings.
- Use stable FR IDs.
- Prefer continuous paragraphs over complex tables.
- Keep field rules, business rules, error handling, permission rules, and acceptance criteria explicit.
- Keep rules close to the relevant feature when helpful.
- Avoid fragmenting important constraints into tiny list-only sections.

### 7. Optional aligned rewrite

Use `prompts/srs-aligned-rewrite.md` only when the user wants a version closer to an existing SRS style.

`aligned` is not the default. It is for historical style comparison, not for the default downstream knowledge-base input.

### 8. Generate readable text-layer PDF

Use the bundled script:

```bash
python <skill_dir>/scripts/generate_srs_pdf.py \
  --input <run_dir>/srs-kb-friendly.md \
  --output <run_dir>/srs-kb-friendly.pdf \
  --title "<Project Module SRS>"
```

PDF requirements:

- Text layer must be extractable.
- PDF must be human-readable.
- Title must not be duplicated.
- English terms must not be rendered as separated letters.
- Heading hierarchy must be visible.
- Overall style should be simple, clean, and close to the confirmed reference SRS style when one exists.

### 9. Check PDF text layer and readability

Use the bundled script:

```bash
python <skill_dir>/scripts/check_pdf_text_layer.py \
  --pdf <run_dir>/srs-kb-friendly.pdf \
  --report <run_dir>/pdf-text-check-report.md \
  --key-term 字段 \
  --key-term 异常 \
  --key-term 验收标准 \
  --manual-readability pass
```

The script outputs:

```text
pdf_text_layer_gate: pass | conditional pass | fail
pdf_readability_gate: pass | conditional pass | fail
```

Only `pass + pass` is fully acceptable.

### 10. Self review

Use `prompts/self-review.md`.

Self review is a reference check only. It must not be used as the final pass decision.

### 11. Independent review

Use `prompts/independent-review.md`.

The independent reviewer can use the same model as the generator, but it must be a separate agent/context with a different prompt.

Review dimensions:

```text
function_coverage: /5
source_accuracy: /5
rule_completeness: /5
requirement_expression_quality: /5
kb_friendliness: /5
total: /25
```

### 12. Gate result

Use `templates/skill-a-review-gate.md`.

A pass requires:

- Scope confirmed.
- No hard-fail item.
- SRS covers the confirmed scope.
- Source evidence supports key conclusions.
- `pdf_text_layer_gate = pass`.
- `pdf_readability_gate = pass`.
- Independent review passes or manual review explicitly allows pass.

## Hard-fail items

Any one of these should fail the skill gate:

- Fabricated requirement, field, permission, flow, or rule that is not supported by source evidence.
- Missing core feature.
- Key rule written opposite to source behavior.
- Unusable document structure.
- PDF text layer cannot be extracted.
- PDF readability gate fails.
- Key conclusion has no source evidence and no explicit manual approval.

## Handoff to downstream knowledge-base work

When this skill passes, hand off:

```text
PROJECT_NAME=
BUSINESS_DOMAIN=
TEST_SCOPE=
MIN_BUSINESS_FLOW=
SRS_MARKDOWN=
SRS_PDF=
SOURCE_EVIDENCE_MAP=
PDF_QUALITY_REPORT=
INDEPENDENT_REVIEW_REPORT=
GATE_RESULT=pass
KNOWN_LIMITATIONS=
```

For RAGFlow knowledge-base creation and retrieval evaluation, use the downstream knowledge-base builder skill rather than this skill.

## Portable resources

This skill includes:

```text
references/  — detailed specs
prompts/     — execution prompts
templates/   — output templates
scripts/     — PDF generation and quality-check scripts
```

Important references:

- `references/skill-a-source-to-srs.md`
- `references/skill-a-scope-confirmation.md`
- `references/skill-a-source-evidence-map.md`
- `references/skill-a-scorecard.md`
- `references/skill-a-review-and-gate.md`
- `references/skill-a-pdf-generation-and-text-check.md`
- `references/handoff-sync-policy.md`

Important scripts:

- `scripts/generate_srs_pdf.py`
- `scripts/check_pdf_text_layer.py`

## Common problems

### PDF shows English as separated letters

Use the bundled `generate_srs_pdf.py`. It defaults to a CJK-capable font strategy and avoids the older `STSong-Light` visual spacing problem in the ReportLab path.

### PDF passes text extraction but looks bad

Do not pass the skill gate. `pdf_readability_gate` must be checked separately from text extraction.

### The generated SRS is accurate but too implementation-heavy

Run the knowledge-base-friendly rewrite step again. The final SRS should express requirements, not source-code notes.

### Scope is unclear

Do not force a full SRS. Produce `scope-confirmation.md` with `blocked` or `risk_items`, and ask for clarification unless autonomous mode is explicitly allowed and risk is acceptable.

### User asks to continue into RAGFlow

Stop this skill after producing the verified SRS package and handoff. Use the knowledge-base builder skill for RAGFlow dataset creation, chunk checks, retrieval sanity checks, and retrieval gate.
