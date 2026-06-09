# Skill A 基线与验证收敛

Status: completed

## Objective

将 Skill A 收敛为稳定、可复用、可验证的 `source-to-srs` 能力，完成规范、模板、prompt、PDF 生成与检查、质量 gate、多样本验证以及可移植 skill 打包。

## Scope

- 固化 Skill A 职责边界、输入输出契约、scope confirm、review 与 gate。
- 建立 Skill A prompts、templates、scripts 与固定产物集合。
- 完成最小可行 Skill A 和多样本验证。
- 修复 PDF 人类可读性与文本层检查缺口。
- 同步到 portable skill：`.claude/skills/source-to-srs/`。

## Out of scope

- 不创建 RAGFlow 知识库。
- 不做 retrieval gate。
- 不进入 Skill C。
- 不执行 TestHub 自动化闭环。

## Approach

1. 用 `specs/` 固化 Skill A 契约。
2. 将执行过程拆分为 Skill A prompts、templates 与 scripts。
3. 建立 `source-evidence-map.md`、PDF gate、independent review 等关键产物。
4. 通过用户管理、角色管理、ERP 仓库管理、MES 盘点任务等样例验证。
5. 收紧非研发可读性要求，将技术细节默认下沉到 `source-evidence-map.md`。
6. 打包为 `.claude/skills/source-to-srs/`。

## Acceptance criteria

- Skill A 规范已落在 `specs/skill-a-*.md`。
- Skill A prompts、templates、scripts 已建立。
- 最小可行 Skill A 已完成。
- 多个样例 run 已通过 Skill A gate。
- PDF 文本层与可读性 gate 已建立并通过回归。
- `source-to-srs` 已作为可移植 skill 可用。

## Risks

- Skill A 规范与 portable skill references 后续可能发生漂移，需要继续遵守 repo specs 为 canonical 的同步策略。
- 主文档与 `source-evidence-map.md` 的职责边界若被放松，可能再次引入技术细节污染。

## Learnings

- `source-evidence-map.md` 必须作为强制产物存在，否则事实追溯与可读性分层很难同时成立。
- PDF gate 不能只检查文本层，必须同时检查人类可读性。
- 面向业务的主文档与面向追溯的 evidence 文档拆层，是 Skill A 可迁移性的关键前提。
