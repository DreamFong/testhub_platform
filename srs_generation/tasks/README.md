# SRS Skill 化任务清单目录

本目录用于拆解“源码逆向生成 SRS → RAGFlow 知识库验证 → TestHub 自动化闭环”的实施任务。

## 文件说明

- [00-implementation-roadmap.md](00-implementation-roadmap.md)：总实施路线图
- [01-skill-a-spec-tasks.md](01-skill-a-spec-tasks.md)：Skill A 规范固化任务
- [02-skill-a-execution-prompts-tasks.md](02-skill-a-execution-prompts-tasks.md)：Skill A 可执行化与 prompt 任务
- [03-skill-a-validation-tasks.md](03-skill-a-validation-tasks.md)：Skill A 多样本验证任务
- [04-skill-b-tasks.md](04-skill-b-tasks.md)：Skill B 知识库构建与检索验证任务
- [05-skill-c-tasks.md](05-skill-c-tasks.md)：Skill C 执行约束增强任务
- [06-orchestration-skill-tasks.md](06-orchestration-skill-tasks.md)：总编排 Skill 任务
- [07-artifact-structure-tasks.md](07-artifact-structure-tasks.md)：产物目录与文件命名任务
- [08-open-decisions.md](08-open-decisions.md)：待确认决策清单

## 建议执行顺序

```text
00 → 01 → 02 → 03 → 04 → 05 → 06
          ↘ 07
          ↘ 08 持续维护
```

## 当前优先级

建议先完成：

1. Skill A 规范固化
2. Skill A prompt 可执行化
3. 第二个样本验证

Skill A 稳定后，再推进 Skill B、Skill C 和总编排。
