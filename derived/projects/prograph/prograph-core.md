<!-- prograph:generated -->

---
indexed_at: "2026-07-10T17:42:43Z"
kind: rust
name: prograph-core
parent: prograph
prograph: project
root: ./prograph/prograph-core
snapshot: 6
---

# prograph-core

## Manifest

- declared package: `prograph-core`

## Public surface

### MCP tools exposed

- `attrs_changed` — `src/store.rs:996`
- `import_from_relative` — `src/parsers/python.rs:554`
- `import_source` — `src/parsers/js.rs:209`
- `import_symbol` — `src/parsers/python.rs:545`
- `import_target` — `src/parsers/python.rs:541`
- `import_use` — `src/parsers/rust.rs:478`
- `symbol_class` — `src/parsers/python.rs:549`
- `symbol_class_export` — `src/parsers/js.rs:207`
- `symbol_const` — `src/parsers/python.rs:550`
- `symbol_const_export` — `src/parsers/js.rs:208`
- `symbol_enum` — `src/parsers/rust.rs:472`
- `symbol_function` — `src/parsers/python.rs:548`
- `symbol_function_export` — `src/parsers/js.rs:206`
- `symbol_name` — `src/parsers/python.rs:540`
- `symbol_struct` — `src/parsers/rust.rs:471`
- `symbol_trait` — `src/parsers/rust.rs:473`
- `symbol_type` — `src/parsers/rust.rs:477`

### Contracts declared

_None._

### Public symbols

- `detect` (function) — `src/detectors/contracts.rs:14`
- `DeclaredDetection` (struct) — `src/detectors/declared.rs:13`
- `detect_declared` (function) — `src/detectors/declared.rs:65`
- `detect` (function) — `src/detectors/deps.rs:11`
- `drain_collision_warnings` (function) — `src/detectors/deps.rs:111`
- `detect` (function) — `src/detectors/mcp.rs:10`
- `edge_attrs_hash` (function) — `src/detectors/mod.rs:18`
- `EdgeCandidate` (struct) — `src/detectors/mod.rs:29`
- `EvidenceLocation` (struct) — `src/detectors/mod.rs:48`
- `ContractCandidate` (struct) — `src/detectors/mod.rs:59`
- `DetectionResult` (struct) — `src/detectors/mod.rs:69`
- `detect_all` (function) — `src/detectors/mod.rs:79`
- `DiffEntry` (struct) — `src/diff.rs:9`
- `DiffChange` (enum) — `src/diff.rs:17`
- `diff_by_identity` (function) — `src/diff.rs:34`
- `classify_project` (function) — `src/discovery.rs:24`
- `scan_monorepo` (function) — `src/discovery.rs:83`
- `py_scan_monorepo` (function) — `src/discovery.rs:302`
- `tracked_closure` (function) — `src/discovery.rs:319`
- `missing_names` (function) — `src/discovery.rs:339`
- `py_tracked_closure` (function) — `src/discovery.rs:361`
- `py_missing_names` (function) — `src/discovery.rs:373`
- `DriftFinding` (struct) — `src/drift.rs:7`
- `DriftKind` (enum) — `src/drift.rs:18`
- `EntityKind` (enum) — `src/drift.rs:37`
- `Confidence` (enum) — `src/drift.rs:58`
- `as_str` (function) — `src/drift.rs:65`
- `detect_all` (function) — `src/drift.rs:82`
- `detect_missing` (function) — `src/drift.rs:98`
- `detect_extra` (function) — `src/drift.rs:182`
- `detect_stale_todos` (function) — `src/drift.rs:272`
- `PrographError` (enum) — `src/errors.rs:8`
- `Result` (type) — `src/errors.rs:45`
- `DepRequirement` (struct) — `src/facts.rs:13`
- `Manifest` (struct) — `src/facts.rs:20`
- `ParseWarning` (struct) — `src/facts.rs:37`
- `ContractFile` (struct) — `src/facts.rs:44`
- `ContractKind` (enum) — `src/facts.rs:57`
- `McpToolDecl` (struct) — `src/facts.rs:76`
- `DeclaredMode` (enum) — `src/facts.rs:87`
- `DeclaredPath` (struct) — `src/facts.rs:104`
- `McpClientUse` (struct) — `src/facts.rs:118`
- `Module` (struct) — `src/facts.rs:126`
- `PublicSymbol` (struct) — `src/facts.rs:140`
- `SymbolKind` (enum) — `src/facts.rs:147`
- `as_str` (function) — `src/facts.rs:158`
- `InternalImport` (struct) — `src/facts.rs:172`
- `ExternalImport` (struct) — `src/facts.rs:181`
- `ProjectFacts` (struct) — `src/facts.rs:193`
- `ParseStatus` (enum) — `src/facts.rs:221`
- `IntentItem` (struct) — `src/facts.rs:231`
- `IntentItemKind` (enum) — `src/facts.rs:241`
- `TodoItem` (struct) — `src/facts.rs:251`
- `IntentDoc` (struct) — `src/facts.rs:262`
- `index_monorepo` (function) — `src/indexer.rs:41`
- `parse` (function) — `src/intent/markdown.rs:37`
- `extract_intent` (function) — `src/intent/mod.rs:16`
- `IndexLockGuard` (struct) — `src/lock.rs:11`
- `acquire` (function) — `src/lock.rs:26`
- `path` (function) — `src/lock.rs:57`
- `ProjectKind` (enum) — `src/models.rs:8`
- `ProjectCandidate` (struct) — `src/models.rs:37`
- `NodeKind` (enum) — `src/models.rs:71`
- `EdgeKind` (enum) — `src/models.rs:93`
- `name` (function) — `src/models.rs:106`
- `Edge` (struct) — `src/models.rs:119`
- `ChangeKind` (enum) — `src/models.rs:148`
- `EntityKind` (enum) — `src/models.rs:171`
- `ChangeEvent` (struct) — `src/models.rs:195`
- `SnapshotInfo` (struct) — `src/models.rs:223`
- `Contract` (struct) — `src/models.rs:247`
- `IndexSummary` (struct) — `src/models.rs:274`
- `OutboundEdge` (struct) — `src/models.rs:305`
- `InboundEdge` (struct) — `src/models.rs:325`
- `McpToolDeclRow` (struct) — `src/models.rs:341`
- `ContractFileRow` (struct) — `src/models.rs:349`
- `RecentChangeRow` (struct) — `src/models.rs:358`
- `ProjectDescription` (struct) — `src/models.rs:368`
- `ContractOwner` (struct) — `src/models.rs:409`
- `ContractDescription` (struct) — `src/models.rs:417`
- `ProjectSummary` (struct) — `src/models.rs:431`
- `ContractSummary` (struct) — `src/models.rs:439`
- `MonorepoOverview` (struct) — `src/models.rs:448`
- `EdgeRow` (struct) — `src/models.rs:465`
- `EdgeEvidenceRow` (struct) — `src/models.rs:492`
- `SearchHit` (struct) — `src/models.rs:504`
- `DiffEdgeRow` (struct) — `src/models.rs:515`
- `ModuleRow` (struct) — `src/models.rs:544`
- `PublicSymbolRow` (struct) — `src/models.rs:553`
- `InternalImportRow` (struct) — `src/models.rs:564`
- `SymbolRefRow` (struct) — `src/models.rs:575`
- `DriftFindingRow` (struct) — `src/models.rs:602`
- `scan` (function) — `src/parsers/contracts.rs:13`
- `parse` (function) — `src/parsers/js.rs:25`
- `monorepo_root_from_project` (function) — `src/parsers/mod.rs:15`
- `ParserOutput` (struct) — `src/parsers/mod.rs:34`
- `parse_project` (function) — `src/parsers/mod.rs:52`
- `read_prograph_excludes` (function) — `src/parsers/python.rs:66`
- `workspace_members` (function) — `src/parsers/python.rs:83`
- `declares_workspace` (function) — `src/parsers/python.rs:102`
- `parse` (function) — `src/parsers/python.rs:111`
- `extract_declared_from_table` (function) — `src/parsers/python.rs:224`
- `extract_declared_paths` (function) — `src/parsers/python.rs:282`
- `declares_workspace` (function) — `src/parsers/rust.rs:75`
- `workspace_members` (function) — `src/parsers/rust.rs:89`
- `parse` (function) — `src/parsers/rust.rs:111`
- `ResolvedRef` (struct) — `src/resolvers/mod.rs:15`
- `build_publisher_index` (function) — `src/resolvers/mod.rs:34`
- `resolve` (function) — `src/resolvers/python.rs:11`
- `resolve` (function) — `src/resolvers/rust.rs:9`
- `Store` (struct) — `src/store.rs:48`
- `open` (function) — `src/store.rs:54`
- `schema_version` (function) — `src/store.rs:97`
- `alive_projects` (function) — `src/store.rs:108`
- `alive_edges` (function) — `src/store.rs:130`
- `begin_snapshot` (function) — `src/store.rs:159`
- `alive_mcp_tool_decls` (function) — `src/store.rs:165`
- `alive_contracts` (function) — `src/store.rs:189`
- `describe_project` (function) — `src/store.rs:213`
- `describe_contract` (function) — `src/store.rs:457`
- `monorepo_overview` (function) — `src/store.rs:542`
- `project_by_name` (function) — `src/store.rs:640`
- `snapshot_by_id` (function) — `src/store.rs:655`
- `find_edges_filtered` (function) — `src/store.rs:682`
- `find_edges_with_status_since` (function) — `src/store.rs:760`
- `edge_evidence_for` (function) — `src/store.rs:818`
- `search_fts` (function) — `src/store.rs:840`
- `refs_to_symbol` (function) — `src/store.rs:884`
- `refs_from_project` (function) — `src/store.rs:923`
- `changelog_paginated` (function) — `src/store.rs:950`
- `latest_snapshot_info` (function) — `src/store.rs:1007`
- `connection` (function) — `src/store.rs:1034`
- `recent_changelog_labels` (function) — `src/store.rs:1042`
- `drifts_for_project` (function) — `src/store.rs:1063`
- `find_drifts_filtered` (function) — `src/store.rs:1091`
- `SnapshotWriter` (struct) — `src/store.rs:1147`
- `insert_snapshot` (function) — `src/store.rs:1153`
- `insert_project` (function) — `src/store.rs:1169`
- `touch_project` (function) — `src/store.rs:1186`
- `insert_edge` (function) — `src/store.rs:1209`
- `touch_edge` (function) — `src/store.rs:1231`
- `insert_change_log` (function) — `src/store.rs:1253`
- `insert_contract` (function) — `src/store.rs:1273`
- `touch_contract` (function) — `src/store.rs:1288`
- `insert_contract_file` (function) — `src/store.rs:1296`
- `touch_contract_file` (function) — `src/store.rs:1312`
- `insert_mcp_tool_decl` (function) — `src/store.rs:1327`
- `touch_mcp_tool_decl` (function) — `src/store.rs:1350`
- `insert_edge_evidence` (function) — `src/store.rs:1364`
- `insert_module` (function) — `src/store.rs:1398`
- `insert_public_symbol` (function) — `src/store.rs:1422`
- `insert_internal_import` (function) — `src/store.rs:1451`
- `insert_symbol_ref` (function) — `src/store.rs:1481`
- `conn` (function) — `src/store.rs:1520`
- `rebuild_search_fts` (function) — `src/store.rs:1526`
- `insert_drift_finding` (function) — `src/store.rs:1555`
- `commit` (function) — `src/store.rs:1598`

## Modules

_25 files, 157 public symbols, 52 internal imports._

- `src/detectors/contracts.rs` (rust)
- `src/detectors/declared.rs` (rust)
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
