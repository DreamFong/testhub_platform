# Scope Inference

## 基本信息

```text
source_project: g:/work/genlot/projects/ruoyi-vue-pro
target_module: system role management
status: confirmed
```

## 入口发现

### Controller / Router

- RoleController.java：`@RequestMapping("/system/role")`，覆盖创建、修改、删除、批量删除、详情、分页、精简列表和导出。

### Service

- RoleServiceImpl.java：覆盖 createRole、updateRole、deleteRole、deleteRoleList、getRole、getRolePage、getRoleListByStatus、validateRoleDuplicate、validateRoleForUpdate、validateRoleList、updateRoleDataScope 等逻辑。

### DTO / VO / Schema

- RoleSaveReqVO.java：创建/修改字段规则。
- RolePageReqVO.java：分页查询条件。
- RoleRespVO.java：响应和导出字段。

### Entity / Mapper / SQL

- RoleDO.java：角色数据对象，包含名称、标识、排序、状态、类型、备注、数据范围和指定部门集合。
- RoleMapper.java：分页查询、按名称查询、按标识查询、按状态查询。

### Permission

- `system:role:create`
- `system:role:update`
- `system:role:delete`
- `system:role:query`
- `system:role:export`

### ErrorCode

- ROLE_NOT_EXISTS
- ROLE_NAME_DUPLICATE
- ROLE_CODE_DUPLICATE
- ROLE_CAN_NOT_UPDATE_SYSTEM_TYPE_ROLE
- ROLE_IS_DISABLE
- ROLE_ADMIN_CODE_ERROR

## 候选纳入范围

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

## 待确认相邻能力

- 数据范围更新：RoleServiceImpl 中存在 updateRoleDataScope，但 RoleController 当前文件未暴露角色数据范围更新入口；本轮作为相邻能力记录，不纳入 Controller 主线 SRS。
- 角色权限授权：删除角色时调用 permissionService.processRoleDeleted；本轮说明副作用，不展开权限授权模块。
- 缓存：RoleServiceImpl 使用角色缓存注解；本轮作为实现细节，不作为需求主线。

## 建议排除范围

- 角色菜单授权
- 角色数据范围配置接口
- 用户角色分配
- 权限菜单管理
- 缓存管理

## 自动确认结论

```text
status: confirmed
reason: 角色管理 Controller、Service、VO、Mapper、错误码入口完整，核心 CRUD、查询、导出和精简列表范围清晰；相邻权限授权和数据范围能力已记录但不展开。
```

## 风险项

- RoleServiceImpl 中包含 updateRoleDataScope，但当前 RoleController 未暴露对应接口，因此不作为本轮角色管理 Controller 主线功能展开。
