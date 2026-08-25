---
title: devtools — activity journal
type: journal
source: kb-save
project: devtools
updated: 2026-08-18
---

# devtools — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.

## 2026-08-17 16:05 — change: резолв состояния issue-блокеров `<repo>#<number>` (обратное плечо ADR-ECO-006)

- Принят inbox-issue devtools#40 от prograph-vault (правило cross-repo-waits, там PR #72) под запрошенным слагом `blocker-issue-state-resolution`; реализация — devtools PR #41 (CI зелёный, ревью-замечание Copilot закрыто).
- `check-plan-fields.py` теперь резолвит issue-форму блокеров через `gh`: закрытый/вмерженный target у открытого пункта → ERROR класса PF-BLOCKER-STALE (stale = всё, что не OPEN — gh резолвит и PR-номера, state MERGED); недоступный резолв → явный [DT-ISSUE-STATE-UNAVAILABLE], не clean; issue-рефы изъяты из legacy slug-графа и PF-LEGACY-AMBIGUOUS-шума.
- Links: devtools/check-plan-fields.py, devtools/tests/test_issue_blockers.py, devtools/TODO.md (@id:blocker-issue-state-resolution), devtools#40, devtools PR #41

## 2026-08-18 00:20 — change: SSOT conformance-фикстуры каталога — единый owner-путь (devtools#43, PP-103 (b))

- Принят inbox-issue devtools#43 от impresario (PP-103 acceptance (b)) под запрошенным слагом `catalog-conformance-single-owner`: devtools — единый owner-путь conformance трёх загрузчиков каталога (Maestro / ATP / arbiter), последняя миля ADR-ECO-003b (риск №1: дивергенция загрузчиков → общий conformance-тест на фикстурах).
- Опубликован набор `contracts/catalog-conformance-fixtures/v1/` (PR #44, merge 2a5c154): фикстуры valid / invalid V1–V5 / warn V6–V7 / parse-error (словарь правил — arbiter catalog-loader design §4; V2+V3 зеркалят Check 5 `check-agent-id-conformance.py`), `expectations.toml` с классами `valid|parse-error|error|flag` + pathres-сценарии слоя `$ATP_CATALOG` (ADR-ECO-003b D2, XDG вне v1), `manifest.json` (sha256 + tree_sha256 — пин-поверхность copy-integrity), README с зафиксированными дивергенциями загрузчиков на 2026-08-17 (Maestro: молчаливый None при missing-file, нет V1–V5; ATP: нет V2/V3/V6, V7 жёсткий schema-fail — конформно классу flag; arbiter — эталон).
- Owner-QA: `check-catalog-fixtures.py` (stdlib референс-валидатор V1–V7, `--check`/`--write-manifest`, `make catalog-fixtures`) + tests/test_catalog_fixtures.py (невакуумность чекера доказана); ревью Copilot обоих PR отработано.
- Условие (2) — три сьюта зелёные на пиненом наборе — у потребителей: inbox-issues maestro#188 / atp-platform#292 / arbiter#74 (слаг `catalog-conformance-wiring`, пин 2a5c154); ожидание закреплено @blocked_by-тегами в TODO.md (PR #45, merge 3048c89). devtools#43 остаётся открыт до (2) — закрытие будет сигналом инициатору (ADR-ECO-006).
- Links: devtools/contracts/catalog-conformance-fixtures/v1/, devtools/check-catalog-fixtures.py, devtools/TODO.md (@id:catalog-conformance-single-owner), devtools#43, PR #44, PR #45, maestro#188, atp-platform#292, arbiter#74

## 2026-08-18 09:30 — result: catalog-conformance-single-owner закрыт — все три сьюта зелёные на пиненом наборе

- Условие (2) devtools#43 выполнено за сутки: maestro#188→PR #189, atp-platform#292→PR #293, arbiter#74→PR #75 (фолд в `@id:catalog-conformance-fixtures`) — все смержены с зелёным CI, PIN у всех на devtools@2a5c154, copy-integrity по manifest.json подтверждена на master.
- Набор оправдал себя при первом же подключении: в Rust-схеме arbiter нашлось реальное расхождение — обязательный `harnesses.*.shim` (вне словаря V1–V7) валил 7/10 кейсов parse-ошибкой; стал `Option<String>`. Arbiter дополнительно проверил негативные кейсы мутациями (отключение V1…V7 краснит ровно свой кейс).
- Обратное плечо ADR-ECO-006 отработало по задумке: закрытие трёх wiring-issues дало в devtools ровно 3×PF-BLOCKER-STALE («ожидание доставлено») — теги сняты, пункт [x] (PR #46), devtools#43 закрыт как сигнал инициатору (impresario, @blocked_by:devtools#43).
- Links: devtools#43, devtools PR #46, maestro PR #189, atp-platform PR #293, arbiter PR #75

## 2026-08-18 12:40 — change: catalog-conformance v1 — аддитивные кейсы по развилкам из maestro (devtools#47)

- Принят inbox devtools#47 (maestro, из wiring-разбора maestro#189) под слагом `catalog-conformance-v1-gaps`: два места, где v1 не выносил решения и загрузчики расходились молча.
- Канонизировано (README «Пограничные решения», PR #48 / merge 2533ff7): (1) пустая плоскость `[harnesses]` при непустых `[[agents]]` → V1 fail-closed — совпало с фактическим поведением ATP и arbiter, «третьего варианта» не оказалось, расхождение было ровно maestro-вским; пустая плоскость без агентов валидна; (2) V7 получил kind-only фикстуру — старая варьировала status+kind разом и pydantic-загрузчики проходили её схемой по status, не проверив kind.
- Maestro заранее заявил обе новые фикстуры у себя красными (scaffolding-чтение + намеренная невалидация kind) — рабочий режим набора, зафиксировано в README-дивергенциях.
- Приёмка потребителей — pin-bump issues maestro#192 / atp-platform#294 / arbiter#76 (пин 2533ff7), ожидание @blocked_by-тегами (PR #49). devtools#47 открыт до приёмки всех трёх.
- Links: devtools#47, devtools PR #48, PR #49, contracts/catalog-conformance-fixtures/v1/ (14 файлов), maestro#192, atp-platform#294, arbiter#76

## 2026-08-18 18:30 — result: vocabulary.toml + закрыты devtools#47 и #51 — conformance-контур каталога сомкнулся

- devtools#51 (maestro): vocabulary.toml — машиночитаемый словарь enum'ов ADR-ECO-003 в наборе (PR #54, merge 070acdc); референс-валидатор читает его же (рантайм-копии в devtools нет), roundtrip-кейс делает выпавшее значение наблюдаемым (мутационный тест), version/типы валидируются up front. Manifest — 16 файлов. Закрытие issue = сигнал maestro сносить интерим HARNESS_KINDS/MODEL_STATUSES.
- devtools#47 закрыт целиком: все три потребителя приняли v1-gaps на пине 2533ff7 — arbiter#76→PR #77 (84114ef, конформен без правок), maestro#192→PR #193 (0285bcd, обе развилки ПОЧИНЕНЫ: пустая плоскость → V1 по model_fields_set; kind против интерим-константы), atp-platform#294→PR #295 (6509727, V7-kind → CatalogWarning).
- README-дивергенции: штампы из #50 сразу отработали — запись Maestro устарела за часы и обновлена (единственная оставшаяся дивергенция всего контура: maestro missing-file → молчаливый None, осознанная). Ревью Copilot PR #54: 3 валидных замечания (валидация vocabulary, 2 формулировки) закрыты в a66921b.
- Из одного inbox devtools#43 выросла цепочка: #43 → #47 → #50 + #51; все закрыты, план чист (0 err/0 warn), закрывающий тик — PR #55.
- Links: devtools#47, devtools#51, devtools PR #54, PR #55, vocabulary.toml, maestro PR #193, atp-platform PR #295, arbiter PR #77

## 2026-08-18 21:40 — change: три слепые зоны plan-check закрыты (devtools#56/#57/#58, PR #59)

- #56 (главный): квадрант «@id-источник × legacy `<repo>#<slug>` × закрытая цель» не проверял никто — пакетный legacy-граф пропускает @id-источники, канонический из legacy-формы ребра не строит. Фикс во враппере: check_id_source_legacy_stale (warning, stale-only, матчер слага переиспользован из пакета). Докстринг честен, cross-repo-waits не трогали.
- #57: check_tag_placement — DT-TAG-ON-CONTINUATION (строка-продолжение, начинающаяся с тега; упоминания в прозе не флагуются) + DT-TRIGGER-UNTERMINATED (разорванная кавычка @trigger). #58: issue_ref_exclusions по всем пунктам — тег-история на [x] больше не даёт ложный PF-LEGACY-AMBIGUOUS.
- Детекторы окупились до мержа: 2 протухших ожидания maestro (arbiter#R-07 давно завершён) и 5 невидимых @id (disputatio ×3, kapelle ×2); находки доставлены — maestro#196, disputatio#21, kapelle#29 (в disputatio/kapelle создан лейбл inbox). Ревью Copilot PR #59 — без замечаний.
- Флот сейчас: 1 канонический ERROR (maestro ждёт доставленный vocabulary — их сигнал) + 7 честных warnings у соседей; ложные warnings impresario ушли. Тик закрытия — PR #60.
- Links: devtools#56, devtools#57, devtools#58, devtools PR #59, PR #60, check-plan-fields.py, tests/test_plan_check_detectors.py, maestro#196, disputatio#21, kapelle#29
