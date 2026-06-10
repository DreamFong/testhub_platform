# Handoff 与同步策略

版本：v0.1  
状态：draft

## 1. 目的

本文档用于定义 `specs/`、Skill 可移植参考副本、run handoff、`current-work-summary.md` 和 `session-handoff.md` 之间的角色边界与同步规则。

## 2. 权威 handoff 定义

当前阶段的权威 handoff，是被 `current-work-summary.md` 与 `session-handoff.md` 明确引用、且代表最新有效阶段结论的 handoff 文件。

当前权威 handoff 示例：

```text
srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-b-package-validation/skill-b-handoff.md
```

## 3. 角色边界

- `specs/`：规范事实源，定义规则、契约、边界与标准。
- `.claude/skills/*/references/`：可移植执行副本，不独立演化规范。
- `runs/*/skill-*-handoff.md`：阶段性事实 handoff，记录某次真实执行结果。
- `current-work-summary.md`：当前状态快照，记录当前 stop point、最近有效结论和下一步建议。
- `session-handoff.md`：新会话恢复入口，记录先读顺序、禁止事项和当前主计划。

## 4. Source Priority

当多个来源不一致时，优先级如下：

1. `specs/`
2. 最新 canonical run handoff / gate 结果
3. `current-work-summary.md`
4. `session-handoff.md`
5. Skill 可移植参考副本
6. 旧 `tasks/` 与历史讨论

## 5. 同步触发条件

以下情况应触发同步：

- 规范发生实质变化：先更新 `specs/`，再同步 skill references。
- 当前权威 handoff 改变：更新 `current-work-summary.md` 与 `session-handoff.md`。
- stop point 改变：更新 `session-handoff.md`。
- 当前工作焦点改变：更新 active `exec-plan`，必要时同步更新 summary 与 handoff。

## 6. 同步规则

- `current-work-summary.md` 只保留摘要和关键路径，不复制完整 handoff 内容。
- `session-handoff.md` 只保留恢复入口，不承担长期历史说明。
- 若 summary 与 handoff 冲突，应以 `specs/` 与最新 run handoff 为准，并修正文档入口文件。
- Skill 可移植参考副本仅在对应 repo spec 更新后同步，不应单独修订语义。
