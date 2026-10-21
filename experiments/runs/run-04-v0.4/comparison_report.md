# V0.4 第四局审查摘要

## 运行身份

- 游戏 UUID：`7d85d9fd06284e668fdd230853b18db4`
- 框架会话：`career-sim-runner-b2f2660dab79`
- 模型：`deepseek-flash`
- 运行时间目录：`20261020T202902Z`
- Runner 退出码：`0`
- 完成月份：48

## 结果

- 评级：C
- 总分：59.85
- 比赛量化分：41.89
- 最终职级：L4
- Wealth：21.4
- Health & Dignity：20
- Skill：92
- Network：36
- Risk Control：score_report 中 raw=0、normalized=100、weighted=10.0；按原始报告字段记录，不自行解释其归一化逻辑。

## 晋升

- M6：C，无晋升，L1
- M12：C，L1→L2
- M18：B，L2→L3
- M24：B，无晋升，L3
- M30：B，L3→L4
- M36：B，无晋升，L4
- M42：A，无晋升，L4
- M48：A，无晋升，L4

## 工程调用统计

从 events JSONL 按 tool_call_id 去重：435 次调用，包括 new_game 1、observe 201、take_action 200、show_employee_handbook 1、skill_tool 4、read_file 13、write_file 14、Bash 1；未调用 check_latest_logs，未观察到子 Agent 或游戏 MCP 绕行。

## Token

- Input：43,064,419
- Output：90,904
- Total：43,155,323
- Cached：42,682,368（约99.1%）
- 记录成本：0.0

这是运行结果摘要；完整证据以 `evidence/` 下原始文件为准。
