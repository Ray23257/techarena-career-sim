# Run 04 vs Run 05 — Evidence-Based Comparison

Date: 2026-10-22  
Scope: V0.4 run at `20261020T202902Z` and V0.5.1 run at `20261021T220734Z`. Both completed 48 months. The event paths were not matched by a controlled random seed, so this is a descriptive comparison, not a causal estimate.

## 1. Final results

| Metric | Run 04 / V0.4 | Run 05 / V0.5.1 | Difference |
|---|---:|---:|---:|
| Final grade | C | C | — |
| Quantitative score | 59.85 | 50.40 | -9.45 |
| Final Level | L4 | L4 | — |
| Wealth raw | 21.4 | 17.6 | -3.8 |
| Health + Dignity raw | 20/20 | 20/20 | — |
| Skill raw | 92 | 80 | -12 |
| Risk Control | 10/10 (raw 0) | 3/10 (raw 7) | -7 |
| Network raw | 36 | 36 | — |

The 9.45-point score gap decomposes into Risk Control -7.00, Skill -1.50 and Wealth -0.95. Level, Health & Dignity, and Network contribute the same final weighted score in both runs. The risk-control difference is the largest visible component of the final-score gap.

## 2. Promotion timeline

| Review | Run 04 / V0.4 | Run 05 / V0.5.1 |
|---|---|---|
| M6 | C, no promotion | C, no promotion |
| M12 | L1→L2 | L1→L2 |
| M18 | L2→L3 | C, remains L2 |
| M24 | no promotion | L2→L3 |
| M30 | L3→L4 | B, remains L3 |
| M36 | no promotion | L3→L4 |
| M42 | L4, no promotion | B, remains L4 |
| M48 | terminal review | terminal review; remains L4 |

Run 05 reached L3 and L4 one review window later than Run 04. Both missed the M6 promotion seen in the V0.2 and V0.3.3 baselines. This pattern is a useful hypothesis, but two different stochastic traces cannot identify a causal reason.

## 3. Main Action flexibility

| Main Action | Run 04 | Run 05 |
|---|---:|---:|
| Key Project | 10 | 16 |
| Report results to manager | 4 | 0 |
| Build a mentorship | 1 | 0 |
| Apply for rotation | 1 | 0 |

Run 05 selected Key Project in all 16 quarterly Main Action phases. Key Project is not inherently wrong; it can raise several career attributes. The concern is the lack of observable adaptation after repeated non-promotions and repeated feedback that work was not translating into sufficiently clear outcomes. Run 04 used four action families, although this alone does not prove its choices were better.

## 4. Repeated Energy actions and marginal utility

The Run 05 audit records:
- At M15, three Prepare Report actions: Output rose from 5 to 6; the next two repeats had no additional immediate visible gain.
- At M33, three Prepare Report actions: Output rose from 15 to 16; the next two repeats had no additional immediate visible gain.
- Defuse legacy risk at M27, M39 and M45 cost 2 Energy and had no immediate visible attribute change.

This is stronger evidence of low marginal efficiency than a general claim that the model always wastes Health Recovery. The decision rule should stop repeating an action when the latest observation shows no incremental visible effect, unless a separately evidenced delayed benefit justifies it. The logs do not establish whether any hidden delayed benefit existed.

## 5. Important correction: final Health score does not prove cap-waste

Both runs finished with Health + Dignity = 20/20. However, the recorded selected Energy actions show **no Health Recovery chosen when pre-action Health was already 10** in either run. Health Recovery was generally chosen when visible Health was lower. Therefore, the final full resilience score is not evidence that these two runs actually spent Energy on Health Recovery at a full Health cap.

The broader cap-awareness requirement remains valid: recalculate the real marginal gain from the latest state, including clipped Dignity components, rather than counting an action's nominal full benefit.

## 6. The M43 risk event in Run 05

The Run 05 event trace shows the state immediately before the landmine event at M43 with Wealth 19, Output 25 and Dignity 10. The next observed state is Wealth 13, Output 21 and Dignity 8, accompanied by the message that old landmines detonated together. Health remained 10. This is consistent with a severe accumulated-risk event and is an important explanation to investigate for the final Risk Control raw value of 7 and lower Wealth.

It does **not** prove which earlier choice caused the event, or that any single Defuse action would have prevented it. The visible record shows several Defuse actions, yet the risk event still occurred. The next audit should examine whether the risk ledger represented multiple unresolved risks and whether mitigation status was verified after each intervention.

## 7. Cross-Skill handoff and feedback-loop evidence

The Run 05 audit records one successful Skill read for each of the four Skills. Later HR warnings and risk changes occurred during the game, but the trace does not show a fresh Risk Management Skill read after those later warnings. The Controller's routing rule calls for reloading Risk Management when risk status is unresolved or its context is missing. This is a trace-level compliance gap to investigate; it does not prove the Skill body was unavailable in the model's context, but it means the logs do not demonstrate a fresh risk reassessment at those points.

The actual action pattern also suggests weak end-to-end replanning: Career Planning repeatedly chose Key Project, Resource Optimisation repeated Prepare Report even after zero immediate visible gains, and Risk Management selected Defuse on several warning windows. Those actions can complement one another, but the run does not show a reliable shared stop condition or a verified post-mitigation risk status. The problem is better described as **insufficiently enforced coordination and feedback**, not proven contradictory Skill text.

## 8. Next testable changes

1. **Action repetition gate:** after every action, observe again and compare actual before/after state. If marginal gain is zero, do not repeat the same action unless the agent names a concrete delayed benefit and a check that can validate it.
2. **Promotion feedback pivot:** after a missed promotion or repeated “clearer outcomes” feedback, require a fresh diagnosis of delivery, visibility, scope, relationships and risk before choosing another Main Action.
3. **Risk accumulation audit:** preserve each distinct risk source, urgency, mitigation attempt and verification result. One Defuse action must not be treated as proof that every legacy risk is cleared; new warnings should trigger an explicit Risk Management reassessment.
4. **Cap-aware resource allocation:** calculate marginal gain after caps and costs; a final score of 20/20 is not a substitute for quarter-by-quarter state inspection.

## Evidence limits

The raw event logs, transcripts and score reports are archived alongside this report. The runs differ in events, choices and model sampling; no matched-seed experiment was performed. Promotion thresholds and hidden-risk mechanics remain unpublished. Conclusions above distinguish observed behavior from hypotheses.
