---
title: authored/ — guardrail
type: rule
status: living
owner: Andrei
updated: 2026-07-05
---

# authored/ — пишут ЛЮДИ

Всё здесь редактируется людьми через **git-review (PR)**. Инструментам запись сюда **запрещена**
(prograph и авто-скилы пишут в `../derived/`).

## Подпапки

| Папка | Что держит | SSOT? |
|---|---|---|
| `rules/` | cross-cutting правила: `code-style.md`, `gui.md`, `tui.md`, `libraries.md` | ✅ KB владеет |
| `decisions/` | ADR (cross-repo), `YYYY-MM-DD-adr-<slug>.md` | ✅ cross-repo *почему* |
| `templates/` | spec-шаблоны, steward-профили (`lite`/`team`), scaffolds | ✅ SSOT профилей |
| `skills/` | project-specific скилы: исходники/доки ИЛИ указатели на Cowork skills | ⚠️ runtime — у механизма skills |
| `notes/` | планы, намерения, cross-cutting TODO | ✅ (repo-local TODO — в репе) |
| `registry/` | COWORK_CONTEXT (реестр + карта интеграций) | ✅ KB владеет |

## Правила

- Repo-local правила сюда **не** кладём — они в CLAUDE.md соответствующей репы.
- Контракты сюда **не** кладём как авторитет — авторитет в репе-производителе; снапшот в `derived/`.
- Устаревшее → `<подпапка>/archive/` с `archived:`/`reason:` во frontmatter. Не удалять.
- Каждый файл — с frontmatter (`title/type/status/owner/updated`), см. `../CLAUDE.md` §7.
