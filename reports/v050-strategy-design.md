# V0.5 Career Survival 策略设计：动态晋升准备度与风险预算

## 0. 结论先行

V0.5 应继续使用 **1 Agent + 4 Skills**，先不增加 Agent、工具或运行时 Router。核心变化不是再加入一批行动建议，而是给 Agent 一个可重复的“职业证据账本”和评审反馈循环：

> 读取当前状态与事件 → 判断下一次真实评审前最缺的证据 → 比较当前菜单中能在剩余时间内兑现的行动 → 施加风险约束 → 只执行一个合法行动 → 观察实际结果 → 更新证据账本和下一步假设。

“争取每一次评审都晋升”是正确的优化方向，但“每 6 个月一定升一级”不是当前证据支持的假设。公开规则明确说高职级有更高整体要求，晋升阈值、绩效公式和风险计数器均未公开。V0.5 应最大化每个窗口的晋升准备度，同时保留完整 48 个月的 Wealth、Network、Health、Skill 和 Risk Control。

目前最有价值的空间是：

1. 让 L4 阶段的高绩效更可能转化为晋升，减少 M30–M42 之间的无目标重复投入。
2. 在不损害前 12 个月晋升能力的前提下，提高 Network 与 Wealth。
3. 把“真实成果、组织可见性、领导范围、关系支持、能力积累”分开记录，避免把 Output 数值当成晋升门槛。
4. 让 Energy 和季度主行动围绕同一个下一评审目标协同，而不是各自重复刷属性。

---

## 1. 数据范围、证据质量和限制

### 使用的原始证据

- V0.2 第一局：`20261019T214724Z`，游戏 UUID `a86e8ff1b7924a598bc63422d52afd69`。
- V0.3.3 第三局：`20261020T172255Z`，游戏 UUID `e173ebcb61964fa58385148cc424e206`。
- V0.4 第四局：`20261020T202902Z`，游戏 UUID `7d85d9fd06284e668fdd230853b18db4`。
- 三局各自的 `score_report.json`、`events-*.jsonl`、`transcript-*.log`、已有审计报告。
- 官方 `docs/rules.rst`、`docs/failure-and-ending.rst`、`docs/handbook.rst`。
- 当前 V0.3.3 的四个 Skill 和 `reports/v033-promotion-analysis.md`。

### 已知的数据问题

- 三局不是匹配随机种子，事件序列、模型输出和工具重试次数不同。
- 因此只能把“实际发生了什么”归因于日志，不能把分数变化直接归因于某一条策略。
- 评审前的完整隐藏状态不可见；部分状态是在评审结算后才返回的。报告中的“评审前状态”只使用评审前最近一次可信 `observe`。
- 日志会记录模型提出的理由和工具返回的变化，但不能证明某一条提示词在模型内部被严格执行，也不能单独证明行动的因果效果。
- 官方公开表给出了行动方向和工资表，但没有给出晋升阈值、绩效公式、隐藏风险公式或剧情触发概率。

---

## 2. 三局结果与晋升事实

| 局次 | 结果 | 最终 Level | Wealth raw | Risk Control | Network | Skill | Health & Dignity |
|---|---:|---:|---:|---:|---:|---:|---:|
| V0.2 第一局 | B / 63.02 | L5 | 35.1 | 1/10 | 63 | 118 | 18 |
| V0.3.3 第三局 | A / 70.38 | L5 | 33.7 | 10/10 | 44 | 117 | 20 |
| V0.4 第四局 | C / 59.85 | L4 | 21.4 | 10/10 | 36 | 92 | 20 |

V0.3.3 的半年评审轨迹：

| 窗口 | 绩效 | 晋升结果 | 关键反馈或状态 |
|---|---|---|---|
| M6 | C | L1→L2 | “neither hot nor cold”“on watch list”“show clearer outcomes next phase”；HR 提示累计风险。 |
| M12 | B | L2→L3 | “You climbed too fast”；旧网络没有适应新头衔，Network 7→4，Health 6→5，Dignity 10→9。 |
| M18 | B | 未晋升，留在 L3 | HR 语气改善；随后出现肝功能、甲状腺和心电异常，需要降低压力并就医。 |
| M24 | B | L3→L4 | 经理要求“show clearer outcomes so I can speak in committee”；同时出现工作压力和请假处置。 |
| M30 | B | 未晋升，留在 L4 | “do not look like you only hustle without winning. Same bar in six months.” |
| M36 | A | 未晋升，留在 L4 | “you were first on my list... come to me with ideas and I will fight for resources.” |
| M42 | A | L4→L5 | 晋升为 Principal/team lead；“Less hallway politics, more output and relationships.” |
| M48 | B | 未晋升，留在 L5 | 这是半年评审等级；最终结算评级另为 A。 |

因此实际观察到的晋升间隔为 **6、6、12、18 个月**。V0.2 也记录 M6、M12、M24、M42 晋升。重复日期是重要线索，但不是固定任职门槛的证明。

V0.4 的轨迹是 M6 未晋升、M12 L1→L2、M18 L2→L3、M24 未晋升、M30 L3→L4、M36 未晋升、M42 未晋升、M48 未晋升。它从第一窗口开始落后，最终少了一个职级，工资累积和 Skill/Network 也随之落后。

---

## 3. 隐藏晋升机制的竞争假设

### H1：存在随职级增加的任职或资格约束

**支持证据：**

- 两局都在 M6、M12、M24、M42 晋升。
- V0.3.3 的 L4 在 M30 和 M36 都未晋升，直到 M42 才升。
- 官方明确说高职级整体要求更高。

**反对或不足：**

- 只有两局在相同日期晋升，样本很小，且无匹配随机种子。
- V0.4 的晋升时间不同，说明日期不是一个简单的全局固定表。
- M18 的 L3 duration 为 7，M30 的 L4 duration 为 7，M36 的 L4 duration 为 13；这些读数不能单独区分任职约束与能力/剧情因素。

**结论：** 可作为待验证假设，不能写成“L4 至少要 18 个月”或任何硬编码月份。

### H2：晋升主要由长期职业资本和组织证据决定

**支持证据：**

- 官方写明晋升关注长期结果，不是某一个突然变亮的月份。
- V0.3.3 M24 和 M42 的晋升都伴随较长期间的 Output、Skill、Network 和反馈积累。
- M36 虽为 A，却没有晋升，说明单次绩效等级不是充分条件。

**反对或不足：**

- 不能从日志确定 Skill、Output、Network 的真实权重。
- 不能证明“准备报告”或“关键项目”中的任何一个是晋升必要条件。

**结论：** 这是最适合指导 V0.5 的工作假设，但必须保持证据标签：已观察、推测、未知。

### H3：A 或 S 绩效不保证晋升，组织范围和支持可能是额外条件

**支持证据：**

- V0.3.3 M36 为 A，经理明确认可并愿意争取资源，仍未晋升。
- V0.3.3 M42 为 A 且晋升，反馈提到产出和关系；两次 A 的结果不同。
- V0.4 M42 为 A 但仍为 L4。

**结论：** A/S 应提高准备度判断，但不能直接转成“下一次必升”。V0.5 必须在高绩效未晋升时切换调查方向，而不是继续无条件加班。

### H4：两局前 12 个月策略相似，导致日期一致

**支持证据：**

- V0.2 与 V0.3.3 都在 M6、M12 晋升，且都在早期使用关键项目、成果展示和健康/风险处置的组合。

**反对或不足：**

- 两局故事不同，模型行动也不完全相同。
- V0.4 采用了不同的早期行动，结果从 M6 开始落后；这只能说明行动轨迹和事件环境共同重要。

**结论：** “相似行动导致相似晋升”是可研究的相关性，不能当作因果证明。

---

## 4. 为什么 V0.4 失败

V0.4 的失败是一个真实结果，但它没有证明“积极争取晋升”不可行。更准确的解释是：V0.4 把策略文字写得更积极，却没有把“当前缺少哪类晋升证据”变成一个稳定的状态变量。

### 结果差异

- V0.3.3：M6、M12 早期连续晋升，M24 晋升，M42 晋升，最终 L5、Wealth 33.7、Skill 117、Network 44。
- V0.4：M6 未晋升，M12 才升 L2，M18 升 L3，M30 升 L4，最终 L4、Wealth 21.4、Skill 92、Network 36。

### 可能原因与证据边界

1. **第一窗口的差异具有放大效应。** V0.4 M6 为 C 且未晋升；之后工资、可用发展时间和评审起点都落后。它是事实，但不能证明是某一个 M3 行动造成的。
2. **V0.4 的 Energy 选择更丰富，却没有形成明确的评审证据链。** 它在 M12 选择了健康恢复、报告、Network 和导师关系，但仍是 C、没有当期晋升。导师动作可能有长期价值，但没有公开证据能证明它在该窗口兑现。
3. **V0.4 在 M33、M36、M42 使用了 Skill study，但最终 Skill 仍为 92，低于 V0.3.3 的 117。** 这说明单独增加 Skill study 并没有抵消早期职级落后和不同剧情的影响。
4. **V0.4 仍然重复关键项目和报告。** 因此“增加策略文字”没有阻止机械动作，证明 V0.5 需要记录职业证据缺口和行动兑现期限，而不是再增加原则。
5. **随机剧情是重大混杂因素。** 三局没有匹配种子，不能把 V0.4 的 C 归因给 Skill 文件，也不能把 V0.3.3 的 A 归因给某个单一行动。

V0.4 的真正教训是：策略必须改变行动选择的触发条件，且每个评审周期只能检验少量明确假设；增加描述本身不会带来动态行为。

---

## 5. V0.5 核心状态：Promotion Readiness Ledger

V0.5 不使用数值评分或自造晋升阈值。Controller 已经维护必要的会话和风险安全边界；Career Planning 增加一个很小的职业证据摘要，按每次评审更新。

### 记录字段

```text
next_review: observed next six-month review opportunity, or unknown
current_level: returned Level
level_duration: returned duration_in_level; context only
review_history: last reviews and promotions with exact feedback

evidence:
  delivery: strong | partial | unknown | negative
  visibility: strong | partial | unknown | negative
  capability: strong | partial | unknown | negative
  scope: strong | partial | unknown | negative
  relationships: strong | partial | unknown | negative
  sustainability: stable | strained | severe | unknown

current_hypothesis: one sentence
candidate_action_families: at most three offered families
next_check: the observation or review that can confirm or weaken the hypothesis
unknowns: explicit list
```

这些标签是我们自己的证据记录，不是模拟器字段，也不是隐藏评分的替代品。

### 证据如何更新

- **strong：** 日志中有明确结果或反馈支持，例如已完成并被领导/客户/团队承认的成果。
- **partial：** 有动作或局部结果，但兑现时间、组织认可或影响范围尚未确认。
- **negative：** 明确的负反馈、关系损失、失败交付或风险事件。
- **unknown：** 当前没有可靠证据。不得从原始状态数值大小推断“已经满足”。
- **sustainability：** 由实际健康变化、风险警告和未解决问题组成，不等同于 Health 数值，也不等同于 Risk Control 评分。

### 每次评审后的通用循环

1. 保存评审等级、实际奖金、职级变化、经理反馈、HR 警告和评审前最近观察。
2. 比较上一阶段的证据是否真的变化：成果是否完成、是否被看见、影响范围是否扩大、关系是否稳定、风险是否缓解。
3. 如果晋升成功，先读取晋升后的 Network、Health、Dignity、警告和职级时长，处理实际代价，再准备下一窗口。
4. 如果没有晋升，按反馈选择一个新的调查方向：交付、可见性、能力、范围或关系。不要自动重复上一次解决方案。
5. 如果 A/S 但没有晋升，保留高绩效事实，并把“绩效不是充分条件”写入当前假设；优先检查范围、组织支持、关系和任职上下文。
6. 如果 B/C/D，先区分反馈是在说结果不足、展示不足、能力不足、关系问题还是风险问题；只有反馈支持时才改变对应投入。
7. 为下一次评审设一个可观察的验证点，而不是设一个保证晋升的目标。例如：“在下一次评审前完成一次有明确交付结果的跨团队责任，并观察是否得到组织认可”。

### 如何识别当前机会

每个故事和主行动先归类为一个或多个证据机会：

- **真实交付：** 能完成、交付、稳定或量化结果的工作。
- **可见性：** 已完成成果需要向正确的领导/评审链路展示。
- **能力：** 当前事件明确需要的技术能力或长期能力积累。
- **范围/领导：** 承担责任、协调团队、管理资源、跨团队影响。
- **关系/组织支持：** 修复摩擦、建立可信合作、获得必要支持。
- **生存/合规：** 健康、尊严、风险、合规红线和未解决组织问题。

“Output 增加”只代表可见绩效资本发生变化，不等于真实成果完成，也不等于晋升证据已经完整。报告、关键项目、资源申请、导师关系和轮岗必须根据当前事件和反馈判断它们代表的证据类型。

---

## 6. Career Planning 的决策规则

### 输入

- 当前 `observe` 的状态、事件、合法选项、剩余月份和当前 Level。
- 最近一次可信的风险摘要。
- 评审/晋升历史和每次反馈。
- 当前 Promotion Readiness Ledger。
- 本季度 Energy 已花费和当前剩余预算。

### 输出

Career Planning 只返回建议给同一个 Agent：

1. 当前主要晋升机会或长期价值机会。
2. 当前最弱且有证据支持的职业证据类别；没有证据时返回 `unknown`。
3. 最多三个当前合法候选行动，注明兑现时间、机会成本和未知结果。
4. 一个下一次检查点。
5. 不执行工具、不锁定未来 choice、不声明晋升保证。

### 主行动选择

按以下顺序检查，但不形成机械动作序列：

1. 当前合法性、Controller 终局和 Risk Management 硬约束。
2. 当前故事是否提供能在下一评审前兑现的真实机会。
3. 当前评审反馈最明确地指向哪类证据缺口。
4. 比较交付、可见性、能力、范围和关系候选；只保留 2–3 个有实质差异的选项。
5. 选择收益更可能在剩余时间内兑现、风险可控且机会成本可接受的行动。
6. 行动成功后重新 `observe`，记录实际变化；如果没有兑现，不要把推测写成结果。

### 连续未晋升的处理

- 第一次未晋升：保留上一假设，检查反馈和实际变化，避免一次结果就完全重构。
- 第二次连续未晋升：审计上一假设是否真的被执行、是否产生了对应证据；选择一个不同的、反馈支持的干预方向。
- 第三次或更久未晋升：把“任职时间、范围、组织支持或隐藏条件”列为未知竞争假设；不要强行刷同一属性，也不要直接认定无解。
- 如果任职时间可能是因素，仍然利用剩余时间提高 Wealth、Network、Skill 和 Risk Control；等待窗口不等于重复报告。

### 晋升后的处理

晋升后立刻检查：

- Network 是否下降或出现摩擦。
- Health/Dignity 是否下降。
- HR/经理风险提示是否改变。
- 当前新职级是否需要更大范围的成果或领导证据。

如果出现 M12 这种 Network 7→4 的明确代价，关系修复和组织融入应进入下一阶段候选；但不假设一次修复会清除隐藏风险。若没有可见损伤，则不为“晋升后恢复”机械消耗资源。

---

## 7. Resource Optimisation 的动态风险预算

Resource Optimisation 继续使用最多三个候选方案，避免运行时穷举 112 种组合。它必须读取 Career Planning 的当前证据缺口，并与 Risk Management 合并筛选。

### 三档风险状态

这是我们的保守决策状态，不是模拟器的隐藏数值：

- **Red：** 明确严重或持续升级的风险警告；Health/Dignity/Network/Wealth 已接近公开失败方向；或存在未解决合规/组织问题。禁止为了晋升增加已知风险，先保留相关处置和可恢复动作。
- **Amber：** 有中等警告、近期明显恶化或晋升后的关系摩擦，但没有明确严重触发。最多接受一个有明确职业兑现机会的已知成本，执行后立即观察，不把未知收益当作理由。
- **Green：** 没有严重警告，状态稳定或改善，当前行动成本可恢复。可以接受一个有限的、已知方向的职业成本，但不把两个高代价动作叠加，也不强迫耗尽 Energy。

Health 的“可以接受消耗”必须由当前观察和趋势支持：没有明确健康警告、当前不在近期低谷、并且替代方案不能提供同等的评审证据。这里不设置数字阈值。

### 3 点 Energy 的候选生成

1. 先过滤当前菜单和真实成本，不能使用记忆中的 choice 编号。
2. Red 状态先保留相关风险处置或健康动作。
3. 对 Health/Dignity 已满的已知增益做裁剪；未知效果保留为未知。
4. 生成最多三个候选：
   - 保护候选：风险或健康优先。
   - 评审候选：直接服务当前证据缺口。
   - 平衡候选：保护和职业资本各占一部分。
5. 如果 Skill、Network、报告或高强度工作都可选，比较它们的兑现时间、公开成本和当前证据需求：
   - Skill study：2 Energy，Skill+、Health-；适合明确能力缺口，不能因为 Skill 数值大就继续刷。
   - Network maintenance：1 Energy，Network+、Dignity+；适合关系证据不足或晋升后摩擦，不能假设它清除所有组织风险。
   - Prepare report：1 Energy，Output+、Dignity+；适合已有成果需要整理/展示，不能把重复报告当成真实交付。
   - Intensive work：2 Energy，Output+、Health-、Dignity-；只有当前有具体交付机会、健康与风险状态允许、且无更安全替代时才进入候选。
   - Defuse：2 Energy，效果可能不可见；只在已有风险证据支持时保留，不因为“看起来保险”而每季度重复。
6. 每次只提交当前第一步，成功后重新观察。旧候选不自动授权后续行动。
7. Energy 为 0 只表示预算已用完；是否浪费要看当时是否选择了无用、封顶或明显劣势动作。保留 Energy 也可以是合理结果。

### 主行动和 Energy 的配合

- Career Planning 先确定本阶段证据目标，例如“交付结果不足”或“范围/组织支持未知”。
- Resource Optimisation 再比较 Energy 是否能支持该目标，并保护健康和风险。
- 主行动可用于形成真正成果或范围，Energy 可用于支持关系、能力、报告或恢复；二者不能把同一个 Output 增长重复当作两个独立证据。
- 如果主行动已完成真实交付，Energy 可以偏向可见性或关系；如果只有报告没有成果，不能继续堆报告来假装完成了职业目标。

---

## 8. 20 个真实决策场景回放

下面的场景来自事件日志的季度菜单和转录记录。它们是离线决策材料，不能计算反事实分数；“V0.5 应如何判断”描述的是输入到策略的变化，不是已经验证的结果。

| # | 时点 | V0.3.3 实际 | V0.4 实际 | V0.5 应读取的差异与决策 |
|---:|---|---|---|---|
| 1 | Q1 / M3 | Network maintenance + report + health recovery；主行动 key project。 | Intensive work + Network maintenance；主行动 key project。 | 先看 M6 前是否已有真实交付、健康和风险警告。高强度工作只有在具体交付且无健康/风险红线时进入候选；报告不能替代交付。 |
| 2 | Q2 / M6 | Defuse + health recovery；主行动 report results。 | Health recovery + defuse；主行动 key project。 | 评审结果已返回后，读取 C/B、反馈和风险，而不是把上一季度动作延续。成果已存在时展示成果，成果不足时才比较 key project。 |
| 3 | Q3 / M9 | Health recovery×2 + report；主行动 key project。 | Health + report + Network；主行动 report。 | 若上一评审要求“清晰成果”，要比较真实交付与展示现有成果；不能只根据 Output 数值选择。 |
| 4 | Q4 / M12 | Health recovery + defuse；主行动 lay low。 | Health + report + Network；主行动 mentor。 | M12 后 V0.3.3 明确出现“爬得太快、Network 7→4”。下一阶段应由实际摩擦触发关系修复；没有摩擦时不机械 mentor。 |
| 5 | Q5 / M15 | Intensive work + report；主行动 key project。 | Intensive work + report；主行动 key project。 | 两局相同选择不能说明它总是正确。检查当前 Health、警告和交付期限，决定是否承担 2 Energy 的健康成本。 |
| 6 | Q6 / M18 | Report×2 + health；主行动 key project。 | Defuse + Network；主行动 key project。 | V0.3.3 M18 B 未晋升，且随后有健康检查异常。V0.5 应把“能力/成果/范围/健康”分开；不能把 M18 写成固定晋升月，也不能因未升就无条件加班。 |
| 7 | Q7 / M21 | Report + Network + report；主行动 key project。 | Health + report + Network；主行动 report results。 | 若当前已有交付但组织认可不足，report/Network 可能比再做同类项目更匹配；若交付仍不足，报告的边际价值有限。 |
| 8 | Q8 / M24 | Report×3；主行动 key project，随后晋升 L4。 | Report + health + Network；主行动 key project，未晋升。 | 同样的主行动在不同事件环境下结果不同。V0.5 必须保存当期真实成果和组织反馈，不能把 key project 当作晋升按钮。 |
| 9 | Q9 / M27 | Health + report×2；主行动 key project。 | Report + health + Network；主行动 report results。 | 报告应服务已完成成果；若上一窗口没有晋升，应先查“缺成果、缺认可还是缺范围”，不能用报告次数替代诊断。 |
| 10 | Q10 / M30 | Health + report×2；主行动 key project。 | Defuse + report；主行动 key project。 | V0.3.3 M30 B 反馈是“不要只忙碌，要赢得结果”。这应触发“真实交付/资源范围”候选，而不是继续三次报告。 |
| 11 | Q11 / M33 | Network + report×2；主行动 key project。 | Report + Skill study；主行动 key project。 | 若当前能力已经足够而范围/认可未知，Skill study 不一定是最优；若剧情明确能力要求，Skill study 才有更强证据。 |
| 12 | Q12 / M36 | Report×3；主行动 key project；随后评审 A 但未晋升。 | Skill study + report；主行动 key project；随后评审 B 未晋升。 | A 未晋升是关键分支：V0.5 应停止机械刷 Output，寻找领导范围、组织支持或关系证据；同时保留风险/健康约束。 |
| 13 | Q13 / M39 | Health + report×2；主行动 key project。 | Defuse + report；主行动 report results。 | M36 未升后，先根据反馈决定是范围、可见性还是关系缺口。若风险已稳定，defuse 不应自动占用职业机会。 |
| 14 | Q14 / M42 | Report×3；主行动 key project，随后 A、L4→L5。 | Skill study + report；主行动 key project，A 但未晋升。 | V0.3.3 M42 反馈强调“产出和关系”。V0.5 将其作为证据组合，而不是把成功归因给 report×3 或 key project 单项。 |
| 15 | Q15 / M45 | Report×3；主行动 key project。 | Health + report + Network；主行动 key project。 | 最终评审已处理后，比较直接计分属性和财富机会，不为不存在的下一晋升窗口继续刷 Output。 |
| 16 | Q16 / M48 | Defuse + Network；主行动 rotation。 | Health×2 + Network；主行动 rotation。 | M48 的最后阶段不能假定还有 L6 机会。若评审已结算，rotation 的延迟收益可能来不及兑现，应比较直接分数和已确认收益。 |
| 17 | M5–M6 故事 | V0.3.3 为赶 M6 交付选择周末推进项目；随后 M6 仍为 C 但晋升。 | V0.4 在 M9 也选择周末推进项目，时间点不同且 M6 已未晋升。 | 识别“短期 Output+”与健康成本、评审截止时间、当前风险。行动可提升交付，但不能保证高绩效或晋升。 |
| 18 | M12 后关系摩擦 | V0.3.3 记录快速晋升后的 Network 下降，并在后续故事中采用责任承担、关系修复和团队融入。 | V0.4 在 M12 处于 burnout 故事，之后走 mentor/架构方向，但早期晋升已经落后。 | 晋升后先检查实际摩擦和健康；根据返回状态决定修复、范围或能力投入。不能预设晋升后必然需要 mentor。 |
| 19 | M36 AI 透明度/领导范围 | V0.3.3 选择推动团队 AI transparency standard，得到积极领导反馈，但 M36 仍未晋升。 | V0.4 也选择承担类似透明度和管理方向，最终 L4。 | 领导型故事可能增加范围证据，但是否影响晋升未知；应在账本中记录“scope partial”，下一阶段再用一项具体可见责任验证。 |
| 20 | M41–M42 责任范围 | V0.3.3 选择 hybrid tech-and-people holding role，随后 M42 晋升 L5。 | V0.4 M42 面对更高加薪和新环境故事，但没有晋升。 | 真实领导责任、可验证成果和关系支持要一起观察；不能把一次 holding role 直接写成晋升原因。 |

这些场景说明 V0.5 的区别不在于把“key project”换成另一个固定动作，而在于：相同菜单下，当前证据缺口不同，候选集合和接受的机会成本不同。

---

## 9. V0.5 的通用执行流程

### 月度故事

1. `observe` 后读取当前事件和所有合法选项。
2. 给选项标注：交付、可见性、能力、范围、关系、生存/合规中的一个或多个类别。
3. 对每个候选分开记录立即效果、可能的延迟后果和未知项。
4. 删除违反 Controller 或 Risk Management 硬约束的候选。
5. 若存在能在下一评审前兑现的高价值职业机会，比较它与安全/关系候选；没有明确兑现路径时，不为“看起来积极”付出健康或风险成本。
6. 选一个当前合法 choice，提交简短 notes，成功后重新观察。

### 季度 Energy

1. 读取实际 Energy 菜单、剩余预算和已确认行动成本。
2. 获取 Risk Management 的 Red/Amber/Green 约束。
3. 获取 Career Planning 的下一评审证据缺口。
4. 生成保护、评审、平衡三类候选，最多保留三组。
5. 裁剪已封顶的 Health/Dignity 增益和没有明确用途的重复行动。
6. 逐步提交第一步，成功后重新观察并重建剩余候选。

### 季度主行动

1. 只使用当前主行动菜单。
2. 真实交付优先于机械增加 Output；已有成果需要认可时，报告/公开结果才有针对性。
3. 关系或范围证据不足时比较 mentor、resource request、rotation、relationship repair 或当前剧情中的承担责任机会。
4. 不强制 action rotation，也不强制 key project；每次说明当前证据和机会成本。

### 评审反馈

- 保存事实：等级、奖金、职级变化、反馈、风险和评审前最近状态。
- 更新一个工作假设，不同时改变所有投入。
- 下一窗口检验假设。如果仍未晋升，改变诊断方向，而不是重复同一动作。
- 若晋升后 Network/Health 下降，先恢复可见状态并保留对隐藏风险的未知标记。

### 游戏尾段

在真实 M48 评审结算前，继续比较晋升可能与直接计分属性；结算后，不再为了不存在的第九个窗口刷 Output。优先确认 Wealth、Network、Health、Risk Control、Skill 和终局处理。

---

## 10. 各 Skill 的协作边界

### career-controller

保持 V0.3.3 的 session、真实游戏 UUID、固定 checkpoint、原生 MCP、恢复和终局规则。它只负责把专家建议合并成一个合法 choice，并维护 Promotion Readiness Ledger 的必要写入，不承担晋升公式推理。

### risk-management

提供风险证据、Red/Amber/Green 状态、已知处置、未解决风险和下一次核查点。它可以阻止明显严重风险下的高代价选择，但不能因为未知效果就否决所有职业机会。

### career-planning

维护 Promotion Readiness Ledger，解释反馈，提出 2–3 个候选职业证据方向，并明确哪些是事实、推测和未知。它不执行 MCP，也不声明阈值。

### resource-optimisation

把 Career Planning 的证据目标转换成三点 Energy 的少量可行候选，比较公开成本、兑现时间、健康风险和机会成本。它不负责决定长期职业目标，也不穷举全部组合。

统一裁决顺序：合法性和终局安全 → 严重生存风险 → 直接风险控制 → 下一评审可兑现的职业证据 → Level/Wealth 长期价值 → Network/Skill/Health 等其他得分与资源效率。

---

## 11. 如何证明这不是 V0.4 式文字堆叠

V0.5 必须用离线规则测试证明“输入不同，建议会变”，而不是只检查文档里出现了更多关键词。

### 必须覆盖的参考场景

1. 同一个菜单、`delivery=unknown` 与 `visibility=partial` 时，Career Planning 可以保留 key project/资源请求，并说明交付机会。
2. 同一个菜单、`delivery=strong`、`visibility=partial` 时，报告/公开成果可以进入候选，不能继续把报告当成新成果。
3. `A + no promotion` 时，下一假设必须调查 scope/relationships/tenure context，不能自动增加 intensive work。
4. `C + delivery feedback` 与 `C + presentation feedback` 必须产生不同候选顺序。
5. 连续两次未晋升后，参考策略不得继续原样重复上一干预。
6. M12 的 Network 下降后才触发关系修复候选；没有下降时不强制修复。
7. Red 状态禁止 intensive work；Amber 状态最多一个有明确兑现路径的高代价机会；Green 状态仍不能强制耗尽 Energy。
8. Health/Dignity 已满时裁剪纯恢复候选；Skill/Network/Output 不得被当作已知封顶。
9. 所有季度策略都读取当前菜单，不得把 M18/M24/M36 等月份写成固定 action。
10. 反事实场景只验证参考规则，不能宣称 Agent 已经学会或分数已提高。

### 实际运行前的证据

- 静态 JSON/YAML/frontmatter、四 Skill 路由和 Controller 边界检查。
- 对三局真实场景的离线回放，只验证候选分类、反馈分支和风险状态，不调用模型或 MCP。
- 保存 V0.3.3 版本和 V0.5 实验版本的完整哈希。
- 下一局使用单一新版本、新 UUID 和一份独立审计报告；不覆盖 V0.3.3 原始记录。
- 结果比较只能报告分数、晋升、状态和动作差异，不能把单局改善写成因果证明。

---

## 12. 预期收益、代价与失败回退

| 目标 | 可能收益 | 代价或风险 |
|---|---|---|
| 更早晋升 | 更高 Level 评分；提前获得更高月薪 | 为范围、关系或交付投入 Energy，可能损失 Health/Network |
| Wealth | 每提前一个窗口，增加更高工资档位的剩余月份 | 晋升未兑现时，昂贵行动可能只带来健康或风险损失 |
| Network | 减少 M12 类快速晋升摩擦，补足组织支持 | 关系行动可能占用真实交付机会，且不保证隐藏风险消失 |
| Health | 仍保留 V0.3.3 的生存硬约束和针对性恢复 | 过度恢复会牺牲晋升和 Wealth 机会 |
| Risk Control | 保留 V0.3.3 的 10/10 结果和原生风险台账 | Red 状态下过度保守可能延迟职业资本，但这是可接受的生存约束 |
| Skill | 在明确能力缺口时获得长期收益 | V0.4 说明单独增加 Skill study 不能保证晋升或抵消早期落后 |

公开工资表给出理论参考：L4 为 0.7 Wealth/月，L5 为 1.0，L6 为 1.5。若仅作静态估算，L4→L5 提前 6 个月且工资从下一月生效，理论增加约 `(1.0-0.7)×6 = 1.8` Wealth；L3→L4 提前 6 个月约 `(0.7-0.5)×6 = 1.2`。这是带有生效月份假设的反事实上界式估算，不是模拟结果，也不含奖金、剧情收益或失败损失。

### 回退方案

V0.5 必须在独立分支和独立版本目录中开发。正式运行前保留 V0.3.3 的完整快照、Skill 哈希和部署备份。若 V0.5 出现低于基线的结果、工具绕行、存储门禁失败、严重 Token 浪费或策略无法解释，直接恢复 `versions/v0.3.3/solution`，保留 V0.5 日志作为失败实验，不覆盖历史局。

---

## 13. 独立判断

“尽可能早地晋升”是合理目标；“M6、M12、M18、M24 连续晋升”只能作为实验目标，不能作为设计前提。随着职级上升，公开规则明确提高整体要求，且较高职级需要更大影响范围。把每个窗口都当成同一难度，会鼓励模型在高职级阶段盲目消耗 Health 或 Risk。

V0.5 最值得做的不是让 Agent 更激进，而是让它在每次评审后回答三个可审计问题：

1. 上一阶段到底产生了什么证据？
2. 哪一类证据仍然未知或不足？
3. 当前菜单中哪一个行动最可能在下一次评审前补足它，且成本可控？

如果答案是“未知”，Agent 应保留一项安全的、有用的基线行动，并把假设写清楚。这样既能追求更早晋升，也能在晋升不兑现时继续积累 Wealth、Network、Skill 和 Risk Control。

当前证据支持 V0.5 作为 **单 Agent、四 Skill 的定向实验**，不支持多 Agent，也不支持硬编码任何晋升月份或门槛。
