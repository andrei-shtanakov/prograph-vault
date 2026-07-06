---
title: derived/ — guardrail
type: rule
status: living
owner: prograph (auto)
updated: 2026-07-05
---

# derived/ — written by TOOLS

> ⚠️ **Do not edit by hand.** The contents are overwritten by tools. Manual edits will be lost. If you
> want to record knowledge — it goes in `../authored/`.

## Subfolders

| Folder | Written by | What |
|---|---|---|
| `graph/` | prograph | project structure: deps, contracts, MCP calls |
| `contracts/` | prograph / vendor scripts | contract **snapshots** for search (NOT authority — that is in the producing repo) |
| `projects/` | prograph | auto-facts per repo |
| `journal/` | kb-save skill | per-project activity log — **append-only, NOT regenerable** (the one exception; see ADR 2026-07-06) |
| `digests/` | digest skills | claude-kb digests |

## Rules

- A tool writes **only** to its own `derived/` subfolder; writing to `../authored/` is forbidden.
- A contract snapshot is tagged with the source and the hash/version of the original (traceability to the owner).
- `derived/` is regenerated — do not store anything here that cannot be reproduced from the sources.
  **Exception:** `journal/` is append-only human-caused narrative written by `kb-save`; prograph must
  not touch it. Curation/archival is by `kb-curator`.
