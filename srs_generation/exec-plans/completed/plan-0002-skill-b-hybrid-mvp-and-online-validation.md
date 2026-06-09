# Skill B Hybrid MVP 与在线验证收敛

Status: completed

## Objective

将 Skill B 收敛为稳定的知识库准备度与检索验证层，完成 Hybrid MVP 规范、模板、prompt、可移植 skill 打包，以及用户管理样例的 package validation 与真实 online 验证。

## Scope

- 固化 Skill B 的职责边界、输入输出契约、offline / online gate 语义。
- 建立 Skill B templates、prompts 与 handoff 结构。
- 明确主载体、解析策略与 blocked 语义。
- 基于用户管理样例完成 package validation 和真实 online 验证。
- 同步到 portable skill：`.claude/skills/srs-to-ragflow-kb/`。

## Out of scope

- 不生成或修改 SRS。
- 不进入 Skill C 执行约束增强。
- 不生成 TestHub scenario JSON。
- 不把源码级证据追溯强行塞进主 SRS KB。

## Approach

1. 先用 `specs/skill-b-knowledge-base-and-retrieval.md` 固化 Hybrid MVP 语义。
2. 建立 `kb-plan.md`、`parse-config-plan.md`、`retrieval-question-set.md`、`skill-b-handoff.md` 等固定产物。
3. 明确 offline_readiness_gate 与 online_retrieval_gate 的边界和 blocked 语义。
4. 对用户管理样例执行 package validation 与真实 online 验证。
5. 基于真实结果收敛主载体选择策略。
6. 打包为 `.claude/skills/srs-to-ragflow-kb/`。

## Acceptance criteria

- Skill B 规范已落在 `specs/skill-b-knowledge-base-and-retrieval.md`。
- Skill B templates 与 prompts 已建立。
- 用户管理样例已形成 canonical handoff。
- 当前 canonical run 已达到：`online_retrieval_gate=pass`、`skill_b_status=online_verified`。
- 主 SRS KB 载体策略已收敛为 TXT carrier + `book`。
- `srs-to-ragflow-kb` 已作为可移植 skill 可用。

## Risks

- 当前主 SRS KB 只覆盖业务需求，不直接承担源码级证据追溯。
- 外部系统能力变化可能影响 Markdown / PDF / TXT 的相对可用性，需要通过新 run 重新验证，而不是回写旧结论。

## Learnings

- Hybrid MVP 比纯 offline 或直接 full online 更适合当前链路，因为它能同时表达准备度、blocked 语义和真实在线结果。
- 主载体选择必须以真实 parser 结果为准，而不是以文档格式表面直觉为准。
- `blocked` 语义必须明确，否则很容易伪造“看起来完成了”的在线结果。
