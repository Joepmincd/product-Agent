# 产品 Agent 团队

当前版本：`2026.09.30.2`。产品负责人作为统一对话入口，按任务调用产品思考、调研分析、交互走查、结构图和 HTML 演示等能力。

## 安装到 Codex

需要 Python 3.11 或更新版本。克隆本仓库后，在仓库根目录执行：

```bash
python3 product-agent-team/install.py --check
python3 product-agent-team/install.py
```

第一条命令只校验安装包；第二条命令安装 Skill 和 Agent 预设到当前用户的 Codex 目录，并备份旧版。安装后新建 Codex 任务以加载新版本。可用 `--codex-home` 指定其他 Codex 目录。

## 文件说明

完整发布包位于 [`product-agent-team/`](product-agent-team/)。`SKILL.md` 是技能入口，`Agent.md` 说明读取顺序；`workflow.md` 管理分析、澄清、方案和交付流程，`project-memory-rules.md` 管理事实与项目基线。`skills/` 包含专项方法，`roles/` 包含团队分工。`release.json` 记录版本和文件校验值。

产品方案会检查实际使用过程、重要交互选择与研发可执行性。首次使用、状态、反馈、异常恢复和完成标准按任务适用性展开；不会把说明性案例当成已确认的业务事实。

## 更新产品 Agent

仓库里的 `product-agent-team/` 是发布源文件。修改这里的文件，再发布新版本；不要直接修改某个人电脑上 `~/.codex/skills/product-agent-team/` 的安装副本。

1. 先确定修改归属：阶段与澄清流程在 `workflow.md`，事实采纳与项目基线在 `project-memory-rules.md`，团队职责在 `TEAM.md`，交互标准在 `PRODUCT_INTERACTION_RULES.md` 及关联规范，具体方法在 `skills/`。`Agent.md` 只负责导航；模板只提供内容结构。
2. 修改时保留已有用户决定、授权边界和产品能力标准。新增规则尽量只写在负责该规则的文件，其他文件通过链接引用。若改了文件名或章节标题，检查所有相对链接。
3. 使用新版本号更新清单，然后校验并运行安装测试：

   ```bash
   python3 update_release.py 2026.10.01.1
   python3 product-agent-team/install.py --check
   python3 product-agent-team/scripts/test_install.py
   ```

4. 评审改动及测试结果后提交。需要在本机使用时运行安装命令；安装后新建 Codex 任务验证典型对话。协作者通过分支和 Pull Request 提交修改，说明原问题、规则变化、可能影响的任务以及验证结果。

`update_release.py` 只更新版本、发布日期和文件校验值，不会判断规则是否合理。校验器要求发布包内的文件与 `release.json` 完全一致；新建或删除文件时也必须重新生成清单。仓库根目录的 README 和更新脚本属于维护工具，不包含在安装包中。
