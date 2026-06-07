# Scope Confirmation

## Final Included Scope

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

## Explicit Exclusions

- 部门、角色、岗位的独立管理能力
- 个人中心旧密码校验流程
- 用户注册能力
- OAuth2 完整认证与授权流程
- IM 好友管理能力

## Risk Items

| 风险项 | 影响 | 处理 |
|---|---|---|
| 部门、岗位、OAuth2 在本模块中作为依赖出现 | 易被误写成主功能 | 仅在业务规则或副作用中引用，不扩写为主需求 |

## Confirmation Result

```text
status: confirmed
mode: autonomous_confirm
```
