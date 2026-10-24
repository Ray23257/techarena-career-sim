---
name: career-controller
description: Coordinate one Career Emulator session; read at entry, continuation or compression to restore session-isolated state, route specialist advice, execute one legal native MCP action and finish cleanly.
---

# Career Controller

## Scope and entry

One Agent coordinates all four Skills. Specialist Skills provide advice; the Controller integrates their recommendations and is the sole executor of game actions. Use the current game state, the registered native tools and the available Skill-loading capabilities. This Skill defines decision coordination and recovery without assuming undocumented framework components or external runtime services.

For each turn, the Controller reads the latest observation, applies the relevant Skill advice, checks the session and legal choices, executes one native action, and observes its result. Risk Management supplies risk judgments; the Controller enforces applicable restrictions without creating a second risk system.

For gameplay, use only the five registered native identifiers shown in the current tool list: `mcp_career-emulator-engine_show_employee_handbook`, `mcp_career-emulator-engine_new_game`, `mcp_career-emulator-engine_observe`, `mcp_career-emulator-engine_take_action` and `mcp_career-emulator-engine_check_latest_logs`. Select each tool from the live registered tool list; treat its identifier as an opaque label. Never type, alter or rebuild an identifier from memory. Never replace native tools with Bash, scripts, subprocesses or direct database access. If a required registered tool is absent, report the engineering failure and stop before creating a game.

Check the current conversation and native tool history for an existing game; uncertainty never authorizes a new game. A framework conversation ID is never a game `session_id`. Only at a confirmed fresh start, read the handbook and call `new_game()`. If a call is explicitly rejected before dispatch because its tool identifier is unregistered, discard that identifier, refresh/select the exact registered entry from the live tool list, and reconcile native history for the same operation. If the rejection confirms no game was created, retry using the registered entry; repeat this recovery for each confirmed pre-dispatch rejection without a fixed retry-count limit. Never resend a rejected identifier. For a timeout, transport error, tool/game error after dispatch, missing `session_id`, or any ambiguous result, first reconcile available native call history and returned evidence. Do not retry while creation may have succeeded; if no usable session ID or no reliable confirmation is available, stop and request operator help. Keep a confirmed game ID in the current conversation.

## Loading and reuse

- Read this Skill at entry and after any continuation, compression/handoff notice or missing control context, using `skill_tool(skill_name="career-controller")`.
- Apply relevant methods to each decision. Read missing/incomplete specialist bodies with `skill_tool(skill_name="...")`; otherwise reuse available bodies. No quarterly reload of all three is required.
- At a fresh entry, read Career Planning, Risk Management and Resource Optimisation before the first game action. A Skill is ready only after its body is returned. Do not take a story, Energy or Main Action before the relevant specialist body is available. On later turns, reload only a needed body that is missing.
- Recovery uses the confirmed game session in the current conversation, native `observe` and recent logs, regardless of pending status. Retain `events` and risk evidence. A non-resolved risk status requires preserving and applying the existing risk advice; it does not by itself require rereading the Skill. Reload Risk Management only when its body or risk context is missing. A name or saved loaded flag does not prove body retention.
- Multiple specialists can advise on one observation. Read bodies separately; no array-valued bulk call exists and Skill reads do not advance the game.

## Routing and arbitration

All nonterminal decisions apply risk screening and career priorities; Energy decisions additionally apply resource comparison.

| Situation | Methods to apply |
| --- | --- |
| Monthly story | Controller reads the event and applies a quick Risk Management screen; use full Risk Management comparison when the event has a warning, links to recorded risk, or presents a material survival/irreversible-loss uncertainty. Use Career Planning when it affects a career/wealth choice |
| New/repeated warning or mitigation feedback | risk-management first; career-planning within its constraints |
| Quarterly Energy menu | risk-management + resource-optimisation; use Career Planning's current objective as context |
| Quarterly main action | risk-management + career-planning |
| Approaching review or received review/promotion feedback | career-planning + risk-management; record feedback before revising targets |
| Final review confirmed, Energy menu | risk-management + resource-optimisation; compare only benefits still reachable before the game ends |
| Final review confirmed, Main Action | risk-management + career-planning; compare only benefits still reachable before the game ends |
| Continuation, compression or uncertain action | controller recovery; then relevant specialists |
| Terminal observation | controller only; settle and stop |

Identify the phase from the current event/menu and returned feedback, not just the month. Treat the final review as settled only when the observation or returned feedback confirms it; the month alone is not proof. After that review, stop preparing for another promotion, but continue any legal actions that can still improve the ending state. Stop only on the actual terminal observation. Do not treat an internal revision label as new game evidence.

Advice shares the current observation: Risk Management supplies relevant risk evidence and restrictions, Career Planning supplies the objective for Main Actions and career-related stories, and Resource Optimisation supplies Energy candidates. The Controller integrates relevant advice, checks legality, chooses one action and is the sole executor. Resolve legality and session safety first. Apply Risk Management's restrictions for immediate failure or clearly evidenced major, hard-to-reverse loss. For ordinary risks, compare the specific evidence and plausible harm with the candidate action's supported benefits; a warning or score label alone is not an automatic veto. Minor warnings stay advisory unless evidence warrants restriction. Do not invent numerical rewards or repeat a full comparison when its relevant evidence has not changed.

Use actual one-based choice IDs from the latest successful observation; recheck session, terminal flags, menu, budget and constraints. Once the best legal action is selected, execute it without reopening the same comparison unless new evidence or a legality change gives a reason to reconsider. Only this Agent issues one `take_action` at a time. Keep intent/event/result in the current conversation. Keep action notes to one short sentence stating the current evidence and main trade-off; do not repeat the state, old history or private deliberation.

## Session continuity and working state

Use only the five native Career Emulator MCP tools named above for gameplay. Do not require a framework directory, local file tools, custom checkpoint files, project paths, database access or private Runner identifiers. Do not access a different game or infer a game ID from a framework conversation ID.

Keep a compact working summary in the current conversation: the exact game `session_id` returned by native `new_game`, latest confirmed time/state/menu/events, unresolved risk evidence, observed reviews and feedback, current strategy feedback, quarter Energy spending and the last action result. Distinguish returned facts from hypotheses; missing information stays unknown. This summary is decision context, not an independent simulator record.

At a confirmed fresh start, call `new_game()`. A framework-level rejection that explicitly proves the call was not dispatched may be corrected and retried only after confirming no game was created. A timeout, post-dispatch error, missing usable session ID or ambiguous result requires reconciliation first; never retry while creation may have succeeded. If creation cannot be confirmed with a usable session ID, take no game actions and ask for operator help. On continuation, use only the same confirmed game ID. If identity is missing or conflicting, make no game call and ask for operator help.

After context loss, reload this Skill and recover only from the current conversation and native observations/logs for the confirmed game. Preserve known risk and review evidence; never treat missing history as a clean risk state or invent a processed review. If required identity or safety-relevant history cannot be established, stop rather than guess.
## Recovery and terminal handling

On an interruption, context compression or transport ambiguity, pause actions and reconcile using native `observe(session_id)` and `check_latest_logs(session_id, count=10)` for the same confirmed game. Compare the latest time, event/menu/phase, returned changes and ordered action records where available. Missing log entries or unchanged visible stats do not prove non-execution. If the action is confirmed committed and the state is coherent, discard the old intent and decide again from the fresh observation. Never resend a cached choice; the same action may be selected anew only if it is currently legal and still best supported.

If a tool is explicitly rejected before dispatch as unregistered, discard that identifier and select the matching registered entry from the refreshed live tool list; never resend the rejected identifier. Reconcile the same confirmed session with `observe`, then make a fresh decision from the returned menu. Retry only when the rejection proves the operation was not dispatched, no action committed, the same session is confirmed, and the choice remains legal. If another rejection is also explicitly pre-dispatch, refresh the tool list and repeat the recovery; there is no fixed retry-count limit. Do not turn repeated pre-dispatch name errors into a terminal-game decision. For any post-dispatch error or uncertain result, inspect the error and reconcile before acting; if execution or session identity remains uncertain, stop and report rather than replaying or creating another game.

After every successful action, including the final action, obtain native `observe`. On terminal state, report the exact returned ending score, grade and survival duration, then stop game calls. Interpret completion from the native terminal result; do not invent played months or cutoffs. Do not use shell output or locally fabricated JSON in place of native termination evidence.

Keep any engineering blocker in the current conversation. A later continuation does not authorize a new game or replay. Resume the same game only when its identity and current state are confirmed by native evidence. The Skill cannot guarantee model compliance, atomic execution or recovery of an unreturned game ID; do not claim otherwise or fake a terminal result.
