---
title: devtools — activity journal
type: journal
source: kb-save
project: devtools
updated: 2026-08-17
---

# devtools — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.

## 2026-08-17 16:05 — change: резолв состояния issue-блокеров `<repo>#<number>` (обратное плечо ADR-ECO-006)

- Принят inbox-issue devtools#40 от prograph-vault (правило cross-repo-waits, там PR #72) под запрошенным слагом `blocker-issue-state-resolution`; реализация — devtools PR #41 (CI зелёный, ревью-замечание Copilot закрыто).
- `check-plan-fields.py` теперь резолвит issue-форму блокеров через `gh`: закрытый/вмерженный target у открытого пункта → ERROR класса PF-BLOCKER-STALE (stale = всё, что не OPEN — gh резолвит и PR-номера, state MERGED); недоступный резолв → явный [DT-ISSUE-STATE-UNAVAILABLE], не clean; issue-рефы изъяты из legacy slug-графа и PF-LEGACY-AMBIGUOUS-шума.
- Links: devtools/check-plan-fields.py, devtools/tests/test_issue_blockers.py, devtools/TODO.md (@id:blocker-issue-state-resolution), devtools#40, devtools PR #41
