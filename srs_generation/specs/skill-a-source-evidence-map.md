# Skill A：Source Evidence Map 规范

版本：v0.1  
适用范围：Skill A 关键结论源码可追溯性记录

## 1. 目标

`source_evidence_map` 用于记录 SRS 中功能需求、字段规则、业务规则、权限规则、异常处理和验收标准对应的源码依据。它是 Skill A 的强制产物。

关键结论无法提供源码依据时，应触发 fail 或人工复核。

## 2. 文件格式

`source_evidence_map` 使用 Markdown 文件，建议命名为：

```text
source-evidence-map.md
```

它应至少包含：

- 基本信息。
- 功能需求 Evidence。
- 字段规则 Evidence。
- 业务规则 Evidence。
- 权限规则 Evidence。
- 异常处理 Evidence。
- 验收标准 Evidence。
- Evidence 质量检查。
- Gate 影响结论。

## 3. 功能需求 Evidence

每个主要 FR 必须记录：

- FR 编号。
- 功能名称。
- Controller / Router 来源。
- Service 来源。
- Request DTO / VO 来源。
- Response DTO / VO 来源。
- Entity / Mapper / SQL 来源。
- 权限来源。
- 异常来源。

没有公开入口但从源码推导出的能力，应标记为低置信度并触发复核。

## 4. 字段规则 Evidence

字段规则应记录：

- 字段所属对象。
- 字段来源 DTO / VO。
- 字段来源 Entity / DO。
- 校验注解或校验方法。
- 默认值来源。
- 唯一性来源。
- 枚举来源。

不得凭通用业务经验补写字段规则。

## 5. 业务规则 Evidence

业务规则应记录：

- Service 层校验逻辑。
- 跨实体校验逻辑。
- 状态变更逻辑。
- 删除限制逻辑。
- 导入导出处理逻辑。
- 事务或批量处理逻辑。

如果规则由多个方法共同形成，应记录主要调用链。

## 6. 权限规则 Evidence

权限规则应记录：

- 权限注解位置。
- 权限码。
- 菜单或角色初始化来源。
- 无需权限或特殊权限例外。
- 权限与功能需求的对应关系。

若功能入口没有权限注解，应记录为特殊情况，而不是自动推断权限。

## 7. 异常处理 Evidence

异常处理应记录：

- 错误码常量。
- 错误信息。
- 抛出异常的位置。
- 触发条件。
- 与功能需求的对应关系。

错误码本身不等同于完整异常规则，必须结合抛出位置和触发条件说明。

## 8. 验收标准 Evidence

验收标准可以分为三类来源：

```text
direct_from_source：源码直接体现。
derived_from_source：由功能和规则合理推导。
requires_review：需要人工复核。
```

对于 `derived_from_source`，必须说明推导依据。对于 `requires_review`，不得作为无争议结论。

## 9. Evidence 质量检查

必须检查：

- 是否存在无依据 FR。
- 是否存在无依据字段规则。
- 是否存在无依据权限规则。
- 是否存在无依据异常规则。
- 是否存在 evidence 与 SRS 内容不一致。
- 是否存在低置信度关键结论。

## 10. Gate 影响

以下情况会影响 Skill A gate：

- 核心 FR 无 evidence：通常 fail。
- 关键字段规则无 evidence：conditional pass 或 fail，视影响而定。
- 权限规则无 evidence 但写成确定需求：fail 或人工复核。
- 异常规则无 evidence：conditional pass 或 fail。
- 验收标准为合理推导但未说明依据：conditional pass。

## 11. 置信度定义

### high

源码中有直接入口、规则或注解支撑。

### medium

源码中有间接依据，或由多个规则合理推导。

### low

依据不完整，需要人工复核。

低置信度项不得作为无争议需求写入最终 SRS。
