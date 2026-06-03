# RuoYi 用户管理 SRS v2 基准拆解

## 1. 基准目标

以 `docs/ruoyi-user-management-srs-v2.pdf` 作为验收基准，后续从源码重新逆向生成 SRS 时，需要尽量拟合其结构、覆盖范围和表达方式。

---

## 2. 既有 SRS v2 章节结构

```text
1 Introduction
  1.1 Purpose
  1.2 Scope
  1.3 Definitions
2 Overall Description
  2.1 User Classes
  2.2 Product Perspective
  2.3 Business Process Overview
3 System Features
  3.1 User Management Functional Requirements
  3.2 Page and Interaction Requirements
  3.3 Data Requirements
  3.4 Business Rules
  3.5 Permission Requirements
  3.6 Error Handling and Messages
4 Non-functional Requirements
  4.1 Security
  4.2 Usability
  4.3 Performance and Maintainability
5 Acceptance Criteria
6 Boundaries and Exclusions
```

---

## 3. 必须覆盖的功能点

| 编号 | 功能 | 基准要求 |
|------|------|----------|
| FR-USER-001 | 用户列表查询 | 支持按用户账号、手机号码、状态、创建时间、部门、角色筛选；按部门筛选包含下级部门；分页展示 |
| FR-USER-002 | 启用用户精简列表 | 返回状态正常用户，用于下拉选择场景 |
| FR-USER-003 | 用户详情 | 可查看基础资料、部门、岗位、状态、创建时间、最后登录信息；不存在时返回空结果 |
| FR-USER-004 | 新增用户 | 必填用户账号、用户昵称、密码；可选部门、岗位、手机号、邮箱、性别、备注、头像；默认正常状态 |
| FR-USER-005 | 创建校验 | 校验租户账号数量、账号唯一性、手机号唯一性、邮箱唯一性、部门和岗位可用性 |
| FR-USER-006 | 编辑用户 | 可编辑昵称、手机号、邮箱、部门、岗位、性别、头像、备注；普通编辑不修改密码和状态 |
| FR-USER-007 | 删除用户 | 支持单个/批量删除；删除后清理角色关联和岗位关联；不存在时失败提示 |
| FR-USER-008 | 重置密码 | 支持管理员重置密码；密码必须符合规则 |
| FR-USER-009 | 修改账号状态 | 支持启用/停用；停用用户不能继续登录或使用后台功能 |
| FR-USER-010 | 用户导入 | 支持模板下载和导入；使用配置中的初始密码；初始密码为空时导入失败 |
| FR-USER-011 | 导入更新与校验 | 支持允许更新已存在用户；逐条校验并返回成功/失败明细 |
| FR-USER-012 | 用户导出 | 可按当前查询条件导出用户数据 |

---

## 4. 字段规则基准

| 字段 | 必填 | 规则 |
|------|------|------|
| 用户账号 | 是 | 新增必填；登录标识；系统内唯一；只能包含字母和数字；长度 4 到 30 个字符 |
| 用户昵称 | 是 | 新增必填；用于展示；长度不超过 30 个字符 |
| 密码 | 新增/重置必填 | 长度 4 到 16 位；不在列表或详情中明文展示 |
| 手机号码 | 否 | 如果填写，必须符合手机号格式，并且系统内唯一 |
| 邮箱 | 否 | 如果填写，必须符合邮箱格式，长度不超过 50 个字符，并且系统内唯一 |
| 部门 | 否 | 如果选择，只能选择可用部门；列表支持按部门筛选 |
| 岗位 | 否 | 可选择一个或多个岗位；如果选择，只能选择可用岗位 |
| 账号状态 | 系统控制 | 新增默认正常；通过独立启用/停用功能修改 |
| 性别 | 否 | 使用系统字典值 |
| 备注 | 否 | 用户补充说明 |
| 头像 | 否 | 用户头像地址 |

---

## 5. 业务规则基准

- 用户账号必须唯一。
- 手机号和邮箱填写后必须唯一。
- 用户账号保存后作为后台登录标识。
- 用户密码不得明文展示。
- 新增用户时状态默认为正常，不支持选择初始状态。
- 创建用户前校验当前租户账号数量是否已达上限。
- 停用用户不能登录后台系统。
- 已登录用户被停用后，系统删除其登录凭证。
- 删除用户时清理用户角色关联和岗位关联数据。
- 新增或编辑用户时，选择的部门和岗位必须可用。
- 查询部门用户时，应包含所选部门及其下级部门。
- 导入用户时逐条校验并返回成功和失败结果。

---

## 6. 权限规则基准

| 权限场景 | 基准要求 |
|----------|----------|
| 访问控制 | 未登录用户不能访问用户管理页面；无查看权限不能访问列表和详情 |
| 新增/编辑/删除 | 无对应权限不能新增、修改资料、修改状态或删除用户 |
| 密码/导入/导出 | 无重置密码、导入、导出权限不能执行对应操作 |
| 前后端一致性 | 页面按钮根据权限动态展示，后端必须进行权限校验 |

---

## 7. 异常处理基准

| 异常场景 | 处理要求 |
|----------|----------|
| 用户账号重复 | 阻止创建或保存，并提示账号已存在 |
| 手机号码重复 | 阻止创建或保存，并提示手机号已存在 |
| 邮箱重复 | 阻止创建或保存，并提示邮箱已存在 |
| 用户不存在 | 查看详情返回空结果；编辑、删除、重置密码或修改状态时提示用户不存在 |
| 部门或岗位不可用 | 提示所选部门不可用或所选岗位不可用 |
| 密码格式不符合规则 | 阻止提交，并提示密码规则 |
| 导入文件为空或无有效数据 | 提示导入数据不能为空 |
| 导入初始密码为空 | 阻止导入，并提示初始密码不能为空 |
| 导入部分失败 | 展示失败明细，便于管理员修正后重新导入 |

---

## 8. 验收标准基准

| 验收项 | 验收标准 |
|--------|----------|
| 用户列表 | 管理员进入用户管理页面后可以看到列表；可以按账号、手机号、状态、创建时间、部门和角色筛选；无结果时展示空数据提示 |
| 新增用户 | 填写账号、昵称和密码后可创建；状态默认为正常；账号、手机号、邮箱重复或字段格式不合法时阻止提交并提示原因 |
| 编辑用户 | 可修改基础资料；成功后列表和详情展示最新数据；普通编辑入口不提供密码修改和状态修改 |
| 删除用户 | 删除前确认；确认后用户从列表移除；同时清理用户角色关联和岗位关联 |
| 重置密码 | 合法新密码可重置；不符合规则时阻止提交并提示原因 |
| 导入导出 | 可下载模板并导入合法数据；导入错误展示失败明细；可按查询条件导出用户数据 |

---

## 9. 边界范围基准

- 只维护后台系统用户。
- 不维护前台会员用户。
- 用户角色分配属于权限管理能力，不在本模块展开。
- 部门和岗位的新增、编辑、删除由对应管理模块负责。
- 菜单和按钮权限配置由菜单管理和角色管理负责。
- 第三方登录、OAuth2 授权和社交账号绑定不属于本模块范围。

---

## 10. 已定位源码依据

### 10.1 后端 Controller

- `/root/projects/github/ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/admin/user/UserController.java`
  - 新增用户：`POST /system/user/create`
  - 修改用户：`PUT /system/user/update`
  - 删除用户：`DELETE /system/user/delete`
  - 批量删除：`DELETE /system/user/delete-list`
  - 重置密码：`PUT /system/user/update-password`
  - 修改状态：`PUT /system/user/update-status`
  - 分页查询：`GET /system/user/page`
  - 精简列表：`GET /system/user/list-all-simple` / `/simple-list`
  - 详情：`GET /system/user/get`
  - 导出：`GET /system/user/export-excel`
  - 导入模板：`GET /system/user/get-import-template`
  - 导入：`POST /system/user/import`

### 10.2 后端 Service

- `/root/projects/github/ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/service/user/AdminUserServiceImpl.java`
  - 创建用户默认启用
  - 创建前校验租户账号数量
  - 校验用户名、手机号、邮箱唯一性
  - 校验部门和岗位可用性
  - 编辑用户不更新密码
  - 停用用户删除 access token
  - 删除用户清理角色关系和岗位关系
  - 导入用户校验初始密码和空列表
  - 导入支持更新已存在用户

### 10.3 请求与响应 VO

- `/root/projects/github/ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/admin/user/vo/user/UserSaveReqVO.java`
  - username：必填，正则 `^[a-zA-Z0-9]{4,30}$`，长度 4-30
  - nickname：长度不超过 30
  - email：邮箱格式，长度不超过 50
  - mobile：手机号格式
  - password：新增必填，长度 4-16
  - deptId、postIds、sex、avatar、remark 可选

- `/root/projects/github/ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/admin/user/vo/user/UserPageReqVO.java`
  - 支持 username、mobile、status、createTime、deptId、roleId 筛选

- `/root/projects/github/ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/admin/user/vo/user/UserRespVO.java`
  - 返回用户编号、账号、昵称、部门、岗位、邮箱、手机号、性别、头像、状态、最后登录 IP、最后登录时间、创建时间

- `/root/projects/github/ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/admin/user/vo/user/UserImportExcelVO.java`
  - 导入字段包括登录名称、用户名称、部门编号、邮箱、手机号、性别、账号状态

### 10.4 数据模型与查询

- `/root/projects/github/ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/dal/dataobject/user/AdminUserDO.java`
  - 用户数据模型字段：id、username、password、nickname、remark、deptId、postIds、email、mobile、sex、avatar、status、loginIp、loginDate

- `/root/projects/github/ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/dal/mysql/user/AdminUserMapper.java`
  - 支持按 username、mobile、status、createTime、deptId、roleId 相关 userIds 分页查询
  - 支持按 username、email、mobile 查询唯一性

### 10.5 错误码与权限数据

- `/root/projects/github/ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/enums/ErrorCodeConstants.java`
  - 用户账号已存在
  - 手机号已存在
  - 邮箱已存在
  - 用户不存在
  - 导入用户数据不能为空
  - 用户密码校验失败
  - 用户已被禁用
  - 超过租户账号配额
  - 初始密码不能为空

- `/root/projects/github/ruoyi-vue-pro/sql/mysql/ruoyi-vue-pro.sql`
  - 用户管理菜单：`system:user:list`
  - 用户查询：`system:user:query`
  - 用户新增：`system:user:create`
  - 用户修改：`system:user:update`
  - 用户删除：`system:user:delete`
  - 用户导出：`system:user:export`
  - 用户导入：`system:user:import`
  - 重置密码：`system:user:update-password`
  - 初始密码配置：`system.user.init-password`

---

## 11. 下一步生成要求

后续逆向生成 SRS 初稿时，应严格以本基准拆解为验收标准：

1. 章节结构必须覆盖既有 SRS v2 的主要章节。
2. 功能点必须覆盖 FR-USER-001 到 FR-USER-012。
3. 字段规则必须与源码 VO 校验保持一致。
4. 异常处理必须覆盖错误码中与用户管理相关的错误。
5. 权限规则必须覆盖 SQL 菜单权限和 Controller `@PreAuthorize` 权限。
6. 输出文档必须使用连续段落表达，避免过度碎片化 bullet。
