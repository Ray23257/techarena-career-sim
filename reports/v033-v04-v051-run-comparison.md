# V0.3.3 / V0.4 / V0.5.1 Run Comparison

Date: 2026-10-22

## Evidence boundary

This report compares four completed 48-month trajectories:
- V0.3.3 third run: 2026-10-20 17:22:55 UTC.
- V0.4 experiment, fourth run: 2026-10-20 20:29:02 UTC.
- V0.5.1 experiment, fifth run: 2026-10-21 22:07:34 UTC.
- V0.3.3 replication: 2026-10-21 23:52:42 UTC; only its score report was supplied, so no event-level comparison is possible for this replication.

Different runs contain different event sequences. These results are observational and do not establish causal effects of a Skill revision.

## Final score reports

| Run | Grade | Quantitative score | Level | Wealth | Resilience raw | Skill | Risk-control raw / weighted | Network |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| V0.3.3 third run | A | 70.38 | L5 | 33.7 | 20 | 117 | 0 / 10.0 | 44 |
| V0.4 fourth run | C | 59.85 | L4 | 21.4 | 20 | 92 | 0 / 10.0 | 36 |
| V0.5.1 fifth run | C | 50.40 | L4 | 17.6 | 20 | 80 | 7 / 3.0 | 36 |
| V0.3.3 replication | B | 69.76 | L5 | 37.7 | 20 | 116 | 1 / 9.0 | 41 |

All runs survived 48 months. Resilience was 20 in every run, so it does not explain the score differences.

The public rules do not publish a numeric final-score-to-grade cutoff. The two V0.3.3 outcomes (70.38/A and 69.76/B) are insufficient to infer a universal 70-point threshold.

## Score-dimension deltas

### V0.3.3 third run → V0.3.3 replication

Weighted-score changes:
- Level: 0.00
- Wealth: +1.00
- Resilience: 0.00
- Skill: -0.12
- Risk control: -1.00
- Network: -0.50
- Total: -0.62

The replication retained L5 and improved raw Wealth from 33.7 to 37.7. Its lower grade is associated with the combined weighted-score changes, especially Risk Control and Network; this does not by itself indicate a strategy failure.

### V0.4 fourth run → V0.5.1 fifth run

Weighted-score changes:
- Level: 0.00
- Wealth: -0.95
- Resilience: 0.00
- Skill: -1.50
- Risk control: -7.00
- Network: 0.00
- Total: -9.45

In this single comparison, V0.5.1 did not improve any final-score dimension over V0.4; the largest difference is Risk Control. Different event trajectories remain a confounder.

## Action-trace observations

Counts below are deduplicated native `take_action` calls, classified from the agent's action notes. They describe what the agent attempted, not proven causal effectiveness.

### V0.4 fourth run
39 energy-action calls were noted: 12 report preparation, 9 Health recovery, 9 Network maintenance, 4 risk defusing, 3 Skill study, and 2 intensive-work actions. The notes repeatedly reference named review months and prior feedback, for example choosing actions “before M30” or “before M42.”

### V0.5.1 fifth run
43 energy-action calls were noted: 25 report preparation, 7 Health recovery, 6 risk defusing, 4 Network maintenance, and 1 other. No Skill-study action appeared in the notes. Of 16 quarterly main-action calls, 15 were key-project actions and 1 was a risk-defusing action.

A concrete terminal-phase mismatch appears in the fifth-run trace: the M48 review had already returned B/no promotion, but the final-quarter energy plan still selected report preparation twice and described Output as having “direct terminal value.” Output is not a direct dimension in the final score report, and the M48 review was already settled. The agent should instead compare currently available actions against confirmed terminal-score effects and opportunity costs.

The fifth-run trace also contains repeated report preparation justified by Output being the “graded lever.” A positive uncapped Output delta alone is not sufficient evidence that another report is the best action: the agent must check whether the current feedback calls for delivery, visibility, capability, scope or relationship evidence, and whether the review it could influence is still unprocessed.

## Design conclusion

1. Historical runs belong in offline evaluation and hypothesis generation, not in the live agent's decision context as month-specific scripts.
2. A month or review horizon can be used as an observed state variable, but the agent must confirm the current event, review settlement, feedback and remaining horizon. Month alone must not prove that a review happened or that a particular action is appropriate.
3. At every decision, use the current observation and legal menu to calculate effective marginal gains after caps, current risk constraints, evidence fit, opportunity cost and remaining horizon.
4. After each action, re-observe and compare actual state changes with the intended effect. Repeatedly choosing a positive local stat gain is not enough if it fails to address the current bottleneck.
5. Do not prepare for an imagined ninth review after M48 is explicitly processed. Optimize only confirmed direct terminal effects at that point.

V0.5.1's written policy already states that it should not create a fixed month plan. The fifth-run action trace shows a gap between that intended rule and actual execution. Future revisions should target this execution gap and validate it with repeated state-based scenarios, rather than adding more month-specific branches.
