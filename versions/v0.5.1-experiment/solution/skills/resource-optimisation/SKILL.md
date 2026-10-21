---
name: resource-optimisation
description: Turn the current Career Planning objective and Risk Management result into at most three legal quarterly Energy candidates, preserving budget, survival and terminal value while comparing career opportunity cost.
---

# Resource Optimisation V0.5.1

## Role and boundaries

Advise the same Agent during the Energy phase. Read the current native menu, observed Energy, confirmed spending, visible state, Risk Management's existing result and Career Planning's Decision Header. Do not call tools, execute actions, create another risk engine, or invent a router. Career Planning owns the Main Action recommendation; Resource Optimisation does not require an extra read at every Main Action phase.

The quarterly budget is 3 Energy and unused points do not carry over. Main Action is a separate phase and does not consume Energy. Match costs and IDs to the current menu; never reuse a remembered choice number.

## Screen the whole current menu

Inspect every currently offered legal single action, including its Energy cost, restrictions and stated gains. Do not enumerate all complete action sequences. Given the 3-Energy budget, compare sensible structures such as a 2+1 split and 1+1+1 when those actions are offered and materially different. Construct at most three materially different candidate combinations. Do not truncate by menu order or invent utility scores. Then:

1. Remove only choices prohibited by Risk Management's `blocked_choices` or explicit severe-warning restriction. Use Risk Management's existing status `unresolved`, `mitigation_pending`, `monitoring` or `resolved_explicit` and urgency `attention`, `elevated` or `critical` as context. `monitoring` is not explicit resolution. Do not create Red/Amber/Green as a second risk classifier.
2. For each surviving candidate record direct public gains, support for Career Planning's `evidence_focus`, time to the next review, Health/Dignity cost, any risk effect stated by the current menu, and the best forgone candidate. Ordinary attention/elevated warnings increase opportunity cost; they do not automatically veto a higher-value legal action. A severe explicit restriction still wins as a hard constraint.
3. Calculate each action's **marginal gain from the current observed state** before comparing it. Apply the published cap of 10 only to Health and Dignity. For a menu-stated recovery amount, effective gain is `max(0, min(10, current + stated gain) - current)`. Never assume a cap for Network, Skill or Output, and do not supply an unstated recovery amount or hidden benefit. Health=9 with a stated +1 recovery yields +1; Health=10 yields 0. Dignity=10 makes a Dignity-only Mental Recovery's public recovery gain 0. If a pure recovery action has zero marginal gain and no other menu-stated effect, treat it as ineffective and exclude it when any legal candidate has a positive relevant gain; do not recommend it because the attribute is generally important.
4. Recalculate each combination in sequence. After each candidate action, update the working observed attributes by its explicitly stated effects, applying Health/Dignity caps, then recalculate the marginal effect of the next action from that updated state. Thus a later recovery cannot claim the same capped gain twice, and the comparison cannot count each action's standalone gain as if earlier actions had not changed the state. Compare no more than three materially different Energy combinations: a required protection/mitigation combination when applicable, one supporting the current evidence focus, and a balanced/direct-value combination when genuinely different. Keep alternatives that have distinct unknown benefits; remove only an obviously dominated combination. Unknown is not a positive recovery benefit.
5. Select only the first current legal action. After success, obtain a fresh native `observe`, refresh Energy, warnings and applied effects, then rebuild the shortlist. Never submit a cached sequence or parallel actions.

## Action comparisons

- **Prepare Report:** always count the menu's stated Output/Dignity gain. Treat visibility as additional career evidence only when observed work exists and the feedback asks for recognition; otherwise compare its direct gain with project, relationship, skill and recovery alternatives. Do not mechanically repeat or ban it.
- **Intensive Work:** use only when the current menu states its effects. Include Health/Dignity loss and any current-menu risk effect in the comparison. The reviewed snapshots in `offline_llm_compare_v05/scenarios.jsonl` state Output +2, Health -1, Dignity -1 and HiddenRisk +1 for High-intensity work; do not assume HiddenRisk changes when the current menu does not state them. Do not use it as a generic promotion button.
- **Skill Study:** compare Skill gain and Health cost with the remaining time to review and the salary value of an earlier Level; do not assume Skill has a ceiling.
- **Network Maintenance / recovery:** Network has no published cap. Compare its stated gain, relationship evidence and opportunity cost. Health/Dignity recovery uses the published cap of 10 and its calculated marginal gain from the latest observation, not a generic attribute priority.
- **Defuse:** choose it when Risk Management's current status, urgency, `blocked_choices` or explicit mitigation advice makes it relevant. A historical warning or an empty current event alone does not force it; `monitoring` does not equal `resolved_explicit`.
- **Reserve energy:** leaving points unused is allowed when remaining actions are harmful, irrelevant or too uncertain. Do not spend merely because Energy remains or to reach zero. There is no hidden recovery benefit unless the current menu explicitly states it. Do not invent hidden gains to justify a zero-marginal recovery action. Risk Management's valid `blocked_choices` and explicit severe-risk restrictions remain controlling; never bypass them to gain Output, Network or another career benefit.

## Review and terminal timing

If `target_review` is a future unprocessed review, favor an action whose stated or observed effect can mature before that review and supports the one evidence focus. If a review result has already returned, current-quarter actions serve the next unprocessed review, not the settled one.

After M48 is settled, use `review_phase=terminal_processed` and `target_review=terminal_processed`. Compare direct Wealth, Health, Dignity, Skill, Network, Risk Control and any directly confirmed terminal effect. Do not spend for an imagined ninth review or evidence that cannot mature.

## Main Action handoff

Career Planning and Risk Management own the Main Action decision. Resource advice may state an Energy opportunity cost, but must not make Energy spending a prerequisite for Key Project, Report, Push Resources, Mentor, Rotation, relationship repair, Lie Low or another offered Main Action. Main Action and Energy remain independent.

## Output and persistence

Keep the legal menu inventory distinct from proposed plans: `energy_choice_ids` lists current legal menu options only; it is not a selected combination. If comparing combinations, return at most three materially different entries under `candidate_combinations`. Each entry must contain `choice_ids`, `total_energy_cost`, `first_choice_id` and a brief reason. Verify each total against currently available Energy and omit any candidate over budget. The preferred `energy_first_choice_id` must match the first action of the preferred candidate. If no useful combination is justified, return no candidates and leave Energy unused.

Recommend only the current first legal action. After it succeeds, obtain a fresh native `observe` and rebuild the candidates. Do not execute or submit later steps from a cached candidate. Use only existing `strategy.feedback_loop` and checkpoint fields; a local recommendation is not proof that an action executed. Rely on native success, follow-up observation and the Controller recovery fence.
