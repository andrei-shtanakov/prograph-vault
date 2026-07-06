---
title: 'Sync: all_ai_orchestrators → Linear (LABS)'
type: note
status: archived
owner: Andrei
updated: 2026-04-15
archived: 2026-07-06
reason: Linear tracking frozen — historical
---

# Sync: all_ai_orchestrators → Linear (LABS)

> 2026-04-15 · Author: Cowork (Claude)

## TL;DR

- The Linear workspace has only one team — **Labs** (key `LABS`). It already contained 4 projects: ATP Platform, Arbiter, Maestro, spec-runner (54 issues in total).
- For ATP Platform, **11 issues** are closed (auth, security, CI, circular deps). For Maestro/Arbiter/spec-runner — 0 closed, backlog only.
- Created an umbrella project **`all_ai_orchestrators`** (team: Labs) — for cross-project and ecosystem tasks.
- Filed **10 issues** (LABS-55..64): inventory, integration gaps, missing Linear projects, contracts, CI synchronization, summary of completed work.
- Main mismatches with the actual folder: `proctor-a`, `open-prose`, `agents-for-game` are not reflected in Linear; `executor` and `pylon` are declared in COWORK_CONTEXT.md but absent from the folder.

## State of Linear at the starting point

| Project | Team | Issues (total) | Done | Backlog/Todo |
|---|---|---:|---:|---:|
| ATP Platform | Labs | 23 | 11 | 12 |
| Maestro | Labs | 10 | 0 | 10 |
| Arbiter | Labs | 10 | 0 | 10 |
| spec-runner | Labs | 10 | 0 | 10 |
| Onboarding (LABS-1..4) | Labs | 4 | 0 | 4 |

## Folder ↔ Linear mapping

| Folder | Language | Linear project | Comment |
|---|---|---|---|
| `atp-platform/` | Python | ATP Platform | In progress, 1.0 GA |
| `Maestro/` | Python | Maestro | Active Beta |
| `arbiter/` | Rust+Python | Arbiter | Stable MVP |
| `spec-runner/` | Python | spec-runner | Active development, but mentioned in COWORK_CONTEXT only as a dev dependency |
| `proctor-a/` | Python | ❌ none | See LABS-59 |
| `open-prose/` | Markdown | ❌ none | See LABS-60 |
| `agents-for-game/` | Python | ❌ none | See LABS-61 |
| *(not in folder)* | — | — | `executor/`, `pylon/` — declared in COWORK_CONTEXT, physically absent |

## Created project

**Linear:** <https://linear.app/atp-platform-project/project/all-ai-orchestrators-76eebdc969e5>

Purpose — a coordination umbrella: cross-project issues, inventory, integration gaps, recording completed work. Not an implementation project.

## Created issues

| ID | Priority | Topic |
|---|---|---|
| LABS-55 | High | Ecosystem inventory: 7 projects in the folder, 4 in Linear |
| LABS-56 | Medium | Mismatch COWORK_CONTEXT.md ↔ folder (executor/pylon absent; spec-runner/agents-for-game not in the registry) |
| LABS-57 | High | Integration gap: Maestro ↔ Arbiter (`route_task` MCP) not implemented — linked to LABS-53 |
| LABS-58 | Medium | Integration gap: Maestro ↔ ATP (`verify`) not implemented — linked to LABS-47 |
| LABS-59 | Medium | Set up a Linear project for `proctor-a` |
| LABS-60 | Low | Set up a Linear project for `open-prose` |
| LABS-61 | Low | Decide the fate of `agents-for-game` |
| LABS-62 | — (Done) | Summary of completed work: ATP Platform — 11 closed issues |
| LABS-63 | Medium | A single "Ecosystem Contracts" artifact |
| LABS-64 | Low | Synchronize CI/CD across sub-projects (linked to LABS-44, LABS-32) |

## Decisions 2026-04-15 (follow-up)

| Project | Decision | Actions |
|---|---|---|
| `agents-for-game` | **Don't track** — sandbox/learning directory | LABS-61 Canceled; in COWORK_CONTEXT as a one-line sandbox |
| `proctor-a` | **Separate Linear project** | [proctor-a](https://linear.app/atp-platform-project/project/proctor-a-6844cfdf6443) created; filed LABS-65..71 (7 issues for Phase 2-4); LABS-59 closed Done |
| `open-prose` | **No separate project** — 2 roadmap issues in the umbrella (P1, P2) | LABS-72 (P1), LABS-73 (P2, blocked by 72); LABS-60 closed Done. Revisit once a compiler/VM appears |

## Created project proctor-a (7 issues)

| ID | Phase | P | Topic |
|---|---|---|---|
| LABS-65 | 2 | High | Router (event → workflow) |
| LABS-66 | 2 | Med | WebhookTrigger |
| LABS-67 | 2 | High | LiteLLM full wiring |
| LABS-68 | 3 | Med | NATS transport |
| LABS-69 | 3 | Med | Worker pool + task queue |
| LABS-70 | 3 | Med | MCP tools (link with Arbiter / LABS-57) |
| LABS-71 | 4 | Low | WorkflowMode `fsm` |

## Recommended actions

1. **Maestro:** close the Arbiter integration gap (LABS-53 + umbrella LABS-57); this unblocks `verify` via ATP (LABS-58).
2. **Arbiter / spec-runner:** start the first wave of execution — with 0 closed so far, the pace lags well behind ATP Platform.
3. **proctor-a:** start with LABS-67 (LiteLLM) — this unblocks the rest of Phase 2. In parallel — LABS-65 (Router), since without it webhook/telegram won't scale.
4. **Ecosystem:** assemble the first version of "Ecosystem Contracts" (LABS-63) — a prerequisite for contract tests.
5. **COWORK_CONTEXT.md** (LABS-56): update the registry — remove `executor`/`pylon`, add `proctor-a` as Early Dev with a Linear link, mark `agents-for-game` as a sandbox.
