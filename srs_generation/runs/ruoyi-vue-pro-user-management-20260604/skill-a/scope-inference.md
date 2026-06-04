# Scope Inference

## 基本信息

```text
source_project: g:/work/genlot/projects/ruoyi-vue-pro
target_module: system user management
status: confirmed
```

## 入口发现

### Controller / Router

- UserController.java：`@RequestMapping("/system/user")`，覆盖用户新增、修改、删除、批量删除、重置密码、修改状态、分页查询、列表查询、精简列表、详情、导出、导入模板、导入，以及两个免鉴权精简查询接口。

### Service

- AdminUserServiceImpl.java：覆盖 createUser、updateUser、deleteUser、deleteUserList、updateUserPassword、updateUserStatus、getUserPage、getUserList、getUserListByStatus、getDeptUsers、getUserListByNickname、importUserList 等逻辑。

### DTO / VO / Schema

- UserSaveReqVO.java：新增/修改字段规则。
- UserPageReqVO.java：分页查询条件。
- UserRespVO.java：用户响应和导出字段。
- UserImportExcelVO.java：导入模板字段。
- UserImportRespVO.java：导入结果结构。
- UserUpdatePasswordReqVO.java：重置密码字段规则。
- UserUpdateStatusReqVO.java：状态修改字段规则。

### Entity / Mapper / SQL

- AdminUserDO.java：用户数据对象和状态字段。
- AdminUserMapper.java：用户名、邮箱、手机号唯一查询，分页筛选，昵称模糊查询，状态查询，部门查询。

### Permission

- `system:user:create`
- `system:user:update`
- `system:user:delete`
- `system:user:update-password`
- `system:user:query`
- `system:user:export`
- `system:user:import`

### ErrorCode

- USER_USERNAME_EXISTS
- USER_MOBILE_EXISTS
- USER_EMAIL_EXISTS
- USER_NOT_EXISTS
- USER_IMPORT_LIST_IS_EMPTY
- USER_PASSWORD_FAILED
- USER_IS_DISABLE
- USER_COUNT_MAX
- USER_IMPORT_INIT_PASSWORD
- USER_REGISTER_DISABLED

## 候选纳入范围

- 用户分页查询
- 用户列表查询
- 用户精简列表查询
- 用户详情查询
- 用户新增
- 用户修改
- 用户删除
- 用户批量删除
- 重置用户密码
- 修改用户状态
- 用户导出
- 用户导入模板下载
- 用户导入
- 免鉴权精简用户查询
- 按昵称模糊搜索用户精简信息

## 待确认相邻能力

- 部门树筛选：作为依赖说明，不展开部门管理需求。
- 角色筛选：作为查询条件依赖，不展开角色管理需求。
- 岗位关联：作为用户保存规则的一部分说明，不展开岗位管理需求。
- OAuth2 token 删除：作为禁用用户后的副作用说明，不展开认证模块。
- IM 名片和加好友搜索：作为免鉴权接口使用场景说明，不展开 IM 模块需求。

## 建议排除范围

- 部门管理 CRUD
- 角色管理 CRUD
- 岗位管理 CRUD
- 用户个人中心资料修改
- 用户注册
- OAuth2 认证流程
- IM 好友管理流程

## 自动确认结论

```text
status: confirmed
reason: 用户管理 Controller、Service、VO、Mapper、错误码入口完整，核心功能范围清晰；相邻能力已作为依赖说明或排除项记录。
```

## 风险项

- 免鉴权精简用户查询接口属于用户管理 Controller，但主要服务于 IM 等场景；本次纳入为用户管理扩展查询能力，不展开 IM 流程。
- 部门、角色、岗位均参与用户规则，但不作为独立模块展开。
