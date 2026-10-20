"""Read-only V0.3.3 contract and policy-reference tests; never an Agent router.

No framework imports, clients, processes, network calls or game initialization.
Official pure functions are selected from local source with AST, not module imports.
Scenario helpers below model explicit policy examples, not LLM compliance or game
counterfactuals. All fixture changes are in memory. Run with python -B.
"""

from __future__ import annotations

import ast
import asyncio
from copy import deepcopy
from dataclasses import dataclass
import hashlib
from itertools import product
import json
from pathlib import Path, PureWindowsPath, PurePosixPath
import re
import sys
from types import ModuleType, SimpleNamespace
from typing import Any
import unittest
import zipfile
from unittest.mock import Mock

import yaml  # Already installed; parsing only. No dependency installation.


ROOT = Path(__file__).resolve().parents[1]
SOLUTION = ROOT / "solution"
BASELINE = ROOT / ".career_sim_runner/career_emu/outputs/The Raytirement Plan/20261019T214724Z"
BACKUPS = sorted((ROOT.parents[1] / "backups").glob("v03-phase1-*/backup-manifest.json"))
if not BACKUPS:
    raise RuntimeError("Verified phase-one backup is required before these tests")
BACKUP = BACKUPS[-1].parent
EXPECTED_SKILLS = {
    "career-controller", "risk-management", "career-planning", "resource-optimisation"
}
PREFIX = "mcp_career-emulator-engine_"
SID = "a86e8ff1b7924a598bc63422d52afd69"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def isolated_definitions(path: Path, names: set[str], bindings: dict) -> dict:
    """Compile only explicitly named definitions, never top-level module code."""
    tree = ast.parse(read(path), filename=str(path))
    definitions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and node.name in names
    ]
    if {node.name for node in definitions} != names:
        raise AssertionError(f"Source definitions changed: {path}")
    # Reject imports anywhere in the selected definitions, including lazy imports.
    if any(isinstance(node, (ast.Import, ast.ImportFrom)) for top in definitions for node in ast.walk(top)):
        raise AssertionError("Selected pure definitions unexpectedly contain imports")
    module_name = "_v03_offline_" + path.stem
    module = ModuleType(module_name)
    module.__dict__.update(bindings)
    sys.modules[module_name] = module  # stdlib dataclass resolves its defining module.
    code = ast.Module(body=definitions, type_ignores=[])
    exec(compile(ast.fix_missing_locations(code), str(path), "exec"), module.__dict__)
    return module.__dict__


def source_literal(path: Path, name: str):
    tree = ast.parse(read(path))
    node = next(n for n in tree.body if isinstance(n, ast.AnnAssign)
                and isinstance(n.target, ast.Name) and n.target.id == name)
    value = node.value
    if isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == "frozenset":
        return frozenset(ast.literal_eval(value.args[0]))
    return ast.literal_eval(value)


OFFICIAL_PREFIX = source_literal(ROOT / "career_sim_runner/constants.py", "EMULATOR_MCP_TOOL_PREFIX")
CONTRACT = isolated_definitions(
    ROOT / "career_sim_runner/skill_contract.py",
    {"SubmissionError", "validate_manifest", "validate_skill_frontmatter", "list_bundle_skill_ids"},
    {"Path": Path, "Any": Any, "yaml": yaml,
     "SUPPORTED_RUN_MODES": source_literal(ROOT / "career_sim_runner/constants.py", "SUPPORTED_RUN_MODES"),
     "_PLACEHOLDER_TEAM_NAMES": source_literal(ROOT / "career_sim_runner/skill_contract.py", "_PLACEHOLDER_TEAM_NAMES")},
)
WALK = isolated_definitions(
    ROOT / "career_sim_runner/transcript.py", {"_walk"}, {"Any": Any}
)["_walk"]
WS = isolated_definitions(
    ROOT / "career_sim_runner/ws_client.py",
    {"_GameState", "_parse_tool_result_payload", "_extract_game_signals", "_has_ended"},
    {"Any": Any, "dataclass": dataclass, "json": json, "_walk": WALK,
     "_CAREER_MCP_PREFIX": OFFICIAL_PREFIX, "_GAME_OVER_PREFIX": "GAME OVER:"},
)
design = read(SOLUTION / "design/skills_design.md")
policy_match = re.search(r"<!-- offline-policy-contract -->\s*```json\s*(.*?)\s*```", design, re.S)
if policy_match is None:
    raise RuntimeError("Missing documented offline policy contract")
POLICY = json.loads(policy_match.group(1))
SKILLS = {name: read(SOLUTION / "skills" / name / "SKILL.md") for name in EXPECTED_SKILLS}


def reference_route(phase: str, *, new_warning: bool = False) -> list[str]:
    """Offline reference only; terminal takes precedence over all routing."""
    route = list(POLICY["routes"][phase])
    if new_warning and phase not in {"terminal", "entry", "recovery", "uncertain"}:
        route = ["risk-management"] + [s for s in route if s != "risk-management"]
    return route


def reference_risk(status: str, event: str, previous_status: str = "unresolved") -> str:
    if event in POLICY["risk_preserve_events"]:
        return status
    if event == "mitigation_failure":
        return previous_status
    return POLICY["risk_transition_events"][event]


def reference_sequences(costs: dict[str, int], budget: int) -> list[tuple[str, ...]]:
    if budget < 0 or any(cost <= 0 for cost in costs.values()):
        raise ValueError("Invalid budget/cost")
    result = [()]
    if not costs:
        return result
    for length in range(1, budget // min(costs.values()) + 1):
        for seq in product(costs, repeat=length):
            if sum(costs[name] for name in seq) <= budget:
                result.append(seq)
    return result


def reference_effects(state: dict, effects: list[dict]) -> dict:
    """Known-effect fixture arithmetic only; not engine predictions."""
    result = dict(state)
    for effect in effects:
        for name, delta in effect.items():
            result[name] = result.get(name, 0) + delta
            if name in POLICY["public_caps"]:
                result[name] = min(POLICY["public_caps"][name], result[name])
    return result


def reference_state_filename(session_id: str) -> str:
    if re.fullmatch(r"[0-9a-fA-F]{32}", session_id) is None:
        raise ValueError("Expected the current interface's returned UUID-hex ID")
    return f"career-state-{session_id}.json"


def reference_restore(record: dict, session_id: str) -> dict:
    if record.get("session_id") != session_id:
        raise ValueError("Cross-session state")
    if record.get("schema_version") != POLICY["state_schema_version"]:
        raise ValueError("Unknown state schema")
    if record.get("solution_version") != POLICY["version"]:
        raise ValueError("Unknown solution version")
    return deepcopy(record)


def native_frame(tool: str, result: Any) -> dict:
    return {"body": {"event_type": "chat.tool_result", "tool_name": PREFIX + tool,
                     "raw_output": {"result": result}}}


def reference_legal_intent(observation: dict, intent: dict) -> bool:
    """Offline example of the controller's checks; never sends an action."""
    current = observation["current_state"]
    flags = current.get("simulation_flags") or {}
    return bool(
        current.get("session_id") and intent.get("session_id") == current["session_id"]
        and intent.get("observation_revision") == observation["local_revision"]
        and type(intent.get("choice")) is int and intent["choice"] >= 1
        and intent["choice"] in {item["choice"] for item in observation["choices"]}
        and isinstance(intent.get("notes"), str) and intent["notes"].strip()
        and flags.get("alive") is not False and flags.get("failed") is not True
    )


class FakeSkillDir:
    """In-memory path stand-in for negative frontmatter tests."""
    name = "fixture-skill"

    def __init__(self, text: str):
        self.text = text

    def __truediv__(self, name):
        assert name == "SKILL.md"
        return SimpleNamespace(is_file=lambda: True, read_text=lambda **kw: self.text)


class SubmissionTests(unittest.TestCase):
    def test_exact_submission_files_and_no_legacy_skill(self):
        expected = {"manifest.json", "README.md", "design/skills_design.md", "design/decision_report.md"}
        expected |= {f"skills/{name}/SKILL.md" for name in EXPECTED_SKILLS}
        actual = {p.relative_to(SOLUTION).as_posix() for p in SOLUTION.rglob("*") if p.is_file()}
        self.assertEqual(actual, expected)
        self.assertEqual(set(CONTRACT["list_bundle_skill_ids"](SOLUTION)), EXPECTED_SKILLS)

    def test_manifest_official_validator_and_persistent_constraints(self):
        manifest = json.loads(read(SOLUTION / "manifest.json"))
        self.assertEqual(CONTRACT["validate_manifest"](manifest), [])
        self.assertEqual(manifest["team"], "The Raytirement Plan")
        self.assertEqual(manifest["mode"], "agent")
        instruction = manifest["instruction"]
        for required in ["career-controller", PREFIX, "session_id", "context compression", "ending_score", "stop"]:
            self.assertIn(required, instruction)

    def test_official_manifest_rejects_placeholders_and_bad_mode(self):
        self.assertTrue(CONTRACT["validate_manifest"]({"team": "", "mode": "agent"}))
        self.assertTrue(CONTRACT["validate_manifest"]({"team": "enter your team name here", "mode": "agent"}))
        self.assertTrue(CONTRACT["validate_manifest"]({"team": "Real", "mode": "swarm"}))

    def test_frontmatter_matches_directories_and_official_validator(self):
        for name, text in SKILLS.items():
            with self.subTest(name=name):
                raw = (SOLUTION / "skills" / name / "SKILL.md").read_bytes()
                self.assertRegex(raw, br"^---\r?\n")  # LF and Windows CRLF are both valid.
                self.assertNotIn(b"\\---", raw)
                self.assertTrue(text.startswith("---\n"))
                self.assertNotIn("\\---", text)
                self.assertFalse(text.startswith("\ufeff"))
                fm = yaml.safe_load(text.split("---", 2)[1])
                self.assertEqual(fm["name"], name)
                self.assertIsInstance(fm["description"], str)
                self.assertTrue(fm["description"].strip())
                self.assertEqual(CONTRACT["validate_skill_frontmatter"](SOLUTION / "skills" / name), [])

    def test_official_frontmatter_negative_fixtures(self):
        for text in ["no frontmatter", "---\nname: x\n", "---\nname: x\n---\n", "---\nname: [\n---\n"]:
            with self.subTest(text=text):
                self.assertTrue(CONTRACT["validate_skill_frontmatter"](FakeSkillDir(text)))

    def test_native_mcp_signatures_from_installed_source_without_import(self):
        path = ROOT / ".venv/Lib/site-packages/career_emulator/server/tools.py"
        tree = ast.parse(read(path))
        actual = {n.name: ([a.arg for a in n.args.args], len(n.args.defaults))
                  for n in tree.body if isinstance(n, ast.AsyncFunctionDef)}
        self.assertEqual(actual, {
            "new_game": ([], 0), "observe": (["session_id"], 0),
            "take_action": (["session_id", "choice", "notes"], 0),
            "check_latest_logs": (["session_id", "count"], 1), "show_employee_handbook": ([], 0)})
        self.assertEqual(PREFIX, OFFICIAL_PREFIX)
        for name in actual:
            self.assertIn(f"`{name}(", SKILLS["career-controller"])

    def test_local_weights_match_actual_baseline(self):
        report = json.loads(read(BASELINE / "score_report.json"))
        weights = {d["name"]: d["weight"] for d in report["ending_score"]["dimensions"]}
        self.assertEqual(weights, {"level": .3, "wealth": .2, "resilience": .15,
                                   "skill": .15, "risk_control": .1, "network": .1})
        risk = next(d for d in report["ending_score"]["dimensions"] if d["name"] == "risk_control")
        self.assertEqual(risk["weighted_score"], 1)


class RoutingTests(unittest.TestCase):
    def test_all_routes_use_only_installed_skill_names(self):
        for route in POLICY["routes"].values():
            self.assertTrue(set(route) <= EXPECTED_SKILLS)
            self.assertEqual(len(route), len(set(route)))

    def test_story_and_main_use_risk_and_career(self):
        for phase in ["story", "main"]:
            self.assertEqual(reference_route(phase), ["risk-management", "career-planning"])

    def test_energy_routes_all_three_methods_in_order(self):
        self.assertEqual(reference_route("energy"),
                         ["risk-management", "career-planning", "resource-optimisation"])

    def test_new_warning_precedes_review_planning(self):
        self.assertEqual(reference_route("review")[0], "career-planning")
        self.assertEqual(reference_route("review", new_warning=True)[0], "risk-management")

    def test_terminal_overrides_warning_and_stops_specialists(self):
        self.assertEqual(reference_route("terminal", new_warning=True), ["career-controller"])

    def test_recovery_and_uncertain_action_return_to_controller(self):
        self.assertEqual(reference_route("recovery"), ["career-controller"])
        self.assertEqual(reference_route("uncertain"), ["career-controller"])

    def test_loading_rules_and_single_executor_are_explicit(self):
        controller = SKILLS["career-controller"]
        for phrase in ["otherwise reuse", "No quarterly reload", "not an official simulator field",
                       "Only this Agent issues one final", "after any continuation"]:
            self.assertIn(phrase, controller)
        for specialist in EXPECTED_SKILLS - {"career-controller"}:
            self.assertIn("same Agent", SKILLS[specialist])


class RiskTests(unittest.TestCase):
    def test_warning_survives_empty_events(self):
        self.assertEqual(reference_risk("unresolved", "empty_events"), "unresolved")
        self.assertEqual(reference_risk("monitoring", "empty_events"), "monitoring")

    def test_mitigation_does_not_prove_clearance(self):
        pending = reference_risk("unresolved", "mitigation_intent")
        self.assertEqual(pending, "mitigation_pending")
        self.assertEqual(reference_risk(pending, "mitigation_success"), "monitoring")
        self.assertEqual(reference_risk("monitoring", "benign_feedback"), "monitoring")

    def test_rejected_mitigation_and_recurring_warning_preserve_issue(self):
        self.assertEqual(reference_risk("mitigation_pending", "mitigation_failure"), "unresolved")
        self.assertEqual(reference_risk("monitoring", "warning"), "unresolved")

    def test_explicit_resolution_is_scoped(self):
        ledger = {"R1": "monitoring", "R2": "unresolved"}
        ledger["R1"] = reference_risk(ledger["R1"], "explicit_scoped_resolution")
        self.assertEqual(ledger, {"R1": "resolved_explicit", "R2": "unresolved"})

    def test_official_pending_warning_consumption_in_memory_only(self):
        tree = ast.parse(read(ROOT / ".venv/Lib/site-packages/career_emulator/game.py"))
        fn = next(n for n in ast.walk(tree) if isinstance(n, ast.AsyncFunctionDef)
                  and n.name == "_attach_observe_warning")
        # The isolated method only touches fake session/store and fake response.
        ns = {"GameSession": Any, "ObserveResponse": SimpleNamespace}
        exec(compile(ast.Module(body=[fn], type_ignores=[]), "isolated_warning_method", "exec"), ns)
        store = SimpleNamespace(save_session=Mock())

        async def save_session(session):
            store.save_session(session)

        owner = SimpleNamespace(store=SimpleNamespace(save_session=save_session))
        session = SimpleNamespace(pending_observe_warning="Observed risk warning")
        response = SimpleNamespace(current_state={}, current_event={}, choices=[], ending_score=None)
        first = asyncio.run(ns["_attach_observe_warning"](owner, session, response))
        self.assertEqual(first.warning, "Observed risk warning")
        self.assertEqual(session.pending_observe_warning, "")
        second = asyncio.run(ns["_attach_observe_warning"](owner, session, response))
        self.assertIs(second, response)
        store.save_session.assert_called_once_with(session)

    def test_documented_statuses_and_risk_score_goal(self):
        text = SKILLS["risk-management"]
        for status in POLICY["risk_statuses"]:
            self.assertIn(status, text)
        for phrase in ["Hard exclusion", "Conservative restriction", "Advice", "contributing 1/10"]:
            self.assertIn(phrase, text)


class ResourceTests(unittest.TestCase):
    def test_public_costs_and_all_budget_three_sequences(self):
        costs = POLICY["energy_costs"]
        self.assertEqual(sorted(costs.values()), [1, 1, 1, 1, 2, 2, 2])
        sequences = reference_sequences(costs, 3)
        self.assertEqual(len(sequences), 112)  # Fixture: all seven categories offered, repeats allowed.
        self.assertTrue(all(sum(costs[n] for n in seq) <= 3 for seq in sequences))

    def test_zero_budget_and_reduced_current_menu(self):
        self.assertEqual(reference_sequences(POLICY["energy_costs"], 0), [()])
        self.assertEqual(reference_sequences({"prepare_report": 1}, 2),
                         [(), ("prepare_report",), ("prepare_report", "prepare_report")])

    def test_reserve_two_energy_for_relevant_mitigation(self):
        costs = POLICY["energy_costs"]
        feasible = reference_sequences(costs, 3)
        reserved = [s for s in feasible if "defuse_landmines" in s]
        self.assertIn(("defuse_landmines", "health_recovery"), reserved)
        self.assertNotIn(("intensive_work", "defuse_landmines"), feasible)

    def test_cap_and_order_change_known_marginal_gain(self):
        state = {"health": 10, "dignity": 10}
        recovery = {"health": 2}
        work = {"health": -1, "dignity": -1, "output": 2}
        self.assertEqual(reference_effects(state, [recovery])["health"], 10)
        self.assertEqual(reference_effects(state, [work, recovery])["health"], 10)
        self.assertEqual(reference_effects(state, [recovery, work])["health"], 9)

    def test_known_report_comparison_is_not_hidden_safety_claim(self):
        state = {"health": 9, "dignity": 9, "output": 5}
        reports = reference_effects(state, [{"output": 1, "dignity": 1}] * 2)
        intensive = reference_effects(state, [{"output": 2, "health": -1, "dignity": -1}])
        self.assertEqual(reports["output"], intensive["output"])
        self.assertGreater(reports["health"], intensive["health"])
        self.assertIn("not proof of permanent dominance or hidden safety", SKILLS["resource-optimisation"])

    def test_only_health_and_dignity_have_documented_caps(self):
        self.assertEqual(POLICY["public_caps"], {"health": 10, "dignity": 10})
        self.assertEqual(reference_effects({"skill": 118}, [{"skill": 10}])["skill"], 128)

    def test_choice_numbers_are_from_current_menu_not_cached_categories(self):
        current = {2: "prepare_report", 5: "health_recovery"}
        allowed = [choice for choice, name in current.items() if name == "prepare_report"]
        self.assertEqual(allowed, [2])
        self.assertNotIn(7, allowed)  # The old full menu's report ID must not be reused.


class StateAndTimingTests(unittest.TestCase):
    def setUp(self):
        text = SKILLS["career-controller"]
        self.state = json.loads(re.search(r"```json\s*(.*?)\s*```", text, re.S).group(1))
        self.state["session_id"] = SID

    def test_json_state_example_has_minimal_required_fields(self):
        self.assertEqual(set(self.state), {"schema_version", "solution_version", "session_id",
            "observation_revision", "time", "visible_state", "risks", "reviews", "quarter",
            "strategy", "action", "ending"})
        self.assertEqual(reference_restore(self.state, SID), self.state)

    def test_session_filename_isolation_and_path_traversal_rejection(self):
        self.assertNotEqual(reference_state_filename(SID), reference_state_filename("b" * 32))
        for sid in ["../other", "", "x/y", "a" * 31]:
            with self.subTest(sid=sid), self.assertRaises(ValueError):
                reference_state_filename(sid)

    def test_cross_session_and_unknown_schema_rejected(self):
        with self.assertRaises(ValueError):
            reference_restore(self.state, "b" * 32)
        self.state["schema_version"] = 99
        with self.assertRaises(ValueError):
            reference_restore(self.state, SID)

    def test_pending_intent_is_not_permission_to_resend(self):
        self.state["action"]["status"] = "pending"
        restored = reference_restore(self.state, SID)
        self.assertEqual(restored["action"]["status"], "pending")
        self.assertIn("reconciled, not resent", SKILLS["career-controller"])
        self.assertIn("keep `uncertain` and stop", SKILLS["career-controller"])

    def test_ordinary_observe_is_not_a_checkpoint_trigger(self):
        self.assertNotIn("ordinary_observe", POLICY["checkpoint_reasons"])
        self.assertNotIn("before_action", POLICY["checkpoint_reasons"])
        self.assertIn("Ordinary successful actions", SKILLS["career-controller"])
        self.assertIn("No per-action pending write is required", SKILLS["career-controller"])

    def test_all_eight_review_entries_and_unknowns_can_survive_roundtrip(self):
        self.state["reviews"] = [{"month": m, "grade": None, "level_after": None}
                                 for m in POLICY["review_months"]]
        self.state["risks"] = [{"id": "R1", "status": "unresolved", "evidence": "warning"}]
        restored = reference_restore(json.loads(json.dumps(self.state)), SID)
        self.assertEqual(len(restored["reviews"]), 8)
        self.assertIsNone(restored["reviews"][0]["grade"])
        self.assertEqual(restored["risks"][0]["status"], "unresolved")

    def test_final_review_already_processed_has_no_future_window(self):
        remaining = [m for m in POLICY["review_months"] if m not in set(POLICY["review_months"])]
        self.assertEqual(remaining, [])
        self.assertIn("imagined ninth promotion window", SKILLS["career-planning"])
        self.assertIn("already processed review", SKILLS["career-planning"])

    def test_review_grade_is_not_promotion_and_raw_scales_not_thresholds(self):
        text = SKILLS["career-planning"]
        self.assertIn("S review without promotion", text)
        self.assertIn("raw number is smallest", text)
        self.assertIn("not an eligibility threshold", text)

    def test_same_month_energy_cannot_reopen_processed_review(self):
        observed_review_months = {6}
        current_month, phase = 6, "energy"
        next_window = next(m for m in POLICY["review_months"]
                           if m >= current_month and m not in observed_review_months)
        self.assertEqual(next_window, 12)
        self.assertEqual(reference_route(phase)[-1], "resource-optimisation")
        self.assertIn("not just month modulo six", SKILLS["career-controller"])

    def test_current_choice_session_notes_and_local_revision(self):
        observation = {"local_revision": 12, "current_state": {"session_id": SID,
                       "simulation_flags": {"alive": True, "failed": False}},
                       "choices": [{"choice": 2}, {"choice": 5}]}
        intent = {"session_id": SID, "observation_revision": 12, "choice": 5, "notes": "v03:r12 relevant reason"}
        self.assertTrue(reference_legal_intent(observation, intent))
        for key, value in [("choice", 0), ("choice", 3), ("choice", True), ("notes", ""),
                           ("observation_revision", 11), ("session_id", "")]:
            with self.subTest(key=key, value=value):
                self.assertFalse(reference_legal_intent(observation, {**intent, key: value}))
        observation["current_state"]["simulation_flags"]["alive"] = False
        self.assertFalse(reference_legal_intent(observation, intent))


class TerminalAndBackupTests(unittest.TestCase):
    def test_actual_archived_ending_recognized_as_native_terminal(self):
        ending = json.loads(read(BACKUP / "first-run-workspace/ending_raw.json"))
        state = WS["_GameState"]()
        WS["_extract_game_signals"](native_frame("observe", json.dumps(ending)), state)
        self.assertTrue(WS["_has_ended"](state))
        self.assertEqual(state.session_id, SID)
        self.assertEqual(state.last_month, 49)
        self.assertTrue(ending["ending_score"]["completed"])
        self.assertEqual(ending["ending_score"]["survival_months"], 48)

    def test_bash_printed_ending_not_native_terminal(self):
        ending = json.loads(read(BACKUP / "first-run-workspace/ending_raw.json"))
        frame = native_frame("observe", ending)
        frame["body"]["tool_name"] = "bash"
        state = WS["_GameState"]()
        WS["_extract_game_signals"](frame, state)
        self.assertFalse(state.ended)

    def test_successful_final_action_needs_followup_observe(self):
        state = WS["_GameState"]()
        WS["_extract_game_signals"](native_frame("take_action", {"success": True}), state)
        self.assertFalse(state.ended)
        ending = json.loads(read(BACKUP / "first-run-workspace/ending_raw.json"))
        WS["_extract_game_signals"](native_frame("observe", ending), state)
        self.assertTrue(state.ended)

    def test_game_over_error_and_malformed_payload(self):
        state = WS["_GameState"]()
        WS["_extract_game_signals"](native_frame("observe", "invalid JSON"), state)
        self.assertFalse(state.ended)
        WS["_extract_game_signals"](native_frame("take_action",
            {"success": False, "error": "GAME OVER: Completed the 48-month simulation."}), state)
        self.assertTrue(state.ended)

    def test_native_new_game_signal_parsed_without_calling_a_game(self):
        state = WS["_GameState"]()
        WS["_extract_game_signals"](native_frame("new_game", {"session_id": SID}), state)
        self.assertEqual(state.session_id, SID)
        self.assertFalse(state.ended)

    def test_archived_files_match_recorded_checksums(self):
        manifest = json.loads(read(BACKUP / "backup-manifest.json"))
        for item in manifest["files"]:
            with self.subTest(path=item["backup"]):
                p = Path(item["backup"])
                self.assertEqual(p.stat().st_size, item["bytes"])
                self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), item["sha256"])

    def test_baseline_source_and_results_preserved_outside_submission(self):
        self.assertTrue((BACKUP / "solution-v02/skills/career-survival/SKILL.md").is_file())
        self.assertEqual(json.loads(read(BASELINE / "score_report.json"))["ending_score"]["quantitative_score"], 63.02)
        self.assertTrue((BASELINE / "events-20261019T214724Z.jsonl").is_file())
        self.assertTrue((BASELINE / "transcript-20261019T214724Z.log").is_file())

    def test_only_four_verified_legacy_files_were_cleaned(self):
        report = json.loads(read(BACKUP / "cleanup-report.json"))
        expected = {"mcp_call.py", "look.py", "obs.json", "ending_raw.json"}
        self.assertEqual({Path(item["source"]).name for item in report["removed_files"]}, expected)
        for item in report["removed_files"]:
            self.assertFalse(Path(item["source"]).exists())
            self.assertEqual(hashlib.sha256(Path(item["backup"]).read_bytes()).hexdigest(), item["sha256"])

    def test_protected_source_config_indexes_and_baseline_bytes_unchanged(self):
        manifest = json.loads(read(BACKUP / "backup-manifest.json"))
        run2 = json.loads(read(RUN2_AUDIT / "run-audit.json"))
        # Installation/game changes are authorized phase transitions, not edits by this task.
        phase_changed = {str(ROOT / ".career_sim_runner/career_emu/career_emulator.sqlite3"),
                         str(INSTANCE / "agent/workspace/skills/skills_state.json"),
                         str(INSTANCE / "agent/workspace/skills/career-survival/SKILL.md")}
        archive_by_source = {item["source"]: Path(item["backup"]) for item in manifest["files"]}
        install_archive = ROOT.parents[1] / "backups/v032-install-20261020T151522927315Z"
        archive_by_source.update({
            str(ROOT / ".career_sim_runner/career_emu/career_emulator.sqlite3"):
                install_archive / "runner-before/career_emulator.sqlite3",
            str(INSTANCE / "agent/workspace/skills/skills_state.json"):
                install_archive / "instance-before/agent/workspace/skills/skills_state.json",
            str(INSTANCE / "agent/workspace/skills/career-survival/SKILL.md"):
                BACKUP / "solution-v02/skills/career-survival/SKILL.md"})
        for item in manifest["protected_files"]:
            p = Path(item["path"])
            with self.subTest(path=str(p)):
                if str(p) in phase_changed:
                    # Retain the historical baseline assertion against its original saved bytes.
                    archived = archive_by_source[str(p)]
                    self.assertEqual(hashlib.sha256(archived.read_bytes()).hexdigest(), item["sha256"])
                else:
                    self.assertTrue(p.is_file())
                    self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), item["sha256"])
        # Independently pin the post-run-two live DB/config/installed Skills; no exclusions there.
        for raw, expected in PRESERVED_RUN2_SHA256.items():
            with self.subTest(current_phase=raw):
                self.assertEqual(hashlib.sha256(Path(raw).read_bytes()).hexdigest(), expected)
        for raw, entry in run2["protected_file_comparison"].items():
            if "solution" not in Path(raw).parts:
                self.assertEqual(hashlib.sha256(Path(raw).read_bytes()).hexdigest(), entry["after"])

    def test_original_session_and_file_history_preserved(self):
        manifest = json.loads(read(BACKUP / "backup-manifest.json"))
        history = [item for item in manifest["files"] if "first-run-session" in Path(item["backup"]).parts
                   or Path(item["source"]).name.startswith("file_ops_")]
        self.assertGreaterEqual(len(history), 3)
        for item in history:
            # Official authorized install removed the old live session; its archive must stay exact.
            self.assertEqual(hashlib.sha256(Path(item["backup"]).read_bytes()).hexdigest(), item["sha256"])
        for raw, expected in PRESERVED_RUN2_SHA256.items():
            if "sessions" in Path(raw).parts:
                self.assertEqual(hashlib.sha256(Path(raw).read_bytes()).hexdigest(), expected)

    def test_no_framework_or_game_package_initialized(self):
        forbidden = ("jiuwenswarm", "openjiuwen", "career_emulator", "career_sim_runner")
        self.assertFalse(any(name == p or name.startswith(p + ".")
                             for name in sys.modules for p in forbidden))


def reference_checkpoint_calls(events: list[str]) -> int:
    """Policy reference: one compact coalesced write; binding also read-backs."""
    material = set(events) & set(POLICY["checkpoint_reasons"])
    if not material:
        return 0
    return POLICY["binding_checkpoint_file_calls"] if "session_bound" in material else 1


def reference_storage_gate(**evidence: bool) -> bool:
    required = {"assigned_directory", "framework_scope", "native_write_tool", "native_read_tool",
                "probe_absent", "confirmed_fresh_start", "write_succeeded", "readback_matches",
                "semantic_paths_match", "marker_payload_validated"}
    return all(evidence.get(key) is True for key in required)


def reference_recovery(checkpoint_action: str | None, proof: str, coherent: bool) -> dict:
    """Never use checkpoint status/absence as proof of execution or a replay key."""
    return {"native_checks_required": True,
            "next": "fresh_current_choice" if proof == "confirmed_commit" and coherent else "stop_uncertain",
            "resend_cached_choice": False}


def reference_feedback(review: dict, offered: set[str], previous_focus: str | None = None) -> dict:
    """Hypothesis-selection fixture, NOT an Agent or a promotion prediction."""
    evidence = review.get("evidence", [])
    promoted = review.get("promoted") is True
    if review.get("severe_risk"):
        branch = "protect"
        candidates = [x for x in ["repair_relationship", "lie_low"] if x in offered]
    else:
        branch = "post_promotion" if promoted else "maintain_uncertain"
        candidates = []
        for signal in evidence:
            candidates.extend(x for x in POLICY["feedback_focus_by_evidence"].get(signal, [])
                              if x in offered and x not in candidates)
        if candidates and not promoted:
            branch = "feedback_targeted"
        if not candidates:
            # No forced variety or promotion assumption: retain a justified focus if offered.
            candidates = [previous_focus] if previous_focus in offered else []
    return {"branch": branch, "candidates": candidates, "grade": review.get("grade"),
            "reassess_previous_hypothesis": bool(review.get("successive_missed_windows")),
            "promotion_guaranteed": False, "hypothesis_status": "unproven"}


def reference_shortlist(proposals: list[dict], menu: dict[int, dict], budget: int,
                        state: dict, blocked: set[int] | None = None,
                        required_mitigation: int | None = None) -> list[dict]:
    """Offline bounded-proposal filtering with explicit known fixture effects only.

    No exhaustive generation, numeric utility, hidden risk model or actual choice
    execution. Fixture risk tags must explicitly describe comparable known risk;
    unknown effects prevent dominance pruning.
    """
    blocked = blocked or set()
    screened, seen = [], set()
    for proposal in proposals:
        actions = tuple(proposal["actions"])
        if not actions or actions in seen:
            continue
        seen.add(actions)
        if any(type(i) is not int or i not in menu or i in blocked for i in actions):
            continue
        if any(type(menu[i].get("cost")) is not int or menu[i]["cost"] <= 0 for i in actions):
            continue
        cost = sum(menu[i]["cost"] for i in actions)
        if cost > budget or (required_mitigation is not None and required_mitigation not in actions):
            continue
        unknowns = list(proposal.get("unknowns", []))
        effects = []
        for i in actions:
            if menu[i].get("effects") is None:
                unknowns.append(f"unknown effect of {i}")
            else:
                effects.append(menu[i]["effects"])
        end = reference_effects(state, effects)
        if end.get("health", 1) <= 0:
            continue
        gains = {k: end.get(k, 0) - state.get(k, 0) for k in set(end) | set(state)}
        if not any(v > 0 for v in gains.values()) and not unknowns and not proposal.get("distinct_purpose"):
            continue
        screened.append({**proposal, "actions": actions, "cost": cost, "gains": gains, "unknowns": unknowns})

    def dominates(better, worse):
        if better["unknowns"] or worse["unknowns"] or worse.get("distinct_purpose"):
            return False
        if not better.get("known_risk_tag") or better.get("known_risk_tag") != worse.get("known_risk_tag"):
            return False
        keys = set(better["gains"]) | set(worse["gains"])
        no_worse = better["cost"] <= worse["cost"] and all(
            better["gains"].get(k, 0) >= worse["gains"].get(k, 0) for k in keys)
        strictly_better = better["cost"] < worse["cost"] or any(
            better["gains"].get(k, 0) > worse["gains"].get(k, 0) for k in keys)
        return no_worse and strictly_better

    filtered = [p for p in screened if not any(q is not p and dominates(q, p) for q in screened)]
    # Supplied order is proposal priority for this fixture, not a scalar utility.
    return filtered[:POLICY["resource_max_candidates"]]


class PersistenceRevisionTests(unittest.TestCase):
    def test_ordinary_action_and_observation_zero_file_calls(self):
        self.assertEqual(reference_checkpoint_calls(["before_action", "ordinary_success", "ordinary_observe"]), 0)

    def test_material_triggers_each_write_once(self):
        for event in ["risk_changed", "review_observed", "promotion_observed", "strategy_changed",
                      "execution_uncertain", "terminal", "action_rejected"]:
            with self.subTest(event=event):
                self.assertEqual(reference_checkpoint_calls([event]), 1)

    def test_review_promotion_strategy_batch_coalesces(self):
        self.assertEqual(reference_checkpoint_calls(["review_observed", "promotion_observed", "strategy_changed"]), 1)

    def test_binding_probe_has_explicit_one_time_cost(self):
        self.assertEqual(reference_checkpoint_calls(["session_bound"]), 4)
        self.assertEqual(POLICY["storage_gate_file_calls"] + reference_checkpoint_calls(["session_bound"]), 7)

    def test_identical_warning_and_clean_handoff_do_not_write(self):
        self.assertEqual(reference_checkpoint_calls(["unchanged_warning", "revision_only", "clean_handoff"]), 0)
        self.assertEqual(reference_checkpoint_calls(["dirty_handoff"]), 1)

    def test_storage_capability_cannot_be_assumed(self):
        evidence = dict.fromkeys(["assigned_directory", "framework_scope", "native_write_tool",
                                  "native_read_tool", "probe_absent", "confirmed_fresh_start",
                                  "write_succeeded", "readback_matches",
                                  "semantic_paths_match", "marker_payload_validated"], True)
        self.assertTrue(reference_storage_gate(**evidence))
        for key in evidence:
            with self.subTest(missing=key):
                incomplete = evidence.copy()
                incomplete.pop(key)
                self.assertFalse(reference_storage_gate(**incomplete))

    def test_recovery_fence_even_with_no_pending_or_confirmed_checkpoint(self):
        for status in [None, "confirmed", "pending", "uncertain"]:
            with self.subTest(status=status):
                result = reference_recovery(status, "missing_log", True)
                self.assertTrue(result["native_checks_required"])
                self.assertEqual(result["next"], "stop_uncertain")
                self.assertFalse(result["resend_cached_choice"])

    def test_recovered_commit_uses_new_menu_never_cached_intent(self):
        result = reference_recovery(None, "confirmed_commit", True)
        self.assertEqual(result["next"], "fresh_current_choice")
        self.assertFalse(result["resend_cached_choice"])
        self.assertEqual(reference_recovery(None, "confirmed_commit", False)["next"], "stop_uncertain")

    def test_unchanged_stats_are_not_nonexecution_proof(self):
        self.assertEqual(reference_recovery("confirmed", "unchanged_stats", True)["next"], "stop_uncertain")

    def test_controller_documents_gate_atomicity_limit_and_costs(self):
        text = SKILLS["career-controller"]
        for phrase in ["Storage capability gate", "one write and one read-back", "No per-action pending write",
                       "state saving and action-log append are separate", "no exact-once guarantee",
                       "On EVERY continuation", "count=30 once"]:
            self.assertIn(phrase, text)


class FeedbackRevisionTests(unittest.TestCase):
    def test_high_performance_no_promotion_visibility_feedback(self):
        result = reference_feedback({"grade": "S", "promoted": False, "evidence": ["visibility"]},
                                    {"key_project", "leadership_report"}, "key_project")
        self.assertEqual(result["candidates"], ["leadership_report"])
        self.assertFalse(result["promotion_guaranteed"])

    def test_high_grade_no_evidence_does_not_force_variety_or_more_output(self):
        result = reference_feedback({"grade": "A", "promoted": False},
                                    {"key_project", "job_rotation"}, "key_project")
        self.assertEqual(result["branch"], "maintain_uncertain")
        self.assertEqual(result["candidates"], ["key_project"])

    def test_poor_results_and_visibility_feedback_are_different(self):
        offered = {"key_project", "push_resources", "leadership_report"}
        delivery = reference_feedback({"grade": "C", "evidence": ["delivery"]}, offered)
        visibility = reference_feedback({"grade": "C", "evidence": ["visibility"]}, offered)
        self.assertEqual(delivery["candidates"], ["key_project", "push_resources"])
        self.assertEqual(visibility["candidates"], ["leadership_report"])

    def test_promotion_and_poor_grade_remain_separate_facts(self):
        result = reference_feedback({"grade": "C", "promoted": True, "evidence": ["delivery"]}, {"key_project"})
        self.assertEqual(result["branch"], "post_promotion")
        self.assertEqual(result["grade"], "C")
        self.assertEqual(result["candidates"], ["key_project"])

    def test_severe_risk_overrides_optional_development(self):
        result = reference_feedback({"grade": "S", "severe_risk": True, "evidence": ["delivery"]},
                                    {"key_project", "repair_relationship", "lie_low"})
        self.assertEqual(result["branch"], "protect")
        self.assertNotIn("key_project", result["candidates"])

    def test_long_tenure_reassesses_without_inventing_gate(self):
        result = reference_feedback({"grade": "S", "successive_missed_windows": True},
                                    {"key_project"}, "key_project")
        self.assertTrue(result["reassess_previous_hypothesis"])
        self.assertEqual(result["hypothesis_status"], "unproven")
        self.assertEqual(result["candidates"], ["key_project"])

    def test_capability_scope_relationship_candidates_must_be_offered(self):
        for evidence, offered, expected in [("capability", {"mentor"}, ["mentor"]),
                ("scope", {"job_rotation"}, ["job_rotation"]),
                ("relationship", {"repair_relationship"}, ["repair_relationship"])]:
            with self.subTest(evidence=evidence):
                self.assertEqual(reference_feedback({"evidence": [evidence]}, offered)["candidates"], expected)
        self.assertEqual(reference_feedback({"evidence": ["capability"]}, {"lie_low"})["candidates"], [])

    def test_feedback_loop_and_repetition_evidence_are_explicit_in_document(self):
        text = SKILLS["career-planning"]
        for phrase in ["14/16", "do not force a rotation quota", "strategy.feedback_loop",
                       "C review with promotion", "A/S but no promotion", "not isolated causal proof"]:
            self.assertIn(phrase, text)


class CandidateRevisionTests(unittest.TestCase):
    def setUp(self):
        self.menu = {1: {"cost": 1, "effects": {"output": 1, "dignity": 1}},
                     2: {"cost": 2, "effects": {"output": 2, "health": -1, "dignity": -1}},
                     3: {"cost": 1, "effects": {"health": 2}},
                     4: {"cost": 2, "effects": None}}
        self.state = {"health": 10, "dignity": 10, "output": 5}

    def test_menu_budget_and_severe_risk_filtering(self):
        proposals = [{"actions": [99]}, {"actions": [1, 1, 1, 1]}, {"actions": [2]}, {"actions": [1]}]
        result = reference_shortlist(proposals, self.menu, 3, self.state, blocked={2})
        self.assertEqual([p["actions"] for p in result], [(1,)])

    def test_capped_recovery_alone_removed_but_after_cost_preserved(self):
        proposals = [{"actions": [3]}, {"actions": [2, 3], "unknowns": ["hidden effects unknown"]}]
        result = reference_shortlist(proposals, self.menu, 3, self.state)
        self.assertEqual([p["actions"] for p in result], [(2, 3)])
        self.assertEqual(result[0]["gains"]["health"], 0)

    def test_obvious_disadvantage_requires_known_comparable_risk(self):
        proposals = [{"actions": [2], "known_risk_tag": "same explicit fixture risk"},
                     {"actions": [1, 1], "known_risk_tag": "same explicit fixture risk"}]
        result = reference_shortlist(proposals, self.menu, 3, self.state)
        self.assertEqual([p["actions"] for p in result], [(1, 1)])

    def test_unknown_effects_are_not_ranked_as_zero_or_dominated(self):
        proposals = [{"actions": [2], "unknowns": ["distinct delayed benefit unknown"]}, {"actions": [1, 1]},
                     {"actions": [4], "distinct_purpose": "mitigate observed hazard"}]
        result = reference_shortlist(proposals, self.menu, 3, self.state)
        self.assertEqual(len(result), 3)
        self.assertTrue(next(p for p in result if p["actions"] == (4,))["unknowns"])

    def test_at_most_three_distinct_candidates_not_a_full_search(self):
        proposals = [{"actions": [1]}, {"actions": [1]}, {"actions": [1, 1]},
                     {"actions": [2], "unknowns": ["uncertain"]}, {"actions": [4]}]
        result = reference_shortlist(proposals, self.menu, 3, self.state)
        self.assertLessEqual(len(result), 3)
        self.assertEqual(len({p["actions"] for p in result}), len(result))
        self.assertEqual(POLICY["resource_max_candidates"], 3)

    def test_mitigation_reservation_survives_shortlisting(self):
        proposals = [{"actions": [1, 1, 1]}, {"actions": [4, 1]}, {"actions": [2, 4]}]
        result = reference_shortlist(proposals, self.menu, 3, self.state, required_mitigation=4)
        self.assertEqual([p["actions"] for p in result], [(4, 1)])

    def test_first_step_then_new_menu_instead_of_cached_sequence(self):
        initial = reference_shortlist([{"actions": [1, 1]}], self.menu, 3, self.state)[0]
        first_choice = initial["actions"][0]
        self.assertEqual(first_choice, 1)
        # New fixture menu no longer contains 1; the old planned second choice is invalid.
        updated_menu = {3: self.menu[3]}
        self.assertEqual(reference_shortlist([initial], updated_menu, 2, self.state), [])

    def test_document_limits_candidates_and_preserves_unknowns(self):
        text = SKILLS["resource-optimisation"]
        for phrase in ["Do not enumerate", "at most three", "Cap clipping", "Prune obvious disadvantage",
                       "not a globally optimal search guarantee", "not a numeric utility"]:
            self.assertIn(phrase, text)


# V0.3.2 safety examples only; these helpers are NOT runtime code.
FRAMEWORK_ID_RE = r"career-sim-runner-[0-9a-f]{12}"
F_ID = "career-sim-runner-012345abcdef"
INTERNAL_DIR = r"C:\verified-instance\agent\workspace"
TASK_DIR = INTERNAL_DIR + "\\projects\\" + F_ID


def reference_framework_scope(cwd: str, internal_dir: str, *, project_bound=False) -> dict:
    if project_bound:
        raise ValueError("No project-bound fallback is authorized")
    paths = []
    for raw in (cwd, internal_dir):
        if not isinstance(raw, str) or not raw or raw.startswith(("\\\\", "//")) or "\x00" in raw:
            raise ValueError("Not a supported absolute runtime path")
        if any(part in {".", ".."} for part in re.split(r"[\\/]", raw)):
            raise ValueError("Dot components are rejected, not sanitized")
        kind = PureWindowsPath if re.match(r"^[A-Za-z]:[\\/]", raw) else PurePosixPath
        p = kind(raw)
        if not p.is_absolute():
            raise ValueError("Relative runtime path")
        paths.append(p)
    task, internal = paths
    if type(task) is not type(internal) or task.parent != internal / "projects":
        raise ValueError("Runtime cwd not in the source-backed session layout")
    if not re.fullmatch(FRAMEWORK_ID_RE, task.name, flags=re.ASCII):
        raise ValueError("Invalid framework ID; do not rewrite it")
    return {"framework_session_id": task.name, "verified_directory": str(task),
            "probe_path": str(task / "career-checkpoint.json")}


def reference_probe(scope: dict, game_id: str | None = None, phase="reserved", halted_reason=None) -> dict:
    state_path = None
    if game_id is not None:
        state_path = str(type_path(scope["verified_directory"]) / reference_state_filename(game_id))
    return {"schema_version": POLICY["state_schema_version"], "solution_version": POLICY["version"],
            "verified_directory": scope["verified_directory"], "verified_path": state_path,
            "game_session_id": game_id, "phase": phase, "halted_reason": halted_reason}


def type_path(raw: str):
    return PureWindowsPath(raw) if re.match(r"^[A-Za-z]:[\\/]", raw) else PurePosixPath(raw)


def reference_marker_semantics(scope: dict, marker, actual_path: str) -> bool:
    """Reference only: independent trusted scope, never two generated ID strings."""
    fields = {"schema_version", "solution_version", "verified_directory", "verified_path",
              "game_session_id", "phase", "halted_reason"}
    if not isinstance(marker, dict) or set(marker) != fields:
        return False
    if actual_path != scope["probe_path"] or marker["verified_directory"] != scope["verified_directory"]:
        return False
    if type(marker["schema_version"]) is not int or marker["schema_version"] != POLICY["state_schema_version"]:
        return False
    if marker["solution_version"] != POLICY["version"] or marker["halted_reason"] is not None:
        return False
    if marker["phase"] == "reserved":
        return marker["game_session_id"] is None and marker["verified_path"] is None
    if marker["phase"] != "bound":
        return False
    try:
        expected = str(type_path(scope["verified_directory"]) / reference_state_filename(marker["game_session_id"]))
    except (TypeError, ValueError):
        return False
    return marker["verified_path"] == expected


def reference_bound_state(scope: dict, marker: dict, state, actual_state_path: str,
                          *, context_game=None) -> bool:
    if not reference_marker_semantics(scope, marker, scope["probe_path"]) or marker["phase"] != "bound":
        return False
    game_id = marker["game_session_id"]
    if context_game is not None and context_game != game_id:
        return False
    if not isinstance(state, dict) or actual_state_path != marker["verified_path"]:
        return False
    try:
        reference_restore(state, game_id)
        binding = state["strategy"]["checkpoint"]
    except (KeyError, TypeError, ValueError):
        return False
    return (set(binding) == {"verified_directory", "verified_path", "reason", "halted_reason"}
            and binding["verified_directory"] == scope["verified_directory"]
            and binding["verified_path"] == marker["verified_path"]
            and binding["halted_reason"] is None)


def reference_bootstrap(scope: dict, probe, *, fresh=False, continuation=False,
                        context_game=None, halted=False, state=None, actual_marker_path=None,
                        absence_confirmed=False, prior_scope=False) -> str:
    if halted:
        return "halt_no_tools"
    if (scope["framework_session_id"] == "career-sim-runner-7a72e52cc135"
            or context_game == "cc0ca28b4e694fd993c60b538aac3c80"
            or (isinstance(probe, dict) and probe.get("game_session_id") == "cc0ca28b4e694fd993c60b538aac3c80")
            or prior_scope):
        return "halt"
    if probe is None:
        return ("reserve_before_one_create" if fresh and absence_confirmed and not continuation
                and context_game is None else "halt")
    actual_marker_path = actual_marker_path or scope["probe_path"]
    if not reference_marker_semantics(scope, probe, actual_marker_path) or probe["phase"] != "bound":
        return "halt"
    if not reference_bound_state(scope, probe, state, probe["verified_path"], context_game=context_game):
        return "halt"
    return "recover_native_observe_and_logs"


def reference_state_for_scope(scope, game_id=SID):
    """Synthetic in-memory fixture; never rewrite a real checkpoint."""
    state = json.loads(re.search(r"```json\s*(.*?)\s*```", SKILLS["career-controller"], re.S).group(1))
    state["session_id"] = game_id
    state["strategy"]["checkpoint"].update({
        "verified_directory": scope["verified_directory"],
        "verified_path": str(type_path(scope["verified_directory"]) / reference_state_filename(game_id)),
        "reason": "synthetic offline bound fixture", "halted_reason": None})
    return state


def reference_one_create_authority(scope, marker, actual_path, *, write_ok, read_ok,
                                   fresh_initial=False, same_uninterrupted_request=False,
                                   just_reserved=False, existing_marker=False):
    return (write_ok is True and read_ok is True and fresh_initial is True
            and same_uninterrupted_request is True and just_reserved is True
            and existing_marker is False
            and reference_marker_semantics(scope, marker, actual_path)
            and marker["phase"] == "reserved"
            and scope["framework_session_id"] != "career-sim-runner-7a72e52cc135")


def reference_native_create_result(payload: dict) -> str | None:
    # A native-response fixture; this never calls new_game.
    if not isinstance(payload, dict) or "error" in payload:
        return None
    game_id = payload.get("session_id")
    try:
        reference_state_filename(game_id)
    except (ValueError, TypeError):
        return None
    return game_id


class BootstrapRevisionTests(unittest.TestCase):
    def setUp(self):
        self.scope = reference_framework_scope(TASK_DIR, INTERNAL_DIR)

    def test_scope_uses_trusted_cwd_binding_not_generic_workspace(self):
        self.assertEqual(self.scope["framework_session_id"], F_ID)
        self.assertEqual(PureWindowsPath(self.scope["probe_path"]).parent, PureWindowsPath(TASK_DIR))
        with self.assertRaises(ValueError):
            reference_framework_scope(INTERNAL_DIR, INTERNAL_DIR)

    def test_windows_and_posix_source_layouts(self):
        scope = reference_framework_scope("/instance/agent/workspace/projects/" + F_ID,
                                          "/instance/agent/workspace")
        self.assertEqual(scope["framework_session_id"], F_ID)
        self.assertTrue(scope["probe_path"].startswith(scope["verified_directory"] + "/"))

    def test_rejects_bound_project_relative_unc_and_dot_paths(self):
        for bad in ["projects/" + F_ID, "\\\\server\\share\\" + F_ID,
                    INTERNAL_DIR + "\\projects\\..\\projects\\" + F_ID,
                    TASK_DIR + "\\.", TASK_DIR + "\\child", INTERNAL_DIR + "\\other\\" + F_ID]:
            with self.subTest(path=bad), self.assertRaises(ValueError):
                reference_framework_scope(bad, INTERNAL_DIR)
        with self.assertRaises(ValueError):
            reference_framework_scope(TASK_DIR, INTERNAL_DIR, project_bound=True)

    def test_framework_whitelist_rejects_lossy_sanitization_and_wrong_length(self):
        for bad in ["unknown", "default", "career-sim-runner-ABCDEF012345", F_ID + "x",
                    "career-sim-runner-012345abcde", "career-sim-runner-012345abcdeg",
                    "career-sim-runner-012345abcde\u0430", "career-sim-runner-012345abcdef.json"]:
            with self.subTest(id=bad), self.assertRaises(ValueError):
                reference_framework_scope(INTERNAL_DIR + "\\projects\\" + bad, INTERNAL_DIR)

    def test_framework_id_is_never_valid_as_game_id(self):
        with self.assertRaises(ValueError):
            reference_state_filename(F_ID)
        self.assertIsNone(reference_native_create_result({"session_id": F_ID}))
        self.assertEqual(reference_native_create_result({"session_id": SID}), SID)

    def test_fresh_missing_marker_requires_reservation_before_create(self):
        self.assertEqual(reference_bootstrap(self.scope, None, fresh=True, absence_confirmed=True), "reserve_before_one_create")
        self.assertEqual(reference_bootstrap(self.scope, None), "halt")
        self.assertEqual(reference_bootstrap(self.scope, None, fresh=True, context_game=SID), "halt")

    def test_automatic_continuation_is_never_fresh_even_without_marker(self):
        self.assertEqual(reference_bootstrap(self.scope, None, fresh=True, continuation=True), "halt")

    def test_reserved_create_timeout_never_recreates_game(self):
        marker = reference_probe(self.scope)
        for continuation in (False, True):
            self.assertEqual(reference_bootstrap(self.scope, marker, fresh=True,
                                                continuation=continuation), "halt")
        self.assertIsNone(marker["game_session_id"])

    def test_existing_unrecognized_marker_never_overwritten_or_used(self):
        for marker in [{}, "invalid JSON", {"phase": "bound", "game_session_id": SID}]:
            self.assertEqual(reference_bootstrap(self.scope, marker, fresh=True), "halt")

    def test_create_error_or_missing_id_leaves_reservation(self):
        reserved = reference_probe(self.scope)
        for payload in [{"error": "timeout", "session_id": SID}, {}, {"session_id": "unknown"},
                        {"session_id": "../other"}, {"session_id": None}]:
            with self.subTest(payload=payload):
                self.assertIsNone(reference_native_create_result(payload))
                self.assertEqual(reference_bootstrap(self.scope, reserved, continuation=True), "halt")

    def test_bound_marker_recovers_only_real_game_in_same_framework(self):
        marker = reference_probe(self.scope, SID, "bound")
        self.assertEqual(reference_bootstrap(self.scope, marker, continuation=True, context_game=SID,
                                             state=reference_state_for_scope(self.scope)),
                         "recover_native_observe_and_logs")
        self.assertEqual(reference_state_filename(marker["game_session_id"]), f"career-state-{SID}.json")

    def test_conflicting_unknown_or_framework_continuation_id_halts(self):
        marker = reference_probe(self.scope, SID, "bound")
        for conflicting in ["unknown", F_ID, "b" * 32]:
            self.assertEqual(reference_bootstrap(self.scope, marker, continuation=True,
                                                context_game=conflicting), "halt")

    def test_cross_framework_directory_schema_and_version_rejected(self):
        for key, value in [("framework_session_id", "career-sim-runner-ffffffffffff"),
                           ("verified_directory", INTERNAL_DIR), ("schema_version", 99),
                           ("solution_version", "0.3.1")]:
            marker = reference_probe(self.scope, SID, "bound")
            marker[key] = value
            self.assertEqual(reference_bootstrap(self.scope, marker, continuation=True), "halt")

    def test_halted_latch_blocks_generic_continuation_and_tools(self):
        marker = reference_probe(self.scope, SID, "halted", "MCP unavailable")
        self.assertEqual(reference_bootstrap(self.scope, marker, continuation=True), "halt")
        self.assertEqual(reference_bootstrap(self.scope, None, fresh=True, continuation=True, halted=True),
                         "halt_no_tools")

    def test_all_storage_capabilities_and_explicit_absence_are_required(self):
        evidence = dict.fromkeys(["assigned_directory", "framework_scope", "native_write_tool",
                                  "native_read_tool", "probe_absent", "confirmed_fresh_start",
                                  "write_succeeded", "readback_matches",
                                  "semantic_paths_match", "marker_payload_validated"], True)
        self.assertTrue(reference_storage_gate(**evidence))
        for key in evidence:
            invalid = evidence.copy()
            invalid[key] = False
            self.assertFalse(reference_storage_gate(**invalid))

    def test_direct_file_call_budget_is_seven_not_per_action(self):
        self.assertEqual(POLICY["storage_gate_file_calls"], 3)
        self.assertEqual(reference_checkpoint_calls(["session_bound"]), 4)
        self.assertEqual(reference_checkpoint_calls(["ordinary_success"]), 0)
        self.assertIn("Seven startup calls", read(SOLUTION / "design/skills_design.md"))

    def test_documents_agree_on_two_ids_source_scope_and_latched_halt(self):
        controller = SKILLS["career-controller"]
        for phrase in ["career-sim-runner-[0-9a-f]{12}", "framework_session_id", "game_session_id",
                       "phase=reserved", "phase=bound", "phase=halted", "explicit not-found",
                       "Never overwrite an unrecognized file", "single-driver", "not an atomic lock",
                       "generic Runner continuation", "not separately supplied"]:
            self.assertIn(phrase, controller)
        fence = chr(96) * 3
        checkpoint = json.loads(re.search(fence + r"json\s*(.*?)\s*" + fence, controller, re.S).group(1))
        self.assertNotIn("framework_session_id", checkpoint["strategy"]["checkpoint"])
        self.assertIn("verified_directory", checkpoint["strategy"]["checkpoint"])
        self.assertNotIn("task_id", checkpoint["strategy"]["checkpoint"])
        manifest = json.loads(read(SOLUTION / "manifest.json"))
        self.assertEqual(manifest["name"], "Career Survival V0.3.3")
        self.assertIn("Engineering halts remain latched", manifest["instruction"])

    def test_three_professional_skills_and_old_archives_unchanged(self):
        original = ROOT / "v031-review.zip"
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(),
                         "f660c49b4d845527729dc1e795487d257b6998724243cd0cec35cfc5db83ad83")
        with zipfile.ZipFile(original) as old:
            for name in EXPECTED_SKILLS - {"career-controller"}:
                relative = f"solution/skills/{name}/SKILL.md"
                self.assertEqual((ROOT / relative).read_bytes(), old.read(relative))
            old_tree = ast.parse(old.read("offline_tests/test_v03.py").decode("utf-8"))
        def case_names(tree):
            return {f"{node.name}.{m.name}" for node in tree.body if isinstance(node, ast.ClassDef)
                    for m in node.body if isinstance(m, ast.FunctionDef) and m.name.startswith("test_")}
        previous = case_names(old_tree)
        self.assertEqual(len(previous), 74)
        self.assertTrue(previous <= case_names(ast.parse(read(Path(__file__)))))
        self.assertEqual(hashlib.sha256((ROOT / "v03-review.zip").read_bytes()).hexdigest(),
                         "fa249d8277817e0df31eb32e0cb166e0a6aa5eef92e931c16e3b7a461ee0e999")


class BootstrapSourceTests(unittest.TestCase):
    """Actual selected source fragments under memory stubs, not an Agent run."""
    def test_actual_runner_noncontinue_allocates_new_id_and_continue_reuses_old(self):
        source = ROOT / "career_sim_runner/headless_play.py"
        ns = isolated_definitions(source, {"new_drive_session_id", "resolve_drive_session_id"}, {
            "uuid": SimpleNamespace(uuid4=lambda: SimpleNamespace(hex="012345abcdef" + "0" * 20)),
            "DRIVE_SESSION_PREFIX": source_literal(ROOT / "career_sim_runner/constants.py", "DRIVE_SESSION_PREFIX"),
            "load_last_drive_session_id": lambda: "career-sim-runner-ffffffffffff"})
        self.assertEqual(ns["resolve_drive_session_id"](False), F_ID)
        self.assertEqual(ns["resolve_drive_session_id"](True), "career-sim-runner-ffffffffffff")

    def test_actual_default_builder_fallback_is_shared_and_not_accepted_scope(self):
        class MemoryPath:
            def __init__(self, value):
                self.value = PureWindowsPath(value)
            def __truediv__(self, suffix):
                return MemoryPath(str(self.value / suffix))
            def mkdir(self, **kwargs):
                pass
        ns = isolated_definitions(ROOT / ".venv/Lib/site-packages/jiuwenswarm/common/utils.py",
            {"get_default_project_session_workspace_dir"}, {"Path": MemoryPath, "re": re,
            "get_default_project_workspace_dir": lambda: MemoryPath(INTERNAL_DIR + "\\projects")})
        shared = str(ns["get_default_project_session_workspace_dir"](None).value)
        self.assertEqual(shared, INTERNAL_DIR + "\\projects")
        with self.assertRaises(ValueError):
            reference_framework_scope(shared, INTERNAL_DIR)

    def test_runner_envelope_contains_internal_id_but_no_project_or_cwd(self):
        ns = isolated_definitions(ROOT / "career_sim_runner/ws_client.py", {"_build_envelope"},
                                  {"Any": Any, "uuid": SimpleNamespace(uuid4=lambda: SimpleNamespace(hex="0" * 32))})
        envelope = ns["_build_envelope"]("fixture prompt", F_ID, "agent")
        self.assertEqual(envelope["session_id"], F_ID)
        self.assertNotIn("cwd", envelope["params"])
        self.assertNotIn("project_dir", envelope["params"])
        self.assertNotIn(F_ID, envelope["params"]["content"])

    def test_actual_no_project_path_builder_isolates_framework_id(self):
        class MemoryPath:
            def __init__(self, value):
                self.value = PureWindowsPath(value)
            def __truediv__(self, suffix):
                return MemoryPath(str(self.value / suffix))
            def mkdir(self, **kwargs):
                pass  # In-memory stub; no directories are created.
        utils = ROOT / ".venv/Lib/site-packages/jiuwenswarm/common/utils.py"
        ns = isolated_definitions(utils, {"get_default_project_session_workspace_dir"},
                                  {"Path": MemoryPath, "re": re,
                                   "get_default_project_workspace_dir": lambda: MemoryPath(INTERNAL_DIR + "\\projects")})
        result = ns["get_default_project_session_workspace_dir"](F_ID)
        self.assertEqual(str(result.value), TASK_DIR)
        self.assertNotEqual(str(ns["get_default_project_session_workspace_dir"]("other").value), TASK_DIR)

    def test_actual_runtime_directory_prompt_exposes_bound_path(self):
        path = ROOT / ".venv/Lib/site-packages/jiuwenswarm/agents/harness/common/rails/runtime_prompt_rail.py"
        tree = ast.parse(read(path))
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "RuntimePromptRail")
        method = next(n for n in cls.body if isinstance(n, ast.AsyncFunctionDef) and n.name == "before_model_call")
        block = next(n for n in method.body if isinstance(n, ast.If)
                     and ast.unparse(n.test) == "self._channel in ('tui', 'web')")
        fn = ast.FunctionDef(name="emit", args=ast.arguments(posonlyargs=[], args=[ast.arg(arg="self")],
                              kwonlyargs=[], kw_defaults=[], defaults=[]), body=[block], decorator_list=[])
        module = ast.Module(body=[fn], type_ignores=[])
        sections = {}
        fake = SimpleNamespace(_channel="web", _trusted_dirs=[], _workspace_dir=INTERNAL_DIR,
                               _project_dir=None, _cwd=TASK_DIR, _force_english=True, _language="en",
                               _existing_dirs=lambda x: [], _existing_dir=lambda x: x,
                               _same_path=lambda a, b: PureWindowsPath(a) == PureWindowsPath(b),
                               system_prompt_builder=SimpleNamespace(add_section=lambda section: sections.update({section.name: section})))
        bindings = {"PromptSection": SimpleNamespace, "get_agent_workspace_dir": lambda: INTERNAL_DIR,
                    "get_user_workspace_dir": lambda: PureWindowsPath(r"C:\verified-instance")}
        exec(compile(ast.fix_missing_locations(module), str(path), "exec"), bindings)
        bindings["emit"](fake)
        text = sections["tui_current_project_policy"].content["en"]
        self.assertIn("Current project directory: not set", text)
        self.assertIn("Current working directory (cwd and Bash default directory): " + TASK_DIR, text)
        self.assertIn("Agent internal data directory: " + INTERNAL_DIR, text)
        self.assertEqual(reference_framework_scope(TASK_DIR, INTERNAL_DIR)["framework_session_id"], F_ID)
        # Exercise the installed Chinese prompt branch, too, without initialization.
        fake._force_english = False
        fake._language = "cn"
        bindings["emit"](fake)
        chinese = sections["tui_current_project_policy"].content["cn"]
        self.assertIn("当前项目目录：未设置", chinese)
        self.assertIn("当前工作目录（cwd，也是 Bash 默认执行目录）：" + TASK_DIR, chinese)
        self.assertIn("Agent 内部数据目录：" + INTERNAL_DIR, chinese)

    def test_source_signatures_show_internal_id_and_native_file_tools_not_exclusive_lock(self):
        base = ROOT / ".venv/Lib/site-packages"
        prompt = read(ROOT / "career_sim_runner/prompts/play_headless.md")
        self.assertNotIn("framework_session_id", prompt)
        self.assertNotIn("task_id", prompt)
        rail = read(base / "openjiuwen/harness/rails/sys_operation_rail.py")
        for text in ["ReadFileTool(", "WriteFileTool(", "agent.ability_manager.add_ability(tool.card, tool)"]:
            self.assertIn(text, rail)
        files = ast.parse(read(base / "openjiuwen/harness/tools/filesystem.py"))
        cls = next(n for n in files.body if isinstance(n, ast.ClassDef) and n.name == "WriteFileTool")
        invoke = next(n for n in cls.body if isinstance(n, ast.AsyncFunctionDef) and n.name == "invoke")
        body = ast.unparse(invoke)
        self.assertIn("create_if_not_exist=True", body)
        self.assertNotIn("exclusive=True", body)
        self.assertIn("_append_op_history", body)
        driver = read(ROOT / "career_sim_runner/ws_client.py")
        self.assertIn('termination_reason = "max_continuations"', driver)
        self.assertIn("if _has_ended(game)", driver)


def reference_material_risk_update(before, after, *, material_warning=False):
    """Persistence examples only, not hidden failure thresholds or risk scoring."""
    if material_warning:
        return True
    before = before or {}
    for field in ("network", "health", "dignity", "wealth"):
        value = after.get(field)
        old = before.get(field)
        vulnerable = (isinstance(value, (int, float)) and not isinstance(value, bool)
                      and (value < 0 if field == "wealth" else value == 0))
        was_vulnerable = (isinstance(old, (int, float)) and not isinstance(old, bool)
                          and (old < 0 if field == "wealth" else old == 0))
        if (vulnerable or was_vulnerable) and value != old:
            return True
    return False


def reference_unique_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate JSON key")
            result[key] = value
        return result
    return json.loads(text, object_pairs_hook=pairs)


class FixedMarkerRegressionTests(unittest.TestCase):
    """C: deterministic examples, including actual bad fixtures. Not LLM behavior."""
    @classmethod
    def setUpClass(cls):
        if hashlib.sha256(RUN2_REVIEW_ZIP.read_bytes()).hexdigest() != "d35bf6fd4e99c66069b39fbf2bad97c81a443392ecc2c2b44f7595bea3d8084f":
            raise AssertionError("Run-two review ZIP changed")
        with zipfile.ZipFile(RUN2_REVIEW_ZIP) as archive:
            cls.bad_probe = json.loads(archive.read(
                "run2/storage-snapshot/career-checkpoint-probe-7a72e52cc135.json"))
            cls.bad_state = json.loads(archive.read(
                "run2/storage-snapshot/career-state-cc0ca28b4e694fd993c60b538aac3c80.json"))

    def setUp(self):
        self.scope = reference_framework_scope(TASK_DIR, INTERNAL_DIR)
        self.marker = reference_probe(self.scope, SID, "bound")
        self.state = reference_state_for_scope(self.scope)

    def test_fixed_filename_has_no_generated_id_suffix(self):
        self.assertEqual(type_path(self.scope["probe_path"]).name, "career-checkpoint.json")
        self.assertNotIn("framework_session_id", self.marker)
        self.assertNotIn("framework_session_id", self.state["strategy"]["checkpoint"])

    def test_original_truncated_run_two_marker_is_rejected(self):
        self.assertEqual(self.bad_probe["framework_session_id"], "7a72e52cc135")
        self.assertFalse(reference_marker_semantics(self.scope, self.bad_probe, self.scope["probe_path"]))
        self.assertEqual(reference_bootstrap(self.scope, self.bad_probe, fresh=True), "halt")

    def test_actual_native_readback_success_still_contains_bad_semantics(self):
        with zipfile.ZipFile(RUN2_REVIEW_ZIP) as archive:
            calls = json.loads(archive.read("audit/deduplicated-calls.json"))
        result = calls["results"]["call_00_wOchBCw9E1XoDxp5fMMa9491"]["parsed"]
        lines = result["content"].splitlines()
        unnumbered = []
        for i, line in enumerate(lines, 1):
            match = re.fullmatch(r"\s*" + str(i) + r"\t(.*)", line)
            self.assertIsNotNone(match)
            unnumbered.append(match.group(1))
        parsed = reference_unique_json("\n".join(unnumbered))
        expected_reserved = {**self.bad_probe, "phase": "reserved", "game_session_id": None}
        self.assertEqual(parsed, expected_reserved)
        self.assertFalse(reference_marker_semantics(self.scope, parsed, result["file_path"]))
        bound_result = calls["results"][calls["file_ops"][-1]["id"]]["parsed"]
        bound_text = "\n".join(re.sub(r"^\s*\d+\t", "", line, count=1)
                               for line in bound_result["content"].splitlines())
        self.assertEqual(reference_unique_json(bound_text), self.bad_probe)
        self.assertFalse(reference_marker_semantics(self.scope, self.bad_probe, bound_result["file_path"]))

    def test_full_json_values_are_not_display_escapes_or_line_prefixes(self):
        serialized = json.dumps(self.marker, indent=2)
        displayed = "\n".join(f"{i:6d}\t{line}" for i, line in enumerate(serialized.splitlines(), 1))
        stripped = "\n".join(re.sub(r"^\s*\d+\t", "", line, count=1) for line in displayed.splitlines())
        parsed = reference_unique_json(stripped)
        self.assertEqual(parsed["verified_directory"], self.scope["verified_directory"])
        self.assertTrue(reference_marker_semantics(self.scope, parsed, self.scope["probe_path"]))

    def test_renaming_bad_marker_and_bumping_version_does_not_fix_identity(self):
        forged = deepcopy(self.bad_probe)
        forged.update(schema_version=2, solution_version="0.3.3")
        self.assertFalse(reference_marker_semantics(self.scope, forged, self.scope["probe_path"]))
        self.assertIn("framework_session_id", forged)

    def test_original_state_remains_legacy_even_with_valid_game_uuid(self):
        self.assertRegex(self.bad_state["session_id"], r"^[0-9a-f]{32}$")
        self.assertFalse(reference_bound_state(self.scope, self.marker, self.bad_state,
                                               self.marker["verified_path"]))
        forged = deepcopy(self.bad_state)
        forged.update(schema_version=2, solution_version="0.3.3", session_id=SID)
        self.assertFalse(reference_bound_state(self.scope, self.marker, forged,
                                               self.marker["verified_path"]))

    def test_complete_legal_binding_passes_reference_semantics(self):
        self.assertTrue(reference_marker_semantics(self.scope, self.marker, self.scope["probe_path"]))
        self.assertTrue(reference_bound_state(self.scope, self.marker, self.state,
                                              self.marker["verified_path"], context_game=SID))
        self.assertEqual(reference_bootstrap(self.scope, self.marker, continuation=True,
                                             state=self.state, context_game=SID),
                         "recover_native_observe_and_logs")

    def test_same_basename_different_task_directories_do_not_cross_restore(self):
        other = reference_framework_scope(INTERNAL_DIR + "\\projects\\career-sim-runner-abcdef012345", INTERNAL_DIR)
        self.assertEqual(type_path(other["probe_path"]).name, type_path(self.scope["probe_path"]).name)
        self.assertNotEqual(other["probe_path"], self.scope["probe_path"])
        self.assertFalse(reference_marker_semantics(other, self.marker, other["probe_path"]))
        self.assertFalse(reference_bound_state(other, self.marker, self.state, self.marker["verified_path"]))

    def test_matching_wrong_path_and_json_cannot_override_independent_scope(self):
        forged = deepcopy(self.marker)
        wrong = INTERNAL_DIR + "\\projects\\career-sim-runner-abcdef012345"
        forged["verified_directory"] = wrong
        forged["verified_path"] = str(type_path(wrong) / reference_state_filename(SID))
        self.assertFalse(reference_marker_semantics(self.scope, forged,
                                                    str(type_path(wrong) / "career-checkpoint.json")))

    def test_marker_actual_path_must_equal_fixed_path(self):
        wrong = str(type_path(TASK_DIR) / "career-checkpoint-probe-012345abcdef.json")
        self.assertFalse(reference_marker_semantics(self.scope, self.marker, wrong))

    def test_game_uuid_conflicts_at_each_binding_are_rejected(self):
        for key in ("state", "marker", "context"):
            marker, state, context = deepcopy(self.marker), deepcopy(self.state), SID
            if key == "state":
                state["session_id"] = "f" * 32
            elif key == "marker":
                marker["game_session_id"] = "f" * 32
            else:
                context = "f" * 32
            self.assertFalse(reference_bound_state(self.scope, marker, state,
                                                   marker["verified_path"], context_game=context))

    def test_verified_path_is_full_state_file_not_directory_or_marker(self):
        for wrong in (TASK_DIR, self.scope["probe_path"], "career-state-" + SID + ".json"):
            marker = deepcopy(self.marker)
            marker["verified_path"] = wrong
            self.assertFalse(reference_marker_semantics(self.scope, marker, self.scope["probe_path"]))
            state = deepcopy(self.state)
            state["strategy"]["checkpoint"]["verified_path"] = wrong
            self.assertFalse(reference_bound_state(self.scope, self.marker, state, self.marker["verified_path"]))

    def test_directory_field_cannot_be_a_full_file_path(self):
        marker = deepcopy(self.marker)
        marker["verified_directory"] = self.marker["verified_path"]
        self.assertFalse(reference_marker_semantics(self.scope, marker, self.scope["probe_path"]))

    def test_all_existing_nonbound_states_block_new_game(self):
        for phase in ("reserved", "halted", "error", "unknown", None):
            marker = reference_probe(self.scope, None, phase)
            self.assertEqual(reference_bootstrap(self.scope, marker, fresh=True,
                                                 absence_confirmed=True), "halt")

    def test_unknown_or_framework_game_id_is_rejected(self):
        for value in ("unknown", F_ID, "7a72e52cc135", "../other", None, 42, "a" * 31):
            marker = deepcopy(self.marker)
            marker["game_session_id"] = value
            self.assertFalse(reference_marker_semantics(self.scope, marker, self.scope["probe_path"]))

    def test_read_write_success_without_semantics_does_not_authorize_create(self):
        reserved = reference_probe(self.scope)
        reserved["verified_directory"] = INTERNAL_DIR
        self.assertFalse(reference_one_create_authority(self.scope, reserved, self.scope["probe_path"],
                         write_ok=True, read_ok=True, fresh_initial=True,
                         same_uninterrupted_request=True, just_reserved=True))

    def test_only_fresh_same_request_semantic_reservation_can_authorize_one_create(self):
        reserved = reference_probe(self.scope)
        evidence = dict(write_ok=True, read_ok=True, fresh_initial=True,
                        same_uninterrupted_request=True, just_reserved=True, existing_marker=False)
        self.assertTrue(reference_one_create_authority(self.scope, reserved, self.scope["probe_path"], **evidence))
        for key in evidence:
            changed = {**evidence, key: not evidence[key]}
            self.assertFalse(reference_one_create_authority(self.scope, reserved, self.scope["probe_path"], **changed))

    def test_preexisting_valid_reserved_is_not_same_request_authority(self):
        self.assertFalse(reference_one_create_authority(self.scope, reference_probe(self.scope),
                         self.scope["probe_path"], write_ok=True, read_ok=True,
                         fresh_initial=True, same_uninterrupted_request=True,
                         just_reserved=True, existing_marker=True))

    def test_missing_state_with_bound_marker_halts_not_new_game(self):
        self.assertEqual(reference_bootstrap(self.scope, self.marker, fresh=True,
                                             absence_confirmed=True, state=None), "halt")

    def test_missing_marker_on_continuation_or_known_prior_scope_halts(self):
        self.assertEqual(reference_bootstrap(self.scope, None, fresh=True,
                                             continuation=True, absence_confirmed=True), "halt")
        self.assertEqual(reference_bootstrap(self.scope, None, fresh=True,
                                             prior_scope=True, absence_confirmed=True), "halt")

    def test_explicit_absence_and_fresh_provenance_are_separate_requirements(self):
        self.assertEqual(reference_bootstrap(self.scope, None, fresh=True), "halt")
        self.assertEqual(reference_bootstrap(self.scope, None, absence_confirmed=True), "halt")

    def test_known_run_two_scope_and_game_are_protected(self):
        protected = reference_framework_scope(INTERNAL_DIR + "\\projects\\career-sim-runner-7a72e52cc135", INTERNAL_DIR)
        self.assertEqual(reference_bootstrap(protected, None, fresh=True, absence_confirmed=True), "halt")
        marker = reference_probe(self.scope, "cc0ca28b4e694fd993c60b538aac3c80", "bound")
        self.assertEqual(reference_bootstrap(self.scope, marker, state=self.state), "halt")

    def test_uncertain_execution_never_replays_old_choice_even_without_pending(self):
        for status in (None, "none", "pending", "confirmed", "uncertain"):
            result = reference_recovery(status, "missing_log", True)
            self.assertTrue(result["native_checks_required"])
            self.assertFalse(result["resend_cached_choice"])
            self.assertEqual(result["next"], "stop_uncertain")

    def test_marker_schema_types_and_extra_or_duplicate_keys_rejected(self):
        for key, value in (("schema_version", "2"), ("schema_version", True),
                           ("solution_version", "0.3.2"), ("halted_reason", "stopped"),
                           ("framework_session_id", F_ID)):
            marker = {**self.marker, key: value}
            self.assertFalse(reference_marker_semantics(self.scope, marker, self.scope["probe_path"]))
        with self.assertRaises(ValueError):
            reference_unique_json('{"verified_directory":"good","verified_directory":"bad"}')

    def test_reserved_marker_rejects_nonnull_game_or_full_path(self):
        for key, value in (("game_session_id", SID), ("verified_path", self.marker["verified_path"])):
            marker = {**reference_probe(self.scope), key: value}
            self.assertFalse(reference_marker_semantics(self.scope, marker, self.scope["probe_path"]))

    def test_original_ninety_six_case_names_remain(self):
        with zipfile.ZipFile(ROOT / "v032-review.zip") as old:
            previous = ast.parse(old.read("offline_tests/test_v03.py").decode("utf-8"))
        def names(tree):
            return {f"{c.name}.{f.name}" for c in tree.body if isinstance(c, ast.ClassDef)
                    for f in c.body if isinstance(f, ast.FunctionDef) and f.name.startswith("test_")}
        self.assertEqual(len(names(previous)), 96)
        self.assertTrue(names(previous) <= names(ast.parse(read(Path(__file__)))))

    def test_v032_zip_and_all_specialist_strategy_bytes_are_unchanged(self):
        oldzip = ROOT / "v032-review.zip"
        self.assertEqual(hashlib.sha256(oldzip.read_bytes()).hexdigest(),
                         "0abe41b0915d649edd41375d1d6416f0feca23d077e80d0932b6660c36d892a0")
        with zipfile.ZipFile(oldzip) as old:
            for name in EXPECTED_SKILLS - {"career-controller"}:
                path = f"solution/skills/{name}/SKILL.md"
                self.assertEqual((ROOT / path).read_bytes(), old.read(path))

    def test_documents_use_fixed_marker_independent_directory_and_protected_history(self):
        for text in (SKILLS["career-controller"], read(SOLUTION / "README.md"),
                     read(SOLUTION / "design/skills_design.md"),
                     json.loads(read(SOLUTION / "manifest.json"))["instruction"]):
            self.assertIn("career-checkpoint.json", text)
            self.assertIn("verified_directory", text)
            self.assertIn("verified_path", text)
        self.assertIn("not independently enforced tool-boundary validators", SKILLS["career-controller"])


class VulnerabilityPersistenceTests(unittest.TestCase):
    """C/A: persistence reference examples and document agreement, not risk scoring."""
    def test_first_network_zero_with_no_warning_is_material(self):
        self.assertTrue(reference_material_risk_update({"network": 1}, {"network": 0}))
        self.assertTrue(reference_material_risk_update(None, {"network": 0}))
        self.assertEqual(reference_checkpoint_calls(["risk_changed"]), 1)

    def test_unchanged_network_zero_deduplicates_but_does_not_resolve(self):
        self.assertFalse(reference_material_risk_update({"network": 0}, {"network": 0}))
        self.assertEqual(reference_risk("unresolved", "empty_events"), "unresolved")

    def test_actual_warning_and_visible_vulnerability_are_distinct_sources(self):
        self.assertTrue(reference_material_risk_update({"network": 3}, {"network": 3}, material_warning=True))
        self.assertTrue(reference_material_risk_update({"network": 0}, {"network": 1}))
        self.assertEqual(reference_risk("monitoring", "benign_feedback"), "monitoring")

    def test_no_invented_health_three_or_other_hidden_threshold(self):
        self.assertFalse(reference_material_risk_update({"health": 4}, {"health": 3}))
        self.assertTrue(reference_material_risk_update({"wealth": 0}, {"wealth": -1}))
        self.assertTrue(reference_material_risk_update({"dignity": 1}, {"dignity": 0}))

    def test_controller_requires_persistence_before_next_call_and_preserves_risk_skill(self):
        text = SKILLS["career-controller"]
        self.assertIn("even with empty events", text)
        self.assertIn("checkpoint before the next game call", text)
        self.assertIn("not a hidden failure threshold", text)
        with zipfile.ZipFile(ROOT / "v032-review.zip") as old:
            self.assertEqual((SOLUTION / "skills/risk-management/SKILL.md").read_bytes(),
                             old.read("solution/skills/risk-management/SKILL.md"))


# V0.3.3 preservation baseline captured before any runtime mutation (none authorized).
INSTANCE = Path('C:\\Users\\Ray\\.jiuwenswarm-instances\\career_emu')
RUN2_AUDIT = Path('C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z')
RUN2_REVIEW_ZIP = ROOT.parents[1] / "run2-v032-gpt-review-20261020.zip"
PRESERVED_RUN2_SHA256 = {'C:\\Users\\Ray\\.jiuwenswarm-instances\\career_emu\\agent\\sessions\\career-sim-runner-7a72e52cc135\\history.jsonl': '4d583afe1391362b2e91f29a5461a5852bd7ebfbdef5bae73507446fb77ed39c',
 'C:\\Users\\Ray\\.jiuwenswarm-instances\\career_emu\\agent\\sessions\\career-sim-runner-7a72e52cc135\\metadata.json': '1cb054d814979901da2bde74d3926362f7561ccc5d39eb280b91832962e1f60c',
 'C:\\Users\\Ray\\.jiuwenswarm-instances\\career_emu\\agent\\workspace\\IDENTITY.md': '43b12307b544948252a26c3ba0bc720586df498309ac5b5397961423dec04127',
 'C:\\Users\\Ray\\.jiuwenswarm-instances\\career_emu\\agent\\workspace\\projects\\career-sim-runner-7a72e52cc135\\career-checkpoint-probe-7a72e52cc135.json': '0c78577e421ed4a282e86269881d6bc1f41b392c5cdcf11253bb68d5b537c1e5',
 'C:\\Users\\Ray\\.jiuwenswarm-instances\\career_emu\\agent\\workspace\\projects\\career-sim-runner-7a72e52cc135\\career-state-cc0ca28b4e694fd993c60b538aac3c80.json': '24024bfdaa88cdd91d64d8e7547940dbaedd139b2172c2c5dca1a4c7b1c142e2',
 'C:\\Users\\Ray\\.jiuwenswarm-instances\\career_emu\\agent\\workspace\\skills\\career-controller\\SKILL.md': 'da532176cf47655b844f78a0f0f929fd5b69aa84ce26a9cbaa7846c3778e7631',
 'C:\\Users\\Ray\\.jiuwenswarm-instances\\career_emu\\agent\\workspace\\skills\\career-planning\\SKILL.md': 'e7271fee67833a8bcbcef3a427d92de084d7ec12dce7d1d8e1a4bbb02d0209b4',
 'C:\\Users\\Ray\\.jiuwenswarm-instances\\career_emu\\agent\\workspace\\skills\\resource-optimisation\\SKILL.md': '0447df5d7746cf9eed66d02943352a726f02c4f30bb3f35e817d6708f64efabd',
 'C:\\Users\\Ray\\.jiuwenswarm-instances\\career_emu\\agent\\workspace\\skills\\risk-management\\SKILL.md': 'ae859c195ee133a3363baa6974c6326721e7aeb6c23de445c4b016678745ffcb',
 'C:\\Users\\Ray\\.jiuwenswarm-instances\\career_emu\\agent\\workspace\\skills\\skills_state.json': '654b63d4e6d565e999d09896994dac457d7925a756e15ffd91570f21eeafdb56',
 'C:\\Users\\Ray\\.jiuwenswarm-instances\\career_emu\\config\\.env': '321d2cc61c347fa7b2103834ea7b911aed5ff507b9a91e4c7d5380fe61766adf',
 'C:\\Users\\Ray\\.jiuwenswarm-instances\\career_emu\\config\\config.yaml': '109448f0c71d854202a977ff1d9539991fd495378e5333a247d53ecdbedb58cd',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\IDENTITY-before.md': '43b12307b544948252a26c3ba0bc720586df498309ac5b5397961423dec04127',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\agent-session-after\\history.jsonl': '4d583afe1391362b2e91f29a5461a5852bd7ebfbdef5bae73507446fb77ed39c',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\agent-session-after\\metadata.json': '1cb054d814979901da2bde74d3926362f7561ccc5d39eb280b91832962e1f60c',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\baseline-comparison-input.json': '658170dc73dd58fb614fc2c0df67976975665d553acb5f0a5f5c9ea4f3435898',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\cc0ca28b4e694fd993c60b538aac3c80.log': '1437707502b2acdd96a09817913918c33cdddd5cffcfe6d5245a0b4bf6761136',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\config-before\\.env': '321d2cc61c347fa7b2103834ea7b911aed5ff507b9a91e4c7d5380fe61766adf',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\config-before\\builtin_rules.yaml': 'd81413b9ffae62f15bfcd32e1ea446ef7230e18e3cd30408f614c9806df0e1ce',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\config-before\\config.lock': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\config-before\\config.yaml': '109448f0c71d854202a977ff1d9539991fd495378e5333a247d53ecdbedb58cd',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\config-before\\runtime_state\\career-sim-runner-b7d5117302ee.yaml': '29b5ecb4c9f7c8c357abe3bde17882a27d05ae78321b6551f52331bb60a5016a',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\config-before\\runtime_state\\heartbeat_1a1559f59f5_61f8ee.yaml': '39e42afe50bd60b94b1ff31b7b92375257988077636159e328fb8ceba888fbd7',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\config-before\\runtime_state\\heartbeat_1a155d65d98_c3ac67.yaml': '39e42afe50bd60b94b1ff31b7b92375257988077636159e328fb8ceba888fbd7',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\config-before\\runtime_state\\heartbeat_1a158420d0d_0dbb0d.yaml': '39e42afe50bd60b94b1ff31b7b92375257988077636159e328fb8ceba888fbd7',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\config-before\\runtime_state\\web_1a15149c3cf_29e4ed8259bb.yaml': '751e5635e480cad2f57e7dbf7dc1cb1b0d0b08a8aa6167914a4e6f88a4d49441',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\config-before\\runtime_state\\web_1a156ee54a7_6acd1e7d423f.yaml': '29b5ecb4c9f7c8c357abe3bde17882a27d05ae78321b6551f52331bb60a5016a',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\config-before\\runtime_state\\web_1a156f881b3_48d70a01bcf9.yaml': '29b5ecb4c9f7c8c357abe3bde17882a27d05ae78321b6551f52331bb60a5016a',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\config-before\\runtime_state\\web_1a159f2f066_0acb52eb316a.yaml': '29b5ecb4c9f7c8c357abe3bde17882a27d05ae78321b6551f52331bb60a5016a',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\database-after.sqlite3': '6f5833e31b6db69346d2079f1e4d1322093ea905ff013cf865284cd1c6c10a58',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\deduplicated-calls.json': '906bd0c1d6edd0661863582c89837ad1449237b7a88b44e8081eae68fa559271',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\finalize_audit.py': '4a4e7836c9e515f57b3e01661dcc5d2a43e3f25f81656dce948c1c6dc2464e49',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\game-workspace-after\\career-checkpoint-probe-7a72e52cc135.json': '0c78577e421ed4a282e86269881d6bc1f41b392c5cdcf11253bb68d5b537c1e5',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\game-workspace-after\\career-state-cc0ca28b4e694fd993c60b538aac3c80.json': '24024bfdaa88cdd91d64d8e7547940dbaedd139b2172c2c5dca1a4c7b1c142e2',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\mcp-preflight.json': '0263052771018c0411101fe46b276f5029c398b755cef1b2e92b95368dbe539d',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\model-events.json': '3e138bece64042eb0ebb255a039aa3379f9af832d4b2c643f784cd4973a1ac26',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\model-usage.json': 'f8b16442a60fa8391e2ed72a029d8a3d65eab010a266310a61fb5bee88a635e2',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\monitor-latest.json': '22311060a5e1f6c40d1f31cf06bda0e1e2d042a6049eb6cc82b13d1083be4fed',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\monitor.py': '17d3867b96b2507c6779da3d54aba8ecb3647bc1679226a1d7cf703464cb3d66',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\new-game-persisted-state.json': '93ddcce7acd9c94b63d8346037144d11fb7df910bcc1964536a8e6701930e67f',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\post-game-audit.md': '28a4cd4c39910be9cf323b72f8f52faeeadbfcdd3f078dcd8b77bc87399a20ab',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\preflight.json': 'f69cb3a9fdb1afca86c6ece00c680b953e085c258ca07943f18b7ed172e6a981',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\run-audit.json': 'bd14737ee40aa376d5bd5c98f27073da7568dd267eb633a35621625821039e83',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\run-output-after\\events-20261020T155544Z.jsonl': 'ac95e6a1d3b52f44e8c809f0093de04dae61b27713b5d3e17c0f8fb922245eb5',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\run-output-after\\transcript-20261020T155544Z.log': '028b16777051a5b0d3d9534e51b1e64828663cc6f20b8c4c956d5a5fddd0b207',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runner-before\\active_install.json': '58b14ea6eaac7ab514501708210f2065b9d363691625a12869b0864380d24484',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runner-before\\career_emulator.sqlite3': '30e85ac20fe2f787c6dd302ff8c31ee4edaf3a33532c080d290d81200d20775a',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runner-before\\emulator_logs\\a86e8ff1b7924a598bc63422d52afd69.log': '92177d3b38e7184cc208f8f452afb293f98e5e2cbe8813217cb093b81a11b340',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runner-before\\last_drive_session.txt': '8967b29d65f246d6861a751fd515d94650bf3b70ce46e2ece8a3a9a5ac4a1f9b',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runner-before\\last_output_dir.txt': '1e7549c5910a3479486444818d7cb7ac074f6420d2f8a652767f60d5df4bebaa',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runner-before\\outputs\\The Raytirement Plan\\20261019T214724Z\\events-20261019T214724Z.jsonl': 'b812092d975116d1b22c9c68516b2a7f84bf7ed433e60155f39e32586716e455',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runner-before\\outputs\\The Raytirement Plan\\20261019T214724Z\\score_report.json': '1b1c00b4e89a3727cd29e854f90ddc7eb74ddd2d114e7317daa76f86d5cd1cca',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runner-before\\outputs\\The Raytirement Plan\\20261019T214724Z\\transcript-20261019T214724Z.log': '8eab88153e78a59f26ea34952e0f6f0ae0f8fd759462d5f021d012b6714490ab',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runtime-log-deltas\\agent\\.logs\\agent_server.log': 'ced51edef30a5c090b863125b20c28ff72fa6ff64ec1a90ea973e2ca38d32359',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runtime-log-deltas\\agent\\.logs\\channel.log': '01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runtime-log-deltas\\agent\\.logs\\full.log': '14b6e57737b2d8364478f316e9c6bfb4992765b8c0cf53dbf38a4cb842f5ad7c',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runtime-log-deltas\\agent\\.logs\\gateway.log': '96323ab744b98c2f00e154a9401b8d4bea807f243081462b5f60fcd6ac0045c3',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runtime-log-deltas\\agent\\.logs\\permissions.log': '01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runtime-log-deltas\\agent\\.logs\\ws-dev.log': '01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runtime-log-deltas\\logs\\logs\\llm.log': 'f8b181e991a631b04f92f5f54b21f98b79f348566fc7d74e46bd0facfd2293c3',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runtime-log-deltas\\logs\\logs\\memory.log': '91e0f78da88326616c51d2ebae680638ebd9a2a28ddaa7bd2b7d9f7487703b4c',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runtime-log-deltas\\logs\\logs\\run\\jiuwen.log': 'b9adf52722bdfe033c8452662eb73695062ec5529fa865d1d4bcae82b5b29839',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runtime-log-deltas\\logs\\logs\\runner.log': '836d9354047343483c0976f84bcc2c6e0967ab477c1315238e41ab3b3b430dc9',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runtime-log-deltas\\logs\\logs\\server.log': 'e55f5bd1922f8bbd1eb16371bdfdb639a7e87f0d843b2b4afa5cf2c70a203875',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runtime-log-deltas\\logs\\logs\\session.log': 'bbf80f922cee57801fd34dda5091ec590fc27803857082e9a1aecd0dd0801d44',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\runtime-log-deltas\\logs\\logs\\sys_operation.log': '650d36664437b66f10a7254ab1d5e385cb21ad155a8c2196da79491537794b3c',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\skills-before\\career-controller\\SKILL.md': 'da532176cf47655b844f78a0f0f929fd5b69aa84ce26a9cbaa7846c3778e7631',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\skills-before\\career-planning\\SKILL.md': 'e7271fee67833a8bcbcef3a427d92de084d7ec12dce7d1d8e1a4bbb02d0209b4',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\skills-before\\resource-optimisation\\SKILL.md': '0447df5d7746cf9eed66d02943352a726f02c4f30bb3f35e817d6708f64efabd',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\skills-before\\risk-management\\SKILL.md': 'ae859c195ee133a3363baa6974c6326721e7aeb6c23de445c4b016678745ffcb',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\skills-before\\skills_state.json': '654b63d4e6d565e999d09896994dac457d7925a756e15ffd91570f21eeafdb56',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\backups\\v032-run2-20261020T155233130707Z\\stop-result.json': 'ba25aa38546fec529d3f1f21a8f36e08bb4ba0bccc91ab980a4f334075a90565',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\run2-v032-gpt-review-20261020.zip': 'd35bf6fd4e99c66069b39fbf2bad97c81a443392ecc2c2b44f7595bea3d8084f',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\starter-kit\\techarena-career-sim\\.career_sim_runner\\career_emu\\active_install.json': '58b14ea6eaac7ab514501708210f2065b9d363691625a12869b0864380d24484',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\starter-kit\\techarena-career-sim\\.career_sim_runner\\career_emu\\career_emulator.sqlite3': '6f5833e31b6db69346d2079f1e4d1322093ea905ff013cf865284cd1c6c10a58',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\starter-kit\\techarena-career-sim\\.career_sim_runner\\career_emu\\emulator_logs\\a86e8ff1b7924a598bc63422d52afd69.log': '92177d3b38e7184cc208f8f452afb293f98e5e2cbe8813217cb093b81a11b340',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\starter-kit\\techarena-career-sim\\.career_sim_runner\\career_emu\\emulator_logs\\cc0ca28b4e694fd993c60b538aac3c80.log': '1437707502b2acdd96a09817913918c33cdddd5cffcfe6d5245a0b4bf6761136',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\starter-kit\\techarena-career-sim\\.career_sim_runner\\career_emu\\last_drive_session.txt': 'ad118492ec41950abcd6f02953095ef5e87ed73e98c579534d70755d2d3e6718',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\starter-kit\\techarena-career-sim\\.career_sim_runner\\career_emu\\last_output_dir.txt': 'c46194862791bf16bc409411c62c5bd418e786d1f029bfa0f85aa6304d98e0bd',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\starter-kit\\techarena-career-sim\\.career_sim_runner\\career_emu\\outputs\\The Raytirement Plan\\20261019T214724Z\\events-20261019T214724Z.jsonl': 'b812092d975116d1b22c9c68516b2a7f84bf7ed433e60155f39e32586716e455',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\starter-kit\\techarena-career-sim\\.career_sim_runner\\career_emu\\outputs\\The Raytirement Plan\\20261019T214724Z\\score_report.json': '1b1c00b4e89a3727cd29e854f90ddc7eb74ddd2d114e7317daa76f86d5cd1cca',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\starter-kit\\techarena-career-sim\\.career_sim_runner\\career_emu\\outputs\\The Raytirement Plan\\20261019T214724Z\\transcript-20261019T214724Z.log': '8eab88153e78a59f26ea34952e0f6f0ae0f8fd759462d5f021d012b6714490ab',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\starter-kit\\techarena-career-sim\\.career_sim_runner\\career_emu\\outputs\\The Raytirement Plan\\20261020T155544Z\\events-20261020T155544Z.jsonl': 'ac95e6a1d3b52f44e8c809f0093de04dae61b27713b5d3e17c0f8fb922245eb5',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\starter-kit\\techarena-career-sim\\.career_sim_runner\\career_emu\\outputs\\The Raytirement Plan\\20261020T155544Z\\transcript-20261020T155544Z.log': '028b16777051a5b0d3d9534e51b1e64828663cc6f20b8c4c956d5a5fddd0b207',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\starter-kit\\techarena-career-sim\\.env': 'f6f468ac5c73de64dd3669cdce65feeaad056645857c4e114d24c7cdf009a54c',
 'C:\\Users\\Ray\\Desktop\\tech-arena\\starter-kit\\techarena-career-sim\\uv.lock': 'faa577d46300f939e4273698c6c40a448680b9f25b8047eeb5b65437f310774f'}


if __name__ == "__main__":
    print("OFFLINE ONLY: isolated source parsers + documented policy fixtures; no Agent/model/game.", flush=True)
    print(f"Verified backup fixture: {BACKUP}", flush=True)
    unittest.main(verbosity=2)
