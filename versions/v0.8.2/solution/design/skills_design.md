# Skill Design

## System shape

One JiuwenSwarm agent loads four Skills. The Career Controller is the only coordinator and executor. Career Planning, Resource Optimisation, and Risk Management return advice to that same agent; they do not call game tools or act as separate agents.

At a fresh entry, the Controller reads all four Skill bodies before the first game action. It then uses the current native observation and the relevant specialist advice. After each successful action it observes again. The next choice is based on the returned state and current menu, not on a cached action sequence.

## Responsibilities and information

| Skill | Decision responsibility | Main inputs | Output to the Controller |
| --- | --- | --- | --- |
| Career Controller | Session continuity, routing, legality, final arbitration, execution, and terminal stopping | Current observation, live registered tool list, specialist advice, confirmed native history | One current legal action, executed through a registered native tool; then a fresh observation |
| Career Planning | Story choices, quarterly Main Actions, review interpretation, career evidence, and Wealth trade-offs | Full current observation including returned events and feedback, current menu, visible state, confirmed review history, current strategy feedback | A preferred legal choice, a concise reason, the best alternative, its opportunity cost, and unknowns; when promotion reasoning is used, a brief note naming the explicit evidence or stating that the specific gap is unknown |
| Resource Optimisation | Quarterly Energy budget and marginal-value comparison | Current Energy menu and budget, visible attributes, returned effects, Career Planning objective, Risk Management restrictions | Up to three materially different feasible combinations, with cost and first choice; one current preferred step |
| Risk Management | Risk evidence, urgency, blocking advice, mitigation, and follow-up | Current events and choices, visible state, relevant confirmed risk evidence and native logs | Risk-specific restrictions or safer alternatives, evidence, status update, and unknowns |

The Controller integrates the advice. Risk Management is the only risk judge. The Controller enforces its valid restrictions, while Career Planning and Resource Optimisation compare the remaining legal opportunities. Ordinary risk is not an automatic veto; evidence of immediate failure or major hard-to-reverse loss can restrict an exposed action.

## Decision handoffs

1. Read the latest observation, including the complete event text, available choices, remaining Energy, and any returned review or risk evidence.
2. Apply Risk Management to every decision. Use its fuller comparison when a warning, recorded risk, or material survival uncertainty is relevant.
3. For a story or Main Action, ask Career Planning to compare the currently offered legal options. For Energy, ask Resource Optimisation to compare feasible budget structures; Career Planning supplies the current career objective.
4. Resolve session identity, legality, current budget, and risk restrictions before choosing. Compare supported immediate effects, relevant future implications, remaining time, and opportunity cost. Do not invent hidden thresholds or numeric utilities.
5. The Controller executes one action. After success, it observes again and refreshes only the comparisons affected by the new state, menu, events, budget, or risk evidence.
6. When the final review is confirmed settled, stop pursuing another promotion and compare only benefits that can still affect the ending state.

## Limits

The Skills distinguish returned facts from hypotheses. A review calendar indicates when a review may occur; only returned evidence confirms its result. Health and Dignity have public caps of 10. No cap is assumed for Skill, Network, or Output without explicit game evidence. Promotion thresholds, hidden effects, and exact official cloud outcome formulas remain unknown.
