# Run 05 — V0.5.1 Controlled Experiment

- Run timestamp: `20261021T220734Z`
- Outcome: completed 48/48 months
- Final grade: C
- Quantitative score: 50.40/100
- Final Level: L4
- Wealth raw: 17.6
- Code-change hashes and V0.5.1 strategy context: [implementation audit](../../../reports/v051-implementation-audit.md) and [strategy research](../../../reports/v051-strategy-research.md)

## Evidence

- [Raw event log](events-20261021T220734Z.jsonl)
- [Agent transcript](transcript-20261021T220734Z.log)
- [score_report.json](score_report.json)
- [Final run audit](final-audit.md)

Source SHA-256 values recorded in the final audit:
- Events: `f7913bcb0868507a19f78353b30eb44e00d6f2ebbabe82ee50f1721b848558ed`
- Transcript: `ffeeb3641b18f937c179194f1be75fad50ecbb82eb09864d22847d727bbace1`
- Score report: `27352587622e71a7d66eb3cfb3e03f37efd02fe27cf64c832bfcf574f4f9372`

Important observed behavior: all 16 quarterly Main Actions were Key Project. At M15 and M33, the first Prepare Report produced an immediate Output increase, while the next two repetitions produced no additional immediate gain. At M43, accumulated hidden risks detonated and the visible state lost Wealth, Output and Dignity. See the audit and comparison report for evidence and limitations.

This is one stochastic run; the result does not prove that V0.5.1 caused the lower score.
