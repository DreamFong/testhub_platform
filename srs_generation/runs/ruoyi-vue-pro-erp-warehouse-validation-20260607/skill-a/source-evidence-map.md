# Source Evidence Map

## 基本信息

```text
project: ruoyi-vue-pro
target_module: ERP 仓库管理
source_project: /root/projects/github/ruoyi-vue-pro
srs_markdown: srs-kb-friendly.md
srs_pdf: srs-kb-friendly.pdf
run_id: ruoyi-vue-pro-erp-warehouse-validation-20260607
status: completed
```

## Evidence 质量摘要

```text
fr_total: 8
fr_with_evidence: 8
field_rules_total: 8
field_rules_with_evidence: 8
business_rules_total: 4
business_rules_with_evidence: 4
permission_rules_total: 7
permission_rules_with_evidence: 7
exception_rules_total: 2
exception_rules_with_evidence: 2
acceptance_criteria_total: 7
acceptance_criteria_with_evidence: 7
```

## 功能需求 Evidence

### FR-WH-001 仓库创建
- source_confidence: high
- Controller / Router: ErpWarehouseController#createWarehouse，`POST /erp/warehouse/create`
- Service: ErpWarehouseServiceImpl#createWarehouse
- Request DTO / VO: ErpWarehouseSaveReqVO
- Entity / DO: ErpWarehouseDO
- Permission: `erp:warehouse:create`

### FR-WH-002 仓库修改
- source_confidence: high
- Controller / Router: ErpWarehouseController#updateWarehouse，`PUT /erp/warehouse/update`
- Service: ErpWarehouseServiceImpl#updateWarehouse
- Request DTO / VO: ErpWarehouseSaveReqVO
- Permission: `erp:warehouse:update`
- ErrorCode: WAREHOUSE_NOT_EXISTS

### FR-WH-003 默认仓库状态维护
- source_confidence: high
- Controller / Router: ErpWarehouseController#updateWarehouseDefaultStatus，`PUT /erp/warehouse/update-default-status`
- Service: ErpWarehouseServiceImpl#updateWarehouseDefaultStatus
- Mapper / SQL: ErpWarehouseMapper#selectByDefaultStatus
- Permission: 无显式 PreAuthorize
- ErrorCode: WAREHOUSE_NOT_EXISTS

### FR-WH-004 仓库删除
- source_confidence: high
- Controller / Router: ErpWarehouseController#deleteWarehouse，`DELETE /erp/warehouse/delete`
- Service: ErpWarehouseServiceImpl#deleteWarehouse
- Permission: `erp:warehouse:delete`
- ErrorCode: WAREHOUSE_NOT_EXISTS

### FR-WH-005 仓库详情查询
- source_confidence: high
- Controller / Router: ErpWarehouseController#getWarehouse，`GET /erp/warehouse/get`
- Service: ErpWarehouseServiceImpl#getWarehouse
- Response DTO / VO: ErpWarehouseRespVO
- Permission: `erp:warehouse:query`

### FR-WH-006 仓库分页查询
- source_confidence: high
- Controller / Router: ErpWarehouseController#getWarehousePage，`GET /erp/warehouse/page`
- Service: ErpWarehouseServiceImpl#getWarehousePage
- Request DTO / VO: ErpWarehousePageReqVO
- Mapper / SQL: ErpWarehouseMapper#selectPage（name like，status eq，id desc）
- Permission: `erp:warehouse:query`

### FR-WH-007 仓库精简列表查询
- source_confidence: high
- Controller / Router: ErpWarehouseController#getWarehouseSimpleList，`GET /erp/warehouse/simple-list`
- Service: ErpWarehouseServiceImpl#getWarehouseListByStatus
- Mapper / SQL: ErpWarehouseMapper#selectListByStatus
- Response DTO / VO: 仅映射 id、name、defaultStatus
- Permission: 无显式 PreAuthorize

### FR-WH-008 仓库导出
- source_confidence: high
- Controller / Router: ErpWarehouseController#exportWarehouseExcel，`GET /erp/warehouse/export-excel`
- Service: ErpWarehouseServiceImpl#getWarehousePage
- Response DTO / VO: ErpWarehouseRespVO Excel 字段
- 处理细节: `pageReqVO.setPageSize(PageParam.PAGE_SIZE_NONE)`
- Permission: `erp:warehouse:export`

## 字段规则 Evidence
- name：ErpWarehouseSaveReqVO `@NotEmpty(message = "仓库名称不能为空")`
- sort：ErpWarehouseSaveReqVO `@NotNull(message = "排序不能为空")`
- status：ErpWarehouseSaveReqVO `@NotNull` + `@InEnum(CommonStatusEnum.class)`
- address：ErpWarehouseSaveReqVO 可选字段
- remark：ErpWarehouseSaveReqVO 可选字段
- principal：ErpWarehouseSaveReqVO 可选字段
- warehousePrice：ErpWarehouseSaveReqVO BigDecimal 字段；ErpWarehouseRespVO 导出字段“仓储费，单位：元”
- truckagePrice：ErpWarehouseSaveReqVO BigDecimal 字段；ErpWarehouseRespVO 导出字段“搬运费，单位：元”

## 业务规则 Evidence
- 默认仓库唯一：ErpWarehouseServiceImpl#updateWarehouseDefaultStatus 在开启默认状态时先查询并关闭已有默认仓库。
- 默认仓库状态更新事务性：ErpWarehouseServiceImpl#updateWarehouseDefaultStatus 使用 `@Transactional(rollbackFor = Exception.class)`。
- 仓库存在性校验：ErpWarehouseServiceImpl#validateWarehouseExists。
- 仓库启用校验：ErpWarehouseServiceImpl#validWarehouseList；若状态禁用则抛出 WAREHOUSE_NOT_ENABLE。

## 权限规则 Evidence
- `erp:warehouse:create`：ErpWarehouseController#createWarehouse 上的 `@PreAuthorize`
- `erp:warehouse:update`：ErpWarehouseController#updateWarehouse 上的 `@PreAuthorize`
- `erp:warehouse:delete`：ErpWarehouseController#deleteWarehouse 上的 `@PreAuthorize`
- `erp:warehouse:query`：ErpWarehouseController#getWarehouse 与 getWarehousePage 上的 `@PreAuthorize`
- `erp:warehouse:export`：ErpWarehouseController#exportWarehouseExcel 上的 `@PreAuthorize`
- 默认状态维护：ErpWarehouseController#updateWarehouseDefaultStatus 无显式 `@PreAuthorize`
- 精简列表：ErpWarehouseController#getWarehouseSimpleList 无显式 `@PreAuthorize`

## 异常处理 Evidence
- WAREHOUSE_NOT_EXISTS：ErrorCodeConstants#WAREHOUSE_NOT_EXISTS；由 validateWarehouseExists 与 validWarehouseList 触发。
- WAREHOUSE_NOT_ENABLE：ErrorCodeConstants#WAREHOUSE_NOT_ENABLE；由 validWarehouseList 在仓库禁用时触发，并带入仓库名称。

## 验收标准 Evidence
- AC-WH-001：createWarehouse 与 ErpWarehouseSaveReqVO 必填校验。
- AC-WH-002：updateWarehouse + validateWarehouseExists。
- AC-WH-003：updateWarehouseDefaultStatus + selectByDefaultStatus + 关闭已有默认仓库逻辑。
- AC-WH-004：deleteWarehouse + validateWarehouseExists。
- AC-WH-005：selectPage 条件与排序逻辑。
- AC-WH-006：getWarehouseSimpleList 仅返回启用仓库且仅映射精简字段。
- AC-WH-007：exportWarehouseExcel 中取消分页限制并导出 ErpWarehouseRespVO 字段。

## Evidence 质量检查
- 无依据 FR：无。
- 无依据字段规则：无。
- 无依据权限规则：无。
- 无依据异常规则：无。
- SRS 与 evidence 不一致项：无关键冲突。
- 低置信度关键项：无。

## Gate 影响

```text
has_missing_critical_evidence: false
has_source_conflict: false
requires_manual_review: false
recommended_gate: pass
```

## 结论
- Evidence 覆盖结论：主功能、关键字段规则、默认仓库唯一性规则、权限例外与异常均可追溯到源码。
- 主要风险：正文若写入权限码、路由、注解名会损害非工程读者可读性，因此应保留在 evidence map。
- 必须修复：无。
- 建议修复：后续可单独说明 validWarehouseList 为跨模块依赖校验，而非当前 Controller 主入口。 