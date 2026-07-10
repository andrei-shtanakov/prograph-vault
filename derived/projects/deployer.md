<!-- prograph:generated -->

---
indexed_at: "2026-07-10T12:31:55Z"
kind: python
name: deployer
prograph: project
root: ./deployer
snapshot: 4
---

# deployer

> Research bench for deploy-authoring agents: an LLM authors a Dockerfile from deterministic project facts + a declarative `deploytarget` intent; a deterministic pipeline verifies it (static checks…

## Manifest

- declared package: `deployer` version `0.1.0`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

_None._

### Public symbols

- `DockerfileAuthor` (class) — `src/deployer/author.py:25`
- `author_dockerfile` (function) — `src/deployer/author.py:39`
- `main` (function) — `src/deployer/cli.py:164`
- `analyze_project` (function) — `src/deployer/facts.py:40`
- `KNOWN_SYSTEM_DEPS` (const) — `src/deployer/hints.py:15`
- `collect_hints` (function) — `src/deployer/hints.py:62`
- `DEFAULT_MODEL` (const) — `src/deployer/llm.py:10`
- `MAX_TOKENS` (const) — `src/deployer/llm.py:11`
- `SYSTEM_PROMPT` (const) — `src/deployer/llm.py:13`
- `AnthropicAuthor` (class) — `src/deployer/llm.py:80`
- `ServiceSpec` (class) — `src/deployer/models.py:9`
- `DeployTarget` (class) — `src/deployer/models.py:16`
- `ProjectFacts` (class) — `src/deployer/models.py:26`
- `SystemDepHint` (class) — `src/deployer/models.py:43`
- `CheckStatus` (class) — `src/deployer/models.py:54`
- `FailureKind` (class) — `src/deployer/models.py:63`
- `CheckResult` (class) — `src/deployer/models.py:70`
- `VerificationReport` (class) — `src/deployer/models.py:87`
- `IterationRecord` (class) — `src/deployer/models.py:118`
- `StopReason` (const) — `src/deployer/models.py:127`
- `AuthoringRun` (class) — `src/deployer/models.py:137`
- `HADOLINT_VERSION` (const) — `src/deployer/verify.py:24`
- `DEFAULT_BUILD_TIMEOUT` (const) — `src/deployer/verify.py:25`
- `DEFAULT_HEALTH_TIMEOUT` (const) — `src/deployer/verify.py:26`
- `parse_dockerfile` (function) — `src/deployer/verify.py:31`
- `verify_static` (function) — `src/deployer/verify.py:265`
- `ENVIRONMENT_MARKERS` (const) — `src/deployer/verify.py:289`
- `detect_container_tool` (function) — `src/deployer/verify.py:302`
- `verify_docker` (function) — `src/deployer/verify.py:458`
- `verify` (function) — `src/deployer/verify.py:490`
- `FIXTURES` (const) — `tests/conftest.py:5`
- `Handler` (class) — `tests/fixtures/hello_service/main.py:6`
- `main` (function) — `tests/fixtures/hello_service/main.py:20`
- `Handler` (class) — `tests/fixtures/pip_service/main.py:6`
- `main` (function) — `tests/fixtures/pip_service/main.py:20`
- `Handler` (class) — `tests/fixtures/sysdep_service/main.py:8`
- `main` (function) — `tests/fixtures/sysdep_service/main.py:22`
- `GOOD` (const) — `tests/test_author.py:14`
- `BAD_COPY` (const) — `tests/test_author.py:17`
- `NO_FROM` (const) — `tests/test_author.py:18`
- `ScriptedAuthor` (class) — `tests/test_author.py:32`
- `test_success_on_first_iteration` (function) — `tests/test_author.py:53`
- `test_repair_path_fixes_bad_copy` (function) — `tests/test_author.py:63`
- `test_no_progress_early_stop` (function) — `tests/test_author.py:71`
- `test_budget_exhausted_returns_failed_run` (function) — `tests/test_author.py:80`
- `ExplodingAuthor` (class) — `tests/test_author.py:90`
- `test_generate_error_yields_llm_error_run` (function) — `tests/test_author.py:111`
- `test_repair_error_preserves_completed_iterations` (function) — `tests/test_author.py:121`
- `test_environment_failure_retries_once_without_consuming_iteration` (function) — `tests/test_author.py:130`
- `test_hints_offered_recorded_and_facts_passed` (function) — `tests/test_author.py:173`
- `test_second_environment_failure_stops_run` (function) — `tests/test_author.py:210`
- `test_author_forwards_timeouts_to_both_verify_calls` (function) — `tests/test_author.py:246`
- `test_verify_command_passes_on_good_dockerfile` (function) — `tests/test_cli.py:21`
- `test_verify_command_fails_without_dockerfile` (function) — `tests/test_cli.py:33`
- `test_author_command_writes_dockerfile_and_report` (function) — `tests/test_cli.py:37`
- `test_author_reads_target_json` (function) — `tests/test_cli.py:62`
- `test_author_rejects_nonpositive_max_iterations` (function) — `tests/test_cli.py:87`
- `test_verify_rejects_nonpositive_timeouts` (function) — `tests/test_cli.py:91`
- `test_author_rejects_nonpositive_timeouts` (function) — `tests/test_cli.py:97`
- `test_verify_flags_reach_library` (function) — `tests/test_cli.py:102`
- `test_author_flags_reach_library` (function) — `tests/test_cli.py:144`
- `test_print_report_shows_full_failed_message_only` (function) — `tests/test_cli.py:184`
- `test_verify_writes_report_json_on_pass` (function) — `tests/test_cli.py:218`
- `test_verify_writes_report_json_on_fail` (function) — `tests/test_cli.py:231`
- `test_verify_rejects_nondir_project` (function) — `tests/test_cli.py:245`
- `test_author_rejects_nondir_project` (function) — `tests/test_cli.py:250`
- `test_verify_rejects_missing_target_file` (function) — `tests/test_cli.py:255`
- `test_author_rejects_missing_target_file` (function) — `tests/test_cli.py:262`
- `test_rejects_malformed_target_json` (function) — `tests/test_cli.py:268`
- `test_rejects_target_failing_validation` (function) — `tests/test_cli.py:275`
- `test_nondir_project_wins_over_bad_target` (function) — `tests/test_cli.py:282`
- `test_missing_dockerfile_still_exit_1` (function) — `tests/test_cli.py:306`
- `test_rejects_non_utf8_target_file` (function) — `tests/test_cli.py:310`
- `test_print_report_blank_tail_lines_have_no_trailing_spaces` (function) — `tests/test_cli.py:317`
- `test_verify_report_write_failure_warns_not_crashes` (function) — `tests/test_cli.py:335`
- `test_author_report_write_failure_warns_not_crashes` (function) — `tests/test_cli.py:349`
- `test_analyze_hello_service` (function) — `tests/test_facts.py:6`
- `test_analyze_empty_dir_yields_explicit_nones` (function) — `tests/test_facts.py:16`
- `test_malformed_pyproject_degrades_to_empty` (function) — `tests/test_facts.py:26`
- `test_wrong_typed_values_are_not_invented` (function) — `tests/test_facts.py:33`
- `test_pip_service_facts` (function) — `tests/test_facts.py:43`
- `test_uv_lock_wins_over_requirements` (function) — `tests/test_facts.py:50`
- `test_no_manager_when_nothing_present` (function) — `tests/test_facts.py:58`
- `test_requirements_parsing_normalizes` (function) — `tests/test_facts.py:62`
- `test_multiple_requirements_files` (function) — `tests/test_facts.py:84`
- `test_has_build_system_detected` (function) — `tests/test_facts.py:94`
- `test_unreadable_requirements_degrades_to_empty` (function) — `tests/test_facts.py:101`
- `test_bom_prefixed_requirements_parse_clean` (function) — `tests/test_facts.py:107`
- `test_vcs_and_url_requirements_are_skipped` (function) — `tests/test_facts.py:113`
- `test_psycopg2_matched_from_pyproject_deps` (function) — `tests/test_hints.py:5`
- `test_psycopg2_binary_is_explicit_no_hint` (function) — `tests/test_hints.py:14`
- `test_matches_requirements_files_and_skips_directives` (function) — `tests/test_hints.py:20`
- `test_normalization_and_dedup` (function) — `tests/test_hints.py:30`
- `test_sorted_output` (function) — `tests/test_hints.py:39`
- `test_wheel_covered_packages_absent_from_table` (function) — `tests/test_hints.py:45`
- `test_every_gcc_entry_also_carries_libc6_dev` (function) — `tests/test_hints.py:50`
- `test_collect_hints_returns_copies` (function) — `tests/test_hints.py:56`
- `test_extract_strips_markdown_fences` (function) — `tests/test_llm.py:39`
- `test_generate_sends_facts_and_returns_dockerfile` (function) — `tests/test_llm.py:45`
- `test_repair_includes_previous_dockerfile_and_failures` (function) — `tests/test_llm.py:57`
- `test_generate_includes_hints_and_system_packages` (function) — `tests/test_llm.py:76`
- `test_generate_omits_empty_blocks` (function) — `tests/test_llm.py:92`
- `test_system_prompt_carries_install_strategy_rules` (function) — `tests/test_llm.py:101`
- `test_deploy_target_defaults` (function) — `tests/test_models.py:23`
- `test_deploy_target_roundtrip_json` (function) — `tests/test_models.py:30`
- `test_report_passed_ignores_warnings` (function) — `tests/test_models.py:36`
- `test_report_failed_and_taxonomy` (function) — `tests/test_models.py:47`
- `test_error_signature_is_stable_and_first_line_only` (function) — `tests/test_models.py:58`
- `test_authoring_run_serializes` (function) — `tests/test_models.py:69`
- `test_failed_check_requires_failure_kind` (function) — `tests/test_models.py:83`
- `test_error_signature_sorts_multiple_failures` (function) — `tests/test_models.py:88`
- `test_system_dep_hint_defaults` (function) — `tests/test_models.py:97`
- `test_new_facts_fields_default_safe` (function) — `tests/test_models.py:103`
- `test_deploy_target_system_packages_roundtrip` (function) — `tests/test_models.py:110`
- `test_authoring_run_records_hints` (function) — `tests/test_models.py:116`
- `test_report_image_size_default_none` (function) — `tests/test_models.py:131`
- `pytestmark` (const) — `tests/test_verify_docker.py:8`
- `TARGET` (const) — `tests/test_verify_docker.py:10`
- `test_good_dockerfile_builds_runs_and_healthchecks` (function) — `tests/test_verify_docker.py:25`
- `test_broken_run_instruction_fails_build_as_authoring` (function) — `tests/test_verify_docker.py:37`
- `test_wrong_port_fails_healthcheck` (function) — `tests/test_verify_docker.py:51`
- `test_no_tool_degrades_to_static_only` (function) — `tests/test_verify_docker.py:60`
- `test_e2e_author_loop_with_real_docker` (function) — `tests/test_verify_docker.py:67`
- `test_cli_author_with_real_docker_exits_zero` (function) — `tests/test_verify_docker.py:84`
- `test_pip_service_e2e` (function) — `tests/test_verify_docker.py:114`
- `test_sysdep_service_apt_layers_build_and_healthcheck` (function) — `tests/test_verify_docker.py:123`
- `GOOD` (const) — `tests/test_verify_static.py:6`
- `UV_STYLE` (const) — `tests/test_verify_static.py:14`
- `PIP_STYLE` (const) — `tests/test_verify_static.py:18`
- `test_parse_joins_continuations_and_skips_comments` (function) — `tests/test_verify_static.py:29`
- `test_good_dockerfile_passes_static` (function) — `tests/test_verify_static.py:37`
- `test_missing_from_fails_as_authoring` (function) — `tests/test_verify_static.py:44`
- `test_copy_of_nonexistent_file_fails` (function) — `tests/test_verify_static.py:51`
- `test_copy_from_stage_is_ignored` (function) — `tests/test_verify_static.py:59`
- `test_unpinned_base_image_warns` (function) — `tests/test_verify_static.py:70`
- `test_pinned_base_image_passes` (function) — `tests/test_verify_static.py:76`
- `test_base_pinned_skips_platform_flag` (function) — `tests/test_verify_static.py:81`
- `test_hadolint_skipped_marks_non_comparable` (function) — `tests/test_verify_static.py:91`
- `test_hadolint_timeout_degrades_to_skipped` (function) — `tests/test_verify_static.py:100`
- `test_hadolint_garbage_output_degrades_to_skipped` (function) — `tests/test_verify_static.py:115`
- `test_install_strategy_skipped_without_facts` (function) — `tests/test_verify_static.py:138`
- `test_pip_project_using_uv_fails` (function) — `tests/test_verify_static.py:143`
- `test_uv_project_using_pip_fails` (function) — `tests/test_verify_static.py:151`
- `test_no_build_system_project_install_fails` (function) — `tests/test_verify_static.py:157`
- `test_no_install_project_flag_passes_per_line` (function) — `tests/test_verify_static.py:163`
- `test_matching_strategy_passes` (function) — `tests/test_verify_static.py:176`
- `test_echoed_uv_sync_string_does_not_trigger` (function) — `tests/test_verify_static.py:182`
- `test_python_m_pip_detected_in_uv_project` (function) — `tests/test_verify_static.py:194`
- `test_env_prefix_does_not_bypass_rules` (function) — `tests/test_verify_static.py:205`
- `test_echoed_python_m_pip_does_not_trigger` (function) — `tests/test_verify_static.py:225`
- `test_verify_forwards_timeouts_to_verify_docker` (function) — `tests/test_verify_static.py:257`
- `test_verify_defaults_match_module_constants` (function) — `tests/test_verify_static.py:275`

## Modules

_21 files, 152 public symbols, 73 internal imports._

- `src/deployer/__init__.py` (python)
- `src/deployer/author.py` (python)
- `src/deployer/cli.py` (python)
- `src/deployer/facts.py` (python)
- `src/deployer/hints.py` (python)
- `src/deployer/llm.py` (python)
- `src/deployer/models.py` (python)
- `src/deployer/verify.py` (python)
- `tests/__init__.py` (python)
- `tests/conftest.py` (python)
- `tests/fixtures/hello_service/main.py` (python)
- `tests/fixtures/pip_service/main.py` (python)
- `tests/fixtures/sysdep_service/main.py` (python)
- `tests/test_author.py` (python)
- `tests/test_cli.py` (python)
- `tests/test_facts.py` (python)
- `tests/test_hints.py` (python)
- `tests/test_llm.py` (python)
- `tests/test_models.py` (python)
- `tests/test_verify_docker.py` (python)
- `tests/test_verify_static.py` (python)

## Inbound references

_None._

## Outbound references

_None._

## Outbound edges

_None._

## Inbound edges

_None._

## Recent changes (last 5)

- snapshot 1 (2026-07-07T16:11:23Z): project added (added)

## Drift findings

_None._
