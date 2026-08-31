---
title: devtools — activity journal
type: journal
source: kb-save
project: devtools
updated: 2026-08-31
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
