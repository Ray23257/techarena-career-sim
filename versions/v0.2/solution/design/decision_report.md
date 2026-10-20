# Decision Report

## V0.2 rule alignment

This update aligns the first single-agent, single-Skill solution with the public timing and scoring guidance. No game has been run, so there are no measured results or claims of score improvement.

## Public rules used

The official rules and handbook state:

- A game lasts 48 months. Each quarter provides 3 Energy points that do not carry over, plus one main action or no main action.
- A formal performance review and a promotion window occur every six months. Performance depends on many factors. Promotion considers Skill, Network, Output, and more; it reflects long-term results, and higher levels have higher requirements.
- Monthly salary is paid by Level and increases at higher levels.
- Public final-score priorities are Level (`Higher`), accumulated Wealth (`High`), physical/mental Health and professional Skill (`Medium`), and risk control and coworker relationships (`Some weight`). The local ending rating is S, A, B, C, D, or E.
- Public early-failure directions include Health reaching zero, long-term low Dignity, hidden hazards, repeated low performance, Network staying at zero too long, Wealth bottoming out too long, and Skill continually falling behind.
- The cloud evaluation also considers strategy engineering quality and resource efficiency.

Sources: `docs/rules.rst`, `docs/failure-and-ending.rst`, and `docs/handbook.rst`.

## Strategy assumptions

- Address explicit warnings and sustained visible deterioration before pursuing optional score gains. Because most danger boundaries are not published, use visible state and feedback rather than invented thresholds.
- Once major survival concerns are controlled, favor long-term Level and Wealth progress while maintaining Health, Dignity, Skill, Network, and Output. The priority tiers guide trade-offs; they do not dictate one action type on every turn.
- Higher Levels receive higher monthly salary. Earlier advancement may therefore increase accumulated Wealth across the remaining months. This is an inference from the public salary table, not a guaranteed promotion, score formula, or action effect.
- Review quarterly Energy and main-action choices when that phase appears. Because unused Energy expires, useful and safe opportunities should not be ignored by default; spending solely to exhaust the budget is not required.
- Use feedback around six-month reviews and promotion windows to assess long-term trends. No single action is assumed to determine either outcome.

These are untested strategy hypotheses. They have not been shown to improve the score.

## Unknowns and risks

The qualitative priorities are public, but exact numeric score weights and the complete scoring formula remain unknown. So do the performance formula, promotion thresholds, precise failure boundaries and counters, hidden hazard values and trigger probabilities, and the full downstream effects of actions. The order in which semi-annual review and promotion processing resolve should be taken from runtime observations rather than assumed. No S-grade cutoff is published. The local ending rating is not the full cloud contest evaluation.

## Evaluation plan

After the team confirms that a full run should begin, record the solution revision, engine/data versions, model ID, and a random seed if the runner exposes one. Run one baseline and preserve the returned transcript, event history, resource use, terminal month, ending rating, and score components. Then change one decision rule at a time and compare runs under the same conditions where possible. Treat a change as an improvement only when comparable results support it.

No baseline run or strategy evaluation has been performed.
