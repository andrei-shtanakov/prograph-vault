# Handoff → Maestro: guard-hooks и evidence-ref v2 для gates-in-DAG (WS-006 / RD-004)

> **Контекст (2026-07-12):** steward WS-006 «risk model + mandatory gates» — дизайн смержен
> (steward PR #5, master `04accdd`): `steward/workstreams/WS-006-risk-model/spec/design.md`.
> Это закрывает design-часть RD-004 (contracts-v1). Скелет gates-in-DAG оценён против текущего
> Maestro (DESIGN-611); оценка выявила работы **на стороне Maestro** — steward чужой код не
> правит, поэтому фиксируются handoff'ом здесь. Ничто из списка не блокирует steward M1
> (risk-classify CLI): контракт между репо — JSON-вывод классификатора (DESIGN-610), Maestro
> вендорит его схему пиненой копией, когда возьмёт работы в план.

## TL;DR

Гейт = **guard на transition-table** существующей state-machine workstream'а, не узел DAG
(второго планировщика не появляется). Maestro-side работ четыре; первые три — механика guard'ов,
четвёртая — расширение контракта evidence-ref.

## Работы

### M-1. Guard-hook на переходах + персистентный verdict-record

- Точка врезки: валидация переходов `WorkstreamStatus`
  (`maestro/models.py` — PENDING → DECOMPOSING → READY → RUNNING → MERGING → PR_CREATED → DONE);
  preflight уже fail-fast, guard встраивается тем же паттерном.
- Каждая оценка guard'а пишет запись в `logs/<ULID>/gate_verdicts.jsonl`:
  `{gate_id, obligation, verdict, tier, phase, sha, risk_model_version, ts, waiver_ref?, note?}`.
- Семантика fail-closed: для mandatory-гейта отсутствие verdict'а или `error` = fail —
  на любом tier'е (таблица verdict × obligation в DESIGN-606).
- Tier Maestro **не вычисляет** — консюмит JSON `steward risk-classify` (одна точка истины);
  скелет поля `gates:` в `project.yaml` — DESIGN-611. Схема самого `project.yaml` — собственность
  Maestro, поле добавляет он.

### M-2. Канал аннотаций advisory-fail в run-metadata

- Advisory-гейт с verdict `fail`/`error` не режет граф, но обязан оставить аннотацию в
  run-metadata (+ verdict-record из M-1) — иначе advisory-гейты декоративны и неаудируемы.

### M-3. SHA-инвалидация verdict'ов

- Verdict валиден только для head SHA, для которого вычислен; verdict-store ключуется
  `(gate_id, sha)`. Новый коммит в ветке workstream'а ⇒ все verdict'ы (и waiver'ы)
  инвалидированы, ex-post tier пересчитывается. Закрывает TOCTOU между READY→RUNNING и
  RUNNING→MERGING.

### M-4. evidence-ref v2: предложение `kind: gate-verdict` (OQ-1)

- v1 обходится существующими kind'ами (`log` по `pipeline_id` — грубо, до всего run-каталога;
  `artifact` — для CI-вердиктов steward), контракт не трогается.
- Предложение v2 в `Maestro/contracts/observability/`: kind `gate-verdict`,
  required keys `gate_id` + `sha` — адресация конкретной записи, а не каталога.
  Решение за Maestro как владельцем контракта; по правилам самого контракта новый kind
  post-adoption = version bump.

## Напоминание (не новая работа)

`maestro validate --no-fs` не ловит висячий `depends_on` (`steward/emitter-contract-check.md`) —
целостность dep-link остаётся обязанностью `gate_check` выше по потоку; гейты `tests`/`validate`
её не заменяют.

## Ссылки

- Дизайн: `steward/workstreams/WS-006-risk-model/spec/design.md` (DESIGN-606..612)
- Роадмап: `authored/roadmaps/contracts-v1.yaml` → RD-004
- Консолидированный роадмап: `2026-07-11-ai-dark-factory-consolidated-roadmap.md`
