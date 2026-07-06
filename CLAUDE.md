# Ecosystem KB — правила (CLAUDE.md)

> Единая база знаний мульти-проектной экосистемы (повышена из prograph-vault, ADR 2026-07-05).
> Этот файл — **конституция KB**. Все агенты и люди следуют ему при чтении/записи.

## 0. Назначение

KB хранит **cross-cutting знание экосистемы**: правила, ADR, контракты (снапшоты), шаблоны,
скилы-указатели, заметки/планы, реестр проектов. KB — **источник правды для cross-cutting**;
он **не дублирует** то, чем владеют репо (см. §4).

## 1. Золотые правила (инварианты)

1. **`authored/` пишут ЛЮДИ (через git-review). `derived/` пишут ИНСТРУМЕНТЫ.** Никогда не смешивать.
2. **KB ссылается на контракты, но не владеет ими.** Авторитет — в репе-производителе.
3. **Repo-local правила живут в CLAUDE.md репы.** KB держит только cross-cutting; CLAUDE.md репы
   *ссылается* на `authored/rules/`, не копирует.
4. **Канон рождается в `_cowork_output/` (dev-scratch) и graduated в KB.** Runtime никогда не читает
   `_cowork_output/`.
5. **Ничего не удаляем — архивируем** с пометкой дата+почему. История решений ценна.

## 2. authored/ vs derived/

| | `authored/` | `derived/` |
|---|---|---|
| Кто пишет | люди (PR + review) | prograph и др. инструменты (авто) |
| Можно править руками | да | **нет** (перезапишется) |
| Примеры | rules, decisions (ADR), templates, notes, registry | graph, снапшоты контрактов, projects-факты, digests |
| Git-review | обязателен | коммит инструментом, review опционален |

**Инструментам:** prograph пишет **только** в `derived/`. Запись в `authored/` из автоматики
запрещена (граница директорий — жёсткая).

## 3. Карта директорий (что где)

```
authored/
  rules/        cross-cutting: code-style.md, gui.md, tui.md, libraries.md
  decisions/    ADR (cross-repo), YYYY-MM-DD-<kebab>.md
  templates/    spec-шаблоны, steward-профили (lite/team), scaffolds
  skills/       project-specific скилы: исходники/доки ИЛИ указатели на Cowork skills
  notes/        планы, намерения, cross-cutting TODO
  registry/     COWORK_CONTEXT (реестр + карта интеграций)
derived/
  graph/        вывод prograph (структура, deps, MCP-вызовы)
  contracts/    СНАПШОТЫ контрактов для поиска (не авторитет)
  projects/     авто-факты по репам (prograph)
  digests/      claude-kb/digests (авто)
```

## 4. SSOT-границы (против дублей)

| Знание | Владелец (SSOT) | Роль KB |
|---|---|---|
| Inter-repo контракт | репо-производитель | `derived/contracts/` — снапшот/индекс, НЕ авторитет |
| Repo-local правила | CLAUDE.md репы | нет; репа ссылается на `authored/rules/` |
| Cross-cutting правила | **KB `authored/rules/`** | владеет |
| История кода | git репы | нет; `authored/decisions/` = cross-repo *почему* |
| Реестр проектов | **KB `authored/registry/`** | владеет; корень — указатель |
| Runtime-скилы | механизм Cowork skills | `authored/skills/` — исходники/указатели |
| Структура/дрейф | prograph (авто) | `derived/graph/` |
| Транзитные черновики | `_cowork_output/` | канон graduated сюда |

Правило-мнемоника: **если этим владеет конкретная репа — KB только ссылается. KB владеет лишь тем,
что не принадлежит ни одной репе.**

## 5. Naming

- Датированные: `YYYY-MM-DD-<kebab>.md` (ADR, заметки, статусы).
- Тематические стабильные: `<kebab>.md` (rules, templates).
- ADR: `authored/decisions/YYYY-MM-DD-adr-<slug>.md`.

## 6. Lifecycle

- **Состояния ADR/доков:** `Proposed → Accepted → Superseded | Archived`. Superseded/Archived —
  ссылка на заменяющий + причина.
- **Архивация:** устаревшее → `authored/**/archive/` с YAML-пометкой `archived: YYYY-MM-DD` +
  `reason:`. Не удалять.
- **Graduation:** черновик в `_cowork_output/` → став каноном, переезжает в KB под git-review.
- **Freshness:** `registry/` и `derived/` ре-аудитятся по расписанию (курационный скил, Stage 2).

## 7. Frontmatter документа (минимум)

```yaml
---
title: <короткий>
type: rule | adr | template | note | contract-snapshot | registry
status: proposed | accepted | superseded | archived | living   # для authored
owner: <кто ведёт>            # для authored
source: <derived-инструмент>  # для derived
updated: YYYY-MM-DD
---
```

## 8. Как добавить

- **Правило (cross-cutting):** `authored/rules/<topic>.md`, `type: rule`, PR + review. Если правило
  repo-local — оно идёт в CLAUDE.md репы, не сюда.
- **ADR:** `authored/decisions/YYYY-MM-DD-adr-<slug>.md`, `status: proposed`.
- **Шаблон/профиль:** `authored/templates/`. steward-профили `lite`/`team` — здесь (SSOT профилей).
- **Контракт:** авторитет — в репе-производителе; сюда — снапшот в `derived/contracts/` (инструментом).

## 9. Инструменты и агенты

- **Поиск:** Obsidian-MCP над vault (KB — Obsidian-совместим).
- **Пополнение `derived/`:** prograph.
- **Курация (Stage 2):** скил архивации/freshness/link-fix (паттерн `consolidate-memory`).
- **Энфорс (Stage 3):** правила `authored/rules/` → CI-проверки (à la `gate-check`); дрейф →
  prograph → dispatcher → авто-PR.

## 10. Связи

- **steward** — потребитель `authored/templates/` (профили гейтов) и `authored/rules/`.
- **prograph** — писатель `derived/`.
- **dispatcher** — читатель для панелей состояния.
- **COWORK_CONTEXT** — переезжает в `authored/registry/`; в корне остаётся указатель.
