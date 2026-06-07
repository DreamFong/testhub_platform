# Risk Items

## RISK-001 删除盘点结果后的数量回退口径不清

- level: high
- status: open
- scope: 盘点差异处理 / 盘点结果删除回退

### 风险描述

源码在删除盘点结果时，会将原盘点数量取相反数后传入任务行更新逻辑，用于回退该行的盘点数量与状态。但任务行更新逻辑本身采用覆盖式写入盘点数量，而不是基于既有盘点数量进行增减运算。因此，负值数量究竟表示“内部回退指令”还是会被直接视为新的盘点数量，在业务口径上存在不透明之处。

### 影响

- 盘点差异处理的业务表达无法完全收敛为单一、稳定、可对外宣称的规则。
- 若在正文中将正负数量处理方式写死，存在把实现细节误写成确定业务规则的风险。
- review 与 gate 必须显式暴露该问题，避免误判为“已完全明确”。

### 源码依据

- `MesWmStockTakingTaskResultServiceImpl#deleteStockTakingTaskResult`：使用 `result.getTakingQuantity().negate()` 调用任务行更新。
- `MesWmStockTakingTaskLineServiceImpl#updateStockTakingTaskLineTakingQuantity`：直接 `setTakingQuantity(takingQuantity)`，随后重新计算状态。

### 建议

- 在当前 Skill A 输出中将其保留为显式风险，不在正文中固化成确定业务规则。
- 若后续进入更高置信阶段，应结合运行验证或上游业务说明进一步确认删除回退的真实业务意图。
