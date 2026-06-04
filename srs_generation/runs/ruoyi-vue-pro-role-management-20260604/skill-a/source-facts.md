# Source Facts

## 1. 功能点

### 角色创建

- 类型：新增
- 入口：`POST /system/role/create`
- Controller：RoleController#createRole
- Service：RoleServiceImpl#createRole
- 请求对象：RoleSaveReqVO
- 响应：角色 ID
- 权限码：`system:role:create`
- 主要规则：角色名称和标识唯一；角色标识不能为超级管理员标识；默认角色类型为自定义；未传状态时默认启用；默认数据范围为全部数据。
- 异常：ROLE_NAME_DUPLICATE、ROLE_CODE_DUPLICATE、ROLE_ADMIN_CODE_ERROR。

### 角色修改

- 类型：编辑
- 入口：`PUT /system/role/update`
- Controller：RoleController#updateRole
- Service：RoleServiceImpl#updateRole
- 请求对象：RoleSaveReqVO
- 权限码：`system:role:update`
- 主要规则：校验角色存在且不是系统内置角色；角色名称和标识唯一；更新角色基础信息；清理角色缓存。
- 异常：ROLE_NOT_EXISTS、ROLE_CAN_NOT_UPDATE_SYSTEM_TYPE_ROLE、ROLE_NAME_DUPLICATE、ROLE_CODE_DUPLICATE、ROLE_ADMIN_CODE_ERROR。

### 角色删除

- 类型：删除
- 入口：`DELETE /system/role/delete`
- Controller：RoleController#deleteRole
- Service：RoleServiceImpl#deleteRole
- 权限码：`system:role:delete`
- 主要规则：校验角色存在且不是系统内置角色；删除角色；清理角色相关权限数据；清理角色缓存。
- 异常：ROLE_NOT_EXISTS、ROLE_CAN_NOT_UPDATE_SYSTEM_TYPE_ROLE。

### 角色批量删除

- 类型：批量删除
- 入口：`DELETE /system/role/delete-list`
- Controller：RoleController#deleteRoleList
- Service：RoleServiceImpl#deleteRoleList
- 权限码：`system:role:delete`
- 主要规则：逐个校验角色可更新；批量删除角色；逐个清理权限关联。
- 异常：ROLE_NOT_EXISTS、ROLE_CAN_NOT_UPDATE_SYSTEM_TYPE_ROLE。

### 角色详情查询

- 类型：详情
- 入口：`GET /system/role/get`
- Controller：RoleController#getRole
- Service：RoleServiceImpl#getRole
- 响应对象：RoleRespVO
- 权限码：`system:role:query`

### 角色分页查询

- 类型：查询
- 入口：`GET /system/role/page`
- Controller：RoleController#getRolePage
- Service：RoleServiceImpl#getRolePage
- 请求对象：RolePageReqVO
- 响应对象：PageResult<RoleRespVO>
- 权限码：`system:role:query`
- 查询条件：角色名称、角色标识、状态、创建时间。
- 主要规则：名称和标识模糊匹配；状态精确匹配；创建时间范围匹配；按 sort 升序。

### 角色精简列表查询

- 类型：查询
- 入口：`GET /system/role/list-all-simple` 与 `GET /system/role/simple-list`
- Controller：RoleController#getSimpleRoleList
- Service：RoleServiceImpl#getRoleListByStatus
- 权限码：无显式 PreAuthorize
- 主要规则：只返回启用角色，并按 sort 升序排序。

### 角色导出

- 类型：导出
- 入口：`GET /system/role/export-excel`
- Controller：RoleController#export
- Service：RoleServiceImpl#getRolePage
- 响应对象：RoleRespVO
- 权限码：`system:role:export`
- 主要规则：使用分页查询条件但设置为不分页，导出 RoleRespVO Excel 字段。

## 2. 字段规则

### RoleSaveReqVO

| 字段 | 规则 | 来源 | 置信度 |
|---|---|---|---|
| id | 角色编号；修改时用于定位角色 | RoleSaveReqVO#id | high |
| name | 必填；长度不超过 30；唯一 | RoleSaveReqVO 注解；validateRoleDuplicate | high |
| code | 必填；长度不超过 100；唯一；不能为超级管理员标识 | RoleSaveReqVO 注解；validateRoleDuplicate | high |
| sort | 必填 | RoleSaveReqVO#sort | high |
| status | 必填；必须属于 CommonStatusEnum | RoleSaveReqVO#status | high |
| remark | 长度不超过 500 | RoleSaveReqVO#remark | high |

### RolePageReqVO

| 字段 | 规则 | 来源 | 置信度 |
|---|---|---|---|
| name | 模糊匹配 | RoleMapper#selectPage | high |
| code | 模糊匹配 | RoleMapper#selectPage | high |
| status | 精确匹配 | RoleMapper#selectPage | high |
| createTime | 时间范围查询 | RoleMapper#selectPage | high |

## 3. 业务规则

- 创建角色时校验角色名称和角色标识唯一。
- 角色标识不能使用超级管理员标识。
- 创建角色默认类型为自定义角色。
- 创建角色默认状态为启用，除非请求中指定状态。
- 创建角色默认数据范围为全部数据。
- 修改、删除、批量删除前必须校验角色存在且不是系统内置角色。
- 删除角色后必须清理角色相关权限数据。
- 角色精简列表只返回启用角色并按排序字段升序。

## 4. 权限规则

| 功能 | 权限码 | 来源 | 置信度 |
|---|---|---|---|
| 创建角色 | system:role:create | RoleController#createRole | high |
| 修改角色 | system:role:update | RoleController#updateRole | high |
| 删除角色 | system:role:delete | RoleController#deleteRole / deleteRoleList | high |
| 查询角色 | system:role:query | getRole / getRolePage | high |
| 导出角色 | system:role:export | export | high |
| 精简列表 | 无显式权限注解 | getSimpleRoleList | high |

## 5. 异常处理

| 异常 | 错误码 | 触发条件 | 来源 | 置信度 |
|---|---|---|---|---|
| 角色不存在 | ROLE_NOT_EXISTS | 修改、删除、批量删除等目标角色不存在 | validateRoleForUpdate | high |
| 角色名称重复 | ROLE_NAME_DUPLICATE | 名称被其他角色使用 | validateRoleDuplicate | high |
| 角色标识重复 | ROLE_CODE_DUPLICATE | 标识被其他角色使用 | validateRoleDuplicate | high |
| 不能操作系统内置角色 | ROLE_CAN_NOT_UPDATE_SYSTEM_TYPE_ROLE | 修改或删除系统内置角色 | validateRoleForUpdate | high |
| 角色已禁用 | ROLE_IS_DISABLE | validateRoleList 校验角色集合时角色禁用 | validateRoleList | medium |
| 超级管理员标识不可用 | ROLE_ADMIN_CODE_ERROR | 创建或修改时使用超级管理员标识 | validateRoleDuplicate | high |

## 6. 验收要点

- 有 `system:role:create` 权限且输入合法时，创建角色返回角色 ID。
- 名称重复、标识重复或使用超级管理员标识时，系统返回对应错误码。
- 修改或删除系统内置角色时，系统返回 ROLE_CAN_NOT_UPDATE_SYSTEM_TYPE_ROLE。
- 分页查询支持名称、标识、状态和创建时间条件，并按 sort 升序。
- 精简列表只返回启用角色并按 sort 升序。
- 导出角色应复用分页查询条件，并输出 RoleRespVO Excel 字段。
