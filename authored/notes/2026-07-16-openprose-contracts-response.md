---
title: Ответ на оффер open-prose (receipts, IR) — мяч принят, первый потребитель atp-platform
type: note
status: accepted
owner: andrei-shtanakov
updated: 2026-07-16
---

# Ответ на оффер open-prose (receipts, IR): мяч принят, первый потребитель — atp-platform

**Дата:** 2026-07-16
**В ответ на:** `2026-07-16-openprose-contracts-offer.md`
**От кого:** владелец соседних репо (оценка со стороны proctor; на стороне
atp-platform задача в тот же день переведена в ACTIVE — см. «Статус адресатов»)

## Решение

Оффер прочитан и принят. Распределение по адресатам:

- **atp-platform — назначен первым потребителем.** Это eval-платформа
  экосистемы, у неё уже отработана ровно эта механика: вендоренные
  пинованные схемы + contract-тесты (learning-event-v1, EvidenceRef v1,
  RD-007 закрыт 2026-07-12). Receipts ложатся в существующую
  evidence-driven модель как новый evidence-source. Сам open-prose в
  Rust-гейте (задача 4.6 плана `open-prose/docs/plans/2026-07-16-development-plan.md`)
  называет atp-platform поимённо («a `receipts-verify` crate used by
  atp-platform»). Объём задачи: вендорить `contracts/{receipt.md,ir.md}`
  (+ `canonical.py`), написать reader, тесты на корпусе
  `open-prose/skills/prose/examples/runs/` и битых фикстурах
  `open-prose/tests/fixtures/`.
- **proctor — pass.** proctor не исполняет `.prose`-программы и не
  оценивает чужие прогоны; eval-контура в его roadmap нет, скоуп
  сознательно минимален (роль — dogfooding Maestro, следующая фаза —
  `mcp/`). Вендорить контракт без потребляющего кода — speculative.
  Receipt-паттерн (append-only hash-chain + fingerprints + честная
  атрибуция usage) остаётся **дизайн-референсом** для возможной будущей
  верифицируемости `episodes.db` — читать как образец, не вендорить.
- **arbiter — отложено.** «Цепочка доказательств для спорных прогонов»
  имеет смысл после того, как atp-platform построит и обкатает reader
  и появятся реальные спорные прогоны. Не стартовать с arbiter.

## Про триггер гейтов (важный нюанс)

Сама публикация оффера гейты **не** открывает: критерий и у Rust-гейта
(4.6, ревизит в конце Phase 4 open-prose), и у Phase 6 (6.1) — «именованный
потребитель *появился*», т.е. факт: вендоренный контракт + работающий
reader в репо потребителя. Причинность прямая: сначала задача в
atp-platform доводится до reader'а, потом она легитимно триггерит
пересмотр 4.6/6.1. Спешки нет — контракты append-frozen, ожидание
ничего не стоит.

## Статус адресатов (на 2026-07-16)

- **atp-platform: ACTIVE.** Задача заведена в `atp-platform/TODO.md` в тот же
  день (журнал `derived/journal/atp-platform/journal.md`, записи 11:07 и
  11:38 — утренний DEFERRED пересмотрен в ACTIVE). Условие в задаче: reader
  обязан приземлиться на существующую потребляющую поверхность ATP
  (checker `receipt_chain` и/или маппинг receipts → EvalCheck/EvidenceRef),
  иначе заявка для гейта формальная.
- **proctor: pass** (журнал `derived/journal/proctor/journal.md`, 11:13).
- **arbiter: отложено** — вторичный потребитель.

## Следующие шаги

1. atp-platform: довести задачу до reader'а на master (вендоринг + reader
   + тесты на корпусе). Ссылаться на эту заметку и на оффер.
2. К моменту ревизита 4.6 у open-prose должен существовать либо факт
   потребления (atp reader на master), либо явный отказ — тогда 4.6
   пере-подтверждает Python-only.
