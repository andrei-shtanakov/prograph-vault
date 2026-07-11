# Anti-pattern checklist: «agent theater»

> Правило экосистемы (contracts roadmap, RD-000). Источник: Часть VIII
> `authored/notes/2026-07-11-ai-dark-factory-consolidated-roadmap.md`.
> Применять на ревью любого дизайна многоагентной системы/фичи — своего или
> заимствованного (пример разбора внешнего: OpenOPC, org-theater как
> анти-паттерн при инженерно ценном workflow-слое).

Система скатилась в дорогой театр агентов, если наблюдается хотя бы
несколько из признаков:

- [ ] много ролей, но мало проверяемых gates;
- [ ] агенты общаются без artifact contracts;
- [ ] нет acceptance criteria на каждый шаг;
- [ ] нет evidence trail;
- [ ] verification слабее generation;
- [ ] роли названы как должности, но без authority boundary;
- [ ] много «совещаний агентов», мало результатов;
- [ ] нет cost accounting и stop conditions;
- [ ] learning loop не обновляет evals/policies/playbooks (только копит заметки).

## Как применять

1. На дизайн-ревью: пройтись по списку; ≥3 отметок — дизайн возвращается
   с требованием контрактов/gates, а не новых ролей.
2. При заимствовании чужих паттернов: брать workflow-слой (transition
   tables, gates, adapter registries, fail-closed verdicts), НЕ брать
   оргметафору (оргчарты, митинги, prose-«должности»).
3. Позитивная формулировка того же правила: главный объект — управляемый
   контур `Goal → WorkItem → … → Verify → Evidence → Decide → Learn`;
   роли — только runtime-функции (capability, authority, verification),
   не HR-должности.

## Связанное

- Consolidated contracts roadmap: `authored/notes/2026-07-11-ai-dark-factory-consolidated-roadmap.md`
- Границы применения verification-first: «dark» (человек вне петли ревью)
  допустим только там, где verification доказуемо сильнее generation.
