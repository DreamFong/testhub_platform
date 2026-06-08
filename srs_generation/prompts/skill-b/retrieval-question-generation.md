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
skill_a_run_dir: 
question_total: 
critical_question_total: 
risk_question_total: 
```

## 2. 问题列表

| ID | 类型 | 优先级 | 问题 | 期望命中范围 | 来源章节 | 风险关联 |
|---|---|---|---|---|---|---|
| Q-001 | functional | P0 |  |  |  |  |

## 3. 风险专项问题

- 

## 4. 不应纳入主问题集的技术追溯问题

| 问题 | 原因 | 建议去向 |
|---|---|---|
|  |  | evidence_only / handoff_only |
```

## 禁止事项

- 不要直接把接口路径、类名、方法名写成主问题集主体。
- 不要把实现细节问题误写成业务问题。
- 不要忽略 `risk-items.md`。
- 不要生成无法从当前 SRS 主体回答的问题。
