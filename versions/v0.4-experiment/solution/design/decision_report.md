# V0.4 strategy experiment — decision report

## Measured V0.2 baseline

One 48-month game completed: B, quantitative score 63.02, competition partial score 44.12. Session: `a86e8ff1b7924a598bc63422d52afd69`. Evidence is in `.career_sim_runner/career_emu/outputs/The Raytirement Plan/20261019T214724Z/` and the matching emulator log.

| Local dimension | Observed weight | Normalized score | Weighted contribution |
| --- | ---: | ---: | ---: |
| Level | 30% | 50 | 15 |
| Wealth | 20% | 43.88 | 8.78 |
| Health/Dignity | 15% | 90 | 13.5 |
| Skill | 15% | 98.33 | 14.75 |
| Risk Control | 10% | 10 | 1 |
| Network | 10% | 100 | 10 |

These are the actual local report's values. Exact promotion/performance formulas, hidden failure counters, hazard values and future event outcomes remain unknown. Local weights do not reveal promotion weights or the full cloud scoring rule. The subsequent V0.3.3 run scored A / 70.38, but the changed event trace and policy/runtime differences prevent attributing the result to one cause.

The old run used Bash clients, and the Runner returned `play_exit_code: 1`, `termination_reason: max_continuations` despite completed settlement. Its reported input/output tokens were 43,039,082 / 143,499. Reported `total_cost: 0` is not reliable evidence of zero billing. Native MCP registration was subsequently repaired at framework level; V0.3.2 run two subsequently proved native new_game/observe/take_action and all four Skill reads, but was stopped for a storage-binding defect; terminal and recovery paths remain unverified.

## Evidence and proposed changes

| V0.2 evidence | V0.3 response | What is not established |
| --- | --- | --- |
| Risk normalized 10/100; repeated severe warnings; risk explosion in emulator log line 711 | Durable scoped risk ledger, relevant mitigation before optional gains, reassessment after intervention | Exact hazard value, causal contribution of each event, quantitative score benefit of mitigation |
| Notes repeatedly called Output the bottleneck because its raw number was smaller | Use explicit feedback and within-stat trends; retain all review windows | Hidden promotion thresholds or guaranteed optimal allocation |
| S review without promotion; long stays at L3/L4 | Start review preparation early, track tenure and actual promotion feedback separately | S grade as eligibility, a fixed tenure gate |
| 48 Energy spent; 21 report actions, 10 health recoveries, 4 defuses, 1 network maintenance, 4 intensive-work actions | Compare feasible sequences, caps and opportunity costs | Zero Energy as evidence of waste; permanent dominance of one action |
| Final-month intensive work/report/project still justified through promotion | Check whether final review already resolved and compare direct terminal benefits | A ninth review or guaranteed late promotion |
| Temporary clients bypassed native structured tool events | Native-only instructions, missing-tool stop, final native observe | End-to-end model compliance before another actual run |

The action counts above are baseline audit observations, not a required future pattern. Promotion first appeared in observations at months 6, 12, 24 and 42. Baseline feedback may be processed before the same month's later quarterly choices; public handbook ordering is approximate. Use actual phase and returned feedback, not a retroactive claim that a later action changed an earlier review.

## Public rules and policy hypotheses

Public: 48 months, 3 non-carrying Energy per quarter, repeat Energy actions while offered, one quarterly main action or none, six-month reviews/promotion windows, higher salary at higher Level, Health/Dignity caps of 10, and the broad failure directions. The public bonus table gives grade directions; actual Wealth amounts must come from returned results rather than assuming that table entries are exact currency.

Hypotheses to test: earlier preparation can improve advancement and cumulative salary; persistent risk evidence can improve risk control; feasible-sequence comparison can reduce avoidable resource costs; concise notes and correct native termination can improve resource efficiency. None is a demonstrated V0.3 score improvement. A risky choice is not automatically wrong merely because its realized outcome was bad.

Risk statuses and urgency classes, event-triggered checkpoints and volatile ordinary intents, the local observation_revision and the notes length target are our policy bookkeeping. They are not official engine fields, counters or hidden thresholds. Skill/Network settlement normalization does not imply an in-game cap or promotion sufficiency.

## Historical V0.3.1 targeted revision after independent review

This section records the previous design; historical V0.3.2 and then current V0.3.3 below supersede its task-ID assumption and startup file-call budget.

| Area | Before (V0.3) | Now (V0.3.1) | Cost/remaining uncertainty |
| --- | --- | --- | --- |
| Ordinary action bookkeeping | Required full pending checkpoint before every action | Volatile intent + native response/notes; file writes only on material triggers | Zero routine file calls per successful ordinary action; crash reconciliation can stop rather than auto-resume |
| Storage assumptions | Assigned writable directory not actually verified | Explicit task/path binding, native tools and write/read-back capability gate before a fresh game; initial session checkpoint verified separately | Two probe calls + two binding calls once, not measured Tokens; runtime capability is still untested |
| Recovery without pending | Pending was the main local intent anchor | EVERY continuation/ambiguity fences execution with observe/logs, independent of saved action status | One observe + one recent-log read, at most one bounded expansion; no exactly-once claim |
| Review feedback | Broad balancing principles | Facts -> prior-period comparison -> evidence-based branch -> one targeted allocation -> next feedback check | More actionable hypotheses; no measured promotion effect |
| Main actions | Generic comparison, project repetition possible | Compare relevant current project/report/mentor/rotation/repair/resource/low-exposure alternatives; require a reason to repeat, not a quota to change | V0.2's 14/16 projects motivate a comparison check, not a causal diagnosis |
| Energy reasoning | Enumerate feasible combinations | Directly construct at most three distinct proposals after legality/risk/cap checks, then prune clear disadvantage and replan after first step | Approximate shortlist can omit an optimum; unknowns remain explicit |

Baseline evidence used for feedback branches: the month-6 C feedback asked for clearer outcomes (emulator log lines 131-139); early leadership-report choices appear at lines 194 and 284. The S review around month 36 did not promote, while L5 first appeared around month 42 (lines 1045-1052 and 1230-1235). Key-project repetition at 14/16 main actions and the large raw-attribute comparisons motivated review of the old habit. These facts do not prove that reporting, mentoring, rotation or any counterfactual would have improved promotion.

A newly checked engineering limit matters for reduced writes: installed `career_emulator/game.py:244-251` performs session save and action-log append separately. A timeout can leave committed state without a matching recent action log. The controller therefore never interprets no log or unchanged stats as non-execution. It stops on unresolved ambiguity after bounded reconciliation; reduced routine persistence trades some automatic recoverability for fewer file calls, not for replay permission.

Material checkpoint triggers preserve consumable risk evidence, actual review/promotion history, major strategy changes and unresolved execution. Costs are explained per trigger in the controller. Same-batch triggers coalesce; ordinary actions/observations and unchanged warnings need no full JSON write. No live file capability, persistent checkpoint, model compliance or Token savings is claimed by offline tests.

Test results are reported in three separate evidence classes: document/format consistency; actual isolated official pure-function behavior under in-memory fixtures; and proposed-policy reference algorithms. Passing the last class is not Agent strategy acceptance. Existing critical format, risk-continuity, session, budget and native-terminal cases are retained while pending-write expectations are updated for the intentional policy change. No V0.3 review ZIP, archived baseline, runtime configuration or source dependency is changed.

## Phase-one verification

Pure offline tests cover current source contract functions isolated with AST, actual JSON/YAML, four-Skill routing contract and scenarios, risk-status continuity, Energy budget/cap examples, session isolation, review timing fixtures and native terminal parsing using the preserved actual ending payload. They neither call the CLI validator nor import/initialize JiuwenSwarm, a model, MCP or the simulator.

Behavioral reference cases check policy consistency, not that the natural-language Agent will implement them. No framework/LLM test and no V0.3/V0.3.1 game is part of phase one. File-tool durability, skill reading, compression recovery, stable MCP after install/reload and final native Agent events remain acceptance items.

## Historical V0.3.2 experiment plan (superseded; not current authorization)

1. Preserve V0.2 source/evidence and verify V0.3 static checks. The first-run temporary clients are archived and removed only after checksum verification; official output/log/database evidence stays intact.
2. Separately approve installation into career_emu. Do not run setup or upgrade dependencies. Check absolute MCP command and native registration after installation/configuration reload, because prior hot reload removed tools.
3. Verify four installed Skill directories, metadata, descriptions and actual native tool schemas. A file installed is not proof a Skill was read or followed. File-tool state save/restore needs actual execution verification.
4. After run authorization, run exactly one current V0.3.2 game. Audit successful Skill reads, one new session, native calls, concise notes, event-triggered writes and recovery reconciliation when not engineering-halted, risk/review history and native terminal recognition. Stop on renewed bypass/registration errors; do not silently replace a failed run.
5. Compare Level, Wealth and risk contribution with the baseline; also survival, other dimensions, review timing, Energy use, native-tool errors and token usage. Separate engineering savings from strategy improvement: V0.2 had abnormal continuation overhead, so total token differences alone do not isolate strategy effects.
6. For later separately approved comparisons change one policy at a time and record model, data/package versions and snapshot hashes. The current new_game API exposes no seed argument; do not claim paired identical-seed trials. Multiple runs may be needed to separate randomness from benefit. Never infer hidden formulas from a single result.

## Historical V0.3.2 storage/bootstrap correction (superseded by V0.3.3)

V0.3.1's safe-task-id probe assumed the model knew an explicitly supplied task ID. Source shows the WebSocket envelope carries the framework ID internally, whereas the initial play prompt does not. The installed no-project path builder and RuntimePromptRail expose cwd as `<Agent internal data directory>/projects/career-sim-runner-<12 lowercase hex>`. V0.3.2 derives framework identity only from that exact trusted binding; custom/bound-project or conflicting scopes halt. The generic Workspace header may refer to Agent-owned data and is not the storage scope.

The probe is now a durable reservation/locator with explicit framework identity, directory, version, phase and a separately bound real game UUID. Only explicit absence at a confirmed fresh start permits reserving; only a successful native new_game response supplies a new game UUID. Reservation survives an uncertain create; no retry is allowed. A bound marker locates only that game's state file in the same current-framework directory. Invalid/unknown/conflicting IDs, marker or path stop. Initial absence/probe/state/binding checks cost seven direct file calls on the happy path, not per action; actual file-tool stale-read guards may add reads. write_file also records framework history, so storage is not side-effect free.

Engineering halt is latched across automatic continuation prompts, with a best-effort owned-marker write when possible. No cached choice replay or fresh new_game follows a generic continuation. No Skill-only transactional, concurrency, process-termination or total-context-loss guarantee is asserted; the unmodified Runner can still consume continuations until operator stop or its limit. A lost/unreturned game UUID and unresolvable execution need operator intervention. These are remaining engineering limits, not improved game outcomes.

Career Planning, Risk Management and Resource Optimisation are byte-identical to the reviewed V0.3.1 package. Four Skills, team and agent mode remain unchanged. No game/model/instance operation accompanies this correction. Source-backed static readiness permits requesting installation acceptance; it does not constitute installation, live storage or Agent end-to-end acceptance.

## V0.3.3 engineering correction after run two

Run two created exactly one game cc0ca28b4e694fd993c60b538aac3c80 in framework conversation career-sim-runner-7a72e52cc135. All four complete Skill bodies were returned. Seven native take_action calls succeeded; no Bash game bypass occurred. The model nevertheless wrote the truncated framework ID 7a72e52cc135 into an ID-suffixed probe and checkpoint. Read-back succeeded but independent semantic checks were not applied. External cancellation stopped the run after M2 actions; database current_month=3, ending_score=null. There is no grade or quantitative score to compare with B/63.02. Original probe, state, sessions, logs, database, audit and review ZIP must remain unchanged.

The checked no-project runtime creates a separate task cwd from the framework conversation. V0.3.3 therefore uses fixed D/career-checkpoint.json within the complete injected directory D, removing the unnecessary ID transformation. It stores no framework_session_id; paths and directory fields are checked against the original trusted runtime input, not against each other. Game UUID still comes only from native new_game. verified_directory is D and verified_path is the complete D/career-state-G.json path. Schema 2 and solution version 0.3.3 prevent silently accepting legacy records. Missing state, uncertain create, existing reserved/halted/conflicting markers and automatic continuations never permit a new game. The known second-run scope/game are explicitly blocked from operations by this revision.

Network reached0 in run two and notes identified vulnerability, but no subsequent risk checkpoint was written. Controller now explicitly persists serious visible vulnerability separately from a true events warning before another game call; unchanged repeats coalesce. Network=0 is evidence for conservative tracking, not proof of immediate failure or any hidden counter. This is a persistence clarification, not a rewrite of risk mitigation or the career/resource strategies.

The fixed marker simplifies the model's work; it does not enforce equality at a tool boundary. No Python Router, tool wrapper, transactional write or Runner modification was added. LLM compliance, concurrent writers, directory aliases, external path changes, missing history and a UUID lost before response remain risks. Offline reference validation can reject the recorded bad marker, but cannot prove that a live model will run the validator or follow the Skill.

## Separate future acceptance decisions

- Recovering run two: separate explicit approval, immutable evidence backup/verification, an audited migration/recovery design for the existing V0.3.2 binding, actual native MCP availability, verified original UUID and sufficient history, then bounded observe/log reconciliation without replay. V0.3.3 deliberately rejects the old records and cannot by itself resume them; no migration is implemented here. Installing first could erase evidence and is not a recovery plan.
- Starting a new game: separate explicit approval deciding what to do about the unfinished run (without treating it as completed or silently abandoned); preserve all evidence; separately authorize any necessary install/reload with safeguards against session deletion; verify installed version, native MCP, four Skills and an actually new isolated framework cwd. A fresh missing fixed marker still needs positive initial-request provenance. One authorized new_game only after semantic storage checks. No new game is authorized by this report.
- Before either: external design review plus offline regressions, including the actual run-two bad JSON snapshots from the immutable review ZIP; test evidence is explicitly separated from LLM behavior. Actual Agent recovery and terminal behavior still require future authorization.

## V0.4 strategy experiment (current source; not yet run)

### Evidence and boundaries

The comparison uses the read-only evidence package `career-strategy-evidence.zip`, raw Game 1 and Game 3 score reports/events/transcripts, the prior Game 3 audit as a locator aid, and public `docs/rules.rst`, `docs/handbook.rst` and `docs/failure-and-ending.rst`. Game 1 is UUID `a86e8ff1b7924a598bc63422d52afd69` (B / 63.02); Game 3 is `e173ebcb61964fa58385148cc424e206` (A / 70.38). Both reached L5 through promotions at M6, M12, M24 and M42. Different event traces and one run per policy cannot establish that the V0.3.3 strategy caused the higher score.

Public rules give the local ending-score directions/weights used here (Level 30%, Wealth 20%) and public directional Energy effects. They do not publish promotion thresholds, tenure gates, numeric action deltas, or action-specific promotion probabilities. Accordingly, V0.4 uses early career-capital investment and evidence-targeted review preparation as hypotheses, not numerical optimization claims.

### V0.3.3 observations motivating the experiment

- Game 3 had B/no promotion at M18 (Skill31, Network18, Output9), B/no promotion at M30 (Skill56, Network31, Output24, with “do not look like you only hustle without winning”), and A/no promotion at M36 (Skill77, Network36, Output23, with “first on my list”). It promoted at M42 with A (Skill97, Network34, Output26). This shows those grades/feedback did not mechanically guarantee promotion; the decisive factor remains unknown.
- The Game 3 trace labels 27 report preparations, 13 key-project main actions, 9 Health recoveries and 4 Network-maintenance actions; no Skill-study label was found in the matched action names. This is observed usage, not proof that report preparation or project actions caused or harmed promotion. The game trace's Q5 Energy bundle is incomplete; the evidence CSV preserves it as unknown.
- Network declined from 7 to 4 after the M12 promotion in Game 3, then visibly reached 36 at M36 and 44 at the end. Health visibly recovered from a low of 3 to 10. Neither visible recovery establishes that hidden risks or organizational friction were cleared.
- Game 3 ended with Level L5, Wealth33.7, Risk Control10/10, Skill117, Network44 and Health/Dignity raw20. Game 1 ended L5, Wealth35.1, Risk Control1/10, Skill118, Network63 and Health/Dignity raw18. This motivates testing balance after early advancement; it does not establish causal trade-offs.

### V0.4 policy changes

Career Planning chooses one evidence-backed objective per period and compares currently offered main actions against the actual feedback: delivery/resource constraint, visibility, capability/scope, or relationship damage. M18, M30 and M36 become explicit diagnostic branches. A/S without promotion no longer supports automatic work intensification; an uninformative review remains unknown. A repeated key project or report is allowed when current evidence still favors it, without a quota either way. Earlier Level/Wealth and L5 by M36 are experiment targets; L6 is considered only through a real remaining review, no later than the observed final M48 review.

Resource Optimisation compares up to three materially different legal Energy proposals. In low-risk, tolerable-state quarters it must consider a relevant career-growth candidate when available, including Skill study or a delivery/visibility/relationship option. It compares the public costs and directions: Skill study (2E, Skill+, Health−), report preparation (1E, Output+, Dignity+), Network maintenance (1E, Network+, Dignity+), and intensive work (2E, Output+, Health−, Dignity−). It does not force study, report, or intensive work. Risk-mandated mitigation and relevant recovery remain protected; actual post-promotion Health/Network changes guide targeted restoration. After M48 review processing, it pivots from promotion preparation to current direct-score and survival needs.

No changes are made to Controller, Risk Management, the four-Skill architecture, native-MCP-only contract, checkpoint format, restoration path or terminal handling. Manifest changes only the displayed version name. No installed instance is modified.

### Falsifiable next-run hypotheses and measurements

1. **H-A — feedback-targeted main action:** after M30 “hustle without winning,” selecting the currently offered action that best supplies verifiable outcome evidence, leadership visibility or an explicitly named need increases M36 readiness/promotion versus repeating an unexamined project/report pattern. Measure selected main-action family, returned effects, M36 grade, promotion, manager feedback and pre-review state. No promotion formula is assumed.
2. **H-B — career-capital Energy:** in quarters without a severe risk constraint and with tolerable visible Health, a shortlist that considers Skill study/Network maintenance as well as reports produces more useful pre-review Skill or Network progress without a worse Health/risk-warning trajectory. Measure actual Energy actions/costs, state deltas at the next observation/review, warnings, Health, Network and promotion. A single observed delta is not isolated causality.
3. **H-C — post-promotion recovery:** when promotion feedback is followed by a visible Network or Health decline, targeted offered recovery restores the visible metric by the next review without recurring severe warnings. Measure the decline, selected response, metric path and warning sequence separately; visible recovery does not count as hidden-risk clearance.

These are hypotheses only. The next game has no paired-seed guarantee; differences in story events and model behavior remain confounders. V0.4 has no measured score, promotion, Token or risk-control improvement yet. Offline tests validate text/format and limited reference examples only, not Agent strategy execution.
