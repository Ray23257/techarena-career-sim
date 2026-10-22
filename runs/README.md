# Career simulation run archive

This directory stores raw run evidence for comparing strategy versions. Event logs and transcripts retain their record content, with line endings normalized to LF during upload; they are not byte-for-byte copies. Score reports are retained as JSON.

## Runs

| Run | Strategy snapshot | Result | Key ending state |
|---|---|---|---|
| Third run | V0.3.3, 2026-10-20 17:22:55 UTC | A, 70.38 | L5, Wealth 33.7, Skill 117, Risk Control weighted 10.0, Network 44 |
| Fourth run | V0.4 experiment, 2026-10-20 20:29:02 UTC | C, 59.85 | L4, Wealth 21.4, Skill 92, Risk Control weighted 10.0, Network 36 |
| Fifth run | V0.5.1 experiment, 2026-10-21 22:07:34 UTC | C, 50.40 | L4, Wealth 17.6, Skill 80, Risk Control weighted 3.0, Network 36 |
| V0.3.3 replication | V0.3.3, 2026-10-21 23:52:42 UTC | B, 69.76 | L5, Wealth 37.7, Skill 116, Risk Control weighted 9.0, Network 41 |

All four runs completed 48 months. These are individual trajectories with different event sequences; score differences alone do not establish that a Skill change caused an outcome.

The public rules do not specify a numeric score-to-final-grade cutoff. Do not infer a universal 70-point A threshold from the two V0.3.3 results.

## Included artifacts

- `run4-v0.4-20261020T202902Z/`: fourth-run event log, transcript and score report.
- `run5-v0.5.1-20261021T220734Z/`: fifth-run event log, transcript and score report.
- `v0.3.3-replication-20261021T235242Z/score_report.json`: score report supplied for the latest V0.3.3 rerun. Its event log and transcript were not included in the supplied materials at the time of this commit.

For strategy comparisons, derive hypotheses from repeated state/action/outcome evidence, but do not encode a prior run's month-specific action sequence as a future decision script. Each action should be selected from the current observation, actual event/menu, current risk evidence, marginal stat changes and remaining horizon.
