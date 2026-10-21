---
name: career-controller
description: Coordinate one Career Emulator session; read at entry, continuation or compression to restore session-isolated state, route specialist advice, execute one legal native MCP action and finish cleanly.
---

# Career Controller V0.5.1

## Scope and entry

One Agent applies all four Skills. Specialists supply advice, not Agents or executors. No delegation, Symphony, runtime router or Skill rewriting. Official IDENTITY supplies the basic loop; this Skill adds routing and recovery.

Use the native tools actually exposed under `mcp_career-emulator-engine_`: `show_employee_handbook()`, `new_game()`, `observe(session_id)`, `take_action(session_id, choice, notes)`, `check_latest_logs(session_id, count=10)`. Never replace them with Bash, scripts, subprocesses or direct database access. If native tools are missing, report the engineering failure and stop before creating a game.

Check the runner continuation, conversation and verified binding marker for an existing game; uncertainty never authorizes a new game. A framework conversation ID is never a game session_id. Only at a confirmed fresh start, pass the storage gate, read the handbook and call `new_game()` once. On `error` or missing non-empty `session_id`, stop without retry. Checkpoint a valid ID. The handbook may be reread; the game may not be recreated.

## Loading and reuse

- Unless already engineering-halted, read this Skill at entry and after any continuation, compression/handoff notice or missing control context, using `skill_tool(skill_name="career-controller")`.
- Apply relevant methods to each decision. Read missing/incomplete specialist bodies with `skill_tool(skill_name="...")`; otherwise reuse available bodies. No quarterly reload of all three is required.
- Recovery always requires verified framework scope, matching checkpoint if available, native observe and recent logs, regardless of pending status. Retain `events`. Reload risk-management for any status other than `resolved_explicit` or missing risk context; load other needed bodies. A name or saved loaded flag does not prove body retention.
- Multiple specialists can advise on one observation. Read bodies separately; no array-valued bulk call exists and Skill reads do not advance the game.

## Routing and arbitration

The Controller remains the only execution and final arbitration center. Apply priorities in this order:

1. **Hard constraints:** current-menu legality, session identity, terminal state, engineering and recovery fences, and explicit severe survival restrictions or `blocked_choices` supplied by Risk Management.
2. **Primary optimization:** sustainable long-term combined result, with priority to earlier promotion, higher Level/Wealth and the cumulative salary that follows.
3. **Marginal trade-offs:** compare Skill, Network, Health, Dignity, Output, Risk Control and efficiency from the current observation. Ordinary warnings are opportunity costs until Risk Management supplies an explicit restriction.

Risk Management remains the only risk judge. Career Planning supplies the main career objective and Main Action basis; Resource Optimisation compares Energy combinations. No specialist can execute an action or replace the Controller's safety and legality checks.

| Situation | Methods to apply |
| --- | --- |
| Monthly story | risk-management + career-planning: immediate benefit, delayed consequences, uncertainty |
| New/repeated warning or mitigation feedback | risk-management identifies restrictions/evidence; career-planning compares career value within those constraints |
| Quarterly Energy menu | risk-management -> career-planning -> resource-optimisation |
| Quarterly main action | career-planning + applicable Risk Management constraints; Resource Optimisation is not required unless an Energy opportunity cost is material |
| Approaching review or received review/promotion feedback | career-planning + risk-management; record feedback before revising targets |
| Continuation, compression or uncertain action | controller recovery; then relevant specialists |
| Terminal observation | controller only; settle and stop |

Identify the phase from the current event/menu and returned feedback, not just month modulo six. In one month several events and phases can occur. For each observation increment `observation_revision`, our local bookkeeping counter, not an official simulator field, action nonce or idempotency guarantee.

Advice shares that revision: Risk Management supplies constraints/evidence, Career Planning supplies the objective and Main Action comparison, and Resource Optimisation supplies at most three distinct Energy combinations. Resolve legality/session/terminal safety first, then explicit severe survival restrictions, then optimize earlier Level and Wealth while comparing other dimensions by current marginal value. `monitoring` is not `resolved_explicit`; `attention` and `elevated` warnings remain advisory unless Risk Management supplies evidence for a restriction. No voting, invented numerical reward, promotion formula or hidden threshold.

The `strategy.priority` value in the checkpoint example below is a historical structure example from the prior bundle, not a V0.5.1 target. Any V0.5.1-created or updated strategic objective should prioritize the long-term combined result, earlier promotion, Level and Wealth, while obeying explicit survival and legality constraints.

Use actual one-based choice IDs from the latest successful observation; recheck session, terminal flags, menu, budget and constraints. Only this Agent issues one final `take_action` at a time. Keep intent/event/result in memory. Non-empty notes can say `v033:r12 M9 report; risk=R1:monitoring; prepare review safely`; normally stay within 300 characters (our target, not an official limit). Tags/revisions are not idempotency keys, can recur after lost context and are not preserved in every phase. No ledger dump or lengthy reasoning.

## Minimal durable state

### Storage capability gate

Use only the framework-injected **Runtime Directory Context / Working Directory Policy** (or their Chinese equivalents), not a generic Workspace header, a Skill path or a user-supplied path. Let D be the complete current cwd copied from that trusted context. Require project directory to be explicitly unset and D's parent to equal `<Agent internal data directory>/projects`. D's final component must fully match `career-sim-runner-[0-9a-f]{12}` (ASCII lowercase hex). Validate this layout without extracting an ID to construct a filename. The WebSocket ID is not separately supplied in the task text. Any other layout, conflicting directory context, relative path, UNC path or `.`/`..` component -> engineering halt. Do not inspect config/runtime_state files or scan other directories. D is a source-backed single-conversation namespace, not a tool-enforced sandbox or an independently authenticated task token.

The existing run-two scope ending in `career-sim-runner-7a72e52cc135` and game `cc0ca28b4e694fd993c60b538aac3c80` are protected historical evidence: halt without file/game operations in that scope or for that game. V0.3.3 does not repair, migrate or resume them. Any reuse of a previously used/pre-V0.3.3 scope or evidence of an old marker/game requires separate operator review; absence of the new fixed marker does not authorize migration. Do not search for legacy filenames. Only an independently confirmed initial Runner request in a newly allocated framework conversation can qualify as fresh; a generic continuation, missing context or claimed fresh flag without that provenance cannot.

Use absolute file paths inside that verified cwd; no cross-task/reinstall persistence is promised. Inspect actual native tool schemas for `read_file(file_path=...)` and `write_file(file_path=..., content=...)`; missing tools/permissions -> halt before new_game. Native file writes may also create framework history; do not edit that history. This is a single-driver scheme, not an atomic lock for concurrent drivers or a defense against host path/symlink changes.

The sole V0.3.3 locator is the fixed absolute path `D/career-checkpoint.json`. It contains exactly: schema_version=2, solution_version=0.3.3, verified_directory=D, verified_path, game_session_id, phase and halted_reason. Do not persist `framework_session_id`: the complete trusted directory is the isolation binding, so there is no model-generated framework-ID pair to compare. `verified_directory` always means D, the directory; `verified_path` means the full absolute `D/career-state-<real-game-UUID>.json` path when bound, and null while reserved. Never use the marker path or directory as verified_path. Native file results supply data.file_path; read results supply data.content, which may have tool-added line-number display prefixes. Interpret the complete underlying JSON, excluding only those display prefixes, not string contents; a partial or unparseable read-back cannot pass. Do not compare an escaped display string instead of the parsed JSON value.

At a confirmed fresh entry, read only that fixed marker. Only an explicit not-found result permits reservation; access errors/ambiguous errors do not. An existing marker goes to validation/recovery, never to another new_game. Never overwrite an unrecognized file. Make one write and one read-back with game_session_id=null, verified_path=null, phase=reserved and halted_reason=null. File I/O success is not semantic validation: independently compare the returned absolute file path with trusted D plus the constant `career-checkpoint.json`, and the parsed verified_directory with the original injected D, not with another generated JSON field. Reject missing/extra/duplicate keys, wrong types/schema/version/phase, non-null reserved game/path or any path mismatch. Only this freshly written, semantically verified reservation within the same uninterrupted initial request permits the one new_game attempt. An existing reserved marker never does. Do not delete/reset markers yourself. No marker on a continuation is also not a fresh-start authorization.

Only the successful native new_game response supplies the initial real game `session_id` G; require a full `[0-9a-fA-F]{32}` UUID-hex match and no error. Error, timeout or invalid/missing ID -> halt with the reservation retained, no observe/take_action or second new_game. Derive P as D plus the constant `career-state-` plus that exact returned G plus `.json`. After success write/read-back the state at P, then update/read-back the owned fixed marker to phase=bound, game_session_id=G and verified_path=P. Validate actual returned paths against independently derived D/P, directory fields against original injected D, and all game IDs against the actual native response G. Matching two self-generated strings is insufficient. Complete both bindings before game actions. Binding metadata lives in `strategy.checkpoint`; there too verified_directory=D and verified_path=P. No framework-ID field, shortened ID or unknown ID is a substitute for G.

On recovery obtain D anew from the trusted injection, validate the fixed marker's exact path/schema/version/directory/phase and full state path, then read only the referenced state in D. A valid game ID in the current native tool history/Runner continuation must agree with marker and state; `unknown`, a framework ID or a conflicting UUID is not authority to select another game. Reserved, halted, malformed, incompatible or conflicting binding -> halt. Reject legacy framework_session_id fields rather than silently normalizing them. Missing marker or state on recovery -> halt, never treat it as a fresh game or an empty risk ledger. Do not enumerate state files, read another framework's marker or automatically reconstruct/migrate a missing checkpoint. Offline checks do not verify live file capability.

Our checkpoint example (placeholder strings are not game values):

```json
{
  "schema_version": 2,
  "solution_version": "0.3.3",
  "session_id": "<returned-session-id>",
  "observation_revision": 0,
  "time": {},
  "visible_state": {},
  "risks": [],
  "reviews": [],
  "quarter": {"key": null, "observed_energy": null, "confirmed_spend": [], "remaining_plan": [], "main_action_status": "unknown"},
  "strategy": {"priority": "survival, risk control, long-term Level and Wealth", "next_review": null, "hypotheses": [], "feedback_loop": null, "checkpoint": {"verified_directory": null, "verified_path": null, "reason": null, "halted_reason": null}},
  "action": {"status": "none", "observation_revision": null, "choice": null, "notes": null},
  "ending": null
}
```

- `time`/`visible_state`: actual observed fields; unknown stays unknown. A later snapshot is not exact pre-review state.
- `risks`: id, first_seen, last_seen, evidence, policy_urgency, mitigation_attempts, status, next_check. Retain unresolved issues and material changes; merge repeats. Urgency is our label, not hidden state.
- `reviews`: retain all eight possible observed reviews: month, known levels/grade/actual bonus, feedback and last-observed pre-review state; unavailable fields stay null.
- `quarter`: separate confirmed spending from tentative plans. Use returned evidence; Energy zero alone is not waste.
- `action.status`: none/pending/confirmed/rejected/uncertain/terminal. Ordinary changes stay in memory. Disk is a snapshot, not a write-ahead journal or proof of no later action. Old pending records must be reconciled, not resent.

### Write schedule

No per-action pending write is required. Ordinary successful actions use native results, concise notes and in-memory state, with zero extra file calls. Coalesce adjacent triggers with no game call between them; write one compact snapshot of necessary history, not the full transcript. Costs below are file-tool call budgets, not measured API Token/currency costs:

| Trigger | Why persist | Expected additional file operations |
| --- | --- | --- |
| Verified session binding | Bind the real game ID and its checkpoint to the framework locator | Four calls once: state write/read-back + owned marker update/read-back; pre-game absence read + probe write/read-back costs three more |
| New issue, worse/material risk evidence, confirmed mitigation or explicit resolution | Preserve consumable warning evidence and unresolved issues, including serious visible vulnerability even without an events warning | One write per material update; identical recurring evidence with no urgency/decision change stays in memory until the next checkpoint |
| Observed half-year review or promotion | Retain all eight review records, actual feedback and state changes | One write per observed batch; review and promotion together share one write |
| Material strategic switch | Persist the feedback hypothesis, changed allocation and next review check | One write only when objective/evidence/hypothesis materially changes; coalesce with review/risk updates, not every different choice |
| Timeout/transport ambiguity, substantive rejection or persistence failure | Record the uncertain/rejected action and block blind resend | One write if storage works; reconcile using native observe/logs; inability to write is reported, not retried in a loop |
| Reconciliation completed or genuine imminent handoff | Preserve recovered history or a known interruption boundary | At most one write when state changed/dirty; none for a clean ordinary observation |
| Terminal settlement | Preserve exact ending and remaining unresolved risks | One write if possible, then report ending and stop all game calls even if that write fails |

Save material `events` before another game call: observe consumes warnings; empty events do not clear risk. Deduplicate repeats, update last_seen in memory and flush at the next trigger. No full transcript, routine quarterly/revision-only writes or credentials.

Visible vulnerability is also evidence: first observing Network=0 or another published failure-direction boundary (for example Health=0, Dignity=0 or Wealth below zero) requires a compact risk entry and checkpoint before the next game call, even with empty events. Record actual value/month/revision and its source separately from a simulator warning. This is our conservative persistence trigger, not a hidden failure threshold or a numeric risk formula. Persist material worsening, meaningful mitigation/result or explicit resolution; repeated unchanged values alone do not require a write every observe. Do not auto-clear the entry when a value recovers; record that visible improvement without asserting hidden safety. For other deterioration use actual warnings, outcomes and risk-management evidence; do not invent universal numeric cutoffs.

If a required nonterminal checkpoint fails, do not submit the next action: preserve the ID and report the persistence error. Do not switch to a Bash client or start another game. If an uncertainty checkpoint itself was lost in a crash, the unconditional recovery fence below still applies; absence of a pending file is never permission to replay.

## Recovery and terminal handling

Only the real game ID from a verified native new_game result or its current-directory bound marker identifies the game. Runner continuation IDs must agree; never substitute the framework ID or `unknown`. Native observe confirms current state, not ownership by itself. Read only the file whose directory/path/game binding is independently verified, then check `schema_version`, `solution_version`, `session_id` and strategy.checkpoint directory/full path. Reject cross-session state, missing/malformed state and older versions; do not silently import, migrate or reconstruct them. If necessary risk/review history or session identity cannot be recovered sufficiently for safe continuation, report the gap and stop instead of guessing or creating another game.

On EVERY continuation first honor any latched engineering halt: it blocks further tool calls until explicit operator repair/authorization. Otherwise, for interruption or transport ambiguity, pause actions regardless of saved action status. Obtain native observe and `check_latest_logs(session_id, count=10)`; if necessary request count=30 once. These counts are our retrieval budget, not engine limits. Compare the latest event/menu/phase, time, changes, ordered action/outcome records and notes where available. If the last action is confirmed committed and the current phase is coherent, discard the old intent and decide only from the current observation. Never resend a cached choice. An unchanged visible state or missing log entry is not proof of non-execution: state saving and action-log append are separate source operations, and capped/hidden effects can leave visible stats unchanged. If ambiguous after bounded reconciliation, keep `uncertain` and stop; no exact-once guarantee is claimed.

Reconcile warnings first, reviews second, then budget and strategy. On explicit `success:false`, inspect the error and do not assume nothing changed after an unexpected engine error; substantive errors use the same recovery fence. Correct a rejected choice only after evidence establishes current progress and a fresh observation authorizes it. Logs supplement the menu; they never authorize old choice IDs.

After every success, including the final action, obtain native observe. On terminal state save ending if possible, report exact scores/grade/survival months and stop game calls/repeated completion messages. `ending_score.completed=true` can mean normal completion despite `failed=true` or month 49; do not invent played months/cutoffs. Bash DONE/JSON cannot replace native structured termination.

## Engineering halt across Runner continuations

On an engineering halt, retain the reason in current conversation/state and, only if storage still works and the current-version fixed marker was independently validated as ours, set its phase=halted and halted_reason with one best-effort write (read first if the file tool requires it). Never modify a conflicting, legacy or protected record to make it pass. Do not retry failed persistence in a loop. Once halted, generic Runner continuation prompts do not authorize recovery attempts, another new_game or action submission: report the same short blocker without repeating tool calls. Resume only after explicit operator repair and authorization; do not infer repair from a prompt saying continue. A genuine recoverable interruption without a prior engineering halt still uses the bounded reconciliation fence. Unknown execution never authorizes resending an old choice.

The Runner may keep sending continuations because a normal error report is not a structured terminal game event. A Skill cannot stop that driver, guarantee compliance after context/state loss, provide atomic execution or recover an unreturned game UUID. Directory equality and semantic checks here are model instructions, not independently enforced tool-boundary validators, transactions or locks. Fixed naming removes an unnecessary ID transformation; it does not guarantee LLM compliance or exclusive creation. Do not fake ending_score/DONE to escape; operator intervention is required. If all halt evidence is lost, an automatic continuation is still never a fresh-start authorization.
