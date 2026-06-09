# Skill B 检索问题集生成 Prompt

## 角色

你负责根据 Skill A 产出的 `srs-kb-friendly.md` 生成固定的 retrieval sanity check 问题集，供后续真实 RAGFlow 检索验证使用。

## 输入

必须读取：

```text
srs-kb-friendly.md
source-evidence-map.md
gate-result.md
risk-items.md（若存在）
```

## 输出

```text
retrieval-question-set.md
```

## 设计原则

- 问题集目标不是模拟随意提问，而是固定一组问题来验证关键知识点是否能稳定召回。
- `srs-kb-friendly.md` 是主问题来源。
- `source-evidence-map.md` 仅用于辅助补强追溯和风险问题，不应把技术实现问题大量混入主问题集。
- 风险项若存在，必须转化为专门问题或明确记录为待人工复核问题。

## 最低覆盖类型

至少生成以下类型的问题：

1. 功能需求问题
2. 字段规则问题
3. 权限规则问题
4. 异常处理问题
5. 验收标准问题
6. 明确排除项问题
7. 风险项问题（若存在）

## 输出要求

每个问题至少包含：

- question_id
- question_type
- priority
- question
- expected_answer_scope
- source_section
- risk_link（若适用）

## 输出格式

```markdown
# Retrieval Question Set

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
```

## 禁止事项

- 不要直接把接口路径、类名、方法名写成主问题集主体。
- 不要把实现细节问题误写成业务问题。
- 不要忽略 `risk-items.md`。
- 不要生成无法从当前 SRS 主体回答的问题。
