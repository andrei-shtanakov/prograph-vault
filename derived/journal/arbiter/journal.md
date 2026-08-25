---
title: arbiter — activity journal
type: journal
source: kb-save
project: arbiter
updated: 2026-07-12
---

# arbiter — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.

## 2026-07-12 12:45 — decision: RD-006 Capability/Authority split design drafted (PR #49)

- docs/2026-07-12-authority-split-design.md: arbiter owns Capability decision +
  Authority enforcement contract; steward owns policy data (vendored pinned copy,
  agents-catalog pattern). role x phase allowlist (decompose|implement|review|
  benchmark x authoring|execution|merge|pr), wire = constraints.authority_context
  (kept out of the 22-dim vector), pipeline capability->authority->scoring,
  exact harness@model + harness@* only, all-denied = REJECT with
  authority_no_authorized_candidates + audit payload. Tools/escalation = v2.
- M1..M5 plan + contracts/capability promotion; OQ-1..3 open for owner review.
- Links: https://github.com/andrei-shtanakov/arbiter/pull/49

## 2026-07-12 13:06 — change: RD-006 M1 shipped as PR #50 (authority enforcement + both contracts)

- arbiter-core/src/authority.rs (pure engine, fail-closed), wire
  constraints.authority_context (excluded from feature vector), route_task
  step 3b (capability -> authority -> scoring), REJECT
  authority_no_authorized_candidates + audit at metadata.authority,
  load_authority with sha256 provenance + hot-reload, contracts/authority/ +
  contracts/capability/ with live-output tests, conformance script (+7 tests).
- Design refinement: retired-model check applies to exact pins only
  (wildcards covered by routable requirement; catalog CI owns live retired refs).
- 15/15 cargo targets, 107 pytest, clippy clean.
- Links: https://github.com/andrei-shtanakov/arbiter/pull/50

## 2026-07-12 14:38 — result: RD-006 M2..M5 complete; authority ACTIVE

- M1+review merged (#50/#51). M2 = steward #9 (profiles/authority.yaml SSOT).
  M4 = Maestro #74 (authority_context on every route call) — deliberately
  BEFORE M3: activating deny without the context would reject all routing.
  M3 = arbiter #52 (ACTIVE vendored config/authority.toml @ steward SSOT
  45eddb3d…, AUTHORITY_PINNED_SHA CI gate, live fail-closed e2e proof:
  context-less route_task = reject/authority_no_authorized_candidates).
- M5 = vault PR (this one): RD-006 evidence_rules -> board flips verified.

## 2026-08-16 20:03 — result: R-07 crossover-гейт закрыт; A/B-вью над benchmark_runs отгружен

- Crossover-гейт (@id:r-07-crossover-gate) закрыт анализом бенчмарка №2 (PR #69, merged `e17a3fa`):
  сигнал rank_score task-зависим (Δ 0.209 на code-review не переносится, ничья 1.0 на req-extraction),
  global bias не утекает; оговорка — суит №2 сатурирован, сильная форма crossover ненаблюдаема,
  контекст уехал в @id:r-07-link-strength-decision (теперь разблокирована).
- A/B-вью (@id:benchmark-ab-view) — подкоманда `ab` в scripts/check_routable_gate.py (PR #70,
  ревью в процессе): «агент A vs B на бенчмарке T» для человеческого гейта флипа routable;
  вью, не гейт. Все три arbiter-пункта ADR-ECO-003a выполнены (#32, #41, #70).
- Ограничение v1: benchmark_runs не хранит suite identity — вью предполагает один суит и печатает NOTE.
- Links: arbiter/docs/2026-08-16-r07-crossover-gate-analysis.md, arbiter/scripts/check_routable_gate.py,
  arbiter/tests/test_ab_view.py, arbiter/TODO.md

## 2026-08-17 21:49 — change: PP-103 last mile merged (ADR-ECO-003b closed out)

- PR #73 merged to master (`bd538d1`), issue #72 (inbox, from impresario) auto-closed.
  arbiter-mcp now validates agents.toml against the user-config catalog at startup
  ($ATP_CATALOG → XDG atp/): missing/retired refs (Check 5) → fail-loud exit 1;
  no catalog on machine → warn-and-start; bare ids ([aider]) outside SSOT → warning.
- Provider-swap smoke shipped: retire X + promote Y by catalog edit only
  (+ gen_agents_scaffold.py → apply → restart) flips route_task X → Y, consumer
  byte-identical. Both PP-103 observable acceptance conditions covered by tests
  over the real binary.
- Links: arbiter-mcp/src/catalog_guard.rs, orchestrator/tests/test_provider_swap_smoke.py,
  docs/2026-07-05-catalog-loader-design.md §1, TODO.md (slugs arbiter-mcp-catalog-loader,
  approved-pp-103-catalog-last-mile — both closed)

## 2026-08-22 12:11 — change: контракт report_benchmark-v1 — единица score и score_semantics

- PR #83 merged в master (`238fc8c`); inbox-issues #81 и #82 (обе from maestro) закрыты
  автоматически. Обе правки садятся на один путь чтения (`Database::get_benchmark_score`),
  поэтому сделаны одним PR.
- **#81, единица.** У `score` было два продюсера с разными величинами: atp-platform клал долю
  [0..1], maestro — ATP `total_score` в процентах [0..100]. Потребитель делал
  `.clamp(0.0, 1.0)`, поэтому любой прогон maestro выше 1% приезжал идеальной `1.0` и был
  неотличим от честного максимума. Канон — **доля [0..1]** (так лежат все существующие строки,
  так устроен `rank_score`, и это предполагает арифметика ре-ранка `(score - 0.5) * weight`).
  Валидация на ингесте → `-32602`; `minimum`/`maximum` в схеме; на чтении значение вне
  диапазона **игнорируется**, а не клампится. Нижний кламп сохранён: `rank_score` законно
  уходит чуть ниже нуля при нулевом pass rate.
- **#82, семантика.** Принят `score_semantics` (ATP score contract v1): хранится дословно
  (миграция схемы **v3**, nullable-колонка `benchmark_runs.score_semantics`), читается только
  `quality_signal`. Присутствующий блок, не являющийся `schema_version: 1` + `quality_signal:
  true`, записывается, но в тайбрейкер не идёт. **Отсутствие блока = legacy-продюсер и остаётся
  пригодным** — осознанное отклонение от буквы контракта: все существующие строки блока не имеют,
  и строгое чтение выключило бы R-07 целиком.
- **Изменение пути чтения:** `get_benchmark_score` идёт от новейшего прогона к старому и
  возвращает **первый пригодный**, а не фильтрует единственный новейший. Иначе не-качественный
  прогон маскировал бы качественный, и агент читался бы как «бенчмарка нет».
- **Найденная мина:** бамп `payload_version` **ломающий по построению** — сервер пинует
  `"1.0.0"` и отвергает прочее с `-32602`, поэтому продюсер, бампнувший версию ради *аддитивного*
  поля, получает отказ, пока обе стороны не переедут синхронно. Аддитивные изменения остаются на
  `1.0.0` и едут на `additionalProperties: true`. Записано в CLAUDE.md (правило 10) и AC-4.9.4.
- **Следствие для retention** (`@id:benchmark-runs-retention`, открыт): пригодный прогон может
  лежать за хвостом удержанных, поэтому политика обязана считать **пригодные прогоны**, а не строки —
  иначе N не-качественных прогонов вытеснят единственный качественный ровно как возрастной purge.
- Регресса нет: на копии реальной БД (21 строка) миграция чистая, A/B-дельта на `code-review`
  прежняя (`-0.076`). Ревью Copilot: 2 валидных замечания (лишний `Vec` вместо курсора;
  `PRAGMA table_info` на каждую строку) — исправлены в `ce191ef`.
- **Ожидание снято с maestro:** они могут смягчить свой fail-closed гейт с «не отправлять» до
  «отправлять с меткой» — сейчас они не шлют в arbiter ничего.
- Links: arbiter-mcp/src/db.rs (get_benchmark_score, semantics_permit_routing, routing_score_of,
  migrate v3), arbiter-mcp/src/tools/report_benchmark.rs,
  arbiter-mcp/tests/contract/report_benchmark-v1.schema.json, scripts/check_routable_gate.py,
  arbiter-spec.md §3.2/§3.3/§4.9, CLAUDE.md (правило 10), TODO.md
  (slugs benchmark-score-unit-mismatch, benchmark-score-semantics — оба закрыты)
