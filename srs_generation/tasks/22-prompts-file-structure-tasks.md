# Prompt 文件结构任务清单

## 目标

规划 Skill A / B / C 的 prompt 文件拆分方式，避免所有逻辑堆在一个大 prompt 中。

## 1. Prompt 目录结构

- [x] 创建 `srs_generation/prompts/` 目录
- [x] 创建 `srs_generation/prompts/skill-a/` 子目录
- [x] 创建 `srs_generation/prompts/skill-b/` 子目录
- [x] 创建 `srs_generation/prompts/skill-c/` 子目录
- [x] 创建 `srs_generation/prompts/orchestration/` 子目录

完成标准：不同阶段 prompt 有独立维护位置。

## 2. Skill A Prompt 文件

- [x] `skill-a-controller.md`
- [x] `scope-inference.md`
- [x] `source-fact-extraction.md`
- [x] `source-evidence-map.md`
- [x] `srs-draft-generation.md`
- [x] `srs-kb-friendly-rewrite.md`
- [x] `srs-aligned-rewrite.md`
- [x] `self-review.md`
- [x] `independent-review.md`

完成标准：Skill A 每个关键步骤都有单独 prompt。

## 3. Skill B Prompt 文件

- [x] `skill-b-controller.md`
- [x] `ragflow-kb-plan.md`
- [x] `chunk-quality-check.md`
- [x] `retrieval-sanity-check.md`
- [x] `retrieval-gate.md`

完成标准：Skill B 可逐步从手动流程转为可执行流程。

## 4. Skill C Prompt 文件

- [x] `skill-c-controller.md`
- [x] `auth-constraint-extraction.md`
- [x] `entity-id-extraction.md`
- [x] `minimal-body-template.md`
- [x] `headers-template.md`
- [x] `negative-constraints.md`
- [x] `execution-constraint-report.md`

完成标准：执行约束提炼可模块化维护。

## 5. Orchestration Prompt 文件

- [x] `workflow-controller.md`
- [x] `stage-gate-policy.md`
- [x] `handoff-summary.md`
- [x] `failure-recovery.md`

完成标准：总编排可以引用 A/B/C prompt，而不是复制内容。

## 6. Prompt 编写规范

- [x] 每个 prompt 写明输入
- [x] 每个 prompt 写明输出
- [x] 每个 prompt 写明禁止事项
- [x] 每个 prompt 写明质量要求
- [x] 每个 prompt 写明失败条件
- [x] 每个 prompt 给出最小示例

完成标准：prompt 文件本身具备可测试性。
