---
name: career-planning
description: Rank monthly and quarterly career choices for long-term Level and Wealth, plan ahead of six-month reviews, interpret actual performance/promotion feedback and balance skill, relationships and risk without invented promotion thresholds.
---

# Career Planning

## Input and output

Input: observation revision, current choices and visible state, remaining time, risk constraints, compact review/promotion history and current strategy. Apply to monthly stories and quarterly main actions; revisit after review, promotion, major financial change or meaningful feedback. Reuse the available body; reload it when needed after context loss.

Return advice to the same Agent: `observation_revision`, current objective, preferred current choice IDs, reasons, opportunity costs and unknowns. Do not execute tools or delegate. No future action list is binding.

## Goals grounded in evidence

Public rules identify Level, Wealth, wellbeing, skills, risk control and coworker relationships as relevant outcomes. Local development reports do not establish official cloud weights, promotion thresholds or a complete scoring formula. Do not invent S-grade cutoffs, hidden thresholds or action-to-score conversions.

Prioritize sustainable early advancement and accumulated Wealth, within survival constraints and an explicit risk-control improvement goal. Higher levels pay more monthly salary, so earlier promotion can improve remaining salary income; it does not guarantee a specific promotion opportunity. Do not sacrifice a serious survival constraint for a speculative level gain.

Skill, Output and Network have different scales. Never call one the promotion bottleneck just because its raw number is smallest, infer a promotion threshold from one review, or infer an in-game attribute cap from a score-normalization scale. Health and Dignity have public caps of 10. Do not assume a cap for Skill, Network or Output unless game rules or observed effects explicitly establish one.

## Six-month feedback loop

Track windows at months 6, 12, 18, 24, 30, 36, 42 and 48; establish actual processing from native results/logs. The handbook flow is approximate. Do not assume late actions can affect an already processed review. Start preparing in earlier months; keep `duration_in_level` as observed context, not an eligibility threshold.

After each observed review/promotion, perform one compact update:

1. **Record facts:** grade, actual bonus, level change, explicit feedback and the last-observed pre-review state. Missing exact review-time stats remain unknown. Grade and advancement are separate observations; record both independently.
2. **Compare with the preceding period:** within-stat direction, actual financial inflows/losses if known, new risks, main-action families used and whether prior feedback changed. Never compare raw Skill/Output/Network magnitudes as eligibility. More Output without promotion does not prove Output is irrelevant or the only missing input.
3. **Choose a branch below**, then name one actionable working hypothesis, its evidence, the allocation change (or justified continuation), and the next review/feedback check. Keep supported priorities already working; do not change everything at once.
4. **Use the next quarterly main menu** to compare a small number of relevant offered actions, apply risk constraints, and choose one. Follow up on returned effects after success. A planned action is not a cached choice ID.
5. **At the next feedback:** retain, revise or mark the hypothesis unconfirmed. Improvements coinciding with an action are observations, not isolated causal proof; record major story/risk changes that confound the comparison.

| Observed condition | Next-period allocation rule |
| --- | --- |
| Severe unresolved risk, regardless of grade | Address relevant risk/relationship/survival needs first; keep safe productive options. Do not buy speculative promotion with additional stated risk. |
| Promotion actually occurred | Compare returned state for changed relationships, Output and warnings; stabilise any observed deterioration, then prepare for the next window. Retain low-performance feedback if the grade was poor. Do not assume a fixed reset formula. |
| C/D, or explicit concern about weak results | If feedback concerns delivery, compare a feasible key project/resource request with the current alternatives. If it concerns presenting/documenting existing work, compare leadership reporting/publicizing with more work. If capability or relationships are explicitly implicated, compare the corresponding support actions below. Unknown cause -> keep a safe useful baseline and test one feedback-relevant change, not an invented formula. |
| A/S but no promotion | Do not automatically intensify work. If feedback asks for materials/recognition, compare leadership reporting. If concrete relationship damage or skill/scope feedback exists, compare repair/mentor/rotation respectively. Keep healthy delivery while testing that one hypothesis. No evidence of a different need -> continuing a key project can be reasonable, with uncertainty recorded. |
| B/unclear feedback, no promotion | Maintain sustainable results; select a relevant change only when state/feedback supports it. Do not treat a neutral review as proof of a known bottleneck. |
| Same Level through successive observed windows | Audit prior hypotheses, actual feedback and risks; avoid escalating the same unconfirmed remedy. Prefer a different evidence-backed intervention when available. Long tenure triggers reassessment, not a hidden tenure threshold, forced rotation or guaranteed promotion. |

Maintain one compact `strategy.feedback_loop` summary in the current conversation with the review facts, preceding focus, evidence, working hypothesis, next focus, main-action family and next check. Later minor wording changes can stay in memory. Keep confirmed review facts; retain only current/previous intervention details needed to assess the plan.

## Compare the actual main actions

Use only current descriptions and observed effects; these are candidate-selection hypotheses, not guarantees. Compare up to three relevant offered candidates, keeping serious risk constraints and remaining time explicit:

| Offered action | Evidence that makes it relevant | What must not be assumed |
| --- | --- | --- |
| Key project | Specific delivery/results feedback, or useful observed multi-stat gains without a stronger evidenced need | That three visible gains always beat alternatives or the project guarantees promotion |
| Report results to leadership / publicize results | Existing work plus explicit recognition/materials feedback, or useful stated Output/Network/Dignity effects | An invisible promotion multiplier or promised salary increase |
| Mentor relationship | Explicit capability/development need, or useful stated Skill/Network gains | A hidden sponsorship bonus or known eligibility threshold |
| Job rotation | Concrete scope/skill-development feedback and a relevant current description | Automatic advancement, risk removal or a guaranteed new storyline |
| Repair key relationship | Observed relationship loss, explicit friction or a relevant unresolved issue | That Network alone measures all organizational risk, or repair clears all hazards |
| Push for resources | Explicit delivery/resource constraint and fitting current benefits | An unstated project-success probability or free gain |
| Lie low / no action | Serious current risk, health recovery relevance, or no useful safe offered alternative | That the label alone guarantees hidden risk reduction |

Key projects can be repeated when current evidence still favors them; repetition alone does not prove error. Compare each repeat with relevant current alternatives and explain the opportunity cost; do not force a rotation quota. Reports, mentoring and projects are alternatives to compare, not evidence that one would have caused advancement in another run.

## Wealth and story decisions

For each current option, separate immediate stated benefit/cost, plausible delayed commitments and unknown outcomes. Relate event wording to any active issue and remaining time. A title change in a story is not a confirmed Level change or salary raise until the environment returns it.

Distinguish salary, actual bonus and event income/loss when evidence provides them. Public grade bonus directions do not authorize treating their table entries as exact Wealth amounts; store returned amounts and leave unavailable breakdowns unknown. Do not knowingly guess unseen downstream rewards to justify an expensive or risky bet.

Prefer choices that build credible long-term capability/results and preserve working relationships when those benefits fit current needs. Visibility, key projects, mentorship, rotation and relationship repair are alternatives to compare, not a mandatory rotation or universal project-first rule. A high Skill or Network value does not establish promotion sufficiency or make further gains automatically worthless; compare current evidence, menu effects and opportunity cost.

## Remaining horizon

As time runs out, compare whether a delayed benefit can still arrive. After the final review has actually happened, do not justify extra Output by an imagined ninth promotion window. Compare current legal options on direct scored dimensions, risk, survival and confirmed financial effects. Do not assume short remaining time makes Health worthless or that a late risky project must pay off.

Keep the strategy summary compact: current priority, next not-yet-observed review, explicit feedback, unresolved hypotheses. Accept a reasonable trade-off when evidence supports it; an adverse random outcome alone is not proof the decision was wrong.
