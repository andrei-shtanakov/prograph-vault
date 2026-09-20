---
title: План развития пайплайна «интервью → реализация» (ревизия 4, принят)
type: note
status: accepted
owner: andrei-shtanakov
updated: 2026-09-20
---

# Пайплайн «интервью → реализация»: состояние и план развития

**Дата:** 2026-09-13 (ревизия 2 — по ревью владельца: разведены две
нумерации, усилена модель runtime-state, снапшот PP, матрица артефактов;
ревизия 3 — два маршрута прогона, транскрипт согласован с инвариантом,
E0.6 сужен до governance-state, терминальный механизм S8, путь снапшота PP;
ревизия 4 — **принят владельцем**: шесть решений §4 внесены (prograph-vault#127),
факт S8 и три человеческие границы R3 исправлены)
**Статус:** accepted — принят владельцем 2026-09-13 (prograph-vault#127). Пункты с
владельцем изменений devtools заведены (devtools#210); инвентаризация state
spec-runner — inbox spec-runner#478.

Порядок и границы наследуют решение владельца 2026-08-31 (спека
behaviour-конвейера devtools, §1): пайплайнов **два** — внутренний (развитие
экосистемы) и внешний (сторонний продукт); внутренний делается первым,
внешний переиспользует его как участок, добавляя сверху impresario и
discovery-интервью в customer-фрейме. Развилок под внешний вариант во
внутреннем не закладывать.

## 0. Две нумерации

В документе две независимые последовательности; они не смешиваются.

- **Runtime-компоненты R1–R5** — компоненты, через которые проходит *один
  продуктовый прогон*: R1 интервью, R2 продуктовый контур, R3
  governance-конвейер, R4 исполнение, R5 обратная связь. Номера — имена, не
  порядок: маршрут зависит от варианта пайплайна.
  - **Внутренний вариант:** R1 (engineer-фрейм, бриф) → R3 → R4 → R5.
  - **Внешний вариант:** R2 (Idea → PP → QG-5) → bootstrap репо продукта →
    R1 (customer-фрейм) → R3 → R4 → R5.
- **Roadmap-этапы E0–E4** — последовательность *разработки самого
  пайплайна*: E0 стабилизация → E1 вход из брифа → E2 вызываемость Need →
  E3 внешний контур → E4 замыкание петли. Здесь номера — порядок.

## 1. Состояние runtime-компонентов на 2026-09-13

> Снимок дня принятия; что изменилось с тех пор — §7. Живая плоскость
> исполнения, а не этот снимок, — `devtools/TODO.md`, раздел «План развития
> пайплайна «интервью → реализация»».


| Компонент | Владелец | Состояние |
|---|---|---|
| R1. Интервью → discovery-brief | discovery-toolkit (методика), discovery (runtime) | Готова как автономная стадия: живая приёмка 2026-08-19, бриф доставлен PR-ом dispatcher#162. **Конвейером не вызывается.** |
| R2. Idea → RankedBacklog → QG-4/QG-5 → approved ProductProposal | impresario | M0–M4 закрыты, PP-101 и PP-103 прошли полный круг ([[2026-08-12-impresario-bootstrap]]). Intake-контракт вендорен в steward (`proposal-intake`). **К конвейеру не подключена** (осознанно). |
| R3. Governance-конвейер | devtools (`make spec-loop`) | 6 узлов charter → requirements → behaviour-spec → design → acceptance → decomposition → tasks. Три человеческие границы (после §I12): мерж бандл-PR, одобрение DAG-узлов (`--approve-node`), approve tasks-спеки. Два полных цикла кнопки (kapelle, spec-runner). Авторинг behaviour-узла переведён на document-пайплайн disputatio (devtools#203). |
| R4. Исполнение | spec-runner `run --strict` + devtools `accept-pr` + `merge-pr.sh` ([[2026-08-30-adr-eco-011-darkfactory-default-agent-merge]]) | Прожита целиком несколько раз (kapelle 10/10, WS-367 15/15, WS-341 18/18, supersede-воркстрим 15/15). Раннер работает с dev-версии master: релиза ≥2.36 с verify_first нет. |
| R5. Обратная связь | S8 verify, переиздание tasks (§I12), dispatcher observation | §I12 доставлен и прожит 2026-09-11. |

Разрывы: стык R1 → R3 ручной (бриф переносится как текст `SUBJECT`);
R2 → R3 не имеет кода; у R3 открыт governance-долг (триаж devtools
2026-09-13, шесть workstream-пунктов); часть runtime-state существует только
на машине оператора (§2.2).

## 2. Модель размещения артефактов

### 2.1. Правило

1. **Продуктовая истина** — в репо продукта (репо-цель конвейера).
2. **Портфельная истина** — в impresario (идеи, бэклог, оценки, решения
   QG-4/QG-5, оригиналы PP).
3. **Код инструментов** — в репозиториях инструментов (devtools,
   spec-runner, steward, discovery, disputatio).
4. **Продуктовая конфигурация инструментов и пины** — в репо продукта
   (`profiles/`, review-context, `spec-runner.config.yaml`, пины контрактов).
5. **Операционное состояние** — во внешнем durable storage.
6. **Локально** — только восстанавливаемое или временное состояние.

Правило репо-границ: [[repo-boundaries]]. Следствие: **репо продукта
рождается на границе QG-5**; до approve продукт живёт только в impresario.

### 2.2. Инвариант runtime-state

> Любой результат, необходимый для продолжения, проверки или
> воспроизведения продуктового прогона, не должен существовать только на
> машине оператора.

Durable storage сегодня — два места, и оба уже используются: **факты
GitHub** (PR review как вердикт ревью, подпись одобрения узла из
`mergedBy`/`mergedAt` candidate-PR, доставка tasks по имени ветки — durable
reconciliation в `task_bridge`) и **репо продукта** (бандл, tasks-спека,
waivers, замеры, evidence-документы). Отдельное хранилище не вводится, пока
эти два не исчерпаны.

Классификация локального состояния на 2026-09-13:

| Локальный объект | Класс | Восстановимо без машины? | Действие |
|---|---|---|---|
| `devtools/out/governance-runs/<run-id>/run.json` | нужен для продолжения | частично: tasks-PR находится по ветке, бандл-PR — по ветке `spec/<ws-id>-behaviour`; статусы узлов — в frontmatter бандла | E0.6: повтор `spec-loop` восстанавливает леджер из фактов GitHub; проверка — удалить `out/` и продолжить прогон |
| `~/.discovery/sessions/<id>/journal.jsonl` | нужен для продолжения **до выпуска брифа**; после публикации проверенного брифа — необязателен | нет | политика §2.4: проверенный бриф — единственный durable-результат R1; окно интервью — принятое ограниченное исключение из инварианта |
| `devtools/out/governance-runs/<run-id>/s8-gate-verdicts.jsonl` (S8; `.steward/gate_verdicts.jsonl` в корне репо-цели — транзиентный источник steward, прибирается после переноса) | доказательство прохождения гейта | да, детерминированный перезапуск гейта на default branch | E0.6: вердикт S8 едет **внутри tasks-PR** того же цикла (`workstreams/<ws-id>/evidence/`), отдельный evidence-PR не создаётся |
| `spec/.executor-*state.db`, `spec/.executor-*logs/`, claims | нужен для продолжения | статусы задач — в tasks-спеке (tracked), `reset` безопасен; логи и claims — нет | вне E0.6: inbox-issue владельцу spec-runner на инвентаризацию; логи неудачных попыток — кандидат в evidence |
| кеши, locks, `.pyc`, worktrees | временное | не требуется | без изменений |

### 2.3. Снапшот ProductProposal в репо продукта

- Оригинал PP остаётся **каноническим в impresario** (`pilot/forconcept/pp-NNN/`).
- В репо продукта попадает **неизменяемый снапшот** по content-addressed
  пути `workstreams/<ws-id>/spec/pp-<id>-v<N>-<hash>.yaml`: `pp_id`, версия
  и CAS impresario, hash содержимого, ссылка на источник (репо + путь +
  коммит). Новая версия — новый файл, старый не перезаписывается.
- charter трассируется **на снапшот**, не на живой PP.
- Изменение PP после approve = новая версия в impresario и новый снапшот
  PR-ом; редактируемых версий одного утверждения две не бывает.

### 2.4. Транскрипт интервью

- Durable-результат R1 — **только проверенный бриф** (gate pass), он
  публикуется в репо продукта. Транскрипт после этого **необязателен**: он
  не нужен ни для продолжения, ни для проверки, ни для воспроизведения
  прогона, поэтому инвариант §2.2 на него не распространяется. Основание:
  бриф всегда выводится из журнала заново и проверяется гейтом как
  самостоятельный документ; дальше прогон читает бриф, а не журнал.
- **Окно до брифа — принятое ограниченное исключение.** Пока интервью не
  выпустило бриф, журнал нужен для продолжения и существует только в
  `$DISCOVERY_HOME`. Потеря машины в этом окне = перезапуск интервью.
  Смягчение: ответы приходят файлами (`answer --file`) и остаются у
  отвечающего. Переносимое хранилище журнала сейчас не вводится (решение §4).
- Хранение транскрипта после брифа — вопрос приватности, не durability:
  **90 дней после закрытия workstream'а** (решение §4), затем удаление
  явной командой с записью в журнал; доступ — оператор интервью. Транскрипт
  содержит персональные данные и случайные обещания.
- В репо продукта транскрипт попадает **только по явному основанию** (решение
  владельца, зафиксированное в charter).

### 2.5. Дефолт по количеству репо

> Внешний продукт считается **однорепозиторным**. Появление второго
> репозитория **блокирует decomposition** и инициирует отдельное owner
> decision (Mode-2 или нарезка на воркстримы по репо через inbox-issues,
> [[2026-07-28-adr-eco-006-cross-repo-issue-inbox]]).

«Отложили Mode-2» означает этот дефолт, а не неопределённое поведение.
Решение владельца (§4): Mode-2 откладывается до первого фактического случая
второго репо у одного продукта.

## 3. Roadmap-этапы

Этапы последовательны по зависимостям: E0 → E1 → E2 → E3 → E4. Единица
планирования — workstream через тот же конвейер; даты не ставятся.

### E0. Стабилизация внутреннего участка

Пункты 1–5 назначены триажем devtools 2026-09-13 (`devtools/TODO.md`,
«Триаж открытого governance-долга»); пункт 6 добавлен этим планом.

1. Fidelity ревью (devtools#136, #166).
2. Fail-honest supersede (devtools#177, #168, #181, #175) — **закрыт**
   devtools#209 (2026-09-13).
3. Контракт файловой цели verify-first (devtools#201, inbox из spec-runner),
   следом остаточный долг task_bridge (#123, #162, #198, #200).
4. Остатки document-runner (devtools#204) до следующего behaviour-авторинга.
5. spec-runner: релиз ≥2.36 с verify_first; закрытие spec-runner#429 →
   переписанный #427.
6. **Durable governance-state** (§2.2) — объём ограничен состоянием R3:
   восстановление леджера `spec-loop` из фактов GitHub и доставка
   S8-вердиктов. **Терминальный механизм S8:** S8 выполняется после мержа
   бандла и до доставки tasks-PR (`resume` → `completed` → `deliver`),
   поэтому вердикт едет внутри tasks-PR того же цикла в
   `workstreams/<ws-id>/evidence/`; у tasks-PR собственного S8 нет, второй
   вердикт не порождается. Альтернатива без записи в репо — check run на
   sha мержа бандла. Состояние R1 (§2.4) и R4 (inbox-issue владельцу
   spec-runner) в объём не входят. Приёмка: прогон R3 продолжен после
   удаления `out/` и `.steward/`.

**Выход:** один workstream проходит `spec-loop` → approve → `run --strict`
→ accept-pr → merge без ручных исключений и без новых issues класса
«обвязка», и R3 продолжается после потери локального governance-state.

### E1. Вход конвейера из discovery-brief (engineer-фрейм)

Первый непройденный участок R1 → R3; одновременно триггер, ради которого
discovery получил runtime («вызываемость стадии прогоном»).

- **Контракт входа.** `spec-loop --brief <path>`: бриф обязан пройти
  вендоренный gate_check со статусом pass, иначе fail-closed. Хэш брифа
  входит в frontmatter charter как upstream — §I2-сверка анкера видит бриф
  как остальные узлы.
- **Авторинг S2 из брифа.** Промпты charter/requirements (`governance/ops.py`)
  получают бриф как источник: G-NN и FR-NN переносятся с трассировкой, не
  пересочиняются. Гвард: каждый Must-FR брифа встречается в requirements.
- **Провенанс.** Бриф лежит в бандле как нулевой узел
  (`workstreams/<ws-id>/spec/`), доставляется тем же PR, что и charter.
  Граница author ≠ execute discovery сохраняется: PR открывает конвейер.
- **Приёмка.** Живой прогон: интервью engineer-фрейма → бриф → spec-loop →
  approved tasks-спека → исполнение spec-runner; evidence в журнале.

Зависимость (решение §4): E1 стартует после fidelity (E0.1) и file-target
(E0.3) пунктов и параллельно с ними не идёт — та же поверхность
task_bridge/S2. Fail-honest supersede (E0.2) уже закрыт devtools#209.
Владелец изменений: devtools.

### E2. Вызываемость стадии Need из прогона

- **Шаг S-need** перед S2: `discovery start --frame engineer --target <repo>`
  → цикл `status` → пауза `awaiting_input` → `answer` от человека →
  `brief --out`. Пауза — тот же паттерн, что `waiting_human_merge`: повтор
  одной команды продолжает прогон.
- **Транскрипт** — по политике §2.4.
- **Режим Need запускается только при наличии реального стейкхолдера**
  (решение §4); иначе используется вход из готового брифа (`--brief`, E1).
  Мини-форма фрейма для одного человека не вводится: без реальных
  стейкхолдеров интервью вырождается в самоопрос (открытый вопрос
  `discovery/TODO.md`).
- Фаза 3 grounding discovery имеет собственный триггер и сюда не входит.
- **Приёмка.** Прогон, где ни один артефакт не создан руками: от
  `spec-loop --need` до integration-PR.

### E3. Внешний контур: impresario сверху конвейера

- **Шаг 0 — bootstrap репо продукта** на границе QG-5: `repos.sh bootstrap`,
  регистрация в `workspace-manifest.toml`, governance-gate caller, волна
  `profiles/` и review-context, снапшот PP (§2.3). Сегодня делается руками.
- **Вход.** `spec-loop --proposal <PP-id>`: subject и ws-id выводятся из
  снапшота PP, `pp_id` входит в frontmatter charter, интервью идёт в
  customer-фрейме, evidence QG-4/QG-5 ссылается из charter.
- **Дефолт** — однорепозиторный продукт (§2.5).
- **Репо продукта** (решение §4): первый внешний продукт получает **новый
  выделенный репо только после QG-5 принятого PP**; пустой репо заранее не
  создаётся, имя выводится при bootstrap из принятого продукта.
- **Приёмка.** Одна идея из pilot-бэклога доведена до влитого
  integration-PR с непрерывной цепочкой evidence: Idea → PP → снапшот → бриф
  → бандл → tasks → PR.

### E4. Замыкание петли

- S8-вердикты и merged-факты integration-PR проецируются в статус PP
  (impresario) и в наблюдение dispatcher.
- Ритм по [[2026-08-27-adr-eco-009-ecosystem-cadence]]: fleet-check
  показывает workstream'ы на человеческой границе с `waiting_since`.
- Эксперимент libretto для ритуала ревью-стопа — опциональный пункт с
  числовым критерием, вне критического пути.

## 4. Развилки и решения владельца

Решения приняты владельцем 2026-09-13 (prograph-vault#127) и внесены в основной текст.

| Решение | Нужно к | Решение владельца (2026-09-13) |
|---|---|---|
| E1 параллельно E0 или после | старт E1 | E1 стартует после fidelity и file-target пунктов E0; параллельно с ними не идёт |
| Срок хранения транскрипта после закрытия workstream'а (приватность, §2.4) | E1 | 90 дней после закрытия workstream, затем удаление с записью в журнал |
| Окно интервью до брифа — локальное исключение из инварианта или переносимое хранилище журнала | E2 | Принимается как ограниченное локальное исключение; переносимое хранилище сейчас не вводится |
| Соло-режим интервью | старт E2 | Режим Need запускается только при наличии реального стейкхолдера; иначе вход из готового брифа |
| Целевой репо первого внешнего продукта | шаг 0 E3 | Новый выделенный репо после QG-5 принятого PP; пустой репо заранее не создаётся, имя выводится при bootstrap из принятого продукта |
| Mode-2 для кросс-репного продукта | только при втором репо у продукта (§2.5) | Откладывается до первого фактического случая второго репо у одного продукта |

## 5. Матрица артефактов

Один объект — одна строка. «Доставка» — как объект попадает к владельцу.

| Объект | Canonical owner | Путь | Формат | Producer | Consumer | Доставка | Версия / hash | Retention | Gate |
|---|---|---|---|---|---|---|---|---|---|
| Методика и банк вопросов | discovery-toolkit | `frames/*.md`, `DISCOVERY-BRIEF-CONTRACT.md` | md | человек | discovery (пин) | вендоринг пиненой копии | коммит пина, copy-integrity | бессрочно | drift-check |
| Журнал интервью | discovery (runtime) | `$DISCOVERY_HOME/sessions/<id>/journal.jsonl` | jsonl, append-only | discovery | discovery (`brief`) | не доставляется; необязателен после брифа | event-id | §2.4: 90 дней после закрытия workstream | — |
| discovery-brief | репо продукта | `workstreams/<ws-id>/spec/` (E1); сейчас `spec/discovery-brief-*.md` | md + frontmatter | discovery | конвейер S2 | PR тем, кто ведёт прогон | `git hash-object` → upstream charter | бессрочно | gate_check pass |
| Idea, оценки, бэклог, решения QG | impresario | `pilot/{ideas,assessments,briefs,runs,decisions}/`, `backlog.yaml` | yaml | impresario CLI + человек | rank engine, QG | PR | CAS: input_hash + version | бессрочно | валидатор impresario |
| ProductProposal (оригинал) | impresario | `pilot/forconcept/pp-NNN/` | yaml | цикл researcher/creator | steward intake, снапшот | PR | version + hash | бессрочно | QG-5 |
| Снапшот PP | репо продукта | `workstreams/<ws-id>/spec/pp-<id>-v<N>-<hash>.yaml` (E3) | yaml, immutable | bootstrap E3 | charter | PR | pp_id + version + hash + источник; новая версия — новый файл | бессрочно | §I2-анкер |
| Профили конвейера, review-context | репо продукта | `profiles/*.yaml`, `.github/codex/review-context.txt` | yaml, txt | волна devtools + человек | spec-loop, review-pr | PR, authority-root | коммит | бессрочно | мерж человеком |
| Бандл (charter … decomposition) | репо продукта | `workstreams/<ws-id>/spec/NN-*.md` | md + frontmatter | spec-loop S2–S3 | гейты S4/S8, task_bridge | бандл-PR; узлы — `--approve-node` | `upstream_hashes`, content_anchor | бессрочно | steward gate-check, DAG-одобрение |
| Леджер прогона | devtools (оператор) | `devtools/out/governance-runs/<run-id>/run.json` | json, write-ahead | spec-loop/runner | spec-loop resume | не доставляется; E0.6 — восстановление из GitHub | run-id | до закрытия workstream | — |
| Вердикт ревью | GitHub (PR review от ai-prosto) | PR review; локально `--write-verdict <file>` | verdict/v1 json | review-pr.sh | merge_gate, accept-pr | публикация PR review | head sha + fp | бессрочно | approve/request-changes |
| S8-вердикты гейта | репо продукта (E0.6); сейчас локально | `devtools/out/governance-runs/<run-id>/s8-gate-verdicts.jsonl` (транзиентный источник — `.steward/gate_verdicts.jsonl` в репо-цели); E0.6 — `workstreams/<ws-id>/evidence/` | jsonl | steward `--emit-verdicts` | runner S8, dispatcher | E0.6 — внутри tasks-PR того же цикла, без отдельного evidence-PR | sha default branch | бессрочно | fail-closed без файла |
| Tasks-спека | репо продукта | `spec/<ws-id>-tasks.md` | md, spec-runner грамматика | task_bridge | spec-runner | tasks-PR + conform-PR | approve-штамп, §I12 | бессрочно | spec approve (человек) |
| State-DB, логи, claims spec-runner | spec-runner (оператор) | `spec/.executor-*state.db`, `spec/.executor-*logs/`, `.*task-history.log` | sqlite, jsonl | spec-runner | spec-runner resume | не доставляется; статусы — в спеке | ULID попытки | E0.6 инвентаризация | sync-гард |
| Waivers и замеры | репо продукта | `spec/.tdd-evidence/{waivers,measurements}/` | json | человек + исполнитель | гейты spec-runner, ревью | PR | baseline_sha | бессрочно | approved_by: human |
| Код и тесты | репо продукта | дерево репо | по стеку | spec-runner | CI, ревью | integration-PR → accept-pr → merge-pr | sha мержа, merged_by | бессрочно | CI + ревью + DarkFactory |
| Evidence живых прогонов | репо продукта | `docs/evidence/<дата>-*.md` | md | оператор | ревью, аудит | PR | ссылки на sha | бессрочно | — |
| Журнал экосистемы, отчёты флота | prograph-vault | `derived/journal/<repo>/journal.md`, `derived/fleet/` | md | kb-save, fleet_report | Robin, люди | PR (`journal/pending`) | дата записи | бессрочно | — |
| Учётки и харнесс оператора | машина оператора | `~/.config/review/`, `~/.config/ai-prosto/harness.env` | yaml, env | человек | review-pr, merge-pr | не доставляется | — | свойство машины | сверка логина ai-prosto |

## 7. Прогресс на 2026-09-20 (указатели, не второй источник)

Сверено по коду и TODO владельцев; чекбоксы живут в `devtools/TODO.md`.

| Этап | Состояние | Чем доказано |
|---|---|---|
| E0.1–E0.5 | закрыты | слаги в `devtools/TODO.md`: `review-evidence-fidelity-wave` (PR #206), `tasks-supersede-fail-honest-wave` (#209), `accept-file-target-contract` + `task-bridge-residual-debt-wave` (#214), `behaviour-document-runner-residuals` (#242/#243); релиз spec-runner **v2.36.0** (15.09) |
| E0.6a леджер | закрыт | devtools#211; живая приёмка 13.09 — R3 восстановлен из фактов GitHub в изолированном клоне с пустым `RUNS_ROOT` |
| E0.6b S8-вердикт | закрыт | вердикт едет внутри tasks-PR того же цикла |
| **E1 вход из брифа** | **закрыт, живая приёмка 14.09** | devtools#219; `docs/evidence/2026-09-14-discovery-brief-spec-loop-run.md`: интервью (customer → engineer) → бриф → бандл spec-runner#490 → §I12 → tasks #505 → approve #506 → `run --all --strict` 4/4, четыре integration-PR влиты |
| E2 customer-маршрут | код влит (#246), **приёмка не завершена** | `docs/evidence/2026-09-15-need-stage-live-run.md`: стадия Need отработала без ручных вмешательств, run доведён до `completed`; по букве §9 не пройдено — `waiting_human_merge` раннером не пройден (PR смержен человеком в обход S7), tasks-/approval-PR не заведены |
| E2 engineer-маршрут | **разблокирован 18.09**, не реализован | discovery#50 (`49dbc2a`) — `start --upstream` и caller-assigned `--session-id` |
| E3 внешний контур | не начат | пунктов нет ни у devtools, ни у impresario |
| E4 замыкание петли | не начат | — |

Что план не предусмотрел и что вскрылось исполнением:

- **Акт approval брифа не существует как механизм.** `--need` выпускает бриф
  со `status: draft`, а `start --upstream` соседа принимает только
  `approved` — на живой приёмке E1 подпись `approved_by` дописал агент.
  Контур заведён 2026-09-20: `devtools/TODO.md`
  `@id:discovery-brief-approval-act`; чей это акт и откуда подпись —
  решение владельца.
- **Размер бандла вышел за пределы, которые подтверждает ревью.** Behaviour-узел
  в 6.3k строк за один проход: восемь кругов терминального ревью, потолки кита
  поднимались трижды (400k → 800k), доработка остатков стоила ещё 14 платных
  кругов. Предложенный порог (warning 250 KiB / stop 350 KiB перед платным S6)
  решения владельца пока не получил.
- **Стоимость ревью стала ограничением планирования**, а не фоном: правка
  нормативного текста стоит кругов пропорционально числу мест, где норма
  пересказана (requirements ↔ design ↔ behaviour ↔ acceptance ↔ decomposition).
- **Арка не размечена на оси эпиков.** Пункты плана в `devtools/TODO.md` идут
  без `@epic`; в `ai-orchestrators-workspace/epics.toml` эпика под пайплайн
  нет, ближайшие по смыслу — `eco.dark-factory` и `eco.governance-plane`.
  После `missing_error_after = 2026-11-01` это станет ошибкой сенсора.

## 6. После принятия

- Пункты E1 и E0.6 заведены в `devtools/TODO.md` (devtools#210);
  инвентаризация state spec-runner — inbox spec-runner#478.
- Bootstrap репо продукта (шаг 0 E3) → кандидат в скрипт devtools после
  первого ручного прохода.
- Решения §4 зафиксированы, статус `accepted` (prograph-vault#127, ревизия 4).
