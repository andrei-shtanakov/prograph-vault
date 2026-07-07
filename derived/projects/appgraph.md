<!-- prograph:generated -->

---
indexed_at: "2026-07-07T16:11:23Z"
kind: python
name: appgraph
prograph: project
root: ./appgraph
snapshot: 1
---

# appgraph

## Manifest

- declared package: `appgraph` version `0.1.0`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

_None._

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
- `DEFAULT_EXCLUDES` (const) — `appgraph/analyze.py:17`
- `SnapshotDiff` (class) — `appgraph/analyze.py:21`
- `analyze_repo` (function) — `appgraph/analyze.py:27`
- `diff_snapshots` (function) — `appgraph/analyze.py:114`
- `app` (const) — `appgraph/cli.py:27`
- `console` (const) — `appgraph/cli.py:28`
- `NEIGHBOR_EDGE_KINDS` (const) — `appgraph/export_md.py:15`
- `export_markdown` (function) — `appgraph/export_md.py:18`
- `NodeKind` (class) — `appgraph/model.py:13`
- `EdgeKind` (class) — `appgraph/model.py:18`
- `SymbolKind` (class) — `appgraph/model.py:24`
- `Node` (class) — `appgraph/model.py:30`
- `Edge` (class) — `appgraph/model.py:40`
- `Snapshot` (class) — `appgraph/model.py:46`
- `file_node_id` (function) — `appgraph/model.py:55`
- `symbol_node_id` (function) — `appgraph/model.py:60`
- `ParseResult` (class) — `appgraph/parse/base.py:13`
- `LanguageParser` (class) — `appgraph/parse/base.py:19`
- `register_parser` (function) — `appgraph/parse/base.py:30`
- `parser_for` (function) — `appgraph/parse/base.py:35`
- `JavaScriptParser` (class) — `appgraph/parse/javascript.py:27`
- `PythonParser` (class) — `appgraph/parse/python.py:24`
- `RustParser` (class) — `appgraph/parse/rust.py:23`
- `STATIC_DIR` (const) — `appgraph/server.py:16`
- `create_app` (function) — `appgraph/server.py:19`
- `GraphStore` (class) — `appgraph/store.py:14`
- `public_func` (function) — `tests/fixtures/parser_repo/pkg/feature.py:18`
- `async_public` (function) — `tests/fixtures/parser_repo/pkg/feature.py:22`
- `PublicClass` (class) — `tests/fixtures/parser_repo/pkg/feature.py:26`
- `Helper` (class) — `tests/fixtures/parser_repo/pkg/helpers.py:1`
- `helper_func` (function) — `tests/fixtures/parser_repo/pkg/helpers.py:5`
- `Sibling` (class) — `tests/fixtures/parser_repo/pkg/sibling.py:1`
- `test_analyze_repo_emits_cross_file_reference_edge` (function) — `tests/test_analyze.py:12`
- `test_analyze_repo_documents_overconnection_on_shared_names` (function) — `tests/test_analyze.py:43`
- `test_analyze_repo_skips_same_file_shadowing` (function) — `tests/test_analyze.py:80`
- `test_analyze_repo_walks_supported_files_and_honors_excludes` (function) — `tests/test_analyze.py:119`
- `test_analyze_repo_creates_mixed_language_snapshot` (function) — `tests/test_analyze.py:169`
- `test_analyze_repo_honors_gitignore_patterns_and_negation` (function) — `tests/test_analyze.py:207`
- `test_analyze_repo_skips_external_source_symlinks` (function) — `tests/test_analyze.py:271`
- `test_analyze_repo_does_not_attach_module_level_usage_to_previous_symbol` (function) — `tests/test_analyze.py:297`
- `test_analyze_repo_reuses_unchanged_files_and_reparses_only_changed` (function) — `tests/test_analyze.py:329`
- `test_analyze_repo_parses_new_files_during_incremental_run` (function) — `tests/test_analyze.py:360`
- `test_analyze_repo_recomputes_import_edges_when_file_set_changes` (function) — `tests/test_analyze.py:377`
- `test_analyze_repo_reuses_rewritten_files_with_identical_hash` (function) — `tests/test_analyze.py:396`
- `test_analyze_repo_drops_removed_files_from_incremental_snapshot` (function) — `tests/test_analyze.py:415`
- `test_analyze_repo_reresolves_references_over_merged_incremental_graph` (function) — `tests/test_analyze.py:431`
- `test_diff_snapshots_reports_added_removed_and_changed_nodes` (function) — `tests/test_analyze.py:459`
- `PROJECT_ROOT` (const) — `tests/test_bootstrap.py:15`
- `test_version_is_exported` (function) — `tests/test_bootstrap.py:22`
- `test_cli_version_flag` (function) — `tests/test_bootstrap.py:26`
- `test_installed_cli_entry_point_reports_version` (function) — `tests/test_bootstrap.py:33`
- `test_sample_repo_fixture_exists` (function) — `tests/test_bootstrap.py:45`
- `test_pyproject_declares_bootstrap_dependencies_and_tooling` (function) — `tests/test_bootstrap.py:51`
- `test_pyproject_configures_required_quality_tools` (function) — `tests/test_bootstrap.py:80`
- `test_tree_sitter_language_pack_has_required_grammars` (function) — `tests/test_bootstrap.py:101`
- `test_cli_analyze_persists_snapshot_and_status_reports_counts` (function) — `tests/test_cli.py:15`
- `test_cli_analyze_never_snapshots_default_or_custom_excluded_dirs` (function) — `tests/test_cli.py:63`
- `test_cli_analyze_can_disable_gitignore` (function) — `tests/test_cli.py:83`
- `test_cli_analyze_passes_latest_snapshot_as_previous` (function) — `tests/test_cli.py:101`
- `test_cli_analyze_drops_import_edges_to_gitignored_files` (function) — `tests/test_cli.py:127`
- `test_cli_status_returns_error_without_snapshot` (function) — `tests/test_cli.py:148`
- `test_cli_status_shows_delta_against_previous_snapshot` (function) — `tests/test_cli.py:155`
- `test_cli_serve_runs_uvicorn_for_persisted_snapshot` (function) — `tests/test_cli.py:215`
- `test_cli_serve_returns_error_without_snapshot` (function) — `tests/test_cli.py:241`
- `test_export_markdown_matches_golden_tree` (function) — `tests/test_export_md.py:15`
- `test_cli_export_md_reads_latest_snapshot_without_store_writes` (function) — `tests/test_export_md.py:29`
- `test_cli_export_md_uses_latest_snapshot` (function) — `tests/test_export_md.py:58`
- `test_export_markdown_mermaid_escapes_labels_and_avoids_id_collisions` (function) — `tests/test_export_md.py:92`
- `test_export_markdown_mermaid_handles_isolated_files_and_duplicate_edges` (function) — `tests/test_export_md.py:142`
- `test_export_markdown_preserves_extensions_to_avoid_card_collisions` (function) — `tests/test_export_md.py:204`
- `test_export_markdown_rejects_paths_outside_file_cards_dir` (function) — `tests/test_export_md.py:251`
- `test_file_node_id_is_deterministic_and_stable_for_same_path` (function) — `tests/test_model.py:21`
- `test_file_node_id_normalizes_equivalent_relative_paths` (function) — `tests/test_model.py:28`
- `test_symbol_node_id_is_deterministic_and_stable_for_same_path_and_name` (function) — `tests/test_model.py:33`
- `test_symbol_node_id_rejects_empty_symbol_name` (function) — `tests/test_model.py:59`
- `test_snapshot_round_trips_through_model_dump_and_reparse` (function) — `tests/test_model.py:64`
- `test_models_reject_unknown_enum_values` (function) — `tests/test_model.py:101`
- `test_parser_for_dispatches_javascript_and_typescript_files` (function) — `tests/test_parse_javascript.py:10`
- `test_javascript_parser_emits_export_symbols_and_relative_import_edges` (function) — `tests/test_parse_javascript.py:18`
- `test_typescript_parser_reports_typescript_and_emits_expected_graph` (function) — `tests/test_parse_javascript.py:97`
- `test_jsx_and_tsx_files_parse_with_expected_grammars` (function) — `tests/test_parse_javascript.py:189`
- `test_javascript_parser_handles_default_expression_and_duplicate_exports` (function) — `tests/test_parse_javascript.py:269`
- `test_javascript_parser_limits_exported_variable_names_to_bindings` (function) — `tests/test_parse_javascript.py:324`
- `test_parser_for_dispatches_python_files` (function) — `tests/test_parse_python.py:10`
- `test_python_parser_emits_exact_file_symbol_and_contains_graph` (function) — `tests/test_parse_python.py:17`
- `test_python_parser_resolves_internal_imports_and_drops_external_imports` (function) — `tests/test_parse_python.py:79`
- `test_python_parser_resolves_imports_from_package_init` (function) — `tests/test_parse_python.py:101`
- `test_parser_for_dispatches_rust_files` (function) — `tests/test_parse_rust.py:10`
- `test_rust_parser_emits_public_symbols_and_internal_import_edges` (function) — `tests/test_parse_rust.py:16`
- `test_rust_parser_parses_module_files_without_private_symbols` (function) — `tests/test_parse_rust.py:103`
- `test_rust_parser_emits_public_symbols_inside_inline_modules` (function) — `tests/test_parse_rust.py:129`
- `test_rust_parser_resolves_use_only_grouped_crate_imports` (function) — `tests/test_parse_rust.py:151`
- `test_rust_parser_resolves_crate_imports_from_nested_crate_root` (function) — `tests/test_parse_rust.py:191`
- `test_graph_returns_latest_snapshot_nodes_and_edges` (function) — `tests/test_server.py:13`
- `test_root_returns_static_cytoscape_page` (function) — `tests/test_server.py:83`
- `test_static_app_js_is_served` (function) — `tests/test_server.py:94`
- `test_graph_filters_by_node_kind_and_edge_kind` (function) — `tests/test_server.py:105`
- `test_graph_rejects_invalid_filters` (function) — `tests/test_server.py:142`
- `test_node_returns_node_neighbors_and_directional_edges` (function) — `tests/test_server.py:152`
- `test_file_node_returns_mixed_neighbors_and_directional_edges` (function) — `tests/test_server.py:205`
- `test_status_returns_snapshot_summary` (function) — `tests/test_server.py:235`
- `test_rest_reads_latest_snapshot` (function) — `tests/test_server.py:254`
- `test_unknown_node_returns_404` (function) — `tests/test_server.py:274`
- `test_empty_store_returns_404_for_rest_reads` (function) — `tests/test_server.py:283`
- `test_uninitialized_store_returns_404_for_rest_reads` (function) — `tests/test_server.py:299`
- `test_schema_missing_store_returns_404_for_rest_reads` (function) — `tests/test_server.py:309`
- `test_snapshot_round_trips_through_store_identically` (function) — `tests/test_store.py:14`
- `test_two_snapshots_coexist_and_latest_returns_newest` (function) — `tests/test_store.py:26`
- `test_empty_and_missing_snapshot_reads_return_none` (function) — `tests/test_store.py:52`
- `test_init_schema_creates_tables_indexes_and_enables_wal` (function) — `tests/test_store.py:61`
- `test_write_snapshot_rolls_back_all_rows_on_failure` (function) — `tests/test_store.py:92`
- `test_write_snapshot_rejects_edges_to_missing_nodes` (function) — `tests/test_store.py:113`
- `test_latest_uses_timestamp_instant_not_lexicographic_text` (function) — `tests/test_store.py:141`

## Modules

_37 files, 134 public symbols, 83 internal imports._

- `Sourcetrail/bin/app/user/projects/tictactoe_py/src/tictactoe.py` (python)
- `Sourcetrail/script/getSystemString.py` (python)
- `Sourcetrail/testing/project_setup/custom_command_python/data/src/bar.py` (python)
- `Sourcetrail/testing/project_setup/custom_command_python/data/src/foo.py` (python)
- `Sourcetrail/testing/project_setup/custom_command_python/data/src/main.py` (python)
- `Sourcetrail/testing/project_setup/python_empty/data/src/bar.py` (python)
- `Sourcetrail/testing/project_setup/python_empty/data/src/baz.py` (python)
- `Sourcetrail/testing/project_setup/python_empty/data/src/foo.py` (python)
- `Sourcetrail/testing/project_setup/python_empty/data/src/main.py` (python)
- `appgraph/__init__.py` (python)
- `appgraph/analyze.py` (python)
- `appgraph/cli.py` (python)
- `appgraph/export_md.py` (python)
- `appgraph/model.py` (python)
- `appgraph/parse/__init__.py` (python)
- `appgraph/parse/base.py` (python)
- `appgraph/parse/javascript.py` (python)
- `appgraph/parse/python.py` (python)
- `appgraph/parse/rust.py` (python)
- `appgraph/server.py` (python)
- `appgraph/store.py` (python)
- `tests/conftest.py` (python)
- `tests/fixtures/parser_repo/pkg/__init__.py` (python)
- `tests/fixtures/parser_repo/pkg/feature.py` (python)
- `tests/fixtures/parser_repo/pkg/helpers.py` (python)
- `tests/fixtures/parser_repo/pkg/sibling.py` (python)
- `tests/fixtures/sample_repo/pkg/__init__.py` (python)
- `tests/test_analyze.py` (python)
- `tests/test_bootstrap.py` (python)
- `tests/test_cli.py` (python)
- `tests/test_export_md.py` (python)
- `tests/test_model.py` (python)
- `tests/test_parse_javascript.py` (python)
- `tests/test_parse_python.py` (python)
- `tests/test_parse_rust.py` (python)
- `tests/test_server.py` (python)
- `tests/test_store.py` (python)

## Inbound references

_None._

## Outbound references

_None._

## Outbound edges

- → [[spec-runner]] · `package_dep` · `spec-runner` `>=2.2.1`

## Inbound edges

_None._

## Recent changes (last 5)

- snapshot 1 (2026-07-07T16:11:23Z): project added (added)

## Drift findings

_None._
