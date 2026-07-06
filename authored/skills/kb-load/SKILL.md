---
name: kb-load
description: Proactively warm up context from the Ecosystem KB (prograph-vault) when starting work on a known area — interfaces, cross-cutting rules, contracts, or established patterns for the current project. Loads the relevant bundle at once (applicable rules + this project's facts/interfaces + related contracts + recent journal). Use at the start of a work area; for a single targeted question use kb-search instead.
allowed-tools: Bash, Read, Grep, Glob
---

# kb-load — warm up work-area context from the KB

Front-loads the set of KB knowledge relevant to what you are about to work on, so the rules,
interfaces and patterns are in context before you start. This is the **proactive bulk** counterpart
to `kb-search` (which answers one ad-hoc question).

## Step 0 — Locate the KB and the project

```bash
_kb() { local d; d="$(pwd -P)"; while [ "$d" != "/" ]; do
    [ -d "$d/prograph-vault/authored" ] && { printf '%s\n' "$d/prograph-vault"; return 0; }
    [ -d "$d/authored" ] && [ -f "$d/CLAUDE.md" ] && [ "$(basename "$d")" = prograph-vault ] && { printf '%s\n' "$d"; return 0; }
    d="$(dirname "$d")"; done; return 1; }
KB_ROOT="${KB_ROOT:-$(_kb)}"
[ -z "$KB_ROOT" ] && { echo "ℹ️  prograph-vault not found — continuing without the KB."; exit 0; }
source "$KB_ROOT/authored/skills/kb-utils/kb-env.sh"
PROJECT="$(kb_project "${1:-}" || true)"
```

`PROJECT` = explicit argument, else the current ecosystem repo. `TOPIC` = the rest of the argument
or the conversation context (e.g. `gui`, `tui`, `contracts`, `code-style`, an interface name).

## Step 1 — Load the relevant bundle (read these into context)

Pull the pieces that match the project and topic — do not read the whole KB:

```bash
# Cross-cutting rules (all, or the ones matching the topic: gui/tui/code-style/libraries)
ls "$KB_ROOT/authored/rules/"
# read the applicable ones, e.g.:
#   Read "$KB_ROOT/authored/rules/<topic>.md"

# This project's facts / interfaces (written by prograph)
ls "$KB_ROOT/derived/projects/${PROJECT}"* 2>/dev/null

# Contracts this project produces or consumes (snapshots — authority is in the producing repo)
kb_grep "${PROJECT}" "$KB_ROOT/derived/contracts" 2>/dev/null

# Recent activity for this project
tail -n 60 "$KB_ROOT/derived/journal/${PROJECT}/journal.md" 2>/dev/null

# Templates / scaffolds, when present
ls "$KB_ROOT/authored/templates/" 2>/dev/null
```

Use `Read`/`Grep` to open the files the listings surface. Prefer the topic-relevant subset.

## Step 2 — Summarize what was loaded

- Which files were pulled in (paths).
- Key rules / interfaces / patterns that apply here (3–6 bullets).
- Anything expected but missing — if the area is new to the KB, suggest `/kb-save` to record work as
  it happens.

Reading and search are unrestricted across the whole KB. This skill **does not write**.
