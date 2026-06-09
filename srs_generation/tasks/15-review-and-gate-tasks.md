# Skill A Review 与 Gate 任务清单

> 当前状态：本文件已归并到 `../exec-plans/completed/plan-0001-skill-a-foundation-and-validation.md`，其稳定规则现以 `../specs/skill-a-review-and-gate.md` 为准。

## 目标

细化 Skill A 的自评、独立评审、人工复核和 gate 判定流程，确保生成的 SRS 质量可控。

## 1. 自评流程

- [x] 定义自评输入
- [x] 定义自评输出
- [x] 定义自评五维评分格式
- [x] 定义自评风险项格式
- [x] 定义自评不确定项格式
- [x] 明确自评不能作为最终通过依据

完成标准：生成 Agent 能主动暴露问题。

## 2. 独立评审流程

- [x] 定义独立评审输入
- [x] 定义独立评审输出
- [x] 定义独立评审必须读取的产物
- [x] 定义源码依据核验要求
- [x] 定义硬性不合格项检查要求
- [x] 定义正式评分格式
- [x] 定义必须修改项和建议修改项格式

完成标准：独立评审 Agent 可以作为机器主评分来源。

## 3. 分差处理

- [x] 定义自评与正式评审分差计算方式
- [x] 定义总分差 ≥ 3 的处理方式
- [x] 定义单项分差过大的处理方式
- [x] 定义分差触发人工复核的记录格式

完成标准：评分冲突不会被忽略。

## 4. Gate 判定

- [x] 定义 `pass` 判定条件
- [x] 定义 `conditional pass` 判定条件
- [x] 定义 `fail` 判定条件
- [x] 定义硬性不合格项优先级
- [x] 定义必须修改项与 gate 的关系
- [x] 定义进入 Skill B 的最低条件

完成标准：每次 Skill A 执行都有明确去向。

## 5. 人工复核

- [x] 定义人工复核触发条件
- [x] 定义人工复核输入资料
- [x] 定义人工复核输出格式
- [x] 定义人工复核如何覆盖机器评分
- [x] 定义人工复核记录文件名

完成标准：争议情况可以由人工最终裁决。

## 6. Review 报告模板

- [x] 定义 summary 部分
- [x] 定义 scorecard 部分
- [x] 定义 hard-fail checklist 部分
- [x] 定义 source evidence findings 部分
- [x] 定义 required fixes 部分
- [x] 定义 recommended improvements 部分
- [x] 定义 final gate 部分

完成标准：review 报告可读、可审计、可作为 handoff 文件。
