# Career Survival Agent

**Team:** The Raytirement Plan  
**Run mode:** One JiuwenSwarm agent (`agent`) coordinating four Skills.

This submission is designed for the 48-month Career Survival simulation. It uses the current game observation and registered native tools to choose legal actions, pursue career and wealth outcomes, and protect against early failure and clearly evidenced major losses.

## Included Skills

- **Career Controller** coordinates the four Skills, preserves the confirmed game session, checks current legality, executes one action at a time, and observes the result.
- **Career Planning** advises on story choices, quarterly Main Actions, review feedback, career evidence, and financial trade-offs.
- **Resource Optimisation** compares feasible uses of the current quarterly Energy budget, using observed marginal effects and public caps.
- **Risk Management** is the sole source of risk judgments and mitigation advice. It distinguishes follow-up status from urgency and does not treat every ordinary warning as a veto.

The Skills use no auxiliary scripts or reference files. Gameplay relies on the official native Career Emulator tools and the state and feedback returned during the current run.

## Submission boundaries

The strategy does not encode a fixed event or action sequence, unpublished promotion thresholds, or assumed cloud scoring formulas. It treats the official qualitative outcome guidance as direction, not as numeric weights. Local historical results are development evidence, not guarantees of official performance.

See `design/skills_design.md` for the division of responsibility and `design/decision_report.md` for the decision approach and evidence limits.
