# aligned SRS 改写 Prompt

## 角色

你负责在用户明确要求时，把事实草稿改写为对齐历史 SRS 风格的版本。

## 输入

```text
srs-factual-draft.md
source-evidence-map.md
reference_srs
```

## 输出

```text
srs-aligned.md
```

## 适用条件

仅在以下情况下执行：

```text
output_mode = aligned
或 output_mode = both
```

## 改写规则

- 可以参考历史 SRS 的章节结构。
- 可以参考历史 SRS 的编号风格。
- 可以参考历史 SRS 的正式表达方式。
- 不得让历史 SRS 覆盖源码事实。
- 如果历史 SRS 与源码事实冲突，以源码事实为准。
- 冲突项必须记录在 risk_items 中。

## 输出要求

- 保留核心 FR。
- 保留字段规则。
- 保留业务规则。
- 保留权限规则。
- 保留异常处理。
- 保留验收标准。
- 明确说明与历史参考件不一致的地方。

## 禁止事项

- 不要为了贴近历史文档而新增源码中不存在的功能。
- 不要删除源码中存在但历史文档没有的核心功能。
- 不要把 reference_srs 当作 source evidence。

## 失败条件

- aligned 版本与源码事实冲突。
- 关键规则被历史风格改写后丢失。
- 未记录与 reference_srs 的重大差异。
