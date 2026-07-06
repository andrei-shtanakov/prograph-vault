#!/usr/bin/env bash
# kb-env.sh — shared helpers for the kb-* skills. Filesystem-only, no Obsidian.
# Single source of truth: lives ONLY in the KB at
#   prograph-vault/authored/skills/kb-utils/kb-env.sh
# The kb-* skills locate the KB, then `source` this file from $KB_ROOT.
# Do not run directly.

# kb_root — print the absolute path to the Ecosystem KB (prograph-vault), or fail.
# Resolution: $KB_ROOT / $PROGRAPH_VAULT override → nearest ancestor of $PWD that
# has a `prograph-vault/authored` dir → $PWD itself when it IS the vault.
kb_root() {
  local override="${KB_ROOT:-${PROGRAPH_VAULT:-}}"
  if [ -n "$override" ] && [ -d "$override/authored" ] && [ -f "$override/CLAUDE.md" ]; then
    printf '%s\n' "$override"; return 0
  fi
  local dir; dir="$(pwd -P)"
  while [ "$dir" != "/" ]; do
    if [ -d "$dir/prograph-vault/authored" ]; then
      printf '%s\n' "$dir/prograph-vault"; return 0
    fi
    if [ -d "$dir/authored" ] && [ -f "$dir/CLAUDE.md" ] && [ "$(basename "$dir")" = "prograph-vault" ]; then
      printf '%s\n' "$dir"; return 0
    fi
    dir="$(dirname "$dir")"
  done
  return 1
}

# kb_project [explicit] — print the ecosystem project the session works on, or fail.
# Resolution: explicit arg → $KB_PROJECT → basename of the git toplevel when it is a
# sibling of prograph-vault (i.e. a real ecosystem repo, not the workspace root and
# not the vault). Fails (empty) when ambiguous — the caller must ask the user.
kb_project() {
  local explicit="${1:-${KB_PROJECT:-}}"
  if [ -n "$explicit" ]; then printf '%s\n' "$explicit"; return 0; fi
  local top; top="$(git rev-parse --show-toplevel 2>/dev/null)"
  if [ -n "$top" ]; then
    local base; base="$(basename "$top")"
    if [ "$base" != "prograph-vault" ] && [ ! -d "$top/prograph-vault" ]; then
      printf '%s\n' "$base"; return 0
    fi
  fi
  return 1
}

# kb_grep <query> [path…] — case-insensitive search under the KB (read-only).
# Uses ripgrep if present, else grep. Paths default to the whole KB.
kb_grep() {
  local kb; kb="$(kb_root)" || return 1
  local query="$1"; shift
  local -a paths=("$@"); [ "${#paths[@]}" -eq 0 ] && paths=("$kb")
  if command -v rg >/dev/null 2>&1; then
    rg -i -n --max-columns 200 -g '!.git' "$query" "${paths[@]}" 2>/dev/null
  else
    grep -rInI --exclude-dir=.git "$query" "${paths[@]}" 2>/dev/null
  fi
}
