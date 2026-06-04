# RuoYi-Vue-Pro 用户管理模块 SRS

## 1. 文档概述

本文档描述 RuoYi-Vue-Pro 管理后台用户管理模块的需求规格。文档基于用户管理相关 Controller、Service、VO、DO、Mapper 和错误码源码逆向生成，默认面向知识库构建场景，采用连续段落和稳定编号，减少复杂表格依赖。

## 2. 模块范围

本模块覆盖用户分页查询、用户列表查询、用户精简列表查询、用户详情查询、用户新增、用户修改、用户删除、用户批量删除、重置用户密码、修改用户状态、用户导出、用户导入模板下载、用户导入、免鉴权精简用户查询以及按昵称模糊搜索精简用户。

本模块不展开部门管理、角色管理、岗位管理、用户个人中心、用户注册、OAuth2 认证流程和 IM 好友管理流程。部门、角色、岗位、OAuth2 token 和 IM 场景只作为用户管理中的依赖、筛选条件或副作用说明。

## 3. 角色与权限概述

用户管理的后台管理能力由权限码控制。新增用户需要 `system:user:create` 权限，修改用户和修改状态需要 `system:user:update` 权限，删除和批量删除需要 `system:user:delete` 权限，重置密码需要 `system:user:update-password` 权限，分页、列表和详情查询需要 `system:user:query` 权限，导出需要 `system:user:export` 权限，导入需要 `system:user:import` 权限。

用户精简列表、导入模板下载、免鉴权精简用户查询和按昵称模糊搜索精简用户在 Controller 中没有显式 `PreAuthorize` 权限注解，应作为特殊入口记录。

## 4. 功能需求

### FR-USER-001 用户分页查询

系统应支持后台管理员通过 `GET /system/user/page` 分页查询用户。查询条件包括用户账号、手机号码、状态、创建时间范围、部门编号和角色编号。用户账号和手机号码采用模糊匹配，状态采用精确匹配，创建时间采用范围匹配。

当传入部门编号时，系统应将该部门及其子部门共同作为筛选条件。当传入角色编号时，系统应先查询该角色关联的用户编号集合；如果角色下没有用户，系统应返回空分页结果。查询结果按用户 ID 倒序排列，并在返回前拼接部门信息。

该功能需要 `system:user:query` 权限。

### FR-USER-002 用户列表查询

系统应支持后台管理员通过 `GET /system/user/list` 按用户 ID 列表查询用户详情列表。若查询结果为空，系统应返回空列表；若查询到用户，系统应拼接用户所属部门信息后返回。

该功能需要 `system:user:query` 权限。

### FR-USER-003 用户精简列表查询

系统应支持通过 `GET /system/user/list-all-simple` 或 `GET /system/user/simple-list` 获取精简用户列表。该能力主要用于前端下拉选择等场景。

当请求包含部门编号时，系统应返回该部门下的用户；当请求未包含部门编号时，系统应只返回状态为启用的用户。系统应在返回前拼接部门信息。

该功能在 Controller 中无显式权限注解。

### FR-USER-004 用户详情查询

系统应支持后台管理员通过 `GET /system/user/get` 按用户 ID 查询用户详情。若用户不存在，系统应返回 null；若用户存在，系统应返回用户详情并拼接部门信息。

该功能需要 `system:user:query` 权限。

### FR-USER-005 用户新增

系统应支持后台管理员通过 `POST /system/user/create` 新增用户。新增用户时，用户账号必填，且只能由数字和字母组成，长度为 4-30 个字符。新增时密码必填，长度为 4-16 位。邮箱必须符合邮箱格式且长度不超过 50，手机号必须符合手机号格式。

系统在新增前应检查租户账号数量是否超过配额；如果超过配额，应返回 `USER_COUNT_MAX`。系统还应校验用户名、手机号和邮箱唯一性，分别对应 `USER_USERNAME_EXISTS`、`USER_MOBILE_EXISTS` 和 `USER_EMAIL_EXISTS`。系统应校验部门和岗位有效。新增成功后，系统应将用户状态设置为启用，对密码加密保存，并维护用户岗位关联。

该功能需要 `system:user:create` 权限。

### FR-USER-006 用户修改

系统应支持后台管理员通过 `PUT /system/user/update` 修改用户。修改前系统应校验用户存在；如果用户不存在，应返回 `USER_NOT_EXISTS`。系统还应校验用户名、手机号和邮箱唯一性，并校验部门和岗位有效。

修改用户时，通用保存接口不更新密码。系统应更新用户基础信息和岗位关联。当昵称或头像发生变化时，系统应发送用户资料更新消息供下游订阅。

该功能需要 `system:user:update` 权限。

### FR-USER-007 用户删除

系统应支持后台管理员通过 `DELETE /system/user/delete` 删除单个用户。删除前系统应校验用户存在；如果用户不存在，应返回 `USER_NOT_EXISTS`。删除用户后，系统应清理该用户的权限关联和岗位关联。

该功能需要 `system:user:delete` 权限。

### FR-USER-008 用户批量删除

系统应支持后台管理员通过 `DELETE /system/user/delete-list` 批量删除用户。系统应根据传入的用户 ID 集合批量删除用户记录，并逐个清理权限关联和岗位关联。

该功能需要 `system:user:delete` 权限。

### FR-USER-009 重置用户密码

系统应支持后台管理员通过 `PUT /system/user/update-password` 重置用户密码。请求中的用户 ID 必填，新密码必填且长度为 4-16 位。系统应先校验目标用户存在；若用户不存在，应返回 `USER_NOT_EXISTS`。系统保存密码时必须进行加密处理。

该功能需要 `system:user:update-password` 权限。

### FR-USER-010 修改用户状态

系统应支持后台管理员通过 `PUT /system/user/update-status` 修改用户状态。请求中的用户 ID 和状态必填，状态必须属于 `CommonStatusEnum`，并符合通用状态字典。

系统应先校验用户存在；若用户不存在，应返回 `USER_NOT_EXISTS`。当用户被修改为禁用状态时，系统应删除该用户的后台 OAuth2 token，使其后续无法继续使用已发放的后台访问令牌。

该功能需要 `system:user:update` 权限。

### FR-USER-011 用户导出

系统应支持后台管理员通过 `GET /system/user/export-excel` 导出用户数据。导出功能使用与分页查询相同的筛选条件，但应将分页大小设置为不分页，导出所有符合条件的用户。导出结果使用 `UserRespVO` 定义的 Excel 字段，并拼接部门信息。

该功能需要 `system:user:export` 权限。

### FR-USER-012 用户导入模板下载

系统应支持通过 `GET /system/user/get-import-template` 下载用户导入模板。模板应包含示例用户数据，字段来自 `UserImportExcelVO`，包括登录名称、用户名称、部门编号、用户邮箱、手机号码、用户性别和账号状态。

该功能在 Controller 中无显式权限注解。

### FR-USER-013 用户导入

系统应支持后台管理员通过 `POST /system/user/import` 导入用户 Excel 文件。请求应包含 Excel 文件和可选的 `updateSupport` 参数。`updateSupport` 默认为 false，表示用户名已存在时不更新。

系统应读取 Excel 为用户导入列表。若导入列表为空，应返回 `USER_IMPORT_LIST_IS_EMPTY`。系统应读取用户初始化密码配置；若初始化密码为空，应返回 `USER_IMPORT_INIT_PASSWORD`。系统逐行校验字段和业务规则，校验失败时将失败原因写入导入结果。若用户名不存在，系统应创建用户并使用初始化密码加密保存；若用户名已存在且 `updateSupport=false`，系统应记录失败；若用户名已存在且 `updateSupport=true`，系统应更新该用户。

导入结果应分别返回创建成功的用户名列表、更新成功的用户名列表和失败用户名及原因。

该功能需要 `system:user:import` 权限。

### FR-USER-014 免鉴权精简用户查询

系统应支持通过 `GET /system/user/get-simple` 按用户 ID 查询精简用户信息。该接口用于点头像弹名片等场景，在 Controller 中无显式权限注解。若用户不存在，系统应返回 null；若用户存在，系统应返回精简用户信息，并在可能的情况下拼接部门信息。

### FR-USER-015 按昵称模糊搜索精简用户

系统应支持通过 `GET /system/user/list-by-nickname` 按昵称关键词模糊搜索精简用户信息。该接口用于加好友等场景，在 Controller 中无显式权限注解。若昵称为空，系统应返回空列表；若昵称非空，系统应去除首尾空白后按昵称模糊匹配用户，并拼接部门信息。

## 5. 字段与输入规则

用户账号 `username` 必填，只能由数字和字母组成，长度为 4-30 个字符，并且在用户表中必须唯一。用户昵称 `nickname` 长度不能超过 30 个字符。用户邮箱 `email` 必须符合邮箱格式，长度不能超过 50 个字符，并且必须唯一。手机号 `mobile` 必须符合手机号格式，并且必须唯一。

新增用户时，密码 `password` 必填，长度为 4-16 位。修改用户时，通用保存接口不会更新密码；密码变更必须通过重置密码功能完成。重置密码时，用户 ID 必填，新密码必填且长度为 4-16 位。

用户状态修改时，用户 ID 和状态均必填。状态必须属于 `CommonStatusEnum`，并符合通用状态字典。分页查询支持用户账号、手机号、状态、创建时间、部门编号和角色编号作为查询条件，其中部门编号会扩展到子部门，角色编号会转换为关联用户 ID 集合。

导入用户模板字段包括登录名称、用户名称、部门编号、用户邮箱、手机号码、用户性别和账号状态。导入时这些字段会被转换为用户保存请求进行校验，并使用系统配置中的初始化密码。

## 6. 业务规则

新增用户前，系统必须检查租户账号数量是否超过租户配额。新增和修改用户时，系统必须校验用户名、手机号、邮箱唯一性，并校验部门和岗位是否有效。为了避免数据权限影响唯一性判断，相关校验在忽略数据权限的上下文中执行。

修改用户时，系统不会通过通用保存接口更新密码。岗位关联通过新增和删除差异集合进行维护。用户昵称或头像发生变化时，系统会发送用户资料更新消息，供 IM 等下游模块订阅。

删除用户时，系统删除用户记录后还会清理权限关联和岗位关联。批量删除用户时，系统会批量删除用户记录，并逐个清理相关权限和岗位关系。

修改用户状态时，如果目标状态为禁用，系统会删除该用户的后台 OAuth2 token。

用户导入时，系统必须保证导入列表非空，并且初始化密码配置存在。导入过程逐行处理，每一行根据校验结果进入创建成功、更新成功或失败结果集合。

## 7. 异常处理规则

当用户名已被占用时，系统返回 `USER_USERNAME_EXISTS`。当手机号已被占用时，系统返回 `USER_MOBILE_EXISTS`。当邮箱已被占用时，系统返回 `USER_EMAIL_EXISTS`。当更新、删除、重置密码或状态修改的目标用户不存在时，系统返回 `USER_NOT_EXISTS`。

当导入用户数据为空时，系统返回 `USER_IMPORT_LIST_IS_EMPTY`。当导入所需的初始化密码配置为空时，系统返回 `USER_IMPORT_INIT_PASSWORD`。当新增用户超过租户账号配额时，系统返回 `USER_COUNT_MAX`。

`USER_PASSWORD_FAILED` 和 `USER_IS_DISABLE` 在用户服务中存在，但分别主要用于个人中心旧密码校验和用户集合有效性校验，不作为本次管理后台用户 CRUD 主流程的核心异常展开。

## 8. 验收标准

### FR-USER-001 验收标准

当管理员具备 `system:user:query` 权限并提交分页查询条件时，系统应返回符合条件的用户分页结果。部门筛选应包含子部门，角色筛选应正确转换为用户 ID 集合。无匹配角色用户时，系统应返回空分页结果。

### FR-USER-005 验收标准

当管理员具备 `system:user:create` 权限并提交合法用户信息时，系统应新增用户并返回用户 ID。新增用户默认启用，密码应加密保存。若用户名、手机号或邮箱重复，系统应返回对应错误码。

### FR-USER-006 验收标准

当管理员具备 `system:user:update` 权限并修改存在的用户时，系统应更新用户基础信息和岗位关联，但不应通过该接口更新密码。目标用户不存在时，系统应返回 `USER_NOT_EXISTS`。

### FR-USER-007 验收标准

当管理员具备 `system:user:delete` 权限并删除存在的用户时，系统应删除用户记录，并清理权限关联和岗位关联。目标用户不存在时，系统应返回 `USER_NOT_EXISTS`。

### FR-USER-010 验收标准

当管理员具备 `system:user:update` 权限并将用户状态修改为禁用时，系统应更新用户状态，并删除该用户后台 OAuth2 token。

### FR-USER-013 验收标准

当管理员具备 `system:user:import` 权限并上传有效 Excel 文件时，系统应逐行处理用户数据，并返回创建成功、更新成功和失败明细。导入列表为空时，应返回 `USER_IMPORT_LIST_IS_EMPTY`；初始化密码为空时，应返回 `USER_IMPORT_INIT_PASSWORD`。

## 9. 明确排除项

本 SRS 不描述部门管理、角色管理、岗位管理、用户个人中心、用户注册、OAuth2 认证流程和 IM 好友管理流程。上述能力只在影响用户管理功能时作为依赖、筛选条件或副作用说明。

## 10. 源码依据说明

本 SRS 的主要依据包括 `UserController.java`、`AdminUserServiceImpl.java`、`UserSaveReqVO.java`、`UserPageReqVO.java`、`UserRespVO.java`、`UserImportExcelVO.java`、`UserUpdatePasswordReqVO.java`、`UserUpdateStatusReqVO.java`、`AdminUserDO.java`、`AdminUserMapper.java` 和 `ErrorCodeConstants.java`。详细映射见 `source-evidence-map.md`。
