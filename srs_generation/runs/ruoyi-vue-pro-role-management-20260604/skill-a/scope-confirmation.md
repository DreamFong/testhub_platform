# Scope Confirmation

## 基本信息

```text
project: ruoyi-vue-pro
target_module: system role management
scope_confirm_status: confirmed
confirmed_by: autonomous_source_evidence
confirmed_at: 2026-06-04
```

## 最终纳入范围

- 角色创建
- 角色修改
- 角色删除
- 角色批量删除
- 角色详情查询
- 角色分页查询
- 角色精简列表查询
- 角色导出
- 角色唯一性校验
- 系统内置角色保护

## 明确排除范围

- 角色菜单授权
- 角色数据范围配置接口
- 用户角色分配
- 权限菜单管理
- 缓存管理

## 作为依赖说明但不展开的能力

- 删除角色后权限关联清理
- 系统内置角色类型保护
- 角色缓存失效
- 数据范围字段展示

## Scope 风险项

| 风险 | 影响 | 处理方式 | 是否阻断 |
|---|---|---|---|
| Service 中存在数据范围更新但 Controller 未暴露 | 可能误纳入相邻能力 | 不纳入本轮 Controller 主线，仅在字段和依赖中说明 | 否 |
