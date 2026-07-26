# Handoff → spec-runner-vscode: frontmatter-схема открыта, нужен ре-вендоринг

> Дата: 2026-07-26 · Автор: сессия Claude Code в `spec-runner` · Статус: **готово к применению**
> Правки в `spec-runner-vscode/` здесь **не сделаны** — это handoff, применяет владелец репо через PR.

## Условие применения

Применять **после мержа** `spec-runner` PR #54. Он уже влит: merge-коммит `6d92ca1` в `master`.
Выпущено как **`v2.11.0`** (PyPI + GitHub Release, 2026-07-26, release commit `7be192c`).
Версия-пин можно поднимать до `>=2.11.0`.

**Срочность: средняя, не аварийная.** Расширение fail-soft — оно логирует дрейф и продолжает
работать на best-effort значениях. Ничего у пользователей не сломается. Но до ре-вендоринга
предупреждение будет срабатывать на **каждой здоровой** governed-спеке, то есть сигнализация
перестанет что-либо обнаруживать.

## Что изменилось в `schemas/spec-frontmatter.schema.json`

Две правки, обе намеренные.

**1. `additionalProperties: false` → `true`.**
Старое значение стояло как сигнализация дрейфа — в описании прямо было написано «so a new
SpecMeta field trips the contract test». Оно вошло в прямое противоречие с contract v2:
frontmatter теперь **намеренно расширяем**, чужие ключи расширяющих слоёв (steward пишет
`traces_to`, `upstream_hashes`) сохраняются spec-runner'ом losslessly и остаются в файле.
При `additionalProperties: false` любая реально управляемая спека провалила бы валидацию.

Защита от дрейфа не потеряна, а усилена: она переехала в тест
`test_schema_lists_every_canonical_field`, который сверяет `properties` с
`canonical_fields()`. Он строже прежнего — срабатывает на новое поле `SpecMeta` даже без
живого документа, который бы его содержал, тогда как `additionalProperties: false` нуждался
в таком документе.

**2. `spec_stage`: `enum: ["requirements","design","tasks"]` → `type: string, minLength: 1`.**
Это починка **латентного бага**, не следствие contract v2. Стадийные профили появились в
`spec-runner` v2.9.0, и с тех пор спека на любой не-`lite` стадии (например `acceptance`)
проваливала ваш контракт. Принадлежность стадии активному профилю — runtime-проверка против
конфигурации; JSON Schema без профиля выразить её не может.

**3. Добавлено свойство `owner_role`** типа `["string", "null"]` — новое каноническое поле
`SpecMeta` (CODEOWNERS-роль вида `"@role[,@role]"`).

В схему добавлен `$comment`, фиксирующий: `properties` описывает канонические поля, которыми
владеет spec-runner; дополнительные ключи разрешены намеренно и сохраняются losslessly;
принадлежность стадии проверяется в рантайме.

## Что делать

1. **Ре-вендорить** `schemas/spec-frontmatter.schema.json` из `spec-runner` `6d92ca1`.
   Точки, где живёт пиненая копия и валидация: `src/schemas.ts` (около строки 18 —
   `additionalProperties: false`) и `src/specState.ts` (около строк 88–91 — рантайм-валидация
   живого frontmatter с предупреждением `[spec-runner] frontmatter drift in ...`).
2. **Проверить, что предупреждение о дрейфе больше не ложносрабатывает** на спеке с
   `owner_role` и с чужими ключами вида `traces_to`.
3. **Проверить кастомный профиль**: спека со `spec_stage: acceptance` должна проходить.
4. Version-pin: поднять до `spec-runner>=2.11.0` — релиз опубликован.

## Смежное: `--spec-prefix` ВСЁ ЕЩЁ СЛОМАН

Отдельный баг, который расширения касается напрямую и **в этот релиз не вошёл**.
Перепроверено на `v2.11.0`:

| Вызов | Факт |
|---|---|
| `spec-runner --spec-prefix=X run` (флаг ПЕРЕД субкомандой) | молча игнорируется, значение `''` |
| `spec-runner run --spec-prefix=X` (флаг ПОСЛЕ) | работает |
| `spec-runner spec status --spec-prefix=X` | `SystemExit 2`, флаг не принимается |

Причина первого: `--spec-prefix` объявлен и на top-level парсере, и в parent-парсере
`common`, от которого наследуются субкоманды; субпарсер применяет свой `default=""` после
top-level и затирает значение. **Расширение ставит флаг именно перед субкомандой**, то есть
настройка `spec-runner.specPrefix` сейчас не работает вообще.

Обходной путь до фикса: ставить флаг **после** субкоманды. Семейство `spec` обойти нельзя —
там флага нет вовсе.

Фикс запланирован на стороне `spec-runner` (открытые пункты в его `TODO.md`), отдельным PR.
Эта заметка будет обновлена, когда он выйдет.

## Ссылки

- Контракт: `spec-runner/docs/CONTRACTS.md`
- Дизайн: `spec-runner/docs/superpowers/specs/2026-07-26-specmeta-contract-v2-design.md`
- PR схемы: https://github.com/andrei-shtanakov/spec-runner/pull/54
- PR профильной осведомлённости: https://github.com/andrei-shtanakov/spec-runner/pull/53
- Релиз: https://github.com/andrei-shtanakov/spec-runner/releases/tag/v2.11.0
