# Разбор _cowork_output → 3 назначения

> Дата: 2026-07-05 · Не всё едет в KB. Три пункта: **KB** (знание), **репо-владелец** (спеки),
> **discard/archive** (scratch/сделанное). `_cowork_output` **не удаляем** — чистим до dev-scratch.

## Правило маршрутизации

- Знание об экосистеме (ADR, roadmap, status, заметки, снапшоты контрактов) → **KB**.
- Implementation-спека → **репо, чей код она меняет** (placement-правило).
- Уже применённое / чистый scratch → **discard**.
- Код-тулинг и бинарники — **не** в KB (у них своя ниша).

## В KB (`prograph-vault/`) — при переносе дописать frontmatter (title/type/status/owner/updated)

| Элемент | Куда | Действие |
|---|---|---|
| `decisions/` (13 ADR) | `authored/decisions/` | перенести все; проставить `status` (accepted/superseded) |
| `roadmap/` | `authored/notes/` | перенести |
| `plans/` (ownership-plan) | `authored/notes/` | перенести |
| `status/` (33 отчёта) | `authored/notes/status/` | **bulk-архив** (историческое) |
| `contracts/` (7) | `derived/contracts/` | снапшоты; пометить источник+хеш |
| `2026-07-05-sdd-framework-state-and-comparison.md` | `authored/notes/` | анализ |
| `2026-07-01-reliability-...paper-eval.md` | `authored/notes/` | анализ |
| `2026-06-28-opinion-review-and-agent-id-drift.md` | `authored/notes/` | анализ |
| `2026-05-25-polyrepo-workflow-setup.md` | `authored/notes/` (или `rules/`) | workflow |
| `project-status-2026-04-16.md` | `authored/notes/status/` | архив |
| `linear-*` (sync/audit/deltas, 6 шт) | `authored/notes/archive/` | Linear заморожен → архив |
| `заметки.txt` | `authored/notes/` | review, разложить |
| `diagrams/` (3) | `authored/notes/` или `derived/graph/` | по природе (ручные vs генерённые) |
| `integration/` (2) | `authored/notes/` | review |

## В репо-владельцы (placement-правило)

| Элемент | Куда | Действие |
|---|---|---|
| `spec-runner-c1-stages-profile/` | `spec-runner/docs/plans/` | перенести |
| `spec-runner-c2-specmeta-contract/` | `spec-runner/docs/plans/` | перенести |
| `maestro-c4-decomposer-delegation/` | `Maestro/docs/plans/` | перенести |
| `maestro-backlog/` (I1) | `Maestro/` | отчёт → `Maestro/docs/`; actionable → строка в `Maestro/TODO.md` |
| `spec-governance-dogfood/` (6) | `steward/` | dogfood-спека → `steward/spec/`; WS-002 → `steward/`; `project.yaml`/emitter-check → `steward/docs/` |

## Discard / уже применено

| Элемент | Почему |
|---|---|
| `kb-bootstrap/` | уже скопировано в prograph-vault |
| `steward-bootstrap/` | уже применено в steward |
| `drafts/` (1) | scratch — review, скорее всего удалить |

## Решить отдельно (не KB)

| Элемент | Заметка |
|---|---|
| `devtools/` (10) | **код-тулинг**, не знание. Оставить в `_cowork_output/devtools/` (разрешено правилом) ИЛИ вынести в отдельную tools-репу. Не в KB |
| `ATP-presentation.pptx` | бинарь-артефакт, не KB-знание. В `atp-platform/docs/` или архив вне KB |

## После разбора: чистить, не удалять

`_cowork_output` **остаётся** как dev-scratch:
- Проектные правила требуют, чтобы выходные файлы шли в `_cowork_output/`.
- Сюда пишутся черновики каждой сессии до graduation.
- `devtools/` может тут жить по правилу.

Итог: после переноса `_cowork_output` — почти пустой (только `devtools/` + свежий scratch), но
директория и её роль сохраняются.

## Как выполнять

1. Прогонять по одному назначению за раз, **отдельным коммитом** в целевом репо (чистая история).
2. KB-переносы — через процедуру **graduation** скила `kb-curator` (дописать frontmatter, починить
   ссылки после перемещений).
3. Спеки в репо-владельцы — простой `cp`/`git mv` в `docs/plans/`, затем коммит там.
4. После каждого блока — прогнать `kb-curator` freshness + link-check.
