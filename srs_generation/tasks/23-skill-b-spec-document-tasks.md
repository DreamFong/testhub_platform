# Skill B 正式 Spec 文档编写任务清单

## 目标

把 Skill B 的知识库构建与检索验证流程整理为正式规范，建议路径为 `srs_generation/specs/skill-b-kb-validation.md`。

## 1. 文档元信息

- [ ] 写明文档标题
- [ ] 写明版本号
- [ ] 写明适用范围
- [ ] 写明与 Skill A 的关系
- [ ] 写明与 Skill C 的关系

完成标准：读者能明确 Skill B 是知识库质量层。

## 2. 职责边界

- [ ] 写明负责 RAGFlow 知识库创建 / 复用
- [ ] 写明负责文档上传与解析
- [ ] 写明负责 chunk 质量检查
- [ ] 写明负责检索 sanity check
- [ ] 写明负责 retrieval gate
- [ ] 写明不负责生成 SRS
- [ ] 写明不负责执行约束增强

完成标准：B 不和 A/C 混淆。

## 3. 输入契约

- [ ] 写明 SRS Markdown 输入
- [ ] 写明 SRS PDF 输入
- [ ] 写明 Skill A gate 输入
- [ ] 写明知识库名称输入
- [ ] 写明解析策略输入
- [ ] 写明检索问题集输入

完成标准：Skill B 可直接消费 Skill A handoff。

## 4. RAGFlow 建库规则

- [ ] 写明新建知识库规则
- [ ] 写明复用知识库规则
- [ ] 写明命名规则
- [ ] 写明 dataset_id / SRS_KB_ID 记录规则
- [ ] 写明外部系统操作需确认的规则

完成标准：建库行为可控且可追踪。

## 5. Chunk 质量评估

- [ ] 写明 chunk 数量记录
- [ ] 写明短 chunk 阈值
- [ ] 写明短 chunk 比例阈值
- [ ] 写明关键章节 chunk 检查
- [ ] 写明异常 chunk 检查
- [ ] 写明报告格式

完成标准：分块质量有基本门槛。

## 6. 检索质量评估

- [ ] 写明 sanity check 问题类型
- [ ] 写明功能需求检索问题
- [ ] 写明字段规则检索问题
- [ ] 写明权限规则检索问题
- [ ] 写明异常处理检索问题
- [ ] 写明验收标准检索问题
- [ ] 写明命中判定标准

完成标准：retrieval gate 有可解释依据。

## 7. Gate 与 Handoff

- [ ] 写明 pass / conditional pass / fail
- [ ] 写明进入 Skill C 或 TestHub 的条件
- [ ] 写明 fail 时处理方式
- [ ] 写明输出文件集合

完成标准：Skill B 输出可以驱动后续流程。
