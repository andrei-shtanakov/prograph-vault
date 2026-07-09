---
title: registry/ — guardrail
type: rule
status: living
owner: Andrei
updated: 2026-07-08
---

# registry/ — project registry (COWORK_CONTEXT)

The KB-owned SSOT for the **ecosystem project registry + integration map**: what repos exist, their
role/status, and how they connect. Human-authored, git-reviewed.

## Files

- [`registry.md`](registry.md) — the project registry + integration map (this folder's main doc).

## Boundaries

- **This is a human-curated overview, not structural authority.** Machine-detected structure
  (package deps, MCP calls, contract links) is owned by **prograph** in `../../derived/graph/` and
  `../../derived/projects/`. The registry *references* that, it does not restate it as truth.
- **Contracts** are owned by their producing repos; the registry only points to them.
- Per-repo detail belongs in each repo's own `COWORK_CONTEXT.md` / `CLAUDE.md`; the registry holds the
  cross-cutting map only.
- Update on schedule (kb-curator freshness audit) or when repos are added/removed/re-roled.
