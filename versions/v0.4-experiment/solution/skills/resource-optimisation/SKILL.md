---
name: resource-optimisation
description: "Compare up to three feasible quarterly Energy proposals for the current career phase, review objective and risk constraints; load for Energy decisions and replan after the first action."
---

# Resource Optimisation V0.4 Strategy Experiment

## Input and output

Input: observation revision, current Energy menu, observed Energy, visible state, confirmed spending, risk constraints and career objective. Apply in the Energy phase; reuse the body while available and reload when absent. Do not spend Energy during a story just because its month is divisible by three.

Return advice to the same Agent: `observation_revision`, at most three materially distinct feasible candidates, known benefits/costs, uncertainty, a preferred next current choice ID and remaining budget. One or two candidates are sufficient. This is a comparison method, not a Python router or independent executor. The controller chooses and executes once.

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

Do not enumerate or reason through all 112 full-menu sequences. That count is an offline exhaustive budget fixture, not a runtime task. Use this bounded screen instead:

1. **Menu legality:** keep only offered actions, their actual IDs and affordable public/stated costs. Repeats or stopping are possible only while offered. Do not invent a stop choice.
2. **Severe risk constraints:** remove avoidable risk-increasing choices prohibited by the risk advice. If relevant urgent mitigation needs 2 points, reserve those points in any accepted proposal before optional gains. Unknown effects alone are not proof of danger or safety.
3. **Cap clipping:** Health and Dignity cap at 10. Clip known marginal gains, and discard a recovery-only proposal whose only known gain is already capped unless it has a distinct evidenced purpose. Recovery after a known harmful first step can still matter: preserve order. Do not infer caps for Skill/Network/Output or numeric deltas for unknown effects.
4. **Construct at most three distinct proposals directly:** a protection/mitigation proposal when needed; one supporting the current career feedback objective; and, if useful, a balanced or materially different uncertainty trade-off. Each uses at most the observed remaining budget, normally a 2+1 or 1+1+1 pattern; do not expand a search tree. Deduplicate proposals and omit irrelevant slots instead of filling a quota.
5. **Prune obvious disadvantage:** discard a proposal only where known benefits are no better and known costs/risks no lower than a feasible alternative, with at least one strict disadvantage and no distinct material unknown benefit/risk. Unknown or incomparable effects are marked, not assigned invented scores. Two reports versus intensive work is a useful known-effect comparison from V0.2, not proof of permanent dominance or hidden safety. The three-candidate cap is our reasoning budget, not a globally optimal search guarantee.
6. **Choose and replan:** compare the remaining candidates using urgent protection, risk-control improvement, current Level/Wealth preparation and remaining horizon. Give one concise trade-off, not a numeric utility. Submit only the first current choice via the controller. After success and native observe, refresh effects, Energy, warnings and phase; rebuild a small shortlist if needed. No cached combination authorizes parallel calls or stale IDs.

## V0.4 career-phase comparison

This overlay tests earlier career-capital investment. It does not change the public three-point budget, tool rules or risk-management constraints. Route the current career objective from Career Planning into this shortlist; do not create a second objective. Do not force study, reporting or intensive work every quarter. Keep no more than three feasible Energy proposals.

In early and pre-review quarters, when Risk Management identifies no severe constraint and the observed state makes the known costs tolerable, ensure the candidates include a growth-oriented option when currently offered. Compare only materially different candidates relevant to the stated objective:

- **Capability:** Skill study costs 2E and publicly increases Skill while reducing Health; compare the Health cost against current Health, the actual warning/risk context, and the next review horizon.
- **Delivery/visibility:** Prepare a report costs 1E and publicly increases Output and Dignity. Intensive work costs 2E and publicly increases Output while reducing Health and Dignity. Compare intensive work only as an optional candidate when risk advice permits and the current state supports accepting those visible costs; never make it the default way to accelerate.
- **Relationships:** Network maintenance costs 1E and publicly increases Network and Dignity. Prefer it when a visible decline, promotion friction or relationship-focused feedback makes that need current; do not assume it repairs hidden risk by itself.
- **Protection/recovery:** Reserve any mitigation or recovery required by Risk Management before optional career gains. After a promotion or observed Health/Network deterioration, compare targeted recovery against growth actions using the fresh state. Keep the protection requirement even when it changes or removes the growth candidate.

Before an actual six-month review, use Career Planning's feedback-backed objective to choose among capability, delivery/visibility and relationship options. Do not infer that Skill is deficient because its raw number is lower than Output, or the reverse. After the review, compare returned grade, promotion, feedback and state with the preceding focus; then change the next shortlist only for observed reasons. Reports, study, maintenance and intensive work are substitutes with different public opportunity costs, not a fixed rotation.

After L5 is reached, prepare for L6 only while a real review remains and current Career Planning evidence supports it. At M48, wait for the final review result. Once it is processed, stop optimizing for promotion and compare the current legal candidates by direct remaining score dimensions, protection needs and confirmed immediate effects. Do not assume another level window, delayed payoff or salary increase beyond the observed horizon.

Evaluate any selected first step by its actual returned effect and fresh observation. The published rules give directions, not numeric deltas or action-specific promotion probabilities. Keep unknown outcomes incomparable; do not rank them by made-up expected values. The three-proposal limit and first-step replanning rule remain unchanged.

Track `quarter.key` using observed time, `observed_energy`, confirmed action costs and a short remaining plan. A new quarter resets the budget only when the environment shows it. Confirm cost from returned evidence; if a delta crosses a quarter/phase boundary do not mislabel the reset as spending or free Energy. Retain uncertainty instead of correcting the server's budget locally.

## Main action and stopping

Use career-planning and risk-management for the main-action menu. Do not assume the previous Energy choice determines which main action is best. Compare project, report, resource request, rotation, visibility, mentor, relationship repair, lie-low or none only when actually offered. Visible multi-stat gains are not automatically better than relevant risk reduction or relationship repair.

Energy reaching zero is normal if it purchased useful actions. Waste means avoidable harm, capped/useless benefit or missing a better evidenced alternative; it cannot be inferred from zero remaining Energy alone. Unspent Energy is allowed when remaining options are harmful, irrelevant or too uncertain. Do not spend simply to exhaust the budget.
