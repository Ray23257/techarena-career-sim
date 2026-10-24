---
name: career-controller
description: Coordinate one Career Emulator session; read at entry, continuation or compression to restore session-isolated state, route specialist advice, execute one legal native MCP action and finish cleanly.
---

# Career Controller

## Scope and entry

One Agent coordinates all four Skills. Specialist Skills provide advice; the Controller integrates their recommendations and is the sole executor of game actions. Use the current game state, the registered native tools and the available Skill-loading capabilities. This Skill defines decision coordination and recovery without assuming undocumented framework components or external runtime services.

Use the native tools actually exposed under `mcp_career-emulator-engine_`: `show_employee_handbook()`, `new_game()`, `observe(session_id)`, `take_action(session_id, choice, notes)`, `check_latest_logs(session_id, count=10)`. Never replace them with Bash, scripts, subprocesses or direct database access. If native tools are missing, report the engineering failure and stop before creating a game.

Check the current conversation and native tool history for an existing game; uncertainty never authorizes a new game. A framework conversation ID is never a game `session_id`. Only at a confirmed fresh start, read the handbook and call `new_game()`. If the framework explicitly rejects the tool name or call shape before dispatch, correct that invocation and retry only after confirming native history shows no game was created. For a timeout, transport error, tool/game error after dispatch, missing `session_id`, or any ambiguous result, first reconcile available native call history and returned evidence. Do not retry while creation may have succeeded; if no usable session ID or no reliable confirmation is available, stop and request operator help. Keep a confirmed game ID in the current conversation.

## Loading and reuse

- Read this Skill at entry and after any continuation, compression/handoff notice or missing control context, using `skill_tool(skill_name="career-controller")`.
- Apply relevant methods to each decision. Read missing/incomplete specialist bodies with `skill_tool(skill_name="...")`; otherwise reuse available bodies. No quarterly reload of all three is required.
- Recovery uses the confirmed game session in the current conversation, native `observe` and recent logs, regardless of pending status. Retain `events`. Reload risk-management for any status other than `resolved_explicit` or missing risk context; load other needed bodies. A name or saved loaded flag does not prove body retention.
- Multiple specialists can advise on one observation. Read bodies separately; no array-valued bulk call exists and Skill reads do not advance the game.

## Routing and arbitration

All nonterminal decisions apply risk screening and career priorities; Energy decisions additionally apply resource comparison.

| Situation | Methods to apply |
| --- | --- |
| Monthly story | risk-management + career-planning: immediate benefit, delayed consequences, uncertainty |
| New/repeated warning or mitigation feedback | risk-management first; career-planning within its constraints |
| Quarterly Energy menu | risk-management -> career-planning -> resource-optimisation |
| Quarterly main action | risk-management + career-planning; resource-optimisation only if resource trade-offs remain relevant |
| Approaching review or received review/promotion feedback | career-planning + risk-management; record feedback before revising targets |
| Continuation, compression or uncertain action | controller recovery; then relevant specialists |
| Terminal observation | controller only; settle and stop |

Identify the phase from the current event/menu and returned feedback, not just month modulo six. In one month several events and phases can occur. For each observation increment `observation_revision`, our local bookkeeping counter, not an official simulator field, action nonce or idempotency guarantee.

Advice shares that revision: risk supplies constraints/evidence, planning an objective, resources at most three distinct candidates. Resolve legality/session/terminal safety first, then evidenced severe survival risk, risk control with long-term Level/Wealth, then other dimensions/efficiency. Minor warnings stay advisory unless evidence warrants restriction. No voting or invented numerical reward.

Use actual one-based choice IDs from the latest successful observation; recheck session, terminal flags, menu, budget and constraints. Only this Agent issues one final `take_action` at a time. Keep intent/event/result in memory. Keep non-empty notes concise and tied to the current visible decision; do not include historical run identifiers. There is no official note-length limit in the available evidence. Tags/revisions are not idempotency keys, can recur after lost context and are not preserved in every phase. No ledger dump or lengthy reasoning.

## Session continuity and working state

Use only the five native Career Emulator MCP tools named above for gameplay. Do not require a framework directory, local file tools, custom checkpoint files, project paths, database access or private Runner identifiers. Do not access a different game or infer a game ID from a framework conversation ID.

Keep a compact working summary in the current conversation: the exact game `session_id` returned by native `new_game`, latest confirmed time/state/menu/events, unresolved risk evidence, observed reviews and feedback, current strategy feedback, quarter Energy spending and the last action result. Distinguish returned facts from hypotheses; missing information stays unknown. This summary is decision context, not an independent simulator record.

At a confirmed fresh start, call `new_game()`. A framework-level rejection that explicitly proves the call was not dispatched may be corrected and retried only after confirming no game was created. A timeout, post-dispatch error, missing usable session ID or ambiguous result requires reconciliation first; never retry while creation may have succeeded. If creation cannot be confirmed with a usable session ID, take no game actions and ask for operator help. On continuation, use only the same confirmed game ID. If identity is missing or conflicting, make no game call and ask for operator help.

After context loss, reload this Skill and recover only from the current conversation and native observations/logs for the confirmed game. Preserve known risk and review evidence; never treat missing history as a clean risk state or invent a processed review. If required identity or safety-relevant history cannot be established, stop rather than guess.
## Recovery and terminal handling

On an interruption, context compression or transport ambiguity, pause actions and reconcile using native `observe(session_id)` and `check_latest_logs(session_id, count=10)` for the same confirmed game. Compare the latest time, event/menu/phase, returned changes and ordered action records where available. Missing log entries or unchanged visible stats do not prove non-execution. If the action is confirmed committed and the state is coherent, discard the old intent and decide again from the fresh observation. Never resend a cached choice; the same action may be selected anew only if it is currently legal and still best supported.

If the action result is explicitly unsuccessful, inspect the returned error and refresh the current state before deciding again. Do not assume an unexpected engine error had no side effects. If state or execution remains ambiguous after reconciliation, stop and report the uncertainty; do not replay the action or create another game.

After every successful action, including the final action, obtain native `observe`. On terminal state, report the exact returned ending score, grade and survival duration, then stop game calls. Interpret completion from the native terminal result; do not invent played months or cutoffs. Do not use shell output or locally fabricated JSON in place of native termination evidence.

Keep any engineering blocker in the current conversation. A later continuation does not authorize a new game or replay. Resume the same game only when its identity and current state are confirmed by native evidence. The Skill cannot guarantee model compliance, atomic execution or recovery of an unreturned game ID; do not claim otherwise or fake a terminal result.