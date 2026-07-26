# Handoff → spec-runner / dispatcher / Maestro: `owner_role` — singular slug (DEC-007)

> **Контекст (2026-07-26):** владелец steward принял DEC-007 — каноническая форма `owner_role`
> меняется на **одну роль-slug без `@`**. Это **отменяет форму значения**, о которой steward
> просил в `2026-07-15-spec-runner-specmeta-v2-handoff.md`; остальная часть того ask'а в силе.
> Решение зафиксировано в `steward/spec/20-design.md` (DEC-007 + «Модель идентичности ролей»),
> каталог ролей заведён как `steward/profiles/roles.yaml`. Правки в чужих репо не сделаны —
> каждый шаг делает владелец своего репо через PR.

## 0. TL;DR — почему это срочно

spec-runner **прямо сейчас** реализует SpecMeta contract v2 (ветка `feat/specmeta-contract-v2`,
план `spec-runner/docs/superpowers/plans/2026-07-26-specmeta-contract-v2.md`, `owner_role` уже
first-class в `35f47ff`). Он делает это по ask'у от 2026-07-15, где значение поля описано как
`"@role[,@role]"`. **Этой формы steward больше не просит.** Если v2 зафиксирует её, контракт
придётся ломать вторым бампом.

Новая каноническая форма: `owner_role: <role-slug>` — **одна** роль, slug **без `@`**.

## 1. Решение (DEC-007)

- `owner_role` — ровно **одна accountable роль**; slug без `@`; стабильное машинное имя,
  не display name и не `@github-handle`.
- Множественность моделируется **отдельными полями**, а не tuple внутри `owner_role`:
  `reviewer_roles: [<slug>]` (обязательные ревьюеры) и `allowed_approver_roles: [<slug>]`
  (кто вправе аппрувнуть гейт).
- Причина: ownership и authorization — разные отношения. Несколько допустимых аппруверов ≠
  несколько владельцев. Singular-форма убирает преобразования на границах
  spec-runner ↔ steward ↔ dispatcher.
- Каталог ролей и `slug_pattern` — **SSOT steward**: `steward/profiles/roles.yaml` (v1,
  `^[a-z][a-z0-9-]{1,31}$`). Потребители вендорят пиненую копию; собственной формы не определяют.
- Валидация на стороне steward: уникальность slug, соответствие шаблону, разрешимость ссылок
  `owner_role`/`reviewer_roles`/`allowed_approver_roles`, запрет удаления используемой роли без
  явной миграции и бампа версии каталога.
- `authority.yaml` описывает **полномочия** (role/phase allowlist агентов) и намеренно **не**
  владеет идентичностью governance-ролей — это разные оси.

Пример canonical-фронтматтера:

```yaml
spec_stage: requirements
owner_role: product
reviewer_roles: [architects]
allowed_approver_roles: [product, tech-lead]
```

Правила миграции legacy-формы `"@a,@b"`: снять `@`; tuple длины 1 → строка; **tuple длины > 1 не
нормализуется молча** — требуется выбрать accountable владельца, остальные роли переносятся в
`reviewer_roles`/`allowed_approver_roles`; reader временно принимает legacy, writer выпускает
только canonical v2.

## 2. Что это меняет для spec-runner (C2 / SpecMeta v2)

Изменение **только в семантике значения**, не в типе поля — `owner_role: str = ""` остаётся:

- значение — один slug (`product`), а не список через запятую и не `@product`;
- spec-runner **не валидирует** словарь ролей и не разбирает значение: он носитель поля,
  семантика принадлежит steward (как и в ask'е от 07-15);
- желательно (не блокирует): `reviewer_roles` / `allowed_approver_roles` проходят как
  pass-through ключи наравне с `upstream_hashes` — интерпретирует их steward;
- остальное в силе: `SPEC_META_CONTRACT = 2`, `approved_by` = git-handle человека,
  `generated_by` = agent-id. По замеру самого spec-runner (2026-07-26) это уже так, и REQ-402
  бандла сводится к «задокументировать», а не «добавить поле».

После этого steward ре-вендорит контракт и убирает обход «читаем `owner_role` из сырого
frontmatter-dict» (`steward/src/steward/meta.py`).

## 3. Что это меняет для dispatcher

Предложение из `2026-07-13-dispatcher-owner-role-and-gates-handoff.md` §1 — **одна строка-роль,
не список, без `@`, не person/@handle** — **принято целиком**. Расхождение было на стороне
steward (мы парсили `"@a,@b"` в tuple) и устраняется у нас.

- dispatcher продолжает нести `owner_role` сквозным полем, ничего не валидируя (анти-цель в силе);
- когда каталог стабилизируется — вендорить пиненую копию `roles.yaml` рядом со схемой
  verdict-записей.

## 4. Что это значит для Maestro (WS-006 M-1)

`gate_verdicts.jsonl` обязан ссылаться на ту же role identity model: поле роли в записи — тот же
slug из каталога steward. Схема записи и каталог `gate_id` — за steward (в работе, `steward/TODO.md`
§3); Maestro вендорит пиненую копию, как и планировалось в
`2026-07-12-ws006-gates-maestro-handoff.md`.

## 5. Открытый вопрос (решает steward, не потребители)

Маппинг `slug → @github-handle` для CODEOWNERS. В модель ролей он не входит (роль — не handle) и
живёт на границе с CODEOWNERS; форма (отдельный файл против секции в профиле) не выбрана —
пункт в `steward/TODO.md` §1.

## Ссылки

- Решение: `steward/spec/20-design.md` — DEC-007 + «Модель идентичности ролей».
- Каталог: `steward/profiles/roles.yaml` (v1).
- Открытые пункты миграции: `steward/TODO.md` §1 «Role identity model (DEC-007)».
- Предыдущий ask (устарел в части формы значения):
  `2026-07-15-spec-runner-specmeta-v2-handoff.md`.
- Предложение dispatcher, которое здесь принимается:
  `2026-07-13-dispatcher-owner-role-and-gates-handoff.md`.
