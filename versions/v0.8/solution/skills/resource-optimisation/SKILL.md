---
name: resource-optimisation
description: Compare feasible quarterly Energy sequences and their marginal benefits against observed caps, risk constraints and career needs; load for the Energy phase or changed resource trade-offs, then reuse until context is missing.
---

# Resource Optimisation

## Input and output

Input: the latest native observation, current Energy menu and budget, visible state, confirmed spending, Risk Management's restrictions and Career Planning's current objective. Apply only in the Energy phase; reuse the Skill body while available and reload it when missing. Do not spend Energy during a story just because the month is divisible by three.

Return advice to the same Agent: the current objective, up to three materially different feasible combinations, known benefits/costs, uncertainty, the preferred first current choice ID and remaining budget. For each combination, state its offered choice IDs, total Energy cost and first choice. Every total must fit the observed budget. One or two combinations are enough. The Controller submits one Energy action per call; the quarter may contain more than one action. After every successful action, observe again and rebuild the comparison from the new menu and remaining budget.

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
6. **Choose and continue:** compare candidates using Risk Management's restrictions, the full supported benefit/cost bundle and remaining time. Do not use risk labels or raw attribute points as substitute scores. Before acting, confirm the current menu, events, Energy and risk advice; reuse the comparison only if they do not materially change the candidates' effects, costs or relevance. Once the best worthwhile legal action is selected, execute it without reopening the same comparison. After success, observe again and record changes before and after, without claiming causation when events or timing confound them. Refresh the menu, Energy and risk advice before the next choice. Before repeating an Energy action, use its latest comparable result. A missing gain in one stat does not erase other observed gains. If a recent comparable use showed a worthwhile observed benefit across its full bundle, and current conditions still make the benefit relevant while its costs remain acceptable, it may be repeated if it still compares well with the current alternatives and leaving Energy unused; no new evidence is required just to repeat a useful action. If the relevant return was absent or unclear, require a reason tied to its expected benefit before repeating. A routine Energy/menu change or “no better option” alone is not a reason to spend. A zero/unclear result does not prove permanent ineffectiveness; confounded results stay unknown. Stop when no offered action has a supported benefit worth its cost. Continue only while a legal, affordable and worthwhile action remains, then handle the independent Main Action. Never execute a cached sequence or stale choice ID.

Track only the observed time, returned Energy, confirmed action costs and a short current plan in the conversation. Reset the budget only when the environment shows a new quarter. If a returned change crosses a quarter boundary, do not mislabel the reset as spending or free Energy. Do not create a new state field or correct the environment's budget locally.

## Main action and stopping

Use career-planning and risk-management for the main-action menu. Do not assume the previous Energy choice determines which main action is best. Compare project, report, resource request, rotation, visibility, mentor, relationship repair, lie-low or none only when actually offered. Visible multi-stat gains are not automatically better than relevant risk reduction or relationship repair.

Once the final review is confirmed as settled, do not spend Energy preparing for another promotion. Compare only benefits that can still affect the ending state before terminal. The public ending dimensions do not list Output as a direct score component, so do not count Output alone as direct ending-score gain after the final review. Count other listed attribute gains separately when the menu supports them; judge a project by its actual offered effects, not its label. If final-review settlement is not confirmed, keep it unknown and do not infer it from the month. Energy reaching zero is normal if it purchased useful actions. Waste means avoidable harm, capped/useless benefit or missing a better evidenced alternative; it cannot be inferred from zero remaining Energy alone. Unspent Energy is allowed when remaining options are harmful, irrelevant or too uncertain. Do not spend simply to exhaust the budget.
