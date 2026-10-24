# Decision Report

## Objective

The agent seeks the highest valid competition result over the full 48-month run. It gives strategic attention to Level and Wealth in line with the published qualitative outcome guidance, while preserving wellbeing, professional skill, risk control, and coworker relationships as distinct outcomes. Raw attribute points are not treated as interchangeable.

Official Stage 1 scoring is 80% live play, 10% Skill-document design quality, and 10% token efficiency. Live play is the arithmetic mean of three official runs' `quantitative_score`; the Skill-document score is averaged across the submitted Skills. For each run, token efficiency is based on total tokens per month survived: up to 500,000 scores 100, at least 3,000,000 scores 0, and values between them decline linearly. An early-ending run is capped at 50 on this component. The agent therefore aims to make decisions executable and generalisable while avoiding repeated analysis when relevant evidence has not changed. It does not cut required observation, legality, or recovery checks to save tokens. A single local run is not an official score. A team reaching Stage 2 must also pass the top-ten selection; only then is the final competition score 70% Stage 1 and 30% expert review.

## Evidence used during play

The agent uses:

- The current native observation, including the full `events` text, visible attributes, current choices, Energy budget, and returned status changes.
- The public handbook and public rules when available through the native tool.
- Explicit performance, promotion, compensation, and manager feedback returned by the game.
- Current-session action results and relevant confirmed risk evidence from native history.

Historical development runs are used only to improve general decision behavior. For example, retained logs show both strong Level outcomes with different total scores and repeated rejected `take_action` tool identifiers. The current design responds with explicit evidence checks and live registered-tool selection. These are observations from the development environment, not proof of official score gains or cloud behavior.

The review calendar is used only to identify a possible review opportunity. The agent confirms settlement from returned evidence and does not infer a processed review from the month alone. It distinguishes a performance grade from a promotion result and keeps missing targets or effects unknown.

## Choice method

For each decision, the Controller first checks session identity, current legality, budget, and risk restrictions. Career Planning screens all offered Main Actions and compares a small relevant set using direct effects, evidence for the current career need, cash cost, time remaining, plausible promotion or future-pay implications, and the best alternative. A report may make completed work visible; it is not treated as delivery by itself. Evidence focus guides diagnosis but does not exclude a stronger current opportunity.

Resource Optimisation screens all currently legal Energy choices, clips known Health and Dignity gains at their public cap, and constructs no more than three materially different feasible budget proposals. It does not enumerate full action trees or invent utility scores. It recommends one current step; the Controller observes after success and then compares again using the new menu and remaining Energy. Main Action remains a separate quarterly choice.

Risk Management evaluates risk evidence and urgency. Unresolved follow-up status alone is not severity, and an empty later event field does not clear a previously observed risk. The agent protects against early failure and supported major hard-to-reverse losses while comparing ordinary risks against concrete career and financial benefits.

## Adaptation and generalisation

The policy contains no fixed event-to-action script and assumes no particular event will occur at a given month. It responds to current menus, returned effects, review feedback, and risk evidence. At each confirmed review, Career Planning starts the next window from the latest evidence; older feedback remains historical unless newer feedback or current results support carrying it forward. A low raw attribute alone does not identify a promotion gap. The agent distinguishes delivering work or taking wider responsibility from presenting completed work, and compares the current legal options without assuming that any one action guarantees promotion. A missed promotion prompts a review of the evidence and action mix, not an invented threshold or forced change for its own sake. After the final review is confirmed settled, it stops preparing for another promotion and considers only remaining ending value.

The public rules and development runs do not establish all official cloud thresholds, formulas, or event outcomes. Local historical scores are evidence about those observed runs only. This design therefore uses verified public effects and current returned state, marks indirect benefits as uncertain, and expects to adapt if evaluation conditions differ.

## Evidence limits

The strategy has not been validated through an official scored run. The repository's local preflight checks the manifest and Skill front matter; the online submission requirements describe a broader required-file check. Neither local check proves that the official platform accepted an upload, that the runtime will follow every instruction, or that the strategy will achieve a target grade. Actual official results require the competition evaluation.

## Public references

- [Competition rules and fair play](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html)
- [Submission requirements](https://techarena-career-sim.readthedocs.io/en/latest/submission.html)
- [Public handbook](https://techarena-career-sim.readthedocs.io/en/latest/handbook.html)
- [Public rules](https://techarena-career-sim.readthedocs.io/en/latest/rules.html)
