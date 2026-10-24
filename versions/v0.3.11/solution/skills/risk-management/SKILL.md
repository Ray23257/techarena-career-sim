---
name: risk-management
description: Evaluate every decision's survival and delayed risk; load when warnings, unresolved risks or mitigation feedback need interpretation, and reload after lost risk context. Preserve evidence until resolution is supported.
---

# Risk Management

## Input and output

Input: latest observation revision, visible state, current `events`, current choices, unresolved risk entries and relevant confirmed history. Use this method for every decision; reuse its body while available. If risk context was compressed or lost, read this Skill again and restore the matching session ledger from confirmed current-conversation or native evidence; missing evidence remains unknown.

Output advice to the same Agent: `observation_revision`, `blocked_choices`, `preferred_choices`, supporting evidence, ledger updates and unknowns. Only use current choice IDs. Do not call game actions independently. The controller integrates advice and executes once.

## Evidence before interpretation

1. Read warning information from `events`, plus explicit event descriptions, outcomes, performance/promotion feedback and relevant native logs. Do not invent a separate warning field or hidden counters.
2. Preserve the warning text and its observed month/revision. A later empty `events` is not a clearance: the engine consumes pending warnings when observed. Absence of a new warning means only no new warning was returned.
3. Maintain compact entries: `id`, `first_seen`, `last_seen`, `evidence`, `policy_urgency`, `mitigation_attempts`, `status`, `next_check`. Deduplicate recurring evidence; do not remove unresolved older risks to shorten context. Urgency labels `attention`, `elevated`, `critical` are our policy classifications, not official numeric hazard bands.
4. Separate confirmed effects from plausible delayed consequences and unknowns. An apparently professional or ethical story answer can still have relationship costs; do not promise that it is mechanically risk-free. A favorable visible delta cannot prove hidden safety.

## Constraints and risk scoring

Health reaching zero is an explicit failure. Other published failure directions include sustained low dignity, network at zero too long, wealth bottoming out too long, skill falling behind, repeated poor performance and hidden organizational hazards. Exact thresholds/counters, hidden risk formulas and future events remain unknown.

- **Hard exclusion:** an option's known effect would cause an explicit immediate failure, where another legal alternative exists. Do not invent a numerical safety threshold for other stats.
- **Conservative restriction:** an explicit severe/unresolved warning or serious deterioration has direct relevance to a candidate's stated risk. While a feasible safer alternative or relevant mitigation exists, block avoidable additional risk and prefer dealing with the concern. Record evidence and the condition for reassessment. This is our policy, not a simulator prohibition.
- **Advice:** minor warnings, uncertain consequences and moderate trade-offs. Compare them with career benefit; do not veto all development indefinitely. Unknown effects are not automatically fatal or safe.
- Risk control is a final-score objective as well as a survival concern. Do not ignore unresolved observed hazards just because visible Health/Dignity are high or the game has not ended; do not treat local score reports as official cloud weights.

## Mitigation and follow-up

For a relevant warning, compare currently offered mitigation, safer story alternatives, relationship repair and career/resource opportunity cost. Reserve 2 Energy for a currently available landmine-defusing action when its relevance and urgency warrant it; do not spend those points first on optional gains. Do not assume every risk is fixed by that action or that it clears all risk at once.

Use ledger statuses `unresolved`, `mitigation_pending`, `monitoring`, `resolved_explicit`:

- New risk evidence -> `unresolved`; repeated/worse evidence after mitigation -> `unresolved`, preserving prior attempts.
- An intended mitigation is pending only after the controller records intent. Confirm its execution from `success`/logs; a failed action is not a completed attempt. On explicit rejection restore the prior status; on transport uncertainty retain `mitigation_pending` and reconcile before another action.
- Confirmed mitigation without explicit resolution -> `monitoring`; a quieter or favorable message can support improvement but cannot prove a hidden value is zero.
- Only a clearly scoped explicit resolution supports `resolved_explicit`; it resolves that identified issue, not all organizational risk. Never clear the whole ledger because one issue closed.

After mitigation, examine subsequent returned warnings and relevant results; use bounded logs if causality is unclear. At the next available decision reconsider both residual risk and any newly created exposure. Repeated mitigation must have a reason; neither one-and-done clearance nor automatic quarterly defusing is justified.

At the final phase, compare available risk-reduction opportunities with remaining score gains. Do not invent a predictable numerical risk-score increase. Include unresolved observed risks in the final audit report.
