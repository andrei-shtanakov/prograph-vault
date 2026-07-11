# Фаза 0.5 — разведка correlation-ключей (ручной проход по базам)

> Дата: 2026-07-11. Контекст: фаза 0.5 consolidated roadmap
> (`prograph-vault/authored/notes/2026-07-11-ai-dark-factory-consolidated-roadmap.md`).
> Метод: ручной проход по коду и живым БД (не прототип в dispatcher — его пишем после).
> Статус: **обе половины exit-критерия выполнены** — аудит ключей + цепочка показана
> на реальном прогоне (см. «Контрольный прогон» ниже).

## Вопрос

Хватает ли существующих ключей (task_id, trace_id/run_id из observability-contract)
для drill-down «спека → DAG-ран → routing-решение → benchmark → outcome», или нужен
новый минтованный `work_item_id`?

## Ответ (TL;DR)

**Новый id минтить не нужно — сценарий (1), лучший из трёх.** Сквозные ключи в
основном существуют по построению; разрывов два, и оба локальные. Живых данных,
демонстрирующих полную цепочку, в базах сейчас нет — цепочка доказана кодом.

## Аудит по звеньям

| Звено | Ключ | Статус | Evidence |
|-------|------|--------|----------|
| Maestro DAG-нода → arbiter decision | `task.id` передаётся дословно в `route_task` → `decisions.task_id` (indexed) | ✅ сквозной по построению | `Maestro/maestro/coordination/routing.py:181`; `arbiter.db` schema |
| decision → outcome | FK `outcomes.decision_id → decisions.id` в схеме | ⚠ спроектировано, **не используется**: `outcomes` пуста (0 строк) | `arbiter.db` |
| Ран (кросс-проектный) | `pipeline_id` (ULID = имя каталога `Maestro/logs/<ULID>/`) + W3C `TraceId`/`SpanId` в каждой JSONL-записи; arbiter пишет в каталог сессии Maestro | ✅ уже работает через observability-contract | `Maestro/logs/01KWVPAWAS.../arbiter-95752.jsonl` |
| Спека → DAG | Словари разные (spec-runner `TASK-706` vs Maestro kebab-слаги). Мостик композитный: воркстрим владеет spec-каталогом, Maestro читает executor-state по spec-runner `task_id` | ⚠ связь 1:N через `spec_dir`, общего id нет — **разрыв №1** | `Maestro/maestro/spec_runner.py:100-138`; `Maestro/maestro/decomposer.py` |
| Benchmark → задача | `benchmark_runs` без task-ссылки; `per_task` = только `task_index/task_type` (анонимные eval-задачи). Связь с раном — через логи (`pipeline_id`), не через БД | ✅ осознанный не-разрыв: benchmark = evidence для routing, не work item | `arbiter.db` `benchmark_runs.per_task` |

## Оговорки по данным

- `~/.maestro/maestro.db` — демо-мусор с 2026-04-19 (greet/compute/summarize, 3 задачи).
- Все 16 строк `decisions` — от A/B-прогона arbiter (`ab-review-w0*`, пары с одинаковым
  timestamp = shadow-routing двух политик), **не** от реальных Maestro-задач.
- В логах виден известный баг `report_benchmark failed: agent_id required`
  (уже зафиксирован при смоуке dispatcher).

## Выводы для WorkCorrelation v1

1. **Минтер — Maestro**, по данным: уже минтит `task.id` (протекает в arbiter) и
   `pipeline_id` (ULID на ран). Критерий «кто первым создаёт работу» указывает туда же.
2. **v1 наследует ключи:** `work_item_id` = Maestro `task.id`; run-контекст =
   `pipeline_id`; трейсинг = `TraceId`. «Тяжёлые 90% проводки» в звене
   Maestro↔arbiter↔логи уже сделаны.
3. **Недостающие звенья (реальный скоуп фазы 1):**
   - мостик `spec-runner TASK-nnn ↔ Maestro task.id` — данные у Maestro есть
     (spec_dir per workstream), нужна фиксация соответствия;
   - задействовать `report_outcome` (пустые `outcomes` = нет «чем закончилось»).
4. **Сюръективная проекция статусов подтверждена практикой:** `success/failed`
   (spec-runner) vs `pending/done/NEEDS_REVIEW` (Maestro) vs `assign/reject/fallback`
   (arbiter) — биекция была бы невозможна.

## Контрольный прогон (2026-07-11, вечер) — цепочка на данных

Один реальный ран: `maestro run` (advisory arbiter, `agent_type: auto`), задача
`corr-demo-note-2` (docs/python/trivial, scratch-репо). Полная цепочка одним ключом:

| Хранилище | Запись |
|-----------|--------|
| Maestro DB (`~/.maestro/maestro.db`) | `tasks.id=corr-demo-note-2`, status=`done` |
| arbiter `decisions` | id=22, `task_id=corr-demo-note-2`, `assign claude_code@claude-sonnet-4-6`, confidence 1.0 |
| arbiter `outcomes` | `task_id=corr-demo-note-2`, **`decision_id=22`** (FK работает), success, 0.21 min, $0.089 |
| JSONL (`Maestro/logs/01KX8V7Z9DHBKYWGSN2KTWM8AB/`) | `pipeline_id=01KX8V7Z9D...` + `TraceId=b11462b5...`, событие `outcome.recorded` |
| Артефакт | `NOTE.md` создан агентом корректно |

Корректировки к аудиту выше:

1. **`outcomes` больше не пуста — `report_outcome` работает.** «Спроектировано, но не
   используется» → «работает, но не было ни одного реального прогона». Связка
   decision→outcome подтверждена данными.
2. **Найден живой контрактный баг — словарный дрейф статусов в природе:**
   `report_outcome failed: Invalid status 'interrupted'. Must be one of: success,
   failure, timeout, cancelled` — Maestro шлёт статус вне enum arbiter'а (для
   rejected/NEEDS_REVIEW задачи). Это ровно тот несогласованный status-словарь,
   под который roadmap требует сюръективную проекцию. Кандидат на issue в Maestro.
3. **Первый reject тоже был информативен:** задача с `language: other` дала
   `No eligible agents` (никто в `agents.toml` не поддерживает `other`) — capability-
   фильтр работает, decision с action=reject тоже коррелируется по `task_id` (id=21).

## Что дальше

- ~~Read-side join прототип в dispatcher~~ **сделано**: dispatcher PR #5
  (`feat/work-items-correlation`) — `GET /api/work-items`, `core/correlation.py`,
  outcomes в arbiter-коллекторе. Проверено на живых данных: обе demo-цепочки
  восстанавливаются (assign→outcome + reject).
- ~~Issue про `interrupted`~~ **заведено**: Maestro #65.
- Остаётся: мостик `spec-runner TASK-nnn ↔ Maestro task.id` (фаза 1, минтер Maestro);
  UI-вкладка work-items в dispatcher SPA (после мержа PR #5).
