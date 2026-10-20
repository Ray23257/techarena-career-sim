# The Raytirement Plan — Career Survival V0.3.3

## Scope and status

One JiuwenSwarm Agent, four Skills, native Career Emulator MCP. No runtime Python router, Symphony or sub-agents. V0.3.3 is an uninstalled engineering revision with no new game or measured score improvement. V0.3.2 run two stopped after M2 actions, entering M3, because its framework-ID storage binding was truncated. It has no settlement; its original records remain protected.

The preserved V0.2 baseline completed 48 months: grade B, quantitative score 63.02, competition partial score 44.12. Risk control contributed only 1/10. Its Runner exit was abnormal (`max_continuations`) after Bash-mediated MCP calls; successful game settlement did not validate the original native Agent integration.

## Submission contents

- `manifest.json`: exact registered team, `mode: agent`, persistent global constraints and controller entry point.
- `skills/career-controller/SKILL.md`: routing, compact durable state, arbitration, native execution and recovery.
- `skills/risk-management/SKILL.md`: warning evidence, delayed risks, mitigation and follow-up.
- `skills/career-planning/SKILL.md`: Level/Wealth priorities, six-month history and event choices.
- `skills/resource-optimisation/SKILL.md`: feasible Energy sequences, caps and resource trade-offs.
- `design/skills_design.md`: interfaces, routing contract and state lifetime.
- `design/decision_report.md`: baseline evidence, changes, unknowns and evaluation plan.

The archived `career-survival` V0.2 Skill is outside this submission. The four current Skills are documents read by the same Agent, not four executors. The installed instance remains unchanged until a separately approved installation.

## Runtime state and Skill reading

At entry/recovery read the controller with `skill_tool`. Read a specialist only when needed and its body is unavailable; reuse relevant methods while present. `skill_mode: all` lists metadata rather than injecting every body. Context compression can lose details despite recent-Skill reinjection. The manifest remains the short recovery anchor through generated IDENTITY.md.

V0.3.3 uses only the complete framework-injected no-project cwd D, validated as `<Agent internal data directory>/projects/career-sim-runner-<12 lowercase hex>`. It uses fixed `D/career-checkpoint.json`; it no longer extracts a framework ID for a filename or stores framework_session_id in JSON. Compare directory fields and actual returned file paths independently with injected D. verified_directory is D; verified_path is the complete state file path, not the directory. A new reservation has a null game ID/path; after successful native new_game, both marker and `D/career-state-<real-game-UUID>.json` must bind the exact returned UUID and full state path. Schema 2 / solution_version 0.3.3 rejects legacy records; no automatic migration is allowed. File operation success alone does not establish semantic correctness. The startup direct budget remains seven calls; it is not an atomic lock or a guarantee of model obedience.

Only a positively confirmed initial Runner request in a newly allocated conversation can qualify as fresh. An existing marker, previous scope, uncertain create or automatic continuation blocks new_game. Missing marker or missing state during recovery is a halt, not a new-game condition. Do not scan other scopes or legacy names. The known run-two framework `career-sim-runner-7a72e52cc135` and game `cc0ca28b4e694fd993c60b538aac3c80` are explicitly protected from file/game operations by this revision. This change does not authorize their recovery, repair or abandonment.

Checkpoint material warnings and serious visible vulnerability even without a warning: Network=0, for example, must be recorded before another game call. This is a persistence policy, not a claim of immediate failure or a hidden threshold. Repeated identical evidence can coalesce; actual improvement is recorded without declaring hidden risk cleared. Review/promotion, strategic switch, execution uncertainty and ending triggers remain; ordinary successful actions still have no mandatory pending-file write.

On a recoverable interruption (without a latched engineering halt), EVERY recovery reconciles native observe and recent logs before any action, regardless of saved pending status. A latched engineering halt needs explicit operator repair/authorization; generic Runner continuations cannot clear it. Logs can lag saved game state; absent logs or unchanged stats do not authorize replay. If progress/history cannot be established, stop instead of reusing an old choice. Native file durability and Agent recovery still need actual execution acceptance.

Career Planning now includes explicit review-feedback branches and evidence-based comparison of main actions. Resource Optimisation directly shortlists at most three distinct proposals; the model is not asked to enumerate 112 sequences. These are unproven policy changes, not measured score improvements.

## Safe offline checks

From the project root, use the already installed interpreter:

```powershell
.\.venv\Scripts\python.exe -B -X utf8 offline_tests/test_v03.py
```

The test file is outside `solution/` and excluded from the competition bundle. It reads files and exercises isolated pure official functions plus explicit policy reference cases. It does not import JiuwenSwarm, initialize an Agent, connect to services, run the CLI validator, invoke models, create game data or prove that an LLM follows these instructions.

## Installation and any future game — separate approval required

Do not run setup to install Skills: setup can overwrite the repaired MCP command. Back up evidence first because official installation clears sessions and parts of the instance workspace. Install only into `career_emu` using the existing Runner after approval. Keep the model and locked dependencies unchanged.

An approved `play --submission solution` installs Skills and reloads Agent configuration. A past successful MCP probe does not guarantee registration survives that reload. Verify the repaired absolute MCP executable, five native tools and schemas, actual four-Skill visibility, and registration stability after any approved install/reload. No Bash fallback is permitted. Missing native tools are an engineering stop condition.

No installation is authorized now: official install can clear the protected run-two session. Before any later installation, obtain explicit approval of an evidence-preserving plan. Recovery of run two and allocation of a new game are distinct decisions; neither is implied by reviewing this package. Only after the applicable gates and separate authorization may one simulation proceed, without an automatic retry. Inspect native `chat.tool_call` / `chat.tool_result`, Skill read success, event-triggered state writes/restoration and replay fencing, one game session and the final native observe. Preserve events, transcript, emulator log and score report. Report cost only from reliable billing/usage evidence: the old report's `total_cost: 0` is not proof of free API use.

Package only this directory's contents, following the official final upload instructions. Do not include backups, runtime state, tests, credentials or old workspace clients.

## V0.3.3 acceptance boundary

Only Controller storage/bootstrap, persistence clarification and their global/document/test contracts changed. Three specialist bodies are byte-identical to V0.3.2. Runtime source supports per-conversation path isolation only in the checked no-project branch with one driver; it is not an OS sandbox. Bound-project/custom cwd, concurrent drivers, path aliases/symlink or cwd changes remain unsupported. The model can still fail to apply an equality check: deterministic offline examples do not enforce actual tool calls. A lost/unreturned game UUID, missing state or inability to prove safe execution requires operator intervention. The unmodified Runner can continue after an engineering report until externally stopped. No live V0.3.3 storage, recovery or terminal behavior has been accepted.
