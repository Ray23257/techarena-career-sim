# Skill Design: `career-survival`

## Purpose

Guide one JiuwenSwarm agent through one 48-month Career Emulator game. One Skill contains the observation loop, risk triage, long-term trade-offs, and tool-use constraints. It does not prescribe an action sequence because events and valid choices depend on the current state.

## Decision flow

1. Read the public employee handbook, create one game session, and retain its `session_id`.
2. Before every action, observe again. Use the current month and phase, visible stats, event and warning information in `events`, available choices, and any feedback already returned.
3. Apply survival constraints first. Health at zero ends the game; the other documented failure directions include long-term low Dignity, Network remaining at zero too long, Wealth bottoming out for too long, Skill continually falling behind, repeated low performance, and hidden organizational hazards. Watch visible trends and warnings, but do not invent hidden values or danger thresholds.
4. When risk is controlled, use the public score priorities as qualitative guidance: Level (`Higher`) and Wealth (`High`); Health/Dignity and Skill (`Medium`); risk control and coworker relationships (`Some weight`). The higher monthly salary at higher levels makes earlier advancement a plausible source of greater cumulative Wealth over 48 months; this is an inference from the salary table, not a guaranteed outcome.
5. Account for the public cadence. Every quarter provides 3 non-carrying Energy points and one main action or none. Use current options where useful and safe; do not spend just to exhaust the budget. Every six months a performance review and promotion window occur. Use longer-term Output, Skill, Network, survival trends, and explicit feedback; formulas and thresholds are not public.
6. Choose only the one-based `choice` in the latest observation and pass concise `notes`. Submit sequentially, inspect `success`, then observe again after success. On failure, read the error and do not assume state changed.
7. Use `check_latest_logs(session_id, count)` to clarify recent history, then return to a fresh observation before acting. Stop on a terminal state and report only the ending information the environment returns.

## Constraints

- Use the actual available choices and published or observed effects; do not assume an action guarantees promotion, performance, safety, or a score change.
- Do not invent numeric weights, promotion/performance formulas, danger thresholds, or hidden-state access.
- Keep the first version to one agent and one Skill; do not create or orchestrate sub-agents.
- Do not restart an active game, replace its `session_id`, or send conflicting actions in parallel.

## Why this shape

The two-stage policy separates early-failure prevention from the published final-score priorities. The quarterly and semi-annual cadence adds timing context without turning the Skill into a fixed playbook. This remains a strategy hypothesis until a full simulation is run; no score improvement has been demonstrated.
