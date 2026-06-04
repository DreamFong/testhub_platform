# Scope Confirmation

## 基本信息

```text
project: ruoyi-vue-pro
target_module: system user management
scope_confirm_status: confirmed
confirmed_by: autonomous_source_evidence
confirmed_at: 2026-06-04
```

## 最终纳入范围

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

## 明确排除范围

- 部门管理 CRUD
- 角色管理 CRUD
- 岗位管理 CRUD
- 用户个人中心资料修改
- 用户注册
- OAuth2 认证流程
- IM 好友管理流程

## 作为依赖说明但不展开的能力

- 部门树筛选和部门名称拼接
- 角色筛选用户 ID
- 岗位有效性校验和用户岗位关联维护
- 禁用用户后删除 OAuth2 token
- 昵称或头像变更后发送用户资料更新消息

## Scope 风险项

| 风险 | 影响 | 处理方式 | 是否阻断 |
|---|---|---|---|
| 免鉴权精简接口服务于 IM 场景 | 可能扩大用户管理边界 | 纳入用户查询能力，但不展开 IM 流程 | 否 |
| 部门、角色、岗位参与用户规则 | 可能误纳入相邻模块 | 作为依赖说明，不展开 CRUD | 否 |
