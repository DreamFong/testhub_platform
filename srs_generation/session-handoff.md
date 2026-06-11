# SRS Skill 化新会话交接摘要

更新时间：2026-06-09  
分支：`srs-generation-skill-a-prep`

## 1. 当前 stop point

当前 stop point 是：

```text
继续推进 srs_generation 文档骨架治理
不访问 RAGFlow
不进入 Skill C
不修改 runs 事实产物
```

当前主治理计划：

```text
srs_generation/exec-plans/active/plan-0004-sdd-doc-structure-governance.md
```

当前骨架治理 Phase 1 收官记录：

```text
srs_generation/exec-plans/completed/plan-0003-sdd-doc-structure-governance-phase-1.md
```

## 2. 当前最重要的事实

- Skill A 已打包为 `.claude/skills/source-to-srs/`
- Skill B 已打包为 `.claude/skills/srs-to-ragflow-kb/`
- 当前 canonical Skill B handoff 已 online verified
- 当前工作重点是骨架整改，不是继续外部系统执行
- Skill A / Skill B 参考副本同步已完成，剩余差异仅保留可移植改写（如 `<skill_dir>`、`<run_dir>`、通用参考文档名），不涉及 gate、handoff 或输入输出契约语义漂移

当前 canonical handoff：

```text
srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-b-package-validation/skill-b-handoff.md
```

## 3. 新会话先读顺序

1. `srs_generation/README.md`
2. `srs_generation/session-handoff.md`
3. `srs_generation/current-work-summary.md`
4. `srs_generation/exec-plans/active/plan-0004-sdd-doc-structure-governance.md`
5. 当前 canonical handoff
6. 必要时再读相关 `specs/` 与 `design-docs/`

不建议默认先读：

- 旧 `tasks/` 全目录
- `runs/` 全目录
- 旧版长历史 summary

## 4. 当前不要做

- 不要访问 RAGFlow
- 不要进入 Skill C
- 不要修改 `runs/` 下的事实产物
- 不要把新推进内容重新写回旧 `tasks/`
- 不要把设计解释继续堆进 `current-work-summary.md`
- 不要重复发起 Skill A / Skill B 参考副本逐字一致性检查，除非 `specs/` 再次发生实质变化

## 5. 当前工作焦点

当前优先处理：

1. 维持 `README`、`DELIVERY`、`QUALITY_SCORE`、`summary`、`handoff` 与当前 active/completed plans 一致。
2. 保持 `specs/` 与 `.claude/skills/*/references/` 的 source-of-truth 关系清晰。
3. 旧 `tasks/` 已全部标注当前状态与归属去向，默认视为只读历史材料。
4. 若无新的骨架治理需求，可把当前状态视为 Phase 1 已收官。

## 6. 推荐新会话动作

新会话建议先做：

1. 读取本文件
2. 读取当前主治理计划
3. 读取骨架治理收官记录
4. 读取当前 canonical handoff
5. 视需要快速浏览：
   - `exec-plans/completed/plan-0001-skill-a-foundation-and-validation.md`
   - `exec-plans/completed/plan-0002-skill-b-hybrid-mvp-and-online-validation.md`
   - `exec-plans/active/plan-0005-skill-c-and-orchestration-readiness.md`
6. 检查工作区状态：
   - `git status --short`
   - `git log -3 --oneline`
7. 如无新的骨架治理目标，避免重新展开大规模结构调整

## 7. 推荐提示词

```text
继续 testhub_platform 的 SRS Skill 化骨架治理工作。

当前分支：srs-generation-skill-a-prep

请先读取：
- srs_generation/README.md
- srs_generation/session-handoff.md
- srs_generation/current-work-summary.md
- srs_generation/exec-plans/active/plan-0004-sdd-doc-structure-governance.md
- srs_generation/exec-plans/completed/plan-0003-sdd-doc-structure-governance-phase-1.md
- srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-b-package-validation/skill-b-handoff.md
- srs_generation/exec-plans/completed/plan-0001-skill-a-foundation-and-validation.md
- srs_generation/exec-plans/completed/plan-0002-skill-b-hybrid-mvp-and-online-validation.md

目标：
继续收敛 srs_generation 的 docs skeleton，保持 specs / design-docs / exec-plans / runs / summary / handoff 边界清晰。

限制：
- 不访问 RAGFlow
- 不进入 Skill C
- 不修改 runs 事实产物
- 优先在新骨架内治理，不回到旧 tasks 扩写
```
