#!/usr/bin/env bash
# install-skills.sh — distribute the kb-* runtime skills from the KB into ecosystem
# sub-projects. Source of truth lives here (prograph-vault/authored/skills/); this
# copies the runtime skills into each target project's .claude/skills/.
#
# The shared helper kb-utils/kb-env.sh is NOT copied — each skill locates the KB and
# sources it from there, so there is a single, always-fresh copy in the KB.
#
# Usage:
#   ./install-skills.sh --from-config       # install into every project in targets.txt
#   ./install-skills.sh <dir> [<dir> ...]   # install into the given project dirs
#   ./install-skills.sh --kb                # sync kb-curator into the KB's own .claude/skills
#   ./install-skills.sh --list              # list candidate sibling projects
#   ./install-skills.sh --track ...         # do NOT gitignore installed skills in the target
#   ./install-skills.sh -h | --help
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"   # …/prograph-vault/authored/skills
KB_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd -P)"                    # …/prograph-vault
WORKSPACE="$(cd "$KB_ROOT/.." && pwd -P)"                        # …/all_ai_orchestrators
CONFIG="$SCRIPT_DIR/targets.txt"
SKILLS=(kb-load kb-save kb-search kb-session)
TRACK=0

usage() { sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; }

list_candidates() {
  echo "Candidate sibling projects under $WORKSPACE:"
  for d in "$WORKSPACE"/*/; do
    d="${d%/}"; local base; base="$(basename "$d")"
    [ "$base" = "prograph-vault" ] && continue
    [ -d "$d/.git" ] && echo "  $base"
  done
}

# Ensure installed skills are ignored by the target repo (keeps it clean).
ensure_gitignore() {
  local skills_dir="$1" gi="$1/.gitignore" line
  [ -f "$gi" ] || printf '# kb-* skills installed by prograph-vault/authored/skills/install-skills.sh\n' > "$gi"
  for s in "${SKILLS[@]}"; do
    line="$s/"
    grep -qxF "$line" "$gi" 2>/dev/null || printf '%s\n' "$line" >> "$gi"
  done
}

# kb-curator is KB-side only: sync it into the KB's own runtime skills dir.
install_curator() {
  local dst="$KB_ROOT/.claude/skills/kb-curator"
  mkdir -p "$(dirname "$dst")"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete "$SCRIPT_DIR/kb-curator/" "$dst/"
  else
    rm -rf "$dst"; cp -R "$SCRIPT_DIR/kb-curator" "$dst"
  fi
  echo "  ✓ kb-curator  →  ${dst#$KB_ROOT/} (KB-side)"
}

install_into() {
  local target="$1"
  # Resolve relative names against the workspace root.
  [ -d "$target" ] || target="$WORKSPACE/$target"
  if [ ! -d "$target" ]; then echo "  ✗ not found: $1" >&2; return 1; fi
  target="$(cd "$target" && pwd -P)"
  if [ "$(basename "$target")" = "prograph-vault" ]; then echo "  ↷ skip vault: $1"; return 0; fi

  local dst="$target/.claude/skills"
  mkdir -p "$dst"
  for s in "${SKILLS[@]}"; do
    if command -v rsync >/dev/null 2>&1; then
      rsync -a --delete "$SCRIPT_DIR/$s/" "$dst/$s/"
    else
      rm -rf "${dst:?}/$s"; cp -R "$SCRIPT_DIR/$s" "$dst/$s"
    fi
  done
  [ "$TRACK" -eq 0 ] && ensure_gitignore "$dst"
  echo "  ✓ $(basename "$target")  →  ${dst#$WORKSPACE/}"
}

main() {
  local -a targets=()
  local from_config=0
  for arg in "$@"; do
    case "$arg" in
      -h|--help) usage; exit 0 ;;
      --list) list_candidates; exit 0 ;;
      --kb) install_curator; exit 0 ;;
      --track) TRACK=1 ;;
      --from-config) from_config=1 ;;
      *) targets+=("$arg") ;;
    esac
  done

  if [ "$from_config" -eq 1 ]; then
    [ -f "$CONFIG" ] || { echo "no targets.txt at $CONFIG" >&2; exit 1; }
    while IFS= read -r line; do
      line="${line%%#*}"; line="$(echo "$line" | xargs || true)"
      [ -n "$line" ] && targets+=("$line")
    done < "$CONFIG"
  fi

  if [ "${#targets[@]}" -eq 0 ]; then usage; exit 1; fi

  echo "Installing [${SKILLS[*]}] from $KB_ROOT"
  local rc=0
  for t in "${targets[@]}"; do install_into "$t" || rc=1; done
  exit "$rc"
}

main "$@"
