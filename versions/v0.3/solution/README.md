# The Raytirement Plan — Career Survival V0.3

## Scope and status

One JiuwenSwarm Agent, four Skills, native Career Emulator MCP. No runtime Python router, Symphony or sub-agents. V0.3 has not played a game and makes no measured improvement claim.

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

Use `career-state-<session_id>.json` in the task's assigned working directory, never this source directory or a fixed Windows path. Validate its session ID when restoring. Checkpoint binding, material risk/review changes, uncertain actions, terminal state and pending intent before execution. Ordinary observations stay in memory. The controller gives the complete schedule and reconciliation procedure. Native file-tool persistence and compression recovery still require actual Agent verification.

## Safe offline checks

From the project root, use the already installed interpreter:

```powershell
.\.venv\Scripts\python.exe -B -X utf8 offline_tests/test_v03.py
```

The test file is outside `solution/` and excluded from the competition bundle. It reads files and exercises isolated pure official functions plus explicit policy reference cases. It does not import JiuwenSwarm, initialize an Agent, connect to services, run the CLI validator, invoke models, create game data or prove that an LLM follows these instructions.

## Installation and second-run gate — future approval required

Do not run setup to install Skills: setup can overwrite the repaired MCP command. Back up evidence first because official installation clears sessions and parts of the instance workspace. Install only into `career_emu` using the existing Runner after approval. Keep the model and locked dependencies unchanged.

An approved `play --submission solution` installs Skills and reloads Agent configuration. A past successful MCP probe does not guarantee registration survives that reload. Verify the repaired absolute MCP executable, five native tools and schemas, actual four-Skill visibility, and registration stability after any approved install/reload. No Bash fallback is permitted. Missing native tools are an engineering stop condition.

Only after those gates and separate authorization run one simulation, not an automatic retry. Inspect native `chat.tool_call` / `chat.tool_result`, Skill read success, state writes/restoration, one game session and the final native observe. Preserve events, transcript, emulator log and score report. Report cost only from reliable billing/usage evidence: the old report's `total_cost: 0` is not proof of free API use.

Package only this directory's contents, following the official final upload instructions. Do not include backups, runtime state, tests, credentials or old workspace clients.
