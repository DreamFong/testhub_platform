# Scope 自动推断与确认机制任务清单

> 当前状态：本文件已归并到 `../exec-plans/completed/plan-0001-skill-a-foundation-and-validation.md`，其稳定规则现以 `../specs/skill-a-scope-confirmation.md` 为准。

## 目标

细化 Skill A 的 scope confirm gate，确保用户不需要预先完整定义模块范围，但正式生成前必须确认边界。

## 1. 入口发现

- [x] 定义如何从 target_module 搜索 Controller / Router
- [x] 定义如何从 target_module 搜索 Service
- [x] 定义如何从 target_module 搜索 DTO / VO / Schema
- [x] 定义如何从 target_module 搜索 Entity / DO / Mapper
- [x] 定义如何从权限码搜索功能边界
- [x] 定义如何从错误码搜索功能边界

完成标准：Skill A 能从模块名找到候选源码入口。

## 2. 功能候选归类

- [x] 定义查询类功能归类规则
- [x] 定义详情类功能归类规则
- [x] 定义新增类功能归类规则
- [x] 定义编辑类功能归类规则
- [x] 定义删除类功能归类规则
- [x] 定义批量操作功能归类规则
- [x] 定义导入导出功能归类规则
- [x] 定义状态流转功能归类规则
- [x] 定义配置类功能归类规则

完成标准：候选功能能以业务能力而不是代码方法名展示。

## 3. 相邻能力识别

- [x] 定义跨模块调用识别规则
- [x] 定义共享基础能力识别规则
- [x] 定义只读依赖能力识别规则
- [x] 定义可配置但非本模块主线能力识别规则
- [x] 定义待确认相邻能力输出格式

完成标准：Skill A 不把所有相关代码都误纳入本轮 SRS。

## 4. 用户确认问题

- [x] 编写标准确认问题模板
- [x] 编写候选范围确认格式
- [x] 编写排除项确认格式
- [x] 编写遗漏项补充格式
- [x] 编写确认后范围摘要格式

完成标准：用户能快速确认范围，不需要阅读大量源码细节。

## 5. Gate 状态

- [x] 定义 `confirmed`
- [x] 定义 `confirmed_with_changes`
- [x] 定义 `blocked`
- [x] 定义 blocked 时需要补充的信息
- [x] 定义重新推断 scope 的触发条件

完成标准：流程不会在范围不明时继续生成正式 SRS。

## 6. 记录文件

- [x] 定义 scope-inference.md
- [x] 定义 scope-confirmation.md
- [x] 定义 excluded-scope.md
- [x] 定义 adjacent-capabilities.md
- [x] 定义 scope-risk-items.md

完成标准：范围决策可追踪、可复审。
