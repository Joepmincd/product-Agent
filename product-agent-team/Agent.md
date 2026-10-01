# Product Agent Team

## 定位与入口

产品负责人是唯一对话入口，内部按需要采用咨询师、产品经理和专项能力。保持自然对话与渐进澄清，不要求用户切换角色或重复背景。Codex Skill 和独立 subagent 预设读取同一安装目录。

本文件是标准导航，不重复执行规则。宿主系统与开发者约束优先；用户的明确任务、授权和交付偏好优先于本包默认约定。

## 规则归属

| 内容 | 唯一维护位置 |
|---|---|
| 阶段、澄清时机、场景、生成、研发和角色交付 | [workflow.md](workflow.md) |
| 事实来源、采纳资格、模型回写、文件归档 | [project-memory-rules.md](project-memory-rules.md) |
| 团队分工与角色交接 | [TEAM.md](TEAM.md)；roles/ 只补角色专属任务 |
| 交互约束的选取与检查入口 | [PRODUCT_INTERACTION_RULES.md](PRODUCT_INTERACTION_RULES.md) |
| 交互专业原则及示例 | [P3–P6 能力项](产品经理交互体验能力项_P3-P6.md) |
| 产品类型的设计语言 | [产品大类设计语言与规范](产品大类设计语言与规范.md) |
| 走查上下文、取证、评审阈值 | [product-audit](skills/product-audit/SKILL.md) |
| 能力职责、依赖和工具降级 | [capability-matrix.md](capability-matrix.md) |
| 各类成果的专业方法 | 对应专项 Skill 及其按需引用 |

入口、角色、模板和专业方法通过链接使用共享规则。维护时改责任文件及必要的调用说明，不复制新版本正文到其他文件。专业示例仅说明规则在当前情境的应用；模板结构不新增审批或交付范围。发现实际冲突时依据责任文件处理，业务决定的缺口按工作流处理。

## 读取顺序

首次使用读取本文件、workflow.md 和 project-memory-rules.md，再读取当前项目相关上下文与任务所需专项方法。涉及交互时通过交互规约选取适用专业章节；角色协作和工具选择按需读取 TEAM.md、roles/ 和能力矩阵。同一版本已完整读取的内容可复用。

## 文件结构与安装

### 文件分层

| 层次 | 文件或目录 | 阅读目的 |
|---|---|---|
| 入口 | SKILL.md、Agent.md | 发现能力、确认规则归属与读取顺序 |
| 共享执行规则 | workflow.md、project-memory-rules.md | 决定何时澄清、推进、交付，以及哪些事实可以保存 |
| 职责与运行条件 | TEAM.md、roles/、capability-matrix.md | 确认角色分工、工具依赖与降级方式 |
| 专业标准 | PRODUCT_INTERACTION_RULES.md 及其关联规范 | 选择并应用适用的交互标准 |
| 专项方法 | skills/ 及各自 references/、assets/ | 执行当前交付任务，不重复共享规则 |
| 内容模板 | project-template.md、usecase-template.md | 按任务裁剪内容结构，不新增审批或范围 |
| 安装与校验 | install.py、release.json、codex/、scripts/ | 安装入口、校验完整性、保留升级备份 |

### 工作流导航

workflow.md 按“任务与路由 → 产品分析前置判断 → 对象与场景细化 → 文档表达 → 专业检查 → 修订交付”组织。产品思考与调研使用同一前置判断；事实采纳始终查 project-memory-rules.md。规则全文保留在归属文件，导航不替代首次必读内容。

### 安装与升级

release.json 记录版本、技能注册和文件校验值；codex/product-agent-team.toml 为预设模板。使用 Python 3.11 或更新版本运行 install.py，可用 --codex-home 指定目标；scripts/validate_package.py 校验包的完整性。安装器同步更新两个入口并备份旧版。新任务加载新版，已开始任务不保证热更新。

预设的 name、description 和 developer_instructions 由发布包维护；升级保留已有的 model、model_provider、model_reasoning_effort、model_verbosity 字符串配置。其他自定义字段留在旧预设备份中，并在安装结果中列出未保留的字段名；不会自动迁移额外权限或工具配置。旧预设无法解析或上述运行配置类型不合法时，安装器在替换前停止。
