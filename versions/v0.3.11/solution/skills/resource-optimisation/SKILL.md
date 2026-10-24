---
name: resource-optimisation
description: Compare feasible quarterly Energy sequences and their marginal benefits against observed caps, risk constraints and career needs; load for the Energy phase or changed resource trade-offs, then reuse until context is missing.
---

# Resource Optimisation

## Input and output

Input: observation revision, current Energy menu, observed Energy, visible state, confirmed spending, risk constraints and career objective. Apply in the Energy phase; reuse the body while available and reload when absent. Do not spend Energy during a story just because its month is divisible by three.

Return advice to the same Agent: `observation_revision`, at most three materially distinct feasible candidates, known benefits/costs, uncertainty, a preferred next current choice ID and remaining budget. One or two candidates are sufficient. The controller submits one Energy action per tool call; this is not a one-action-per-quarter limit. After each successful action, observe again and replan. The same quarter may include further currently legal, affordable and worthwhile Energy actions.

## Public budget

Each quarter supplies 3 Energy, unused points do not carry over, and repeat Energy actions are allowed while offered. Costs in the public rules:

| Category | Energy cost |
| --- | --- |
| Intensive work | 2 |
| Skill study | 2 |
| Network maintenance | 1 |
| Defuse past landmines | 2 |
| Mental recovery | 1 |
| Health recovery | 1 |
| Prepare a report | 1 |

Match categories to actual current descriptions; never copy a remembered choice number. Menu changes and insufficient Energy can remove options. The quarterly main action is a separate phase: at most one offered main action or a legal no-action option, not another Energy purchase.

## Bounded candidate procedure

Use this bounded screen instead:

1. **Menu legality:** keep only offered actions, their actual IDs and affordable public/stated costs. Repeats or stopping are possible only while offered. Do not invent a stop choice.
2. **Severe risk constraints:** remove avoidable risk-increasing choices prohibited by the risk advice. If relevant urgent mitigation needs 2 points, reserve those points in any accepted proposal before optional gains. Unknown effects alone are not proof of danger or safety.
3. **Cap clipping:** Health and Dignity cap at 10. Clip known marginal gains, and discard a recovery-only proposal whose only known gain is already capped unless it has a distinct evidenced purpose. Recovery after a known harmful first step can still matter: preserve order. Do not infer caps for Skill/Network/Output or numeric deltas for unknown effects.
4. **Construct at most three distinct proposals directly:** a protection/mitigation proposal when needed; one supporting the current career feedback objective; and, if useful, a balanced or materially different uncertainty trade-off. Each uses at most the observed remaining budget, normally a 2+1 or 1+1+1 pattern; do not expand a search tree. Deduplicate proposals and omit irrelevant slots instead of filling a quota.
5. **Prune obvious disadvantage:** discard a proposal only where known benefits are no better and known costs/risks no lower than a feasible alternative, with at least one strict disadvantage and no distinct material unknown benefit/risk. Unknown or incomparable effects are marked, not assigned invented scores. Compare reports and intensive work only using costs and effects explicitly available in the current menu or observed results; do not infer permanent dominance or hidden safety. The three-candidate cap is our reasoning budget, not a globally optimal search guarantee.
6. **Choose and replan:** compare the remaining candidates using urgent protection, risk-control improvement, current Level/Wealth preparation and remaining horizon. Give one concise trade-off, not a numeric utility. Submit exactly one current Energy action per tool call through the controller. This limits each call, not the quarter: after success, observe again, refresh effects, Energy, warnings and phase, then choose another currently legal, affordable and worthwhile Energy action if one remains. Continue until the Energy phase closes or no such action is worthwhile; then handle the independent Main Action. No cached combination authorizes parallel calls, consecutive unobserved actions or stale IDs.

Track `quarter.key` using observed time, `observed_energy`, confirmed action costs and a short remaining plan. A new quarter resets the budget only when the environment shows it. Confirm cost from returned evidence; if a delta crosses a quarter/phase boundary do not mislabel the reset as spending or free Energy. Retain uncertainty instead of correcting the server's budget locally.

## Main action and stopping

Use career-planning and risk-management for the main-action menu. Do not assume the previous Energy choice determines which main action is best. Compare project, report, resource request, rotation, visibility, mentor, relationship repair, lie-low or none only when actually offered. Visible multi-stat gains are not automatically better than relevant risk reduction or relationship repair.

Energy reaching zero is normal if it purchased useful actions. Waste means avoidable harm, capped/useless benefit or missing a better evidenced alternative; it cannot be inferred from zero remaining Energy alone. Unspent Energy is allowed when remaining options are harmful, irrelevant or too uncertain. Do not spend simply to exhaust the budget.
