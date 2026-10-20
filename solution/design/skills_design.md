# V0.3.3 Skill design

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
- Resources: at most three materially different feasible proposals after legality/risk/cap/dominance screening, known effects/costs, a next choice and remaining budget. No runtime exhaustive enumeration.
- Controller: reconciles the above, checks the newest menu and submits one action with concise notes.

A hard constraint requires evidence of explicit failure or the documented conservative severe-risk policy. Minor/unknown risk is advisory. Do not sum invented utilities or vote across the specialist methods. The ranking is legality/session/terminal safety, evidenced severe survival risk, risk-control improvement with long-term Level/Wealth, then other scored dimensions and efficiency.

## Session-isolated, event-driven state

V0.3.1 removes the V0.3 full pending-JSON write before every action. Native game results/logs carry ordinary action evidence; compact in-memory state supplies current reasoning. The controller specifies every checkpoint trigger and its file-call cost. No Token savings have been measured.

Storage is gated, not assumed. V0.3.3 validates the complete no-project cwd D from the framework Runtime Directory Context against injected internal-directory/projects plus the whitelist `career-sim-runner-[0-9a-f]{12}` for the final path component. Copy D directly; do not manufacture a framework ID or filename suffix. The fixed marker is D/career-checkpoint.json. No framework_session_id is stored. Independently validate the actual returned file path against D plus the constant basename and every directory field against original injected D. File-tool success or agreement between two model-generated strings is insufficient.

Marker keys are schema_version, solution_version, verified_directory, verified_path, game_session_id, phase and halted_reason. A same-request verified reserved marker has null game ID/path. Binding requires G from successful native new_game, P=D/career-state-G.json, marker phase=bound, marker/state IDs=G and full paths=P. verified_directory always means D; verified_path always means full P (null only for the reserved marker). State strategy.checkpoint repeats D/P, never a framework ID. schema_version=2 and solution_version=0.3.3 reject old records without migration. Runtime relative/UNC/dot/conflicting/custom/project-bound scopes halt. No directory scans or cross-framework recovery are allowed.

Only an independently confirmed initial Runner request in a newly allocated conversation can qualify as fresh; marker absence alone cannot. Existing reserved/halted/malformed/conflicting/unknown markers stop; a valid bound marker permits only state validation and native recovery, never new_game. A missing checkpoint or marker on recovery stops rather than reconstructing or recreating. V0.3.2's known run-two framework and game are expressly protected: no file/game access, repair, migration or recovery under this revision. Cross-task/reinstall durability is not promised.

Filename remains career-state-<session_id>.json, with the actual 32-hex game UUID, never a framework ID. Keep unresolved risks and compact mitigation history, observed reviews/promotions and feedback hypotheses, current state/budget and uncertain execution. observation_revision remains our local marker, not an engine idempotency key.

Write triggers are session binding, materially new/worse risk or confirmed mitigation/resolution, review/promotion, material strategic switch, execution ambiguity/substantive rejection, dirty handoff/reconciliation and terminal settlement. A trigger normally costs one compact write; review+promotion+new strategy in the same returned batch share it. Identical warnings without changed urgency/decision, ordinary successful actions and ordinary observations add zero file calls. Repeat last_seen updates flush with the next triggered write. No routine quarterly writes or write to clear each pending flag are required. Binding costs seven initial file calls: absence read + probe write/read-back + state write/read-back + marker update/read-back; there is no promised total because material risk/uncertainty events vary.

Every recoverable interruption without a latched engineering halt is a replay fence even with no pending file: native observe + recent logs count=10, with one count=30 expansion if needed. Those counts are retrieval budgets, not server limits. Compare session, phase/event/menu, ordered logs, results and notes where available. Game source saves state and appends story-action logs as separate operations; absence of logs and unchanged visible stats cannot prove no execution. If the last action is confirmed committed and current progress coherent, discard old intent and decide from the new menu. Otherwise stop after bounded reconciliation. This fail-closed rule prevents blind resubmission, but provides no transactional exactly-once guarantee or automatic crash recovery guarantee.

Observe consumes pending warnings; empty events never clear the ledger. Material evidence is saved before another game call. Serious visible vulnerability also triggers persistence without a warning: first observing Network=0, Health=0, Dignity=0 or Wealth below zero records the actual value/month/revision and evidence type. These are conservative persistence triggers, not invented hidden failure cutoffs. Material worsening, mitigation/improvement or explicit resolution is saved; identical unchanged evidence is deduplicated. No change to the risk-management specialist is required. If required nonterminal persistence fails, report and stop before another action; terminal persistence failure cannot reopen the game or suppress reporting the returned ending. Missing necessary history is not silently converted into a clean ledger. File-tool storage and Agent-level reconciliation still require authorized runtime acceptance.

## Career feedback and bounded resource comparison

After each actual review, record facts, compare within-stat changes and prior intervention, select one evidence-backed hypothesis, choose a fitting current main action and evaluate again at the next actual feedback. Severe risk overrides optional development; promotion triggers state reassessment; poor results versus weak visibility call for different candidates; A/S without promotion does not justify automatic Output escalation. Long Level tenure prompts hypothesis reassessment, not a tenure eligibility threshold. Project repetition is allowed when evidence still favors it; no diversification quota is used.

Candidate relevance comes from current descriptions/observed effects and feedback: projects/resources for delivery constraints, reports/publicity for recognized results needing visibility, mentors/rotation for documented capability/scope needs, repair for actual relationship damage, and low exposure/recovery where relevant. These links are testable policy hypotheses, not proven promotion causes.

For Energy, directly construct at most three protection/career/balanced proposals. Filter the offered menu and budget, apply serious-risk constraints, clip public Health/Dignity gains, deduplicate and remove only evidenced dominated candidates. Preserve material unknowns instead of fictitious numeric ranking. A two-call sequence is only a plan; execute its first choice, observe and replan. The offline exhaustive 112-sequence fixture remains solely as a budget regression test and is not an instruction for the model.

## Termination

Always obtain native observe after a successful action, including the last. The Runner recognizes the native prefix and structured `raw_output.result`, not printed DONE or Bash JSON. On terminal observe persist exact ending information, classify completion using `ending_score.completed` rather than `failed` alone, and stop game calls. The baseline terminal month counter was 49 while survival_months was 48.

## Offline policy contract

The following data encodes the documented routes, public budgets and our status labels for offline consistency/scenario tests. It is not a runtime router, official schema, executable policy in the submitted Agent, hidden formula or guarantee of model compliance. The test harness also checks the Skill text against these entries.

<!-- offline-policy-contract -->
```json
{
  "version": "0.3.3",
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
  "state_schema_version": 2,
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
    "promotion_observed",
    "strategy_changed",
    "execution_uncertain",
    "action_rejected",
    "reconciliation_changed",
    "dirty_handoff",
    "terminal"
  ],
  "notes_target_chars": 300,
  "no_checkpoint_events": [
    "ordinary_observe",
    "ordinary_success",
    "before_action",
    "revision_only",
    "unchanged_warning",
    "clean_handoff"
  ],
  "resource_max_candidates": 3,
  "feedback_focus_by_evidence": {
    "delivery": [
      "key_project",
      "push_resources"
    ],
    "visibility": [
      "leadership_report",
      "publicize_results"
    ],
    "capability": [
      "mentor",
      "job_rotation"
    ],
    "scope": [
      "job_rotation",
      "mentor"
    ],
    "relationship": [
      "repair_relationship"
    ]
  },
  "feedback_branch_priority": [
    "protect",
    "post_promotion",
    "feedback_targeted",
    "maintain_uncertain"
  ],
  "storage_gate_file_calls": 3,
  "binding_checkpoint_file_calls": 4
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

## V0.3.3 bootstrap source chain and limits

- Runner `headless_play.new_drive_session_id` generates a framework ID; `ws_client._build_envelope` sends it as envelope.session_id while params contain no cwd/project. `prompts/play_headless.md` supplies neither task ID nor directory.
- Installed adapter `_apply_runtime_config_stages` selects the no-project per-session directory with `common.utils.get_default_project_session_workspace_dir`, seeds native cwd, and passes cwd and session ID to RuntimePromptRail. Its before_model_call adds current cwd/internal directory sections to system_prompt_builder. The ID is internally stored as well, but only the documented path binding is used by our model instructions.
- SysOperationRail.init adds native read/write tools to ability_manager. `_resolve_tool_file_path` resolves against get_cwd; using the injected absolute path removes generic-workspace-header ambiguity. WriteFileTool has pre-read/staleness checks but no create-exclusive transaction; it also appends framework history. Seven startup calls are the happy-path direct tool budget, excluding additional pre-reads/recovery calls required by actual tool protection.
- A reservation left by timeout/error or an incomplete binding blocks automatic recreation. Engineering halts persist in conversation/checkpoint and, when possible, the owned marker; generic Runner continuation does not clear them. A best-effort halt write is one extra call when already read, possibly preceded by a native read after context loss. A failed write is not retried.
- The Runner continues on ordinary final responses without native ending signals (ws_client.drive). Pure Skills cannot terminate its WebSocket loop, guarantee exactly-once execution, survive loss of all halt evidence, provide multi-driver locking or recover a never-returned game UUID. Stop rather than guess; explicit operator repair/authorization is necessary. No host symlink/cwd change or concurrent driver is supported.

V0.3.3 replaces the old ID-suffixed probe with fixed career-checkpoint.json in the trusted task directory. Framework ID exists in transport/runtime internals but is not persisted by our scheme. Source-backed directory isolation is a namespace property, not tool-boundary enforcement; Skill text cannot provide atomicity, a transaction or model-compliance guarantees. Second-run fixtures prove the old implementation violated the contract despite successful reads and writes. The three specialist bodies and all strategic routes remain unchanged. Offline safety references test this contract, not model compliance or live tool availability. Real installation/MCP/file-tool acceptance remains a separately authorized stage.
