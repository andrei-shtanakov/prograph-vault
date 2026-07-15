# Handoff → spec-runner: SpecMeta contract v2 — `owner_role` + человеческий approver (C2)

> **Контекст (2026-07-15):** steward закрыл свою часть C2 (роадмап
> `steward/NEXT-STEPS.md`): frontmatter расширен `upstream_hashes` (пиновка блоб-хешей
> upstream при аппруве downstream), на этом реализован stale-cascade check REQ-206
> (`steward/src/steward/gatecheck/checks.py::check_stale_cascade`, findings
> GC-STALE / GC-STALE-UNPINNED / GC-STALE-KEY). Осталась **spec-runner-часть** C2 —
> она у владельца формата: `tasks.md` / SpecMeta принадлежат spec-runner, steward их
> только вендорит пиненой копией (`steward/src/steward/_vendor/spec_meta.py`, DEC-003).

## Что просит steward от spec-runner

1. **Добавить в `SpecMeta` (spec-runner/src/spec_runner/spec.py) аддитивные поля:**
   - `owner_role: str = ""` — CODEOWNERS-роль(и) владельца артефакта, строка вида
     `"@role[,@role]"` (семантику ролей владеет steward; spec-runner — только носитель поля).
   - человеческий approver уже частично есть (`approved_by`/`approved_at`); требование C2 —
     зафиксировать, что `approved_by` — **git-handle человека**, проставляемый при PR-merge,
     а не agent-id (agent-id остаётся в `generated_by`). Если это уже так — просто
     задокументировать в контракте.
2. **Бампнуть `SPEC_META_CONTRACT` → 2** (сейчас в вендоренной копии steward — v1) и
   пометить изменения как backward-compatible (новые поля с дефолтами; `meta_from_dict`
   уже игнорирует неизвестные ключи, так что старые читатели не ломаются).
3. Опционально (не блокирует): узнать `upstream_hashes` как pass-through ключ —
   spec-runner может его игнорировать; интерпретация принадлежит steward (gate-check).

## Что сделает steward после этого

- Ре-вендорит `split_frontmatter`/`SpecMeta`/`meta_from_dict` байт-в-байт как contract v2
  и уберёт временный обход «читаем `owner_role` из сырого frontmatter-dict»
  (`steward/src/steward/meta.py`).

## Ссылки

- steward C2/C3: `steward/NEXT-STEPS.md` (Phase 2), `steward/spec/20-design.md`
  (frontmatter-схема REQ-002, теперь с `upstream_hashes`).
- Stale-механика: `steward/workstreams/WS-002-gate-check/spec/design.md` DESIGN-207.
- Границы владения: `2026-07-05-steward-ownership-and-implementation-plan.md`.
