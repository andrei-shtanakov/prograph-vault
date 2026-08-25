---
title: dispatcher — activity journal
type: journal
source: kb-save
project: dispatcher
updated: 2026-08-02
---

# dispatcher — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.

## 2026-08-02 19:07 — result: WS-005 governance-бандл закрыт насквозь (WS-B + WS-C за один день)

- Capability «достоверная read-only панель governance-бандла» доведена до конца:
  WS-A (steward PR #33, контракт gate-verdicts/v1 + emitter) → WS-B (dispatcher
  PR #107, inbox #106) → WS-C (dispatcher PR #109, inbox #108). Оба inbox-issue
  прошли полный цикл ADR-ECO-006 (принятие пунктом TODO.md → PR → ревью → мерж
  пользователем → закрытие issue со ссылкой на PR) и закрыты completed.
- WS-B: вендор канона steward @ 4836345 в contracts/steward-gate-verdicts/v1
  (одновходовый скрипт scripts/revendor_steward_gate_verdicts.sh + runbook
  docs/revendor-steward-gate-verdicts.md); две раздельные гарантии по правилу
  PR #99 — offline copy-integrity (tests/test_gate_verdicts_vendor.py, PR-гейт,
  не скипается) и scheduled drift-джоб (upstream-drift.yml, репортёр получил
  --canon-probe: канон steward без manifest.json, роль пробы — SCHEMA.json).
  Collector dispatcher/core/governance.py: классификация бандла в 6 состояний
  (no-data → unreadable → stale → unresolvable → blocked → pass, приоритет
  первого совпадения), fail-closed (NFR-02): нет файла → no-data через саму
  попытку чтения (без TOCTOU), любая ошибка чтения/парсинга и неизвестные
  git-факты — никогда не pass. ARCH-C1 (не импортирует steward) закреплён
  структурным тестом; ARCH-C3 — по построению (только классификация,
  единственный subprocess — локальный git).
- WS-C: GET /api/projects/{name}/governance через read_api-фасад (DESIGN-701);
  ARCH-C4 — панель потребляет только collect_governance; BEH-09/ARCH-C2 —
  route-enumeration тест (governance-поверхность только GET/HEAD). Веб-панель
  renderGovernance(): «✅» может появиться только у pass (M-01), блокер бандла
  читается с одного экрана (M-02), provenance из header (FR-05); 7 кейсов в
  Node-harness tests/web/governance_harness.js (вкл. XSS-экранирование).
  Сквозной smoke: scripts/install_pinned_steward.sh ставит настоящий gate-check
  на пине из вендоренного манифеста (второй копии пина нет), smoke детерминирован
  на пине (blocked: GC-TRACE-EMPTY + GC-STALE-UNPINNED); в CI рядом с пиненным
  github-checker, падает-не-скипается (дисциплина PR #98).
- Ревью: PR #107 — валидное замечание Copilot (вводящая в заблуждение причина
  «unsupported schema_version None») исправлено с регрессионным тестом, невалидное
  (мутабельные дефолты pydantic) отклонено с обоснованием; PR #109 — без замечаний.
  Полный сьют после мержа: 772 passed, 0 skipped.
- Links: dispatcher PR #107, #109; issues #106, #108; steward PR #33 @ 4836345;
  spec: steward/workstreams/WS-005-gate-verdicts/spec/; TODO.md
  @id:ws005-governance-collector, @id:ws005-governance-panel.

## 2026-08-13 10:14 — change: product-proposal-parity shipped (PR #138)

- gate_waiting/needs_human стали видимы на всех поверхностях: MCP-тул
  `product_proposals` (пин whitelist 15→16, ToolError со стабильным JSON
  `code`), секции в TUI ProjectDetailScreen (через read_api, 404-семейства
  скрывают, прочие ошибки — fail-loud), VSCode formatting-only секция в
  onboarding-доке (независимые запросы + generation guard). Закрыт последний
  хвост inbox #129/#136; issue #136 закрыт completed.
- Правило нулевых состояний закреплено кросс-поверхностно (web приведён к
  нему же): уверенный «0 gates/loops waiting» только при все-ok бандлах и
  без report-level diagnostics — иначе classification suppressed/incomplete.
- Links: dispatcher PR #138; dispatcher/mcp_server.py, dispatcher/tui/detail.py,
  vscode-ext/src/productProposals.ts, dispatcher/server/static/index.html;
  TODO.md @id:product-proposal-parity [x].

## 2026-08-16 13:10 — change: принят inbox #147 (maestro-per-project-run-dbs), PR #148

- Maestro-коллектор dispatcher перечисляет per-project run DBs
  (~/.maestro/projects/<host>/<owner>/<repo>/runs/<id>/state.db, включая
  двухсегментный _local) вместо одного legacy-пути; продюсерская сторона уже
  приземлилась (maestro a4caef0).
- Fail-closed статусы ранов: без терминальной записи — interrupted, никогда
  «running»; running только по свидетельству orchestrate.holder + живой pid
  (ужесточение против holder-only resolve_runs maestro); нечитаемая БД /
  отсутствующий run row — unreadable, legacy-файл помечен legacy.
- Новое аддитивное поле ProjectSnapshot.runs; конфиг-ключ maestro_home
  (дефолт — родитель maestro_db). Рендер runs-панели на поверхностях —
  follow-up @id:maestro-runs-panel-parity.
- Links: dispatcher PR #148; dispatcher/docs/superpowers/specs/2026-08-16-maestro-per-project-run-dbs-design.md;
  dispatcher/core/collectors/maestro.py; maestro/docs/superpowers/specs/2026-08-15-maestro-state-layout-design.md

## 2026-08-16 13:50 — change: runs-панель на всех поверхностях (maestro-runs-panel-parity), PR #149

- ProjectSnapshot.runs отрендерен на web (#runs-панель в detail, fail-loud,
  race-guard), TUI (секция orchestration runs) и VSCode (независимый fetch +
  src/runs.ts); MCP — осознанно без нового тула (снапшот уже в туле project).
- Кросс-поверхностные пины: идентичные слова бейджей; незнакомый статус —
  «✖ <status>» вербатим; zero-state — чистый ноль скрывает секцию, warning с
  префиксом run /runs  открывает как «unknown, not zero» (префикс запинован
  тестом). Core-hardening: is_dir()-гарды убраны из енумерирования — stat-ошибка
  теперь warning, не молчаливый ноль (замечание Copilot).
- Links: dispatcher PR #149; spec §7a
  docs/superpowers/specs/2026-08-16-maestro-per-project-run-dbs-design.md;
  tests/web/runs_harness.js; vscode-ext/src/runs.ts

## 2026-08-16 16:44 — decision: спека фазы 2 benchmark run-status (первый хранимый секрет), PR #150

- Спека atp-benchmark-runs-phase2: dispatcher.toml несёт только ПУТЬ
  ([benchmarks].token_file; инлайн-токен = load-time error); файл читается
  per-request, permission-гейт mode&0o077==0, секретность запинована
  канарейка-тестом по всем состояниям сервиса.
- Run-id — ручной ввод (прецедент merge-gate #93), листинга у продюсера нет;
  апгрейд-пути записаны, не взяты. Токен-гейтед fetch только по клику
  (прецедент pr-detail) — секрет не ездит в фоновом цикле, NFR-02 не тронут.
- Продюсерские факты сверены с atp-platform @ da3a264: score_semantics/
  score_components уже в RunStatusResponse (заметка фазы 1 устарела —
  вычеркнута в TODO); осознанный 404 на чужой ран → в UI «not found — or not
  owned by this token». Цепочка: PR-1 спека → PR-2 re-vendor+core → PR-3 web.
- Links: dispatcher PR #150;
  docs/superpowers/specs/2026-08-16-atp-benchmark-run-status-design.md

## 2026-08-16 17:11 — change: benchmark run-status PR-2 (re-vendor + core), PR #151

- Ре-вендор atp-benchmark-api на том же пине da3a264: +GET /runs/{id}/status,
  prune переносит securitySchemes (и падает громко на неопределённой схеме);
  две authored-фикстуры run-status, provenance в PINNED.txt.
- Первый хранимый секрет реализован по спеке: token_file-путь (инлайн-токен —
  ошибка загрузки), чтение per-request, lstat+S_ISREG (симлинк — reject),
  mode&0o077==0, rstrip-only парс (ведущий пробел — reject). Канарейка-тест
  по всем состояниям + проверка, что Bearer реально нёс токен.
- Классификация §5: unauthorized/not_found («not found, or not owned by this
  token»)/unavailable/unreadable/ok + 5 config/token-состояний; статус
  продюсера — вербатим. Отравленный fetcher пинует: фоновый цикл не трогает
  токен-гейтед путь. Маршрут GET /api/benchmarks/runs/{run_id}; MCP-тула нет.
- Ревью Copilot: 3 замечания, все валидные, исправлены. Осталось: PR-3 web.
- Links: dispatcher PR #151; spec 2026-08-16-atp-benchmark-run-status-design.md

## 2026-08-16 17:25 — change: benchmark run-status PR-3 (web-панель), PR #152 — фаза 2 закрыта цепочкой

- Run-status row в секции Benchmarks: ручной ввод run-id, клик-driven fetch,
  formatting-only (серверные формулировки not_found/token_* — вербатим),
  in-flight lock + generation guard, fail-loud; нулевого состояния нет.
- Node-харнес run_status_harness.js (8 кейсов; по ревью Copilot второй клик
  теперь реально диспатчится во время полёта); live-smoke ранбук расширен
  фазой 2 (chmod-644 отказ вживую, grep токена по странице/отчёту/логам).
- TODO @id:atp-benchmark-runs-phase2 закрыт: #150 спека → #151 core → #152 web.
- Links: dispatcher PR #152; docs/atp-benchmark-live-smoke.md (Phase 2)

## 2026-08-16 17:51 — change: Benchmarks-паритет TUI/VSCode/MCP, PR #153

- Тонкие рендереры над read_api.benchmarks (+start_fetch passthrough):
  TUI-вкладка (hide_tab на unconfigured), VSCode view dispatcherBenchmarks
  (when-контекст, чистые узлы в model.ts под vitest, offline ≠ unconfigured,
  контекст стартует TRUE), MCP-тул benchmarks (whitelist 16→17).
- Осознанное расхождение с no-fetch паттерном sync_status: kick-and-wait
  одного троттленного read-only GET публичной поверхности (in-memory кэш
  per-process); MCP-сервис без token_file по построению + пин отравленным
  run_status_fetcher.
- Zero-state правило запиновано на каждой поверхности; по ревью Copilot
  закрыты: хвостовое двоеточие (все 3 рендерера), missing-leaderboard-entry
  как unknown (TUI + pre-existing щель web), init контекста.
- TODO @id:atp-benchmark-view-parity закрыт — тема atp-benchmark-view
  (inbox #139) полностью исчерпана: #143-#145, #150-#152, #153.
- Links: dispatcher PR #153

## 2026-08-17 12:10 — change: принят inbox #154 — qg4_backlog wait (фаза 3 gate_waiting), PR #155

- Принят inbox-issue #154 от impresario (слаг product-proposal-qg4-backlog-wait,
  без переименования): read-only ожидание QG-4 над текущей версией RankedBacklog —
  identity (backlog_id, version), любой исход QG-4 гасит, selectable = new|under_review.
- Ре-пин ВСЕХ impresario-контрактов @ a9d11fa: теперь 5 директорий под одним пином
  (добавлены ranked-backlog/v1 и loop-resume-decision/v1).
- Попутный фикс: живой pp-101 получил decisions/lrd-001.yaml (loop-resume-decision) —
  правило фазы 1 роняло бандл в unknown; LRD-записи теперь распознаются и игнорируются.
- Links: dispatcher PR #155; spec docs/superpowers/specs/2026-08-17-qg4-backlog-wait-design.md;
  core dispatcher/core/product_proposals.py; TODO id product-proposal-qg4-backlog-wait
