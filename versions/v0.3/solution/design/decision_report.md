# V0.3 decision report

## Measured V0.2 baseline

One 48-month game completed: B, quantitative score 63.02, competition partial score 44.12. Session: `a86e8ff1b7924a598bc63422d52afd69`. Evidence is in `.career_sim_runner/career_emu/outputs/The Raytirement Plan/20261019T214724Z/` and the matching emulator log.

| Local dimension | Observed weight | Normalized score | Weighted contribution |
| --- | ---: | ---: | ---: |
| Level | 30% | 50 | 15 |
| Wealth | 20% | 43.88 | 8.78 |
| Health/Dignity | 15% | 90 | 13.5 |
| Skill | 15% | 98.33 | 14.75 |
| Risk Control | 10% | 10 | 1 |
| Network | 10% | 100 | 10 |

These are the actual local report's values. Exact promotion/performance formulas, hidden failure counters, hazard values and future event outcomes remain unknown. Local weights do not reveal promotion weights or the full cloud scoring rule. No improvement has been measured for V0.3.

The old run used Bash clients, and the Runner returned `play_exit_code: 1`, `termination_reason: max_continuations` despite completed settlement. Its reported input/output tokens were 43,039,082 / 143,499. Reported `total_cost: 0` is not reliable evidence of zero billing. Native MCP registration was subsequently repaired at framework level; the full Agent path remains to be verified during an authorized run.

## Evidence and proposed changes

| V0.2 evidence | V0.3 response | What is not established |
| --- | --- | --- |
| Risk normalized 10/100; repeated severe warnings; risk explosion in emulator log line 711 | Durable scoped risk ledger, relevant mitigation before optional gains, reassessment after intervention | Exact hazard value, causal contribution of each event, quantitative score benefit of mitigation |
| Notes repeatedly called Output the bottleneck because its raw number was smaller | Use explicit feedback and within-stat trends; retain all review windows | Hidden promotion thresholds or guaranteed optimal allocation |
| S review without promotion; long stays at L3/L4 | Start review preparation early, track tenure and actual promotion feedback separately | S grade as eligibility, a fixed tenure gate |
| 48 Energy spent; 21 report actions, 10 health recoveries, 4 defuses, 1 network maintenance, 4 intensive-work actions | Compare feasible sequences, caps and opportunity costs | Zero Energy as evidence of waste; permanent dominance of one action |
| Final-month intensive work/report/project still justified through promotion | Check whether final review already resolved and compare direct terminal benefits | A ninth review or guaranteed late promotion |
| Temporary clients bypassed native structured tool events | Native-only instructions, missing-tool stop, final native observe | End-to-end model compliance before another actual run |

The action counts above are baseline audit observations, not a required future pattern. Promotion first appeared in observations at months 6, 12, 24 and 42. Baseline feedback may be processed before the same month's later quarterly choices; public handbook ordering is approximate. Use actual phase and returned feedback, not a retroactive claim that a later action changed an earlier review.

## Public rules and policy hypotheses

Public: 48 months, 3 non-carrying Energy per quarter, repeat Energy actions while offered, one quarterly main action or none, six-month reviews/promotion windows, higher salary at higher Level, Health/Dignity caps of 10, and the broad failure directions. The public bonus table gives grade directions; actual Wealth amounts must come from returned results rather than assuming that table entries are exact currency.

Hypotheses to test: earlier preparation can improve advancement and cumulative salary; persistent risk evidence can improve risk control; feasible-sequence comparison can reduce avoidable resource costs; concise notes and correct native termination can improve resource efficiency. None is a demonstrated V0.3 score improvement. A risky choice is not automatically wrong merely because its realized outcome was bad.

Risk statuses and urgency classes, pending-intent checkpoints, the local observation_revision and the notes length target are our policy bookkeeping. They are not official engine fields, counters or hidden thresholds. Skill/Network settlement normalization does not imply an in-game cap or promotion sufficiency.

## Phase-one verification

Pure offline tests cover current source contract functions isolated with AST, actual JSON/YAML, four-Skill routing contract and scenarios, risk-status continuity, Energy budget/cap examples, session isolation, review timing fixtures and native terminal parsing using the preserved actual ending payload. They neither call the CLI validator nor import/initialize JiuwenSwarm, a model, MCP or the simulator.

Behavioral reference cases check policy consistency, not that the natural-language Agent will implement them. No framework/LLM test and no V0.3 game is part of phase one. File-tool durability, skill reading, compression recovery, stable MCP after install/reload and final native Agent events remain acceptance items.

## Next authorized experiment

1. Preserve V0.2 source/evidence and verify V0.3 static checks. The first-run temporary clients are archived and removed only after checksum verification; official output/log/database evidence stays intact.
2. Separately approve installation into career_emu. Do not run setup or upgrade dependencies. Check absolute MCP command and native registration after installation/configuration reload, because prior hot reload removed tools.
3. Verify four installed Skill directories, metadata, descriptions and actual native tool schemas. A file installed is not proof a Skill was read or followed. File-tool state save/restore needs actual execution verification.
4. After run authorization, run exactly one V0.3 game. Audit successful Skill reads, one new session, native calls, concise notes, pending/result reconciliation, risk/review history and native terminal recognition. Stop on renewed bypass/registration errors; do not silently replace a failed run.
5. Compare Level, Wealth and risk contribution with the baseline; also survival, other dimensions, review timing, Energy use, native-tool errors and token usage. Separate engineering savings from strategy improvement: V0.2 had abnormal continuation overhead, so total token differences alone do not isolate strategy effects.
6. For later separately approved comparisons change one policy at a time and record model, data/package versions and snapshot hashes. The current new_game API exposes no seed argument; do not claim paired identical-seed trials. Multiple runs may be needed to separate randomness from benefit. Never infer hidden formulas from a single result.
