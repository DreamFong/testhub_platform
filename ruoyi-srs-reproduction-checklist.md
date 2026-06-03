# RuoYi 用户管理 SRS 复现执行清单

## 1. 文档目的

本文用于指导按顺序复现 `ruoyi-user-management-srs-v2.pdf` 的生成过程。目标不是直接生成最终文件名相同的 PDF，而是按既有主线，复现以下过程：

```text
开源项目源码
→ 逆向整理 PRD 文本
→ 生成 PRD PDF
→ 在 RAGFlow 中验证 PDF 分块质量
→ 识别文本层结构问题
→ 重构为更适合检索的 SRS v2
→ 再次验证分块质量
→ 投入 RAGFlow → TestHub 自动化链路
```

---

## 2. 执行前提清单

开始前，先确认以下条件全部具备。

### 2.1 源码与分析对象

- [ ] 已获取 `RuoYi-Vue-Pro` 源码
- [ ] 可访问用户管理模块相关代码
- [ ] 已确认重点阅读对象：
  - `UserController`
  - `AdminUserServiceImpl`
  - `UserSaveReqVO`
  - 权限/字典/SQL 相关数据

### 2.2 本地文档生成环境

- [ ] 可生成 Markdown / TXT / PDF
- [ ] 已安装或准备 PDF 生成工具
- [ ] 至少具备一种初版 PDF 生成方式
- [ ] 至少具备一种优化版 PDF 生成方式

### 2.3 RAGFlow 环境

- [ ] 有可用的 RAGFlow 实例
- [ ] 可创建知识库
- [ ] 可上传 PDF 文档
- [ ] 可触发解析
- [ ] 可查看 chunks
- [ ] 可执行检索测试

### 2.4 后续闭环验证环境

- [ ] 已有 API 文档知识库或可用 API 文档输入
- [ ] 有可用的 RAGFlow Agent 工作流环境
- [ ] 有可用的 TestHub 导入与执行环境

---

## 3. 最终交付物清单

完成后，至少应得到以下产物：

- [ ] 一份源码逆向整理后的 PRD 文本
- [ ] 一份初版 PRD PDF
- [ ] 一份 RAGFlow 分块测试记录
- [ ] 一份优化后的 SRS v2 文本/结构稿
- [ ] 一份优化后的 SRS v2 PDF
- [ ] 一份优化版 PDF 的 RAGFlow 分块结果
- [ ] 一份可用于 RAGFlow → TestHub 的需求文档输入

建议统一保留这些文件：

```text
artifacts/ruoyi-user-management-prd.txt
artifacts/ruoyi-user-management-prd.pdf
artifacts/ruoyi-user-management-srs-v2.md
artifacts/ruoyi-user-management-srs-v2.pdf
artifacts/ragflow-chunk-evaluation.md
```

---

## 4. 执行步骤

按顺序执行，不要跳步。

### 步骤 1：拉起源码分析范围

目标：明确逆向整理的输入边界。

执行动作：

1. 打开 `RuoYi-Vue-Pro` 源码仓库。
2. 定位用户管理相关实现。
3. 重点阅读以下对象：
   - Controller：接口入口、请求路径、主流程
   - Service：业务规则、校验逻辑、异常分支
   - Request/Response VO：字段定义、必填项、格式约束
   - 权限/字典/SQL：角色、状态、枚举、依赖关系
4. 记录用户管理模块的核心能力：
   - 新增用户
   - 查询用户
   - 修改用户
   - 删除用户
   - 导入/导出（如存在）
   - 唯一性校验
   - 权限与状态相关规则

本步输出：

- 一份源码阅读笔记
- 一份功能点与规则清单

验收标准：

- 能明确说出用户管理模块的核心功能
- 能明确列出关键字段、校验规则、异常类型

---

### 步骤 2：逆向整理 PRD 文本

目标：把源码实现整理成产品需求文档文本。

执行动作：

1. 新建 PRD 文本初稿。
2. 建议使用以下结构：

```text
1. 模块目标
2. 角色与使用场景
3. 核心功能流程
4. 字段规则
5. 业务规则
6. 异常处理
7. 验收要点
```

3. 写入内容时遵循以下规则：
   - 从实现中提炼需求语义，不抄代码
   - 不写无关技术细节
   - 必填/可选字段分开写
   - 唯一性约束单独写
   - 失败场景单独写
   - 导入类能力如存在，单独列异常规则

建议至少覆盖以下信息：

- 用户账号、昵称、密码等字段要求
- 手机号、邮箱是否唯一
- 是否存在部门、岗位、性别、备注、头像等可选字段
- 创建、编辑、删除、查询时的约束
- 导入失败场景
- 常见错误提示语义

本步输出：

- `artifacts/ruoyi-user-management-prd.txt`

验收标准：

- 文本能被非研发读者理解
- 字段规则、异常处理、主流程已成体系

---

### 步骤 3：生成初版 PRD PDF

目标：得到第一版可送入 RAGFlow 的需求文档 PDF。

执行动作：

1. 将 PRD 文本转换成 PDF。
2. 第一版允许使用当前最方便的 PDF 生成方案。
3. 生成后检查 PDF 的阅读效果：
   - 标题是否明显
   - 内容是否连续
   - 是否大量逐行 bullet
   - 字段规则是否过碎

本步输出：

- `artifacts/ruoyi-user-management-prd.pdf`

验收标准：

- PDF 可正常打开
- 文档结构完整
- 无明显乱码或排版崩坏

---

### 步骤 4：将初版 PDF 上传 RAGFlow 做分块测试

目标：判断第一版 PDF 是否适合作为知识库输入。

执行动作：

1. 在 RAGFlow 创建测试知识库。
2. 上传初版 PRD PDF。
3. 依次测试以下组合：
   - `book + DeepDOC`
   - `book + Plain Text`
   - `naive + DeepDOC`
   - 如有条件，再补 Vision / overlap 测试
4. 记录每组测试结果：
   - chunk 数量
   - 是否出现大量碎片
   - 标题与正文是否被拆开
   - 字段规则和异常说明是否被拆散
   - 检索是否能命中关键问题

建议验证问题：

- 新增用户的必填字段是什么？
- 用户账号是否有唯一性要求？
- 手机号和邮箱是否允许重复？
- 删除用户的业务规则是什么？
- 导入失败有哪些典型场景？

本步输出：

- `artifacts/ragflow-chunk-evaluation.md`

验收标准：

- 至少能明确判断初版 PDF 是否存在结构性分块问题
- 能指出问题是否来自 parser，还是来自 PDF 文本层结构

---

### 步骤 5：定位问题并重构 SRS v2 结构

目标：把初版 PRD 改造成更适合 RAGFlow 检索的 SRS 风格文档。

执行动作：

1. 根据分块结果重写文档结构。
2. 将以下内容明确化并集中写入：
   - 必填字段
   - 可选字段
   - 唯一性异常
   - 导入异常
   - Error Handling and Messages
3. 调整文档表达方式：
   - 减少碎片化 bullet
   - 增加连续段落说明
   - 保证标题后有完整正文
   - 字段规则与对应业务说明放在相邻位置
4. 建议使用更接近 SRS 的章节结构：

```text
1. Overview
2. Functional Requirements
3. Field Rules
4. Business Rules
5. Error Handling and Messages
6. Acceptance Criteria
```

本步输出：

- `artifacts/ruoyi-user-management-srs-v2.md`

验收标准：

- 文档结构比 PRD 更稳定
- 字段规则、异常处理、流程语义更集中
- 明显优于逐行 bullet 风格

---

### 步骤 6：生成优化版 SRS v2 PDF

目标：得到适合再次送入 RAGFlow 验证的优化版 PDF。

执行动作：

1. 将重构后的 SRS v2 文本转成 PDF。
2. 生成时优先保证：
   - 标题层级清晰
   - 标题下是连续正文
   - 避免把每个要点都拆成独立行
   - 让段落更接近自然需求文档结构
3. 生成后检查：
   - 标题和正文是否连续
   - 字段规则段落是否完整
   - Error Handling 章节是否可独立检索

本步输出：

- `artifacts/ruoyi-user-management-srs-v2.pdf`

验收标准：

- PDF 文本层结构明显优于初版 PRD PDF
- 适合再次上传 RAGFlow 做分块验证

---

### 步骤 7：对优化版 PDF 再做一次 RAGFlow 验证

目标：确认 SRS v2 的 chunk 质量已达到可用水平。

执行动作：

1. 上传 `artifacts/ruoyi-user-management-srs-v2.pdf`
2. 优先测试 `book + DeepDOC`
3. 记录结果：
   - chunk 数量
   - 碎片率
   - 检索命中情况
4. 再次使用关键问题检索验证：
   - 必填字段
   - 可选字段
   - 唯一性约束
   - 导入异常
   - Error Handling

本步输出：

- 更新 `artifacts/ragflow-chunk-evaluation.md`

验收标准：

- chunk 数量和碎片率明显优于初版
- 关键信息能稳定检索到
- 可作为后续 Agent 输入文档

---

### 步骤 8：投入 RAGFlow → TestHub 自动化链路验证

目标：确认这份 SRS 不只是可检索，还能支撑后续自动化闭环。

执行动作：

1. 将优化后的 SRS v2 作为 requirement knowledge input。
2. 与 API 文档知识库一起绑定到 RAGFlow Agent。
3. 用最小场景做验证，例如：

```text
管理员登录
→ 创建用户
→ 查询用户
→ 修改用户
→ 删除用户
```

4. 观察：
   - 是否能基于 SRS + API 文档生成候选 JSON
   - 是否能导入 TestHub
   - 是否能执行最小闭环

本步输出：

- 一份链路验证结果记录

验收标准：

- SRS 可作为真实自动化链路输入
- 不只是“看起来像需求文档”，而是“能支撑生成和执行”

---

## 5. 执行顺序总览

严格按以下顺序执行：

```text
1. 阅读源码
2. 整理 PRD 文本
3. 生成初版 PDF
4. 上传 RAGFlow 做分块测试
5. 重构为 SRS v2
6. 生成优化版 PDF
7. 再次上传 RAGFlow 验证
8. 投入 RAGFlow → TestHub 链路验证
```

---

## 6. 每一步完成后必须回答的问题

为防止只做动作、不做判断，每一步完成后都回答以下问题：

### 步骤 1 后
- 我是否已经列清楚核心功能、字段规则、异常分支？

### 步骤 2 后
- 这份 PRD 是否已经脱离代码细节，变成可读的需求表述？

### 步骤 3 后
- 初版 PDF 是否明显存在逐行 bullet、内容碎片化问题？

### 步骤 4 后
- 问题究竟出在解析器，还是出在 PDF 文本层结构？

### 步骤 5 后
- SRS v2 是否已经把字段规则、异常处理、错误消息集中表达？

### 步骤 6 后
- 优化版 PDF 是否比初版更接近真实需求文档结构？

### 步骤 7 后
- SRS v2 的检索效果是否已经达到可用水平？

### 步骤 8 后
- 这份文档是否真的支撑了生成、导入、执行闭环？

---

## 7. 最终完成标准

只有满足以下条件，才算复现完成：

- [ ] 已完成源码 → PRD → PDF → SRS v2 的完整链路
- [ ] 已得到一份结构稳定的 SRS v2 PDF
- [ ] 已通过 RAGFlow 分块与检索验证
- [ ] 已确认该文档可进入 RAGFlow → TestHub 自动化链路

如果只完成到 RAGFlow 检索验证，则算完成了“文档复现”；
如果进一步完成到 TestHub 导入执行，则算完成了“闭环复现”。
