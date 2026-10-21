# V0.5.1 策略研究与正式设计报告

日期：2026-10-21  
状态：第一轮评审修订完成；未修改正式 solution、Controller、Risk Management、运行环境或历史游戏；未调用游戏 MCP、未启动新局。

## 0. 结论先行

V0.5.1 继续保持 **1 Agent + 4 Skills**，只改 `Career Planning` 与 `Resource Optimisation` 的决策规则。核心问题不是缺少更多行动建议，而是模型仍会在三个地方排错顺序：

1. 把当前评审是否已经结算与下一次要服务的评审混在一起。
2. 把低 Output 直接当成需要汇报，忽略“真实交付”和“组织可见性”是两类证据。
3. 在没有明确风险或终局已到时，仍优先恢复、排雷或刷报告，牺牲 Network、Skill、Wealth 或直接终局分。

V0.5.1 的目标不是保证某个等级，而是让每次选择都回答：当前评审状态是什么？Risk Management 的限制是什么？下一次需要哪类证据？当前菜单里哪个合法行动能在剩余时间内产生该证据，同时保留更高等级带来的工资和终局直接分？

最重要的行为修正：

- **Delivery 反馈且没有已确认成果时，Key Project/资源与责任机会优先于单纯 Report。**
- **Visibility 反馈且已有工作成果时，Report/Prepare Report 才获得职业证据优先级；其公开 Output/Dignity/Network 收益始终保留。**
- **Defuse 只在 Risk Management 的 `unresolved`/`mitigation_pending` 状态、紧迫程度和明确处置建议共同支持时优先；`monitoring` 不等于解除，历史上出现过风险也不等于当前自动必须排雷。**
- **Health=9 且没有健康警告时，不自动把 Health recovery 放在第一位；Health=10 时纯恢复通常被裁剪。**
- **M48 评审已经结算后进入 `terminal_processed`，不再为假想的第九次评审刷 Output。**

## 1. 范围、数据与证据质量

### 1.1 已审查材料

- 官方公开规则：`docs/rules.rst`、`docs/handbook.rst`、`docs/failure-and-ending.rst`。
- V0.2 第一局：`20261019T214724Z`，最终 B / 63.02 / L5。
- V0.3.3 第三局：`20261020T172255Z`，最终 A / 70.38 / L5。
- V0.4 第四局：`20261020T202902Z`，最终 C / 59.85 / L4。
- 三局的 `score_report.json`、`events-*.jsonl`、`transcript-*.log`。
- V0.3.3 晋升分析、V0.4 游戏报告、V0.5 策略设计、V0.5 修订补充和修正报告。
- V0.3.3 与 V0.5 的 16 场景真实 DeepSeek 离线对照、32 次最终请求的完整输出和输入快照。

### 1.2 数据质量与限制

- 三局没有匹配随机种子，事件、故事选项、模型路径和重试次数不同；只能把日志里的发生事实当作事实，不能把局间分差归因给单条规则。
- 官方不公开晋升阈值、绩效公式、隐藏风险计数器或行动到晋升的概率。
- 评审月的原生观察显示：评审结果先返回，然后才进入该月季度 Energy/Main Action。评审后的当月动作不能成为已经结算评审的原因。
- 评审后的状态不是评审前状态。任何“评审前能力”只能使用最近一次可信的评审前 `observe`；不能用评审结算后的状态倒推原因。
- V0.5 离线输入只包含当前快照、当前菜单、当前 `events` 和最近少量行动 notes，没有把完整 `strategy.feedback_loop` 传入模型。因此 `target_review` 在 32 次请求中有 30 次为 `unknown`，这首先是输入边界问题；它同时暴露出实际 Agent 必须显式携带评审阶段和反馈账本，不能只依赖 Skill 文本。
- 离线实验只验证模型建议是否合法和是否改变，不能证明真实 Agent、JiuwenSwarm、MCP、持久化或最终分数的端到端效果。

## 2. 官方规则与可用的直接收益

公开规则支持以下稳定事实：

- 每个季度有 3 点 Energy；未使用不结转。
- 每季度另有 1 个 Main Action，和 Energy 独立。
- 每 6 个月发生一次绩效评审和晋升窗口，共 M6、M12、M18、M24、M30、M36、M42、M48。
- 评审等级与晋升不是同一变量；等级只公开近期表现和奖金方向。
- 晋升看长期结果，且职级越高要求越高；精确阈值未知。
- 月薪随 Level 增长：L1 0.3、L2 0.4、L3 0.5、L4 0.7、L5 1.0、L6 1.5、L7 2.3、L8 3.6、L9 5.7、L10 9.1 Wealth/月。
- Energy 的可见菜单方向：Skill Study 提高 Skill 但降低 Health；Network Maintenance 提高 Network/Dignity；Defuse 处理旧风险但公开属性收益为零；Mental/Health Recovery 分别恢复 Dignity/Health；Prepare Report 提高 Output/Dignity。High-intensity/Intensive Work 在实际菜单快照 `offline_llm_compare_v05/scenarios.jsonl` 中明确显示 Output +2、Health -1、Dignity -1、HiddenRisk +1；这是菜单证据，不把它扩写成脱离当前菜单的官方通用保证。
- Main Action 的公开方向：Key Project 提高 Output/Skill/Network；Report Results 提高 Output/Network/Dignity；Push for Resources 提高 Output/Network；Rotation 提高 Skill/Network；Mentor 提高 Skill/Network；Repair Relationship 提高 Network/Dignity；Lay Low 提高 Health。

本地终局量化报告使用的观察权重是 Level 30%、Wealth 20%、Health & Dignity 15%、Skill 15%、Risk Control 10%、Network 10%。这些是本地量化结算的证据，不能当作云端最终评分或晋升权重。

工资表说明更早晋升具有真实长期价值。例如在“晋升后下个月开始按新 Level 发薪”的假设下，L4→L5 提前 6 个月的工资差约为 `(1.0 - 0.7) × 6 = 1.8` Wealth，L5→L6 提前 6 个月约为 `(1.5 - 1.0) × 6 = 3.0`。这是机会成本参考，不是晋升结果保证。

## 3. 历史结果与晋升证据

### 3.1 三局终局

| 版本 | 评级 / 量化分 | 最终 Level | Wealth | Health & Dignity | Skill | Risk Control | Network |
|---|---:|---:|---:|---:|---:|---:|---:|
| V0.2 | B / 63.02 | L5 | 35.1 | 18 | 118 | 1/10 | 63 |
| V0.3.3 | A / 70.38 | L5 | 33.7 | 20 | 117 | 10/10 | 44 |
| V0.4 | C / 59.85 | L4 | 21.4 | 20 | 92 | 10/10 | 36 |

V0.3.3 的分数缺口集中在 Level 15/30 和 Wealth 8.43/20；Health/Dignity、Skill、Risk Control 已接近或达到本地量化高位。V0.5.1 应把更多机会成本放在晋升转换、工资时间、Network 和直接终局价值，而不是无条件继续恢复或排雷。

### 3.2 八次评审的观察事实

| 月份 | V0.3.3 | V0.4 | 证据结论 |
|---:|---|---|---|
| M6 | C，L1→L2 | C，留 L1 | C 不排除晋升；低职级窗口可能已满足长期组合条件，但精确原因未知。 |
| M12 | B，L2→L3；晋升后出现 Network 摩擦 | C，L1→L2 | B 可以晋升；晋升后的关系代价是真实观测。 |
| M18 | B，留 L3 | B，L2→L3 | B 既可能晋升也可能不晋升；等级不是门槛。 |
| M24 | B，L3→L4 | B，留 L3 | 相同等级、不同晋升结果，说明长期状态和故事/组织因素共同作用。 |
| M30 | B，留 L4；反馈“不要只忙碌，要赢得结果” | B，L3→L4 | 单纯忙碌或属性上涨不足以解释晋升。 |
| M36 | A，留 L4；经理说“first on my list… fight for resources” | B，留 L4 | A 和经理支持也不是充分条件，范围、时机、组织支持或未知条件仍可能不足。 |
| M42 | A，L4→L5；反馈“Less hallway politics, more output and relationships” | A，留 L4 | 相同 A 也可能晋升或不晋升；反馈中的组织关系和影响范围需要被当作证据，而不是保证。 |
| M48 | B，留 L5 | A，留 L4 | M48 评审同时是最终窗口；结算后不再存在第九次评审。 |

### 3.3 重点问题的解释

#### 为什么 V0.3.3 在 M6 绩效 C 仍晋升

事实是：M6 返回 C、奖金为负向调整，同时返回 L1→L2。经理评价“neither hot nor cold”、仍在 watch list，并要求下一阶段展示更清晰成果。最合理的工作假设是：近期绩效偏弱，但低职级的长期职业资本、前六个月累积证据或组织支持仍达到了该窗口的晋升条件。日志没有公开哪个因素起决定作用，因此不能写成“C 也能稳定晋升”或把 M3 的某个动作当成唯一原因。

设计含义：C+晋升后不能继续按“已经证明策略正确”运行；应保留低绩效反馈，把下一阶段目标设为反馈要求的证据。

#### 为什么 M12 绩效 B 仍能晋升

事实是：B、L2→L3，随后出现“climbed too fast”以及旧网络没有吸收新头衔的摩擦，Network 从评审前的可见状态下降。说明晋升是长期结果与组织状态的综合判断，B 不等于失败；同时晋升会改变关系环境，不能只记录 Level 上升而忽略 Network/Health/Dignity 变化。

设计含义：晋升后先检查真实下降，再决定是否投入关系/健康修复；没有下降时不机械花费资源。

#### 为什么 M36 绩效 A 仍没有晋升

事实是：A、奖金正向调整，经理说关键里程碑和跨团队工作得到记忆，并愿意争取资源，但 Level 仍为 L4。A 证明近期表现被认可，不证明晋升组合已经完成。可能原因包括责任范围、组织支持、时间因素、隐藏条件或随机剧情；样本不足以区分。

设计含义：A+未晋升必须进入诊断分支，不能自动 Intensive Work、自动 Report 或自动把某个属性写成瓶颈。先审计上一假设是否执行、目标证据是否出现，再根据新反馈选择 scope、relationships、visibility 或继续 delivery。

#### 为什么 V0.2 和 V0.3.3 出现相同晋升月份

两局都观察到 M6、M12、M24、M42 晋升。这可能来自相似的早期职业资本轨迹、职级相关的组合条件或引擎中的部分确定性；也可能只是小样本的共同结果。V0.4 的轨迹不同，说明日期不是简单的全局固定表。V0.5.1 只能把日期当作窗口，不能硬编码“L4 必须等 18 个月”或“下一次一定在 M42 晋升”。

### 3.4 V0.4 的重要差异

V0.4 M6 未晋升，随后 M12 才到 L2、M18 到 L3、M30 到 L4，最终停在 L4。V0.3.3 在 M6、M12、M24 已先建立更高 Level，工资、评审起点和可用发展时间因此更有利。V0.4 使用了更多 Network Maintenance、Skill Study、Mentor、Intensive Work 和 Defuse，V0.3.3 使用了更多 Prepare Report；统计如下：

| 行动 | V0.3.3 | V0.4 |
|---|---:|---:|
| Prepare Report | 27 | 12 |
| Key Project | 13 | 10 |
| Health Recovery | 9 | 9 |
| Network Maintenance | 4 | 9 |
| Defuse | 3 | 4 |
| Intensive Work | 1 | 2 |
| Skill Study | 0 | 3 |
| Main Report | 1 | 4 |

这些是行动使用次数，不是效果估计。V0.4 的低分不能归因给某一个行动；但它明确说明“增加导师、技能、关系动作”本身不能补回早期 Level 落后，也说明 V0.5.1 不应复制固定的行动轮换。

## 4. V0.5 离线对照的诊断

### 4.1 已确认的工程质量

- 32/32 HTTP 200。
- 32/32 输出是可解析 JSON。
- 32/32 choice 合法，全部来自当前菜单。
- 16 个相同快照中 7 个第一 choice 不同，9 个保持一致；没有为了显示变化而强行换选项。

### 4.2 暴露的策略缺陷

1. **评审目标没有稳定传入。** 30/32 的 `target_review` 为 `unknown`。V0.5 的文本要求模型读取 `strategy.feedback_loop`，但离线输入没有该对象；实际运行也必须确保它出现在当前决策上下文中。
2. **M9、M18 的“低 Output”压过了“真实成果”反馈。** V0.5 选择 Report；V0.3.3 选择 Key Project。M6/M18 的反馈要求“show clearer outcomes”，且快照没有已确认交付，Delivery 目标下更应优先能产生真实结果的项目/资源行动。Report 仍可作为直接 Output/Network/Dignity 收益候选，不能被删除。
3. **M6 的风险证据没有被明确分级。** 快照历史 notes 有 `R1:elevated, defuse Q3`。如果 Risk Management 仍把它标为待处置，Defuse 应获得优先级；如果已经明确解决，则 Health recovery 可以优先。Career Planning 不能自己裁决，必须读取 Risk Management 的状态。
4. **M33 的 H9 恢复偏早。** 没有当前 warning，Health recovery 的 +2 会有一部分被 10 的公开上限裁剪；Network/Report 仍可能提供公开增益。
5. **M36 的 Report 和 V0.3.3 的 Defuse 都不能成为固定答案。** 当前快照 H/D=10/10、没有事件。没有活跃风险时，机械 Defuse 是过度防守；没有真实工作和 visibility 反馈时，机械 Report 也可能只是刷 Output。
6. **M42 的 Report×3 可能忽视关系目标。** V0.3.3 已晋升 L5，反馈同时说 output 和 relationships；Skill 已很高，Dignity/Health 已封顶。应比较 Report 与 Network/关系行动。
7. **M48 的 Report 可能没有兑现时间。** 最终评审已经处理，公开终局维度不直接包含 Output。除非当前报告有明确终局直接收益，否则 Network、Skill、Health、Wealth 或 Risk 的直接收益更有根据。
8. **同一条 `evidence_focus` 可能变成硬约束。** 评审目标是排序信号，不是唯一分数。若证据候选无法在目标前兑现，或其成本明显高于直接终局价值，应切换到直接价值比较。

## 5. V0.5.1 总体设计

### 5.1 设计目标

V0.5.1 的目标函数按以下顺序解释：

1. 完成 48 个月并避免可预见的提前结束或不可逆长期损失。
2. 在每次真实评审前积累能被下一次评审观察到的职业资本，优先争取更早晋升。
3. 尽早提升 Level 以获得更多高工资月份，同时保持足够的 Skill、Network、Output、Health、Dignity 和 Wealth。
4. 在 M48 评审结算后，优先选择会直接改善终局综合成绩的行动；不把无法兑现的 Output 证据当作终局价值。

这不是一个固定行动序列，也不是晋升预测器。它是一个在当前菜单、历史反馈、Risk Management 状态和剩余时间约束下进行候选比较的规则系统。所有晋升原因、分数公式和 S 级条件继续视为未知。

### 5.2 每季度开始必须形成的 Decision Header

Career Planning 根据当前 `observe`、已有评审反馈和现有 `strategy.feedback_loop` 形成一个短的 `Decision Header`，再交给 Resource Optimisation 使用。Career Controller 保持原样，不承担新的诊断或字段生成职责。建议只复用现有策略字段：

```text
review_phase: pre_review | post_review | terminal_processed
target_review: next unprocessed review | unknown | terminal_processed
evidence_focus: delivery | visibility | capability | scope | relationships | unknown
evidence_status: observed | partial | negative | unknown
prior_intervention_family: delivery | scope | relationships | visibility | recovery | risk | none
next_check: 下一次要验证的具体结果和月份
```

规则：

- `review_phase` 必须按评审结算先于同月 Energy/Main Action 处理。M6 等月份先读取评审结果，再决定当月剩余行动；不能用当月行动解释已经结算的晋升。
- `target_review` 只在下一次尚未处理的真实评审窗口存在时填写；若当前输入无法确认目标，使用既有的 `unknown`。M48 评审结算后，`review_phase` 和 `target_review` 统一设置为 `terminal_processed`，不再使用 `none`。
- `evidence_focus` 是当前最值得验证的职业假设，不是排他条件。它可以改变候选排序，但不能压过明显更高的直接终局价值或生存需要。
- `evidence_status` 只使用既有枚举：`observed` 表示已观察到结果，`partial` 表示正在进行或受阻但已有部分证据，`negative` 表示预期结果明确未发生，`unknown` 表示当前无法判断。概念上的“confirmed”映射为 `observed`，“in progress/blocked”映射为 `partial` 并在说明中写明原因，“missing”映射为 `unknown`，“failed to appear”映射为 `negative`。不要把这些英文概念引入为持久化状态；Prepare Report 或单纯 Intensive Work 不得自动写成 `observed` delivery。
- `next_check` 必须是可观察的结果，例如“下次评审是否提到可量化里程碑”“下一季度是否出现资源批准”“Network 摩擦是否缓解”，不能写成“继续努力”。

### 5.3 候选比较框架

两个 Skill 都必须先列出当前合法候选，再比较候选，不得因为菜单顺序、旧版本选择或单一 focus 直接截断候选。每个候选至少记录：

| 比较项 | 需要回答的问题 |
|---|---|
| Direct gain | 本次公开属性、工资或终局指标的即时收益是什么？若存在已知上限，是否会被裁剪？ |
| Evidence gain | 它能产生哪一种真实成果、责任范围、组织认可或关系证据？何时能被观察？ |
| Timing | 能否在 `target_review` 前兑现？M48 后是否仍有意义？ |
| Cost/risk | Energy、Health、Dignity、当前菜单明确列出的风险属性变化、关系摩擦和提前结束风险是什么？Risk Management 是否有明确指示？ |
| Opportunity cost | 放弃的另一个高价值动作是什么？这个动作是否只能在本季度或本职级使用？ |
| Unknowns | 该收益是否只是合理假设，还是已有本局反馈支持？ |

排序原则：先剔除会明显违反生存和执行安全规则的候选；再按目标评审的可兑现职业证据和长期工资价值排序；若证据无法及时兑现，则按直接属性和终局价值排序。若两候选都未知，选择成本更低、可逆性更高、能留下下一次验证机会的候选，而不是制造确定性假设。

### 5.4 时间和工资的使用原则

- 评审前，提前一个 Level 的预期工资价值可以改变当期选择，但只能作为边际价值加入比较，不能当作已知晋升概率。行动应回答：“这个动作是否显著增加下一次评审可见的晋升证据，且收益足以覆盖它放弃的直接属性？”
- 评审后，先消化新的等级、反馈和属性变化，再规划下一阶段；不要用上一阶段的 focus 继续自动执行。
- 越接近 M48，越少投入只在未来评审中才有价值的 Output 证据；越应检查 Network、Skill、Health、Dignity、Risk 和 Wealth 的直接终局收益。
- 不把每季度 3 Energy 视为必须全部花在职业行动上。若有可验证的健康或风险需要，使用恢复/Defuse；若没有，按候选的边际价值花费 Energy。未使用 Energy 不会积累，仍需比较当前本季度的机会成本。
- 独立 Main Action 必须单独比较，不能因 Energy 已经耗尽而默认 Lie low，也不能因本季度选择了 Key Project 就自动重复。Main Action 的选择应看其公开收益、实际成果机会、关系/责任范围和剩余兑现时间。

## 6. 两个策略 Skill 的正式行为规则

以下规则只适用于 Career Planning 和 Resource Optimisation。Career Controller 仍是唯一协调中心，Risk Management 仍是唯一风险判断来源。

### 6.1 Career Planning：评审和职业资本规则

#### CP-1：先读评审结果，再建立下一目标

**观察条件：** 当前月份是 M6/M12/M18/M24/M30/M36/M42/M48，或刚收到新反馈。

**优先行动类型：** 先更新 `review_phase`、Level、绩效、晋升结果、反馈关键词和 `next_check`；再比较 delivery、scope、relationships、visibility 等行动。

**为什么更好：** 直接尊重评审结算顺序，避免把同月行动倒因果，也避免用旧 focus 处理新职级。

**机会成本：** 更新诊断本身不产生公开属性；如果当季有极短窗口的直接行动，需在完成诊断后立即比较，不得拖延整个季度。

**反例：** 若 Career Planning 没有收到评审输出，不能猜测已晋升或未晋升；应把 `target_review` 标为既有的 `unknown`，并仅使用已知状态。

#### CP-2：把反馈转成可验证的证据假设

**观察条件：** 评审含有“clearer outcomes”“scope”“relationships”“resources”“output”等反馈。

**优先行动类型：**

- “clearer outcomes / deliverables / win” → 优先 Key Project、Push Resources 或能形成真实范围的 Main Action；Report 只作为并列的直接收益候选。
- “scope / resources / cross-team” → 优先能扩大责任范围、争取资源或完成跨团队交付的 Key Project、Push Resources、Rotation、Mentor；不得把准备报告写成已获得范围。
- “relationships / hallway politics / friction” → 优先 Network Maintenance、Repair Relationship、Mentor 或能产生真实协作的项目；不是无条件加 Report。
- “visibility / speak for you / leadership” → 比较 Report、Publicize 和有结果支撑的 Key Project；若没有可展示成果，Report 只能增加直接 Output/Network/Dignity，不能自动生成可信交付证据。
- “keep improving skill” → 比较 Skill Study、Rotation、Mentor 与能同时产生结果的 Key Project；Skill 已高或目标评审临近时，不能只因反馈出现“skill”就牺牲更有时效的成果。

**为什么更好：** 将自然语言反馈转换成下一次可观察结果，同时保留同菜单其他合法收益。

**机会成本：** 证据行动可能牺牲当期直接 Output、Network 或 Health；必须记录放弃的最高价值候选。

**反例：** 反馈若只谈近期情绪或没有可执行结果，不能强行归类；使用既有 `evidence_status=unknown`，回到直接收益和低成本可逆行动比较。

#### CP-3：Key Project 与 Report 的选择

**观察条件：** 两者同处 Main Action 菜单，且目标评审尚未结算。

**优先行动类型：**

- 选择 Key Project 的条件：最近反馈要求真实成果/责任范围；当前没有 `evidence_status=observed` 的交付；有足够 Health/Dignity/Skill 和剩余季度让结果被观察；或项目可以补足此前连续“准备但未交付”的证据缺口。
- 选择 Report 的条件：已有 `evidence_status=observed` 的成果需要向领导可见地呈现；反馈明确要求 visibility/speak for you；项目交付已观察到但组织认可尚未形成；或 Key Project 的兑现时间已短于目标评审且 Report 的直接收益更可靠。
- 若两者都满足，比较 `Evidence gain × time to review` 与 Report 的直接 Output/Network/Dignity 及其机会成本；不得用“Key Project 永远优先”或“Output 永远优先”。

**为什么更好：** 解决 M9/M18 的核心问题：真实成果与领导可见性是两个不同阶段，Report 不能替代未完成的项目，项目也不能替代已完成成果的组织可见性。

**反例：** 若 Key Project 的结果明确会拖到 M48 之后，且当前终局直接属性明显不足，Report 或其他直接收益可以胜出；若已有多个未展示的成果，继续做项目可能不如 Report。

#### CP-4：A/B/C 与晋升的解释边界

**观察条件：** 评审给出绩效等级和是否晋升。

**优先行动类型：** 以“反馈要求的证据”作为下一阶段 focus；不把等级本身作为固定动作触发器。

**为什么更好：** M6 的 C+晋升、M12 的 B+晋升、M36 的 A+未晋升和 M42 的 A+晋升共同证明，绩效等级不是充分或必要的单一门槛。

**机会成本：** 过度解读等级会导致 Intensive Work、Report 或 Defuse 的机械重复，损失下一阶段真正需要的资本。

**反例：** 若连续多次低绩效伴随明确的生存/能力问题，不能因为一次 C 曾经晋升就继续冒险；应把已观察的低绩效和 Risk Management 输出纳入候选成本。

#### CP-5：A+未晋升审计

**观察条件：** 本次绩效为 A/S，但未晋升。

**优先行动类型：** 做一次短审计：上一阶段 focus 是否真的完成、哪类证据缺失、下一窗口是否仍有时间兑现；随后选择 scope、relationships、visibility、delivery 中证据最缺的方向。

**为什么更好：** 防止把 M36 的 A 误读成“继续加班即可晋升”，也防止自动刷 Report。

**机会成本：** 审计可能延后一次行动；只允许延后到足以选出方向，不能每季度反复生成长报告。

**反例：** 如果 A+未晋升同时有明确的组织支持/资源已到位但项目尚未落地，继续完成 Key Project 可能比关系修复更有价值；审计必须接受这个结果。

#### CP-6：晋升后的关系摩擦

**观察条件：** 晋升后出现 Network、Dignity 或事件中的关系摩擦。

**优先行动类型：** 先比较 Repair Relationship、Network Maintenance、Mentor 与能形成真实协作的项目；若没有可观察下降，不机械消耗资源。

**为什么更好：** M12 的“climbed too fast”说明晋升可能改变组织环境；把 Level 上升和 Network 成本同时记录，才能守住长期工资收益。

**机会成本：** 关系动作可能少于 Key Project 的 Output/Skill；只有在已观察摩擦、关系目标或事件要求时提高其优先级。

**反例：** Network 没有已公开的上限，因此不能按某个假设数值裁剪或降权。只有当当前菜单显示无增益、已有明确关系目标已满足，或其他候选的直接/职业价值更高时，才降低 Network 行动的优先级。

### 6.2 Resource Optimisation：Energy 和 Main Action 规则

#### RO-1：Risk Management 是唯一风险闸门

**观察条件：** 当前有事件、历史风险提示或 Risk Management 输出包含既有风险状态 `unresolved`、`mitigation_pending`、`monitoring`、`resolved_explicit`，以及既有紧迫程度 `attention`、`elevated`、`critical`。

**优先行动类型：** 只依据 Risk Management 的既有状态、紧迫程度和 `blocked_choices`/明确处置建议决定 Defuse 是否优先；Career Planning 可以说明职业机会成本，但不得重算风险等级。`monitoring` 不是明确解除，不能按 `resolved_explicit` 处理。

**为什么更好：** 避免把“无新事件”误当作风险解除，也避免新 Skill 自己发明第二套风险裁决机制。

**机会成本：** Defuse 消耗 2 Energy 且通常没有公开属性；只有状态明确要求或其避免的损失明显大于被放弃行动时，才排在高价值职业行动前。

**反例：** 只有当 Risk Management 状态为 `resolved_explicit` 且没有新的 warning 时，才可以认为已有风险被明确解除；即使如此，Defuse 仍不能仅因旧历史记录自动获得最高优先级。`monitoring` 不能触发同样的解除结论。

#### RO-2：Health/Dignity 的边际价值和上限裁剪

**观察条件：** Health 或 Dignity 低于已公开的 10 点上限，或有明确下降趋势/生存风险。

**优先行动类型：** Health Recovery、Mental Recovery、Network/Repair、低成本工作候选按缺口和风险比较；若属性已经封顶且没有新风险，恢复不自动优先。

**为什么更好：** 修正 M33 选择 Health recovery 的问题：H9 到 H10 的 +2 有部分会被裁剪，而 Network/Report 仍可能提供公开增益；Network 不作上限裁剪假设。

**机会成本：** 恢复会牺牲 Network、Output、Skill 或证据机会；必须说明边际收益是否实际超过被放弃动作。

**反例：** H9 看似接近 10 点上限，但 Risk Management 或事件明确提示短期健康危险时，生存价值可以压过职业资本。

#### RO-3：Intensive Work 只在可交付收益明确时使用

**观察条件：** 当前有明确高价值交付窗口，Health/Dignity 足够，Risk Management 没有阻止，且普通 Key Project/Push Resources 无法在目标期内完成同等结果。

**优先行动类型：** Intensive Work 最多作为候选之一；当前菜单若明确列出 HiddenRisk 变化，才把该变化计入成本。已审查的菜单快照 `offline_llm_compare_v05/scenarios.jsonl` 将 High-intensity work 描述为 Output +2、Health -1、Dignity -1、HiddenRisk +1；若当前菜单没有该项描述，不得自行补写 HiddenRisk 效果。与此同时比较 Skill/Network 机会成本和 Health/Dignity 损失。

**为什么更好：** 既避免为了冲 Level 过度损害 Health，也保留确有交付期限时的进取性。

**机会成本：** 它消耗 2 Energy，还可能需要后续恢复；若只是得到更多公开 Output 而没有真实成果，通常不如普通职业资本动作。

**反例：** 当前 H/D 已接近危险线、连续多个季度没有恢复窗口，或项目结果无法被评审观察时，不选 Intensive Work。

#### RO-4：Prepare Report 的两层价值

**观察条件：** Energy 菜单有 Prepare Report。

**优先行动类型：**

- 有已确认交付、需要组织可见性时，把它视为“直接 Output/Dignity + visibility 支持”的候选。
- 没有已确认交付时，只计入公开 Output/Dignity；不得把它写成真实成果、资源批准或晋升证据。
- 若目标评审临近且报告能在窗口内让成果被看见，visibility 价值可以提高其排序；若只是为了刷 Output 且 `evidence_status=unknown`，Key Project/Push Resources/Network 等仍有公开增益的候选应优先比较。

**为什么更好：** 保留 Prepare Report 的实际公开收益，同时修正“准备动作等于交付”的混淆。

**机会成本：** 每点 Energy 可能替代 Network、Health、Defuse 或另一份报告；报告的直接收益要与这些放弃项量化比较。

**反例：** 若当前没有真实成果且评审已处理，Report 的 visibility 假设没有兑现时间；应转向终局直接价值。

#### RO-5：三点 Energy 的组合而非单点贪心

**观察条件：** 每季度开始有 3 Energy。

**优先行动类型：** 先为每点 Energy 产生 2–3 个候选组合，再考虑组合副作用。例如 Defuse 2 点后只剩 1 点，Intensive Work 2 点后可能需要恢复；Prepare Report 1 点允许保留另一点给 Health/Network。

**为什么更好：** 单个动作看起来高收益，但组合可能改变风险、健康和下一季度可行性；组合比较能避免“先点最高 Output，再被迫恢复”的隐性成本。

**机会成本：** 组合分析增加少量文本长度；必须保持候选最多 3 组，避免模型在菜单中失去重点。

**反例：** 若 Risk Management 有明确紧急处置要求，先满足该约束，不为追求完美组合延迟安全动作。

#### RO-6：Main Action 的独立评价

**观察条件：** 每季度可单独选择一次 Main Action。

**优先行动类型：** Key Project、Report Leadership、Push Resources、Rotation、Publicize、Mentor、Repair Relationship、Lie Low 逐项按当前目标比较。

**为什么更好：** Main Action 的公开收益与 Energy 行动不同；不能把 Energy 已经用于恢复当作 Main Action 也必须恢复，也不能因本季度有 Key Project 就重复选择。

**机会成本：** 选择一种 Main Action 会放弃另一种即时属性或组织价值；必须记录最高替代项。

**反例：** 事件明确限制某类行动、Risk Management 要求保守或 Health/Dignity 已到危险状态时，安全和执行规则优先。

#### RO-7：M48 终局切换

**观察条件：** M48 评审结算完成，`review_phase=terminal_processed` 且 `target_review=terminal_processed`。

**优先行动类型：** 直接比较 Network、Skill、Health、Dignity、Risk、Wealth 和可确认的 Level/Salary 终局收益；只有存在明确、可兑现的终局 Output 计分作用时才选择纯 Output 行动。

**为什么更好：** 修正 M48 继续 Prepare Report 的问题，并承认最后一季度没有第九次评审。

**机会成本：** 放弃 Report 可能损失 Output/Dignity；若最终评分实际包含这些维度或报告已有直接收益，不能凭假设排除它。

**反例：** 当前引擎明确给出报告会直接提升终局指标时，终局规则应以该公开证据为准；本规则不能用未知公式取代游戏输出。

## 7. 关键场景的预期判断对照

下表不是固定月份攻略，而是把已观察快照重新放入 V0.5.1 的条件判断中。最终选择仍必须以当局实际菜单、Risk Management 输出和最新反馈为准。

| 场景 | 旧版分歧 | V0.5.1 预期判断 | 关键证据与机会成本 |
|---|---|---|---|
| M6，`R1:elevated, defuse Q3` | V0.3.3 Defuse；V0.5 Health | 若 Risk Management 状态为 `unresolved` 或 `mitigation_pending`，且其紧迫程度/`blocked_choices` 要求处置，先 Defuse，再比较剩余 Energy；若状态为 `resolved_explicit` 且 H 有缺口，Health 可先 | 不能凭“没有新 event”清除旧风险；`monitoring` 也不等于明确解除；Career Planning 不自行升级风险。 |
| M9，L2，O6，H7，D10，主菜单 Key/Report | V0.3.3 Key；V0.5 Report | 若上一反馈要求 clearer outcomes 且 `evidence_status` 不是 `observed`，Key Project 优先；已有交付但缺 visibility 时 Report 优先 | Key 的成本是放弃 Report 的直接 O/N/D；Report 不能替代未交付成果。 |
| M18，L3，H10，D10，S32，N20，O10 | V0.3.3 Key；V0.5 Report | 沿用 CP-3：未完成真实成果则 Key；已有成果待呈现则 Report | H/D 已封顶，恢复机会成本高；仅因 O=10 低不能自动刷 Report。 |
| M33，L4，H9，D10，无当前 warning | V0.3.3 Defuse；V0.5 Health | 若 Risk Management 状态为 `resolved_explicit`，比较 Network/Report/职业证据；若为 `monitoring`，继续读取其建议，不能当作已解除；Health 只有在趋势或风险说明其边际价值更高时优先 | H9→H10 可能有裁剪；Defuse 不能因旧历史自动优先。 |
| M36，L4，H10，D10，无 event | V0.3.3 Defuse；V0.5 Report | 两者都不固定。若目标仍需真实 delivery/scope，Key/Push/Report 比较；若 Risk Management 已为 `resolved_explicit` 且无新 warning，Defuse 通常不应无条件第一 | 不能把无风险等同于必须 Defuse，也不能把 Report 等同于真实成果。 |
| M42，V0.3.3 已晋升 L5，H/D/S 高，反馈含 output 和 relationships | V0.3.3 Defuse；V0.5 Report | 比较 Report 与 Network/Repair/Mentor/协作项目；若关系没有下降，Report 的直接收益仍需和终局价值比较 | 已进入高工资职级，关系与可见成果都可能影响长期收益；单一 Report×3 缺乏依据。 |
| M48，评审已处理，L5，H/D/S 较高 | V0.3.3 Defuse；V0.5 Report | 设置 `review_phase=terminal_processed`、`target_review=terminal_processed`，优先直接终局收益；Report 只有在当前输出明确有终局作用或仍有可兑现的同月结果时胜出 | 不存在第九次评审；纯 Output 的未来兑现时间为零。 |

## 8. 反例审查与修正结果

### 8.1 会不会为了冲 Level 过度损害 Health

有这个风险，尤其是把 Intensive Work 误当成晋升按钮。设计已加入三道限制：

1. Intensive Work 必须说明可兑现的交付/窗口，并与普通 Key Project、Push Resources 比较。
2. H/D 的公开上限、趋势和后续恢复成本进入机会成本；低健康不能只用“本季度有 3 Energy”解释。
3. 晋升概率和固定门槛未知，因此不能用假设收益覆盖明确的健康损失。

仍需保留的弱点：游戏隐藏风险和生存规则可能比公开状态更敏感。此处只能读取 Risk Management 输出，不能承诺“健康尚可就安全”。

### 8.2 会不会为了减少风险再次牺牲高价值机会

有这个风险，尤其是 M33/M36/M42 把 Defuse 当成无条件的第一动作。设计将 Defuse 限定为 Risk Management 的 `unresolved`/`mitigation_pending` 状态、紧迫程度和明确处置建议共同支持时优先；`monitoring` 继续视为未明确解除，`resolved_explicit` 才表示已明确解除。这样保留风险处置能力，也不把历史事件永久化为禁令。

仍需保留的弱点：Risk Management 可能给出信息不足的摘要。任何不属于四个既有状态的文本都只能作为未知信息交给 Resource Optimisation，不能映射成新的正式状态或自行发明阈值。

### 8.3 会不会错误地把报告当成真实成果

设计继续使用既有 `evidence_status` 枚举：`observed` 表示已确认成果，`partial` 表示部分进展或受阻，`negative` 表示预期结果未发生，`unknown` 表示无法判断。Prepare Report 只有在 `observed` 成果存在时才获得额外 visibility 解释；否则只计公开 Output/Dignity。Report 仍可能是合理动作，但理由必须是直接收益或已完成成果的呈现，而不是虚构交付。

反例是：某些菜单文本可能隐含报告本身就是正式产出。若游戏公开反馈如此，应按既有枚举更新为 `observed` 或 `partial`；Skill 不能预先否认该可能性。

### 8.4 会不会让单一 evidence_focus 压过财富和 Skill

不会把 focus 设成 veto。比较表要求同时列 Direct gain、Timing 和 Opportunity cost；若证据无法在目标评审前兑现，或终局已经临近，直接 Wealth/Skill/Health/Network 价值可以胜出。焦点只负责解释当前最需要验证的假设。

### 8.5 会不会误读评审前后时序

Decision Header 的 `review_phase` 和 `target_review` 是硬性上下文。评审月先处理结果，后处理 Energy/Main Action；M48 结算后统一进入 `terminal_processed`。报告禁止使用“本月行动导致本月已经结算的晋升”这类因果表述。

### 8.6 会不会对未知风险过度乐观或保守

风险判断只来自 Risk Management；Career Planning 只能说明行动的职业收益和机会成本。无新 event 只说明当前输入没有新事件，不代表历史风险已经解除。`monitoring` 也不是 `resolved_explicit`；只有后者表示已明确解除。所有未知都必须显式写入既有 `unknown`，并在候选比较中降低确定性，而不是虚构概率。

### 8.7 会不会重复 V0.4 的问题

V0.4 的可观察问题不是“缺少某个单独动作”，而是早期 Level 落后、Prepare Report 使用减少、Network/Skill/Defuse/Intensive Work 增多后仍未追回工资时间。V0.5.1 因而不采用固定的 Network、Skill、Defuse 或加班轮换，也不把 V0.3.3 的行动次数复制成攻略。它强调早期评审前的可兑现成果，同时在晋升后按反馈重新诊断。

## 9. 给 Luna 的实施规格

### 9.1 只修改的范围

- 修改 `Career Planning` Skill 的决策规则、Decision Header、评审诊断、证据状态和 Key Project/Report 比较。
- 修改 `Resource Optimisation` Skill 的 Risk Management 依赖、Energy 组合比较、边际上限、Intensive Work、Prepare Report 和 M48 terminal 规则。
- 保留 Career Controller 的唯一协调职责、现有 session 绑定、checkpoint、恢复和原生 MCP 协议。
- 保留 Risk Management 为唯一风险来源，不添加第二套风险评分、RAG 门槛或隐藏分数模型。
- 不修改正式 solution、Controller、Risk Management、运行环境、历史游戏和比赛规则。

### 9.2 建议的最小指令结构

每个 Skill 的正文建议按以下顺序压缩，减少冲突：

1. Role and hard boundaries。
2. Decision Header 输入与评审时序。
3. Candidate comparison fields。
4. 4–7 条行为规则（带条件、优先动作、机会成本、反例）。
5. 输出格式和 handoff 字段。
6. 禁止事项：不猜公式、不把报告写成交付、不自建风险裁决、不硬编码月份、不在 M48 虚构第九次评审。

删除重复的价值口号、固定轮换示例和与 Controller 重复的执行协议。原有合法性、max 3 candidates、terminal_processed、single focus、A/S audit 等有用机制保留，但按本文规则解释。

### 9.3 责任边界与实施阻碍

- Career Planning 负责读取当前 `observe`、已有反馈和现有 `strategy.feedback_loop`，形成简短 Decision Header；Resource Optimisation 读取该摘要并结合当前 Energy 菜单、剩余预算和 Risk Management 输出做候选比较。
- Career Controller 保持现有职责、状态协议、checkpoint、session 绑定和 MCP 流程，不新增字段生成逻辑，也不负责晋升诊断。
- 两个 Skill 继续复用现有字段和枚举：`review_phase` 使用 `pre_review`、`post_review`、`terminal_processed`；`target_review` 使用下一次未处理评审、既有 `unknown`，或 M48 后的 `terminal_processed`；`evidence_focus` 使用 `delivery`、`visibility`、`capability`、`scope`、`relationships`、`unknown`；`evidence_status` 使用 `observed`、`partial`、`negative`、`unknown`。
- 现有 Risk Management 状态只使用 `unresolved`、`mitigation_pending`、`monitoring`、`resolved_explicit`，紧迫程度只使用 `attention`、`elevated`、`critical`；`monitoring` 不得被解释为已解除。
- 已知实施阻碍是离线对照输入没有完整 `strategy.feedback_loop`，因此 30/32 次 `target_review` 为 `unknown`。Luna 需要确认现有运行时是否能让 Career Planning 读取该账本；若不能，这是实施前的上下文可见性阻碍，应通过既有 checkpoint/state 暴露，不得修改 Controller 协议或假设新接口已经存在。

### 9.4 验收标准

Luna 实施后，评审人应逐项检查：

1. **时序：** M6/M12/.../M48 的评审结果先于同月行动进入决策；M48 后 `review_phase=terminal_processed` 且 `target_review=terminal_processed`，不存在第九次评审。
2. **风险边界：** 所有 Defuse 优先理由都能追溯到 Risk Management；Skill 没有新增风险评分或隐藏 veto。
3. **证据边界：** Prepare Report/Intensive Work 不会自动把 `evidence_status` 写成 `observed` delivery；Key Project 也不会自动保证晋升。
4. **动态比较：** 同一菜单能同时比较 Key Project、Report、Push Resources、Rotation、Mentor、Network/Repair、恢复和 Defuse，并记录至少一个机会成本。
5. **focus 可让步：** evidence_focus 无法及时兑现或终局直接价值更高时，模型能选择 focus 之外的合法动作，并解释原因。
6. **健康约束：** Intensive Work 会计入 Health/Dignity、风险和后续恢复成本；不会因为 Level 目标自动成为第一选择。
7. **终局切换：** M48 已结算后，模型能优先比较直接终局维度，而不是机械刷 Output/Report。
8. **输入完整性：** 离线同类快照若提供 `strategy_feedback_loop`，模型能读取 `target_review` 和 `evidence_status`；若不提供，输出会标记 unknown 而不是编造。
9. **精简性：** 两个 Skill 在不重复 Controller/Risk Management 协议的前提下，保持短、分支清楚、无固定月份攻略。
10. **回归场景：** 至少人工复核 M6、M9、M18、M33、M36、M42、M48 七类场景，确认输出是条件化判断，而非强制复制 V0.3.3 或 V0.5 的选择。

## 10. 结论与待批准状态

V0.5.1 最值得押注的改进不是增加更多原则，而是把“下一次评审需要什么证据”“当前动作是否真的产生了该证据”“该证据能否及时兑现”连成一个可检查的决策链。历史数据支持三点：晋升早于最终评分有巨大工资时间价值；绩效等级不能单独预测晋升；风险处置必须保留但不能无限挤占职业资本。V0.5 离线对照进一步显示，策略文本已有不少正确机制，但评审上下文没有稳定进入输入，导致模型在真实成果、报告可见性、健康恢复和排雷之间出现可解释但不够有证据的分歧。

本报告是 V0.5.1 的研究和设计规格，不是对 S 级、固定晋升月份或具体得分的保证。完成正式 Skill 修改前，应先由评审批准本设计；批准后再交给 Luna 实施并按验收标准复核。
