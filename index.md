---
title: Ecosystem KB — index
type: registry
status: living
owner: Andrei
updated: 2026-07-08
---

# Ecosystem KB

Unified knowledge base of the AI-orchestrators ecosystem. Maintenance rules — see `CLAUDE.md`.

## Navigation

**authored/** — owned by humans (git-review):
- [rules/](authored/rules/) — cross-cutting rules: code-style, gui, tui, libraries
- [decisions/](authored/decisions/) — ADRs (cross-repo)
- [templates/](authored/templates/) — spec templates, steward profiles, scaffolds
- [skills/](authored/skills/) — project-specific skills / pointers
- [notes/](authored/notes/) — plans, intentions, cross-cutting TODOs
- [registry/](authored/registry/) — project registry (COWORK_CONTEXT)

**derived/** — written by tools (do not touch by hand):
- [graph/](derived/graph/) — structure/dependencies (prograph)
- [contracts/](derived/contracts/) — contract snapshots (not authority)
- [projects/](derived/projects/) — auto-facts per repo
- [digests/](derived/digests/) — digests

## Quick rules

1. authored is written by humans, derived by tools. Do not mix.
2. The KB references contracts, it does not own them.
3. Repo-local rules go in the repo's CLAUDE.md; the KB holds only cross-cutting knowledge.
4. Nothing is deleted — archive with a date + reason.

## Migration status

- [x] `git init`, authored/derived skeleton
- [x] Migrate from `_cowork_output/` (decisions, roadmap, status, contract snapshots)
- [x] Reclassify current contracts/projects/mcp_patterns → authored|derived
- [x] COWORK_CONTEXT → `authored/registry/` (`registry.md`, 2026-07-08); index.md is the root pointer
- [x] Register the KB in the registry (`prograph-vault` listed in `authored/registry/registry.md`)

Migration complete (2026-07-08). Ongoing upkeep is handled by the `kb-curator` freshness audit.
