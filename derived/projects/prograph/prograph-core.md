<!-- prograph:generated -->

---
indexed_at: "2026-07-07T16:11:23Z"
kind: rust
name: prograph-core
parent: prograph
prograph: project
root: ./prograph/prograph-core
snapshot: 1
---

# prograph-core

## Manifest

- declared package: `prograph-core`

## Public surface

### MCP tools exposed

- `attrs_changed` — `src/store.rs:995`
- `import_from_relative` — `src/parsers/python.rs:475`
- `import_source` — `src/parsers/js.rs:206`
- `import_symbol` — `src/parsers/python.rs:466`
- `import_target` — `src/parsers/python.rs:462`
- `import_use` — `src/parsers/rust.rs:455`
- `symbol_class` — `src/parsers/python.rs:470`
- `symbol_class_export` — `src/parsers/js.rs:204`
- `symbol_const` — `src/parsers/python.rs:471`
- `symbol_const_export` — `src/parsers/js.rs:205`
- `symbol_enum` — `src/parsers/rust.rs:449`
- `symbol_function` — `src/parsers/python.rs:469`
- `symbol_function_export` — `src/parsers/js.rs:203`
- `symbol_name` — `src/parsers/python.rs:461`
- `symbol_struct` — `src/parsers/rust.rs:448`
- `symbol_trait` — `src/parsers/rust.rs:450`
- `symbol_type` — `src/parsers/rust.rs:454`

### Contracts declared

_None._

### Public symbols

- `detect` (function) — `src/detectors/contracts.rs:16`
- `detect` (function) — `src/detectors/deps.rs:13`
- `drain_collision_warnings` (function) — `src/detectors/deps.rs:116`
- `detect` (function) — `src/detectors/mcp.rs:12`
- `EdgeCandidate` (struct) — `src/detectors/mod.rs:14`
- `EvidenceLocation` (struct) — `src/detectors/mod.rs:33`
- `ContractCandidate` (struct) — `src/detectors/mod.rs:44`
- `DetectionResult` (struct) — `src/detectors/mod.rs:54`
- `detect_all` (function) — `src/detectors/mod.rs:60`
- `DiffEntry` (struct) — `src/diff.rs:9`
- `DiffChange` (enum) — `src/diff.rs:17`
- `diff_by_identity` (function) — `src/diff.rs:34`
- `classify_project` (function) — `src/discovery.rs:24`
- `scan_monorepo` (function) — `src/discovery.rs:83`
- `py_scan_monorepo` (function) — `src/discovery.rs:303`
- `DriftFinding` (struct) — `src/drift.rs:7`
- `DriftKind` (enum) — `src/drift.rs:18`
- `EntityKind` (enum) — `src/drift.rs:35`
- `Confidence` (enum) — `src/drift.rs:54`
- `as_str` (function) — `src/drift.rs:61`
- `detect_all` (function) — `src/drift.rs:78`
- `detect_missing` (function) — `src/drift.rs:94`
- `detect_extra` (function) — `src/drift.rs:178`
- `detect_stale_todos` (function) — `src/drift.rs:268`
- `PrographError` (enum) — `src/errors.rs:8`
- `Result` (type) — `src/errors.rs:45`
- `DepRequirement` (struct) — `src/facts.rs:13`
- `Manifest` (struct) — `src/facts.rs:20`
- `ParseWarning` (struct) — `src/facts.rs:37`
- `ContractFile` (struct) — `src/facts.rs:44`
- `ContractKind` (enum) — `src/facts.rs:57`
- `McpToolDecl` (struct) — `src/facts.rs:76`
- `McpClientUse` (struct) — `src/facts.rs:86`
- `Module` (struct) — `src/facts.rs:94`
- `PublicSymbol` (struct) — `src/facts.rs:108`
- `SymbolKind` (enum) — `src/facts.rs:115`
- `as_str` (function) — `src/facts.rs:126`
- `InternalImport` (struct) — `src/facts.rs:140`
- `ExternalImport` (struct) — `src/facts.rs:149`
- `ProjectFacts` (struct) — `src/facts.rs:161`
- `ParseStatus` (enum) — `src/facts.rs:186`
- `IntentItem` (struct) — `src/facts.rs:196`
- `IntentItemKind` (enum) — `src/facts.rs:206`
- `TodoItem` (struct) — `src/facts.rs:216`
- `IntentDoc` (struct) — `src/facts.rs:227`
- `index_monorepo` (function) — `src/indexer.rs:24`
- `parse` (function) — `src/intent/markdown.rs:37`
- `extract_intent` (function) — `src/intent/mod.rs:16`
- `IndexLockGuard` (struct) — `src/lock.rs:11`
- `acquire` (function) — `src/lock.rs:26`
- `path` (function) — `src/lock.rs:57`
- `ProjectKind` (enum) — `src/models.rs:8`
- `ProjectCandidate` (struct) — `src/models.rs:37`
- `NodeKind` (enum) — `src/models.rs:71`
- `EdgeKind` (enum) — `src/models.rs:93`
- `name` (function) — `src/models.rs:105`
- `Edge` (struct) — `src/models.rs:117`
- `ChangeKind` (enum) — `src/models.rs:146`
- `EntityKind` (enum) — `src/models.rs:169`
- `ChangeEvent` (struct) — `src/models.rs:193`
- `SnapshotInfo` (struct) — `src/models.rs:221`
- `Contract` (struct) — `src/models.rs:245`
- `IndexSummary` (struct) — `src/models.rs:272`
- `OutboundEdge` (struct) — `src/models.rs:303`
- `InboundEdge` (struct) — `src/models.rs:323`
- `McpToolDeclRow` (struct) — `src/models.rs:339`
- `ContractFileRow` (struct) — `src/models.rs:347`
- `RecentChangeRow` (struct) — `src/models.rs:356`
- `ProjectDescription` (struct) — `src/models.rs:366`
- `ContractOwner` (struct) — `src/models.rs:407`
- `ContractDescription` (struct) — `src/models.rs:415`
- `ProjectSummary` (struct) — `src/models.rs:429`
- `ContractSummary` (struct) — `src/models.rs:437`
- `MonorepoOverview` (struct) — `src/models.rs:446`
- `EdgeRow` (struct) — `src/models.rs:463`
- `EdgeEvidenceRow` (struct) — `src/models.rs:490`
- `SearchHit` (struct) — `src/models.rs:502`
- `DiffEdgeRow` (struct) — `src/models.rs:513`
- `ModuleRow` (struct) — `src/models.rs:542`
- `PublicSymbolRow` (struct) — `src/models.rs:551`
- `InternalImportRow` (struct) — `src/models.rs:562`
- `SymbolRefRow` (struct) — `src/models.rs:573`
- `DriftFindingRow` (struct) — `src/models.rs:600`
- `scan` (function) — `src/parsers/contracts.rs:13`
- `parse` (function) — `src/parsers/js.rs:25`
- `monorepo_root_from_project` (function) — `src/parsers/mod.rs:15`
- `ParserOutput` (struct) — `src/parsers/mod.rs:34`
- `parse_project` (function) — `src/parsers/mod.rs:50`
- `read_prograph_excludes` (function) — `src/parsers/python.rs:66`
- `workspace_members` (function) — `src/parsers/python.rs:83`
- `declares_workspace` (function) — `src/parsers/python.rs:102`
- `parse` (function) — `src/parsers/python.rs:111`
- `declares_workspace` (function) — `src/parsers/rust.rs:73`
- `workspace_members` (function) — `src/parsers/rust.rs:87`
- `parse` (function) — `src/parsers/rust.rs:109`
- `ResolvedRef` (struct) — `src/resolvers/mod.rs:15`
- `build_publisher_index` (function) — `src/resolvers/mod.rs:34`
- `resolve` (function) — `src/resolvers/python.rs:11`
- `resolve` (function) — `src/resolvers/rust.rs:9`
- `Store` (struct) — `src/store.rs:47`
- `open` (function) — `src/store.rs:53`
- `schema_version` (function) — `src/store.rs:96`
- `alive_projects` (function) — `src/store.rs:107`
- `alive_edges` (function) — `src/store.rs:129`
- `begin_snapshot` (function) — `src/store.rs:158`
- `alive_mcp_tool_decls` (function) — `src/store.rs:164`
- `alive_contracts` (function) — `src/store.rs:188`
- `describe_project` (function) — `src/store.rs:212`
- `describe_contract` (function) — `src/store.rs:456`
- `monorepo_overview` (function) — `src/store.rs:541`
- `project_by_name` (function) — `src/store.rs:639`
- `snapshot_by_id` (function) — `src/store.rs:654`
- `find_edges_filtered` (function) — `src/store.rs:681`
- `find_edges_with_status_since` (function) — `src/store.rs:759`
- `edge_evidence_for` (function) — `src/store.rs:817`
- `search_fts` (function) — `src/store.rs:839`
- `refs_to_symbol` (function) — `src/store.rs:883`
- `refs_from_project` (function) — `src/store.rs:922`
- `changelog_paginated` (function) — `src/store.rs:949`
- `latest_snapshot_info` (function) — `src/store.rs:1006`
- `connection` (function) — `src/store.rs:1033`
- `recent_changelog_labels` (function) — `src/store.rs:1041`
- `drifts_for_project` (function) — `src/store.rs:1062`
- `find_drifts_filtered` (function) — `src/store.rs:1090`
- `SnapshotWriter` (struct) — `src/store.rs:1146`
- `insert_snapshot` (function) — `src/store.rs:1152`
- `insert_project` (function) — `src/store.rs:1168`
- `touch_project` (function) — `src/store.rs:1185`
- `insert_edge` (function) — `src/store.rs:1208`
- `touch_edge` (function) — `src/store.rs:1230`
- `insert_change_log` (function) — `src/store.rs:1252`
- `insert_contract` (function) — `src/store.rs:1272`
- `touch_contract` (function) — `src/store.rs:1287`
- `insert_contract_file` (function) — `src/store.rs:1295`
- `touch_contract_file` (function) — `src/store.rs:1311`
- `insert_mcp_tool_decl` (function) — `src/store.rs:1326`
- `touch_mcp_tool_decl` (function) — `src/store.rs:1349`
- `insert_edge_evidence` (function) — `src/store.rs:1363`
- `insert_module` (function) — `src/store.rs:1397`
- `insert_public_symbol` (function) — `src/store.rs:1421`
- `insert_internal_import` (function) — `src/store.rs:1450`
- `insert_symbol_ref` (function) — `src/store.rs:1480`
- `conn` (function) — `src/store.rs:1519`
- `rebuild_search_fts` (function) — `src/store.rs:1525`
- `insert_drift_finding` (function) — `src/store.rs:1554`
- `commit` (function) — `src/store.rs:1597`

## Modules

_24 files, 146 public symbols, 46 internal imports._

- `src/detectors/contracts.rs` (rust)
- `src/detectors/deps.rs` (rust)
- `src/detectors/mcp.rs` (rust)
- `src/detectors/mod.rs` (rust)
- `src/diff.rs` (rust)
- `src/discovery.rs` (rust)
- `src/drift.rs` (rust)
- `src/errors.rs` (rust)
- `src/facts.rs` (rust)
- `src/indexer.rs` (rust)
- `src/intent/markdown.rs` (rust)
- `src/intent/mod.rs` (rust)
- `src/lib.rs` (rust)
- `src/lock.rs` (rust)
- `src/models.rs` (rust)
- `src/parsers/contracts.rs` (rust)
- `src/parsers/js.rs` (rust)
- `src/parsers/mod.rs` (rust)
- `src/parsers/python.rs` (rust)
- `src/parsers/rust.rs` (rust)
- `src/resolvers/mod.rs` (rust)
- `src/resolvers/python.rs` (rust)
- `src/resolvers/rust.rs` (rust)
- `src/store.rs` (rust)

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
