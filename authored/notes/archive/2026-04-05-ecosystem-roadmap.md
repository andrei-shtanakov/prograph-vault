---
title: Ecosystem roadmap
type: note
status: archived
owner: Andrei
updated: 2026-07-05
archived: 2026-07-08
reason: "superseded by the 2026-07-08 roadmap (../ecosystem-roadmap.md). The R-01..R-10 critical
  path here (agent-ID normalization, Maestro<->Arbiter MCP client, spec-runner contract) shipped -
  confirmed live and working in status/2026-07-08-1228-status.md. The new roadmap covers what
  replaced it as the live strategic surface: GitHub Models retirement exposure, MCP protocol
  evolution, proctor positioning, observability unification."
---

# AI Orchestrators ecosystem roadmap

**Date:** 2026-04-05 · **Snapshot:** 2026-04-25

> **This file is a strategic roadmap.** Current state and evidence live in the latest status file:
> `../status/2026-04-24-status.md` (or later). Per-project tactics live in `<project>/TODO.md`.

## TL;DR (updated 2026-04-25)

1. **Critical path closed:** R-01..R-04 shipped (Maestro v0.2.0); R-09 + R-10 CI shipped; R-06a CLI quick win shipped (`docs/maestro-integration.md` in ATP); arbiter#9 (decision_id in response) fixed 2026-04-25 — paired commits `arbiter@d1a8ecd` + `Maestro@e5915f2/f1f7d26`. R-05 closed at the contract level.
2. **Cross-project observability v1 shipped:** spec-runner reference impl, Maestro M1 (vendored obs.py + child_env propagation) + M2 (scheduler instrumentation), arbiter Rust impl (`arbiter-core::obs`). Contract in `Maestro/_cowork_output/observability-contract/`.
3. **Maestro↔spec-runner contract frozen:** R-04 closed (JSON Schema, fixtures, `read_executor_state` with SQLite-first read).
4. **Maestro↔ATP CLI shipped (R-06a)**, SDK integration (R-06b) — **reformulated** (see `_cowork_output/decisions/2026-04-25-r06b-design.md`): SDK = participant-client, not validator-client; R-06b is now "agent benchmarking via ATP", not "validation via SDK". Approve the formulation → M1 thin slice can start.
5. **CI/CD everywhere:** ATP (7 workflows) + Maestro (`ci.yml`) + Arbiter (Rust+Python matrix + release binaries linux-x64/macos-arm64) + proctor (`ci.yml`).

### What remained from the original formulation (historical context 2026-04-05)
~~Main blocker: documentation describes integrations as existing, but in code there are 0 lines.~~ → closed by R-03 (Maestro v0.2.0).
~~The only working link (Maestro→spec-runner) is an informal contract.~~ → closed by R-04.
Dependencies are compatible (Python 3.12+, Pydantic v2). This is still current.

---

## Critical path

The execution order is determined by hard dependencies between tasks. Each next step is impossible without the previous one.

```
[R-01] Normalize agent IDs (codex↔codex_cli)
    │
    ├──▶ [R-02] Extend TaskConfig (task_type, language, complexity)
    │        │
    │        └──▶ [R-03] MCP client in Maestro (route_task, report_outcome)
    │                 │
    │                 ├──▶ [R-05] Integration tests Maestro↔Arbiter
    │                 │
    │                 └──▶ [R-06] ATP verification via validation_cmd
    │                              │
    │                              └──▶ [R-07] Eval-driven routing (Arbiter↔ATP)
    │
    └──▶ [R-04] Formalize spec-runner contract (in parallel with R-02/R-03)
```

**Why exactly this order:**

- R-01 blocks R-03: if agent IDs are not normalized, Arbiter will return a routing error on the first call.
- R-02 blocks R-03: Arbiter requires `task_type`, `language`, `complexity` as required fields. Without them — rejection.
- R-03 blocks R-05 and R-06: no client — nothing to test, no data for the feedback loop.
- R-04 can be done in parallel — it is the only working link, independent of Arbiter.

---

## Tasks by priority

### P0 — Ecosystem blockers

Without these tasks the projects cannot work together.

---

#### R-01. Normalize agent IDs

| | |
|---|---|
| **Description** | Maestro uses `codex`, Arbiter uses `codex_cli`. On an integration attempt, Arbiter won't find the agent and will return fallback/reject. Also, Maestro has an `announce` agent that does not exist in Arbiter — need to decide whether to bypass it during routing. |
| **Projects** | Maestro (`maestro/models.py:AgentType`), Arbiter (`config/agents.toml`) |
| **Blocks** | R-03 (MCP client) |
| **Effort** | **S** — change an enum in one of the projects + update config in the other |
| **Impact** | 🔴 — without this, routing through Arbiter is impossible |

**Solution options:**
1. Maestro renames `codex` → `codex_cli` (minimal blast radius — Arbiter has been stable for 2 months)
2. Arbiter renames `codex_cli` → `codex` (breaks existing data in SQLite)
3. Mapping layer in the MCP client (adds complexity, but touches neither project)

**Recommendation:** option 1 — change it in Maestro, since it is under active development.

---

#### R-02. Extend Maestro TaskConfig for compatibility with Arbiter

| | |
|---|---|
| **Description** | Arbiter requires `task_type` (7 enum), `language` (6 enum), `complexity` (5 enum) as required fields. Maestro TaskConfig does not have these fields. Also, `priority` is incompatible: Maestro — int(-100..100), Arbiter — enum(low/normal/high/urgent). |
| **Projects** | Maestro (`maestro/models.py:81-154`), Arbiter (`arbiter-core/src/types.rs`) |
| **Blocks** | R-03 (MCP client) |
| **Effort** | **M** — add fields to the Pydantic model + priority mapping + optional auto-inference from prompt/scope |
| **Impact** | 🔴 — without this, Arbiter will reject 100% of requests |

**Priority mapping details:**
- -100..−26 → `low`, −25..25 → `normal`, 26..75 → `high`, 76..100 → `urgent`

**Auto-inference option:**
- `language` can be determined from scope (*.py → python, *.rs → rust)
- `task_type` can be determined from prompt (keywords: "fix" → bugfix, "test" → test)
- `complexity` — heuristic based on scope_size / estimated_tokens

---

#### R-03. Arbiter MCP client in Maestro

| | |
|---|---|
| **Description** | Implement calls to `route_task` and `report_outcome` from Maestro. Arbiter already has a ready Python client (`orchestrator/arbiter_client.py`), which can be taken as a basis or imported. Decide the mode: advisory (with fallback to static routing) or authoritative. |
| **Projects** | Maestro (`maestro/scheduler.py`, `maestro/coordination/`), Arbiter (`orchestrator/arbiter_client.py`) |
| **Depends on** | R-01, R-02 |
| **Blocks** | R-05 (tests), R-07 (eval-driven routing) |
| **Effort** | **L** — new module in Maestro, change to scheduler.py, graceful fallback |
| **Impact** | 🔴 — the key ecosystem integration; without it, Arbiter is an isolated project |

**Architectural decision (from the existing analysis):**
A `RoutingStrategy` ABC is proposed, with implementations `StaticRouting` (current behavior) and `ArbiterRouting` (via MCP). Graceful fallback: if Arbiter is unavailable, static routing is used.

---

#### R-08. Fix the COWORK_CONTEXT.md documentation

| | |
|---|---|
| **Description** | The integration map shows Maestro→Arbiter and Maestro→ATP as existing links (arrows without notes). This is misleading. All unimplemented links must be marked `🔴 NOT IMPLEMENTED`. |
| **Projects** | Root `COWORK_CONTEXT.md:57-68` |
| **Blocks** | Nothing technically, but it blocks correct planning |
| **Effort** | **S** — text edit |
| **Impact** | 🔴 — inaccurate documentation leads to wrong assumptions during onboarding |

---

### P1 — Formalization

The ecosystem works, but the contracts are not formally pinned down.

---

#### R-04. Formalize the Maestro↔spec-runner contract

| | |
|---|---|
| **Description** | The only working integration rests on ad-hoc parsing: `.executor-state.json` is parsed via `state.get("tasks", {})` without typing, `executor.config.yaml` is generated from a dict without a shared schema, and the spec-runner version is not pinned. |
| **Projects** | Maestro (`maestro/orchestrator.py:406-438`, `maestro/models.py:716-763`), executor (`spec-runner`) |
| **Depends on** | Nothing (can start immediately) |
| **Blocks** | Stability of the only working integration |
| **Effort** | **M** — ExecutorState Pydantic model + pinned version + integration tests |
| **Impact** | 🟡 — works now, but may break with any spec-runner update |

**Actions:**
1. Create an `ExecutorState` Pydantic model in Maestro for `.executor-state.json`
2. Pin the `spec-runner` version in `Maestro/pyproject.toml`
3. Add contract tests: Maestro generates the config → spec-runner parses it (and vice versa)

---

#### R-05. Integration tests Maestro↔Arbiter

| | |
|---|---|
| **Description** | Neither project has tests for this link. Arbiter tests its client in isolation (PT-01..PT-07), but there are zero cross-project tests. |
| **Projects** | Maestro (`tests/`), Arbiter (`tests/`) |
| **Depends on** | R-03 (MCP client) |
| **Blocks** | Confidence in the integration |
| **Effort** | **M** — tests with a mock Arbiter + tests with a real Arbiter subprocess |
| **Impact** | 🟡 — without tests the integration will break with each update |

---

#### R-09. CI/CD for Maestro

| | |
|---|---|
| **Description** | Maestro is the most active project (daily commits), but the only one without CI/CD. 29 tests are run only manually. |
| **Projects** | Maestro (missing `.github/workflows/`) |
| **Depends on** | Nothing |
| **Blocks** | Refactoring safety for R-02, R-03 |
| **Effort** | **S** — GitHub Actions: pytest + ruff + pyrefly |
| **Impact** | 🟡 — without CI, regressions are found only during dogfooding |

---

#### R-10. CI/CD for Arbiter

| | |
|---|---|
| **Description** | 238 Rust tests + a Makefile with 150+ targets, but no automatic run. Although the project is stable, once integration starts (R-03) changes become inevitable. |
| **Projects** | Arbiter (missing `.github/workflows/`) |
| **Depends on** | Nothing |
| **Blocks** | Safety of changes during integration |
| **Effort** | **S** — GitHub Actions: cargo test + cargo clippy + ruff (Python) |
| **Impact** | 🟡 — Arbiter is stable, but CI is mandatory before integration |

---

### P2 — DX improvements

They don't block work, but they significantly speed up development.

---

#### R-11. Unified ecosystem onboarding guide

| | |
|---|---|
| **Description** | Each project has its own README, CLAUDE.md, COWORK_CONTEXT.md — but there is no single entry point for a developer who wants to bring up the whole ecosystem and understand how the projects are connected. |
| **Projects** | All |
| **Depends on** | R-08 (correct documentation) |
| **Effort** | **M** — a document with architecture, setup instructions, and a description of contracts |
| **Impact** | 🟢 — speeds up onboarding, but does not block development |

---

#### R-12. Setup script for the whole ecosystem

| | |
|---|---|
| **Description** | Automate bringing up the environment: `uv sync` for Python projects, `cargo build` for Arbiter, dependency checks (git, gh, Claude CLI). All projects use `uv` — this can be unified. |
| **Projects** | All |
| **Depends on** | Nothing |
| **Effort** | **S** — bash/Makefile script |
| **Impact** | 🟢 — quality-of-life |

---

#### R-13. Normalize guardrails: ATP ← Arbiter

| | |
|---|---|
| **Description** | ATP guardrails (`atp/evaluators/guardrails.py`) are "inspired by arbiter's invariant rules" — 3 rules. Arbiter has 10 invariants. The code is not shared. A shared invariants library could be extracted, or at least the naming/semantics aligned. |
| **Projects** | ATP (`atp/evaluators/guardrails.py`), Arbiter (`arbiter-core/src/invariant/`) |
| **Depends on** | Nothing |
| **Effort** | **M** — analysis + shared types or codegen |
| **Impact** | 🟢 — reduces duplication, but not critical |

---

### P3 — Strategic

Long-term improvements to the ecosystem architecture.

---

#### R-06a. ATP verification via validation_cmd (quick win)

| | |
|---|---|
| **Description** | Add documentation and an example config `validation_cmd: "atp run suite.yaml"` in Maestro. Requires no code changes — only a YAML config and documentation. The ATP CLI is already ready. |
| **Projects** | Maestro (examples/), ATP (CLI) |
| **Depends on** | Nothing (the ATP CLI works autonomously) |
| **Effort** | **S** — documentation + YAML example |
| **Impact** | 🟡 — gives access to ATP evaluation without a single line of code |

> **Note:** Moved from P3 to P1 based on verification results. The CLI path with 0 lines of code should not wait for R-03.

---

#### R-06b. Agent benchmarking via ATP (reformulated 2026-04-25)

> **Reformulated.** The original description — "ATP verification via SDK" — was inaccurate: the ATP SDK is a **participant** client of the benchmark, not a validator client. Three features had been conflated under the name R-06b (validation deepening / agent benchmarking / Maestro-as-participant); the design doc in `_cowork_output/decisions/2026-04-25-r06b-design.md` pins down the choice of F2 (agent benchmarking). Below is the new formulation.

| | |
|---|---|
| **Description** | Maestro runs its spawned agents (claude_code/codex_cli/aider) through an external ATP benchmark. `BenchmarkResult` (agent_id, benchmark_id, score, per_task, cost) goes to Arbiter as a new routing signal. |
| **Projects** | Maestro (new `maestro/benchmark/`), ATP (SDK is ready: `atp_sdk.ATPClient`) |
| **Depends on** | R-03 ✅, design doc approved |
| **Effort** | **M0** design ✅ done · **M1** thin slice (Mock + scaffold) S–M · **M2** spawner integration M · **M3** auth + live ATP S · **M4** Arbiter feedback wiring M · **M5** CLI S |
| **Impact** | 🟡 — gives Arbiter a new per-agent-per-benchmark signal; unblocks R-07 (eval-driven routing uses BenchmarkResult as a weighting input) |

---

#### R-07. Eval-driven routing validation (Arbiter↔ATP)

| | |
|---|---|
| **Description** | A/B testing of the quality of Arbiter's decisions via ATP: DT routing vs random vs always-best-agent. ~200 LOC in `scripts/eval_routing.py`. Planned as ECO-3 in the Arbiter roadmap. |
| **Projects** | Arbiter (`SUGGESTIONS.md:70-83`), ATP |
| **Depends on** | R-06 (ATP verification), R-03 (MCP client) |
| **Effort** | **L** — test suites + scripts + analysis |
| **Impact** | 🟡 — allows objectively assessing the value of Arbiter for the ecosystem |

---

#### R-14. Shared type library

| | |
|---|---|
| **Description** | Extract common types (TaskInput, AgentStatus, OutcomeReport) into a shared Python package imported by Maestro and ATP. Arbiter (Rust) generates JSON Schema from serde — the shared package can validate against it. |
| **Projects** | All |
| **Depends on** | R-01, R-02 (schema stabilization) |
| **Effort** | **XL** — new package, revision of all models, CI for shared types |
| **Impact** | 🟡 — eliminates mismatches once and for all, but expensive |

---

#### R-15. Declarative agent-infra.yaml

| | |
|---|---|
| **Description** | A single file describing the entire ecosystem: which agents are available, their capabilities, routing policies, ATP test suites, observability endpoints. Right now this is smeared across `tasks.yaml`, `agents.toml`, `invariants.toml`, ATP configs. |
| **Projects** | All |
| **Depends on** | R-14 (shared types), R-03 (integration works) |
| **Effort** | **XL** — format design, parsers in each project, config migration |
| **Impact** | 🟢 — strategic goal, but premature before integrations stabilize |

---

#### R-16. Monorepo vs multi-repo decision

| | |
|---|---|
| **Description** | Right now the projects sit side by side but do not form a monorepo: no shared workspace, no cross-project CI, no shared dependency management. A decision is needed: formalize as a monorepo (uv workspace, unified CI) or keep multi-repo with contract tests at the boundaries. |
| **Projects** | All |
| **Depends on** | R-14 (shared types — if monorepo), R-05 (contract tests — if multi-repo) |
| **Effort** | **XL** — architectural decision + migration |
| **Impact** | 🟢 — determines the long-term strategy, but does not block current work |

---

## Dependency diagram

```
                    ╔═══════════════════════════════════════════════════╗
                    ║          CAN START IMMEDIATELY (in parallel)      ║
                    ╚═══════════════════════════════════════════════════╝

          ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
          │ R-08 Docs        │   │ R-09 CI Maestro │   │ R-10 CI Arbiter │
          │ COWORK_CONTEXT  │   │ GitHub Actions   │   │ GitHub Actions   │
          │ Effort: S       │   │ Effort: S ⚡     │   │ Effort: S        │
          └────────┬────────┘   └─────────────────┘   └─────────────────┘
                   │
          ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
          │ R-11 Onboarding │   │ R-12 Setup script│   │R-06a ATP CLI    │
          │ guide           │   │ Effort: S        │   │ quick win       │
          │ Effort: M       │   └─────────────────┘   │ Effort: S       │
          └─────────────────┘                          └─────────────────┘

          ┌─────────────────┐
          │ R-04 Formalize   │ ◄── can start immediately
          │ spec-runner      │
          │ Effort: M        │
          └─────────────────┘

                    ╔═══════════════════════════════════════════════════╗
                    ║              CRITICAL PATH (sequential)           ║
                    ╚═══════════════════════════════════════════════════╝

          ┌─────────────────┐
          │ R-01 Normalize   │ ◄── START HERE
          │ agent IDs        │
          │ Effort: S  🔴    │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ R-02 Extend      │
          │ TaskConfig       │
          │ Effort: M  🔴    │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ R-03 MCP client  │
          │ Arbiter in Maestro│
          │ Effort: L  🔴    │
          └────────┬────────┘
                   │
            ┌──────┴──────┐
            │             │
            ▼             ▼
   ┌────────────────┐  ┌─────────────────┐
   │ R-05 Integration│  │ R-06b ATP SDK   │
   │ tests M↔A      │  │ integration      │
   │ Effort: M  🟡   │  │ Effort: M  🟡    │
   └────────────────┘  └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ R-07 Eval-driven │
                       │ routing A↔ATP    │
                       │ Effort: L  🟡    │
                       └─────────────────┘

                    ╔═══════════════════════════════════════════════════╗
                    ║              STRATEGIC (after stabilization)      ║
                    ╚═══════════════════════════════════════════════════╝

   R-01 + R-02 ──▶ ┌─────────────────┐
                    │ R-14 Shared types│
                    │ Effort: XL  🟡   │
                    └────────┬────────┘
                             │
                  ┌──────────┴──────────┐
                  │                     │
                  ▼                     ▼
         ┌────────────────┐   ┌─────────────────┐
         │ R-15 agent-     │   │ R-16 Mono/Multi  │
         │ infra.yaml      │   │ repo decision    │
         │ Effort: XL 🟢   │   │ Effort: XL 🟢    │
         └────────────────┘   └─────────────────┘

   R-13 Guardrails ◄── can be done at any time (Effort: M, 🟢)
```

---

## Summary table

| ID | Task | Projects | Depends on | Effort | Impact | Priority |
|----|--------|---------|------------|--------|--------|-----------|
| R-01 | Normalize agent IDs | Maestro, Arbiter | — | S | 🔴 | P0 |
| R-02 | Extend TaskConfig | Maestro, Arbiter | R-01 | M | 🔴 | P0 |
| R-03 | Arbiter MCP client in Maestro | Maestro, Arbiter | R-01, R-02 | L | 🔴 | P0 |
| R-08 | Fix documentation | COWORK_CONTEXT.md | — | S | 🔴 | P0 |
| R-04 | Formalize spec-runner contract | Maestro, executor | — | M | 🟡 | P1 |
| R-05 | Integration tests M↔A | Maestro, Arbiter | R-03 | M | 🟡 | P1 |
| R-09 | CI/CD for Maestro | Maestro | — | S | 🟡 | P1 |
| R-10 | CI/CD for Arbiter | Arbiter | — | S | 🟡 | P1 |
| R-06a | ATP verification (CLI quick win) | Maestro, ATP | — | S | 🟡 | P1 |
| R-06b | ATP verification (SDK integration) | Maestro, ATP | R-03 | M–L | 🟡 | P3 |
| R-07 | Eval-driven routing | Arbiter, ATP | R-06b, R-03 | L | 🟡 | P3 |
| R-11 | Onboarding guide | All | R-08 | M | 🟢 | P2 |
| R-12 | Setup script | All | — | S | 🟢 | P2 |
| R-13 | Normalize guardrails | ATP, Arbiter | — | M | 🟢 | P2 |
| R-14 | Shared type library | All | R-01, R-02 | XL | 🟡 | P3 |
| R-15 | agent-infra.yaml | All | R-14, R-03 | XL | 🟢 | P3 |
| R-16 | Monorepo vs multi-repo | All | R-14 / R-05 | XL | 🟢 | P3 |

---

## Recommended execution plan

### Sprint 1 (week 1–2): Unblocking

In parallel:
- **R-01** (S) — normalize agent IDs
- **R-08** (S) — fix documentation
- **R-09** (S) — CI/CD for Maestro *(higher priority than R-10: daily commits without CI)*
- **R-10** (S) — CI/CD for Arbiter
- **R-06a** (S) — ATP verification via CLI (quick win, 0 lines of code)
- **R-04** (M) — start formalizing the spec-runner contract

### Sprint 2 (week 3–4): Integration foundation

Sequentially (R-09 already provides a safety net):
- **R-02** (M) — extend TaskConfig
- **R-04** (M) — finish formalizing spec-runner

### Sprint 3 (week 5–8): Key integration

- **R-03** (L) — Arbiter MCP client in Maestro

### Sprint 4 (week 9–10): Validation

In parallel:
- **R-05** (M) — integration tests M↔A
- **R-06b** (M) — ATP verification via SDK

### Next: by priority and capacity

- R-07 → R-14 → R-15/R-16 (strategic, as they become ready)

---

*Generated from the reports: `_cowork_output/contracts/contract-analysis.md`, `_cowork_output/integration/integration-health.md`, `_cowork_output/status/2026-04-05-status.md`*
