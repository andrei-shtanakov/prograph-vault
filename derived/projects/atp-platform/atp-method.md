<!-- prograph:generated -->

---
indexed_at: "2026-07-10T12:31:55Z"
kind: python
name: atp-method
parent: atp-platform
prograph: project
root: ./atp-platform/packages/atp-method
snapshot: 4
---

# atp-method

> ATP plugin that runs [`method/`](../../method/) agent-eval-case methodology cases through the platform: a schema model + a loader that maps each case to an ATP `TestDefinition`, a methodology-aware…

## Manifest

- declared package: `atp-method` version `0.1.0`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

_None._

### Public symbols

- `TEXT_SUFFIXES` (const) — `atp_method/corpus.py:15`
- `normalize_lf` (function) — `atp_method/corpus.py:87`
- `CorpusResolver` (class) — `atp_method/corpus.py:126`
- `CorpusIntegrityVerifier` (class) — `atp_method/corpus.py:177`
- `CorpusMaterializer` (class) — `atp_method/corpus.py:254`
- `generate_manifest` (function) — `atp_method/corpus_manifest.py:11`
- `DEFAULT_MODEL` (const) — `atp_method/envelopes.py:16`
- `REVIEW_ENVELOPE` (const) — `atp_method/envelopes.py:18`
- `GENERIC_ENVELOPE` (const) — `atp_method/envelopes.py:26`
- `get_envelope` (function) — `atp_method/envelopes.py:35`
- `build_prompt` (function) — `atp_method/envelopes.py:40`
- `CRITICAL_THRESHOLD` (const) — `atp_method/evaluators/case_evaluator.py:26`
- `AgentEvalCaseEvaluator` (class) — `atp_method/evaluators/case_evaluator.py:29`
- `METHOD_CRITICAL_CHECK` (const) — `atp_method/loader.py:28`
- `METHOD_RUBRIC` (const) — `atp_method/loader.py:29`
- `case_to_test_definition` (function) — `atp_method/loader.py:117`
- `load_case` (function) — `atp_method/loader.py:156`
- `is_agent_eval_case` (function) — `atp_method/loader.py:169`
- `load_suite` (function) — `atp_method/loader.py:192`
- `register` (function) — `atp_method/plugin.py:44`
- `serve_corpus_tools` (function) — `atp_method/runtime.py:33`
- `CorpusRunPreparer` (class) — `atp_method/runtime.py:52`
- `Status` (const) — `atp_method/schema.py:23`
- `SuiteType` (const) — `atp_method/schema.py:24`
- `Capability` (const) — `atp_method/schema.py:25`
- `ConstructionAxis` (const) — `atp_method/schema.py:33`
- `AxisLevel` (const) — `atp_method/schema.py:41`
- `ToolName` (const) — `atp_method/schema.py:42`
- `SideEffects` (const) — `atp_method/schema.py:43`
- `ArtifactType` (const) — `atp_method/schema.py:44`
- `GraderType` (const) — `atp_method/schema.py:45`
- `TurnRole` (const) — `atp_method/schema.py:53`
- `RunMode` (const) — `atp_method/schema.py:54`
- `WIRED_RUN_MODES` (const) — `atp_method/schema.py:57`
- `Artifact` (class) — `atp_method/schema.py:77`
- `CorpusDigest` (class) — `atp_method/schema.py:89`
- `ArtifactCorpus` (class) — `atp_method/schema.py:105`
- `CorpusFileMetadata` (class) — `atp_method/schema.py:140`
- `CorpusMetadata` (class) — `atp_method/schema.py:150`
- `RubricItem` (class) — `atp_method/schema.py:168`
- `ExpectedFinding` (class) — `atp_method/schema.py:177`
- `ForbiddenAnchor` (class) — `atp_method/schema.py:187`
- `Turn` (class) — `atp_method/schema.py:195`
- `Environment` (class) — `atp_method/schema.py:204`
- `Grader` (class) — `atp_method/schema.py:222`
- `BehaviorAssertion` (class) — `atp_method/schema.py:277`
- `OutputContract` (class) — `atp_method/schema.py:287`
- `Provenance` (class) — `atp_method/schema.py:299`
- `AgentEvalCase` (class) — `atp_method/schema.py:321`
- `TASK_TYPE_TO_BENCHMARK_ID` (const) — `atp_method/taxonomy.py:11`
- `benchmark_id_for` (function) — `atp_method/taxonomy.py:17`
- `REPO_ROOT` (const) — `tests/conftest.py:8`
- `EXAMPLE_CASES_DIR` (const) — `tests/conftest.py:9`
- `ROOT` (const) — `tests/test_cases_load.py:12`
- `CASES` (const) — `tests/test_cases_load.py:13`
- `REQ_CASES` (const) — `tests/test_cases_load.py:14`
- `SCHEMA` (const) — `tests/test_cases_load.py:15`
- `test_cases_present` (function) — `tests/test_cases_load.py:18`
- `test_cases_validate_pydantic_and_contract` (function) — `tests/test_cases_load.py:27`
- `test_req_extraction_cases_present` (function) — `tests/test_cases_load.py:44`
- `test_req_extraction_cases_are_deterministic` (function) — `tests/test_cases_load.py:53`
- `test_all_code_review_cases_discovered` (function) — `tests/test_code_review_structured.py:14`
- `test_every_code_review_case_declares_object_output_contract` (function) — `tests/test_code_review_structured.py:20`
- `test_code_review_prompt_uses_object_format_instruction` (function) — `tests/test_code_review_structured.py:34`
- `test_object_output_grades_through_case_schema` (function) — `tests/test_code_review_structured.py:49`
- `test_resolver_selects_canonical_sorted_included_files` (function) — `tests/test_corpus.py:85`
- `test_resolver_rejects_symlink_selected_file` (function) — `tests/test_corpus.py:104`
- `test_verifier_requires_manifest_paths_to_match_selected_set` (function) — `tests/test_corpus.py:115`
- `test_verifier_rejects_duplicate_manifest_paths` (function) — `tests/test_corpus.py:131`
- `test_verifier_hashes_lf_normalized_content_and_builds_line_index` (function) — `tests/test_corpus.py:151`
- `test_verifier_rejects_hash_mismatch` (function) — `tests/test_corpus.py:169`
- `test_materializer_copies_verified_files_preserving_relative_paths` (function) — `tests/test_corpus.py:187`
- `test_materializer_accepts_safe_single_corpus_id` (function) — `tests/test_corpus.py:215`
- `test_materializer_rejects_absolute_corpus_id_without_touching_outside_paths` (function) — `tests/test_corpus.py:248`
- `test_default_model_is_pinned` (function) — `tests/test_envelopes.py:13`
- `test_get_envelope_review` (function) — `tests/test_envelopes.py:17`
- `test_get_envelope_unknown_raises` (function) — `tests/test_envelopes.py:22`
- `test_build_prompt_inlines_task_and_artifacts` (function) — `tests/test_envelopes.py:27`
- `test_build_prompt_tolerates_missing_fields` (function) — `tests/test_envelopes.py:43`
- `test_build_prompt_delivers_loader_artifacts_end_to_end` (function) — `tests/test_envelopes.py:47`
- `test_build_prompt_uses_format_instruction_when_present` (function) — `tests/test_envelopes.py:77`
- `test_build_prompt_includes_response_schema_with_format_instruction` (function) — `tests/test_envelopes.py:97`
- `test_build_prompt_falls_back_to_review_without_contract` (function) — `tests/test_envelopes.py:131`
- `test_build_prompt_contract_without_instruction_uses_review` (function) — `tests/test_envelopes.py:137`
- `test_build_prompt_includes_corpus_id_and_paths_without_file_contents` (function) — `tests/test_envelopes.py:151`
- `test_build_prompt_lists_fixture_corpus_paths_without_inlining_fixture_text` (function) — `tests/test_envelopes.py:183`
- `FakeJudge` (class) — `tests/test_evaluator.py:16`
- `RecordingJudge` (class) — `tests/test_evaluator.py:127`
- `BombJudge` (class) — `tests/test_evaluator.py:204`
- `test_load_clean_case_structure` (function) — `tests/test_loader.py:16`
- `test_critical_check_is_a_hard_gate` (function) — `tests/test_loader.py:27`
- `test_rubric_assertion_present_when_rubric_exists` (function) — `tests/test_loader.py:37`
- `test_governance_and_sweep_tags` (function) — `tests/test_loader.py:45`
- `test_tools_mapped_to_allowed_tools` (function) — `tests/test_loader.py:54`
- `test_none_tools_becomes_empty_allow_list` (function) — `tests/test_loader.py:60`
- `test_no_rubric_emits_only_critical` (function) — `tests/test_loader.py:85`
- `test_loader_threads_checker_into_critical_config` (function) — `tests/test_loader.py:102`
- `test_loader_appends_behavior_assertions_as_normal_assertions` (function) — `tests/test_loader.py:131`
- `test_loader_preserves_reserved_critical_config_values` (function) — `tests/test_loader.py:187`
- `test_tags_include_case_version` (function) — `tests/test_loader.py:247`
- `test_tags_include_task_type_and_language_when_set` (function) — `tests/test_loader.py:275`
- `test_tags_omit_task_type_language_when_absent` (function) — `tests/test_loader.py:308`
- `REPO_ROOT` (const) — `tests/test_loader_artifact_corpus.py:9`
- `CORPUS_CASE_PATH` (const) — `tests/test_loader_artifact_corpus.py:10`
- `CORPUS_ASSETS_PATH` (const) — `tests/test_loader_artifact_corpus.py:17`
- `test_loader_preserves_corpus_metadata_without_inlining_contents` (function) — `tests/test_loader_artifact_corpus.py:79`
- `test_loader_loads_corpus_backed_req_extraction_fixture` (function) — `tests/test_loader_artifact_corpus.py:96`
- `test_output_contract_goes_into_input_data` (function) — `tests/test_loader_output_contract.py:46`
- `test_critical_assertion_carries_schema_and_assertions` (function) — `tests/test_loader_output_contract.py:53`
- `test_findings_match_case_gets_null_schema_empty_assertions` (function) — `tests/test_loader_output_contract.py:61`
- `ROOT` (const) — `tests/test_p2_correctness_determinism.py:9`
- `CHECKER` (const) — `tests/test_p2_correctness_determinism.py:10`
- `L1` (const) — `tests/test_p2_correctness_determinism.py:24`
- `test_l1_good_passes` (function) — `tests/test_p2_correctness_determinism.py:30`
- `test_l1_miss_fails` (function) — `tests/test_p2_correctness_determinism.py:44`
- `test_l1_near_miss_anchor_not_accepted` (function) — `tests/test_p2_correctness_determinism.py:49`
- `test_l1_wellformed_not_malformed` (function) — `tests/test_p2_correctness_determinism.py:58`
- `L2` (const) — `tests/test_p2_correctness_determinism.py:76`
- `test_l2_good_passes` (function) — `tests/test_p2_correctness_determinism.py:82`
- `test_l2_miss_fails` (function) — `tests/test_p2_correctness_determinism.py:96`
- `test_l2_near_miss_anchor_not_accepted` (function) — `tests/test_p2_correctness_determinism.py:101`
- `test_l2_wellformed_not_malformed` (function) — `tests/test_p2_correctness_determinism.py:116`
- `F1` (const) — `tests/test_p2_correctness_determinism.py:134`
- `test_f1_good_no_findings_passes` (function) — `tests/test_p2_correctness_determinism.py:139`
- `test_f1_bad_flags_must_not_flag_fails` (function) — `tests/test_p2_correctness_determinism.py:144`
- `test_f1_precision_two_false_positives` (function) — `tests/test_p2_correctness_determinism.py:158`
- `test_f1_wellformed_empty_not_malformed` (function) — `tests/test_p2_correctness_determinism.py:177`
- `F2` (const) — `tests/test_p2_correctness_determinism.py:184`
- `test_f2_good_no_findings_passes` (function) — `tests/test_p2_correctness_determinism.py:190`
- `test_f2_bad_flags_must_not_flag_fails` (function) — `tests/test_p2_correctness_determinism.py:195`
- `test_f2_precision_two_false_positives` (function) — `tests/test_p2_correctness_determinism.py:209`
- `test_f2_wellformed_empty_not_malformed` (function) — `tests/test_p2_correctness_determinism.py:228`
- `F3` (const) — `tests/test_p2_correctness_determinism.py:235`
- `test_f3_good_no_findings_passes` (function) — `tests/test_p2_correctness_determinism.py:241`
- `test_f3_bad_flags_must_not_flag_fails` (function) — `tests/test_p2_correctness_determinism.py:246`
- `test_f3_wellformed_empty_not_malformed` (function) — `tests/test_p2_correctness_determinism.py:260`
- `S1` (const) — `tests/test_p2_correctness_determinism.py:267`
- `test_s1_good_passes` (function) — `tests/test_p2_correctness_determinism.py:270`
- `test_s1_miss_fails` (function) — `tests/test_p2_correctness_determinism.py:284`
- `test_s1_near_miss_anchor_not_accepted` (function) — `tests/test_p2_correctness_determinism.py:289`
- `test_s1_wellformed_not_malformed` (function) — `tests/test_p2_correctness_determinism.py:304`
- `S2` (const) — `tests/test_p2_correctness_determinism.py:322`
- `test_s2_good_passes` (function) — `tests/test_p2_correctness_determinism.py:328`
- `test_s2_miss_fails` (function) — `tests/test_p2_correctness_determinism.py:342`
- `test_s2_near_miss_anchor_not_accepted` (function) — `tests/test_p2_correctness_determinism.py:347`
- `test_s2_wellformed_not_malformed` (function) — `tests/test_p2_correctness_determinism.py:362`
- `D1` (const) — `tests/test_p2_correctness_determinism.py:380`
- `test_d1_good_passes` (function) — `tests/test_p2_correctness_determinism.py:386`
- `test_d1_miss_fails` (function) — `tests/test_p2_correctness_determinism.py:400`
- `test_d1_near_miss_distractor_not_accepted` (function) — `tests/test_p2_correctness_determinism.py:405`
- `test_d1_precision_two_false_positives` (function) — `tests/test_p2_correctness_determinism.py:420`
- `test_d1_wellformed_not_malformed` (function) — `tests/test_p2_correctness_determinism.py:439`
- `test_d1_overflag_dict_line_is_fp` (function) — `tests/test_p2_correctness_determinism.py:455`
- `D2` (const) — `tests/test_p2_correctness_determinism.py:472`
- `test_d2_good_passes` (function) — `tests/test_p2_correctness_determinism.py:478`
- `test_d2_miss_fails` (function) — `tests/test_p2_correctness_determinism.py:492`
- `test_d2_near_miss_distractor_not_accepted` (function) — `tests/test_p2_correctness_determinism.py:497`
- `test_d2_precision_two_false_positives` (function) — `tests/test_p2_correctness_determinism.py:512`
- `test_d2_wellformed_not_malformed` (function) — `tests/test_p2_correctness_determinism.py:531`
- `test_d2_overflag_compliant_line_is_fp` (function) — `tests/test_p2_correctness_determinism.py:547`
- `D3` (const) — `tests/test_p2_correctness_determinism.py:564`
- `test_d3_good_passes` (function) — `tests/test_p2_correctness_determinism.py:570`
- `test_d3_miss_fails` (function) — `tests/test_p2_correctness_determinism.py:584`
- `test_d3_near_miss_distractor_not_accepted` (function) — `tests/test_p2_correctness_determinism.py:589`
- `test_d3_precision_two_false_positives` (function) — `tests/test_p2_correctness_determinism.py:604`
- `test_d3_wellformed_not_malformed` (function) — `tests/test_p2_correctness_determinism.py:623`
- `test_d3_overflag_fallthrough_line_is_fp` (function) — `tests/test_p2_correctness_determinism.py:639`
- `test_register_does_not_import_corpus_runtime` (function) — `tests/test_plugin.py:48`
- `test_register_wires_evaluator_source_and_corpus_preparer` (function) — `tests/test_plugin.py:57`
- `test_detector_matches_example_and_rejects_native` (function) — `tests/test_plugin.py:146`
- `test_load_suite_file_and_sweep` (function) — `tests/test_plugin.py:157`
- `ROOT` (const) — `tests/test_req_extraction_determinism.py:11`
- `CLEAN` (const) — `tests/test_req_extraction_determinism.py:12`
- `MODERATE` (const) — `tests/test_req_extraction_determinism.py:19`
- `SEVERE` (const) — `tests/test_req_extraction_determinism.py:26`
- `VERY_SEVERE` (const) — `tests/test_req_extraction_determinism.py:33`
- `CHECKER` (const) — `tests/test_req_extraction_determinism.py:41`
- `test_clean_case_is_json_path` (function) — `tests/test_req_extraction_determinism.py:53`
- `test_clean_faithful_passes_fabricated_fails` (function) — `tests/test_req_extraction_determinism.py:59`
- `test_moderate_qualifier_preserved_fabricated_fails` (function) — `tests/test_req_extraction_determinism.py:109`
- `test_severe_null_deadline_passes_fabricated_fails` (function) — `tests/test_req_extraction_determinism.py:158`
- `test_very_severe_null_deadline_passes_fabricated_fails` (function) — `tests/test_req_extraction_determinism.py:207`
- `test_checker_is_deterministic_same_input` (function) — `tests/test_req_extraction_determinism.py:245`
- `test_all_example_cases_validate` (function) — `tests/test_schema.py:12`
- `test_duplicate_tools_rejected` (function) — `tests/test_schema.py:23`
- `test_invalid_created_date_rejected` (function) — `tests/test_schema.py:29`
- `test_invalid_tag_pattern_rejected` (function) — `tests/test_schema.py:37`
- `test_duplicate_tags_rejected` (function) — `tests/test_schema.py:45`
- `test_none_tool_must_be_exclusive` (function) — `tests/test_schema.py:53`
- `test_rubric_grader_requires_rubric` (function) — `tests/test_schema.py:59`
- `test_volatility_requires_inject_turn` (function) — `tests/test_schema.py:71`
- `test_extra_field_forbidden` (function) — `tests/test_schema.py:78`
- `test_behavior_assertions_default_empty_and_validate_entries` (function) — `tests/test_schema.py:86`
- `test_findings_match_grader_accepts_structured_ground_truth` (function) — `tests/test_schema.py:136`
- `test_findings_match_grader_requires_expected_findings_key` (function) — `tests/test_schema.py:157`
- `test_findings_match_grader_allows_empty_expected_findings` (function) — `tests/test_schema.py:168`
- `test_grader_type_findings_match_now_rejected` (function) — `tests/test_schema.py:181`
- `test_programmatic_checker_findings_requires_expected_findings` (function) — `tests/test_schema.py:192`
- `test_programmatic_checker_findings_accepts_empty_expected` (function) — `tests/test_schema.py:202`
- `test_checker_requires_programmatic_type` (function) — `tests/test_schema.py:213`
- `test_task_type_and_language_optional_default_none` (function) — `tests/test_schema.py:274`
- `test_task_type_and_language_accepted` (function) — `tests/test_schema.py:282`
- `test_task_type_rejects_non_token` (function) — `tests/test_schema.py:292`
- `test_empty_checker_rejected` (function) — `tests/test_schema.py:299`
- `test_corpus_models_accept_spec_example_paths` (function) — `tests/test_schema_artifact_corpus.py:73`
- `test_artifact_corpus_under_text_out_is_rejected` (function) — `tests/test_schema_artifact_corpus.py:90`
- `test_read_only_corpus_without_artifact_corpus_is_rejected` (function) — `tests/test_schema_artifact_corpus.py:100`
- `test_read_only_corpus_with_valid_corpus_validates_as_wired_mode` (function) — `tests/test_schema_artifact_corpus.py:110`
- `test_duplicate_tools_rejected_for_corpus_case_before_wiring` (function) — `tests/test_schema_artifact_corpus.py:165`
- `test_citation_grounding_requires_non_empty_expected_config` (function) — `tests/test_schema_artifact_corpus.py:175`
- `SCHEMA` (const) — `tests/test_schema_contract.py:10`
- `test_contract_accepts_programmatic_checker_findings` (function) — `tests/test_schema_contract.py:36`
- `test_contract_rejects_findings_checker_without_expected_findings` (function) — `tests/test_schema_contract.py:52`
- `test_contract_allows_expected_finding_without_severity` (function) — `tests/test_schema_contract.py:65`
- `test_contract_rejects_empty_checker` (function) — `tests/test_schema_contract.py:80`
- `test_contract_accepts_task_type_language` (function) — `tests/test_schema_contract.py:94`
- `test_contract_accepts_behavior_assertions_and_rejects_extra_keys` (function) — `tests/test_schema_contract.py:109`
- `test_output_contract_parses_and_aliases_schema` (function) — `tests/test_schema_output_contract.py:47`
- `test_case_with_output_contract_and_run_mode_valid` (function) — `tests/test_schema_output_contract.py:56`
- `test_run_mode_unwired_tier_rejected` (function) — `tests/test_schema_output_contract.py:62`
- `test_run_mode_defaults_to_text_out` (function) — `tests/test_schema_output_contract.py:67`
- `test_json_path_requires_assertions` (function) — `tests/test_schema_output_contract.py:73`
- `test_review_maps_to_code_review` (function) — `tests/test_taxonomy.py:8`
- `test_registry_is_the_source` (function) — `tests/test_taxonomy.py:12`
- `test_unknown_task_type_raises` (function) — `tests/test_taxonomy.py:16`

## Modules

_30 files, 225 public symbols, 90 internal imports._

- `atp_method/__init__.py` (python)
- `atp_method/corpus.py` (python)
- `atp_method/corpus_manifest.py` (python)
- `atp_method/envelopes.py` (python)
- `atp_method/evaluators/__init__.py` (python)
- `atp_method/evaluators/case_evaluator.py` (python)
- `atp_method/loader.py` (python)
- `atp_method/plugin.py` (python)
- `atp_method/runtime.py` (python)
- `atp_method/schema.py` (python)
- `atp_method/taxonomy.py` (python)
- `tests/__init__.py` (python)
- `tests/conftest.py` (python)
- `tests/test_cases_load.py` (python)
- `tests/test_code_review_structured.py` (python)
- `tests/test_corpus.py` (python)
- `tests/test_envelopes.py` (python)
- `tests/test_evaluator.py` (python)
- `tests/test_loader.py` (python)
- `tests/test_loader_artifact_corpus.py` (python)
- `tests/test_loader_output_contract.py` (python)
- `tests/test_p2_correctness_determinism.py` (python)
- `tests/test_plugin.py` (python)
- `tests/test_req_extraction_determinism.py` (python)
- `tests/test_runtime_corpus_preparer.py` (python)
- `tests/test_schema.py` (python)
- `tests/test_schema_artifact_corpus.py` (python)
- `tests/test_schema_contract.py` (python)
- `tests/test_schema_output_contract.py` (python)
- `tests/test_taxonomy.py` (python)

## Inbound references

- from [[atp-platform]]:
  - `method/run_pipe_check.py:50` → `evaluators::AgentEvalCaseEvaluator`
  - `method/run_pipe_check.py:51` → `loader::METHOD_CRITICAL_CHECK`
  - `method/run_pipe_check.py:51` → `loader::METHOD_RUBRIC`
  - `method/run_pipe_check.py:51` → `loader::load_suite`
  - `method/run_pipe_check.py:52` → `taxonomy::benchmark_id_for`
  - `method/run_pipe_check.py:411` → `runtime::CorpusRunPreparer`
  - `method/spawners/_cli_common.py:20` → `envelopes::build_prompt`
  - `method/spawners/_cli_common.py:20` → `envelopes::get_envelope`
  - `method/spawners/_openai_compat.py:19` → `envelopes::build_prompt`
  - `method/spawners/_openai_compat.py:19` → `envelopes::get_envelope`
  - `method/spawners/anthropic_api_shim.py:36` → `envelopes::DEFAULT_MODEL`
  - `method/spawners/anthropic_api_shim.py:36` → `envelopes::build_prompt`
  - `method/spawners/anthropic_api_shim.py:36` → `envelopes::get_envelope`
  - `method/spawners/claude_code_shim.py:23` → `envelopes::DEFAULT_MODEL`
  - `method/spawners/claude_code_shim.py:23` → `envelopes::build_prompt`
  - `method/spawners/claude_code_shim.py:23` → `envelopes::get_envelope`
  - `method/spawners/codex_cli_shim.py:44` → `envelopes::build_prompt`
  - `method/spawners/codex_cli_shim.py:44` → `envelopes::get_envelope`
  - `method/spawners/deepseek_shim.py:33` → `envelopes::build_prompt`
  - `method/spawners/deepseek_shim.py:33` → `envelopes::get_envelope`
  - `method/spawners/ollama_shim.py:35` → `envelopes::build_prompt`
  - `method/spawners/ollama_shim.py:35` → `envelopes::get_envelope`
  - `packages/atp-method/atp_method/__init__.py:3` → `evaluators::AgentEvalCaseEvaluator`
  - `packages/atp-method/atp_method/__init__.py:5` → `loader::METHOD_CRITICAL_CHECK`
  - `packages/atp-method/atp_method/__init__.py:6` → `loader::METHOD_RUBRIC`
  - `packages/atp-method/atp_method/__init__.py:7` → `loader::case_to_test_definition`
  - `packages/atp-method/atp_method/__init__.py:8` → `loader::load_case`
  - `packages/atp-method/atp_method/__init__.py:10` → `schema::AgentEvalCase`
  - `packages/atp-method/atp_method/corpus.py:13` → `schema::ArtifactCorpus`
  - `packages/atp-method/atp_method/corpus.py:13` → `schema::CorpusMetadata`
  - `packages/atp-method/atp_method/corpus_manifest.py:8` → `corpus::TEXT_SUFFIXES`
  - `packages/atp-method/atp_method/corpus_manifest.py:8` → `corpus::normalize_lf`
  - `packages/atp-method/atp_method/evaluators/__init__.py:3` → `evaluators.case_evaluator::AgentEvalCaseEvaluator`
  - `packages/atp-method/atp_method/evaluators/case_evaluator.py:23` → `loader::METHOD_CRITICAL_CHECK`
  - `packages/atp-method/atp_method/evaluators/case_evaluator.py:23` → `loader::METHOD_RUBRIC`
  - `packages/atp-method/atp_method/loader.py:26` → `schema::AgentEvalCase`
  - `packages/atp-method/atp_method/plugin.py:50` → `evaluators::AgentEvalCaseEvaluator`
  - `packages/atp-method/atp_method/plugin.py:52` → `loader::METHOD_CRITICAL_CHECK`
  - `packages/atp-method/atp_method/plugin.py:53` → `loader::METHOD_RUBRIC`
  - `packages/atp-method/atp_method/plugin.py:54` → `loader::is_agent_eval_case`
  - `packages/atp-method/atp_method/plugin.py:55` → `loader::load_suite`
  - `packages/atp-method/atp_method/runtime.py:17` → `corpus::CorpusIntegrityVerifier`
  - `packages/atp-method/atp_method/runtime.py:18` → `corpus::CorpusMaterializer`
  - `packages/atp-method/atp_method/runtime.py:19` → `corpus::CorpusResolver`
  - `packages/atp-method/atp_method/runtime.py:20` → `corpus::MaterializedCorpus`
  - `packages/atp-method/atp_method/runtime.py:22` → `schema::ArtifactCorpus`
  - `packages/atp-method/tests/test_cases_load.py:9` → `loader::load_case`
  - `packages/atp-method/tests/test_cases_load.py:10` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_code_review_structured.py:4` → `envelopes::build_prompt`
  - `packages/atp-method/tests/test_code_review_structured.py:4` → `envelopes::get_envelope`
  - `packages/atp-method/tests/test_code_review_structured.py:5` → `loader::load_case`
  - `packages/atp-method/tests/test_code_review_structured.py:23` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_code_review_structured.py:53` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_corpus.py:12` → `schema::ArtifactCorpus`
  - `packages/atp-method/tests/test_corpus.py:64` → `corpus::CorpusVerificationResult`
  - `packages/atp-method/tests/test_corpus.py:64` → `corpus::VerifiedCorpusFile`
  - `packages/atp-method/tests/test_corpus.py:86` → `corpus::CorpusResolver`
  - `packages/atp-method/tests/test_corpus.py:105` → `corpus::CorpusResolver`
  - `packages/atp-method/tests/test_corpus.py:116` → `corpus::CorpusIntegrityVerifier`
  - `packages/atp-method/tests/test_corpus.py:116` → `corpus::CorpusResolver`
  - `packages/atp-method/tests/test_corpus.py:132` → `corpus::CorpusIntegrityVerifier`
  - `packages/atp-method/tests/test_corpus.py:132` → `corpus::CorpusResolver`
  - `packages/atp-method/tests/test_corpus.py:154` → `corpus::CorpusIntegrityVerifier`
  - `packages/atp-method/tests/test_corpus.py:154` → `corpus::CorpusResolver`
  - `packages/atp-method/tests/test_corpus.py:170` → `corpus::CorpusIntegrityVerifier`
  - `packages/atp-method/tests/test_corpus.py:170` → `corpus::CorpusResolver`
  - `packages/atp-method/tests/test_corpus.py:191` → `corpus::CorpusIntegrityVerifier`
  - `packages/atp-method/tests/test_corpus.py:192` → `corpus::CorpusMaterializer`
  - `packages/atp-method/tests/test_corpus.py:193` → `corpus::CorpusResolver`
  - `packages/atp-method/tests/test_corpus.py:216` → `corpus::CorpusMaterializer`
  - `packages/atp-method/tests/test_corpus.py:233` → `corpus::CorpusMaterializer`
  - `packages/atp-method/tests/test_corpus.py:251` → `corpus::CorpusMaterializer`
  - `packages/atp-method/tests/test_envelopes.py:6` → `envelopes::DEFAULT_MODEL`
  - `packages/atp-method/tests/test_envelopes.py:7` → `envelopes::REVIEW_ENVELOPE`
  - `packages/atp-method/tests/test_envelopes.py:8` → `envelopes::build_prompt`
  - `packages/atp-method/tests/test_envelopes.py:9` → `envelopes::get_envelope`
  - `packages/atp-method/tests/test_envelopes.py:59` → `loader::load_suite`
  - `packages/atp-method/tests/test_envelopes.py:191` → `corpus::CorpusIntegrityVerifier`
  - `packages/atp-method/tests/test_envelopes.py:191` → `corpus::CorpusResolver`
  - `packages/atp-method/tests/test_envelopes.py:192` → `loader::load_case`
  - `packages/atp-method/tests/test_envelopes.py:193` → `schema::ArtifactCorpus`
  - `packages/atp-method/tests/test_evaluator.py:12` → `evaluators::AgentEvalCaseEvaluator`
  - `packages/atp-method/tests/test_evaluator.py:13` → `loader::METHOD_CRITICAL_CHECK`
  - `packages/atp-method/tests/test_evaluator.py:13` → `loader::METHOD_RUBRIC`
  - `packages/atp-method/tests/test_loader.py:8` → `loader::METHOD_CRITICAL_CHECK`
  - `packages/atp-method/tests/test_loader.py:9` → `loader::METHOD_RUBRIC`
  - `packages/atp-method/tests/test_loader.py:10` → `loader::case_to_test_definition`
  - `packages/atp-method/tests/test_loader.py:11` → `loader::load_case`
  - `packages/atp-method/tests/test_loader.py:13` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_loader.py:276` → `loader::case_to_test_definition`
  - `packages/atp-method/tests/test_loader.py:277` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_loader.py:309` → `loader::case_to_test_definition`
  - `packages/atp-method/tests/test_loader.py:310` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_loader_artifact_corpus.py:82` → `loader::load_case`
  - `packages/atp-method/tests/test_loader_artifact_corpus.py:97` → `loader::load_case`
  - `packages/atp-method/tests/test_loader_artifact_corpus.py:176` → `loader::load_case`
  - `packages/atp-method/tests/test_loader_artifact_corpus.py:177` → `runtime::CorpusRunPreparer`
  - `packages/atp-method/tests/test_loader_output_contract.py:3` → `loader::METHOD_CRITICAL_CHECK`
  - `packages/atp-method/tests/test_loader_output_contract.py:3` → `loader::case_to_test_definition`
  - `packages/atp-method/tests/test_loader_output_contract.py:4` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_p2_correctness_determinism.py:7` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_plugin.py:18` → `evaluators::AgentEvalCaseEvaluator`
  - `packages/atp-method/tests/test_plugin.py:20` → `loader::METHOD_CRITICAL_CHECK`
  - `packages/atp-method/tests/test_plugin.py:21` → `loader::METHOD_RUBRIC`
  - `packages/atp-method/tests/test_plugin.py:22` → `loader::is_agent_eval_case`
  - `packages/atp-method/tests/test_plugin.py:23` → `loader::load_suite`
  - `packages/atp-method/tests/test_plugin.py:25` → `plugin::register`
  - `packages/atp-method/tests/test_req_extraction_determinism.py:9` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_runtime_corpus_preparer.py:15` → `runtime::CorpusRunPreparer`
  - `packages/atp-method/tests/test_runtime_corpus_preparer.py:84` → `runtime::CorpusRunPreparer`
  - `packages/atp-method/tests/test_schema.py:9` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_schema.py:9` → `schema::Grader`
  - `packages/atp-method/tests/test_schema.py:275` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_schema.py:283` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_schema.py:293` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_schema_artifact_corpus.py:74` → `schema::ArtifactCorpus`
  - `packages/atp-method/tests/test_schema_artifact_corpus.py:74` → `schema::CorpusDigest`
  - `packages/atp-method/tests/test_schema_artifact_corpus.py:91` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_schema_artifact_corpus.py:101` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_schema_artifact_corpus.py:111` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_schema_artifact_corpus.py:111` → `schema::WIRED_RUN_MODES`
  - `packages/atp-method/tests/test_schema_artifact_corpus.py:139` → `schema::ArtifactCorpus`
  - `packages/atp-method/tests/test_schema_artifact_corpus.py:156` → `schema::CorpusDigest`
  - `packages/atp-method/tests/test_schema_artifact_corpus.py:166` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_schema_artifact_corpus.py:176` → `schema::Grader`
  - `packages/atp-method/tests/test_schema_output_contract.py:6` → `schema::AgentEvalCase`
  - `packages/atp-method/tests/test_schema_output_contract.py:6` → `schema::Grader`
  - `packages/atp-method/tests/test_schema_output_contract.py:6` → `schema::OutputContract`
  - `packages/atp-method/tests/test_taxonomy.py:5` → `taxonomy::TASK_TYPE_TO_BENCHMARK_ID`
  - `packages/atp-method/tests/test_taxonomy.py:5` → `taxonomy::benchmark_id_for`
  - `tests/unit/evaluators/test_citation_grounding_checker.py:103` → `corpus::CorpusIntegrityVerifier`
  - `tests/unit/evaluators/test_citation_grounding_checker.py:103` → `corpus::CorpusResolver`
  - `tests/unit/evaluators/test_citation_grounding_checker.py:104` → `loader::load_case`
  - `tests/unit/evaluators/test_citation_grounding_checker.py:105` → `schema::ArtifactCorpus`
  - `tests/unit/method_spawners/test_anthropic_api_shim.py:12` → `envelopes::build_prompt`
  - `tests/unit/method_spawners/test_anthropic_api_shim.py:12` → `envelopes::get_envelope`
  - `tests/unit/method_spawners/test_run_pipe_check.py:134` → `loader::load_case`
  - `tests/unit/method_spawners/test_run_pipe_check.py:170` → `loader::load_case`
  - `tests/unit/method_spawners/test_run_pipe_check.py:307` → `loader::load_case`

## Outbound references

_None._

## Outbound edges

- → [[atp-platform]] · `package_dep` · `atp-platform`

## Inbound edges

- ← [[atp-platform]] · `package_dep` · `atp-method`

## Recent changes (last 5)

- snapshot 1 (2026-07-07T16:11:23Z): project added (added)

## Drift findings

_None._
