# Apifox GUI 测试场景配置指南

## 前置条件

- Apifox 项目：芋道快速开发平台（ID: 8163797）
- 目标服务：ruoyi-vue-pro，`http://81.70.235.9:48080`
- 已导入 333 个接口、285 个 schema

---

## 第一步：环境配置

进入 Apifox → 环境管理 → 选择 `ruoyi-dev`

### 1.1 基本信息

- 前置 URL：`http://81.70.235.9:48080`

### 1.2 全局请求头

| Key | Value |
|-----|-------|
| `tenant-id` | `1` |

### 1.3 环境变量

| 变量名 | 远程值 | 本地值 | 说明 |
|--------|--------|--------|------|
| `accessToken` | 空 | 空 | 步骤1登录后自动提取 |
| `userId` | 空 | 空 | 步骤2创建用户后自动提取 |
| `username` | 空 | 空 | 步骤2创建用户后自动提取 |

---

## 第二步：创建测试场景

左侧导航 → 自动化测试 → 测试场景 → 新建场景

- 场景名称：`用户管理 CRUD 测试链`

---

## 第三步：编排 10 个步骤

每一步操作：添加步骤 → 发送请求 → 从接口列表中选择对应接口

### 步骤 1：登录获取 Token

- 接口：`POST /admin-api/system/auth/login`
- Body（JSON）：
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```
- 后置操作（提取变量）：
  - 提取 `accessToken`：从响应体 `$.data.accessToken` 提取
- 断言：
  - `$.code` 等于 `0`
  - `$.data.accessToken` 存在（类型为 string）

---

### 步骤 2：新增用户

- 接口：`POST /admin-api/system/user/create`
- Auth：Bearer Token = `{{accessToken}}`
- Body（JSON）：
  ```json
  {
    "username": "testuser_auto",
    "nickname": "测试用户",
    "password": "Test@1234",
    "mobile": "13900001111",
    "sex": 1
  }
  ```
- 后置操作（提取变量）：
  - 提取 `userId`：从响应体 `$.data` 提取（返回值就是用户 ID）
- 断言：
  - `$.code` 等于 `0`
  - `$.data` 存在（类型为 number）

> 注意：使用固定用户名 `testuser_auto`，重复运行前需手动删除上次创建的用户，或每次手动修改用户名。

---

### 步骤 3：查询用户详情

- 接口：`GET /admin-api/system/user/get`
- Query 参数：`id` = `{{userId}}`
- Auth：Bearer Token = `{{accessToken}}`
- 断言：
  - `$.code` 等于 `0`
  - `$.data.id` 等于 `{{userId}}`

---

### 步骤 4：分页查询用户列表

- 接口：`GET /admin-api/system/user/page`
- Query 参数：`pageNo` = `1`, `pageSize` = `10`
- Auth：Bearer Token = `{{accessToken}}`
- 断言：
  - `$.code` 等于 `0`
  - `$.data.list` 类型为 array
  - `$.data.total` 大于 `0`

---

### 步骤 5：修改用户

- 接口：`PUT /admin-api/system/user/update`
- Auth：Bearer Token = `{{accessToken}}`
- Body（JSON）：
  ```json
  {
    "id": "{{userId}}",
    "username": "testuser_auto",
    "nickname": "测试用户_已修改",
    "password": "Test@1234",
    "sex": 2
  }
  ```
- 断言：
  - `$.code` 等于 `0`

---

### 步骤 6：禁用用户

- 接口：`PUT /admin-api/system/user/update-status`
- Auth：Bearer Token = `{{accessToken}}`
- Body（JSON）：
  ```json
  {
    "id": "{{userId}}",
    "status": 1
  }
  ```
- 断言：
  - `$.code` 等于 `0`

---

### 步骤 7：启用用户

- 接口：`PUT /admin-api/system/user/update-status`
- Auth：Bearer Token = `{{accessToken}}`
- Body（JSON）：
  ```json
  {
    "id": "{{userId}}",
    "status": 0
  }
  ```
- 断言：
  - `$.code` 等于 `0`

---

### 步骤 8：重置用户密码

- 接口：`PUT /admin-api/system/user/update-password`
- Auth：Bearer Token = `{{accessToken}}`
- Body（JSON）：
  ```json
  {
    "id": "{{userId}}",
    "password": "NewPass@2026"
  }
  ```
- 断言：
  - `$.code` 等于 `0`

---

### 步骤 9：删除用户

- 接口：`DELETE /admin-api/system/user/delete`
- Query 参数：`id` = `{{userId}}`
- Auth：Bearer Token = `{{accessToken}}`
- 断言：
  - `$.code` 等于 `0`

---

### 步骤 10：确认用户已删除

- 接口：`GET /admin-api/system/user/get`
- Query 参数：`id` = `{{userId}}`
- Auth：Bearer Token = `{{accessToken}}`
- 断言：
  - `$.data` 等于 `null`

---

## 快速参考

### 变量依赖关系

```
步骤1 (登录) → 提取 accessToken
    ↓
步骤2 (创建用户) → 使用 accessToken，提取 userId
    ↓
步骤3-10 → 使用 accessToken + userId
```

### 每步操作总结

| 步骤 | 方法 | 路径 | 提取变量 | 断言数量 |
|------|------|------|----------|----------|
| 1. 登录 | POST | /admin-api/system/auth/login | accessToken | 2 |
| 2. 新增用户 | POST | /admin-api/system/user/create | userId | 2 |
| 3. 查询详情 | GET | /admin-api/system/user/get | - | 2 |
| 4. 分页查询 | GET | /admin-api/system/user/page | - | 3 |
| 5. 修改用户 | PUT | /admin-api/system/user/update | - | 1 |
| 6. 禁用用户 | PUT | /admin-api/system/user/update-status | - | 1 |
| 7. 启用用户 | PUT | /admin-api/system/user/update-status | - | 1 |
| 8. 重置密码 | PUT | /admin-api/system/user/update-password | - | 1 |
| 9. 删除用户 | DELETE | /admin-api/system/user/delete | - | 1 |
| 10. 确认删除 | GET | /admin-api/system/user/get | - | 1 |

### Auth 配置说明

步骤 2-10 都需要配置 Auth：
- 方式：Bearer Token
- 值：`{{accessToken}}`（引用环境变量，步骤1自动提取）

### ruoyi 响应格式参考

成功响应：
```json
{
  "code": 0,
  "data": { ... },
  "msg": ""
}
```

失败响应：
```json
{
  "code": 401,
  "data": null,
  "msg": " unauthorized"
}
```

所有断言的核心判断：`$.code` 等于 `0` 表示成功。
