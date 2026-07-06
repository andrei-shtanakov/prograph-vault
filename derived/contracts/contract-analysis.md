---
title: Contract analysis
type: contract-snapshot
status: living
source: _cowork_output/contracts/contract-analysis.md
sha256: 194745b2943a48144415bef0b556c07578a95f2f8e08abff338d3fd434065d4a
updated: 2026-07-06
---

# Анализ контрактных точек между проектами

**Дата:** 2026-04-05

> **Обновление 2026-04-17:** основной статус ниже (Maestro↔Arbiter, Maestro↔ATP)
> **устарел** — Maestro v0.2.0 (commit `e4f0a9f`) выкатил MCP-клиент для Arbiter,
> вендорнув DTO из arbiter `861534e`. Раздел "Рекомендуемые действия" пунктов 1-2-4
> закрыт. Пункты 3 и 5 закрыты в R-04 (`0498c82`).
>
> Для семантического маппинга invariants ↔ guardrails (R-13) см.
> `arbiter/docs/guardrails-atp-mapping.md`. Вкратце: системы работают в
> непересекающихся фазах (arbiter = pre-dispatch, ATP = pre-evaluation),
> shared-типы извлекать преждевременно.

## TL;DR

1. **Maestro → Arbiter (MCP route_task / report_outcome / get_agent_status): НЕ РЕАЛИЗОВАНО.** Arbiter определяет полноценные MCP-контракты с serde-валидацией, но в Maestro нет ни одной строки кода, вызывающей Arbiter. Интеграция существует только в документации (COWORK_CONTEXT.md).
2. **Maestro → ATP Platform (verify): НЕ РЕАЛИЗОВАНО.** Нет кода, ссылок или конфигов. Только упоминания в шаблонах.
3. **Maestro → spec-runner: РЕАЛИЗОВАНО.** Subprocess-вызов + callback REST endpoint + polling `.executor-state.json`. Контракт неформальный — нет shared schema, mapping захардкожен в обоих проектах.
4. **Maestro tasks.yaml / project.yaml: ФОРМАЛИЗОВАНО.** Полная Pydantic-валидация с типами, диапазонами, кросс-валидацией зависимостей.
5. **Главный риск:** Карта интеграций в COWORK_CONTEXT.md описывает связи Maestro↔Arbiter и Maestro↔ATP как существующие, но это **планируемые**, не реализованные контракты.

---

## Контракт 1: Maestro → Arbiter `route_task` (MCP)

### Статус: 🔴 НЕ РЕАЛИЗОВАНО (Maestro-сторона отсутствует)

### Сторона Arbiter (потребитель — полностью готов)

**Определение:** `arbiter/arbiter-mcp/src/tools/route_task.rs`, `arbiter/arbiter-mcp/src/server.rs`

**Input Schema (JSON, serde-validated):**

| Поле | Тип | Required | Описание |
|------|-----|----------|----------|
| `task_id` | string | ✅ | Уникальный ID задачи |
| `task.type` | enum | ✅ | `"feature"` / `"bugfix"` / `"refactor"` / `"test"` / `"docs"` / `"review"` / `"research"` |
| `task.language` | enum | ✅ | `"python"` / `"rust"` / `"typescript"` / `"go"` / `"mixed"` / `"other"` |
| `task.complexity` | enum | ✅ | `"trivial"` / `"simple"` / `"moderate"` / `"complex"` / `"critical"` |
| `task.priority` | enum | ✅ | `"low"` / `"normal"` / `"high"` / `"urgent"` |
| `task.scope` | string[] | ❌ | Файлы/директории (default: []) |
| `task.branch` | string? | ❌ | Git-ветка |
| `task.estimated_tokens` | u64? | ❌ | Оценка токенов |
| `task.has_dependencies` | bool | ❌ | default: false |
| `task.requires_internet` | bool | ❌ | default: false |
| `task.sla_minutes` | u32? | ❌ | SLA в минутах |
| `task.description` | string? | ❌ | Описание |
| `constraints.preferred_agent` | string? | ❌ | Предпочтительный агент |
| `constraints.excluded_agents` | string[] | ❌ | Исключённые агенты |
| `constraints.budget_remaining_usd` | f64? | ❌ | Оставшийся бюджет |
| `constraints.total_pending_tasks` | u32? | ❌ | Задач в очереди |
| `constraints.running_tasks` | RunningTask[] | ❌ | Текущие запущенные задачи |

**Output Schema:**

| Поле | Тип | Описание |
|------|-----|----------|
| `task_id` | string | ID задачи |
| `action` | enum | `"assign"` / `"reject"` / `"fallback"` |
| `chosen_agent` | string | ID выбранного агента |
| `confidence` | f64 | 0.0–1.0 |
| `reasoning` | string | Объяснение решения |
| `decision_path` | string[] | Путь по дереву решений |
| `invariant_checks` | InvariantResult[] | Результаты проверок безопасности |
| `metadata.inference_us` | u64 | Время инференса (мкс) |
| `metadata.feature_vector` | f64[22] | Вектор фичей |

**Валидация:** serde derive + runtime fallback (unknown task_type → "feature", unknown language → "other"). Не JSON Schema, но строго типизировано.

### Сторона Maestro (источник — НЕ СУЩЕСТВУЕТ)

**Поиск:** `grep -r "route_task\|arbiter" maestro/` → **0 результатов** в исходном коде.

В Maestro определена своя модель `TaskConfig` (Pydantic):

| Поле Maestro | Тип | Эквивалент в Arbiter |
|--------------|-----|---------------------|
| `id` | str | → `task_id` ✅ |
| `title` | str | — (нет в Arbiter) |
| `prompt` | str | → `task.description` ≈ |
| `agent_type` | enum: claude_code/codex/aider/announce | ≠ Arbiter сам выбирает агента |
| `scope` | list[str] | → `task.scope` ✅ |
| `priority` | int (-100..100) | ≠ Arbiter ожидает enum: low/normal/high/urgent |
| `timeout_minutes` | int | → `task.sla_minutes` ≈ |
| — | — | `task.type` — НЕТ в Maestro |
| — | — | `task.language` — НЕТ в Maestro |
| — | — | `task.complexity` — НЕТ в Maestro |

### Анализ совместимости

| Аспект | Оценка | Детали |
|--------|--------|--------|
| Формат task_id | ✅ Совместим | Оба — строки |
| task.type | ❌ Нет маппинга | Maestro не передаёт тип задачи; Arbiter требует enum |
| task.language | ❌ Нет маппинга | Maestro не имеет поля language; Arbiter требует enum |
| task.complexity | ❌ Нет маппинга | Maestro не имеет поля complexity; Arbiter требует enum |
| priority | 🟡 Несовместимые типы | Maestro: int (-100..100), Arbiter: enum (low/normal/high/urgent) |
| scope | ✅ Совместим | Оба — массив строк |
| agent selection | ❌ Конфликт концепций | Maestro: agent_type задаётся в конфиге вручную. Arbiter: сам выбирает агента. Конфликт ролей |

### Риск: 🔴 Контракт не реализован

**Рекомендация:**
1. Определить, будет ли Maestro делегировать выбор агента Arbiter'у (заменить `agent_type` на вызов `route_task`) или Arbiter остаётся advisory
2. Добавить в `TaskConfig` поля `task_type`, `language`, `complexity` (или автоматически извлекать из prompt/scope)
3. Создать маппинг `priority: int → enum` при формировании запроса к Arbiter
4. Реализовать MCP-клиент в `maestro/coordination/` для вызова Arbiter

---

## Контракт 2: Maestro → Arbiter `report_outcome` (MCP)

### Статус: 🔴 НЕ РЕАЛИЗОВАНО (Maestro-сторона отсутствует)

### Сторона Arbiter (полностью готов)

**Определение:** `arbiter/arbiter-mcp/src/tools/report_outcome.rs`

**Input Schema:**

| Поле | Тип | Required | Описание |
|------|-----|----------|----------|
| `task_id` | string | ✅ | ID задачи (из route_task) |
| `agent_id` | string | ✅ | Агент, выполнивший задачу |
| `status` | enum | ✅ | `"success"` / `"failure"` / `"timeout"` / `"cancelled"` |
| `duration_min` | f64? | ❌ | Длительность в минутах |
| `tokens_used` | u64? | ❌ | Потреблённые токены |
| `cost_usd` | f64? | ❌ | Стоимость в USD |
| `exit_code` | i32? | ❌ | Код выхода процесса |
| `files_changed` | u32? | ❌ | Количество изменённых файлов |
| `tests_passed` | bool? | ❌ | Прошли ли тесты |
| `validation_passed` | bool? | ❌ | Прошла ли валидация |
| `error_summary` | string? | ❌ | Описание ошибки |
| `retry_count` | u32 | ❌ | Кол-во повторов (default: 0) |

**Output Schema:**

| Поле | Тип | Описание |
|------|-----|----------|
| `task_id` | string | ID задачи |
| `recorded` | bool | Записано ли в БД |
| `updated_stats.success_rate` | f64 | Обновлённый success rate агента |
| `retrain_suggested` | bool | Нужно ли переобучить дерево |

### Сторона Maestro

**Поиск:** `grep -r "report_outcome" maestro/` → **0 результатов**.

Maestro хранит результаты в своей SQLite (`database.py`) и обновляет `TaskStatus`, но **не отправляет их в Arbiter**.

Maestro имеет все необходимые данные для формирования report_outcome:

| Данные Maestro | Поле Arbiter | Источник |
|----------------|-------------|----------|
| task.id | task_id | models.py:Task.id |
| task.agent_type | agent_id | models.py:Task.agent_type (нужен маппинг → arbiter agent_id) |
| task.status | status | models.py:TaskStatus (DONE→"success", FAILED→"failure") |
| started_at → completed_at | duration_min | models.py:Task.started_at / completed_at |
| retry_count | retry_count | models.py:Task.retry_count |
| validation_cmd result | validation_passed | validator.py:ValidationResult |
| — | tokens_used | ❌ Не собирается (есть cost_tracker.py, но токены не на уровне задач) |
| — | cost_usd | ❌ Не собирается на уровне задач |

### Риск: 🔴 Контракт не реализован

**Рекомендация:** При реализации интеграции route_task, добавить report_outcome как callback после завершения задачи в `scheduler.py` (метод обработки завершения).

---

## Контракт 3: Maestro → Arbiter `get_agent_status` (MCP)

### Статус: 🔴 НЕ РЕАЛИЗОВАНО (Maestro-сторона отсутствует)

### Сторона Arbiter (полностью готов)

**Определение:** `arbiter/arbiter-mcp/src/tools/agent_status.rs`

**Input:** `{ "agent_id": "string" }` (optional — без него возвращает все агенты)

**Output:** Список агентов с `id`, `display_name`, `state` (active/busy/failed), `capabilities`, `current_load`, `performance` (success_rate, by_language, by_type).

### Сторона Maestro

Не используется. Maestro управляет агентами через свой `spawners/registry.py` — статический реестр, без runtime-статистики.

### Риск: 🔴 Контракт не реализован

**Рекомендация:** Может быть полезен для динамического выбора агента и отображения состояния в дашборде Maestro.

---

## Контракт 4: Maestro → ATP Platform (verify)

### Статус: 🔴 НЕ РЕАЛИЗОВАНО (обе стороны не связаны)

**Поиск в Maestro:** `grep -r "atp\|benchmark\|evaluate" maestro/` → **0 релевантных результатов** (только unrelated matches).

**Поиск в ATP:** ATP — framework-agnostic платформа. Имеет 12+ адаптеров, включая HTTP и CLI. Maestro мог бы использовать:
- `atp run` CLI для запуска тестов
- HTTP API дашборда для получения результатов
- Python SDK (`atp-platform-sdk`) для программной интеграции

### Потенциальный контракт

| Сторона | Формат | Готовность |
|---------|--------|------------|
| ATP CLI | `atp run --config test.yaml --adapter cli` | ✅ Готов |
| ATP HTTP API | FastAPI endpoints | ✅ Готов |
| ATP Python SDK | `from atp_sdk import ...` | ✅ Готов (v2.0.0) |
| Maestro вызов | — | ❌ Не существует |

### Риск: 🔴 Контракт не реализован

**Рекомендация:** Определить, на каком этапе нужна верификация через ATP — после завершения задачи (validation hook) или как отдельный шаг в DAG.

---

## Контракт 5: Maestro → spec-runner (subprocess)

### Статус: 🟡 РЕАЛИЗОВАНО, но контракт неформальный

### Сторона Maestro (источник)

**Вызов:** `maestro/orchestrator.py:340-356`
```
spec-runner run --all [--callback-url <url>]
```

**Конфигурация:** `maestro/models.py:716-763` — `SpecRunnerConfig` (Pydantic), конвертируется в `executor.config.yaml` через `to_executor_config()`:

```python
class SpecRunnerConfig(BaseModel):
    max_retries: int = 3
    task_timeout_minutes: int = 30
    claude_command: str = "claude"
    auto_commit: bool = True
    create_git_branch: bool = True
    run_tests_on_done: bool = True
    test_command: str = "uv run pytest"
    lint_command: str = "uv run ruff check ."
    run_lint_on_done: bool = True
```

**Callback receiver:** `maestro/coordination/rest_api.py:1061-1100`
```python
class CallbackRequest(BaseModel):
    task_id: str       # spec-runner task ID
    status: str        # Task status (строка, не enum!)
    duration_seconds: float = 0.0
    error: str | None = None
```

**Progress polling:** `maestro/orchestrator.py:406-438` — читает `.executor-state.json`:
```python
state = json.loads(content)
tasks = state.get("tasks", {})
done = sum(1 for t in tasks.values() if t.get("status") == "success")
```

### Сторона spec-runner (потребитель)

spec-runner — **внешний пакет** (не в этой экосистеме). Контракт определяется только:
- CLI interface: `spec-runner run --all [--callback-url URL]`
- Формат `executor.config.yaml` — Maestro генерирует, spec-runner читает
- Формат `.executor-state.json` — spec-runner пишет, Maestro читает
- Callback POST body — spec-runner отправляет, Maestro принимает

### Анализ совместимости

| Контрактная точка | Валидация | Риск |
|-------------------|-----------|------|
| CLI args (`--all`, `--callback-url`) | Нет формальной схемы | 🟡 Зависит от spec-runner CLI stability |
| `executor.config.yaml` формат | Maestro генерирует dict → YAML. spec-runner парсит. Нет shared schema | 🟡 Рассогласование возможно при обновлении spec-runner |
| `.executor-state.json` формат | Maestro парсит ad-hoc (`state.get("tasks", {})`, `t.get("status")`) | 🟡 Хрупкий — нет типизированной модели на стороне Maestro |
| Callback POST body | Pydantic `CallbackRequest` на Maestro. Формат на стороне spec-runner неизвестен | 🟡 Валидация только на приёмной стороне |

### Риск: 🟡 Контракт неформальный

**Рекомендация:**
1. Создать Pydantic-модель `ExecutorState` в Maestro для типизированного парсинга `.executor-state.json`
2. Добавить интеграционные тесты, которые проверяют совместимость с реальным spec-runner
3. Зафиксировать версию spec-runner в зависимостях Maestro

---

## Контракт 6: Maestro tasks.yaml (внутренний)

### Статус: 🟢 ФОРМАЛИЗОВАНО (Pydantic)

**Определение:** `maestro/models.py:81-442` + `maestro/config.py:170-224`

**Валидация:**
- Pydantic v2 модели с Field constraints
- Task ID: regex `^[a-zA-Z0-9_-]+$`
- timeout_minutes: range 1–1440
- max_retries: range 0–10
- priority: range -100..100
- Кросс-валидация: нет self-dependencies, все depends_on ссылаются на существующие ID, уникальность ID
- Environment variable substitution: `${VAR}` синтаксис
- Defaults application через `model_validator(mode="after")`

**AgentType enum (Maestro):**

| Значение | Описание |
|----------|----------|
| `claude_code` | Claude Code CLI |
| `codex` | Codex CLI |
| `aider` | Aider |
| `announce` | Notification-only (no execution) |

Сравнение с Arbiter `agents.toml`:

| Maestro AgentType | Arbiter agent_id | Совпадение |
|-------------------|-----------------|------------|
| `claude_code` | `claude_code` | ✅ |
| `codex` | `codex_cli` | ❌ Разные имена! |
| `aider` | `aider` | ✅ |
| `announce` | — | ❌ Нет в Arbiter |

### Риск: 🟢 Внутренний контракт формализован

**Но:** при будущей интеграции с Arbiter — маппинг `codex` ↔ `codex_cli` потребует нормализации.

---

## Контракт 7: Maestro MCP Coordination (внутренний)

### Статус: 🟢 ФОРМАЛИЗОВАНО (FastMCP + Pydantic)

**Определение:** `maestro/coordination/mcp_server.py:164-399`

**Инструменты:**

| Tool | Input | Output | Валидация |
|------|-------|--------|-----------|
| `get_available_tasks` | `agent_id: str` | Список задач со статусом READY | Pydantic |
| `claim_task` | `agent_id: str, task_id: str` | ClaimResult | Optimistic locking + state machine |
| `update_status` | `agent_id, task_id, status, result_summary?, error_message?` | StatusResult | State transition validation |
| `get_task_result` | `task_id: str` | TaskResult | Pydantic |
| `post_message` | `agent_id, message, to_agent?` | MessageResponse | Pydantic |
| `read_messages` | `agent_id, unread_only?` | list[MessageResponse] | Pydantic |

**REST API зеркалирует MCP:** `maestro/coordination/rest_api.py` — те же endpoints через FastAPI.

### Риск: 🟢 Формализован, типизирован, протестирован

---

## Сводная таблица контрактов

| # | Контракт | Источник → Потребитель | Статус реализации | Валидация | Риск |
|---|----------|----------------------|-------------------|-----------|------|
| 1 | `route_task` MCP | Maestro → Arbiter | ❌ Не реализован | serde (Arbiter) / — (Maestro) | 🔴 |
| 2 | `report_outcome` MCP | Maestro → Arbiter | ❌ Не реализован | serde (Arbiter) / — (Maestro) | 🔴 |
| 3 | `get_agent_status` MCP | Maestro → Arbiter | ❌ Не реализован | serde (Arbiter) / — (Maestro) | 🔴 |
| 4 | Verify/evaluate | Maestro → ATP | ❌ Не реализован | — / — | 🔴 |
| 5 | spec-runner subprocess | Maestro → spec-runner | ✅ Реализован | Pydantic (Maestro) / ad-hoc (state file) | 🟡 |
| 6 | tasks.yaml config | User → Maestro | ✅ Реализован | Pydantic v2, полная валидация | 🟢 |
| 7 | MCP coordination | Agents ↔ Maestro | ✅ Реализован | FastMCP + Pydantic | 🟢 |

---

## Ключевые несовместимости (для будущей интеграции)

### При реализации Maestro → Arbiter:

| Проблема | Maestro | Arbiter | Решение |
|----------|---------|---------|---------|
| Agent ID naming | `codex` | `codex_cli` | Нормализовать в одном из проектов или создать маппинг |
| Priority format | `int (-100..100)` | `enum (low/normal/high/urgent)` | Маппинг: -100..-26→low, -25..25→normal, 26..75→high, 76..100→urgent |
| Нет task_type | — | required enum (7 значений) | Добавить поле в TaskConfig или вывести из prompt/scope |
| Нет language | — | required enum (6 значений) | Добавить поле или определять из scope (*.py → python) |
| Нет complexity | — | required enum (5 значений) | Добавить поле или эвристика по scope_size / estimated_tokens |
| announce agent | Есть | Нет в agents.toml | announce не маршрутизируется через Arbiter |

---

## Рекомендуемые действия

1. **🔴 Обновить COWORK_CONTEXT.md** — карта интеграций показывает Maestro→Arbiter и Maestro→ATP как существующие связи. Нужно пометить их как **planned**, не implemented.
   - *Привязка:* `COWORK_CONTEXT.md`, секция "Карта интеграций"

2. **🔴 Создать интеграционный план Maestro↔Arbiter** — определить:
   - Будет ли Arbiter advisory (подсказки) или authoritative (принимает решения)?
   - Кто добавляет недостающие поля (task_type, language, complexity) — пользователь в YAML или Maestro автоматически?
   - *Привязка:* `Maestro/maestro/models.py:81-154` (TaskConfig), `arbiter/arbiter-core/src/types.rs` (TaskInput)

3. **🟡 Типизировать `.executor-state.json`** — создать Pydantic-модель в Maestro для парсинга вместо ad-hoc `state.get("tasks", {})`.
   - *Привязка:* `Maestro/maestro/orchestrator.py:406-438`

4. **🟡 Нормализовать agent IDs** — `codex` vs `codex_cli` вызовет ошибку при интеграции.
   - *Привязка:* `Maestro/maestro/models.py` (AgentType enum), `arbiter/config/agents.toml`

5. **🟢 Зафиксировать spec-runner version** — добавить в `pyproject.toml` как зависимость с pinned version.
   - *Привязка:* `Maestro/pyproject.toml`
