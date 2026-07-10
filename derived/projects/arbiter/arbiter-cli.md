<!-- prograph:generated -->

---
indexed_at: "2026-07-10T12:31:55Z"
kind: rust
name: arbiter-cli
parent: arbiter
prograph: project
root: ./arbiter/arbiter-cli
snapshot: 4
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

_3 files, 0 public symbols, 0 internal imports._

- `benches/routing.rs` (rust)
- `src/main.rs` (rust)
- `tests/catalog_cli.rs` (rust)

## Inbound references

_None._

## Outbound references

- to [[arbiter-core]]:
  - `src/main.rs:19` → `catalog::Catalog`
  - `src/main.rs:19` → `catalog::Severity`
  - `src/main.rs:19` → `catalog::self`
  - `benches/routing.rs:14` → `policy::decision_tree::DecisionTree`
  - `src/main.rs:20` → `policy::decision_tree::DecisionTree`
  - `benches/routing.rs:15` → `types::*`
  - `src/main.rs:21` → `types::*`
- to [[arbiter-mcp]]:
  - `benches/routing.rs:17` → `agents::AgentRegistry`
  - `src/main.rs:23` → `agents::AgentRegistry`
  - `benches/routing.rs:18` → `config::*`
  - `src/main.rs:24` → `config::*`
  - `benches/routing.rs:19` → `db::Database`
  - `src/main.rs:25` → `db::Database`
  - `src/main.rs:25` → `db::DecisionRecord`
  - `src/main.rs:25` → `db::OutcomeRecord`
  - `benches/routing.rs:20` → `metrics::Metrics`
  - `benches/routing.rs:21` → `tools::route_task`
  - `src/main.rs:26` → `tools::route_task`

## Outbound edges

- → [[arbiter-core]] · `package_dep` · `arbiter-core`
- → [[arbiter-mcp]] · `package_dep` · `arbiter-mcp`

## Inbound edges

_None._

## Recent changes (last 5)

- snapshot 1 (2026-07-07T16:11:23Z): project added (added)

## Drift findings

_None._
