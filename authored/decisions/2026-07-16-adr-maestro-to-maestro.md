---
title: Maestro -> maestro repository/path lowercase rename
type: adr
status: accepted
owner: Andrei
updated: 2026-07-16
---

# TL;DR

- Rename scope is repository/path identity: `Maestro` -> `maestro`.
- Python package, import package, and CLI command are already canonical lowercase `maestro`; no package/CLI rename is needed.
- Human-facing product name remains `Maestro` unless a string is a path, repo slug, remote URL, or workspace target.
- Historical notes and dated reports keep old `Maestro/` paths unless they are active runbooks or living maps.

# ADR: Maestro repository/path lowercase rename

## Context

The workspace currently has a top-level repo directory `Maestro/` with remote
`git@github.com:andrei-shtanakov/Maestro.git`. The Python project is already
lowercase:

- `pyproject.toml`: `name = "maestro"`;
- import package: `maestro`;
- CLI command: `maestro`;
- project URLs already point to `https://github.com/andrei-shtanakov/maestro`.

The remaining mismatch is the repo slug/local directory and many cross-repo
path references. This rename should be smaller than the Libretto rename: it is
not a language/package/contract namespace migration.

## Decision

Use `maestro` as canonical repo slug and local directory name:

| Surface | Old | New | Policy |
|---|---|---|---|
| GitHub repo slug | `andrei-shtanakov/Maestro` | `andrei-shtanakov/maestro` | rename after core docs are clean |
| Local directory | `Maestro/` | `maestro/` | rename with remote change |
| Workspace manifest app key | `[apps.Maestro]` | `[apps.maestro]` | update after local dir rename |
| Path references | `Maestro/...`, `../Maestro/` | `maestro/...`, `../maestro/` | update active docs/tools |
| Python package | `maestro` | `maestro` | no change |
| CLI | `maestro` | `maestro` | no change |
| Product/brand text | `Maestro` | `Maestro` | keep title case in prose/UI/logs |

## Consequences

- This is a low-risk rename compared with a package rename because imports and
  commands do not change.
- Devtools that locate the workspace by `Maestro/` must be changed with the
  local directory rename.
- Cross-repo contract paths under `maestro/contracts/...` must be updated in
  active docs and scripts, but historical status reports can remain unchanged.
- GitHub redirects will likely cover old URLs, but active docs should not rely
  on redirects.

## Migration Order

1. Inventory exact path/remote references.
2. Confirm the decision boundary: lowercase repo/path only, title-case brand stays.
3. Prepare a core branch in `Maestro` for repo-local path/remote docs that can
   be changed before the actual directory rename.
4. Rename GitHub repo `Maestro` -> `maestro`.
5. Set local remote to `git@github.com:andrei-shtanakov/maestro.git`.
6. Rename local directory `Maestro/` -> `maestro/`.
7. Update workspace/KB/downstream active path references.

## Non-Goals

- Do not lowercase all occurrences of `Maestro` in README/docs/code comments.
- Do not change the Python package, CLI command, entry points, or import names.
- Do not rewrite historical archives/status reports unless they are published
  as living/current indices.
