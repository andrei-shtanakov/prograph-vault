<!-- prograph:generated -->

---
indexed_at: "2026-07-10T12:31:55Z"
kind: python
name: steward
prograph: project
root: ./steward
snapshot: 4
---

# steward

> > Рабочее имя проекта: steward (провизорно). Управляет жизненным циклом спек, не исполняет. > Это спека самого steward, написанная в его собственном формате (dogfood). > Статус бандла: DRAFT ·…

## Manifest

- declared package: `steward` version `0.1.0`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

_None._

### Public symbols

- `SPEC_META_CONTRACT` (const) — `src/steward/_vendor/spec_meta.py:24`
- `split_frontmatter` (function) — `src/steward/_vendor/spec_meta.py:42`
- `meta_from_dict` (function) — `src/steward/_vendor/spec_meta.py:65`
- `ProfileError` (class) — `src/steward/graph.py:28`
- `load_profile` (function) — `src/steward/graph.py:58`
- `load_profile_data` (function) — `src/steward/graph.py:64`
- `MetaError` (class) — `src/steward/meta.py:42`
- `parse_owner_roles` (function) — `src/steward/meta.py:80`
- `parse_artifact` (function) — `src/steward/meta.py:89`
- `load_artifact` (function) — `src/steward/meta.py:116`
- `PROFILES_DIR` (const) — `tests/test_graph.py:15`
- `test_load_data_builds_graph_with_all_nodes` (function) — `tests/test_graph.py:35`
- `test_nodes_are_specnodes` (function) — `tests/test_graph.py:43`
- `test_upstream_edges_parsed` (function) — `tests/test_graph.py:48`
- `test_delegate_field_parsed` (function) — `tests/test_graph.py:54`
- `test_node_required_defaults_true` (function) — `tests/test_graph.py:60`
- `test_node_can_be_optional` (function) — `tests/test_graph.py:65`
- `test_solo_auto_approve_defaults_false` (function) — `tests/test_graph.py:72`
- `test_dangling_upstream_raises_profile_error` (function) — `tests/test_graph.py:79`
- `test_cycle_raises_profile_error` (function) — `tests/test_graph.py:86`
- `test_duplicate_id_raises_profile_error` (function) — `tests/test_graph.py:98`
- `test_missing_owner_role_raises_profile_error` (function) — `tests/test_graph.py:105`
- `test_empty_artifacts_raises_profile_error` (function) — `tests/test_graph.py:112`
- `test_non_mapping_raises_profile_error` (function) — `tests/test_graph.py:117`
- `test_non_bool_solo_auto_approve_raises_profile_error` (function) — `tests/test_graph.py:122`
- `test_non_bool_required_raises_profile_error` (function) — `tests/test_graph.py:129`
- `test_empty_string_upstream_raises_profile_error` (function) — `tests/test_graph.py:136`
- `test_null_upstream_treated_as_empty` (function) — `tests/test_graph.py:143`
- `test_duplicate_upstream_raises_profile_error` (function) — `tests/test_graph.py:150`
- `test_topo_order_upstream_before_downstream` (function) — `tests/test_graph.py:157`
- `test_topo_order_covers_all_nodes` (function) — `tests/test_graph.py:163`
- `test_load_shipped_lite_profile` (function) — `tests/test_graph.py:168`
- `test_load_shipped_team_profile` (function) — `tests/test_graph.py:176`
- `SPEC_DIR` (const) — `tests/test_meta.py:15`
- `MANAGED` (const) — `tests/test_meta.py:17`
- `test_parse_managed_artifact_base_fields` (function) — `tests/test_meta.py:33`
- `test_owner_roles_split_and_stripped` (function) — `tests/test_meta.py:42`
- `test_traces_to_parsed` (function) — `tests/test_meta.py:48`
- `test_owner_role_and_traces_absent_are_empty` (function) — `tests/test_meta.py:54`
- `test_no_frontmatter_is_unmanaged` (function) — `tests/test_meta.py:61`
- `test_frontmatter_without_spec_stage_is_unmanaged` (function) — `tests/test_meta.py:65`
- `test_empty_spec_stage_is_unmanaged` (function) — `tests/test_meta.py:69`
- `test_malformed_traces_to_raises` (function) — `tests/test_meta.py:73`
- `test_broken_yaml_frontmatter_raises` (function) — `tests/test_meta.py:79`
- `test_unterminated_frontmatter_raises` (function) — `tests/test_meta.py:87`
- `test_non_string_spec_stage_raises` (function) — `tests/test_meta.py:93`
- `test_whitespace_only_trace_id_raises` (function) — `tests/test_meta.py:99`
- `test_trace_ids_are_stripped` (function) — `tests/test_meta.py:105`
- `test_unknown_frontmatter_keys_ignored` (function) — `tests/test_meta.py:112`
- `test_parse_owner_roles_helper` (function) — `tests/test_meta.py:119`
- `test_load_real_dogfood_design_spec` (function) — `tests/test_meta.py:126`
- `test_load_real_dogfood_requirements_multi_owner` (function) — `tests/test_meta.py:134`
- `test_all_dogfood_specs_are_managed` (function) — `tests/test_meta.py:140`

## Modules

_8 files, 53 public symbols, 14 internal imports._

- `src/steward/__init__.py` (python)
- `src/steward/_vendor/__init__.py` (python)
- `src/steward/_vendor/spec_meta.py` (python)
- `src/steward/graph.py` (python)
- `src/steward/meta.py` (python)
- `tests/__init__.py` (python)
- `tests/test_graph.py` (python)
- `tests/test_meta.py` (python)

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
