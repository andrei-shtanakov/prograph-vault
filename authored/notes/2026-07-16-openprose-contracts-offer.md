# Handoff: open-prose предлагает машинные контракты (receipts, IR) как evaluation-входы

**Дата:** 2026-07-16
**Источник:** open-prose, Phase 5 (host adapters), задача 5.4 плана
`open-prose/docs/plans/2026-07-16-development-plan.md`
**Кому:** владельцы atp-platform / proctor / arbiter (на их усмотрение —
это предложение, не требование; сторона потребителя решает сама)

## Что предлагается

open-prose теперь оставляет от каждого запуска два машинно-читаемых,
keyless-верифицируемых артефакта:

1. **`receipts.jsonl`** (`openprose.receipt.v1`,
   `open-prose/contracts/receipt.md`) — append-only hash-chained журнал:
   по receipt на statement, fingerprints входов/выходов, честная
   атрибуция токенов (`usage.basis: exact|estimated|unavailable`),
   записанные discretion-решения, skip-provenance. Верификация:
   `openprose-tools verify <run-dir>` (chain consistency при доверенном
   `ledger_head`).
2. **`{program}.ir.json`** (`openprose.compile-ir.v1`,
   `open-prose/contracts/ir.md`) — content-addressed компиляционный
   артефакт: инвентарь statement'ов, таблицы агентов (хэши промптов),
   wiring сессий, диагностики. Свежесть: `openprose-tools ir-check`.

## Зачем это соседям

- **atp-platform / proctor**: receipts — готовый ground-truth для
  оценки агентных прогонов (что реально исполнилось, в каком порядке,
  над какими входами, почём) без парсинга человекочитаемых логов.
- **arbiter**: hash-chain + fingerprints дают проверяемую цепочку
  доказательств для спорных прогонов.

## Правила потребления

- Контракты **вендорятся пинованной копией** внутрь потребителя
  (workspace-правило), не референсятся по пути. Копировать:
  `open-prose/contracts/{receipt.md,ir.md}` + при желании референсную
  реализацию канонизации `open-prose/tools/src/openprose_tools/canonical.py`.
- Контракты append-frozen: поля добавляются с bump'ом `v`, никогда не
  переименовываются/переинтерпретируются; неизвестные поля игнорировать,
  неизвестные `v` — отклонять.
- Примеры для интеграционных тестов: `open-prose/skills/prose/examples/runs/`
  (4 закоммиченных прогона, включая skip-semantics resume) и
  `open-prose/tests/fixtures/{runs,ir}/` (испорченные варианты).

## Статус

Никаких обязательств со стороны open-prose не создаётся; при интересе —
завести задачу в своём репо и вендорить. Вопросы: через журнал KB или
задачу в open-prose.
