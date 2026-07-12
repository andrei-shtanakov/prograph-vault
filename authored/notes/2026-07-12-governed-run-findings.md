# Первый governed-прогон (gates live в orchestrate): находки и handoff'ы

> **Контекст (2026-07-12, вечер):** первый `maestro orchestrate` с активными gates
> (WS-006/RD-004) на реальной задаче (steward risk-model docs-rule, scope
> `profiles/**` → tier high). Итог: **гейты отработали end-to-end и поймали пустую
> имплементацию** — задача ушла обычным PR (steward #10), а прогон принёс четыре
> находки. Verdict-トrail: Maestro `logs/01KXBGM26QYQX66WC1XM0ZZFQR/gate_verdicts.jsonl`
> (11 записей: ex-ante block → operator approval → ex-post scope_violation block).

## Что сработало как задумано

1. Ex-ante: tier high → блок до спавна, `human.owner_approval missing`, маркер в
   `error_message`. Операторский re-queue (UPDATE status) засчитан как approval для
   того же SHA — спавн пошёл.
2. Ex-post: дифф содержал ТОЛЬКО служебные spec-файлы (имплементации ноль) и вышел
   за declared scope → `scope_violation` → блок. **Без гейта Maestro смёржил бы
   пустой PR** (spec-runner вернул rc=0).

## Находки → handoff'ы

### H-1 (spec-runner, P1 — bug): validation failure → exit 0
`spec-runner run --all` (v2.9.0) при «Validation failed before execution / No tasks
found in spec/tasks.md» завершается **кодом 0**. Maestro интерпретирует rc=0 как
успех воркстрима. Ожидание: невалидная спека = ненулевой exit (Maestro тогда честно
уводит в FAILED/NEEDS_REVIEW со своей стороны).

### H-2 (spec-runner, P1 — контракт формата): plan ↔ run дрейф
`plan --full` сгенерировал задачи как `## TASK-001 — Title`, а парсер `run`
требует `^### (TASK-\d+): ` (`src/spec_runner/task.py:16`). Генерация обязана
валидировать собственный вывод против парсера (или шаблон должен жёстко
диктоваться, не полагаясь на LLM-дисциплину).

### H-3 (Maestro gates, P1 — дизайн approval-памяти): маркеры перезатираются
Approval-маркер живёт в одном `workstream.error_message`: ex-post блок затёр
ex-ante approval → повторный спавн снова блокируется ex-ante, и фазы вечно
вымывают друг друга. Нужна аккумуляция per (phase, sha) — например, verdict-store
lookup (gate_verdicts.jsonl уже содержит всё нужное) вместо/в дополнение к маркеру.

### H-4 (Maestro gates, P2): spec-коммиты оркестратора триггерят scope_violation
`_commit_spec_in_workspace` кладёт `spec/**` + `spec-runner.config.yaml` в ветку —
эти пути не в declared scope воркстрима → ex-post всегда scope_violation, даже у
честной имплементации. Варианты: исключать orchestrator-managed пути из ex-post
path-set, либо автоматически расширять declared scope этими путями.

### H-5 (Maestro UX, P3): нет CLI для re-queue воркстрима
Операторский approval сегодня = ручной `sqlite3 UPDATE workstreams SET
status='ready'`. Нужен `maestro workstream approve|requeue <id>` (по аналогии с
`maestro approve` для задач) — заодно место, где корректно сохранять/переносить
approval-маркеры (H-3).

## Порядок

H-1+H-2 — spec-runner (владелец формата и exit-контракта); H-3..H-5 — Maestro
(gates v1.1). После H-3/H-4 повторить governed-прогон — ожидаемо полный проход до
PR с двумя осмысленными аппрувами (spawn + merge).
