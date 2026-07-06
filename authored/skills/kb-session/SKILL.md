---
name: kb-session
description: Orient the session in the Ecosystem KB (prograph-vault) at start. Called automatically via a SessionStart hook. Read-only — detects the current project, surfaces applicable cross-cutting rules and the latest project journal entries, and points to /kb-load, /kb-save, /kb-search. Never writes to the KB.
allowed-tools: Bash, Read, Grep, Glob
user-invocable: false
---

# kb-session — orient in the Ecosystem KB

Lightweight, **read-only** orientation for the current project against the shared KB
(`prograph-vault`). Loads nothing heavy — just enough to know what the KB already holds. For a full
context warm-up use `/kb-load`; to record work use `/kb-save`; for a targeted lookup use `/kb-search`.

## Step 0 — Locate the KB

```bash
_kb() { local d; d="$(pwd -P)"; while [ "$d" != "/" ]; do
    [ -d "$d/prograph-vault/authored" ] && { printf '%s\n' "$d/prograph-vault"; return 0; }
    [ -d "$d/authored" ] && [ -f "$d/CLAUDE.md" ] && [ "$(basename "$d")" = prograph-vault ] && { printf '%s\n' "$d"; return 0; }
    d="$(dirname "$d")"; done; return 1; }
KB_ROOT="${KB_ROOT:-$(_kb)}"
[ -z "$KB_ROOT" ] && { echo "ℹ️  prograph-vault not found — continuing without the KB."; exit 0; }
source "$KB_ROOT/authored/skills/kb-utils/kb-env.sh"
PROJECT="$(kb_project || true)"
echo "KB: $KB_ROOT | project: ${PROJECT:-<unknown>}"
```

If the KB is not found, print the notice and **continue the session silently** — do not block startup.

## Step 1 — Show what the KB has for this project

```bash
# Cross-cutting rules that apply everywhere
ls "$KB_ROOT/authored/rules/" 2>/dev/null

# This project's auto-facts (written by prograph)
ls "$KB_ROOT/derived/projects/${PROJECT}"* 2>/dev/null

# Latest journal entries for this project (written by kb-save)
tail -n 30 "$KB_ROOT/derived/journal/${PROJECT}/journal.md" 2>/dev/null
```

## Step 2 — Brief recap (2–3 lines)

Print to the user, concisely:
- Which project the session is in, and whether the KB has facts/journal for it.
- The 2–3 most recent journal entries (date + one-line summary), if any.
- A pointer: `/kb-load <topic>` to warm up context, `/kb-save` to record significant actions,
  `/kb-search <query>` to look something up.

**Do not dump file contents.** Keep it to a few lines; the KB is not loaded wholesale here.
Write **nothing** to the KB.
