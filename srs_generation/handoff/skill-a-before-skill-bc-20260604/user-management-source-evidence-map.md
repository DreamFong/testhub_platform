# Source Evidence Map

## 基本信息

```text
project: ruoyi-vue-pro
target_module: system user management
srs_markdown: srs-kb-friendly.md
srs_pdf: srs-kb-friendly.pdf
```

## 功能需求 Evidence

### FR-USER-001 用户分页查询

- source_confidence: high
- Controller / Router: UserController#getUserPage，`GET /system/user/page`
- Service: AdminUserServiceImpl#getUserPage
- Request DTO / VO: UserPageReqVO
- Response DTO / VO: UserRespVO
- Entity / Mapper / SQL: AdminUserMapper#selectPage
- Permission: `system:user:query`

### FR-USER-002 用户列表查询

- source_confidence: high
- Controller / Router: UserController#getUserList，`GET /system/user/list`
- Service: AdminUserServiceImpl#getUserList
- Response DTO / VO: UserRespVO
- Permission: `system:user:query`

### FR-USER-003 用户精简列表查询

- source_confidence: high
- Controller / Router: UserController#getSimpleUserList，`GET /system/user/list-all-simple`、`GET /system/user/simple-list`
- Service: AdminUserServiceImpl#getDeptUsers、getUserListByStatus
- Permission: 无显式 PreAuthorize

### FR-USER-004 用户详情查询

- source_confidence: high
- Controller / Router: UserController#getUser，`GET /system/user/get`
- Service: AdminUserServiceImpl#getUser
- Permission: `system:user:query`

### FR-USER-005 用户新增

- source_confidence: high
- Controller / Router: UserController#createUser，`POST /system/user/create`
- Service: AdminUserServiceImpl#createUser
- Request DTO / VO: UserSaveReqVO
- Permission: `system:user:create`
- ErrorCode: USER_COUNT_MAX、USER_USERNAME_EXISTS、USER_MOBILE_EXISTS、USER_EMAIL_EXISTS

### FR-USER-006 用户修改

- source_confidence: high
- Controller / Router: UserController#updateUser，`PUT /system/user/update`
- Service: AdminUserServiceImpl#updateUser
- Request DTO / VO: UserSaveReqVO
- Permission: `system:user:update`
- ErrorCode: USER_NOT_EXISTS、USER_USERNAME_EXISTS、USER_MOBILE_EXISTS、USER_EMAIL_EXISTS

### FR-USER-007 用户删除

- source_confidence: high
- Controller / Router: UserController#deleteUser，`DELETE /system/user/delete`
- Service: AdminUserServiceImpl#deleteUser
- Permission: `system:user:delete`
- ErrorCode: USER_NOT_EXISTS

### FR-USER-008 用户批量删除

- source_confidence: high
- Controller / Router: UserController#deleteUserList，`DELETE /system/user/delete-list`
- Service: AdminUserServiceImpl#deleteUserList
- Permission: `system:user:delete`

### FR-USER-009 重置用户密码

- source_confidence: high
- Controller / Router: UserController#updateUserPassword，`PUT /system/user/update-password`
- Service: AdminUserServiceImpl#updateUserPassword(Long, String)
- Request DTO / VO: UserUpdatePasswordReqVO
- Permission: `system:user:update-password`
- ErrorCode: USER_NOT_EXISTS

### FR-USER-010 修改用户状态

- source_confidence: high
- Controller / Router: UserController#updateUserStatus，`PUT /system/user/update-status`
- Service: AdminUserServiceImpl#updateUserStatus
- Request DTO / VO: UserUpdateStatusReqVO
- Permission: `system:user:update`
- ErrorCode: USER_NOT_EXISTS

### FR-USER-011 用户导出

- source_confidence: high
- Controller / Router: UserController#exportUserList，`GET /system/user/export-excel`
- Service: AdminUserServiceImpl#getUserPage
- Response DTO / VO: UserRespVO
- Permission: `system:user:export`

### FR-USER-012 用户导入模板下载

- source_confidence: high
- Controller / Router: UserController#importTemplate，`GET /system/user/get-import-template`
- DTO / VO: UserImportExcelVO
- Permission: 无显式 PreAuthorize

### FR-USER-013 用户导入

- source_confidence: high
- Controller / Router: UserController#importExcel，`POST /system/user/import`
- Service: AdminUserServiceImpl#importUserList
- Request DTO / VO: UserImportExcelVO
- Response DTO / VO: UserImportRespVO
- Permission: `system:user:import`
- ErrorCode: USER_IMPORT_LIST_IS_EMPTY、USER_IMPORT_INIT_PASSWORD、USER_USERNAME_EXISTS

### FR-USER-014 免鉴权精简用户查询

- source_confidence: high
- Controller / Router: UserController#getSimpleUser，`GET /system/user/get-simple`
- Service: AdminUserServiceImpl#getUser
- Permission: 无显式 PreAuthorize

### FR-USER-015 按昵称模糊搜索精简用户

- source_confidence: high
- Controller / Router: UserController#getSimpleUserListByNickname，`GET /system/user/list-by-nickname`
- Service: AdminUserServiceImpl#getUserListByNickname
- Mapper: AdminUserMapper#selectListByNickname
- Permission: 无显式 PreAuthorize

## 字段规则 Evidence

- username：UserSaveReqVO `@NotBlank`、`@Pattern`、`@Size(4,30)`；AdminUserServiceImpl#validateUsernameUnique；AdminUserMapper#selectByUsername。
- nickname：UserSaveReqVO `@Size(max=30)`。
- email：UserSaveReqVO `@Email`、`@Size(max=50)`；AdminUserServiceImpl#validateEmailUnique；AdminUserMapper#selectByEmail。
- mobile：UserSaveReqVO `@Mobile`；AdminUserServiceImpl#validateMobileUnique；AdminUserMapper#selectByMobile。
- password：UserSaveReqVO `@Length(4,16)` 和 `isPasswordValid`；UserUpdatePasswordReqVO `@NotEmpty`、`@Length(4,16)`。
- status：UserUpdateStatusReqVO `@InEnum(CommonStatusEnum)`、`@InDict(COMMON_STATUS)`；AdminUserDO#status。
- page query：UserPageReqVO username、mobile、status、createTime、deptId、roleId；AdminUserMapper#selectPage。

## 业务规则 Evidence

- 租户账号配额：AdminUserServiceImpl#createUser 中 tenantService.handleTenantInfo 与 USER_COUNT_MAX。
- 唯一性校验：validateUsernameUnique、validateMobileUnique、validateEmailUnique。
- 部门岗位有效性：validateUserForCreateOrUpdate 调用 deptService.validateDeptList 与 postService.validatePostList。
- 修改不更新密码：AdminUserServiceImpl#updateUser 调用 `updateReqVO.setPassword(null)`。
- 删除清理关联：deleteUser 调用 permissionService.processUserDeleted 与 userPostMapper.deleteByUserId。
- 禁用删除 token：updateUserStatus 中 CommonStatusEnum.isDisable 后 removeAccessToken。
- 导入逐行处理：importUserList 中 createUsernames、updateUsernames、failureUsernames。

## 权限规则 Evidence

- `system:user:create`：UserController#createUser。
- `system:user:update`：UserController#updateUser 与 updateUserStatus。
- `system:user:delete`：UserController#deleteUser 与 deleteUserList。
- `system:user:update-password`：UserController#updateUserPassword。
- `system:user:query`：UserController#getUserPage、getUserList、getUser。
- `system:user:export`：UserController#exportUserList。
- `system:user:import`：UserController#importExcel。
- 无显式权限：getSimpleUserList、importTemplate、getSimpleUser、getSimpleUserListByNickname。

## 异常处理 Evidence

- USER_USERNAME_EXISTS：ErrorCodeConstants；validateUsernameUnique。
- USER_MOBILE_EXISTS：ErrorCodeConstants；validateMobileUnique。
- USER_EMAIL_EXISTS：ErrorCodeConstants；validateEmailUnique。
- USER_NOT_EXISTS：ErrorCodeConstants；validateUserExists。
- USER_IMPORT_LIST_IS_EMPTY：ErrorCodeConstants；importUserList。
- USER_IMPORT_INIT_PASSWORD：ErrorCodeConstants；importUserList。
- USER_COUNT_MAX：ErrorCodeConstants；createUser。
- USER_IS_DISABLE：ErrorCodeConstants；validateUserList。

## 验收标准 Evidence

- AC-USER-001：分页查询条件、部门子树、角色筛选来自 getUserPage、getDeptCondition、AdminUserMapper#selectPage。
- AC-USER-002：新增成功和重复校验来自 createUser 与唯一性校验方法。
- AC-USER-003：修改不更新密码来自 updateUser 中 setPassword(null)。
- AC-USER-004：删除清理关联来自 deleteUser。
- AC-USER-005：禁用删除 token 来自 updateUserStatus。
- AC-USER-006：导入结果分类来自 importUserList。

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
