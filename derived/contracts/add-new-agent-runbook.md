---
title: Add-new-agent runbook
type: contract-snapshot
status: living
source: _cowork_output/contracts/add-new-agent-runbook.md
sha256: 9a1b43bbba63800d56491d1aa89bd4ba62b532f32b8f328da74ce9fa080fa8e8
updated: 2026-07-06
---

# Runbook: добавление нового агента / CLI-инструмента в петлю ATP → arbiter → Maestro

> Живой документ (не статус-снапшот). Привязка к коду на 2026-07-01.
> Режим проекта: read-only по репозиториям; правки делает человек в своих репах.
> **Обновлено под ADR-ECO-003:** ростер агентов ведётся из SSOT-каталога
> `contracts/agents-catalog.toml`. Обе последовательности **начинаются с правки
> каталога**; случай A теперь = одна правка каталога (+ пере-вендор + sweep).

## TL;DR

1. **Сначала определись с типом:** новая **модель на существующем harness** (дёшево) vs новый **harness/CLI-инструмент** (нужен код в ATP и Maestro). Это разные последовательности. **Обе стартуют с правки SSOT-каталога** `agents-catalog.toml` (ADR-ECO-003); случай B дополнительно требует код (шим в ATP + спаунер в Maestro).
2. **`agent_id = "<harness>@<model>"` — единый join-ключ.** Он связывает все три репа; везде должен совпадать байт-в-байт.
3. **Порядок диктуется зависимостями:** Maestro должен **уметь спаунить** агента до того, как arbiter начнёт на него роутить (иначе `unknown_agent` → HOLD). ATP-данные нужны для seed cost/score и re-rank, но не для базовой роутируемости.
4. **⚠ Ограничение для «новой модели»:** Maestro выбирает спаунер по harness и **не пробрасывает модель** (`spawners/base.py:57`, `claude_code.py` — нет `model`-параметра). Две модели одного harness как отдельные routable-агенты **не исполнимы раздельно** без доработки спаунера.
5. **Включение re-rank — поэтапное:** `ARBITER_BENCH_WEIGHT=0` (проверка) → A/B `0.15`.

---

## Где какой факт живёт (карта)

| Реп | Файл | Что добавляется | Тип факта |
|---|---|---|---|
| **SSOT** | `_cowork_output/contracts/agents-catalog.toml` | `[[agents]]` пара (+ `[harnesses.X]` и `[models."..."]` для нового harness/модели) | **единый источник ростера** |
| ATP | `method/agents-catalog.toml` (вендоренная копия) | пере-вендорить из SSOT; `run_pipe_check` грузит её (`_load_agent_catalog`, строит `HARNESSES`/`AGENT_MODELS`) | как **бенчмаркать** |
| ATP | `method/spawners/<harness>_shim.py` | шим запуска (только для нового harness) | код запуска |
| arbiter | `config/agents.toml` | секция `["<harness>@<model>"]` с policy + cost/duration (ключи scaffold'ятся из `routable=true` каталога) | политика **роутинга** |
| Maestro | `maestro/models.py:72` `AgentType` | значение enum (только для нового harness) | ключ спаунера |
| Maestro | `maestro/spawners/<harness>.py` + `registry.py` | спаунер (только для нового harness) | код **исполнения** |

Единственное общее — `agent_id`, и он **порождается каталогом** (`f"{harness}@{model}"`). Всё остальное (policy, спаунер) живёт у владельца. Согласованность вендоренных копий и arbiter-секций стережёт `make conformance` (ADR-ECO-003).

---

## Случай A — новая МОДЕЛЬ на существующем harness

Пример: `claude_code@claude-sonnet-4-6` (harness `claude_code` уже есть).

| # | Реп | Действие |
|---|-----|----------|
| A1 | **SSOT** | Добавить `[[agents]]` в `agents-catalog.toml`: `harness="claude_code"`, `model="claude-sonnet-4-6"`, `tested=true`, `routable=` по решению (тестирование ≠ роутинг). При новой модели — и `[models."claude-sonnet-4-6"]` в плоскости 1. |
| A2 | ATP | Пере-вендорить: `cp` SSOT → `atp-platform/method/agents-catalog.toml`. Шим уже есть; `run_pipe_check` соберёт `agent_id` из каталога сам. (`make conformance` подтвердит байт-в-байт.) |
| A3 | — | Прогнать sweep → строки в `benchmark_runs` с новым `agent_id`. |
| A4 | arbiter | Если `routable=true` — секция `["claude_code@claude-sonnet-4-6"]` в `config/agents.toml` (см. ниже «Заполнение секции»). Иначе агент только измеряется. |
| A5 | Maestro | **Ничего** — `harness_of_agent_id` (`models.py:103`) редуцирует к `claude_code`, спаунер уже зарегистрирован. |
| A6 | — | Verify join (`make conformance`) + включить вес поэтапно. |

**⚠ Подводный камень A4.** Maestro заспаунит `claude_code` со **своей дефолтной моделью**, а не с выбранной arbiter (модель в спаунер не передаётся). Поэтому:
- Если новая модель — это просто **смена дефолта** harness (заменяем пинованную модель CLI) → работает.
- Если нужны **две модели одного harness одновременно** как отдельные routable-агенты, между которыми arbiter выбирает → **сегодня не исполнимо сквозь Maestro**. Требуется доработка: спаунер должен принимать модель из `routed_agent_type`/Task и прокидывать её в CLI (`--model`/env). Это отдельная задача в Maestro, без неё выбор модели теряется на спауне.

---

## Случай B — новый HARNESS / CLI-инструмент

Пример: `gemini_cli@gemini-2.5-pro` (harness `gemini_cli` новый).

| # | Реп | Действие | Почему в этом порядке |
|---|-----|----------|----------------------|
| B1 | контракт | Зафиксировать `agent_id = "gemini_cli@gemini-2.5-pro"` (точная строка модели провайдера). | Это join-ключ для всех трёх. |
| B2 | SSOT+ATP | В **каталоге**: `[harnesses.gemini_cli]` (`kind`, `shim="method/spawners/gemini_cli_shim.py"`, `model_env="GEMINI_MODEL"`, `routable`) + `[models."gemini-2.5-pro"]` + `[[agents]]` пара; пере-вендорить в ATP. В **ATP**: написать шим; env в `ALLOWED_ENV`. | Способность бенчмаркать. |
| B3 | Maestro | Добавить `GEMINI_CLI = "gemini_cli"` в `AgentType` (`models.py:72`); написать `spawners/gemini_cli.py` (наследник `AgentSpawner`); зарегистрировать в `registry.py`. | **До** того, как arbiter начнёт роутить — иначе HOLD. |
| B4 | — | Прогнать ATP-sweep → `benchmark_runs`. | Данные для seed cost/score и re-rank. |
| B5 | arbiter | Секция `["gemini_cli@gemini-2.5-pro"]` в `config/agents.toml`. | Делает агента routable. |
| B6 | — | Verify join (gen-скрипт) + включить вес поэтапно. | |

**Критично — порядок B3 перед B5.** Если добавить агента в `agents.toml` (B5) раньше, чем появится спаунер Maestro (B3), arbiter начнёт его выбирать, а Maestro вернёт `unknown_agent` → задача в HOLD. Спаунер должен существовать первым.

**Шим (ATP) ≠ спаунер (Maestro).** Это два разных куска кода: шим в ATP запускает агента для бенчмарка, спаунер в Maestro — для реальной работы. Оба нужны, ни один не выводится из другого.

---

## Заполнение секции `agents.toml`

Поля `AgentConfig` (`arbiter-mcp/src/config.rs:18`) — все обязательны:

```toml
["gemini_cli@gemini-2.5-pro"]          # ключ в кавычках (bare-ключ TOML не может содержать '@')
display_name = "Gemini CLI"             # политика
supports_languages = ["python", "go"]   # ПОЛИТИКА — гейт кандидата (route_task.rs:250)
supports_types = ["feature", "review"]  # ПОЛИТИКА — "review" обязателен, чтобы re-rank по code-review сработал
max_concurrent = 2                      # политика
cost_per_hour = 0.25                    # засеять из benchmark_runs (total_cost_usd / часы)
avg_duration_min = 9.0                  # засеять из benchmark_runs (duration_seconds / 60)
```

- `supports_languages` / `supports_types` — **гейт**, а не метаданные: агент попадает в кандидаты (и к re-rank) только если они содержат тип задачи и язык (`route_task.rs:250`). Из бенчмарка не выводятся — это решение по политике.
- `cost_per_hour` / `avg_duration_min` — засеиваются из реальных данных: **`devtools/gen_agents_toml.py`** генерит готовый блок (cost/duration из `benchmark_runs`, policy сохраняет/помечает TODO). ⚠ **Интерим:** этот генератор читает `benchmark_runs` (Variant C, отвергнут ADR-ECO-003 §Options) — подлежит замене на catalog-driven scaffold (ADR-003 a.i.#5). До замены используем его только для **cost/duration-seed**; список routable-ключей берём из каталога.

---

## Verification (join-гард) перед включением

1. **`make conformance`** (или `python3 _cowork_output/devtools/check-agent-id-conformance.py`) — 5 проверок ADR-ECO-003, ловят рассинхрон ДО прогона:
   - вендоренная копия ATP `agents-catalog.toml` == SSOT (байт-в-байт);
   - каждый `routable=true` `agent_id` ↔ секция в arbiter `agents.toml` (байт-в-байт) — прямая защита от silent-None;
   - каждый `routable=true` harness ↔ `AgentType` Maestro (иначе HOLD);
   - нет `safe_agent_id`-коллизий; нет ссылок на `retired`-модели.
2. Запустить `python3 _cowork_output/devtools/gen_agents_toml.py` (интерим) — cost/duration-seed + routable-ключи **без** строк в `benchmark_runs` (→ silent-None, re-rank no-op).
3. Если бенчмарк по типу задачи ≠ `review` — нужна пара в `benchmark_id_for` (`arbiter route_task.rs:42`) **И** `TASK_TYPE_TO_BENCHMARK_ID` (`ATP taxonomy.py`); иначе данные лягут, но в роутинге не используются.

---

## Планируемые расширения (см. ADR-ECO-002)

Две правки в Maestro снимают текущие ограничения этого runbook — зафиксированы в
`decisions/2026-06-20-adr-harness-model-management.md`:

- **D1 — model-passing:** спаунер читает модель из `routed_agent_type` и прокидывает в CLI → случай A2 (две модели одного harness) станет исполнимым.
- **D2 — открыть гейт `AgentType`:** валидация по `SpawnerRegistry` (уже плагинный) вместо enum → кастомные harness/AI-приложения подключаются плагином без правки core, шаг B3 упрощается.
- **D3 — ✅ реализован ADR-ECO-003:** общий harness+model-descriptor вынесен в SSOT-каталог `agents-catalog.toml` (ATP уже генерит ростер из него; Maestro-генерация #4 ждёт D2; arbiter scaffold #5 в работе).

## Рекомендуемые действия

- **Maestro (предусловие для любого нового harness):** добавить спаунер + `AgentType` **до** регистрации агента в arbiter.
- **Maestro (P1, разблокирует случай A2):** научить спаунер принимать модель из `routed_agent_type` и прокидывать в CLI — иначе мульти-модельный роутинг одного harness не исполним (ADR-ECO-002 D1).
- **arbiter:** routable-набор ведётся из **SSOT-каталога** (ADR-ECO-003), не из `benchmark_runs`. Ключи scaffold'ятся из `routable=true`; policy-поля (cost/duration/supports_*) руками. `gen_agents_toml.py` (из `benchmark_runs`) — интерим Variant C, подлежит замене (a.i.#5).
- **Кросс-реп (когда выйдем за code-review):** синхронно добавлять пару `task_type ↔ benchmark_id` в обоих репах.
