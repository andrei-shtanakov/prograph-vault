---
name: kb-search
description: Answer a targeted question against the Ecosystem KB (prograph-vault) — standards, cross-cutting rules, templates, contracts, project facts, recent changes, or past activity. Use for ad-hoc lookups like "what's the rule for X", "which template for Y", "what changed in Z lately", "did we decide about W". Read-only, unrestricted across the whole KB. For proactively loading a work area up front, use kb-load instead.
allowed-tools: Bash, Read, Grep, Glob
---

# kb-search — targeted lookup in the KB

Answers one question by searching the whole KB. This is the **reactive Q&A** counterpart to
`kb-load` (which bulk-loads an area proactively). Reading and search are **unrestricted** — the whole
vault is fair game.

## Step 0 — Locate the KB

```bash
_kb() { local d; d="$(pwd -P)"; while [ "$d" != "/" ]; do
    [ -d "$d/prograph-vault/authored" ] && { printf '%s\n' "$d/prograph-vault"; return 0; }
    [ -d "$d/authored" ] && [ -f "$d/CLAUDE.md" ] && [ "$(basename "$d")" = prograph-vault ] && { printf '%s\n' "$d"; return 0; }
    d="$(dirname "$d")"; done; return 1; }
KB_ROOT="${KB_ROOT:-$(_kb)}"
[ -z "$KB_ROOT" ] && { echo "ℹ️  prograph-vault not found — nothing to search."; exit 0; }
source "$KB_ROOT/authored/skills/kb-utils/kb-env.sh"
```

## Step 1 — Search, narrowing by area when obvious

```bash
# Whole KB
kb_grep "<query>"

# Or scope to the area the question is about:
kb_grep "<query>" "$KB_ROOT/authored/rules"        # standards / cross-cutting rules
kb_grep "<query>" "$KB_ROOT/authored/templates"    # templates / scaffolds
kb_grep "<query>" "$KB_ROOT/authored/decisions"    # ADRs — cross-repo "why"
kb_grep "<query>" "$KB_ROOT/derived/contracts"     # contract snapshots
kb_grep "<query>" "$KB_ROOT/derived/projects"      # per-project facts
kb_grep "<query>" "$KB_ROOT/derived/journal"       # recorded activity
kb_grep "<query>" "$KB_ROOT/derived/digests"       # AI/IT digests
```

Strategy: exact terms first; if empty, broaden or try synonyms; if still empty, list the area's files
(`ls`) and skim. Open promising hits with `Read`.

## Step 2 — Answer

- Direct answer to the question, if found.
- Cite the file path(s) and quote the relevant lines — do not paraphrase from memory.
- If nothing is found: say so, and if it is something worth recording later, suggest `/kb-save`.
