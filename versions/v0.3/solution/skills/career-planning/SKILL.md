---
name: career-planning
description: Rank monthly and quarterly career choices for long-term Level and Wealth, plan ahead of six-month reviews, interpret actual performance/promotion feedback and balance skill, relationships and risk without invented promotion thresholds.
---

# Career Planning V0.3

## Input and output

Input: observation revision, current choices and visible state, remaining time, risk constraints, compact review/promotion history and current strategy. Apply to monthly stories and quarterly main actions; revisit after review, promotion, major financial change or meaningful feedback. Reuse the available body; reload it when needed after context loss.

Return advice to the same Agent: `observation_revision`, current objective, preferred current choice IDs, reasons, opportunity costs and unknowns. Do not execute tools or delegate. No future action list is binding.

## Goals grounded in evidence

The V0.2 local ending report gives Level 30%, Wealth 20%, Health/Dignity 15%, Skill 15%, Risk Control 10%, Network 10%. These are observed local settlement weights, not promotion weights, a complete future scoring formula or the cloud total. The public rules additionally describe engineering quality and resource efficiency in cloud evaluation. Do not invent S-grade cutoffs, hidden thresholds or action-to-score conversions.

Prioritize sustainable early advancement and accumulated Wealth, within survival constraints and an explicit risk-control improvement goal. Higher levels pay more monthly salary, so earlier promotion can improve remaining salary income; it does not guarantee a specific promotion opportunity. Do not sacrifice a serious survival constraint for a speculative level gain.

Skill, Output and Network have different scales. Never call one the promotion bottleneck just because its raw number is smallest, assume a score-normalized attribute is an in-game cap, or infer a promotion threshold from a single successful/failed review. Health and Dignity have public caps of 10; Skill/Network/Output do not acquire an in-game cap from this report.

## Six-month planning

1. Track observed review windows at months 6, 12, 18, 24, 30, 36, 42 and 48. Determine what has actually happened from native observations/results/logs. The handbook gives an approximate flow; V0.2 observed reviews before some same-month quarterly choices. Do not assume late actions can affect an already processed review.
2. Start preparing in the preceding months/quarter. Use explicit manager feedback, sustained results, capability, relationships and documented contributions. Do not rely on a last-month burst or on generic workplace intuition as proof of a game mechanism.
3. Retain one compact entry per observed review: month, last-observed pre-review state, level before/after, grade, actual bonus if returned and feedback. Do not fabricate unobserved exact review-time stats. Record missing promotion separately from a poor grade: V0.2 had an S review without promotion.
4. Use `duration_in_level` as observed context, not an eligibility threshold. After promotion, compare returned state for any actual changes rather than assuming a fixed reset formula. Reassess relationships and risk warnings as well as output.
5. If not promoted, form a limited hypothesis tied to feedback and alter the next period's useful allocation. Keep alternatives open. Do not repeatedly hammer Output because its number is smaller than Skill/Network; strong grades without promotion warrant uncertainty, not an invented cutoff.

## Wealth and story decisions

For each current option, separate immediate stated benefit/cost, plausible delayed commitments and unknown outcomes. Relate event wording to any active issue and remaining time. A title change in a story is not a confirmed Level change or salary raise until the environment returns it.

Distinguish salary, actual bonus and event income/loss when evidence provides them. Public grade bonus directions do not authorize treating their table entries as exact Wealth amounts; store returned amounts and leave unavailable breakdowns unknown. Do not knowingly guess unseen downstream rewards to justify an expensive or risky bet.

Prefer choices that build credible long-term capability/results and preserve working relationships when those benefits fit current needs. Visibility, key projects, mentorship, rotation and relationship repair are alternatives to compare, not a mandatory rotation or universal project-first rule. A locally high Skill/Network settlement score can reduce the immediate score benefit of more of that stat, but it does not establish promotion sufficiency.

## Remaining horizon

As time runs out, compare whether a delayed benefit can still arrive. After the final review has actually happened, do not justify extra Output by an imagined ninth promotion window. Compare current legal options on direct scored dimensions, risk, survival and confirmed financial effects. Do not assume short remaining time makes Health worthless or that a late risky project must pay off.

Keep the strategy summary compact: current priority, next not-yet-observed review, explicit feedback, unresolved hypotheses. Accept a reasonable trade-off when evidence supports it; an adverse random outcome alone is not proof the decision was wrong.
