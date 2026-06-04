# 下一步行动清单

## 立即下一步

- [ ] 创建 `srs_generation/specs/` 目录
- [ ] 将 Skill A spec v0.2 整理成正式文档
- [ ] 根据 `01-skill-a-spec-tasks.md` 校验 Skill A spec 是否完整
- [ ] 创建 `srs_generation/prompts/` 目录
- [ ] 起草 Skill A 总控 prompt
- [ ] 起草 scope 自动推断 prompt
- [ ] 起草 source_evidence_map 输出模板

## 本轮优先完成

- [ ] 完成 Skill A spec 文档
- [ ] 完成 Skill A scope confirm 机制文档
- [ ] 完成 Skill A 评分表
- [ ] 完成 Skill A 输出目录结构草案

## 随后推进

- [ ] 把 RuoYi-Vue-Pro 用户管理案例作为 Skill A 回归样本
- [ ] 选择第二个验证模块
- [ ] 对第二个验证模块执行 scope 推断
- [ ] 根据验证结果修订 prompt

## 暂缓事项

- [ ] 暂缓正式实现 Skill B 自动建库
- [ ] 暂缓引入 RAGAS
- [ ] 暂缓将 Skill C 执行约束混入纯 SRS 知识库
- [ ] 暂缓做最终总编排自动化

## 当前建议

先不要急着把 A/B/C 全部自动化。更稳妥的顺序是：

```text
Skill A spec 定稿
→ Skill A prompt 跑通
→ 第二样本验证
→ 再沉淀 Skill B / C
```
