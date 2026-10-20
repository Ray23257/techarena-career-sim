---
name: career-survival
description: Guide a JiuwenSwarm agent through the Career Emulator using public rules, current observations, and valid MCP choices.
---

# Career Survival

Complete one 48-month career by following the public rules and adapting to the latest game state. Use one JiuwenSwarm agent and this Skill only.

## Game loop

1. Before the game, call `show_employee_handbook()` once and read the published rules.
2. At game start, call `new_game()` exactly once. Check the response. If it contains an `error`, or lacks a non-empty `session_id`, stop this run and report the error or missing session. Do not retry indefinitely, claim success, or call `observe` or `take_action` without a valid `session_id`.
3. Before every action, call `observe(session_id)`. Read the latest month and phase, visible stats, current event, warning information in `events`, and all currently available choices. If the environment reports a terminal state, stop acting and report the returned ending score or rating exactly as provided.
4. Choose an action using the decision process below and only the latest observation. Do not follow a fixed action sequence.
5. Select only a one-based `choice` identifier from that observation. Call `take_action(session_id, choice, notes)` with a concise rationale in the required `notes` field. Submit one action at a time; never send conflicting actions in parallel.
6. Check the returned `success`. On success, observe again before deciding. On failure, read `error`, do not assume the action took effect, and obtain a fresh observation before any further action. Never retry blindly.
7. Call `check_latest_logs(session_id, count)` when recent history is needed to understand a change or warning. Use logs as evidence, then make the next decision from a fresh observation.

## Decision process

### 1. Protect the career from early failure

- Treat the published failure directions and explicit warnings as constraints. Health reaching zero ends the game immediately. Also monitor long-term low Dignity, Network remaining at zero too long, Wealth bottoming out for too long, Skill continually falling behind, repeated low performance, and signs of hidden organizational hazards.
- Respond to explicit warnings, sustained negative trends, and clearly relevant risks before pursuing optional gains. Hidden hazard values and exact danger boundaries are not observable or published; do not invent them. Use visible state, `events`, feedback, and logs to judge urgency.
- If an action's published or observed effects would worsen a serious current risk, prefer a safer available option when one exists. Do not assume an undocumented action is safe.

### 2. Pursue the published long-term priorities

- Once serious survival risks are controlled, favor choices that support Level (`Higher`) and Wealth (`High`). Health and Dignity together, and professional Skill, have `Medium` importance; risk control and coworker relationships have `Some weight`.
- Higher levels receive higher monthly salary in the published rules. Reaching a higher level earlier can therefore increase cumulative Wealth over the 48 months; this is an inference from the salary table, not a guaranteed promotion or score formula.
- Compare the actual current choices and observed effects. No action guarantees promotion or a particular score. Do not let one priority override a serious risk or mechanically choose the same type of action every turn.

### 3. Use the six-month review and promotion cadence

- A formal performance review and a promotion window occur every six months. Promotion considers Skill, Network, Output, and other factors; it reflects long-term results, and higher levels have a higher bar. Exact review and promotion formulas and thresholds are unknown.
- As each window approaches, use current stats, long-term trends, and explicit feedback to balance Output, Skill, Network, and survival. Do not assume one last-minute action determines the result.
- If the environment reports a performance grade or bonus change, treat it as evidence about the recent period. The published bonus directions are S +2, A +1, B 0, C -1, and D -2; the performance formula remains unknown.

### 4. Use quarterly resources deliberately

- Each quarter provides 3 Energy points, which do not carry over, and permits one main action or none. When the observation enters the quarterly action phase, review the currently available Energy actions and main actions.
- Prefer useful, relevant actions when their known benefits fit the current need. Avoid hoarding Energy without reason, but do not spend it merely to reach zero or accept a disproportionate health or survival risk. Stopping with Energy unused is acceptable when available actions are harmful, irrelevant, or too uncertain.
- Choose the main action separately from Energy spending, based on the current state, available choices, and observed feedback. Do not assume an action has an effect beyond its published description or returned result.

## Boundaries

- Do not call `new_game` again during an active game or discard the saved `session_id`.
- Do not create, delegate to, or orchestrate sub-agents. This version tests one agent and one Skill.
- Do not invent choices, action effects, hidden state, danger thresholds, numerical score weights, promotion thresholds, or a scoring formula. The local ending rating is S, A, B, C, D, or E; no grade cutoff is published. The cloud evaluation also considers strategy engineering quality and resource efficiency, so a local rating is not the complete contest result.
- If there is no valid choice, the environment returns an error, or the game ends, do not fabricate an action. Follow the returned state and the runner's completion instruction.
