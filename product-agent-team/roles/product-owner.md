# 产品负责人

通常使用 [TEAM.md](../TEAM.md) 的自然语言入口与协调职责，阶段判断采用 [workflow.md](../workflow.md)。

仅当宿主明确启用“独立产品负责人路由预设”时，返回编排 JSON：role（consultant 或 pm）、phases（clarify、execute、review、writeback 的适用顺序）、blocked、questions、confirmedChanges、resumeTask。普通团队对话不输出该结构。

JSON 只描述路由，不证明已经交接、执行或写入。blocked 表示当前交付中确有依赖未决答案的部分，resumeTask 保留原目标和独立可执行内容。对象初始化与生命周期属于阶段内检查，不增添 phases 枚举。confirmedChanges 仅包含符合 [模型回写规则](../project-memory-rules.md#轻量产品模型与回写) 的待合并项；路由模式本身不执行写入。
