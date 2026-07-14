# Handoff → steward: `owner_role` semantics + gates → verification-rule mapping (REQ-013 / TASK-105)

> **Контекст (2026-07-13):** dispatcher — read-model роадмапа (DESIGN-001,
> `dispatcher/core/roadmap.py`): собирает факты и рендерит computed status, **смысл**
> governance (roadmap/gates/owner model) принадлежит **steward** — зафиксировано в
> `2026-07-11-roadmap-dashboard-dispatcher.md` и `2026-07-05-steward-ownership-and-implementation-plan.md`
> (DEC-006). TASK-105 делает dispatcher готовым **нести**, но не **оценивать**, поле `owner_role`,
> и фиксирует здесь предложение по семантике + маппингу gate → verification-rule, которое
> steward примет/уточнит как владелец модели.

## TL;DR

- dispatcher добавил **опциональный pass-through** `owner_role` на roadmap item
  (`RoadmapItemView`): значение из authored YAML попадает в `/api/roadmap` **без интерпретации**,
  status-ladder его не касается. Никакой evaluation-логики на стороне dispatcher нет и не будет —
  это анти-цель (иначе dispatcher начнёт владеть моделью, которой владеет steward).
- steward остаётся SSOT для: словаря ролей, gate-каталога, obligation-таблицы, waiver-политики.
- Ниже — что dispatcher **ожидает потреблять**, чтобы рендерить governance-колонки честно.

## 1. `owner_role` — предлагаемая семантика

- **Тип:** одна строка-роль (не список). Значение — роль из governance model / CODEOWNERS
  (`tech-lead`, `qa`, `Ops`, `spec-governance`, …), а **не** person/@handle и не project.
  `owner_project` (уже есть) отвечает на «какой репо», `owner_role` — «какая роль отвечает за
  gate/approval этого item'а».
- **Опциональность:** отсутствие поля ⇒ `null`; в solo-mode роли схлопываются в одного владельца
  (+`solo_auto_approve`), поэтому пустое значение — норма, не ошибка.
- **Где живёт:** authored roadmap YAML (`prograph-vault/authored/roadmaps/*.yaml`), на уровне item.
  dispatcher читает его тем же путём, что `owner_project`/`phase`.
- **Валидация словаря:** dispatcher **не** валидирует значение против словаря ролей — если steward
  захочет enforced-словарь, это gate-check на стороне steward/CI, не рендер-слой.
- **Отношение к статусу:** `owner_role` **никогда** не влияет на `computed_status`
  (unknown/planned/implemented/verified/blocked/drift). Это чисто атрибут ответственности.

## 2. Gates → verification-rule mapping (предложение к обсуждению)

dispatcher уже имеет закрытый набор **типизированных evidence-правил** (`_RULES` в `roadmap.py`):
`project_detected`, `file_exists`, `sqlite_has_row`, `contract_in_sync`, `work_item_chain`.
Каждое правило имеет `kind: implementation | verification`. Гейт steward'а естественно ложится
на `kind: verification`-правило: «gate пройден» ≙ «verification-evidence passed».

| steward gate (обяз-во) | dispatcher verification-rule (evidence, которую он умеет проверять) |
|---|---|
| completeness/traceability (`gate-check`) | `file_exists` на артефакт спеки / `work_item_chain` (есть цепочка задача→PR) |
| quality/acceptance (Gate 2/4, atp) | `sqlite_has_row` по acceptance-run БД / `file_exists` на отчёт |
| contract-in-sync (Gate contracts-v1) | `contract_in_sync` (уже проецируется в `drift`, REQ-010) |
| deploy (Gate 5, deployer) | `file_exists`/`sqlite_has_row` на deploy-evidence |
| approval (CODEOWNERS + CI) | **пока не покрыто** — нет типа evidence «human approval recorded» |

**Что нужно от steward, чтобы это заработало honest'но:**

1. **Стабильный gate-id + verdict-record location.** Как в WS-006 handoff'е
   (`2026-07-12-ws006-gates-maestro-handoff.md`): verdict пишется в
   `logs/<ULID>/gate_verdicts.jsonl` c `{gate_id, obligation, verdict, tier, sha, ...}`.
   Если dispatcher сможет прочитать эту запись (через `sqlite_has_row`/`file_exists` над
   стабильным путём/схемой), гейт становится машинно-проверяемым verification-rule без нового
   кода-типа. **Это предпочтительный контракт**: dispatcher вендорит пиненую копию схемы записи.
2. **evidence-ref для approval.** «Approval recorded» сейчас не выразима существующими правилами.
   Варианты: (a) approval материализуется в тот же `gate_verdicts.jsonl` как `obligation: approval`
   → покрывается пунктом 1 без нового правила; (b) отдельный тип evidence `approval_recorded` в
   dispatcher — но добавлять его будем **только** по стабильному контракту steward, не спекулятивно.
3. **Маппинг `owner_role` → gate-obligation.** dispatcher рендерит «кто отвечает» из `owner_role`,
   а «что не пройдено» — из verification-evidence. Явная связка (роль X отвечает за obligation Y)
   принадлежит governance-модели steward; dispatcher её только **отображает** рядом, не выводит.

## 3. Что dispatcher ожидает потреблять (сводка контракта)

- **Сейчас (TASK-105, сделано):** `owner_role: <string>` в authored roadmap YAML → сквозное поле в
  `/api/roadmap`, `/api/roadmap/{id}`. No-op для статуса.
- **Далее (когда steward стабилизирует):** пиненая копия схемы `gate_verdicts.jsonl` + gate-каталога,
  чтобы завести verification-rule(-ы) поверх verdict-записей. Контракт вендорится **внутрь**
  dispatcher (не ссылка наружу), version-bump при изменении — по правилу репо-границ.
- **Анти-цели dispatcher:** не валидировать словарь ролей, не вычислять tier/risk, не решать
  waiver'ы, не владеть gate-каталогом. Всё это — steward.

## Ссылки

- Реализация: `dispatcher/dispatcher/core/roadmap.py` (`RoadmapItemView.owner_role`), REQ-013/DESIGN-001.
- Роадмап-дашборд контекст: `2026-07-11-roadmap-dashboard-dispatcher.md` (§ owner_role, gates).
- Governance ownership / DEC-006: `2026-07-05-steward-ownership-and-implementation-plan.md`.
- Gates-in-DAG / verdict-record: `2026-07-12-ws006-gates-maestro-handoff.md`.
