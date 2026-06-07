`# Scope Inference

## Candidate In-Scope Features

- 用户分页查询
- 用户详情查询
- 用户精简列表查询
- 用户新增
- 用户修改
- 用户删除
- 用户批量删除
- 重置用户密码
- 修改用户状态
- 用户导出
- 用户导入模板下载
- 用户导入

## Adjacent Capabilities To Exclude

- 部门管理本身
- 角色管理本身
- 岗位管理本身
- 用户个人中心修改密码流程
- 用户注册流程
- OAuth2 完整认证流程
- IM 好友管理流程

## Scope Decision

```text
status: confirmed
confidence: high
reason: Controller 入口、Service 逻辑、请求对象与错误码能够形成完整闭环；相邻能力仅作为依赖或副作用出现。
```
