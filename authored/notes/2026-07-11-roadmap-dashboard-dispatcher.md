# Roadmap Dashboard: использовать Dispatcher как human control plane

> **Ревизия 2 (2026-07-11, ревью):** evidence matcher сведён к типизированным
> правилам (без regex-костылей, честный `unknown`); MVP-статусы сокращены до 4+1;
> `drift` переиспользует существующий `/api/contracts`; view Owners вынесен из MVP;
> добавлена связка `RoadmapItem.evidence_refs` ↔ work-item-цепочки из `/api/work-items`
> (dispatcher PR #5). Связанные доки: consolidated contracts roadmap
> (`prograph-vault/authored/notes/2026-07-11-ai-dark-factory-consolidated-roadmap.md`),
> `2026-07-11-roadmap-implementation-pipeline.md`.

## TL;DR

- Для отслеживания roadmap реализации нужен не файл с ручными отметками, а read-model/dashboard поверх evidence из проектов.
- Лучший существующий подпроект для этого - `dispatcher`: он уже является read-only monitoring dashboard для экосистемы.
- Новый подпроект создавать не надо. Практичнее добавить в `dispatcher` модуль `roadmap`.
- `steward`/`ecosystem-kb` должны владеть смыслом roadmap, gates и owner model; `dispatcher` должен только собирать факты и показывать computed status.
- Roadmap item считается выполненным не по галочке, а по найденному evidence: contract exists, consumer updated, checks passed, no drift.

---

## 1. Задача

Нужно отслеживать реализацию roadmap для человеческой команды.

Важно: речь не про отметки в markdown-файлах, а про dashboard, который показывает состояние реализации на основе фактов:

- какие roadmap items начаты;
- что реализовано;
- что заблокировано;
- где drift между spec и implementation;
- какие owners перегружены;
- какое evidence подтверждает статус;
- какие gates ещё не пройдены.

---

## 2. Лучший кандидат: `dispatcher`

Лучший существующий подпроект для этой задачи - `dispatcher`.

Он уже является read-only monitoring dashboard для AI-orchestrators ecosystem:

```text
dispatcher
 -> web dashboard
 -> TUI
 -> VSCode extension
 -> collectors
 -> /api/overview
 -> /api/projects/{name}
 -> /api/errors
 -> /api/models
 -> /api/contracts
```

Ключевой плюс: `dispatcher` уже работает как read-model поверх on-disk artifacts. Monitored projects не обязаны быть запущены. Missing projects просто не показываются или дают warnings.

Это ровно та модель, которая нужна для roadmap dashboard:

```text
roadmap intent + project evidence -> computed team-facing status
```

---

## 3. Почему не новый подпроект

Новый подпроект добавит:

- ещё один UI;
- ещё один API;
- ещё один collector layer;
- ещё одну точку drift;
- ещё одну ownership проблему.

В экосистеме уже есть `dispatcher`, который создан именно для monitoring/control-plane read-model. Поэтому roadmap dashboard должен быть extension внутри `dispatcher`, а не новым сервисом.

---

## 4. Почему не `steward` как dashboard

`steward` должен владеть governance:

- какие artifacts должны быть approved;
- какие gates обязательны;
- кто owner;
- какие dependencies между spec artifacts;
- когда downstream становится stale;
- как компилировать вниз в Maestro/spec-runner.

Но `steward` не должен становиться dashboard. Иначе он смешает:

```text
authoring/governance
monitoring/read-model
team UI
```

Правильная граница:

```text
steward defines gates
ecosystem-kb stores roadmap intent
projects emit evidence
dispatcher renders truth
```

---

## 5. Рекомендуемая архитектура

```text
prograph-vault / ecosystem-kb
  -> human-authored roadmap intent

steward
  -> governance model, gates, owner roles, approvals

arbiter / Maestro / ATP / spec-runner / proctor / deployer
  -> implementation evidence, logs, db rows, checks, contracts

prograph
  -> dependency graph / impact graph

dispatcher
  -> read-only collection, computed status, dashboard/API/TUI/VSCode

robin-runtime
  -> natural-language explanation over KB/status, not primary dashboard
```

Короткая формула:

```text
Intent lives in KB/steward.
Facts live in project artifacts.
Truth is rendered by dispatcher.
```

---

## 6. Что добавить в `dispatcher`

Добавить модуль:

```text
dispatcher.core.roadmap
dispatcher.core.collectors.roadmap
dispatcher.server /api/roadmap
Roadmap tab в web dashboard
Roadmap tab в TUI
Roadmap view в VSCode extension
```

Минимальные API:

```text
GET /api/roadmap
GET /api/roadmap/{item_id}
```

Опционально позже:

```text
GET /api/roadmap/phases
GET /api/roadmap/owners
GET /api/roadmap/drift
GET /api/roadmap/blockers
```

---

## 7. Минимальная модель `RoadmapItem`

```text
RoadmapItem:
- id
- title
- owner_project
- owner_role
- phase
- depends_on
- target_contract
- expected_evidence
- computed_status
- blockers
- last_seen
- evidence_refs
```

Где:

- `owner_project` - проект, отвечающий за реализацию;
- `owner_role` - роль из governance model / CODEOWNERS;
- `target_contract` - контрактная область: `WorkCorrelation`, `Budget`, `PolicyDecision`, `Evidence`, `RiskModel`, `Authority`, `LearningEvent`;
- `expected_evidence` - список фактов, которые dashboard должен уметь найти;
- `computed_status` - статус, рассчитанный из evidence;
- `evidence_refs` - ссылки на конкретные файлы, DB rows, API contracts, test results, logs.

**Связка с execution-уровнем:** `evidence_refs` должен уметь указывать на
work-item-цепочки из `GET /api/work-items` (dispatcher PR #5). `RoadmapItem` — уровень
intent, `WorkItemChain` — уровень execution; для items типа «изменение прошло через
routing/outcome» execution-evidence получается бесплатно из уже существующей корреляции.

---

## 8. Статусы

Статусы должны быть вычисляемыми, а не ручными.

**MVP — четыре статуса плюс blocked** (полный набор — позже):

```text
planned      # item описан, evidence не найдено
implemented  # все implementation-правила прошли
verified     # implementation + verification правила прошли
unknown      # evidence не выражается доступными правилами — честно unknown
blocked      # строго: depends_on не достиг implemented+
```

Сознательно НЕ в MVP:

- `in_progress` — «частичное evidence» неопределимо (частичное по числу правил —
  это шум, а не сигнал); item либо planned, либо implemented;
- `drift` — подключается вторым шагом как проекция существующего
  `/api/contracts` (canon vs vendored sync), НЕ отдельной механикой.

Пример интерпретации (полный целевой набор):

| Статус | Смысл |
|--------|-------|
| `planned` | item описан, evidence реализации не найдено |
| `blocked` | dependency из `depends_on` не достигла implemented+ |
| `implemented` | expected implementation evidence найдено |
| `verified` | implementation evidence + verification evidence найдены |
| `drift` | (после MVP) `/api/contracts` видит рассинхрон canon/vendored |
| `unknown` | roadmap item не может быть оценён из текущих правил |

---

## 9. Пример вычисления статуса

Roadmap item:

```text
Promote arbiter decision_id to PolicyDecisionRef v1
```

Expected evidence:

```text
- arbiter README/spec documents decision_id
- route_task response exposes metadata.decision_id
- Maestro stores arbiter_decision_id
- dispatcher can read and correlate decisions
```

Computed status:

```text
implemented
  if all implementation evidence present

verified
  if implementation evidence + tests/checks present

drift
  if arbiter exposes decision_id, but Maestro or dispatcher consumer is missing

blocked
  if owner project cannot emit required artifact
```

---

## 10. Что должен показывать dashboard

| View | Что показывает | Когда |
|------|----------------|-------|
| Roadmap Overview | фазы, прогресс, blocked items | MVP |
| Dependencies | что блокирует что | MVP |
| Evidence | почему item считается done/blocked | MVP |
| Contract Drift | где спецификация есть, а consumer не обновлён (из `/api/contracts`) | после MVP |
| Freshness | когда последний раз видели evidence | после MVP |
| Risk Gates | какие high-risk items без approval/test/evidence | после steward WS-002 |
| Owners | загрузка проектов/ролей — PM-аналитика, не evidence-модель | вне scope dashboard |

Минимальный первый экран:

```text
Phase | Item | Owner | Status | Blockers | Evidence | Freshness
```

---

## 11. Где хранить roadmap intent

Dashboard не должен зависеть от `_cowork_output/` как runtime source.

Для разработки черновики в `_cowork_output/` допустимы, но production/read-model должен читать canonical source.

Варианты:

| Вариант | Оценка |
|---------|--------|
| `prograph-vault/authored/roadmaps/*.yaml` | Лучший вариант для human-owned ecosystem roadmap |
| `steward/spec/40-decomposition.md` + profiles/gates | Хорошо, если roadmap должен быть governance-managed |
| отдельный `roadmap.yaml` в ecosystem-kb | Самый простой старт |
| `_cowork_output/*.md` | Только dev draft, не runtime source |

Рекомендация:

```text
roadmap definition -> prograph-vault/authored/roadmaps/
approval/gates -> steward
visualization -> dispatcher
```

---

## 12. Как roadmap item считается выполненным

Roadmap item считается выполненным не потому, что кто-то поставил галочку, а потому что `dispatcher` нашёл evidence:

```text
spec exists
contract exported
consumer updated
tests/checks passed
dashboard can correlate
no drift detected
```

Это важное отличие от markdown checklist.

Ручные отметки допустимы только как intent/status override с audit trail, но не как primary truth.

---

## 13. MVP

Минимальный MVP для `dispatcher`:

1. Прочитать roadmap YAML из `prograph-vault/authored/roadmaps/`.
2. Добавить модель `RoadmapItem`.
3. Добавить `expected_evidence` как **типизированные правила** — маленький закрытый
   набор, никакой прозы и никаких regex:
   - `project_detected(name)`;
   - `file_exists(project, relpath)`;
   - `sqlite_has_row(project, db, query)` — read-only, как в существующих коллекторах;
   - `contract_in_sync(name)` — делегирование в существующий contracts-checker;
   - `work_item_chain(work_item_id, min_links)` — делегирование в `/api/work-items`.

   **Правило честности:** item, чьё evidence не выражается этим набором, остаётся
   `unknown`. Расширять набор правил — да; подгонять item под правила regex-костылём —
   нет. Прозаичные `expected_evidence` («Maestro persists decision_id») — это
   документация намерения, машинная проверка живёт только в типизированных правилах.
4. Добавить `/api/roadmap`.
5. Добавить web tab `Roadmap`.
6. Добавить TUI tab `Roadmap` (можно вторым PR).

Не включать в MVP:

- сложный query language;
- запись статусов;
- GitHub API;
- автоматическое создание issues;
- ML/LLM summary;
- runtime mutations.

---

## 14. Рекомендуемые действия

| Проект / контекст | Действие | Приоритет |
|-------------------|----------|-----------|
| `dispatcher` | Добавить `roadmap` module и `/api/roadmap` | P1 |
| `dispatcher` | Добавить Roadmap tab в web dashboard | P1 |
| `dispatcher` | Добавить Roadmap tab в TUI | P2 |
| `prograph-vault` / ecosystem-kb | Завести canonical `authored/roadmaps/*.yaml` | P1 |
| `steward` | Связать roadmap items с owner_role/gates/approval model | P2 |
| `prograph` | Позже дать dependency graph для roadmap blockers | P2 |
| `robin-runtime` | Позже давать natural-language briefing по roadmap status | P3 |

---

## 15. Главный вывод

Для human-team dashboard по roadmap не нужен новый проект.

Нужно расширить `dispatcher`:

```text
dispatcher = operational read-model / dashboard
roadmap module = computed status over ecosystem evidence
```

А смысл и governance должны остаться у `steward` и ecosystem-kb:

```text
steward defines gates
ecosystem-kb stores roadmap intent
projects emit evidence
dispatcher renders truth
```
