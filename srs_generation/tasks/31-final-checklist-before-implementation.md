# 实施前最终检查清单

> 当前状态：本文件保留为历史实施前检查快照。当前 live 交付、关闭与文档维护规则请以 `../DELIVERY.md` 为准。

## 目标

在开始编写正式 spec、prompt、template 或脚本之前，确认当前任务拆解没有遗漏关键前置条件。

## 1. 目标确认

- [ ] 确认当前优先目标是 Skill A，而不是 A/B/C 全自动化
- [ ] 确认 Skill A 默认输出 kb-friendly
- [ ] 确认 aligned 仅作为可选输出
- [ ] 确认 Skill A 不直接做 RAGFlow 检索质量评估

## 2. 输入确认

- [ ] 确认 `source_project` 必填
- [ ] 确认 `target_module` 必填
- [ ] 确认 `scope_hint` 选填
- [ ] 确认 `entry_files` 选填
- [ ] 确认 `reference_srs` 选填
- [ ] 确认未提供 scope_hint 时自动推断 scope

## 3. Gate 确认

- [ ] 确认 scope confirm 是强制前置 gate
- [ ] 确认 SRS 文档质量 gate 存在
- [ ] 确认 PDF 文本层不可提取是硬性 fail
- [ ] 确认关键结论无源码依据是硬性 fail 或人工复核触发项
- [ ] 确认 conditional pass 被允许

## 4. 产物确认

- [ ] 确认 SRS Markdown 是主产物
- [ ] 确认 SRS PDF 是主产物
- [ ] 确认 source_evidence_map 是强制产物
- [ ] 确认 self_review_report 是支撑产物
- [ ] 确认 independent_review_report 是支撑产物
- [ ] 确认 risk_items 是支撑产物

## 5. 样本确认

- [ ] 确认用户管理模块作为回归样本
- [ ] 确认需要选择第二验证样本
- [ ] 确认第二样本应优先降低跨项目变量
- [ ] 确认第二样本要覆盖不同复杂点

## 6. 文件组织确认

- [ ] 确认任务清单位于 `srs_generation/tasks/`
- [ ] 确认 spec 建议位于 `srs_generation/specs/`
- [ ] 确认 prompt 建议位于 `srs_generation/prompts/`
- [ ] 确认 template 建议位于 `srs_generation/templates/`
- [ ] 确认 script 建议位于 `srs_generation/scripts/`
- [ ] 确认 run 产物建议位于 `srs_generation/runs/`

## 7. 下一步确认

- [ ] 决定是否立即创建 Skill A spec 文档
- [ ] 决定是否同时创建 templates
- [ ] 决定是否先只创建 Skill A prompts
- [ ] 决定第二样本选择时间点

## 建议结论

如果以上没有异议，下一步直接进入：

```text
创建 srs_generation/specs/skill-a-source-to-srs.md
创建 srs_generation/templates/source-evidence-map.md
创建 srs_generation/templates/skill-a-scorecard.md
```
