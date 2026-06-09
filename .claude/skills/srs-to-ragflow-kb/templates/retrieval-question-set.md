# Skill B 检索问题集模板

## 1. 基本信息

```text
project: 
target_module: 
run_id: 
question_set_type: offline_seed | hybrid_mvp_online_subset
status: draft
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
| Q-001 | functional | P0 |  |  |  |  | 是 / 否 |

### 3.1 类型取值

```text
functional      — 功能需求问题
field_rule      — 字段 / 输入 / 校验规则问题
permission      — 权限或访问边界问题
exception       — 异常、边界、失败处理问题
acceptance      — 验收标准问题
exclusion       — 明确排除项问题
risk            — 风险项问题
```

### 3.2 优先级取值

```text
P0 — 首轮 online sanity check 必测问题
P1 — 建议纳入扩展 online 检索验证的问题
P2 — 可选问题，主要用于人工复核或后续扩展
```

## 4. 风险专项问题

| ID | 风险类型 | 问题 | 预期验证方式 | 当前处理 |
|---|---|---|---|---|
| RQ-001 | 业务口径 / 范围 / evidence |  | online 验证 / 人工复核 |  |

## 5. 不应纳入主问题集的技术追溯问题

| 问题 | 原因 | 建议去向 |
|---|---|---|
|  | 源码级证据不属于主 SRS KB 的默认职责 | evidence_only / handoff_only |

## 6. 结论

```text
question_total: 
critical_question_total: 
risk_question_total: 
online_subset_total: 
online_subset_critical_total: 
ready_for_online_retrieval: true | false
notes: 
```
