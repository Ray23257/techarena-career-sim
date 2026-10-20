# V0.4 Strategy Experiment — Review Report

## Status

V0.4 is a strategy experiment source bundle for **The Raytirement Plan**. It retains `mode: agent`, one Agent, four Skills, and the five native Career Emulator MCP tools. The manifest's displayed name is updated; its global instruction is unchanged. The Controller and Risk Management Skills are unchanged from the V0.3.3 review archive. The version has **not** been installed or run. No setup, install, reload, play, game MCP call or model API request was made.

## Evidence used

The review uses the read-only `career-strategy-evidence.zip`, first and third game score reports, event traces and transcripts, the prior third-game audit as a locator aid, and public `docs/rules.rst`, `docs/handbook.rst` and `docs/failure-and-ending.rst`.

- Game 1, UUID `a86e8ff1b7924a598bc63422d52afd69`: B / 63.02, L5, Wealth 35.1, Risk Control 1/10.
- Game 3, UUID `e173ebcb61964fa58385148cc424e206`: A / 70.38, L5, Wealth 33.7, Risk Control 10/10.
- Both runs promoted at M6, M12, M24 and M42. The shared dates do not establish a minimum-tenure rule or promotion formula.
- Game 3 had no promotion at M18 (B), M30 (B; “do not look like you only hustle without winning”) or M36 (A; “first on my list”), then promoted at M42 (A). The evidence shows that grade and advocacy alone did not guarantee promotion; the decisive factor is unknown.
- The third-game trace recorded 27 report-preparation calls, 13 key-project main actions, 9 Health recoveries and 4 Network-maintenance actions; no Skill-study action label was found in the matched event names. These counts describe usage, not action effectiveness. The M15 Energy bundle is incomplete and remains `UNKNOWN` in the evidence CSV.
- Network fell from 7 to 4 after the M12 promotion, later reached 36 by M36 and 44 at the ending. Visible Health recovered from a low of 3 to 10. Neither fact proves that hidden risks or relationship friction were cleared.

Public rules state the local score weights used for this experiment (Level 30%, Wealth 20%), the six-month review schedule, the quarterly three-point Energy budget, and directional action costs/effects. They do not publish promotion thresholds, tenure gates, exact numeric action deltas, or action-specific promotion probabilities.

## V0.3.3 → V0.4 changes

| Area | V0.3.3 | V0.4 experiment |
| --- | --- | --- |
| Career Planning | Sustainable Level/Wealth priority and general feedback branches | Adds a more explicit early career-capital focus; turns M18/M30/M36 into evidence-led review branches; compares delivery, visibility, capability/scope and relationship actions; prevents automatic work intensification after strong grades without promotion; makes L5 by M36 and exploration of L6 at a real remaining review hypotheses only. |
| Resource Optimisation | Up to three feasible proposals with risk, cap and dominance screening | Sends the current Career Planning objective into the shortlist; explicitly compares Skill study, reporting, Network maintenance and optional intensive work using public costs/directions; protects risk mitigation and targeted post-promotion recovery; pivots after the actual M48 review is processed. |
| Controller / Risk Management | V0.3.3 session storage, recovery, native-tool and risk constraints | No change. Checkpoint protocol, true game UUID binding, uncertainty/replay fence, termination behavior and risk ledger remain intact. |
| Manifest / architecture | One Agent, four Skills, team `The Raytirement Plan`, agent mode | Same team/mode/instruction and architecture. Only the displayed manifest name changes to `Career Survival V0.4 Strategy Experiment`. |

Neither Skill forces project repetition, quarterly study/reporting, intensive work, or a fixed action rotation. The Agent must use current menus and returned effects. No unknown future outcome or numerical marginal value is invented.

## Offline verification

Executed the complete offline suite with the already-installed project interpreter:

```powershell
.\.venv\Scripts\python.exe -B -X utf8 offline_tests/test_v03.py
```

**140 passed, 0 failures, 0 errors.** This comprises 131 existing test method names and 9 additional V0.4 document/policy consistency checks. The preservation check was made phase-aware: immutable backups and the unfinished run-two session are checked, while mutable live installation/game indexes are no longer compared against their older pre-deployment values.

The suite checks JSON/YAML/frontmatter, manifest constraints, four-Skill packaging, Controller and Risk Management preservation against the immutable V0.3.3 archive, and strategy text contracts. Other existing tests exercise isolated official functions and deterministic reference fixtures. These checks do **not** invoke an Agent, LLM, MCP server, simulator or live file tool. A passing reference test does not prove the model will follow the Skill.

## Falsifiable next-run hypotheses

1. **Feedback-targeted main action:** after “hustle without winning” feedback, an offered action that supplies evidence of an outcome, leadership visibility or a specifically stated need improves the next review's readiness or promotion versus an unexamined project/report repeat. Record the action family, actual deltas, review grade, promotion and feedback.
2. **Career-capital Energy:** where no severe risk constraint applies and visible Health makes costs tolerable, considering Skill study or Network maintenance alongside reports improves pre-review Skill/Network without a worse Health or warning trajectory. Record every Energy choice/cost and subsequent observation/review; do not attribute an overlapping story delta to one action.
3. **Post-promotion recovery:** after an observed Network or Health decline, targeted offered recovery improves that visible metric by the next review without recurring severe warnings. Keep visible recovery separate from claims about hidden-risk clearance.

There are only two completed runs and no matched-seed guarantee. Random event traces, model choices and other run differences confound the comparison. V0.4 has no measured score, promotion, Token or risk-control improvement. A future game requires separate authorization and should preserve the existing one-game safety gates and all historical records.
