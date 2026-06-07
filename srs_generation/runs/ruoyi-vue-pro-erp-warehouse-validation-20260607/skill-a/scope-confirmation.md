# Scope 自动推断与确认

## 1. 基本信息

```text
project: ruoyi-vue-pro
target_module: ERP 仓库管理
source_project: /root/projects/github/ruoyi-vue-pro
output_mode: kb-friendly
run_id: ruoyi-vue-pro-erp-warehouse-validation-20260607
status: confirmed
```

## 2. 输入摘要

### 2.1 必填输入

```text
source_project: /root/projects/github/ruoyi-vue-pro
target_module: ERP 仓库管理
```

### 2.2 选填输入

```text
entry_files:
  - /root/projects/github/ruoyi-vue-pro/yudao-module-erp/src/main/java/cn/iocoder/yudao/module/erp/controller/admin/stock/ErpWarehouseController.java
  - /root/projects/github/ruoyi-vue-pro/yudao-module-erp/src/main/java/cn/iocoder/yudao/module/erp/service/stock/ErpWarehouseService.java
  - /root/projects/github/ruoyi-vue-pro/yudao-module-erp/src/main/java/cn/iocoder/yudao/module/erp/service/stock/ErpWarehouseServiceImpl.java
scope_hint: ERP 仓库管理
reference_srs: none
domain_hints: ERP、库存、仓库主数据
```

## 9. 用户确认结果

```text
scope_confirm_status: confirmed
confirmed_by: autonomous validation
confirmed_at: 2026-06-07
```

### 9.1 最终纳入范围
- 仓库创建、修改、删除。
- 仓库详情查询、分页查询、精简列表查询。
- 仓库默认状态切换。
- 仓库导出。
- 与上述功能直接相关的字段规则、启用状态规则、默认仓库唯一性规则、存在性校验、异常处理与权限说明。

### 9.2 明确排除范围
- 采购、销售、其它出入库、盘点、调拨等下游单据业务。
- 库存数量变更、库存成本计算等库存事务能力。

### 9.3 作为依赖说明但不展开的能力
- validWarehouseList 对其它业务传入仓库编号集合的有效性校验。

## 10. Scope 风险项

| 风险 | 影响 | 处理方式 | 是否阻断 |
|---|---|---|---|
| 默认状态更新接口缺少显式权限注解 | 可能导致权限描述与主流 CRUD 不一致 | 在 SRS 中仅描述能力与例外说明，不推断额外权限 | 否 |
| validWarehouseList 未被当前 Controller 直接暴露 | 容易被误写成主功能 | 仅作为依赖规则说明，不纳入主功能 FR | 否 |