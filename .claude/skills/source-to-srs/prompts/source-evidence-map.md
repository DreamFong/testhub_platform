# Source Evidence Map 生成 Prompt

## 角色

你负责把 source facts 和 SRS 中的关键结论映射回源码依据，生成 `source-evidence-map.md`。

## 输入

```text
source-facts.md
srs-factual-draft.md 或 srs-kb-friendly.md
scope-confirmation.md
源码文件摘录
```

## 输出

```text
source-evidence-map.md
```

## 映射对象

必须覆盖：

- 功能需求 FR
- 字段规则
- 业务规则
- 权限规则
- 异常处理
- 验收标准

## 置信度

使用三档置信度：

```text
high: 源码直接支撑
medium: 源码间接支撑或规则合理推导
low: 依据不足，需要人工复核
```

## 输出结构

```markdown
# Source Evidence Map

## 基本信息

project:
target_module:
srs_markdown:
srs_pdf:

## 功能需求 Evidence

### FR-{MODULE}-{NNN} {功能名称}

- source_confidence: high | medium | low
- Controller / Router:
- Service:
- Request DTO / VO:
- Response DTO / VO:
- Entity / Mapper / SQL:
- Permission:
- ErrorCode:
- SRS 章节：

## 字段规则 Evidence

### {field_name}

- 所属对象：
- 规则摘要：
- DTO / VO 来源：
- Entity / DO 来源：
- 校验注解 / 方法：
- 默认值来源：
- 唯一性来源：
- source_confidence:

## 业务规则 Evidence

### {rule_name}

- 关联功能：
- 规则摘要：
- Service 来源：
- Mapper / SQL 来源：
- 调用链：
- source_confidence:

## 权限规则 Evidence

### {permission_code}

- 关联功能：
- 权限注解：
- 权限码来源：
- 菜单 / 初始化来源：
- source_confidence:

## 异常处理 Evidence

### {error_code}

- 关联功能：
- 错误信息：
- 抛出位置：
- 触发条件：
- source_confidence:

## 验收标准 Evidence

### AC-{MODULE}-{NNN}

- 关联功能：
- 验收标准：
- 来源类型：direct_from_source | derived_from_source | requires_review
- 依据：
- source_confidence:

## Evidence 质量检查

- 无依据 FR：
- 无依据字段规则：
- 无依据权限规则：
- 无依据异常规则：
- SRS 与 evidence 不一致项：
- 低置信度关键项：

## Gate 影响

recommended_gate: pass | conditional pass | fail
reason:
```

## 禁止事项

- 不要为没有源码依据的内容伪造 evidence。
- 不要把 reference_srs 当作 evidence。
- 不要把 domain_hints 当作 evidence。
- 不要隐藏 low confidence 项。

## 失败条件

- 核心 FR 无 evidence。
- 关键权限或异常规则无 evidence 却写成确定需求。
- evidence 与 SRS 内容明显冲突。
