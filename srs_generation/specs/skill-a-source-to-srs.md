# Skill A：源码逆向生成 SRS 规范

版本：v0.2  
状态：draft  
适用阶段：Skill A 规范固化与可执行化前置规范

## 1. 文档目的

本文档用于规范 Skill A 的职责、输入、输出、执行流程、质量评审与交接方式。Skill A 的目标是将一个明确业务模块的源码实现逆向整理为结构化 SRS 文档，并生成后续可进入知识库链路的标准产物。

本文档不是单次实验记录。当前 RuoYi-Vue-Pro 用户管理模块案例是 Skill A 规范形成的验证样本之一，用于校验规范是否可复现、可迁移、可评审。

## 2. 适用范围与非适用范围

### 2.1 适用范围

Skill A 适用于以下场景：

- 已有源码实现，需要逆向生成需求规格说明。
- 已明确目标业务模块，但不一定完整知道模块范围。
- 希望生成适合后续进入 RAGFlow 等知识库系统的 SRS 文档。
- 希望 SRS 中的关键功能、规则、权限、异常可追溯到源码依据。
- 希望在进入知识库构建前先完成文档质量评审。

Skill A 的标准链路为：

```text
源码 / 配置 / 数据结构 / 错误码 / 权限点
→ scope 自动推断与确认
→ 需求语义抽取
→ SRS Markdown
→ SRS PDF
→ 文档质量评审
→ Skill B handoff
```

### 2.2 非适用范围

Skill A 不负责以下工作：

- 不负责创建 RAGFlow 知识库。
- 不负责 RAGFlow chunk 质量评估。
- 不负责 retrieval gate。
- 不负责 RAGAS 等检索指标评估。
- 不负责执行约束增强。
- 不负责真实接口调用闭环验证。
- 不负责从运行时日志反推未在源码中体现的业务规则。

对应边界为：

```text
Skill A：评估 SRS 文档质量
Skill B：评估知识库分块与检索质量
Skill C：提炼执行约束增强层
```

## 3. 背景与目标

### 3.1 源码逆向生成 SRS 的目标

Skill A 的核心目标不是解释源码，而是把源码中已经实现的业务能力逆向整理为需求规格说明。最终 SRS 应能回答：

- 该模块包含哪些功能需求？
- 每个功能的输入、输出、前置条件和主要规则是什么？
- 字段规则、业务规则、权限规则和异常规则是什么？
- 哪些能力明确不在本次模块范围内？
- 关键需求和规则分别来自哪些源码依据？

### 3.2 默认输出 kb-friendly 的原因

Skill A 默认输出 `kb-friendly` SRS，即知识库友好版 SRS。

原因是：

- 后续主要用途是进入知识库构建与检索链路。
- 连续段落比复杂表格更适合文本提取和 chunk 解析。
- 稳定标题、稳定编号和低表格依赖更利于检索。
- 字段规则、异常处理、验收标准需要能被稳定召回。

`aligned` 版本仅作为显式要求时的可选输出，用于对齐历史 SRS 风格或复现既有文档结构。

### 3.3 需要 scope confirm 的原因

用户通常只能提供目标模块名称，未必能在开始时完整列出模块功能边界。如果直接生成 SRS，容易出现两类问题：

- 范围过窄：漏掉导入、导出、批量操作、状态变更等边界功能。
- 范围过宽：把部门、角色、权限、配置等相邻模块误纳入本轮 SRS。

因此 Skill A 必须先自动推断候选 scope，再由用户确认。未完成 scope confirm，不得进入正式 SRS 生成。

### 3.4 需要源码依据映射的原因

SRS 是从源码逆向生成的，因此关键结论必须可审计。源码依据映射文件 `source-evidence-map.md` 用于记录 SRS 中功能、字段、业务规则、权限、异常和验收标准对应的源码依据。

它用于：

- 降低编造风险。
- 支撑独立评审。
- 支撑人工复核。
- 支撑后续样本迁移验证。

关键结论无法提供源码依据时，应触发 `fail` 或人工复核。

## 4. 输入契约

### 4.1 必填输入

#### source_project

源码项目根目录。

示例：

```text
~/projects/github/ruoyi-vue-pro
```

#### target_module

目标业务模块名称，用于指示本次逆向生成的核心对象。

示例：

```text
system user management
```

### 4.2 选填输入

#### entry_files

用户已知的关键入口文件列表。若提供，Skill A 应优先从这些文件出发推断范围与抽取事实；若未提供，Skill A 应自行发现候选入口。

示例：

```text
UserController.java
AdminUserServiceImpl.java
AdminUserMapper.java
```

#### scope_hint

用户提供的范围提示，用于辅助候选 scope 推断。`scope_hint` 不是必填项，也不是事实来源。

规则：

```text
scope_hint 是提示，不是事实来源。
若 scope_hint 与源码事实冲突，以源码事实为准。
```

#### reference_srs

历史 SRS 或目标风格参考件。它只用于章节组织、编号风格、表达风格参考，不得覆盖源码事实。

规则：

```text
reference_srs 只能影响表达方式，不能改变源码事实。
```

#### output_mode

输出模式。

可选值：

- `kb-friendly`
- `aligned`
- `both`

默认值：

```text
kb-friendly
```

#### domain_hints

用户提供的业务术语、角色定义、边界说明、排除项等辅助上下文。它只能帮助理解，不得被直接写成确定需求。

### 4.3 输入默认值

当用户未显式提供时，Skill A 应使用以下默认值：

```text
entry_files = 自动发现
scope_hint = 空
reference_srs = 空
output_mode = kb-friendly
domain_hints = 空
```

### 4.4 参数优先级

事实来源优先级如下：

```text
源码事实 > 已确认 scope > 用户提示 > 历史 SRS 风格参考
```

任何用户提示、历史文档或模型推断都不得覆盖源码中可验证的事实。

## 5. Scope 自动推断与确认机制

### 5.1 设计原则

Skill A 不要求用户预先完整定义模块范围。用户只提供 `source_project` 和 `target_module` 时，Skill A 也必须能先推断候选范围，再请求用户确认。

该机制是正式生成前的强制前置 gate。

```text
未完成 scope confirm，不进入正式 SRS 生成。
```

### 5.2 自动推断来源

Skill A 应综合以下信号推断候选 scope：

- Controller / Router
- Service / Use case
- ReqVO / DTO / Schema
- RespVO / View object
- Entity / DO / Mapper
- 权限注解 / 权限码
- import / export 相关类
- ErrorCodeConstants / 异常定义
- SQL / migration / 初始化数据
- 用户提供的 `entry_files`
- 用户提供的 `scope_hint`

### 5.3 候选范围输出格式

Skill A 应把推断结果拆成两类。

#### 候选纳入范围

明确看起来属于本模块主线的功能点。

示例：

```text
候选范围：
- 用户列表查询
- 用户详情查询
- 新增用户
- 编辑用户
- 删除用户
- 批量删除用户
- 重置密码
- 修改用户状态
- 导入用户
- 导出用户
```

#### 待确认的相邻能力

可能相关，但是否纳入取决于本轮目标的能力。

示例：

```text
待确认的相邻能力：
- 用户角色关联
- 用户数据权限
- 部门树联动筛选
```

### 5.4 用户确认机制

Skill A 在正式生成前必须向用户提出确认问题：

```text
请确认：
1. 上述候选范围是否全部纳入？
2. 哪些能力应排除？
3. 是否有遗漏的能力需要补充？
```

用户确认后，应形成一份 scope confirmation 记录，至少包含：

- 最终纳入范围。
- 明确排除范围。
- 待后续复核的范围风险。
- 确认状态。

### 5.5 Scope Confirm Gate 状态

Scope confirm gate 有三种状态：

#### confirmed

用户确认候选范围可直接进入生成。

#### confirmed_with_changes

用户补充或排除了部分能力后进入生成。

#### blocked

范围仍不明确，不允许继续生成正式 SRS。

### 5.6 blocked 处理方式

出现以下情况时，应进入 `blocked`：

- 无法定位目标模块入口文件。
- 候选范围与用户目标明显不一致。
- 相邻能力边界无法判断，且会显著影响 SRS 内容。
- 用户未完成范围确认。

`blocked` 时，Skill A 应输出需要用户补充的信息，而不是继续生成。

## 6. 标准执行流程

### Step 0：输入标准化

规范化用户输入，确定：

- `source_project`
- `target_module`
- `entry_files`
- `scope_hint`
- `reference_srs`
- `output_mode`
- `domain_hints`

输出：输入快照。

### Step 1：候选范围推断

基于源码结构、入口文件、权限码、错误码、DTO / VO、Service 方法等信息，输出候选范围和待确认相邻能力。

输出：scope inference 结果。

### Step 2：用户确认范围

用户确认、补充或排除范围。只有完成 scope confirm 后，才能进入后续步骤。

输出：scope confirmation 记录。

### Step 3：源码事实抽取

从已确认范围内抽取以下六类事实：

1. 功能点
2. 字段规则
3. 业务规则
4. 权限规则
5. 异常处理
6. 验收要点

要求：

```text
优先抽取可直接由源码支持的事实。
不得为了补全文档结构而编造需求。
```

输出：source facts。

### Step 4：事实草稿生成

先生成一版以准确性和完整性为优先的事实草稿。该草稿不追求最终文风，重点是：

- 不漏核心功能。
- 不漏关键规则。
- 标记不确定项。
- 保留源码依据。

输出：SRS factual draft。

### Step 5：正式 SRS 改写

按 `output_mode` 生成正式 SRS。

#### kb-friendly

要求：

- 优先连续段落。
- 控制表格依赖。
- 标题稳定。
- 编号清晰。
- 字段规则、异常处理、验收标准适合检索。

#### aligned

要求：

- 尽量对齐历史 SRS 的章节风格。
- 尽量贴近历史表达习惯。
- 不得偏离源码事实。

输出：最终 SRS Markdown。

### Step 6：PDF 生成与基础检查

Skill A 应生成 SRS PDF，并至少检查：

- PDF 是否生成成功。
- PDF 文本层是否可提取。
- 一级 / 二级标题是否可识别。
- FR 编号是否可识别。
- 关键字段规则是否可检索。
- 关键异常规则是否可检索。

说明：

```text
这一步只做文档可用性检查，不做知识库 chunk 质量检查。
```

输出：SRS PDF 与 PDF text check 报告。

### Step 7：质量评审与 gate

执行三阶段质量评审：

1. 生成 Agent 自评。
2. 独立评审 Agent 正式评分。
3. 必要时人工复核。

输出：self review report、independent review report、gate 结果。

## 7. 输出契约

### 7.1 主产物

#### srs_markdown

最终 SRS Markdown 文档。

命名建议：

```text
{project}-{module}-srs-kb-friendly.md
{project}-{module}-srs-aligned.md
```

#### srs_pdf

最终 SRS PDF 文档。

命名建议：

```text
{project}-{module}-srs-kb-friendly.pdf
{project}-{module}-srs-aligned.pdf
```

### 7.2 支撑产物

#### source-evidence-map.md

源码依据清单。最低要求：

- 主要功能点可溯源。
- 关键字段规则可溯源。
- 关键业务规则可溯源。
- 关键权限规则可溯源。
- 关键异常规则可溯源。
- 关键验收要点可溯源或明确说明其推导依据。

#### self_review_report

生成 Agent 自评分报告。用于自检和暴露风险点，不作为最终通过依据。

#### independent_review_report

独立评审 Agent 正式评审报告。作为默认机器主评分来源。

#### risk_items

待人工复核风险项清单。应包含：

- 范围风险。
- 源码依据不足风险。
- 规则推断风险。
- 文档表达风险。
- PDF 可用性风险。

#### pdf_text_check_report

PDF 文本层检查报告。用于判断 PDF 是否具备进入 Skill B 的基础条件。

### 7.3 文件命名建议

建议每次运行使用独立目录：

```text
srs_generation/runs/{project}-{module}-{run_id}/skill-a/
```

建议文件集合：

```text
input-snapshot.md
scope-inference.md
scope-confirmation.md
source-facts.md
srs-factual-draft.md
srs-kb-friendly.md
srs-kb-friendly.pdf
source-evidence-map.md
pdf-text-check-report.md
self-review-report.md
independent-review-report.md
risk-items.md
gate-result.md
```

## 8. SRS 文档模板

### 8.1 默认章节

Skill A 默认输出以下章节：

1. 文档概述
2. 模块范围
3. 角色与权限概述
4. 功能需求
5. 字段与输入规则
6. 业务规则
7. 异常处理规则
8. 验收标准
9. 明确排除项
10. 源码依据说明

### 8.2 FR 编号规则

功能需求使用稳定 FR 编号。

推荐格式：

```text
FR-{MODULE}-{NNN}
```

示例：

```text
FR-USER-001 用户列表查询
FR-USER-002 用户详情查询
FR-USER-003 新增用户
```

要求：

- 同一 SRS 内编号唯一。
- 编号顺序优先按业务流程和接口主线排列。
- 不因文档改写随意变更已确定编号。

### 8.3 kb-friendly 表达规则

`kb-friendly` 版本应满足：

- 使用稳定标题层级。
- 每个功能需求独立成段。
- 字段规则、异常规则、验收标准优先使用连续段落或短列表。
- 避免大表格承载关键信息。
- 避免把多个关键规则压缩到一个复杂单元格中。
- 保留足够关键词，便于检索命中。

### 8.4 aligned 表达规则

`aligned` 版本应满足：

- 仅在用户显式要求时生成。
- 可以参考历史 SRS 的章节结构和表达风格。
- 不得为了对齐历史文档而新增源码中不存在的功能或规则。
- 如果历史 SRS 与源码事实冲突，应以源码事实为准，并在风险项中记录。

### 8.5 表格使用限制

表格可以用于摘要，但不应承载唯一的关键规则来源。

以下内容在 `kb-friendly` 版本中应优先使用段落或列表：

- 字段规则。
- 权限规则。
- 错误处理。
- 验收标准。

## 9. 评分与 Gate

### 9.1 五维评分模型

Skill A 使用 5 个维度评分，每项 5 分，总分 25 分：

1. 功能覆盖度
2. 源码准确度
3. 规则完整度
4. 需求表达质量
5. 知识库友好度

### 9.2 评分维度说明

#### 功能覆盖度

评估核心功能、边界功能和明确排除项是否完整。

#### 源码准确度

评估 SRS 是否忠于源码事实，是否存在误读、编造或关键规则写反。

#### 规则完整度

评估字段规则、业务规则、权限规则、异常处理和验收要点是否充分。

#### 需求表达质量

评估文档是否以需求规格方式表达，而不是源码阅读笔记。

#### 知识库友好度

评估标题、编号、段落、表格使用和 PDF 文本层是否适合后续知识库处理。

### 9.3 硬性不合格项

以下任一命中即 `fail`：

1. 编造源码中不存在的需求、字段、权限或流程。
2. 核心功能缺失。
3. 关键规则写反。
4. 文档结构不可用。
5. PDF 文本层不可提取。
6. 关键结论无法提供源码依据。

### 9.4 自评机制

生成 Agent 自评只用于：

- 自检。
- 暴露风险点。
- 标记不确定项。

自评不能作为最终通过依据。

### 9.5 独立评审机制

独立评审 Agent 是默认机器正式评分来源。

要求：

- 使用独立上下文。
- 使用独立提示词。
- 检查 SRS 与 `source-evidence-map.md` 的一致性。
- 检查硬性不合格项。
- 输出正式评分与 gate 建议。

### 9.6 人工复核机制

以下情况应触发人工复核：

- 自评与正式评审总分相差 3 分及以上。
- 是否命中硬性不合格项存在争议。
- 正式评审结果为 `conditional pass`。
- 模块规则复杂、跨模块边界不清或推断性强。

人工复核拥有最高裁决优先级。

### 9.7 Gate 结果定义

#### pass

满足：

- 无硬性不合格项。
- 文档质量可直接进入 Skill B。
- 只有轻微表达问题或非阻断问题。

#### conditional pass

满足：

- 无致命问题。
- 存在少量必须修改项。
- 修正后可进入 Skill B。

#### fail

满足任一：

- 命中硬性不合格项。
- 核心功能或关键规则明显缺失。
- 文档不具备可靠交接条件。

### 9.8 进入 Skill B 的条件

允许进入 Skill B 的条件：

- gate 为 `pass`。
- 或 gate 为 `conditional pass` 且必须修改项已经完成并通过复核。

不允许进入 Skill B 的条件：

- gate 为 `fail`。
- scope confirm 未完成。
- PDF 文本层不可提取。
- 关键结论无源码依据且未完成人工复核。

## 10. Skill A → Skill B Handoff

### 10.1 最小 handoff 文件集合

Skill A 向 Skill B 至少交付：

1. 最终版 SRS Markdown。
2. 最终版 SRS PDF。
3. 源码依据映射文件 `source-evidence-map.md`。
4. `independent_review_report`。
5. `gate-result`。
6. `pdf_text_check_report`。
7. 输出模式标记。

### 10.2 默认交接版本

默认交接版本为：

```text
kb-friendly
```

如果同时生成 `aligned`，也不得默认用 aligned 进入 Skill B，除非用户明确要求。

### 10.3 conditional pass 交接规则

`conditional pass` 不应自动进入 Skill B。必须满足：

- 必须修改项已完成。
- 修改后通过复核。
- gate 结果更新为 `pass`，或人工明确允许带条件进入 Skill B。

### 10.4 fail 处理规则

`fail` 时不得交接给 Skill B。Skill A 应输出：

- fail 原因。
- 命中的硬性不合格项。
- 必须修改项。
- 是否需要重新执行 scope confirm。

## 11. 附录

### 11.1 输入示例

```text
source_project: ~/projects/github/ruoyi-vue-pro
target_module: system user management
entry_files:
  - UserController.java
  - AdminUserServiceImpl.java
output_mode: kb-friendly
scope_hint: 用户列表、详情、新增、编辑、删除、导入导出、重置密码、状态修改
reference_srs: docs/ruoyi-user-management-srs-v2.pdf
```

### 11.2 Scope 输出示例

```text
候选范围：
- 用户列表查询
- 用户详情查询
- 新增用户
- 编辑用户
- 删除用户
- 批量删除用户
- 重置密码
- 修改用户状态
- 导入用户
- 导出用户

待确认的相邻能力：
- 用户角色关联
- 数据权限规则
- 部门树筛选联动

请确认：
1. 上述候选范围是否全部纳入？
2. 哪些应排除？
3. 是否有遗漏项？
```

### 11.3 source-evidence-map.md 示例

```text
FR-USER-001 用户列表查询
- Controller: UserController#getUserPage
- Service: AdminUserServiceImpl#getUserPage
- Request: UserPageReqVO
- Response: UserRespVO

字段规则：username 必填且唯一
- Request: UserSaveReqVO
- Entity: AdminUserDO
- Service: AdminUserServiceImpl#validateUserForCreateOrUpdate

异常规则：用户不存在
- ErrorCode: USER_NOT_EXISTS
- Service: AdminUserServiceImpl#validateUserExists

权限规则：用户查询
- Permission: system:user:query
- Controller: UserController#getUserPage
```

### 11.4 评分表示例

```text
功能覆盖度：5/5
源码准确度：4/5
规则完整度：4/5
需求表达质量：5/5
知识库友好度：5/5
总分：23/25

硬性不合格项：未命中
Gate：pass
```

### 11.5 Gate 输出示例

```text
gate: pass
reason: SRS 覆盖目标模块核心功能，关键规则可由源码依据支撑，PDF 文本层可提取。
required_fixes: []
recommended_improvements:
  - 可进一步补充导入失败场景的验收标准。
risk_items:
  - 部门树筛选联动属于相邻能力，已记录为非本轮核心范围。
next_stage: Skill B
```
