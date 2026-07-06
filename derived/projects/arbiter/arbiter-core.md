<!-- prograph:generated -->

---
indexed_at: "2026-05-27T12:45:37Z"
kind: rust
name: arbiter-core
parent: arbiter
prograph: project
root: ./arbiter/arbiter-core
snapshot: 48
---

# arbiter-core

## Manifest

- declared package: `arbiter-core`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

_None._

### Public symbols

- `ArbiterError` (enum) — `src/error.rs:7`
- `Result` (type) — `src/error.rs:26`
- `AgentContext` (struct) — `src/invariant/rules.rs:17`
- `SystemContext` (struct) — `src/invariant/rules.rs:40`
- `InvariantThresholds` (struct) — `src/invariant/rules.rs:57`
- `agent_available` (function) — `src/invariant/rules.rs:77`
- `scope_isolation` (function) — `src/invariant/rules.rs:107`
- `branch_not_locked` (function) — `src/invariant/rules.rs:146`
- `concurrency_limit` (function) — `src/invariant/rules.rs:176`
- `budget_remaining` (function) — `src/invariant/rules.rs:203`
- `retry_limit` (function) — `src/invariant/rules.rs:241`
- `rate_limit` (function) — `src/invariant/rules.rs:265`
- `agent_health` (function) — `src/invariant/rules.rs:289`
- `task_compatible` (function) — `src/invariant/rules.rs:313`
- `sla_feasible` (function) — `src/invariant/rules.rs:354`
- `check_all_invariants` (function) — `src/invariant/rules.rs:409`
- `has_critical_failure` (function) — `src/invariant/rules.rs:430`
- `DEFAULT_REDACT_KEYS` (const) — `src/obs.rs:44`
- `init_logging` (function) — `src/obs.rs:82`
- `child_env` (function) — `src/obs.rs:156`
- `DecisionTree` (struct) — `src/policy/decision_tree.rs:44`
- `from_json` (function) — `src/policy/decision_tree.rs:68`
- `predict` (function) — `src/policy/decision_tree.rs:150`
- `node_count` (function) — `src/policy/decision_tree.rs:293`
- `depth` (function) — `src/policy/decision_tree.rs:298`
- `n_classes` (function) — `src/policy/decision_tree.rs:303`
- `n_features` (function) — `src/policy/decision_tree.rs:308`
- `class_names` (function) — `src/policy/decision_tree.rs:313`
- `feature_names` (function) — `src/policy/decision_tree.rs:318`
- `evaluate_for_agents` (function) — `src/policy/engine.rs:18`
- `InferenceBackend` (trait) — `src/traits.rs:16`
- `DecisionStore` (trait) — `src/traits.rs:38`
- `AgentStore` (trait) — `src/traits.rs:64`
- `AgentAction` (enum) — `src/types.rs:15`
- `AgentState` (enum) — `src/types.rs:27`
- `Severity` (enum) — `src/types.rs:40`
- `TaskType` (enum) — `src/types.rs:50`
- `Language` (enum) — `src/types.rs:63`
- `Complexity` (enum) — `src/types.rs:75`
- `Priority` (enum) — `src/types.rs:86`
- `as_ordinal` (function) — `src/types.rs:141`
- `InvariantResult` (struct) — `src/types.rs:157`
- `TaskInput` (struct) — `src/types.rs:170`
- `Constraints` (struct) — `src/types.rs:205`
- `RunningTask` (struct) — `src/types.rs:231`
- `PredictionResult` (struct) — `src/types.rs:246`

## Modules

_12 files, 46 public symbols, 9 internal imports._

- `src/error.rs` (rust)
- `src/invariant/mod.rs` (rust)
- `src/invariant/rules.rs` (rust)
- `src/lib.rs` (rust)
- `src/obs.rs` (rust)
- `src/policy/decision_tree.rs` (rust)
- `src/policy/engine.rs` (rust)
- `src/policy/mod.rs` (rust)
- `src/traits.rs` (rust)
- `src/types.rs` (rust)
- `tests/emit_contract.rs` (rust)
- `tests/fixtures_contract.rs` (rust)

## Inbound references

- from [[arbiter-cli]]:
  - `benches/routing.rs:14` → `policy::decision_tree::DecisionTree`
  - `benches/routing.rs:15` → `types::*`
  - `src/main.rs:17` → `policy::decision_tree::DecisionTree`
  - `src/main.rs:18` → `types::*`
- from [[arbiter-mcp]]:
  - `src/features.rs:8` → `types::Constraints`
  - `src/features.rs:8` → `types::TaskInput`
  - `src/features.rs:301` → `types::Complexity`
  - `src/features.rs:301` → `types::Constraints`
  - `src/features.rs:301` → `types::Language`
  - `src/features.rs:301` → `types::Priority`
  - `src/features.rs:301` → `types::RunningTask`
  - `src/features.rs:301` → `types::TaskInput`
  - `src/features.rs:301` → `types::TaskType`
  - `src/main.rs:12` → `policy::decision_tree::DecisionTree`
  - `src/server.rs:15` → `policy::decision_tree::DecisionTree`
  - `src/server.rs:16` → `types::Constraints`
  - `src/server.rs:16` → `types::TaskInput`
  - `src/tools/route_task.rs:14` → `invariant::rules::AgentContext`
  - `src/tools/route_task.rs:14` → `invariant::rules::InvariantThresholds`
  - `src/tools/route_task.rs:14` → `invariant::rules::SystemContext`
  - `src/tools/route_task.rs:14` → `invariant::rules::check_all_invariants`
  - `src/tools/route_task.rs:14` → `invariant::rules::has_critical_failure`
  - `src/tools/route_task.rs:17` → `policy::decision_tree::DecisionTree`
  - `src/tools/route_task.rs:18` → `policy::engine::evaluate_for_agents`
  - `src/tools/route_task.rs:19` → `types::AgentAction`
  - `src/tools/route_task.rs:19` → `types::AgentState`
  - `src/tools/route_task.rs:19` → `types::Constraints`
  - `src/tools/route_task.rs:19` → `types::InvariantResult`
  - `src/tools/route_task.rs:19` → `types::TaskInput`
  - `src/tools/route_task.rs:457` → `types::PredictionResult`
  - `src/tools/route_task.rs:587` → `types::*`
  - `src/watcher.rs:19` → `policy::decision_tree::DecisionTree`
  - `tests/golden_tests.rs:15` → `policy::decision_tree::DecisionTree`
  - `tests/integration.rs:11` → `policy::decision_tree::DecisionTree`
  - `tests/integration.rs:12` → `types::*`

## Outbound references

_None._

## Outbound edges

_None._

## Inbound edges

- ← [[arbiter-cli]] · `package_dep` · `arbiter-core`
- ← [[arbiter-mcp]] · `package_dep` · `arbiter-core`

## Recent changes (last 5)

- snapshot 41 (2026-05-27T10:39:37Z): project attrs_changed (attrs_changed)
- snapshot 39 (2026-05-27T10:18:26Z): project added (added)

## Drift findings

_None._
