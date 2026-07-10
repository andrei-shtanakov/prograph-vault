<!-- prograph:generated -->

---
indexed_at: "2026-07-10T12:31:55Z"
kind: rust
name: arbiter-mcp
parent: arbiter
prograph: project
root: ./arbiter/arbiter-mcp
snapshot: 4
---

# arbiter-mcp

## Manifest

- declared package: `arbiter-mcp`

## Public surface

### MCP tools exposed

- `get_agent_status` — `src/server.rs:483`
- `get_budget_status` — `src/server.rs:488`
- `get_metrics` — `src/server.rs:487`
- `report_benchmark` — `src/server.rs:475`
- `report_outcome` — `src/server.rs:479`
- `route_task` — `src/server.rs:471`

### Contracts declared

- [[https---github-com-andrei-shtanakov-maestro-benchmark-contract-report_benchmark-v1-schema-json]] (json_schema) — `tests/contract/report_benchmark-v1.schema.json` — `https://github.com/andrei-shtanakov/maestro/benchmark-contract/report_benchmark-v1.schema.json`

### Public symbols

- `AgentRegistry` (struct) — `src/agents.rs:39`
- `new` (function) — `src/agents.rs:47`
- `get_agent_info` (function) — `src/agents.rs:74`
- `invalidate_cache` (function) — `src/agents.rs:133`
- `invalidate_all_cache` (function) — `src/agents.rs:138`
- `get_all_agent_info` (function) — `src/agents.rs:143`
- `get_total_running_tasks` (function) — `src/agents.rs:154`
- `get_config` (function) — `src/agents.rs:160`
- `agent_ids` (function) — `src/agents.rs:166`
- `AgentConfig` (struct) — `src/config.rs:18`
- `BudgetConfig` (struct) — `src/config.rs:39`
- `RetriesConfig` (struct) — `src/config.rs:46`
- `RateLimitConfig` (struct) — `src/config.rs:53`
- `AgentHealthConfig` (struct) — `src/config.rs:60`
- `ConcurrencyConfig` (struct) — `src/config.rs:67`
- `SlaConfig` (struct) — `src/config.rs:74`
- `InvariantConfig` (struct) — `src/config.rs:81`
- `ArbiterConfig` (struct) — `src/config.rs:97`
- `validate_agents` (function) — `src/config.rs:111`
- `validate_invariants` (function) — `src/config.rs:136`
- `load_agents` (function) — `src/config.rs:160`
- `load_invariants` (function) — `src/config.rs:178`
- `load_config` (function) — `src/config.rs:193`
- `DecisionRecord` (struct) — `src/db.rs:63`
- `OutcomeRecord` (struct) — `src/db.rs:82`
- `AgentStats` (struct) — `src/db.rs:100`
- `BenchmarkRunInput` (struct) — `src/db.rs:115`
- `Database` (struct) — `src/db.rs:136`
- `open` (function) — `src/db.rs:151`
- `open_in_memory` (function) — `src/db.rs:182`
- `migrate` (function) — `src/db.rs:191`
- `insert_decision` (function) — `src/db.rs:213`
- `find_decision_id_by_task` (function) — `src/db.rs:251`
- `find_decision_by_task` (function) — `src/db.rs:267`
- `insert_outcome` (function) — `src/db.rs:309`
- `update_agent_stats` (function) — `src/db.rs:351`
- `get_agent_stats` (function) — `src/db.rs:409`
- `get_agent_stats_by_category` (function) — `src/db.rs:467`
- `get_recent_failures` (function) — `src/db.rs:513`
- `increment_running_tasks` (function) — `src/db.rs:533`
- `decrement_running_tasks` (function) — `src/db.rs:552`
- `get_running_tasks` (function) — `src/db.rs:571`
- `get_total_running_tasks` (function) — `src/db.rs:584`
- `upsert_agent` (function) — `src/db.rs:601`
- `get_agent_state` (function) — `src/db.rs:625`
- `list_agent_ids` (function) — `src/db.rs:640`
- `purge_older_than` (function) — `src/db.rs:656`
- `get_total_cost` (function) — `src/db.rs:689`
- `get_cost_by_agent` (function) — `src/db.rs:703`
- `reset_all_running_tasks` (function) — `src/db.rs:731`
- `insert_benchmark_run` (function) — `src/db.rs:757`
- `count_benchmark_runs` (function) — `src/db.rs:798`
- `get_benchmark_score` (function) — `src/db.rs:817`
- `connection` (function) — `src/db.rs:845`
- `FEATURE_DIM` (const) — `src/features.rs:17`
- `AgentInfo` (struct) — `src/features.rs:58`
- `SystemState` (struct) — `src/features.rs:79`
- `build_feature_vector` (function) — `src/features.rs:123`
- `Metrics` (struct) — `src/metrics.rs:10`
- `MetricsSnapshot` (struct) — `src/metrics.rs:22`
- `LatencySnapshot` (struct) — `src/metrics.rs:31`
- `new` (function) — `src/metrics.rs:40`
- `record_decision` (function) — `src/metrics.rs:57`
- `snapshot` (function) — `src/metrics.rs:107`
- `JsonRpcRequest` (struct) — `src/server.rs:30`
- `JsonRpcResponse` (struct) — `src/server.rs:41`
- `JsonRpcError` (struct) — `src/server.rs:53`
- `McpServer` (struct) — `src/server.rs:227`
- `new` (function) — `src/server.rs:241`
- `run` (function) — `src/server.rs:263`
- `dispatch` (function) — `src/server.rs:349`
- `StatusResult` (struct) — `src/tools/agent_status.rs:17`
- `AgentStatus` (struct) — `src/tools/agent_status.rs:23`
- `Capabilities` (struct) — `src/tools/agent_status.rs:34`
- `CurrentLoad` (struct) — `src/tools/agent_status.rs:43`
- `Performance` (struct) — `src/tools/agent_status.rs:50`
- `CategoryStats` (struct) — `src/tools/agent_status.rs:61`
- `execute` (function) — `src/tools/agent_status.rs:92`
- `result_to_json` (function) — `src/tools/agent_status.rs:200`
- `execute` (function) — `src/tools/get_budget.rs:17`
- `execute` (function) — `src/tools/get_metrics.rs:14`
- `ReportBenchmarkError` (enum) — `src/tools/report_benchmark.rs:15`
- `jsonrpc_code` (function) — `src/tools/report_benchmark.rs:24`
- `execute` (function) — `src/tools/report_benchmark.rs:59`
- `ReportResult` (struct) — `src/tools/report_outcome.rs:18`
- `UpdatedStats` (struct) — `src/tools/report_outcome.rs:28`
- `execute` (function) — `src/tools/report_outcome.rs:46`
- `result_to_json` (function) — `src/tools/report_outcome.rs:205`
- `RouteResult` (struct) — `src/tools/route_task.rs:105`
- `execute` (function) — `src/tools/route_task.rs:204`
- `result_to_json` (function) — `src/tools/route_task.rs:621`
- `WatchPaths` (struct) — `src/watcher.rs:30`
- `ReloadableState` (struct) — `src/watcher.rs:38`
- `path_matches_config` (function) — `src/watcher.rs:54`
- `path_matches_tree` (function) — `src/watcher.rs:61`
- `start_watcher` (function) — `src/watcher.rs:184`

## Modules

_20 files, 96 public symbols, 41 internal imports._

- `src/agents.rs` (rust)
- `src/config.rs` (rust)
- `src/db.rs` (rust)
- `src/features.rs` (rust)
- `src/lib.rs` (rust)
- `src/main.rs` (rust)
- `src/metrics.rs` (rust)
- `src/server.rs` (rust)
- `src/tools/agent_status.rs` (rust)
- `src/tools/get_budget.rs` (rust)
- `src/tools/get_metrics.rs` (rust)
- `src/tools/mod.rs` (rust)
- `src/tools/report_benchmark.rs` (rust)
- `src/tools/report_outcome.rs` (rust)
- `src/tools/route_task.rs` (rust)
- `src/watcher.rs` (rust)
- `tests/contract_test.rs` (rust)
- `tests/golden_tests.rs` (rust)
- `tests/integration.rs` (rust)
- `tests/report_benchmark_test.rs` (rust)

## Inbound references

- from [[arbiter-cli]]:
  - `benches/routing.rs:17` → `agents::AgentRegistry`
  - `benches/routing.rs:18` → `config::*`
  - `benches/routing.rs:19` → `db::Database`
  - `benches/routing.rs:20` → `metrics::Metrics`
  - `benches/routing.rs:21` → `tools::route_task`
  - `src/main.rs:23` → `agents::AgentRegistry`
  - `src/main.rs:24` → `config::*`
  - `src/main.rs:25` → `db::Database`
  - `src/main.rs:25` → `db::DecisionRecord`
  - `src/main.rs:25` → `db::OutcomeRecord`
  - `src/main.rs:26` → `tools::route_task`

## Outbound references

- to [[arbiter-core]]:
  - `src/tools/route_task.rs:14` → `invariant::rules::AgentContext`
  - `src/tools/route_task.rs:14` → `invariant::rules::InvariantThresholds`
  - `src/tools/route_task.rs:14` → `invariant::rules::SystemContext`
  - `src/tools/route_task.rs:14` → `invariant::rules::check_all_invariants`
  - `src/tools/route_task.rs:14` → `invariant::rules::has_critical_failure`
  - `src/main.rs:12` → `policy::decision_tree::DecisionTree`
  - `src/server.rs:15` → `policy::decision_tree::DecisionTree`
  - `src/tools/route_task.rs:17` → `policy::decision_tree::DecisionTree`
  - `src/watcher.rs:19` → `policy::decision_tree::DecisionTree`
  - `tests/golden_tests.rs:15` → `policy::decision_tree::DecisionTree`
  - `tests/integration.rs:11` → `policy::decision_tree::DecisionTree`
  - `src/tools/route_task.rs:18` → `policy::engine::evaluate_for_agents`
  - `src/features.rs:8` → `types::Constraints`
  - `src/features.rs:8` → `types::TaskInput`
  - `src/features.rs:301` → `types::Complexity`
  - `src/features.rs:301` → `types::Constraints`
  - `src/features.rs:301` → `types::Language`
  - `src/features.rs:301` → `types::Priority`
  - `src/features.rs:301` → `types::RunningTask`
  - `src/features.rs:301` → `types::TaskInput`
  - `src/features.rs:301` → `types::TaskType`
  - `src/server.rs:16` → `types::Constraints`
  - `src/server.rs:16` → `types::TaskInput`
  - `src/tools/route_task.rs:19` → `types::AgentAction`
  - `src/tools/route_task.rs:19` → `types::AgentState`
  - `src/tools/route_task.rs:19` → `types::Constraints`
  - `src/tools/route_task.rs:19` → `types::InvariantResult`
  - `src/tools/route_task.rs:19` → `types::PredictionResult`
  - `src/tools/route_task.rs:19` → `types::TaskInput`
  - `src/tools/route_task.rs:19` → `types::TaskType`
  - `src/tools/route_task.rs:533` → `types::PredictionResult`
  - `src/tools/route_task.rs:663` → `types::*`
  - `tests/integration.rs:12` → `types::*`

## Outbound edges

- ↔ [[https---github-com-andrei-shtanakov-maestro-benchmark-contract-report_benchmark-v1-schema-json]] · `contract_link` · `json_schema`
- → [[arbiter-core]] · `package_dep` · `arbiter-core`

## Inbound edges

- ← [[Maestro]] · `mcp_call` · tool `report_outcome`
- ← [[Maestro]] · `mcp_call` · tool `get_agent_status`
- ← [[Maestro]] · `mcp_call` · tool `route_task`
- ← [[Maestro]] · `mcp_call` · tool `report_benchmark`
- ← [[arbiter]] · `mcp_call` · tool `report_outcome`
- ← [[arbiter]] · `mcp_call` · tool `get_agent_status`
- ← [[arbiter]] · `mcp_call` · tool `route_task`
- ← [[arbiter]] · `mcp_call` · tool `report_benchmark`
- ← [[arbiter-cli]] · `package_dep` · `arbiter-mcp`

## Recent changes (last 5)

- snapshot 1 (2026-07-07T16:11:23Z): project added (added)

## Drift findings

_None._
