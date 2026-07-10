<!-- prograph:generated -->

---
indexed_at: "2026-07-10T12:31:55Z"
kind: mixed
name: prograph
prograph: project
root: ./prograph
snapshot: 4
---

# prograph

> Cross-project structure mapper for monorepos. Detects how independent projects in a workspace talk to each other (package deps, shared contracts, MCP calls) and exposes the graph to humans (browser…

## Description

Cross-project structure mapper for monorepos. Detects how independent projects in a workspace talk to each other (package deps, shared contracts, MCP calls) and exposes the graph to humans (browser UI) and AI agents (MCP).

**Status:** M11 — Spec/TODO drift detection (v1.3). Every index run extracts declared intent from each project's `README.md` + `TODO.md` + `docs/superpowers/specs/*.md` (recognising headings `## Public surface`, `## MCP tools exposed`, `## Contracts declared`, `## TODO`) and compares against detected reality. Three drift kinds are persisted in `drift_findings`: **missing** (declared but not implemented), **extra** (implemented but not declared — fires only when the project has SOME intent docs), and **stale_todo** (open TODO whose tokens overlap a recent change_log label). Exposed via MCP tool `find_drifts`, CLI `prograph drift`, REST endpoint `GET /api/drifts`, MD project-card section "## Drift findings", browser UI side panel. Closes the original 2026-05-25 brainstorm requirement "Spec/TODO-driven target state".

See `docs/superpowers/specs/2026-05-25-prograph-design.md` for the full design and `docs/superpowers/plans/` for milestone plans.

## Install (development)

Requires Rust 1.75+ and Python 3.11+.

```sh
uv sync   # installs Python deps AND builds the Rust extension via maturin
```

## Usage

```sh
cd <your-monorepo-root>
prograph init                 # creates .prograph/config.toml + .gitignore
prograph index [--export-md]  # discovers projects, parses manifests, detects edges,
                              #   persists snapshot, writes change_log entries
prograph status [--json]      # shows discovered projects + latest snapshot summary
prograph index --json         # IndexSummary JSON (snapshot_id, n_projects, n_edges, n_changes, ...)
prograph export-md            # re-render MD from latest snapshot (no reindex)
prograph drift [--kind missing|extra|stale_todo] [--json]   # show drift findings (M11)
prograph mcp                  # MCP…

## Manifest

- declared package: `prograph` version `0.1.0`

## Public surface

### MCP tools exposed

- `decide` — `tests/fixtures/monorepo_mcp/py_server/server.py:7`
- `tool_real` — `tests/fixtures/monorepo_drift/declarer/server.py:7`

### Contracts declared

- [[contract-real]] (json_schema) — `tests/fixtures/monorepo_drift/declarer/contracts/contract-real.json` — `contract-real`
- [[obs-v1]] (json_schema) — `tests/fixtures/monorepo_mcp/shared_a/schemas/obs-v1.json` — `obs-v1`

### Public symbols

- `numberIn` (function) — `Sourcetrail/bin/app/user/projects/tictactoe_py/src/tictactoe.py:5`
- `numberOut` (function) — `Sourcetrail/bin/app/user/projects/tictactoe_py/src/tictactoe.py:9`
- `stringOut` (function) — `Sourcetrail/bin/app/user/projects/tictactoe_py/src/tictactoe.py:13`
- `GameObject` (class) — `Sourcetrail/bin/app/user/projects/tictactoe_py/src/tictactoe.py:17`
- `Field` (class) — `Sourcetrail/bin/app/user/projects/tictactoe_py/src/tictactoe.py:21`
- `Player` (class) — `Sourcetrail/bin/app/user/projects/tictactoe_py/src/tictactoe.py:138`
- `HumanPlayer` (class) — `Sourcetrail/bin/app/user/projects/tictactoe_py/src/tictactoe.py:148`
- `ArtificialPlayer` (class) — `Sourcetrail/bin/app/user/projects/tictactoe_py/src/tictactoe.py:183`
- `TicTacToe` (class) — `Sourcetrail/bin/app/user/projects/tictactoe_py/src/tictactoe.py:244`
- `main` (function) — `Sourcetrail/bin/app/user/projects/tictactoe_py/src/tictactoe.py:302`
- `arch` (const) — `Sourcetrail/script/getSystemString.py:6`
- `system` (const) — `Sourcetrail/script/getSystemString.py:7`
- `dist` (const) — `Sourcetrail/script/getSystemString.py:8`
- `s` (const) — `Sourcetrail/script/getSystemString.py:9`
- `Bar` (class) — `Sourcetrail/testing/project_setup/custom_command_python/data/src/bar.py:1`
- `Foo` (class) — `Sourcetrail/testing/project_setup/custom_command_python/data/src/foo.py:3`
- `main` (function) — `Sourcetrail/testing/project_setup/custom_command_python/data/src/main.py:3`
- `Bar` (class) — `Sourcetrail/testing/project_setup/python_empty/data/src/bar.py:3`
- `Baz` (class) — `Sourcetrail/testing/project_setup/python_empty/data/src/baz.py:1`
- `Foo` (class) — `Sourcetrail/testing/project_setup/python_empty/data/src/foo.py:3`
- `test` (function) — `Sourcetrail/testing/project_setup/python_empty/data/src/main.py:4`
- `core_version` (function) — `prograph/__init__.py:41`
- `console` (const) — `prograph/cli.py:23`
- `err_console` (const) — `prograph/cli.py:24`
- `app` (const) — `prograph/cli.py:26`
- `DEFAULT_CONFIG_TOML` (const) — `prograph/cli.py:53`
- `DEFAULT_GITIGNORE` (const) — `prograph/cli.py:80`
- `DEFAULT_TRACKED_TOML` (const) — `prograph/cli.py:95`
- `read_auto_export` (function) — `prograph/config.py:13`
- `read_export_root` (function) — `prograph/config.py:27`
- `TrackedConfigError` (class) — `prograph/config.py:46`
- `read_tracked_projects` (function) — `prograph/config.py:55`
- `export_snapshot` (function) — `prograph/export/__init__.py:82`
- `extract_intro` (function) — `prograph/export/intro.py:12`
- `extract_readme_body` (function) — `prograph/export/intro.py:74`
- `render_project` (function) — `prograph/export/render.py:23`
- `render_contract` (function) — `prograph/export/render.py:228`
- `render_index` (function) — `prograph/export/render.py:275`
- `slugify` (function) — `prograph/export/slug.py:6`
- `contract_slug` (function) — `prograph/export/slug.py:16`
- `build_server` (function) — `prograph/mcp_server.py:27`
- `serve` (function) — `prograph/mcp_server.py:390`
- `main` (function) — `prograph/mcp_server.py:397`
- `ProjectKind` (class) — `prograph/models.py:18`
- `ProjectCandidate` (class) — `prograph/models.py:30`
- `NodeKind` (class) — `prograph/models.py:50`
- `EdgeKind` (class) — `prograph/models.py:59`
- `ChangeKind` (class) — `prograph/models.py:69`
- `EntityKind` (class) — `prograph/models.py:79`
- `Edge` (class) — `prograph/models.py:89`
- `ChangeEvent` (class) — `prograph/models.py:119`
- `SnapshotInfo` (class) — `prograph/models.py:147`
- `IndexSummary` (class) — `prograph/models.py:175`
- `Contract` (class) — `prograph/models.py:201`
- `OutboundEdge` (class) — `prograph/models.py:225`
- `InboundEdge` (class) — `prograph/models.py:245`
- `McpToolDeclRow` (class) — `prograph/models.py:263`
- `ContractFileRow` (class) — `prograph/models.py:275`
- `RecentChangeRow` (class) — `prograph/models.py:293`
- `ModuleRow` (class) — `prograph/models.py:311`
- `PublicSymbolRow` (class) — `prograph/models.py:325`
- `InternalImportRow` (class) — `prograph/models.py:347`
- `SymbolRefRow` (class) — `prograph/models.py:367`
- `DriftFinding` (class) — `prograph/models.py:391`
- `ProjectDescription` (class) — `prograph/models.py:419`
- `ContractOwner` (class) — `prograph/models.py:467`
- `ContractDescription` (class) — `prograph/models.py:483`
- `ProjectSummary` (class) — `prograph/models.py:511`
- `ContractSummary` (class) — `prograph/models.py:523`
- `MonorepoOverview` (class) — `prograph/models.py:541`
- `EdgeRow` (class) — `prograph/models.py:569`
- `EdgeEvidenceRow` (class) — `prograph/models.py:601`
- `SearchHit` (class) — `prograph/models.py:623`
- `DiffEdgeRow` (class) — `prograph/models.py:643`
- `build_app` (function) — `prograph/web_app.py:21`
- `FIXTURES_DIR` (const) — `tests/conftest.py:10`
- `assert_md_dir_matches_golden` (function) — `tests/conftest.py:40`
- `CleanClass` (class) — `tests/fixtures/monorepo_drift/cleaner/cleaner/__init__.py:1`
- `Implemented` (class) — `tests/fixtures/monorepo_drift/declarer/declarer/__init__.py:1`
- `ImportedFrom` (class) — `tests/fixtures/monorepo_drift/declarer/declarer/__init__.py:5`
- `undocumented_extra_fn` (function) — `tests/fixtures/monorepo_drift/declarer/declarer/__init__.py:9`
- `mcp` (const) — `tests/fixtures/monorepo_drift/declarer/server.py:3`
- `Whatever` (class) — `tests/fixtures/monorepo_drift/nointent/nointent/__init__.py:1`
- `TodoListClient` (class) — `tests/fixtures/monorepo_drift/todolist/todolist/__init__.py:1`
- `run` (function) — `tests/fixtures/monorepo_mcp/py_client/client.py:1`
- `run` (function) — `tests/fixtures/monorepo_mcp/py_dual_client/client.py:1`
- `server` (const) — `tests/fixtures/monorepo_mcp/py_server/server.py:3`
- `PublicAPI` (class) — `tests/fixtures/monorepo_modules/py_lib/py_lib/api.py:7`
- `public_fn` (function) — `tests/fixtures/monorepo_modules/py_lib/py_lib/api.py:17`
- `PUBLIC_CONST` (const) — `tests/fixtures/monorepo_modules/py_lib/py_lib/api.py:25`
- `normalize` (function) — `tests/fixtures/monorepo_modules/py_lib/py_lib/helpers.py:1`
- `Store` (class) — `tests/fixtures/monorepo_modules/py_lib/py_lib/storage.py:1`
- `main` (function) — `tests/fixtures/monorepo_symbol_refs/py_consumer/py_consumer/uses.py:5`
- `Client` (class) — `tests/fixtures/monorepo_symbol_refs/py_sdk/py_sdk/client.py:1`
- `AdminClient` (class) — `tests/fixtures/monorepo_symbol_refs/py_sdk/py_sdk/client.py:6`
- `helper` (function) — `tests/fixtures/monorepo_symbol_refs/py_sdk/py_sdk/client.py:10`
- `cli_runner` (const) — `tests/integration/test_bench_baseline.py:21`
- `FIXTURE` (const) — `tests/integration/test_bench_baseline.py:22`
- `pytestmark` (const) — `tests/integration/test_bench_baseline.py:25`
- `test_bench_monorepo_overview` (function) — `tests/integration/test_bench_baseline.py:39`
- `test_bench_describe_project` (function) — `tests/integration/test_bench_baseline.py:43`
- `test_bench_find_edges` (function) — `tests/integration/test_bench_baseline.py:49`
- `test_bench_search_fts` (function) — `tests/integration/test_bench_baseline.py:53`
- `test_bench_reindex_no_changes` (function) — `tests/integration/test_bench_baseline.py:57`
- `runner` (const) — `tests/integration/test_cli_drift.py:12`
- `FIXTURE_MCP` (const) — `tests/integration/test_cli_drift.py:16`
- `test_drift_command_runs` (function) — `tests/integration/test_cli_drift.py:28`
- `test_drift_command_json_empty` (function) — `tests/integration/test_cli_drift.py:36`
- `test_drift_command_filter_by_kind` (function) — `tests/integration/test_cli_drift.py:43`
- `test_drift_command_no_db` (function) — `tests/integration/test_cli_drift.py:48`
- `runner` (const) — `tests/integration/test_cli_export_md.py:10`
- `test_index_with_export_md_writes_files` (function) — `tests/integration/test_cli_export_md.py:23`
- `test_export_md_standalone` (function) — `tests/integration/test_cli_export_md.py:39`
- `test_export_md_idempotent_byte_stable` (function) — `tests/integration/test_cli_export_md.py:50`
- `test_export_md_requires_init` (function) — `tests/integration/test_cli_export_md.py:65`
- `test_export_md_requires_snapshot` (function) — `tests/integration/test_cli_export_md.py:70`
- `test_auto_export_in_config_triggers_md` (function) — `tests/integration/test_cli_export_md.py:78`
- `test_auto_export_false_skips_md` (function) — `tests/integration/test_cli_export_md.py:93`
- `test_golden_monorepo_full` (function) — `tests/integration/test_cli_export_md.py:119`
- `test_golden_monorepo_multilang` (function) — `tests/integration/test_cli_export_md.py:125`
- `test_golden_monorepo_mcp` (function) — `tests/integration/test_cli_export_md.py:131`
- `test_reindex_md_stable_modulo_timestamps` (function) — `tests/integration/test_cli_export_md.py:137`
- `runner` (const) — `tests/integration/test_cli_export_root.py:10`
- `test_index_out_dir_writes_cards_to_staging` (function) — `tests/integration/test_cli_export_root.py:30`
- `test_index_config_export_root_writes_to_staging` (function) — `tests/integration/test_cli_export_root.py:50`
- `test_out_dir_overrides_config` (function) — `tests/integration/test_cli_export_root.py:66`
- `test_export_md_standalone_respects_out_dir` (function) — `tests/integration/test_cli_export_root.py:83`
- `test_default_still_writes_to_prograph` (function) — `tests/integration/test_cli_export_root.py:93`
- `runner` (const) — `tests/integration/test_cli_index.py:10`
- `test_index_requires_init` (function) — `tests/integration/test_cli_index.py:24`
- `test_index_writes_snapshot_with_one_edge` (function) — `tests/integration/test_cli_index.py:31`
- `test_index_fails_when_another_holds_lock` (function) — `tests/integration/test_cli_index.py:49`
- `test_index_json_output` (function) — `tests/integration/test_cli_index.py:69`
- `runner` (const) — `tests/integration/test_cli_index_full.py:11`
- `FIXTURE` (const) — `tests/integration/test_cli_index_full.py:13`
- `test_full_index_detects_all_three_cross_deps` (function) — `tests/integration/test_cli_index_full.py:32`
- `test_full_reindex_idempotent` (function) — `tests/integration/test_cli_index_full.py:41`
- `test_full_version_bump_produces_attrs_changed` (function) — `tests/integration/test_cli_index_full.py:48`
- `test_full_status_after_index_includes_snapshot` (function) — `tests/integration/test_cli_index_full.py:61`
- `runner` (const) — `tests/integration/test_cli_index_mcp.py:13`
- `FIXTURE` (const) — `tests/integration/test_cli_index_mcp.py:14`
- `test_mcp_index_detects_mcp_calls_and_contract_links` (function) — `tests/integration/test_cli_index_mcp.py:56`
- `test_mcp_edge_attrs_carry_tool_name` (function) — `tests/integration/test_cli_index_mcp.py:70`
- `test_mcp_contract_node_created_with_declared_id` (function) — `tests/integration/test_cli_index_mcp.py:87`
- `test_mcp_idempotent_reindex` (function) — `tests/integration/test_cli_index_mcp.py:102`
- `runner` (const) — `tests/integration/test_cli_index_multilang.py:13`
- `FIXTURE` (const) — `tests/integration/test_cli_index_multilang.py:15`
- `test_multilang_index_detects_all_cross_lang_edges` (function) — `tests/integration/test_cli_index_multilang.py:51`
- `test_multilang_python_alias_edge` (function) — `tests/integration/test_cli_index_multilang.py:66`
- `test_multilang_rust_edge` (function) — `tests/integration/test_cli_index_multilang.py:77`
- `test_multilang_js_edge` (function) — `tests/integration/test_cli_index_multilang.py:85`
- `test_multilang_dependency_groups_edge` (function) — `tests/integration/test_cli_index_multilang.py:93`
- `runner` (const) — `tests/integration/test_cli_init.py:10`
- `test_init_creates_prograph_skeleton` (function) — `tests/integration/test_cli_init.py:13`
- `test_init_is_idempotent` (function) — `tests/integration/test_cli_init.py:33`
- `test_init_uses_cwd_when_no_monorepo_flag` (function) — `tests/integration/test_cli_init.py:46`
- `test_init_creates_tracked_toml_template` (function) — `tests/integration/test_cli_init.py:53`
- `test_init_does_not_overwrite_tracked_toml` (function) — `tests/integration/test_cli_init.py:61`
- `runner` (const) — `tests/integration/test_cli_mcp.py:15`
- `FIXTURE` (const) — `tests/integration/test_cli_mcp.py:16`
- `test_mcp_list_tools_returns_ten` (function) — `tests/integration/test_cli_mcp.py:41`
- `test_mcp_monorepo_overview_returns_projects` (function) — `tests/integration/test_cli_mcp.py:62`
- `test_mcp_list_projects_filter_by_kind` (function) — `tests/integration/test_cli_mcp.py:73`
- `test_mcp_describe_project` (function) — `tests/integration/test_cli_mcp.py:83`
- `test_mcp_find_edges_kind_filter` (function) — `tests/integration/test_cli_mcp.py:93`
- `test_mcp_edge_evidence_for_mcp_call` (function) — `tests/integration/test_cli_mcp.py:103`
- `test_mcp_changelog` (function) — `tests/integration/test_cli_mcp.py:120`
- `test_mcp_search_finds_project` (function) — `tests/integration/test_cli_mcp.py:130`
- `test_mcp_snapshot_info_latest` (function) — `tests/integration/test_cli_mcp.py:139`
- `test_mcp_unknown_tool_returns_error` (function) — `tests/integration/test_cli_mcp.py:149`
- `cli_runner` (const) — `tests/integration/test_cli_serve.py:13`
- `FIXTURE` (const) — `tests/integration/test_cli_serve.py:14`
- `test_health` (function) — `tests/integration/test_cli_serve.py:31`
- `test_root_serves_html` (function) — `tests/integration/test_cli_serve.py:37`
- `test_graph_returns_nodes_and_edges` (function) — `tests/integration/test_cli_serve.py:44`
- `test_project_by_name` (function) — `tests/integration/test_cli_serve.py:55`
- `test_project_by_name_404` (function) — `tests/integration/test_cli_serve.py:61`
- `test_project_by_id` (function) — `tests/integration/test_cli_serve.py:66`
- `test_edge_with_evidence` (function) — `tests/integration/test_cli_serve.py:74`
- `test_changelog_returns_list` (function) — `tests/integration/test_cli_serve.py:87`
- `test_search_finds_project` (function) — `tests/integration/test_cli_serve.py:93`
- `test_snapshots_list_and_by_id` (function) — `tests/integration/test_cli_serve.py:100`
- `test_contract_endpoints` (function) — `tests/integration/test_cli_serve.py:111`
- `test_static_html_serves` (function) — `tests/integration/test_cli_serve.py:121`
- `test_static_js_files_load` (function) — `tests/integration/test_cli_serve.py:129`
- `runner` (const) — `tests/integration/test_cli_status.py:10`
- `test_status_lists_classified_projects` (function) — `tests/integration/test_cli_status.py:22`
- `test_status_json_output_is_valid_json` (function) — `tests/integration/test_cli_status.py:38`
- `test_status_requires_init` (function) — `tests/integration/test_cli_status.py:51`
- `test_status_shows_snapshot_info_after_index` (function) — `tests/integration/test_cli_status.py:57`
- `test_status_json_includes_snapshot_when_indexed` (function) — `tests/integration/test_cli_status.py:68`
- `test_status_json_snapshot_null_when_not_indexed` (function) — `tests/integration/test_cli_status.py:79`
- `runner` (const) — `tests/integration/test_cli_tracked.py:11`
- `test_index_filters_to_allowlist_closure` (function) — `tests/integration/test_cli_tracked.py:43`
- `test_index_without_tracked_toml_indexes_all` (function) — `tests/integration/test_cli_tracked.py:53`
- `test_index_malformed_tracked_toml_exits_1` (function) — `tests/integration/test_cli_tracked.py:64`
- `test_index_discover_json_embeds_audit` (function) — `tests/integration/test_cli_tracked.py:72`
- `test_index_discover_text_goes_to_stderr` (function) — `tests/integration/test_cli_tracked.py:85`
- `test_status_json_annotates_tracked` (function) — `tests/integration/test_cli_tracked.py:95`
- `test_status_without_allowlist_all_tracked` (function) — `tests/integration/test_cli_tracked.py:106`
- `test_status_malformed_tracked_toml_exits_1` (function) — `tests/integration/test_cli_tracked.py:114`
- `test_serve_malformed_tracked_toml_exits_1` (function) — `tests/integration/test_cli_tracked.py:121`
- `test_serve_logs_audit_before_start` (function) — `tests/integration/test_cli_tracked.py:130`
- `runner` (const) — `tests/integration/test_cli_version.py:7`
- `test_version_flag_prints_versions_and_exits_zero` (function) — `tests/integration/test_cli_version.py:10`
- `test_no_args_shows_help` (function) — `tests/integration/test_cli_version.py:17`
- `cli_runner` (const) — `tests/integration/test_diff_view_rest.py:12`
- `test_graph_without_since_returns_alive_edges` (function) — `tests/integration/test_diff_view_rest.py:48`
- `test_graph_with_since_tags_diff` (function) — `tests/integration/test_diff_view_rest.py:60`
- `test_scan_monorepo_minimal_fixture` (function) — `tests/integration/test_discovery.py:6`
- `test_scan_monorepo_errors_on_missing_root` (function) — `tests/integration/test_discovery.py:19`
- `runner` (const) — `tests/integration/test_drift_persistence.py:14`
- `FIXTURE` (const) — `tests/integration/test_drift_persistence.py:15`
- `test_declarer_missing_public_symbol` (function) — `tests/integration/test_drift_persistence.py:27`
- `test_declarer_missing_mcp_tool` (function) — `tests/integration/test_drift_persistence.py:38`
- `test_declarer_extra_public_symbol` (function) — `tests/integration/test_drift_persistence.py:46`
- `test_cleaner_has_no_drift` (function) — `tests/integration/test_drift_persistence.py:54`
- `test_nointent_skipped_for_extra` (function) — `tests/integration/test_drift_persistence.py:60`
- `test_drift_first_seen_stable_across_reindex` (function) — `tests/integration/test_drift_persistence.py:66`
- `test_drift_findings_filtered_by_kind` (function) — `tests/integration/test_drift_persistence.py:105`
- `cli_runner` (const) — `tests/integration/test_edge_evidence_all_kinds.py:12`
- `FIXTURE` (const) — `tests/integration/test_edge_evidence_all_kinds.py:13`
- `test_evidence_persisted_in_monorepo_full` (function) — `tests/integration/test_edge_evidence_all_kinds.py:41`
- `test_evidence_persisted_for_mcp_call` (function) — `tests/integration/test_edge_evidence_all_kinds.py:57`
- `test_evidence_persisted_for_contract_link` (function) — `tests/integration/test_edge_evidence_all_kinds.py:64`
- `runner` (const) — `tests/integration/test_mcp_find_drifts.py:15`
- `FIXTURE` (const) — `tests/integration/test_mcp_find_drifts.py:16`
- `test_find_drifts_no_filter` (function) — `tests/integration/test_mcp_find_drifts.py:39`
- `test_find_drifts_by_project` (function) — `tests/integration/test_mcp_find_drifts.py:50`
- `test_find_drifts_by_kind` (function) — `tests/integration/test_mcp_find_drifts.py:59`
- `test_find_drifts_invalid_kind` (function) — `tests/integration/test_mcp_find_drifts.py:68`
- `runner` (const) — `tests/integration/test_mcp_find_symbol_references.py:15`
- `FIXTURE` (const) — `tests/integration/test_mcp_find_symbol_references.py:16`
- `test_find_symbol_references_inbound` (function) — `tests/integration/test_mcp_find_symbol_references.py:39`
- `test_find_symbol_references_outbound` (function) — `tests/integration/test_mcp_find_symbol_references.py:54`
- `test_find_symbol_references_missing_project_arg` (function) — `tests/integration/test_mcp_find_symbol_references.py:68`
- `test_find_symbol_references_invalid_direction` (function) — `tests/integration/test_mcp_find_symbol_references.py:80`
- `runner` (const) — `tests/integration/test_module_facts_js.py:12`
- `FIXTURE` (const) — `tests/integration/test_module_facts_js.py:13`
- `test_js_lib_has_exports` (function) — `tests/integration/test_module_facts_js.py:25`
- `test_js_lib_has_relative_imports` (function) — `tests/integration/test_module_facts_js.py:47`
- `runner` (const) — `tests/integration/test_module_facts_python.py:12`
- `FIXTURE` (const) — `tests/integration/test_module_facts_python.py:13`
- `test_py_lib_has_public_symbols` (function) — `tests/integration/test_module_facts_python.py:25`
- `test_py_lib_has_internal_imports` (function) — `tests/integration/test_module_facts_python.py:48`
- `runner` (const) — `tests/integration/test_module_facts_rust.py:12`
- `FIXTURE` (const) — `tests/integration/test_module_facts_rust.py:13`
- `test_rust_lib_has_pub_symbols` (function) — `tests/integration/test_module_facts_rust.py:25`
- `test_rust_lib_has_crate_imports` (function) — `tests/integration/test_module_facts_rust.py:49`
- `REAL_MONOREPO` (const) — `tests/integration/test_smoke_real.py:38`
- `runner` (const) — `tests/integration/test_smoke_real.py:40`
- `runner` (const) — `tests/integration/test_symbol_refs_python.py:13`
- `FIXTURE` (const) — `tests/integration/test_symbol_refs_python.py:14`
- `test_python_inbound_refs_for_py_sdk` (function) — `tests/integration/test_symbol_refs_python.py:26`
- `test_python_inbound_refs_filter_by_symbol` (function) — `tests/integration/test_symbol_refs_python.py:36`
- `test_python_outbound_refs_for_consumer` (function) — `tests/integration/test_symbol_refs_python.py:44`
- `runner` (const) — `tests/integration/test_symbol_refs_rust.py:13`
- `FIXTURE` (const) — `tests/integration/test_symbol_refs_rust.py:14`
- `test_rust_inbound_refs_for_sdk` (function) — `tests/integration/test_symbol_refs_rust.py:26`
- `test_rust_inbound_module_path_stripped` (function) — `tests/integration/test_symbol_refs_rust.py:34`
- `cli_runner` (const) — `tests/integration/test_workspace_discovery.py:13`
- `FIXTURE` (const) — `tests/integration/test_workspace_discovery.py:14`
- `test_discovery_finds_python_workspace_members` (function) — `tests/integration/test_workspace_discovery.py:25`
- `test_discovery_finds_rust_workspace_members` (function) — `tests/integration/test_workspace_discovery.py:35`
- `test_index_finds_workspace_cross_deps` (function) — `tests/integration/test_workspace_discovery.py:44`
- `test_read_export_root_returns_value` (function) — `tests/unit/test_config.py:20`
- `test_read_export_root_missing_key_is_none` (function) — `tests/unit/test_config.py:28`
- `test_read_export_root_missing_section_is_none` (function) — `tests/unit/test_config.py:33`
- `test_read_export_root_missing_file_is_none` (function) — `tests/unit/test_config.py:38`
- `test_read_export_root_broken_toml_is_none` (function) — `tests/unit/test_config.py:42`
- `test_read_export_root_non_string_is_none` (function) — `tests/unit/test_config.py:47`
- `test_auto_export_still_works` (function) — `tests/unit/test_config.py:52`
- `test_read_tracked_missing_file_is_none` (function) — `tests/unit/test_config.py:58`
- `test_read_tracked_valid_list` (function) — `tests/unit/test_config.py:62`
- `test_read_tracked_empty_list_is_none` (function) — `tests/unit/test_config.py:67`
- `test_read_tracked_missing_key_is_none` (function) — `tests/unit/test_config.py:72`
- `test_read_tracked_malformed_toml_raises` (function) — `tests/unit/test_config.py:77`
- `test_read_tracked_non_list_raises` (function) — `tests/unit/test_config.py:83`
- `test_read_tracked_non_string_items_raise` (function) — `tests/unit/test_config.py:89`
- `test_paths_tracked_path` (function) — `tests/unit/test_config.py:95`
- `test_tracked_closure_subset_and_members` (function) — `tests/unit/test_core_tracked.py:10`
- `test_missing_names_deduplicated` (function) — `tests/unit/test_core_tracked.py:19`
- `test_index_monorepo_two_arg_call_still_works` (function) — `tests/unit/test_core_tracked.py:24`
- `test_drift_finding_pydantic_round_trip` (function) — `tests/unit/test_drift_detection.py:6`
- `test_drift_finding_kind_is_string_not_enum` (function) — `tests/unit/test_drift_detection.py:22`
- `test_intro_from_readme` (function) — `tests/unit/test_export_intro.py:8`
- `test_intro_prefers_readme_over_claude` (function) — `tests/unit/test_export_intro.py:15`
- `test_intro_falls_back_to_claude` (function) — `tests/unit/test_export_intro.py:21`
- `test_intro_falls_back_to_todo` (function) — `tests/unit/test_export_intro.py:26`
- `test_intro_returns_none_when_no_probe` (function) — `tests/unit/test_export_intro.py:31`
- `test_intro_strips_markdown_emphasis` (function) — `tests/unit/test_export_intro.py:35`
- `test_intro_collapses_multiline_paragraph` (function) — `tests/unit/test_export_intro.py:40`
- `test_intro_truncates_long_text` (function) — `tests/unit/test_export_intro.py:45`
- `test_intro_skips_blank_after_heading` (function) — `tests/unit/test_export_intro.py:54`
- `test_intro_handles_no_heading` (function) — `tests/unit/test_export_intro.py:59`
- `test_render_project_minimal` (function) — `tests/unit/test_export_render.py:40`
- `test_render_project_frontmatter_alphabetical` (function) — `tests/unit/test_export_render.py:49`
- `test_render_project_includes_intro_when_provided` (function) — `tests/unit/test_export_render.py:57`
- `test_render_project_omits_intro_when_none` (function) — `tests/unit/test_export_render.py:63`
- `test_render_outbound_edge_package_dep_with_version` (function) — `tests/unit/test_export_render.py:69`
- `test_render_outbound_edge_mcp_call_includes_tool` (function) — `tests/unit/test_export_render.py:85`
- `test_render_outbound_edge_contract_link_uses_double_arrow` (function) — `tests/unit/test_export_render.py:101`
- `test_render_project_is_deterministic` (function) — `tests/unit/test_export_render.py:117`
- `test_render_contract_minimal` (function) — `tests/unit/test_export_render.py:133`
- `test_render_index_minimal` (function) — `tests/unit/test_export_render.py:153`
- `test_public_symbols_render_when_present` (function) — `tests/unit/test_export_render_public_surface.py:35`
- `test_modules_section_renders_summary` (function) — `tests/unit/test_export_render_public_surface.py:52`
- `test_empty_sections_render_none` (function) — `tests/unit/test_export_render_public_surface.py:72`
- `test_render_is_deterministic_with_module_facts` (function) — `tests/unit/test_export_render_public_surface.py:83`
- `test_slugify_ascii_alphanumeric_preserved` (function) — `tests/unit/test_export_slug.py:6`
- `test_slugify_replaces_non_safe_chars` (function) — `tests/unit/test_export_slug.py:10`
- `test_slugify_preserves_case` (function) — `tests/unit/test_export_slug.py:14`
- `test_slugify_empty_returns_unnamed` (function) — `tests/unit/test_export_slug.py:18`
- `test_slugify_unicode_replaced` (function) — `tests/unit/test_export_slug.py:22`
- `test_contract_slug_uses_declared_id` (function) — `tests/unit/test_export_slug.py:27`
- `test_contract_slug_falls_back_to_hash` (function) — `tests/unit/test_export_slug.py:31`
- `test_contract_slug_empty_declared_falls_back` (function) — `tests/unit/test_export_slug.py:36`
- `test_golden_helper_passes_on_identical` (function) — `tests/unit/test_golden_helper.py:8`
- `test_golden_helper_raises_on_diff` (function) — `tests/unit/test_golden_helper.py:21`
- `test_golden_helper_raises_on_missing_file` (function) — `tests/unit/test_golden_helper.py:35`
- `test_golden_helper_normalizes_timestamp` (function) — `tests/unit/test_golden_helper.py:48`
- `runner` (const) — `tests/unit/test_intent_markdown.py:12`
- `FIXTURE` (const) — `tests/unit/test_intent_markdown.py:13`
- `test_intent_extracted_visible_via_describe_project` (function) — `tests/unit/test_intent_markdown.py:16`
- `test_kind_round_trip_via_name` (function) — `tests/unit/test_models.py:15`
- `test_candidate_round_trip` (function) — `tests/unit/test_models.py:26`
- `test_candidate_is_frozen` (function) — `tests/unit/test_models.py:40`
- `test_edge_kind_round_trip` (function) — `tests/unit/test_models.py:49`
- `test_node_kind_round_trip` (function) — `tests/unit/test_models.py:53`
- `test_change_kind_round_trip` (function) — `tests/unit/test_models.py:58`
- `test_entity_kind_round_trip` (function) — `tests/unit/test_models.py:67`
- `test_edge_kind_round_trip_extended` (function) — `tests/unit/test_models.py:72`
- `test_contract_pydantic_mirror_round_trip` (function) — `tests/unit/test_models.py:79`
- `test_project_description_round_trip` (function) — `tests/unit/test_models.py:94`
- `test_search_hit_pydantic_shape` (function) — `tests/unit/test_models.py:128`
- `test_default_paths_under_monorepo_root` (function) — `tests/unit/test_paths.py:8`
- `test_ensure_dirs_creates_missing` (function) — `tests/unit/test_paths.py:20`
- `test_initialized_false_when_no_prograph_dir` (function) — `tests/unit/test_paths.py:29`
- `test_initialized_true_after_ensure_dirs_and_config` (function) — `tests/unit/test_paths.py:34`
- `test_export_root_none_identical_to_default` (function) — `tests/unit/test_paths.py:44`
- `test_relative_export_root_resolves_from_monorepo_root` (function) — `tests/unit/test_paths.py:63`
- `test_export_root_does_not_move_db_or_internals` (function) — `tests/unit/test_paths.py:70`
- `test_absolute_export_root_used_verbatim` (function) — `tests/unit/test_paths.py:80`
- `test_ensure_dirs_creates_export_root_md_dirs` (function) — `tests/unit/test_paths.py:87`
- `cli_runner` (const) — `tests/unit/test_pep508_url_deps.py:11`
- `test_url_dep_resolves_to_in_monorepo_publisher` (function) — `tests/unit/test_pep508_url_deps.py:32`
- `test_python_package_version` (function) — `tests/unit/test_smoke.py:6`
- `test_rust_core_version_matches` (function) — `tests/unit/test_smoke.py:10`
- `STATIC_DIR` (const) — `tests/unit/test_web_static.py:5`
- `test_static_dir_exists` (function) — `tests/unit/test_web_static.py:8`
- `test_index_html_references_expected_ids` (function) — `tests/unit/test_web_static.py:12`
- `test_index_html_loads_app_module` (function) — `tests/unit/test_web_static.py:25`
- `test_graph_js_exports_expected_functions` (function) — `tests/unit/test_web_static.py:31`
- `test_app_js_imports_graph_and_dom` (function) — `tests/unit/test_web_static.py:37`
- `test_app_js_dispatches_select_event` (function) — `tests/unit/test_web_static.py:43`
- `test_app_js_does_not_use_innerHTML` (function) — `tests/unit/test_web_static.py:48`
- `test_graph_js_does_not_use_innerHTML` (function) — `tests/unit/test_web_static.py:57`
- `test_dom_helper_exports_el` (function) — `tests/unit/test_web_static.py:62`
- `test_index_html_has_diff_picker` (function) — `tests/unit/test_web_static.py:68`
- `test_app_js_handles_since_param` (function) — `tests/unit/test_web_static.py:74`
- `test_graph_js_tags_edge_status` (function) — `tests/unit/test_web_static.py:80`
- `test_app_js_renders_public_symbols` (function) — `tests/unit/test_web_static.py:87`
- `test_app_js_renders_inbound_outbound_refs` (function) — `tests/unit/test_web_static.py:95`
- `test_app_js_renders_drift_findings` (function) — `tests/unit/test_web_static.py:103`

## Modules

_81 files, 364 public symbols, 179 internal imports._

- `Sourcetrail/bin/app/user/projects/tictactoe_py/src/tictactoe.py` (python)
- `Sourcetrail/script/getSystemString.py` (python)
- `Sourcetrail/testing/project_setup/custom_command_python/data/src/bar.py` (python)
- `Sourcetrail/testing/project_setup/custom_command_python/data/src/foo.py` (python)
- `Sourcetrail/testing/project_setup/custom_command_python/data/src/main.py` (python)
- `Sourcetrail/testing/project_setup/python_empty/data/src/bar.py` (python)
- `Sourcetrail/testing/project_setup/python_empty/data/src/baz.py` (python)
- `Sourcetrail/testing/project_setup/python_empty/data/src/foo.py` (python)
- `Sourcetrail/testing/project_setup/python_empty/data/src/main.py` (python)
- `prograph/__init__.py` (python)
- `prograph/cli.py` (python)
- `prograph/config.py` (python)
- `prograph/export/__init__.py` (python)
- `prograph/export/intro.py` (python)
- `prograph/export/render.py` (python)
- `prograph/export/slug.py` (python)
- `prograph/mcp_server.py` (python)
- `prograph/models.py` (python)
- `prograph/paths.py` (python)
- `prograph/web_app.py` (python)
- `tests/__init__.py` (python)
- `tests/conftest.py` (python)
- `tests/fixtures/monorepo_drift/cleaner/cleaner/__init__.py` (python)
- `tests/fixtures/monorepo_drift/declarer/declarer/__init__.py` (python)
- `tests/fixtures/monorepo_drift/declarer/server.py` (python)
- `tests/fixtures/monorepo_drift/nointent/nointent/__init__.py` (python)
- `tests/fixtures/monorepo_drift/todolist/todolist/__init__.py` (python)
- `tests/fixtures/monorepo_mcp/py_client/client.py` (python)
- `tests/fixtures/monorepo_mcp/py_dual_client/client.py` (python)
- `tests/fixtures/monorepo_mcp/py_server/server.py` (python)
- `tests/fixtures/monorepo_modules/py_lib/py_lib/__init__.py` (python)
- `tests/fixtures/monorepo_modules/py_lib/py_lib/api.py` (python)
- `tests/fixtures/monorepo_modules/py_lib/py_lib/helpers.py` (python)
- `tests/fixtures/monorepo_modules/py_lib/py_lib/storage.py` (python)
- `tests/fixtures/monorepo_symbol_refs/py_consumer/py_consumer/__init__.py` (python)
- `tests/fixtures/monorepo_symbol_refs/py_consumer/py_consumer/uses.py` (python)
- `tests/fixtures/monorepo_symbol_refs/py_sdk/py_sdk/__init__.py` (python)
- `tests/fixtures/monorepo_symbol_refs/py_sdk/py_sdk/client.py` (python)
- `tests/integration/__init__.py` (python)
- `tests/integration/test_bench_baseline.py` (python)
- `tests/integration/test_cli_drift.py` (python)
- `tests/integration/test_cli_export_md.py` (python)
- `tests/integration/test_cli_export_root.py` (python)
- `tests/integration/test_cli_index.py` (python)
- `tests/integration/test_cli_index_full.py` (python)
- `tests/integration/test_cli_index_mcp.py` (python)
- `tests/integration/test_cli_index_multilang.py` (python)
- `tests/integration/test_cli_init.py` (python)
- `tests/integration/test_cli_mcp.py` (python)
- `tests/integration/test_cli_serve.py` (python)
- `tests/integration/test_cli_status.py` (python)
- `tests/integration/test_cli_tracked.py` (python)
- `tests/integration/test_cli_version.py` (python)
- `tests/integration/test_diff_view_rest.py` (python)
- `tests/integration/test_discovery.py` (python)
- `tests/integration/test_drift_persistence.py` (python)
- `tests/integration/test_edge_evidence_all_kinds.py` (python)
- `tests/integration/test_mcp_find_drifts.py` (python)
- `tests/integration/test_mcp_find_symbol_references.py` (python)
- `tests/integration/test_module_facts_js.py` (python)
- `tests/integration/test_module_facts_python.py` (python)
- `tests/integration/test_module_facts_rust.py` (python)
- `tests/integration/test_smoke_real.py` (python)
- `tests/integration/test_symbol_refs_python.py` (python)
- `tests/integration/test_symbol_refs_rust.py` (python)
- `tests/integration/test_workspace_discovery.py` (python)
- `tests/unit/__init__.py` (python)
- `tests/unit/test_config.py` (python)
- `tests/unit/test_core_tracked.py` (python)
- `tests/unit/test_drift_detection.py` (python)
- `tests/unit/test_export_intro.py` (python)
- `tests/unit/test_export_render.py` (python)
- `tests/unit/test_export_render_public_surface.py` (python)
- `tests/unit/test_export_slug.py` (python)
- `tests/unit/test_golden_helper.py` (python)
- `tests/unit/test_intent_markdown.py` (python)
- `tests/unit/test_models.py` (python)
- `tests/unit/test_paths.py` (python)
- `tests/unit/test_pep508_url_deps.py` (python)
- `tests/unit/test_smoke.py` (python)
- `tests/unit/test_web_static.py` (python)

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
