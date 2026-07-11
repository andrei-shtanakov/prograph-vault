---
title: authored/ — guardrail
type: rule
status: living
owner: Andrei
updated: 2026-07-05
---

# authored/ — written by HUMANS

Everything here is edited by humans via **git-review (PR)**. Writing here from tools is **forbidden**
(prograph and auto-skills write to `../derived/`).

## Subfolders

| Folder | What it holds | SSOT? |
|---|---|---|
| `rules/` | cross-cutting rules: `code-style.md`, `gui.md`, `tui.md`, `libraries.md`, `repo-boundaries.md`, `git-workflow.md` | ✅ KB owns |
| `decisions/` | ADRs (cross-repo), `YYYY-MM-DD-adr-<slug>.md` | ✅ cross-repo *why* |
| `templates/` | spec templates, steward profiles (`lite`/`team`), scaffolds | ✅ SSOT of profiles |
| `skills/` | project-specific skills: sources/docs OR pointers to Cowork skills | ⚠️ runtime — owned by the skills mechanism |
| `notes/` | plans, intentions, cross-cutting TODOs | ✅ (repo-local TODOs — in the repo) |
| `registry/` | COWORK_CONTEXT (registry + integration map) | ✅ KB owns |

## Rules

- Repo-local rules do **not** go here — they live in the corresponding repo's CLAUDE.md.
- Contracts do **not** go here as authority — authority is in the producing repo; the snapshot goes in `derived/`.
- Obsolete → `<subfolder>/archive/` with `archived:`/`reason:` in the frontmatter. Do not delete.
- Every file has frontmatter (`title/type/status/owner/updated`), see `../CLAUDE.md` §7.
