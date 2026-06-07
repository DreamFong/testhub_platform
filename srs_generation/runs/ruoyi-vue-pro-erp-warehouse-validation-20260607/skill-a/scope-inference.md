# ERP 仓库管理 Scope 推断

## 基本信息

```text
project: ruoyi-vue-pro
target_module: ERP 仓库管理
source_project: /root/projects/github/ruoyi-vue-pro
output_mode: kb-friendly
run_id: ruoyi-vue-pro-erp-warehouse-validation-20260607
status: inferred
```

## 入口发现结果

### Controller / Router
- ErpWarehouseController：创建、更新、更新默认仓库状态、删除、详情、分页、精简列表、导出。

### Service / Use Case
- ErpWarehouseService / ErpWarehouseServiceImpl：创建、更新、默认状态切换、删除、按状态列表、分页、有效性校验。

### DTO / VO / Schema
- ErpWarehouseSaveReqVO
- ErpWarehousePageReqVO
- ErpWarehouseRespVO

### Entity / Mapper
- ErpWarehouseDO
- ErpWarehouseMapper

### 权限码
- erp:warehouse:create
- erp:warehouse:update
- erp:warehouse:delete
- erp:warehouse:query
- erp:warehouse:export
- 精简列表与默认状态更新接口无显式权限注解

### 错误码
- WAREHOUSE_NOT_EXISTS
- WAREHOUSE_NOT_ENABLE

## 候选纳入范围
- 仓库创建
- 仓库更新
- 仓库默认状态更新
- 仓库删除
- 仓库详情查询
- 仓库分页查询
- 仓库精简列表查询
- 仓库导出
- 仓库存在性校验
- 启用状态校验
- 默认仓库唯一性规则

## 相邻能力
- validWarehouseList 主要服务于其它 ERP 单据或库存业务，建议只作为依赖规则说明，不展开为主功能。

## 建议结论
```text
scope_confirm_status: confirmed
confirmed_by: autonomous validation
confirmed_at: 2026-06-07
```