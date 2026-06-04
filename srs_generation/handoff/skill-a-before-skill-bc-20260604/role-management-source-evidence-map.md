# Source Evidence Map

## 基本信息

```text
project: ruoyi-vue-pro
target_module: system role management
srs_markdown: srs-kb-friendly.md
srs_pdf: srs-kb-friendly.pdf
```

## 功能需求 Evidence

### FR-ROLE-001 角色创建

- source_confidence: high
- Controller / Router: RoleController#createRole，`POST /system/role/create`
- Service: RoleServiceImpl#createRole
- Request DTO / VO: RoleSaveReqVO
- Entity / Mapper: RoleDO、RoleMapper
- Permission: `system:role:create`
- ErrorCode: ROLE_NAME_DUPLICATE、ROLE_CODE_DUPLICATE、ROLE_ADMIN_CODE_ERROR

### FR-ROLE-002 角色修改

- source_confidence: high
- Controller / Router: RoleController#updateRole，`PUT /system/role/update`
- Service: RoleServiceImpl#updateRole
- Request DTO / VO: RoleSaveReqVO
- Permission: `system:role:update`
- ErrorCode: ROLE_NOT_EXISTS、ROLE_CAN_NOT_UPDATE_SYSTEM_TYPE_ROLE、ROLE_NAME_DUPLICATE、ROLE_CODE_DUPLICATE

### FR-ROLE-003 角色删除

- source_confidence: high
- Controller / Router: RoleController#deleteRole，`DELETE /system/role/delete`
- Service: RoleServiceImpl#deleteRole
- Permission: `system:role:delete`
- ErrorCode: ROLE_NOT_EXISTS、ROLE_CAN_NOT_UPDATE_SYSTEM_TYPE_ROLE

### FR-ROLE-004 角色批量删除

- source_confidence: high
- Controller / Router: RoleController#deleteRoleList，`DELETE /system/role/delete-list`
- Service: RoleServiceImpl#deleteRoleList
- Permission: `system:role:delete`
- ErrorCode: ROLE_NOT_EXISTS、ROLE_CAN_NOT_UPDATE_SYSTEM_TYPE_ROLE

### FR-ROLE-005 角色详情查询

- source_confidence: high
- Controller / Router: RoleController#getRole，`GET /system/role/get`
- Service: RoleServiceImpl#getRole
- Response DTO / VO: RoleRespVO
- Permission: `system:role:query`

### FR-ROLE-006 角色分页查询

- source_confidence: high
- Controller / Router: RoleController#getRolePage，`GET /system/role/page`
- Service: RoleServiceImpl#getRolePage
- Request DTO / VO: RolePageReqVO
- Response DTO / VO: RoleRespVO
- Mapper: RoleMapper#selectPage
- Permission: `system:role:query`

### FR-ROLE-007 角色精简列表查询

- source_confidence: high
- Controller / Router: RoleController#getSimpleRoleList，`GET /system/role/list-all-simple`、`GET /system/role/simple-list`
- Service: RoleServiceImpl#getRoleListByStatus
- Mapper: RoleMapper#selectListByStatus
- Permission: 无显式 PreAuthorize

### FR-ROLE-008 角色导出

- source_confidence: high
- Controller / Router: RoleController#export，`GET /system/role/export-excel`
- Service: RoleServiceImpl#getRolePage
- Response DTO / VO: RoleRespVO
- Permission: `system:role:export`

## 字段规则 Evidence

- name：RoleSaveReqVO `@NotBlank`、`@Size(max=30)`；RoleServiceImpl#validateRoleDuplicate；RoleMapper#selectByName。
- code：RoleSaveReqVO `@NotBlank`、`@Size(max=100)`；RoleServiceImpl#validateRoleDuplicate；RoleMapper#selectByCode；RoleCodeEnum.isSuperAdmin。
- sort：RoleSaveReqVO `@NotNull`。
- status：RoleSaveReqVO `@NotNull`、`@InEnum(CommonStatusEnum)`；RoleDO#status。
- remark：RoleSaveReqVO `@Size(max=500)`。
- page query：RolePageReqVO name、code、status、createTime；RoleMapper#selectPage。

## 业务规则 Evidence

- 唯一性校验：RoleServiceImpl#validateRoleDuplicate。
- 超级管理员标识保护：RoleCodeEnum.isSuperAdmin 调用与 ROLE_ADMIN_CODE_ERROR。
- 默认角色类型：createRole 中 RoleTypeEnum.CUSTOM。
- 默认状态：createRole 中 CommonStatusEnum.ENABLE。
- 默认数据范围：createRole 中 DataScopeEnum.ALL。
- 系统内置角色保护：validateRoleForUpdate 中 RoleTypeEnum.SYSTEM。
- 删除清理权限关联：deleteRole 和 deleteRoleList 调用 permissionService.processRoleDeleted。
- 精简列表排序：RoleController#getSimpleRoleList 中按 RoleDO#sort 排序。

## 权限规则 Evidence

- `system:role:create`：RoleController#createRole。
- `system:role:update`：RoleController#updateRole。
- `system:role:delete`：RoleController#deleteRole 和 deleteRoleList。
- `system:role:query`：RoleController#getRole 和 getRolePage。
- `system:role:export`：RoleController#export。
- 无显式权限：RoleController#getSimpleRoleList。

## 异常处理 Evidence

- ROLE_NOT_EXISTS：ErrorCodeConstants；RoleServiceImpl#validateRoleForUpdate。
- ROLE_NAME_DUPLICATE：ErrorCodeConstants；RoleServiceImpl#validateRoleDuplicate。
- ROLE_CODE_DUPLICATE：ErrorCodeConstants；RoleServiceImpl#validateRoleDuplicate。
- ROLE_CAN_NOT_UPDATE_SYSTEM_TYPE_ROLE：ErrorCodeConstants；RoleServiceImpl#validateRoleForUpdate。
- ROLE_IS_DISABLE：ErrorCodeConstants；RoleServiceImpl#validateRoleList。
- ROLE_ADMIN_CODE_ERROR：ErrorCodeConstants；RoleServiceImpl#validateRoleDuplicate。

## 验收标准 Evidence

- AC-ROLE-001：创建成功和重复校验来自 createRole 与 validateRoleDuplicate。
- AC-ROLE-002：修改系统内置角色限制来自 validateRoleForUpdate。
- AC-ROLE-003：删除清理权限关联来自 deleteRole 和 permissionService.processRoleDeleted。
- AC-ROLE-004：分页查询条件和排序来自 RoleMapper#selectPage。
- AC-ROLE-005：精简列表启用过滤和 sort 排序来自 getSimpleRoleList。

## Evidence 质量检查

- 无依据 FR：无。
- 无依据字段规则：无。
- 无依据权限规则：无。
- 无依据异常规则：无。
- SRS 与 evidence 不一致项：无。
- 低置信度关键项：无。

## Gate 影响

```text
has_missing_critical_evidence: false
has_source_conflict: false
requires_manual_review: false
recommended_gate: pass
```
