---
title: Ecosystem shared-infrastructure decisions
type: adr
status: proposed
owner: Andrei
updated: 2026-07-05
---

# Ecosystem shared-infrastructure decisions

**Date:** 2026-04-05

## TL;DR

1. **Shared Types Library** — do NOT create a Python package. Instead: JSON Schema as the source of
   truth, generating Pydantic/serde from it. Effort: M, but **defer** until the Maestro↔Arbiter
   integration stabilizes (R-03).
2. **Contract Testing** — JSON Schema validation in each project's CI + one integration test runner. Do
   this **now** (R-04/R-05), effort: M.
3. **Unified Setup** — a `Makefile` at the root + `docker-compose.yml` for the full stack. Do this
   **now**, effort: S.
4. **Ecosystem Documentation** — a unified `docs/` with Architecture Decision Records + Getting Started.
   Do this **now** (R-11), effort: M.
5. **Monorepo vs Multi-repo** — keep multi-repo with light coordination (root Makefile + contract
   tests). **Reject** the monorepo — the overhead is not justified for 1 developer and 3 projects in
   different languages.
6. **agent-infra.yaml** — a **premature abstraction**. Defer until the Maestro↔Arbiter integration has
   been running in production for at least 2 weeks.

---

## 1. Shared Types Library

### Problem

Three projects define overlapping data types independently:

| Concept | Maestro (Pydantic) | Arbiter (serde/Rust) | ATP (Pydantic) |
|-----------|--------------------|-----------------------|-----------------|
| Task ID | `str`, regex `^[a-zA-Z0-9_-]+$` | `String` | `str`, regex `^[a-zA-Z0-9_-]+$` |
| Scope | `list[str]` (globs) | `Vec<String>` (paths) | `list[str]` (artifacts) |
| Priority | `int (-100..100)` | `enum (Low/Normal/High/Urgent)` | — |
| Timeout | `timeout_minutes: int` | `sla_minutes: u32` | `timeout_seconds: int` |
| Agent ID | `codex` | `codex_cli` | — |
| Status | 8-state machine | `Assign/Reject/Fallback` | `Completed/Failed/Timeout/Cancelled/Partial` |

**The real scale of the problem:** the Maestro↔Arbiter contract (route_task) is the only point where a
mismatch would cause a runtime error. ATP is framework-agnostic, its types differ deliberately. In other
words, the shared-types problem is relevant **only for two projects**, and only for a single contract.

### Options

#### Option A: A Python package `orchestrator-types`

```
orchestrator-types/
├── pyproject.toml
├── orchestrator_types/
│   ├── task.py      # Task, TaskInput, TaskConfig
│   ├── agent.py     # AgentType, AgentStatus
│   ├── outcome.py   # OutcomeReport, Decision
│   └── enums.py     # Priority, Complexity, Language, TaskType
```

| For | Against |
|----|--------|
| Import and IDE autocomplete | Coupling: any type change → update all consumers |
| A single source of truth | Arbiter (Rust) cannot import a Python package — it would have to duplicate or code-generate |
| Pydantic v2 validation out of the box | Yet another package to maintain, version, and publish |
| | 3 projects, 1 developer — the overhead is disproportionate |

**Effort:** XL (a new package + revising the models across all projects + CI + versioning)
**Impact:** 🟡 — removes mismatches, but only for Maestro↔Arbiter, which is not yet integrated

#### Option B: JSON Schema → code generation

```
_schemas/
├── task-input.schema.json    # Source of truth
├── outcome-report.schema.json
├── agent-status.schema.json
└── generate.sh               # → Pydantic (datamodel-codegen) + Rust (typify)
```

| For | Against |
|----|--------|
| Language-agnostic source of truth | datamodel-codegen and typify are not perfect: sometimes manual touch-up is needed |
| Python and Rust get types from one schema | Two steps: edit schema → regenerate → commit |
| JSON Schema — a standard, interoperability | Yet another artifact to version |
| Maestro already exports JSON Schema (`schemas/project_config.json`) | Arbiter uses serde, not JSON Schema — the mapping is non-obvious |

**Effort:** M (schemas + generation script + CI job)
**Impact:** 🟡 — elegant, but solves a problem that has not yet arrived

#### Option C: Contract types at the integration point

```
Maestro/maestro/contracts/
├── arbiter_types.py   # Pydantic models FOR calling Arbiter
│   # RouteTaskRequest, RouteTaskResponse, ReportOutcomeRequest
└── arbiter_mapping.py # TaskConfig → RouteTaskRequest mapping
```

| For | Against |
|----|--------|
| Minimal blast radius: we change only Maestro | Duplication: Arbiter's types are described in two places |
| No coupling between projects | On an Arbiter API change — manual update |
| Can start right now | Does not scale to 10+ integrations |
| Mapping priority, codex→codex_cli — in one place | |

**Effort:** S (one module in Maestro)
**Impact:** 🟢 — solves the real problem at the real scale

### Recommendation: Option C now → Option B later

**Now (when implementing R-03):** create `contracts/arbiter_types.py` in Maestro. This is the minimal
effort that solves a real problem: mapping `codex` → `codex_cli`, `priority: int → enum`, adding
`task_type`/`language`/`complexity`.

**Later (after R-05, once the integration stabilizes):** extract the shared types into JSON Schema. By
that point the types will have stabilized through real use, and code generation will not be shooting at a
moving target.

**Never (at this scale):** a Python package `orchestrator-types`. Three projects, one developer, two
languages — the overhead is not justified. If the ecosystem grows to 5+ projects with 3+ consumers of
the same types — reconsider.

| | Effort | Impact | Recommendation |
|---|--------|--------|-------------|
| Python package | XL | 🟡 | ❌ Reject |
| JSON Schema + codegen | M | 🟡 | ⏸️ Defer (after R-05) |
| Contract types in Maestro | S | 🟢 | ✅ Do at R-03 |

---

## 2. Contract Testing

### Problem

Of the 7 contract points in the ecosystem (see `_cowork_output/contracts/contract-analysis.md`):
- 4 are not implemented (Maestro→Arbiter ×3, Maestro→ATP)
- 1 works with an informal contract (Maestro→spec-runner)
- 2 are internal and formalized (tasks.yaml, MCP coordination)

The only working integration (Maestro→spec-runner) can break when spec-runner is updated:
`.executor-state.json` is parsed ad-hoc (`state.get("tasks", {})`), the spec-runner version is not
pinned.

### Options

#### Option A: Pact tests (consumer-driven contracts)

| For | Against |
|----|--------|
| Industry standard for contract testing | Pact for Rust — via FFI, complex setup |
| Consumer-driven: Maestro describes what it needs | Overhead: Pact Broker, CI integration, learning curve |
| Automatic detection of mismatches | For 1 real integration — using a cannon to kill a sparrow |

**Effort:** L
**Impact:** 🟡

#### Option B: JSON Schema validation in CI

```yaml
# .github/workflows/contract-check.yml (in each project)
- name: Validate contracts
  run: |
    # Arbiter: exports JSON Schema from serde types
    cargo test --test export_schemas
    # Maestro: validates its request/response against Arbiter's schema
    python -m pytest tests/contracts/ -k "arbiter_schema"
```

Each project stores its "expectations" of the partner as a JSON Schema or a Pydantic model. CI checks
that `RouteTaskRequest` (Maestro) is compatible with `TaskInput` (Arbiter) — via JSON Schema validation
or snapshot tests.

| For | Against |
|----|--------|
| Zero new dependencies | Manual update on API changes |
| Works in the existing CI | No automatic detection of breaking changes cross-repo |
| Maestro already exports JSON Schema | Requires discipline: update the schema on changes |

**Effort:** M
**Impact:** 🟡

#### Option C: Integration test suite (a separate runner)

```
_integration_tests/
├── test_maestro_arbiter.py    # Spins up an Arbiter subprocess, sends route_task
├── test_maestro_specrunner.py # Spins up spec-runner, checks executor-state.json
├── test_arbiter_schemas.py    # Validates Arbiter JSON Schema vs Maestro types
├── conftest.py                # Fixtures: build Arbiter binary, setup test data
└── Makefile                   # make test-contracts
```

| For | Against |
|----|--------|
| Real end-to-end checks | Requires building all projects |
| One runner for all contracts | Slower than unit tests |
| Easy to extend | Needs CI that has access to all repos |

**Effort:** M
**Impact:** 🟢

### Recommendation: Option B + C (a two-level approach)

**Level 1 — JSON Schema validation in each project's CI (Option B):**
- Arbiter: export JSON Schema from serde types (cargo test `--test export_schemas`)
- Maestro: when implementing R-03, add `tests/contracts/test_arbiter_compat.py` — validates
  `RouteTaskRequest` against Arbiter's schema
- spec-runner: create a Pydantic model `ExecutorState` (R-04), a format snapshot test

**Level 2 — Integration test runner at the root (Option C):**
- `_integration_tests/` next to `_cowork_output/`
- Run manually or on a schedule (not on every push)
- Tests: Maestro→Arbiter MCP round-trip, Maestro→spec-runner config generation

**Pact — no.** For a single developer and 1-2 real integrations, the overhead is not justified.

| | Effort | Impact | Recommendation |
|---|--------|--------|-------------|
| Pact tests | L | 🟡 | ❌ Reject |
| JSON Schema validation | M | 🟡 | ✅ Do now (R-04/R-05) |
| Integration test suite | M | 🟢 | ✅ Do after R-03 |

---

## 3. Unified Setup

### Problem

A new contributor (or you in 3 months) must:
1. Clone 3+ repositories
2. For each: `uv sync` (Python) or `cargo build` (Rust)
3. Set up external dependencies: git CLI, gh CLI, Claude CLI, SQLite
4. Understand how to run the tests in each project

Right now this is ~15 minutes of manual work reading 3 different READMEs. Not critical, but annoying when
switching context.

### Options

#### Option A: A bash script `bootstrap.sh`

```bash
#!/bin/bash
set -euo pipefail
echo "=== Checking prerequisites ==="
command -v git >/dev/null || { echo "git required"; exit 1; }
command -v uv >/dev/null || { echo "uv required"; exit 1; }
command -v cargo >/dev/null || { echo "cargo required (for Arbiter)"; exit 1; }

echo "=== Installing Python deps ==="
for proj in Maestro atp-platform executor; do
  (cd "$proj" && uv sync)
done

echo "=== Building Arbiter ==="
(cd arbiter && cargo build --release)

echo "=== Running smoke tests ==="
(cd Maestro && uv run pytest tests/ -x --timeout=30)
(cd arbiter && cargo test)
(cd atp-platform && uv run pytest tests/ -x --timeout=30)
```

| For | Against |
|----|--------|
| Zero dependencies | Not cross-platform (bash) |
| Easy to read and debug | No parallelism |
| 30 minutes to write | No idempotency |

#### Option B: A Makefile at the root

```makefile
.PHONY: install test lint all

install: install-maestro install-arbiter install-atp install-executor
install-maestro:
	cd Maestro && uv sync
install-arbiter:
	cd arbiter && cargo build --release
install-atp:
	cd atp-platform && uv sync
install-executor:
	cd executor && uv sync

test: test-maestro test-arbiter test-atp
test-maestro:
	cd Maestro && uv run pytest tests/ -x
test-arbiter:
	cd arbiter && cargo test
test-atp:
	cd atp-platform && uv run pytest tests/ -x

lint: lint-maestro lint-arbiter lint-atp
lint-maestro:
	cd Maestro && uv run ruff check .
lint-arbiter:
	cd arbiter && cargo clippy
lint-atp:
	cd atp-platform && uv run ruff check .
```

| For | Against |
|----|--------|
| A standard tool, make is everywhere | Makefile syntax — not for everyone |
| Parallelism: `make -j4 install` | Tab vs spaces |
| Modular: `make test-maestro` | Lacks dependency management |
| Arbiter already uses a Makefile | |

#### Option C: docker-compose

```yaml
services:
  arbiter:
    build: ./arbiter
    command: cargo run --release --bin arbiter-mcp
  maestro:
    build: ./Maestro
    depends_on: [arbiter]
    command: uv run maestro run --config examples/tasks.yaml
  atp-dashboard:
    build: ./atp-platform
    ports: ["8080:8080"]
    command: uv run atp dashboard
```

| For | Against |
|----|--------|
| Isolated environment | Arbiter MCP — stdio-based, not a service → needs an adapter |
| Reproducible on any OS | Maestro works with git worktrees → mount volumes |
| Full stack with one command | Heavyweight for 1 developer |
| | Slower than native: image rebuilds on changes |

#### Option D: just (modern command runner)

```justfile
# Ecosystem setup
install:
    just install-maestro & just install-arbiter & just install-atp & wait

install-maestro:
    cd Maestro && uv sync
install-arbiter:
    cd arbiter && cargo build --release
install-atp:
    cd atp-platform && uv sync

test:
    just test-maestro & just test-arbiter & just test-atp & wait

test-maestro:
    cd Maestro && uv run pytest tests/ -x
```

| For | Against |
|----|--------|
| Cleaner than a Makefile, no tab issues | An extra dependency (just) |
| Native parallelism | Less widespread |
| Cross-platform | |

### Recommendation: Option B (Makefile) + a lite docker-compose for the dashboard

**A Makefile at the root** — standard, zero dependencies, Arbiter already uses a Makefile. Targets:
`install`, `test`, `lint`, `check-contracts`. Parallelism via `make -j`.

**docker-compose** — only for the full stack with the dashboard (ATP). Not for daily development.

**just** — a good alternative, but `make` is already familiar and in use. Not worth introducing yet
another tool.

| | Effort | Impact | Recommendation |
|---|--------|--------|-------------|
| bootstrap.sh | S | 🟢 | ⏸️ Intermediate option |
| Makefile at the root | S | 🟢 | ✅ Do now |
| docker-compose (full) | M | 🟢 | ⏸️ Defer (after integrations) |
| just | S | 🟢 | ❌ Do not add a new tool |

---

## 4. Ecosystem Documentation

### Problem

Documentation is fragmented:
- `COWORK_CONTEXT.md` — the integration map (partly inaccurate: planned shown as implemented)
- Each project: README.md + CLAUDE.md (good, but isolated)
- `_cowork_output/` — analysis reports (useful, but not developer documentation)
- No unified Getting Started, no Architecture Decision Records, no single entry point

A new developer must read 6+ files to understand how everything is connected.

### Solution

```
docs/
├── README.md                    # Entry point: what it is, why, how to start
├── getting-started.md           # A 15-minute guide: clone → install → run → test
├── architecture.md              # Diagrams, data flows, contract points
├── adr/                         # Architecture Decision Records
│   ├── 001-multi-repo.md        # Why multi-repo, not monorepo
│   ├── 002-mcp-for-routing.md   # Why MCP for Maestro↔Arbiter
│   ├── 003-shared-types.md      # The shared-types decision (this document)
│   └── template.md              # ADR template
└── diagrams/
    └── ecosystem.mermaid        # Mermaid diagram of integrations
```

**`README.md` (root):**
- One sentence: what it is
- A table of projects (from COWORK_CONTEXT.md, but with accurate status)
- Quick start: `make install && make test`
- Links to getting-started.md and architecture.md

**`getting-started.md`:**
- Prerequisites: Python 3.12+, Rust, uv, git, gh
- `make install` — what happens
- Running each project separately
- Running the integration (once it exists)

**`architecture.md`:**
- A Mermaid diagram with the **real** status of the links
- A description of each contract point: format, validation, status
- Links to specific files in the projects

**ADR:**
- Each architectural decision — a separate file
- Format: context → decision → consequences → status
- Versioned alongside the code

### Recommendation: do now

| | Effort | Impact | Recommendation |
|---|--------|--------|-------------|
| docs/ structure + README | M | 🟢 | ✅ Do now |
| ADR for key decisions | S (per ADR) | 🟡 | ✅ Start with this document |
| Mermaid diagrams | S | 🟢 | ✅ Do now |

---

## 5. Monorepo vs Multi-repo

### Problem

The current situation is a **pseudo-monorepo**: the projects sit side by side in one folder, but:
- Each has its own `.git` (separate repositories)
- No shared workspace (`uv workspace`, `cargo workspace`)
- No cross-project CI
- No shared dependency management
- COWORK_CONTEXT.md plays the role of the "glue"

### Analysis of current multi-repo problems

| Problem | Severity | Frequency |
|----------|-------------|---------|
| Agent ID mismatch (`codex` vs `codex_cli`) | 🔴 | Once, but blocks the integration |
| No cross-project CI | 🟡 | On every change to contract points |
| Manual contract versioning | 🟡 | On every breaking change |
| Duplication of dev dependencies (ruff, pytest) | 🟢 | Minimal overhead |
| Separate git histories | 🟢 | Not a problem with 1 developer |

### Options

#### Option A: A full monorepo

```
ai-orchestrators/
├── Cargo.toml          # Rust workspace
├── pyproject.toml      # uv workspace
├── packages/
│   ├── maestro/
│   ├── arbiter/
│   ├── atp-platform/
│   └── executor/
├── shared/
│   └── orchestrator-types/
└── .github/workflows/
    └── ci.yml          # A single CI for all
```

| For | Against |
|----|--------|
| Atomic commits across project boundaries | Different languages (Rust + Python) → a complex workspace |
| Unified CI/CD | atp-platform already has its own uv workspace with 7 packages — nested workspaces |
| Shared deps management | Arbiter has been stable for 2 months — why drag it into a monorepo? |
| One `git blame` over the whole history | git history migration: squash or preserve? |
| | 1 developer — no problem of "I don't see my colleague's changes" |

**Effort:** XL
**Impact:** 🟢 — solves problems that are not critical at this scale

#### Option B: Multi-repo + coordination

```
all_ai_orchestrators/        # A regular folder (not a git repo)
├── Maestro/                 # git repo
├── arbiter/                 # git repo
├── atp-platform/            # git repo
├── executor/                # git repo
├── Makefile                 # Root: install, test, lint, check-contracts
├── docs/                    # Shared documentation
├── _integration_tests/      # Cross-project tests
├── _schemas/                # JSON Schema of contracts (optional)
└── _cowork_output/          # Analysis reports
```

| For | Against |
|----|--------|
| Each project lives its own life | No atomic commits |
| No migration, no breakage | Contract versioning — manual |
| ATP can be reused in other ecosystems | Cross-project CI must be set up separately |
| Arbiter is not touched unless needed | |

**Effort:** S (add a Makefile + docs/)
**Impact:** 🟢 — minimal overhead, maximum flexibility

#### Option C: git submodules

| For | Against |
|----|--------|
| A single clone: `git clone --recursive` | submodules — notoriously complex |
| Pinned versions of each project | Detached HEAD, forgotten `git submodule update` |
| | Does not solve the shared-types problem |
| | Adds friction in daily work |

**Effort:** M
**Impact:** 🔴 — adds complexity without solving the main problems

### Recommendation: Option B (multi-repo + coordination)

**An honest assessment for the current scale:** 1 developer, 3 active projects, 2 languages
(Python + Rust), 1 implemented integration. A monorepo solves problems you do not have: coordination
between teams, atomic cross-project deploys, dependency diamonds.

The problems that do exist (agent ID mismatch, absence of cross-project CI) are solved far more cheaply:
contract tests + a root Makefile + documentation.

**If the ecosystem grows** to 5+ Python projects with shared dependencies — reconsider toward a uv
workspace monorepo (without Rust — Arbiter can stay separate).

| | Effort | Impact | Recommendation |
|---|--------|--------|-------------|
| Full monorepo | XL | 🟢 | ❌ Reject |
| Multi-repo + coordination | S | 🟢 | ✅ Do now |
| git submodules | M | 🔴 | ❌ Reject |

---

## 6. agent-infra.yaml — a unified declarative layer

### Problem (from COWORK_CONTEXT.md and roadmap R-15)

The ecosystem configuration is smeared across projects:
- `Maestro/tasks.yaml` — task DAG, agent_type, timeouts
- `arbiter/config/agents.toml` — agents, capabilities, parameters
- `arbiter/config/invariants.toml` — 10 safety rules
- `atp-platform/*.yaml` — test suites, evaluators
- `Maestro/executor.config.yaml` (generated) — spec-runner settings

The idea of `agent-infra.yaml`: one file describing the whole ecosystem.

```yaml
# agent-infra.yaml (hypothetical)
agents:
  claude_code:
    capabilities: [python, rust, typescript]
    cost_per_1k_tokens: 0.003
    max_concurrent: 3
  codex_cli:
    capabilities: [python, javascript]
    cost_per_1k_tokens: 0.001
    max_concurrent: 5

routing:
  engine: arbiter
  fallback: static
  invariants:
    - name: budget_guard
      severity: critical
      threshold: 100.0

orchestration:
  engine: maestro
  default_timeout_minutes: 30
  parallelism: 4

verification:
  engine: atp
  default_suite: smoke-tests.yaml
```

### Maturity analysis

| Precondition | Status | Blocker? |
|-------------|--------|---------|
| Maestro↔Arbiter integration works | 🔴 NO (0 lines of code) | ✅ Critical |
| Maestro↔ATP integration works | 🔴 NO | ✅ Critical |
| Types are stabilized | 🔴 NO (agent IDs, priority incompatible) | ✅ Critical |
| There is experience of daily use of the integrations | 🔴 NO | ✅ Critical |
| It is clear which parameters are runtime vs build-time | 🟡 Partly | 🟡 Needs defining |

**Verdict: 4 of 5 preconditions are unmet. This is a classic premature abstraction.**

### Why agent-infra.yaml is dangerous now

1. **No feedback loop.** Not a single integration works. The format would be based on assumptions, not
   experience. After a month of real operation it will turn out that fields we did not anticipate are
   needed, and fields we added are not.

2. **Coupling amplifier.** A single file = a single point of change. Any update of an agent, policy, or
   test requires editing agent-infra.yaml. With 1 developer this is tolerable, but the format becomes
   legacy before it becomes useful.

3. **A false sense of control.** "We have a unified declarative layer" — sounds good, but if Maestro
   does not call Arbiter and does not use ATP, the file describes a dream, not reality.

### When agent-infra.yaml becomes relevant

When the following are **simultaneously** met:
- R-03 (MCP client) is implemented and has been working for 2+ weeks
- R-06 (ATP verification) — at least via CLI
- There are 3+ real runs where Maestro → Arbiter → Agent → ATP is a full cycle
- A need arises to change parameters without editing code (runtime config)

**Roughly:** 2-3 months after work on R-03 begins.

### What to do instead

**COWORK_CONTEXT.md** already plays the role of a "unified description of the ecosystem" — but for
people, not for machines. That is the right level of abstraction at the current stage.

Once the integrations are working, the first step is not agent-infra.yaml, but **`orchestrator.toml`**
at the root of Maestro:

```toml
[routing]
strategy = "arbiter"          # or "static"
arbiter_binary = "../arbiter/target/release/arbiter-mcp"
fallback = "static"

[verification]
enabled = true
command = "atp run smoke.yaml"

[spec_runner]
version = "1.1.0"
binary = "spec-runner"
```

This is not "a single file for the whole ecosystem", but Maestro's config for working with external
services. Much more modest, much more useful.

| | Effort | Impact | Recommendation |
|---|--------|--------|-------------|
| agent-infra.yaml (full) | XL | 🟢 | ❌ Defer (≥ 2-3 months) |
| orchestrator.toml (Maestro) | S | 🟡 | ⏸️ Do at R-03 |
| COWORK_CONTEXT.md (as is) | — | 🟢 | ✅ Keep using |

---

## Final summary of decisions

| # | Decision | What we do | Effort | Impact | When |
|---|---------|-----------|--------|--------|-------|
| 1 | **Shared Types** | Contract types in `Maestro/contracts/`, then JSON Schema | S→M | 🟢→🟡 | At R-03, JSON Schema after R-05 |
| 2 | **Contract Testing** | JSON Schema validation + integration test runner | M | 🟡 | Now (R-04/R-05) |
| 3 | **Unified Setup** | Makefile at the root (`install`, `test`, `lint`) | S | 🟢 | Now |
| 4 | **Documentation** | `docs/` with README, getting-started, architecture, ADR | M | 🟢 | Now |
| 5 | **Monorepo** | Keep multi-repo + coordination (Makefile, docs, tests) | S | 🟢 | Now |
| 6 | **agent-infra.yaml** | Defer. Instead: `orchestrator.toml` in Maestro at R-03 | — | — | ≥ 2-3 months |

### Order of execution

```
Sprint 1 (in parallel, effort: S+S+M)
├── Makefile at the root                       # 30 min
├── docs/ structure + README + architecture    # 2-4 hours
└── ADR-001: multi-repo decision                # 30 min

Sprint 2 (when implementing R-03)
├── Maestro/contracts/arbiter_types.py          # As part of R-03
├── orchestrator.toml in Maestro                # As part of R-03
└── tests/contracts/test_arbiter_compat.py      # As part of R-05

Later (after the integrations stabilize)
├── _schemas/ with JSON Schema + codegen        # Once the types stabilize
├── _integration_tests/                         # After R-03
└── docker-compose for the full stack           # As needed

Do not do
├── Python package orchestrator-types
├── Full monorepo
├── git submodules
├── Pact tests
└── agent-infra.yaml (until stabilization)
```

---

## Recommended actions (mapped to projects)

1. **Create a `Makefile` at the root of `all_ai_orchestrators/`** — targets: install, test, lint, status.
   Effort: 30 min.
   - *Mapping:* `all_ai_orchestrators/Makefile` (new file)

2. **Create `docs/` at the root** — README.md, getting-started.md, architecture.md. Use the
   `_cowork_output/` reports as a source.
   - *Mapping:* `all_ai_orchestrators/docs/` (new folder)

3. **ADR-001: Multi-repo decision** — record the decision to keep multi-repo with justification.
   - *Mapping:* `all_ai_orchestrators/docs/adr/001-multi-repo.md`

4. **When implementing R-03:** create `Maestro/maestro/contracts/arbiter_types.py` with the mapping
   codex→codex_cli, priority int→enum, adding task_type/language/complexity.
   - *Mapping:* `Maestro/maestro/contracts/` (new folder)

5. **Type `.executor-state.json`** — a Pydantic model `ExecutorState` in Maestro (R-04).
   - *Mapping:* `Maestro/maestro/models.py` or `Maestro/maestro/contracts/specrunner_types.py`

6. **Do NOT create agent-infra.yaml** until Maestro↔Arbiter stabilizes. Instead — `orchestrator.toml`
   in Maestro.
   - *Mapping:* revisit 2-3 months after R-03

---

*Based on the reports: `_cowork_output/contracts/contract-analysis.md`,
`_cowork_output/integration/integration-health.md`, `_cowork_output/roadmap/ecosystem-roadmap.md`,
`_cowork_output/status/2026-04-05-status.md`*
