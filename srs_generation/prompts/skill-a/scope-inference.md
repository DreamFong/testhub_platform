# Scope 自动推断 Prompt

## 角色

你负责从 `source_project` 和 `target_module` 自动发现目标模块候选范围，并输出 scope confirmation 所需的信息。

## 输入

```text
source_project: 
target_module: 
entry_files: 可选
scope_hint: 可选
domain_hints: 可选
```

## 输出

必须输出：

```text
scope-inference.md
scope-confirmation.md
adjacent-capabilities.md
excluded-scope.md
scope-risk-items.md
```

可以合并在同一文件中，但章节必须清晰。

## 执行步骤

### 1. 入口发现

从 `target_module` 推断关键词，搜索：

- Controller / Router
- Service / Use Case
- DTO / VO / Schema
- Entity / DO / Mapper
- Permission / 权限码
- ErrorCode / 异常定义
- SQL / migration
- import / export 相关类

优先级：

```text
entry_files > Controller / Router > Service > DTO / VO > Permission > ErrorCode > Entity / Mapper
```

### 2. 功能识别

从 Controller / Router 识别候选功能：

- 查询类
- 详情类
- 新增类
- 编辑类
- 删除类
- 批量操作
- 导入导出
- 状态流转
- 配置类

### 3. 规则线索识别

从 Service 识别：

- 业务校验
- 唯一性检查
- 状态限制
- 删除限制
- 导入导出处理
- 批量处理

从 DTO / VO 识别：

- 必填字段
- 长度限制
- 格式限制
- 枚举限制
- 分页 / 查询条件
- 导入导出字段

从权限注解识别：

- 功能权限码
- 查询 / 创建 / 更新 / 删除 / 导入 / 导出权限

从错误码识别：

- 异常场景
- 规则失败原因
- 不存在、重复、禁用、不可删除等条件

### 4. 相邻能力识别

以下默认进入“待确认相邻能力”或“依赖说明”，不要直接纳入核心范围：

- 跨模块 Service 调用
- 认证和用户会话
- 角色权限基础能力
- 组织架构 / 部门等只读筛选依赖
- 字典 / 枚举配置
- 文件上传基础能力

## 输出格式

```markdown
# Scope Inference

## 基本信息

source_project: 
target_module: 
status: confirmed | confirmed_with_changes | blocked

## 入口发现

### Controller / Router
- 文件：
- 依据：

### Service
- 文件：
- 依据：

### DTO / VO / Schema
- 文件：
- 依据：

### Entity / Mapper / SQL
- 文件：
- 依据：

### Permission
- 权限码：
- 依据：

### ErrorCode
- 错误码：
- 依据：

## 候选纳入范围

- 

## 待确认相邻能力

- 能力：
  - 来源：
  - 建议：纳入 / 排除 / 作为依赖说明
  - 原因：

## 建议排除范围

- 

## 自动确认结论

status: confirmed | confirmed_with_changes | blocked
reason: 

## 风险项

- 
```

## 禁止事项

- 不要直接生成 SRS。
- 不要把相邻能力自动写成核心功能。
- 不要把 scope_hint 当作源码事实。
- 不要忽略入口缺失风险。

## 失败条件

- `source_project` 不可读。
- 找不到任何目标模块入口。
- 候选范围与 target_module 明显不一致。

## 最小示例

输入：

```text
target_module: system user management
```

输出候选范围：

```text
用户列表、详情、新增、编辑、删除、批量删除、重置密码、状态修改、导入、导出
```
