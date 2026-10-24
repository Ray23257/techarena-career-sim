---
name: career-planning
description: Use when choosing a Career Sim story response or quarterly Main Action, interpreting review feedback, or comparing career and Wealth trade-offs.
---

# Career Planning

## Input and output

Input: the full latest native observation, especially `events`, current choices, visible state, remaining time, risk advice, confirmed review history and the current `strategy.feedback_loop`. Apply to career/wealth story choices and quarterly Main Actions; revisit after actual feedback, promotion or a material financial change. Reuse the available Skill body; reload it when missing after context loss.

Return advice to the same Agent: current objective, preferred legal choice IDs, concise reasons, best alternative, opportunity cost and unknowns. When promotion reasoning affects the recommendation, include one brief `Review evidence` note: the explicit rule/feedback supporting the diagnosis, or `specific bottleneck unknown`. This is advice, not a new state field. Do not execute tools or delegate. No future action list is binding.

## Goals grounded in evidence

Public ending guidance ranks Level as Higher, Wealth as High, physical/mental wellbeing and professional skill as Medium, and risk control and coworker relationships as Some weight. Use that published hierarchy to guide attention: Level and Wealth deserve greater strategic priority, while the other outcomes still matter. These are qualitative labels, not exact percentages. Local development reports do not establish official cloud weights, promotion thresholds or a complete scoring formula. Do not invent S-grade cutoffs, hidden thresholds or action-to-score conversions.

Optimize the final competition score, not any single state value. Give Level and Wealth greater strategic attention in line with the published qualitative importance, but compare candidate actions by their supported effects rather than by the names of the stats they mention. Level, Wealth, wellbeing, Skill, Risk Control and Network are distinct outcomes; their raw attribute points cannot be compared directly. Exact official cloud weights are unpublished, and local report percentages are not guaranteed to carry over. For each action, compare verified direct effects and any supported implications for survival, promotion, future pay and remaining time. Keep unverified benefits unknown. Earlier promotion may increase future salary only when current rules or returned state support that implication. Apply Risk Management's evidence-based limits against early failure and clearly evidenced major, hard-to-reverse loss; do not treat ordinary risk as an automatic veto.

Skill, Output and Network have different scales. A rule that lists one as relevant to promotion establishes relevance, not a current shortfall. Name a specific bottleneck only when current feedback or an explicit rule identifies it; otherwise mark it unconfirmed. Never infer it from cross-stat raw-number comparisons or one review. Health and Dignity have public caps of 10. Do not assume a cap for Skill, Network or Output unless game rules or observed effects explicitly establish one.

## Six-month feedback loop

Read the complete current observation, including review messages inside `events`. Extract only returned performance, promotion, pay/bonus and manager feedback. A review is processed only when current or safely recovered native evidence confirms it; do not mark one processed from the month alone. If existing review fields are supplied, preserve their names and enum values. Do not add a field, ledger or Controller interface. If no confirmed result or recoverable target exists, keep the target unknown and compare current legal choices using known direct effects.

The known review calendar is M6, M12, M18, M24, M30, M36, M42 and M48, but the calendar predicts an opportunity, not that its result was received. Review settlement happens before same-month Energy/Main Action; those later actions cannot explain that review. After the M48 review is explicitly settled, use `terminal_processed` only if that existing field is available, stop planning for another promotion and compare remaining actions for ending value.

Use an available `evidence_focus` as a diagnostic question, not an action filter. A legal action with stronger direct or broader value can take priority after comparing the current evidence and opportunity cost. If `review_phase`, `target_review` or `evidence_status` is supplied, preserve its current enum and update it only from confirmed evidence; do not create a replacement status.

After each observed review/promotion, perform one compact update:

1. **Record facts:** grade, actual bonus, level change, explicit feedback and the last-observed pre-review state. Missing exact review-time stats remain unknown. Grade and advancement are separate observations; record both independently.
2. **Compare with the preceding period:** within-stat direction, actual financial inflows/losses if known, new risks, main-action families used and whether prior feedback changed. More Output without promotion does not prove Output is irrelevant or the only missing input.
3. **Update the working hypothesis before choosing.** Separate feedback that names a specific metric or criterion from broad feedback about results or impact. “No standout wins” or “clearer outcomes” can support comparing delivery with visibility, but does not by itself establish a numerical Output deficit. Do not turn a lower raw Output value than Skill or Network into promotion evidence. Compare current legal options by their stated effects, costs and timing: creating substantive work, making completed work visible, building capability/scope, or improving relationships. A report can surface completed work; it does not prove new delivery or advancement. Grade and promotion are separate: A/S does not prove eligibility, and a miss does not identify a hidden threshold. If evidence grew without promotion, treat the prior action mix as unproven and compare current alternatives; change direction when another option is better supported. If no specific gap or better action is supported, keep the cause unknown and choose the best current option.
4. **Use the next quarterly main menu** to compare a small number of relevant offered actions, apply risk constraints, and choose one. Follow up on returned effects after success. A planned action is not a cached choice ID.
5. **At the next feedback:** retain, revise or mark the hypothesis unconfirmed. Improvements coinciding with an action are observations, not isolated causal proof; record major story/risk changes that confound the comparison.

| Observed condition | Next-period allocation rule |
| --- | --- |
| Risk Management identifies a current, directly relevant restriction | Follow that restriction and keep other safe productive options available. An unresolved status alone is not a severity judgment or an automatic veto. |
| Promotion actually occurred | Compare returned state for changed relationships, Output and warnings; stabilise any observed deterioration, then prepare for the next window. Retain low-performance feedback if the grade was poor. Do not assume a fixed reset formula. |
| C/D, or explicit concern about weak results | If feedback concerns delivery, compare a feasible key project/resource request with the current alternatives. If it concerns presenting/documenting existing work, compare leadership reporting/publicizing with more work. If capability or relationships are explicitly implicated, compare the corresponding support actions below. Unknown cause -> keep a safe useful baseline and test one feedback-relevant change, not an invented formula. |
| Feedback says results lacked a standout contribution | Treat this as broad impact feedback, not a measured Output deficit. Compare concrete delivery with making completed work visible; choose from the current menu and evidence. A report does not replace new delivery. |
| A/S but no promotion | Do not automatically intensify work. Check the manager's actual feedback and prior-period changes. Compare reporting only when there is completed work to make visible; compare repair, mentor, rotation, resource support or delivery when current evidence points there. Reassess immediately if the next review is the last realistic promotion opportunity. |
| B/unclear feedback, no promotion | Maintain sustainable results; select a relevant change only when state/feedback supports it. Do not treat a neutral review as proof of a known bottleneck. |
| Same Level through successive observed windows | Reassess the action mix using actual feedback, changes and risks. Repeated misses strengthen the evidence for a change; do not infer a tenure threshold, force rotation or promise promotion. |

Maintain one compact `strategy.feedback_loop` summary in the current conversation: confirmed review and feedback; key action families and notable repeats during the period; important observed changes; major events or new risks; current hypothesis and next check. Preserve unknowns. Keep enough recent evidence to compare the plan, not the whole transcript.

## Compare the actual main actions

Use only current descriptions and observed effects; these are candidate-selection hypotheses, not guarantees. First screen every currently offered legal action for its direct effects, explicit cash cost, risk restriction, timing and material unknowns. Then compare up to three relevant finalists in depth, keeping opportunity costs and remaining time explicit. Do not omit an action just because it costs money or prefer one just because it is free:

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

Screen all currently offered legal options, including paid and no-cash options. For each paid option, count its stated cash cost now and compare its supported benefits and risks with the best actual alternatives, whether paid or free. A free option has zero cash cost but can still have worse career, health, time or opportunity effects. Count a future return only when current rules, menu text or observed results support it; an unknown future benefit does not justify a known cash loss by itself.

Prefer choices that build credible long-term capability/results and preserve working relationships when those benefits fit current needs. Visibility, key projects, mentorship, rotation and relationship repair are alternatives to compare, not a mandatory rotation or universal project-first rule. A high Skill or Network value does not establish promotion sufficiency or make further gains automatically worthless; compare current evidence, menu effects and opportunity cost.

## Remaining horizon

As time runs out, compare whether a delayed benefit can still arrive. Once the final review is confirmed as settled, do not prepare for another promotion or justify extra Output through a future review. Compare current legal options on benefits that can still affect the ending state, including confirmed financial effects and relevant survival risks. Do not assume short remaining time makes Health worthless or that a late project must pay off. If the final review is not confirmed, keep its status unknown and do not infer settlement from the month alone.

Keep the strategy summary compact: current priority, next not-yet-observed review, explicit feedback, unresolved hypotheses. Accept a reasonable trade-off when evidence supports it; an adverse random outcome alone is not proof the decision was wrong.
