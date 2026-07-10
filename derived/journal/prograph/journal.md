---
title: prograph — activity journal
type: journal
source: kb-save
project: prograph
updated: 2026-07-10
---

# prograph — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.

## 2026-07-10 16:49 — result: найден drift «граф vs реестр» (proctor изолирован в графе, но связан в карте интеграций)

- Граф prograph (snapshot 4) показывает proctor с 0 рёбер; карта интеграций COWORK_CONTEXT
  содержит dispatcher ↔ proctor с 2026-07-05 (dispatcher/core/collectors/proctor.py читает
  config/proctor.yaml, data/state.db и логи proctor с диска). Файловая интеграция невидима
  для всех трёх детекторов (deps/contracts/mcp) — слепое пятно инструмента; по той же
  причине невидимы ВСЕ рёбра dispatcher к подопечным проектам.
- Зафиксировано: prograph/TODO.md — задача «declared edges» (M12-кандидат: декларация
  `[tool.prograph] reads = [...]` → пунктирное ребро «declared, not detected»), коммит c6ac6d1.
- Links: devtools/proposals/2026-07-10-graph-vs-registry-check.md (инвариант fleet-агента,
  коммит 8d6576d); ADR 2026-07-07 (namespace repo proctor vs service-id proctor-a).
