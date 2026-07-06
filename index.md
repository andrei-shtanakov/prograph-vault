---
title: Ecosystem KB — index
type: registry
status: living
owner: Andrei
updated: 2026-07-05
---

# Ecosystem KB

Единая база знаний экосистемы AI-оркестраторов. Правила ведения — `CLAUDE.md`.

## Навигация

**authored/** — владеют люди (git-review):
- [rules/](authored/rules/) — cross-cutting правила: code-style, gui, tui, libraries
- [decisions/](authored/decisions/) — ADR (cross-repo)
- [templates/](authored/templates/) — spec-шаблоны, steward-профили, scaffolds
- [skills/](authored/skills/) — project-specific скилы / указатели
- [notes/](authored/notes/) — планы, намерения, cross-cutting TODO
- [registry/](authored/registry/) — реестр проектов (COWORK_CONTEXT)

**derived/** — пишут инструменты (руками не трогать):
- [graph/](derived/graph/) — структура/зависимости (prograph)
- [contracts/](derived/contracts/) — снапшоты контрактов (не авторитет)
- [projects/](derived/projects/) — авто-факты по репам
- [digests/](derived/digests/) — дайджесты

## Быстрые правила

1. authored пишут люди, derived — инструменты. Не смешивать.
2. KB ссылается на контракты, не владеет ими.
3. Repo-local правила — в CLAUDE.md репы; KB — только cross-cutting.
4. Ничего не удаляем — архивируем с датой+причиной.

## Статус миграции

- [ ] `git init`, скелет authored/derived
- [ ] Перенос из `_cowork_output/` (decisions, roadmap, status, contracts-снапшоты)
- [ ] Реклассификация текущих contracts/projects/mcp_patterns → authored|derived
- [ ] COWORK_CONTEXT → `authored/registry/`, указатель в корне
- [ ] Регистрация KB в реестре
