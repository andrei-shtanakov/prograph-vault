---
name: kb-save
description: Record a significant action on the CURRENT project into the Ecosystem KB (prograph-vault) journal. Use after any notable project event — a decision, an interface/contract change, a new component, a migration, a status change, or a noteworthy result. Not just hard problems: log all significant project actions. Scoped to the current project only; appends to derived/journal/<project>/journal.md. Delivers via the rolling journal/pending branch + PR — never commits to master or leaves the entry stranded in the local checkout.
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

## Step 2 — Compose the entry

Entry shape (newest at the bottom; tail-friendly). Fill `<CATEGORY>`, `<short title>`, the body
bullets and links; `<DATE>`/`<TIME>` come from `date +%Y-%m-%d` / `date +%H:%M`. Refer to files by
`path:line` where useful.

```markdown
## <DATE> <TIME> — <CATEGORY>: <short title>

- <what happened, 1–3 lines>
- Links: <touched files / contracts / ADRs, if any>
```

On the journal's **first ever** entry the file starts with this frontmatter:

```markdown
---
title: <PROJECT> — activity journal
type: journal
source: kb-save
project: <PROJECT>
updated: <DATE>
---

# <PROJECT> — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.
```

## Step 3 — Deliver via the rolling `journal/pending` branch (never local master)

The KB's `master` is PR-only with no machine bypass: a commit made in the local checkout can never
be pushed and silently strands the entry (incident 2026-08-28, rescue PRs #108/#109). Delivery goes
through a **detached worktree** on the rolling branch — the main KB checkout is never switched
(the snapshot publisher commits to whatever branch is checked out there, so `master` must stay
checked out) and never dirtied.

```bash
cd "$KB_ROOT"
git fetch origin --prune
BASE="origin/master"
git show-ref --verify --quiet refs/remotes/origin/journal/pending && BASE="origin/journal/pending"
WT="$(mktemp -d)/journal-pending"
git worktree add --detach "$WT" "$BASE"

DIR="$WT/derived/journal/$PROJECT"; FILE="$DIR/journal.md"
mkdir -p "$DIR"
# First use: create $FILE with the frontmatter block from Step 2.
# Append the composed entry to $FILE; bump the frontmatter `updated:` to today.

git -C "$WT" add "derived/journal/$PROJECT/journal.md"
git -C "$WT" commit -m "journal($PROJECT): <short title>"
git -C "$WT" push origin HEAD:refs/heads/journal/pending || {
  # lost a race with another kb-save: rebase onto the fresh tip, retry once
  git -C "$WT" fetch origin journal/pending &&
  git -C "$WT" rebase FETCH_HEAD &&
  git -C "$WT" push origin HEAD:refs/heads/journal/pending
}
git worktree remove "$WT"

# One accumulation cycle = one PR: create it only if none is open yet
[ "$(gh pr list --head journal/pending --state open --json number --jq length)" = 0 ] &&
  gh pr create --head journal/pending \
    --title "journal: pending записи" \
    --body "Скользящая доставка журналов kb-save; PR накапливает записи, после мержа ветка пересоздаётся от master."
```

Lifecycle: the PR accumulates commits until a human merges it; GitHub deletes the branch; the next
kb-save recreates it from fresh `origin/master`. At most one unmerged batch of entries exists at any
time, so tail-append conflicts cannot chain. The **local** checkout's `derived/journal/**` copy is
therefore behind until the pending PR merges — the freshest entries live on
`origin/journal/pending` (`git show origin/journal/pending:derived/journal/<project>/journal.md`).

**Fallback** (no remote access, `gh` unavailable, or the push failed twice): append the entry to the
main checkout's `$KB_ROOT/derived/journal/$PROJECT/journal.md` as a plain uncommitted edit and tell
the user delivery to `journal/pending` is pending manually. Never `git commit` in the main checkout.

## Step 4 — Confirm

Tell the user: the journal file path, the category, a one-line summary of what was recorded, and the
delivery state — pushed to `journal/pending` and which PR carries it (created now or already open).
The merge is a human step.
