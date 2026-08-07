---
title: "ADR-ECO-005a: typed operational owner principals"
type: adr
status: proposed
owner: Andrei
updated: 2026-08-07
---

# ADR-ECO-005a: typed operational owner principals

**Status:** Proposed (2026-08-07, Andrei) · **Date:** 2026-08-07
**Deciders:** Andrei (sole owner of the ecosystem today)
**Scope:** operational `TODO.md` ownership grammar, canonical plan-fields
projection, and fleet/digest reporting; governance `owner_role` remains DEC-007
**Type:** Amendment to
`authored/decisions/2026-07-27-adr-eco-005-plan-fields-two-plane-model.md`
(ADR-ECO-005)
**Related:** `authored/contracts/plan-fields/v1/`,
`ai-orchestrators-workspace/workspace-manifest.toml`,
`devtools/check-plan-fields.py`, `robin-runtime/src/robin/plan_state.py`

## Контекст

ADR-ECO-005 закрепил `@owner` операционного `TODO.md` как DEC-007 role-slug и
проецирует его в `OperationalNode.owner_role`. Живой флот использует поле иначе:
часть значений обозначает человека (`andrei`), часть — репозиторий, которому
принадлежит следующий шаг (`arbiter`, `atp`, `devtools`). Метрика «без владельца»
не может отличить человеческое назначение, владение репозиторием, осознанный TBD
и отсутствующую разметку.

DEC-007 governance-role и operational principal отвечают на разные вопросы.
Тихо расширить regex `owner_role` значениями `github:*`/`repo:*` означало бы
сломать уже принятую семантику steward.

## Решение

### Typed grammar

Канонический `@owner` в операционных планах обозначает accountable principal:

| Форма | Смысл | Reporting bucket |
|---|---|---|
| `github:<handle>` | конкретный GitHub-пользователь | `human-owned` |
| `github-team:<org>/<team>` | человеческая команда | `human-owned` |
| `repo:<manifest-key>` | репозиторий и его ownership-процесс | `repo-owned` |
| `TBD` | владелец осознанно не определён | `TBD` |
| тег отсутствует | назначение не заявлено | `missing` |

`repo:<manifest-key>` проверяется fleet-layer относительно frozen
`workspace-manifest.toml`; folder presence и origin URL не являются authority.

### Canonical projection and compatibility

В следующую schema revision `OperationalNode` получает nullable `owner_ref`:

```json
{
  "kind": "github_user | github_team | repository | tbd",
  "id": "andrei-shtanakov | org/team | dispatcher | null",
  "raw": "github:andrei-shtanakov"
}
```

`owner_role` остаётся переходным полем только для bare DEC-007 role-slug. Один
`@owner` порождает либо `owner_ref`, либо legacy `owner_role`, но не оба.
Governance-артефакты steward продолжают использовать самостоятельное
`owner_role`; это решение их контракт не меняет.

Переходные правила parser-а:

- typed form → `owner_ref`, `owner_role=null`;
- bare DEC-007 role-slug → `owner_role=<slug>`, `owner_ref=null`, диагностика
  `PF-OWNER-LEGACY-ROLE`;
- tag absent → оба `null`, `PF-OWNER-MISSING`;
- invalid value → оба `null`, `PF-OWNER-GRAMMAR`, raw value сохраняется;
- неизвестный manifest key для `repo:` → fleet-диагностика
  `PF-OWNER-REPO-UNKNOWN`.

`TBD` валиден и не считается missing. Его age/escalation policy не входит в
этот amendment.

### Reporting has two independent axes

Ownership axis:

- `human-owned`;
- `repo-owned`;
- `TBD`;
- `missing`;
- `invalid-owner`;
- `unknown-repo-owner`.

Movement axis:

- `actionable`;
- `waiting-by-trigger`;
- `waiting-by-blocker`;
- `stale-condition`;
- `malformed-condition`.

`waiting-by-trigger` не является видом owner и не вытесняет ownership bucket.
Отчёт обязан публиковать обе суммы и матрицу ownership × movement. Реальные
бесхозные висяки — прежде всего `missing + actionable`; stale blocker требует
реакции независимо от owner.

## Миграция

После доставки нового parser/reporting известные значения мигрируют так:

| Старое | Каноническое |
|---|---|
| `andrei` | `github:andrei-shtanakov` |
| `arbiter` | `repo:arbiter` |
| `atp` | `repo:atp-platform` |
| `devtools` | `repo:devtools` |

Пустые owner-поля не заполняются массово личным handle. Их triage начинается
после появления раздельного отчёта и сохраняет `missing`, когда назначение
действительно неизвестно.

## Rollout

1. Обновить authority plan-fields: schema/diagnostics/fixtures/manifest.
2. Ре-вендорить контракт и реализовать parser/fleet API в `dispatcher`.
3. Поднять immutable pin в `devtools`, удалить локальный `STRICT_OWNER`, добавить
   ownership/movement totals и матрицу.
4. Поднять pin и reporting в `robin-runtime`, не создавая собственной grammar.
5. Только затем провести малые migration PR по планам флота.

## Приёмка

- typed forms дают стабильный `owner_ref`;
- неизвестный `repo:` не считается валидным `repo-owned`;
- `TBD` отличим от missing;
- trigger/blocker не меняет owner-классификацию;
- сумма ячеек матрицы равна числу открытых пунктов;
- devtools и Robin дают одинаковые totals на общей фикстуре;
- runtime-потребители используют пинованный контракт и никогда не читают
  `_cowork_output/`.

## Последствия

- Действующая формулировка ADR-ECO-005 «operational `@owner` is settled as one
  role-slug» superseded этим amendment для `TODO.md`.
- DEC-007 остаётся каноном governance `owner_role`.
- Schema revision и consumer pins изменяются явно; старое поле не получает
  новую семантику молча.
