# Artifact 与 Run 目录规范

版本：v0.1  
状态：draft

## 1. 目的

本文档用于定义 `srs_generation/` 下运行目录、固定产物命名和事实产物治理规则。

## 2. 顶层职责

- `runs/`：单次执行事实区。保存样例运行目录、检查结果、handoff 和真实产物。
- `handoff/`：人工整理的阶段性交付包或汇总快照，可作为阅读入口，但不替代最新 run 事实。
- `reports/`：跨 run 的总结报告或回归报告。

## 3. Run 目录规则

每次独立验证、回归或阶段执行，应创建新的 run 目录，而不是覆盖旧结果。

推荐结构：

```text
srs_generation/runs/<project>-<module>-<yyyymmdd>-<tag>/<skill>/
```

其中：

- `<project>`：来源项目标识
- `<module>`：目标业务模块标识
- `<yyyymmdd>`：执行日期
- `<tag>`：如 `validation`、`package-validation`、`regression`
- `<skill>`：如 `skill-a`、`skill-b-package-validation`

## 4. 固定产物命名

### 4.1 Skill A 常见固定产物

- `srs-kb-friendly.md`
- `srs-kb-friendly.pdf`
- `source-evidence-map.md`
- `pdf-text-check-report.md`
- `independent-review-report.md`
- `gate-result.md`
- `risk-items.md`（按需生成）

### 4.2 Skill B 常见固定产物

- `skill-b-input-snapshot.md`
- `kb-plan.md`
- `parse-config-plan.md`
- `retrieval-question-set.md`
- `offline-retrieval-readiness-report.md`
- `online-retrieval-check-report.md`（仅真实 online 执行后生成）
- `retrieval-gate-result.md`
- `skill-b-handoff.md`

## 5. 事实产物治理规则

- `runs/` 内文件属于事实产物，不应为目录治理或文档收敛目的被重写。
- 若后续结论变化，应创建新 run，而不是回写旧 run。
- `current-work-summary.md` 与 `session-handoff.md` 只引用 run 路径和结论，不复制完整事实内容。
- `handoff/` 中的人工整理包可保留，但若与更晚的 run handoff 冲突，以更晚的 run handoff 为准。

## 6. 维护规则

- 新增验证时优先复用既有固定命名，避免同义文件名并存。
- 若某阶段尚未真实执行，不得伪造对应事实产物。
- run 目录结构发生实质变化时，应同步更新本规范与相关模板。
