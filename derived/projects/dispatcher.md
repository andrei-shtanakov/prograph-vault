<!-- prograph:generated -->

---
indexed_at: "2026-07-10T12:31:55Z"
kind: python
name: dispatcher
prograph: project
root: ./dispatcher
snapshot: 4
---

# dispatcher

> Read-only monitoring dashboard for the AI-orchestrators ecosystem (atp-platform, Maestro, arbiter, spec-runner, proctor). Reads on-disk artifacts directly — monitored projects don't need to be…

## Manifest

- declared package: `dispatcher` version `0.1.0`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

_None._

### Public symbols

- `build_parser` (function) — `dispatcher/cli.py:11`
- `main` (function) — `dispatcher/cli.py:23`
- `COLLECTORS` (const) — `dispatcher/core/collectors/__init__.py:10`
- `ArbiterCollector` (class) — `dispatcher/core/collectors/arbiter.py:36`
- `AtpCollector` (class) — `dispatcher/core/collectors/atp.py:31`
- `SEVERITY_ERROR` (const) — `dispatcher/core/collectors/base.py:20`
- `SourceReadError` (class) — `dispatcher/core/collectors/base.py:30`
- `Collector` (class) — `dispatcher/core/collectors/base.py:43`
- `read_rows` (function) — `dispatcher/core/collectors/base.py:57`
- `table_names` (function) — `dispatcher/core/collectors/base.py:85`
- `version_check` (function) — `dispatcher/core/collectors/base.py:91`
- `coerce_str` (function) — `dispatcher/core/collectors/base.py:99`
- `mask_secrets` (function) — `dispatcher/core/collectors/base.py:108`
- `shallow_summary` (function) — `dispatcher/core/collectors/base.py:122`
- `read_otel_errors` (function) — `dispatcher/core/collectors/base.py:140`
- `newest_mtime` (function) — `dispatcher/core/collectors/base.py:190`
- `read_yaml` (function) — `dispatcher/core/collectors/base.py:198`
- `read_toml` (function) — `dispatcher/core/collectors/base.py:207`
- `MaestroCollector` (class) — `dispatcher/core/collectors/maestro.py:30`
- `ProctorCollector` (class) — `dispatcher/core/collectors/proctor.py:31`
- `SpecRunnerCollector` (class) — `dispatcher/core/collectors/spec_runner.py:31`
- `check_contracts` (function) — `dispatcher/core/contracts.py:31`
- `DEFAULT_PORT` (const) — `dispatcher/core/discovery.py:11`
- `load_config` (function) — `dispatcher/core/discovery.py:41`
- `discover` (function) — `dispatcher/core/discovery.py:58`
- `ModelInUse` (class) — `dispatcher/core/models.py:19`
- `TaskInfo` (class) — `dispatcher/core/models.py:30`
- `TestRunSummary` (class) — `dispatcher/core/models.py:42`
- `ContractStatus` (class) — `dispatcher/core/models.py:55`
- `ErrorEvent` (class) — `dispatcher/core/models.py:65`
- `ConfigSummary` (class) — `dispatcher/core/models.py:76`
- `SchemaVersionCheck` (class) — `dispatcher/core/models.py:84`
- `ProjectSnapshot` (class) — `dispatcher/core/models.py:93`
- `OverviewEntry` (class) — `dispatcher/core/models.py:110`
- `OverviewResponse` (class) — `dispatcher/core/models.py:121`
- `ERRORS_DAYS_DEFAULT` (const) — `dispatcher/core/service.py:17`
- `recent_errors` (function) — `dispatcher/core/service.py:22`
- `SnapshotService` (class) — `dispatcher/core/service.py:37`
- `create_app` (function) — `dispatcher/server/app.py:27`
- `MSG_LIMIT` (const) — `dispatcher/tui/app.py:31`
- `ERRORS_LIMIT` (const) — `dispatcher/tui/app.py:32`
- `truncate` (function) — `dispatcher/tui/app.py:35`
- `DispatcherApp` (class) — `dispatcher/tui/app.py:40`
- `ProjectDetailScreen` (class) — `dispatcher/tui/detail.py:78`
- `ErrorMessageScreen` (class) — `dispatcher/tui/detail.py:102`
- `write_otel_error_log` (function) — `tests/conftest.py:25`
- `make_spec_runner` (function) — `tests/conftest.py:45`
- `make_arbiter` (function) — `tests/conftest.py:84`
- `make_maestro` (function) — `tests/conftest.py:120`
- `make_maestro_home` (function) — `tests/conftest.py:129`
- `make_atp` (function) — `tests/conftest.py:155`
- `make_proctor` (function) — `tests/conftest.py:203`
- `pytestmark` (const) — `tests/test_api.py:12`
- `test_overview` (function) — `tests/test_api.py:26`
- `test_project_detail_and_404` (function) — `tests/test_api.py:38`
- `test_errors_feed` (function) — `tests/test_api.py:47`
- `test_errors_negative_limit_rejected` (function) — `tests/test_api.py:56`
- `test_errors_sorted_newest_first` (function) — `tests/test_api.py:62`
- `test_errors_project_filter` (function) — `tests/test_api.py:69`
- `test_errors_service_filter` (function) — `tests/test_api.py:82`
- `test_errors_days_filter` (function) — `tests/test_api.py:92`
- `test_recent_errors_helper` (function) — `tests/test_api.py:103`
- `test_models_and_contracts` (function) — `tests/test_api.py:119`
- `test_index_served` (function) — `tests/test_api.py:128`
- `test_detect` (function) — `tests/test_arbiter.py:16`
- `test_collect_happy_path` (function) — `tests/test_arbiter.py:22`
- `test_collect_null_confidence` (function) — `tests/test_arbiter.py:39`
- `test_collect_without_db` (function) — `tests/test_arbiter.py:56`
- `test_detect` (function) — `tests/test_atp.py:15`
- `test_collect_happy_path` (function) — `tests/test_atp.py:21`
- `test_collect_without_dashboard_db` (function) — `tests/test_atp.py:48`
- `test_collect_with_unstatable_bench_output` (function) — `tests/test_atp.py:56`
- `test_collect_catalog_skips_malformed_agent_entry` (function) — `tests/test_atp.py:67`
- `test_read_rows_returns_dicts` (function) — `tests/test_base.py:34`
- `test_read_rows_is_readonly` (function) — `tests/test_base.py:41`
- `test_read_rows_missing_db` (function) — `tests/test_base.py:48`
- `test_read_rows_retries_through_lock` (function) — `tests/test_base.py:53`
- `test_table_names` (function) — `tests/test_base.py:71`
- `test_version_check` (function) — `tests/test_base.py:77`
- `test_mask_secrets_by_key_and_value` (function) — `tests/test_base.py:83`
- `test_shallow_summary_collapses_containers` (function) — `tests/test_base.py:101`
- `test_read_otel_errors` (function) — `tests/test_base.py:108`
- `test_read_otel_errors_missing_dir` (function) — `tests/test_base.py:134`
- `test_read_otel_errors_masks_secrets_in_body` (function) — `tests/test_base.py:138`
- `test_coerce_str` (function) — `tests/test_base.py:158`
- `test_newest_mtime` (function) — `tests/test_base.py:165`
- `test_serve_defaults` (function) — `tests/test_cli.py:8`
- `test_serve_overrides` (function) — `tests/test_cli.py:15`
- `test_tui_subcommand_parses` (function) — `tests/test_cli.py:22`
- `test_drift_detected` (function) — `tests/test_contracts.py:10`
- `test_in_sync` (function) — `tests/test_contracts.py:18`
- `test_canon_missing` (function) — `tests/test_contracts.py:28`
- `test_schema_listing` (function) — `tests/test_contracts.py:35`
- `test_collectors_registry` (function) — `tests/test_discovery.py:11`
- `test_load_config_from_file` (function) — `tests/test_discovery.py:16`
- `test_load_config_defaults` (function) — `tests/test_discovery.py:27`
- `test_discover_finds_projects` (function) — `tests/test_discovery.py:34`
- `test_discover_missing_root` (function) — `tests/test_discovery.py:43`
- `test_discover_dedupes_by_name` (function) — `tests/test_discovery.py:49`
- `test_discover_skips_cowork_output` (function) — `tests/test_discovery.py:58`
- `test_config_is_frozen` (function) — `tests/test_discovery.py:67`
- `test_detect` (function) — `tests/test_maestro.py:12`
- `test_collect_happy_path` (function) — `tests/test_maestro.py:18`
- `test_collect_without_home_db` (function) — `tests/test_maestro.py:42`
- `test_collect_null_status_task_does_not_raise` (function) — `tests/test_maestro.py:50`
- `test_snapshot_defaults_are_empty` (function) — `tests/test_models.py:15`
- `test_snapshot_serializes_to_json` (function) — `tests/test_models.py:26`
- `test_overview_entry` (function) — `tests/test_models.py:43`
- `test_detect` (function) — `tests/test_proctor.py:16`
- `test_collect_happy_path` (function) — `tests/test_proctor.py:22`
- `test_collect_without_state_db` (function) — `tests/test_proctor.py:40`
- `test_collect_masks_secrets_in_log_errors` (function) — `tests/test_proctor.py:48`
- `test_collect_null_status_task_does_not_raise` (function) — `tests/test_proctor.py:62`
- `test_collect_config_llm_not_dict_does_not_raise` (function) — `tests/test_proctor.py:75`
- `test_collects_detected_and_undetected` (function) — `tests/test_service.py:22`
- `test_ttl_cache_returns_same_object` (function) — `tests/test_service.py:30`
- `test_collector_crash_degrades_to_warning` (function) — `tests/test_service.py:35`
- `test_concurrent_get_collects_once` (function) — `tests/test_service.py:49`
- `test_web_days_default_matches_core` (function) — `tests/test_service.py:68`
- `test_detect` (function) — `tests/test_spec_runner.py:15`
- `test_collect_happy_path` (function) — `tests/test_spec_runner.py:22`
- `test_collect_without_db` (function) — `tests/test_spec_runner.py:37`
- `test_collect_with_unexpected_schema` (function) — `tests/test_spec_runner.py:45`
- `pytestmark` (const) — `tests/test_tui.py:19`
- `test_app_boots_with_four_tabs` (function) — `tests/test_tui.py:36`
- `test_projects_table_populates` (function) — `tests/test_tui.py:50`
- `test_undetected_project_row_dimmed` (function) — `tests/test_tui.py:60`
- `test_footer_shows_update_time` (function) — `tests/test_tui.py:70`
- `test_r_binding_recollects` (function) — `tests/test_tui.py:77`
- `test_collect_failure_keeps_last_data` (function) — `tests/test_tui.py:95`
- `test_models_table_matches_web_columns` (function) — `tests/test_tui.py:132`
- `test_contracts_table_shows_drift` (function) — `tests/test_tui.py:145`
- `test_truncate_web_parity` (function) — `tests/test_tui.py:155`
- `test_errors_tab_lists_and_counts` (function) — `tests/test_tui.py:160`
- `test_errors_service_filter` (function) — `tests/test_tui.py:171`
- `test_errors_project_filter` (function) — `tests/test_tui.py:182`
- `test_errors_project_filter_clearable` (function) — `tests/test_tui.py:192`
- `test_errors_days_toggle` (function) — `tests/test_tui.py:212`
- `test_errors_empty_state` (function) — `tests/test_tui.py:223`
- `test_enter_opens_project_detail` (function) — `tests/test_tui.py:236`
- `test_enter_ignored_on_undetected_project` (function) — `tests/test_tui.py:256`
- `test_enter_on_error_row_shows_full_message` (function) — `tests/test_tui.py:268`
- `test_e_key_prefilters_errors_for_project` (function) — `tests/test_tui.py:283`

## Modules

_33 files, 143 public symbols, 150 internal imports._

- `dispatcher/__init__.py` (python)
- `dispatcher/cli.py` (python)
- `dispatcher/core/__init__.py` (python)
- `dispatcher/core/collectors/__init__.py` (python)
- `dispatcher/core/collectors/arbiter.py` (python)
- `dispatcher/core/collectors/atp.py` (python)
- `dispatcher/core/collectors/base.py` (python)
- `dispatcher/core/collectors/maestro.py` (python)
- `dispatcher/core/collectors/proctor.py` (python)
- `dispatcher/core/collectors/spec_runner.py` (python)
- `dispatcher/core/contracts.py` (python)
- `dispatcher/core/discovery.py` (python)
- `dispatcher/core/models.py` (python)
- `dispatcher/core/service.py` (python)
- `dispatcher/server/__init__.py` (python)
- `dispatcher/server/app.py` (python)
- `dispatcher/tui/__init__.py` (python)
- `dispatcher/tui/app.py` (python)
- `dispatcher/tui/detail.py` (python)
- `tests/conftest.py` (python)
- `tests/test_api.py` (python)
- `tests/test_arbiter.py` (python)
- `tests/test_atp.py` (python)
- `tests/test_base.py` (python)
- `tests/test_cli.py` (python)
- `tests/test_contracts.py` (python)
- `tests/test_discovery.py` (python)
- `tests/test_maestro.py` (python)
- `tests/test_models.py` (python)
- `tests/test_proctor.py` (python)
- `tests/test_service.py` (python)
- `tests/test_spec_runner.py` (python)
- `tests/test_tui.py` (python)

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
