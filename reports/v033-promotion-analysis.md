# V0.3.3 晋升轨迹与优化空间分析

## 证据范围

本报告只使用第三局 V0.3.3 的公开运行证据和已经生成的审计记录，不修改方案、不运行新游戏。

- 评分：`.career_sim_runner/career_emu/outputs/The Raytirement Plan/20261020T172255Z/score_report.json`
- 事件：`.career_sim_runner/career_emu/outputs/The Raytirement Plan/20261020T172255Z/events-20261020T172255Z.jsonl`
- 对话：`.career_sim_runner/career_emu/outputs/The Raytirement Plan/20261020T172255Z/transcript-20261020T172255Z.log`
- 现有审计：`.career_sim_runner/career_emu/outputs/The Raytirement Plan/20261020T172255Z/audit-v033-third-game.md`
- 游戏 UUID：`e173ebcb61964fa58385148cc424e206`

## 晋升窗口

| 窗口 | 评审等级 | 晋升结果 | 评审后职级 | 反馈和可定位证据 |
|---|---|---|---|---|
| M6 | C | 是，L1→L2 | L2 | 经理称表现“neither hot nor cold”、处于 watch list，要求下一阶段展示更清晰成果；HR提示累计风险。见 transcript 中 “Month6, half-year review”。 |
| M12 | B | 是，L2→L3 | L3 | 记录为 “You climbed too fast”，旧人脉尚未适应新头衔，Network 7→4、Health 6→5、Dignity 10→9；HR提示风险严重。 |
| M18 | B | 否 | L3 | 经理/HR语气转好，记录为 “you最近干得还不错”；随后出现明确健康检查异常和避免高压、熬夜的医嘱。 |
| M24 | B | 是，L3→L4 | L4 | 经理要求 “show clearer outcomes so I can speak in committee”；随后记录健康压力和请假处置。 |
| M30 | B | 否 | L4 | 反馈是 “do not look like you only hustle without winning. Same bar in six months.” 没有晋升记录。 |
| M36 | A | 否 | L4 | 反馈为 “you were first on my list... come to me with ideas and I will fight for resources.” 仍没有晋升记录。 |
| M42 | A | 是，L4→L5 | L5 | 晋升为 Principal/team lead；反馈为 “Less hallway politics, more output and relationships.” |
| M48 | B | 否 | L5 | 审计记录为 M48 B、留在 L5；这是半年评审等级，不是最终结算评级。最终 `score_report.json` 的整体评级为 A。 |

第三局的晋升间隔是 6、6、12、18 个月。第一局 V0.2 也记录为 M6、M12、M24、M42，因此两局都观察到同一轨迹，但这不能单独证明存在任职时间门槛。

## 直接可见的状态证据

在关键窗口的最近可信观察中，状态大致为：

- M6：晋升后 L2，Health 6、Skill 12、Network 6、Output 5、Wealth 3。
- M12：晋升后 L3，Health 5、Skill 23、Network 7、Output 4、Wealth 6；剧情随后明确把 Network 降到 4。
- M18：L3，duration 7，Health 8、Skill 32、Network 20、Output 10、Wealth 8；B 但未晋升。
- M24：晋升后 L4，Health 10、Skill 43、Network 18、Output 17、Wealth 11。
- M30：L4，duration 7，Health 10、Skill 59、Network 36、Output 26、Wealth 15；B 但未晋升。
- M36：L4，duration 13，Health 9、Skill 80、Network 36、Output 25、Wealth 22；A 但未晋升。
- M42：晋升后 L5，Health 10、Skill 100、Network 37、Output 29、Wealth 25。
- M48：最终观察到 L5，Health 10、Dignity 10、Skill 117、Network 44、Output 38、Wealth 33；未出现 L6 晋升。

这些读数来自事件日志中的 `current_state.status`；它们是观察值，不是官方公开的晋升公式或门槛。

## 对“还有多少优化空间”的判断

### 已经做得好的部分

1. **M6 和 M12 已经很快。** 两个早期窗口都晋升，说明当前策略能在前 12 个月形成足够的可见表现和基本能力。
2. **M24 晋升成功。** 在 L3 阶段的 12 个月停留后晋升 L4，说明健康恢复、风险处置和可见成果并非完全牺牲职业发展。
3. **Risk Control 和 Health/Dignity 已经满分。** `score_report.json` 中 Risk Control 为 10/10，Health & Dignity 为满分；继续无条件增加恢复或排雷的边际价值可能很低。
4. **Skill 已接近满量化。** Skill raw 117、normalized 97.5，当前分数的主要缺口不在技能分本身。

### 最大的可优化区

1. **L4→L5 的 18 个月停留是主要晋升瓶颈。** M30 为 B、M36 为 A，仍到 M42 才晋升。日志不能证明是任职时间限制，也不能证明只要 A 就晋升；但 M36 的 A 反馈已经说明“绩效等级高”不是充分条件。
2. **Network 和 Wealth 是当前直接分数缺口。** 终局 Network raw 44、normalized 73.33；Wealth raw 33.7、weighted 8.43/20。健康、风险和技能已经接近满分，下一步的机会成本应更多比较可见领导力、关系质量、财富积累与继续刷技能之间的差异。
3. **M12 的快速晋升带来可见关系代价。** 晋升后 Network 7→4，说明“前期冲刺后期修复”存在可恢复的空间，但也说明晋升本身可能触发关系摩擦。该摩擦不是理论假设，而是本局明确记录的状态变化。
4. **M36 的 A 未转化为晋升。** 经理说愿意为资源出面，说明认可度高；但没有晋升。最稳妥的结论是：还缺少某种未公开的组合条件，可能涉及任职时间、岗位/领导范围、关系结构或其他状态。日志无法区分这些因素。
5. **M48 之后没有可验证的 L6 窗口。** 最后一段只有约 6 个月，且 M48 仍为 L5。不能据此断言 L6 不可能，只能说本局没有观察到 L6。

## 可验证的下一步假设

以下是实验假设，不是已证实规则：

- **H1：** 在 L4、距离下一评审 6 个月以上时，减少已经接近上限的纯 Skill/Health 投入，增加一次有明确领导范围和可见结果的主行动，可能比继续重复准备报告更有利于 M36/M42 晋升。指标：下一评审的 Level、Network、Output、反馈措辞。
- **H2：** M36 的 A 未晋升意味着 A 不是充分条件；在 M36 前需要同时保留可见产出和关系/领导范围证据。指标：M36 是否仍 A、是否晋升、Network 是否出现下降。
- **H3：** 前期职业加速后，后期定向修复 Network/风险可能提高综合分，但修复成本会占用 Level/Wealth 机会。指标：M12 后 Network 的最低点、后续恢复速度、最终 Wealth 与 Level。

## 建议的决策重点

下一版若只做一项改变，应优先改 **L4 阶段的半年反馈循环**：M30 B 或 M36 A 后，不机械重复同一类行动，而是根据反馈选择“可见成果 + 领导/资源范围 + 关系维护”中证据最弱的一项，同时保留风险和健康硬约束。Energy 仍可用简单候选筛选，避免为了填满 3 点而浪费在已达上限的属性上。

不要把 M6、M12、M24、M42 的重复日期直接写成硬编码晋升周期；下一局应该把“是否在 M36 前获得 L5”作为可证伪目标，而不是保证结果。

## 结论

V0.3.3 的主要提升来自风险控制和健康管理，晋升上限仍是 L5。可优化空间集中在 **L4 阶段的晋升转化、Network、Wealth 和减少低边际重复投入**。目前证据支持继续做单 Agent、四 Skill 的定向实验；不支持直接声称存在固定任职时间门槛，也不支持立即改成多 Agent。
