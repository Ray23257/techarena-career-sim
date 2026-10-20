# Career Survival: Minimal Agent Submission

This submission uses JiuwenSwarm's `agent` mode with one Skill, `career-survival`. The Skill supplies a repeatable decision loop for the 48-month Career Emulator game. It uses the current observation and handbook as evidence and does not encode guessed scoring weights or hidden mechanics.

## Contents

- `manifest.json` identifies the registered team, submission, run mode, and agent instruction. Set `team` to the exact registered team name before packaging.
- `skills/career-survival/SKILL.md` contains the agent's game-playing procedure.
- `design/skills_design.md` explains the decision flow and constraints.
- `design/decision_report.md` records assumptions, unknowns, and the evaluation plan.

## Use with the local runner

Keep this directory at the repository path `solution/`. Once the manifest has the team's registered name and the existing `career_emu` instance is running, start a game with:

```powershell
.\.venv\Scripts\python.exe -m career_sim_runner play --submission solution
```

This direct runner command validates the submission, installs its Skill into the named JiuwenSwarm instance, reloads the agent configuration, runs one game, and writes transcripts, events, and a score report under `.career_sim_runner/career_emu/outputs/`. It can change the instance's installed Skill workspace and the emulator's run data. This instruction is for a deliberate future run; no game has been run for this submission yet.

The repository's `make play` target first upgrades `career-emulator-engine` and `career-emulator-techarena` and refreshes the engine dataset before it runs the runner. Use the direct command above when you want to use the versions already in the local environment.

For the competition upload, package the contents of `solution/` as one ZIP while preserving the relative paths shown above. Follow any final packaging instructions released with the starter kit.

## Results

No simulation or strategy evaluation has been run. This submission makes no performance claim.