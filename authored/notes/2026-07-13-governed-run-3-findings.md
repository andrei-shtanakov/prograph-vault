---
title: Governed run #3 — gates v1.2 подтверждены e2e; находки H-8, H-9
type: note
status: living
owner: andrei-shtanakov
updated: 2026-07-13
---

# Governed run #3 (gates v1.2 live): H-6/H-7 подтверждены, находки H-8..H-9

> **Контекст (2026-07-13):** первый прогон `maestro orchestrate` на gates v1.2
> (Maestro PR #76, `f287c8c`). Реальная задача: покрытие atp-platform в
> каноническом risk-model steward (`path_class` + `consumer_registry`), scope
> `profiles/risk-model.yaml` → policy → tier high — намеренно, чтобы блокировались
> оба edge. Итог: **полный проход до PR с двумя осмысленными аппрувами**
> (ex-ante spawn + ex-post merge-gate) — ожидание из findings-заметки прогона #1
> выполнено. Результат: steward PR #12. Verdict-trail: Maestro
> `logs/01KXD6*/gate_verdicts.jsonl` (несколько пайплайнов — прогон шёл с
> рестартами).

## Что подтвердилось (v1.2 работает)

1. **H-6 resume-in-place — главный результат.** Ex-post блок (tier high +
   честный scope_violation) → `workstream-approve` → resume: маркер
   `phase=ex_post sha=6b7c8d5` + неизменный worktree HEAD → **без DECOMPOSING,
   без регенерации, сразу ex-post → MERGING → PR → DONE за секунды**;
   `error_message` очищен ровно на DONE. В v1.1 здесь был вечный цикл
   (regen → новый sha → инвалидация approval), дожимавшийся руками.
2. **H-7 изоляция.** `spec/maestro-*` спокойно жили рядом с governance-доками
   steward в одной `spec/`; exclude-блок в `$GIT_COMMON_DIR/info/exclude` спрятал
   их от `git add -A` агента; **PR #12 содержит ровно 4 осмысленных файла, ноль
   harness-артефактов**.
3. **DESIGN-608 вживую:** мерж steward PR #11 посреди прогона сдвинул master →
   ex-ante approval корректно инвалидировался (новый sha) и потребовал повторного
   аппрува. Оба новых preflight-guard'а (`spec-runner-prefix-unsupported`,
   tracked-config) отработали на старте без ложных срабатываний.
4. **Сюжет про agency:** агент вышел за declared scope осознанно — новый
   registry-ключ (точный файл вне `contracts/`) был бы мёртвыми данными без
   расширения `_blast_of_paths`/`classify_declared` в
   `src/steward/riskclassify/classify.py`. Ex-post честно поймал scope_violation,
   оператор осознанно одобрил (диff по делу + тесты). Ровно та петля
   «agent judgement → gate → human review», ради которой всё строилось.

## Находки → handoff'ы

### H-8 (Maestro gates/workspace, P2): `spec/.maestro-*` не покрыт изоляцией
spec-runner именует task-history и spec-lock с точкой **перед** префиксом:
`spec/.{spec_prefix}task-history.log`, `spec/.{spec_prefix}spec.lock` →
`spec/.maestro-task-history.log`. Паттерны v1.2 (`spec/maestro-*`,
`spec/.executor-*`) его не ловят: файл закоммитился агентским `git add -A` в
task-ветку и поехал бы в PR (в прогоне вычищен оператором:
`git rm --cached` + operator-строка в exclude). Фикс Maestro: добавить
`spec/.maestro-*` (шире: `spec/.{SPEC_PREFIX}*`) в exclude-блок, stale-cleanup
и `_ORCHESTRATOR_MANAGED`.

### H-9 (Maestro gates, P1): approval-маркер гибнет от genuine failure между аппрувом и гейтом
Арка: ex-ante блок → approve → resume → **регенерация спеки упала честно**
(`plan --full` code 1, бюджет) → `_handle_failure` перезаписал `error_message`
сообщением об ошибке → retry дошёл до ex-ante → маркера нет, а
`_prior_block_recorded` смотрит только в verdict-store **текущего** пайплайна
(новый ULID на каждый `orchestrate`) → approval потерян, повторный блок на том
же sha. Две дыры одной природы (родня H-3): (a) single-slot `error_message`
конфликтует между маркером и failure-сообщениями — при перезаписи сохранять/
конкатенировать маркер (паттерн уже есть в v1.2 для PR-note); (b) verdict-store
lookup должен быть durable поверх рестартов (читать все `logs/*/`
gate_verdicts.jsonl или вынести approval-память в БД).

### Операционные заметки (не баги)
- `_merge_into_base` двигает **локальный** master целевого репо вперёд origin до
  человеческого мержа PR — после мержа PR #12 локальный master steward надо
  реконсилировать (`git fetch && git reset --keep origin/master` или дождаться
  совпадения историй).
- Регенерация спеки на каждый respawn (в т.ч. после kill'ов оркестратора) —
  деньги и время; вместе с H-9 это аргумент за идемпотентность/кэш spec-gen.
- `spec_gen_budget_usd: 1.0` мало для полного `plan --full` на нетривиальной
  задаче — в прогоне поднято до 3.0.

## Порядок

H-8 — мелкий, чисто Maestro (gates v1.2.1). H-9 — P1, дизайн-развилка та же,
что была у H-3 (где живёт durable approval-память) — решить до следующего
губернед-прогона с флаки-этапами. После H-9 повторный прогон не обязателен:
v1.2-петля подтверждена этим прогоном целиком.
