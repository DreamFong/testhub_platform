# 后续文件创建清单

## 目标

记录完成任务清单之后，下一批应该创建的正式 spec、prompt、template 文件。

## Specs

- [ ] `srs_generation/specs/skill-a-source-to-srs.md`
- [ ] `srs_generation/specs/skill-b-kb-validation.md`
- [ ] `srs_generation/specs/skill-c-execution-constraints.md`
- [ ] `srs_generation/specs/orchestration-workflow.md`

## Skill A Prompts

- [ ] `srs_generation/prompts/skill-a/skill-a-controller.md`
- [ ] `srs_generation/prompts/skill-a/scope-inference.md`
- [ ] `srs_generation/prompts/skill-a/source-fact-extraction.md`
- [ ] `srs_generation/prompts/skill-a/source-evidence-map.md`
- [ ] `srs_generation/prompts/skill-a/srs-draft-generation.md`
- [ ] `srs_generation/prompts/skill-a/srs-kb-friendly-rewrite.md`
- [ ] `srs_generation/prompts/skill-a/srs-aligned-rewrite.md`
- [ ] `srs_generation/prompts/skill-a/self-review.md`
- [ ] `srs_generation/prompts/skill-a/independent-review.md`

## Skill B Prompts

- [ ] `srs_generation/prompts/skill-b/skill-b-controller.md`
- [ ] `srs_generation/prompts/skill-b/ragflow-kb-plan.md`
- [ ] `srs_generation/prompts/skill-b/chunk-quality-check.md`
- [ ] `srs_generation/prompts/skill-b/retrieval-sanity-check.md`
- [ ] `srs_generation/prompts/skill-b/retrieval-gate.md`

## Skill C Prompts

- [ ] `srs_generation/prompts/skill-c/skill-c-controller.md`
- [ ] `srs_generation/prompts/skill-c/auth-constraint-extraction.md`
- [ ] `srs_generation/prompts/skill-c/entity-id-extraction.md`
- [ ] `srs_generation/prompts/skill-c/minimal-body-template.md`
- [ ] `srs_generation/prompts/skill-c/headers-template.md`
- [ ] `srs_generation/prompts/skill-c/negative-constraints.md`
- [ ] `srs_generation/prompts/skill-c/execution-constraint-report.md`

## Templates

- [ ] `srs_generation/templates/source-evidence-map.md`
- [ ] `srs_generation/templates/skill-a-scorecard.md`
- [ ] `srs_generation/templates/scope-confirmation.md`
- [ ] `srs_generation/templates/pdf-text-check-report.md`
- [ ] `srs_generation/templates/ragflow-kb-record.md`
- [ ] `srs_generation/templates/chunk-quality-report.md`
- [ ] `srs_generation/templates/retrieval-sanity-check.md`
- [ ] `srs_generation/templates/execution-constraints.md`
- [ ] `srs_generation/templates/testhub-handoff.md`

## Reports

- [ ] `srs_generation/reports/skill-a-user-management-regression.md`
- [ ] `srs_generation/reports/skill-a-second-sample-validation.md`
- [ ] `srs_generation/reports/end-to-end-validation.md`

## Scripts

- [ ] `srs_generation/scripts/generate_srs_pdf.py`
- [ ] `srs_generation/scripts/check_pdf_text_layer.py`

## 建议

优先创建：

1. Skill A spec
2. Skill A prompts
3. Source evidence map template
4. Skill A scorecard template
5. 通用 PDF 脚本
