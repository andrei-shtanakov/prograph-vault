<!-- prograph:generated -->

---
indexed_at: "2026-07-10T17:42:43Z"
kind: mixed
name: arbiter
prograph: project
root: ./arbiter
snapshot: 6
---

# arbiter

> An MCP server that decides which coding agent (Claude Code, Codex CLI, Aider) should handle a given task, based on Decision Tree inference, safety invariants, and historical performance data.

## Description

An MCP server that decides which coding agent (Claude Code, Codex CLI, Aider) should handle a given task, based on Decision Tree inference, safety invariants, and historical performance data.

## Quick Start

### Prerequisites

- Rust 1.75+ (with `cargo`)
- Python 3.11+ (with [`uv`](https://github.com/astral-sh/uv))

### Build

```bash
# Build entire workspace (release mode)
cargo build --release

# Verify tests pass
cargo test
```

### Generate Decision Tree

```bash
uv run python scripts/bootstrap_agent_tree.py
```

This creates `models/agent_policy_tree.json` from expert rules.

### Run the MCP Server

```bash
cargo run --release --bin arbiter-mcp
```

The server reads JSON-RPC 2.0 from stdin and writes responses to stdout. All logs go to stderr.

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--tree <PATH>` | `models/agent_policy_tree.json` | Decision tree JSON file |
| `--config <DIR>` | `config/` | Config directory (agents.toml, invariants.toml) |
| `--db <PATH>` | `arbiter.db` | SQLite database path |
| `--log-level <LEVEL>` | `info` | Log level: trace, debug, info, warn, error |

If the decision tree file is missing or invalid, the server starts in **degraded round-robin mode** and still accepts requests.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              Agent Orchestrator (Python)             │
│         Task Queue → Dependency Resolver → Spawner  │
│                        │                            │
│                   MCP Client                        │
└────────────────────────┬────────────────────────────┘
                         │ JSON-RPC 2.0 (stdio)
┌────────────────────────▼────────────────────────────┐
│              Arbiter (Rust MCP Server)               │
│                                                      │
│  route_task → Feature Builder → DT Inference         │
│                                  → Invariant Check   │
│                                  → Age…

## Manifest

- declared package: `arbiter` version `0.1.0`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

- [[https---all_ai_orchestrators-observability-contract-v1]] (json_schema) — `arbiter-core/tests/contract/log-schema.json` — `https://all_ai_orchestrators/observability-contract/v1`
- [[https---github-com-andrei-shtanakov-maestro-benchmark-contract-report_benchmark-v1-schema-json]] (json_schema) — `arbiter-mcp/tests/contract/report_benchmark-v1.schema.json` — `https://github.com/andrei-shtanakov/maestro/benchmark-contract/report_benchmark-v1.schema.json`

### Public symbols

- `init_logging` (function) — `orchestrator/_vendor/obs.py:147`
- `get_logger` (function) — `orchestrator/_vendor/obs.py:204`
- `Span` (class) — `orchestrator/_vendor/obs.py:208`
- `child_env` (function) — `orchestrator/_vendor/obs.py:257`
- `current_trace_id` (function) — `orchestrator/_vendor/obs.py:273`
- `current_span_id` (function) — `orchestrator/_vendor/obs.py:277`
- `current_pipeline_id` (function) — `orchestrator/_vendor/obs.py:281`
- `logger` (const) — `orchestrator/arbiter_client.py:21`
- `ArbiterError` (class) — `orchestrator/arbiter_client.py:24`
- `ArbiterConnectionError` (class) — `orchestrator/arbiter_client.py:28`
- `ArbiterProtocolError` (class) — `orchestrator/arbiter_client.py:32`
- `ArbiterClient` (class) — `orchestrator/arbiter_client.py:55`
- `PROJECT_ROOT` (const) — `orchestrator/tests/test_arbiter_integration.py:26`
- `BINARY_PATH` (const) — `orchestrator/tests/test_arbiter_integration.py:27`
- `TREE_PATH` (const) — `orchestrator/tests/test_arbiter_integration.py:28`
- `CONFIG_DIR` (const) — `orchestrator/tests/test_arbiter_integration.py:29`
- `test_fallback_scheduler_round_robin` (function) — `orchestrator/tests/test_arbiter_integration.py:295`
- `test_fallback_scheduler_reset` (function) — `orchestrator/tests/test_arbiter_integration.py:309`
- `test_fallback_scheduler_custom_agents` (function) — `orchestrator/tests/test_arbiter_integration.py:318`
- `PROJECT_ROOT` (const) — `orchestrator/tests/test_e2e_smoke.py:26`
- `TREE_PATH` (const) — `orchestrator/tests/test_e2e_smoke.py:32`
- `CONFIG_DIR` (const) — `orchestrator/tests/test_e2e_smoke.py:33`
- `REVIEW_TASK` (const) — `scripts/ab_bench_rerank.py:26`
- `run_once` (function) — `scripts/ab_bench_rerank.py:34`
- `main_async` (function) — `scripts/ab_bench_rerank.py:56`
- `main` (function) — `scripts/ab_bench_rerank.py:63`
- `FEATURE_NAMES` (const) — `scripts/bootstrap_agent_tree.py:32`
- `AGENTS` (const) — `scripts/bootstrap_agent_tree.py:58`
- `AGENT_IDX` (const) — `scripts/bootstrap_agent_tree.py:64`
- `TASK_FEATURE` (const) — `scripts/bootstrap_agent_tree.py:67`
- `TASK_BUGFIX` (const) — `scripts/bootstrap_agent_tree.py:68`
- `TASK_REFACTOR` (const) — `scripts/bootstrap_agent_tree.py:69`
- `TASK_TEST` (const) — `scripts/bootstrap_agent_tree.py:70`
- `TASK_DOCS` (const) — `scripts/bootstrap_agent_tree.py:71`
- `TASK_REVIEW` (const) — `scripts/bootstrap_agent_tree.py:72`
- `TASK_RESEARCH` (const) — `scripts/bootstrap_agent_tree.py:73`
- `COMP_TRIVIAL` (const) — `scripts/bootstrap_agent_tree.py:76`
- `COMP_SIMPLE` (const) — `scripts/bootstrap_agent_tree.py:77`
- `COMP_MODERATE` (const) — `scripts/bootstrap_agent_tree.py:78`
- `COMP_COMPLEX` (const) — `scripts/bootstrap_agent_tree.py:79`
- `COMP_CRITICAL` (const) — `scripts/bootstrap_agent_tree.py:80`
- `LANG_PYTHON` (const) — `scripts/bootstrap_agent_tree.py:83`
- `LANG_RUST` (const) — `scripts/bootstrap_agent_tree.py:84`
- `LANG_TYPESCRIPT` (const) — `scripts/bootstrap_agent_tree.py:85`
- `LANG_GO` (const) — `scripts/bootstrap_agent_tree.py:86`
- `LANG_MIXED` (const) — `scripts/bootstrap_agent_tree.py:87`
- `LANG_OTHER` (const) — `scripts/bootstrap_agent_tree.py:88`
- `PRI_LOW` (const) — `scripts/bootstrap_agent_tree.py:91`
- `PRI_NORMAL` (const) — `scripts/bootstrap_agent_tree.py:92`
- `PRI_HIGH` (const) — `scripts/bootstrap_agent_tree.py:93`
- `PRI_URGENT` (const) — `scripts/bootstrap_agent_tree.py:94`
- `make_base_features` (function) — `scripts/bootstrap_agent_tree.py:102`
- `generate_expert_examples` (function) — `scripts/bootstrap_agent_tree.py:153`
- `inject_noise` (function) — `scripts/bootstrap_agent_tree.py:399`
- `export_tree_json` (function) — `scripts/bootstrap_agent_tree.py:429`
- `extract_from_db` (function) — `scripts/bootstrap_agent_tree.py:482`
- `train_and_export` (function) — `scripts/bootstrap_agent_tree.py:521`
- `main` (function) — `scripts/bootstrap_agent_tree.py:646`
- `SUITE_RE` (const) — `scripts/check_routable_gate.py:28`
- `ISO_DATE_RE` (const) — `scripts/check_routable_gate.py:29`
- `REQUIRED_BENCH_KEYS` (const) — `scripts/check_routable_gate.py:30`
- `DATE_FRESHNESS_DAYS` (const) — `scripts/check_routable_gate.py:31`
- `DEFAULT_EPS` (const) — `scripts/check_routable_gate.py:32`
- `GateInputError` (class) — `scripts/check_routable_gate.py:35`
- `load_catalog` (function) — `scripts/check_routable_gate.py:39`
- `agent_id` (function) — `scripts/check_routable_gate.py:50`
- `agents_map` (function) — `scripts/check_routable_gate.py:55`
- `validate_bench` (function) — `scripts/check_routable_gate.py:94`
- `run_verify` (function) — `scripts/check_routable_gate.py:195`
- `run_gate` (function) — `scripts/check_routable_gate.py:311`
- `main` (function) — `scripts/check_routable_gate.py:354`
- `AGENTS` (const) — `scripts/eval_tree.py:26`
- `AGENT_COSTS` (const) — `scripts/eval_tree.py:28`
- `F_TASK_TYPE` (const) — `scripts/eval_tree.py:35`
- `F_LANGUAGE` (const) — `scripts/eval_tree.py:36`
- `F_COMPLEXITY` (const) — `scripts/eval_tree.py:37`
- `F_PRIORITY` (const) — `scripts/eval_tree.py:38`
- `F_SCOPE_SIZE` (const) — `scripts/eval_tree.py:39`
- `F_EST_TOKENS` (const) — `scripts/eval_tree.py:40`
- `F_HAS_DEPS` (const) — `scripts/eval_tree.py:41`
- `F_REQ_INTERNET` (const) — `scripts/eval_tree.py:42`
- `F_SLA_MINUTES` (const) — `scripts/eval_tree.py:43`
- `F_SUCCESS_RATE` (const) — `scripts/eval_tree.py:44`
- `F_AVAIL_SLOTS` (const) — `scripts/eval_tree.py:45`
- `F_RUNNING_TASKS` (const) — `scripts/eval_tree.py:46`
- `F_AVG_DURATION` (const) — `scripts/eval_tree.py:47`
- `F_AVG_COST` (const) — `scripts/eval_tree.py:48`
- `F_RECENT_FAILURES` (const) — `scripts/eval_tree.py:49`
- `F_SUPPORTS_TYPE` (const) — `scripts/eval_tree.py:50`
- `F_SUPPORTS_LANG` (const) — `scripts/eval_tree.py:51`
- `F_TOTAL_RUNNING` (const) — `scripts/eval_tree.py:52`
- `F_TOTAL_PENDING` (const) — `scripts/eval_tree.py:53`
- `F_BUDGET_REMAINING` (const) — `scripts/eval_tree.py:54`
- `F_TIME_OF_DAY` (const) — `scripts/eval_tree.py:55`
- `F_SCOPE_CONFLICTS` (const) — `scripts/eval_tree.py:56`
- `TASK_FEATURE` (const) — `scripts/eval_tree.py:59`
- `TASK_BUGFIX` (const) — `scripts/eval_tree.py:60`
- `TASK_REFACTOR` (const) — `scripts/eval_tree.py:61`
- `TASK_TEST` (const) — `scripts/eval_tree.py:62`
- `TASK_DOCS` (const) — `scripts/eval_tree.py:63`
- `TASK_REVIEW` (const) — `scripts/eval_tree.py:64`
- `TASK_RESEARCH` (const) — `scripts/eval_tree.py:65`
- `COMP_TRIVIAL` (const) — `scripts/eval_tree.py:68`
- `COMP_SIMPLE` (const) — `scripts/eval_tree.py:69`
- `COMP_MODERATE` (const) — `scripts/eval_tree.py:70`
- `COMP_COMPLEX` (const) — `scripts/eval_tree.py:71`
- `COMP_CRITICAL` (const) — `scripts/eval_tree.py:72`
- `LANG_PYTHON` (const) — `scripts/eval_tree.py:75`
- `LANG_RUST` (const) — `scripts/eval_tree.py:76`
- `LANG_TYPESCRIPT` (const) — `scripts/eval_tree.py:77`
- `LANG_GO` (const) — `scripts/eval_tree.py:78`
- `LANG_MIXED` (const) — `scripts/eval_tree.py:79`
- `LANG_OTHER` (const) — `scripts/eval_tree.py:80`
- `EXPERT_RULES` (const) — `scripts/eval_tree.py:101`
- `generate_benchmark` (function) — `scripts/eval_tree.py:244`
- `load_tree` (function) — `scripts/eval_tree.py:284`
- `predict_tree` (function) — `scripts/eval_tree.py:290`
- `strategy_decision_tree` (function) — `scripts/eval_tree.py:314`
- `strategy_round_robin` (function) — `scripts/eval_tree.py:322`
- `strategy_always_claude` (function) — `scripts/eval_tree.py:327`
- `evaluate_strategy` (function) — `scripts/eval_tree.py:350`
- `print_results` (function) — `scripts/eval_tree.py:373`
- `main` (function) — `scripts/eval_tree.py:396`
- `REPO_ROOT` (const) — `scripts/gen_agents_scaffold.py:40`
- `DEFAULT_CATALOG` (const) — `scripts/gen_agents_scaffold.py:41`
- `DEFAULT_AGENTS_TOML` (const) — `scripts/gen_agents_scaffold.py:42`
- `load_routable_ids` (function) — `scripts/gen_agents_scaffold.py:68`
- `split_sections` (function) — `scripts/gen_agents_scaffold.py:80`
- `render_stub` (function) — `scripts/gen_agents_scaffold.py:106`
- `reconcile` (function) — `scripts/gen_agents_scaffold.py:124`
- `render_scaffold` (function) — `scripts/gen_agents_scaffold.py:143`
- `main` (function) — `scripts/gen_agents_scaffold.py:162`
- `ingest` (function) — `scripts/ingest_benchmark_payloads.py:31`
- `main` (function) — `scripts/ingest_benchmark_payloads.py:74`
- `ExecutorState` (class) — `spec/executor.py:93`
- `build_task_prompt` (function) — `spec/executor.py:208`
- `pre_start_hook` (function) — `spec/executor.py:300`
- `post_done_hook` (function) — `spec/executor.py:326`
- `execute_task` (function) — `spec/executor.py:378`
- `run_with_retries` (function) — `spec/executor.py:481`
- `cmd_run` (function) — `spec/executor.py:510`
- `cmd_status` (function) — `spec/executor.py:570`
- `cmd_retry` (function) — `spec/executor.py:604`
- `cmd_logs` (function) — `spec/executor.py:626`
- `cmd_reset` (function) — `spec/executor.py:643`
- `main` (function) — `spec/executor.py:658`
- `TASKS_FILE` (const) — `spec/task.py:30`
- `HISTORY_FILE` (const) — `spec/task.py:31`
- `TASK_HEADER` (const) — `spec/task.py:34`
- `TASK_META` (const) — `spec/task.py:35`
- `CHECKLIST_ITEM` (const) — `spec/task.py:36`
- `TRACES_TO` (const) — `spec/task.py:37`
- `DEPENDS_ON` (const) — `spec/task.py:38`
- `BLOCKS` (const) — `spec/task.py:39`
- `ESTIMATE` (const) — `spec/task.py:40`
- `STATUS_EMOJI` (const) — `spec/task.py:42`
- `STATUS_FROM_EMOJI` (const) — `spec/task.py:49`
- `PRIORITY_EMOJI` (const) — `spec/task.py:51`
- `PRIORITY_FROM_EMOJI` (const) — `spec/task.py:58`
- `parse_tasks` (function) — `spec/task.py:87`
- `update_task_status` (function) — `spec/task.py:202`
- `update_checklist_item` (function) — `spec/task.py:239`
- `log_change` (function) — `spec/task.py:272`
- `get_task_by_id` (function) — `spec/task.py:280`
- `resolve_dependencies` (function) — `spec/task.py:290`
- `get_next_tasks` (function) — `spec/task.py:303`
- `cmd_list` (function) — `spec/task.py:314`
- `cmd_show` (function) — `spec/task.py:360`
- `cmd_start` (function) — `spec/task.py:395`
- `cmd_done` (function) — `spec/task.py:420`
- `cmd_block` (function) — `spec/task.py:450`
- `cmd_check` (function) — `spec/task.py:463`
- `cmd_stats` (function) — `spec/task.py:485`
- `cmd_next` (function) — `spec/task.py:539`
- `cmd_graph` (function) — `spec/task.py:565`
- `cmd_export_gh` (function) — `spec/task.py:599`
- `main` (function) — `spec/task.py:633`
- `TREE_PATH` (const) — `tests/test_bootstrap_tree.py:11`
- `test_bootstrap_script_runs` (function) — `tests/test_bootstrap_tree.py:14`
- `test_tree_json_exists` (function) — `tests/test_bootstrap_tree.py:32`
- `test_tree_json_valid_format` (function) — `tests/test_bootstrap_tree.py:39`
- `test_tree_depth_constraint` (function) — `tests/test_bootstrap_tree.py:62`
- `test_tree_node_count_constraint` (function) — `tests/test_bootstrap_tree.py:77`
- `test_tree_node_structure` (function) — `tests/test_bootstrap_tree.py:84`
- `test_bootstrap_accuracy_above_95` (function) — `tests/test_bootstrap_tree.py:98`
- `test_bootstrap_generates_enough_examples` (function) — `tests/test_bootstrap_tree.py:119`
- `test_bootstrap_deterministic` (function) — `tests/test_bootstrap_tree.py:130`
- `CATALOG` (const) — `tests/test_gen_agents_scaffold.py:24`
- `AGENTS_TOML` (const) — `tests/test_gen_agents_scaffold.py:59`
- `test_load_routable_ids_ordered_and_filtered` (function) — `tests/test_gen_agents_scaffold.py:74`
- `test_split_sections_marks_fused_ignores_bare` (function) — `tests/test_gen_agents_scaffold.py:80`
- `test_render_stub_is_keys_only_no_invented_policy` (function) — `tests/test_gen_agents_scaffold.py:90`
- `test_reconcile_partitions_kept_new_stale` (function) — `tests/test_gen_agents_scaffold.py:100`
- `test_reconcile_preserves_known_section_verbatim` (function) — `tests/test_gen_agents_scaffold.py:110`
- `test_script_runs_against_vendored_catalog` (function) — `tests/test_gen_agents_scaffold.py:122`
- `VALID_BENCH` (const) — `tests/test_routable_gate.py:27`
- `make_entry` (function) — `tests/test_routable_gate.py:36`
- `bench_with` (function) — `tests/test_routable_gate.py:48`
- `bench_without` (function) — `tests/test_routable_gate.py:54`
- `TestValidateBench` (class) — `tests/test_routable_gate.py:60`
- `TestCatalogLoading` (class) — `tests/test_routable_gate.py:114`
- `CATALOG_HEADER` (const) — `tests/test_routable_gate.py:152`
- `AGENT_NOT_ROUTABLE` (const) — `tests/test_routable_gate.py:163`
- `AGENT_ROUTABLE_NO_BENCH` (const) — `tests/test_routable_gate.py:171`
- `BENCH_LINE` (const) — `tests/test_routable_gate.py:179`
- `AGENT_ROUTABLE_WITH_BENCH` (const) — `tests/test_routable_gate.py:184`
- `write_pair` (function) — `tests/test_routable_gate.py:187`
- `gate` (function) — `tests/test_routable_gate.py:195`
- `TestGateRuleA` (class) — `tests/test_routable_gate.py:200`
- `TestGateRuleB` (class) — `tests/test_routable_gate.py:240`
- `TestGateExitCodes` (class) — `tests/test_routable_gate.py:271`
- `BENCHMARK_RUNS_SCHEMA` (const) — `tests/test_routable_gate.py:303`
- `make_db` (function) — `tests/test_routable_gate.py:323`
- `write_catalog` (function) — `tests/test_routable_gate.py:352`
- `verify` (function) — `tests/test_routable_gate.py:358`
- `R1_R2` (const) — `tests/test_routable_gate.py:370`
- `TestVerify` (class) — `tests/test_routable_gate.py:373`
- `TestVerifyExitCodes` (class) — `tests/test_routable_gate.py:450`
- `test_cargo_build` (function) — `tests/test_workspace.py:6`
- `test_cargo_test` (function) — `tests/test_workspace.py:17`
- `test_cargo_clippy` (function) — `tests/test_workspace.py:28`
- `test_cargo_fmt` (function) — `tests/test_workspace.py:39`

## Modules

_21 files, 222 public symbols, 0 internal imports._

- `orchestrator/__init__.py` (python)
- `orchestrator/_vendor/__init__.py` (python)
- `orchestrator/_vendor/obs.py` (python)
- `orchestrator/arbiter_client.py` (python)
- `orchestrator/tests/__init__.py` (python)
- `orchestrator/tests/test_arbiter_integration.py` (python)
- `orchestrator/tests/test_e2e_smoke.py` (python)
- `orchestrator/types.py` (python)
- `scripts/ab_bench_rerank.py` (python)
- `scripts/bootstrap_agent_tree.py` (python)
- `scripts/check_routable_gate.py` (python)
- `scripts/eval_tree.py` (python)
- `scripts/gen_agents_scaffold.py` (python)
- `scripts/ingest_benchmark_payloads.py` (python)
- `spec/executor.py` (python)
- `spec/task.py` (python)
- `tests/__init__.py` (python)
- `tests/test_bootstrap_tree.py` (python)
- `tests/test_gen_agents_scaffold.py` (python)
- `tests/test_routable_gate.py` (python)
- `tests/test_workspace.py` (python)

## Inbound references

_None._

## Outbound references

_None._

## Outbound edges

- ↔ [[https---all_ai_orchestrators-observability-contract-v1]] · `contract_link` · `json_schema`
- ↔ [[https---github-com-andrei-shtanakov-maestro-benchmark-contract-report_benchmark-v1-schema-json]] · `contract_link` · `json_schema`
- → [[arbiter-mcp]] · `mcp_call` · tool `report_outcome`
- → [[arbiter-mcp]] · `mcp_call` · tool `get_agent_status`
- → [[arbiter-mcp]] · `mcp_call` · tool `route_task`
- → [[arbiter-mcp]] · `mcp_call` · tool `report_benchmark`
- → [[spec-runner]] · `package_dep` · `spec-runner` `>=0.1.1`

## Inbound edges

- ← [[dispatcher]] · `declared` · read `arbiter/logs`
- ← [[dispatcher]] · `declared` · read `arbiter/config/agents.toml`
- ← [[dispatcher]] · `declared` · read `arbiter/arbiter.db`
- ← [[dispatcher]] · `declared` · read `arbiter/config/invariants.toml`

## Recent changes (last 5)

- snapshot 1 (2026-07-07T16:11:23Z): project added (added)

## Drift findings

_None._
