# 产物目录与文件命名任务清单

> 当前状态：本文件的已确定部分已收敛到 `../specs/artifact-run-standard.md`；其余未来阶段内容由 `../exec-plans/active/plan-0005-skill-c-and-orchestration-readiness.md` 接续。

## 目标

统一 SRS Skill 化链路的输出目录和文件命名，降低后续审计、复用、对比和自动编排成本。

## 1. 运行目录结构

- [ ] 定义一次运行的根目录格式
- [ ] 定义按项目名命名的规则
- [ ] 定义按模块名命名的规则
- [ ] 定义按日期或 run id 命名的规则
- [ ] 定义避免覆盖历史产物的规则

建议结构：

```text
srs_generation/runs/{project}-{module}-{date}/
```

完成标准：每次运行都有独立、可追踪的目录。

## 2. Skill A 子目录

- [ ] 定义 `skill-a/` 子目录
- [ ] 定义 scope 推断结果文件名
- [ ] 定义 scope 确认结果文件名
- [ ] 定义源码事实抽取文件名
- [ ] 定义事实草稿文件名
- [ ] 定义 kb-friendly SRS 文件名
- [ ] 定义 aligned SRS 文件名
- [ ] 定义 PDF 文件名
- [ ] 定义 source_evidence_map 文件名
- [ ] 定义 self_review_report 文件名
- [ ] 定义 independent_review_report 文件名

完成标准：Skill A 产物命名稳定。

## 3. Skill B 子目录

- [ ] 定义 `skill-b/` 子目录
- [ ] 定义知识库创建记录文件名
- [ ] 定义上传文档记录文件名
- [ ] 定义解析配置记录文件名
- [ ] 定义 chunk 质量报告文件名
- [ ] 定义检索 sanity check 报告文件名
- [ ] 定义 retrieval gate 文件名

完成标准：Skill B 产物能直接追踪到 RAGFlow 知识库状态。

## 4. Skill C 子目录

- [ ] 定义 `skill-c/` 子目录
- [ ] 定义认证规则文件名
- [ ] 定义 ID 提取规则文件名
- [ ] 定义最小 body 模板文件名
- [ ] 定义 headers 模板文件名
- [ ] 定义错误黑名单文件名
- [ ] 定义执行约束增强文档文件名

完成标准：Skill C 输出能直接被执行编排引用。

## 5. Handoff 子目录

- [ ] 定义 `handoff/` 子目录
- [ ] 定义 Skill A → Skill B handoff 文件
- [ ] 定义 Skill B → Skill C handoff 文件
- [ ] 定义 Skill C → TestHub handoff 文件
- [ ] 定义最终总 handoff 文件

完成标准：跨阶段交接不依赖口头说明。

## 6. Reports 子目录

- [ ] 定义 `reports/` 子目录
- [ ] 定义总执行摘要文件
- [ ] 定义质量评审汇总文件
- [ ] 定义验证报告文件
- [ ] 定义风险项汇总文件
- [ ] 定义人工确认记录文件

完成标准：人类读者可以快速了解一次运行的最终状态。
