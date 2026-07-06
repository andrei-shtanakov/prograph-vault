<!-- prograph:generated -->

---
indexed_at: "2026-05-27T12:45:37Z"
kind: rust
name: arbiter-cli
parent: arbiter
prograph: project
root: ./arbiter/arbiter-cli
snapshot: 48
---

# arbiter-cli

## Manifest

- declared package: `arbiter-cli`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

_None._

### Public symbols

_None._

## Modules

_2 files, 0 public symbols, 0 internal imports._

- `benches/routing.rs` (rust)
- `src/main.rs` (rust)

## Inbound references

_None._

## Outbound references

- to [[arbiter-core]]:
  - `benches/routing.rs:14` → `policy::decision_tree::DecisionTree`
  - `src/main.rs:17` → `policy::decision_tree::DecisionTree`
  - `benches/routing.rs:15` → `types::*`
  - `src/main.rs:18` → `types::*`
- to [[arbiter-mcp]]:
  - `benches/routing.rs:17` → `agents::AgentRegistry`
  - `src/main.rs:20` → `agents::AgentRegistry`
  - `benches/routing.rs:18` → `config::*`
  - `src/main.rs:21` → `config::*`
  - `benches/routing.rs:19` → `db::Database`
  - `src/main.rs:22` → `db::Database`
  - `src/main.rs:22` → `db::DecisionRecord`
  - `src/main.rs:22` → `db::OutcomeRecord`
  - `benches/routing.rs:20` → `metrics::Metrics`
  - `benches/routing.rs:21` → `tools::route_task`
  - `src/main.rs:23` → `tools::route_task`

## Outbound edges

- → [[arbiter-core]] · `package_dep` · `arbiter-core`
- → [[arbiter-mcp]] · `package_dep` · `arbiter-mcp`

## Inbound edges

_None._

## Recent changes (last 5)

- snapshot 41 (2026-05-27T10:39:37Z): project attrs_changed (attrs_changed)
- snapshot 39 (2026-05-27T10:18:26Z): project added (added)

## Drift findings

_None._
