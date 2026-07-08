#!/usr/bin/env bash
# ============================================================
#  promote-prograph.sh — переносит вывод prograph из staging (.prograph/)
#  в KB (prograph-vault/derived/graph/) атомарно, с drift-гейтом и коммитом.
#
#  ЗАЧЕМ: prograph пишет рендер в репо-локальный staging (.prograph/).
#  Владение записью в git-канон KB отдано ЭТОМУ промоутеру, а не самому
#  инструменту (см. ADR prograph↔vault format divergence, 2026-07-08):
#    - гейт качества (drift) между generate и commit;
#    - атомарность для Robin (живой read-only консюмер derived/);
#    - безопасное удаление устаревших карточек (rsync --delete, scoped);
#    - prograph остаётся самодостаточным, не знает путь KB.
#
#  РАЗМЕЩЕНИЕ: prograph-vault/authored/skills/ (владение записью в KB — у KB).
#  Едет с клоном вольта; раздаётся install-skills.sh при необходимости.
#
#  ПРИМЕРЫ:
#     ./promote-prograph.sh                 # reindex → drift(warn) → rsync → commit
#     ./promote-prograph.sh --dry-run       # показать, что изменится; без записи/коммита
#     ./promote-prograph.sh --fail-on-drift # строгий CI-режим: drift → выход !=0, без промоушена
#     ./promote-prograph.sh --no-reindex    # промоутить текущий .prograph/ как есть
#     ./promote-prograph.sh --no-commit     # записать в derived/graph, но не коммитить
# ============================================================
set -uo pipefail

# --- пути (как в соседнем install-skills.sh: skills → KB → workspace) ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"   # …/prograph-vault/authored/skills
KB="$(cd "$SCRIPT_DIR/../.." && pwd -P)"                         # …/prograph-vault
ROOT="$(cd "$KB/.." && pwd -P)"                                  # …/all_ai_orchestrators (workspace root)
STAGING="$ROOT/.prograph"                                        # вывод prograph (P0: export_root)
DEST="$KB/derived/graph"                                         # tool-owned поддерево в KB

# --- флаги ---
DRY_RUN=0; REINDEX=1; DO_COMMIT=1; FAIL_ON_DRIFT=0
for a in "$@"; do
  case "$a" in
    --dry-run)       DRY_RUN=1 ;;
    --no-reindex)    REINDEX=0 ;;
    --no-commit)     DO_COMMIT=0 ;;
    --fail-on-drift) FAIL_ON_DRIFT=1 ;;
    -h|--help) sed -n '2,26p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) echo "unknown flag: $a" >&2; exit 2 ;;
  esac
done

# --- цвета ---
if [ -t 1 ]; then C_RST=$'\033[0m'; C_R=$'\033[31m'; C_G=$'\033[32m'; C_Y=$'\033[33m'; C_B=$'\033[1m'
else C_RST=""; C_R=""; C_G=""; C_Y=""; C_B=""; fi
say()  { printf "%b==>%b %s\n" "$C_B" "$C_RST" "$*"; }
warn() { printf "%b!  %s%b\n" "$C_Y" "$*" "$C_RST"; }
die()  { printf "%bX  %s%b\n" "$C_R" "$*" "$C_RST" >&2; exit 1; }

# --- preflight ---
command -v rsync >/dev/null 2>&1 || die "rsync не найден"
command -v prograph >/dev/null 2>&1 || warn "prograph не в PATH — --no-reindex/gate могут не работать (uv run prograph?)"
[ -d "$KB/.git" ] || die "KB не git-репозиторий: $KB"
[ -d "$STAGING" ] || die "нет staging $STAGING — сначала прогони prograph"

# --- 0. reindex (обновить staging из реальности) ---
if [ "$REINDEX" -eq 1 ]; then
  say "prograph index --export-md (root=$ROOT)"
  if [ "$DRY_RUN" -eq 0 ]; then
    ( cd "$ROOT" && prograph index --export-md ) || die "prograph index упал"
  else
    warn "dry-run: reindex пропущен"
  fi
fi

# --- 1. drift-гейт ---
say "drift-гейт"
DRIFT_N=0
if command -v prograph >/dev/null 2>&1; then
  DRIFT_JSON="$( cd "$ROOT" && prograph drift --json 2>/dev/null )" || DRIFT_JSON=""
  if [ -n "$DRIFT_JSON" ]; then
    DRIFT_N="$(printf '%s' "$DRIFT_JSON" | python3 -c 'import sys,json
try:
    d=json.load(sys.stdin)
    print(len(d) if isinstance(d,list) else len(d.get("findings",d.get("drifts",[]))))
except Exception:
    print(0)' 2>/dev/null)"
    DRIFT_N="${DRIFT_N:-0}"
  else
    warn "prograph drift --json пусто/недоступно — гейт в режиме best-effort"
  fi
fi
if [ "$DRIFT_N" -gt 0 ]; then
  warn "drift findings: $DRIFT_N (README/TODO vs реальность). Детали: prograph drift"
  if [ "$FAIL_ON_DRIFT" -eq 1 ]; then
    die "--fail-on-drift: промоушен остановлен, есть $DRIFT_N drift-находок"
  fi
  warn "продолжаю (warn-режим); используй --fail-on-drift для строгого гейта"
else
  printf "%b   drift: 0%b\n" "$C_G" "$C_RST"
fi

# --- 2. атомарный promote (rsync --delete, ТОЛЬКО в derived/graph) ---
say "promote staging → $DEST"
mkdir -p "$DEST/projects" "$DEST/contracts"
RSYNC_OPTS=(-a --delete --prune-empty-dirs)
[ "$DRY_RUN" -eq 1 ] && RSYNC_OPTS+=(-n -v)
# только рендер; graph.db/бэкапы/локи/конфиг НЕ тащим в KB
sync_one() { # <src> <dst>
  [ -e "$1" ] || { warn "нет $1 — пропуск"; return 0; }
  rsync "${RSYNC_OPTS[@]}" "$1" "$2"
}
sync_one "$STAGING/projects/"  "$DEST/projects/"
sync_one "$STAGING/contracts/" "$DEST/contracts/"
if [ -f "$STAGING/index.md" ]; then
  if [ "$DRY_RUN" -eq 1 ]; then rsync -n -v "$STAGING/index.md" "$DEST/index.md"
  else cp "$STAGING/index.md" "$DEST/index.md"; fi
fi

# --- provenance ---
PROG_VER="$(prograph --version 2>/dev/null | head -1 || echo unknown)"
SRC_SHA="$(git -C "$ROOT" rev-parse --short HEAD 2>/dev/null || echo nogit)"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if [ "$DRY_RUN" -eq 0 ]; then
  cat > "$DEST/PROVENANCE.md" <<EOF
<!-- generated by promote-prograph.sh — do not edit by hand -->
- promoted_at: $STAMP
- prograph_version: $PROG_VER
- source_root_commit: $SRC_SHA
- drift_findings_at_promote: $DRIFT_N
EOF
fi

# --- 3. commit (только derived/graph) ---
if [ "$DRY_RUN" -eq 1 ]; then say "dry-run: коммит пропущен"; exit 0; fi
if [ "$DO_COMMIT" -eq 0 ]; then say "--no-commit: изменения в $DEST не закоммичены"; exit 0; fi

if git -C "$KB" diff --quiet -- derived/graph && git -C "$KB" diff --cached --quiet -- derived/graph \
   && [ -z "$(git -C "$KB" ls-files --others --exclude-standard -- derived/graph)" ]; then
  say "нет изменений в derived/graph — коммит не нужен"; exit 0
fi
say "commit в KB (scoped: derived/graph)"
git -C "$KB" add -- derived/graph
git -C "$KB" commit -q -m "KB: promote prograph graph → derived/graph (src $SRC_SHA, drift $DRIFT_N)" \
  && printf "%b   ok: %s%b\n" "$C_G" "$(git -C "$KB" log --oneline -1)" "$C_RST"
