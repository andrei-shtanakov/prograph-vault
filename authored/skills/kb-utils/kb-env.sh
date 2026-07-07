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
# Identity is the git-remote repo NAME (stable across clones / directory renames),
# NOT the directory basename — e.g. a repo cloned into `proctor-a/` whose remote is
# `…/proctor.git` resolves to `proctor`. Resolution: explicit arg → $KB_PROJECT →
# remote repo name of the git toplevel → toplevel basename (fallback when no remote).
# Fails (empty) when the toplevel is the vault or the workspace root (ambiguous) so
# the caller asks the user.
kb_project() {
  local explicit="${1:-${KB_PROJECT:-}}"
  if [ -n "$explicit" ]; then printf '%s\n' "$explicit"; return 0; fi
  local top; top="$(git rev-parse --show-toplevel 2>/dev/null)" || return 1
  [ -z "$top" ] && return 1
  local base; base="$(basename "$top")"
  # not the vault, not the workspace root (which contains the vault)
  { [ "$base" = "prograph-vault" ] || [ -d "$top/prograph-vault" ]; } && return 1
  # prefer the stable git remote repo name; fall back to the directory basename
  local url name; url="$(git -C "$top" remote get-url origin 2>/dev/null)"
  name="${url##*/}"; name="${name%.git}"
  [ -n "$name" ] && { printf '%s\n' "$name"; return 0; }
  printf '%s\n' "$base"
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
