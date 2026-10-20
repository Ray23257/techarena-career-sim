# V0.3 Skill design

## Boundaries

The official Runner installs the Skill Bundle, generates IDENTITY.md, drives the conversation, collects logs and recognizes structured MCP game signals. IDENTITY already describes the basic observe/action loop and session reuse. Our controller adds state retention, routing, arbitration and uncertain-action recovery; it is not another game runner.

One Agent reads four documents. Specialists do not independently execute tools. No runtime Python, Symphony, sub-agent or parallel game-action orchestration is part of this bundle. These are instruction-level constraints, not separate tool permission sandboxes.

## Loading and context

The installed jiuwenswarm 0.2.4b3 / openjiuwen 0.1.16.post2 scans multiple Skill directories. `skill_tool` reads one named Skill/file at a time. `react.skill_mode: all` publishes descriptions, not full bodies. Session Skill metadata and checkpoints do not prove body retention or compliance. Compressors attempt to reinject recent Skill reads but do not guarantee all four full texts remain available.

Manifest instructions are rendered into IDENTITY.md and assembled into the model system context. Keep global native-MCP/session/terminal invariants and the controller recovery entry there. At entry and continuation/compression re-read the controller; restore only the current session state and load missing relevant specialist bodies. Do not re-read all Skills every quarter merely because time passed.

## Routing and advice contracts

Controller uses the actual event/menu and feedback to choose the route, not an assumed month-only schedule. Risk screening and career priorities apply to every nonterminal choice; Energy adds resource comparison. Review feedback is consumed before changing future targets. New risk evidence is handled before optional benefits.

Advice shares the local `observation_revision`, not an official server field or idempotency key:

- Risk: blocked/preferred current choices, scoped evidence, ledger changes and unknowns.
- Career: current objective, preferred choices, opportunity costs and unknowns.
- Resources: feasible tentative sequences, known effects/costs, a next current choice and remaining budget.
- Controller: reconciles the above, checks the newest menu and submits one action with concise notes.

A hard constraint requires evidence of explicit failure or the documented conservative severe-risk policy. Minor/unknown risk is advisory. Do not sum invented utilities or vote across the specialist methods. The ranking is legality/session/terminal safety, evidenced severe survival risk, risk-control improvement with long-term Level/Wealth, then other scored dimensions and efficiency.

## Session-isolated state

The controller contains the complete JSON example and write schedule. Filename: `career-state-<session_id>.json` in the current task's assigned working directory, resolved from runtime context and checked for filename safety. No path is hardcoded and no other session's summary is read or overwritten. A missing/malformed/mismatched file never authorizes a new game.

Preserve actual time/status, unresolved risk entries, all observed half-year reviews, current objective, confirmed quarterly spending, tentative remaining plan and pending/uncertain action. Keep risk labels and planning hypotheses explicitly separate from simulator fields. Store no credentials or full conversation dump. First/latest warning evidence plus material changes is enough; retain all unresolved issues and scoped mitigation history.

Checkpoint session binding, material warning/review updates, errors/uncertainty and ending. Before each action persist pending intent. Coalesce adjacent reasons with no game call between them. Normal observations need no separate read/write. After success update memory and include confirmation in the next required checkpoint; after a crash a stale pending record is reconciled using native observation/logs, never replayed blindly. If required persistence fails, stop before the next action and report.

Observe consumes pending warnings. An empty `events` cannot erase the ledger. A successful mitigation does not reveal the hidden residual value. Old history that cannot be reconstructed stays unknown. Official installation clears some sessions/memory, so this design promises recovery within a session with its file, not preservation across arbitrary reinstall/reset.

## Termination

Always obtain native observe after a successful action, including the last. The Runner recognizes the native prefix and structured `raw_output.result`, not printed DONE or Bash JSON. On terminal observe persist exact ending information, classify completion using `ending_score.completed` rather than `failed` alone, and stop game calls. The baseline terminal month counter was 49 while survival_months was 48.

## Offline policy contract

The following data encodes the documented routes, public budgets and our status labels for offline consistency/scenario tests. It is not a runtime router, official schema, executable policy in the submitted Agent, hidden formula or guarantee of model compliance. The test harness also checks the Skill text against these entries.

<!-- offline-policy-contract -->
```json
{
  "version": "0.3",
  "routes": {
    "entry": [
      "career-controller"
    ],
    "story": [
      "risk-management",
      "career-planning"
    ],
    "warning": [
      "risk-management",
      "career-planning"
    ],
    "energy": [
      "risk-management",
      "career-planning",
      "resource-optimisation"
    ],
    "main": [
      "risk-management",
      "career-planning"
    ],
    "review": [
      "career-planning",
      "risk-management"
    ],
    "recovery": [
      "career-controller"
    ],
    "uncertain": [
      "career-controller"
    ],
    "terminal": [
      "career-controller"
    ]
  },
  "risk_statuses": [
    "unresolved",
    "mitigation_pending",
    "monitoring",
    "resolved_explicit"
  ],
  "risk_transition_events": {
    "warning": "unresolved",
    "mitigation_intent": "mitigation_pending",
    "mitigation_success": "monitoring",
    "explicit_scoped_resolution": "resolved_explicit"
  },
  "risk_preserve_events": [
    "empty_events",
    "benign_feedback"
  ],
  "energy_costs": {
    "intensive_work": 2,
    "skill_study": 2,
    "network_maintenance": 1,
    "defuse_landmines": 2,
    "mental_recovery": 1,
    "health_recovery": 1,
    "prepare_report": 1
  },
  "public_caps": {
    "health": 10,
    "dignity": 10
  },
  "review_months": [
    6,
    12,
    18,
    24,
    30,
    36,
    42,
    48
  ],
  "state_schema_version": 1,
  "action_statuses": [
    "none",
    "pending",
    "confirmed",
    "rejected",
    "uncertain",
    "terminal"
  ],
  "state_filename": "career-state-<session_id>.json",
  "checkpoint_reasons": [
    "session_bound",
    "risk_changed",
    "review_observed",
    "execution_uncertain",
    "action_rejected",
    "before_action",
    "terminal"
  ],
  "notes_target_chars": 300
}
```

## Source map

- `career_sim_runner/skill_contract.py`: bundle enumeration, manifest and frontmatter checks.
- `career_sim_runner/install.py`: copy each Skill tree, write IDENTITY and clear selected workspace/session files.
- `career_sim_runner/prompts/identity.md`: existing loop/session/recovery instructions.
- `career_sim_runner/ws_client.py`: native structured game/terminal recognition.
- Installed `openjiuwen/harness/tools/skills/skill_tool.py` and `rails/skills/skill_use_rail.py`: reading, metadata and persistence.
- Installed `openjiuwen/harness/rails/context_engineer/context_assemble_rail.py` and `core/context_engine/processor/forked/compressor/reinjection/builders.py`: identity injection and bounded Skill reinjection.
- `docs/handbook.rst`, `docs/rules.rst`, `docs/failure-and-ending.rst`: public rules, approximate timing and unknown mechanisms.

The auxiliary tests are outside the submission and do not import framework modules. File-format tests and policy reference cases are not an end-to-end Agent test.
