# Exec-Plans Index

`exec-plans/` 用于记录 SRS Skill 化变更的执行计划与推进状态。

## 目的

每个 exec-plan 都应回答：

- 这次变更要解决什么问题
- 范围是什么
- 不包含什么
- 准备如何推进
- 验收标准是什么
- 有哪些风险与 learnings

## 目录结构

- `active/`：正在推进的计划
- `completed/`：已完成、已停止或已归档的计划

## 命名规则

- 统一使用 `plan-xxxx-<slug>.md` 形式命名。
- `xxxx` 使用四位数字，不足补 `0`，例如 `plan-0001-...`。
- 数字主要表达计划进入体系的先后顺序，便于肉眼快速判断主线演进顺序。
- 若后续新增计划，不回改已存在文件编号；直接为新计划分配下一个可用编号。
- 文件名中的 `<slug>` 仍保留语义化主题，避免只靠编号理解内容。

## 什么时候要新建 exec-plan

以下情况应新建或更新 exec-plan：

- 新增一个明确的治理变更
- 对 Skill A / B / C 的规范做实质性调整
- 重组目录结构、handoff 机制或同步策略
- 引入新的质量门禁、运行标准或设计分层
- 开始一个会影响多个文件的阶段性工作

## 推荐模板

```md
# <plan title>

Status: active

## Objective

## Scope

## Out of scope

## Approach

## Acceptance criteria

## Risks

## Learnings
```

## 生命周期

1. 计划开始前写入 `active/`
2. 方案明确后按该 plan 推进
3. 完成后补齐 `Learnings`
4. 移入 `completed/`

## 当前优先级记录方式

- 当前 live priority 不再维护在共享的静态 `tasks/` 索引里。
- 当前优先级、下一步与阻塞，应记录在相关 `active/` plan 中。
- 若多个 plan 并行，按当前用户目标和风险顺序决定主 plan。

## 当前 active plan

- `active/plan-0004-sdd-doc-structure-governance.md`：当前主治理计划，用于收敛 `srs_generation/` 骨架、冻结旧 `tasks/` 并压缩 summary / handoff。
- `active/plan-0005-skill-c-and-orchestration-readiness.md`：延后计划，用于未来切换焦点时接续 Skill C、总编排与最终 handoff。

## 当前 completed plans

- `completed/plan-0003-sdd-doc-structure-governance-phase-1.md`：骨架治理 Phase 1 的收官记录，说明目录边界、恢复入口与旧 tasks 历史层状态。
- `completed/plan-0001-skill-a-foundation-and-validation.md`：Skill A 规范、prompt、脚本、PDF gate、多样本验证与 portable skill 打包的完成归并。
- `completed/plan-0002-skill-b-hybrid-mvp-and-online-validation.md`：Skill B Hybrid MVP、主载体策略、package validation 与真实 online 验证的完成归并。

## 当前工作流分组

当前阶段建议按以下 workstream 维护：

- 文档骨架与治理整改
- Skill A 规范、prompt 与验证
- Skill B 契约、建库策略与验证
- Skill C / 总编排 / handoff

## 与旧 tasks/ 的关系

- 旧 `tasks/` 作为历史材料暂时保留。
- 新增推进内容不再默认写入 `tasks/`。
- 后续会逐步把仍然有效的推进内容收敛到 `exec-plans/`。
