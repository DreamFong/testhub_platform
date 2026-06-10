# 当前 SRS Skill 化工作总结

更新日期：2026-06-09  
当前分支：`srs-generation-skill-a-prep`

## 1. 当前总体状态

当前工作已分成两条线：

```text
能力线：Skill A / Skill B 的规范、验证与可移植 skill 打包
治理线：srs_generation 文档骨架整改
```

当前结论：

- Skill A 已完成项目级可移植打包：`.claude/skills/source-to-srs/`
- Skill B 已完成项目级可移植打包：`.claude/skills/srs-to-ragflow-kb/`
- Skill B 用户管理样例已通过 package validation 与真实 online 验证
- 当前工作焦点不是进入 Skill C，而是收敛 `srs_generation/` 的文档骨架

## 2. 能力链当前状态

### 2.1 Skill A

已形成稳定产物链：

```text
源码逆向
→ scope confirm
→ srs-kb-friendly.md
→ PDF 生成与文本层检查
→ independent review
→ gate result
→ handoff
```

当前已知验证样例：

- `ruoyi-vue-pro-user-management-20260606-validation/skill-a/`
- `ruoyi-vue-pro-role-management-20260604/skill-a/`
- `ruoyi-vue-pro-erp-warehouse-validation-20260607/skill-a/`
- `ruoyi-vue-pro-mes-stocktaking-task-validation-20260607/skill-a/`

已知状态：主文档偏业务可读，技术细节默认下沉到 `source-evidence-map.md`。

### 2.2 Skill B

当前 canonical 验证结果来自：

```text
srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-b-package-validation/
```

关键结论：

```text
SRS_KB_ID=79991b2c63b311f18243434b552cc465
online_retrieval_gate=pass
skill_b_status=online_verified
allowed_next_stage=skill_c
```

当前载体策略：

- 主 SRS KB 默认使用 TXT carrier
- `source-evidence-map.md` 默认不上传主 SRS KB
- PDF 保留为阅读版和 parser 对比实验输入

详情见：`design-docs/ragflow-carrier-selection.md`

### 2.3 Skill C

当前未进入 Skill C。骨架治理阶段不推进 Skill C 实施。

## 3. 当前文档骨架治理状态

已完成：

- 新建总入口：`README.md`
- 新建治理入口：`DELIVERY.md`、`QUALITY_SCORE.md`
- 新建目录索引：`specs/README.md`、`exec-plans/README.md`、`design-docs/index.md`
- 新建规范补充：`specs/artifact-run-standard.md`、`specs/handoff-sync-policy.md`
- 新建设计文档：
  - `design-docs/doc-boundary-model.md`
  - `design-docs/lifecycle-governance.md`
  - `design-docs/skill-reference-sync-strategy.md`
  - `design-docs/ragflow-carrier-selection.md`
- 建立执行计划目录：`exec-plans/active/`、`exec-plans/completed/`
- 当前主治理计划：`exec-plans/active/plan-0004-sdd-doc-structure-governance.md`（后续小修入口）
- 新增骨架治理收官记录：`exec-plans/completed/plan-0003-sdd-doc-structure-governance-phase-1.md`
- 新增 completed plans：
  - `exec-plans/completed/plan-0001-skill-a-foundation-and-validation.md`
  - `exec-plans/completed/plan-0002-skill-b-hybrid-mvp-and-online-validation.md`
- 新增延后计划：`exec-plans/active/plan-0005-skill-c-and-orchestration-readiness.md`
- 旧 `tasks/` 已进入冻结迁移期，全部历史任务文件均已补充当前状态与归属去向提示
- Skill A / Skill B 参考副本一致性检查已完成：正式规范是规范事实源，Skill 参考副本允许保留路径、样例名和参考文档名的可移植改写；gate、handoff、输入输出契约与状态语义不得漂移

## 4. 当前 canonical handoff

当前 canonical handoff：

```text
srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-b-package-validation/skill-b-handoff.md
```

当前 canonical handoff block：

```text
PROJECT_NAME=ruoyi-pro
BUSINESS_DOMAIN=user management
TEST_SCOPE=用户新增、编辑、启停用、唯一性校验、权限约束、异常提示
MIN_BUSINESS_FLOW=查询用户列表 → 新增用户 → 编辑用户 → 禁用用户
SRS_KB_ID=79991b2c63b311f18243434b552cc465
API_DOCS_KB_ID=
RETRIEVAL_PARAMS=top_k=6-8, similarity_threshold=0.10-0.20, vector_similarity_weight=0.30, rerank=enabled if available
KNOWN_CAVEATS=主 SRS KB 只覆盖业务需求，不直接提供 Controller、Service、接口路径、权限码等源码级证据；这些应从 source-evidence-map.md 或独立 evidence KB 获取。部分综合问题需要合并多个 chunks。
offline_readiness_gate=pass
online_retrieval_gate=pass
skill_b_status=online_verified
allowed_next_stage=skill_c
```

## 5. 当前约束

当前骨架治理阶段默认遵守：

- 不访问 RAGFlow
- 不进入 Skill C
- 不修改 `runs/` 内事实产物
- 不删除历史文档
- 不让旧 `tasks/` 重新承担 live 规范或推进职责

## 6. 新会话恢复顺序

建议按以下顺序恢复：

1. `srs_generation/README.md`
2. `srs_generation/session-handoff.md`
3. `srs_generation/current-work-summary.md`
4. `srs_generation/exec-plans/active/plan-0004-sdd-doc-structure-governance.md`
5. 当前 canonical handoff
6. 必要时再读相关 `specs/` 或 `design-docs/`

## 7. 下一步建议

骨架治理的下一步优先级：

1. 维持 `current-work-summary.md` 与 `session-handoff.md` 的同步。
2. 继续以 `specs/` 作为规范事实源，以 `design-docs/` 承接设计解释。
3. 若无新的骨架治理需求，可将当前阶段视为稳定状态，后续按需做维护性小修。
4. 在未明确切换目标前，不进入 Skill C 和外部系统操作。

## 8. 历史细节入口

如需查历史细节，不要先回滚 summary，而是优先查看：

- `runs/`：某次真实执行与验证事实
- `design-docs/`：为什么这样设计
- `specs/`：当前有效规则与契约
- 旧 `tasks/`：冻结迁移期历史材料
