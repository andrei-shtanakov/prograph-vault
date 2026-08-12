# impresario: product-governance реализация в экосистеме

**Дата:** 2026-08-12
**Статус:** решение принято, репо создан

## Решение о границе

- **Методология** product-governance (спеки стадий 4–5, идеи, планы) живёт
  и развивается в `vkgeorgia/airun` — приватном репо EPAM-контекста
  (соревнование команд по AI-инструментам разработки; инструменты могут
  быть открытыми, приватными или клиентскими).
- **Реализация** живёт в нашей публичной экосистеме:
  `github.com/andrei-shtanakov/impresario` (подпроект
  `all_ai_orchestrators/impresario/`). Имя — из музыкальной линии
  (maestro/kapelle/libretto): импресарио решает, какие постановки ставить
  и финансировать.
- Класть код в airun было бы стратегической ошибкой: приватный репо,
  чужой владелец, EPAM-связанное имя.

## Что в impresario (bootstrap, M0 закрыт)

- `contracts/` — 8 схем v1 (`urn:impresario:contract:<name>:v1`):
  idea, axis-assessment, ranked-backlog, research-pack, concept-draft,
  exchange-log, product-proposal, gate-decision + fixtures + канонический
  bundle `examples/pp-001`.
- `docs/semantics.md` — **самодостаточный SSOT семантики** (FSM
  ProductProposal, GateDecision c append-only supersession, скоринг
  score-vs-blocker, цикл researcher↔creator): ссылки на приватные спеки
  публично не разрешаются, поэтому семантика описана на месте.
- Валидатор `impresario validate`: schema + 14 кросс-проверок,
  JSON-отчёт, exit 0/1/2; 51 тест.

## История

Код прошёл два бот-ревью-раунда как `vkgeorgia/airun` PR #22 (10 замечаний
Codex/Copilot, все отработаны), затем перенесён и переименован
(`airun` → `impresario`); PR #22 закрыт с пояснением. PR #21 (rulings в
спеки методологии: SSOT FSM, GateDecision outcomes, readiness как
вычисляемое предусловие, enforcement-классы) остаётся в airun.

## Потребители (по мере M2–M4)

kapelle (execution backend цикла), steward/discovery (входной контракт
approved ProductProposal), dispatcher/Robin (read-only gate_waiting) —
все получают **пинованные копии** контрактов вендорингом.

## Follow-ups

- Зарегистрировать impresario в списке зеркал Robin (список молча слеп к
  новым репо — прецедент maestro/libretto 2026-07).
- M1 Stage 4 pilot: нужны артефакты стратегии/стандартов и 5–10 реальных
  Idea (см. `impresario/TODO.md`).
