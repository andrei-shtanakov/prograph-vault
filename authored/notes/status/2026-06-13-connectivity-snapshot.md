---
title: Ecosystem state and connectivity — 2026-06-13
type: note
status: archived
owner: Andrei
updated: 2026-06-13
archived: 2026-07-06
reason: historical status snapshot (bulk-archived on graduation from _cowork_output)
---

# Ecosystem state and connectivity — 2026-06-13

> A snapshot of the current state and interconnections of the AI-orchestrator projects.
> Method: `git log/status/branch` across all repositories, reading the registry
> `COWORK_CONTEXT.md`, the contract files, and the `prograph-vault/` graph.
> Mode: read-only. Comparison baseline: `_cowork_output/status/2026-06-12-status.md`.

## TL;DR

1. **The ecosystem runs at two speeds.** The "hot" loop is `spec-runner` (96 commits since 05-23, releases up to v2.4.1, commits today) and `atp-platform` (38 commits, release v2.1.0, commits today). The "frozen" loop is `Maestro` and `arbiter`: **0 commits for 21 days**, both sitting on docs branches since 2026-05-23.
2. **The "benchmark → routing" loop (R-07) has been idle for a fourth week.** All dependencies (R-06b M4, `report_benchmark`, protocol 1.1.0) were closed back on 05-23, but `arbiter` still has not begun to use `BenchmarkResult` as an input to the decision-tree. This is the main connectivity gap: the contract is built, but no traffic flows through it.
3. **Contracts are stable — no drift at the joints.** No cross-project contract (`executor-state`, `json-result`, `report_benchmark-v1`, observability `log-schema`) changed. The atp v2.1.0 and spec-runner v2.4.x releases are additive. `prograph` confirms: 7 contracts, 28 edges, the shared `report_benchmark-v1.schema.json` is in sync across 3 owners (Maestro + arbiter + arbiter-mcp).
4. **The `COWORK_CONTEXT.md` registry has drifted for 3 weeks (P1, not closed).** Updated 05-23; the versions are stale (`spec-runner` is listed as 2.0.0 → actual **2.4.1**; `atp-platform` 2.0.0 → actual **2.1.0**). Four projects are unregistered: `appgraph`, `prograph`, `prograph-vault`, `spec-runner-tasks`.
5. **The connectivity-mapping tool itself is stale.** `prograph-vault/` (the Obsidian graph) was generated from snapshot 48 on **2026-05-27** — 17 days ago. It does not see `appgraph` and `spec-runner-tasks`, which appeared later. The map of interconnections lags behind the reality it is meant to reflect.

---

## 1. Activity by repository (since 2026-05-23)

| Project | Branch (HEAD) | Commits since 05-23 | Last commit | Uncommitted | State |
|--------|--------------|---:|------------------|---:|-----------|
| **spec-runner** | `feat/config-presets` | 96 | 2026-06-13 `fix(validate)` | 1 | 🟢 Hot; releases v2.3.1→v2.4.1 |
| **atp-platform** | `infra/aws-bedrock-terraform` | 38 | 2026-06-13 `feat(infra) SSM run-sweep` | 1 | 🟢 Hot; release v2.1.0 |
| **spec-runner-tasks** | `main` | 19 | 2026-06-12 `Merge TASK-020 (pi-demo)` | 1 | 🟢 Dogfooding loop |
| **arbiter** | `docs/r-06b-m4-update` | 17* | 2026-05-23 `docs: Copilot review` | 2 | 🔴 Silent 21 days |
| **Maestro** | `docs/r-06b-m4-followup` | 9* | 2026-05-23 `docs(changelog)` | 2 | 🔴 Silent 21 days |
| **prograph / appgraph** | (root repo) | 0 | 2026-05-28 `appgraph: fix tasks.md` | `M appgraph/spec/tasks.md` | 🟡 Not in registry; index 17 days |
| **proctor-a** | `master` | 0 | 2026-04-16 | 4 | 🔴 Paused 8+ wk |
| **open-prose** | `main` | 0 | 2026-04-07 | 3 | ⏸️ Idle 9+ wk |

> \* For Maestro/arbiter all commits since 05-23 are the history of docs branches up to the freeze date; there are **no** new commits after 2026-05-23. The `master`/`main` of both stand at 2026-05-23.
> All active repos sit on feature branches, not on `master` — merges into the main line lag (especially atp on `infra/...` and spec-runner on `feat/config-presets`).

---

## 2. Unregistered projects (registry drift)

| Project | What it is | Link to the ecosystem | In registry? |
|--------|---------|---------------------|:---:|
| **prograph** | Cross-project structure mapper (Rust+Python). M11: detect package-deps / shared contracts / MCP calls between projects, serves the graph to humans (browser UI) and agents (MCP `find_drifts`). | **Connectivity meta-tool** — indexes the whole folder, owns the `prograph-vault/` graph. | ❌ |
| **appgraph** | Build/explore a graph of `file`+`symbol` nodes of a single repo (SQLite `.appgraph/graph.db`, tree-sitter, FastAPI+cytoscape). v0.1.0. | Overlaps with `prograph` (both are code graphs) and, per a note in memory, with the **Maestro DAG**. Scope needs delimiting. | ❌ |
| **prograph-vault** | Obsidian vault — the **output** of `prograph` (projects/contracts/mcp_patterns). Snapshot 48 @ 2026-05-27. | This is the current (but stale) connectivity map. | ❌ |
| **spec-runner-tasks** | Dogfooding: the `textkit` project (19 tasks), actually run through spec-runner end-to-end. | A live consumer of spec-runner; exposed the DONE-commit bug fixed in v2.3.1. | ❌ |
| **spec-runner-test** | Test scaffold for spec-runner (Makefile, spec/, src/). No `.git` of its own. | Sandbox for spec-runner. | ❌ |

`appgraph` and `prograph` conceptually duplicate each other — both build code graphs. Worth recording a decision: `appgraph` = a graph **inside** a single repo (symbols/imports), `prograph` = a graph **between** repositories (contracts/MCP). If so — these are layers, not competitors; if not — one of them is redundant.

---

## 3. Connectivity map (contract points)

Data from `prograph-vault/` (snapshot 48) + file checks. All contracts in the current window are **unchanged** — the joints are stable.

| Contract | Owners (direction) | Status |
|----------|-------------------------|--------|
| `report_benchmark-v1.schema.json` | **Maestro** (benchmark-contract) → **arbiter** + **arbiter-mcp** (tests/contract) — 3 owners, byte-for-byte | 🟢 frozen, protocol 1.1.0 |
| `executor-state.schema.json` | **spec-runner** → **Maestro** (`ExtraState`, `extra="ignore"`) | 🟢 unchanged; ⚠ debt: interop fixtures not synchronized with v2.3.0 (`error_kind`/`error_stage`) |
| `json-result.schema.json` | **spec-runner** → **Maestro** | 🟢 frozen (R-04) |
| observability `log-schema.json` (`obs-v1`) | **Maestro** (owner) → vendored into **spec-runner** + **arbiter** @ `fa6b106` | 🟢 4-way axis aligned |
| arbiter MCP (6 tools) | **Maestro** → **arbiter** (`route_task`/`report_outcome`/.../`report_benchmark`) | 🟢 pin held |
| atp `agent-eval-case.schema.json` | **atp-method** (internal) | 🆕 new, no external consumers |
| spec-runner `doctor-result.schema.json` | **spec-runner** (internal) | 🆕 new, no external consumers |

**Data flow (how it should work):**
`Maestro` (DAG scheduler) → `route_task` → `arbiter` (policy/decision-tree) → spawn agents → `spec-runner` (spec execution → Claude CLI) → validation via `atp-platform` → `report_benchmark` → `arbiter.benchmark_runs` → **(R-07: should influence routing, but does not)**.

**The gap:** the last link is closed at the schema level (M4 ✅) but not at the code level (R-07 not started). The ready signal `error_kind` from spec-runner sits unused.

---

## 4. Misalignment risks

| # | Risk | Where | Severity |
|---|------|-----|:---:|
| R1 | The R-07 routing loop has been idle for 4 wk; benchmark data accumulates but does not influence routing | arbiter / Maestro | 🔴 P1 |
| R2 | The `COWORK_CONTEXT.md` registry lies about versions and is unaware of 4 projects | `COWORK_CONTEXT.md` | 🟠 P1 |
| R3 | `prograph-vault` (the connectivity map) is 17 days stale — does not see appgraph/spec-runner-tasks | `prograph-vault/index.md:5` | 🟠 P2 |
| R4 | The scope of `appgraph` vs `prograph` is not delimited; possible duplicate | appgraph / prograph | 🟡 P2 |
| R5 | The Maestro interop fixtures do not reflect `error_kind`/`error_stage` from spec-runner v2.3.0 | `spec-runner/tests/fixtures/maestro-interop/` | 🟡 P2 |
| R6 | Active work is stuck on feature branches, not merged into master | atp / spec-runner | 🟡 P3 |

---

## Recommended actions

1. **arbiter + Maestro — unfreeze R-07.** Start a thin slice: `BenchmarkResult` from the `benchmark_runs` table as a weighting input to decision-tree inference. This is the only thing that turns the built contract into a working loop. (anchor: `arbiter/`, `Maestro/maestro/benchmark/`)
2. **Update `COWORK_CONTEXT.md`** — bump the versions (`spec-runner` 2.4.1, `atp-platform` 2.1.0), add `prograph`, `appgraph`, `prograph-vault`, `spec-runner-tasks` to the registry. The debt has dragged on for 4 weeks. (anchor: root)
3. **Regenerate the `prograph` index** (`prograph index` / `prograph drift`) — refresh `prograph-vault/` to the current snapshot so that the connectivity map includes appgraph and the dogfooding loop. Also run `find_drifts`. (anchor: `prograph/`)
4. **Record an ADR: appgraph vs prograph** — "inside-repo symbol graph" vs "between-repo contract graph". Split the scope or merge. (anchor: `_cowork_output/decisions/`)
5. **Synchronize the Maestro interop fixtures** with `executor-state` v2.3.0 (`error_kind`/`error_stage`) so R-07 gets a classified failure signal. (anchor: `spec-runner/tests/fixtures/maestro-interop/`)
6. **Merge the feature branches into master** on atp (`infra/aws-bedrock-terraform`) and spec-runner (`feat/config-presets`) after review — remove the main-line divergence. (anchor: both repos)
