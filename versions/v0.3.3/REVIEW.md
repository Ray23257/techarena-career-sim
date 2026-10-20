# V0.3.3 最小工程修复及审查包

生成时间：2026-10-20T16:36:47.337704+00:00。

**修订与静态/离线回归完成：131通过、0失败、0错误、0跳过。未安装、未重载、未调用模型或游戏工具，未恢复或新开任何游戏。**

- ZIP完整Windows路径：`C:\Users\Ray\Desktop\tech-arena\starter-kit\techarena-career-sim\v033-review.zip`
- 本报告完整路径：`C:\Users\Ray\Desktop\tech-arena\starter-kit\techarena-career-sim\v033-review-report.md`
- 本地发行版本：JiuwenSwarm 0.2.4b3；openjiuwen 0.1.16.post2。只读取发行元数据与源码，没有导入框架。
- 保持The Raytirement Plan、mode=agent、1 Agent+4 Skills。三个专业Skill逐字节未改。

## 一、问题范围与设计判断

这是局部工程缺陷，不需要重构职业策略或四Skill架构。实际缺陷是读写成功后没有正确执行独立语义校验，不能以“把两个错误字符串改成一致”作为修复。V0.3.3删除了生成框架ID后再拼接文件名的步骤，在经可信系统注入验证的独立任务目录D内使用固定career-checkpoint.json。

**源码依据足以支持正常无项目、单驱动分支的会话命名空间隔离；不足以提供事务、操作系统沙箱、并发排他或模型必然服从的保证。** Runner UUID截取12位，目录mkdir允许已存在；不能只看到一个合规目录名或一个不存在的标记就证明它从未使用过。初始官方任务、当前会话历史和新分配Runner会话的来源也必须一致；缺乏可信fresh依据就停止。绑定项目/custom cwd/共享fallback均不接受。固定文件名相同但D不同，绝对路径不同，不跨目录恢复。

## 二、实际源码调用链

| 结论 | 本地源码位置 | 函数/限制 |
| --- | --- | --- |
| 新游戏请求生成新的框架对话；continue复用历史框架ID | [career_sim_runner/headless_play.py:32](C:/Users/Ray/Desktop/tech-arena/starter-kit/techarena-career-sim/career_sim_runner/headless_play.py:32) | new_drive_session_id；resolve_drive_session_id:71；play_headless:98,129 |
| 框架ID进入WebSocket信封；模型任务文本不直接携带ID/cwd | [career_sim_runner/ws_client.py:149](C:/Users/Ray/Desktop/tech-arena/starter-kit/techarena-career-sim/career_sim_runner/ws_client.py:149) | _build_envelope；prompts/play_headless.md:1 |
| 无项目默认目录为内部目录/projects/安全化会话ID；空ID回退共享根 | [.venv/Lib/site-packages/jiuwenswarm/common/utils.py:1452](C:/Users/Ray/Desktop/tech-arena/starter-kit/techarena-career-sim/.venv/Lib/site-packages/jiuwenswarm/common/utils.py:1452) | get_default_project_session_workspace_dir；mkdir(exist_ok=True)，并非排他创建 |
| 逐请求选定task_workspace/task_cwd，传入原生cwd及提示rail | [.venv/Lib/site-packages/jiuwenswarm/server/runtime/agent_adapter/interface_deep.py:6249](C:/Users/Ray/Desktop/tech-arena/starter-kit/techarena-career-sim/.venv/Lib/site-packages/jiuwenswarm/server/runtime/agent_adapter/interface_deep.py:6249) | _apply_runtime_config_stages:6266–6299 |
| 模型调用前系统提示实际加入cwd、项目未设置及内部目录 | [.venv/Lib/site-packages/jiuwenswarm/agents/harness/common/rails/runtime_prompt_rail.py:498](C:/Users/Ray/Desktop/tech-arena/starter-kit/techarena-career-sim/.venv/Lib/site-packages/jiuwenswarm/agents/harness/common/rails/runtime_prompt_rail.py:498) | before_model_call；英文分支:690–724，中文分支:587–612 |
| 原生读写工具加入Agent ability_manager | [.venv/Lib/site-packages/openjiuwen/harness/rails/sys_operation_rail.py:50](C:/Users/Ray/Desktop/tech-arena/starter-kit/techarena-career-sim/.venv/Lib/site-packages/openjiuwen/harness/rails/sys_operation_rail.py:50) | SysOperationRail.init |
| 文件路径按cwd解析；写入带预读/历史记录且没有排他事务 | [.venv/Lib/site-packages/openjiuwen/harness/tools/filesystem.py:351](C:/Users/Ray/Desktop/tech-arena/starter-kit/techarena-career-sim/.venv/Lib/site-packages/openjiuwen/harness/tools/filesystem.py:351) | _resolve_tool_file_path；WriteFileTool.invoke:1083；file_path返回:1220；create_if_not_exist:1195 |
| install会清理sessions/memory等，不能用于本次现场修复 | [career_sim_runner/install.py:46](C:/Users/Ray/Desktop/tech-arena/starter-kit/techarena-career-sim/career_sim_runner/install.py:46) | install_submission:46–55；本次从未调用 |

区别：框架内部确实保存transport session_id，但它不作为任务文字独立提供给模型。RuntimePromptRail最终构建的系统段落才给模型完整D和内部目录。V0.3.3以该完整目录作为输入，不从用户路径、Skill路径、通用Workspace标题或两个自造字段建立身份。原生文件操作返回data.file_path及读回data.content；后者可能包含工具添加的行号前缀，必须区别显示格式与解析后的JSON值。

## 三、最终标记和路径契约

| 内容 | V0.3.2 | V0.3.3 |
| --- | --- | --- |
| 框架定位 | 从目录截取F，再拼probe文件名并保存framework_session_id | 保留可信完整D；不在标记或state元数据保存framework_session_id，不做该ID拼接 |
| 固定标记 | career-checkpoint-probe-F.json | D/career-checkpoint.json |
| JSON版本 | schema1 / solution0.3.2 | schema2 / solution0.3.3，旧版不自动迁移 |
| verified_directory | 目录语义但与其他字段混淆 | 必须等于原始可信注入D，完整目录 |
| verified_path | 曾写入目录 | 必须是完整D/career-state-G.json；仅reserved标记中为null |
| 游戏UUID G | 原生new_game返回的真实UUID | 保持32位hex验证和原始返回值，不用框架ID；marker/state/native history需一致 |
| 读写验收 | 成功回执和相互匹配仍可能漏掉错误 | I/O成功、实际工具返回路径、完整JSON/schema/phase、独立D/G证据各自核对 |
| 不完整/旧绑定 | 有条件重建存在误解空间 | 缺标记/缺state、旧版、未知/冲突记录立即停；不扫描、修复、迁移或重建 |

标记恰有7个键：schema_version、solution_version、verified_directory、verified_path、game_session_id、phase、halted_reason。拒绝额外、缺失、重复键及类型错误。

1. 仅可信、明确的全新初始Runner请求，且原生固定标记读出明确不存在，才能先预约。
2. 写入并读回phase=reserved，game_session_id和verified_path均null；检查工具实际file_path等于D/固定basename，verified_directory等于**原始注入D**。已有reserved不能被视为本请求刚建立的创建权限。
3. 只有同一次未中断初始请求中完成语义验收的预约，才允许一次new_game。错误、超时、未知UUID均保留现场停止。
4. 成功原生响应G独立约束state顶层session_id、marker.game_session_id、状态文件名及完整路径P。state写读通过后，再把同一owned marker绑定为bound并写读核对。
5. 恢复必须重新核对原始D、固定marker、完整state及当前原生历史/Runner真实游戏ID。之后才可原生observe+check_latest_logs有界对账；不确定时绝不重发旧choice。自动续接不解除工程halt，也不授权新游戏。

普通行动仍不强制pending落盘；开局直接文件调用预算仍为7次，另有工具预读保护可能增加读操作。固定命名简化的是身份变换，不是删除文件能力、语义或恢复安全检查。

## 四、风险持久化最小澄清

第二局Network达到0且notes注意到风险，state却只保留初始化快照。现在Controller明确：重大可见脆弱状态本身也是证据，不必等events另发文字警告。首次观察Network=0，或公开失败方向对应的Health=0/Dignity=0/Wealth负值，记录实际值、月份、revision、证据来源并在下一次游戏调用前做紧凑checkpoint。与真实警告分开标注；重复未变证据合并，实质恶化/缓解/解决另存。数值回升不等于隐藏风险清零。没有发明连续次数、隐藏阈值或风险公式，没有把Health=3设为新阈值。Risk Management、Career Planning、Resource Optimisation正文全未改。

## 五、实际文件修改及差异

| 文件 | V0.3.2 SHA-256 | V0.3.3 SHA-256 | 实际改动 |
| --- | --- | --- | --- |
| `solution/design/decision_report.md` | `9bafa74991ac316ab2906d69f96651273ef8f6984ad1aabd554fdf997b0bdaae` | `915aeb3da626cc1c2721b7b6732a00c2f2782cc02d4cd3bec1f259f73932edec` | 记录run-two实证、工程变更、历史章节标记、恢复与新局的独立条件 |
| `solution/design/skills_design.md` | `a46b300c91ada4ebba79664bab90d205f10bf3e2ab013f7bd550d6edac059ff0` | `f5ea43c287a7a596a4f4cc6c2a92947dec6d2cbc1c9b597f10b1835445d7bb4f` | 与Controller匹配的目录/版本/schema契约；路由及专业策略保持原样 |
| `solution/manifest.json` | `6b457847efee3a79026c54b459326883235f11f0c7e482ab98d47858e4bd1d13` | `098c5f503dfb84d1a3f9dc23af7fef399deb059d46778007b16eb7e6680aa943` | 版本名；固定D/marker全局门禁、独立语义验证、双路径含义、保护旧局及可见脆弱状态持久化；队名/mode不变 |
| `solution/README.md` | `c3351e49b7f411280512fcd2f07b5e5516bc9568a09363b2b5b723481b9d9b5e` | `dd6b1f43aab72c2f914873f7386b3194468373c53b6f0a67a2b2b2adaf276270` | 当前状态、固定标记使用边界和未来安装/游戏审批说明 |
| `solution/skills/career-controller/SKILL.md` | `da532176cf47655b844f78a0f0f929fd5b69aa84ce26a9cbaa7846c3778e7631` | `f0b2138f07144bf0d77e5bf69096c9d39bfae23251a995828ac3527b740db8e4` | 删除框架ID拼接/持久化；固定marker、schema2、独立D/G验证、缺state停机、保护第二局、风险保存及工具显示格式说明 |
| `offline_tests/test_v03.py` | `c2bb49ae9e721f962b4ab1f806db8fd0d05123eeea03f33482584d013e538da7` | `820a385d46faeb76bc77433d317e9a6f8425d6b1e0f2e2420dd60770ad9b7682` | 保留原96测试名；固定标记参考验证、35项新用例、历史阶段断言和86项现场指纹保护 |
| `offline_tests/RESULTS.md` | `f73fdae694020ea668cfb52c4adaf9fc56f63903dfaeea82b61e7c1308444626` | `61d0a76e3f7c773331d86ee670f1ce97f31ce709602c271a66c600cf488f8ada` | 完整131项结果、证据等级、重现依赖和初始失败口径说明 |

未变的3个文件为solution/skills/risk-management/SKILL.md、career-planning/SKILL.md、resource-optimisation/SKILL.md，均与v032-review.zip逐字节相同。没有修改已安装实例，active_install及已安装IDENTITY仍是原有V0.3.2。

## 六、回归结果及证据等级

- **131通过，0失败，0错误，0跳过**；原96测试方法名称全部保留，新增35项。
- A类文档/源码/指纹一致性24项；B类真实官方纯函数/源码片段在内存桩下15项；C类确定性策略/安全参考92项。
- 实际反例来自run2-v032-gpt-review-20261020.zip，SHA-256为d35bf6fd4e99c66069b39fbf2bad97c81a443392ecc2c2b44f7595bea3d8084f。只在内存读取原始错误probe/state及原生readback，不提取或写入运行目录。
- 截断旧marker、单纯重命名/改版本、错误字段相互一致、跨目录同名marker、UUID冲突、reserved/halted/异常marker、缺state/恢复缺marker、仅I/O成功、旧choice重放等均被拒绝；合法完整参考绑定可通过。
- 原生读回fixture核对reserved与bound两个真实时序；行号前缀去除不改变JSON字段值。
- 初次执行未修改的旧96项时，两项历史方法存在过期live断言：数据库、skills_state、旧career-survival三个子断言失败，旧会话文件读取报错。它们属于已获授权安装/第二局运行的阶段变化。现在仍验证历史副本原哈希，并额外验证当前86项现场/配置指纹，未跳过测试、未恢复旧文件、未忽略真实变化。
- 新增readback用例初次曾把reserved读回与最终bound快照要求整体相等，出现1失败；已按真实时序分别校验，未改生产策略以迎合测试。最终命令完整通过。

执行命令：

```powershell
.\.venv\Scripts\python.exe -B -X utf8 offline_tests/test_v03.py
```

完整逐项记录见offline_tests/RESULTS.md。测试仍依赖本地已安装源码及不可变历史fixtures；十文件审查包不是自包含的运行环境。确定性参考通过不代表模型运行时执行了同样校验，未做任何LLM/Agent/文件工具live验收。

## 七、第二局现场保护

本次对第二局错误probe、state、framework session、原始events/transcript、模拟器日志、数据库、全部审计证据及旧审查ZIP只读取。86项SHA-256保护全部通过；旧基线、Runner源码、环境配置和锁文件也有持续指纹断言。未删除、覆盖、移动、修复、迁移或安装。

- 受保护框架：career-sim-runner-7a72e52cc135。
- 受保护游戏：cc0ca28b4e694fd993c60b538aac3c80。
- 当前数据库仍与run-two database-after.sqlite3一致：6f5833e31b6db69346d2079f1e4d1322093ea905ff013cf865284cd1c6c10a58。
- 不使用install间接清理现场；默认WorkSwarm、依赖、模型配置均未操作。

## 八、剩余风险和两种后续验收

**静态修订可交外部审查，尚不能声称运行门禁已强制修复或允许安装/游戏。**

1. Skill仍是提示词，不是工具边界验证器。模型可能漏做D/G相等检查；固定文件名只去掉一个已失败的变换。若要求不可绕过保证，需要另行评审确定性工具/执行边界机制，当前授权范围未实现。
2. 文件工具没有事务或排他创建；同框架并发、UUID前缀碰撞、宿主路径/symlink变化、上下文全丢失或日志落后都无法靠本修订保证恢复。正常单驱动命名空间隔离不是绝对唯一性证明。
3. 缺失marker/state或legacy版本一律停机，代价是自动恢复能力受限；不是允许新开局。Runner仍可能发续接并消耗Token，需要外部停止，不能伪造终局。
4. 新增门禁尚未经模型、真实写读或完整48个月执行验收；131项测试不能替代这些验收。

### 若要恢复第二局（本次未授权）

- 单独明确批准恢复该UUID，先确认原始现场、审查包、数据库及会话证据完整。
- 另行审核并批准旧版本绑定的修复/迁移设计、写入边界和回滚证据；当前V0.3.3明确拒绝接管它，不含迁移实现。
- 不得先install以免删掉现有会话。核对原生MCP及实际实例任务状态、原始UUID、风险/行动历史及路径绑定。
- 仅在之后获得游戏工具授权时，原生observe/check_latest_logs对账；无法确认进度则停，不重放旧choice、不调用new_game。

### 若要启动新游戏（本次未授权）

- 单独决定未完成第二局的保留/后续安排，并明确批准新一局；不静默放弃旧局。
- 若需要安装，先另批保护现场的安装方案并完成备份及恢复验证，不能直接使用会删sessions的默认install。之后另批实例操作，核对实际安装版本、四Skill及原生MCP稳定性。
- 在真正全新无项目框架会话中，确认官方初始任务与可信D来源、原生文件工具、固定marker不存在；完成独立语义门禁后才允许一次new_game。不得使用旧框架/游戏或continue混入新局。
- 运行时重点观察存储语义、风险checkpoint、恢复栅栏及最终原生终局识别；异常停机，不自动重试。

## 九、审查ZIP验收

- 恰好10个文件：solution8 + offline_tests2；无额外目录条目、重复/绝对/越界路径。
- ZIP CRC完整性通过；每个条目SHA-256等于源文件；打包前后源文件字节未变。
- 凭据内存扫描通过；不包含.env、API Key、实例配置、数据库、会话或游戏日志。
- 旧ZIP和第二局审查包/历史备份未修改。
- v033-review.zip SHA-256：`2454bbac1acb2e1388f647f988bdc754715814f9469dc26926a986c55b609f35`。

| ZIP相对路径 | ZIP条目与源文件共同SHA-256 |
| --- | --- |
| `solution/design/decision_report.md` | `915aeb3da626cc1c2721b7b6732a00c2f2782cc02d4cd3bec1f259f73932edec` |
| `solution/design/skills_design.md` | `f5ea43c287a7a596a4f4cc6c2a92947dec6d2cbc1c9b597f10b1835445d7bb4f` |
| `solution/manifest.json` | `098c5f503dfb84d1a3f9dc23af7fef399deb059d46778007b16eb7e6680aa943` |
| `solution/README.md` | `dd6b1f43aab72c2f914873f7386b3194468373c53b6f0a67a2b2b2adaf276270` |
| `solution/skills/career-controller/SKILL.md` | `f0b2138f07144bf0d77e5bf69096c9d39bfae23251a995828ac3527b740db8e4` |
| `solution/skills/career-planning/SKILL.md` | `e7271fee67833a8bcbcef3a427d92de084d7ec12dce7d1d8e1a4bbb02d0209b4` |
| `solution/skills/resource-optimisation/SKILL.md` | `0447df5d7746cf9eed66d02943352a726f02c4f30bb3f35e817d6708f64efabd` |
| `solution/skills/risk-management/SKILL.md` | `ae859c195ee133a3363baa6974c6326721e7aeb6c23de445c4b016678745ffcb` |
| `offline_tests/test_v03.py` | `820a385d46faeb76bc77433d317e9a6f8425d6b1e0f2e2420dd60770ad9b7682` |
| `offline_tests/RESULTS.md` | `61d0a76e3f7c773331d86ee670f1ce97f31ce709602c271a66c600cf488f8ada` |

## 附录：Controller与manifest实际统一差异

其余五个改动文件的差异职责及新旧哈希见第五节；专业Skill无差异。

```diff
--- V0.3.2/solution/manifest.json
+++ V0.3.3/solution/manifest.json
@@ -1,6 +1,6 @@
-{
-  "team": "The Raytirement Plan",
-  "name": "Career Survival V0.3.2",
-  "mode": "agent",
-  "instruction": "Use one Agent and four Skills. Unless already engineering-halted, at entry and after continuation/context compression read career-controller with skill_tool. Use only native mcp_career-emulator-engine_* tools for games; never substitute Bash, clients, subprocesses or database access, delegate, enable Symphony or rewrite Skills. Before new_game follow the controller storage gate: derive framework_session_id only from the trusted no-project runtime cwd binding, verify native file tools and persist/read-back a reserved probe; halt if unavailable. Framework IDs are never game session_id values. Read missing relevant Skill bodies on demand and reuse available bodies. Checkpoints are event-driven, not mandatory before ordinary actions. Bind career-state-<session_id>.json only to the real native new_game UUID in the verified framework scope, and persist/read-back the probe-to-game binding. Never assume cross-task persistence or scan other sessions. Never call new_game if a game exists or may exist, a reservation exists, or this is an automatic continuation; halt on error/missing session_id without retry. Engineering halts remain latched across generic Runner continuation prompts; only explicit operator repair/authorization permits resumption. Never fake termination to stop the driver. Without a latched engineering halt, on EVERY recovery or uncertain execution reconcile native observe and check_latest_logs regardless of checkpoint status; missing logs/unchanged stats do not prove non-execution. If unresolved, stop rather than replay an old choice or start over. Preserve material risk, reviews, promotion and strategic changes; stop before the next action on nonterminal checkpoint failure. Observe before each action, use one current legal one-based choice with concise non-empty notes, check success and keep game calls serial. Specialists advise this same Agent. Prioritize sustainable Level/Wealth and risk-control improvement without invented thresholds, formulas or future outcomes. After the final success obtain native observe termination, report exact ending_score and stop game calls even if terminal file persistence fails. Distinguish completed settlement from failed=true flags."
-}
+{
+  "team": "The Raytirement Plan",
+  "name": "Career Survival V0.3.3",
+  "mode": "agent",
+  "instruction": "Use one Agent and four Skills. Unless already engineering-halted, at entry and after continuation/context compression read career-controller with skill_tool. Use only native mcp_career-emulator-engine_* tools for games; never substitute Bash, clients, subprocesses or database access, delegate, enable Symphony or rewrite Skills. Before new_game verify the complete trusted no-project runtime cwd D and native file tools; use only fixed D/career-checkpoint.json, not a filename assembled from a framework ID. File read/write success alone is insufficient: compare returned paths and parsed directory fields independently with original injected D, and game IDs with the actual native response. Do not persist framework_session_id. verified_directory is D; verified_path is the full D/career-state-<real-game-UUID>.json path, null only in the reserved marker. Reserve/write/read-back and semantically validate before the single create; bind state and marker to the returned game session_id before actions. Never call new_game if any marker/game may already exist, the scope was previously used, execution is uncertain or this is an automatic continuation. Missing marker/state on recovery is a halt, not permission to start over. No silent legacy migration, cross-task persistence or directory scans. The protected run-two framework career-sim-runner-7a72e52cc135 and game cc0ca28b4e694fd993c60b538aac3c80 must not be accessed, changed or resumed by this version without separate operator approval. Engineering halts remain latched across generic Runner continuation prompts; only explicit operator repair/authorization permits resumption. Never fake termination. On EVERY authorized recoverable interruption or uncertain action reconcile native observe and check_latest_logs; missing logs/unchanged stats do not prove non-execution. If unresolved, stop rather than replay an old choice or start over. Read missing relevant Skill bodies on demand and reuse available bodies. Preserve material warnings AND serious visible vulnerability such as Network=0 before the next game call, plus reviews, promotion, strategic changes and uncertain execution. Ordinary successful actions do not require pending-file writes. Stop before the next action on nonterminal checkpoint failure. Observe before each action; use one current legal one-based choice with concise non-empty notes, check success and keep game calls serial. Specialists advise this same Agent. Prioritize sustainable Level/Wealth and risk-control improvement without invented thresholds, formulas or future outcomes. After the final success obtain native observe termination, report exact ending_score and stop game calls even if terminal persistence fails. Distinguish completed settlement from failed=true flags. Skill instructions and fixed naming do not enforce transactions or tool-boundary safety."
+}

```

```diff
--- V0.3.2/solution/skills/career-controller/SKILL.md
+++ V0.3.3/solution/skills/career-controller/SKILL.md
@@ -4,5 +4,5 @@
 ---
 
-# Career Controller V0.3.2
+# Career Controller V0.3.3
 
 ## Scope and entry
@@ -39,5 +39,5 @@
 Advice shares that revision: risk supplies constraints/evidence, planning an objective, resources at most three distinct candidates. Resolve legality/session/terminal safety first, then evidenced severe survival risk, risk control with long-term Level/Wealth, then other dimensions/efficiency. Minor warnings stay advisory unless evidence warrants restriction. No voting or invented numerical reward.
 
-Use actual one-based choice IDs from the latest successful observation; recheck session, terminal flags, menu, budget and constraints. Only this Agent issues one final `take_action` at a time. Keep intent/event/result in memory. Non-empty notes can say `v032:r12 M9 report; risk=R1:monitoring; prepare review safely`; normally stay within 300 characters (our target, not an official limit). Tags/revisions are not idempotency keys, can recur after lost context and are not preserved in every phase. No ledger dump or lengthy reasoning.
+Use actual one-based choice IDs from the latest successful observation; recheck session, terminal flags, menu, budget and constraints. Only this Agent issues one final `take_action` at a time. Keep intent/event/result in memory. Non-empty notes can say `v033:r12 M9 report; risk=R1:monitoring; prepare review safely`; normally stay within 300 characters (our target, not an official limit). Tags/revisions are not idempotency keys, can recur after lost context and are not preserved in every phase. No ledger dump or lengthy reasoning.
 
 ## Minimal durable state
@@ -45,13 +45,17 @@
 ### Storage capability gate
 
-Use only the framework-injected **Runtime Directory Context / Working Directory Policy** (or their Chinese equivalents), not a generic Workspace header, a Skill path or a user-supplied path. In the audited no-project Runner path, cwd equals `<Agent internal data directory>/projects/<framework_session_id>`. Require project directory to be explicitly unset and that exact parent/child relationship. The final component must fully match `career-sim-runner-[0-9a-f]{12}` (ASCII lowercase hex; no replacement, truncation or invented suffix). This derives the framework ID from a model-visible, source-backed directory binding; the WebSocket ID itself is not separately supplied in the task text. Any other layout, conflicting directory context, relative path, UNC path or `.`/`..` component -> engineering halt. Do not inspect config/runtime_state files to discover an ID or scan other directories.
+Use only the framework-injected **Runtime Directory Context / Working Directory Policy** (or their Chinese equivalents), not a generic Workspace header, a Skill path or a user-supplied path. Let D be the complete current cwd copied from that trusted context. Require project directory to be explicitly unset and D's parent to equal `<Agent internal data directory>/projects`. D's final component must fully match `career-sim-runner-[0-9a-f]{12}` (ASCII lowercase hex). Validate this layout without extracting an ID to construct a filename. The WebSocket ID is not separately supplied in the task text. Any other layout, conflicting directory context, relative path, UNC path or `.`/`..` component -> engineering halt. Do not inspect config/runtime_state files or scan other directories. D is a source-backed single-conversation namespace, not a tool-enforced sandbox or an independently authenticated task token.
+
+The existing run-two scope ending in `career-sim-runner-7a72e52cc135` and game `cc0ca28b4e694fd993c60b538aac3c80` are protected historical evidence: halt without file/game operations in that scope or for that game. V0.3.3 does not repair, migrate or resume them. Any reuse of a previously used/pre-V0.3.3 scope or evidence of an old marker/game requires separate operator review; absence of the new fixed marker does not authorize migration. Do not search for legacy filenames. Only an independently confirmed initial Runner request in a newly allocated framework conversation can qualify as fresh; a generic continuation, missing context or claimed fresh flag without that provenance cannot.
 
 Use absolute file paths inside that verified cwd; no cross-task/reinstall persistence is promised. Inspect actual native tool schemas for `read_file(file_path=...)` and `write_file(file_path=..., content=...)`; missing tools/permissions -> halt before new_game. Native file writes may also create framework history; do not edit that history. This is a single-driver scheme, not an atomic lock for concurrent drivers or a defense against host path/symlink changes.
 
-At a confirmed fresh entry, read only the exact `career-checkpoint-probe-<framework_session_id>.json`. Only an explicit not-found result permits creation; access errors/ambiguous errors do not. An existing marker goes to recovery, never to another new_game. Never overwrite an unrecognized file. Make one write and one read-back of a small marker with schema_version=1, solution_version=0.3.2, framework_session_id, verified_directory, game_session_id=null, phase=reserved and halted_reason=null. Require success, matching returned file path and matching content. This persistent reservation precedes the single new_game attempt. A reserved marker encountered on continuation means creation may have occurred: stop, never retry. Do not delete/reset markers yourself. No marker on a continuation is also not a fresh-start authorization.
+The sole V0.3.3 locator is the fixed absolute path `D/career-checkpoint.json`. It contains exactly: schema_version=2, solution_version=0.3.3, verified_directory=D, verified_path, game_session_id, phase and halted_reason. Do not persist `framework_session_id`: the complete trusted directory is the isolation binding, so there is no model-generated framework-ID pair to compare. `verified_directory` always means D, the directory; `verified_path` means the full absolute `D/career-state-<real-game-UUID>.json` path when bound, and null while reserved. Never use the marker path or directory as verified_path. Native file results supply data.file_path; read results supply data.content, which may have tool-added line-number display prefixes. Interpret the complete underlying JSON, excluding only those display prefixes, not string contents; a partial or unparseable read-back cannot pass. Do not compare an escaped display string instead of the parsed JSON value.
 
-Only the successful native new_game response supplies the initial real game `session_id`; require a full `[0-9a-fA-F]{32}` UUID-hex match and no error. Error, timeout or invalid/missing ID -> halt with the reservation retained, no observe/take_action or second new_game. After success write/read-back `career-state-<session_id>.json` in verified cwd, then update/read-back the owned probe to phase=bound and game_session_id equal to that exact returned ID. Complete both bindings before game actions. Binding metadata lives in `strategy.checkpoint`. The probe is a current-framework locator, not game state; never use framework_session_id as a game ID or filename suffix for career-state.
+At a confirmed fresh entry, read only that fixed marker. Only an explicit not-found result permits reservation; access errors/ambiguous errors do not. An existing marker goes to validation/recovery, never to another new_game. Never overwrite an unrecognized file. Make one write and one read-back with game_session_id=null, verified_path=null, phase=reserved and halted_reason=null. File I/O success is not semantic validation: independently compare the returned absolute file path with trusted D plus the constant `career-checkpoint.json`, and the parsed verified_directory with the original injected D, not with another generated JSON field. Reject missing/extra/duplicate keys, wrong types/schema/version/phase, non-null reserved game/path or any path mismatch. Only this freshly written, semantically verified reservation within the same uninterrupted initial request permits the one new_game attempt. An existing reserved marker never does. Do not delete/reset markers yourself. No marker on a continuation is also not a fresh-start authorization.
 
-On recovery derive scope again, validate the exact marker's schema/version/framework/directory and phase, then read only its bound game's checkpoint. A valid game ID in the current native tool history/Runner continuation must agree with the marker; `unknown`, a framework ID or a conflicting UUID is not authority to select another game. Reserved, halted, malformed, incompatible or conflicting binding -> halt. Missing necessary state uses bounded reconstruction below only with an independently verified game binding. Do not enumerate state files or read a different framework's marker. Offline checks do not verify live file capability.
+Only the successful native new_game response supplies the initial real game `session_id` G; require a full `[0-9a-fA-F]{32}` UUID-hex match and no error. Error, timeout or invalid/missing ID -> halt with the reservation retained, no observe/take_action or second new_game. Derive P as D plus the constant `career-state-` plus that exact returned G plus `.json`. After success write/read-back the state at P, then update/read-back the owned fixed marker to phase=bound, game_session_id=G and verified_path=P. Validate actual returned paths against independently derived D/P, directory fields against original injected D, and all game IDs against the actual native response G. Matching two self-generated strings is insufficient. Complete both bindings before game actions. Binding metadata lives in `strategy.checkpoint`; there too verified_directory=D and verified_path=P. No framework-ID field, shortened ID or unknown ID is a substitute for G.
+
+On recovery obtain D anew from the trusted injection, validate the fixed marker's exact path/schema/version/directory/phase and full state path, then read only the referenced state in D. A valid game ID in the current native tool history/Runner continuation must agree with marker and state; `unknown`, a framework ID or a conflicting UUID is not authority to select another game. Reserved, halted, malformed, incompatible or conflicting binding -> halt. Reject legacy framework_session_id fields rather than silently normalizing them. Missing marker or state on recovery -> halt, never treat it as a fresh game or an empty risk ledger. Do not enumerate state files, read another framework's marker or automatically reconstruct/migrate a missing checkpoint. Offline checks do not verify live file capability.
 
 Our checkpoint example (placeholder strings are not game values):
@@ -59,6 +63,6 @@
 ```json
 {
-  "schema_version": 1,
-  "solution_version": "0.3.2",
+  "schema_version": 2,
+  "solution_version": "0.3.3",
   "session_id": "<returned-session-id>",
   "observation_revision": 0,
@@ -68,5 +72,5 @@
   "reviews": [],
   "quarter": {"key": null, "observed_energy": null, "confirmed_spend": [], "remaining_plan": [], "main_action_status": "unknown"},
-  "strategy": {"priority": "survival, risk control, long-term Level and Wealth", "next_review": null, "hypotheses": [], "feedback_loop": null, "checkpoint": {"framework_session_id": null, "verified_path": null, "reason": null, "halted_reason": null}},
+  "strategy": {"priority": "survival, risk control, long-term Level and Wealth", "next_review": null, "hypotheses": [], "feedback_loop": null, "checkpoint": {"verified_directory": null, "verified_path": null, "reason": null, "halted_reason": null}},
   "action": {"status": "none", "observation_revision": null, "choice": null, "notes": null},
   "ending": null
@@ -87,5 +91,5 @@
 | --- | --- | --- |
 | Verified session binding | Bind the real game ID and its checkpoint to the framework locator | Four calls once: state write/read-back + owned marker update/read-back; pre-game absence read + probe write/read-back costs three more |
-| New issue, worse/material risk evidence, confirmed mitigation or explicit resolution | Preserve consumable warning evidence and unresolved issues | One write per material update; identical recurring warning text with no urgency/decision change stays in memory until the next checkpoint |
+| New issue, worse/material risk evidence, confirmed mitigation or explicit resolution | Preserve consumable warning evidence and unresolved issues, including serious visible vulnerability even without an events warning | One write per material update; identical recurring evidence with no urgency/decision change stays in memory until the next checkpoint |
 | Observed half-year review or promotion | Retain all eight review records, actual feedback and state changes | One write per observed batch; review and promotion together share one write |
 | Material strategic switch | Persist the feedback hypothesis, changed allocation and next review check | One write only when objective/evidence/hypothesis materially changes; coalesce with review/risk updates, not every different choice |
@@ -96,9 +100,11 @@
 Save material `events` before another game call: observe consumes warnings; empty events do not clear risk. Deduplicate repeats, update last_seen in memory and flush at the next trigger. No full transcript, routine quarterly/revision-only writes or credentials.
 
+Visible vulnerability is also evidence: first observing Network=0 or another published failure-direction boundary (for example Health=0, Dignity=0 or Wealth below zero) requires a compact risk entry and checkpoint before the next game call, even with empty events. Record actual value/month/revision and its source separately from a simulator warning. This is our conservative persistence trigger, not a hidden failure threshold or a numeric risk formula. Persist material worsening, meaningful mitigation/result or explicit resolution; repeated unchanged values alone do not require a write every observe. Do not auto-clear the entry when a value recovers; record that visible improvement without asserting hidden safety. For other deterioration use actual warnings, outcomes and risk-management evidence; do not invent universal numeric cutoffs.
+
 If a required nonterminal checkpoint fails, do not submit the next action: preserve the ID and report the persistence error. Do not switch to a Bash client or start another game. If an uncertainty checkpoint itself was lost in a crash, the unconditional recovery fence below still applies; absence of a pending file is never permission to replay.
 
 ## Recovery and terminal handling
 
-Only the real game ID from a verified native new_game result or its current-framework bound marker identifies the game. Runner continuation IDs must agree; never substitute the framework ID or `unknown`. Native observe confirms current state, not ownership by itself. Read only the file whose framework/path/game binding is independently verified, then check `schema_version`, `solution_version` and `session_id`. Reject cross-session state and do not silently import an older solution version. Missing/malformed state is not a safe empty ledger: reconstruct only what native evidence supports. If necessary risk/review history or session identity cannot be recovered sufficiently for safe continuation, report the gap and stop instead of guessing or creating another game.
+Only the real game ID from a verified native new_game result or its current-directory bound marker identifies the game. Runner continuation IDs must agree; never substitute the framework ID or `unknown`. Native observe confirms current state, not ownership by itself. Read only the file whose directory/path/game binding is independently verified, then check `schema_version`, `solution_version`, `session_id` and strategy.checkpoint directory/full path. Reject cross-session state, missing/malformed state and older versions; do not silently import, migrate or reconstruct them. If necessary risk/review history or session identity cannot be recovered sufficiently for safe continuation, report the gap and stop instead of guessing or creating another game.
 
 On EVERY continuation first honor any latched engineering halt: it blocks further tool calls until explicit operator repair/authorization. Otherwise, for interruption or transport ambiguity, pause actions regardless of saved action status. Obtain native observe and `check_latest_logs(session_id, count=10)`; if necessary request count=30 once. These counts are our retrieval budget, not engine limits. Compare the latest event/menu/phase, time, changes, ordered action/outcome records and notes where available. If the last action is confirmed committed and the current phase is coherent, discard the old intent and decide only from the current observation. Never resend a cached choice. An unchanged visible state or missing log entry is not proof of non-execution: state saving and action-log append are separate source operations, and capped/hidden effects can leave visible stats unchanged. If ambiguous after bounded reconciliation, keep `uncertain` and stop; no exact-once guarantee is claimed.
@@ -110,5 +116,5 @@
 ## Engineering halt across Runner continuations
 
-On an engineering halt, retain the reason in current conversation/state and, if storage still works and the probe is recognized as ours, set its phase=halted and halted_reason with one best-effort write (read first if the file tool requires it). Do not retry failed persistence in a loop. Once halted, generic Runner continuation prompts do not authorize recovery attempts, another new_game or action submission: report the same short blocker without repeating tool calls. Resume only after explicit operator repair and authorization; do not infer repair from a prompt saying continue. A genuine recoverable interruption without a prior engineering halt still uses the bounded reconciliation fence. Unknown execution never authorizes resending an old choice.
+On an engineering halt, retain the reason in current conversation/state and, only if storage still works and the current-version fixed marker was independently validated as ours, set its phase=halted and halted_reason with one best-effort write (read first if the file tool requires it). Never modify a conflicting, legacy or protected record to make it pass. Do not retry failed persistence in a loop. Once halted, generic Runner continuation prompts do not authorize recovery attempts, another new_game or action submission: report the same short blocker without repeating tool calls. Resume only after explicit operator repair and authorization; do not infer repair from a prompt saying continue. A genuine recoverable interruption without a prior engineering halt still uses the bounded reconciliation fence. Unknown execution never authorizes resending an old choice.
 
-The Runner may keep sending continuations because a normal error report is not a structured terminal game event. A Skill cannot stop that driver, guarantee compliance after context/state loss, provide atomic execution or recover an unreturned game UUID. Do not fake ending_score/DONE to escape; operator intervention is required. If all halt evidence is lost, an automatic continuation is still never a fresh-start authorization.
+The Runner may keep sending continuations because a normal error report is not a structured terminal game event. A Skill cannot stop that driver, guarantee compliance after context/state loss, provide atomic execution or recover an unreturned game UUID. Directory equality and semantic checks here are model instructions, not independently enforced tool-boundary validators, transactions or locks. Fixed naming removes an unnecessary ID transformation; it does not guarantee LLM compliance or exclusive creation. Do not fake ending_score/DONE to escape; operator intervention is required. If all halt evidence is lost, an automatic continuation is still never a fresh-start authorization.

```
