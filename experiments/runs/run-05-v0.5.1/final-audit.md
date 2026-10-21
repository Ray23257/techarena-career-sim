# V0.5.1 第五局受控实战最终审计

审计日期：2026-10-21（UTC）。本报告记录本轮一次受控部署、一次重载和一次完整游戏；没有启动第六局，也没有在游戏后改Skill。

## 结果摘要

- 最终评级 **C**；量化分 **50.4/100**；存活并完成 **48个月**；最终职业级别 **L4**；终局财富 **17.6**。
- `competition_partial_score` 原样记录为 **35.28**。量化分各维加权和为50.4；partial字段的单独口径未在日志中解释。
- 晋升：M12 L1→L2、M24 L2→L3、M36 L3→L4；M6、M18、M30、M42、M48未晋升。M48终局评审后仍为L4。
- 本局未达到S级。相对第一、三、四局分数更低；这只是单局观察，不能证明版本间因果效果。

## 部署、重载与隔离

- 部署前现场：active install指向正式V0.3.3；career_emu为停止状态；数据库有4条会话。文件级部署使用V0.5.1隔离方案，未覆盖正式`solution/`、V0.3.3基线、V0.5副本或历史输出。
- 正式审查包SHA-256：`552bda9eada41a3a49d3210e74bc10b221c986b6d3b39eb55f3947909d378f10`。
- 仅替换运行时Career Controller、Career Planning、Resource Optimisation、全局`IDENTITY.md`及active install元数据；Risk Management和Skill注册保持原样。active install指向V0.5.1实验方案。持久化`solution_version=0.3.3`按批准要求保留。
- 部署前备份/回滚清单：`C:\Users\Ray\Desktop\tech-arena\backups\v051-run5-predeploy-20261021T220528Z`。含被替换文件、哈希清单和数据库一致性快照。部署前SQLite快照SHA-256：`3b5b4f5cf874bc3e96134c354e4b245959f089c4ec6b8a2c222f383b151fd8b8`；`quick_check=ok`，4条旧会话。
- career_emu原为停止状态；一次受控启动后，唯一一次`agent.reload_config`（`ws://127.0.0.1:19092`）返回true。启动期间发生一次自动探测：deepseek-flash，非流式，max_tokens=32，输入200、输出1、总201、缓存0，响应“Red”。reload_config未触发额外探测，随后没有重复重载。
- 部署后Skill SHA-256与审查版一致：Controller `968f57675d6e5a74117a6ae97b7ff9353657307e27cb13e211232018583863e2`；Career Planning `589f5312e24e045bdd96abbba787a044646c43917271739e6594682e02a97c0c`；Resource Optimisation `e5eefd3629178de8e947be91ef8c66f1e4fb1034f316ed47d3f70879a60d4f11`；Risk Management `ae859c195ee133a3363baa6974c6326721e7aeb6c23de445c4b016678745ffcb`（未替换）。四个Skill均启用。模型仍为deepseek-flash，未改`.env`、端点或密钥。

## 最终属性

| 维度 | 开局 | 终局/评分报告 | 变化或得分 |
|---|---:|---:|---:|
| Career Level | L1 | L4 | +3级；raw 4，weighted 12/30 |
| Wealth | 1 | 17.6 | +16.6；raw 17.6，weighted 4.4/20 |
| Health | 5 | 10 | +5 |
| Dignity | 5 | 10 | +5；两项合计raw 20/20，weighted 15/15 |
| Skill | 1 | 80 | +79；raw 80，weighted 10/15 |
| Network | 1 | 36 | +35；raw 36，weighted 6/10 |
| Output | 0 | 26 | +26；评分报告未单列Output维度 |
| Risk Control | 起始值不可见 | raw 7 | normalized 30，weighted 3/10 |

量化分分项：Level 12/30、Wealth 4.4/20、Health&Dignity 15/15、Skill 10/15、Risk Control 3/10、Network 6/10，合计50.4。

## 半年评审与评审前季度行动

评审结算先于同月季度Energy/Main Action。下表“前季”是评审月之前最近一次季度配置（如M6前为M3）。属性变化来自对应Energy/Main Action前后原生观察，未将其后的事件或评审奖励算作行动收益；未列属性当次无可见变化。

| 评审 | 评审时绩效、晋升与反馈 | 前季Energy及直接属性变化 | 前季Main Action及直接属性变化 |
|---|---|---|---|
| M6 | L1，C，未晋升。反馈：表现平平、仍在关注名单，下一阶段需更清晰成果；奖金−0.3，L1月薪+0.3。 | M3：Health Recovery，Health 3→5；Network Maintenance无属性变化；Prepare Report无属性变化。 | Key Project，Skill 5→6。 |
| M12 | L1→L2，C，晋升。反馈仍称表现平平/在关注名单；奖金−0.3，记录L1月薪+0.3，随后通知晋升Engineer。 | M9：Health Recovery，Health 3→5；Network Maintenance无变化；Prepare Report，Output 2→3。 | Key Project，当次无直接属性变化（职级时长推进）；评审通知随后确认晋升。 |
| M18 | L2，C，未晋升。反馈：不要只忙而没有赢得成果；奖金−0.4，L2月薪+0.4。 | M15：三次Prepare Report；Output 5→6，后两次无额外即时收益。 | Key Project，Wealth 4→5。 |
| M24 | L2→L3，B，晋升。经理称整体可接受、无突出成果也无灾难；奖金+0.2，L2月薪+0.4，随后晋升Senior engineer。 | M21：两次Prepare Report，Output 3→5；Network Maintenance，Network 5→6。 | Key Project，Network 6→7、Output 5→6、Wealth 5→6。 |
| M30 | L3，B，未晋升。经理称整体可接受、无突出成果也无灾难；奖金+0.25，L3月薪+0.5。 | M27：Defuse legacy risk（Energy成本2，无即时属性变化）；Prepare Report，Output 9→10。 | Key Project，Skill 29→30、Network 15→16、Output 10→12、Wealth 7→8。 |
| M36 | L3→L4，B，晋升。反馈再次提醒不要只忙于工作却没有成果；奖金+0.25，L3月薪+0.5，随后晋升Staff engineer。 | M33：三次Prepare Report；Output 15→16，后两次无额外即时收益。 | Key Project，Network 19→20。 |
| M42 | L4，B，未晋升。反馈：表现平平、仍在关注名单，要求更清晰成果；奖金+0.35，L4月薪+0.7。 | M39：Defuse legacy risk（成本2，无即时属性变化）；Prepare Report，Output 22→23。 | Key Project，Skill 55→56、Network 27→28、Output 23→25、Wealth 15→16。 |
| M48 | L4，B，终局评审未晋升。反馈称不要只忙而没有成果；奖金+0.35，L4月薪+0.7。 | M45：Defuse legacy risk（成本2，无即时属性变化）；Prepare Report，Output 21→22。 | Key Project，Skill 69→70、Output 22→24、Wealth 14→15。 |

评审结算瞬间快照（字段顺序：Level/Health/Dignity/Skill/Network/Output/Wealth）：M6 L1/6/10/9/3/2/3；M12 L2/3/10/9/3/3/4；M18 L2/9/10/21/5/6/5；M24 L3/6/9/21/7/6/8；M30 L3/9/10/35/21/13/9；M36 L4/10/10/42/19/15/13；M42 L4/10/10/59/35/25/18；M48 L4/9/10/75/36/25/16。M48评审后仍有当季终局行动，故终局评分属性不同于评审瞬间状态。

## Skill读取、MCP与恢复

- Career Controller、Career Planning、Risk Management、Resource Optimisation各成功读取一次（事件序列1、53、57、133）；决策仍由单Agent/Controller协调。
- 原生游戏MCP：`show_employee_handbook` 1次，`new_game` 1次，`observe` 204次，`take_action` 203次。仅有UUID `1359058407d94c66848fa447d334dca1`。每次成功行动后均有observe；未使用`--continue`、旧局恢复或第二次`new_game`。
- 事件文件有431个工具调用及431个结果。3个失败结果：初始固定checkpoint read的预期not-found；两次checkpoint写入因为文件尚未完整读取而被拒。Agent随后完整读取并成功写回；没有重放行动。203次`take_action`全成功，无游戏动作失败或会话恢复事件。
- Runner退出码0，`completed=true`、survival_months=48；未发生提前结束。

## 模型Token与成本

- deepseek-flash；LLM日志记载temperature=0.95、top_p=0.1、streaming=true。游戏时间窗内有433条`llm_call_start`，但只有4条`llm_call_end`，无法把所有开始与完成配对，因此不把433称为已完成模型调用数。Runner只提供聚合用量，没有逐调用Token明细。
- Runner聚合：input **40,927,527**；cached **40,566,272**（约99.1%）；output **83,478**；total **41,011,005**；`total_cost=0.0`。零值不是已核实免费。总输入减缓存输入的派生值为361,255。重载自动探测另计201 Token。没有独立账单证据可确认实际花费。

## 与历史成绩比较

| 局次 | 输出目录 | 评级 | 量化分 | Level | Wealth raw |
|---|---|---:|---:|---:|---:|
| 第一局 | `20261019T214724Z` | B | 63.02 | L5 | 35.1 |
| 第三局 | `20261020T172255Z` | A | 70.38 | L5 | 33.7 |
| 第四局 | `20261020T202902Z` | C | 59.85 | L4 | 21.4 |
| 第五局 | `20261021T220734Z` | C | 50.4 | L4 | 17.6 |

第五局相对第一、三、四局的量化分分别低12.62、19.98、9.45；Level比前两局低一级、与第四局相同；Wealth低于这三局。结果受随机事件、行动结果和模型采样影响，不能据此认定V0.5.1导致退步或证明任何策略因果收益。决策审计中值得后续评审的事实：每季Main Action均为Key Project；M15/M33重复Prepare Report有零即时边际收益；M6/M12/M18/M42绩效反馈未对应晋升。不能仅凭终局Risk Control=7倒推出各风险处置当时不必要。

## 历史完整性及原始材料

- 部署前已哈希记录的12个历史输出文件全部SHA-256匹配（12/12）；第一、二、三、四局的历史输出未改动。
- 部署前数据库快照4条旧会话，其payload哈希目前均一致（4/4）；当前共5条，仅新增本局UUID`1359058407d94c66848fa447d334dca1`。第二局未完成记录仍在。
- 本局原始材料位于：`C:\Users\Ray\Desktop\tech-arena\starter-kit\techarena-career-sim\.career_sim_runner\career_emu\outputs\The Raytirement Plan\20261021T220734Z`，保留events、transcript、score_report.json。
- 本局文件SHA-256：events `f7913bcb0868507a19f78353b30eb44e00d6f2ebbabe82ee50f1721b848558ed`；transcript `ffeeb3641b18f937c179194f1be75fad50ecbb82eb09864d22847d727bbace1e`；score report `27352587622e71a7d66eb3cfb3e03f37efd02fe27cf64c832fbbcf574f4f9372`。
- active install指向：`C:\Users\Ray\Desktop\tech-arena\starter-kit\techarena-career-sim\versions\v0.5.1-experiment\solution`。审计报告：`C:\Users\Ray\Desktop\tech-arena\starter-kit\techarena-career-sim\reports\v051-run5-final-audit.md`。

## 未能确认的边界

Risk Control起始值及逐期隐藏风险状态、逐模型响应的已完成调用数/逐次Token、真实API账单成本、单项行动反事实收益均缺少本地证据。本局不能用于推导未公开的晋升门槛、隐藏分数或S级数学条件。
