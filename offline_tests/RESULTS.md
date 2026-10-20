# V0.3.3 offline verification

Final result: **131 passed, 0 failures, 0 errors, 0 skips**. All **96 original V0.3.2 test method names** remain and pass; **35 new cases** cover the actual bad run-two snapshots, fixed-marker scope/semantics, risk persistence and source-backed fresh-directory behavior.

Executed 2026-10-20T16:34:27.131210+00:00.

```powershell
.\.venv\Scripts\python.exe -B -X utf8 offline_tests/test_v03.py
```

## Evidence classes and limits

| Class | Passed | What this verifies |
| --- | ---: | --- |
| A. Document/source/file consistency | 24 | JSON/YAML/manifest, required text, archives and SHA-256 protection |
| B. Actual isolated official functions/source fragments | 15 | Selected validators, parsers, directory builder/prompt and Runner fresh-vs-continue selection under in-memory stubs |
| C. Deterministic policy-reference examples | 92 | Proposed binding, replay fence, risk, routing, feedback and budget behavior; **not LLM behavior** |

No model, service, native file tool, MCP or simulator is invoked; no framework/game package is imported or initialized. The two actual bad JSON fixtures are read in memory from immutable run2-v032-gpt-review-20261020.zip (SHA-256 d35bf6fd4e99c66069b39fbf2bad97c81a443392ecc2c2b44f7595bea3d8084f); nothing is extracted into a runtime directory. Helpers are outside solution and are not a Python Router.

## Preserved original tests: phase-aware evidence correction

Before this revision, running the untouched 96-case suite found two outdated test methods: three failed subassertions expected the live pre-install database, old skills_state and career-survival file; one error expected the live first-run session deleted by the separately authorized V0.3.2 install. They were not new V0.3.3 regressions. Their original historical hashes are still checked against immutable V0.2/pre-install backup copies. Current instance/config/installed Skills, run-two session/state/database/logs and audit/review evidence are additionally pinned by **86 exact SHA-256 fingerprints** captured before any runtime mutation (none authorized). No test is skipped and no deleted historical file is silently restored.

## New safety coverage

- Fixed career-checkpoint.json under trusted full task directory D; no persisted framework_session_id or ID-suffixed probe.
- Original truncated probe rejected; merely renaming/bumping its version cannot repair it. Original state remains legacy; valid game UUID alone is insufficient.
- Legal synthetic full binding succeeds; actual returned marker/state paths and JSON directory/full-state paths are compared with independent D/G evidence.
- Same marker basename in different task directories cannot cross-restore; mismatched game UUID/unknown ID/schema/type/phase/duplicate or extra keys reject.
- Existing reserved/halted/malformed/conflicting markers, missing marker/state on recovery and uncertain creation never authorize new_game. I/O success is not semantic validity.
- Known unfinished run-two scope/game are protected; no migration or recovery implemented. Uncertain execution always fences with native observation/log reasoning and never replays cached choice.
- Network=0 can trigger a compact checkpoint without an events warning; unchanged repeats deduplicate and visible improvement does not prove hidden clearance. No Health=3 or other new hidden cutoff is introduced.
- The actual isolated Runner selects a new framework ID without continue, and uses the prior ID with continue; default builder's shared fallback is rejected.

- Actual native read-back fixtures include data.file_path and line-numbered data.content: removing only display prefixes reveals the rejected reserved marker and later bound marker. A separate legal display fixture preserves the parsed full directory. This is parsing/reference evidence, not live model/file acceptance.

One newly added native-readback assertion initially compared the reserved-stage read with the final bound-stage file and failed. The fixture assertion was corrected to validate both stages separately against their actual contents; no production rule was weakened. The complete final suite passes.

## Reproduction requirements

This suite intentionally depends on the current local Starter Kit/installed source and immutable historical evidence paths, including run-two review ZIP and backup manifests. The ten-file review ZIP is not a self-contained simulator/test installation. Missing fixtures must fail rather than be synthesized. All successful reference checks remain separate from runtime Agent compliance, storage durability, recovery and terminal acceptance. No installation or game is authorized by these results.

## Complete results

| Class | Test | Result |
| --- | --- | --- |
| C | `BootstrapRevisionTests.test_all_storage_capabilities_and_explicit_absence_are_required` | PASS |
| C | `BootstrapRevisionTests.test_automatic_continuation_is_never_fresh_even_without_marker` | PASS |
| C | `BootstrapRevisionTests.test_bound_marker_recovers_only_real_game_in_same_framework` | PASS |
| C | `BootstrapRevisionTests.test_conflicting_unknown_or_framework_continuation_id_halts` | PASS |
| C | `BootstrapRevisionTests.test_create_error_or_missing_id_leaves_reservation` | PASS |
| C | `BootstrapRevisionTests.test_cross_framework_directory_schema_and_version_rejected` | PASS |
| C | `BootstrapRevisionTests.test_direct_file_call_budget_is_seven_not_per_action` | PASS |
| A | `BootstrapRevisionTests.test_documents_agree_on_two_ids_source_scope_and_latched_halt` | PASS |
| C | `BootstrapRevisionTests.test_existing_unrecognized_marker_never_overwritten_or_used` | PASS |
| C | `BootstrapRevisionTests.test_framework_id_is_never_valid_as_game_id` | PASS |
| C | `BootstrapRevisionTests.test_framework_whitelist_rejects_lossy_sanitization_and_wrong_length` | PASS |
| C | `BootstrapRevisionTests.test_fresh_missing_marker_requires_reservation_before_create` | PASS |
| C | `BootstrapRevisionTests.test_halted_latch_blocks_generic_continuation_and_tools` | PASS |
| C | `BootstrapRevisionTests.test_rejects_bound_project_relative_unc_and_dot_paths` | PASS |
| C | `BootstrapRevisionTests.test_reserved_create_timeout_never_recreates_game` | PASS |
| C | `BootstrapRevisionTests.test_scope_uses_trusted_cwd_binding_not_generic_workspace` | PASS |
| A | `BootstrapRevisionTests.test_three_professional_skills_and_old_archives_unchanged` | PASS |
| C | `BootstrapRevisionTests.test_windows_and_posix_source_layouts` | PASS |
| B | `BootstrapSourceTests.test_actual_default_builder_fallback_is_shared_and_not_accepted_scope` | PASS |
| B | `BootstrapSourceTests.test_actual_no_project_path_builder_isolates_framework_id` | PASS |
| B | `BootstrapSourceTests.test_actual_runner_noncontinue_allocates_new_id_and_continue_reuses_old` | PASS |
| B | `BootstrapSourceTests.test_actual_runtime_directory_prompt_exposes_bound_path` | PASS |
| B | `BootstrapSourceTests.test_runner_envelope_contains_internal_id_but_no_project_or_cwd` | PASS |
| A | `BootstrapSourceTests.test_source_signatures_show_internal_id_and_native_file_tools_not_exclusive_lock` | PASS |
| C | `CandidateRevisionTests.test_at_most_three_distinct_candidates_not_a_full_search` | PASS |
| C | `CandidateRevisionTests.test_capped_recovery_alone_removed_but_after_cost_preserved` | PASS |
| A | `CandidateRevisionTests.test_document_limits_candidates_and_preserves_unknowns` | PASS |
| C | `CandidateRevisionTests.test_first_step_then_new_menu_instead_of_cached_sequence` | PASS |
| C | `CandidateRevisionTests.test_menu_budget_and_severe_risk_filtering` | PASS |
| C | `CandidateRevisionTests.test_mitigation_reservation_survives_shortlisting` | PASS |
| C | `CandidateRevisionTests.test_obvious_disadvantage_requires_known_comparable_risk` | PASS |
| C | `CandidateRevisionTests.test_unknown_effects_are_not_ranked_as_zero_or_dominated` | PASS |
| C | `FeedbackRevisionTests.test_capability_scope_relationship_candidates_must_be_offered` | PASS |
| A | `FeedbackRevisionTests.test_feedback_loop_and_repetition_evidence_are_explicit_in_document` | PASS |
| C | `FeedbackRevisionTests.test_high_grade_no_evidence_does_not_force_variety_or_more_output` | PASS |
| C | `FeedbackRevisionTests.test_high_performance_no_promotion_visibility_feedback` | PASS |
| C | `FeedbackRevisionTests.test_long_tenure_reassesses_without_inventing_gate` | PASS |
| C | `FeedbackRevisionTests.test_poor_results_and_visibility_feedback_are_different` | PASS |
| C | `FeedbackRevisionTests.test_promotion_and_poor_grade_remain_separate_facts` | PASS |
| C | `FeedbackRevisionTests.test_severe_risk_overrides_optional_development` | PASS |
| C | `FixedMarkerRegressionTests.test_actual_native_readback_success_still_contains_bad_semantics` | PASS |
| C | `FixedMarkerRegressionTests.test_all_existing_nonbound_states_block_new_game` | PASS |
| C | `FixedMarkerRegressionTests.test_complete_legal_binding_passes_reference_semantics` | PASS |
| C | `FixedMarkerRegressionTests.test_directory_field_cannot_be_a_full_file_path` | PASS |
| A | `FixedMarkerRegressionTests.test_documents_use_fixed_marker_independent_directory_and_protected_history` | PASS |
| C | `FixedMarkerRegressionTests.test_explicit_absence_and_fresh_provenance_are_separate_requirements` | PASS |
| C | `FixedMarkerRegressionTests.test_fixed_filename_has_no_generated_id_suffix` | PASS |
| C | `FixedMarkerRegressionTests.test_full_json_values_are_not_display_escapes_or_line_prefixes` | PASS |
| C | `FixedMarkerRegressionTests.test_game_uuid_conflicts_at_each_binding_are_rejected` | PASS |
| C | `FixedMarkerRegressionTests.test_known_run_two_scope_and_game_are_protected` | PASS |
| C | `FixedMarkerRegressionTests.test_marker_actual_path_must_equal_fixed_path` | PASS |
| C | `FixedMarkerRegressionTests.test_marker_schema_types_and_extra_or_duplicate_keys_rejected` | PASS |
| C | `FixedMarkerRegressionTests.test_matching_wrong_path_and_json_cannot_override_independent_scope` | PASS |
| C | `FixedMarkerRegressionTests.test_missing_marker_on_continuation_or_known_prior_scope_halts` | PASS |
| C | `FixedMarkerRegressionTests.test_missing_state_with_bound_marker_halts_not_new_game` | PASS |
| C | `FixedMarkerRegressionTests.test_only_fresh_same_request_semantic_reservation_can_authorize_one_create` | PASS |
| A | `FixedMarkerRegressionTests.test_original_ninety_six_case_names_remain` | PASS |
| C | `FixedMarkerRegressionTests.test_original_state_remains_legacy_even_with_valid_game_uuid` | PASS |
| C | `FixedMarkerRegressionTests.test_original_truncated_run_two_marker_is_rejected` | PASS |
| C | `FixedMarkerRegressionTests.test_preexisting_valid_reserved_is_not_same_request_authority` | PASS |
| C | `FixedMarkerRegressionTests.test_read_write_success_without_semantics_does_not_authorize_create` | PASS |
| C | `FixedMarkerRegressionTests.test_renaming_bad_marker_and_bumping_version_does_not_fix_identity` | PASS |
| C | `FixedMarkerRegressionTests.test_reserved_marker_rejects_nonnull_game_or_full_path` | PASS |
| C | `FixedMarkerRegressionTests.test_same_basename_different_task_directories_do_not_cross_restore` | PASS |
| C | `FixedMarkerRegressionTests.test_uncertain_execution_never_replays_old_choice_even_without_pending` | PASS |
| C | `FixedMarkerRegressionTests.test_unknown_or_framework_game_id_is_rejected` | PASS |
| A | `FixedMarkerRegressionTests.test_v032_zip_and_all_specialist_strategy_bytes_are_unchanged` | PASS |
| C | `FixedMarkerRegressionTests.test_verified_path_is_full_state_file_not_directory_or_marker` | PASS |
| C | `PersistenceRevisionTests.test_binding_probe_has_explicit_one_time_cost` | PASS |
| A | `PersistenceRevisionTests.test_controller_documents_gate_atomicity_limit_and_costs` | PASS |
| C | `PersistenceRevisionTests.test_identical_warning_and_clean_handoff_do_not_write` | PASS |
| C | `PersistenceRevisionTests.test_material_triggers_each_write_once` | PASS |
| C | `PersistenceRevisionTests.test_ordinary_action_and_observation_zero_file_calls` | PASS |
| C | `PersistenceRevisionTests.test_recovered_commit_uses_new_menu_never_cached_intent` | PASS |
| C | `PersistenceRevisionTests.test_recovery_fence_even_with_no_pending_or_confirmed_checkpoint` | PASS |
| C | `PersistenceRevisionTests.test_review_promotion_strategy_batch_coalesces` | PASS |
| C | `PersistenceRevisionTests.test_storage_capability_cannot_be_assumed` | PASS |
| C | `PersistenceRevisionTests.test_unchanged_stats_are_not_nonexecution_proof` | PASS |
| C | `ResourceTests.test_cap_and_order_change_known_marginal_gain` | PASS |
| C | `ResourceTests.test_choice_numbers_are_from_current_menu_not_cached_categories` | PASS |
| C | `ResourceTests.test_known_report_comparison_is_not_hidden_safety_claim` | PASS |
| C | `ResourceTests.test_only_health_and_dignity_have_documented_caps` | PASS |
| C | `ResourceTests.test_public_costs_and_all_budget_three_sequences` | PASS |
| C | `ResourceTests.test_reserve_two_energy_for_relevant_mitigation` | PASS |
| C | `ResourceTests.test_zero_budget_and_reduced_current_menu` | PASS |
| A | `RiskTests.test_documented_statuses_and_risk_score_goal` | PASS |
| C | `RiskTests.test_explicit_resolution_is_scoped` | PASS |
| C | `RiskTests.test_mitigation_does_not_prove_clearance` | PASS |
| B | `RiskTests.test_official_pending_warning_consumption_in_memory_only` | PASS |
| C | `RiskTests.test_rejected_mitigation_and_recurring_warning_preserve_issue` | PASS |
| C | `RiskTests.test_warning_survives_empty_events` | PASS |
| A | `RoutingTests.test_all_routes_use_only_installed_skill_names` | PASS |
| C | `RoutingTests.test_energy_routes_all_three_methods_in_order` | PASS |
| A | `RoutingTests.test_loading_rules_and_single_executor_are_explicit` | PASS |
| C | `RoutingTests.test_new_warning_precedes_review_planning` | PASS |
| C | `RoutingTests.test_recovery_and_uncertain_action_return_to_controller` | PASS |
| C | `RoutingTests.test_story_and_main_use_risk_and_career` | PASS |
| C | `RoutingTests.test_terminal_overrides_warning_and_stops_specialists` | PASS |
| C | `StateAndTimingTests.test_all_eight_review_entries_and_unknowns_can_survive_roundtrip` | PASS |
| C | `StateAndTimingTests.test_cross_session_and_unknown_schema_rejected` | PASS |
| C | `StateAndTimingTests.test_current_choice_session_notes_and_local_revision` | PASS |
| C | `StateAndTimingTests.test_final_review_already_processed_has_no_future_window` | PASS |
| C | `StateAndTimingTests.test_json_state_example_has_minimal_required_fields` | PASS |
| A | `StateAndTimingTests.test_ordinary_observe_is_not_a_checkpoint_trigger` | PASS |
| C | `StateAndTimingTests.test_pending_intent_is_not_permission_to_resend` | PASS |
| A | `StateAndTimingTests.test_review_grade_is_not_promotion_and_raw_scales_not_thresholds` | PASS |
| C | `StateAndTimingTests.test_same_month_energy_cannot_reopen_processed_review` | PASS |
| C | `StateAndTimingTests.test_session_filename_isolation_and_path_traversal_rejection` | PASS |
| A | `SubmissionTests.test_exact_submission_files_and_no_legacy_skill` | PASS |
| B | `SubmissionTests.test_frontmatter_matches_directories_and_official_validator` | PASS |
| A | `SubmissionTests.test_local_weights_match_actual_baseline` | PASS |
| B | `SubmissionTests.test_manifest_official_validator_and_persistent_constraints` | PASS |
| A | `SubmissionTests.test_native_mcp_signatures_from_installed_source_without_import` | PASS |
| B | `SubmissionTests.test_official_frontmatter_negative_fixtures` | PASS |
| B | `SubmissionTests.test_official_manifest_rejects_placeholders_and_bad_mode` | PASS |
| B | `TerminalAndBackupTests.test_actual_archived_ending_recognized_as_native_terminal` | PASS |
| A | `TerminalAndBackupTests.test_archived_files_match_recorded_checksums` | PASS |
| A | `TerminalAndBackupTests.test_baseline_source_and_results_preserved_outside_submission` | PASS |
| B | `TerminalAndBackupTests.test_bash_printed_ending_not_native_terminal` | PASS |
| B | `TerminalAndBackupTests.test_game_over_error_and_malformed_payload` | PASS |
| B | `TerminalAndBackupTests.test_native_new_game_signal_parsed_without_calling_a_game` | PASS |
| A | `TerminalAndBackupTests.test_no_framework_or_game_package_initialized` | PASS |
| A | `TerminalAndBackupTests.test_only_four_verified_legacy_files_were_cleaned` | PASS |
| A | `TerminalAndBackupTests.test_original_session_and_file_history_preserved` | PASS |
| A | `TerminalAndBackupTests.test_protected_source_config_indexes_and_baseline_bytes_unchanged` | PASS |
| B | `TerminalAndBackupTests.test_successful_final_action_needs_followup_observe` | PASS |
| C | `VulnerabilityPersistenceTests.test_actual_warning_and_visible_vulnerability_are_distinct_sources` | PASS |
| A | `VulnerabilityPersistenceTests.test_controller_requires_persistence_before_next_call_and_preserves_risk_skill` | PASS |
| C | `VulnerabilityPersistenceTests.test_first_network_zero_with_no_warning_is_material` | PASS |
| C | `VulnerabilityPersistenceTests.test_no_invented_health_three_or_other_hidden_threshold` | PASS |
| C | `VulnerabilityPersistenceTests.test_unchanged_network_zero_deduplicates_but_does_not_resolve` | PASS |
