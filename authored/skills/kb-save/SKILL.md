---
name: kb-save
description: Record a significant action on the CURRENT project into the Ecosystem KB (prograph-vault) journal. Use after any notable project event — a decision, an interface/contract change, a new component, a migration, a status change, or a noteworthy result. Not just hard problems: log all significant project actions. Scoped to the current project only; appends to derived/journal/<project>/journal.md. Does not auto-commit.
allowed-tools: Bash, Read, Grep, Glob, Write
---

# kb-save — record project activity in the KB journal

Appends a dated entry about the **current project** to its journal in the shared KB. Content policy:
record **all significant project actions/events**, not only nontrivial fixes — decisions, interface
or contract changes, new components, migrations, status changes, notable results. Scope is strictly
the current project; never write about another project's work.

## Step 0 — Locate the KB and resolve the project

```bash
_kb() { local d; d="$(pwd -P)"; while [ "$d" != "/" ]; do
    [ -d "$d/prograph-vault/authored" ] && { printf '%s\n' "$d/prograph-vault"; return 0; }
    [ -d "$d/authored" ] && [ -f "$d/CLAUDE.md" ] && [ "$(basename "$d")" = prograph-vault ] && { printf '%s\n' "$d"; return 0; }
    d="$(dirname "$d")"; done; return 1; }
KB_ROOT="${KB_ROOT:-$(_kb)}"
if [ -z "$KB_ROOT" ]; then
  echo "⚠️  prograph-vault not found. Here is the entry to save manually:"
  # print the composed entry below so nothing is lost, then stop.
  exit 0
fi
source "$KB_ROOT/authored/skills/kb-utils/kb-env.sh"
PROJECT="$(kb_project "${1:-}" || true)"
```

If `PROJECT` is empty (session runs from the workspace root, so cwd is ambiguous): **ask the user
which project this entry is about, or pass it explicitly** — do not guess. Never write to
`derived/journal/` without a concrete project.

## Step 1 — Decide what (and whether) to record

Record significant, project-scoped events. Pick a category:
`decision` | `change` | `result` | `status` | `note`.

Skip pure noise (typo fixes, transient scratch). When in doubt about significance, prefer to record —
the journal is meant to capture the project's real activity, and `kb-curator` prunes later.

## Step 2 — Append the entry (newest at the bottom; tail-friendly)

```bash
DIR="$KB_ROOT/derived/journal/$PROJECT"
FILE="$DIR/journal.md"
DATE="$(date +%Y-%m-%d)"; TIME="$(date +%H:%M)"
mkdir -p "$DIR"

# Create the file with frontmatter on first use
if [ ! -f "$FILE" ]; then
  cat > "$FILE" <<EOF
---
title: ${PROJECT} — activity journal
type: journal
source: kb-save
project: ${PROJECT}
updated: ${DATE}
---

# ${PROJECT} — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.
EOF
fi

# Append the entry. Fill CATEGORY, TITLE, and the body bullets/links before running.
cat >> "$FILE" <<'EOF'

## <DATE> <TIME> — <CATEGORY>: <short title>

- <what happened, 1–3 lines>
- Links: <touched files / contracts / ADRs, if any>
EOF

# Keep the frontmatter `updated:` current
# (edit the updated: line to today's date)
```

Compose the real `<CATEGORY>`, `<short title>`, body, and links; substitute `<DATE>`/`<TIME>` with the
values above (use `Read`/`Edit` on `$FILE` for precise edits when needed). Refer to files by
`path:line` where useful. Update the frontmatter `updated:` field to today.

## Step 3 — Confirm

Tell the user: the journal file path, the category, and a one-line summary of what was recorded.
State that it is **written but not committed** — commit to the KB (or run `kb-curator`) is a separate,
manual step.
