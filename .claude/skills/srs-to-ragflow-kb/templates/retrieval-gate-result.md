# Skill B 检索 Gate 结果模板

## 1. 基本信息

```text
project: 
target_module: 
run_id: 
status: draft
```

## 2. Gate 摘要

```text
offline_readiness_gate: pass | conditional pass | fail
online_retrieval_gate: pass | conditional pass | fail | blocked
skill_b_status: offline_ready_pending_online | online_verified | online_verified_with_risks | blocked_waiting_confirmation | blocked_ragflow_unavailable | fail
```

## 3. offline_readiness_gate 结论

```text
reason: 
required_fixes_count: 
manual_review_required: true | false
```

## 4. online_retrieval_gate 结论

```text
result: pass | conditional pass | fail | blocked
blocked_reason: 
real_dataset_id: 
real_chunk_result_available: true | false
real_retrieval_result_available: true | false
```

## 5. 进入下一阶段条件

### 5.1 允许请求 online 执行

- [ ] offline_readiness_gate = pass
- [ ] 或 offline_readiness_gate = conditional pass 且人工明确允许继续
- [ ] 风险项已被记录并允许带条件继续
- [ ] 尚未把 online_retrieval_gate = blocked 误写成可用结论

### 5.2 允许进入 Skill C / 总编排

- [ ] online_retrieval_gate = pass
- [ ] 或 online_retrieval_gate = conditional pass 且风险已显式披露
- [ ] 真实 online 阶段结果已记录

### 5.3 不允许情况

- [ ] offline_readiness_gate = fail
- [ ] online_retrieval_gate = fail
- [ ] online_retrieval_gate = blocked 且仍试图宣称知识库可用
- [ ] 关键风险项未披露

## 6. 结论

```text
allowed_next_stage: request_online_execution | wait_for_ragflow | manual_fix | skill_c | orchestration | none
reason: 
```

### 6.1 allowed_next_stage 取值说明

- `request_online_execution`：离线准备度已满足，下一步应请求执行真实 online 验证。
- `wait_for_ragflow`：当前主要阻塞是 RAGFlow 环境不可用，应等待环境恢复后再继续。
- `manual_fix`：当前存在输入、结构、问题集或风险披露问题，需先人工修复再继续。
- `skill_c`：知识库检索已满足进入下一层能力补强的条件，下一步进入 Skill C 提炼执行约束增强层。
- `orchestration`：知识库结果已可交给总编排层，下一步由端到端流程串联场景生成、归一化、导入与执行。
- `none`：当前没有允许进入的下一阶段，应先处理阻塞项。
