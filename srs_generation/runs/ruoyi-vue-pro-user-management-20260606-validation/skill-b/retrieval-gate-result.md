# Retrieval Gate Result

## 1. 基本信息

```text
project: ruoyi-pro
target_module: user management
run_id: ruoyi-vue-pro-user-management-20260606-validation
status: final
```

## 2. Gate 摘要

```text
offline_readiness_gate: pass
online_retrieval_gate: conditional pass
skill_b_status: online_verified_with_risks
```

## 3. offline_readiness_gate 结论

```text
reason: Skill A 前置条件满足，SRS 结构完整，TXT 载体可稳定进入真实建库与检索验证。
required_fixes_count: 0
manual_review_required: false
```

## 4. online_retrieval_gate 结论

```text
result: conditional pass
blocked_reason: 
real_dataset_id: 00c0dbdc632111f18243434b552cc465
real_chunk_result_available: true
real_retrieval_result_available: true
```

## 5. 进入下一阶段条件

### 5.1 允许请求 online 执行

- [x] offline_readiness_gate = pass
- [x] 或 offline_readiness_gate = conditional pass 且人工明确允许继续
- [x] 风险项已被记录并允许带条件继续
- [x] 尚未把 online_retrieval_gate = blocked 误写成可用结论

### 5.2 允许进入 Skill C / 总编排

- [ ] online_retrieval_gate = pass
- [x] 或 online_retrieval_gate = conditional pass 且风险已显式披露
- [x] 真实 online 阶段结果已记录

### 5.3 不允许情况

- [ ] offline_readiness_gate = fail
- [ ] online_retrieval_gate = fail
- [ ] online_retrieval_gate = blocked 且仍试图宣称知识库可用
- [ ] 关键风险项未披露

## 6. Decision Basis

- `srs-kb-friendly.md` 直接上传在当前 RAGFlow 环境下解析失败，原因是该环境不支持 `.md` 作为可解析文档类型。
- `srs-kb-friendly.pdf` 虽然能完成 OCR、布局分析和切块，但人工抽检发现存在“相邻章节标题串接、正文丢失”的结构性问题，不接受作为当前主 handoff 结果。
- 基于 `srs-kb-friendly.md` 生成的临时 TXT `/tmp/ruoyi-pro-user-management-srs-20260608.txt` 在 `book` 模式下生成 37 个 chunks，未再出现明显标题孤块、正文丢失或跨章节严重串接。
- TXT 方案 6 道 retrieval sanity checks 结果为：5 个命中、1 个弱命中、0 个未命中。
- 弱命中问题主要集中在“源码证据追溯”类提问；这是因为本轮按约束未上传 `source-evidence-map.md`，知识库只能回答“证据已下沉”的说明层，而不能直接返回更细的 controller/service/permission 明细。

## 7. Required Fixes

- 当前不需要回退 Skill A 正文内容。
- 若后续下游强依赖源码级证据追溯，应单独构建 evidence KB，或在编排层显式补充 `source-evidence-map.md` 的使用策略。

## 8. Risk Carry-forward

- 当前 SRS_KB 适合回答业务需求、字段规则、异常处理与验收标准。
- 当前 SRS_KB 不适合作为源码级证据追溯的唯一来源。
- `book` 切块下仍存在顶层文档标题重复进入 chunk 的轻度噪声，建议下游 retrieval 至少查看 top 3，而不是只依赖 top 1。

## 9. 结论

```text
allowed_next_stage: skill_c
reason: 当前 TXT SRS KB 已能稳定支持业务规则与最小业务流检索，适合进入 Skill C 提炼执行约束增强层；但源码级追溯仍应作为后续补充能力，而非当前主 SRS KB 的直接职责。
```

### 9.1 allowed_next_stage 取值说明（本次适用）

- `skill_c`：知识库检索已满足进入下一层能力补强的条件，下一步进入 Skill C 提炼执行约束增强层。
