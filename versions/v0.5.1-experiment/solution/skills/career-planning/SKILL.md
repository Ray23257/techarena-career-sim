---
name: career-planning
description: Set one evidence-based career objective for the next observed review or terminal phase, compare current legal Main Actions and long-term Level/Wealth value, and update the existing feedback loop without inventing promotion rules.
---

# Career Planning V0.5.1

## Role and boundaries

Advise the same Agent; do not call tools, execute actions, delegate, or create another ledger. Read the current native `observe`, current legal choices, Risk Management advice, compact review history and the existing `strategy.feedback_loop`. This Skill supplies the main career decision basis; it does not guarantee promotion or infer hidden thresholds.

Keep the existing `strategy.feedback_loop` as the only career ledger. Reuse these existing fields and enums exactly:

`review_phase` = `pre_review`, `post_review` or `terminal_processed`; `target_review` = the current/next unprocessed review, `unknown` when no target is verifiable, or `terminal_processed` (preserve a last valid value when context is incomplete); `evidence_focus` = `delivery`, `visibility`, `capability`, `scope`, `relationships` or `unknown`; `evidence_status` = `observed`, `partial`, `negative` or `unknown`; `prior_intervention_family`; `hypothesis`; `next_check`; `unknowns`.

Do not create a new promotion formula, probability model, status ledger or fixed month plan. If the existing feedback loop is not visible in the current context, first use the Controller's existing safe recovery path when its prerequisites are satisfied. Report an unresolved absence as an information gap, preserve the last valid `target_review` instead of inventing a new value, and keep affected `evidence_focus` or `evidence_status` fields `unknown`; do not assume a new Controller interface.

When `target_review` is missing, inspect the **current complete native observation**, including every current returned review, every returned `events` text entry and relevant review-history records, for explicit settled-review evidence: final performance/grade, bonus, promotion decision or notice, and manager/HR review feedback. Do not rely only on structured review fields or a persisted loop. A clear returned result is current evidence even when `strategy.feedback_loop` is absent from context. Update the existing loop only after settled review evidence confirms settlement; an upcoming/scheduled review, generic praise, or unrelated manager comment is not settlement. A dated promotion record can confirm settlement only when it clearly ties the level change to a completed review, not merely because the current month matches the date.

After explicit settlement, set `review_phase=post_review` and update `target_review` to the next unprocessed review only when the next point follows from a review cycle already established by confirmed feedback or existing history. Derive the interval from confirmed review records, never from the current month alone. The observed M12 -> M18, M18 -> M24, M30 -> M36 and M36 -> M42 transitions establish examples of the six-month cycle. Thus a current history record explicitly stating “M42 (A, promoted L4->L5)” confirms an M42 review/promotion, and the already evidenced cycle makes M48 the next target. A dated level mention that does not clearly identify a completed review is insufficient. After M48 is explicitly settled, use the existing `terminal_processed` values. If settlement or the next cycle cannot be established, preserve a last valid target or set the existing `target_review` field to `unknown`; do not invent a schedule.

If a last valid `target_review` exists, carry it forward only after checking it against returned review phase and settlement evidence. If neither historical target nor review settlement can be confirmed, do not infer a target from the month or claim that a review was processed. Without explicit review evidence, preserve `unknown` rather than treating the calendar month as proof of settlement. Record the cause in existing `unknowns`, `hypothesis` or `next_check`, and compare only confirmed direct attribute gains and currently legal actions. If the Controller's safety recovery preconditions are not satisfied, follow the existing halt rule instead of deciding from incomplete history.

## Objective and review timing

The main optimization target is the 48-month combined result, with special weight on earlier Level and Wealth gains and the resulting cumulative salary. Health, Dignity, Skill, Network, Output and Risk Control remain real constraints and score contributors. A normal risk warning is an opportunity cost to compare; an explicit severe survival restriction or Risk Management `blocked_choices` is a hard constraint.

At each decision, form a short Decision Header from the current `observe`, returned review/feedback, existing `strategy.feedback_loop` and Risk Management summary, then hand it to Resource Optimisation when Energy is being planned:

```text
review_phase: pre_review | post_review | terminal_processed
target_review: current/next unprocessed review | unknown | terminal_processed (preserve a last valid value when context is incomplete)
evidence_focus: delivery | visibility | capability | scope | relationships | unknown
evidence_status: observed | partial | negative | unknown
prior_intervention_family: existing value or none
next_check: one observable result and when to inspect it
```

On a review month, settle the returned review before interpreting that month's actions. Actions after a returned review serve the next unprocessed review. After M48 is settled, set both `review_phase` and `target_review` to `terminal_processed`; compare direct terminal value and do not prepare for a ninth review.

## Choose one evidence focus

Record facts before interpretation: grade, actual bonus, level change, explicit manager/HR feedback, the latest trustworthy pre-review state and material risk changes. Missing facts remain unknown.

Choose one focus from explicit evidence:

1. `delivery`: a concrete outcome or stable delivery is missing, or feedback explicitly asks for clearer outcomes.
2. `visibility`: work is already observed, but recognition, reporting or decision-maker visibility is the stated gap.
3. `capability`: a current opportunity or feedback identifies a real capability need.
4. `scope`: feedback or an opportunity points to responsibility, resources, cross-team influence or leadership range.
5. `relationships`: observed friction, Network loss, trust or organizational support needs attention.
6. `unknown`: evidence does not distinguish the categories.

`evidence_focus` orders candidates; it never excludes a legal action. A report's stated Output/Dignity gain remains a valid direct benefit even when no delivery is observed. It is additional visibility evidence only when real work exists. Do not treat Skill, Network or Output as capped or as hidden promotion thresholds.

## Rolling review loop

For every current decision, return the existing `target_review`, one `evidence_focus`, one existing `evidence_status`, up to three materially different current legal Main Action candidates, expected time to realize each, direct gains, opportunity costs, unknowns and one `next_check`. Do not return a future choice ID.

- **Risk input:** obey Risk Management's `blocked_choices` and explicit severe restrictions. Read its existing status `unresolved`, `mitigation_pending`, `monitoring` or `resolved_explicit` and urgency `attention`, `elevated` or `critical`; do not reinterpret `monitoring` as resolved or create another risk classifier. If no hard restriction applies, compare risk cost with career value.
- **Promotion occurred:** inspect returned Network, Health, Dignity and warnings. Add relationship or health repair only when deterioration is observed; otherwise invest in the next evidence focus or direct value.
- **C/D or explicit weak-results feedback:** choose the candidate that can produce the named missing evidence before `target_review`. Delivery favours a real project or fitting resource request; visibility favours reporting existing work; capability, scope and relationships use matching current opportunities.
- **A/S without promotion:** audit whether the prior hypothesis was executed and whether its evidence appeared. Then choose the missing evidence or a direct-value action. Do not automatically add Intensive Work or repeat reports.
- **B or unclear feedback:** keep sustainable useful work and change direction only when current evidence supports it.
- **Repeated same-Level reviews:** audit the prior hypothesis and next check. Change intervention only when a different supported opportunity exists; never infer a tenure threshold.

## Compare Main Actions

Use the current menu and descriptions. For each candidate compare direct public gains, plausible evidence gain, time to the next review, long-term Level/Wealth value, health/relationship cost, Risk Management restrictions and the best forgone alternative.

- **Key Project:** prefer when a concrete deliverable or outcome gap exists and it can mature before the target review. Positive stat deltas do not prove success or promotion.
- **Report Results / Publicize:** count stated Output/Network/Dignity gains in every legal menu. Prefer the visibility interpretation when observed work needs recognition; without observed work, it may still win on direct value but is weaker promotion evidence. Compare repeated reports by marginal gain; do not repeat or ban them mechanically.
- **Push for Resources / responsibility:** prefer when a concrete scope or resource constraint is present and the opportunity can expand responsibility before review.
- **Mentor / Rotation:** prefer when capability or scope evidence is explicit and timing supports the next review; do not assume sponsorship or automatic advancement.
- **Repair Relationship:** prefer when friction, Network loss or an unresolved relationship issue is observed; do not claim that it clears all organizational risk.
- **Lie Low / no action:** choose only when Risk Management, Health or the absence of a useful safe opportunity justifies it.

When an evidence candidate cannot mature before the next review, let a better direct or terminal benefit win. Earlier promotion has real salary value, but the promotion result and formula remain unknown; use the salary difference only as opportunity-cost context.

## Story choices and persistence

For each story option, separate stated immediate effects, plausible delayed consequences and unknowns. A narrative claim is not a confirmed Level or salary change until returned by the environment. Keep salary, bonus and event income/loss distinct.

Update the existing `strategy.feedback_loop` only after a review/promotion, material feedback, material risk/state change, changed hypothesis or uncertain execution. Preserve the current and preceding intervention family plus `next_check`; ordinary observations and routine choices stay in memory and do not create another ledger.
