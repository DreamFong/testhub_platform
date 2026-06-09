# Online Retrieval Check Report

## 1. 基本信息

```text
project: ruoyi-pro
target_module: user management
run_id: ruoyi-vue-pro-user-management-20260606-validation
validation_mode: skill_b_package_online_validation
validated_at: 2026-06-09
```

## 2. RAGFlow dataset 信息

```text
dataset_name: ruoyi-pro-user-management-srs-txt-skillb-package-validation-20260609
dataset_id: 79991b2c63b311f18243434b552cc465
SRS_KB_ID: 79991b2c63b311f18243434b552cc465
document_id: 7e654ebe63b311f18243434b552cc465
uploaded_document: /tmp/ruoyi-pro-user-management-srs-20260608.txt
```

未上传：

- `srs-kb-friendly.md`
- `source-evidence-map.md`
- `srs-kb-friendly.pdf`

## 3. 解析结果

```text
parse_status: DONE
parse_progress: 1.0
chunk_method: book
chunk_count: 37
short_chunk_rate: 0.0%
embedding_model: Pro/BAAI/bge-m3@SILICONFLOW
llm_id: qwen-plus@Tongyi-Qianwen
graphrag.use_graphrag: false
raptor.use_raptor: false
image_context_size: 0
table_context_size: 0
```

## 4. Chunk 质量摘要

- 未发现纯标题短块。
- 未发现明显正文丢失。
- 未发现严重相邻 FR 串接。
- 每个 FR 基本按标题上下文和单条正文切分。
- 部分综合问题需要合并多个 chunk，例如“筛选条件 + 部门/角色范围”。

## 5. Retrieval sanity check 结果

| ID | 问题 | 结果 | 说明 |
|---|---|---|---|
| Q-001 | 查询用户列表支持哪些筛选条件？指定部门和角色时结果范围如何变化？ | hit | 命中分页查询、部门下级范围和角色关联用户范围。 |
| Q-002 | 新增用户成功后，系统默认状态是什么，还会建立哪些关联？ | hit | 命中默认启用、密码安全保存、岗位关联。 |
| Q-003 | 新增或修改用户前，用户账号、手机号和邮箱需要满足哪些唯一性规则？ | hit | 命中账号、手机号、邮箱唯一性与部门岗位有效性校验。 |
| Q-004 | 用户管理能力按哪些操作类型进行授权控制？哪些辅助入口需要单独评估访问边界？ | hit | 命中查看、新增、修改、删除、重置密码、导出、导入，以及辅助入口边界说明。 |
| Q-005 | 当导入数据为空、初始化密码未配置或租户账号配额不足时，系统如何处理？ | hit | 命中异常处理规则、导入规则和配额校验。 |
| Q-006 | 管理员修改存在用户时，系统应更新哪些内容，哪些内容不应通过该入口更新？ | hit | 命中更新基础资料和岗位关联，不通过该入口更新密码。 |
| Q-007 | 本用户管理 SRS 明确不覆盖哪些能力？ | hit | 命中明确排除项和模块范围。 |
| Q-008 | 当前主 SRS KB 是否能直接回答接口路径、Controller、Service 和权限码等源码级证据？ | hit | 命中需求追溯说明：细粒度源码证据已下沉到 `source-evidence-map.md`，主 SRS KB 不应直接承担该职责。 |

## 6. Gate 结论

```text
online_retrieval_gate: pass
skill_b_status: online_verified
allowed_next_stage: skill_c
```

## 7. 推荐 retrieval 参数

```text
top_k: 6-8
similarity_threshold: 0.10-0.20
vector_similarity_weight: 0.30
rerank: enabled if available
```

## 8. Caveats

- 当前主 SRS KB 只覆盖业务需求，不直接提供 Controller、Service、接口路径、权限码等源码级证据。
- 源码级证据应从 `source-evidence-map.md` 或后续独立 evidence KB 获取。
- 部分综合问题需要合并多个 chunks，建议下游不要只依赖 top 1。
