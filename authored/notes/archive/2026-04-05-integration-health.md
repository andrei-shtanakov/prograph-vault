---
title: Integration health (2026-04-05 snapshot)
type: note
status: archived
owner: Andrei
updated: 2026-07-08
archived: 2026-07-08
reason: >
  Point-in-time integration audit dated 2026-04-05; core claims are now stale. It states
  "Maestro→Arbiter: NOT IMPLEMENTED, 0 lines" and "spec-runner version not pinned in Maestro",
  but Maestro now has maestro/coordination/arbiter_client.py (MCP handshake + protocolVersion 1.1.0
  negotiation) and pins spec-runner via SPEC_RUNNER_REQUIRED_VERSION + contract tests. It also uses
  the old `executor/` name for spec-runner and covers only ~4 repos (now 14).
superseded_by: >
  authored/registry/registry.md (integration map), authored/notes/ecosystem-roadmap.md,
  authored/notes/status/2026-07-08-1228-status.md; live structure in derived/graph/ (prograph).
---

# Integration health: the real state of the links

> **ARCHIVED 2026-07-08 — historical snapshot, do not treat as current.** See `superseded_by` in the
> frontmatter. Kept for decision history (KB rule §1.5: nothing is deleted).

**Date:** 2026-04-05

## TL;DR

1. **Maestro → Arbiter: NOT IMPLEMENTED.** In Maestro's code there are 0 lines related to Arbiter. The agent is chosen statically from a YAML config (`agent_type: claude_code`). Arbiter has a ready Python client (`orchestrator/arbiter_client.py`), but it is autonomous. Maestro works fully without Arbiter.
2. **Maestro → ATP: NOT IMPLEMENTED.** Maestro has its own validation (`validation_cmd` → shell subprocess), but it does not use ATP. ATP provides an SDK and an `sdk_adapter` for in-process integration — the technical capability exists, the implementation does not.
3. **Arbiter → ATP: NOT IMPLEMENTED.** There is a plan in the roadmap (ECO-3) and an idea of eval-driven tree validation in SUGGESTIONS.md, but no code. ATP guardrails are "inspired by" Arbiter invariants — a back-reference, not an integration.
4. **spec-runner ↔ Maestro: WORKING.** The only real integration. Maestro runs spec-runner as a subprocess in git worktrees. The contract is informal — there is no shared schema, mapping goes through `executor.config.yaml`.
5. **Dependencies: COMPATIBLE.** All projects are on Python 3.12+, Pydantic v2, compatible versions of FastAPI/aiosqlite. There are no conflicts when installing into a single environment.

---

## Integration-health summary table

| Link | Status | Tests | Risk | Comment |
|--------|--------|-------|------|-------------|
| **Maestro → Arbiter (route_task)** | 🔴 not implemented | ❌ none | 🔴 High | Arbiter ready, Maestro — 0 lines of code. Documentation is misleading |
| **Maestro → Arbiter (report_outcome)** | 🔴 not implemented | ❌ none | 🔴 High | Data for the report exists in Maestro, but is not sent |
| **Maestro → Arbiter (get_agent_status)** | 🔴 not implemented | ❌ none | 🟡 Medium | Advisory, does not block operation |
| **Maestro → ATP (verify)** | 🔴 not implemented | ❌ none | 🟡 Medium | ATP SDK ready, Maestro validator.py can be extended |
| **Arbiter → ATP (eval)** | 🔴 not implemented | ❌ none | 🟡 Medium | Only in the roadmap (ECO-3) |
| **Maestro → spec-runner** | 🟢 working | 🟡 partial | 🟡 Medium | The only working integration. The contract is informal |
| **Shared dependencies** | 🟢 compatible | n/a | 🟢 Low | Python 3.12+, Pydantic v2, no conflicts |

---

## 1. Maestro → Arbiter

### 1.1. Is there an ArbiterClient in Maestro?

**NO.** `grep -ri "arbiter\|route_task\|ArbiterClient" Maestro/maestro/` → 0 results in the source code.

ArbiterClient exists, but **in the Arbiter project**, not in Maestro:
- `arbiter/orchestrator/arbiter_client.py:51-131` — a full-fledged MCP client
- Methods: `route_task()`, `report_outcome()`, `get_agent_status()`
- Works over stdin/stdout JSON-RPC 2.0 with the Arbiter subprocess

### 1.2. How does Maestro choose an agent?

**Statically from a YAML config.** No dynamic selection:

```python
# Maestro/maestro/scheduler.py:437-440
spawner = self._spawners.get(task.agent_type.value)
if spawner is None:
    msg = f"No spawner available for agent type '{task.agent_type}'"
    raise SchedulerError(msg)
```

Chain: `tasks.yaml` (agent_type: claude_code) → `models.py:AgentType` (enum: CLAUDE_CODE/CODEX/AIDER/ANNOUNCE) → `scheduler.py` (spawner lookup) → `spawners/` (the concrete spawner).

No analysis of complexity, language, or task scope. No call to an external service.

### 1.3. What happens if you run Maestro without Arbiter?

**Nothing.** Maestro works fully autonomously:
- Arbiter is not listed in `pyproject.toml`
- There are no try-except blocks connecting to Arbiter
- There is no fallback logic (it is not needed — Arbiter is not called)
- All tasks are routed by `task.agent_type` from the config

### 1.4. Integration tests for the link

**NO.** In neither project:
- `Maestro/tests/` — 0 files mentioning Arbiter
- `arbiter/tests/` — 0 files mentioning Maestro

Arbiter has tests of its own client (`orchestrator/tests/test_arbiter_integration.py:1-287`), but they test ArbiterClient in isolation — PT-01..PT-07: handshake, route, report, error handling, crash recovery.

### 1.5. Incompatibilities for a future integration

| Problem | Maestro | Arbiter | Criticality |
|----------|---------|---------|-------------|
| Agent ID | `codex` | `codex_cli` | 🔴 Routing error |
| Priority | `int (-100..100)` | `enum (low/normal/high/urgent)` | 🟡 Mapping needed |
| No `task_type` | — | required enum (7 values) | 🔴 Arbiter rejects the request |
| No `language` | — | required enum (6 values) | 🔴 Arbiter rejects the request |
| No `complexity` | — | required enum (5 values) | 🔴 Arbiter rejects the request |
| `announce` agent | Present | Not in agents.toml | 🟡 Needs to be bypassed |

### 1.6. What exists for the implementation

- ✅ Arbiter: fully ready, MCP server + Python client + integration tests
- ✅ Maestro: there is an integration plan in `_cowork_output/05-architecture-improvements.md:265-357` — it proposes a `RoutingStrategy` ABC with `ArbiterRouting` and graceful fallback
- ❌ Maestro: not a single line of code for the integration

---

## 2. Maestro → ATP

### 2.1. Post-task validation via ATP

**NO.** `grep -ri "atp\|benchmark\|evaluate" Maestro/maestro/` → 0 relevant results.

Maestro has its **own** validation system that works through shell commands:

- `Maestro/maestro/validator.py:96-299` — the `Validator` class
- `Maestro/maestro/scheduler.py:613-639` — post-validation flow
- `Maestro/maestro/models.py:108-110` — the `validation_cmd: str | None` field

Flow: Task DONE → checks `task.validation_cmd` → subprocess → exit code 0 = success.

### 2.2. Mentions in the configs

In the YAML examples, validation is shell commands:

```yaml
# Maestro/examples/tasks.yaml
- id: create-api
  validation_cmd: "uv run pytest tests/test_api.py"
- id: write-tests
  validation_cmd: "uv run pytest --tb=short"
```

There are no mentions of ATP, atp run, atp evaluate.

### 2.3. Can Maestro run an ATP suite?

**Technically — yes, in three ways:**

| Way | Complexity | Changes in Maestro |
|--------|-----------|---------------------|
| `validation_cmd: "atp run suite.yaml"` | Low | 0 lines (config only) |
| Programmatic integration via `atp.sdk.arun()` | Medium | ~50 lines in scheduler.py |
| ATP SDK Adapter (pull model) | High | ~200 lines, architectural changes |

ATP provides ready tools:
- `atp-platform/atp/sdk/__init__.py` — Python SDK (`run()`, `arun()`, `evaluate()`, `score()`)
- `atp-platform/atp/adapters/sdk_adapter.py` — in-process adapter (pull model)
- `atp-platform/atp/adapters/registry.py` — 12+ adapters including CLI

### 2.4. Integration tests

**NO.** Neither project has tests for this link.

---

## 3. Arbiter → ATP

### 3.1. Testing the quality of Arbiter's decisions

**NOT IMPLEMENTED.** Only plans exist:

- `arbiter/_cowork_output/07-roadmap.md:17` — "ECO-3. ATP integration: testing the quality of decisions"
- `arbiter/SUGGESTIONS.md:70-83` — section 2.6 "Eval-driven tree validation": proposes A/B testing (DT routing vs random vs always-best-agent), ~200 LOC in `scripts/eval_routing.py`

### 3.2. ATP test suites for Arbiter

**NO.** In `atp-platform/` there are no YAML files mentioning arbiter, route_task, agent_selection.

### 3.3. Feedback ATP → Arbiter

The only link is **inspiration**, not integration:

```python
# atp-platform/atp/evaluators/guardrails.py:1-3
"""Pre-evaluation guardrails inspired by arbiter's invariant rules.
Run checks before each evaluator to skip wasteful evaluations early."""
```

ATP guardrails (3 rules: response_not_empty, timeout_not_exceeded, within_budget) are architecturally similar to Arbiter invariants (10 rules), but the code is not shared.

---

## 4. spec-runner ↔ the ecosystem

### 4.1. What is spec-runner?

The `executor/` project **is** spec-runner:
- `executor/README.md:1` — "spec-runner — Task automation from markdown specs via Claude CLI"
- `executor/pyproject.toml:6` — `name = "spec-runner"`
- CLI: `spec-runner run`, `spec-runner plan`, `spec-runner mcp`

### 4.2. Duplication or complement?

**Complement.** A clean leaf/root architecture:

| Aspect | spec-runner (executor) | Maestro |
|--------|------------------------|---------|
| **Level** | Tactical — single task runner | Strategic — multi-task orchestrator |
| **Parallelism** | Sequential execution | Parallel spawn in git worktrees |
| **Tasks** | One subtask from `spec/tasks.md` | Decomposition of a project into many subtasks |
| **State** | JSON file (`.executor-state.json`) | SQLite (tasks, subtasks, outcomes) |
| **Git** | One branch per task | git worktree per subtask |
| **Dependency** | Independent (CLI tool) | Depends on spec-runner (subprocess) |

There is no duplication: Maestro delegates execution to spec-runner, adding decomposition, parallelism, PR creation, and workspace isolation.

### 4.3. How does Maestro call spec-runner?

```python
# Maestro/maestro/orchestrator.py:342-356
cmd = ["spec-runner", "run", "--all"]
if self._config.callback_url:
    cmd.extend(["--callback-url", self._config.callback_url])
process = await asyncio.create_subprocess_exec(
    *cmd, cwd=workspace, stdout=log_fd, stderr=asyncio.subprocess.STDOUT
)
```

Stages: decompose → generate `spec/tasks.md` → write `executor.config.yaml` → spawn `spec-runner run --all` → monitor stdout + `.executor-state.json` → receive callback POST.

### 4.4. Contract points

| Contract | Direction | Validation | Risk |
|----------|-------------|-----------|------|
| CLI args (`--all`, `--callback-url`) | Maestro → spec-runner | No formal schema | 🟡 |
| `executor.config.yaml` | Maestro generates, spec-runner reads | `SpecRunnerConfig.to_executor_config()` (Maestro/maestro/models.py:740-763) | 🟡 |
| `.executor-state.json` | spec-runner writes, Maestro reads | Ad-hoc parsing: `state.get("tasks", {})` (Maestro/maestro/orchestrator.py:406-438) | 🟡 |
| Callback POST body | spec-runner → Maestro REST | Pydantic `CallbackRequest` on the Maestro side | 🟡 |

### 4.5. Shared components

**NO.** There is no shared code, shared models, or common utilities. The contract is through the file system (YAML, JSON) and subprocess.

### 4.6. Risks

- The spec-runner version is not pinned in `Maestro/pyproject.toml`
- The `.executor-state.json` format is parsed ad-hoc without a typed model
- On a spec-runner update, a config-format mismatch is possible

---

## 5. Shared dependencies

### 5.1. Python versions

| Project | Python | Status |
|--------|--------|--------|
| Maestro | >=3.12 | ✅ |
| ATP Platform | >=3.12 | ✅ |
| Arbiter | >=3.12 | ✅ |
| Executor | >=3.10 | ⚠️ More lenient, but compatible |

**Conclusion:** All run on Python 3.12+. There are no conflicts.

### 5.2. Key dependencies

| Dependency | Maestro | ATP | Arbiter | Executor | Conflict? |
|-------------|---------|-----|---------|----------|-----------|
| **Pydantic** | >=2.12.5 | >=2.0 | — | — | ❌ All on v2 |
| **FastAPI** | >=0.128.1 | >=0.128.0 | — | — | ❌ Compatible |
| **aiosqlite** | >=0.22.1 | >=0.22.1 | — | — | ❌ Identical |
| **SQLAlchemy** | — | >=2.0.46 | — | — | ❌ |
| **NumPy** | — | — | >=2.4.2 | — | ❌ |
| **scikit-learn** | — | — | >=1.8.0 | — | ❌ |
| **PyYAML** | >=6.0.3 | >=6.0 | — | >=6.0 | ❌ |
| **Rich** | >=14.3.2 | >=13.0 | — | — | ❌ |
| **Ruff (dev)** | >=0.15.0 | >=0.14.14 | >=0.15.0 | >=0.14.14 | ⚠️ Minor |
| **Pytest (dev)** | >=9.0.2 | >=9.0.2 | >=9.0.2 | >=9.0.2 | ❌ |
| **rusqlite (Rust)** | — | — | 0.31 | — | ❌ Isolated |

### 5.3. Pydantic v1 vs v2

**All on v2.** Pydantic v1 is not used in any project.

### 5.4. Conflicts when installing into a single environment

**NO critical conflicts.** All projects install safely into a single Python 3.12+ environment. The only difference is the minor version of ruff (0.14 vs 0.15), which does not affect runtime.

---

## Final integration matrix

```
                    ┌──────────┐
                    │  Arbiter │
                    │ (Rust)   │
                    └────┬─────┘
                         │ 🔴 route_task (NOT IMPLEMENTED)
                         │ 🔴 report_outcome (NOT IMPLEMENTED)
                         │ 🔴 get_agent_status (NOT IMPLEMENTED)
                         ▼
┌──────────┐   🟢   ┌──────────┐   🔴    ┌──────────┐
│spec-runner├───────►│ Maestro  ├────────►│   ATP    │
│(executor) │process │          │verify   │ Platform │
└──────────┘        └──────────┘         └──────────┘
                                              ▲
                         🔴 eval              │
                    ┌──────────┐              │
                    │  Arbiter ├──────────────┘
                    └──────────┘   (NOT IMPLEMENTED)
```

**Legend:** 🟢 working — 🟡 partial — 🔴 not implemented

---

## Recommended actions

### Priority 1 (🔴 blockers)

1. **Update COWORK_CONTEXT.md** — the integration map shows Maestro→Arbiter and Maestro→ATP as existing. They must be explicitly marked **PLANNED**, not implemented.
   - *Anchor:* `COWORK_CONTEXT.md:57-68`

2. **Decide the Maestro↔Arbiter integration strategy** — advisory (hints with fallback to static) or authoritative (Arbiter makes the decisions). Key blockers: the absence of `task_type`, `language`, `complexity` in TaskConfig and the incompatibility of `codex` / `codex_cli`.
   - *Anchor:* `Maestro/maestro/models.py:45-110`, `arbiter/arbiter-core/src/types.rs`

### Priority 2 (🟡 improvements)

3. **Type `.executor-state.json`** — replace ad-hoc parsing with a Pydantic model.
   - *Anchor:* `Maestro/maestro/orchestrator.py:406-438`

4. **Pin the spec-runner version** in `Maestro/pyproject.toml`.
   - *Anchor:* `Maestro/pyproject.toml`

5. **Consider ATP validation** via `validation_cmd: "atp run suite.yaml"` — minimal effort (0 lines of code), maximum benefit.
   - *Anchor:* `Maestro/maestro/validator.py`, `atp-platform/atp/sdk/__init__.py`

### Priority 3 (🟢 roadmap)

6. **Implement eval-driven routing validation** for Arbiter via ATP (ECO-3 from the roadmap).
   - *Anchor:* `arbiter/SUGGESTIONS.md:70-83`, `arbiter/_cowork_output/07-roadmap.md:17`

7. **Normalize agent IDs** (`codex` → `codex_cli` or vice versa) before integration begins.
   - *Anchor:* `Maestro/maestro/models.py` (AgentType), `arbiter/config/agents.toml`
