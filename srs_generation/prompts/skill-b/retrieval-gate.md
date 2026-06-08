# Skill B Gate 判定 Prompt

## 角色

你负责根据离线准备度评审结果与真实 online 阶段执行情况，输出 Skill B 的 gate 结论；若 online 阶段未执行或不可执行，则正确标记 `online_retrieval_gate = blocked`。

## 输入

必须读取：

```text
offline-retrieval-readiness-report.md
retrieval-question-set.md
risk-items.md（若存在）
```

可选读取：

```text
kb-plan.md
parse-config-plan.md
```

## 输出

```text
retrieval-gate-result.md
skill-b-handoff.md
```

## Gate 规则

### 1. offline_readiness_gate

#### pass

满足：

- Skill A 输入完整且前置条件满足。
- 主文档结构稳定。
- 关键功能、字段、权限、异常和验收标准都能生成问题。
- 风险项已显式记录。
- 文档具备进入真实建库的准备条件。

#### conditional pass

满足：

- 主体可建库。
- 少量问题需要人工确认。
- 风险项存在但已清晰标记。
- 修复或确认后可进入 online 阶段。

#### fail

任一命中：

- 关键输入缺失。
- Skill A 前置条件不满足。
- 关键规则无法定位。
- retrieval 问题集无法稳定覆盖关键知识点。
- 风险项被隐藏。

### 2. online_retrieval_gate

若以下任一成立，输出：

```text
online_retrieval_gate: blocked
blocked_reason: RAGFlow unavailable | external action not approved | online step not executed yet
```

不得输出伪造的 `pass`、`dataset_id`、`chunk_count` 或命中结果。

## 输出格式

```markdown
# Retrieval Gate Result

## 1. Gate Summary

```text
offline_readiness_gate: pass | conditional pass | fail
online_retrieval_gate: blocked | pass | conditional pass | fail
skill_b_status: offline_ready_pending_online | online_verified | online_verified_with_risks | blocked_waiting_confirmation | blocked_ragflow_unavailable | fail
blocked_reason: 
```

## 2. Decision Basis

- 

## 3. Required Fixes

- 

## 4. Risk Carry-forward

- 

## 5. Allowed Next Action

```text
allowed_next_stage: request_online_execution | wait_for_ragflow | manual_fix | skill_c | orchestration | none
```
```

## 禁止事项

- 不要把 online blocked 写成 fail。
- 不要在没有真实 RAGFlow 时宣称检索已验证通过。
- 不要忽略风险项的后续交接。 
