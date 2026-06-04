# 第二验证样本选择任务清单

## 目标

选择一个不同于 RuoYi-Vue-Pro 用户管理的样本模块，用于验证 Skill A 的迁移能力。

## 1. 候选样本来源

- [x] 从 RuoYi-Vue-Pro 中选择另一个后端业务模块
- [x] 从 TestHub 当前项目中选择一个业务模块
- [x] 比较跨项目样本和同项目样本的验证价值
- [x] 排除过于简单的 CRUD 模块
- [x] 排除依赖过多外部系统且难以验证的模块

完成标准：形成 2～3 个候选样本。

## 2. 候选样本评估标准

- [x] 是否有清晰 Controller / API 入口
- [x] 是否有 Service 层业务规则
- [x] 是否有 DTO / VO 字段规则
- [x] 是否有权限规则
- [x] 是否有错误码或异常处理
- [x] 是否有导入导出、状态流转或批量操作等复杂点
- [x] 是否能生成有代表性的 SRS

完成标准：样本选择不是随意挑选，而是能验证 Skill A 能力。

## 3. 推荐候选方向

- [x] RuoYi-Vue-Pro 角色管理模块
- [x] RuoYi-Vue-Pro 部门管理模块
- [x] RuoYi-Vue-Pro 菜单管理模块
- [x] TestHub API testing 模块
- [x] TestHub UI automation 模块
- [x] TestHub requirement_analysis 模块

完成标准：至少选出一个首选样本和一个备选样本。

## 4. 样本确认

- [x] 记录最终样本项目路径
- [x] 记录 target_module
- [x] 记录已知入口文件
- [x] 记录预期复杂点
- [x] 记录不纳入范围的能力
- [x] 记录验证目标

完成标准：第二样本可以进入 Skill A scope 推断流程。

## 5. 验证计划

- [x] 对第二样本执行入口发现
- [x] 对第二样本执行 scope 推断
- [x] 请求用户确认 scope
- [x] 生成 SRS
- [x] 生成 PDF
- [x] 执行独立评审
- [x] 汇总泛化问题

完成标准：第二样本能产出完整验证报告。
