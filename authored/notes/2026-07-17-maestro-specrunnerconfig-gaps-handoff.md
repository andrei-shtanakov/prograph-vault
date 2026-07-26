# Handoff → Maestro: `SpecRunnerConfig` прокидывает лишь малую часть `ExecutorConfig`

> **Контекст (2026-07-17):** при разборе вопроса «где у spec-runner конфигурируется модель
> для code-review» выяснилось, что Maestro-запущенный run фактически не имеет доступа к
> большей части настроек spec-runner — `SpecRunnerConfig.to_executor_config()`
> (`maestro/models.py:1152,1184`) сериализует только узкое подмножество полей
> `ExecutorConfig` (`spec-runner/src/spec_runner/config.py`). Находка со стороны
> spec-runner, правки нужны в Maestro — spec-runner чужой код не правит, фиксируется
> здесь. Расширяет более раннюю (2026-06-11) заметку про Telegram-креды тем же корнем
> причины на весь набор полей.

## TL;DR

`SpecRunnerConfig` — вручную поддерживаемое подмножество `ExecutorConfig` без какой-либо
проверки на расхождение. Каждое новое поле `ExecutorConfig` невидимо для Maestro, пока
кто-то руками не добавит зеркальное поле и не прокинет его в `to_executor_config()`.
Сейчас проброшены только: `max_retries`, `task_timeout_minutes`, `claude_command`,
`auto_commit`, `spec_prefix`, `hooks.pre_start.create_git_branch`,
`hooks.post_done.{run_tests,run_lint,auto_commit}`, `commands.{test,lint}`.

## Непроброшенные поля (Maestro-run = spec-runner/CLI-дефолты)

- **Модели**: `claude_model`, `review_command`, `review_model` — задачи и ревью всегда
  идут на дефолтной модели голого `claude` CLI; ревью никогда не получает другую/более
  сильную модель или другой CLI (например codex), хотя `config.py` это поддерживает.
- **Personas**: `personas` (dict `Persona`: system_prompt/model/focus по роли —
  architect/implementer/reviewer/qa) — `get_model_for_role()` всегда падает на
  `claude_model` (тоже пустой), т.к. ни одна persona никогда не сконфигурирована.
- **Параллельное ревью**: `review_parallel` / `review_roles` — multi-agent review никогда
  не активируется в Maestro-запусках.
- **Telegram**: `telegram_bot_token` / `telegram_chat_id` — исходная находка
  (2026-06-11); spec-runner v2.0.0 убрал env-var fallback, поэтому уведомлений в Telegram
  из Maestro-run нет вообще.
- **Webhook**: `webhook_url` / `webhook_method` / `webhook_headers` / `webhook_template`
  — та же дыра, generic webhook-уведомлений тоже нет.
- **Бюджеты**: `budget_usd` / `task_budget_usd` / `max_retry_cost_usd` — не прокидываются;
  ограничен только `spec_gen_budget_usd` (отдельное Maestro-only поле для
  `plan --full`).
- **Прочие hook-флаги**: `lint_blocking`, `integration_pr`, `main_branch`, `sync_deps` —
  вообще не выведены наружу в `SpecRunnerConfig`.

## Рекомендация

Не блокирует ничего срочно, но стоит держать в уме при работе с Maestro↔spec-runner
интеграцией:
1. Перед тем как полагаться на «эта настройка spec-runner сработает и из-под Maestro»,
   проверять — реально ли `SpecRunnerConfig` её прокидывает.
2. Приоритет по ценности, если решат закрывать: `claude_model`/`review_model` (разная
   модель для ревью — самое частое реальное желание), затем Telegram/webhook
   (уведомления), затем бюджеты.
3. Возможный системный фикс вместо ручного зеркалирования поле-за-полем: разрешить
   `SpecRunnerConfig` принимать произвольный `extra_executor_config: dict[str, Any]`,
   который мержится поверх `to_executor_config()` — закрывает будущий дрейф разом, ценой
   типобезопасности этих полей.

## Ссылки

- Источник находки: `spec-runner/src/spec_runner/config.py` (`ExecutorConfig`, `Persona`,
  `get_model_for_role`), `maestro/maestro/models.py:1152` (`SpecRunnerConfig`),
  `maestro/maestro/workspace.py:170` (`setup_spec_runner`)
- Более ранняя частная находка (Telegram-only): spec-runner memory
  `maestro-spec-runner-telegram` (2026-06-11), обновлена 2026-07-17 до полного списка.
