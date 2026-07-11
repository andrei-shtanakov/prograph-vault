# AI Dark Factory — консолидированный roadmap контрактов

> **Что это.** Единый документ, сводящий четыре источника в один roadmap:
> `ai-dark-factory-workflow-first.md` (теория), `current-projects-to-ai-dark-factory-objects.md`
> (маппинг), `ai-dark-factory-contracts-critical-review.md` (критика) и
> `2026-07-11-openopc-borrowable-ideas.md` (внешний источник паттернов).
> **Заменяет** их как рабочий roadmap; исходники остаются как история.
> Дата: 2026-07-11. Роль: TPM / systems architect. Все ссылки — на реальные файлы репо.
> **Ревизия 2 (2026-07-11, вечер):** graduation observability-contract уже выполнен
> (`6795b26`) — Часть III и фаза 3 обновлены; биективность status-map заменена на
> сюръективную проекцию; добавлены критерий выбора минтера и exit-критерии фаз 0.5–2.

## TL;DR

- Направление **workflow-first, а не имитация оргструктуры** — верное и совпадает с уже идущими ADR (gated authoring, model/catalog SSOT, observability-contract). Спорна не концепция, а форма roadmap.
- **Не вводить семь SSOT сразу** — это координационная бомба для полирепо. Правильная рамка: **повысить уже частично построенное** (arbiter budget/`decision_id`, steward gates, observability-contract) до именованных контрактов + тонкий correlation-слой.
- **Порядок:** `correlate first → promote existing → govern → learn last`. Один enabler (`WorkCorrelation`) + три promote, затем `Authority`/`Risk`, затем `LearningEvent`.
- **Две вещи, которых не было ни в одном исходнике и без которых roadmap не стартует:** (1) явный **forcing function** — какая боль сегодня оправдывает работу; (2) **runtime-владелец** `WorkCorrelation` — по критерию «кто первым создаёт работу в потоке», а не «ecosystem-kb / TBD».
- **Ревизия 2:** graduation observability-contract **уже выполнен** (`Maestro/contracts/observability/`, `6795b26`) — фаза 3 сокращена до `evidence_ref`; status-map — сюръективная проекция с сохранением `source_status`, не биекция; фаза 0.5 обязана проверить достаточность существующих ключей (trace_id/run_id) до минтинга нового id.
- **OpenOPC — внешний источник паттернов, не продукт.** Из него берём transition-table, gates-in-DAG, adapter-registry, gate-verdict/escalation; НЕ берём монолит, org-theater, fail-open и неаудируемый self-authoring.

---

## Часть I. Теория: workflow-first, не оргметафора

Для AI dark factory почти без людей копирование человеческой оргструктуры релевантно
лишь частично. Главный архитектурный объект — не роль и не отдел, а **управляемый контур
выполнения работы**:

```text
Goal → WorkItem → Capability → Authority → Policy → Execute → Verify → Evidence → Decide → Deliver → Learn
```

Роли полезны только как **runtime-функции** (accountability slots, capability profiles,
authority boundaries, policy gates, memory scopes, verification responsibilities, cost
controls), а не как HR-должности. Человеческая оргметафора — допустимый **внешний
интерфейс для бизнеса**, но внутренний двигатель — workflow/capability/policy engine.
Иначе получается «дорогой театр агентов».

---

## Часть II. Маппинг экосистемы на объекты dark factory

Сверено с `COWORK_CONTEXT.md` (реестр от 2026-07-08).

| Проект | Роль в dark factory | Подтверждение |
|--------|---------------------|---------------|
| `spec-runner` | Execution / task-spec engine | `COWORK_CONTEXT.md:38` |
| `Maestro` | DAG / planning / orchestration | `COWORK_CONTEXT.md:37` |
| `arbiter` | Routing / policy / cost / benchmark-aware decision | `COWORK_CONTEXT.md:36` |
| `atp-platform` | Verification / evaluation / quality gates | `COWORK_CONTEXT.md:35` |
| `steward` | Spec governance / approval gates | `COWORK_CONTEXT.md:48` |
| `dispatcher` | Read-only observability / control-plane read model | `COWORK_CONTEXT.md:46` |
| `deployer` | Author ≠ execute pipeline (L1 static → L2 sandboxed) | `COWORK_CONTEXT.md:45` |
| `prograph` / `prograph-vault` (ecosystem-kb) | Impact-analysis граф / память-KB | `COWORK_CONTEXT.md:53,67` |
| `robin-runtime` | Knowledge interface / chief-of-staff | `COWORK_CONTEXT.md:54` |

Ключевая мысль: **дыры не в компонентах, а в кросс-проектных контрактах.** Экосистема
именно так и растёт — через маленькие pinned/vendored контракты, а не через один рантайм.

---

## Часть III. Что уже построено частично (promote, а не build)

Половина «недостающих сущностей» существует на 40-60%. Ссылки проверены по коду.

| Область | Что уже есть | Файл |
|---------|--------------|------|
| `Budget/Cost` | `get_budget_status` — total spent, limit, remaining, per-agent breakdown | `arbiter/README.md:216-218` |
| `PolicyDecision` | `route_task` → `decision_id` в `response.metadata`; 10 safety-invariants | `arbiter/README.md:62-74`; `COWORK_CONTEXT.md:248-256` |
| `Evidence` (input) | `report_benchmark` → `benchmark_runs`, идемпотентно по `run_id` | `arbiter/README.md:234-236` |
| `Authority` (governance) | Артефакт=файл+frontmatter, approval=PR ревью CODEOWNERS, `status:approved`=зеркало git | `steward/README.md:53-57` |
| `Authority` (traceability) | Frontmatter `owner_role`/`approved_by`/`approved_at`/`traces_to` | `steward/spec/20-design.md:48-59` |
| `Evidence` (envelope) | observability-contract: log-schema.json + trace context + 4 golden fixtures | `Maestro/maestro/_vendor/obs.py:1-8`; `COWORK_CONTEXT.md:278-287` |
| State-core reuse | steward переиспользует SpecMeta, не плодит второй state-движок | `steward/spec/20-design.md:38-39` |

Вывод: правильный шаг — не «ввести с нуля», а `promote arbiter.get_budget_status → Budget
v1`, `promote decision_id → PolicyDecision ref v1`, `graduate observability-contract → Evidence`.

**Обновление (drift закрыт):** observability-contract уже выехал из `_cowork_output` в
`Maestro/contracts/observability/` (log-schema.json + fixtures + propagation.md) — коммит
`6795b26` «graduate contract authority out of _cowork_output (ADR 2026-07-07)» (Maestro #60).
Владелец де-факто определился — Maestro. Урок остаётся в силе: «контракт без runtime-дома» —
анти-паттерн, который нельзя повторять с новыми сущностями.

---

## Часть IV. Семь контрактных областей и их владельцы

Не «семь недостающих сущностей», а **семь целевых областей, часть уже частично реализована**.
Без **единого владельца** контракт — это shared vocabulary без enforceability. Паттерн
экосистемы: single-owner + pinned consumers (atp владеет catalog, spec-runner — SpecMeta,
steward — profiles/gate-check, Maestro — project.yaml).

| Область | Владелец | Consumers | Статус |
|---------|----------|-----------|--------|
| `WorkCorrelation` (id+status+refs) | **Maestro или spec-runner (runtime-минтер), НЕ ecosystem-kb** | dispatcher, arbiter, steward, atp | новый, тонкий |
| `Budget` | arbiter | Maestro, dispatcher, proctor | promote |
| `PolicyDecision` | arbiter (routing) + steward (approval) | Maestro, dispatcher, proctor | promote |
| `Evidence` envelope | Maestro (graduation выполнен, `6795b26`) | arbiter, deployer, dispatcher, robin | расширить (`evidence_ref`) |
| `Risk model` | steward | arbiter, atp, Maestro | новый |
| `Authority` | steward (approval/governance) + proctor (runtime admission) | arbiter, Maestro, dispatcher | split из существующего |
| `Capability` | arbiter | Maestro, proctor | есть (routing) |
| `LearningEvent` | atp + ecosystem-kb | robin-runtime, prograph-vault, dispatcher | последний |

### `WorkCorrelation` — заменяет `WorkItem SSOT`

Не универсальный объект поверх spec-tasks/DAG-нод/benchmark-runs/governance-items (у них
разные lifecycle и владельцы — это monorepo-мышление в модели данных). Вместо этого —
тонкий **correlation-контракт**:

```text
WorkCorrelation:
- work_item_id            # join-key между проектами
- parent_work_item_id?    # иерархия
- status                  # МИНИМАЛЬНЫЙ общий enum (см. предупреждение ниже)
- source_project          # каждый проект владеет своей локальной схемой
- source_local_id
- source_status           # локальный статус ДОСЛОВНО (без него проекция теряет аудируемость)
- evidence_refs[]?        # ПОЗДНЕЕ (см. Часть VII, фаза 3) — не в v1
```

**Критерий выбора минтера** (снимает «Maestro или spec-runner»): минтер — тот, кто
**первым создаёт работу в потоке**. Если канонический поток «спека → DAG», минтер —
spec-runner, Maestro пропагирует id; если работа рождается и в обход спек (ad-hoc DAG) —
Maestro. Решение принять по итогам фазы 0.5, но по этому критерию, а не «кому удобнее».

**Предупреждение о `status` (трудные 60%).** «Минимальный общий enum» звучит дёшево, но
это семантический маппинг несовместимых словарей: steward — git-зеркало
`draft|approved|stale`; Maestro DAG-ноды — `NEEDS_REVIEW` + spawn-sentinel `-1`;
spec-runner — `ExecutorState`; arbiter — routing. Именно тут живёт «разные проекты говорят
несовместимыми языками». **Не требовать биективности** — четыре словаря разной
гранулярности биективно на общий enum не лягут. Правильная рамка: **сюръективная проекция**
(many-to-one) на минимальный общий enum, с сохранением `source_status` дословно рядом.
Общий статус — честная lossy-проекция для drill-down, а не претензия на семантическую
эквивалентность; это и есть OpenOPC-паттерн «статус = SoT, остальное = чистые проекции».
Избегать статусов, требующих внешнего контекста для проекции.

---

## Часть V. Forcing function (чего не было ни в одном исходнике)

Ни один из четырёх документов не называл **конкретную боль, которую эти контракты
предотвратили бы**. Без forcing function это premature abstraction. Кандидаты, от сильного
к слабому:

1. **Cross-project drill-down в dispatcher/robin.** dispatcher уже read-only собирает
   артефакты всех 5 проектов (`dispatcher/dispatcher/core/collectors/`), но **не может
   связать** «спека X → DAG-ран Y → benchmark Z → approval W» единым ключом. Это реальная,
   сегодняшняя, дешёвая-в-проверке боль. **Рекомендуемый forcing function.**
2. **Status-рассинхрон.** OpenOPC своим же docstring (`phase.py:1-19`) показывает, во что
   выливается «status + N расходящихся sub-state полей». У нас риск того же при росте связок.
3. **Аудит delivery-решений.** «Почему артефакт принят, кто разрешил, какие проверки
   реально прошли» — пока не отвечается единообразно.

Если forcing function = (1), то **владелец фазы 1 следует оттуда** (dispatcher как полигон,
Maestro/spec-runner как минтер), а не из KB — и OpenOPC перестаёт быть dangling reference.

---

## Часть VI. OpenOPC как внешний источник паттернов

> `HKUDS/OpenOPC` — **внешний репо**, временно в чекауте для изучения. Не подпроект, не
> зависимость, не кандидат на вендоринг кода. Только идеи. Полный разбор:
> `_cowork_output/2026-07-11-openopc-borrowable-ideas.md`.

Инженерно ценное в OpenOPC — **ровно наш workflow-first слой**, а не оргметафора, которой
он торгует. Топ заимствований:

| Паттерн OpenOPC | Куда у нас | Брать? |
|-----------------|-----------|--------|
| Статическая transition-table + `_UNIVERSAL_EXITS={FAILED,CANCELLED}` + `_RECOVERY_EXITS={READY}`; статус=SoT, всё остальное=чистые проекции (`phase.py:206-421`) | backbone `WorkCorrelation` / Maestro | **Да, топ-1** (~80 строк, 0 зависимостей) |
| Гейты **внутри DAG**: `gate:{type: review\|approval, reviewer_role}` + `toolset`=allowlist (`vc_investment_firm.yaml:239-404`) | Risk-гейты исполняемы / Maestro+steward+atp | **Да, скелет** |
| Adapter-registry харнессов `is_available`/`describe`/preferred-order (`adapters/registry.py`) | routing / arbiter+Maestro | **Да** (у нас уже есть harness-ось — выровнять) |
| Гейт-вердикт `pass\|rework\|escalate` + `blocker_fingerprint` streak-эскалация (`gate_harness.py:175,360`) | `PolicyDecision`+`Risk` / atp+steward | **Да, но fail-closed** (у них fail-open) |
| Escalation: timeout→default + `approval_context` (`escalation.py`) | `Authority` / steward | **Да** |

**НЕ копировать:** монолит и org-theater (650-строчные prose-контракты, оргчарты, митинги,
bull/bear-дебаты); `metadata_ownership` на ~130 ключей; **fail-open** по умолчанию;
неаудируемый runtime `save_skill`. Последние два — ровно тот drift, против которого мы
строим steward+LearningEvent; их слабость валидирует наш дизайн, а не копируется.

---

## Часть VII. Фазовый roadmap

Логика: `correlate first → promote existing → govern → learn last`.

| Фаза | Действие | Владелец | Почему так / OpenOPC-паттерн |
|------|----------|----------|------------------------------|
| 0 | Зафиксировать `agent theater` checklist (Часть VIII) как rule; OpenOPC = external idea-source | ecosystem-kb | дешёвое знание, сразу полезно для ревью |
| 0.5 | **Прототип correlation как read-side join в dispatcher** — без эмиттеров, без миграций. Обязательная часть: выяснить, **хватает ли существующих ключей** (trace_id/run_id из observability-contract; `run_id` в `report_benchmark`) до минтинга нового id | dispatcher | доказывает контракт и forcing function (V.1) при нулевой стоимости; возможно, join-key уже существует и «тяжёлые 90% проводки» частично сделаны |
| 1 | `WorkCorrelation v1` = `work_item_id + status + source_project + source_local_id + source_status`; **минтер — по критерию «кто первым создаёт работу»** (Часть IV), НЕ KB; если 0.5 показал достаточность trace_id/run_id — v1 наследует его, а не вводит новый | Maestro/spec-runner | join-key; backbone = transition-table из `phase.py` (топ-1 борроу) |
| 2 | Promote arbiter budget + `decision_id` → `Budget v1` / `PolicyDecisionRef v1` | arbiter | уже частично построено (Часть III) |
| 3 | ~~Graduate observability-contract~~ **сделано** (`Maestro/contracts/observability/`, `6795b26`). Осталось: добавить `evidence_ref` поверх trace_id/span_id/run_id; включить в `WorkCorrelation` | Maestro | drift закрыт до консолидации; только теперь `evidence_refs[]` осмыслен |
| 4 | `Risk model` + mandatory gates; оценить **gates-in-DAG** (`gate:{type,reviewer_role}` на узле project.yaml) | steward | steward владеет gate-check; OpenOPC-скелет делает Risk-гейты исполняемыми без центр. оргмодели |
| 5 | Разделить `Capability` (arbiter) и `Authority` (steward); enforcement — role/phase-scoped allowlist | arbiter+steward | после PolicyDecision+Risk границы понятны |
| 6 | `LearningEvent` — через steward-governance (PR/CODEOWNERS), не silent-write | atp+ecosystem-kb | последний слой: потребляет evidence/risk/decisions/outcomes; **не повторять OpenOPC `save_skill`** |

**Порядок исправлений относительно исходного ревью:** (а) владелец фазы 1 — минтер, не
«TBD в KB»; (б) добавлена фаза 0.5 (dispatcher-полигон); (в) `evidence_refs[]` убран из v1
и перенесён в фазу 3 (иначе поле ссылается в пустоту до graduation Evidence);
(г, ревизия 2) фаза 3 сокращена — graduation уже выполнен (`6795b26`), владелец Maestro.

**Exit-критерии ранних фаз** (без них фазы остаются «в процессе» бесконечно):

- **0.5:** dispatcher показывает цепочку «спека X → DAG-ран Y → benchmark Z» для одного
  реального прогона; письменно зафиксировано, каких связей существующим ключам не хватает.
- **1:** минтер + хотя бы один консюмер резолвят один и тот же `work_item_id` в свои
  локальные объекты (round-trip, не только эмиссия).
- **2:** dispatcher читает `Budget v1` / `PolicyDecisionRef v1` по pinned-схеме, а не через
  внутренний API arbiter.

---

## Часть VIII. Anti-pattern checklist «agent theater»

Признаки, что система скатилась в дорогой театр агентов (выносится в `ecosystem-kb` как rule):

- много ролей, но мало проверяемых gates;
- агенты общаются без artifact contracts;
- нет acceptance criteria на каждый шаг;
- нет evidence trail;
- verification слабее generation;
- роли названы как должности, но без authority boundary;
- много «совещаний агентов», мало результатов;
- нет cost accounting и stop conditions;
- learning loop не обновляет evals/policies/playbooks (только копит заметки).

---

## Часть IX. Чего НЕ делать

- **Не вводить семь SSOT сразу** — координационная бомба для полирепо.
- **Не делать `WorkItem SSOT`** как универсальный объект — это monorepo-мышление; экосистема
  сознательно выбрала polyrepo (`prograph-vault/.../2026-05-25-polyrepo-workflow-setup.md`).
- **Не парковать enabler-контракт в рантайм-less KB** с «owner TBD» — это повтор drift
  анти-паттерна observability-contract (закрыт `6795b26`, но урок остаётся).
- **Не копировать из OpenOPC** монолит/org-theater, fail-open, `metadata_ownership`-реестр,
  неаудируемый self-authoring.
- **Не строить контракт без runtime-эмиттера** — определение envelope это лёгкие 10%,
  проводка через полирепо это тяжёлые 90%.

---

## Оценка (сводно)

| Измерение | Оценка | Комментарий |
|-----------|--------|-------------|
| Концепция (workflow-first, anti-theater) | 8/10 | сильная, совпадает с ADR-направлением |
| Маппинг проектов | 7/10 | верен, недооценивал частичные реализации (исправлено, Часть III) |
| Roadmap (после консолидации) | 6→7/10 | добавлены владельцы, forcing function, фаза 0.5, порядок исправлен |
| Готовность к реализации | 6→7/10 | graduation Evidence уже выполнен (`6795b26`); критерий минтера и exit-критерии зафиксированы; остаётся прототип 0.5 |

---

## Рекомендуемые действия

| Проект / контекст | Действие | Приоритет |
|-------------------|----------|-----------|
| ecosystem-kb | Вынести `agent theater` checklist (Часть VIII) как authored rule; зафиксировать OpenOPC = external idea-source | P1 |
| dispatcher | **Фаза 0.5:** прототип `work_item_id` correlation как read-side join поверх существующих collectors; проверить достаточность существующих ключей (trace_id/run_id) до минтинга нового | P1 |
| Maestro / spec-runner | Решить минтера `WorkCorrelation v1` по критерию «кто первым создаёт работу» (Часть IV); прототип transition-table (~5-6 статусов, universal+recovery exits) как backbone | P1 |
| arbiter | Promote `get_budget_status` + `decision_id` → `Budget v1` / `PolicyDecisionRef v1` | P1 |
| Maestro | ~~Graduate observability-contract~~ сделано (`6795b26`); добавить `evidence_ref` поверх trace_id/span_id/run_id в `contracts/observability` | P1 |
| Экосистема | Явно зафиксировать **forcing function** (рекоменд.: cross-project drill-down в dispatcher/robin) — без неё roadmap не стартует | P1 |
| steward | `Risk model` как расширение gate-check/profile; оценить gates-in-DAG (OpenOPC-скелет) | P2 |
| arbiter + steward | Разделить `Capability` / `Authority`; enforcement — role/phase allowlist | P2 |
| atp + ecosystem-kb | `LearningEvent` после stable Evidence-refs, через steward-governance (не silent-write) | P3 |

---

## Источники (проверенные файлы)

Исходные документы: `_cowork_output/{ai-dark-factory-workflow-first,current-projects-to-ai-dark-factory-objects,ai-dark-factory-contracts-critical-review,2026-07-11-openopc-borrowable-ideas}.md`.
Реестр: `COWORK_CONTEXT.md`. Код: `arbiter/README.md`, `steward/README.md`,
`steward/spec/20-design.md`, `Maestro/maestro/_vendor/obs.py`. Внешний источник (только идеи):
`OpenOPC/opc/{layer2_organization,layer3_agent,...}`.
