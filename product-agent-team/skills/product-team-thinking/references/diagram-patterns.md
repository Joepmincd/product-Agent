# 产品图表示例

这里仅提供产品语义与语法示例。图型、事实核对、模板选择、排版、渲染和检查规则由 [结构化图表](../../product-team-diagrams/SKILL.md) 统一维护。示例中的能力、系统、日期和数值均是假设，不是当前产品事实或排期承诺；只复用表达方式，不复制业务规则。

## 1. 用户流程与决策树

用于入口、主路径、条件分支、失败恢复。

```mermaid
flowchart LR
    A[进入功能] --> B[填写信息]
    B --> C{校验通过?}
    C -->|是| D[提交]
    C -->|否| E[定位错误并修改]
    E --> B
    D --> F{处理成功?}
    F -->|是| G[成功态]
    F -->|否| H[保留输入并允许重试]
```


## 2. 状态机

用于订单、审批、任务、账号、内容发布等生命周期。

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Processing: 提交
    Processing --> Succeeded: 成功
    Processing --> Failed: 失败/超时
    Failed --> Processing: 重试
    Succeeded --> [*]
```


## 3. 系统时序

用于客户端、服务端、异步任务和第三方系统协作。

```mermaid
sequenceDiagram
    actor U as 用户
    participant C as 客户端
    participant S as 服务端
    participant T as 第三方
    U->>C: 提交操作
    C->>S: 创建请求（含幂等键）
    S->>T: 执行处理
    alt 成功
        T-->>S: 成功结果
        S-->>C: 完成
        C-->>U: 展示成功态
    else 失败或超时
        T-->>S: 错误/超时
        S-->>C: 可恢复错误
        C-->>U: 说明原因并提供重试
    end
```


## 4. 计划与里程碑

仅在用户需要排期或存在阶段依赖时使用。

```mermaid
gantt
    title 功能交付计划
    dateFormat  YYYY-MM-DD
    section 产品与设计
    方案确认 :a1, 2026-07-06, 3d
    设计交付 :after a1, 5d
    section 研发与验证
    开发 :after a1, 8d
    测试与灰度 :after a1, 4d
```


## 5. 数据图表

只在有真实数值时使用。趋势用折线，分类比较用柱状；样本很少或需要精确读取时用表格。

```mermaid
xychart-beta
    title "指标趋势"
    x-axis [阶段1, 阶段2, 阶段3]
    y-axis "指标值" 0 --> 100
    line [20, 45, 70]
```

## 6. 汇报问题与表达选择

| 需要解释的产品问题 | 可考虑的表达 |
| --- | --- |
| 现状如何演进为目标 | 前后对比、迁移路径 |
| 多入口如何统一 | 入口收敛图 |
| 分阶段交付有哪些依赖 | 时间线、计划与里程碑 |
| 多方如何协作 | 泳道或责任矩阵 |
| 不同资源适用哪些规则 | 规则矩阵 |
