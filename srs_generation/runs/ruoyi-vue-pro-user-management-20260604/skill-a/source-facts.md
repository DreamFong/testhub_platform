# Source Facts

## 1. 功能点

### 用户新增

- 类型：新增
- 入口：`POST /system/user/create`
- Controller：UserController#createUser
- Service：AdminUserServiceImpl#createUser
- 请求对象：UserSaveReqVO
- 响应：用户 ID
- 权限码：`system:user:create`
- 主要规则：租户账号数不能超过配额；用户名、手机号、邮箱唯一；部门和岗位必须有效；新增用户默认启用；密码加密保存；保存岗位关联。
- 异常：USER_COUNT_MAX、USER_USERNAME_EXISTS、USER_MOBILE_EXISTS、USER_EMAIL_EXISTS。

### 用户修改

- 类型：编辑
- 入口：`PUT /system/user/update`
- Controller：UserController#updateUser
- Service：AdminUserServiceImpl#updateUser
- 请求对象：UserSaveReqVO
- 权限码：`system:user:update`
- 主要规则：修改时不更新密码；校验用户存在；用户名、手机号、邮箱唯一；部门和岗位有效；更新岗位关联；昵称或头像变化时发送资料更新消息。
- 异常：USER_NOT_EXISTS、USER_USERNAME_EXISTS、USER_MOBILE_EXISTS、USER_EMAIL_EXISTS。

### 用户删除

- 类型：删除
- 入口：`DELETE /system/user/delete`
- Controller：UserController#deleteUser
- Service：AdminUserServiceImpl#deleteUser
- 权限码：`system:user:delete`
- 主要规则：删除前校验用户存在；删除用户记录；清理权限关联；删除用户岗位关联。
- 异常：USER_NOT_EXISTS。

### 用户批量删除

- 类型：批量删除
- 入口：`DELETE /system/user/delete-list`
- Controller：UserController#deleteUserList
- Service：AdminUserServiceImpl#deleteUserList
- 权限码：`system:user:delete`
- 主要规则：批量删除用户记录；逐个清理权限关联和岗位关联。

### 重置用户密码

- 类型：专项更新
- 入口：`PUT /system/user/update-password`
- Controller：UserController#updateUserPassword
- Service：AdminUserServiceImpl#updateUserPassword(Long, String)
- 请求对象：UserUpdatePasswordReqVO
- 权限码：`system:user:update-password`
- 主要规则：校验用户存在；新密码长度 4-16 位；密码加密保存。
- 异常：USER_NOT_EXISTS。

### 修改用户状态

- 类型：状态流转
- 入口：`PUT /system/user/update-status`
- Controller：UserController#updateUserStatus
- Service：AdminUserServiceImpl#updateUserStatus
- 请求对象：UserUpdateStatusReqVO
- 权限码：`system:user:update`
- 主要规则：校验用户存在；状态必须属于 CommonStatusEnum；禁用用户时删除该用户后台 OAuth2 token。
- 异常：USER_NOT_EXISTS。

### 用户分页查询

- 类型：查询
- 入口：`GET /system/user/page`
- Controller：UserController#getUserPage
- Service：AdminUserServiceImpl#getUserPage
- 请求对象：UserPageReqVO
- 响应对象：PageResult<UserRespVO>
- 权限码：`system:user:query`
- 查询条件：username、mobile、status、createTime、deptId、roleId。
- 主要规则：deptId 同时筛选子部门；roleId 先查询角色下用户 ID，无匹配时返回空分页；按用户 ID 倒序。

### 用户列表查询

- 类型：查询
- 入口：`GET /system/user/list`
- Controller：UserController#getUserList
- Service：AdminUserServiceImpl#getUserList
- 权限码：`system:user:query`
- 主要规则：按 ids 查询用户列表；空结果返回空列表；拼接部门信息。

### 用户精简列表查询

- 类型：查询
- 入口：`GET /system/user/list-all-simple` 与 `GET /system/user/simple-list`
- Controller：UserController#getSimpleUserList
- Service：AdminUserServiceImpl#getDeptUsers 或 getUserListByStatus
- 权限码：无显式 PreAuthorize
- 主要规则：传入 deptId 时查询该部门用户；未传 deptId 时仅返回启用用户；拼接部门信息。

### 用户详情查询

- 类型：详情
- 入口：`GET /system/user/get`
- Controller：UserController#getUser
- Service：AdminUserServiceImpl#getUser
- 权限码：`system:user:query`
- 主要规则：按 id 查询；用户不存在返回 null；存在时拼接部门信息。

### 用户导出

- 类型：导出
- 入口：`GET /system/user/export-excel`
- Controller：UserController#exportUserList
- Service：AdminUserServiceImpl#getUserPage
- 权限码：`system:user:export`
- 主要规则：使用 UserPageReqVO 筛选；pageSize 设置为不分页；导出 UserRespVO Excel。

### 用户导入模板下载

- 类型：导入导出
- 入口：`GET /system/user/get-import-template`
- Controller：UserController#importTemplate
- 权限码：无显式 PreAuthorize
- 主要规则：输出包含示例用户的 Excel 模板，字段来自 UserImportExcelVO。

### 用户导入

- 类型：导入
- 入口：`POST /system/user/import`
- Controller：UserController#importExcel
- Service：AdminUserServiceImpl#importUserList
- 请求：MultipartFile file，Boolean updateSupport
- 响应：UserImportRespVO
- 权限码：`system:user:import`
- 主要规则：导入列表不能为空；初始化密码配置不能为空；逐行校验字段；校验手机号、邮箱、部门；用户名不存在则创建；用户名存在且 updateSupport=false 时记录失败；updateSupport=true 时更新。
- 异常：USER_IMPORT_LIST_IS_EMPTY、USER_IMPORT_INIT_PASSWORD、USER_USERNAME_EXISTS、USER_MOBILE_EXISTS、USER_EMAIL_EXISTS。

### 免鉴权精简用户查询

- 类型：详情
- 入口：`GET /system/user/get-simple`
- Controller：UserController#getSimpleUser
- 权限码：无显式 PreAuthorize
- 主要规则：按 id 查询精简用户；用户不存在返回 null；可拼接部门信息。

### 按昵称模糊搜索精简用户

- 类型：查询
- 入口：`GET /system/user/list-by-nickname`
- Controller：UserController#getSimpleUserListByNickname
- Service：AdminUserServiceImpl#getUserListByNickname
- 权限码：无显式 PreAuthorize
- 主要规则：nickname 为空返回空列表；非空时 trim 后按昵称模糊查询；拼接部门信息。

## 2. 字段规则

### UserSaveReqVO

| 字段 | 规则 | 来源 | 置信度 |
|---|---|---|---|
| id | 用户编号；修改时用于定位用户；新增时为空 | UserSaveReqVO#id | high |
| username | 必填；由数字、字母组成；长度 4-30；唯一 | UserSaveReqVO 注解；validateUsernameUnique | high |
| nickname | 长度不超过 30 | UserSaveReqVO#nickname | high |
| email | 邮箱格式；长度不超过 50；唯一 | UserSaveReqVO 注解；validateEmailUnique | high |
| mobile | 手机号格式；唯一 | UserSaveReqVO#mobile；validateMobileUnique | high |
| password | 新增时必填；长度 4-16；修改时不更新 | UserSaveReqVO#isPasswordValid；updateUser setPassword(null) | high |
| deptId | 部门编号；保存时校验部门有效 | validateUserForCreateOrUpdate | high |
| postIds | 岗位编号集合；保存时校验岗位有效 | validateUserForCreateOrUpdate；updateUserPost | high |

### UserPageReqVO

| 字段 | 规则 | 来源 | 置信度 |
|---|---|---|---|
| username | 模糊匹配 | AdminUserMapper#selectPage | high |
| mobile | 模糊匹配 | AdminUserMapper#selectPage | high |
| status | 精确匹配 | AdminUserMapper#selectPage | high |
| createTime | 时间范围查询 | UserPageReqVO；AdminUserMapper#selectPage | high |
| deptId | 同时筛选子部门 | getDeptCondition | high |
| roleId | 先转换为用户 ID 集合 | getUserPage | high |

## 3. 业务规则

- 新增用户前必须检查租户账号数上限。
- 新增和修改都必须执行用户名、手机号、邮箱唯一性校验。
- 新增和修改都必须校验部门和岗位有效。
- 修改用户不通过通用保存接口更新密码。
- 删除用户会清理权限关联和岗位关联。
- 禁用用户会删除后台 OAuth2 token。
- 用户导入逐行处理，成功创建、成功更新、失败原因分别记录。
- 用户导入依赖初始化密码配置。

## 4. 权限规则

| 功能 | 权限码 | 来源 | 置信度 |
|---|---|---|---|
| 新增用户 | system:user:create | UserController#createUser | high |
| 修改用户 | system:user:update | UserController#updateUser | high |
| 删除用户 | system:user:delete | UserController#deleteUser / deleteUserList | high |
| 重置密码 | system:user:update-password | UserController#updateUserPassword | high |
| 修改状态 | system:user:update | UserController#updateUserStatus | high |
| 查询用户 | system:user:query | getUserPage / getUserList / getUser | high |
| 导出用户 | system:user:export | exportUserList | high |
| 导入用户 | system:user:import | importExcel | high |
| 精简查询 | 无显式权限注解 | getSimpleUserList / getSimpleUser / list-by-nickname | high |

## 5. 异常处理

| 异常 | 错误码 | 触发条件 | 来源 | 置信度 |
|---|---|---|---|---|
| 用户账号已存在 | USER_USERNAME_EXISTS | 用户名被其他用户占用 | validateUsernameUnique | high |
| 手机号已存在 | USER_MOBILE_EXISTS | 手机号被其他用户占用 | validateMobileUnique | high |
| 邮箱已存在 | USER_EMAIL_EXISTS | 邮箱被其他用户占用 | validateEmailUnique | high |
| 用户不存在 | USER_NOT_EXISTS | 更新、删除、重置密码、状态修改等目标用户不存在 | validateUserExists | high |
| 导入用户数据为空 | USER_IMPORT_LIST_IS_EMPTY | 导入列表为空 | importUserList | high |
| 初始密码为空 | USER_IMPORT_INIT_PASSWORD | 导入时初始化密码配置为空 | importUserList | high |
| 用户密码校验失败 | USER_PASSWORD_FAILED | 个人中心旧密码校验失败，不属于本轮管理后台主范围 | validateOldPassword | medium |
| 用户已禁用 | USER_IS_DISABLE | validateUserList 校验用户集合时用户禁用 | validateUserList | medium |
| 超过租户账号配额 | USER_COUNT_MAX | 新增或注册时用户数达到租户上限 | createUser / registerUser | high |

## 6. 验收要点

- 有 `system:user:create` 权限且输入合法时，新增用户返回用户 ID。
- 新增用户名重复时返回 USER_USERNAME_EXISTS。
- 修改用户时不通过保存接口更新密码。
- 删除用户时同步清理权限和岗位关联。
- 禁用用户后应删除对应后台 token。
- 分页查询按条件过滤，并支持部门子树和角色筛选。
- 导入用户应分别返回创建成功、更新成功和失败明细。
- PDF 和知识库友好 SRS 应能检索字段规则、异常处理和验收标准。
