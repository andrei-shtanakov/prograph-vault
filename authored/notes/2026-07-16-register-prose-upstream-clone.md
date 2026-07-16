---
title: Register prose upstream clone and Libretto lineage
type: note
status: proposed
owner: Andrei
updated: 2026-07-16
---

# Handoff: зарегистрировать `prose/` в COWORK_CONTEXT.md + зафиксировать связь libretto → prose

**Дата:** 2026-07-16
**Источник:** libretto (formerly `open-prose`), Phase 0 (spec hygiene), задача 0.8 плана
`libretto/docs/plans/2026-07-16-development-plan.md`
**Кому:** владелец workspace-реестра (COWORK_CONTEXT.md)

## Что нужно

1. **Зарегистрировать `prose/`** в COWORK_CONTEXT.md. Директория
   `all_ai_orchestrators/prose/` — git-checkout публичного репо
   `https://github.com/openprose/prose.git`, но в реестре проектов не значится
   (governance-gap, зафиксирован в
   `_cowork_output/prose-open-prose-comparison-2026-07-16.md`). Предлагаемый
   формат — отдельная секция "external upstream clones" либо строка реестра с
   пометкой external/read-only: это апстрим, мы его не редактируем.

2. **Зафиксировать миграционную связь `libretto` → `prose`** (ADR или note):
   - `openprose/prose` (создан 2026-01-03) — публичный преемник/продуктовое
     ядро OpenProse: responsibility-модель (`*.prose.md`), Reactor runtime
     (TypeScript, npm-пакеты `@openprose/reactor*`), CI/тесты.
   - `andrei-shtanakov/libretto` (создан как `open-prose` 2026-02-23;
     переименован 2026-07-16) — активный downstream / research fork:
     canonical surface `Libretto`, `.libretto`, `libretto-tools`, `libretto.*`;
     legacy `.prose` / `openprose.*` остаются readable для исторических
     artifacts. Решение и фазы: план
     `libretto/docs/plans/2026-07-16-development-plan.md`.

## Контекст

- Сравнительный анализ: `_cowork_output/prose-open-prose-comparison-2026-07-16.md`
- Анализ переносимых уроков: `_cowork_output/open-prose-lessons-from-prose-2026-07-16.md`
- Обе локальные лицензии MIT; GitHub license detection для обоих repo
  возвращает `null` (мелкий пункт — можно поправить при регистрации).
