---
name: resource-optimisation
description: Compare feasible quarterly Energy sequences and their marginal benefits against observed caps, risk constraints and career needs; load for the Energy phase or changed resource trade-offs, then reuse until context is missing.
---

# Resource Optimisation V0.3

## Input and output

Input: observation revision, current Energy menu, observed Energy, visible state, confirmed spending, risk constraints and career objective. Apply in the Energy phase; reuse the body while available and reload when absent. Do not spend Energy during a story just because its month is divisible by three.

Return advice to the same Agent: `observation_revision`, feasible candidate sequences, known benefits/costs, uncertainty, a preferred next current choice ID and remaining budget. This is a comparison method, not a Python router or independent executor. The controller chooses and executes once.

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

## Deterministic comparison procedure

1. Read the current remaining Energy, costs and options. Enumerate feasible sequences within that budget, including repeats and stopping, only where the menu/rules support them. If none is useful and safe, stopping is acceptable when offered. Do not invent a stop choice.
2. Apply risk constraints first. When relevant urgent mitigation needs 2 points, keep a feasible mitigation sequence rather than spending those points on optional gains. Reassess after actual feedback; do not force one identical allocation every quarter.
3. Compare actual marginal effects after public caps: Health and Dignity cap at 10. Recovery at the cap offers no known immediate increase, but later recovery in a sequence may help after a cost. Do not invent caps for Skill/Network/Output or calculate numeric gains from an unknown description.
4. Prefer candidates with useful known benefits at no worse known cost/risk when comparable. Keep unknown effects explicitly unknown. Two report actions versus intensive work is a useful comparison using the V0.2 observed effects, not proof of permanent dominance or hidden safety. Do not invent a scalar utility or promotion probability to rank unlike benefits.
5. Among remaining candidates, compare urgent protection, risk-control improvement, preparation for a not-yet-processed review, sustainable development and remaining-horizon benefits. Give a short reason for the opportunity cost of each scarce point.
6. Submit only the next action through the controller. After success and a fresh observation, reconcile returned Energy and effects, then revalidate the plan. A tentative combination is never permission to execute cached IDs or send parallel actions.

Track `quarter.key` using observed time, `observed_energy`, confirmed action costs and a short remaining plan. A new quarter resets the budget only when the environment shows it. Confirm cost from returned evidence; if a delta crosses a quarter/phase boundary do not mislabel the reset as spending or free Energy. Retain uncertainty instead of correcting the server's budget locally.

## Main action and stopping

Use career-planning and risk-management for the main-action menu. Do not assume the previous Energy choice determines which main action is best. Compare project, report, resource request, rotation, visibility, mentor, relationship repair, lie-low or none only when actually offered. Visible multi-stat gains are not automatically better than relevant risk reduction or relationship repair.

Energy reaching zero is normal if it purchased useful actions. Waste means avoidable harm, capped/useless benefit or missing a better evidenced alternative; it cannot be inferred from zero remaining Energy alone. Unspent Energy is allowed when remaining options are harmful, irrelevant or too uncertain. Do not spend simply to exhaust the budget.
