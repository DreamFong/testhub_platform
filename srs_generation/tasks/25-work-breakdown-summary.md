# 工作拆解汇总

## 总体拆解

本次实施计划已经拆分为以下主线：

```text
P0：Skill A 规范固化
P1：Skill A 可执行化
P2：Skill A 多样本验证
P3：Skill B / Skill C 规范沉淀
P4：总编排与 TestHub handoff
```

## 文件分组

### 总览类

- [00-implementation-roadmap.md](00-implementation-roadmap.md)
- [18-done-criteria.md](18-done-criteria.md)
- [19-task-index-by-priority.md](19-task-index-by-priority.md)
- [20-traceability-matrix.md](20-traceability-matrix.md)
- [25-work-breakdown-summary.md](25-work-breakdown-summary.md)

### Skill A 类

- [01-skill-a-spec-tasks.md](01-skill-a-spec-tasks.md)
- [02-skill-a-execution-prompts-tasks.md](02-skill-a-execution-prompts-tasks.md)
- [03-skill-a-validation-tasks.md](03-skill-a-validation-tasks.md)
- [10-skill-a-scorecard-tasks.md](10-skill-a-scorecard-tasks.md)
- [11-scope-confirmation-tasks.md](11-scope-confirmation-tasks.md)
- [12-source-evidence-map-tasks.md](12-source-evidence-map-tasks.md)
- [13-pdf-generation-and-text-check-tasks.md](13-pdf-generation-and-text-check-tasks.md)
- [14-second-sample-selection-tasks.md](14-second-sample-selection-tasks.md)
- [15-review-and-gate-tasks.md](15-review-and-gate-tasks.md)
- [21-skill-a-spec-document-tasks.md](21-skill-a-spec-document-tasks.md)
- [22-prompts-file-structure-tasks.md](22-prompts-file-structure-tasks.md)

### Skill B 类

- [04-skill-b-tasks.md](04-skill-b-tasks.md)
- [23-skill-b-spec-document-tasks.md](23-skill-b-spec-document-tasks.md)

### Skill C 类

- [05-skill-c-tasks.md](05-skill-c-tasks.md)
- [24-skill-c-spec-document-tasks.md](24-skill-c-spec-document-tasks.md)

### 总编排与交付类

- [06-orchestration-skill-tasks.md](06-orchestration-skill-tasks.md)
- [07-artifact-structure-tasks.md](07-artifact-structure-tasks.md)
- [16-testhub-handoff-tasks.md](16-testhub-handoff-tasks.md)

### 决策与风险类

- [08-open-decisions.md](08-open-decisions.md)
- [09-next-actions.md](09-next-actions.md)
- [17-risk-register.md](17-risk-register.md)

## 建议立即执行的前三个文件

1. [21-skill-a-spec-document-tasks.md](21-skill-a-spec-document-tasks.md)
2. [11-scope-confirmation-tasks.md](11-scope-confirmation-tasks.md)
3. [12-source-evidence-map-tasks.md](12-source-evidence-map-tasks.md)

这三个文件对应当前最关键的落地点：

```text
正式 spec
→ scope confirm gate
→ source evidence map
```

## 当前最小推进路径

```text
先完成 Skill A spec 文档
→ 再完成 Skill A prompt 文件结构
→ 再用用户管理回归
→ 再选第二样本验证
```
