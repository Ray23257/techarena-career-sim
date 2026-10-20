---
name: career-controller
description: Coordinate one Career Emulator session; read at entry, continuation or compression to restore session-isolated state, route specialist advice, execute one legal native MCP action and finish cleanly.
---

# Career Controller V0.3

## Scope and entry

You are the same single Agent throughout. Specialist Skills supply methods, not separate Agents or tool executors. Do not delegate, enable Symphony, write a runtime router or rewrite Skills. The official IDENTITY supplies the basic observe/action loop; this Skill adds routing, evidence retention and recovery.

Use the native tools actually exposed under `mcp_career-emulator-engine_`: `show_employee_handbook()`, `new_game()`, `observe(session_id)`, `take_action(session_id, choice, notes)`, `check_latest_logs(session_id, count=10)`. Never replace them with Bash, scripts, subprocesses or direct database access. If native tools are missing, report the engineering failure and stop before creating a game.

First determine whether a session already exists from the runner continuation, current conversation and this task's saved state. A possible existing session is not permission to start over. Only at a confirmed fresh start: read the employee handbook, call `new_game()` once, reject any `error` or missing non-empty `session_id`, and checkpoint the returned ID. On failure stop without retry. Handbook content may be read again when missing; creating a game may not.

## Loading and reuse

- Read this Skill at entry and after any continuation, compression/handoff notice or missing control context, using `skill_tool(skill_name="career-controller")`.
- Apply relevant specialist methods to every decision. Read a specialist with `skill_tool(skill_name="...")` only when its body is absent, incomplete, contradictory or needs recovery; otherwise reuse its available body. No quarterly reload of all three is required.
- On recovery read the state file first, obtain a native observation, and immediately retain its `events`. Reload `risk-management` if any risk has status other than `resolved_explicit` (including `monitoring` and `mitigation_pending`), or risk context is missing. Reload other specialists needed for the current phase. Do not treat a remembered Skill name or a saved "loaded" flag as proof its body is in context.
- Multiple specialists may advise on one observation. Read missing bodies separately; there is no array-valued bulk Skill call. Their advice does not advance the game.

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

Specialist advice refers to that revision: risk returns blocked/preferred choices and evidence; planning returns objectives and preferred choices; resources returns feasible candidate sequences and a next choice. Resolve in order: legal/session/terminal constraints; evidenced severe survival risk; risk-control improvement and long-term Level/Wealth; other scored dimensions, efficiency and uncertainty. Low-level warnings are advisory unless evidence warrants stronger constraints. Do not average conflicting recommendations or invent a common numerical reward.

Use only the latest successful observation's actual one-based choice IDs. Before execution check the session, terminal flags, current menu, budget and applicable constraints again. Only this Agent issues one final `take_action` at a time, with a short explanation such as `v03:r12 risk=R1:pending; prepare review without adding stated risk`. Notes must be non-empty; keep them normally within 300 characters, a local brevity target, not an official limit. Do not copy the handbook, entire ledger or lengthy reasoning into notes.

## Minimal durable state

Use native file tools to keep one compact UTF-8 JSON file named `career-state-<session_id>.json` directly in this task's assigned working directory. Resolve the actual working directory from runtime context; do not hardcode a host path, use the old run's directory, scan unrelated sessions or overwrite another session's file. Use the exact returned UUID-hex session ID; if its filename safety or the working directory is unclear, report the problem instead of guessing a path. File tools are for bookkeeping, never game execution.

The JSON is our record, not additional simulator state. Minimal shape (angle-bracket strings are explanatory, not game values):

```json
{
  "schema_version": 1,
  "solution_version": "0.3",
  "session_id": "<returned-session-id>",
  "observation_revision": 0,
  "time": {},
  "visible_state": {},
  "risks": [],
  "reviews": [],
  "quarter": {"key": null, "observed_energy": null, "confirmed_spend": [], "remaining_plan": [], "main_action_status": "unknown"},
  "strategy": {"priority": "survival, risk control, long-term Level and Wealth", "next_review": null, "hypotheses": []},
  "action": {"status": "none", "observation_revision": null, "choice": null, "notes": null},
  "ending": null
}
```

- `time` and `visible_state`: copy the latest observed time and status fields, preserving official field names. Unknown values remain unknown. Do not label a later snapshot as the exact pre-review state.
- `risks`: each entry has `id`, `first_seen`, `last_seen`, `evidence`, `policy_urgency`, `mitigation_attempts`, `status`, `next_check`. Retain every unresolved risk; merge duplicate warnings while retaining first/latest evidence and material changes. Policy urgency is our label, never a hidden risk value.
- `reviews`: retain one compact entry per observed six-month review, with month, level before/after if observed, grade, actual bonus if returned, feedback and last-observed pre-review snapshot. Missing fields stay null. Do not invent missed-window details. Keep all eight possible review entries.
- `quarter`: store confirmed spending separately from a tentative plan. Compute spending only from returned evidence; Energy zero is not by itself waste. Review plans after each action.
- `action.status`: `none`, `pending`, `confirmed`, `rejected`, `uncertain` or `terminal`. `pending` records intent, not proof of execution.

### Write schedule

Checkpoint after session binding; new/materially changed risk evidence; observed review/promotion; execution uncertainty/error; and terminal settlement. Before every `take_action`, save a compact pending intent plus necessary history. Coalesce adjacent checkpoint reasons when no game call intervenes. Ordinary `observe` replies update memory, not automatically the file; do not read the file again on every turn. After confirmed success update memory and carry that confirmation into the next checkpoint/pending write; an extra file write solely to clear each pending intent is unnecessary. A stale pending record after interruption must be reconciled, not resent.

Immediately retain new `events` evidence before any later observation: observe consumes pending warnings, so empty events do not clear historical risk. Do not store the full transcript/menu on every turn. Keep compact review history, unresolved risks and only effect evidence needed for current decisions. Before a handoff, save the latest compact record if possible. Never store credentials.

If a required checkpoint cannot be saved, do not submit the next action: preserve the ID and report the persistence error. Do not switch to a Bash client or start another game. Do not claim write/read recovery has passed until file-tool execution has actually been observed.

## Recovery and terminal handling

The runner-provided/current session ID and the server's observation are authoritative. Read only its matching state file and check `schema_version`, `solution_version` and `session_id`. Reject cross-session state. If missing or malformed, rebuild only what native observation and bounded recent logs support; mark older history unknown and unresolved recovered warnings as such. If no session ID can be recovered, stop rather than create another game.

After any continuation, stale pending record or uncertain transport result, observe and use bounded `check_latest_logs` to reconcile the choice/notes and result. Reconcile warnings first, reviews second, then budget and strategy. If execution cannot be established, keep `uncertain` and stop for an engineering report; never blindly resend. On explicit `success:false`, inspect the error, do not claim the action happened, checkpoint rejection and obtain a fresh observation before a corrected choice. Logs supplement the latest menu; they do not authorize old choice IDs.

After each successful action obtain the next native observation, including after the final action. On terminal observation do not submit an action. Persist the returned ending information, report exact available scores/grade/survival months, then stop game calls and repeated completion messages. `ending_score.completed=true` distinguishes completed settlement from early failure even if terminal flags contain `failed=true` or current_month is 49. Do not infer 49 played months or invent a grade cutoff. Native structured termination is required: printing DONE/JSON through Bash is not a replacement.
