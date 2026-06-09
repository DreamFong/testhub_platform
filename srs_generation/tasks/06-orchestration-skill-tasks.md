# 总编排 Skill 任务清单

> 当前状态：本文件后续由 `../exec-plans/active/plan-0005-skill-c-and-orchestration-readiness.md` 接续；当前仍保留作历史拆分清单。

## 目标

将 Skill A、Skill B、Skill C 串联为统一的 `ragflow-testhub-agent-workflow`，形成从源码到 TestHub 自动化闭环的可执行链路。

## 1. 总入口设计

- [ ] 定义总编排 Skill 名称
- [ ] 定义总入口输入参数
- [ ] 定义最小必填输入
- [ ] 定义可选输入
- [ ] 定义默认执行模式
- [ ] 定义只执行 A / B / C 单阶段的模式
- [ ] 定义全链路执行模式

完成标准：用户可以用同一个入口选择执行单阶段或全链路。

## 2. 阶段串联

- [ ] 串联 Skill A scope confirm
- [ ] 串联 Skill A SRS 生成
- [ ] 串联 Skill A review gate
- [ ] 串联 Skill B 知识库构建
- [ ] 串联 Skill B retrieval gate
- [ ] 串联 Skill C 执行约束提炼
- [ ] 串联最终 TestHub handoff

完成标准：每一阶段的输出都能作为下一阶段输入。

## 3. Gate 与失败回退

- [ ] 定义 Skill A fail 时停止流程
- [ ] 定义 Skill A conditional pass 时的处理方式
- [ ] 定义 Skill B fail 时停止流程
- [ ] 定义 Skill B conditional pass 时的处理方式
- [ ] 定义 Skill C 缺少真实跑通案例时的降级方式
- [ ] 定义人工确认节点
- [ ] 定义重跑某一阶段的机制

完成标准：流程不会在关键质量不达标时盲目继续。

## 4. 输出目录结构

- [ ] 定义每次运行的根目录命名规则
- [ ] 定义 Skill A 输出子目录
- [ ] 定义 Skill B 输出子目录
- [ ] 定义 Skill C 输出子目录
- [ ] 定义 reports 子目录
- [ ] 定义 handoff 子目录
- [ ] 定义最终摘要文件

完成标准：一次完整运行的所有产物都能被定位和审计。

## 5. 状态记录与可追踪性

- [ ] 记录输入参数快照
- [ ] 记录 scope confirm 结果
- [ ] 记录 Skill A gate 结果
- [ ] 记录 RAGFlow dataset_id / SRS_KB_ID
- [ ] 记录 Skill B gate 结果
- [ ] 记录 Skill C 约束来源
- [ ] 记录最终交付状态

完成标准：任何一次运行都能追踪关键决策和产物来源。

## 6. 最小闭环验收

- [ ] 用 RuoYi-Vue-Pro 用户管理执行全链路回归
- [ ] 用第二个样本执行全链路验证
- [ ] 检查 Skill A 产物是否完整
- [ ] 检查 Skill B retrieval gate 是否明确
- [ ] 检查 Skill C 是否产生可执行约束
- [ ] 检查最终 handoff 是否可被 TestHub 消费
- [ ] 形成端到端验证报告

完成标准：总编排 Skill 能从源码模块推进到可执行的 TestHub 自动化准备状态。
