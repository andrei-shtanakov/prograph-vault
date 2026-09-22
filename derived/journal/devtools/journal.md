---
title: devtools — activity journal
type: journal
source: kb-save
project: devtools
updated: 2026-09-16
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

## 2026-08-27 20:48 — change: salvage-скан флота принят и реализован (devtools#67, PR #68)

- Принят inbox #67 (инициатор — ecosystem-kb, harvesting-волна №2; @id:fleet-salvage-scan). Новый сенсор salvage_scan.py + make salvage: детерминированный read-only скан набора манифеста по четырём классам обломков — orphan-worktree, branch-no-pr, unpushed-default, stale-lock. Таблица «репо · класс · объект · возраст» + host; пустой результат молчит (exit 0).
- WAIVERS (repo, класс, префикс объекта) помечают осознанные исключения [waived], не чинят и не скрывают; только waived → exit 0. Записаны ОБА лица исключения волта: unpushed master (снапшот-коммиты, ждёт dispatcher#199) и delivery-ветка derived-snapshots без PR by design (ecosystem-kb#98). Fail-honest: gh недоступен → «PR state unknown», не молчание.
- Живой прогон окупился сразу: orphan worktree research-bench (32d, /private/tmp/maestro-ws), 6 веток-кандидатов в disputatio/kapelle/maestro/research-bench. 23 синтетических теста, сети в тестах нет. devtools#67 закрыть после мержа PR #68.
- Links: devtools#67, devtools PR #68, salvage_scan.py, tests/test_salvage_scan.py, dispatcher#199, ecosystem-kb#98

## 2026-08-28 09:15 — change: догоняющая волна re-vendor промпта review-kit (devtools#69, PR-ы по 22 репо)

- Принят inbox #69 (инициатор — steward, @id:review-kit-prompt-lens-wave, встречное ожидание steward#130): волна 2026-08-27 разнесла кит @ e4c43cc ДО мержа steward#129; drift-вахта разъезд не видит — сверяет только 6 файлов PIN, промпт и caller-yml вне перечня по конструкции.
- Разнесено со steward @ ee6d85a побайтово: review-prompt.md (линза ослабления тестов в §4 — ослабление проверки без равноценной замены = минимум major; скоуп «охраняемое поведение остаётся в дереве»; line:0 для чистого удаления; утрата покрытия живого поведения в определении major) → 22 репо; codex-review.yml (довод steward#124 «потолок ≠ гарантия в аварию Actions», только комментарий) → 6 caller-репо. PIN/схема не тронуты — между e4c43cc и ee6d85a не менялись.
- 22 PR: deployer#46, atp-platform-testing#2, discovery-toolkit#9, discovery#26, disputatio#46, github-checker#28, impresario#41, libretto#33, proctor#57, prograph-vault#107, prograph#39, research-bench#28, robin-runtime#57, robin-toolkit#8, spec-runner-vscode#31, devtools#70 (+ приём в TODO.md), arbiter#95, atp-platform#310, dispatcher#212, kapelle#40, maestro#230, spec-runner#323.
- CI: у 6 caller-репо джобы review/report codex-review красные по среде — «You have no credits remaining» у OpenAI-аккаунта (не волна: yml-дельта — комментарий; review-kit-integrity везде зелёный). impresario governance/gate красный pre-existing с 2026-08-20 (pilot/briefs ссылаются на _cowork_output). Copilot-ревьюер через POST requested_reviewers молча не регистрируется ни в одном репо (то же на до-волновых PR).
- Закрыть пункт и devtools#69 после посадки волны на default-ветки (признак — байт-совпадение копий со steward HEAD, prompt sha256 27792de2…eba98).
- Links: devtools#69, devtools PR #70, steward#129, steward#130, TODO.md (@id:review-kit-prompt-lens-wave)

## 2026-08-28 09:55 — result: волна review-kit-prompt-lens-wave посажена, devtools#69 закрыт

- Все 22 PR вмержены пользователем 2026-08-28. Сверка по origin/<default>: prompt 22/22 и caller-yml 6/6 байт-совпадают со steward HEAD (ee6d85a, на момент сверки не уехал). Ветки волны удалены на origin; локальные клоны обновлены ff-only (prograph-vault master — waived-расхождение, не тронуто; arbiter — fetch only, оставлен на рабочей ветке).
- devtools#69 закрыт completed (сигнал steward#130 → PF-BLOCKER-STALE у них). Закрытие пункта TODO — PR devtools#71 (ждёт мержа).
- Links: devtools#69, devtools PR #70, PR #71, steward#129, steward#130

## 2026-08-28 — result: review-pr.sh дедуп влит + боевое крещение (devtools#72, PR #73)

- Принят inbox devtools#72 (steward, кит-половина steward#132): наследование вердикта по отпечатку входа — контракт из 7 пунктов реализован целиком во враппере review-pr.sh (feature-detect fp-режима по литералу; явный pre-fetch базы; строгий stdout-контракт; fp-маркер; наследование только из новейшего полностью распарсенного ревью ai-prosto; --fresh). 34 теста (jq-фильтр через настоящий jq).
- Боевое крещение по-настоящему: инструмент отревьюировал СВОЙ PR — два прогона дали request-changes с реальными дырами (fetch без destination-refspec; same-head-наследование без финальной сверки головы → exit 0 для неревьюенного head), обе закрыты с регрессионными тестами до мержа; третий прогон — approve, опубликован от ai-prosto с fp-маркером (первый наследуемый вердикт флота). review-pr.sh официально заменяет Copilot review и codex-review CI в приёмке devtools.
- Закрытие пункта дало мгновенный PF-BLOCKER-STALE у steward (todo://-ребро) — их сигнал на фазу замера экономии. Инцидент дня: до мержа я удалил ветку открытого PR #73 ритуалом чистки без гейта «PR merged?» (GitHub закрыл PR) — восстановлено за минуту (ветка из уцелевшего коммита + reopen), ритуал теперь начинается с проверки состояния.
- Links: devtools#72, devtools PR #73 (merge 6d3604f), PR #74 (тик), review-pr.sh, tests/test_review_pr.py, steward#126/PR #132

## 2026-08-28 — change: кэш дедупа review-pr.sh ожил (devtools#75, PR #76)

- Дефект интеграции #72, найден первой живой проверкой steward (их PR #134): gh 2.83.1 отвергает --slurp+--jq → поиск наследуемого вердикта падал всегда, кэш мёртв при верном fail-open. Синтетика не ловила — стаб gh игнорировал флаги.
- Фикс: фильтр внешним jq (jq -rs, тот же shape страниц); gh и jq раздельно — отказ каждого со своей причиной, мёртвый кэш не маскируется под «нет ревью»; стаб gh теперь сам отвергает --slurp (регресс красит сьют). Счётчик «N промахов подряд» отклонён: stateless by design.
- Живая проверка лукапа: steward#134 → APPROVED+head+fp извлечены; devtools#73 (маркер без fp от старого кита) → законный miss. devtools#75 открыт до полного живого инцидента наследования (первый открытый PR репо с fp-китом).
- Links: devtools#75, devtools PR #76 (merge 87b7e76), review-pr.sh, tests/test_review_pr.py, steward#134

## 2026-08-28 — result: дедуп-контур review-pr.sh закрыт целиком — живой инцидент наследования состоялся

- steward#135 стал тест-носителем: полный прогон опубликовал approve с fp-маркером, повторный dry-run на неизменном head → «вердикт унаследован» за 10.3 сек без вызова codex (против минут полного прогона). Критерий «сделано» devtools#75 выполнен дословно, issue закрыт, пункт [x] (тик — PR #77, отревьюирован самим инструментом: approve от ai-prosto).
- Цепочка devtools#72 → #75 полностью в бою: контракт наследования, живое крещение с двумя само-находками, оживший кэш после slurp-фикса, подтверждённая экономия. Закрытие пункта дало очередной PF-BLOCKER-STALE у steward — их сигнал на замер.
- Links: devtools#75, devtools PR #76, PR #77, steward#135

## 2026-08-30 11:59 — change: fleet issue console (PR-1) доставлен PR #85

- Спека + план + реализация: TUI (curses/stdlib) открытых issues флота — фильтр до локальных клонов по owner/repo-slug, acceptance-enum через plan-fields, эвристика типов + опция --classify-ai (codex, кэш, порог 0.75), группировка date/repo/author, запуск izolированных tmux-worker-ов (policy-гейт internal→accept/external→reject до Codex, без publish-фаз). 233 теста зелёные.
- Процесс: subagent-driven (9 задач + финальное ревью + фикс-волна); приёмка терминальным codex-ревью — 2 major-находки (усечение gh search 1000, подмена форком по короткому имени) исправлены фикс-коммитами; approve опубликован ai-prosto через verdict-handoff (devtools#80 контур, без второго вызова codex).
- Решение владельца (для конституции, отдельный таск): курс DarkFactory — авто-мерж агентом по умолчанию, human-merge как opt-in; экосистемный конфиг — пререквизит подпроекта issue-runner.
- Links: PR #85; docs/superpowers/specs/2026-08-30-fleet-issue-console-design.md; docs/superpowers/plans/2026-08-30-fleet-issue-console.md

## 2026-08-30 16:07 — change: behaviour governance core (этап A) влит PR #87

- Ядро конвейера behaviour-spec: пин steward@4a1c7c4 (uv-группа governance) с characterization-тестами трёх публичных символов (открытия: profile-ключ artifacts, roles version/slug_pattern, DSL тела, SpecGraph.nodes=dict+topo_order); fail-closed merge_gate по осям ADR-ECO-011; prospective stale-адаптер; bundle_state (blocked/delegated/required_absent/GC-UNPINNED — тишина гейтов не читается как зелёное). 284 теста, CI-шаг группы.
- Первый живой прогон DarkFactory-мержа: approve ai-prosto опубликован, PUT /merge от ai-prosto → 405 (write-прав нет) → передано человеку по fail-closed. Пререквизит владельца прежний: права ai-prosto.
- Этап B (runner S0–S8 + textual-консоль) — @id:behaviour-runner, blocked_by этап A; план после мержа A (условие наступило).
- Links: PR #87; docs/superpowers/specs/2026-08-30-behaviour-spec-pipeline-design.md; docs/superpowers/plans/2026-08-30-behaviour-governance-core.md

## 2026-08-30 20:19 — result: behaviour runner core (B1) влит PR #88 — ПЕРВЫЙ агентский мерж DarkFactory

- Runner S0–S8 конвейера behaviour-spec: policy-оси из вендоренной steward-политики (fail-closed вплоть до пустого PIN и path-traversal run_id), write-ahead журнал с reconciliation всех внешних эффектов (PR/issue/комментарии не дублируются после kill), merged_unverified навсегда + verification-потомок, WS-lock, CLI + make behaviour-run. 380 тестов.
- Приёмка: 8 раундов codex-ревью (final review SDD дал 2 Critical+6 Important; codex добил ещё 8 major по окнам падения/staleness/traversal — все исправлены фикс-коммитами) → «minor only» → approve ai-prosto через verdict-handoff.
- ВЕХА: PR #88 смержен агентом — merged_by=ai-prosto, PUT с sha, mergeStateStatus CLEAN после переработки рулсета (update-правило снято, PR-only + 1 approve сохранены). ADR-ECO-011 работает вживую end-to-end.
- S7 самого runner'а пока waiting_human_merge по данным (agent_merge_allowed=false, ai-prosto не в agent_identities steward) — включение = решение steward + pin-bump.
- Links: PR #88; план docs/superpowers/plans/2026-08-30-behaviour-runner-core.md

## 2026-08-30 23:08 — result: behaviour console (B2) влит PR #89 — второй агентский мерж

- Textual-консоль поверх runner'а (read-only view-model, plain/--json без textual и без группы), verify с сериализацией по состоянию потомков, disp-бэкенд opt-in (факт: --mode document из спеки у disp нет — @id:disp-document-mode-issue), follow-ups B1. 432 теста.
- Приёмка: финал SDD дал 2 Critical + 5 Important (README описывал другую программу; verify инвертировал parent/child), codex — ещё 5 major за 7 раундов (вечная tmux-сессия глушила resume; дубль remediation-issue; цикло-скоупный slug; TOCTOU verify; трупы резервов). Все закрыты; merged_by=ai-prosto, CLEAN.
- Пункт @id:behaviour-runner закрыт (B1 #88 + B2 #89). Конвейер behaviour-spec доставлен целиком: осталась включаемость S7 (steward identities + флаг + pin-bump) и живой смоук.
- Links: PR #89; план docs/superpowers/plans/2026-08-30-behaviour-console.md

## 2026-08-31 — change: хвосты behaviour-конвейера — steward-issues и волна rulesets

- Заведены inbox-issues (ADR-ECO-006): steward#139 agent-identities-ai-prosto,
  steward#140 gate-check-candidate-mode, steward#141
  review-kit-file-missing-finding-type; disputatio#52 single-document-polish-mode.
  Ожидания закреплены @blocked_by-чекбоксами в TODO.md (PR #90, agent-merge
  ai-prosto, merge 82dd91e).
- Волна rulesets по флоту: во всех 21 репо манифеста переработан рулсет
  «Default Branch Restriction» по эталону devtools — убрано голое `update`,
  выключены require_code_owner_review и
  require_extra_approval_for_unattributed_changes, required_approving_review_count=1
  (в spec-runner-vscode был 0 — ужесточение), bypass admin(5)+Integrations
  сохранён. ai-prosto: write подтверждён в 20 репо; в robin-runtime pending-инвайт
  от 2026-08-22 истёк — выдан заново и принят от ai-prosto, теперь write.
- Links: devtools TODO.md (@id:behaviour-s7-actor-policy-pin-bump и соседние),
  ADR-ECO-011.

## 2026-08-31 — result: живой смоук behaviour-конвейера — S0–S7 целиком, waiting_human_merge по authority-root

- Прогон WS-SMOKE-001-a1 (target — смоук-клон devtools): codex-авторинг дал
  DSL-корректный бандл, prospective-гейт S4 зелёный с первого раза
  (error_count=0, required_absent=[]), PR devtools#91, терминальное ревью
  --approve от ai-prosto, S7 → waiting_human_merge (reason: дифф затрагивает
  authority-root пути — profiles/). Терминальный статус ровно по спеке.
- Профиль — урезанный team-exp @ steward 4a1c7c44 (только узлы, которые
  авторит runner + delegate tasks), закоммичен на ветке спеки; master не
  тронут. Попутно: создан лейбл codex-review в devtools (S5b падал без него).
- Links: devtools PR #91, out/governance-runs/WS-SMOKE-001-a1/,
  docs/superpowers/specs/2026-08-30-behaviour-spec-pipeline-design.md

## 2026-08-31 — result: смоук behaviour-конвейера закрыт полным циклом, включая remediation и verify

- PR #91 (бандл + team-exp) смержен владельцем; resume зафиксировал мерж и
  прогнал S8 — config error exit=2 (нет profiles/gate-catalog.yaml) →
  merged_unverified + auto remediation-issue devtools#92: аварийная ветка
  спеки отработала вживую. Причина: S4 (content-check API) каталог гейтов не
  грузит, полный CLI gate-check S8 — грузит.
- Ремедиация: PR #93 — пинованные gate-catalog.yaml + risk-model.yaml
  (@ steward 4a1c7c44), authority-root → мерж человеком (f53914a).
  Verification-run WS-SMOKE-001-a1-v1: gate-authoritative exit=0, completed;
  devtools#92 закрыт с evidence. Консоль показывает пару
  merged_unverified→completed(v1) корректно.
- Links: devtools PR #91/#93, devtools#92, out/governance-runs/

## 2026-08-31 — change: развитие конвейера 1→2→3 — вход из issues, установка во флот, мост к spec-runner

- Перепин actor-policy @ steward 6a70d15 (PR #94, мерж человеком): steward#142
  доставил все три заявки (#139/#140/#141) и включил agent_merge_allowed —
  Safety(True, agent), S7 мержит document-PR сам. Теги ожиданий S4/S6 сняты,
  пункты actionable. PF-BLOCKER-STALE подтверждён живым прогоном чекера.
- Шаг 1 (PR #95, agent-merge): клавиша `b` в issue-console — мост
  «issue → behaviour-run»: subject из заголовка + repo#N, ws-id WS-<repo>-<N>,
  target — локальный клон; только internal-инициатор.
- Шаг 3 (PR #96, agent-merge, две major-находки приёмки исправлены):
  governance/task_bridge.py — draft tasks.md-спека из вмерженного бандла
  PR-ом в репо-владелец (make behaviour-tasks --run-id; CLI требует
  completed; чтение бандла после чекаута базы; approve — человек).
- Шаг 2: волна profiles/ (team-exp урезанный + roles + gate-catalog +
  risk-model @ 4a1c7c44) + лейбл codex-review по флоту — 20 PR, мерж
  человеком (authority-root): spec-runner#326 atp-platform#314 maestro#233
  arbiter#100 dispatcher#222 proctor#61 deployer#49 prograph#42
  robin-runtime#60 github-checker#31 libretto#36 disputatio#55
  research-bench#31 impresario#46 discovery#29 discovery-toolkit#12
  prograph-vault#116 robin-toolkit#11 spec-runner-vscode#34 kapelle#44;
  steward пропущен (профили родные). Последние 8 — через git trees API без
  клонов (SSH-клоны упирались в 10-мин потолок фоновых команд).
- Links: devtools PR #94/#95/#96, governance/task_bridge.py, issue_console.py

## 2026-08-31 — status: волна профилей села — 19/20 смержено владельцем, флот готов к конвейеру

- Владелец смержил 19 PR волны profiles/; открыт остался disputatio#55.
  Влитые ветки chore/behaviour-profiles удалены на origin (11 руками, 9
  удалил GitHub), локальные чекауты флота обновлены ff-only до мержей.
- Гигиена: снята россыпь stale index.lock (0 байт, 29.08 16:02, упавшая
  сессия) в 12 репо; подвисшие ssh git-upload-pack процессы убиты — fetch
  переключён разово на HTTPS (ssh к GitHub сегодня виснет).
- Конвейер теперь запускаем в любом репо флота, кроме disputatio (ждёт #55).

## 2026-08-31 — change: цикл kapelle замкнут (PR #53 draft-спека) + фиксы боевых находок (devtools#99)

- task_bridge сгенерировал draft tasks.md-спеку из бандла WS-kapelle-47 —
  kapelle#53 (19 задач с провенансом #BEH-NN; исполнение после approve
  человека). Первый полный цикл «issue → бандл → мерж → спека задач».
- devtools#99 (agent-merge): DSL-промпт авторинга (имена 00-/10-/15-,
  FR/BEH/traces/checked_by/upstream_hashes), гард GC-DSL-EMPTY в S4,
  reconciliation refuse→merged. Четвёртый фикс (поблажка UNSTABLE) ОТКАЧЕН
  приёмкой: в rulesets флота нет required-чеков, UNSTABLE = «упало что
  угодно» — поблажка мержила бы красный test; мотивация умерла со снятием
  codex-review. Закреплено fail-closed характеризацией.

## 2026-09-01 — result: цикл WS-kapelle-47 закрыт целиком — от issue до кода на master

- kapelle#59 (TASK-004, финальный) — approve без находок, agent-merge с полным
  ожиданием чеков; master a56af35, 502 tests, 0 failures, все 4 задачи DONE.
- Полный путь прожит впервые: issue kapelle#47 → мост b → behaviour-бандл
  (8 FR + 19 BEH) через PR → draft tasks-спека (task_bridge, ужатие по
  Feature) → approve владельца → spec-runner (4 задачи TDD) → 4 integration-PR
  через терминальное ревью (2 блокера и 1 major пойманы и закрыты по ходу) →
  agent-мержи. Проверка PROVENANCE-целостности golden-фикстур живёт в mix test.
- Links: kapelle#47 (закрыть), PR #51/#53/#56–#59, todo://kapelle/golden-provenance-self-integrity

## 2026-09-01 — change: required-чек test в rulesets (волна по следам инцидента kapelle#57)

- В 11 репо в ruleset «Default Branch Restriction» добавлено правило
  required_status_checks (integration_id=15368, strict=false): ровно `test` —
  devtools, steward, robin-runtime, research-bench, discovery,
  spec-runner-vscode, kapelle; матричные — один якорь `test (3.12)` —
  spec-runner, atp-platform, maestro, dispatcher (вся матрица в required
  замуровала бы репо при смене версий).
- Пропущены с докладом владельцу: без CI-чеков — deployer, prograph,
  github-checker, impresario, discovery-toolkit, disputatio, prograph-vault,
  robin-toolkit; другие имена тест-джобов — arbiter (Rust (stable)?),
  proctor (Unit (py3.12)?), libretto (tools (pytest + ruff + pyrefly)?) —
  выбор контекста за владельцем.
- Теперь мерж поверх красного/недоехавшего test блокирует сам GitHub
  (bypass — только admin), а не дисциплина агента.

## 2026-09-01 — change: волна CI на 6 репо без тестового CI + required-чеки до 18/22

- ci.yml (job test: uv sync --frozen + pytest, пины SHA, permissions
  contents:read — валидная находка Copilot, отработана во всех ветках)
  заведён в deployer/prograph/github-checker/impresario/discovery-toolkit/
  disputatio. API-путь упёрся в отсутствие workflow-скоупа у gh-токена —
  ушли на клоны + ssh-push. 4 PR смержены владельцем (deployer#56,
  discovery-toolkit#15, disputatio#63, impresario#49), master-прогоны
  зелёные, required-чек test поставлен. Плюс arbiter/proctor/libretto —
  required с их именами джобов (Rust (stable) / Unit (py3.12) / tools
  (pytest + ruff + pyrefly)). Итого required-чеки в 18 репо.
- Первый же CI-прогон нашёл два скрытых дефекта тестов: prograph#45
  (перенос строки режет tracked.toml на длинных CI-путях) и
  github-checker#35 (фикстура полагается на git-окружение раннера) —
  inbox-issues заведены; их PR (prograph#44, github-checker#34) ждут
  починки, required-чек туда — после зелёного.
- Вне контура осознанно: prograph-vault, robin-toolkit (нет кода/тестов).

## 2026-09-01 — status: kapelle#47 закрыт во всех плоскостях; required-чеки 19/22

- Issue kapelle#47 закрыт с evidence (4 критерия + путь PR #51—#59); пункт
  @id:golden-provenance-self-integrity отмечен [x] PR-ом kapelle#60
  (замечание Copilot про перегруженный чекбокс отработано — evidence
  строками-продолжениями; agent-merge с required-чеком test, который kapelle
  проверил уже сам). prograph починил перенос путей (4e3163f) — CI зелёный,
  required поставлен, prograph#45 закрыт. Осталось: github-checker#35
  (сьют красный, required ждёт), vault/robin-toolkit — вне контура осознанно.

## 2026-09-01 — decision: disp-интеграция запаркована с пользой (PR #106 draft)

- Решение владельца после 13 кругов приёмки (12 реальных фиксов в ветке):
  два оставшихся ограничения не закрываемы со стороны devtools —
  (1) у disp нет read-only команды с верифицированной фазой (status читает
  pipeline.json мимо integrity anchor; проверяет только мутирующий resume);
  (2) пред-коммит upstream-узлов прячет внешние правки от adopt-external.
- Сделано: PR #106 → draft с описанием ограничений; disputatio#68
  (slug: verified-phase-readonly-command) заведён; REVIEW_LOGIN вынесен
  микро-PR devtools#108 (agent-merge, 4a9dcc7) + @blocked_by:disputatio#68
  на пункт disp-авторинга. disp-бэкенд — экспериментальный opt-in
  (суррогат run --mode develop на master) до upstream-фикса и живого смоука.
- Ремарка ценности: 13 кругов дали 12 честных находок, включая три класса
  «переживи сбой в любом окне» и два обхода чужой integrity-модели —
  терминальное ревью с чтением исходников callee работает как формальный
  верификатор интеграций.

## 2026-09-01 — change: accept-pr — приёмка integration-PR spec-runner одной командой (devtools#109)

- Вариант (а) решения владельца: make accept-pr ARGS='--repo <r> --pr <n>' —
  терминальное ревью → полное ожидание чеков → гарды → DarkFactory-мерж →
  подсказка sync. 4 круга приёмки, 4 major закрыты: пустой rollup = pending
  (гонка свежего push), head пинуется до ревью, mergeability fail-closed
  (UNKNOWN ждётся, мерж только на MERGEABLE), гард «ревью и мерж в один
  репо» (origin чекаута vs слаг). Два минора запаркованы. Agent-merge
  32ac3f4; 479 тестов. Ручной шов после каждого цикла spec-runner закрыт.

## 2026-09-02 07:10 — result: два прогона behaviour-конвейера — dispatcher#229 и disputatio#57 (документная фаза закрыта)

- Прогон 1 (WS-dispatcher-229-7ed609, PF-OWNER-REPO-SELF в plan_fields): 3 круга ревью
  (находки валидные — выдуманные manifest-aliases, поле owner_ref.type→kind), approve,
  бандл влит dispatcher#230 (мерж ai-prosto: S7 отказал по транзитному unknown-rollup,
  после позеленения чеков условия DarkFactory выполнены вручную), S8 зелёный, run
  completed; tasks-спека — draft PR dispatcher#231.
- Прогон 2 (WS-disputatio-57-b6a10d, _changed_lines state-парсер + UnicodeDecodeError):
  2 круга (находка: FR-06 vs NFR-05 — противоречие со старыми безханковыми fixtures;
  решение — миграция fixtures на валидный unified diff разрешена явно), approve,
  S7 смержил САМ (decision=agent, все оси зелёные) — первый полностью агентский мерж
  документ-PR в чужом репо; tasks-спека — draft PR disputatio#70.
- Шероховатости: (1) S8 оставляет .steward/gate_verdicts.jsonl в target-репо → dirty-гард
  task_bridge; (2) пин upstream_hashes бывает в инлайн-YAML-форме {requirements: "…"} —
  sed по двухстрочной форме молча промахнулся, ушёл коммит со stale-пином (пойман, дослан).
- Links: dispatcher#230, dispatcher#231, disputatio#69, disputatio#70; governance/runner.py

## 2026-09-02 12:40 — result: кросс-репный контрактный цикл PF-OWNER-REPO-SELF (канон → перевендор) + снятие долларовых потолков

- TASK-001 (WS-dispatcher-229) дважды падала не по своей вине: (1) локально
  отсутствовали пинованные бинари live-smoke (github-checker/steward/impresario —
  CI ставит их отдельными шагами; поставлены локально), (2) агент корректно
  добавил код в diagnostics.yaml, но это вендоренная копия — integrity поймала
  правку мимо канона. Хореография инициатора issue отработана: «скажите» в
  dispatcher#229 → канонная запись vault#125 (additive minor, manifest 2 хэша) →
  перевендор dispatcher#235 (r3, PINNED c13ed78) + пин tree_sha256 в тесте.
- Долларовые потолки spec-runner сняты (dispatcher#235, disputatio локально):
  работа по подписке, total_cost_usd — нотация API-листпрайса; тормоза от
  runaway — max_retries/timeout/consecutive-failures. Урок budget authorize:
  --task-limit пер-тасковый (позиционный task_id).
- Уроки лейна: review-kit читает локальный чекаут — грязное дерево даёт ревью
  ложную фактуру (чистить перед прогоном); вердикт наследуется по отпечатку
  head+diff — обход `--fresh`. Бухгалтерские PR spec-runner сорванных кругов
  (#233, #234) закрыты как шум.
- Links: dispatcher#229/#235, vault#125, devtools#110 (уроки 4-5)

## 2026-09-02 19:30 — result: disputatio#57 закрыт полностью — второй полный цикл конвейера

- WS-disputatio-57 доведён 15/15: TASK-005/006 — реальный TDD (дефект
  header-lookalike эвристики), 7 задач — tdd-waiver/v1 по санкциям владельца
  (одиночная TASK-003, батч 004/007-010, стоячая санкция для 006/012/013),
  TASK-011-015 — сканер/сигнатуры/доки. Все integration-PR (#72-#82) приняты
  accept-pr; ревью-находки на waiver-PR были валидными и укрепили тесты
  (порядок обхода, сохранение экземпляра ошибки, sentinel ast.parse).
- К2 закрыт PR #83 — глубже заявленного: тест на критерий «негодный хвост
  усекается» вскрыл недостижимость fail-closed пути (read_text всего журнала
  ронял читателя сырым UnicodeDecodeError). _read переведён на построчный
  байтовый декод, перехват _seal_tail приведён к конвенции.
- Новые режимы отказа записаны upstream: spec-runner#334 (ws-scoped имена
  red-файлов), #335 (CLI для waive), #336 (markdown-жир вокруг REVIEW_PASSED
  + review_policy: required). Локальные: беспрефиксный .executor-state.db
  ломает tdd-evidence (двойная DB); порядок задач: невлитая задача держит
  claim — следующая red-задача не может стартовать с master.
- dispatcher WS-dispatcher-229 идёт: 9/13 (PR #236-#246 приняты), агент
  стабильно забывает ruff format (2 фикс-коммита) — конфигу нужен lint-хук.
- Links: disputatio#57 (closed), PR disputatio#72-#83, dispatcher#236-#246

## 2026-09-02 22:00 — result: dispatcher#229 закрыт 13/13 — третий полный цикл конвейера; оба прогона дня завершены целиком

- WS-dispatcher-229 доведён: PR #236-#250 приняты accept-pr (ревью-находки —
  2× забытый ruff format, недокрытый BEH-11 → двухскановый архитектурный гард
  «одна классификация repo-owner»: коды только в views/fleet_api, owner_ref
  только в parser/fleet_api/views). Issue закрыт с evidence; conformance-
  фикстура — ход инициатора (vault), заявлено в комментарии закрытия.
- Инфраструктурные фиксы дня: 2ч-зависание раннера на ssh-пуше (git-receive-
  pack держал pipe; ветка доставлена HTTPS, процесс снят) → локальный
  insteadOf https в dispatcher/disputatio закрыл класс; беспрефиксный
  .executor-state.db (пустой) ломал tdd-evidence — удалён; sync-гард требует
  закоммиченный spec/.gitignore (PR #239).
- Ритм конвейера подтверждён: >20 integration/waiver/микро-PR за день, почти
  все приняты accept-pr без ручного вмешательства в мерж; стопы — только
  содержательные (валидные находки ревью, waiver-класс, порядок задач).
- Links: dispatcher#229 (closed), PR dispatcher#236-#250, уроки devtools#110

## 2026-09-02 23:30 — decision: ретроспектива дня → шесть пунктов скриптового лейна (в)

- Разбор ошибок/находок трёх циклов по классам: мои (пайп глотает красноту,
  sed по YAML, конфиг по аналогии, CLI наугад), агентские (правка вендоренной
  копии, 2× забытый формат, markdown-маркер), инструментальные (lite-профиль
  approve, draft-статусы бандла, ревью против полной спеки/локального дерева,
  red-unverifiable нарезка, gate_verdicts в чекауте, беспрефиксная state-DB).
- Кодом лейна (в) — TODO PR #112 (merge 3e22675): accept-pr-materialize-head,
  spec-bridge-approve-conformance, spec-run-preflight, task-bridge-beh-grouping,
  runner-s8-verdicts-cleanup, review-context-increment-wave. Upstream —
  spec-runner#337 (новый); соседям — inbox dispatcher#251 (lint-хук).
  Процессом (без кода): waiver-ритуал, byte-lock порядок задач,
  канон→перевендор, --fresh при повторном ревью.
- Links: devtools#110 (комментарий-итог), devtools PR #112, spec-runner#337,
  dispatcher#251

## 2026-09-03 01:30 — change: лейн (в) — первые три пункта закрыты кодом (PR #113/#114/#115)

- accept-pr (PR #113, 6 кругов): materialize head PR в чекауте цели + гард
  чистого дерева; ревью-эскалации закрыли реальные дыры — исполнение
  scripts/review/ и корневого review-pr.sh из недоверенного PR (harness-гард
  по ЛОКАЛЬНОМУ диффу материализованного head0, не по API — TOCTOU), пин
  base-ветки перед мержем, FETCH_HEAD вместо `origin/<base>`,
  --no-overwrite-ignore на switch.
- runner S8 (PR #114, 3 круга): gate_verdicts.jsonl переезжает в run_dir
  (dirty-гард task_bridge больше не спотыкается); зелёный exit без verdicts —
  fail-closed стоп; pre-clean stale-файла прошлой попытки до запуска гейта.
- spec_run_preflight (PR #115, 10 кругов): `make preflight ARGS='--repo <r>'` —
  конфиг-по-эталону (YAML-парсер, путь = часть требования; круги 2–7 показали,
  что regex = пере-изобретение парсера), insteadOf https, беспрефиксная
  state-DB, live-smoke-env, dirty-tree. pyyaml — прямая зависимость.
- Живые находки при внедрении: (1) ssh-fetch завис на 40 мин в САМОМ devtools —
  insteadOf стоял только у dispatcher/disputatio; поставлен и в devtools;
  (2) у dispatcher лежит НЕпустая spec/.executor-state.db рядом с префиксной —
  судьба у владельца; (3) расхождение dry-run/publish вердиктов review-pr.sh —
  недетерминизм закрыт flow --write-verdict/--use-verdict.
- Links: devtools PR #113, #114, #115; TODO @id:accept-pr-materialize-head,
  runner-s8-verdicts-cleanup, spec-run-preflight

## 2026-09-03 05:30 — result: лейн (в) закрыт целиком — все 6 пунктов ретроспективы реализованы

- Оставшиеся три пункта: волна review-context (шаблон согласован владельцем с
  двумя правками: later-TASK — не находка, только необязательное примечание;
  красный *_red.py — лишь при трёх условиях атрибуции; манифесты несут
  tasks-файл WS как якорь привязки) — devtools#116 / disputatio#84 /
  dispatcher#252 / kapelle#61, approve опубликованы, мерж человеком;
  spec-bridge-approve-conformance (PR #117: конформный frontmatter при
  рождении — spec approve мержит traces и сохраняет пин, штамп статусов
  бандла = mergedBy/mergedAt бандл-PR с перепиновкой цепочки после штампа,
  режим --conform-approve; upstream spec-runner#338 — репо-локальные
  stage-профили); task-bridge-beh-grouping (PR #118: смежные бес-Feature BEH
  одного файла checked_by-цели — одна задача; симуляция на живом WS-57:
  4 задачи вместо 15, все 7 red-unverifiable внутри слитой TASK-001).
- Ревью-лейн дня: находки кругов валидны и укрепляли код (TOCTOU find_pr→
  доставка в открытый PR; повторный approve-штамп) — один транзиент
  «model at capacity» ушёл ретраем.
- Links: devtools PR #116–#118, disputatio#84, dispatcher#252, kapelle#61,
  spec-runner#338, devtools#110 (итоговый комментарий)

## 2026-09-04 07:50 — result: disputatio#65 закрыт 6/6 — четвёртый полный цикл конвейера, первый целиком на новой обвязке

- WS-disputatio-65 (immutable session semantics) доведён: PR #85 (бандл, S7
  агентски) → #86/#87 (tasks-спека: штамп бандла + conform-approve впервые
  вживую) → #90–#95 (6 задач). Ревью каждой доставки — терминальный контур
  с курируемым контекстом; крупные находки закрыты фикс-коммитами (P0
  манифеста, редактирование недоверенных значений, схема снапшотов,
  P9-поверхность), архитектурная (genesis) — пунктом-условием TASK-004 и
  доставлена в нём же с crash/tamper-тестами; TASK-006 — waiver-ритуал
  (санкция владельца, регрессия закрыла непокрытое направление).
- Первый цикл целиком на claude-харнессе (лимиты codex): ревьюер
  scripts/harness/claude-review + авторинг AUTHOR_HARNESS (PR #121/#122);
  первое боевое claude-ревью нашло пропущенный blocker в самом harness-гарде.
- Починки инструментов по ходу: spec-runner#340 (markdown/quote-толерантный
  парсер review-маркеров — 4 боевых попадания класса #336 за два дня,
  включая маркер В КАВЫЧКАХ в собственном промпте) — влит + переустановлен
  оператору; заведены spec-runner#339 (hook-env без префикса/DB),
  spec-runner#341 (auto-fix линта red-файла — попытка сжигалась о 2
  fixable-ошибки, разорвано операторским amend'ом red-коммита);
  disputatio#88 (ws-неймспейс red-файлов WS-57 — второе попадание #334);
  insteadOf https доведён до всех активных клонов (40-мин зависание в
  spec-runner). Гонка push→pull-ref трижды ловилась head-гардом accept-pr.
- Links: disputatio#65 (closed), disputatio PR #85–#95, spec-runner#339/#340/#341,
  devtools PR #119–#122

## 2026-09-05 18:48 — result: design-узел конвейера доставлен в PR #145; бандл WS-spec-runner-367 APPROVED

- Дорожка A: реализация спеки design-узла (влита #142, план #143) завершена SDD-циклом:
  9 задач + финальное ревью ветки (FIX: 2 major) + фикс-волна + scoped re-review (SHIP).
  Терминальное ревью PR #145 — 3 прогона: ложный blocker из-за чтения дерева master-чекаута
  (новая грань devtools#136, задокументирована), настоящий major (fallback абзаца гасил
  deferred-без-reason), затем APPROVED от ai-prosto; 3 minor'а закрыты закалкой design_guard
  без нового круга. 745 passed. Мерж — человек (profiles/ — authority-root).
- Дорожка B: бандл verify-first (spec-runner#367, PR spec-runner#368) прошёл 8 раундов
  терминального ревью (главные дыры: свой класс слов исполнения vs _EXECUTED_WORDS,
  три оси RunOutcome×SelectionProof×ExecutionProof, по-селекторная форма прогона),
  APPROVED на 74e9c61; Copilot-thread про waiver-файлы закрыт фиксом 5d8a854;
  run в waiting_human_merge.
- Links: devtools PR #145, spec-runner PR #368, devtools#136, .superpowers/sdd/2026-09-05-design-node/progress.md

## 2026-09-05 23:37 — result: decomposition-узел реализован — PR #147 (APPROVED, ждёт человеческого мержа)

- План #146: 5 кругов терминального ревью до мержа владельцем; реализация — SDD
  9 задач в worktree devtools-decomposition-node, пер-тасковые ревью с
  мутационными проверками, финальное ревью ветки (opus) SHIP + фикс-волна
  (тесты legacy=4/conform-mismatch, гард forward-рёбер, DSL-предупреждение) +
  re-review CLEAN. Терминальное ревью PR: 1 minor (DSL vs гард порядка
  объявления — синхронизировано фикс-коммитом b78a3d9), APPROVED от ai-prosto.
- 791 passed. verify-DT fail-closed до доставки spec-runner#367
  (@blocked_by-чекбокс в TODO.md). Follow-ups в теле PR (5 шт.).
- Links: devtools PR #147, план docs/superpowers/plans/2026-09-05-decomposition-node.md

## 2026-09-06 04:50 — result: tasks-спека WS-367 (verify-first) — PR spec-runner#369 APPROVED, ждёт человеческого approve

- Конвейер: run e03a72 → completed; мост доставил tasks-спеку (--legacy-bundle 3).
- 8 кругов терминального ревью; по пути закрыты 3 генераторных бага devtools
  (класс #123, PR #148/#149/#150, все агентски смержены ai-prosto): BEH-id с
  буквенным суффиксом (BEH-18a молча выпадал), Traces to/Depends on одной
  скобкой (парсер терял трассируемость 10/14 задач), голый ISO в generated_at.
- Секция «Решения открытых вопросов (уровень design)» написана и выдержала
  4 круга ревью: Q-04 detached-worktree; Q-07 — оси по потребителям
  (пред-прогонное решение: происхождение+config+состав+tree-hash; red-гейт:
  только происхождение); Q-09 — таблица пост-прогонной тройки + шесть
  пред-прогонных случаев; потолки: 900 с/селектор + бюджет группы 1800 с;
  порядок: BEH-24 выделен в TASK-015 перед green-only (008), BEH-25/28/29
  после; записи режима (литерал в _judge_red_commit) — в объёме TASK-015;
  окно claims объявлено.
- Links: spec-runner PR #369 (head 07c1b16), devtools PR #148 #149 #150

## 2026-09-07 04:05 — result: WS-spec-runner-367 (verify-first) ДОСТАВЛЕН ЦЕЛИКОМ; verify-DT разблокированы в мосте

- Исполнение workstream'а: 15/15 задач через конвейер run→accept→merge→sync
  (PR spec-runner#371–#387, 15 циклов). Стопы и лечение: 2 red-стопа (retry
  со свежим агентом), 1 review-not_run ×2 (третий retry), max_consecutive
  (spec-runner retry), конфликт статуса при merge (ручной резолв), красный
  CI-lint на red-артефактах ×2 (format-коммиты).
- Фикс-раунды приёмки по существу: #372 парсер Verifies (6 кругов, терминальный
  дизайн: блок до структурной границы, verbatim-элементы); #375 ядро live_verify
  (4 круга: словарь адаптера, FR-14, флаг-политика, групповой бюджет 1800с);
  #378 evidence (запись в исполнительный путь, green-only reuse); #380 гейты
  (5 кругов: re-verify кандидата, парность claims#214, терминальность,
  verify_first+auto_commit:false = несовместимость до трат); #381 claims release
  state-derived; #383 freeze (дверь release для verify-freeze, reuse не
  rebaseline); #384 (green-only метка при confirmed red, enum схемы +verify);
  #386 честность доков (2-3 replay, не «ровно один»); #387 честный замер
  (RED-дельта, не структурный 0.0).
- Закрытие: issue spec-runner#367 закрыт; devtools PR #152 (2 круга, APPROVED,
  мерж ai-prosto): мост рендерит verify-DT с Mode: verify_first + Verifies
  (формат запинован регексами парсера), отказ на verify без целей; чекбокс
  @id:decomposition-verify-first-unblock закрыт.
- Links: spec-runner PR #371–#387, devtools PR #152, issue spec-runner#367

## 2026-09-07 10:26 — change: acceptance-узел конвейера реализован (SDD, PR #155)

- SDD-прогон плана 2026-09-07-acceptance-node (9 задач): узел acceptance (qa) в profiles/team-exp.yaml, DSL авторинга + Priority у NFR, новый governance/acceptance_guard.py (AC-грамматика + Must-покрытие FR/NFR), шаг author-acceptance + S4-гарды (3 ребра, GC-AC-COVERAGE), 6-узловой _BUNDLE_DAG + _BUNDLE_DAG_LEGACY5 + --legacy-bundle=3|4|5, DT-путь по составу DAG, секция AC в tasks-спеке, сквозной смоук. 833 passed.
- Финальное ревью (opus) поймало Important: _parse_requirements без границ блока всасывал Priority из чужой секции — обход Must-гейта; исправлено фикс-волной с регрессионным тестом.
- PR #155 открыт; profiles/ — authority-root ⇒ мерж человеком. Терминальное ревью — в процессе.
- Links: docs/superpowers/plans/2026-09-07-acceptance-node.md, governance/acceptance_guard.py

## 2026-09-07 11:33 — change: операторская кнопка spec-loop (PR #156)

- Пункт 3 роадмапа: make spec-loop SUBJECT='…' REPO=… — одна идемпотентная команда ведёт workstream через 6-узловой конвейер с остановкой на человеческих границах (мерж бандл-PR, approve tasks-спеки). merge-authority жёстко human; повтор ищет прогон по (repo, subject); неоднозначности fail-closed.
- task_bridge.deliver_for_run: durable reconciliation доставки (write-ahead op tasks-deliver + поиск PR по ветке; повтор не создаёт PR заново).
- Дизайн утверждён владельцем с 4 поправками (bounded-путь, без спеки). Терминальное ревью: approve + 1 major (medium) и 2 minor — закрыты фикс-коммитами (find_pr any_state: вмерженный tasks-PR принимается реконсиляцией, закрытый без мержа — отказ); 4 минора Copilot закрыты. PR #156 влит агентски от ai-prosto (разрешение владельца), master 3e6ba6f, 869 passed.
- Links: governance/spec_loop.py, governance/task_bridge.py, Makefile

## 2026-09-07 14:04 — result: первый живой прогон spec-loop — полный цикл на kapelle

- make spec-loop прогнал workstream real-llm-provider-adapters-20260907 (kapelle#50) через весь 6-узловой конвейер: start → авторинг → S4-гейты → 4 круга встроенного ревью (2+3+1 major исправлены правками бандла с репином) → мерж бандла человеком (kapelle#76) → resume+S8 → идемпотентный deliver → tasks-спека PR-ом (kapelle#77). Стоп на approve спеки — последняя человеческая граница.
- Предусловие: профиль kapelle поднят 4→6 узлов (kapelle#75). Кнопка вела себя строго по дизайну: fail-closed стопы, никаких авто-мержей, повтор одной команды на каждом шаге.
- Links: kapelle#75, kapelle#76, kapelle#77, governance/spec_loop.py

## 2026-09-07 14:30 — result: цикл spec-loop на kapelle закрыт полностью

- Владелец смержил бандл (kapelle#76) и tasks-PR (kapelle#77), выполнил spec approve; conform-approve доставлен PR-ом kapelle#78 (approve опубликован, влит агентски от ai-prosto), ветки вычищены. Workstream real-llm-provider-adapters-20260907 approved и готов к исполнению spec-runner'ом.
- Ревью #78 нашло 2 генераторных минора моста — заведены devtools#157 (approved_at из approve бандла) и devtools#158 (обрезка тела резолюций).
- Links: kapelle#76, kapelle#77, kapelle#78, devtools#157, devtools#158

## 2026-09-08 03:04 — result: workstream real-llm-provider-adapters исполнен spec-runner'ом целиком (10/10)

- Полный цикл «кнопка → бандл → tasks-спека → исполнение»: 10 TDD/verify-задач success, integration-PR kapelle#81–#92 (+#88 селекторный фикс спеки) влиты через accept-pr (терминальное ревью + DarkFactory). Первый боевой verify-DT (TASK-007) исполнен после селекторного фикса.
- 6 инцидентов, все закрыты в корне или обходом с issue: composite lint (kapelle#79), INTERRUPTED-recovery (retry), Verifies-селекторы (kapelle#88, devtools#159, spec-runner#389), офлайн-страж ломал opt-in smoke (#90 фикс-волна), авто-чекер BEH-28 вопреки MUST NOT дизайна (удалён, #92), id вне вендоренной схемы в доке и smoke-тесте (#92 круг 2).
- Стоимость: agent_calls ≈$26.2 (кап поднят владельцем 30→60 после стопа $30.69 на 5 задачах по счётчику runner'а). spec-runner tool стоит dev-версией из локального master (verify_first не зарелижен — нужен ≥2.36).
- Links: kapelle#81..#92, devtools#157/#158/#159, spec-runner#388/#389, docs/live-provider-run.md (kapelle)

## 2026-09-08 04:53 — change: hardening-волна 1 моста влита (PR #160, закрыты #157/#158)

- generated_at теперь с явным офсетом (боевой случай несравнимости с approved_at); секция резолюций tasks-спеки несёт тело Q-блока целиком (parse_design_resolution_bodies + рендер verbatim — таблицы/списки больше не теряются). TDD, 876 passed, агентский мерж от ai-prosto.
- План оздоровления (порядок владельца): дальше spec-runner#389 (file-scope target, НЕ расширение Selector) → релиз ≥2.36 → devtools#159 → spec-runner#388 → спека 2.
- Links: devtools#160, devtools#157, devtools#158

## 2026-09-08 08:58 — result: цикл кнопки №2 закрыт — spec-runner#389 доведён до approved tasks-спеки

- make spec-loop на spec-runner (шаг 2 плана оздоровления): профиль 4→6 (PR #390, human-мерж), бандл verify-first-file-scope-group-targets-20260908 (PR #391, 2 круга встроенного ревью — вдвое меньше kapelle), tasks-спека (PR #392 + approve владельца v2), conform (PR #393, агентский мерж). Ruling владельца закреплён: file-scope target — отдельный тип, НЕ расширение Selector.
- Секция резолюций спеки уже с полными телами Q-блоков (hardening #158 в деле). Инцидент: удалил ветку #392 до сверки мержа — GitHub закрыл PR; восстановлено из sha без потерь, чистка теперь только после подтверждённого MERGED.
- Links: spec-runner#390..#393, spec-runner#389, devtools#160

## 2026-09-09 08:14 — change: поле verifies доставлено (PR #161), supersede вынесен отдельным заходом

- Структурное поле verifies у type: verify DT — группа наблюдения отдельно от владения (checked_by остаётся редактирующим владением): парсер обеих блочных форм и инлайна, находки формы, граф-инвариант «владелец наблюдаемого файла в замыкании depends_on», рендер **Verifies:** объединением checked_by+verifies, промпт авторинга согласован. 905 passed.
- Цена: ~15 кругов терминального ревью. Урок: половина находок — следствие моих поспешных ruling'ов (дедуп по пути схлопывал селекторы; проверка существования verifies-путей в deliver противоречила порядку создания файлов; строгая форма списка с обязательным отступом и обрывом на пустой строке). Формулировать грамматику полей строго и сразу, проверяя против фактических форм авторинга.
- supersede (переиздание tasks-спеки после correction'а) вынесен отдельным заходом: не сошёлся с моделью «одна ветка/один PR/штамп в PR» за три круга.
- Остаточные миноры парсера — devtools#162. Смежное: spec-runner#402.
- Links: devtools#161, devtools#162, spec-runner#402

## 2026-09-13 14:37 — decision: план развития пайплайна «интервью → реализация» принят; пункты E0.6/E1 заведены

- Заметка `authored/notes/2026-09-13-pipeline-interview-to-implementation-plan.md` прошла три предложенных ревизии в vault PR #126 (мерж владельцем 67cdfcf): разведены runtime-компоненты R1–R5 (два маршрута) и roadmap-этапы E0–E4; инвариант «результат, нужный для продолжения/проверки/воспроизведения прогона, не существует только на машине оператора»; снапшот PP content-addressed; транскрипт необязателен после проверенного брифа (окно до брифа — принятое исключение); дефолт однорепозиторного продукта; матрица артефактов. Ревизия 4 с шестью решениями владельца принята по vault#127 и влита vault PR #128 (мерж ab85cb5).
- devtools PR #210 (agent-merge ai-prosto, master 0d679ec): пункты `durable-governance-state-ledger`, `s8-verdict-in-tasks-pr` (после #201), `spec-loop-brief-input` (после fidelity-волны и #201). Три круга терминального ревью — четыре minor'а по фактическим путям и механизмам приняты (s8-gate-verdicts.jsonl в леджере, ws-id с датой восстанавливается по префиксу ветки, gate_check вендорится кодом, т.к. discovery-toolkit package=false). Первый plan-check поймал PF-BLOCKER-STALE: fail-honest supersede уже закрыт #209.
- Inbox spec-runner#478 (slug executor-state-inventory): инвентаризация runtime-state исполнителя.
- Links: vault PR #126/#128, vault#127, devtools#210, spec-runner#478, devtools/TODO.md (раздел «План развития пайплайна»)

## 2026-09-13 16:40 — result: PR #206 (fidelity ревью: exact head PR) — терминальное ревью из доверенного дерева, мерж человеком

- Харнесс-PR (правит review-pr.sh, `_HARNESS_PREFIXES`): ревью выполнено драйвером из worktree origin/master (23bba42) с FLEET_ROOT на worktree head 859b5a1 — код из проверяемого дерева не исполнялся (scripts/review/ в PR не тронуты). Вердикт approve + 2 minor (конфиги харнесса из cwd PR-head; пин prompt/schema через env у старых вендоренных китов), опубликован от ai-prosto. Мерж — владелец (0d7078f), merged_by человеческий по правилу. Закрыты devtools#136, #166; пункт review-evidence-fidelity-wave.
- Побочно: prograph-vault#127 обработан (PR #128 влит, ревизия 4 плана accepted), inbox discovery#43 — решение по соло-режиму; PR #212 закрыл E0.6a.
- Links: devtools#206, prograph-vault#128, discovery#43

## 2026-09-15 — result: devtools#223 закрыт — пин базы вердикта по живой верхушке (D1), спека accepted

- Дизайн (PR #234, 4 круга ревью: две ложные посылки сняты — вход ревьюера якорен на merge-base; повтор приёмки уже наследует вердикт по head+fp бесплатно, платным круг делал update-branch) → решения владельца (PR #235: D1 сейчас, D2 не делать до наблюдаемой гонки, D3 без auto-update-branch, D4 не вводить; объём терминального ревью зафиксирован в CLAUDE.md) → код D1 (PR #236, мерж человеком 9b58582: merge-pr.sh сверяет --expect-base, compare гварда 4 и журнал с git/ref/heads/<base>, fail-closed; accept_pr диагностика кода 5 по remote_branch_head_fact; RED→GREEN 7 тестов, 1613 passed, negative control на compare).
- Харнесс-PR ревьюился драйвером из worktree origin/master с FLEET_ROOT на head-worktree. Остаток — ABSENT верхушки в диагностике (issue заведён). Урок: three-dot compare — диф деревьев, «надмножество от старого снимка» ложно.
- Links: devtools#223, devtools#234, devtools#235, devtools#236

## 2026-09-15 — change: батч правдивости governance-контракта — #182/#185/#195/#237 влиты (PR #239), #184 ждёт человеческого мержа (PR #240)

- PR #239 (agent-merge 61e1e2f): гвард слепых зон §I5 судит каждое совпадение и прощает по группе счёта/зоны (мутанты «первое совпадение» и «весь спан» краснят; второй мутант выживал на первой фикстуре — свойство ненаблюдаемо на снятой основе, фикстура переведена на действующую); accept_pr говорит ровно известное (коды 2/3/4 — «не проверялось», ABSENT — «ветки нет», совпавшие пины — «совпадают с проверенными»); §I2 — граница сверки блоба терминального узла. 1618 passed.
- PR #240 (approve ai-prosto из доверенного дерева, харнесс; мерж человеком 592393b): merge-pr.sh — правило и defense-in-depth, не security boundary, записано в шапке, CLAUDE.md и Ops.merge. #184 закрыт; пункт governance-contract-truth-batch закрыт (PR #241).
- Links: devtools#239, devtools#240, devtools#182, #185, #195, #237, #184

## 2026-09-15 — change: остатки document-pipeline авторинга behaviour-узла — devtools#204 закрыт (PR #242)

- Чеклист doc: B0 из `_AUTHOR_DSL["behaviour-spec"]` (одно место с промптом; S4 — единственный судья DSL). Self-target анкер: XDG_STATE_HOME/devtools/disp-anchors/<run_id>, пин в RunState.disp_anchor_dir. Слаг пинуется в RunState.disp_slug; retry ровно один путь — `disp pipeline resume` только для начатого этим прогоном пайплайна (по `_check_pipeline_dir_absent` соседа); чужой каталог — стоп; ручной выход из пина — файл без каталога принимается как есть; `resume` на терминальном пайплайне у соседа отказывает (PipelineNotResumable).
- Пять кругов ревью (все minor, все приняты кроме последнего — вынесен follow-up PR канонизации анкера), 9 тестов, 6 мутантов. Чекбокс TODO открыт до живого прогона (E2).
- Links: devtools#242, devtools#204

## 2026-09-15 — result: E2 — стадия Need вызывается прогоном (spec-loop --need, customer) — реализована (PR #246)

- Дизайн по секциям с владельцем (D1–D6), спека #244 (accepted после 3 ревизий, ревизия 5 с кодом), план #245 (11 задач, 4 круга ревью плана). Исполнение — SDD: свежий субагент на задачу (haiku для транскрипции, sonnet для раннера/spec-loop), ревью каждой задачи, финальное ревью ветки на opus, одна фикс-волна (README/Makefile, UnicodeDecodeError, мёртвая ветка, 88 колонок, smoke-код answer). 1704 passed; opt-in smoke с настоящим discovery: 19 итераций банка, код 0, рендер детерминирован. Терминальное ревью #246 — approve, два minor → issue-остаток.
- Уроки процесса: venv worktree без группы governance молча пропускает 152 теста раннера (сверять collected); субагенты уходят в фоновый pytest и ждут уведомление, которого нет — запрещать фон в диспатче; из worktree `DEVTOOLS_ROOT.parent/discovery` не резолвится — симлинк на стенде; фоновое ревью убито системой по памяти — foreground.
- Открыто: живая приёмка §9 с реальным стейкхолдером (чекбокс spec-loop-need-stage); engineer-маршрут ждёт discovery#49.
- Links: devtools#244, #245, #246, discovery#49

## 2026-09-16 05:10 — result: живая приёмка E2 (spec-loop --need) на spec-runner#480 — стадия Need прошла, S6 остановлен владельцем

- Прогон `durable-continuation-checkpoint-evidence-20260915-4c2a3e`: интервью 19 ответов (код 0), бриф, E1-путь, disp-авторинг behaviour-узла (2 раунда), S4, bundle-PR spec-runner#522. Три дефекта devtools найдены живьём и влиты: #248 (конфиг disp adapter/model/limits), #249 (коммит бандла до первого `run` disp), #250 (потолки дифа кита `--max-diff-bytes`/env, харнесс — мерж владельца).
- S6: семь кругов терминального ревью бандла (6.3k строк), major-зоны сменялись (сайты/lock → closure → open calls); остановка по решению владельца 2026-09-16, `waiting_human_merge` не достигнут. Evidence — devtools #251; чекбокс `behaviour-document-runner-residuals` закрыт, `spec-loop-need-stage` — решение владельца.
- Links: devtools `docs/evidence/2026-09-15-need-stage-live-run.md`, спека `docs/superpowers/specs/2026-09-15-need-stage-design.md` §9, spec-runner#522, devtools#248/#249/#250/#251
