# Skill B Input Snapshot

## 1. 基本信息

```text
project: ruoyi-pro
target_module: user management
run_id: ruoyi-vue-pro-user-management-20260606-validation
source_skill: source-to-srs / Skill A
validation_mode: offline_package_validation
```

## 2. 输入文件

| 输入 | 路径 | 角色 | 状态 |
|---|---|---|---|
| Skill A run | `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-a/` | 上游产物目录 | exists |
| SRS Markdown | `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-a/srs-kb-friendly.md` | 主分析输入 / TXT 载体来源 | exists |
| Source evidence map | `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-a/source-evidence-map.md` | 必填分析输入 / 默认不上传主 SRS KB | exists |
| Skill A gate result | `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-a/gate-result.md` | 前置 gate | exists |
| PDF text check report | `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-a/pdf-text-check-report.md` | PDF 文本层与可读性证明 | exists |
| SRS PDF | `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-a/srs-kb-friendly.pdf` | 参考输入 / parser 实验候选 | exists |
| risk-items.md | `srs_generation/runs/ruoyi-vue-pro-user-management-20260606-validation/skill-a/risk-items.md` | 选填风险输入 | missing |

## 3. 前置 gate 摘要

```text
skill_a_gate: pass
allowed_next_stage: Skill B
pdf_text_layer_gate: pass
pdf_readability_gate: pass
source_evidence_map_exists: true
risk_items_exists: false
```

## 4. 当前验证目标

本次验证目标是使用项目级 `srs-to-ragflow-kb` skill 包，在不访问 RAGFlow 的前提下，复现用户管理模块的 Skill B 离线准备度判断、retrieval 问题集、gate 语义和 handoff 结构。

## 5. 已知历史经验

- 当前 RAGFlow 环境曾验证 `.md` 直传解析失败。
- PDF 可解析但存在标题串接与正文丢失，不应作为主 handoff 载体。
- 从 `srs-kb-friendly.md` 生成的 TXT 载体曾得到更稳定的 `book` chunk 结果。
- 本次离线验证不复用或伪造在线结果，只记录为后续 online 验证建议。
