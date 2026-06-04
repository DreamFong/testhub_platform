# Source Evidence Map 模板

## 1. 基本信息

```text
project: 
target_module: 
source_project: 
srs_markdown: 
srs_pdf: 
run_id: 
status: draft
```

## 2. Evidence 质量摘要

```text
fr_total: 
fr_with_evidence: 
field_rules_total: 
field_rules_with_evidence: 
business_rules_total: 
business_rules_with_evidence: 
permission_rules_total: 
permission_rules_with_evidence: 
exception_rules_total: 
exception_rules_with_evidence: 
acceptance_criteria_total: 
acceptance_criteria_with_evidence: 
```

## 3. 功能需求 Evidence

每个 FR 必须记录可追溯源码依据。

### FR-{MODULE}-{NNN} {功能名称}

```text
summary: 
source_confidence: high | medium | low
```

#### 源码依据

| 类型 | 文件 | 类 / 方法 / 路由 | 说明 |
|---|---|---|---|
| Controller / Router |  |  |  |
| Service |  |  |  |
| Request DTO / VO |  |  |  |
| Response DTO / VO |  |  |  |
| Entity / DO |  |  |  |
| Mapper / SQL |  |  |  |
| Permission |  |  |  |
| ErrorCode |  |  |  |

#### 对应 SRS 内容

```text
章节：
段落：
```

#### Evidence 备注

- 

## 4. 字段规则 Evidence

### 字段：{field_name}

```text
所属功能：
所属对象：
规则摘要：
source_confidence: high | medium | low
```

| 规则类型 | 源码文件 | 类 / 字段 / 注解 / 方法 | 说明 |
|---|---|---|---|
| 必填 |  |  |  |
| 长度 |  |  |  |
| 格式 |  |  |  |
| 枚举 |  |  |  |
| 默认值 |  |  |  |
| 唯一性 |  |  |  |
| 其他校验 |  |  |  |

## 5. 业务规则 Evidence

### 业务规则：{rule_name}

```text
关联功能：
规则摘要：
source_confidence: high | medium | low
```

| 规则类型 | 源码文件 | 类 / 方法 | 触发条件 / 处理逻辑 |
|---|---|---|---|
| Service 校验 |  |  |  |
| 跨实体校验 |  |  |  |
| 状态变更 |  |  |  |
| 删除限制 |  |  |  |
| 导入导出处理 |  |  |  |
| 事务 / 批量处理 |  |  |  |

## 6. 权限规则 Evidence

### 权限：{permission_code}

```text
关联功能：
权限说明：
source_confidence: high | medium | low
```

| 来源类型 | 源码文件 | 注解 / 配置 / 初始化数据 | 说明 |
|---|---|---|---|
| 权限注解 |  |  |  |
| 权限码常量 |  |  |  |
| 菜单 / 角色初始化 |  |  |  |
| 特殊例外 |  |  |  |

## 7. 异常处理 Evidence

### 异常：{error_code}

```text
关联功能：
错误信息：
触发条件：
source_confidence: high | medium | low
```

| 来源类型 | 源码文件 | 常量 / 方法 | 说明 |
|---|---|---|---|
| ErrorCode 常量 |  |  |  |
| 抛出位置 |  |  |  |
| 触发条件 |  |  |  |
| 响应处理 |  |  |  |

## 8. 验收标准 Evidence

### AC-{MODULE}-{NNN} {验收项}

```text
关联功能：
验收标准摘要：
来源类型：direct_from_source | derived_from_source | requires_review
source_confidence: high | medium | low
```

| 来源类型 | 源码文件 | 类 / 方法 / 字段 | 说明 |
|---|---|---|---|
| 直接源码依据 |  |  |  |
| 由规则推导 |  |  |  |
| 需要人工复核 |  |  |  |

## 9. Evidence 质量检查

### 9.1 无依据项

| 类型 | 标识 | SRS 位置 | 问题 | 处理建议 |
|---|---|---|---|---|
| FR / Field / Rule / Permission / Error / AC |  |  |  |  |

### 9.2 与 SRS 不一致项

| Evidence 项 | SRS 内容 | 不一致说明 | 严重程度 | 处理建议 |
|---|---|---|---|---|
|  |  |  | high / medium / low |  |

### 9.3 低置信度项

| 类型 | 标识 | 原因 | 是否触发人工复核 |
|---|---|---|---|
|  |  |  | 是 / 否 |

## 10. Gate 影响

```text
has_missing_critical_evidence: true | false
has_source_conflict: true | false
requires_manual_review: true | false
recommended_gate: pass | conditional pass | fail
```

## 11. 结论

- Evidence 覆盖结论：
- 主要风险：
- 必须修复：
- 建议修复：
