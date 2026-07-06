---
name: kb-curator
description: >
  Curator of the Ecosystem KB (prograph-vault). Keeps the knowledge base in order: freshness audit
  of the registry and authored docs, archiving of the obsolete (with date+reason, no deletion),
  fixing broken links, knowledge search, graduation of canon from _cowork_output into the KB, and
  pruning/archiving the derived/journal. Run when the user asks: "tidy up the KB / knowledge base",
  "check the registry's freshness", "archive the obsolete", "fix the links in the vault",
  "find … in the KB", "move this from _cowork_output into the KB", "clean up authored", as well as on
  a scheduled (e.g. weekly) run. Works ONLY in the KB; other repos are read-only. Filesystem-only, no
  Obsidian.
allowed-tools: Bash, Read, Grep, Glob, Edit, Write
---

# kb-curator — curator of the Ecosystem KB

Maintains `prograph-vault/` (Ecosystem KB) in accordance with its `CLAUDE.md`, over the **filesystem**
(no Obsidian). Does not build the graph (that's prograph), does not monitor runtime (dispatcher),
does not enforce specs (steward/gate-check) — only **knowledge curation**.

## Step 0 — Locate the KB

```bash
_kb() { local d; d="$(pwd -P)"; while [ "$d" != "/" ]; do
    [ -d "$d/prograph-vault/authored" ] && { printf '%s\n' "$d/prograph-vault"; return 0; }
    [ -d "$d/authored" ] && [ -f "$d/CLAUDE.md" ] && [ "$(basename "$d")" = prograph-vault ] && { printf '%s\n' "$d"; return 0; }
    d="$(dirname "$d")"; done; return 1; }
KB_ROOT="${KB_ROOT:-$(_kb)}"
[ -z "$KB_ROOT" ] && { echo "⚠️  prograph-vault not found — nothing to curate."; exit 0; }
source "$KB_ROOT/authored/skills/kb-utils/kb-env.sh"
```

## Boundaries (important)

- Writes **only** to the KB's `authored/**`. To `derived/**` — **never**, with **one exception**:
  it may prune/archive `derived/journal/**` per ADR 2026-07-06 (task 6). No other `derived/` (owner is
  prograph).
- Other repos are **read-only** (may read to cross-check facts, not modify).
- authored changes — as a PR set (a human reviews); do not auto-merge substantive edits.
- Deletes nothing — **archives** (see below).

## When to do what

### 1. Freshness audit
Goal — catch divergence of the KB from reality.
- Cross-check `authored/registry/` (COWORK_CONTEXT) against the actual checkout: new/removed repos,
  stale statuses/dates/commits (`git -C <repo> log -1`).
- Find authored docs untouched for > N days (by `updated:`/git) → mark as review candidates:
  ```bash
  # frontmatter updated: dates across authored docs
  grep -rn '^updated:' "$KB_ROOT/authored" 2>/dev/null
  # or last git touch of a file
  git -C "$KB_ROOT" log -1 --format='%ci' -- <path>
  ```
- Report: what diverged, with the file named and the proposed action. **Do not** edit silently.

### 2. Archiving the obsolete
- Obsolete/`superseded` doc → move into `authored/<subfolder>/archive/`:
  ```bash
  mkdir -p "$KB_ROOT/authored/<subfolder>/archive"
  git -C "$KB_ROOT" mv <path> "authored/<subfolder>/archive/" 2>/dev/null || mv <path> "$KB_ROOT/authored/<subfolder>/archive/"
  ```
- Set frontmatter (use `Edit`): `status: archived`, `archived: YYYY-MM-DD`, `reason: <why>`,
  `superseded_by: <link>` (if any). **Do not delete** — decision history is valuable.

### 3. Fixing links
- Scan `[[wiki-links]]` and relative links in `authored/**`:
  ```bash
  grep -rnoE '\[\[[^]]+\]\]|\]\([^)]+\)' "$KB_ROOT/authored" 2>/dev/null
  ```
- For each target, check existence on disk; broken ones → fix with `Edit` if the target is unambiguous,
  otherwise → into the report. After moves (archiving, graduation) run this without fail.

### 4. Knowledge search
- Answer "where is X / what do we know about Y" by searching the KB over the filesystem:
  ```bash
  kb_grep "<query>"                       # whole KB (rg/grep, from kb-env.sh)
  kb_grep "<query>" "$KB_ROOT/authored"   # scope to an area
  ```
  Read the hits and return **paths + short quotes**, not a recap from memory.

### 5. Graduation from _cowork_output → KB
- Take a canonical artifact from `_cowork_output/` (ADR, rule, template, registry edit).
- Determine the target `authored/` subfolder by type (see `CLAUDE.md` §3/§8).
- Add correct frontmatter (`title/type/status/owner/updated`), place it (`Write`), fix links (task 3).
- Mark the source in `_cowork_output/` as graduated (or delete the draft, if it's pure scratch).

### 6. Journal curation (`derived/journal/`)
- Per ADR 2026-07-06, kb-save appends per-project activity to `derived/journal/<project>/journal.md`.
  This is the **only** `derived/` area the curator may touch.
- On request/schedule: skim journals for stale or superseded entries. Do **not** delete — move the
  obsolete tail into `derived/journal/<project>/archive/YYYY-MM-DD.md` with a one-line reason. Keep the
  live `journal.md` focused on current, significant activity.

## Formatting rules (from the KB CLAUDE.md)

- Frontmatter required: `title/type/status/owner/updated` (see §7).
- Naming: `YYYY-MM-DD-<kebab>` for dated ones; stable names for rules/templates.
- Do not mix authored ⇄ derived; repo-local rules — not here (in the repo's CLAUDE.md).
- Contracts — only snapshots/links; authority lives in the producer repo.

## Tools

- KB search/read/write: `Grep`/`Read`/`Edit`/`Write` + `kb_grep` (`authored/skills/kb-utils/kb-env.sh`).
  No Obsidian.
- Repo cross-check: `git` read-only, reading `pyproject.toml`/`CLAUDE.md`.
- Populating `derived/` — **not** this skill, but prograph (except `derived/journal/`, owned by kb-save).

## Scheduled run

You can attach a scheduled task (e.g. weekly) for "freshness audit + report"; run archiving/graduation
on the user's decision after they review the report.

## Output

Always end with a short report: what was checked, what was proposed/done, what requires human
review. Substantive authored edits — propose, do not impose.
