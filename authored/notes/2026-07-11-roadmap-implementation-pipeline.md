# Pipeline реализации roadmap средствами экосистемы

> **Ревизия 2 (2026-07-11, ревью). Статус документа: целевая архитектура (north
> star), НЕ план ближайших работ.** Петля требует механик из фаз 1–4 contracts
> roadmap (`evidence_ref` — фаза 3, gates — фаза 4, steward compile-target — после
> WS-002) — см. новый раздел «Хронология». Добавлена глава про главный
> непроработанный пробел: DAG-ноды, ждущие человеческого мержа (PR-only канон).
> MVP переформулирован из-за bootstrap-парадокса. Ближайший исполнимый шаг —
> dashboard (`2026-07-11-roadmap-dashboard-dispatcher.md`), не петля.
> Канон фаз: `prograph-vault/authored/notes/2026-07-11-ai-dark-factory-consolidated-roadmap.md`.

## TL;DR

- Roadmap надо исполнять как governed workflow, а не как список ручных задач.
- Целевая петля: `roadmap intent -> steward governance bundle -> Maestro DAG -> spec-runner leaf tasks -> arbiter routing -> ATP verification -> dispatcher evidence dashboard`.
- `steward` отвечает за "можно ли и под какими gates", `Maestro` - за координацию workstreams, `spec-runner` - за leaf execution, `arbiter` - за routing/policy decision, `ATP` - за verification, `dispatcher` - за computed status.
- Новый "roadmap executor" не нужен. Нужны compile targets, task templates, verification profiles и общий `evidence_ref`.
- Roadmap item считается выполненным только после evidence: contract exists, consumers updated, checks passed, no drift.

---

## 1. Задача

Есть roadmap по развитию экосистемы:

- изменить контракт;
- добавить модуль в `Maestro`;
- поменять код в `arbiter`;
- обновить consumer в `dispatcher`;
- добавить verification в `atp-platform`;
- обновить docs / schemas / drift checks.

Нужно настроить pipeline его реализации средствами самой экосистемы, а не через внешний project-management слой.

Ключевая идея:

```text
Roadmap item должен становиться исполняемым governed workflow.
```

---

## 2. Целевая петля

```text
Roadmap intent
 -> steward governance bundle
 -> spec-runner task specs
 -> Maestro execution DAG
 -> arbiter routing / policy decisions
 -> atp-platform verification
 -> dispatcher roadmap dashboard
 -> learning / updates
```

В более операционной форме:

```text
Intent
 -> Design / Acceptance
 -> Decomposition
 -> DAG
 -> Leaf tasks
 -> Routed execution
 -> Verification gates
 -> Evidence
 -> Dashboard status
```

---

## 3. Роли подпроектов

| Компонент | Роль в pipeline |
|-----------|-----------------|
| `prograph-vault` / ecosystem-kb | Хранит roadmap intent: фазы, цели, контракты, owners |
| `steward` | Превращает roadmap item в governance bundle: requirements, design, acceptance, decomposition |
| `prograph` | Делает impact/dependency analysis: какие проекты и контракты затронуты |
| `Maestro` | Оркестрирует workstreams/DAG: параллельные ветки, зависимости, интеграция |
| `spec-runner` | Исполняет leaf task specs: конкретные изменения в репозиториях |
| `arbiter` | Выбирает агента/исполнителя, применяет routing/policy/budget decisions |
| `atp-platform` | Проверяет результат: tests, evals, benchmarks, regression checks |
| `dispatcher` | Показывает статус реализации roadmap по evidence |
| `robin-runtime` | Позже объясняет состояние roadmap на естественном языке |

---

## 4. Как выглядит один roadmap item

Пример:

```text
RD-002: Promote arbiter decision_id to PolicyDecisionRef v1
```

Как roadmap intent:

```yaml
id: RD-002
title: Promote arbiter decision_id to PolicyDecisionRef v1
owner_project: arbiter
owner_role: "@routing"
phase: contracts-v1
target_contract: PolicyDecisionRef
risk_level: medium
depends_on:
  - RD-001
expected_evidence:
  - arbiter route_task response documents metadata.decision_id
  - Maestro persists arbiter_decision_id
  - dispatcher can correlate decisions
  - ATP regression passes
```

Этот item не должен напрямую превращаться в список ручных checkbox. Он должен пройти governance и decomposition.

---

## 5. `steward`: governance bundle

`steward` открывает governance bundle:

```text
charter / problem
requirements
design
acceptance
decomposition
```

В bundle фиксируются:

- owner;
- affected projects;
- acceptance criteria;
- risk level;
- required gates;
- approval role;
- expected evidence;
- compile-down targets;
- rollback / rework rules.

Назначение `steward`:

```text
should we do it?
under what gates?
who must approve?
what counts as done?
```

---

## 6. `prograph`: impact analysis

Перед исполнением `prograph` должен дать impact/dependency picture:

```text
affected projects
contract consumers
vendored copies
known drift points
dependency edges
test surfaces
```

Пример для изменения `arbiter` contract:

```text
arbiter
 -> Maestro
 -> dispatcher
 -> tests / fixtures
 -> COWORK_CONTEXT contract docs
 -> ATP verification profiles
```

Это помогает `steward` и `Maestro` не пропустить consumers и drift points.

---

## 7. `Maestro`: execution DAG

`steward` компилирует `decomposition` в `Maestro project.yaml`.

Пример DAG:

```yaml
workstreams:
  - id: arbiter-contract
    title: Update arbiter PolicyDecisionRef contract
    depends_on: []

  - id: maestro-consumer
    title: Update Maestro consumer / persistence
    depends_on: [arbiter-contract]

  - id: dispatcher-evidence
    title: Add dispatcher evidence matcher
    depends_on: [arbiter-contract]

  - id: verification
    title: Add ATP regression and drift checks
    depends_on: [maestro-consumer, dispatcher-evidence]
```

Назначение `Maestro`:

```text
how to coordinate execution?
what can run in parallel?
what depends on what?
when can integration happen?
```

---

## 8. `spec-runner`: leaf task execution

Каждый workstream разворачивается в конкретные task specs для `spec-runner`.

Пример:

```text
TASK-001: update arbiter contract docs/schema
TASK-002: update route_task typed response tests
TASK-003: update Maestro consumer
TASK-004: add dispatcher evidence matcher
TASK-005: add ATP regression check
TASK-006: update contract drift check
```

`spec-runner` хорош именно для leaf-level deterministic execution:

- конкретная правка;
- конкретный scope;
- конкретные acceptance criteria;
- локальная проверка;
- report/evidence.

Назначение `spec-runner`:

```text
how to execute this leaf task reproducibly?
```

---

## 9. `arbiter`: routing and policy decision

`Maestro` при запуске workstream может обращаться к `arbiter`:

```text
task features -> route_task -> chosen agent + confidence + decision_id
```

Это даёт:

- capability routing;
- budget awareness;
- decision trace;
- fallback/reject path;
- later correlation через `decision_id`.

`arbiter` не должен владеть roadmap semantics. Его роль в pipeline:

```text
who/what should execute this task?
under current policy and budget, is routing allowed?
```

---

## 10. `atp-platform`: verification gates

Для каждого roadmap item должны быть verification gates.

Примеры:

```text
unit tests pass
contract tests pass
cross-repo consumer tests pass
benchmark/eval if relevant
regression check
drift check
security/static check if risk requires
```

`atp-platform` может быть verification backbone, особенно для:

- agent/eval-heavy изменений;
- regression checks;
- benchmark-aware routing;
- quality gates;
- cross-project verification reports.

Назначение `ATP`:

```text
did it actually work?
what evidence proves it?
```

---

## 11. `dispatcher`: roadmap status by evidence

`dispatcher` не должен читать ручные checkbox как primary truth.

Он должен вычислять:

```text
planned
in_progress
blocked
implemented
verified
drift
unknown
```

по evidence:

```text
contract file exists
tests pass
consumer updated
decision_id visible
ATP result exists
no contract drift
```

Назначение `dispatcher`:

```text
what is the actual state?
why does the system think so?
what is blocked or drifting?
```

---

## 11a. Хронология: петля против фаз contracts roadmap

Петля не строится «сразу вся» — её куски привязаны к фазам consolidated roadmap:

| Кусок петли | Пререквизит | Статус пререквизита |
|-------------|-------------|---------------------|
| dispatcher computed status | ничего нового | ✅ можно сейчас (паттерн PR #5) |
| `decision_id` correlation | фаза 0.5/2 (`PolicyDecisionRef`) | ✅ 0.5 закрыта, promote — фаза 2 |
| `evidence_ref` сквозной | фаза 3 | ⏳ не начата |
| Risk/mandatory gates | фаза 4 + steward WS-002 | ⏳ steward ещё в WS-001 |
| steward compile-target `decomposition → project.yaml` | steward WS-002+ | ⏳ не существует |
| `LearningEvent` (петля «learning/updates») | фаза 6 | ⏳ последняя |

Правило: **кусок петли строится только когда его фаза дошла** — иначе это
«семь SSOT сразу» в новой одежде (compile targets + templates + profiles
веером по восьми репо).

## 11b. Главный непроработанный пробел: человек в петле

Канон экосистемы — PR-only, мерж делает человек. Следствие, которого в петле нет:

- leaf task spec-runner'а в чужом репо завершается не «done», а **«PR открыт»**;
- DAG-нода после этого должна ждать человеческого мержа — часы или дни;
- Maestro сегодня спавнит агентов и ждёт минуты; **долгоживущих DAG с ожиданием
  внешних событий (merge webhook / poll) в нём нет**.

Без этой механики петля работает только в вырожденном случае «все изменения в одном
репо». Варианты решения (выбрать при проектировании, не по умолчанию):
(а) DAG-нода паркуется в существующий `NEEDS_REVIEW` и ран возобновляется
`--resume` после мержа — дёшево, использует готовый механизм;
(б) отдельный «merge-wait» тип ноды с poll GitHub API — дороже, честнее.
Рекомендация для первой итерации: (а).

## 12. Что нужно добавить, чтобы pipeline стал реальным

Минимальные additions:

| Что добавить | Где | Зачем |
|--------------|-----|-------|
| `RoadmapItem` schema | ecosystem-kb или `steward` | Canonical roadmap intent |
| Roadmap item -> governance bundle | `steward` | Перевести intent в requirements/design/acceptance/decomposition |
| Decomposition -> `Maestro project.yaml` | `steward` compile target | Получить execution DAG |
| Cross-repo task templates | `spec-runner` | Типовые leaf tasks для contract/code/docs/test changes |
| Roadmap implementation DAG template | `Maestro` | Стандартизировать workstreams |
| Verification profiles | `atp-platform` | Проверять roadmap items одинаково |
| `/api/roadmap` | `dispatcher` | Показывать computed status |
| `evidence_ref` format | cross-project contract | Связать tasks, checks, decisions, artifacts |

---

## 13. Минимальный MVP pipeline

MVP должен быть узким:

```text
RD item -> steward bundle -> Maestro DAG -> spec-runner tasks -> ATP verification -> dispatcher status
```

Без:

- автоматической записи в чужие репозитории без approval;
- сложного LLM planning loop;
- автоматического merge/deploy;
- GitHub issue sync;
- multi-org RBAC;
- универсального WorkItem SSOT.

### MVP scope

1. Один roadmap item.
2. Один owner project.
3. Один consumer project.
4. Один verification gate.
5. Один dispatcher status.

**Bootstrap-парадокс (важно):** нельзя выбрать MVP-item, который сам является
пререквизитом петли. `RD-002 PolicyDecisionRef` — как раз такой (петля опирается на
`decision_id`-корреляцию). Поэтому:

- **первые items contracts roadmap исполняются руками/полуруками** (обычный
  PR-flow), а dashboard их только *наблюдает* по evidence — это уже ценность;
- полная governed-петля включается с items, у которых её пререквизиты (фазы 1–3)
  закрыты. Петля — **результат** roadmap, а не средство для его первых пунктов.

Пример честного MVP: `RD-002` исполняется вручную через PR-flow, а MVP-проверка —
что dispatcher `/api/roadmap` сам довёл его статус до `implemented`/`verified`
по evidence, без ручной галочки.

---

## 14. Pipeline для cross-repo contract change

Типовой шаблон:

```text
1. steward: approve requirements/design/acceptance
2. prograph: list consumers and vendored copies
3. Maestro: create DAG:
   - owner contract update
   - consumer updates
   - tests/fixtures
   - docs/context
   - verification
4. spec-runner: execute leaf tasks
5. arbiter: route tasks and emit decision_id
6. ATP: run contract/regression checks
7. dispatcher: compute roadmap item status
8. steward: mark governance bundle approved/stale based on evidence
```

---

## 15. Pipeline для new module in `Maestro`

Типовой шаблон:

```text
1. steward: design gate for module responsibility and boundaries
2. prograph: identify affected contracts and projects
3. Maestro: self-hosted workstream DAG
4. spec-runner: leaf tasks for implementation/tests/docs
5. arbiter: route coding/review/test tasks
6. ATP: run module tests + scenario eval
7. dispatcher: detect new module evidence and health
```

Critical gates:

```text
module has clear owner
no duplicate responsibility with existing service
public contract documented
tests and examples present
dispatcher can observe health/status
```

---

## 16. Pipeline для code change in `arbiter`

Типовой шаблон:

```text
1. steward: classify risk: routing/policy/budget/contract
2. prograph: list downstream consumers
3. Maestro: split into implementation + consumer + verification workstreams
4. spec-runner: execute Rust/Python tasks
5. arbiter: local tests + contract tests
6. ATP: scenario/regression benchmark if routing affected
7. dispatcher: verify budget/decision/contract evidence
```

Critical gates:

```text
route_task contract unchanged or versioned
decision_id correlation preserved
budget behavior verified
benchmark_runs compatibility preserved
Maestro consumer still passes
dispatcher collector still reads expected evidence
```

---

## 17. Главный принцип

Не надо строить отдельный "roadmap executor".

Лучше использовать существующую цепочку:

```text
steward = should we do it and under what gates?
Maestro = how to coordinate execution?
spec-runner = how to execute leaf tasks?
arbiter = who/what should execute?
ATP = did it work?
dispatcher = what is the actual state?
```

Это превращает roadmap в управляемый production workflow, а не в список пожеланий.

---

## 18. Рекомендуемые действия

Приоритеты пересобраны по хронологии (раздел 11a): P1 — только то, что не ждёт
недостроенных фаз; остальное стейджится за своими пререквизитами.

| Проект / контекст | Действие | Приоритет | Ждёт |
|-------------------|----------|-----------|------|
| ecosystem-kb / `prograph-vault` | Описать `RoadmapItem` schema и canonical roadmap location | P1 | — |
| `dispatcher` | Добавить `/api/roadmap` и computed status по evidence | P1 | — |
| `arbiter` | Гарантировать emission/correlation `decision_id` для execution tasks | P2 | фаза 2 (promote) |
| `prograph` | Impact-analysis feed для roadmap decomposition | P2 | — |
| `steward` | Flow `roadmap item -> governance bundle` | P2 | WS-002 |
| `steward` + `Maestro` | Compile target `decomposition -> project.yaml` | P3 | WS-002 + механика merge-wait (11b) |
| `spec-runner` | Templates для cross-repo contract/code/docs/test tasks | P3 | merge-wait (11b) |
| `atp-platform` | Verification profiles для roadmap items | P3 | фаза 3 (`evidence_ref`) |
