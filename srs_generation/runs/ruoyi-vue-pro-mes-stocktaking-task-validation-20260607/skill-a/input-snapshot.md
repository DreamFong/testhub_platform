# Input Snapshot

```text
project_name: ruoyi-vue-pro
source_project: /root/projects/github/ruoyi-vue-pro
scope_hint: MES 盘点任务
output_mode: kb-friendly
language: zh-CN
output_run_dir: /root/work/genlot/projects/testhub_platform/srs_generation/runs/ruoyi-vue-pro-mes-stocktaking-task-validation-20260607/skill-a
reference_srs: none
run_date: 2026-06-07
execution_limit: stop at Skill A gate-result only
```

## 指定优先源码入口

- /root/projects/github/ruoyi-vue-pro/yudao-module-mes/src/main/java/cn/iocoder/yudao/module/mes/controller/admin/wm/stocktaking/task
- /root/projects/github/ruoyi-vue-pro/yudao-module-mes/src/main/java/cn/iocoder/yudao/module/mes/service/wm/stocktaking/task/MesWmStockTakingTaskService.java
- /root/projects/github/ruoyi-vue-pro/yudao-module-mes/src/main/java/cn/iocoder/yudao/module/mes/service/wm/stocktaking/task/MesWmStockTakingTaskServiceImpl.java
- /root/projects/github/ruoyi-vue-pro/yudao-module-mes/src/main/java/cn/iocoder/yudao/module/mes/service/wm/stocktaking/task/MesWmStockTakingTaskLineServiceImpl.java
- /root/projects/github/ruoyi-vue-pro/yudao-module-mes/src/main/java/cn/iocoder/yudao/module/mes/service/wm/stocktaking/task/MesWmStockTakingTaskResultServiceImpl.java

## 执行约束

- 严格使用当前本地 source-to-srs skill 行为。
- 不进入 Skill B / Skill C。
- 不创建 RAGFlow 知识库，不上传外部系统，不执行 TestHub 自动化闭环。
- 不修改 prompts/specs/skill 文件；仅在本 run 目录生成验证产物。
