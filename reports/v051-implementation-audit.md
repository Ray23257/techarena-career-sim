# V0.5.1 Implementation and Test Audit

日期：2026-10-21

## Scope

本次仅审计并修订 `versions/v0.5.1-experiment/solution/` 与纯离线测试文件。未修改正式 `solution/`、V0.3.3、V0.5、历史游戏、数据库、日志、受保护会话或运行环境；未调用模型、MCP、Runner、setup、install 或 play。

## 定向修正

### Controller

在 `## Routing and arbitration` 中明确：checkpoint 示例里的 `strategy.priority` 是历史结构示例，不是 V0.5.1 的实际战略目标。新建或更新目标应优先长期综合成绩、提前晋升、Level 和 Wealth，同时服从明确生存与合法性限制。

`## Minimal durable state` 及其以下内容未修改。

### Career Planning

新增缺失 `target_review` 的处理顺序：

1. 优先使用当前真实 review/feedback 与 Controller 现有安全恢复路径取得的 `strategy.feedback_loop`。
2. 最后有效 `target_review` 存在时，先与返回的 review phase 和结算证据核实，再沿用。
3. 无法获取历史目标或无法确认评审是否结算时，不按月份猜测，不虚构已处理评审。
4. 使用既有 `unknowns`、`hypothesis`、`next_check` 记录目标未验证及缺失原因，仅比较可确认的直接属性收益和当前合法行动。
5. Controller 安全恢复前提不满足时，执行原有停止规则。

未新增状态枚举、持久化字段或 Controller 接口。

## Diff and hashes

相对 V0.5 的文本 Diff：

| 文件 | 增加/删除 | SHA-256（V0.5） | SHA-256（V0.5.1） |
|---|---:|---|---|
| `skills/career-controller/SKILL.md` | +13/-5 | `f0b2138f07144bf0d77e5bf69096c9d39bfae23251a995828ac3527b740db8e4` | `968f57675d6e5a74117a6ae97b7ff9353657307e27cb13e211232018583863e2` |
| `skills/career-planning/SKILL.md` | +52/-39 | `615bdba744b0dacb824dad2fd3bbca07433eda467ff12caf8300132257eca429` | `f8cd48fda2837d582516675c2497881ae4a9667898851a60cc54a00c0f520252` |
| `skills/resource-optimisation/SKILL.md` | +24/-26 | `525d246980b0d8167b542c0f887ca23d4fd9017e5cc2194794e1a180d8521c0b` | `c5dfafae11adbe8813d56bd3fd1d3c3b36f8522bd447b69a9fb591dc6683c36a` |
| `skills/risk-management/SKILL.md` | +0/-0 | `ae859c195ee133a3363baa6974c6326721e7aeb6c23de445c4b016678745ffcb` | `ae859c195ee133a3363baa6974c6326721e7aeb6c23de445c4b016678745ffcb` |
| `manifest.json` | +2/-2 | `64c5acf7991861452a6955a6274d091077483d9abe2a2d66008d14f42bbe09bc` | `1731996a30b0f4704b0a660870ee36623262ad34d52e931226f7eb686b6a8eb5` |

Controller 从 `## Minimal durable state` 起的安全关键尾段逐字一致。两侧尾段 SHA-256 均为：

`db135033e9524671330d690b760639897d78be78a83d59b90931fc2cb703d22e`

Risk Management 文件 SHA-256 完全一致。

## `offline_tests/test_v051.py` 的 9 项

1. 隔离副本包含预期的 8 个 bundle 文件。
2. manifest 名称、team、mode 和关键安全条款保持正确。
3. 四个 Skill frontmatter 名称与目录匹配。
4. Risk Management 与 V0.5 字节一致。
5. Controller 安全关键尾段与 V0.5 字节一致。
6. Career Planning 使用既有 `strategy.feedback_loop`、评审字段、证据字段、Main Action、A/S 未晋升处理和 M48 终局协议。
7. Resource Optimisation 保留 3 Energy、最多三个组合、Risk Management 状态、Main Action 独立性和缓存序列禁止规则，并检查公开属性上限。
8. Controller 包含授权的长期 Level/Wealth 仲裁、三 Skill 职责和风险机会成本规则。
9. Intensive Work 的 HiddenRisk 只作为当前菜单/离线场景证据，不被写成通用假设。

结果：`Ran 9 tests ... OK`。

## V0.5 原有 29 项审计

- 7 项结构/旧实验契约测试：隔离文件列表、旧 manifest 名称与 instruction、旧 Controller/Risk 字节一致、旧允许变更列表及 V0.5 字段。它们验证 V0.5 实验副本，不适合作为 V0.5.1 结果判定；V0.5.1 有授权的 Controller 和 manifest 差异。
- 16 项仍直接覆盖 V0.5.1 保留的参考语义：评审窗口时序、证据 focus、A/S 未晋升审计、Report 直接收益、合法菜单全量筛查、Energy 组合机会成本、公开属性 cap、M48 无第九次评审和无隐藏门槛。
- 6 项只验证 V0.5 旧的 Red/Amber/Green 参考分类。V0.5.1 不使用这套正式状态，改为直接读取 Risk Management 的 `unresolved`、`mitigation_pending`、`monitoring`、`resolved_explicit`、紧迫程度和 `blocked_choices`。

结果：`Ran 29 tests ... OK`。上述通过不等于真实 LLM 或完整游戏验证。

## V0.3 原有 131 项审计

### 120 项有效回归

以下安全、状态、风险、资源、反馈、候选、启动、固定 marker 和漏洞持久化类共 120 项通过：

`SubmissionTests`、`RoutingTests`、`RiskTests`、`ResourceTests`、`StateAndTimingTests`、`PersistenceRevisionTests`、`FeedbackRevisionTests`、`CandidateRevisionTests`、`BootstrapRevisionTests`、`BootstrapSourceTests`、`FixedMarkerRegressionTests`、`VulnerabilityPersistenceTests`。

结果：`Ran 120 tests ... OK`。

### 另外补跑的 4 项

从原先未纳入 120 项选择的终局类中，补跑了与本次策略直接相关的 4 项：

- `test_actual_archived_ending_recognized_as_native_terminal`
- `test_bash_printed_ending_not_native_terminal`
- `test_successful_final_action_needs_followup_observe`
- `test_game_over_error_and_malformed_payload`

结果：`Ran 4 tests ... OK`。

### 完整套件的 7 项失败

完整 `python -m unittest offline_tests.test_v03` 为 131 项，7 个失败均来自同一个保护索引测试的 subtest：

`TerminalAndBackupTests.test_protected_source_config_indexes_and_baseline_bytes_unchanged`

不匹配文件均在隔离副本之外：

- 受保护安装目录 `IDENTITY.md`
- 受保护安装目录 `skills/career-controller/SKILL.md`
- `.career_sim_runner/career_emu/active_install.json`
- `.career_sim_runner/career_emu/career_emulator.sqlite3`
- `.career_sim_runner/career_emu/last_drive_session.txt`
- `.career_sim_runner/career_emu/last_output_dir.txt`

这些是当前环境与测试记录中的历史哈希不一致，不是本次 V0.5.1 修改造成的；没有修改测试期望或保护文件。

同一 `TerminalAndBackupTests` 类中的其余保护/归档/历史环境检查没有纳入 120 项有效回归，因为本轮禁止触碰或重建这些受保护状态。完整测试结果保留为已知失败记录。

## Final result

安全关键 Controller 尾段和 Risk Management 字节检查继续通过。新增修正只影响战略说明和缺失评审目标的诊断路径，不改变 checkpoint schema、存储协议、执行恢复协议或风险状态协议。
