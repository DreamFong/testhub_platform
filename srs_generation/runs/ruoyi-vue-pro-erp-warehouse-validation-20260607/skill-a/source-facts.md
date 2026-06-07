# ERP 仓库管理 Source Facts

## 1. 功能事实
- 支持创建仓库，返回新建仓库编号。
- 支持更新仓库基础信息，更新前校验仓库存在。
- 支持更新仓库是否为默认仓库；当设置为默认时，会先取消现有默认仓库，再更新当前仓库状态。
- 支持删除仓库，删除前校验仓库存在。
- 支持按编号查询仓库详情。
- 支持按仓库名称、启用状态分页查询，结果按编号倒序。
- 支持查询启用状态的仓库精简列表，用于下拉选项；精简返回仅包含 id、name、defaultStatus。
- 支持按查询条件导出全部仓库数据到 Excel。

## 2. 字段与对象事实
- 保存请求包含：id、name、address、sort、remark、principal、warehousePrice、truckagePrice、status。
- 必填字段：name、sort、status。
- status 必须属于 CommonStatusEnum。
- 响应字段包含：id、name、address、sort、remark、principal、warehousePrice、truckagePrice、status、defaultStatus、createTime。

## 3. 规则事实
- 更新、删除、默认状态更新都需要先校验仓库存在。
- validWarehouseList 会校验仓库集合中的每个仓库都存在且处于启用状态，否则抛错。
- 默认仓库状态更新采用事务处理。
- 当将某个仓库设为默认时，系统会关闭已有默认仓库，保证默认仓库唯一。

## 4. 权限与异常事实
- 创建、更新、删除、查询、导出有显式权限注解。
- 默认状态更新与精简列表没有显式 PreAuthorize 注解。
- WAREHOUSE_NOT_EXISTS：仓库不存在。
- WAREHOUSE_NOT_ENABLE：仓库未启用。