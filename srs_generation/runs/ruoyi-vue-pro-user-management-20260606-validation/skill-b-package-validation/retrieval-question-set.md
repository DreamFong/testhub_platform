# Retrieval Question Set

## 1. 基本信息

```text
project: ruoyi-pro
target_module: user management
run_id: ruoyi-vue-pro-user-management-20260606-validation
question_set_type: offline_seed
status: final
```

## 2. 问题集设计原则

- 问题集用于后续 retrieval sanity check。
- 问题集优先覆盖关键业务知识点，而不是追求自然聊天风格。
- 每个问题应指向明确答案来源。
- 若存在风险项，应设计专门问题验证其可见性，而不是把风险静默忽略。
- 不应把接口路径、类名、方法名等源码追溯问题混入主业务问题集。

## 3. 问题列表

| ID | 类型 | 优先级 | 问题 | 期望命中范围 | 来源章节 | 风险关联 | 首轮 online 验证 |
|---|---|---|---|---|---|---|---|
| Q-001 | functional | P0 | 查询用户列表支持哪些筛选条件？指定部门和角色时结果范围如何变化？ | 用户分页查询筛选条件、部门下级范围、角色关联用户范围 | FR-USER-001 / 字段与输入规则 |  | 是 |
| Q-002 | functional | P0 | 新增用户成功后，系统默认状态是什么，还会建立哪些关联？ | 默认启用、密码安全保存、岗位关联 | FR-USER-004 |  | 是 |
| Q-003 | field_rule | P0 | 新增或修改用户前，用户账号、手机号和邮箱需要满足哪些唯一性规则？ | 账号、手机号、邮箱唯一性校验 | 字段与输入规则 / 业务规则 |  | 是 |
| Q-004 | permission | P1 | 用户管理能力按哪些操作类型进行授权控制？哪些辅助入口需要单独评估访问边界？ | 查看、新增、修改、删除、重置密码、导出、导入；精简列表和模板下载等辅助入口边界 | 角色与权限概述 / source-evidence-map.md | evidence_detail_not_uploaded | 是 |
| Q-005 | exception | P0 | 当导入数据为空、初始化密码未配置或租户账号配额不足时，系统如何处理？ | 导入空列表、初始化密码、租户配额不足的失败结果 | 异常处理规则 / FR-USER-012 |  | 是 |
| Q-006 | acceptance | P1 | 管理员修改存在用户时，系统应更新哪些内容，哪些内容不应通过该入口更新？ | 更新基础资料和岗位关联，不通过通用修改入口更新密码 | FR-USER-005 验收标准 |  | 是 |
| Q-007 | exclusion | P1 | 本用户管理 SRS 明确不覆盖哪些能力？ | 部门、角色、岗位独立管理；用户注册；个人中心密码校验；完整认证授权；IM 好友管理 | 明确排除项 |  | 是 |
| Q-008 | risk | P1 | 当前主 SRS KB 是否能直接回答接口路径、Controller、Service 和权限码等源码级证据？ | 应回答不能；这些细节下沉到 source-evidence-map.md，默认不属于主 SRS KB | 需求追溯说明 / source-evidence-map.md | evidence_detail_not_uploaded | 是 |

## 4. 风险专项问题

| ID | 风险类型 | 问题 | 预期验证方式 | 当前处理 |
|---|---|---|---|---|
| RQ-001 | evidence | 当前主 SRS KB 是否能稳定回答源码级证据追溯问题？ | online 验证 + 人工复核 | 标记为弱命中风险，不作为主 SRS KB 的 pass 必要条件 |
| RQ-002 | carrier | Markdown / PDF / TXT 三种载体中哪一种适合作为当前环境主上传材料？ | online 验证 | 历史结果显示 TXT 最稳，PDF 不可靠，Markdown 不支持 |

## 5. 不应纳入主问题集的技术追溯问题

| 问题 | 原因 | 建议去向 |
|---|---|---|
| FR-USER-009 对应的 Controller、Service、接口路径和权限码分别是什么？ | 源码级证据不属于主 SRS KB 的默认职责 | evidence_only / handoff_only |
| 新增用户接口的具体 HTTP 方法和路径是什么？ | 接口路径属于实现追溯，不应污染主业务问题集 | evidence_only / API docs KB |

## 6. 结论

```text
question_total: 8
critical_question_total: 4
risk_question_total: 2
online_subset_total: 8
online_subset_critical_total: 4
ready_for_online_retrieval: true
notes: 问题集覆盖功能、字段规则、权限边界、异常处理、验收标准、排除项和 evidence 风险；首轮 online 可取 6-8 题执行。
```
