---
title: State of the AI Orchestrators ecosystem projects
type: note
status: archived
owner: Andrei
updated: 2026-04-16
archived: 2026-07-06
reason: historical status snapshot (bulk-archived on graduation from _cowork_output)
---

# State of the AI Orchestrators ecosystem projects

> Date: 2026-04-16

## TL;DR

1. **atp-platform** — the most active project. Branch `feat/tournament-reasoning` with uncommitted changes, active work on game-theoretic evaluation and CI stabilization. Version 1.0.0 GA.
2. **Maestro** — 4 unpushed commits on master (R-03 design of the Arbiter integration). The Maestro↔Arbiter integration remains the **main blocker** of the ecosystem.
3. **arbiter** — stable, master synced with origin. Documentation and security updated. Waiting for the MCP client on the Maestro side (R-03).
4. **Secondary projects** (proctor-a, spec-runner, open-prose) — low activity, last commits April 6–16, mostly docs/fixes.
5. **New folders** absent from the registry: `Maestro-r03-arbiter` (worktree), `agents-for-game` (ATP-tournament demo) — recommend adding to COWORK_CONTEXT.md.

---

## Main projects

### atp-platform (v1.0.0 GA)

| Parameter | Value |
|----------|---------|
| Branch | `feat/tournament-reasoning` (NOT main!) |
| Last commit | Apr 16 — `feat(tournaments): capture per-move reasoning via MCP` |
| Uncommitted changes | 7 modified + 12 untracked |
| Sync with remote | On the feature branch |

**What is happening:** Active development of game-theoretic evaluation — Battle of Sexes added, reasoning captured via MCP. In parallel, CI stabilization: separation of flaky e2e/container tests from the coverage gate, marking of unstable TUI tests.

**Modified files:** `.gitignore`, `AGENTS.md`, `CLAUDE.md`, `TODO.md`, `packages/atp-sdk/pyproject.toml`, `pyproject.toml`, `uv.lock` — looks like an unfinished session with a dependency bump.

**Risk:** Work is being done on a feature branch with uncommitted changes. A context switch could lose progress.

---

### Maestro (v0.1.0 Alpha)

| Parameter | Value |
|----------|---------|
| Branch | `master` (ahead of origin by 4 commits) |
| Last commit | Apr 16 — `chore: ignore .worktrees/` |
| Uncommitted changes | Only untracked (COWORK_CONTEXT.md, SUGGESTIONS.md, TODO.md) |
| Sync with remote | **4 commits not pushed** |

**What is happening:** A series of R-03 commits — design of the Arbiter MCP integration:
- `docs(R-03): design — Arbiter MCP client integration`
- `docs(R-03): apply review round 1 — mode-aware retry, routed_agent_type, cross-repo contract`
- `docs(R-03): add implementation plan`

The Maestro↔spec-runner contract (R-04) was also formalized and task-classification fields for Arbiter (R-02) were added.

**Risk:** 4 commits on master are not pushed. If something happens to the local copy — loss of the R-03 project documents.

---

### arbiter (v0.1.0 Stable MVP)

| Parameter | Value |
|----------|---------|
| Branch | `master` (up to date with origin) |
| Last commit | `docs: audit and sync documentation with codebase` |
| Uncommitted changes | 1 modified (CLAUDE.md) + 9 untracked |
| Sync with remote | ✅ Synced |

**What is happening:** The project is stabilized. The last cycle — documentation audit, updating vulnerable Python dependencies, typed DTOs for the Maestro integration (commit `861534e`), 12 golden test fixtures. Performance: >10k decisions/sec, <5ms p99.

**Blocker:** Waiting for the R-03 landing on the Maestro side. The arbiter side is ready for integration.

---

## Auxiliary projects

| Project | Branch | Last commit | Dirty? | State |
|--------|-------|------------------|--------|-----------|
| **proctor-a** | master (synced) | Apr 16 — fix tests | Yes (CLAUDE.md + untracked) | Phase 2 in progress, microkernel + event bus. Low activity |
| **spec-runner** | master (synced) | Apr 6 — docs audit | Yes (4 modified + untracked) | v2.0.0 released. Stable, maintenance mode |
| **open-prose** | main (synced) | Apr 7 — "plagin test" | Yes (modified phase-1.md) | Specification, no runtime. Minimal activity |
| **Maestro-r03-arbiter** | worktree of Maestro | — | Unknown | Git worktree for R-03 development. **Not in the registry** |
| **agents-for-game** | not a git repo | — | — | Demo: two Claude agents play Prisoner's Dilemma via ATP MCP. **Not in the registry** |
| **spec-runner-tasks** | not a git repo | — | — | Documentation/tasks for spec-runner. **Not in the registry** |

---

## Critical-path map

```
Arbiter (ready) ──────┐
                      ├──▶ R-03: MCP client in Maestro ──▶ Integration ──▶ E2E
Maestro (design done) ┘                                         │
                                                                 ▼
                                                    R-06: ATP as validator
                                                         │
                                                         ▼
                                                    Full pipeline:
                                                    Task → Route → Execute → Validate
```

**Main blocker:** R-03 (MCP client in Maestro). The design is ready, the implementation plan is written, but the code has not started yet. Maestro has 4 unpushed commits with design documents.

---

## Recommended actions

1. **Maestro → `git push`** — 4 commits on master are not pushed, which is a risk of losing the R-03 design documents.
2. **atp-platform → commit or stash** — 7 modified files on the feature branch, including `pyproject.toml` and `uv.lock`.
3. **Update COWORK_CONTEXT.md** — add `agents-for-game` (ATP tournament demo) and `Maestro-r03-arbiter` (worktree) to the registry.
4. **R-03 implementation** — the next logical step for the ecosystem. Arbiter is ready, the Maestro design is ready, an MCP client implementation is needed.
5. **spec-runner** — 4 modified files (including `src/__init__.py`) are hanging uncommitted. Worth sorting out — is this unfinished work or forgotten changes.
