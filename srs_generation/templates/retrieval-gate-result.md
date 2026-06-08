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
skill_b_status: offline_ready | blocked_waiting_ragflow | fail
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

### 5.1 允许情况

- [ ] offline_readiness_gate = pass
- [ ] 真实 online 阶段已通过
- [ ] 风险项已被记录并允许带条件继续

### 5.2 不允许情况

- [ ] offline_readiness_gate = fail
- [ ] online_retrieval_gate = fail
- [ ] online_retrieval_gate = blocked 且仍试图宣称知识库可用
- [ ] 关键风险项未披露

## 6. 结论

```text
allowed_next_stage: none | wait_for_ragflow | skill_c | orchestration
reason: 
```
