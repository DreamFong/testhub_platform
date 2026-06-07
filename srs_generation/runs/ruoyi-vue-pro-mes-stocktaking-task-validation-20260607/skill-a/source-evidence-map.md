# Source Evidence Map

## 基本信息

```text
project: ruoyi-vue-pro
target_module: MES stocktaking task
srs_markdown: srs-kb-friendly.md
srs_pdf: srs-kb-friendly.pdf
```

## 功能需求 Evidence

### FR-STOCKTAKING-001 盘点任务维护
- source_confidence: high
- Controller / Router: MesWmStockTakingTaskController#create / update / delete / get / page / export-excel
- Service: MesWmStockTakingTaskServiceImpl#createStockTakingTask / updateStockTakingTask / deleteStockTakingTask / getStockTakingTaskPage
- Request DTO / VO: MesWmStockTakingTaskSaveReqVO、MesWmStockTakingTaskPageReqVO
- Permission: `mes:wm-stock-taking-task:create`、`mes:wm-stock-taking-task:update`、`mes:wm-stock-taking-task:delete`、`mes:wm-stock-taking-task:query`、`mes:wm-stock-taking-task:export`
- ErrorCode: WM_STOCK_TAKING_TASK_NOT_EXISTS、WM_STOCK_TAKING_TASK_CODE_DUPLICATE

### FR-STOCKTAKING-002 盘点任务提交流转
- source_confidence: high
- Controller / Router: MesWmStockTakingTaskController#submit / finish / cancel
- Service: MesWmStockTakingTaskServiceImpl#submitStockTakingTask / finishStockTakingTask / cancelStockTakingTask
- Permission: `mes:wm-stock-taking-task:update`、`mes:wm-stock-taking-task:finish`
- ErrorCode: WM_STOCK_TAKING_TASK_NO_LINE、WM_STOCK_TAKING_TASK_NOT_PREPARE、WM_STOCK_TAKING_TASK_NOT_APPROVING、WM_STOCK_TAKING_TASK_CANNOT_CANCEL

### FR-STOCKTAKING-003 盘点任务行生成与维护
- source_confidence: high
- Controller / Router: MesWmStockTakingTaskLineController#get / page / create / update / delete / simple-list
- Service: MesWmStockTakingTaskLineServiceImpl#generateStockTakingLines / createStockTakingTaskLine / updateStockTakingTaskLine / deleteStockTakingTaskLine / getStockTakingTaskLineListByTaskId
- Request DTO / VO: MesWmStockTakingTaskLineSaveReqVO、MesWmStockTakingTaskLinePageReqVO
- Permission: `mes:wm-stock-taking-task:query`、`mes:wm-stock-taking-task:update`
- ErrorCode: WM_STOCK_TAKING_TASK_LINE_NOT_EXISTS、WM_STOCK_TAKING_TASK_NO_STOCK

### FR-STOCKTAKING-004 盘点结果录入与回退
- source_confidence: high
- Controller / Router: MesWmStockTakingTaskResultController#get / page / create / update / delete
- Service: MesWmStockTakingTaskResultServiceImpl#createStockTakingTaskResult / updateStockTakingTaskResult / deleteStockTakingTaskResult
- Request DTO / VO: MesWmStockTakingTaskResultSaveReqVO、MesWmStockTakingTaskResultPageReqVO
- Permission: `mes:wm-stock-taking-task:query`、`mes:wm-stock-taking-task:update`
- ErrorCode: WM_STOCK_TAKING_TASK_RESULT_NOT_EXISTS、WM_STOCK_TAKING_TASK_LINE_ALREADY_TAKEN、WM_STOCK_TAKING_TASK_NOT_APPROVING

### FR-STOCKTAKING-005 盘点差异判定
- source_confidence: medium
- Service: MesWmStockTakingTaskLineServiceImpl#updateStockTakingTaskLineTakingQuantity / calculateLineStatus / createStockTakingTaskLine(MesWmStockTakingTaskResultSaveReqVO)
- Enum: MesWmStockTakingTaskLineStatusEnum NORMAL / GAIN / LOSS
- Evidence note: 差异处理通过任务行状态表达，未见独立“差异处理单”或库存调整落账逻辑。

## 字段规则 Evidence

- task.code：MesWmStockTakingTaskServiceImpl#validateStockTakingTaskCodeUnique；MesWmStockTakingTaskMapper#selectByCode。
- task.name：MesWmStockTakingTaskSaveReqVO `@NotEmpty`。
- task.type：MesWmStockTakingTaskSaveReqVO `@NotNull`；动态盘点在 `buildStockQueryReqVO` 中额外要求 startTime 与 endTime 非空。
- task.userId：MesWmStockTakingTaskSaveReqVO `@NotNull`；AdminUserApi#validateUser。
- task.planId：MesWmStockTakingTaskSaveReqVO `@NotNull`；MesWmStockTakingPlanService#validateStockTakingPlanEnabled。
- task.blindFlag：MesWmStockTakingTaskSaveReqVO `@NotNull`。
- task.frozen：MesWmStockTakingTaskSaveReqVO `@NotNull`；submit/finish/cancel 中联动冻结与解冻。
- line.quantity / takingQuantity：MesWmStockTakingTaskLineDO；`calculateLineStatus(quantity, takingQuantity)`。
- result.lineId：updateStockTakingTaskResult 中显式置空，禁止通过修改接口变更关联任务行。
- result auto-line key：createStockTakingTaskResult 中按 taskId + itemId + areaId 查询既有任务行。

## 业务规则 Evidence

- 创建任务默认草稿：MesWmStockTakingTaskServiceImpl#createStockTakingTask 设置 `PREPARE`。
- 草稿态允许修改和删除：validateStockTakingTaskExistsAndPrepare。
- 提交前必须有任务行：submitStockTakingTask 中 `WM_STOCK_TAKING_TASK_NO_LINE`。
- 提交后进入审批中：submitStockTakingTask 设置 `APPROVING`。
- 完成只允许审批中：finishStockTakingTask 调用 validateStockTakingTaskExistsAndApproving。
- 取消已完成或已取消任务会失败：cancelStockTakingTask 中 `WM_STOCK_TAKING_TASK_CANNOT_CANCEL`。
- 冻结库存：submit 时 `updateMaterialStockFrozen(lines, true)`；finish/cancel 时解冻。
- 自动生成任务行需有库存：generateStockTakingLines 中空库存触发 `WM_STOCK_TAKING_TASK_NO_STOCK`。
- 新任务行默认状态为盘亏：generateStockTakingLines 与 createStockTakingTaskLine(MesWmStockTakingTaskLineSaveReqVO)。
- 差异状态计算：`takingQuantity > quantity => GAIN`，`takingQuantity < quantity => LOSS`，相等 => NORMAL。
- 盘点结果新增需任务处于审批中：createStockTakingTaskResult 调用 validateStockTakingTaskExistsAndApproving。
- 既有任务行若盘点数量大于 0，不允许再次录入：`existingLine.getTakingQuantity().compareTo(BigDecimal.ZERO) > 0`。
- 无匹配任务行时自动补建任务行：createStockTakingTaskResult 调用 createStockTakingTaskLine(createReqVO)。
- 删除盘点结果时以相反数更新任务行盘点数量：deleteStockTakingTaskResult 中 `result.getTakingQuantity().negate()`。
- 覆盖式更新风险：updateStockTakingTaskLineTakingQuantity 直接 `setTakingQuantity(takingQuantity)`，并非基于旧值增减。

## 权限规则 Evidence

- `mes:wm-stock-taking-task:create`：MesWmStockTakingTaskController#createStockTakingTask。
- `mes:wm-stock-taking-task:update`：任务修改、提交、取消、任务行维护、盘点结果维护。
- `mes:wm-stock-taking-task:delete`：任务删除。
- `mes:wm-stock-taking-task:query`：任务、任务行、盘点结果查询。
- `mes:wm-stock-taking-task:export`：任务导出。
- `mes:wm-stock-taking-task:finish`：完成任务。

## 异常处理 Evidence

- WM_STOCK_TAKING_TASK_NOT_EXISTS：任务不存在。
- WM_STOCK_TAKING_TASK_CODE_DUPLICATE：任务编码重复。
- WM_STOCK_TAKING_TASK_NOT_PREPARE：任务非草稿状态不可修改/删除/提交前操作。
- WM_STOCK_TAKING_TASK_NOT_APPROVING：任务非审批中状态不可录入结果或完成。
- WM_STOCK_TAKING_TASK_NO_LINE：提交时无任务行。
- WM_STOCK_TAKING_TASK_CANNOT_CANCEL：已完成或已取消的任务不可取消。
- WM_STOCK_TAKING_TASK_NO_STOCK：方案筛选后无库存可盘。
- WM_STOCK_TAKING_TASK_LINE_NOT_EXISTS：任务行不存在。
- WM_STOCK_TAKING_TASK_LINE_ALREADY_TAKEN：同一任务行已录入过大于 0 的盘点数量。
- WM_STOCK_TAKING_TASK_RESULT_NOT_EXISTS：盘点结果不存在。

## Gate 影响

```text
has_missing_critical_evidence: false
has_source_conflict: false
requires_manual_review: true
recommended_gate: conditional pass
reason: 主结论均可追溯，但“删除盘点结果时负值数量的业务口径”存在低置信解释空间，需要在 review/gate 中显式暴露。
```
