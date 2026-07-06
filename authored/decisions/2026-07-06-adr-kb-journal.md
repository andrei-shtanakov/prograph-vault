---
title: Per-project activity journal in derived/journal (kb-save)
type: adr
status: accepted
owner: Andrei
updated: 2026-07-06
---

# ADR: `derived/journal/<project>/` — a tool-written, append-only project journal

## Context

The KB constitution (§1–§2) enforces a hard binary: `authored/` is written only by humans (via
git-review), `derived/` is written only by the prograph tool and is **regenerable** (§ `derived/README.md`:
"do not store anything here that cannot be reproduced from the sources").

The `kb-save` skill records **significant project actions** (decisions, interface/contract changes,
new components, migrations, status changes, notable results) from within each ecosystem sub-project.
This log is:

- **tool-written** (by kb-save) → it cannot live in `authored/` without breaking golden rule #1;
- **not regenerable** — it is session narrative, not derivable from source → it does not fit the
  existing `derived/` "regenerable" contract, and it must not collide with what prograph regenerates
  in `derived/projects/`.

So it fits neither bucket cleanly.

## Decision

Introduce **`derived/journal/<project>/`** as a new tool-owned area:

- **Writer:** the `kb-save` skill (a *second* automated writer under `derived/`, alongside prograph).
  Each tool still writes only to its own `derived/` subfolder, per the existing guardrail.
- **Layout:** one append-only `journal.md` per project, newest entry at the bottom (tail-friendly),
  frontmatter `type: journal`, `source: kb-save`.
- **Scope:** kb-save writes only about the project the session is working on — never another
  project's activity.
- **Not authoritative, not regenerable:** the journal is an explicit, documented **exception** to the
  "`derived/` is regenerable" rule. prograph must not touch `derived/journal/`.
- **No auto-commit:** kb-save writes the file only; committing/curating is a separate step
  (`kb-curator`).
- **Lifecycle:** `kb-curator` may prune/archive stale entries per the normal archival rules (§6) —
  nothing is deleted, only archived with date + reason.

## Consequences

- `derived/README.md` gains a `journal/` row marked append-only / not-regenerable.
- `CLAUDE.md` §2/§3/§4/§9 note the journal area and kb-save as a `derived/` writer.
- The `authored/decisions/` directory is created by this ADR (progressing the §-index migration).
- Reading and searching the journal are unrestricted (kb-load/kb-search); only *writing* is
  project-scoped.

## Alternatives considered

- **`derived/projects/<project>/`** — reuse prograph's area. Rejected: prograph regeneration would
  overwrite the journal.
- **`authored/notes/<project>/`** — rejected: breaks golden rule #1 (authored is human-only).
- **New top-level `journal/`** outside `authored/`/`derived/` — rejected: adds a third top-level
  class; the "who writes it" rule already places tool output under `derived/`.
